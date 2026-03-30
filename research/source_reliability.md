# Source Reliability

## Reliability Scale

- `5`: official, current enough, directly usable for model anchors
- `4`: official or primary, slightly older or less direct, still robust
- `3`: reputable but secondary or proxy-heavy
- `2`: vendor self-description or sparse evidence
- `1`: too weak to drive the model alone

## Current Source Ratings

| Source Family | Reliability | Why |
| --- | --- | --- |
| DCS census and household counts | 5 | official core population anchors |
| DCS HIES 2019 | 5 | official household economic structure, but older than current crisis environment |
| DCS computer literacy bulletins | 5 | official digital-readiness proxy |
| DCS labour-force survey | 5 | official labour-pressure proxy |
| DCS informal / establishment reports | 4 | official, but less complete for firm digital maturity and revenue detail |
| Mesa docs | 5 | official tool documentation |
| JASSS synthetic population review | 4 | primary method literature, not Sri Lanka-specific |
| DataReportal Sri Lanka | 3 | useful current digital proxy, but not official |
| StatCounter Sri Lanka | 3 | useful device/platform proxy, not an official population survey |
| Vendor offer pages | 2 | concrete for product existence and stated capabilities, weak for actual ROI claims |

## Prompt #02 Rule

- Only reliability `4` and `5` sources should anchor synthetic population and firm counts.
- Reliability `2` and `3` sources can shape scoring assumptions, but those assumptions must stay tagged as `INFERENCE`.
