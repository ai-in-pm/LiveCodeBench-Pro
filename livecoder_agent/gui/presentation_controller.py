#!/usr/bin/env python3
"""
LiveCodeBench Pro - Presentation Controller Component
Interactive presentation management and audience engagement interface
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

class PresentationController:
    """
    Interactive presentation controller for managing LiveCodeBench Pro presentations.
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        
        # Presentation state
        self.presentation_active = False
        self.current_slide = 0
        self.total_slides = 15
        self.presentation_start_time = None
        
        # Presentation content
        self.slides = self._create_sample_slides()
        
        # Audience engagement
        self.qa_active = False
        self.questions = []
        self.polls = {}
        self.feedback = []
        
        self._create_interface()
    
    def _create_interface(self):
        """Create the presentation controller interface."""
        # Main container
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top section - Presentation controls
        self._create_presentation_controls(main_container)
        
        # Middle section - Slide content and navigation
        self._create_slide_section(main_container)
        
        # Bottom section - Audience engagement
        self._create_engagement_section(main_container)
    
    def _create_presentation_controls(self, parent):
        """Create presentation control section."""
        control_frame = ttk.LabelFrame(parent, text="Presentation Control", padding="10")
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Left side - Status and info
        status_frame = ttk.Frame(control_frame)
        status_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Presentation status
        ttk.Label(status_frame, text="Status:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.presentation_status_var = tk.StringVar(value="Ready")
        ttk.Label(status_frame, textvariable=self.presentation_status_var).grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Current slide
        ttk.Label(status_frame, text="Slide:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.slide_info_var = tk.StringVar(value="1 / 15")
        ttk.Label(status_frame, textvariable=self.slide_info_var).grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Duration
        ttk.Label(status_frame, text="Duration:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.presentation_duration_var = tk.StringVar(value="00:00:00")
        ttk.Label(status_frame, textvariable=self.presentation_duration_var).grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Audience size
        ttk.Label(status_frame, text="Audience:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.audience_size_var = tk.StringVar(value="0")
        ttk.Label(status_frame, textvariable=self.audience_size_var).grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Right side - Control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))
        
        self.start_presentation_btn = ttk.Button(
            button_frame, 
            text="Start Presentation", 
            command=self._start_presentation,
            style="Accent.TButton"
        )
        self.start_presentation_btn.pack(pady=2, fill=tk.X)
        
        self.pause_presentation_btn = ttk.Button(
            button_frame, 
            text="Pause", 
            command=self._pause_presentation,
            state="disabled"
        )
        self.pause_presentation_btn.pack(pady=2, fill=tk.X)
        
        self.end_presentation_btn = ttk.Button(
            button_frame, 
            text="End Presentation", 
            command=self._end_presentation,
            state="disabled"
        )
        self.end_presentation_btn.pack(pady=2, fill=tk.X)
        
        ttk.Separator(button_frame, orient='horizontal').pack(fill=tk.X, pady=5)
        
        ttk.Button(
            button_frame, 
            text="Fullscreen", 
            command=self._toggle_fullscreen
        ).pack(pady=2, fill=tk.X)
    
    def _create_slide_section(self, parent):
        """Create slide content and navigation section."""
        slide_frame = ttk.LabelFrame(parent, text="Slide Content & Navigation", padding="10")
        slide_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Navigation controls
        nav_frame = ttk.Frame(slide_frame)
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(nav_frame, text="◀◀ First", command=self._first_slide).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="◀ Previous", command=self._previous_slide).pack(side=tk.LEFT, padx=2)
        
        # Slide number entry
        ttk.Label(nav_frame, text="Go to slide:").pack(side=tk.LEFT, padx=(20, 5))
        self.slide_number_var = tk.StringVar(value="1")
        slide_spinbox = ttk.Spinbox(
            nav_frame, 
            from_=1, 
            to=self.total_slides, 
            textvariable=self.slide_number_var,
            width=5,
            command=self._goto_slide
        )
        slide_spinbox.pack(side=tk.LEFT, padx=2)
        
        ttk.Button(nav_frame, text="Next ▶", command=self._next_slide).pack(side=tk.RIGHT, padx=2)
        ttk.Button(nav_frame, text="Last ▶▶", command=self._last_slide).pack(side=tk.RIGHT, padx=2)
        
        # Slide content area
        content_container = ttk.Frame(slide_frame)
        content_container.pack(fill=tk.BOTH, expand=True)
        
        # Slide preview (left side)
        preview_frame = ttk.LabelFrame(content_container, text="Slide Preview", padding="10")
        preview_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Slide title
        self.slide_title_var = tk.StringVar(value="Welcome to LiveCodeBench Pro")
        title_label = ttk.Label(preview_frame, textvariable=self.slide_title_var, font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Slide content
        self.slide_content = tk.Text(
            preview_frame, 
            height=15, 
            wrap=tk.WORD,
            font=("Arial", 11),
            state="disabled"
        )
        content_scrollbar = ttk.Scrollbar(preview_frame, orient="vertical", command=self.slide_content.yview)
        self.slide_content.configure(yscrollcommand=content_scrollbar.set)
        
        self.slide_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        content_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Slide notes (right side)
        notes_frame = ttk.LabelFrame(content_container, text="Speaker Notes", padding="10")
        notes_frame.pack(side=tk.RIGHT, fill=tk.Y, ipadx=10)
        
        self.slide_notes = tk.Text(
            notes_frame, 
            height=15, 
            width=30,
            wrap=tk.WORD,
            font=("Arial", 10)
        )
        notes_scrollbar = ttk.Scrollbar(notes_frame, orient="vertical", command=self.slide_notes.yview)
        self.slide_notes.configure(yscrollcommand=notes_scrollbar.set)
        
        self.slide_notes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        notes_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load first slide
        self._load_slide(0)
    
    def _create_engagement_section(self, parent):
        """Create audience engagement section."""
        engagement_frame = ttk.LabelFrame(parent, text="Audience Engagement", padding="10")
        engagement_frame.pack(fill=tk.X)
        
        # Create notebook for different engagement features
        engagement_notebook = ttk.Notebook(engagement_frame)
        engagement_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Q&A Tab
        self._create_qa_tab(engagement_notebook)
        
        # Polls Tab
        self._create_polls_tab(engagement_notebook)
        
        # Feedback Tab
        self._create_feedback_tab(engagement_notebook)
    
    def _create_qa_tab(self, parent):
        """Create Q&A management tab."""
        qa_frame = ttk.Frame(parent)
        parent.add(qa_frame, text="Q&A Session")
        
        # Q&A controls
        qa_controls = ttk.Frame(qa_frame)
        qa_controls.pack(fill=tk.X, pady=(0, 10))
        
        self.start_qa_btn = ttk.Button(
            qa_controls, 
            text="Start Q&A", 
            command=self._start_qa
        )
        self.start_qa_btn.pack(side=tk.LEFT, padx=2)
        
        self.end_qa_btn = ttk.Button(
            qa_controls, 
            text="End Q&A", 
            command=self._end_qa,
            state="disabled"
        )
        self.end_qa_btn.pack(side=tk.LEFT, padx=2)
        
        # Q&A status
        self.qa_status_var = tk.StringVar(value="Q&A Inactive")
        ttk.Label(qa_controls, textvariable=self.qa_status_var).pack(side=tk.RIGHT)
        
        # Questions list
        questions_container = ttk.Frame(qa_frame)
        questions_container.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(questions_container, text="Questions:").pack(anchor=tk.W)
        
        # Questions listbox with scrollbar
        questions_frame = ttk.Frame(questions_container)
        questions_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        self.questions_listbox = tk.Listbox(questions_frame, height=6)
        questions_scrollbar = ttk.Scrollbar(questions_frame, orient="vertical", command=self.questions_listbox.yview)
        self.questions_listbox.configure(yscrollcommand=questions_scrollbar.set)
        
        self.questions_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        questions_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Question actions
        question_actions = ttk.Frame(questions_container)
        question_actions.pack(fill=tk.X)
        
        ttk.Button(
            question_actions, 
            text="Answer Selected", 
            command=self._answer_question
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            question_actions, 
            text="Add Sample Question", 
            command=self._add_sample_question
        ).pack(side=tk.LEFT, padx=2)
    
    def _create_polls_tab(self, parent):
        """Create polls management tab."""
        polls_frame = ttk.Frame(parent)
        parent.add(polls_frame, text="Interactive Polls")
        
        # Poll controls
        poll_controls = ttk.Frame(polls_frame)
        poll_controls.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(
            poll_controls, 
            text="Create Poll", 
            command=self._create_poll
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            poll_controls, 
            text="Close Poll", 
            command=self._close_poll
        ).pack(side=tk.LEFT, padx=2)
        
        # Active polls
        ttk.Label(polls_frame, text="Active Polls:").pack(anchor=tk.W)
        
        self.polls_listbox = tk.Listbox(polls_frame, height=8)
        self.polls_listbox.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
    
    def _create_feedback_tab(self, parent):
        """Create feedback management tab."""
        feedback_frame = ttk.Frame(parent)
        parent.add(feedback_frame, text="Audience Feedback")
        
        # Feedback summary
        summary_frame = ttk.Frame(feedback_frame)
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(summary_frame, text="Feedback Summary:").pack(anchor=tk.W)
        
        # Feedback metrics
        metrics_frame = ttk.Frame(summary_frame)
        metrics_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(metrics_frame, text="Total Responses:").grid(row=0, column=0, sticky=tk.W)
        self.feedback_count_var = tk.StringVar(value="0")
        ttk.Label(metrics_frame, textvariable=self.feedback_count_var).grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(metrics_frame, text="Average Rating:").grid(row=1, column=0, sticky=tk.W)
        self.avg_rating_var = tk.StringVar(value="--")
        ttk.Label(metrics_frame, textvariable=self.avg_rating_var).grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        # Feedback list
        ttk.Label(feedback_frame, text="Recent Feedback:").pack(anchor=tk.W, pady=(10, 0))
        
        self.feedback_listbox = tk.Listbox(feedback_frame, height=8)
        self.feedback_listbox.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        # Add sample feedback button
        ttk.Button(
            feedback_frame, 
            text="Add Sample Feedback", 
            command=self._add_sample_feedback
        ).pack()
    
    def _create_sample_slides(self) -> List[Dict[str, Any]]:
        """Create sample presentation slides."""
        return [
            {
                "title": "Welcome to LiveCodeBench Pro",
                "content": """• Advanced Architecture Demonstration Platform
• Intel BERT-base-uncased-MRPC Integration
• Real-time Performance Monitoring
• Interactive Audience Engagement
• CrewAI Framework Orchestration

Today we'll explore how LiveCodeBench Pro revolutionizes architecture demonstrations through intelligent AI integration and real-time visualization capabilities.""",
                "notes": "Welcome the audience and introduce the key features of LiveCodeBench Pro. Emphasize the innovative aspects and real-time capabilities."
            },
            {
                "title": "BERT Model Architecture",
                "content": """• 12-layer Transformer Architecture
• Multi-head Attention Mechanisms
• Intel Optimization (OpenVINO)
• NPU Acceleration Support
• Quantization for Performance

The Intel BERT-base-uncased-MRPC model serves as the foundation for our intelligent code analysis and architecture understanding capabilities.""",
                "notes": "Explain the technical details of the BERT model and how it's optimized for our use case. Mention the performance benefits of Intel optimizations."
            },
            {
                "title": "Component Architecture",
                "content": """• Code Understanding Module (Layers 1-4)
• Pattern Recognition Engine (Layers 5-8)
• Architecture Mapping System (Layers 9-12)
• Visualization Engine (Custom Heads)
• Real-time Demo Pipeline

Each component leverages specific BERT layers for optimal performance and accuracy in their respective domains.""",
                "notes": "Walk through each component and explain how they work together. Use the architecture viewer to show visual representations."
            },
            {
                "title": "Real-time Performance",
                "content": """• Sub-30ms Inference Latency
• 1000+ Operations per Second
• Dynamic Resource Scaling
• Continuous Monitoring
• Adaptive Optimization

Performance metrics are continuously monitored and displayed in real-time during demonstrations.""",
                "notes": "Show the demo dashboard with live metrics. Explain how performance is maintained during live demonstrations."
            },
            {
                "title": "Interactive Features",
                "content": """• Live Architecture Visualization
• Real-time Metrics Dashboard
• Audience Q&A Integration
• Interactive Polls
• Feedback Collection

Engagement features ensure active participation and valuable insights from the audience.""",
                "notes": "Demonstrate the interactive features. Start a Q&A session or create a poll to engage the audience."
            }
        ]
    
    # Presentation control methods
    def _start_presentation(self):
        """Start the presentation."""
        self.presentation_active = True
        self.presentation_start_time = time.time()
        
        # Update UI
        self.presentation_status_var.set("Active")
        self.audience_size_var.set("25")  # Simulated audience
        
        # Update button states
        self.start_presentation_btn.config(state="disabled")
        self.pause_presentation_btn.config(state="normal")
        self.end_presentation_btn.config(state="normal")
        
        # Start duration timer
        self._update_duration()
    
    def _pause_presentation(self):
        """Pause the presentation."""
        self.presentation_active = False
        self.presentation_status_var.set("Paused")
        
        # Update button states
        self.start_presentation_btn.config(state="normal", text="Resume")
        self.pause_presentation_btn.config(state="disabled")
    
    def _end_presentation(self):
        """End the presentation."""
        self.presentation_active = False
        self.presentation_start_time = None
        
        # Update UI
        self.presentation_status_var.set("Ended")
        self.presentation_duration_var.set("00:00:00")
        
        # Update button states
        self.start_presentation_btn.config(state="normal", text="Start Presentation")
        self.pause_presentation_btn.config(state="disabled")
        self.end_presentation_btn.config(state="disabled")
        
        messagebox.showinfo("Presentation Ended", "Presentation has been successfully completed!")
    
    def _toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        # This would integrate with the main window's fullscreen functionality
        pass
    
    def _update_duration(self):
        """Update presentation duration display."""
        if self.presentation_active and self.presentation_start_time:
            duration = time.time() - self.presentation_start_time
            hours = int(duration // 3600)
            minutes = int((duration % 3600) // 60)
            seconds = int(duration % 60)
            duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.presentation_duration_var.set(duration_str)
            
            # Schedule next update
            self.frame.after(1000, self._update_duration)
    
    # Slide navigation methods
    def _first_slide(self):
        """Go to first slide."""
        self.current_slide = 0
        self._load_slide(self.current_slide)
    
    def _previous_slide(self):
        """Go to previous slide."""
        if self.current_slide > 0:
            self.current_slide -= 1
            self._load_slide(self.current_slide)
    
    def _next_slide(self):
        """Go to next slide."""
        if self.current_slide < len(self.slides) - 1:
            self.current_slide += 1
            self._load_slide(self.current_slide)
    
    def _last_slide(self):
        """Go to last slide."""
        self.current_slide = len(self.slides) - 1
        self._load_slide(self.current_slide)
    
    def _goto_slide(self):
        """Go to specific slide number."""
        try:
            slide_num = int(self.slide_number_var.get()) - 1
            if 0 <= slide_num < len(self.slides):
                self.current_slide = slide_num
                self._load_slide(self.current_slide)
        except ValueError:
            pass
    
    def _load_slide(self, slide_index: int):
        """Load slide content."""
        if 0 <= slide_index < len(self.slides):
            slide = self.slides[slide_index]
            
            # Update slide info
            self.slide_info_var.set(f"{slide_index + 1} / {len(self.slides)}")
            self.slide_number_var.set(str(slide_index + 1))
            
            # Update slide content
            self.slide_title_var.set(slide["title"])
            
            self.slide_content.config(state="normal")
            self.slide_content.delete(1.0, tk.END)
            self.slide_content.insert(1.0, slide["content"])
            self.slide_content.config(state="disabled")
            
            # Update speaker notes
            self.slide_notes.delete(1.0, tk.END)
            self.slide_notes.insert(1.0, slide["notes"])
    
    # Engagement methods
    def _start_qa(self):
        """Start Q&A session."""
        self.qa_active = True
        self.qa_status_var.set("Q&A Active")
        
        self.start_qa_btn.config(state="disabled")
        self.end_qa_btn.config(state="normal")
    
    def _end_qa(self):
        """End Q&A session."""
        self.qa_active = False
        self.qa_status_var.set("Q&A Inactive")
        
        self.start_qa_btn.config(state="normal")
        self.end_qa_btn.config(state="disabled")
    
    def _answer_question(self):
        """Answer selected question."""
        selection = self.questions_listbox.curselection()
        if selection:
            question_index = selection[0]
            question = self.questions[question_index]
            question["answered"] = True
            
            # Update display
            self.questions_listbox.delete(question_index)
            self.questions_listbox.insert(question_index, f"✓ {question['text']}")
    
    def _add_sample_question(self):
        """Add a sample question."""
        sample_questions = [
            "How does BERT integration improve performance?",
            "What are the key optimization techniques used?",
            "Can this be deployed in production environments?",
            "How does real-time monitoring work?",
            "What are the hardware requirements?"
        ]
        
        import random
        question_text = random.choice(sample_questions)
        question = {
            "text": question_text,
            "author": "Audience Member",
            "timestamp": datetime.now(),
            "answered": False
        }
        
        self.questions.append(question)
        self.questions_listbox.insert(tk.END, question_text)
    
    def _create_poll(self):
        """Create a new poll."""
        poll_question = "How would you rate this presentation so far?"
        poll_options = ["Excellent", "Good", "Average", "Needs Improvement"]
        
        poll_id = f"poll_{len(self.polls) + 1}"
        poll = {
            "question": poll_question,
            "options": poll_options,
            "votes": {option: 0 for option in poll_options},
            "active": True
        }
        
        self.polls[poll_id] = poll
        self.polls_listbox.insert(tk.END, f"{poll_id}: {poll_question}")
    
    def _close_poll(self):
        """Close selected poll."""
        selection = self.polls_listbox.curselection()
        if selection:
            poll_index = selection[0]
            poll_id = list(self.polls.keys())[poll_index]
            self.polls[poll_id]["active"] = False
            
            # Update display
            current_text = self.polls_listbox.get(poll_index)
            self.polls_listbox.delete(poll_index)
            self.polls_listbox.insert(poll_index, f"[CLOSED] {current_text}")
    
    def _add_sample_feedback(self):
        """Add sample feedback."""
        sample_feedback = [
            {"rating": 5, "comment": "Excellent presentation with great technical depth!"},
            {"rating": 4, "comment": "Very informative, would like more live demos."},
            {"rating": 5, "comment": "Amazing real-time capabilities!"},
            {"rating": 4, "comment": "Good explanation of BERT integration."}
        ]
        
        import random
        feedback = random.choice(sample_feedback)
        feedback["timestamp"] = datetime.now()
        
        self.feedback.append(feedback)
        
        # Update display
        feedback_text = f"★{feedback['rating']}: {feedback['comment']}"
        self.feedback_listbox.insert(0, feedback_text)  # Insert at top
        
        # Update summary
        self.feedback_count_var.set(str(len(self.feedback)))
        avg_rating = sum(f["rating"] for f in self.feedback) / len(self.feedback)
        self.avg_rating_var.set(f"{avg_rating:.1f}")
        
        # Keep only last 20 feedback items
        if len(self.feedback) > 20:
            self.feedback = self.feedback[-20:]
            self.feedback_listbox.delete(20, tk.END)
