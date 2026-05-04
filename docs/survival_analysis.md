# Survival Analysis

## Model Eligibility Checklist
- Use only if the dependent variable is time to event.
- Use only if censoring information is available.
- Use only if event times or follow-up times are recorded.
- Use only if the event indicator is defined.

## Disqualifying Conditions
- Reject survival analysis if timing information is missing.
- Reject survival analysis if censoring information is missing.
- Reject survival analysis if the outcome is not time-to-event.
- Reject Cox models if proportional hazards is not plausible.

## Required Diagnostics
- Compute Kaplan-Meier curves.
- Compute event rates.
- Check censoring proportion.
- Check proportional hazards for Cox models.

## Diagnostic → Action Rules
- If event timing and censoring are available, survival analysis is eligible.
- If censoring is absent and events are fully observed, consider a non-survival model only if the outcome is not time-to-event.
- If proportional hazards is plausible, Cox models are eligible.
- If proportional hazards is violated, abandon Cox and route to a time-varying or parametric alternative.
- If censoring or timing is missing, stop and reject survival analysis.

## Output Restrictions
- Do not present hazard ratios as coefficients.
- Do not claim survival-model validity without censoring and time information.
- Do not output Cox interpretation without a proportional hazards warning or check.