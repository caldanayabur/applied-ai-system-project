# Tobit Regression

## Model Eligibility Checklist
- Use only if the dependent variable is clearly censored.
- Use only if the censoring threshold is known.
- Use only if the latent outcome is plausibly continuous.

## Disqualifying Conditions
- Reject Tobit if the dependent variable is ordinal.
- Reject Tobit if the censoring threshold is unknown.
- Reject Tobit if the data are bounded for reasons other than censoring.
- Reject Tobit if the observed scale is a coded category rather than a censored measure.

## Required Diagnostics
- Compute a histogram of the observed dependent variable.
- Mark the censoring point on the histogram.
- Check the mass accumulated at the censoring threshold.

## Diagnostic → Action Rules
- If a clear pile-up occurs at a known threshold, keep Tobit as eligible.
- If the histogram does not show censoring at a known threshold, abandon Tobit.
- If the observed scale behaves like an ordinal rating, abandon Tobit.
- If censoring is present but threshold information is incomplete, stop and request threshold clarification.

## Output Restrictions
- Must explain the censoring mechanism before interpretation.
- Do not present Tobit as OLS.
- Do not use Tobit when the outcome is only ordinal.