from droidrun import DroidAgent
from droidrun.config_manager import DroidrunConfig
from llama_index.llms.openai_like import OpenAILike
import asyncio
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
import json
from dotenv import load_dotenv
import os
from ux_analyzer import UXAnalyzer
from utils import load_and_format_prompt

load_dotenv()

# Configuration
APP_NAME = "Instagram"
OPENROUTER_KEY = os.getenv("API_KEY")
MAX_STEPS = 110
OUTPUT_FILE = "agent_result.txt"

# Pydantic Model 
class Screen(BaseModel):
    id: str = Field(description="Unique identifier or hash of the screen")
    title: str = Field(description="Human-readable name of the screen")
    depth: int = Field(description="Depth level in navigation flow")


class Transition(BaseModel):
    from_screen: str = Field(description="Source screen ID")
    to_screen: str = Field(description="Destination screen ID")
    action: str = Field(description="UI action that caused the transition")


class UXFlow(BaseModel):
    screens: List[Screen] = Field(description="List of discovered screens")
    transitions: List[Transition] = Field(description="Navigation transitions")
    total_screens: int = Field(description="Total number of unique screens")
    max_depth: int = Field(description="Maximum depth explored")
    exploration_time: float = Field(description="Exploration time in seconds")


# Create OpenRouter LLM with Mistral model
llm = OpenAILike(
    model="mistralai/devstral-2512:free",
    api_base="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_KEY,
    temperature=0.2
)

config = DroidrunConfig()
config.agent.max_steps = MAX_STEPS

# Load agent goal from prompts folder
agent_goal = load_and_format_prompt('agent_goal', app_name=APP_NAME)

agent = DroidAgent(
    goal=agent_goal,
    config=config,
    llms=llm,
)

async def main():
    result = await agent.run()
    
    # Prepare output data
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output_lines = []
    
    try:
        # Capture success status
        success_status = getattr(result, 'success', None)
        output_lines.append(f"Timestamp: {timestamp}")
        output_lines.append(f"Success: {success_status}")
        output_lines.append("-" * 50)
        
        # Capture final answer if available
        if hasattr(result, 'final_answer') and result.final_answer:
            output_lines.append(f"Final Answer:\n{result.final_answer}")
            output_lines.append("-" * 50)
        
        # Capture structured output if available
        if hasattr(result, 'structured_output') and result.structured_output:
            try:
                structured_json = result.structured_output.model_dump_json(indent=2)
                output_lines.append(f"Structured Output:\n{structured_json}")
                
                # Also save structured output as separate JSON file
                with open("discord_ux_flow.json", "w", encoding="utf-8") as json_file:
                    json_file.write(structured_json)
                output_lines.append("-" * 50)
                output_lines.append("Structured output saved to: discord_ux_flow.json")
            except Exception as e:
                output_lines.append(f"Error serializing structured output: {str(e)}")
        
        # Capture reason if available
        if hasattr(result, 'reason') and result.reason:
            output_lines.append(f"Reason: {result.reason}")
        
        # Write to text file
        output_text = "\n".join(output_lines)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as txt_file:
            txt_file.write(output_text)
        
        print(f"Success: {success_status}")
        print(f"Results saved to: {OUTPUT_FILE}")
        
        # Run UX Analysis if exploration was successful
        if success_status:
            print("\n" + "="*60)
            print("Starting UX Analysis...")
            print("="*60)
            try:
                analyzer = UXAnalyzer(api_key=OPENROUTER_KEY)
                analyzer.run_analysis(
                    report_path=OUTPUT_FILE,
                    output_path="ux_analysis_report.html"
                )
            except Exception as analysis_error:
                print(f"⚠️  UX Analysis failed: {str(analysis_error)}")
                print("Main results still saved successfully.")
        
    except Exception as e:
        error_msg = f"Error processing results: {str(e)}\nTimestamp: {timestamp}"
        with open(OUTPUT_FILE, "w", encoding="utf-8") as txt_file:
            txt_file.write(error_msg)
        print(f"Error occurred: {str(e)}")
        print(f"Error details saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())
