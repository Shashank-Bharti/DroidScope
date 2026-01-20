"""
Startup verification script for DroidRun UX Tester
Run this before starting the app to check configuration
"""
import os
import sys
import subprocess
from pathlib import Path

def check_droidrun_connection():
    """Check if DroidRun can connect to device"""
    try:
        print("Checking device connection...")
        result = subprocess.run(
            ['droidrun', 'ping'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ Device connected and responsive")
            return True
        else:
            print("❌ Device not connected or not responding!")
            print(f"   Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Device connection timeout!")
        print("   Device is not responding")
        return False
    except FileNotFoundError:
        print("❌ DroidRun command not found!")
        print("   Is DroidRun installed?")
        return False
    except Exception as e:
        print(f"❌ Error checking device: {str(e)}")
        return False

def check_env_file():
    """Check if .env file exists and has API key"""
    env_path = Path('.env')
    if not env_path.exists():
        print("❌ .env file not found!")
        print("   Create a .env file with: API_KEY=your_openrouter_key")
        return False
    
    with open(env_path, 'r') as f:
        content = f.read()
        if 'API_KEY' not in content:
            print("❌ API_KEY not found in .env file!")
            return False
    
    print("✅ .env file configured")
    return True

def check_directories():
    """Check if required directories exist"""
    dirs = ['templates', 'static', 'prompts']
    all_exist = True
    
    for dirname in dirs:
        dir_path = Path(dirname)
        if not dir_path.exists():
            print(f"❌ Directory missing: {dirname}")
            all_exist = False
        else:
            print(f"✅ Directory exists: {dirname}")
    
    return all_exist

def check_prompt_files():
    """Check if prompt files exist"""
    prompts = ['agent_goal.txt', 'analysis_prompt_v2.txt', 'html_generation_prompt.txt']
    all_exist = True
    
    for prompt in prompts:
        prompt_path = Path('prompts') / prompt
        if not prompt_path.exists():
            print(f"❌ Prompt file missing: {prompt}")
            all_exist = False
        else:
            print(f"✅ Prompt file exists: {prompt}")
    
    return all_exist

def check_template_files():
    """Check if template files exist"""
    files = {
        'templates/index.html': 'Frontend template',
        'static/script.js': 'Frontend JavaScript'
    }
    all_exist = True
    
    for filepath, desc in files.items():
        file_path = Path(filepath)
        if not file_path.exists():
            print(f"❌ File missing: {filepath} ({desc})")
            all_exist = False
        else:
            print(f"✅ File exists: {filepath}")
    
    return all_exist

def check_imports():
    """Check if required packages are installed"""
    packages = {
        'flask': 'Flask',
        'dotenv': 'python-dotenv',
        'llama_index': 'llama-index',
        'droidrun': 'DroidRun'
    }
    all_installed = True
    
    for module, package in packages.items():
        try:
            __import__(module)
            print(f"✅ Package installed: {package}")
        except ImportError:
            print(f"❌ Package missing: {package}")
            print(f"   Install with: pip install {package}")
            all_installed = False
    
    return all_installed

def main():
    """Run all checks"""
    print("=" * 60)
    print("DroidRun UX Tester - Startup Verification")
    print("=" * 60 + "\n")
    
    checks = [
        ("Device Connection", check_droidrun_connection),
        ("Environment Configuration", check_env_file),
        ("Directory Structure", check_directories),
        ("Prompt Files", check_prompt_files),
        ("Template Files", check_template_files),
        ("Python Packages", check_imports)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        print(f"\n{check_name}:")
        print("-" * 40)
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL CHECKS PASSED!")
        print("\nYou're ready to start the app:")
        print("  python app.py")
        print("\nThen visit: http://localhost:5000")
    else:
        print("❌ SOME CHECKS FAILED")
        print("\nPlease fix the issues above before starting the app.")
        sys.exit(1)
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
