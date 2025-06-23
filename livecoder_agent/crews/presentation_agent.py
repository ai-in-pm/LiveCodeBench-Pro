#!/usr/bin/env python3
"""
LiveCodeBench Pro - Interactive Presentation Agent
Specialized CrewAI agent for managing interactive presentations and audience engagement
"""

import json
import time
import numpy as np
from typing import Dict, List, Any, Optional
from crewai import Agent
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from datetime import datetime

class PresentationManagerTool(BaseTool):
    """Tool for managing presentation flow and content delivery."""
    
    name: str = "presentation_manager"
    description: str = "Manages presentation flow, slide transitions, and content delivery for LiveCodeBench Pro"
    
    def __init__(self):
        super().__init__()
        self.presentation_state = "idle"
        self.current_slide = 0
        self.presentation_config = {}
        self.slide_history = []
        
    def _run(self, action: str, parameters: str = "{}") -> str:
        """Execute presentation management actions."""
        try:
            params = json.loads(parameters) if parameters != "{}" else {}
            
            if action == "start_presentation":
                return self._start_presentation(params)
            elif action == "next_slide":
                return self._next_slide()
            elif action == "previous_slide":
                return self._previous_slide()
            elif action == "goto_slide":
                return self._goto_slide(params.get("slide_number", 0))
            elif action == "pause_presentation":
                return self._pause_presentation()
            elif action == "resume_presentation":
                return self._resume_presentation()
            elif action == "end_presentation":
                return self._end_presentation()
            elif action == "get_status":
                return self._get_presentation_status()
            else:
                return f"Unknown action: {action}"
                
        except Exception as e:
            return f"Error in presentation manager: {str(e)}"
    
    def _start_presentation(self, config: Dict[str, Any]) -> str:
        """Start presentation session."""
        if self.presentation_state != "idle":
            return f"Presentation already {self.presentation_state}"
        
        self.presentation_config = {
            "title": config.get("title", "LiveCodeBench Pro Architecture"),
            "total_slides": config.get("total_slides", 15),
            "mode": config.get("mode", "interactive"),
            "audience_size": config.get("audience_size", "medium"),
            "start_time": datetime.now().isoformat(),
            "session_id": f"pres_{int(time.time())}"
        }
        
        self.presentation_state = "running"
        self.current_slide = 0
        self.slide_history.clear()
        
        return f"Presentation started: {self.presentation_config['title']}"
    
    def _next_slide(self) -> str:
        """Move to next slide."""
        if self.presentation_state != "running":
            return f"Cannot navigate - presentation state: {self.presentation_state}"
        
        if self.current_slide < self.presentation_config.get("total_slides", 15) - 1:
            self.current_slide += 1
            self._record_slide_transition("next")
            return f"Moved to slide {self.current_slide + 1}"
        else:
            return "Already at last slide"
    
    def _previous_slide(self) -> str:
        """Move to previous slide."""
        if self.presentation_state != "running":
            return f"Cannot navigate - presentation state: {self.presentation_state}"
        
        if self.current_slide > 0:
            self.current_slide -= 1
            self._record_slide_transition("previous")
            return f"Moved to slide {self.current_slide + 1}"
        else:
            return "Already at first slide"
    
    def _goto_slide(self, slide_number: int) -> str:
        """Go to specific slide."""
        if self.presentation_state != "running":
            return f"Cannot navigate - presentation state: {self.presentation_state}"
        
        total_slides = self.presentation_config.get("total_slides", 15)
        if 0 <= slide_number < total_slides:
            self.current_slide = slide_number
            self._record_slide_transition("goto")
            return f"Moved to slide {self.current_slide + 1}"
        else:
            return f"Invalid slide number: {slide_number + 1}"
    
    def _pause_presentation(self) -> str:
        """Pause presentation."""
        if self.presentation_state != "running":
            return f"Cannot pause - presentation state: {self.presentation_state}"
        
        self.presentation_state = "paused"
        return "Presentation paused"
    
    def _resume_presentation(self) -> str:
        """Resume presentation."""
        if self.presentation_state != "paused":
            return f"Cannot resume - presentation state: {self.presentation_state}"
        
        self.presentation_state = "running"
        return "Presentation resumed"
    
    def _end_presentation(self) -> str:
        """End presentation."""
        if self.presentation_state == "idle":
            return "No presentation to end"
        
        summary = {
            "session_id": self.presentation_config.get("session_id", "unknown"),
            "slides_viewed": len(set(h["slide"] for h in self.slide_history)),
            "total_transitions": len(self.slide_history),
            "duration": self._calculate_duration(),
            "final_slide": self.current_slide + 1
        }
        
        self.presentation_state = "idle"
        self.presentation_config.clear()
        
        return f"Presentation ended. Summary: {json.dumps(summary)}"
    
    def _get_presentation_status(self) -> str:
        """Get current presentation status."""
        status = {
            "state": self.presentation_state,
            "current_slide": self.current_slide + 1 if self.presentation_state != "idle" else 0,
            "total_slides": self.presentation_config.get("total_slides", 0),
            "config": self.presentation_config,
            "slide_transitions": len(self.slide_history),
            "duration": self._calculate_duration() if self.presentation_state != "idle" else 0
        }
        
        return json.dumps(status, indent=2)
    
    def _record_slide_transition(self, transition_type: str):
        """Record slide transition for analytics."""
        self.slide_history.append({
            "timestamp": datetime.now().isoformat(),
            "slide": self.current_slide,
            "transition_type": transition_type
        })
    
    def _calculate_duration(self) -> float:
        """Calculate presentation duration in seconds."""
        if not self.presentation_config.get("start_time"):
            return 0
        
        start_time = datetime.fromisoformat(self.presentation_config["start_time"])
        return (datetime.now() - start_time).total_seconds()

class AudienceEngagementTool(BaseTool):
    """Tool for managing audience engagement and interactions."""
    
    name: str = "audience_engagement"
    description: str = "Manages audience engagement, Q&A sessions, and interactive elements"
    
    def __init__(self):
        super().__init__()
        self.engagement_metrics = {}
        self.qa_session = {"active": False, "questions": []}
        self.polls = {}
        self.feedback = []
    
    def _run(self, action: str, parameters: str = "{}") -> str:
        """Execute audience engagement actions."""
        try:
            params = json.loads(parameters) if parameters != "{}" else {}
            
            if action == "start_qa":
                return self._start_qa_session()
            elif action == "end_qa":
                return self._end_qa_session()
            elif action == "add_question":
                return self._add_question(params)
            elif action == "answer_question":
                return self._answer_question(params)
            elif action == "create_poll":
                return self._create_poll(params)
            elif action == "close_poll":
                return self._close_poll(params.get("poll_id"))
            elif action == "collect_feedback":
                return self._collect_feedback(params)
            elif action == "get_engagement_metrics":
                return self._get_engagement_metrics()
            else:
                return f"Unknown action: {action}"
                
        except Exception as e:
            return f"Error in audience engagement: {str(e)}"
    
    def _start_qa_session(self) -> str:
        """Start Q&A session."""
        if self.qa_session["active"]:
            return "Q&A session already active"
        
        self.qa_session = {
            "active": True,
            "start_time": datetime.now().isoformat(),
            "questions": []
        }
        
        return "Q&A session started"
    
    def _end_qa_session(self) -> str:
        """End Q&A session."""
        if not self.qa_session["active"]:
            return "No active Q&A session"
        
        summary = {
            "total_questions": len(self.qa_session["questions"]),
            "answered_questions": len([q for q in self.qa_session["questions"] if q.get("answered")]),
            "duration": self._calculate_qa_duration()
        }
        
        self.qa_session["active"] = False
        
        return f"Q&A session ended. Summary: {json.dumps(summary)}"
    
    def _add_question(self, params: Dict[str, Any]) -> str:
        """Add question to Q&A session."""
        if not self.qa_session["active"]:
            return "No active Q&A session"
        
        question = {
            "id": len(self.qa_session["questions"]) + 1,
            "text": params.get("question", ""),
            "author": params.get("author", "Anonymous"),
            "timestamp": datetime.now().isoformat(),
            "answered": False,
            "answer": None
        }
        
        self.qa_session["questions"].append(question)
        
        return f"Question added with ID: {question['id']}"
    
    def _answer_question(self, params: Dict[str, Any]) -> str:
        """Answer a question from Q&A session."""
        question_id = params.get("question_id")
        answer = params.get("answer", "")
        
        for question in self.qa_session["questions"]:
            if question["id"] == question_id:
                question["answered"] = True
                question["answer"] = answer
                question["answer_timestamp"] = datetime.now().isoformat()
                return f"Question {question_id} answered"
        
        return f"Question {question_id} not found"
    
    def _create_poll(self, params: Dict[str, Any]) -> str:
        """Create interactive poll."""
        poll_id = f"poll_{len(self.polls) + 1}"
        
        poll = {
            "id": poll_id,
            "question": params.get("question", ""),
            "options": params.get("options", []),
            "votes": {option: 0 for option in params.get("options", [])},
            "active": True,
            "created_at": datetime.now().isoformat()
        }
        
        self.polls[poll_id] = poll
        
        return f"Poll created with ID: {poll_id}"
    
    def _close_poll(self, poll_id: str) -> str:
        """Close poll and return results."""
        if poll_id not in self.polls:
            return f"Poll {poll_id} not found"
        
        poll = self.polls[poll_id]
        poll["active"] = False
        poll["closed_at"] = datetime.now().isoformat()
        
        # Simulate some votes
        for option in poll["options"]:
            poll["votes"][option] = np.random.randint(1, 20)
        
        return f"Poll {poll_id} closed. Results: {json.dumps(poll['votes'])}"
    
    def _collect_feedback(self, params: Dict[str, Any]) -> str:
        """Collect audience feedback."""
        feedback_item = {
            "id": len(self.feedback) + 1,
            "rating": params.get("rating", 5),
            "comment": params.get("comment", ""),
            "category": params.get("category", "general"),
            "timestamp": datetime.now().isoformat()
        }
        
        self.feedback.append(feedback_item)
        
        return f"Feedback collected with ID: {feedback_item['id']}"
    
    def _get_engagement_metrics(self) -> str:
        """Get current engagement metrics."""
        metrics = {
            "qa_session": {
                "active": self.qa_session["active"],
                "total_questions": len(self.qa_session["questions"]),
                "answered_questions": len([q for q in self.qa_session["questions"] if q.get("answered")])
            },
            "polls": {
                "total_polls": len(self.polls),
                "active_polls": len([p for p in self.polls.values() if p["active"]])
            },
            "feedback": {
                "total_feedback": len(self.feedback),
                "average_rating": np.mean([f["rating"] for f in self.feedback]) if self.feedback else 0
            },
            "engagement_score": self._calculate_engagement_score()
        }
        
        return json.dumps(metrics, indent=2)
    
    def _calculate_qa_duration(self) -> float:
        """Calculate Q&A session duration."""
        if not self.qa_session.get("start_time"):
            return 0
        
        start_time = datetime.fromisoformat(self.qa_session["start_time"])
        return (datetime.now() - start_time).total_seconds()
    
    def _calculate_engagement_score(self) -> float:
        """Calculate overall engagement score."""
        score = 0
        
        # Q&A engagement
        if self.qa_session["questions"]:
            qa_score = len(self.qa_session["questions"]) * 10
            score += min(qa_score, 50)  # Cap at 50
        
        # Poll engagement
        if self.polls:
            poll_score = len(self.polls) * 15
            score += min(poll_score, 30)  # Cap at 30
        
        # Feedback engagement
        if self.feedback:
            feedback_score = len(self.feedback) * 5
            avg_rating = np.mean([f["rating"] for f in self.feedback])
            score += min(feedback_score + avg_rating * 2, 20)  # Cap at 20
        
        return min(score, 100)  # Total cap at 100

class PresentationAgent:
    """
    Interactive Presentation Agent for LiveCodeBench Pro.
    Specializes in managing presentations and audience engagement.
    """
    
    def __init__(self, bert_adapter=None, config: Dict[str, Any] = None):
        self.bert_adapter = bert_adapter
        self.config = config or self._get_default_config()
        self.tools = self._create_tools()
        
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for the presentation agent."""
        return {
            "role": "Interactive Presentation Manager",
            "goal": "Deliver engaging and interactive presentations of LiveCodeBench Pro with maximum audience engagement",
            "backstory": """You are an expert presentation manager and audience engagement specialist with extensive 
            experience in technical presentations and interactive demonstrations. You excel at managing presentation 
            flow, facilitating Q&A sessions, conducting polls, and maintaining high audience engagement throughout 
            technical presentations. Your expertise includes coordinating with demonstration systems, managing 
            real-time audience interactions, and delivering compelling technical content.""",
            "verbose": True,
            "allow_delegation": False,
            "max_iter": 8,
            "max_execution_time": 240
        }
    
    def _create_tools(self) -> List[BaseTool]:
        """Create specialized tools for the presentation agent."""
        return [
            PresentationManagerTool(),
            AudienceEngagementTool()
        ]
    
    def create_agent(self) -> Agent:
        """Create the CrewAI agent instance."""
        return Agent(
            role=self.config["role"],
            goal=self.config["goal"],
            backstory=self.config["backstory"],
            tools=self.tools,
            verbose=self.config.get("verbose", True),
            allow_delegation=self.config.get("allow_delegation", False),
            max_iter=self.config.get("max_iter", 8),
            max_execution_time=self.config.get("max_execution_time", 240)
        )

# Factory function for easy agent creation
def create_presentation_agent(bert_adapter=None, config: Dict[str, Any] = None) -> PresentationAgent:
    """
    Factory function to create a Presentation Agent.
    
    Args:
        bert_adapter: BERT adapter instance
        config: Agent configuration
        
    Returns:
        Configured PresentationAgent instance
    """
    return PresentationAgent(bert_adapter=bert_adapter, config=config)

if __name__ == "__main__":
    # Example usage
    agent = create_presentation_agent()
    crewai_agent = agent.create_agent()
    
    print(f"Presentation Agent created: {crewai_agent.role}")
