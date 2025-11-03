# Nutritional Insights App

Interactive dashboard and analysis for dietary recipes, powered by a Python data pipeline and a simple web UI.

## Overview

- Web UI (`project2ui.html`) shows:
  - Bar chart: Average Protein/Carbs/Fat by diet type
  - Pie chart: Recipe distribution per diet type
  - Scatter plot: Sample protein vs carbs (static demo)
  - Filters (search + dropdown) and paginated table (3 rows/page)
  - Simulated API response panel
- Python analysis (`Project1Files/data_analysis.py`) computes metrics from `All_Diets.csv` and saves plots.
- Aggregated results also available in `nutrition_results.json` for fallback/demo.

## Project structure

```
Project2/
├─ project2ui.html
├─ Project1Files/
│  ├─ All_Diets.csv
│  ├─ data_analysis.py
│  ├─ serverless-processing/
│  │  └─ serverless-processing/
│  │     ├─ simulated_nosql/
│  │     │  └─ nutrition_results.json
│  │     ├─ lambda_function.py
│  │     ├─ Dockerfile
│  │     ├─ test_function.py
│  │     └─ ...
└─ README.md (this file)
```

## Prerequisites (Windows)

- Python 3 (available via the Windows launcher `py`)
- pip (comes with Python)

Check versions:

```powershell
py --version
py -m pip --version
```

Install required Python packages:

```powershell
py -m pip install pandas seaborn matplotlib
```

## Quick start

### 1) Run the analysis (from the Project2 folder)

Use the provided CSV to compute the metrics and save plots without opening windows:

```powershell
py Project1Files\data_analysis.py --csv Project1Files\All_Diets.csv --no-show
```

Outputs saved to the current folder:
- `avg_protein_by_diet_type.png`
- `avg_macros_heatmap.png`
- `top_protein_recipes_scatter.png`

If the CSV is missing, the script gracefully falls back to:
`Project1Files/serverless-processing/serverless-processing/simulated_nosql/nutrition_results.json`

Run with fallback only (no CSV):

```powershell
py Project1Files\data_analysis.py --no-show
```

### 2) Open the web UI

- Open `project2ui.html` in your browser to view the dashboard.
- The UI currently uses data synced from the latest CSV run (hardcoded values for simplicity). Filters, charts, and pagination all work offline.

Optional (serve locally, useful if you later switch to dynamic fetch):

```powershell
py -m http.server 5500
# Then open http://localhost:5500/project2ui.html in your browser
```

## Data currently shown in the UI (synced from CSV)

Diet types and averages used by the dashboard:

- Dash: Protein 69.282275, Carbs 160.535754, Fat 101.150562, Recipes 1745
- Keto: Protein 101.266508, Carbs 57.970575, Fat 153.116356, Recipes 1512
- Mediterranean: Protein 101.112316, Carbs 152.905545, Fat 101.416138, Recipes 1753
- Paleo: Protein 88.674765, Carbs 129.552127, Fat 135.669027, Recipes 1274
- Vegan: Protein 56.157030, Carbs 254.004192, Fat 103.299678, Recipes 1522

These values are sourced from `Project1Files/All_Diets.csv` and match the latest run output printed by `data_analysis.py`.

## Troubleshooting
## Troubleshooting Section Summary

Here's a concise summary for your README:

---

### **Troubleshooting**

#### **Issue 1: `ModuleNotFoundError: No module named 'pandas'` (or numpy, seaborn, matplotlib)**

**Symptoms:**
```
ERROR: Unknown compiler(s): [['icl'], ['cl'], ['cc'], ['gcc']...]
× pip subprocess to install build dependencies did not run successfully.
```

**Cause:** Using Python 3.15 (or other very new Python versions) where pre-built wheels for pandas/numpy are not yet available. Pip attempts to build from source but fails due to missing C compiler.

**Solution:**
- Use Python 3.11 or 3.12 instead:
  ```bash
  py -3.12 -m pip install pandas seaborn matplotlib
  ```
- Download Python 3.12 from [python.org](https://www.python.org/downloads/) if not installed

---

#### **Issue 2: Script runs but can't find installed packages**

**Symptoms:**
```
ModuleNotFoundError: No module named 'pandas'
```
(Even after successful installation)

**Cause:** Packages installed in Python 3.12, but script running with a different Python version (e.g., 3.15).

**Solution:**
- Run script with the same Python version where packages were installed:
  ```bash
  py -3.12 Project1Files\data_analysis.py --csv Project1Files\All_Diets.csv --no-show
  ```
- Or set Python 3.12 as default by creating `C:\Users\[username]\AppData\Local\py.ini`:
  ```ini
  [defaults]
  python=3.12
  ```

---

**Recommendation:** Use Python 3.11 or 3.12 for data science projects as they have stable, pre-built packages available.

Recommendation: Use Python 3.11 or 3.12 for data science projects as they have stable, pre-built packages available.

- "Python was not found": use the Windows launcher `py` instead of `python3`.
- Missing packages (e.g., `ModuleNotFoundError: No module named 'pandas'`):

  ```powershell
  py -m pip install pandas seaborn matplotlib
  ```

- VS Code shows unresolved imports for pandas/seaborn/matplotlib: set the VS Code Python interpreter to the one used by `py` (Python 3.x) or ignore—scripts still run with `py`.

## Notes

- The API panel in the UI is a simulated display for coursework purposes.
- If you’d like the UI to load JSON dynamically instead of using hardcoded values, run a local server and I can update the page to fetch from `simulated_nosql/nutrition_results.json`.

## Credits

© 2025 Nutritional Insights. All Rights Reserved.

Group 7 — Annie · Komalpreet · Rhailyn Jane
