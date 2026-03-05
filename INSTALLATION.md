# Installation & Setup Guide

## Quick Start (5 Minutes)

### 1. Clone Repository

```bash
git clone https://github.com/demoivresphenomenal-pixel/neuro-genomic-ai.git
cd neuro-genomic-ai
```

### 2. Set Up Python Environment

**Option A: Using pip**
```bash
pip install -r requirements.txt
```

**Option B: Using conda**
```bash
conda create -n neuro-genomic python=3.9
conda activate neuro-genomic
pip install -r requirements.txt
```

**Option C: Using virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Launch Jupyter Notebook

```bash
jupyter notebook notebooks/01_signal_preprocessing_and_analysis.ipynb
```

### 4. Or Use Google Colab (No Installation)

Open this URL directly in your browser:
```
https://colab.research.google.com/github/demoivresphenomenal-pixel/neuro-genomic-ai/blob/main/notebooks/01_signal_preprocessing_and_analysis.ipynb
```

---

## System Requirements

### Minimum
- Python 3.8+
- 2 GB RAM
- 500 MB disk space (without data)

### Recommended
- Python 3.9+
- 8 GB RAM
- 4 GB disk space
- GPU (for future deep learning models)

---

## Package Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| numpy | >=1.21.0 | Numerical computing |
| pandas | >=1.3.0 | Data manipulation |
| scipy | >=1.7.0 | Signal processing |
| scikit-learn | >=0.24.0 | ML algorithms |
| matplotlib | >=3.4.0 | Plotting |
| wfdb | >=4.1.0 | PhysioNet data loading |
| biosppy | >=0.10.0 | ECG analysis |
| plotly | >=5.0.0 | Interactive plots |
| jupyter | >=1.0.0 | Notebooks |
| seaborn | >=0.11.0 | Statistical visualizations |

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'wfdb'`

**Solution:**
```bash
pip install wfdb
```

### Issue: `Could not find a suitable TLS CA certificate bundle`

**Solution (Windows):**
```bash
pip install --upgrade certifi
/Applications/Python\ 3.9/Install\ Certificates.command
```

### Issue: Jupyter notebook not found

**Solution:**
```bash
pip install --upgrade jupyter jupyterlab
python -m jupyter notebook
```

### Issue: Permission denied on Linux/Mac

**Solution:**
```bash
pip install --user --upgrade pip
pip install --user -r requirements.txt
```

---

## Development Setup (For Contributors)

### 1. Clone and Set Up Virtual Environment

```bash
git clone https://github.com/demoivresphenomenal-pixel/neuro-genomic-ai.git
cd neuro-genomic-ai
python -m venv venv
source venv/bin/activate
```

### 2. Install Development Dependencies

```bash
pip install -r requirements.txt
pip install pytest black flake8  # Testing and linting
```

### 3. Run Tests

```bash
pytest tests/
```

### 4. Check Code Quality

```bash
black src/
flake8 src/
```

### 5. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 6. Push Changes

```bash
git add .
git commit -m "feat: description of changes"
git push origin feature/your-feature-name
```

---

## Verify Installation

Run this Python script to verify all packages are installed:

```python
#!/usr/bin/env python
"""Verify neuro-genomic-ai installation."""

import sys

packages = {
    'numpy': 'Numerical computing',
    'pandas': 'Data manipulation',
    'scipy': 'Scientific computing',
    'sklearn': 'Machine learning',
    'matplotlib': 'Plotting',
    'wfdb': 'PhysioNet data',
    'biosppy': 'ECG analysis',
    'plotly': 'Interactive plots',
    'jupyter': 'Notebooks'
}

print("Checking installed packages...\n")

missing = []
for package, purpose in packages.items():
    try:
        __import__(package)
        print(f"✓ {package.ljust(15)} - {purpose}")
    except ImportError:
        print(f"✗ {package.ljust(15)} - {purpose} [MISSING]")
        missing.append(package)

if missing:
    print(f"\n⚠ Missing packages: {', '.join(missing)}")
    print(f"Install with: pip install {' '.join(missing)}")
    sys.exit(1)
else:
    print("\n✓ All packages installed successfully!")
    sys.exit(0)
```

Save as `verify_installation.py` and run:
```bash
python verify_installation.py
```

---

## Environment Variables (Optional)

For production deployment, set these environment variables:

```bash
# Path to PhysioNet data
export PHYSIONET_HOME=/path/to/physionet/data

# API tokens (if using automated download)
export PHYSIONET_USER=your_username
export PHYSIONET_PASSWORD=your_password

# Logging
export LOG_LEVEL=INFO
```

---

## Google Colab Setup

If using Google Colab instead of local installation:

```python
# In first Colab cell:
!git clone https://github.com/demoivresphenomenal-pixel/neuro-genomic-ai.git
%cd neuro-genomic-ai

!pip install -r requirements.txt

# Mount Google Drive for data storage
from google.colab import drive
drive.mount('/content/drive')
```

---

## Docker Setup (Advanced)

For reproducible environments:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root"]
```

Build and run:
```bash
docker build -t neuro-genomic-ai .
docker run -p 8888:8888 -v $(pwd)/data:/app/data neuro-genomic-ai
```

---

## Next Steps

1. ✓ Install packages (this guide)
2. → Open `notebooks/01_signal_preprocessing_and_analysis.ipynb`
3. → Download PhysioNet data (see `docs/PHYSIONET_GUIDE.md`)
4. → Run preprocessing pipeline
5. → Validate results against ground truth
6. → Extend with your modifications

---

## Getting Help

- **Documentation**: Read `docs/` files
- **Code Examples**: See `notebooks/` directory
- **API Reference**: Check docstrings in `src/`
- **Issues**: Create issue on GitHub
- **PhysioNet Help**: https://physionet.org/help/

---

**Last Updated**: March 5, 2026  
**Status**: Ready for use ✓
