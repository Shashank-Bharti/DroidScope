import os
import json
from datetime import datetime
from llama_index.llms.openai_like import OpenAILike
from dotenv import load_dotenv
from utils import load_and_format_prompt

load_dotenv()


class UXAnalyzer:
    def __init__(self, api_key=None):
        """Initialize the UX Analyzer with OpenRouter LLM"""
        self.api_key = api_key or os.getenv("API_KEY")
        model = os.getenv("LLM_MODEL", "mistralai/devstral-2512:free")
        api_base = os.getenv("LLM_API_BASE", "https://openrouter.ai/api/v1")
        
        # Use a free model from OpenRouter for analysis
        self.llm = OpenAILike(
            model=model,
            api_base=api_base,
            api_key=self.api_key,
            temperature=0.3
        )
    
    def read_report(self, report_path="agent_result.txt"):
        """Read the generated UX exploration report"""
        try:
            if not os.path.exists(report_path):
                print(f"Report file not found: {report_path}")
                return None
            
            with open(report_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            print(f"✓ Report loaded from {report_path}")
            return content
        except Exception as e:
            print(f"Error reading report: {str(e)}")
            return None
    
    def analyze_ux(self, report_content):
        """Send report to LLM for UX analysis"""
        # Load analysis prompt from prompts folder
        analysis_prompt = load_and_format_prompt('analysis_prompt', report_content=report_content)

        try:
            print("🔄 Analyzing UX with LLM...")
            response = self.llm.complete(analysis_prompt)
            analysis_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if analysis_text.startswith("```json"):
                analysis_text = analysis_text.split("```json")[1].split("```")[0].strip()
            elif analysis_text.startswith("```"):
                analysis_text = analysis_text.split("```")[1].split("```")[0].strip()
            
            analysis_json = json.loads(analysis_text)
            print("✓ UX analysis completed")
            return analysis_json
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {str(e)}")
            print(f"Raw response: {analysis_text[:500]}")
            return None
        except Exception as e:
            print(f"Error during analysis: {str(e)}")
            return None
    
    def generate_html_report(self, analysis_data):
        """Generate HTML report request via LLM"""
        # Load HTML generation prompt from prompts folder
        html_generation_prompt = load_and_format_prompt(
            'html_generation_prompt',
            analysis_data=json.dumps(analysis_data, indent=2),
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        try:
            print("🔄 Generating HTML report with LLM...")
            response = self.llm.complete(html_generation_prompt)
            html_content = response.text.strip()
            
            # Remove markdown code blocks if present
            if html_content.startswith("```html"):
                html_content = html_content.split("```html")[1].split("```")[0].strip()
            elif html_content.startswith("```"):
                html_content = html_content.split("```")[1].split("```")[0].strip()
            
            print("✓ HTML report generated")
            return html_content
        except Exception as e:
            print(f"Error generating HTML: {str(e)}")
            return None
    
    def save_html(self, html_content, output_path="ux_analysis_report.html"):
        """Save HTML report to file"""
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"✓ HTML report saved to {output_path}")
            return True
        except Exception as e:
            print(f"Error saving HTML: {str(e)}")
            return False
    
    def run_analysis(self, report_path="agent_result.txt", output_path="ux_analysis_report.html"):
        """Complete analysis pipeline"""
        print("\n" + "="*60)
        print("UX ANALYSIS PIPELINE")
        print("="*60 + "\n")
        
        # Step 1: Read report
        report_content = self.read_report(report_path)
        if not report_content:
            print("❌ Analysis aborted: No report content")
            return False
        
        # Step 2: Analyze UX
        analysis_data = self.analyze_ux(report_content)
        if not analysis_data:
            print("❌ Analysis aborted: Failed to analyze UX")
            return False
        
        # Save analysis JSON
        try:
            with open("ux_analysis.json", "w", encoding="utf-8") as f:
                json.dump(analysis_data, f, indent=2)
            print("✓ Analysis JSON saved to ux_analysis.json")
        except Exception as e:
            print(f"Warning: Could not save analysis JSON: {str(e)}")
        
        # Step 3: Generate HTML
        html_content = self.generate_html_report(analysis_data)
        if not html_content:
            print("❌ Analysis aborted: Failed to generate HTML")
            return False
        
        # Step 4: Save HTML
        success = self.save_html(html_content, output_path)
        
        if success:
            print("\n" + "="*60)
            print(f"✅ ANALYSIS COMPLETE")
            print(f"📊 View report: {output_path}")
            print("="*60 + "\n")
        
        return success
    
    def run_analysis_for_web(self, report_path="agent_result.txt", category="General", progress_callback=None, log_callback=None):
        """Analysis pipeline for web interface - generates JSON blocks instead of full HTML"""
        
        def log(message, log_type='info'):
            """Helper to send log if callback provided"""
            if log_callback:
                log_callback(message, log_type)
            print(f"[{log_type.upper()}] {message}")
        
        if progress_callback:
            progress_callback("Reading exploration report...", 75)
        log("Loading exploration report for analysis", 'info')
        
        # Step 1: Read report
        report_content = self.read_report(report_path)
        if not report_content:
            log("No report content found", 'error')
            if progress_callback:
                progress_callback("Error: No report content", -1)
            return False
        
        log(f"Report loaded: {len(report_content)} characters", 'success')
        if progress_callback:
            progress_callback("Analyzing UX patterns...", 80)
        
        log(f"Starting LLM-based UX analysis for {category} category", 'info')
        # Step 2: Analyze UX with enhanced prompt for positive findings
        analysis_data = self.analyze_ux_with_positive(report_content, category)
        if not analysis_data:
            log("UX analysis failed to produce results", 'error')
            if progress_callback:
                progress_callback("Error: Analysis failed", -1)
            return False
        
        log("UX analysis completed successfully", 'success')
        if progress_callback:
            progress_callback("Generating insights...", 90)
        
        # Save analysis blocks as JSON for web frontend
        try:
            log("Saving analysis to ux_analysis_blocks.json", 'info')
            with open("ux_analysis_blocks.json", "w", encoding="utf-8") as f:
                json.dump(analysis_data, f, indent=2)
            log("Analysis blocks saved successfully", 'success')
        except Exception as e:
            log(f"Error saving analysis: {str(e)}", 'error')
            if progress_callback:
                progress_callback(f"Error: {str(e)}", -1)
            return False
        
        if progress_callback:
            progress_callback("Analysis complete!", 95)
        log("UX analysis pipeline completed", 'success')
        
        return True
    
    def analyze_ux_with_positive(self, report_content, category):
        """Analyze UX with comprehensive metrics extraction"""
        # Load the enhanced analysis prompt
        analysis_prompt = load_and_format_prompt('analysis_prompt_v2', report_content=report_content)

        try:
            print("🔄 Analyzing UX with comprehensive metrics...")
            response = self.llm.complete(analysis_prompt)
            analysis_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if analysis_text.startswith("```json"):
                analysis_text = analysis_text.split("```json")[1].split("```")[0].strip()
            elif analysis_text.startswith("```"):
                analysis_text = analysis_text.split("```")[1].split("```")[0].strip()
            
            analysis_json = json.loads(analysis_text)
            
            # Ensure all required fields exist with comprehensive defaults to prevent undefined errors
            if 'summary' not in analysis_json:
                analysis_json['summary'] = 'UX analysis completed.'
            if 'positive' not in analysis_json:
                analysis_json['positive'] = []
            if 'issues' not in analysis_json:
                analysis_json['issues'] = []
            if 'recommendations' not in analysis_json:
                analysis_json['recommendations'] = []
            
            # App metadata with all nested properties
            if 'app_metadata' not in analysis_json:
                analysis_json['app_metadata'] = {}
            analysis_json['app_metadata'].setdefault('screens_discovered', 0)
            analysis_json['app_metadata'].setdefault('total_interactions', 0)
            analysis_json['app_metadata'].setdefault('core_flows', [])
            
            # Exploration coverage with all nested properties
            if 'exploration_coverage' not in analysis_json:
                analysis_json['exploration_coverage'] = {}
            analysis_json['exploration_coverage'].setdefault('screens_discovered', 0)
            analysis_json['exploration_coverage'].setdefault('clickable_elements_found', 0)
            analysis_json['exploration_coverage'].setdefault('successful_actions_pct', 0)
            analysis_json['exploration_coverage'].setdefault('dead_elements_pct', 0)
            analysis_json['exploration_coverage'].setdefault('navigation_loops_detected', False)
            
            # Navigation metrics with all nested properties
            if 'navigation_metrics' not in analysis_json:
                analysis_json['navigation_metrics'] = {}
            analysis_json['navigation_metrics'].setdefault('avg_depth', 0)
            analysis_json['navigation_metrics'].setdefault('max_depth', 0)
            analysis_json['navigation_metrics'].setdefault('backtracking_frequency', 'low')
            analysis_json['navigation_metrics'].setdefault('orphan_screens', 0)
            analysis_json['navigation_metrics'].setdefault('label_action_match_score', 5)
            analysis_json['navigation_metrics'].setdefault('hub_screen_count', 0)
            analysis_json['navigation_metrics'].setdefault('architecture_quality', 'moderate')
            
            # Interaction feedback with all nested properties
            if 'interaction_feedback' not in analysis_json:
                analysis_json['interaction_feedback'] = {}
            analysis_json['interaction_feedback'].setdefault('visible_feedback_rate_pct', 0)
            analysis_json['interaction_feedback'].setdefault('loading_state_presence_pct', 0)
            analysis_json['interaction_feedback'].setdefault('error_message_clarity', 5)
            analysis_json['interaction_feedback'].setdefault('silent_failures', 0)
            analysis_json['interaction_feedback'].setdefault('feedback_quality', 'moderate')
            
            # Visual hierarchy with all nested properties
            if 'visual_hierarchy' not in analysis_json:
                analysis_json['visual_hierarchy'] = {}
            analysis_json['visual_hierarchy'].setdefault('cta_visibility', 5)
            analysis_json['visual_hierarchy'].setdefault('tap_target_compliance_pct', 0)
            analysis_json['visual_hierarchy'].setdefault('icon_label_clarity', 5)
            analysis_json['visual_hierarchy'].setdefault('hierarchy_issues', 0)
            analysis_json['visual_hierarchy'].setdefault('clarity_rating', 'moderate')
            
            # Consistency with all nested properties
            if 'consistency' not in analysis_json:
                analysis_json['consistency'] = {}
            analysis_json['consistency'].setdefault('reused_patterns', [])
            analysis_json['consistency'].setdefault('inconsistent_labels', 0)
            analysis_json['consistency'].setdefault('action_placement_variance', 'low')
            analysis_json['consistency'].setdefault('pattern_violations', 0)
            
            # Error handling with all nested properties
            if 'error_handling' not in analysis_json:
                analysis_json['error_handling'] = {}
            analysis_json['error_handling'].setdefault('preventable_errors', 0)
            analysis_json['error_handling'].setdefault('recovery_paths_available', False)
            analysis_json['error_handling'].setdefault('error_explanation_quality', 5)
            analysis_json['error_handling'].setdefault('handling_rating', 'moderate')
            
            # UX confidence score with all nested properties
            if 'ux_confidence_score' not in analysis_json:
                analysis_json['ux_confidence_score'] = {}
            analysis_json['ux_confidence_score'].setdefault('score', 5)
            if 'factors' not in analysis_json['ux_confidence_score']:
                analysis_json['ux_confidence_score']['factors'] = {}
            analysis_json['ux_confidence_score']['factors'].setdefault('exploration_coverage', 5)
            analysis_json['ux_confidence_score']['factors'].setdefault('interaction_consistency', 5)
            analysis_json['ux_confidence_score']['factors'].setdefault('feedback_reliability', 5)
            analysis_json['ux_confidence_score']['factors'].setdefault('recovery_robustness', 5)
            
            # Complexity score
            if 'complexity_score' not in analysis_json:
                analysis_json['complexity_score'] = 5
            
            print("✓ UX analysis completed with comprehensive metrics")
            return analysis_json
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {str(e)}")
            print(f"Raw response: {analysis_text[:500]}")
            return None
        except Exception as e:
            print(f"Error during analysis: {str(e)}")
            return None


if __name__ == "__main__":
    # Run as standalone script
    analyzer = UXAnalyzer()
    analyzer.run_analysis()
