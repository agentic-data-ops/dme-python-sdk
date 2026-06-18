# REASONIX.md — dme-python-sdk

Python package (`pydme`) for Huawei DME storage O&M — modular CLI + SDK over the DME REST API.

## Stack
- **Language:** Python 3 (setuptools build)
- **Key dep:** `requests>=2.28`
- **CLI framework:** stdlib `argparse`
- **API client pattern:** auto-login session via `DMEAPIClient`

## Layout
- `pydme/client.py` — REST client: `DMEAPIClient` (central auth+CRUD), `StorageAPIClient` (device-native proxy), `BaseClient`
- `pydme/cli.py` — `DMECLI` controller; entry point for `pydme` command
- `pydme/actions/` — 16 topic modules (protect/san/nas/storage/system/…), each exports `ACTIONS` dict (~435 actions total)
- `pydme/config/blacklist.json` — 122 destructive/risky action keys, bypassed via `--accept-risk` or `DME_ACCEPT_RISK`
- `.reasonix/plans/` — plan documents (7 .md files, completed + pending)
- `.reasonix/scripts/` — test runner shell scripts (`00-lib.sh` with `exec_test` function), helper scripts (`check_prose.py`)
- `.reasonix/reference/` — structured API reference doc (1.7MB, 517+ APIs)

## Commands
- **Dev install:** `pip install -e .` (or `install.sh`: git pull → pip uninstall → reinstall)
- **CLI entry:** `pydme --list-topics` or `python -m pydme.cli`
- **CLI pattern:** `pydme <topic> <subtopic> <action> [--param value …]`
- **Config env vars:** `DME_API_ENDPOINT`, `DME_API_USERNAME`, `DME_API_PASSWORD`, optional `DME_API_AUTH_TOKEN`
- **No test runner/linter** in pyproject.toml — testing uses `.reasonix/scripts/` shell scripts

## Conventions
- **Action functions** take `client: DMEAPIClient` as first arg; optional params default to `None`
- **ACTIONS dict** at module bottom: `{action_name: {func, description, params, subtopic}}` — `subtopic` groups actions under a sub-command
- **Docstrings:** Chinese, structured `Args:` with `param: desc (constraints)。可选值：enum (desc), …`; `Returns:` starts with `{` JSON-style. Parser relies on `参数格式如下：[{` / `属性格式如下：{` as entry markers — using bare `格式：{` causes internal fields to leak as CLI params in `--help`. All field lines end with `,`.
- **Generated files** go in `.reasonix/`: plans → `plans/`, scripts → `scripts/`, output → `output/`
- **Blacklist** loads user override `~/.config/pydme/blacklist.json` if present; falls back to package default

## Watch out for
- **Docstring format is parsed by `cli.py`** — the parser tokenizes `参数格式如下：[{` / `属性格式如下：{` markers. Deviating (e.g. `格式：{`) breaks CLI help rendering. The Returns section must start with `{` on the line after `Returns:` with no prefix text.
- **Action modules are auto-discovered** via `pkgutil.iter_modules` — any new `.py` in `pydme/actions/` becomes a topic automatically. No registration in `cli.py`.
- **No pytest/unittest in the repo** — only `.reasonix/scripts/` shell-based integration tests.
- **Blacklist two-source:** package default (`pydme/config/blacklist.json`) and user override (`~/.config/pydme/`). The user version is authoritative.
