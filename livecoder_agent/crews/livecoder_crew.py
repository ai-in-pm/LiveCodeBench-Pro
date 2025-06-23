#!/usr/bin/env python3
"""
LiveCodeBench Pro - Main CrewAI Crew Implementation
Orchestrates the entire LiveCodeBench Pro architecture demonstration system
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
import json

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from livecoder_agent.models.bert_livecoder_adapter import BERTLiveCoderAdapter
from livecoder_agent.crews.architecture_agent import ArchitectureAgent
from livecoder_agent.crews.demo_agent import DemoAgent
from livecoder_agent.crews.presentation_agent import PresentationAgent

class LiveCoderCrew:
    """
    Main CrewAI crew for LiveCodeBench Pro architecture demonstrations.
    Coordinates multiple specialized agents to deliver comprehensive presentations.
    """
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or "bert_livecoder_config.json"
        self.config = self._load_config()
        self.bert_adapter = None
        self.crew = None
        self.agents = {}
        self.tasks = {}
        
        # Initialize BERT adapter
        self._initialize_bert_adapter()
        
        # Create specialized agents
        self._create_agents()
        
        # Define tasks
        self._create_tasks()
        
        # Assemble crew
        self._assemble_crew()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load LiveCodeBench Pro configuration."""
        try:
            config_file = Path(self.config_path)
            if config_file.exists():
                with open(config_file, 'r') as f:
                    return json.load(f)
            else:
                return self._get_default_config()
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return self._get_default_config()
            
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for LiveCodeBench Pro."""
        return {
            "model_name": "Intel/bert-base-uncased-mrpc",
            "max_sequence_length": 128,
            "crew_config": {
                "process": "sequential",
                "verbose": True,
                "memory": True,
                "max_execution_time": 300
            },
            "agents": {
                "architecture_agent": {
                    "role": "Architecture Visualization Specialist",
                    "goal": "Create comprehensive architecture visualizations",
                    "backstory": "Expert in software architecture analysis and visualization"
                },
                "demo_agent": {
                    "role": "Real-time Demonstration Coordinator",
                    "goal": "Orchestrate live demonstrations of system capabilities",
                    "backstory": "Specialist in interactive system demonstrations"
                },
                "presentation_agent": {
                    "role": "Interactive Presentation Manager",
                    "goal": "Manage and deliver engaging presentations",
                    "backstory": "Expert in technical presentation and audience engagement"
                }
            }
        }
        
    def _initialize_bert_adapter(self):
        """Initialize BERT adapter for architecture analysis."""
        try:
            model_path = self.config.get("model_path", "")
            self.bert_adapter = BERTLiveCoderAdapter(
                model_path=model_path,
                config_path=self.config_path
            )
            print("✅ BERT adapter initialized successfully!")
        except Exception as e:
            print(f"❌ Error initializing BERT adapter: {e}")
            
    def _create_agents(self):
        """Create specialized CrewAI agents."""
        agent_configs = self.config.get("agents", {})
        
        # Architecture Visualization Agent
        self.agents["architecture"] = ArchitectureAgent(
            bert_adapter=self.bert_adapter,
            config=agent_configs.get("architecture_agent", {})
        ).create_agent()
        
        # Real-time Demo Agent
        self.agents["demo"] = DemoAgent(
            bert_adapter=self.bert_adapter,
            config=agent_configs.get("demo_agent", {})
        ).create_agent()
        
        # Interactive Presentation Agent
        self.agents["presentation"] = PresentationAgent(
            bert_adapter=self.bert_adapter,
            config=agent_configs.get("presentation_agent", {})
        ).create_agent()
        
        print(f"✅ Created {len(self.agents)} specialized agents!")
        
    def _create_tasks(self):
        """Create tasks for the crew."""
        # Architecture Analysis Task
        self.tasks["architecture_analysis"] = Task(
            description="""
            Analyze the LiveCodeBench Pro architecture and create comprehensive visualizations.
            
            Steps:
            1. Parse the BERT model architecture components
            2. Generate component interaction diagrams
            3. Create real-time performance metrics
            4. Prepare interactive visualization elements
            
            Expected Output: Complete architecture blueprint with visualizations
            """,
            agent=self.agents["architecture"],
            expected_output="Architecture blueprint with component diagrams and metrics"
        )
        
        # Demo Orchestration Task
        self.tasks["demo_orchestration"] = Task(
            description="""
            Orchestrate real-time demonstration of LiveCodeBench Pro capabilities.
            
            Steps:
            1. Initialize demo environment
            2. Configure real-time metrics monitoring
            3. Set up interactive demonstration controls
            4. Prepare audience engagement features
            
            Expected Output: Active demo session with real-time capabilities
            """,
            agent=self.agents["demo"],
            expected_output="Live demo session with interactive controls and metrics",
            context=[self.tasks["architecture_analysis"]]
        )
        
        # Presentation Management Task
        self.tasks["presentation_management"] = Task(
            description="""
            Manage interactive presentation delivery for LiveCodeBench Pro.
            
            Steps:
            1. Integrate architecture visualizations
            2. Coordinate with demo session
            3. Manage audience interaction
            4. Deliver comprehensive presentation
            
            Expected Output: Complete interactive presentation session
            """,
            agent=self.agents["presentation"],
            expected_output="Interactive presentation with audience engagement",
            context=[self.tasks["architecture_analysis"], self.tasks["demo_orchestration"]]
        )
        
        print(f"✅ Created {len(self.tasks)} specialized tasks!")
        
    def _assemble_crew(self):
        """Assemble the complete CrewAI crew."""
        crew_config = self.config.get("crew_config", {})
        
        self.crew = Crew(
            agents=list(self.agents.values()),
            tasks=list(self.tasks.values()),
            process=Process.sequential if crew_config.get("process") == "sequential" else Process.hierarchical,
            verbose=crew_config.get("verbose", True),
            memory=crew_config.get("memory", True),
            max_execution_time=crew_config.get("max_execution_time", 300)
        )
        
        print("✅ LiveCodeBench Pro crew assembled successfully!")
        
    def start_demonstration(self, demo_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Start the complete LiveCodeBench Pro demonstration.
        
        Args:
            demo_config: Configuration for the demonstration
            
        Returns:
            Demonstration results and session information
        """
        if demo_config is None:
            demo_config = {
                "mode": "interactive",
                "duration": 1800,  # 30 minutes
                "audience_size": "medium",
                "interaction_level": "high"
            }
            
        print("🚀 Starting LiveCodeBench Pro demonstration...")
        print("=" * 60)
        
        try:
            # Execute the crew workflow
            results = self.crew.kickoff(inputs={
                "demo_config": demo_config,
                "bert_config": self.config,
                "session_id": f"livecoder_demo_{hash(str(demo_config)) % 10000}"
            })
            
            demonstration_session = {
                "session_id": f"livecoder_demo_{hash(str(demo_config)) % 10000}",
                "status": "completed",
                "config": demo_config,
                "results": results,
                "agents_involved": list(self.agents.keys()),
                "tasks_completed": list(self.tasks.keys()),
                "bert_integration": "active",
                "interactive_features": [
                    "architecture_visualization",
                    "real_time_metrics",
                    "audience_interaction",
                    "live_demonstrations"
                ]
            }
            
            print("🎉 LiveCodeBench Pro demonstration completed successfully!")
            return demonstration_session
            
        except Exception as e:
            print(f"❌ Error during demonstration: {e}")
            return {
                "session_id": "error_session",
                "status": "failed",
                "error": str(e),
                "config": demo_config
            }
            
    def get_crew_status(self) -> Dict[str, Any]:
        """Get current status of the crew and its components."""
        return {
            "crew_assembled": self.crew is not None,
            "agents_count": len(self.agents),
            "tasks_count": len(self.tasks),
            "bert_adapter_status": "active" if self.bert_adapter else "inactive",
            "config_loaded": bool(self.config),
            "agents": list(self.agents.keys()),
            "tasks": list(self.tasks.keys())
        }
        
    def shutdown(self):
        """Gracefully shutdown the crew and cleanup resources."""
        print("🔄 Shutting down LiveCodeBench Pro crew...")
        
        # Cleanup tasks
        self.tasks.clear()
        
        # Cleanup agents
        self.agents.clear()
        
        # Reset crew
        self.crew = None
        
        print("✅ LiveCodeBench Pro crew shutdown complete!")

# Factory function for easy crew creation
def create_livecoder_crew(config_path: str = None) -> LiveCoderCrew:
    """
    Factory function to create a LiveCodeBench Pro crew.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configured LiveCoderCrew instance
    """
    return LiveCoderCrew(config_path=config_path)

if __name__ == "__main__":
    # Example usage
    crew = create_livecoder_crew()
    status = crew.get_crew_status()
    print(f"Crew Status: {status}")
    
    # Start demonstration
    demo_results = crew.start_demonstration({
        "mode": "interactive",
        "duration": 600,  # 10 minutes for testing
        "audience_size": "small",
        "interaction_level": "high"
    })
    
    print(f"Demo Results: {demo_results}")
    
    # Cleanup
    crew.shutdown()
