#!/usr/bin/env python3
"""
LiveCodeBench Pro - Main Application Entry Point
Comprehensive architecture demonstration platform with BERT integration and CrewAI orchestration
"""

import os
import sys
import argparse
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import LiveCodeBench Pro components
try:
    from livecoder_agent.crews.livecoder_crew import LiveCoderCrew, create_livecoder_crew
    from livecoder_agent.gui.main_interface import LiveCodeBenchProGUI
    from livecoder_agent.models.bert_livecoder_adapter import BERTLiveCoderAdapter
    from livecoder_project_setup import LiveCodeBenchProSetup
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all dependencies are installed and the project structure is correct.")
    sys.exit(1)

class LiveCodeBenchProApplication:
    """
    Main application class for LiveCodeBench Pro.
    Coordinates all components and provides multiple execution modes.
    """
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or "bert_livecoder_config.json"
        self.config = self._load_configuration()
        self.setup_logging()
        
        # Core components
        self.crew = None
        self.gui = None
        self.bert_adapter = None
        
        # Application state
        self.mode = "gui"  # gui, cli, headless, demo
        self.demo_session = None
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("LiveCodeBench Pro Application initialized")
    
    def _load_configuration(self) -> Dict[str, Any]:
        """Load application configuration."""
        try:
            config_file = Path(self.config_path)
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                print(f"✅ Configuration loaded from {self.config_path}")
                return config
            else:
                print(f"⚠️ Configuration file not found: {self.config_path}")
                return self._get_default_configuration()
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            return self._get_default_configuration()
    
    def _get_default_configuration(self) -> Dict[str, Any]:
        """Get default application configuration."""
        return {
            "application": {
                "name": "LiveCodeBench Pro",
                "version": "1.0.0",
                "mode": "gui",
                "log_level": "INFO"
            },
            "model_name": "Intel/bert-base-uncased-mrpc",
            "max_sequence_length": 128,
            "optimization": {
                "quantization": True,
                "openvino": True,
                "qdq_npu": True
            },
            "crew_config": {
                "process": "sequential",
                "verbose": True,
                "memory": True,
                "max_execution_time": 300
            },
            "gui_config": {
                "theme": "azul",
                "fullscreen": False,
                "auto_start_demo": False
            },
            "demo_defaults": {
                "mode": "interactive",
                "duration": 600,
                "audience_size": "medium",
                "interaction_level": "high"
            }
        }
    
    def setup_logging(self):
        """Setup application logging."""
        log_level = self.config.get("application", {}).get("log_level", "INFO")
        
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('livecoder_pro.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def initialize_components(self):
        """Initialize all application components."""
        self.logger.info("Initializing LiveCodeBench Pro components...")
        
        try:
            # Initialize BERT adapter
            self._initialize_bert_adapter()
            
            # Initialize CrewAI crew
            self._initialize_crew()
            
            # Initialize GUI (if in GUI mode)
            if self.mode == "gui":
                self._initialize_gui()
            
            self.logger.info("✅ All components initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Component initialization failed: {e}")
            return False
    
    def _initialize_bert_adapter(self):
        """Initialize BERT adapter."""
        try:
            model_path = self.config.get("model_path", "")
            self.bert_adapter = BERTLiveCoderAdapter(
                model_path=model_path,
                config_path=self.config_path
            )
            self.logger.info("✅ BERT adapter initialized")
        except Exception as e:
            self.logger.warning(f"⚠️ BERT adapter initialization failed: {e}")
            self.bert_adapter = None
    
    def _initialize_crew(self):
        """Initialize CrewAI crew."""
        try:
            self.crew = create_livecoder_crew(config_path=self.config_path)
            self.logger.info("✅ CrewAI crew initialized")
        except Exception as e:
            self.logger.error(f"❌ CrewAI crew initialization failed: {e}")
            raise
    
    def _initialize_gui(self):
        """Initialize GUI interface."""
        try:
            self.gui = LiveCodeBenchProGUI()
            self.logger.info("✅ GUI interface initialized")
        except Exception as e:
            self.logger.error(f"❌ GUI initialization failed: {e}")
            raise
    
    def run_gui_mode(self):
        """Run application in GUI mode."""
        self.logger.info("🚀 Starting LiveCodeBench Pro in GUI mode...")
        
        if not self.gui:
            self.logger.error("❌ GUI not initialized")
            return False
        
        try:
            # Auto-start demo if configured
            if self.config.get("gui_config", {}).get("auto_start_demo", False):
                self._auto_start_demo()
            
            # Start GUI main loop
            self.gui.run()
            return True
            
        except Exception as e:
            self.logger.error(f"❌ GUI execution failed: {e}")
            return False
    
    def run_cli_mode(self, demo_config: Dict[str, Any] = None):
        """Run application in CLI mode."""
        self.logger.info("🚀 Starting LiveCodeBench Pro in CLI mode...")
        
        if not self.crew:
            self.logger.error("❌ Crew not initialized")
            return False
        
        try:
            # Use provided config or defaults
            config = demo_config or self.config.get("demo_defaults", {})
            
            print("\n" + "="*60)
            print("🎯 LiveCodeBench Pro - CLI Demonstration")
            print("="*60)
            
            # Start demonstration
            demo_session = self.crew.start_demonstration(config)
            
            print(f"\n✅ Demo session started: {demo_session['session_id']}")
            print(f"📊 Status: {demo_session['status']}")
            print(f"🎮 Mode: {config.get('mode', 'interactive')}")
            print(f"⏱️ Duration: {config.get('duration', 600)} seconds")
            
            # Display results
            if demo_session.get("results"):
                print(f"\n📋 Results:")
                print(json.dumps(demo_session["results"], indent=2))
            
            print("\n🎉 CLI demonstration completed!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ CLI execution failed: {e}")
            return False
    
    def run_headless_mode(self, demo_config: Dict[str, Any] = None):
        """Run application in headless mode."""
        self.logger.info("🚀 Starting LiveCodeBench Pro in headless mode...")
        
        if not self.crew:
            self.logger.error("❌ Crew not initialized")
            return False
        
        try:
            config = demo_config or self.config.get("demo_defaults", {})
            
            # Start demonstration
            demo_session = self.crew.start_demonstration(config)
            
            self.logger.info(f"Demo session started: {demo_session['session_id']}")
            self.logger.info(f"Status: {demo_session['status']}")
            
            # Save results to file
            results_file = f"demo_results_{demo_session['session_id']}.json"
            with open(results_file, 'w') as f:
                json.dump(demo_session, f, indent=2)
            
            self.logger.info(f"Results saved to: {results_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Headless execution failed: {e}")
            return False
    
    def run_demo_mode(self, demo_type: str = "architecture"):
        """Run application in demo mode with specific demo type."""
        self.logger.info(f"🚀 Starting LiveCodeBench Pro demo: {demo_type}")
        
        demo_configs = {
            "architecture": {
                "mode": "architecture",
                "duration": 900,  # 15 minutes
                "audience_size": "large",
                "interaction_level": "high"
            },
            "realtime": {
                "mode": "realtime",
                "duration": 600,  # 10 minutes
                "audience_size": "medium",
                "interaction_level": "high"
            },
            "presentation": {
                "mode": "presentation",
                "duration": 1800,  # 30 minutes
                "audience_size": "large",
                "interaction_level": "medium"
            }
        }
        
        config = demo_configs.get(demo_type, demo_configs["architecture"])
        return self.run_cli_mode(config)
    
    def _auto_start_demo(self):
        """Auto-start demo if configured."""
        try:
            demo_config = self.config.get("demo_defaults", {})
            if self.crew:
                self.demo_session = self.crew.start_demonstration(demo_config)
                self.logger.info(f"Auto-started demo: {self.demo_session['session_id']}")
        except Exception as e:
            self.logger.warning(f"Auto-start demo failed: {e}")
    
    def shutdown(self):
        """Gracefully shutdown the application."""
        self.logger.info("🔄 Shutting down LiveCodeBench Pro...")
        
        try:
            # Shutdown crew
            if self.crew:
                self.crew.shutdown()
                self.logger.info("✅ Crew shutdown complete")
            
            # Cleanup GUI
            if self.gui:
                # GUI cleanup handled by tkinter
                pass
            
            self.logger.info("✅ LiveCodeBench Pro shutdown complete")
            
        except Exception as e:
            self.logger.error(f"❌ Shutdown error: {e}")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="LiveCodeBench Pro - Architecture Demonstration Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python livecoder_main.py                          # Start GUI mode
  python livecoder_main.py --mode cli               # Start CLI mode
  python livecoder_main.py --mode demo --demo-type architecture
  python livecoder_main.py --mode headless --config custom_config.json
        """
    )
    
    parser.add_argument(
        "--mode", 
        choices=["gui", "cli", "headless", "demo"],
        default="gui",
        help="Application execution mode (default: gui)"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file"
    )
    
    parser.add_argument(
        "--demo-type",
        choices=["architecture", "realtime", "presentation"],
        default="architecture",
        help="Type of demonstration (for demo mode)"
    )
    
    parser.add_argument(
        "--duration",
        type=int,
        help="Demo duration in seconds"
    )
    
    parser.add_argument(
        "--audience-size",
        choices=["small", "medium", "large"],
        help="Expected audience size"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Run initial setup and configuration"
    )
    
    return parser.parse_args()

def run_setup():
    """Run initial setup and configuration."""
    print("🎯 Running LiveCodeBench Pro Setup...")
    print("=" * 50)
    
    try:
        setup = LiveCodeBenchProSetup()
        
        if setup.verify_environment():
            setup.setup_bert_integration()
            setup.create_livecoder_agent_structure()
            setup.setup_gui_framework()
            
            print("\n🎉 LiveCodeBench Pro setup completed successfully!")
            print("You can now run the application with: python livecoder_main.py")
            return True
        else:
            print("❌ Setup failed. Please check the environment.")
            return False
            
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return False

def main():
    """Main entry point for LiveCodeBench Pro."""
    args = parse_arguments()
    
    # Run setup if requested
    if args.setup:
        return run_setup()
    
    # Create application instance
    app = LiveCodeBenchProApplication(config_path=args.config)
    
    # Override config with command line arguments
    if args.duration:
        app.config.setdefault("demo_defaults", {})["duration"] = args.duration
    
    if args.audience_size:
        app.config.setdefault("demo_defaults", {})["audience_size"] = args.audience_size
    
    if args.verbose:
        app.config.setdefault("application", {})["log_level"] = "DEBUG"
        app.setup_logging()
    
    # Set application mode
    app.mode = args.mode
    
    try:
        # Initialize components
        if not app.initialize_components():
            print("❌ Component initialization failed")
            return 1
        
        # Run application based on mode
        success = False
        
        if args.mode == "gui":
            success = app.run_gui_mode()
        elif args.mode == "cli":
            success = app.run_cli_mode()
        elif args.mode == "headless":
            success = app.run_headless_mode()
        elif args.mode == "demo":
            success = app.run_demo_mode(args.demo_type)
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n🔄 Interrupted by user")
        return 0
    except Exception as e:
        print(f"❌ Application error: {e}")
        return 1
    finally:
        app.shutdown()

if __name__ == "__main__":
    sys.exit(main())
