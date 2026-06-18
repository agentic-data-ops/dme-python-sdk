# Plan 000: Sync dev-en → main-en

## Objective

Sync `dev-en` changes into `main-en` for `pydme/`, `README.md`, `install.sh`, and `.gitignore`. Ignore `.reasonix/` and `REASONIX.md`.

## Diff Overview

`origin/dev-en` vs `origin/main-en` in scope:

| File | Change |
|------|--------|
| `pydme/actions/aiops.py` | Returns schema: `task_id` → real fields (4 functions) |
| `pydme/actions/backup.py` | Removed `name`/`quota_type` params; updated all Returns; cleaned imports |
| `pydme/actions/fcswitch.py` | Returns schema: `task_id` → real fields (5 functions) |
| `pydme/actions/ipswitch.py` | Returns schema: `task_id` → real fields (7 functions) |
| `pydme/actions/protect.py` | Updated docstrings with constraints; removed `id:` from group_create Returns |
| `pydme/actions/tenant.py` | New `task_remarks` param on `lun_change_tier`; updated docstrings for bind/unbind |
| `pydme/actions/virt.py` | Returns schema: `task_id` → real fields (4 functions) |
| `pydme/actions/workflow.py` | Returns schema: `task_id` → real fields (4 functions) |
| `pydme/cli.py` | Orphan param fix (multiple orphan → steal all); bool type conversion for CLI params |
| `pydme/client.py` | Gzip handling fix (stream=True, raw byte reading, gzip decompress with fallback) |
| `.gitignore` | `.reasonix/` → `pydme.egg-info` |
| `README.md`, `install.sh` | Present in dev-en, may differ |

No translation needed — both branches are English.

## Steps

```bash
# 1. Checkout all changed files from dev-en
git checkout dev-en -- pydme/ install.sh README.md .gitignore

# 2. Commit (single commit on main-en)
git commit -m "sync: merge pydme/ updates from dev-en

Port Returns schema fixes, gzip handling, orphan param fix,
bool conversion, backup/tenant param changes, .gitignore update."
```

## Verify

- [ ] `python3 -m pydme --list-topics` — all modules load
- [ ] `py_compile` all changed files
- [ ] `git commit` pushed to `origin/main-en`
