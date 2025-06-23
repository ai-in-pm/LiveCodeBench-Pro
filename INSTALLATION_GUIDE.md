# LiveCodeBench Pro - Installation Guide

## 🚀 Quick Start Installation

### Step 1: Verify Prerequisites

**System Requirements:**
- Windows 10/11, Linux, or macOS
- Python 3.8 or higher
- 8GB+ RAM (16GB recommended)
- 5GB+ free disk space

**Check Python Version:**
```bash
python --version
# Should show Python 3.8.x or higher
```

### Step 2: Test Current Installation

Run the installation test to verify everything is set up correctly:

```bash
python test_installation.py
```

This will check:
- ✅ Python version compatibility
- ✅ Project structure integrity
- ✅ Configuration file validity
- ✅ Core module imports
- ✅ LiveCodeBench Pro components
- ✅ GUI framework availability

### Step 3: Install Dependencies

If you haven't already, install the required Python packages:

```bash
# Create and activate virtual environment (recommended)
python -m venv livecoder-env

# Windows
livecoder-env\Scripts\activate

# Linux/macOS
source livecoder-env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Run Initial Setup

```bash
python livecoder_main.py --setup
```

This will:
- Verify environment setup
- Configure BERT integration
- Create agent directory structure
- Set up GUI framework

### Step 5: Launch Application

```bash
# GUI Mode (default)
python livecoder_main.py

# CLI Mode
python livecoder_main.py --mode cli

# Demo Mode
python livecoder_main.py --mode demo --demo-type architecture
```

## 📋 Detailed Installation Steps

### 1. Environment Setup

**Create Virtual Environment:**
```bash
python -m venv livecoder-env
```

**Activate Virtual Environment:**
```bash
# Windows
livecoder-env\Scripts\activate

# Linux/macOS
source livecoder-env/bin/activate
```

**Verify Activation:**
```bash
which python  # Should point to virtual environment
pip list       # Should show minimal packages
```

### 2. Dependency Installation

**Core Dependencies:**
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install core packages individually
pip install torch transformers numpy
pip install crewai crewai-tools
pip install matplotlib plotly tkinter
pip install openvino intel-extension-for-pytorch
```

**Optional Dependencies:**
```bash
# For development
pip install pytest black flake8 mypy

# For advanced features
pip install streamlit dash jupyter
pip install opencv-python pillow
```

### 3. Configuration

**BERT Model Configuration:**

Edit `bert_livecoder_config.json`:
```json
{
  "model_name": "Intel/bert-base-uncased-mrpc",
  "model_path": "path/to/your/bert/model",
  "max_sequence_length": 128,
  "optimization": {
    "quantization": true,
    "openvino": true,
    "qdq_npu": true
  }
}
```

**GUI Configuration:**

Edit `gui_config.json`:
```json
{
  "framework": "tkinter_matplotlib",
  "features": {
    "architecture_diagrams": true,
    "real_time_visualizations": true,
    "interactive_demos": true
  }
}
```

### 4. BERT Model Setup

**Download Intel BERT Model:**
```bash
# Using Hugging Face CLI
huggingface-cli download Intel/bert-base-uncased-mrpc

# Or using Python
python -c "
from transformers import BertModel, BertTokenizer
model = BertModel.from_pretrained('Intel/bert-base-uncased-mrpc')
tokenizer = BertTokenizer.from_pretrained('Intel/bert-base-uncased-mrpc')
print('BERT model downloaded successfully')
"
```

### 5. Verification

**Run Installation Test:**
```bash
python test_installation.py
```

**Test Core Components:**
```bash
# Test BERT adapter
python -c "
from livecoder_agent.models.bert_livecoder_adapter import BERTLiveCoderAdapter
adapter = BERTLiveCoderAdapter('', 'bert_livecoder_config.json')
print('BERT adapter test passed')
"

# Test GUI components
python -c "
from livecoder_agent.gui.main_interface import LiveCodeBenchProGUI
print('GUI components test passed')
"
```

## 🔧 Troubleshooting

### Common Issues

**1. Python Version Error**
```
Error: Python 3.8+ required
Solution: Install Python 3.8 or higher from python.org
```

**2. Module Import Errors**
```
Error: ModuleNotFoundError: No module named 'crewai'
Solution: pip install -r requirements.txt
```

**3. BERT Model Not Found**
```
Error: BERT model directory not found
Solution: Download model or update model_path in config
```

**4. GUI Framework Issues**
```
Error: tkinter not available
Solution: Install tkinter (usually included with Python)
```

**5. Permission Errors**
```
Error: Permission denied
Solution: Run with appropriate permissions or use virtual environment
```

### Platform-Specific Issues

**Windows:**
- Install Visual C++ Build Tools if compilation errors occur
- Use PowerShell or Command Prompt, not Git Bash
- Ensure Windows Defender doesn't block Python execution

**Linux:**
- Install python3-tk for tkinter support: `sudo apt-get install python3-tk`
- Install development headers: `sudo apt-get install python3-dev`

**macOS:**
- Install Xcode Command Line Tools: `xcode-select --install`
- Use Homebrew Python if system Python causes issues

### Performance Optimization

**Intel CPU Optimization:**
```bash
# Install Intel Extension for PyTorch
pip install intel-extension-for-pytorch

# Install OpenVINO
pip install openvino
```

**GPU Acceleration:**
```bash
# For NVIDIA GPUs
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For AMD GPUs
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.4.2
```

## 📊 Verification Checklist

- [ ] Python 3.8+ installed and accessible
- [ ] Virtual environment created and activated
- [ ] All dependencies installed successfully
- [ ] Configuration files are valid JSON
- [ ] BERT model path is configured correctly
- [ ] GUI framework (tkinter) is available
- [ ] Installation test passes all checks
- [ ] Application launches without errors

## 🎯 Next Steps

After successful installation:

1. **Explore the GUI**: Launch with `python livecoder_main.py`
2. **Try CLI Mode**: Run `python livecoder_main.py --mode cli`
3. **Run Demos**: Test different demo types
4. **Customize Configuration**: Adjust settings for your use case
5. **Read Documentation**: Check README.md for detailed usage

## 📞 Getting Help

If you encounter issues:

1. **Check the troubleshooting section above**
2. **Run the installation test**: `python test_installation.py`
3. **Check system requirements and dependencies**
4. **Review error messages carefully**
5. **Create an issue on GitHub with detailed error information**

## 🔄 Updating

To update LiveCodeBench Pro:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run setup again
python livecoder_main.py --setup

# Test installation
python test_installation.py
```

---

**LiveCodeBench Pro Installation Guide** - Get up and running quickly with comprehensive architecture demonstrations!
