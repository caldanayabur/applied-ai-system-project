# Difference-in-Differences (DID)

## Model Eligibility Checklist
- Use only if there is a pre/post structure.
- Use only if a treatment group and a control group are both available.
- Use only if treatment timing is known.
- Use only if pre-treatment outcomes are observed.

## Disqualifying Conditions
- Reject DID if no pre-treatment data exist.
- Reject DID if no untreated comparison group exists.
- Reject DID if the treatment date is unknown.
- Reject DID if the control group is contaminated by treatment.

## Required Diagnostics
- Assess parallel trends before treatment.
- Inspect pre-period outcomes by group.
- Check whether group-level shocks are plausibly time-invariant.

## Diagnostic → Action Rules
- If pre-treatment trends are approximately parallel, DID is eligible.
- If pre-treatment trends diverge materially, stop and reject DID.
- If no pre-treatment data exist, stop and reject DID.
- If the treatment effect is heterogeneous across time, require event-study style checks before final output.
- If the pre/post comparison is valid, interpret the interaction term as the treatment effect.

## Output Restrictions
- Interpretation is limited to the interaction term.
- Do not claim causal identification when parallel trends fail.
- Do not present DID without a valid control group.