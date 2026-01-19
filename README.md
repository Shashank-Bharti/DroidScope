<div align="center">

# 🔭 DroidScope
### Autonomous UI/UX Exploration & Analysis

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Flask-2.x-green.svg?style=flat-square&logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/DroidRun-SDK-orange.svg?style=flat-square" alt="DroidRun">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square" alt="License">
</p>

<p align="center">
An autonomous UI/UX exploration and analysis tool with a sharp, dark-mode web interface.<br>
Uses DroidRun SDK automation to act as an intelligent UX tester, exploring apps and<br>
generating comprehensive analysis reports with real-time execution logs.
</p>

</div>

---

## 🌟 Overview

<table>
<tr>
<td width="50%">

**DroidScope** leverages the DroidRun framework to automatically explore mobile applications, discover navigable screens, record transitions, and produce structured UX flow maps with AI-powered analysis.

</td>
<td width="50%">

**Features** a Flask-based web interface with real-time progress tracking, live terminal logs, and category-aware intelligence that tailors testing to your app type.

</td>
</tr>
</table>

---

## ✨ Features

<table>
<tr>
<td width="50%" valign="top">

### 🎨 Interface & UX
- 🔭 **DroidScope UI** - Sharp dark design with 2px borders
- 📋 **Live Execution Logs** - Real-time terminal events
- 📊 **Dual SSE Streams** - Separate progress & log updates
- 📈 **Visual Reports** - Interactive Chart.js visualizations

</td>
<td width="50%" valign="top">

### 🤖 Intelligence & Safety
- 🎯 **Category-Aware** - Context-specific testing goals
- ✅ **Balanced Analysis** - Strengths + improvements
- 🔒 **Safety First** - Avoids destructive actions
- ✓ **Device Verification** - Pre-flight `droidrun ping`

</td>
</tr>
<tr>
<td width="50%" valign="top">

### ⚙️ Configuration
- **Depth Control** - Adjustable (3-12 levels)
- **Category Selection** - 13 app categories
- **LLM Powered** - OpenRouter API integration

</td>
<td width="50%" valign="top">

### 🚀 Automation
- **Autonomous Navigation** - AI explores like humans
- **Breadth-First Search** - Comprehensive coverage
- **Structured Output** - Navigation graph JSON + analysis blocks

</td>
</tr>
</table>

---

## 🚀 Quick Start

<div align="center">

### **Commands to Launch**

</div>

```powershell
python app.py             # 🚀 Start server
# 🌐 Open http://localhost:5000
```

---

## 📦 Setup

<details open>
<summary><b>1️⃣ Create Virtual Environment</b></summary>

```powershell
python -m venv venv
```

</details>

<details open>
<summary><b>2️⃣ Activate Virtual Environment</b></summary>

```powershell
.\venv\Scripts\Activate.ps1
```

**If you encounter an execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

</details>

<details open>
<summary><b>3️⃣ Install Dependencies</b></summary>

```powershell
pip install -r requirements.txt
```

</details>

<details open>
<summary><b>4️⃣ Configure Environment Variables</b></summary>

Create a `.env` file in the project root:

```env
API_KEY=your_openrouter_api_key_here
```

</details>

---

## 🎯 Usage

### 🌐 Web Interface (Recommended)

```powershell
python app.py
```

Then open **http://localhost:5000** in your browser.

<table>
<tr>
<th>Step</th>
<th>Action</th>
</tr>
<tr>
<td>1️⃣</td>
<td>Enter app name to test</td>
</tr>
<tr>
<td>2️⃣</td>
<td>Select app category (affects analysis focus)</td>
</tr>
<tr>
<td>3️⃣</td>
<td>Adjust exploration depth with slider (3-12)</td>
</tr>
<tr>
<td>4️⃣</td>
<td>Click "Start UX Test" and watch real-time progress</td>
</tr>
<tr>
<td>5️⃣</td>
<td>View results with interactive charts and insights</td>
</tr>
</table>

### 🖥️ CLI Mode (Original)

<details>
<summary><b>Run UX Flow Explorer</b></summary>

```powershell
python ux_flow_explorer.py
```

This will:
1. Explore the target application (configured in the script)
2. Generate `agent_result.txt` with exploration results
3. Automatically run UX analysis
4. Generate `ux_analysis_report.html` with visualizations

</details>

---

## 📂 Output Files

| File | Description |
|------|-------------|
| `agent_result.txt` | Raw exploration results with success status |
| `exploration_output.json` | Structured navigation graph |
| `ux_analysis_blocks.json` | Analysis data for web interface |
| `ux_analysis_report.html` | Standalone HTML report (CLI mode) |

---

## ✅ Launch Checklist

### 🔍 Pre-Launch Verification

Run the verification script to check all dependencies:

```powershell
python verify_setup.py
```

<table>
<tr>
<th>Check</th>
<th>Description</th>
</tr>
<tr>
<td>✅</td>
<td><code>.env</code> file exists with API_KEY</td>
</tr>
<tr>
<td>✅</td>
<td>Device connection via <code>droidrun ping</code></td>
</tr>
<tr>
<td>✅</td>
<td>All directories exist (templates, static, prompts)</td>
</tr>
<tr>
<td>✅</td>
<td>All prompt files present</td>
</tr>
<tr>
<td>✅</td>
<td>Frontend files ready (HTML, CSS, JS)</td>
</tr>
<tr>
<td>✅</td>
<td>Python packages installed</td>
</tr>
</table>

### 🚀 Launch Sequence

<table>
<tr>
<th width="30%">Step</th>
<th>Command</th>
</tr>
<tr>
<td><b>1. Verify Setup</b><br>(recommended)</td>
<td>

```powershell
python verify_setup.py
```

</td>
</tr>
<tr>
<td><b>2. Start Server</b></td>
<td>

```powershell
python app.py
```

You should see:
```
╔═══════════════════════════════════╗
║     🔭 DroidScope Starting...     ║
╚═══════════════════════════════════╝
```

</td>
</tr>
<tr>
<td><b>3. Open Browser</b></td>
<td>Navigate to <code>http://localhost:5000</code></td>
</tr>
</table>

### 🧪 First Test Run

<table>
<tr>
<th>Field</th>
<th>Example</th>
</tr>
<tr>
<td>App Name</td>
<td>"Instagram", "Blinkit", "WhatsApp"</td>
</tr>
<tr>
<td>Category</td>
<td>"Social Media", "Food Delivery", "Messaging"</td>
</tr>
<tr>
<td>Depth Slider</td>
<td>6 (recommended for balanced testing)</td>
</tr>
</table>

> **📌 Note**: Depth ≠ Steps. Depth controls navigation distance, not total actions.

**What to Watch:**
- 📊 Progress bar for completion percentage
- 📋 Terminal logs for real-time execution events
- 📈 Interactive results with charts and insights

### 📊 Expected Progress Phases

```
10%  - Generating category context
20%  - Initializing DroidRun agent  
30%  - Starting exploration (may take 5-15 min)
60%  - Exploration complete
75%  - Loading report
80%  - Running UX analysis
90%  - Generating visualizations
100% - Complete!
```

### 🔧 Troubleshooting

<details>
<summary><b>❌ Device not connected</b></summary>

```powershell
droidrun ping
```
If this fails, check your device/emulator connection.

</details>

<details>
<summary><b>🔑 Missing API key</b></summary>

Create `.env` file with:
```env
API_KEY=sk-or-v1-your_openrouter_key_here
```

</details>

<details>
<summary><b>🔌 Port already in use</b></summary>

Change port in `app.py`:
```python
app.run(debug=True, port=5001)  # Change from 5000
```

</details>

---

## 📁 Project Structure

```
DROIDRUN/
├── app.py                      # Flask web server with SSE
├── exploration_runner.py       # Category-aware exploration
├── ux_analyzer.py              # UX analysis engine
├── verify_setup.py             # Pre-flight checks
├── utils.py                    # Shared utilities
├── templates/
│   └── index.html              # DroidScope web UI
├── static/
│   ├── style.css               # Sharp dark theme (2px borders)
│   └── script.js               # Frontend logic + SSE
├── prompts/
│   ├── agent_goal.txt          # Exploration instructions
│   └── analysis_prompt.txt     # UX analysis template
├── requirements.txt            # Dependencies
├── .env                        # API_KEY (gitignored)
├── trajectories/               # Session data (gitignored)
└── venv/                       # Virtual environment (gitignored)
```

> **💡 Note:** `ux_flow_explorer.py` is the legacy CLI tool. Use the web interface (`app.py`) for the best experience.

---

## 🎨 Key Features Explained

### 🔭 DroidScope Interface

<table>
<tr>
<td width="33%"><b>Sharp Design</b></td>
<td width="67%">2px borders, zero border-radius for modern look</td>
</tr>
<tr>
<td><b>Hover Effects</b></td>
<td>Border colors change to accent blue on hover</td>
</tr>
<tr>
<td><b>Dual SSE Streams</b></td>
<td>Separate endpoints for progress (<code>/api/progress</code>) and logs (<code>/api/logs</code>)</td>
</tr>
</table>

### 📡 Real-Time Updates

| Component | Description |
|-----------|-------------|
| **Progress Bar** | Shows completion percentage (0-100%) |
| **Terminal Logs** | Live execution events with timestamps |
| **Color-Coded** | Info (gray), Success (green), Warning (yellow), Error (red) |

### 🎯 Category Intelligence

The system asks an LLM: *"What should I test in a [category] app?"*

<table>
<tr>
<td>✓</td>
<td>Generates context-specific testing goals</td>
</tr>
<tr>
<td>✓</td>
<td>Focuses on relevant features (e.g., checkout flow for e-commerce)</td>
</tr>
<tr>
<td>✓</td>
<td>Validates industry-specific UX patterns</td>
</tr>
</table>

### ✅ Device Verification

On startup, `verify_setup.py` runs `droidrun ping` to ensure:

- ✓ Device/emulator is connected
- ✓ DroidRun can communicate
- ✓ App won't fail mid-exploration

### 📊 Balanced Analysis

<table>
<tr>
<th width="30%">Aspect</th>
<th>What's Analyzed</th>
</tr>
<tr>
<td>✅ <b>Positive Patterns</b></td>
<td>What works well</td>
</tr>
<tr>
<td>⚠️ <b>Issues</b></td>
<td>Problems found</td>
</tr>
<tr>
<td>💡 <b>Suggestions</b></td>
<td>Actionable improvements</td>
</tr>
<tr>
<td>📈 <b>Metrics</b></td>
<td>Quantitative measurements</td>
</tr>
</table>

---

## ⚙️ Configuration & Customization

### 🔄 Change LLM Model

Edit `exploration_runner.py` or `ux_analyzer.py`:

```python
llm = OpenAILike(
    model="mistralai/devstral-2512:free",  # Change this
    api_base="https://openrouter.ai/api/v1",
    api_key=api_key,
    temperature=0.2
)
```

### 📝 Customize Prompts

Edit files in `prompts/` folder:

| File | Purpose |
|------|---------|
| `agent_goal.txt` | Exploration instructions |
| `analysis_prompt.txt` | UX analysis criteria |

**Variables supported:** `{app_name}`, `{category}`, `{report_content}`

### 📏 Adjust Exploration Depth

**Via web UI slider (3-12)** or in code:

```python
# exploration_runner.py
config.agent.max_steps = max_depth * 15  # Steps = depth × 15
```

---

## 📋 Requirements

<table>
<tr>
<td>🐍</td>
<td>Python 3.8+</td>
</tr>
<tr>
<td>📱</td>
<td>DroidRun framework</td>
</tr>
<tr>
<td>🔑</td>
<td>OpenRouter API key (for free LLM access)</td>
</tr>
<tr>
<td>📲</td>
<td>Android device/emulator with app installed</td>
</tr>
</table>

---

## 🔚 Deactivate Virtual Environment

When done:

```powershell
deactivate
```

---

<div align="center">

## 📄 License

**MIT License** - Feel free to use, modify, and distribute.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

<p>
Made with 🫀 by Team LastCrusade 
</p>

</div>
