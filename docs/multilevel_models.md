# Multilevel (Hierarchical) Models

## Model Eligibility Checklist
- Use only if the data have nested or grouped structure.
- Use only if units are repeated within groups.
- Use only if group-level dependence is expected.

## Disqualifying Conditions
- Reject multilevel models if there is no grouping variable.
- Reject multilevel models if the cluster structure is too small to estimate group effects.
- Reject multilevel models if all groups are singletons and no within-group correlation exists.

## Required Diagnostics
- Compute variance decomposition across levels.
- Compare within-group variance to between-group variance.
- Check whether group-level intercept variation is material.

## Diagnostic → Action Rules
- If within-group correlation exists and group-level variance is material, multilevel modeling is eligible.
- If group-level variance is negligible, prefer pooled OLS or a simpler fixed-effects specification.
- If repeated observations are the main source of dependence, choose multilevel over pooled OLS.
- If cluster counts are small or unstable, stop and avoid random-effects claims.
- If the group structure explains meaningful variance, keep random effects in the candidate set.

## Output Restrictions
- Separate fixed-effects interpretation from random-effects interpretation.
- Do not present pooled OLS as sufficient when variance decomposition shows meaningful clustering.
- TODO: Add a numeric threshold for "material" between-group variance.