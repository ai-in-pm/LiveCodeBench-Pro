#!/usr/bin/env python3
"""
LiveCodeBench Pro - Main GUI Interface
Azul-compatible GUI framework for LiveCodeBench Pro demonstrations
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import threading
import time
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from livecoder_agent.crews.livecoder_crew import LiveCoderCrew
from livecoder_agent.gui.architecture_viewer import ArchitectureViewer
from livecoder_agent.gui.demo_dashboard import DemoDashboard
from livecoder_agent.gui.presentation_controller import PresentationController

class LiveCodeBenchProGUI:
    """
    Main GUI interface for LiveCodeBench Pro demonstrations.
    Provides Azul-compatible interface design with modern styling.
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.crew = None
        self.demo_session = None
        self.presentation_session = None
        
        # GUI Components
        self.architecture_viewer = None
        self.demo_dashboard = None
        self.presentation_controller = None
        
        # State management
        self.current_mode = "idle"  # idle, demo, presentation
        self.status_updates = []
        
        # Initialize GUI
        self._setup_main_window()
        self._create_menu_bar()
        self._create_main_layout()
        self._create_status_bar()
        self._apply_azul_styling()
        
        # Initialize crew
        self._initialize_crew()
        
    def _setup_main_window(self):
        """Setup main window properties."""
        self.root.title("LiveCodeBench Pro - Architecture Demonstration Platform")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (900 // 2)
        self.root.geometry(f"1400x900+{x}+{y}")
        
        # Configure window icon (if available)
        try:
            self.root.iconbitmap("assets/livecoder_icon.ico")
        except:
            pass  # Icon file not found, continue without it
    
    def _create_menu_bar(self):
        """Create application menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Demo Session", command=self._new_demo_session)
        file_menu.add_command(label="Load Configuration", command=self._load_configuration)
        file_menu.add_command(label="Save Session", command=self._save_session)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._exit_application)
        
        # Demo menu
        demo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Demo", menu=demo_menu)
        demo_menu.add_command(label="Start Architecture Demo", command=self._start_architecture_demo)
        demo_menu.add_command(label="Start Real-time Demo", command=self._start_realtime_demo)
        demo_menu.add_command(label="Start Presentation", command=self._start_presentation)
        demo_menu.add_separator()
        demo_menu.add_command(label="Stop Current Demo", command=self._stop_current_demo)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Architecture Viewer", command=self._show_architecture_viewer)
        view_menu.add_command(label="Demo Dashboard", command=self._show_demo_dashboard)
        view_menu.add_command(label="Presentation Controller", command=self._show_presentation_controller)
        view_menu.add_separator()
        view_menu.add_command(label="Full Screen", command=self._toggle_fullscreen)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="User Guide", command=self._show_user_guide)
        help_menu.add_command(label="Keyboard Shortcuts", command=self._show_shortcuts)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _create_main_layout(self):
        """Create main application layout."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Left sidebar for controls
        self._create_control_sidebar(main_frame)
        
        # Main content area
        self._create_content_area(main_frame)
        
        # Right sidebar for status and metrics
        self._create_status_sidebar(main_frame)
    
    def _create_control_sidebar(self, parent):
        """Create left control sidebar."""
        control_frame = ttk.LabelFrame(parent, text="Demo Controls", padding="10")
        control_frame.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Demo mode selection
        ttk.Label(control_frame, text="Demo Mode:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.demo_mode_var = tk.StringVar(value="architecture")
        demo_modes = [
            ("Architecture Analysis", "architecture"),
            ("Real-time Demo", "realtime"),
            ("Interactive Presentation", "presentation")
        ]
        
        for i, (text, value) in enumerate(demo_modes):
            ttk.Radiobutton(
                control_frame, 
                text=text, 
                variable=self.demo_mode_var, 
                value=value,
                command=self._on_demo_mode_change
            ).grid(row=i+1, column=0, sticky=tk.W, pady=2)
        
        # Demo configuration
        ttk.Separator(control_frame, orient='horizontal').grid(row=5, column=0, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(control_frame, text="Configuration:").grid(row=6, column=0, sticky=tk.W, pady=(0, 5))
        
        # Duration setting
        ttk.Label(control_frame, text="Duration (minutes):").grid(row=7, column=0, sticky=tk.W)
        self.duration_var = tk.StringVar(value="10")
        duration_spinbox = ttk.Spinbox(
            control_frame, 
            from_=1, 
            to=60, 
            textvariable=self.duration_var, 
            width=10
        )
        duration_spinbox.grid(row=8, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Audience size setting
        ttk.Label(control_frame, text="Audience Size:").grid(row=9, column=0, sticky=tk.W, pady=(10, 0))
        self.audience_var = tk.StringVar(value="medium")
        audience_combo = ttk.Combobox(
            control_frame, 
            textvariable=self.audience_var,
            values=["small", "medium", "large"],
            state="readonly",
            width=12
        )
        audience_combo.grid(row=10, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Control buttons
        ttk.Separator(control_frame, orient='horizontal').grid(row=11, column=0, sticky=(tk.W, tk.E), pady=10)
        
        self.start_button = ttk.Button(
            control_frame, 
            text="Start Demo", 
            command=self._start_demo,
            style="Accent.TButton"
        )
        self.start_button.grid(row=12, column=0, sticky=(tk.W, tk.E), pady=2)
        
        self.pause_button = ttk.Button(
            control_frame, 
            text="Pause", 
            command=self._pause_demo,
            state="disabled"
        )
        self.pause_button.grid(row=13, column=0, sticky=(tk.W, tk.E), pady=2)
        
        self.stop_button = ttk.Button(
            control_frame, 
            text="Stop Demo", 
            command=self._stop_demo,
            state="disabled"
        )
        self.stop_button.grid(row=14, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Configure column weight
        control_frame.columnconfigure(0, weight=1)
    
    def _create_content_area(self, parent):
        """Create main content area."""
        content_frame = ttk.Frame(parent)
        content_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Notebook for different views
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Architecture Viewer Tab
        self.architecture_viewer = ArchitectureViewer(self.notebook)
        self.notebook.add(self.architecture_viewer.frame, text="Architecture Viewer")
        
        # Demo Dashboard Tab
        self.demo_dashboard = DemoDashboard(self.notebook)
        self.notebook.add(self.demo_dashboard.frame, text="Demo Dashboard")
        
        # Presentation Controller Tab
        self.presentation_controller = PresentationController(self.notebook)
        self.notebook.add(self.presentation_controller.frame, text="Presentation")
        
        # Bind tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)
    
    def _create_status_sidebar(self, parent):
        """Create right status sidebar."""
        status_frame = ttk.LabelFrame(parent, text="System Status", padding="10")
        status_frame.grid(row=0, column=2, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # Status indicators
        self.crew_status_var = tk.StringVar(value="Initializing...")
        ttk.Label(status_frame, text="Crew Status:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(status_frame, textvariable=self.crew_status_var).grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        self.demo_status_var = tk.StringVar(value="Idle")
        ttk.Label(status_frame, text="Demo Status:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(status_frame, textvariable=self.demo_status_var).grid(row=3, column=0, sticky=tk.W, pady=(0, 10))
        
        # Real-time metrics
        ttk.Separator(status_frame, orient='horizontal').grid(row=4, column=0, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(status_frame, text="Real-time Metrics:").grid(row=5, column=0, sticky=tk.W, pady=(5, 0))
        
        # Metrics display
        self.metrics_text = tk.Text(status_frame, height=15, width=25, wrap=tk.WORD)
        metrics_scrollbar = ttk.Scrollbar(status_frame, orient="vertical", command=self.metrics_text.yview)
        self.metrics_text.configure(yscrollcommand=metrics_scrollbar.set)
        
        self.metrics_text.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        metrics_scrollbar.grid(row=6, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(6, weight=1)
    
    def _create_status_bar(self):
        """Create bottom status bar."""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.status_text = tk.StringVar(value="Ready - LiveCodeBench Pro v1.0")
        ttk.Label(self.status_bar, textvariable=self.status_text).grid(row=0, column=0, sticky=tk.W, padx=10, pady=2)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.status_bar, 
            variable=self.progress_var, 
            maximum=100,
            length=200
        )
        self.progress_bar.grid(row=0, column=1, sticky=tk.E, padx=10, pady=2)
        
        self.status_bar.columnconfigure(0, weight=1)
    
    def _apply_azul_styling(self):
        """Apply Azul-compatible styling to the interface."""
        style = ttk.Style()
        
        # Configure modern theme
        try:
            style.theme_use('clam')  # Use clam theme as base
        except:
            style.theme_use('default')
        
        # Define Azul-inspired color scheme
        colors = {
            'primary': '#2563eb',      # Blue
            'secondary': '#64748b',    # Slate
            'accent': '#059669',       # Emerald
            'background': '#f8fafc',   # Light gray
            'surface': '#ffffff',      # White
            'text': '#1e293b',         # Dark slate
            'text_secondary': '#64748b' # Medium slate
        }
        
        # Configure styles
        style.configure('TFrame', background=colors['background'])
        style.configure('TLabel', background=colors['background'], foreground=colors['text'])
        style.configure('TButton', padding=(10, 5))
        
        # Accent button style
        style.configure(
            'Accent.TButton',
            background=colors['primary'],
            foreground='white',
            padding=(15, 8)
        )
        
        # Configure notebook
        style.configure('TNotebook', background=colors['background'])
        style.configure('TNotebook.Tab', padding=(12, 8))
    
    def _initialize_crew(self):
        """Initialize the LiveCodeBench Pro crew."""
        def init_crew():
            try:
                self.crew = LiveCoderCrew()
                self.root.after(0, lambda: self.crew_status_var.set("Ready"))
                self.root.after(0, lambda: self.status_text.set("Crew initialized successfully"))
            except Exception as e:
                self.root.after(0, lambda: self.crew_status_var.set(f"Error: {str(e)}"))
                self.root.after(0, lambda: self.status_text.set(f"Crew initialization failed: {str(e)}"))
        
        # Initialize crew in background thread
        threading.Thread(target=init_crew, daemon=True).start()
    
    def _start_demo(self):
        """Start demonstration based on selected mode."""
        if not self.crew:
            messagebox.showerror("Error", "Crew not initialized")
            return
        
        mode = self.demo_mode_var.get()
        duration = int(self.duration_var.get()) * 60  # Convert to seconds
        audience_size = self.audience_var.get()
        
        demo_config = {
            "mode": mode,
            "duration": duration,
            "audience_size": audience_size,
            "interaction_level": "high"
        }
        
        def start_demo_thread():
            try:
                self.root.after(0, lambda: self._update_demo_status("Starting..."))
                self.root.after(0, lambda: self._set_demo_buttons_state("running"))
                
                self.demo_session = self.crew.start_demonstration(demo_config)
                
                self.root.after(0, lambda: self._update_demo_status("Running"))
                self.root.after(0, lambda: self.status_text.set(f"Demo started: {self.demo_session['session_id']}"))
                
                # Start metrics updates
                self.root.after(0, self._start_metrics_updates)
                
            except Exception as e:
                self.root.after(0, lambda: self._update_demo_status("Error"))
                self.root.after(0, lambda: messagebox.showerror("Demo Error", str(e)))
                self.root.after(0, lambda: self._set_demo_buttons_state("idle"))
        
        threading.Thread(target=start_demo_thread, daemon=True).start()
    
    def _pause_demo(self):
        """Pause current demonstration."""
        # Implementation for pausing demo
        self._update_demo_status("Paused")
        self._set_demo_buttons_state("paused")
    
    def _stop_demo(self):
        """Stop current demonstration."""
        if self.crew:
            self.crew.shutdown()
        
        self._update_demo_status("Stopped")
        self._set_demo_buttons_state("idle")
        self.status_text.set("Demo stopped")
    
    def _update_demo_status(self, status: str):
        """Update demo status display."""
        self.demo_status_var.set(status)
        self.current_mode = status.lower()
    
    def _set_demo_buttons_state(self, state: str):
        """Set demo control buttons state."""
        if state == "idle":
            self.start_button.config(state="normal")
            self.pause_button.config(state="disabled")
            self.stop_button.config(state="disabled")
        elif state == "running":
            self.start_button.config(state="disabled")
            self.pause_button.config(state="normal")
            self.stop_button.config(state="normal")
        elif state == "paused":
            self.start_button.config(state="normal", text="Resume")
            self.pause_button.config(state="disabled")
            self.stop_button.config(state="normal")
    
    def _start_metrics_updates(self):
        """Start real-time metrics updates."""
        def update_metrics():
            if self.current_mode in ["running", "paused"]:
                # Simulate metrics update
                metrics = {
                    "BERT Latency": "15.2ms",
                    "Throughput": "1,250 ops/sec",
                    "Memory Usage": "512MB",
                    "CPU Usage": "45%",
                    "NPU Usage": "78%"
                }
                
                metrics_text = "\n".join([f"{k}: {v}" for k, v in metrics.items()])
                
                self.metrics_text.delete(1.0, tk.END)
                self.metrics_text.insert(1.0, metrics_text)
                
                # Schedule next update
                self.root.after(1000, update_metrics)
        
        update_metrics()
    
    # Event handlers
    def _on_demo_mode_change(self):
        """Handle demo mode change."""
        mode = self.demo_mode_var.get()
        self.status_text.set(f"Demo mode changed to: {mode}")
    
    def _on_tab_change(self, event):
        """Handle notebook tab change."""
        selected_tab = event.widget.tab('current')['text']
        self.status_text.set(f"Switched to: {selected_tab}")
    
    # Menu handlers
    def _new_demo_session(self):
        """Create new demo session."""
        self.status_text.set("New demo session created")
    
    def _load_configuration(self):
        """Load configuration file."""
        self.status_text.set("Configuration loaded")
    
    def _save_session(self):
        """Save current session."""
        self.status_text.set("Session saved")
    
    def _exit_application(self):
        """Exit application."""
        if self.crew:
            self.crew.shutdown()
        self.root.quit()
    
    def _start_architecture_demo(self):
        """Start architecture demonstration."""
        self.demo_mode_var.set("architecture")
        self._start_demo()
    
    def _start_realtime_demo(self):
        """Start real-time demonstration."""
        self.demo_mode_var.set("realtime")
        self._start_demo()
    
    def _start_presentation(self):
        """Start presentation mode."""
        self.demo_mode_var.set("presentation")
        self._start_demo()
    
    def _stop_current_demo(self):
        """Stop current demonstration."""
        self._stop_demo()
    
    def _show_architecture_viewer(self):
        """Show architecture viewer tab."""
        self.notebook.select(0)
    
    def _show_demo_dashboard(self):
        """Show demo dashboard tab."""
        self.notebook.select(1)
    
    def _show_presentation_controller(self):
        """Show presentation controller tab."""
        self.notebook.select(2)
    
    def _toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))
    
    def _show_user_guide(self):
        """Show user guide."""
        messagebox.showinfo("User Guide", "LiveCodeBench Pro User Guide\n\nComing soon...")
    
    def _show_shortcuts(self):
        """Show keyboard shortcuts."""
        shortcuts = """
        Keyboard Shortcuts:
        
        Ctrl+N - New Demo Session
        Ctrl+O - Load Configuration
        Ctrl+S - Save Session
        F11 - Toggle Fullscreen
        Ctrl+Q - Exit Application
        
        Space - Start/Pause Demo
        Esc - Stop Demo
        """
        messagebox.showinfo("Keyboard Shortcuts", shortcuts)
    
    def _show_about(self):
        """Show about dialog."""
        about_text = """
        LiveCodeBench Pro v1.0
        Architecture Demonstration Platform
        
        Powered by:
        - Intel BERT-base-uncased-MRPC
        - CrewAI Framework
        - Azul GUI Framework
        
        © 2025 LiveCodeBench Pro Team
        """
        messagebox.showinfo("About", about_text)
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()

def main():
    """Main entry point for the GUI application."""
    app = LiveCodeBenchProGUI()
    app.run()

if __name__ == "__main__":
    main()
