# Plan 000: Sync dev-en → main-en

## Objective

Sync `dev-en` changes into `main-en` for `pydme/`, `README.md`, `.gitignore`.
Ignore `.reasonix/` and `REASONIX.md` (branch-specific files).

## Diff Overview

`origin/dev-en` vs `origin/main-en` in scope:

| File | Change | Detail |
|------|--------|--------|
| `pydme/actions/kube.py` | +382 / -77 | Full optional params; `namespace`→`namespace_name`; Returns detail |
| `pydme/actions/nas.py` | +17 / -16 | `cifs_share_show_permissions` URL params fix; remove duplicate `payload={}` |
| `pydme/actions/aiops.py` | +4 / -3 | `performance_show_indicators` body format: bare list → `{"indicators": [...]}` |
| `pydme/actions/gfs.py` | +2 / -2 | `migration_task_operate` `operate_type: dict` → `operate_type: str` |
| `README.md` | +28 / -12 | Add action count column to topic table |
| **Total** | **5 files, +382 / -161** | |

## Steps

```bash
# 1. Checkout all changed files from dev-en
git checkout dev-en -- pydme/ README.md .gitignore

# 2. Commit (single commit on main-en)
git commit -m "sync: merge pydme/ updates from dev-en

- kube.py: full optional params, namespace→namespace_name, Returns detail
- nas.py: fix cifs_share_show_permissions URL params, dedup payload
- aiops.py: fix performance_show_indicators body format
- gfs.py: fix migration_task_operate operate_type type
- README.md: action count in topic table"
```

## Verify

- [ ] `python3 -m pydme --list-topics` — all modules load
- [ ] `pip install -e .` succeeds
- [ ] `git commit` pushed to `origin/main-en`
- [ ] `git diff origin/main-en..origin/dev-en -- pydme/ README.md .gitignore` returns empty
