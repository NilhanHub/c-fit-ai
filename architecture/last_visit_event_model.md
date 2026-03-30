# Last Visit Event Model

## Event entity

- `event_id`
- `kind`
- `occurred_at`
- `minutes_ago`
- `urgency_score`
- `trust_score`
- `related_job_id`
- `related_story_id`
- `related_search_id`
- `headline`
- `detail`
- `cta_label`

## Product behavior

- Events are user-visible immediately when their `occurred_at` is newer than `last_visit_at`.
- Stories become hidden from the user exactly when `expires_at <= now`, even if physical deletion is later.
- Trust downgrades can create negative deltas that hide or demote inventory without deleting it.
