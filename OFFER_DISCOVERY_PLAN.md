# Offer Discovery Plan

## Sequence

1. Start with India.
2. Expand outward by relevance and similarity after the India pilot.
3. Keep country-level evidence separate so cross-country effects remain inspectable.

## Target Companies

- small and mid-sized IT firms
- AI product firms with explicit solution pages
- service firms only when the service is packaged into a clear public offer

## Inclusion Rules

- accept only offers with:
  - a concrete named use case
  - explicit delivery mode
  - explicit target buyer or sector
  - public proof artifact such as a case study, deployment note, or product page

## Exclusion Rules

- reject:
  - vague “AI transformation” consulting pages
  - jargon-heavy pages with no operating details
  - obvious fake or inflated claims with no public evidence
  - offers with no identifiable product or service boundary

## Pilot Design For The First 100 Offers

- geography: India only
- archetypes:
  - customer support and conversational AI
  - document intelligence and onboarding
  - sales and marketing automation
  - vertical workflow copilots
- target mix:
  - roughly 25 offers per archetype

## Normalization Requirements

Every accepted offer must be normalized into `contracts/offer.schema.yaml` with:
- vendor metadata
- offer metadata
- target segment
- delivery mode
- pricing posture
- language support
- proof points
- provenance fields

## Evidence Storage

- raw notes and captures should eventually live in `data/external_offers/`
- normalized records should preserve `source_url`, `retrieved_at`, and `evidence_refs`
- any interpretation beyond the source should be marked `INFERENCE`
