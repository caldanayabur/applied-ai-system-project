# Ordinary Least Squares (OLS)

## Purpose
OLS models the linear relationship between a continuous dependent variable and one or more independent variables by minimizing the sum of squared residuals. It is the baseline model for most empirical analyses.

## Model Form
Y = β0 + β1X1 + β2X2 + ... + ε

## Key Assumptions
- Linearity between X and Y
- Independence of errors
- Homoscedasticity
- Normality of errors
- No perfect multicollinearity

## Diagnostics
- Residual vs fitted plots (linearity, heteroscedasticity)
- QQ plots (normality)
- VIF (multicollinearity)
- Cook’s distance (influential observations)

## Common Violations
- Heteroscedasticity
- Omitted variable bias
- Nonlinear relationships

## Interpretation
- Coefficients represent the marginal change in Y for a one‑unit change in X
- Statistical significance does not imply practical relevance

## Related Extensions
- Log‑linear models
- Polynomial terms
- Interaction effects