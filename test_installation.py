#!/usr/bin/env python3
"""
LiveCodeBench Pro - Installation Test Script
Verifies that all components are properly installed and configured
"""

import sys
import os
import json
from pathlib import Path

def test_python_version():
    """Test Python version compatibility."""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def test_project_structure():
    """Test project directory structure."""
    print("\n📁 Testing project structure...")
    
    required_dirs = [
        "livecoder_agent",
        "livecoder_agent/crews",
        "livecoder_agent/tasks", 
        "livecoder_agent/tools",
        "livecoder_agent/models",
        "livecoder_agent/gui",
        "livecoder_agent/visualizations"
    ]
    
    required_files = [
        "livecoder_main.py",
        "livecoder_project_setup.py",
        "requirements.txt",
        "README.md",
        "bert_livecoder_config.json",
        "gui_config.json"
    ]
    
    all_good = True
    
    # Check directories
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ Directory: {dir_path}")
        else:
            print(f"❌ Missing directory: {dir_path}")
            all_good = False
    
    # Check files
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ File: {file_path}")
        else:
            print(f"❌ Missing file: {file_path}")
            all_good = False
    
    return all_good

def test_configuration_files():
    """Test configuration file validity."""
    print("\n⚙️ Testing configuration files...")
    
    configs_to_test = [
        "bert_livecoder_config.json",
        "gui_config.json"
    ]
    
    all_good = True
    
    for config_file in configs_to_test:
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            print(f"✅ Valid JSON: {config_file}")
        except FileNotFoundError:
            print(f"❌ Missing config: {config_file}")
            all_good = False
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in {config_file}: {e}")
            all_good = False
    
    return all_good

def test_core_imports():
    """Test core module imports."""
    print("\n📦 Testing core module imports...")
    
    modules_to_test = [
        ("json", "JSON processing"),
        ("pathlib", "Path handling"),
        ("tkinter", "GUI framework"),
        ("threading", "Threading support"),
        ("datetime", "Date/time handling"),
        ("typing", "Type hints"),
        ("dataclasses", "Data classes"),
        ("abc", "Abstract base classes")
    ]
    
    all_good = True
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name} - {description}")
        except ImportError as e:
            print(f"❌ {module_name} - {description}: {e}")
            all_good = False
    
    return all_good

def test_livecoder_imports():
    """Test LiveCodeBench Pro module imports."""
    print("\n🚀 Testing LiveCodeBench Pro module imports...")
    
    # Add current directory to Python path
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    modules_to_test = [
        ("livecoder_agent.models.bert_livecoder_adapter", "BERT Adapter"),
        ("livecoder_agent.crews.architecture_agent", "Architecture Agent"),
        ("livecoder_agent.crews.demo_agent", "Demo Agent"),
        ("livecoder_agent.crews.presentation_agent", "Presentation Agent"),
        ("livecoder_agent.gui.main_interface", "Main GUI Interface"),
        ("livecoder_agent.gui.architecture_viewer", "Architecture Viewer"),
        ("livecoder_agent.gui.demo_dashboard", "Demo Dashboard"),
        ("livecoder_agent.gui.presentation_controller", "Presentation Controller")
    ]
    
    all_good = True
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name} - {description}")
        except ImportError as e:
            print(f"❌ {module_name} - {description}: {e}")
            all_good = False
        except Exception as e:
            print(f"⚠️ {module_name} - {description}: {e}")
            # Don't fail for other exceptions (like missing dependencies)
    
    return all_good

def test_bert_model_path():
    """Test BERT model path configuration."""
    print("\n🤖 Testing BERT model configuration...")
    
    try:
        with open("bert_livecoder_config.json", 'r') as f:
            config = json.load(f)
        
        model_path = config.get("model_path", "")
        if model_path and Path(model_path).exists():
            print(f"✅ BERT model path exists: {model_path}")
            return True
        else:
            print(f"⚠️ BERT model path not found: {model_path}")
            print("   This is expected if BERT model hasn't been downloaded yet")
            return True  # Don't fail for missing model
            
    except Exception as e:
        print(f"❌ Error checking BERT model path: {e}")
        return False

def test_virtual_environment():
    """Test virtual environment setup."""
    print("\n🔧 Testing virtual environment...")
    
    venv_path = Path("livecoder-env")
    if venv_path.exists():
        print(f"✅ Virtual environment directory exists: {venv_path}")
        
        # Check for key venv files
        venv_files = ["pyvenv.cfg", "Scripts" if os.name == "nt" else "bin"]
        for venv_file in venv_files:
            if (venv_path / venv_file).exists():
                print(f"✅ Virtual environment component: {venv_file}")
            else:
                print(f"⚠️ Missing virtual environment component: {venv_file}")
        
        return True
    else:
        print(f"⚠️ Virtual environment not found: {venv_path}")
        print("   Run setup to create virtual environment")
        return True  # Don't fail for missing venv

def test_gui_components():
    """Test GUI component creation."""
    print("\n🖥️ Testing GUI components...")
    
    try:
        # Test tkinter availability
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the window
        print("✅ Tkinter GUI framework available")
        root.destroy()
        
        # Test matplotlib for charts
        try:
            import matplotlib
            matplotlib.use('Agg')  # Use non-interactive backend
            print("✅ Matplotlib visualization library available")
        except ImportError:
            print("⚠️ Matplotlib not available - charts may not work")
        
        return True
        
    except ImportError as e:
        print(f"❌ GUI framework not available: {e}")
        return False
    except Exception as e:
        print(f"⚠️ GUI test warning: {e}")
        return True

def run_all_tests():
    """Run all installation tests."""
    print("🎯 LiveCodeBench Pro Installation Test")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("Project Structure", test_project_structure),
        ("Configuration Files", test_configuration_files),
        ("Core Imports", test_core_imports),
        ("LiveCodeBench Imports", test_livecoder_imports),
        ("BERT Model Path", test_bert_model_path),
        ("Virtual Environment", test_virtual_environment),
        ("GUI Components", test_gui_components)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! LiveCodeBench Pro is ready to use.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run setup: python livecoder_main.py --setup")
        print("3. Launch application: python livecoder_main.py")
    else:
        print(f"\n⚠️ {total - passed} tests failed. Please check the issues above.")
        print("\nTroubleshooting:")
        print("1. Ensure Python 3.8+ is installed")
        print("2. Check that all files were created properly")
        print("3. Verify configuration files are valid JSON")
        print("4. Install missing dependencies")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
