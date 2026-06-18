# REASONIX.md — dme-python-sdk

Python package (`pydme`) for Huawei DME storage O&M — modular CLI + SDK over the DME REST API.

## Stack
- **Language:** Python 3 (setuptools build, setuptools.build_meta)
- **Key dep:** `requests>=2.28`
- **CLI framework:** stdlib `argparse`
- **API client pattern:** auto-login session via `DMEAPIClient`

## Layout
- `pydme/__init__.py` — exports `DMEAPIClient`, `StorageAPIClient`, `BaseClient`
- `pydme/client.py` — REST client implementation (auth, CRUD, task polling, storage proxy)
- `pydme/cli.py` — `DMECLI` controller; entry point for `pydme` CLI command
- `pydme/actions/` — 17 topic modules (storage, san, nas, protect, system, …), each exports an `ACTIONS` dict
- `pydme/config/blacklist.json` — destructive operation keys, bypassed via `--accept-risk` or `DME_ACCEPT_RISK`
- `.reasonix/plans/` — plan documents (1 plan: sync dev→main)
- `install.sh` — convenience script: git pull → pip uninstall → pip install -e .

## Commands
- **Dev install:** `pip install -e .`
- **CLI entry:** `pydme --list-topics` or `python -m pydme.cli`
- **Reinstall:** `install.sh`
- **No test runner or linter** configured in pyproject.toml — no test files found in repo

## Sync (dev → main)

To sync dev changes to main (no merge commit, just checkout changed files):

1. `git checkout main && git pull origin main`
2. `git diff origin/main..origin/dev --stat -- pydme/` — check pending changes
3. `git checkout origin/dev -- pydme/` — overlay dev files
4. `git commit -m "sync: merge pydme/ updates from dev"`
5. `git push origin main`
6. Verify: `git diff origin/main..origin/dev -- pydme/` returns empty

Ignore `.reasonix/` and `REASONIX.md` — they are main-only files.

## Conventions
- **Action functions** take `client: DMEAPIClient` as first arg; optional params default to `None`
- **ACTIONS dict** at module bottom: `{action_name: {func, description, params[, subtopic]}}` — `subtopic` groups actions under a sub-command (e.g. `pydme storage vlan list`)
- **Docstrings** are Chinese: `Args:` with `param: desc (可选, type, 约束)。可选值：enum (desc)`; `Returns:` starts with `{` JSON-style on the next line
- **Blacklist** checks `~/.config/pydme/blacklist.json` first, falls back to package default
- **Action modules auto-discovered** via `pkgutil.iter_modules` in `pydme/actions/__init__.py`

## Watch out for
- **Docstring format is parsed by `cli.py`** — the parser uses `参数格式如下：[{` / `属性格式如下：{` as entry markers. Deviating from these keywords (e.g. using bare `格式：{`) causes internal fields to leak as CLI parameters in `--help` output.
- **Adding a `.py` to `pydme/actions/`** automatically registers it as a CLI topic — no manual registration needed in `cli.py`.
- **Blacklist has two sources:** user override (`~/.config/pydme/blacklist.json`) takes precedence over package default (`pydme/config/blacklist.json`).
- **No tests exist in the repo** — no pytest, unittest, or test directory.
