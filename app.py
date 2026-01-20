from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import asyncio
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from llama_index.llms.openai_like import OpenAILike
import queue
import threading
import sys
import io
from contextlib import redirect_stdout, redirect_stderr

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'droidrun-ux-tester-secret'

# Global queues for SSE
progress_queue = queue.Queue()
logs_queue = queue.Queue()

# Global flag to signal agent stop
agent_stop_flag = threading.Event()
current_exploration_thread = None

class LogCapture:
    """Captures stdout/stderr and sends to SSE"""
    def __init__(self, log_callback, log_type='info'):
        self.log_callback = log_callback
        self.log_type = log_type
        self.buffer = []
    
    def write(self, message):
        if message.strip():  # Only send non-empty messages
            # Clean and format the message
            clean_msg = message.strip()
            self.log_callback(clean_msg, self.log_type)
            # Also write to original stdout for server logs
            if sys.__stdout__ is not None:
                sys.__stdout__.write(message)
        return len(message)
    
    def flush(self):
        pass
    
    def isatty(self):
        return False

def send_log(message, log_type='info'):
    """Send log message to SSE queue"""
    logs_queue.put({
        'message': message,
        'type': log_type,
        'timestamp': datetime.now().strftime("%H:%M:%S")
    })

def send_progress(message, percentage=0):
    """Send progress update to SSE queue"""
    progress_queue.put({
        'message': message,
        'percentage': percentage,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/')
def index():
    """Render main frontend page"""
    return render_template('index.html')


@app.route('/api/run-test', methods=['POST'])
def run_test():
    """Start UX exploration test"""
    global current_exploration_thread, agent_stop_flag
    
    data = request.json
    app_name = data.get('app_name', 'Unknown App')
    category = data.get('category', 'General')
    max_depth = int(data.get('max_depth', 6))
    
    # Clear previous queues
    while not progress_queue.empty():
        progress_queue.get()
    while not logs_queue.empty():
        logs_queue.get()
    
    # Clear stop flag
    agent_stop_flag.clear()
    
    # Start async test in background thread
    thread = threading.Thread(
        target=run_exploration_async,
        args=(app_name, category, max_depth)
    )
    thread.daemon = True
    thread.start()
    
    # Store reference to current thread
    current_exploration_thread = thread
    
    return jsonify({
        'status': 'started',
        'app_name': app_name,
        'category': category,
        'max_depth': max_depth
    })


@app.route('/api/progress')
def progress():
    """SSE endpoint for progress updates"""
    def generate():
        while True:
            try:
                # Get progress update from queue
                update = progress_queue.get(timeout=30)
                yield f"data: {json.dumps(update)}\n\n"
                
                # If analysis is complete, stop streaming
                if update.get('percentage') >= 100:
                    break
            except queue.Empty:
                # Send keepalive
                yield f"data: {json.dumps({'keepalive': True})}\n\n"
    
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )


@app.route('/api/logs')
def logs():
    """SSE endpoint for execution logs"""
    def generate():
        while True:
            try:
                log = logs_queue.get(timeout=30)
                yield f"data: {json.dumps(log)}\n\n"
                
                # Stop if we see completion message
                if 'complete' in log.get('message', '').lower() and log.get('type') == 'success':
                    break
            except queue.Empty:
                yield f"data: {json.dumps({'keepalive': True})}\n\n"
    
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )



@app.route('/api/results')
def get_results():
    """Get analysis results"""
    try:
        # Read analysis results
        with open('ux_analysis_blocks.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'error': 'No results available yet'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stop-agent', methods=['POST'])
def stop_agent():
    """Stop the currently running agent"""
    global agent_stop_flag, current_exploration_thread
    
    try:
        if current_exploration_thread and current_exploration_thread.is_alive():
            # Set the stop flag
            agent_stop_flag.set()
            send_log("⚠️ Stop signal sent to agent", 'warning')
            send_progress("Agent stopping...", -1)
            
            return jsonify({
                'success': True,
                'message': 'Stop signal sent to agent'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No agent currently running'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def run_exploration_async(app_name, category, max_depth):
    """Run the exploration and analysis asynchronously"""
    global agent_stop_flag
    
    try:
        # Import here to avoid circular imports
        from exploration_runner import run_exploration_with_category
        
        send_log(f"🚀 Starting UX exploration for {app_name}...", 'info')
        send_progress(f"Initializing test for {app_name}...", 5)
        
        # Run the exploration with stop flag
        asyncio.run(run_exploration_with_category(
            app_name=app_name,
            category=category,
            max_depth=max_depth,
            progress_callback=send_progress,
            log_callback=send_log,
            stop_flag=agent_stop_flag
        ))
        
        send_log("✅ Test completed successfully!", 'success')
        send_progress("Test completed successfully!", 100)
    
    except KeyboardInterrupt:
        send_log("⚠️ Agent execution stopped by user", 'warning')
        send_progress("Agent stopped by user", -1)
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        send_log(error_msg, 'error')
        send_progress(error_msg, -1)
        print(f"Exploration error: {e}")


if __name__ == '__main__':
    # Ensure templates and static folders exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Run verification before starting server (only in main process, not reloader)
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        # This is the reloader process, skip verification
        pass
    else:
        # This is the main process, run verification once
        print("Running pre-flight checks...")
        try:
            from verify_setup import main as verify_main
            verify_main()
        except SystemExit as e:
            if e.code != 0:
                print("\n❌ Verification failed. Please fix the issues above.")
                sys.exit(1)
    
    print("\n" + "="*60)
    print("🔭 Starting DroidScope UX Tester...")
    print("="*60)
    
    app.run(debug=True, threaded=True, port=5000)
