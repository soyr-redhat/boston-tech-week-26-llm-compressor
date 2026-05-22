# Workshop Notebook Instructions

## For Participants

The easiest way to participate in the workshop is using the Jupyter notebook. It works on **all platforms** (Windows, Mac, Linux) and requires **minimal setup**.

### Option 1: Google Colab (Recommended - Zero Setup)

**Perfect for everyone, especially if you:**
- Want zero installation
- Are on Windows
- Have limited Python experience
- Just want things to work

**Steps:**

1. Click this button:

   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/soyr-redhat/boston-tech-week-26-llm-compressor/blob/main/workshop_notebook.ipynb)

2. Sign in with your Google account (if not already)

3. Run cells in order by clicking the play button or pressing `Shift+Enter`

4. Follow along with the instructor

**Benefits:**
- No installation required
- Free GPU access (not needed for this workshop, but cool)
- Works in any browser
- Saves your progress automatically

### Option 2: Local Jupyter

**Good for those who:**
- Have Python already installed
- Prefer to work offline
- Want to keep everything local

**Steps:**

```bash
# 1. Install Jupyter (if not already installed)
pip install notebook

# 2. Download the notebook
curl -O https://raw.githubusercontent.com/soyr-redhat/boston-tech-week-26-llm-compressor/main/workshop_notebook.ipynb

# Or using wget:
# wget https://raw.githubusercontent.com/soyr-redhat/boston-tech-week-26-llm-compressor/main/workshop_notebook.ipynb

# 3. Start Jupyter
jupyter notebook workshop_notebook.ipynb
```

Your browser will open automatically with the notebook.

### Option 3: JupyterLab (Advanced)

If you prefer JupyterLab over Jupyter Notebook:

```bash
pip install jupyterlab
jupyter lab workshop_notebook.ipynb
```

## Troubleshooting

### "Command not found: jupyter"

Make sure Python's bin directory is in your PATH:

```bash
# Mac/Linux
export PATH="$HOME/.local/bin:$PATH"

# Windows (PowerShell)
$env:PATH += ";$env:LOCALAPPDATA\Programs\Python\Python3XX\Scripts"
```

### Can't install Jupyter

Use Google Colab instead - it requires zero installation!

### Notebook won't open in browser

Manually navigate to the URL shown in your terminal (usually `http://localhost:8888`)

### Import errors in the notebook

The first cell installs all dependencies. Make sure to run it and wait for it to complete before running other cells.

## What's in the Notebook?

The notebook includes:

1. **Part 1:** Quantization fundamentals and theory
2. **Part 2:** Setup and imports
3. **Part 3:** Benchmark original FP16 model
4. **Part 4:** Benchmark quantized INT4 model
5. **Part 5:** Compare results in a table
6. **Part 6:** Visualize performance with charts
7. **Part 7:** Advanced load testing (optional)
8. **Part 8:** View detailed HTML reports
9. **Summary:** Key takeaways and next steps

Each section has:
- Explanation text (markdown cells)
- Executable code (code cells)
- Example outputs

## Tips

- **Run cells in order** - Later cells depend on earlier ones
- **Wait for cells to complete** - Don't skip ahead while a cell is running
- **Feel free to experiment** - Modify parameters and re-run cells
- **Save your work** - Google Colab auto-saves, local Jupyter needs manual save (Ctrl+S)

## After the Workshop

You can:
- Download the notebook with results (File > Download)
- Share it with colleagues
- Modify it for your own models
- Use it as a template for other benchmarks

## Questions?

Ask during the workshop or open an issue on [GitHub](https://github.com/soyr-redhat/boston-tech-week-26-llm-compressor/issues)!
