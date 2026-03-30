# System Overview

## Tonight's Build

- Frontend: TypeScript React app under `apps/web`
- Data: seeded demo dataset plus shared contracts in `contracts/`
- Verification: Python tests for artifact existence plus web tests for custom logic

## Production-Oriented Direction

- Web first, mobile later using shared TypeScript contracts
- API layer for jobs, stories, applications, alerts, moderation, and verification
- Postgres for primary data, object storage for media, queue workers for expiry and notifications

## Core Modules

- Feed assembly
- Story assembly
- Search and filters
- Trust and moderation
- Alerts and digests
- Admin and review console
