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
        
        # Use a free model from OpenRouter for analysis
        self.llm = OpenAILike(
            model="mistralai/devstral-2512:free",
            api_base="https://openrouter.ai/api/v1",
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


if __name__ == "__main__":
    # Run as standalone script
    analyzer = UXAnalyzer()
    analyzer.run_analysis()
