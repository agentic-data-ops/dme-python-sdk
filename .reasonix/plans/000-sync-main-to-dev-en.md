# Plan 000: Sync main → dev-en (today's changes)

## Objective

Port commit `1d88d67` (today's code change on `main`) to `dev-en`: sync code logic changes and translate Chinese docstrings/comments to English.

## Scope

Commit `1d88d67` — `sync: merge pydme/ updates from dev` — touched 10 files:

| File | Changes |
|------|---------|
| `pydme/actions/protect.py` | New params added to `hypermetro_group_list/create/delete/add_pairs/remove_pairs/pause/force_startup`; Returns schema updates; all docstrings in Chinese |
| `pydme/actions/backup.py` | Removed `name`/`quota_type` params; Returns schema updates; cleaned imports |
| `pydme/actions/fcswitch.py` | Returns schema updates (task_id → real fields) |
| `pydme/actions/ipswitch.py` | Returns schema updates (task_id → real fields) |
| `pydme/actions/aiops.py` | Returns schema updates (task_id → real fields) |
| `pydme/actions/tenant.py` | (part of the sync commit) |
| `pydme/actions/virt.py` | (part of the sync commit) |
| `pydme/actions/workflow.py` | (part of the sync commit) |
| `pydme/cli.py` | (part of the sync commit) |
| `pydme/client.py` | (part of the sync commit) |

**Excluded:** `.reasonix/`, `REASONIX.md` (main-only files).

## Approach

1. Checkout each changed file from `origin/main`
2. Translate all new/modified Chinese in docstrings and comments to English per the keyword map below
3. Keep code logic changes as-is (function bodies, signatures, payloads)
4. Do NOT translate: Python identifiers, URL paths, API payload keys, enum constants

### Keyword Translation Map

| Chinese (main) | English (dev-en) |
|----------------|------------------|
| `参数格式如下：[{` | `parameter format: [{` |
| `属性格式如下：{` | `attribute format: {` |
| `可选值：` | `valid values: ` |
| `（必选）` | `(Required)` |
| `（可选）` | `(Optional)` |
| `DME API 客户端` | `DME API client` |
| `默认` | `default` |
| `是否` | `whether` |
| `查询...信息` | `query ... info` |
| `列表` | `list` |
| `支持模糊匹配` | `supports fuzzy match` |
| `互斥` | `mutually exclusive with` |
| `条件必选` | `conditionally required` |
| `条件可选` | `conditionally optional` |
| `本端` | `local` |
| `远端` | `remote` |
| `双活` | `hypermetro` / `active-active` |
| `一致性组` | `consistency group` |
| `保护组` | `protection group` |

## Steps

```bash
# 1. Checkout changed files from main
git checkout origin/main -- pydme/actions/aiops.py pydme/actions/backup.py pydme/actions/fcswitch.py pydme/actions/ipswitch.py pydme/actions/protect.py pydme/actions/tenant.py pydme/actions/virt.py pydme/actions/workflow.py pydme/cli.py pydme/client.py

# 2. Translate all Chinese docstrings/comments to English in each file

# 3. Commit (single commit on dev-en)
git commit -m "sync: merge pydme/ updates from main (1d88d67) with CN→EN translation"
```

## Verify

- [ ] `python3 -m pydme --list-topics` — all modules load
- [ ] Spot-check 3 files for Chinese remnants (`grep -n '[\u4e00-\u9fff]'`)
- [ ] `py_compile` each changed file
