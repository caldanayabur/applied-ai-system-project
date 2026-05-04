# Instrumental Variables (IV)

## Model Eligibility Checklist
- Use only if endogeneity is a clear problem.
- Use only if a candidate instrument is available.
- Use only if the instrument can plausibly affect the outcome only through the endogenous regressor.

## Disqualifying Conditions
- Reject IV if the instrument is weak.
- Reject IV if the instrument is not plausibly exogenous.
- Reject IV if the exclusion restriction cannot be defended.
- Reject IV if the first stage is negligible.

## Required Diagnostics
- Check first-stage relevance.
- Check instrument strength.
- Check overidentification when multiple instruments are available.

## Diagnostic → Action Rules
- If first-stage relevance is strong, keep IV eligible.
- If first-stage relevance is weak, reject IV or replace the instrument.
- If the instrument is conceptually weak, stop even if the model fits numerically.
- If overidentification fails, reject the instrument set.
- If endogeneity is not established, do not move from OLS to IV.

## Output Restrictions
- Warn if the IV strategy is conceptually weak.
- Do not present weak-instrument estimates as causal.
- Do not suppress first-stage diagnostics.