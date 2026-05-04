# StatBuddy Model Card

## 1. Model Overview

StatBuddy is a statistics peer tool for uploaded CSV files. It inspects the dependent variable, suggests predictors, fits a basic statistical model, and exports a shareable HTML report. It is intended for exploratory analysis and lightweight model selection support, not for fully automated scientific inference.

## 2. Pipeline Summary

- `DatasetLoader` reads the CSV and stores dataset metadata.
- `DVAnalyzer` detects the dependent-variable type and computes distribution statistics.
- `ModelSelector` maps the detected type to a statistical model.
- `CopilotAdvisor` suggests predictors with GitHub Copilot SDK support and a correlation fallback.
- `DescriptiveAnalyzer` generates summaries, tables, and plots for predictors.
- `ModelBuilder` builds a statsmodels formula and fits the selected model family.
- `ReportGenerator` compiles the final HTML report.

## 3. Supported Statistical Models

- OLS: Linear regression for continuous outcomes.
- Logit: Logistic regression for binary outcomes.
- Poisson: Count regression for non-negative event counts.
- Negative Binomial: Count regression when variance exceeds the mean.
- Tobit: Censored-outcome support, approximated with OLS in this scaffold.

## 4. AI Component

StatBuddy integrates the GitHub Copilot SDK through `CopilotAdvisor`. The advisor sends a prompt containing the dataset column names and dependent variable name, then requests a ranked predictor list with brief justifications. If the SDK connection fails, StatBuddy falls back to a correlation-based selection strategy.

## 5. Limitations

StatBuddy does not yet support panel data, survival models, or time-series workflows. It also does not perform advanced feature engineering, automated hyperparameter tuning, or robust causal inference.

## 6. Dependencies

- streamlit
- pandas
- numpy
- scipy
- statsmodels
- matplotlib
- seaborn
- jinja2
- github-copilot-sdk
- pytest

## 7. Responsible AI Reflection

### What are the limitations or biases in your system?

I think the most tedious aspect of data science is data cleaning and preprocessing. Automating that process is very difficult because not all datasets are the same and human judgment is often required to make decisions about how to handle missing values, outliers, and other data quality issues. My system is just meant to help the user when the data is already in a reasonable state.

### Could your AI be misused, and how would you prevent that?

I think the only way it can be misused is if someone relied on it entirely. Statistical analysis requires domain knowledge and critical thinking. If you ask the AI to tell you exactly which predictors you need to include in your model, it will give you all of them most of the time as it will find a way to make everything more meaningful than it is. The user must always use their own judgment and domain expertise to validate the AI's suggestions.

### What surprised you while testing your AI's reliability?

How bad it is. The descriptive analysis is backward. It is running histograms for independent variables instead of the dependent variable. It got very few predictors for the model. Overall, I think it is not enough for an LLM model to handle statistics without enough context.

### Collaboration with AI

**One instance when AI gave a helpful suggestion:**

After the first try, the AI suggested I redesign the report structure, also that I need to improve the domain knowledge and make some changes about the logic.

**One instance where AI's suggestion was flawed or incorrect:**

I did refactor the code based on the AI's suggestion, but it ended up breaking the existing functionality, so I had to returned it to how it was.