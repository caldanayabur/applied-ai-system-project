# Heteroskedasticity, WLS, and FGLS

## Problem
OLS becomes inefficient when error variance is not constant across observations.

## Weighted Least Squares (WLS)
- Applies known or estimated weights to correct heteroskedasticity
- Common when variance is related to scale (e.g., income, wages)

## Feasible GLS (FGLS)
- Estimates the variance function from data
- Applies GLS using estimated weights

## When to Use
- Funnel patterns in residual plots
- Variance increases with fitted values or predictors

## Interpretation
- Coefficients remain unbiased
- Standard errors become reliable

## Risks
- Misspecified variance model leads to worse results than OLS