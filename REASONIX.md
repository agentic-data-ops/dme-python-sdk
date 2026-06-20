# REASONIX.md — dme-python-sdk (dev-en)

Python package (`pydme`) for Huawei DME storage O&M — modular CLI + SDK over the DME REST API.
This branch (`dev-en`) is the English-docstring variant of the `dev` branch.

## Stack
- **Language:** Python 3 (setuptools build)
- **Key dep:** `requests>=2.28`
- **CLI framework:** stdlib `argparse`
- **API client pattern:** auto-login session via `DMEAPIClient`

## Layout
- `pydme/client.py` — REST client: `DMEAPIClient` (central auth+CRUD), `StorageAPIClient` (device-native proxy), `BaseClient`
- `pydme/cli.py` — `DMECLI` controller; entry point for `pydme` command
- `pydme/actions/` — 16 topic modules (protect/san/nas/storage/system/…), each exports `ACTIONS` dict (427 actions total)
- `pydme/config/blacklist.json` — 122 destructive/risky action keys, bypassed via `--accept-risk` or `DME_ACCEPT_RISK`
- `.reasonix/plans/` — sync plans between main/dev/dev-en branches
- `.reasonix/scripts/` — QA scripts (docstring signature check, param key validation, translation helpers)
- `.reasonix/reference/` — structured API reference doc (1.7MB, 517+ APIs)

## Commands
- **Dev install:** `pip install -e .`
- **CLI entry:** `pydme --list-topics` or `python -m pydme.cli`
- **CLI pattern:** `pydme <topic> <subtopic> <action> [--param value …]`
- **Config env vars:** `DME_API_ENDPOINT`, `DME_API_USERNAME`, `DME_API_PASSWORD`, optional `DME_API_AUTH_TOKEN`
- **End-to-end test status:** 420/427 covered (98.4%), 17 env-limited, 2 SKIP (A800 only), 0 pending

## Conventions
- **Action functions** take `client: DMEAPIClient` as first arg; optional params default to `None`
- **ACTIONS dict** at module bottom: `{action_name: {func, description, params, subtopic}}` — `subtopic` groups actions under a sub-command
- **Docstrings:** English (this branch only). Structured `Args:` with `param: desc (constraints). valid values: enum (desc), …`. Returns starts with `{` JSON-style. Parser relies on `parameter format: [{` / `attribute format: {` as entry markers. All field lines end with `,`.
- **Generated files** go in `.reasonix/`: plans → `plans/`, scripts → `scripts/`, output → `output/`
- **Blacklist** loads user override `~/.config/pydme/blacklist.json` if present; falls back to package default

## Watch out for
- **Docstring format is parsed by `cli.py`** — the parser tokenizes `parameter format: [{` / `attribute format: {` markers. Deviating breaks CLI help rendering. The Returns section must start with `{` on the line after `Returns:` with no prefix text.
- **Action modules are auto-discovered** via `pkgutil.iter_modules` — any new `.py` in `pydme/actions/` becomes a topic automatically. No registration in `cli.py`.
- **Blacklist two-source:** package default (`pydme/config/blacklist.json`) and user override (`~/.config/pydme/`). The user version is authoritative.
- **NFS share_path format:** Must be `/{filesystem_name}/{dtree_name}` (two-level path), DTree must exist first.
- **CIFS create fs_id:** `fs_id` is a top-level parameter, NOT inside `create_cifs_param`.
- **cifs_share_show_permissions:** URL contains `{cifs_share_id}` placeholder — must pass `params={"cifs_share_id": cifs_share_id}` to `client.post()`.
- **Kube API** field name is `namespace_name` not `namespace` (in pod_list / pvc_list).
- **GFS migration_task_operate:** `operate_type` is `str`, values `"start"` or `"stop"`.
