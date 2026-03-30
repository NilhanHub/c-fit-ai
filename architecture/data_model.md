# Data Model

## Core Entities

- `SeekerProfile`
- `EmployerProfile`
- `JobPosting`
- `StoryItem`
- `ApplicationRecord`
- `SavedSearch`
- `Alert`
- `ReportCase`

## Key Relationships

- Employers own jobs and employer stories.
- Seekers own profiles, applications, saved searches, and candidate stories.
- Stories can attach to jobs, profiles, or hiring events.
- Reports can target jobs, stories, employers, or seekers.

## Expiry Model

- Story visibility is determined by `expires_at`.
- Cleanup jobs mark expired stories as hidden first, then delete media later according to retention rules.
