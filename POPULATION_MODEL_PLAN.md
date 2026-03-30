# Population Model Plan

## Scope

- v0 geography: Colombo District only.
- Unit split: individuals and households are modeled separately but linked through `household_id`.

## Individuals

- Required demographic attributes:
  - age band
  - gender
  - labor-force or role proxy in later prompts
- Required economic attributes:
  - income band proxy through household linkage
- Required digital attributes:
  - smartphone access
  - internet access pattern
- Required behavioral attributes:
  - adoption posture
  - sensitivity to trust and language friction in later prompts

## Households

- Required household composition:
  - number of adults
  - number of children
  - total size
- Required economic attributes:
  - income band
  - expenditure posture in later prompts
- Required digital attributes:
  - smartphone-count band
  - payment readiness

## Geography

- `FACT`: Prompt #01 anchors geography at the district level.
- `INFERENCE`: future prompts should refine this to divisional or neighborhood clusters where public evidence supports it.

## Generation Method

1. Define district-level household and person targets.
2. Construct household archetypes from official survey distributions.
3. Populate individuals within each household archetype.
4. Check internal consistency:
   - household size matches individual allocations
   - digital context is plausible for the household
   - economic bands remain coherent

## Mandatory Now vs Later

- Mandatory now:
  - IDs and contracts
  - planning interface
  - evidence-backed seed references
- Later:
  - full synthetic generation
  - mobility and network effects
  - pilot-calibrated behavior parameters
