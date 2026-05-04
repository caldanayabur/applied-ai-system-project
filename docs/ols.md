# Ordinary Least Squares (OLS)

## Model Eligibility Checklist
- Use only if the dependent variable is continuous.
- Use only if the dependent variable is unbounded or weakly bounded.
- Use only if the dependent variable is not binary, ordinal, censored, or count.
- Use only if a linear mean structure is plausible after basic transformation checks.

## Disqualifying Conditions
- Reject OLS if the dependent variable is binary.
- Reject OLS if the dependent variable is ordinal.
- Reject OLS if the dependent variable is censored.
- Reject OLS if the dependent variable is a count outcome.
- Reject OLS if the outcome is strictly bounded in a way that creates ceiling or floor effects.
- TODO: Define the numeric cutoff for "weakly bounded" in this project.

## Required Diagnostics
- Compute a dependent-variable histogram.
- Compute a log-dependent-variable histogram when the dependent variable is strictly positive and right-skewed.
- Compute a residual vs fitted plot after a trial OLS fit.
- Compute a normality check on residuals.
- Compute a variance inflation check when multiple predictors are used.

## Diagnostic → Action Rules
- If the dependent-variable histogram is approximately symmetric and residual checks are acceptable, continue with OLS.
- If the dependent-variable histogram is strongly right-skewed and all values are positive, test log(DV) before final model selection.
- If the log-dependent-variable histogram is materially closer to symmetric than the raw histogram, prefer log(DV) in the model formula.
- If the residual vs fitted plot shows curvature, abandon OLS unless a transformation or interaction term removes the pattern.
- If the residual vs fitted plot shows fan-shaped variance, abandon plain OLS and route to heteroskedasticity handling.
- If the residual normality check fails badly, keep OLS only for prediction-oriented use and do not treat the coefficients as inferentially stable.
- If multicollinearity is high, remove or combine predictors before finalizing OLS.
- If assumptions fail after one transformation attempt, stop OLS and switch model family.

## Output Restrictions
- Do not interpret coefficients as final if the residual or variance assumptions fail.
- Do not present OLS as appropriate for binary, ordinal, censored, or count outcomes.
- Do not report inferential claims from OLS when a transformation was required but still leaves diagnostics unresolved.