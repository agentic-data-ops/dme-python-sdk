# Plan 000: Sync main → dev-en

## Objective

Sync the latest code logic fixes from `main` to `dev-en`.
`dev-en` already has CN→EN translation completed; this sync ports only the code changes
(bug fixes, parameter updates) while preserving English docstrings.

## Pending sync commits on main

```
0b63875 sync: merge updates from dev (6 files, +312/-135)
```

## Changes to sync

| File | Change type | Detail |
|------|-------------|--------|
| `pydme/actions/kube.py` | **Code + Docstring** | Add full optional params; fix `namespace`→`namespace_name`; Returns detail |
| `pydme/actions/nas.py` | **Code + Docstring** | Fix `cifs_share_show_permissions` URL param; remove duplicate `payload={}`; docstring cleanup |
| `pydme/actions/aiops.py` | **Code + Docstring** | Fix `performance_show_indicators` body: bare list → `{"indicators": [...]}` |
| `pydme/actions/gfs.py` | **Code + Docstring** | Fix `migration_task_operate` type: `dict` → `str` |
| `README.md` | **Doc** | Update topic table with action counts, test coverage |
| `.gitignore` | **Config** | `.vscode/` → `.vscode` |

**Excluded:** `.reasonix/`, `REASONIX.md` (main-only files).

## Strategy

Use `git checkout origin/main -- <file>` to pull the main version, then re-translate
any Chinese docstrings that came along. Since `dev-en` already has English docstrings,
the checkout will overwrite them with Chinese — needs re-translation after checkout.

Alternatively, use `git merge` with manual conflict resolution for each file.

## Steps

```bash
# 1. Checkout fixed files from main (overwrites English docstrings with Chinese)
git checkout origin/main -- pydme/actions/kube.py pydme/actions/nas.py \
  pydme/actions/aiops.py pydme/actions/gfs.py README.md .gitignore

# 2. Re-translate Chinese docstrings in each file back to English

# 3. Commit
git commit -m "sync: merge bug fixes from main (0b63875) into dev-en

- kube.py: full optional params, namespace→namespace_name, Returns detail
- nas.py: fix cifs_share_show_permissions URL param, dedup payload
- aiops.py: fix performance_show_indicators body format
- gfs.py: fix migration_task_operate operate_type type
- README.md: topic table update
- .gitignore: vscode pattern"
```

## Status

✅ Committed `2e89c45` — aiops.py, gfs.py, kube.js fixes ported:
  - `aiops.py`: performance_show_indicators body format
  - `gfs.py`: migration_task_operate operate_type type
  - `kube.py`: full optional params, namespace→namespace_name, Returns detail

✅ All changes synced (commits 2e89c45 + 3d880c7).
