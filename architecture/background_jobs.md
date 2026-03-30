# Background Jobs

## Required Jobs

- Story expiry sweeper
- Media cleanup worker
- Alert fanout worker
- Digest builder
- Trust-score recompute worker
- Moderation queue triage worker

## Important Distinction

- Hiding expired stories is user-facing product logic.
- Physically deleting media is storage hygiene logic.
- These should never be treated as the same job.
