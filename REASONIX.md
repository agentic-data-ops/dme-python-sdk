# REASONIX.md — dme-python-sdk (main-en)

English stable release branch of the Huawei DME storage O&M Python SDK (`pydme`).

## Stack
- **Language:** Python 3 (setuptools build)
- **Key dep:** `requests>=2.28`
- **CLI framework:** stdlib `argparse`
- **API client pattern:** auto-login via `DMEAPIClient`

## Branch Architecture
| Branch | Lang | Purpose |
|--------|------|---------|
| `main`/`dev` | CN | Chinese docstrings (active dev) |
| `dev-en` | EN | English translation — clean, up-to-date |
| `main-en` | EN | **Stable release** — sync from `dev-en` |

**Sync:** `dev-en` → `main-en` — checkout dev-en files as-is (both English, no translation needed).

## Layout
- `pydme/__init__.py` — exports `DMEAPIClient`, `StorageAPIClient`, `BaseClient`
- `pydme/client.py` — REST client (auth, CRUD, task polling, storage proxy with gzip fix)
- `pydme/cli.py` — `DMECLI` controller; `parse_docstring()` at `cli.py:195-310`
- `pydme/actions/` — 17 topic modules, each exports an `ACTIONS` dict
- `pydme/config/blacklist.json` — destructive operation keys
- `.reasonix/plans/` — sync plan (dev-en → main-en)

## Commands
- **Dev install:** `pip install -e .`
- **CLI entry:** `pydme --list-topics` or `python -m pydme.cli`
- **CLI pattern:** `pydme <topic> <subtopic> <action> [--param ...]`
- **Risk bypass:** `--accept-risk` flag or `DME_ACCEPT_RISK=true`
- **No test runner/linter** in pyproject.toml

## Sync (dev-en → main-en)

To sync dev-en changes into main-en:

1. Regenerate the plan: update `.reasonix/plans/000-sync-dev-en-to-main-en.md` — diff `origin/dev-en..origin/main-en`, find the differences, list changed files
2. Checkout dev-en files: `git checkout dev-en -- pydme/ install.sh README.md .gitignore`
3. `git commit -m "sync: merge pydme/ updates from dev-en"`
4. `git push`

No translation needed — both branches are English. Ignore `.reasonix/` and `REASONIX.md`.

## Conventions
- **Action functions:** first arg `client: DMEAPIClient`, optional params default `None`, returns `dict`
- **ACTIONS dict:** `{name: {func, description, params[, subtopic]}}`
- **Docstrings are English.** Parser at `cli.py:272` detects `'parameter format:'` (English keywords only).
- **All strings are English** — docstrings, comments, print/log, error messages.

## Watch out for
- **main-en is synced from dev-en.** Before syncing, verify `main-en` has no isolated fixes that would be overwritten.
- **Docstring parser uses `'parameter format:'` (English)** — no quotes on keys, fields end with `,`, braces balance. `Returns:` opens with `{`, no prefix text.
- **Adding a `.py` to `pydme/actions/`** auto-registers it as a CLI topic.
