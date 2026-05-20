# Foundation Handoff

Date: 2026-05-20

## Current Direction

The project now uses the Python implementation as the backend and product baseline. Future backend work should continue in Python.

## Kept

| Path | Purpose |
| --- | --- |
| `server.py` | Current Python HTTP service |
| `index.html` | Current usable single-page UI |
| `config.py` | Python runtime configuration |
| `notification_scraper.py` | Notification scraping logic |
| `requirements.txt` | Python dependencies |
| `uploader-python/` | Python uploader copy and related files |
| `apps/desktop/` | Electron + React desktop skeleton |
| `apps/web/` | Next.js web skeleton |
| `packages/` | Shared frontend packages |
| `legacy/` | Legacy documentation |
| `docs/` | Project documentation |

## Removed

| Path | Reason |
| --- | --- |
| Legacy backend directory | Removed from the current Python-first direction |
| `docker-compose.yml` | Removed because the current Python service has no database container dependency |

## Runnable Commands

| Command | Status | Description |
| --- | --- | --- |
| `python server.py` | Available | Starts the current Python service at `http://127.0.0.1:8787` |
| `pnpm run dev:web` | Available | Starts the Next.js skeleton at `http://127.0.0.1:3000` |
| `pnpm run dev:desktop` | Available | Starts the Electron skeleton |
| `pnpm run build` | Placeholder | Builds frontend workspace |
| `pnpm run typecheck` | Placeholder | Type-checks frontend workspace |
| `pnpm run test` | Placeholder | Current package tests are placeholders |

## Known Placeholders

1. `apps/web` currently renders a minimal skeleton page.
2. `apps/desktop` currently renders a minimal skeleton page.
3. `packages/views` contains placeholder business pages.
4. `packages/core` has basic exports and type scaffolding.
5. `packages/ui` has basic component scaffolding.

## Recommended Next Work

1. Keep `python server.py` as the running backend during product iteration.
2. Migrate business views from `index.html` into React components in `packages/views`.
3. Let `apps/web` and `apps/desktop` call Python HTTP APIs directly.
4. Move reusable upload and scraping logic into `uploader-python/`.
5. Add focused tests around Python API behavior before widening frontend migration.

## Risks

1. The Python service currently carries both API and static file responsibilities.
2. `SAU_ROOT` defaults may need adjustment depending on where `social-auto-upload` is placed locally.
3. The frontend workspace is still a skeleton and does not yet replace the Python prototype UI.
