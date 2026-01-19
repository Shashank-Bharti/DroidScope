# DroidRun UX Flow Explorer

An autonomous UI exploration agent that maps application navigation flows and generates detailed UX analysis reports.

## Overview

This project uses the DroidRun framework to automatically explore mobile/web applications, discover navigable screens, record transitions, and produce structured UX flow maps with AI-powered analysis.

## Features

- **Autonomous Exploration**: AI agent navigates apps like a human user
- **Structured Output**: Generates JSON navigation graphs with screens and transitions
- **UX Analysis**: Analyzes structural attention patterns, friction points, and discoverability issues
- **HTML Reports**: Beautiful visualizations with Chart.js and Markdown.js
- **Safety First**: Avoids destructive actions (logout, delete, posting)

## Setup

### 1. Create Virtual Environment

```powershell
python -m venv venv
```

### 2. Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

If you encounter an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
API_KEY=your_openrouter_api_key_here
```

## Usage

### Run UX Flow Explorer

```powershell
python ux_flow_explorer.py
```

This will:
1. Explore the target application (configured in the script)
2. Generate `agent_result.txt` with exploration results
3. Automatically run UX analysis
4. Generate `ux_analysis_report.html` with visualizations

### Run Analysis Only (Standalone)

```powershell
python ux_analyzer.py
```

Analyzes existing `agent_result.txt` and generates HTML report.

## Output Files

- **agent_result.txt** - Raw exploration results with success status
- **discord_ux_flow.json** - Structured navigation graph (if available)
- **ux_analysis.json** - Detailed UX analysis in JSON format
- **ux_analysis_report.html** - Interactive HTML report with charts

## Configuration

### Change Target Application

Edit the `APP_NAME` constant in `ux_flow_explorer.py`:

```python
APP_NAME = "YourAppName"  # Will be inserted into agent_goal.txt
```

Or directly edit `prompts/agent_goal.txt` to fully customize the exploration prompt.

### Adjust Exploration Parameters

In `ux_flow_explorer.py`:

```python
MAX_STEPS = 110  # Maximum steps for exploration
OUTPUT_FILE = "agent_result.txt"  # Output file path
```

### Customize Prompts

All prompts are now in the `prompts/` folder for easy editing:
- **agent_goal.txt** - Controls how the agent explores (supports `{app_name}` variable)
- **analysis_prompt.txt** - Controls UX analysis criteria (supports `{report_content}` variable)
- **html_generation_prompt.txt** - Controls HTML report style (supports `{analysis_data}`, `{timestamp}` variables)

### Change LLM Model

```python
llm = OpenAILike(
    model="mistralai/devstral-2512:free",  # Change model here
    api_base="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_KEY,
    temperature=0.2
)
```

## Project Structure

```
DROIDRUN/
├── prompts/                    # Prompt templates
│   ├── agent_goal.txt         # Exploration goal template
│   ├── analysis_prompt.txt    # UX analysis instructions
│   └── html_generation_prompt.txt  # HTML report generation
├── ux_flow_explorer.py        # Main exploration agent
├── ux_analyzer.py             # UX analysis and HTML generation
├── utils.py                   # Shared utility functions
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
├── .gitignore                 # Git ignore rules
└── trajectories/              # Exploration session data
```

## Features of New Structure

### ✅ Separated Prompts
- All prompts moved to `prompts/` folder
- Easy to edit without touching code
- Supports variable substitution (e.g., `{app_name}`)

### ✅ Shared Utilities
- `utils.py` provides common functions
- `load_prompt()` - Load any prompt file
- `format_prompt()` - Insert variables into templates
- `load_and_format_prompt()` - Load and format in one step

### ✅ Cleaner Code
- Removed redundancy
- Constants at top of files
- Faster loading (prompts loaded on demand)

## Requirements

- Python 3.8+
- DroidRun framework
- OpenRouter API key (for free LLM access)
- Android device/emulator or browser (depending on target)

## Deactivate Virtual Environment

When done:

```powershell
deactivate
```

## License

MIT

## Contributing

Feel free to submit issues or pull requests.
