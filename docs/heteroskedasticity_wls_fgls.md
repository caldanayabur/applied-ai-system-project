# Heteroskedasticity, WLS, and FGLS

## Model Eligibility Checklist
- Use WLS only if heteroskedasticity is present and a variance model is defensible.
- Use FGLS only if the variance structure can be estimated from data with enough stability.
- Use robust standard errors if heteroskedasticity is present but no reliable variance model is available.

## Disqualifying Conditions
- Reject WLS if no variance rationale is available.
- Reject FGLS if the estimated weights are unstable or derived from too little data.
- Reject both WLS and FGLS if the residual pattern does not indicate heteroskedasticity.
- Reject weighted methods if weights are chosen only to improve fit without a variance argument.

## Required Diagnostics
- Inspect residual vs fitted plots for funnel, fan, or cone shapes.
- Inspect residual spread against key predictors.
- Compare variance by fitted-value bins or predictor bins.
- Check whether error variance increases or decreases systematically with scale.

## Diagnostic → Action Rules
- If residual spread increases with fitted values, mark heteroskedasticity as present.
- If residual spread changes systematically across predictor bins, mark heteroskedasticity as present.
- If heteroskedasticity is present and the variance pattern is describable, allow WLS with the corresponding weights.
- If heteroskedasticity is present but the variance pattern is not describable, prefer robust standard errors over WLS.
- If a variance model is estimated from data and remains stable across resamples or subgroups, FGLS is acceptable.
- If the variance model changes materially across resamples or subgroups, abandon FGLS and use robust standard errors.
- If the plot is ambiguous, keep OLS with robust standard errors rather than forcing weights.

## Output Restrictions
- Do not apply WLS without a stated variance rationale.
- Do not present weighted coefficients as superior unless the heteroskedasticity diagnosis is explicit.
- Do not present FGLS as reliable when the estimated variance model is unstable.