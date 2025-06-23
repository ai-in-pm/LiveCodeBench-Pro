#!/usr/bin/env python3
"""
LiveCodeBench Pro - Demo Dashboard Component
Real-time demonstration monitoring and control interface
"""

import tkinter as tk
from tkinter import ttk
import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class DemoDashboard:
    """
    Real-time demonstration dashboard for monitoring and controlling live demos.
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        
        # Demo state
        self.demo_active = False
        self.demo_start_time = None
        self.metrics_history = []
        self.update_thread = None
        self.stop_updates = False
        
        # Metrics data
        self.current_metrics = {}
        self.performance_data = {
            "timestamps": [],
            "latency": [],
            "throughput": [],
            "memory": [],
            "cpu": [],
            "npu": []
        }
        
        self._create_interface()
        self._start_metrics_simulation()
    
    def _create_interface(self):
        """Create the demo dashboard interface."""
        # Main container
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top section - Demo controls and status
        self._create_demo_controls(main_container)
        
        # Middle section - Real-time metrics
        self._create_metrics_section(main_container)
        
        # Bottom section - Performance charts
        self._create_charts_section(main_container)
    
    def _create_demo_controls(self, parent):
        """Create demo control section."""
        control_frame = ttk.LabelFrame(parent, text="Demo Control & Status", padding="10")
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Left side - Status indicators
        status_frame = ttk.Frame(control_frame)
        status_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Demo status
        ttk.Label(status_frame, text="Demo Status:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.demo_status_var = tk.StringVar(value="Idle")
        status_label = ttk.Label(status_frame, textvariable=self.demo_status_var, font=("Arial", 10))
        status_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Session info
        ttk.Label(status_frame, text="Session ID:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.session_id_var = tk.StringVar(value="--")
        ttk.Label(status_frame, textvariable=self.session_id_var).grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Duration
        ttk.Label(status_frame, text="Duration:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.duration_var = tk.StringVar(value="00:00:00")
        ttk.Label(status_frame, textvariable=self.duration_var).grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Audience info
        ttk.Label(status_frame, text="Active Users:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.users_var = tk.StringVar(value="0")
        ttk.Label(status_frame, textvariable=self.users_var).grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Right side - Control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))
        
        self.start_demo_btn = ttk.Button(
            button_frame, 
            text="Start Demo", 
            command=self._start_demo,
            style="Accent.TButton"
        )
        self.start_demo_btn.pack(pady=2, fill=tk.X)
        
        self.pause_demo_btn = ttk.Button(
            button_frame, 
            text="Pause Demo", 
            command=self._pause_demo,
            state="disabled"
        )
        self.pause_demo_btn.pack(pady=2, fill=tk.X)
        
        self.stop_demo_btn = ttk.Button(
            button_frame, 
            text="Stop Demo", 
            command=self._stop_demo,
            state="disabled"
        )
        self.stop_demo_btn.pack(pady=2, fill=tk.X)
        
        ttk.Separator(button_frame, orient='horizontal').pack(fill=tk.X, pady=5)
        
        ttk.Button(
            button_frame, 
            text="Export Metrics", 
            command=self._export_metrics
        ).pack(pady=2, fill=tk.X)
    
    def _create_metrics_section(self, parent):
        """Create real-time metrics section."""
        metrics_frame = ttk.LabelFrame(parent, text="Real-time Metrics", padding="10")
        metrics_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create metrics grid
        self.metrics_widgets = {}
        
        # BERT Model Metrics
        bert_frame = ttk.LabelFrame(metrics_frame, text="BERT Model", padding="5")
        bert_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        bert_metrics = [
            ("Inference Latency", "bert_latency", "ms"),
            ("Tokens/Second", "bert_throughput", "ops/sec"),
            ("Memory Usage", "bert_memory", "MB"),
            ("Accuracy", "bert_accuracy", "")
        ]
        
        for i, (label, key, unit) in enumerate(bert_metrics):
            ttk.Label(bert_frame, text=f"{label}:").grid(row=i, column=0, sticky=tk.W, pady=1)
            var = tk.StringVar(value="--")
            self.metrics_widgets[key] = var
            ttk.Label(bert_frame, textvariable=var, font=("Arial", 10, "bold")).grid(row=i, column=1, sticky=tk.W, padx=(10, 0), pady=1)
            if unit:
                ttk.Label(bert_frame, text=unit).grid(row=i, column=2, sticky=tk.W, padx=(5, 0), pady=1)
        
        # System Metrics
        system_frame = ttk.LabelFrame(metrics_frame, text="System Performance", padding="5")
        system_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        system_metrics = [
            ("CPU Usage", "cpu_usage", "%"),
            ("NPU Usage", "npu_usage", "%"),
            ("GPU Memory", "gpu_memory", "MB"),
            ("Network Latency", "network_latency", "ms")
        ]
        
        for i, (label, key, unit) in enumerate(system_metrics):
            ttk.Label(system_frame, text=f"{label}:").grid(row=i, column=0, sticky=tk.W, pady=1)
            var = tk.StringVar(value="--")
            self.metrics_widgets[key] = var
            ttk.Label(system_frame, textvariable=var, font=("Arial", 10, "bold")).grid(row=i, column=1, sticky=tk.W, padx=(10, 0), pady=1)
            if unit:
                ttk.Label(system_frame, text=unit).grid(row=i, column=2, sticky=tk.W, padx=(5, 0), pady=1)
        
        # Demo Metrics
        demo_frame = ttk.LabelFrame(metrics_frame, text="Demo Session", padding="5")
        demo_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        demo_metrics = [
            ("Interactions/Min", "interactions", ""),
            ("Response Time", "response_time", "ms"),
            ("Error Rate", "error_rate", "%"),
            ("Uptime", "uptime", "s")
        ]
        
        for i, (label, key, unit) in enumerate(demo_metrics):
            ttk.Label(demo_frame, text=f"{label}:").grid(row=i, column=0, sticky=tk.W, pady=1)
            var = tk.StringVar(value="--")
            self.metrics_widgets[key] = var
            ttk.Label(demo_frame, textvariable=var, font=("Arial", 10, "bold")).grid(row=i, column=1, sticky=tk.W, padx=(10, 0), pady=1)
            if unit:
                ttk.Label(demo_frame, text=unit).grid(row=i, column=2, sticky=tk.W, padx=(5, 0), pady=1)
        
        # Configure grid weights
        metrics_frame.columnconfigure(0, weight=1)
        metrics_frame.columnconfigure(1, weight=1)
        metrics_frame.columnconfigure(2, weight=1)
    
    def _create_charts_section(self, parent):
        """Create performance charts section."""
        charts_frame = ttk.LabelFrame(parent, text="Performance Charts", padding="10")
        charts_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for different charts
        chart_notebook = ttk.Notebook(charts_frame)
        chart_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Performance Overview Chart
        self._create_performance_chart(chart_notebook)
        
        # Resource Usage Chart
        self._create_resource_chart(chart_notebook)
        
        # Demo Analytics Chart
        self._create_analytics_chart(chart_notebook)
    
    def _create_performance_chart(self, parent):
        """Create performance overview chart."""
        perf_frame = ttk.Frame(parent)
        parent.add(perf_frame, text="Performance Overview")
        
        # Create matplotlib figure
        self.perf_fig = Figure(figsize=(10, 4), dpi=100)
        self.perf_ax = self.perf_fig.add_subplot(111)
        
        # Configure chart
        self.perf_ax.set_title("BERT Model Performance")
        self.perf_ax.set_xlabel("Time")
        self.perf_ax.set_ylabel("Latency (ms)")
        self.perf_ax.grid(True, alpha=0.3)
        
        # Create canvas
        self.perf_canvas = FigureCanvasTkAgg(self.perf_fig, perf_frame)
        self.perf_canvas.draw()
        self.perf_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initialize empty plot
        self.perf_line, = self.perf_ax.plot([], [], 'b-', linewidth=2, label='Latency')
        self.perf_ax.legend()
    
    def _create_resource_chart(self, parent):
        """Create resource usage chart."""
        resource_frame = ttk.Frame(parent)
        parent.add(resource_frame, text="Resource Usage")
        
        # Create matplotlib figure
        self.resource_fig = Figure(figsize=(10, 4), dpi=100)
        self.resource_ax = self.resource_fig.add_subplot(111)
        
        # Configure chart
        self.resource_ax.set_title("System Resource Usage")
        self.resource_ax.set_xlabel("Time")
        self.resource_ax.set_ylabel("Usage (%)")
        self.resource_ax.grid(True, alpha=0.3)
        self.resource_ax.set_ylim(0, 100)
        
        # Create canvas
        self.resource_canvas = FigureCanvasTkAgg(self.resource_fig, resource_frame)
        self.resource_canvas.draw()
        self.resource_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initialize empty plots
        self.cpu_line, = self.resource_ax.plot([], [], 'r-', linewidth=2, label='CPU')
        self.npu_line, = self.resource_ax.plot([], [], 'g-', linewidth=2, label='NPU')
        self.resource_ax.legend()
    
    def _create_analytics_chart(self, parent):
        """Create demo analytics chart."""
        analytics_frame = ttk.Frame(parent)
        parent.add(analytics_frame, text="Demo Analytics")
        
        # Create matplotlib figure
        self.analytics_fig = Figure(figsize=(10, 4), dpi=100)
        self.analytics_ax = self.analytics_fig.add_subplot(111)
        
        # Configure chart
        self.analytics_ax.set_title("Demo Session Analytics")
        self.analytics_ax.set_xlabel("Time")
        self.analytics_ax.set_ylabel("Interactions per Minute")
        self.analytics_ax.grid(True, alpha=0.3)
        
        # Create canvas
        self.analytics_canvas = FigureCanvasTkAgg(self.analytics_fig, analytics_frame)
        self.analytics_canvas.draw()
        self.analytics_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initialize empty plot
        self.interactions_line, = self.analytics_ax.plot([], [], 'm-', linewidth=2, label='Interactions')
        self.analytics_ax.legend()
    
    def _start_metrics_simulation(self):
        """Start metrics simulation for demonstration."""
        def update_metrics():
            while not self.stop_updates:
                if self.demo_active:
                    # Generate simulated metrics
                    current_time = time.time()
                    
                    # BERT metrics
                    bert_latency = np.random.uniform(10, 30)
                    bert_throughput = np.random.uniform(800, 1500)
                    bert_memory = np.random.uniform(400, 600)
                    bert_accuracy = np.random.uniform(0.88, 0.96)
                    
                    # System metrics
                    cpu_usage = np.random.uniform(30, 80)
                    npu_usage = np.random.uniform(50, 95)
                    gpu_memory = np.random.uniform(200, 400)
                    network_latency = np.random.uniform(5, 25)
                    
                    # Demo metrics
                    interactions = np.random.randint(5, 30)
                    response_time = np.random.uniform(50, 200)
                    error_rate = np.random.uniform(0, 3)
                    uptime = time.time() - self.demo_start_time if self.demo_start_time else 0
                    
                    # Update metrics display
                    self.frame.after(0, lambda: self._update_metrics_display({
                        "bert_latency": f"{bert_latency:.1f}",
                        "bert_throughput": f"{bert_throughput:.0f}",
                        "bert_memory": f"{bert_memory:.0f}",
                        "bert_accuracy": f"{bert_accuracy:.3f}",
                        "cpu_usage": f"{cpu_usage:.1f}",
                        "npu_usage": f"{npu_usage:.1f}",
                        "gpu_memory": f"{gpu_memory:.0f}",
                        "network_latency": f"{network_latency:.1f}",
                        "interactions": f"{interactions}",
                        "response_time": f"{response_time:.0f}",
                        "error_rate": f"{error_rate:.2f}",
                        "uptime": f"{uptime:.0f}"
                    }))
                    
                    # Update performance data
                    self.performance_data["timestamps"].append(current_time)
                    self.performance_data["latency"].append(bert_latency)
                    self.performance_data["throughput"].append(bert_throughput)
                    self.performance_data["memory"].append(bert_memory)
                    self.performance_data["cpu"].append(cpu_usage)
                    self.performance_data["npu"].append(npu_usage)
                    
                    # Keep only last 100 data points
                    for key in self.performance_data:
                        if len(self.performance_data[key]) > 100:
                            self.performance_data[key] = self.performance_data[key][-100:]
                    
                    # Update charts
                    self.frame.after(0, self._update_charts)
                    
                    # Update duration
                    if self.demo_start_time:
                        duration = time.time() - self.demo_start_time
                        duration_str = str(timedelta(seconds=int(duration)))
                        self.frame.after(0, lambda: self.duration_var.set(duration_str))
                
                time.sleep(1)  # Update every second
        
        self.update_thread = threading.Thread(target=update_metrics, daemon=True)
        self.update_thread.start()
    
    def _update_metrics_display(self, metrics: Dict[str, str]):
        """Update metrics display widgets."""
        for key, value in metrics.items():
            if key in self.metrics_widgets:
                self.metrics_widgets[key].set(value)
    
    def _update_charts(self):
        """Update performance charts."""
        if not self.performance_data["timestamps"]:
            return
        
        # Convert timestamps to relative time
        start_time = self.performance_data["timestamps"][0]
        relative_times = [(t - start_time) / 60 for t in self.performance_data["timestamps"]]  # Convert to minutes
        
        # Update performance chart
        self.perf_line.set_data(relative_times, self.performance_data["latency"])
        self.perf_ax.relim()
        self.perf_ax.autoscale_view()
        self.perf_canvas.draw_idle()
        
        # Update resource chart
        self.cpu_line.set_data(relative_times, self.performance_data["cpu"])
        self.npu_line.set_data(relative_times, self.performance_data["npu"])
        self.resource_ax.relim()
        self.resource_ax.autoscale_view()
        self.resource_canvas.draw_idle()
        
        # Update analytics chart (using interactions as proxy)
        interactions_data = [np.random.randint(5, 30) for _ in relative_times]
        self.interactions_line.set_data(relative_times, interactions_data)
        self.analytics_ax.relim()
        self.analytics_ax.autoscale_view()
        self.analytics_canvas.draw_idle()
    
    # Demo control methods
    def _start_demo(self):
        """Start demonstration."""
        self.demo_active = True
        self.demo_start_time = time.time()
        
        # Update UI
        self.demo_status_var.set("Running")
        self.session_id_var.set(f"demo_{int(time.time())}")
        self.users_var.set(str(np.random.randint(5, 25)))
        
        # Update button states
        self.start_demo_btn.config(state="disabled")
        self.pause_demo_btn.config(state="normal")
        self.stop_demo_btn.config(state="normal")
        
        # Clear previous data
        for key in self.performance_data:
            self.performance_data[key].clear()
    
    def _pause_demo(self):
        """Pause demonstration."""
        self.demo_active = False
        self.demo_status_var.set("Paused")
        
        # Update button states
        self.start_demo_btn.config(state="normal", text="Resume")
        self.pause_demo_btn.config(state="disabled")
    
    def _stop_demo(self):
        """Stop demonstration."""
        self.demo_active = False
        self.demo_start_time = None
        
        # Update UI
        self.demo_status_var.set("Stopped")
        self.session_id_var.set("--")
        self.users_var.set("0")
        self.duration_var.set("00:00:00")
        
        # Update button states
        self.start_demo_btn.config(state="normal", text="Start Demo")
        self.pause_demo_btn.config(state="disabled")
        self.stop_demo_btn.config(state="disabled")
        
        # Clear metrics
        for var in self.metrics_widgets.values():
            var.set("--")
    
    def _export_metrics(self):
        """Export metrics data."""
        if not self.performance_data["timestamps"]:
            return
        
        # Create export data
        export_data = {
            "session_info": {
                "session_id": self.session_id_var.get(),
                "start_time": self.demo_start_time,
                "duration": time.time() - self.demo_start_time if self.demo_start_time else 0
            },
            "performance_data": self.performance_data
        }
        
        # Save to file
        filename = f"demo_metrics_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        print(f"Metrics exported to {filename}")
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        self.stop_updates = True
        if self.update_thread and self.update_thread.is_alive():
            self.update_thread.join(timeout=1)
