﻿#!/usr/bin/env python3
"""
LiveCodeBench Pro - Project Setup and Configuration
This script sets up the LiveCodeBench Pro environment with BERT model integration
and CrewAI agent configuration.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class LiveCodeBenchProSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.bert_model_path = self.project_root / "bert-base-uncased-mrpc" / "bert-base-uncased-mrpc" / "huggingface_Intel_bert-base-uncased-mrpc_v1"
        self.venv_path = self.project_root / "livecoder-env"
        
    def verify_environment(self):
        """Verify that the virtual environment and dependencies are properly set up."""
        print("🔍 Verifying environment setup...")
        
        # Check virtual environment
        if not self.venv_path.exists():
            print("❌ Virtual environment not found!")
            return False
            
        # Check BERT model files
        if not self.bert_model_path.exists():
            print("❌ BERT model directory not found!")
            return False
            
        print("✅ Environment verification complete!")
        return True
        
    def setup_bert_integration(self):
        """Set up BERT model integration for LiveCodeBench Pro."""
        print("🤖 Setting up BERT model integration...")
        
        # Create BERT adapter configuration
        bert_config = {
            "model_name": "Intel/bert-base-uncased-mrpc",
            "model_path": str(self.bert_model_path),
            "max_sequence_length": 128,
            "optimization": {
                "quantization": True,
                "openvino": True,
                "qdq_npu": True
            },
            "livecodebensh_pro_adapter": {
                "architecture_visualization": True,
                "real_time_demo": True,
                "interactive_presentation": True
            }
        }
        
        config_path = self.project_root / "bert_livecoder_config.json"
        with open(config_path, 'w') as f:
            json.dump(bert_config, f, indent=2)
            
        print(f"✅ BERT configuration saved to {config_path}")
        
    def create_livecoder_agent_structure(self):
        """Create the basic structure for the LiveCoder AI agent."""
        print("🚀 Creating LiveCoder agent structure...")
        
        # Create agent directories
        agent_dirs = [
            "livecoder_agent",
            "livecoder_agent/tools",
            "livecoder_agent/tasks", 
            "livecoder_agent/crews",
            "livecoder_agent/models",
            "livecoder_agent/gui",
            "livecoder_agent/visualizations"
        ]
        
        for dir_path in agent_dirs:
            (self.project_root / dir_path).mkdir(parents=True, exist_ok=True)
            
        print("✅ Agent directory structure created!")
        
    def setup_gui_framework(self):
        """Set up GUI framework for interactive demonstrations."""
        print("🖥️ Setting up GUI framework...")
        
        # Since Azul is external, we'll use tkinter and matplotlib for now
        gui_requirements = [
            "tkinter",  # Built-in with Python
            "matplotlib",
            "plotly", 
            "dash",
            "streamlit"
        ]
        
        gui_config = {
            "framework": "tkinter_matplotlib",
            "features": {
                "architecture_diagrams": True,
                "real_time_visualizations": True,
                "interactive_demos": True,
                "paper_presentation": True
            },
            "components": {
                "diagram_renderer": "matplotlib",
                "web_interface": "streamlit", 
                "desktop_gui": "tkinter"
            }
        }
        
        config_path = self.project_root / "gui_config.json"
        with open(config_path, 'w') as f:
            json.dump(gui_config, f, indent=2)
            
        print(f"✅ GUI configuration saved to {config_path}")

if __name__ == "__main__":
    setup = LiveCodeBenchProSetup()
    
    print("🎯 Starting LiveCodeBench Pro Setup...")
    print("=" * 50)
    
    if setup.verify_environment():
        setup.setup_bert_integration()
        setup.create_livecoder_agent_structure()
        setup.setup_gui_framework()
        
        print("\n🎉 LiveCodeBench Pro setup completed successfully!")
        print("Next steps:")
        print("1. Run CrewAI crew creation")
        print("2. Configure LiveCoder agent")
        print("3. Build GUI interface")
        print("4. Test architecture demonstrations")
    else:
        print("❌ Setup failed. Please check the environment.")
        sys.exit(1)
