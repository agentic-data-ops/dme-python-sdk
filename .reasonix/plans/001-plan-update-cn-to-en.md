# Plan: Sync origin/main → dev-en with Chinese-to-English Translation

## Objective

Apply changes from the remote `origin/main` commit `7f41a12` to the `dev-en` branch. This commit introduces:
1. **Returns docstring upgrades** — replaces one-line return descriptions with structured JSON/dict schemas
2. **`task_wait` reconstruction** — refactors `system.py`'s `task_wait` to delegate to `client.get_task_result()`

All Chinese docstring text must be translated to English during application.

## Branch Status (Updated)

| Aspect | `origin/main` | `dev-en` (current) |
|--------|---------------|---------------------|
| Language | Chinese (docstrings, comments) | English (already translated) |
| New commit | `7f41a12 update returns docstring and reconstruct task_wait` | — |
| Merge-base | `c4c59e0` | same |

## Commits on `origin/main` not on `dev-en` (3 total)

| Commit | Scope | Summary |
|--------|-------|---------|
| `851fe91` | README.md only | Translate one installation heading to English |
| `5f05e9a` | README.md only | Remove duplicate Chinese topic table |
| **`7f41a12`** | **10 files in `pydme/actions/`** | **Update Returns docstrings + reconstruct `task_wait`** |

**Only `7f41a12` affects `pydme/` source code and requires action.**

## Changes in `7f41a12` — File-by-File Breakdown

| File | +/- Lines | Type of Change |
|------|-----------|----------------|
| `pydme/actions/aiops.py` | +26 / -4 | Returns docstrings for `performance_query`, `performance_show_indicators`, `performance_list_object_types` |
| `pydme/actions/gfs.py` | +46 / -7 | Returns docstrings for `dataspace_show`, `dataspace_site_list`, `namespace_list`, `namespace_show`, `migration_task_list`, `migration_task_show` |
| `pydme/actions/nas.py` | +247 / -35 | Returns docstrings for ~15 functions (cifs_share, dataturbo_share, quota, filesystem, nfs_share, account, etc.) |
| `pydme/actions/protect.py` | +285 / -25 | Returns docstrings for ~20 functions (protection group, snapshot, clone, replication, etc.) |
| `pydme/actions/san.py` | +204 / -16 | Returns docstrings for ~15 functions (lun, mapping_view, host, port_group, etc.) |
| `pydme/actions/server.py` | +70 / -9 | Returns docstrings for ~6 functions |
| `pydme/actions/storage.py` | +61 / -9 | Returns docstrings for ~6 functions (storage, disk, pool, controller, etc.) |
| `pydme/actions/system.py` | +129 / -68 | Returns docstrings + **`task_wait` reconstruction** (logic + docstring) |
| `pydme/actions/virt.py` | +84 / -10 | Returns docstrings for ~8 functions (vm, cluster, datastore, etc.) |
| `pydme/actions/workflow.py` | +2 / -2 | Returns docstring for `workflow_template_list` |

## Implementation Steps

### Step 1: Sync `task_wait` reconstruction in `system.py`

**What:** The new commit replaces the manual polling loop in `task_wait` with a call to `client.get_task_result()`, and adds a structured Returns docstring + Raises section.

**Why:** Logic change — must be ported exactly (the Python code), with docstring translated CN→EN.

**Changes needed in `dev-en`'s `system.py`:**
- Replace the `def task_wait` implementation body (manual polling) with `client.get_task_result(...)` delegation
- Update docstring: translate Chinese structured Returns schema to English, add Raises section
- Remove the now-unnecessary `task_show` call loop

**Risk:** medium — logic change, verify with `pydme system --help` and quick smoke test.

### Step 2: Translate & apply Returns docstring updates (all 9 other files)

**What:** For each of the 9 remaining files, the commit replaced one-line return descriptions with structured `{ key: type (description), }` schemas in Chinese.

**Approach:** For each file, for each changed function:
1. Identify the function from the diff
2. Take the new structured Returns schema
3. Translate all Chinese labels/descriptions to English
4. Apply the translated version to `dev-en`

**Translation pattern (Chinese → English):**

| Chinese | English |
|---------|---------|
| 状态码 (int32) | status code (int32) |
| 错误码 (int32) | error code (int32) |
| 错误消息 (string) | error message (string) |
| 总容量 (string) | total capacity (string) |
| 已用容量 (string) | used capacity (string) |
| 可用容量 (string) | available capacity (string) |
| 任务ID (string) | task ID (string) |
| 任务名称 (string) | task name (string) |
| 状态 (string) | status (string) |
| 参数格式如下：[{ | parameter format: [{ |
| 可选值： | valid values: |
| 必选 | required |
| 可选 | optional |
| 是否开启... | whether to enable... |
| 名称 (string) | name (string) |
| 描述 (string) | description (string) |
| 创建时间 (string) | creation time (string) |
| ... (full translation table in translation-reference) | |

**Risk:** low — docstring-only changes, no logic impact. The main effort is volume (across ~80+ function return schemas).

### Step 3: Verification

- Run `python3 -m pydme system --help` — confirm `task_wait` shows updated docstring in English
- Run `python3 -m pydme --list-topics` — confirm CLI still loads all modules
- `git diff dev-en...origin/main -- pydme/` — confirm only language difference remains (all semantic changes ported)
- Spot-check 3-4 files for translation quality

## Risks & Open Questions

1. **Volume risk:** ~80+ function return schemas across 10 files. Consider batch-processing via script or doing file-by-file.
2. **Translation consistency:** Field names like `raw_id` (在设备上的ID) should follow a consistent pattern. Suggest: `raw_id: ID on the device (string)`
3. **`Raises` section:** Only `system.py`'s `task_wait` gains a `Raises:` section — other files don't need it.

## When to Re-plan

- If any `origin/main` commit after `7f41a12` also touches `pydme/`, re-assess before starting implementation
- If the volume of docstring changes turns out to be significantly larger than estimated, consider splitting into sub-plans per file

---

*Plan generated: 2026-06-15 (updated from remote fetch)*
