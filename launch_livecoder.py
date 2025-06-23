#!/usr/bin/env python3
"""
LiveCodeBench Pro - Simple Launcher
Handles encoding issues and provides better error reporting
"""

import sys
import os
import traceback
from pathlib import Path

def setup_encoding():
    """Setup proper encoding for Windows terminals."""
    if sys.platform == "win32":
        try:
            # Try to set UTF-8 encoding
            import locale
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        except:
            pass
        
        try:
            # Set console code page to UTF-8
            os.system('chcp 65001 > nul')
        except:
            pass

def check_dependencies():
    """Check if basic dependencies are available."""
    print("Checking dependencies...")
    
    required_modules = [
        'json', 'pathlib', 'tkinter', 'threading', 
        'datetime', 'typing', 'dataclasses'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError:
            print(f"✗ {module} - MISSING")
            missing.append(module)
    
    if missing:
        print(f"\nMissing modules: {', '.join(missing)}")
        return False
    
    print("All basic dependencies found!")
    return True

def check_project_structure():
    """Check if project files exist."""
    print("\nChecking project structure...")
    
    required_files = [
        'livecoder_main.py',
        'bert_livecoder_config.json',
        'gui_config.json'
    ]
    
    required_dirs = [
        'livecoder_agent',
        'livecoder_agent/crews',
        'livecoder_agent/gui',
        'livecoder_agent/models'
    ]
    
    missing = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - MISSING")
            missing.append(file_path)
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✓ {dir_path}/")
        else:
            print(f"✗ {dir_path}/ - MISSING")
            missing.append(dir_path)
    
    if missing:
        print(f"\nMissing files/directories: {', '.join(missing)}")
        return False
    
    print("Project structure is complete!")
    return True

def run_simple_test():
    """Run a simple test of core components."""
    print("\nTesting core components...")
    
    try:
        # Test basic imports
        import json
        import tkinter as tk
        print("✓ Basic imports successful")
        
        # Test tkinter
        root = tk.Tk()
        root.withdraw()
        print("✓ GUI framework available")
        root.destroy()
        
        # Test configuration loading
        with open('bert_livecoder_config.json', 'r') as f:
            config = json.load(f)
        print("✓ Configuration files readable")
        
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

def launch_application():
    """Launch the LiveCodeBench Pro application."""
    print("\n" + "="*50)
    print("🚀 Launching LiveCodeBench Pro...")
    print("="*50)
    
    try:
        # Add current directory to Python path
        current_dir = Path(__file__).parent
        sys.path.insert(0, str(current_dir))
        
        # Import and run the main application
        from livecoder_main import LiveCodeBenchProApplication
        
        print("Creating application instance...")
        app = LiveCodeBenchProApplication()
        
        print("Initializing components...")
        if not app.initialize_components():
            print("❌ Component initialization failed")
            return False
        
        print("Starting GUI mode...")
        success = app.run_gui_mode()
        
        if success:
            print("✅ Application completed successfully")
        else:
            print("❌ Application encountered errors")
        
        return success
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\nThis might be due to missing dependencies.")
        print("Try installing requirements: pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        return False

def main():
    """Main launcher function."""
    print("LiveCodeBench Pro Launcher")
    print("=" * 30)
    
    # Setup encoding
    setup_encoding()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed")
        input("Press Enter to exit...")
        return 1
    
    # Check project structure
    if not check_project_structure():
        print("\n❌ Project structure check failed")
        input("Press Enter to exit...")
        return 1
    
    # Run simple test
    if not run_simple_test():
        print("\n❌ Component test failed")
        input("Press Enter to exit...")
        return 1
    
    # Launch application
    try:
        success = launch_application()
        if not success:
            print("\n❌ Application launch failed")
            input("Press Enter to exit...")
            return 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\n🔄 Interrupted by user")
        return 0
    except Exception as e:
        print(f"\n❌ Launcher error: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")
        return 1

if __name__ == "__main__":
    sys.exit(main())
