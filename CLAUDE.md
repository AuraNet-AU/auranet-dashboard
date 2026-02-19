# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

AuraNet is a Flask web dashboard for a Raspberry Pi running Pi-hole v6. It provides a consumer-friendly UI for managing DNS-based network protection (ad blocking, parental controls) without requiring users to interact with Pi-hole directly.

## Running the App

**Development (foreground):**
```bash
python3 app.py
```
Runs on `http://0.0.0.0:8080`. Requires Pi-hole to be installed and `sudo` access for pihole commands.

**Production (systemd service):**
```bash
sudo systemctl start auranet
sudo systemctl restart auranet
sudo journalctl -u auranet -f   # live logs
```

There is no test suite and no linter configured.

## Releasing

```bash
bash release.sh
```
Interactive script that bumps `version.txt`, prepends a section to `CHANGELOG.md`, commits, and creates an annotated git tag. Push separately with `git push origin main --tags`.

## Architecture

The entire backend is a single file: `app.py`. There are no separate modules or packages.

**Pi-hole integration uses two mechanisms:**
1. **Direct SQLite** — `run_sqlite_query()` reads/writes Pi-hole's databases directly:
   - `/etc/pihole/gravity.db` — adlist management (adding/removing/enabling blocklist URLs)
   - `/etc/pihole/pihole-FTL.db` — query stats and network device discovery
2. **subprocess + sudo** — `run_pihole_command()` calls `/usr/local/bin/pihole` CLI for operations that need Pi-hole's own logic (enable, disable, gravity update, allow/deny domains, restartdns).

**Protection model:**
- `CATEGORY_LISTS` (dict at top of `app.py`) maps category IDs → lists of remote blocklist URLs
- `PROTECTION_MODES` maps mode names (`kids`, `family`, `standard`) → subsets of category IDs
- Applying a mode calls `apply_category()` for each category, which inserts/deletes rows in `gravity.db`, then triggers a background gravity update via `update_gravity_background()`
- Gravity updates run in a daemon thread; status is polled by the frontend via `/gravity/status` and persisted to `gravity_status.json`

**Settings** are stored in `~/auranet_dashboard/settings.json` (path resolved at startup). The Flask `SECRET_KEY` is generated once and stored there too. See `settings.example.json` for the schema.

**Templates** use Jinja2 with Bootstrap 5.3 + Bootstrap Icons. `templates/base.html` defines the full layout (header, nav, flash messages, footer). Page templates extend it and set `active_page` to highlight the current nav item.

**Health check** (`run_health_check()`) checks pihole-FTL service, DNS resolution, gravity DB row count, internet connectivity, blocklist source reachability, disk space, and memory. Results are cached in-process for 5 minutes (`HEALTH_CACHE_TTL = 300`).

**Timezone:** Stats queries use AEST (UTC+10, no DST) hardcoded as `AEST_OFFSET`. Change `timedelta(hours=10)` if deploying in another timezone.

## Key Files

| File | Purpose |
|------|---------|
| `app.py` | Entire backend — Flask routes, Pi-hole integration, health checks |
| `settings.json` | Runtime state (active mode, device names, secret key) — not in git |
| `settings.example.json` | Schema reference for settings.json |
| `templates/base.html` | Shared layout; all CSS lives here |
| `gravity_status.json` | Transient gravity update progress (created/deleted at runtime) |
| `version.txt` | Single-line version string used by release.sh |
