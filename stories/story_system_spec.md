# Story System Spec

## Story Purpose

Stories exist to compress **time-sensitive job actions** into a fast, tappable layer.

## Allowed Story Types

- Employer urgent hiring
- Employer walk-in interview
- Employer same-week shift fill
- Candidate intro template
- Campus or institute hiring burst

## Exact 24-Hour Behavior

- `FACT` from product perspective, a story disappears from user surfaces exactly at `expires_at`.
- `INFERENCE` backend deletion may happen later through cleanup jobs.
- Hidden from user means `visible_until > now` is false.
- Physically deleted means media and metadata are removed according to retention policy.

## Visibility Rules

- Employer stories can appear broadly if the employer is verified.
- Candidate stories are scoped by role match, geography, and moderation state.
- Campus stories are scoped by institution and target role clusters.

## Deep-Link Actions

- View job
- Quick apply
- Save job
- Follow employer
- Message candidate or employer only if enabled
- Report content
