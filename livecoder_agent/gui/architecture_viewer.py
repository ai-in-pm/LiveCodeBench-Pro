#!/usr/bin/env python3
"""
LiveCodeBench Pro - Architecture Viewer Component
Interactive architecture visualization panel for the GUI
"""

import tkinter as tk
from tkinter import ttk, canvas
import json
import math
from typing import Dict, List, Any, Optional, Tuple

class ArchitectureViewer:
    """
    Interactive architecture visualization component.
    Displays LiveCodeBench Pro architecture with BERT integration.
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        
        # Architecture data
        self.architecture_data = None
        self.components = {}
        self.connections = []
        self.selected_component = None
        
        # Visualization settings
        self.zoom_level = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.component_colors = {
            "code_understanding": "#3b82f6",      # Blue
            "pattern_recognition": "#10b981",     # Emerald
            "architecture_mapping": "#f59e0b",    # Amber
            "visualization_engine": "#8b5cf6",    # Violet
            "real_time_demo": "#ef4444"           # Red
        }
        
        self._create_interface()
        self._load_sample_architecture()
    
    def _create_interface(self):
        """Create the architecture viewer interface."""
        # Main container
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Toolbar
        self._create_toolbar(main_container)
        
        # Main content area
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Canvas for architecture visualization
        self._create_canvas(content_frame)
        
        # Component details panel
        self._create_details_panel(content_frame)
    
    def _create_toolbar(self, parent):
        """Create toolbar with controls."""
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        # View controls
        ttk.Label(toolbar, text="View:").pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            toolbar, 
            text="Zoom In", 
            command=self._zoom_in,
            width=10
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            toolbar, 
            text="Zoom Out", 
            command=self._zoom_out,
            width=10
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            toolbar, 
            text="Reset View", 
            command=self._reset_view,
            width=10
        ).pack(side=tk.LEFT, padx=2)
        
        # Separator
        ttk.Separator(toolbar, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Component controls
        ttk.Label(toolbar, text="Components:").pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            toolbar, 
            text="Show All", 
            command=self._show_all_components,
            width=10
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            toolbar, 
            text="Hide Details", 
            command=self._hide_component_details,
            width=10
        ).pack(side=tk.LEFT, padx=2)
        
        # Animation controls
        ttk.Separator(toolbar, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        ttk.Label(toolbar, text="Animation:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.animation_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            toolbar, 
            text="Data Flow", 
            variable=self.animation_var,
            command=self._toggle_animation
        ).pack(side=tk.LEFT, padx=2)
        
        # Zoom level display
        self.zoom_label = ttk.Label(toolbar, text="Zoom: 100%")
        self.zoom_label.pack(side=tk.RIGHT, padx=(10, 0))
    
    def _create_canvas(self, parent):
        """Create canvas for architecture visualization."""
        canvas_frame = ttk.Frame(parent)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Canvas with scrollbars
        self.canvas = tk.Canvas(
            canvas_frame, 
            bg='white', 
            highlightthickness=1,
            highlightbackground='#cccccc'
        )
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and canvas
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind events
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<B1-Motion>", self._on_canvas_drag)
        self.canvas.bind("<MouseWheel>", self._on_canvas_scroll)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Set scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _create_details_panel(self, parent):
        """Create component details panel."""
        details_frame = ttk.LabelFrame(parent, text="Component Details", padding="10")
        details_frame.pack(side=tk.RIGHT, fill=tk.Y, ipadx=10)
        
        # Component name
        self.component_name_var = tk.StringVar(value="Select a component")
        ttk.Label(details_frame, textvariable=self.component_name_var, font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # Component description
        ttk.Label(details_frame, text="Description:").pack(anchor=tk.W)
        self.description_text = tk.Text(details_frame, height=4, width=30, wrap=tk.WORD)
        self.description_text.pack(fill=tk.X, pady=(2, 10))
        
        # BERT integration info
        ttk.Label(details_frame, text="BERT Integration:").pack(anchor=tk.W)
        self.bert_info_text = tk.Text(details_frame, height=3, width=30, wrap=tk.WORD)
        self.bert_info_text.pack(fill=tk.X, pady=(2, 10))
        
        # Performance metrics
        ttk.Label(details_frame, text="Performance Metrics:").pack(anchor=tk.W)
        self.metrics_frame = ttk.Frame(details_frame)
        self.metrics_frame.pack(fill=tk.X, pady=(2, 10))
        
        # Create metrics labels
        self.metrics_labels = {}
        metrics = ["Latency", "Throughput", "Memory", "Accuracy"]
        for i, metric in enumerate(metrics):
            ttk.Label(self.metrics_frame, text=f"{metric}:").grid(row=i, column=0, sticky=tk.W, pady=1)
            self.metrics_labels[metric] = ttk.Label(self.metrics_frame, text="--")
            self.metrics_labels[metric].grid(row=i, column=1, sticky=tk.W, padx=(10, 0), pady=1)
        
        # Interactive features
        ttk.Label(details_frame, text="Interactive Features:").pack(anchor=tk.W, pady=(10, 0))
        self.features_listbox = tk.Listbox(details_frame, height=4, width=30)
        self.features_listbox.pack(fill=tk.X, pady=(2, 10))
        
        # Action buttons
        button_frame = ttk.Frame(details_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            button_frame, 
            text="Highlight Component", 
            command=self._highlight_component
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            button_frame, 
            text="Show Data Flow", 
            command=self._show_data_flow
        ).pack(fill=tk.X, pady=2)
        
        ttk.Button(
            button_frame, 
            text="Performance Details", 
            command=self._show_performance_details
        ).pack(fill=tk.X, pady=2)
    
    def _load_sample_architecture(self):
        """Load sample architecture data."""
        self.architecture_data = {
            "title": "LiveCodeBench Pro Architecture",
            "components": {
                "code_understanding": {
                    "position": {"x": 100, "y": 100},
                    "size": {"width": 120, "height": 80},
                    "description": "BERT encoder layers 1-4 for code tokenization and understanding",
                    "bert_layers": "1-4",
                    "metrics": {
                        "Latency": "12.5ms",
                        "Throughput": "1,200 ops/sec",
                        "Memory": "180MB",
                        "Accuracy": "0.945"
                    },
                    "features": ["Token highlighting", "Syntax analysis", "Code parsing"]
                },
                "pattern_recognition": {
                    "position": {"x": 300, "y": 100},
                    "size": {"width": 120, "height": 80},
                    "description": "BERT encoder layers 5-8 for pattern detection and similarity analysis",
                    "bert_layers": "5-8",
                    "metrics": {
                        "Latency": "18.3ms",
                        "Throughput": "950 ops/sec",
                        "Memory": "220MB",
                        "Accuracy": "0.912"
                    },
                    "features": ["Pattern matching", "Similarity heatmap", "Cluster analysis"]
                },
                "architecture_mapping": {
                    "position": {"x": 500, "y": 100},
                    "size": {"width": 120, "height": 80},
                    "description": "BERT encoder layers 9-12 for component relationship mapping",
                    "bert_layers": "9-12",
                    "metrics": {
                        "Latency": "22.1ms",
                        "Throughput": "800 ops/sec",
                        "Memory": "250MB",
                        "Accuracy": "0.889"
                    },
                    "features": ["Component mapping", "Dependency analysis", "Hierarchy building"]
                },
                "visualization_engine": {
                    "position": {"x": 200, "y": 250},
                    "size": {"width": 120, "height": 80},
                    "description": "Custom attention heads for interactive visualization",
                    "bert_layers": "Custom heads",
                    "metrics": {
                        "Latency": "8.7ms",
                        "Throughput": "1,500 ops/sec",
                        "Memory": "150MB",
                        "Accuracy": "0.967"
                    },
                    "features": ["Interactive canvas", "Real-time rendering", "User controls"]
                },
                "real_time_demo": {
                    "position": {"x": 400, "y": 250},
                    "size": {"width": 120, "height": 80},
                    "description": "Streaming inference pipeline for live demonstrations",
                    "bert_layers": "All layers",
                    "metrics": {
                        "Latency": "35.2ms",
                        "Throughput": "600 ops/sec",
                        "Memory": "450MB",
                        "Accuracy": "0.923"
                    },
                    "features": ["Live streaming", "Real-time metrics", "Audience interaction"]
                }
            },
            "connections": [
                {"from": "code_understanding", "to": "pattern_recognition", "type": "data_flow"},
                {"from": "pattern_recognition", "to": "architecture_mapping", "type": "analysis_flow"},
                {"from": "code_understanding", "to": "visualization_engine", "type": "render_flow"},
                {"from": "pattern_recognition", "to": "visualization_engine", "type": "render_flow"},
                {"from": "architecture_mapping", "to": "visualization_engine", "type": "render_flow"},
                {"from": "visualization_engine", "to": "real_time_demo", "type": "display_flow"}
            ]
        }
        
        self._draw_architecture()
    
    def _draw_architecture(self):
        """Draw the architecture on canvas."""
        self.canvas.delete("all")
        
        if not self.architecture_data:
            return
        
        # Draw connections first (so they appear behind components)
        self._draw_connections()
        
        # Draw components
        self._draw_components()
        
        # Update scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _draw_components(self):
        """Draw architecture components."""
        components = self.architecture_data.get("components", {})
        
        for name, component in components.items():
            pos = component["position"]
            size = component["size"]
            color = self.component_colors.get(name, "#6b7280")
            
            # Apply zoom and pan
            x = (pos["x"] + self.pan_x) * self.zoom_level
            y = (pos["y"] + self.pan_y) * self.zoom_level
            w = size["width"] * self.zoom_level
            h = size["height"] * self.zoom_level
            
            # Draw component rectangle
            rect_id = self.canvas.create_rectangle(
                x, y, x + w, y + h,
                fill=color,
                outline="#374151",
                width=2,
                tags=(name, "component")
            )
            
            # Draw component label
            text_id = self.canvas.create_text(
                x + w/2, y + h/2,
                text=name.replace("_", "\n").title(),
                fill="white",
                font=("Arial", int(10 * self.zoom_level), "bold"),
                tags=(name, "component_text")
            )
            
            # Store component info
            self.components[name] = {
                "rect_id": rect_id,
                "text_id": text_id,
                "data": component
            }
    
    def _draw_connections(self):
        """Draw connections between components."""
        connections = self.architecture_data.get("connections", [])
        components = self.architecture_data.get("components", {})
        
        for connection in connections:
            from_comp = components.get(connection["from"])
            to_comp = components.get(connection["to"])
            
            if not from_comp or not to_comp:
                continue
            
            # Calculate connection points
            from_pos = from_comp["position"]
            from_size = from_comp["size"]
            to_pos = to_comp["position"]
            to_size = to_comp["size"]
            
            # Apply zoom and pan
            x1 = (from_pos["x"] + from_size["width"]/2 + self.pan_x) * self.zoom_level
            y1 = (from_pos["y"] + from_size["height"]/2 + self.pan_y) * self.zoom_level
            x2 = (to_pos["x"] + to_size["width"]/2 + self.pan_x) * self.zoom_level
            y2 = (to_pos["y"] + to_size["height"]/2 + self.pan_y) * self.zoom_level
            
            # Draw arrow
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill="#6b7280",
                width=int(2 * self.zoom_level),
                arrow=tk.LAST,
                arrowshape=(16, 20, 6),
                tags="connection"
            )
    
    def _on_canvas_click(self, event):
        """Handle canvas click events."""
        # Find clicked component
        clicked_items = self.canvas.find_overlapping(event.x-5, event.y-5, event.x+5, event.y+5)
        
        for item in clicked_items:
            tags = self.canvas.gettags(item)
            for tag in tags:
                if tag in self.components:
                    self._select_component(tag)
                    return
        
        # No component clicked, deselect
        self._deselect_component()
    
    def _on_canvas_drag(self, event):
        """Handle canvas drag events for panning."""
        # Implementation for panning would go here
        pass
    
    def _on_canvas_scroll(self, event):
        """Handle canvas scroll events for zooming."""
        if event.delta > 0:
            self._zoom_in()
        else:
            self._zoom_out()
    
    def _on_canvas_configure(self, event):
        """Handle canvas resize events."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _select_component(self, component_name: str):
        """Select and highlight a component."""
        self.selected_component = component_name
        
        # Update details panel
        component_data = self.components[component_name]["data"]
        
        self.component_name_var.set(component_name.replace("_", " ").title())
        
        # Update description
        self.description_text.delete(1.0, tk.END)
        self.description_text.insert(1.0, component_data.get("description", ""))
        
        # Update BERT info
        self.bert_info_text.delete(1.0, tk.END)
        bert_info = f"BERT Layers: {component_data.get('bert_layers', 'N/A')}"
        self.bert_info_text.insert(1.0, bert_info)
        
        # Update metrics
        metrics = component_data.get("metrics", {})
        for metric, label in self.metrics_labels.items():
            label.config(text=metrics.get(metric, "--"))
        
        # Update features
        self.features_listbox.delete(0, tk.END)
        features = component_data.get("features", [])
        for feature in features:
            self.features_listbox.insert(tk.END, feature)
        
        # Highlight component on canvas
        self._highlight_selected_component()
    
    def _deselect_component(self):
        """Deselect current component."""
        self.selected_component = None
        self.component_name_var.set("Select a component")
        
        # Clear details
        self.description_text.delete(1.0, tk.END)
        self.bert_info_text.delete(1.0, tk.END)
        
        for label in self.metrics_labels.values():
            label.config(text="--")
        
        self.features_listbox.delete(0, tk.END)
        
        # Remove highlight
        self._remove_highlight()
    
    def _highlight_selected_component(self):
        """Highlight the selected component."""
        if not self.selected_component:
            return
        
        component = self.components[self.selected_component]
        rect_id = component["rect_id"]
        
        # Change outline to highlight color
        self.canvas.itemconfig(rect_id, outline="#fbbf24", width=4)
    
    def _remove_highlight(self):
        """Remove component highlight."""
        for component in self.components.values():
            self.canvas.itemconfig(component["rect_id"], outline="#374151", width=2)
    
    # Toolbar event handlers
    def _zoom_in(self):
        """Zoom in on the architecture."""
        self.zoom_level = min(self.zoom_level * 1.2, 3.0)
        self._update_zoom_display()
        self._draw_architecture()
    
    def _zoom_out(self):
        """Zoom out on the architecture."""
        self.zoom_level = max(self.zoom_level / 1.2, 0.3)
        self._update_zoom_display()
        self._draw_architecture()
    
    def _reset_view(self):
        """Reset view to default zoom and position."""
        self.zoom_level = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self._update_zoom_display()
        self._draw_architecture()
    
    def _update_zoom_display(self):
        """Update zoom level display."""
        zoom_percent = int(self.zoom_level * 100)
        self.zoom_label.config(text=f"Zoom: {zoom_percent}%")
    
    def _show_all_components(self):
        """Show all components."""
        self._draw_architecture()
    
    def _hide_component_details(self):
        """Hide component details."""
        self._deselect_component()
    
    def _toggle_animation(self):
        """Toggle data flow animation."""
        if self.animation_var.get():
            self._start_animation()
        else:
            self._stop_animation()
    
    def _start_animation(self):
        """Start data flow animation."""
        # Implementation for animation would go here
        pass
    
    def _stop_animation(self):
        """Stop data flow animation."""
        # Implementation for stopping animation would go here
        pass
    
    # Detail panel event handlers
    def _highlight_component(self):
        """Highlight the selected component."""
        if self.selected_component:
            self._highlight_selected_component()
    
    def _show_data_flow(self):
        """Show data flow for the selected component."""
        if self.selected_component:
            # Implementation for showing data flow
            pass
    
    def _show_performance_details(self):
        """Show detailed performance information."""
        if self.selected_component:
            # Implementation for showing performance details
            pass
