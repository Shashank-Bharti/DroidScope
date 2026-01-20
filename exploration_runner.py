"""
Exploration runner with category-aware agent and progress tracking
"""
import asyncio
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from llama_index.llms.openai_like import OpenAILike
from droidrun import DroidAgent
from droidrun.config_manager import DroidrunConfig
from utils import load_prompt, format_prompt
from ux_analyzer import UXAnalyzer

load_dotenv()


async def run_exploration_with_category(app_name, category, max_depth, progress_callback, log_callback=None, stop_flag=None):
    """Run exploration with category context and stop capability"""
    
    def log(message, log_type='info'):
        """Helper to send log if callback provided"""
        if log_callback:
            log_callback(message, log_type)
        print(f"[{log_type.upper()}] {message}")
    
    def check_stop():
        """Check if stop was requested"""
        if stop_flag and stop_flag.is_set():
            log("Agent execution stopped by user", 'warning')
            raise KeyboardInterrupt("Agent stopped by user request")
    
    try:
        check_stop()
        log(f"Initializing exploration for {app_name}", 'info')
        progress_callback("Loading exploration parameters...", 15)
        
        log("Loading agent goal template", 'info')
        agent_goal_template = load_prompt('agent_goal')
        agent_goal = format_prompt(agent_goal_template, app_name=app_name, category=category)
        
        # Add depth constraints
        enhanced_goal = f"""{agent_goal}

## EXPLORATION CONSTRAINTS:
- Maximum navigation depth: {max_depth} levels
- Focus on features and flows typical of {category} apps
- Document both positive UX patterns and issues
- Be specific with screen names, tap counts, and locations"""
        
        log(f"Agent goal configured for {category} app with depth={max_depth}", 'success')
        progress_callback(f"Initializing DroidRun agent for {app_name}...", 20)
        
        check_stop()
        
        # Setup LLM and config
        log("Setting up LLM configuration", 'info')
        api_key = os.getenv("API_KEY")
        model = os.getenv("LLM_MODEL", "mistralai/devstral-2512:free")
        api_base = os.getenv("LLM_API_BASE", "https://openrouter.ai/api/v1")
        llm = OpenAILike(
            model=model,
            api_base=api_base,
            api_key=api_key,
            temperature=0.2
        )
        log(f"LLM initialized: {model}", 'success')
        
        check_stop()
        
        log("Creating DroidRun configuration", 'info')
        config = DroidrunConfig()
        config.agent.max_steps = max_depth * 15
        
        log(f"Max steps set to {config.agent.max_steps}", 'info')
        
        check_stop()
        
        progress_callback("Creating exploration agent...", 25)
        log("Creating DroidAgent instance", 'info')
        
        # Create agent
        agent = DroidAgent(
            goal=enhanced_goal,
            config=config,
            llms=llm,
        )
        log("DroidAgent created successfully", 'success')
        
        check_stop()
        
        progress_callback(f"Started UX exploration of {app_name}...", 30)
        log(f"Beginning autonomous exploration (max depth: {max_depth})", 'info')
        log("=" * 60, 'info')
        log("🤖 AGENT EXECUTION - Live Reasoning & Actions", 'info')
        log("=" * 60, 'info')
        
        # Capture agent stdout/stderr but only send on flush or buffer full
        import sys
        from io import StringIO
        
        class BufferedTeeOutput:
            """Buffers output and sends in larger chunks to prevent fragmentation"""
            def __init__(self, original, log_callback, log_type='agent', buffer_size=2048):
                self.original = original
                self.log_callback = log_callback
                self.log_type = log_type
                self.buffer = StringIO()
                self.output_buffer = []
                self.buffer_size = buffer_size
                self.total_chars = 0
            
            def write(self, data):
                if not data:
                    return
                
                # Always write to original
                self.original.write(data)
                # Store in buffer
                self.buffer.write(data)
                self.output_buffer.append(data)
                self.total_chars += len(data)
                
                # Only send to frontend when buffer is large enough or we hit newlines with enough content
                if self.log_callback and self.total_chars >= self.buffer_size:
                    self._flush_buffer()
            
            def _flush_buffer(self):
                """Internal flush of accumulated output"""
                if not self.output_buffer:
                    return
                    
                # Combine all buffered output
                combined = ''.join(self.output_buffer)
                
                # Split into lines and send non-empty ones
                lines = combined.split('\n')
                non_empty_lines = [line for line in lines if line.strip()]
                
                if non_empty_lines and self.log_callback:
                    # Send as batched message
                    self.log_callback('\n'.join(non_empty_lines), self.log_type)
                
                # Clear the output buffer
                self.output_buffer = []
                self.total_chars = 0
            
            def flush(self):
                """Explicit flush - send everything immediately"""
                self.original.flush()
                self._flush_buffer()
            
            def getvalue(self):
                return self.buffer.getvalue()
        
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        
        # Buffer stdout with 2KB chunks, stderr immediately
        tee_stdout = BufferedTeeOutput(original_stdout, log_callback, 'agent', buffer_size=2048)
        tee_stderr = BufferedTeeOutput(original_stderr, log_callback, 'warning', buffer_size=512)
        
        sys.stdout = tee_stdout
        sys.stderr = tee_stderr
        
        try:
            # Run exploration - logs will stream in larger batches
            log("⏳ Agent analyzing app structure...", 'info')
            result = await agent.run()
            
            # Flush any remaining output
            sys.stdout.flush()
            sys.stderr.flush()
            
            # Restore stdout/stderr
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            
            log("=" * 60, 'success')
            log("✅ AGENT EXECUTION COMPLETE", 'success')
            log("=" * 60, 'success')
            log("Agent.run() completed", 'success')
            
        except Exception as agent_error:
            # Restore stdout/stderr on error
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            
            log(f"Agent error: {str(agent_error)}", 'error')
            raise agent_error
        
        progress_callback("Exploration complete. Processing results...", 60)
        log("Processing exploration results", 'info')
        
        # Save results
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        output_lines = []
        
        success_status = getattr(result, 'success', None)
        log(f"Exploration success status: {success_status}", 'success' if success_status else 'warning')
        
        output_lines.append(f"Timestamp: {timestamp}")
        output_lines.append(f"App: {app_name}")
        output_lines.append(f"Category: {category}")
        output_lines.append(f"Max Depth: {max_depth}")
        output_lines.append(f"Success: {success_status}")
        output_lines.append("-" * 50)
        
        if hasattr(result, 'final_answer') and result.final_answer:
            log("Final answer captured from agent", 'success')
            output_lines.append(f"Final Answer:\n{result.final_answer}")
            output_lines.append("-" * 50)
        
        if hasattr(result, 'structured_output') and result.structured_output:
            try:
                log("Serializing structured output", 'info')
                structured_json = result.structured_output.model_dump_json(indent=2)
                output_lines.append(f"Structured Output:\n{structured_json}")
                
                with open("exploration_output.json", "w", encoding="utf-8") as json_file:
                    json_file.write(structured_json)
                log("Structured output saved: exploration_output.json", 'success')
                output_lines.append("-" * 50)
                output_lines.append("Structured output saved to: exploration_output.json")
            except Exception as e:
                log(f"Error serializing structured output: {str(e)}", 'error')
                output_lines.append(f"Error serializing structured output: {str(e)}")
        
        if hasattr(result, 'reason') and result.reason:
            output_lines.append(f"Reason: {result.reason}")
        
        output_text = "\n".join(output_lines)
        with open("agent_result.txt", "w", encoding="utf-8") as txt_file:
            txt_file.write(output_text)
        log("Results saved: agent_result.txt", 'success')
        
        progress_callback("Results saved. Starting UX analysis...", 70)
        
        # Run UX analysis
        if success_status:
            log("Starting UX analysis pipeline", 'info')
            analyzer = UXAnalyzer(api_key=api_key)
            analyzer.run_analysis_for_web(
                report_path="agent_result.txt",
                category=category,
                progress_callback=progress_callback,
                log_callback=log
            )
        else:
            error_reason = result.reason if hasattr(result, 'reason') else 'Unknown error'
            log(f"Exploration failed: {error_reason}", 'error')
            progress_callback(f"Exploration failed: {error_reason}", -1)
            
    except Exception as e:
        log(f"Critical error: {str(e)}", 'error')
        progress_callback(f"Error during exploration: {str(e)}", -1)
        raise
