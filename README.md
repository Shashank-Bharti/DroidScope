<div align="center">
<img src='./images/Header.png' alt='DroidScope Autonomous UX Exploration & Analysis Tool Based on Droidrun Framework'>


<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Flask-2.x-green.svg?style=flat-square&logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/DroidRun-SDK-orange.svg?style=flat-square" alt="DroidRun">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square" alt="License">
</p>

<p align="center">
An autonomous UX exploration and analysis tool with a sleek monochrome web interface.<br>
Uses <a href="https://github.com/droidrun/droidrun">DroidRun SDK</a> automation to act as an intelligent UX tester, exploring apps and<br>
generating comprehensive analysis reports with real-time execution logs and professional metrics.
</p>

</div>

---

## 📚 Quick Reference

<table>
<tr>
<td width="50%" valign="top">

### 🚀 Getting Started (First Time)

```powershell
# 1. Create & activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key
copy .env.example .env
# Edit .env and add your API_KEY

# 4. Verify setup
python verify_setup.py

# 5. Launch!
python app.py
```

**Then:** Open http://localhost:5000

</td>
<td width="50%" valign="top">

### 🔄 Daily Usage (Already Set Up)

```powershell
# 1. Activate environment
.\venv\Scripts\Activate.ps1

# 2. Connect device
adb devices  # Verify device shown

# 3. Launch server
python app.py

# 4. When done
deactivate
```

**Common Commands:**
```powershell
droidrun ping          # Test device connection
python verify_setup.py # Check configuration
```

</td>
</tr>
</table>

---

## 🔍 Overview

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
- **Monochrome Design** - Clean black & white theme with grid background
- **Live Execution Logs** - Real-time terminal events with agent reasoning
- **Dual SSE Streams** - Separate progress & log updates
- **Visual Reports** - Interactive Chart.js visualizations with 8 stat cards
- **Card-Based Layout** - Professional result cards with metadata
- **Rounded Corners** - Modern UI with consistent border-radius

</td>
<td width="50%" valign="top">

### 🤖 Intelligence & Analysis
- **Category-Aware** - Context-specific testing goals
- **Comprehensive Metrics** - 12 UX categories analyzed
- **Professional Reports** - Interaction feedback, visual hierarchy, consistency tracking
- **Safety First** - Avoids destructive actions
- **Device Verification** - Pre-flight droidrun ping
- **Schema-Agnostic** - Backward & forward compatible JSON handling

</td>
</tr>
<tr>
<td width="50%" valign="top">

### ⚙️ Configuration
- **Depth Control** - Adjustable (3-12 levels)
- **Category Selection** - 13 app categories
- **Dynamic LLM Config** - Model & provider from environment variables
- **Flexible API** - Supports any OpenAI-compatible endpoint

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

## 🎨 Interface Preview

<div align="center">

### **Main Interface**
<img src="./images/ui 1.png" alt="DroidScope Main Interface" width="800">

### **Real-Time Execution Logs**
<img src="./images/ui 2.png" alt="Live Terminal Logs" width="800">

### **Analysis Results & Reports**
<img src="./images/ui 3.png" alt="UX Analysis Results" width="800">

</div>

---

## 📦 Setup

> **⏱️ Setup Time:** ~5 minutes | **💡 Tip:** Run `python verify_setup.py` after setup to check everything

<details open>
<summary><b>1️⃣ Prerequisites</b></summary>

Before starting, ensure you have:

- ✅ **Python 3.8+** installed ([Download](https://python.org))
- ✅ **Android device/emulator** with USB debugging enabled
- ✅ **ADB** working (`adb devices` should list your device)
- ✅ **Internet connection** for API calls

**Quick Check:**
```powershell
python --version  # Should be 3.8 or higher
adb devices       # Should show your device
```

</details>

<details open>
<summary><b>2️⃣ Clone/Download Repository</b></summary>

If you haven't already:

```powershell
git clone <repository-url>
cd DroidScope
```

Or download and extract the ZIP file, then navigate to the folder in PowerShell.

</details>

<details open>
<summary><b>3️⃣ Create Virtual Environment</b></summary>

**Why?** Keeps dependencies isolated and prevents conflicts with other Python projects.

```powershell
python -m venv venv
```

This creates a `venv` folder containing an isolated Python environment.

</details>

<details open>
<summary><b>4️⃣ Activate Virtual Environment</b></summary>

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
```

**Expected Result:** Your terminal prompt should now show `(venv)` at the beginning.

**If you encounter an execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

</details>

<details open>
<summary><b>5️⃣ Install Dependencies</b></summary>

**With activated venv:**
```powershell
pip install -r requirements.txt
```

This installs:
- `flask` - Web framework
- `droidrun` - Android automation
- `python-dotenv` - Environment variable management
- Other required packages

**To verify installation:**
```powershell
pip list
```

</details>

<details open>
<summary><b>6️⃣ Install DroidRun Framework</b></summary>

**If not already installed:**

```powershell
pip install droidrun
```

**Verify DroidRun:**
```powershell
droidrun --version
droidrun ping  # Should detect your device
```

**Troubleshooting:**
- If `droidrun ping` fails, check device connection with `adb devices`
- Ensure USB debugging is enabled on your device

📖 **Learn more:** [DroidRun Documentation](https://github.com/droidrun/droidrun)

</details>

<details open>
<summary><b>7️⃣ Configure Environment Variables</b></summary>

**Create `.env` file in project root:**

1. **Copy the example file:**
   ```powershell
   copy .env.example .env
   ```

2. **Edit `.env` with your API key:**
   ```env
   # Required: Your OpenRouter API Key
   API_KEY=sk-or-v1-your_actual_key_here
   
   # Optional: LLM Configuration (defaults shown)
   LLM_MODEL=mistralai/devstral-2512:free
   LLM_API_BASE=https://openrouter.ai/api/v1
   ```

3. **Get your API key:**
   - Visit: https://openrouter.ai/keys
   - Sign up (free tier available)
   - Create API key
   - Copy and paste into `.env`

**Using OpenAI instead?**
```env
API_KEY=sk-your_openai_key_here
LLM_MODEL=gpt-4o-mini
LLM_API_BASE=https://api.openai.com/v1
```

**Security Note:** Never commit `.env` to version control (it's in `.gitignore`)

</details>

<details open>
<summary><b>8️⃣ Verify Setup</b></summary>

**Run the verification script:**
```powershell
python verify_setup.py
```

**This checks:**
- ✅ `.env` file exists with API_KEY
- ✅ Device connection via `droidrun ping`
- ✅ All required directories exist
- ✅ All prompt files present
- ✅ Frontend files (HTML, CSS, JS)
- ✅ Python packages installed

**If all checks pass ✅, you're ready to launch!**

</details>

---

## 🎯 Usage

### 🌐 Web Interface (Recommended)

**Start the server:**
```powershell
python app.py
```

**Expected output:**
```
╔═══════════════════════════════════╗
║     🔭 DroidScope Starting...     ║
╚═══════════════════════════════════╝
 * Running on http://127.0.0.1:5000
```

Then open **http://localhost:5000** in your browser (Chrome/Edge recommended).

---

### 📝 Step-by-Step Testing Guide

<table>
<tr>
<th width="10%">Step</th>
<th width="30%">Action</th>
<th width="60%">Details</th>
</tr>
<tr>
<td align="center">1️⃣</td>
<td><b>Enter App Name</b></td>
<td>Type the display name of the app (e.g., "Instagram", "WhatsApp")<br><i>Not the package name!</i></td>
</tr>
<tr>
<td align="center">2️⃣</td>
<td><b>Select Category</b></td>
<td>Choose from 13 categories - affects which UX patterns are tested<br>
<details>
<summary>Available categories</summary>

- Social Media
- E-commerce
- Food Delivery
- Messaging
- Finance/Banking
- Productivity
- Entertainment
- Education
- Health & Fitness
- Travel
- News
- Utilities
- Other

</details>
</td>
</tr>
<tr>
<td align="center">3️⃣</td>
<td><b>Set Exploration Depth</b></td>
<td>
Use slider (3-12):
<ul>
<li><b>3-4:</b> Quick test (~3-5 min) - Surface-level screens</li>
<li><b>5-7:</b> Balanced (~10-15 min) - Recommended for most apps</li>
<li><b>8-12:</b> Deep dive (~20-30 min) - Comprehensive testing</li>
</ul>
<i>Note: Steps = Depth × 15</i>
</td>
</tr>
<tr>
<td align="center">4️⃣</td>
<td><b>Click "Start UX Test"</b></td>
<td>Watch real-time progress and terminal logs<br>
✅ Safe to browse away - test continues in background</td>
</tr>
<tr>
<td align="center">5️⃣</td>
<td><b>View Results</b></td>
<td>
<ul>
<li>📊 Interactive Chart.js visualizations</li>
<li>📈 8 metric stat cards</li>
<li>📝 Executive summary</li>
<li>✅ Strengths found</li>
<li>⚠️ Issues categorized</li>
<li>💡 Actionable recommendations</li>
</ul>
</td>
</tr>
</table>

---

### 🎬 What Happens During Testing

**Progress Phases:**

```
 0% → 10%   Generating category-specific testing goals
10% → 20%   Initializing DroidRun agent on device
20% → 60%   🤖 Active exploration (this takes longest)
             ├─ AI navigates through app
             ├─ Takes screenshots
             ├─ Records UI hierarchy
             └─ Builds navigation graph
60% → 75%   Loading exploration report
75% → 80%   🔍 Running UX analysis with LLM
80% → 90%   Generating visualizations
90% → 100%  Rendering results
100% ✅     Complete!
```

**Real-Time Features:**
- 📊 **Progress bar** - Shows completion percentage
- 📋 **Terminal logs** - Live execution events with color coding
  - 🔵 Info (gray) - General updates
  - 🟢 Success (green) - Completed actions
  - 🟡 Warning (yellow) - Non-critical issues
  - 🔴 Error (red) - Problems encountered
- 🧠 **Agent reasoning** - See actual LLM decision-making

---

## 📊 Analysis Output

### Generated Files

| File | Description |
|------|-------------|
| `agent_result.txt` | Raw exploration results with markdown report |
| `ux_analysis_blocks.json` | Comprehensive UX analysis with 12 metric categories |
| `trajectories/[session]/` | Session data including screenshots and actions |

### Metrics Analyzed

<table>
<tr>
<td width="50%" valign="top">

**Navigation & Structure**
- Total screens discovered
- Max depth reached
- Orphan screens
- Hub screen count
- Dead elements percentage

</td>
<td width="50%" valign="top">

**Interaction & Feedback**
- Visible feedback rate
- Silent failures count
- CTA visibility score (1-10)
- Preventable errors
- Loading state presence

</td>
</tr>
</table>

### Report Sections

- **Executive Summary** - Overall UX maturity assessment
- **Key Metrics** - 3 charts + 8 stat cards with quantified data
- **Strengths** - Positive UX patterns with evidence
- **Issues** - Categorized problems with severity, location, and impact
- **Recommendations** - Prioritized improvements with effort estimates

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

**Symptoms:**
- `droidrun ping` fails or hangs
- "No device connected" error
- Exploration doesn't start

**Solutions:**

1. **Check ADB Connection**
   ```powershell
   adb devices
   ```
   You should see your device listed. If not:
   
2. **Restart ADB Server**
   ```powershell
   adb kill-server
   adb start-server
   adb devices
   ```

3. **For Physical Devices:**
   - Enable USB Debugging in Developer Options
   - Check USB cable (use data cable, not charge-only)
   - Allow USB debugging on device popup
   - Try different USB ports

4. **For Emulators:**
   - Ensure emulator is fully booted
   - Try restarting the emulator
   - Check if emulator shows in `adb devices`
   
5. **Verify DroidRun Installation**
   ```powershell
   droidrun --version
   droidrun ping
   ```
   If DroidRun is not installed:
   ```powershell
   pip install droidrun
   ```

6. **Multiple Devices:**
   If you have multiple devices, specify one:
   ```powershell
   adb devices  # List all devices
   # Use the device ID in your commands
   ```

</details>

<details>
<summary><b>🔑 Missing API key</b></summary>

**Symptoms:**
- "API key not found" error
- LLM requests fail
- Analysis doesn't generate

**Solutions:**

1. **Create `.env` File**
   
   In your project root, create a file named `.env` (not `.env.txt`):
   
   ```env
   API_KEY=sk-or-v1-your_openrouter_key_here
   LLM_MODEL=mistralai/devstral-2512:free
   LLM_API_BASE=https://openrouter.ai/api/v1
   ```

2. **Get Your API Key**
   
   - Visit: https://openrouter.ai/keys
   - Sign up/login
   - Generate a new API key
   - Copy the key (starts with `sk-or-v1-`)

3. **Using OpenAI Instead**
   
   If you prefer OpenAI:
   ```env
   API_KEY=sk-your_openai_key_here
   LLM_MODEL=gpt-4o-mini
   LLM_API_BASE=https://api.openai.com/v1
   ```

4. **Verify API Key**
   
   Run the verification script:
   ```powershell
   python verify_setup.py
   ```
   
   It will check if your `.env` file is properly configured.

5. **Common Issues:**
   - ❌ File named `.env.txt` instead of `.env`
   - ❌ API key has extra spaces
   - ❌ Missing `API_KEY=` prefix
   - ❌ File in wrong directory (must be in project root)

6. **Test API Connection**
   ```powershell
   # Run a simple test
   python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key loaded:', 'Yes' if os.getenv('API_KEY') else 'No')"
   ```

</details>

<details>
<summary><b>🔌 Port already in use</b></summary>

**Symptoms:**
- "Address already in use" error
- "OSError: [WinError 10048]"
- Flask fails to start

**Solutions:**

1. **Find Process Using Port 5000**
   
   ```powershell
   netstat -ano | findstr :5000
   ```
   
   This shows the PID (Process ID) of the program using the port.

2. **Kill the Process**
   
   ```powershell
   taskkill /PID <process_id> /F
   ```
   
   Replace `<process_id>` with the number from step 1.

3. **Change DroidScope Port**
   
   Edit [app.py](app.py) (at the bottom):
   
   ```python
   if __name__ == '__main__':
       app.run(debug=True, port=5001)  # Changed from 5000 to 5001
   ```
   
   Then access at: `http://localhost:5001`

4. **Use Any Available Port**
   
   ```python
   # app.py - Let Flask choose a free port
   if __name__ == '__main__':
       app.run(debug=True, port=0)  # Automatically finds free port
   ```
   
   Flask will print the actual port it's using.

5. **Close Other Instances**
   
   Make sure you don't have multiple terminal windows running `python app.py`

</details>

<details>
<summary><b>🐍 Python/Virtual Environment Issues</b></summary>

**Symptoms:**
- "python: command not found"
- "venv not activating"
- Packages not found after installation

**Solutions:**

1. **Check Python Installation**
   ```powershell
   python --version
   # Should show Python 3.8 or higher
   ```
   
   If not installed, download from: https://python.org

2. **Execution Policy Error (Windows)**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Recreate Virtual Environment**
   ```powershell
   # Remove old venv
   Remove-Item -Recurse -Force venv
   
   # Create new one
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

4. **Packages Not Found**
   
   Ensure venv is activated (you should see `(venv)` in terminal):
   ```powershell
   .\venv\Scripts\Activate.ps1
   pip list  # Check installed packages
   ```

</details>

<details>
<summary><b>📱 App Not Installed/Opening</b></summary>

**Symptoms:**
- "App not found" error
- Wrong app opens
- App crashes immediately

**Solutions:**

1. **Check App Installation**
   ```powershell
   adb shell pm list packages | findstr instagram  # Replace with your app
   ```

2. **Install App on Device**
   ```powershell
   adb install path/to/app.apk
   ```

3. **Use Correct Package Name**
   
   When entering app name, use the display name (e.g., "Instagram", not "com.instagram.android")

4. **Grant Permissions**
   
   Some apps need permissions. Grant them manually or:
   ```powershell
   adb shell pm grant com.yourapp.package android.permission.PERMISSION_NAME
   ```

</details>

<details>
<summary><b>⚡ Slow Performance/Timeouts</b></summary>

**Symptoms:**
- Exploration takes too long
- "Timeout" errors
- App freezes during testing

**Solutions:**

1. **Reduce Exploration Depth**
   
   Use slider to set depth to 3-5 for faster tests

2. **Check Device Performance**
   
   - Close background apps
   - Use a more powerful emulator configuration
   - Increase emulator RAM in AVD settings

3. **Network Issues**
   
   Ensure stable internet for API calls to LLM

4. **Use Faster LLM Model**
   
   Edit `.env`:
   ```env
   LLM_MODEL=mistralai/devstral-2512:free  # Faster, free model
   ```

</details>

<details>
<summary><b>📊 Analysis Not Generating</b></summary>

**Symptoms:**
- Progress stops at 60%
- No analysis report
- Empty results page

**Solutions:**

1. **Check Terminal Logs**
   
   Look for error messages in the terminal where you ran `python app.py`

2. **Verify Report Files**
   ```powershell
   # Check if exploration generated output
   dir agent_result.txt
   dir ux_analysis_blocks.json
   ```

3. **API Rate Limits**
   
   If using free tier, you might hit rate limits. Wait a few minutes and try again.

4. **Re-run Analysis Manually**
   ```powershell
   python ux_analyzer.py
   ```

5. **Check Prompt Files**
   
   Ensure all files in `prompts/` folder exist:
   - `agent_goal.txt`
   - `analysis_prompt_v2.txt`
   - `html_generation_prompt.txt`

</details>

<details>
<summary><b>🌐 Browser/UI Issues</b></summary>

**Symptoms:**
- Page not loading
- Logs not showing
- Charts not rendering

**Solutions:**

1. **Clear Browser Cache**
   
   Press `Ctrl + Shift + R` to hard refresh

2. **Check Browser Console**
   
   Press `F12` → Console tab to see JavaScript errors

3. **Try Different Browser**
   
   Chrome/Edge recommended for best compatibility

4. **Check Network Tab**
   
   F12 → Network → Look for failed SSE connections to `/api/progress` or `/api/logs`

5. **Disable Browser Extensions**
   
   Ad blockers might interfere with SSE streams

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
<td width="33%"><b>Monochrome Theme</b></td>
<td width="67%">Clean black & white design with subtle grid pattern background</td>
</tr>
<tr>
<td><b>Rounded Design</b></td>
<td>Consistent border-radius (8px-12px) across all UI elements</td>
</tr>
<tr>
<td><b>Card-Based Layout</b></td>
<td>Professional result cards with headers, badges, descriptions, and metadata</td>
</tr>
<tr>
<td><b>Dual SSE Streams</b></td>
<td>Separate endpoints for progress (<code>/api/progress</code>) and logs (<code>/api/logs</code>)</td>
</tr>
<tr>
<td><b>Agent Reasoning</b></td>
<td>Real-time stdout/stderr capture shows actual LLM chain-of-thought</td>
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

Edit `.env` file:

```env
# Use a different model
LLM_MODEL=anthropic/claude-3.5-sonnet

# Or use OpenAI
LLM_MODEL=openai/gpt-4
LLM_API_BASE=https://api.openai.com/v1
```

**Supported providers:**
- OpenRouter (default) - Multiple models via single API
- OpenAI - Direct GPT models
- Any OpenAI-compatible endpoint

### 📝 Customize Prompts

Edit files in `prompts/` folder:

| File | Purpose | Variables |
|------|---------|----------|
| `agent_goal.txt` | Exploration instructions with 12 data collection categories | `{app_name}`, `{category}` |
| `analysis_prompt_v2.txt` | Professional UX analysis criteria with comprehensive metrics | `{report_content}` |
| `html_generation_prompt.txt` | HTML report generation template | `{report_content}` |

**Note:** JSON examples in prompts must use escaped braces: `{{"key": "value"}}`

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
<td><a href="https://github.com/droidrun/droidrun">DroidRun framework</a></td>
</tr>
<tr>
<td>🔑</td>
<td><a href="https://openrouter.ai">OpenRouter</a> API key (for free LLM access)</td>
</tr>
<tr>
<td>📲</td>
<td>Android device/emulator with app installed</td>
</tr>
</table>

---

## � Common Issues & Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| ❌ "Device not connected" | Run `adb devices` to check, then `droidrun ping` |
| 🔑 "API key not found" | Create `.env` file with `API_KEY=your_key` |
| 🔌 "Port 5000 in use" | Change port in [app.py](app.py): `app.run(port=5001)` |
| 🐌 Slow exploration | Reduce depth slider to 3-5 |
| 📊 No analysis generated | Check terminal logs and verify API key is valid |
| 🌐 UI not loading | Clear cache (`Ctrl+Shift+R`) or try another browser |
| 🐍 Venv won't activate | Run as admin: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| 📱 Wrong app opens | Use display name, not package name (e.g., "Instagram") |

**Still stuck?** See detailed troubleshooting section above ⬆️

---

## �🔚 Deactivate Virtual Environment

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

### Contributors

- **Shashank Bharti** - Core Development
- **Sudhanshu Kumar** - Core Development
- **Sumit Kumar** - Motivational Support🤌🏼

---

<p>
Made with 🫀 by Team LastCrusade 
</p>

</div>
