# Logit and Probit Models

## Model Eligibility Checklist
- Use only if the dependent variable is binary.
- Use only if the dependent variable is coded consistently as two classes.
- Use only if class labels can be mapped to 0/1 without ambiguity.

## Disqualifying Conditions
- Reject logit and probit if the dependent variable is continuous.
- Reject logit and probit if the dependent variable is ordinal.
- Reject logit and probit if the dependent variable has more than two unordered classes.
- Reject logit and probit if the binary coding is ambiguous or inconsistent.

## Required Diagnostics
- Compute class balance.
- Check for complete or quasi-complete separation.
- Inspect confusion-matrix performance after fitting.
- Inspect ROC/AUC when class imbalance is not extreme.

## Diagnostic → Action Rules
- If the class balance is heavily skewed, flag imbalance before model selection.
- If separation is detected or strongly suspected, stop standard maximum-likelihood fitting and use a penalized or fallback strategy.
- If the binary outcome is well formed and no separation warning appears, proceed with logit or probit.
- If the user needs odds-based interpretation, prefer logit.
- If the project needs a latent-normal interpretation, prefer probit.
- If class imbalance is severe, require threshold adjustment or class-weight handling before output.

## Output Restrictions
- Do not present raw coefficients alone.
- Do not interpret coefficients without marginal effects or odds ratios.
- Do not present binary GLM output as valid for continuous or ordinal outcomes.