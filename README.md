
https://github.com/user-attachments/assets/6a93a52e-8ff9-4b9b-8a12-7aed609c6f3d

# StatBuddy

## Original Project Context

This project replaces the **Music Recommender Simulation** (from Modules 1-3), which analyzed Spotify track metadata and recommended songs based on user preferences for genre, mood, energy, acousticness, and other audio features. The original system ranked candidates by weighted scoring and returned the top recommendations with explanations. While that system was domain-specific to music, StatBuddy generalizes the recommendation and analysis pattern to **any tabular dataset**, enabling users to upload a CSV, automatically detect the statistical model that best fits a dependent variable, and get AI-powered predictor suggestions via GitHub Copilot.

## Project Summary

StatBuddy is a Python 3.11+ statistics peer tool that analyzes user-uploaded CSV files, detects a suitable dependent-variable model, requests ranked predictor suggestions from GitHub Copilot when available, fits the chosen model, and exports a shareable HTML report with analysis tables and plots. It bridges exploratory data analysis and lightweight model selection.

## Architecture Overview

StatBuddy implements a **seven-stage pipeline**:

1. **DatasetLoader**: Reads and validates CSV files, extracts column metadata
2. **DVAnalyzer**: Detects dependent-variable type (binary, count, continuous_normal, continuous_skewed, censored) via distribution tests and summary statistics
3. **ModelSelector**: Maps detected DV type to a statistical model (OLS, Logit, Poisson, NegativeBinomial, Tobit) using `knowledge/model_rules.json`
4. **CopilotAdvisor**: Queries GitHub Copilot SDK to suggest ranked predictors; falls back to correlation-based selection if SDK unavailable
5. **DescriptiveAnalyzer**: Generates numeric summaries, categorical frequency tables, correlation matrices, and distribution plots for predictors
6. **ModelBuilder**: Constructs a statsmodels regression formula and fits the selected model family
7. **ReportGenerator**: Compiles all results into a templated HTML report with embedded figures (as base64-encoded PNGs)

The `StatBuddy` orchestrator class owns all pipeline components and drives execution via `run(file_path, dv_name)`.

## Folder Structure

```text
├── app.py
├── core/
│   ├── __init__.py
│   ├── statbuddy.py
│   ├── dataset_loader.py
│   ├── dv_analyzer.py
│   └── model_selector.py
├── analysis/
│   ├── __init__.py
│   ├── descriptive_analyzer.py
│   └── model_builder.py
├── ai/
│   ├── __init__.py
│   └── copilot_advisor.py
├── output/
│   ├── __init__.py
│   └── report_generator.py
├── knowledge/
│   └── model_rules.json
├── templates/
│   └── report.html
├── tests/
│   ├── test_dataset_loader.py
│   ├── test_dv_analyzer.py
│   ├── test_model_selector.py
│   ├── test_descriptive_analyzer.py
│   ├── test_model_builder.py
│   └── test_copilot_advisor.py
├── requirements.txt
└── README.md
```

## Setup

### Prerequisites

- Python 3.11 or higher

### Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

The app will open in your browser. Optionally, if you have GitHub Copilot SDK access, StatBuddy will use it for predictor suggestions. If not, it will automatically fall back to correlation-based selection.

### What to Do in the App

1. Upload a CSV file using the file uploader
2. Select a dependent variable from the dropdown menu
3. Click "Run StatBuddy"
4. Save or open the generated HTML report from the output folder shown by the app

## Sample Interactions

### Example 1: Continuous Regression (BigMart Sales)
**Input CSV:** `BigMartSales.csv` with columns: `Item_ID`, `Item_Weight`, `Item_Fat_Content`, `Item_Visibility`, `Item_Type`, `Item_MRP`, `Outlet_ID`, `Outlet_Year`, `Outlet_Size`, `City_Type`, `Outlet_Type`, `Item_Sales`  
**User Action:** Upload CSV → Select "Item_Sales" as dependent variable → Click "Run StatBuddy"  
**AI Output from CopilotAdvisor:**
```
Suggested predictors (ranked):
1. Item_MRP
2. Item_Visibility
3. Outlet_Year
```
**Model Selected:** OLS (ordinary least squares for continuous outcome)  
**Generated Report:** HTML file with linear regression summary, R-squared, residual plots, and predictor coefficient intervals

### Example 2: Credit Risk Regression (CreditRating)
**Input CSV:** `CreditRating.csv` with columns: `ID`, `Income`, `Limit`, `Rating`, `Cards`, `Age`, `Education`, `Gender`, `Student`, `Married`, `Ethnicity`, `Balance`  
**User Action:** Upload CSV → Select "Rating" as dependent variable → Click "Run StatBuddy"  
**AI Output from CopilotAdvisor:**
```
Suggested predictors (ranked):
1. Limit
2. Balance
3. Income
```
**Model Selected:** Logit or OLS depending on how `Rating` is encoded in the uploaded file  
**Generated Report:** HTML file with the selected model's summary, diagnostics, and predictor interval estimates

## Design Decisions

### 1. **AI Integration via GitHub Copilot SDK**
**Decision:** Use Copilot API for predictor suggestions instead of hard-coded heuristics.  
**Trade-off:** Requires SDK availability and network access, but enables contextual, domain-aware recommendations. If SDK fails, the system gracefully falls back to correlation-based selection.

### 2. **Automatic Model Selection Based on DV Type**
**Decision:** Inspect dependent-variable distribution to choose the model family (binary → Logit, count → Poisson, etc.).  
**Trade-off:** Eliminates manual model selection, but may misclassify edge cases such as zero-inflated counts.

### 3. **Statsmodels for Regression Fitting**
**Decision:** Use statsmodels instead of scikit-learn or TensorFlow for classical statistical models.  
**Trade-off:** Provides interpretable coefficients, p-values, and assumption diagnostics, but is less optimized for large-scale prediction tasks.

### 4. **Jinja2 HTML Report Template**
**Decision:** Render reports as templated HTML with embedded base64-encoded matplotlib figures.  
**Trade-off:** Reports are self-contained, but embedded images make the HTML file larger.

### 5. **Streamlit as the Web Interface**
**Decision:** Chose Streamlit over Flask/FastAPI for rapid prototyping and low boilerplate.  
**Trade-off:** Simpler to build interactive UIs without custom frontend code, but less flexible for advanced styling.

## Testing Summary

**Test Coverage:** 18 unit tests across 6 test modules (test_dataset_loader.py, test_dv_analyzer.py, test_model_selector.py, test_descriptive_analyzer.py, test_model_builder.py, test_copilot_advisor.py)

### What Worked
-  Dataset loading and validation correctly parsed CSV files and extracted metadata
- A report was created.

### What Didn't Work (and Fixes Applied)
- The report didn't look very professional.
- The predictor variables were very few and not well-explained.

### What We Learned
- The importance of a good user interface and report design for effective communication of results.
- The need for more comprehensive and accurate predictor selection.

## Reflection

**What This Project Taught About AI and Problem-Solving:**

1. **AI as a Tool, Not a Replacement:** GitHub Copilot SDK integration showed that AI suggestions (predictors) are not very good. Although it is clear that the project itself needs refinement, that also shows that a human expert should never rely solely on AI-generated suggestions.

**Next Steps (If Extending):**  
- Improve the domain knowledge base of the different models used for different dependent variables.
- Make a more detailed report rather than such as simple one.
