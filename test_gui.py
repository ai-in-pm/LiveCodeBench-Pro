#!/usr/bin/env python3
"""
Simple GUI Test for LiveCodeBench Pro
Tests if tkinter GUI can display properly
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

def test_simple_gui():
    """Test basic tkinter functionality."""
    print("Testing basic tkinter GUI...")
    
    try:
        # Create root window
        root = tk.Tk()
        root.title("LiveCodeBench Pro - GUI Test")
        root.geometry("600x400")
        
        # Center the window
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (600 // 2)
        y = (root.winfo_screenheight() // 2) - (400 // 2)
        root.geometry(f"600x400+{x}+{y}")
        
        # Make sure window appears on top
        root.lift()
        root.attributes('-topmost', True)
        root.after_idle(lambda: root.attributes('-topmost', False))
        
        # Create content
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="LiveCodeBench Pro - GUI Test", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Status
        status_label = ttk.Label(
            main_frame, 
            text="✅ GUI Framework is working correctly!", 
            font=("Arial", 12)
        )
        status_label.pack(pady=10)
        
        # Test components
        ttk.Label(main_frame, text="Test Components:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(20, 5))
        
        # Button test
        def button_test():
            messagebox.showinfo("Test", "Button clicked successfully!")
        
        ttk.Button(main_frame, text="Test Button", command=button_test).pack(pady=5, fill=tk.X)
        
        # Entry test
        ttk.Label(main_frame, text="Test Input:").pack(anchor=tk.W, pady=(10, 0))
        test_entry = ttk.Entry(main_frame)
        test_entry.pack(fill=tk.X, pady=5)
        test_entry.insert(0, "Type here to test input...")
        
        # Progress bar test
        ttk.Label(main_frame, text="Test Progress Bar:").pack(anchor=tk.W, pady=(10, 0))
        progress = ttk.Progressbar(main_frame, mode='indeterminate')
        progress.pack(fill=tk.X, pady=5)
        progress.start()
        
        # Instructions
        instructions = """
Instructions:
1. If you can see this window, the GUI framework is working
2. Try clicking the "Test Button" 
3. Try typing in the text field
4. Close this window to continue with LiveCodeBench Pro

If this window doesn't appear, there may be a display issue.
        """
        
        text_widget = tk.Text(main_frame, height=8, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        text_widget.insert(1.0, instructions)
        text_widget.config(state=tk.DISABLED)
        
        # Close button
        def close_app():
            root.quit()
            root.destroy()
        
        ttk.Button(main_frame, text="Close and Continue", command=close_app).pack(pady=(10, 0))
        
        print("✅ GUI window created successfully")
        print("🖥️ Window should now be visible on your desktop")
        print("📍 Window position: center of screen")
        print("📏 Window size: 600x400 pixels")
        
        # Start the GUI
        root.mainloop()
        
        print("✅ GUI test completed")
        return True
        
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        return False

def test_display_environment():
    """Test display environment variables."""
    print("\n🖥️ Testing display environment...")
    
    import os
    
    # Check display variables
    display_vars = ['DISPLAY', 'WAYLAND_DISPLAY', 'XDG_SESSION_TYPE']
    
    for var in display_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: {value}")
        else:
            print(f"⚠️ {var}: Not set")
    
    # Check if we're in WSL
    try:
        with open('/proc/version', 'r') as f:
            version_info = f.read()
            if 'microsoft' in version_info.lower() or 'wsl' in version_info.lower():
                print("🐧 Running in WSL (Windows Subsystem for Linux)")
                print("💡 WSL may require X11 forwarding for GUI applications")
                return "wsl"
    except:
        pass
    
    # Check platform
    if sys.platform == "win32":
        print("🪟 Running on Windows")
        return "windows"
    elif sys.platform == "darwin":
        print("🍎 Running on macOS")
        return "macos"
    elif sys.platform.startswith("linux"):
        print("🐧 Running on Linux")
        return "linux"
    
    return "unknown"

def provide_troubleshooting_tips(platform):
    """Provide platform-specific troubleshooting tips."""
    print(f"\n🔧 Troubleshooting tips for {platform}:")
    
    if platform == "windows":
        print("""
Windows Troubleshooting:
1. Make sure you're running from Command Prompt or PowerShell
2. Check if Windows Defender is blocking Python
3. Try running as administrator if needed
4. Ensure Python has permission to create windows
5. Check if any antivirus is blocking GUI applications
        """)
    
    elif platform == "wsl":
        print("""
WSL Troubleshooting:
1. Install an X11 server like VcXsrv or Xming on Windows
2. Set DISPLAY environment variable: export DISPLAY=:0
3. Or use WSL2 with WSLg (Windows 11)
4. Alternative: Run the application directly on Windows Python
        """)
    
    elif platform == "linux":
        print("""
Linux Troubleshooting:
1. Ensure X11 or Wayland is running
2. Check if tkinter is installed: sudo apt-get install python3-tk
3. Verify DISPLAY variable is set correctly
4. Try: xhost +local: (if using X11 forwarding)
        """)
    
    elif platform == "macos":
        print("""
macOS Troubleshooting:
1. Ensure Python was installed with tkinter support
2. Try installing Python from python.org instead of Homebrew
3. Check System Preferences > Security & Privacy
4. Grant Python permission to control the computer if prompted
        """)

def main():
    """Main test function."""
    print("LiveCodeBench Pro - GUI Diagnostic Test")
    print("=" * 40)
    
    # Test display environment
    platform = test_display_environment()
    
    # Provide troubleshooting tips
    provide_troubleshooting_tips(platform)
    
    print("\n" + "=" * 40)
    print("🚀 Starting GUI test...")
    print("=" * 40)
    
    # Test GUI
    success = test_simple_gui()
    
    if success:
        print("\n✅ GUI test completed successfully!")
        print("The GUI framework is working correctly.")
        print("You can now try running LiveCodeBench Pro again.")
    else:
        print("\n❌ GUI test failed!")
        print("There may be an issue with the display environment.")
        print("Please check the troubleshooting tips above.")
    
    return success

if __name__ == "__main__":
    main()
