# Panel Models

## Model Eligibility Checklist
- Use only if there are repeated observations over time for the same unit.
- Use only if the panel identifier and time index are available.
- Use only if within-unit dependence is expected.

## Disqualifying Conditions
- Reject panel models if there is no repeated observation structure.
- Reject panel models if the unit identifier is missing.
- Reject panel models if the time index is missing.
- Reject panel models if the panel is effectively cross-sectional.

## Required Diagnostics
- Compare within-unit variation to between-unit variation.
- Check whether unit-specific effects are material.
- Evaluate whether time effects are present.
- Mention Hausman test logic when comparing fixed and random effects.

## Diagnostic → Action Rules
- If repeated observations exist and unit effects are material, panel models are eligible.
- If unobserved unit heterogeneity is likely correlated with regressors, choose fixed effects.
- If unobserved unit heterogeneity is likely independent of regressors, random effects may be acceptable.
- If the Hausman logic favors fixed effects, reject random effects.
- If within-unit variation is minimal, stop and prefer a simpler pooled specification.

## Output Restrictions
- Do not collapse fixed and random effects into one interpretation.
- Do not present panel estimates without stating the unit and time structure.
- Do not claim panel-model validity if repeated observations are absent.