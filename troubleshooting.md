Troubleshooting
Issue 1: ModuleNotFoundError: No module named 'pandas' (or numpy, seaborn, matplotlib)
Symptoms:
ERROR: Unknown compiler(s): [['icl'], ['cl'], ['cc'], ['gcc']...]
× pip subprocess to install build dependencies did not run successfully.
Cause: Using Python 3.15 (or other very new Python versions) where pre-built wheels for pandas/numpy are not yet available. Pip attempts to build from source but fails due to missing C compiler.
Solution:

Use Python 3.11 or 3.12 instead:

bash  py -3.12 -m pip install pandas seaborn matplotlib
```
- Download Python 3.12 from [python.org](https://www.python.org/downloads/) if not installed

---

#### **Issue 2: Script runs but can't find installed packages**

**Symptoms:**
```
ModuleNotFoundError: No module named 'pandas'
(Even after successful installation)
Cause: Packages installed in Python 3.12, but script running with a different Python version (e.g., 3.15).
Solution:

Run script with the same Python version where packages were installed:

bash  py -3.12 Project1Files\data_analysis.py --csv Project1Files\All_Diets.csv --no-show

Or set Python 3.12 as default by creating C:\Users\[username]\AppData\Local\py.ini:

ini  [defaults]
  python=3.12

Recommendation: Use Python 3.11 or 3.12 for data science projects as they have stable, pre-built packages available.