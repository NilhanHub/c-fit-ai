# API Contracts

## Public Seeker APIs

- `GET /jobs`
- `GET /jobs/{jobId}`
- `POST /saved-searches`
- `POST /applications`
- `POST /stories`
- `POST /reports`

## Employer APIs

- `POST /employers/verify`
- `POST /jobs`
- `PATCH /jobs/{jobId}`
- `POST /stories/urgent`
- `PATCH /applications/{applicationId}/status`

## Admin APIs

- `GET /moderation/queue`
- `POST /moderation/cases/{caseId}/decision`
- `POST /trust/recompute`
