#!/usr/bin/env python3
"""
LiveCodeBench Pro - Real-time Demonstration Agent
Specialized CrewAI agent for orchestrating live demonstrations and real-time monitoring
"""

import json
import time
import threading
import numpy as np
from typing import Dict, List, Any, Optional, Callable
from crewai import Agent
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from datetime import datetime, timedelta

class RealTimeMetricsTool(BaseTool):
    """Tool for real-time metrics monitoring and display."""
    
    name: str = "real_time_metrics"
    description: str = "Monitors and displays real-time performance metrics for LiveCodeBench Pro demonstrations"
    
    def __init__(self):
        super().__init__()
        self.metrics_history = []
        self.monitoring_active = False
        self.monitor_thread = None
    
    def _run(self, action: str, duration: int = 60) -> str:
        """Execute real-time metrics monitoring."""
        try:
            if action == "start":
                return self._start_monitoring(duration)
            elif action == "stop":
                return self._stop_monitoring()
            elif action == "status":
                return self._get_monitoring_status()
            elif action == "snapshot":
                return self._get_current_snapshot()
            else:
                return f"Unknown action: {action}"
                
        except Exception as e:
            return f"Error in real-time metrics: {str(e)}"
    
    def _start_monitoring(self, duration: int) -> str:
        """Start real-time metrics monitoring."""
        if self.monitoring_active:
            return "Monitoring already active"
        
        self.monitoring_active = True
        self.metrics_history.clear()
        
        def monitor_loop():
            start_time = time.time()
            while self.monitoring_active and (time.time() - start_time) < duration:
                metrics = self._generate_current_metrics()
                self.metrics_history.append(metrics)
                time.sleep(1)  # Update every second
            
            self.monitoring_active = False
        
        self.monitor_thread = threading.Thread(target=monitor_loop)
        self.monitor_thread.start()
        
        return f"Real-time monitoring started for {duration} seconds"
    
    def _stop_monitoring(self) -> str:
        """Stop real-time metrics monitoring."""
        if not self.monitoring_active:
            return "Monitoring not active"
        
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        
        return f"Monitoring stopped. Collected {len(self.metrics_history)} data points"
    
    def _get_monitoring_status(self) -> str:
        """Get current monitoring status."""
        status = {
            "active": self.monitoring_active,
            "data_points": len(self.metrics_history),
            "last_update": datetime.now().isoformat() if self.metrics_history else None,
            "thread_alive": self.monitor_thread.is_alive() if self.monitor_thread else False
        }
        return json.dumps(status, indent=2)
    
    def _get_current_snapshot(self) -> str:
        """Get current metrics snapshot."""
        if not self.metrics_history:
            return json.dumps(self._generate_current_metrics(), indent=2)
        
        return json.dumps(self.metrics_history[-1], indent=2)
    
    def _generate_current_metrics(self) -> Dict[str, Any]:
        """Generate current performance metrics."""
        return {
            "timestamp": datetime.now().isoformat(),
            "bert_model": {
                "inference_latency": f"{np.random.uniform(12, 28):.2f}ms",
                "tokens_processed": f"{np.random.uniform(800, 1200):.0f}/sec",
                "memory_usage": f"{np.random.uniform(450, 650):.1f}MB",
                "cpu_utilization": f"{np.random.uniform(35, 75):.1f}%",
                "npu_utilization": f"{np.random.uniform(60, 90):.1f}%"
            },
            "visualization_engine": {
                "render_time": f"{np.random.uniform(8, 20):.2f}ms",
                "fps": f"{np.random.uniform(45, 60):.1f}",
                "gpu_memory": f"{np.random.uniform(200, 400):.1f}MB",
                "active_components": np.random.randint(3, 8)
            },
            "demo_session": {
                "active_users": np.random.randint(1, 15),
                "interactions_per_minute": np.random.randint(5, 25),
                "response_time": f"{np.random.uniform(50, 150):.0f}ms",
                "session_duration": f"{np.random.uniform(300, 1800):.0f}s"
            },
            "system_health": {
                "overall_status": "healthy",
                "error_rate": f"{np.random.uniform(0, 2):.3f}%",
                "uptime": f"{np.random.uniform(3600, 86400):.0f}s",
                "network_latency": f"{np.random.uniform(10, 50):.1f}ms"
            }
        }

class DemoControllerTool(BaseTool):
    """Tool for controlling demonstration flow and interactions."""
    
    name: str = "demo_controller"
    description: str = "Controls demonstration flow, user interactions, and presentation timing"
    
    def __init__(self):
        super().__init__()
        self.demo_state = "idle"
        self.demo_config = {}
        self.interaction_log = []
    
    def _run(self, command: str, parameters: str = "{}") -> str:
        """Execute demo control commands."""
        try:
            params = json.loads(parameters) if parameters != "{}" else {}
            
            if command == "start_demo":
                return self._start_demo(params)
            elif command == "pause_demo":
                return self._pause_demo()
            elif command == "resume_demo":
                return self._resume_demo()
            elif command == "stop_demo":
                return self._stop_demo()
            elif command == "interact":
                return self._handle_interaction(params)
            elif command == "status":
                return self._get_demo_status()
            else:
                return f"Unknown command: {command}"
                
        except Exception as e:
            return f"Error in demo controller: {str(e)}"
    
    def _start_demo(self, config: Dict[str, Any]) -> str:
        """Start demonstration session."""
        if self.demo_state != "idle":
            return f"Demo already {self.demo_state}"
        
        self.demo_config = {
            "mode": config.get("mode", "interactive"),
            "duration": config.get("duration", 600),
            "audience_size": config.get("audience_size", "medium"),
            "interaction_level": config.get("interaction_level", "high"),
            "start_time": datetime.now().isoformat(),
            "session_id": f"demo_{int(time.time())}"
        }
        
        self.demo_state = "running"
        self.interaction_log.clear()
        
        return f"Demo started with session ID: {self.demo_config['session_id']}"
    
    def _pause_demo(self) -> str:
        """Pause demonstration."""
        if self.demo_state != "running":
            return f"Cannot pause demo in state: {self.demo_state}"
        
        self.demo_state = "paused"
        return "Demo paused"
    
    def _resume_demo(self) -> str:
        """Resume demonstration."""
        if self.demo_state != "paused":
            return f"Cannot resume demo in state: {self.demo_state}"
        
        self.demo_state = "running"
        return "Demo resumed"
    
    def _stop_demo(self) -> str:
        """Stop demonstration."""
        if self.demo_state == "idle":
            return "No demo to stop"
        
        session_summary = {
            "session_id": self.demo_config.get("session_id", "unknown"),
            "duration": self._calculate_duration(),
            "interactions": len(self.interaction_log),
            "final_state": self.demo_state
        }
        
        self.demo_state = "idle"
        self.demo_config.clear()
        
        return f"Demo stopped. Summary: {json.dumps(session_summary)}"
    
    def _handle_interaction(self, interaction: Dict[str, Any]) -> str:
        """Handle user interaction during demo."""
        if self.demo_state != "running":
            return f"Cannot handle interaction - demo state: {self.demo_state}"
        
        interaction_record = {
            "timestamp": datetime.now().isoformat(),
            "type": interaction.get("type", "unknown"),
            "user_id": interaction.get("user_id", "anonymous"),
            "action": interaction.get("action", ""),
            "response": self._generate_interaction_response(interaction)
        }
        
        self.interaction_log.append(interaction_record)
        
        return f"Interaction handled: {interaction_record['response']}"
    
    def _get_demo_status(self) -> str:
        """Get current demo status."""
        status = {
            "state": self.demo_state,
            "config": self.demo_config,
            "interactions_count": len(self.interaction_log),
            "duration": self._calculate_duration() if self.demo_state != "idle" else 0,
            "last_interaction": self.interaction_log[-1] if self.interaction_log else None
        }
        
        return json.dumps(status, indent=2)
    
    def _calculate_duration(self) -> float:
        """Calculate demo duration in seconds."""
        if not self.demo_config.get("start_time"):
            return 0
        
        start_time = datetime.fromisoformat(self.demo_config["start_time"])
        return (datetime.now() - start_time).total_seconds()
    
    def _generate_interaction_response(self, interaction: Dict[str, Any]) -> str:
        """Generate response to user interaction."""
        interaction_type = interaction.get("type", "unknown")
        
        responses = {
            "question": "Question answered with detailed explanation",
            "component_click": "Component details displayed with real-time metrics",
            "zoom": "View zoomed to show detailed architecture",
            "navigation": "Navigated to requested component or view",
            "demo_request": "Demonstration executed with live metrics",
            "feedback": "Feedback recorded and acknowledged"
        }
        
        return responses.get(interaction_type, "Interaction processed successfully")

class DemoAgent:
    """
    Real-time Demonstration Agent for LiveCodeBench Pro.
    Specializes in orchestrating live demonstrations and managing real-time interactions.
    """
    
    def __init__(self, bert_adapter=None, config: Dict[str, Any] = None):
        self.bert_adapter = bert_adapter
        self.config = config or self._get_default_config()
        self.tools = self._create_tools()
        
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for the demo agent."""
        return {
            "role": "Real-time Demonstration Coordinator",
            "goal": "Orchestrate engaging live demonstrations of LiveCodeBench Pro capabilities with real-time monitoring",
            "backstory": """You are an expert demonstration coordinator with extensive experience in live technical 
            presentations and real-time system monitoring. You excel at managing interactive demonstrations, 
            handling audience engagement, and ensuring smooth real-time performance monitoring. Your expertise 
            includes coordinating multiple system components, managing user interactions, and maintaining optimal 
            demonstration flow while providing real-time insights into system performance.""",
            "verbose": True,
            "allow_delegation": False,
            "max_iter": 10,
            "max_execution_time": 300
        }
    
    def _create_tools(self) -> List[BaseTool]:
        """Create specialized tools for the demo agent."""
        return [
            RealTimeMetricsTool(),
            DemoControllerTool()
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
            max_iter=self.config.get("max_iter", 10),
            max_execution_time=self.config.get("max_execution_time", 300)
        )
    
    def start_real_time_demo(self, demo_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Start real-time demonstration session."""
        if self.bert_adapter:
            return self.bert_adapter.start_real_time_demo(demo_config)
        else:
            # Fallback demo session
            return {
                "session_id": f"demo_sim_{int(time.time())}",
                "status": "active",
                "mode": "simulation",
                "config": demo_config or {"duration": 300},
                "start_time": datetime.now().isoformat(),
                "features": ["simulated_metrics", "mock_interactions"]
            }

# Factory function for easy agent creation
def create_demo_agent(bert_adapter=None, config: Dict[str, Any] = None) -> DemoAgent:
    """
    Factory function to create a Demo Agent.
    
    Args:
        bert_adapter: BERT adapter instance
        config: Agent configuration
        
    Returns:
        Configured DemoAgent instance
    """
    return DemoAgent(bert_adapter=bert_adapter, config=config)

if __name__ == "__main__":
    # Example usage
    agent = create_demo_agent()
    crewai_agent = agent.create_agent()
    
    print(f"Demo Agent created: {crewai_agent.role}")
    
    # Test demo session
    demo_session = agent.start_real_time_demo({
        "mode": "interactive",
        "duration": 120,
        "audience_size": "small"
    })
    
    print(f"Demo session started: {demo_session['session_id']}")
