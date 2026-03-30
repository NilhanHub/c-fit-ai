# Wedge Matrix

## Scoring Model

- Scale: `1` weak to `5` strong
- Criteria: habit potential, implementation feasibility, defensibility, trust, monetization, Colombo launchability, expansion potential

| Wedge | Habit | Feasibility | Defensibility | Trust | Monetization | Launchability | Expandability | Total | Verdict |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Verified freshness feed | 5 | 4 | 4 | 5 | 4 | 5 | 4 | 31 | strong |
| Employer story feed | 4 | 4 | 3 | 4 | 4 | 4 | 4 | 27 | useful but insufficient alone |
| Candidate story feed | 2 | 3 | 2 | 2 | 2 | 3 | 4 | 18 | reject as primary |
| Walk-in interview engine | 5 | 4 | 4 | 4 | 4 | 4 | 4 | 29 | strong secondary wedge |
| Salary-transparency-first board | 3 | 3 | 3 | 5 | 4 | 3 | 4 | 25 | useful feature, weak core wedge |
| Anti-scam trust-first product | 4 | 4 | 4 | 5 | 4 | 4 | 4 | 29 | strong but incomplete alone |
| Application tracking + response-speed engine | 5 | 4 | 5 | 5 | 5 | 4 | 5 | 33 | elite wedge |
| Campus / tuition / ambassador layer | 4 | 3 | 3 | 3 | 3 | 3 | 4 | 23 | growth layer, not core wedge |
| Referrals / friend graph layer | 3 | 2 | 4 | 3 | 4 | 2 | 5 | 23 | too complex for launch |
| Hybrid: verified freshness + urgent stories + status + trust | 5 | 4 | 5 | 5 | 5 | 5 | 5 | 34 | winner |

## Explicit Rejections

### Candidate story feed as the main product

- `INFERENCE` This is the most likely version to become cringe chaos.
- `INFERENCE` It shifts moderation cost up before trust and supply are strong.
- `INFERENCE` Users will not check 20x/day just to see semi-random self-promo videos from unknown candidates.

### Salary transparency as the whole product

- `INFERENCE` Salary transparency is powerful, but by itself it does not create enough day-long urgency.
- `INFERENCE` It works better as a ranking, trust, and filter enhancer inside a broader freshness/status system.

### Referrals or friend graph as the launch wedge

- `INFERENCE` This can become valuable later, but it adds graph cold-start risk before the core problem is solved.

## Why the Hybrid Wins

- `FACT` Fresh inventory exists locally, but trust and response visibility are inconsistent. Sources: `ikmanjobs-sri-lanka-2026`, `topjobs-app-store-2026`, `xpressjobs-recruiter-features-2026`.
- `FACT` Walk-ins, CV-less apply, and direct recruiter follow-up are already real operational patterns in Sri Lanka. Sources: `xpressjobs-recruiter-features-2026`, `xpressjobs-package-details-2026`, `labour-ministry-job-fair-2025`.
- `FACT` Short-form behavior is relevant enough to matter, but professional utility still matters. Sources: `datareportal-digital-2026-sri-lanka`, `linkedin-app-store-2026`.
- `INFERENCE` The best product is therefore not “TikTok for jobs”; it is **a trust-first job utility product with an urgent story layer**.

## Winner and Backup

- Winner: **Hybrid = verified freshness feed + urgent employer stories + application status / response speed + anti-scam trust**
- Backup: **Application tracking + response-speed engine** with walk-in alerts if the story layer underperforms
