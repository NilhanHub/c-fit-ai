# Topology Index

| Node | Role | Load % | Owned Roots | Verification |
| --- | --- | --- | --- | --- |
| san.repo_os | control-plane | 16.12 | AGENTS.md, san, README.md, AGENT_GUIDE.md ... | uv run python scripts/san_sync.py --check, uv run python scripts/sanlock.py |
| sim.market_core | product | 14.47 | population, firms, offers, scoring ... | uv run pytest -q |
| sim.research_evidence | evidence | 14.42 | data, research, reports, model ... | uv run pytest -q |
| jobs.web_app | product | 15.03 | apps/web | npm --prefix apps/web test -- --runInBand, npm --prefix apps/web typecheck |
| jobs.product_doctrine | product-doctrine | 11.09 | product, architecture, alerts, ranking ... | uv run pytest -q |
| jobs.design_ux | design | 11.63 | design, ux, stories, trust ... | uv run pytest -q |
| shared.tests_and_scripts | shared | 17.24 | tests, scripts, pyproject.toml, uv.lock | uv run pytest -q, uv run python scripts/san_verify.py |
