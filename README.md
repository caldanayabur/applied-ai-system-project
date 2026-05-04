# StatBuddy

## Original Project Context

This project replaces the **Music Recommender Simulation** (from Modules 1-3), which analyzed Spotify track metadata and recommended songs based on user preferences for genre, mood, energy, acousticness, and other audio features. The original system ranked candidates by weighted scoring and returned the top recommendations with explanations. While that system was domain-specific to music, StatBuddy generalizes the recommendation and analysis pattern to **any tabular dataset**, enabling users to upload a CSV, automatically detect the statistical model that best fits a dependent variable, and get AI-powered predictor suggestions via GitHub Copilot.

## Project Summary

StatBuddy is a Python 3.11+ statistics peer tool that analyzes user-uploaded CSV files, detects a suitable statistical model for a dependent variable (binary, count, continuous, or censored), requests ranked predictor suggestions from GitHub Copilot, fits the chosen model, and exports a shareable HTML report with analysis tables and plots. It bridges exploratory data analysis and lightweight model selection, making statistical modeling more accessible to non-experts.

## Architecture Overview

StatBuddy implements a **seven-stage pipeline**:

1. **DatasetLoader**: Reads and validates CSV files, extracts column metadata
2. **DVAnalyzer**: Detects dependent-variable type (binary, count, continuous_normal, continuous_skewed, censored) via distribution tests (Shapiro-Wilk normality, overdispersion checks)
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

2. **Run the app:**
   ```bash
   streamlit run app.py
   ```

The app will open at `http://localhost:8501` in your browser. Optionally, if you have GitHub Copilot SDK access, StatBuddy will use it for predictor suggestions. If not, it will automatically fall back to correlation-based selection.

### What to Do in the App

1. Upload a CSV file using the file uploader
2. Select a dependent variable from the dropdown menu
3. Click "Run StatBuddy"
4. Download the generated HTML report with analysis and model results

## Sample Interactions

### Example 1: Binary Classification (Loan Default)
**Input CSV:** `loan_data.csv` with columns: Age, Income, CreditScore, LoanAmount, Default (binary: 0/1)  
**User Action:** Upload CSV → Select "Default" as dependent variable → Click "Run StatBuddy"  
**AI Output from CopilotAdvisor:**
```
Suggested predictors (ranked):
1. CreditScore (correlation: -0.68) — Strong negative indicator of default
2. Income (correlation: -0.55) — Higher income correlates with lower default
3. LoanAmount (correlation: 0.42) — Larger loans show higher default risk
```
**Model Selected:** Logit (logistic regression for binary outcome)  
**Generated Report:** HTML file with logistic regression coefficients, odds ratios, assumption checks, and predictor distribution plots

### Example 2: Count Regression (Customer Support Tickets)
**Input CSV:** `support_tickets.csv` with columns: DayOfWeek, Season, TeamSize, TrainingHours, TicketCount (non-negative integer)  
**User Action:** Upload CSV → Select "TicketCount" as dependent variable → Click "Run StatBuddy"  
**AI Output from CopilotAdvisor:**
```
Suggested predictors (ranked):
1. TeamSize (correlation: 0.71) — Larger teams handle more tickets
2. Season (correlation: 0.45) — Holiday season drives ticket volume
3. TrainingHours (correlation: -0.38) — Better training reduces tickets
```
**Model Selected:** Poisson (count regression for non-negative outcomes)  
**Generated Report:** HTML file with Poisson regression results, incident rate ratios, goodness-of-fit tests, and count distribution

### Example 3: Continuous Regression (Housing Prices)
**Input CSV:** `housing.csv` with columns: SquareFeet, Bedrooms, YearBuilt, PropertyTax, SalePrice (continuous)  
**User Action:** Upload CSV → Select "SalePrice" as dependent variable → Click "Run StatBuddy"  
**Normality Test:** Shapiro-Wilk p-value = 0.32 → SalePrice is normally distributed  
**AI Output from CopilotAdvisor:**
```
Suggested predictors (ranked):
1. SquareFeet (correlation: 0.82) — Strong size-price relationship
2. Bedrooms (correlation: 0.71) — More bedrooms increase value
3. YearBuilt (correlation: 0.45) — Newer homes command premiums
```
**Model Selected:** OLS (ordinary least squares for continuous normal outcome)  
**Generated Report:** HTML file with linear regression summary, R-squared, residual plots, and predictor coefficient intervals

## Design Decisions

### 1. **AI Integration via GitHub Copilot SDK**
**Decision:** Use Copilot API for predictor suggestions instead of hard-coded heuristics.  
**Trade-off:** Requires SDK availability and network access, but enables contextual, domain-aware recommendations. If SDK fails, system gracefully falls back to correlation-based selection, ensuring robustness without sacrificing functionality.

### 2. **Automatic Model Selection Based on DV Type**
**Decision:** Inspect dependent-variable distribution to choose model family (binary → Logit, count → Poisson, etc.).  
**Trade-off:** Eliminates manual model selection (simpler UX), but may misclassify edge cases (e.g., zero-inflated counts). Confidence in selection is transparent via the Shapiro-Wilk test and overdispersion check.

### 3. **Statsmodels for Regression Fitting**
**Decision:** Use statsmodels instead of scikit-learn or TensorFlow for classical statistical models.  
**Trade-off:** Provides interpretable coefficients, p-values, and assumption diagnostics (ideal for exploratory analysis), but less optimized for large-scale prediction tasks. Falls back to a lightweight `_FallbackResult` class if statsmodels import fails.

### 4. **Jinja2 HTML Report Template**
**Decision:** Render reports as templated HTML with embedded base64-encoded matplotlib figures.  
**Trade-off:** No external dependencies beyond matplotlib; reports are fully self-contained (no linked assets). Trade-off is slightly larger file size for embedded images vs. external image links.

### 5. **Streamlit as the Web Interface**
**Decision:** Chose Streamlit over Flask/FastAPI for rapid prototyping and low boilerplate.  
**Trade-off:** Simpler to build interactive UIs without custom frontend code, but less flexible for advanced styling. Sufficient for this exploratory-analysis use case.

## Testing Summary

**Test Coverage:** 18 unit tests across 6 test modules (test_dataset_loader.py, test_dv_analyzer.py, test_model_selector.py, test_descriptive_analyzer.py, test_model_builder.py, test_copilot_advisor.py)

### What Worked
- ✓ Dataset loading and validation correctly parsed CSV files and extracted metadata
- ✓ Dependent-variable type detection accurately classified binary, count, and continuous outcomes via statistical tests
- ✓ Model selection consistently mapped DV types to appropriate statsmodels families
- ✓ Predictor suggestion fallback (correlation-based) reliably ranked numeric columns when Copilot SDK unavailable
- ✓ Matplotlib plotting with Agg backend successfully generated figures in headless pytest environment
- ✓ HTML report rendering via Jinja2 correctly populated all sections without external dependencies

### What Didn't Work (and Fixes Applied)
- ✗ **Initial Issue:** pytest module import errors when running from tests/ directory  
  **Fix:** Created `tests/conftest.py` to add workspace root to sys.path, enabling top-level package imports
- ✗ **Initial Issue:** Matplotlib Tk backend failed in headless environment (`_tkinter.TclError`)  
  **Fix:** Added `matplotlib.use("Agg")` in dv_analyzer.py and descriptive_analyzer.py before pyplot import
- ✗ **Initial Issue:** Statsmodels import could fail on some systems  
  **Fix:** Added try-catch in model_builder.py to fall back to lightweight `_FallbackResult` class

### What We Learned
1. **Type hints and docstrings are crucial** for maintainability; they clarified expected inputs/outputs and caught design issues early
2. **Graceful fallbacks are essential** — Copilot SDK → correlation, statsmodels → _FallbackResult, Jinja2 → basic HTML — made the system resilient
3. **Matplotlib backend selection matters** for deployment; defaulting to Tk caused silent failures in CI/testing
4. **Statistical assumptions (normality, overdispersion) must be tested**, not assumed — revealed why some models fit poorly
5. **CSV validation prevents downstream errors** — catching missing values and type mismatches upfront saved hours of debugging

## Reflection

**What This Project Taught About AI and Problem-Solving:**

1. **AI as a Tool, Not a Replacement:** GitHub Copilot SDK integration showed that AI suggestions (predictors) need fallbacks and validation. Blind trust in AI outputs leads to poor recommendations; pairing AI with statistical rigor (correlation, model diagnostics) creates a more reliable system.

2. **Generalization is Hard:** Moving from a domain-specific music recommender to a general-purpose CSV analyzer required rethinking the architecture. The original project was tightly coupled to Spotify data; StatBuddy decouples data loading, analysis, and reporting, but this flexibility introduced complexity. Trade-offs between specificity and generality are fundamental.

3. **Exploratory Analysis > Prediction:** StatBuddy prioritizes interpretability (p-values, coefficients, diagnostic plots) over predictive accuracy. This reflects a philosophy that understanding data matters more than maximizing a metric, especially for non-experts using the tool.

4. **Testing Reveals Assumptions:** The matplotlib backend issue, import errors, and statsmodels fallback didn't surface until tests ran in a headless environment. Real-world deployment often differs from development; testing forces you to confront these differences early.

5. **Documentation and Type Hints are Code Quality:** Writing detailed docstrings and type annotations took time but paid dividends. They clarified the design, caught bugs, and made the codebase approachable for future maintenance.

6. **Iterative Refinement Beats Big Design:** The scaffold was built incrementally — load data → analyze DV → select model → advise → describe → fit → report. Each stage was small enough to test and debug independently, reducing the risk of cascading failures.

**Next Steps (If Extending):**  
- Add panel data and time-series support
- Implement more statistical models (survival analysis, mixed-effects)
- Enhance Copilot prompting with real-time data summaries for richer suggestions
- Deploy as a cloud service with user authentication and result history