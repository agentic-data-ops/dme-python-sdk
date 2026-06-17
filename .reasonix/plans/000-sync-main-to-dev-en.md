# Plan: Sync origin/main → dev-en with Chinese-to-English Translation

## Objective

Compare `dev-en` with `main` on the specified paths (`pydme/`, `install.sh`, `pyproject.toml`, `README.md`), sync `main`'s changes into `dev-en`, and translate all Chinese content to English during application.

## Branch Status

| Aspect | `main` (source) | `dev-en` (target) |
|--------|-----------------|-------------------|
| Language | Chinese (docstrings, comments, README) | English (already translated) |
| `install.sh` | ✅ Present | ❌ Missing (new file) |
| `pyproject.toml` | No change vs dev-en | No change vs main |
| `README.md` | Full Chinese version | Full English version |
| `pydme/` modules | 19 files — Chinese docstrings/comments + code changes (`task_wait` reconstruction) | 19 files — English docstrings/comments, older code |
| Merge base | `c4c59e0` | same |

## Commits on `main` not on `dev-en` (7 total)

| Commit | Scope | Summary |
|--------|-------|---------|
| `851fe91` | README.md | Translate one installation heading to English |
| `5f05e9a` | README.md | Remove duplicate Chinese topic table |
| `0bb716d` | README.md, pydme/ | Sync dev into main: risk blacklist mechanism, README docs |
| `7f41a12` | pydme/actions/ (10 files) | Update Returns docstrings + reconstruct `task_wait` in `system.py` |
| `ce4d506` | .gitignore | Ignore compiled files |
| `71a490a` | .reasonix/plans/ | Add branch sync plan (infra only) |
| `39cb3d2` | pydme/, README.md, install.sh, pyproject.toml | Sync merge from dev (Chinese content) |

**Note:** `71a490a`, `ce4d506` touch only `.reasonix/` and `.gitignore` — out of scope. `pyproject.toml` has **zero diff** between branches.

## Scope — Files to Sync (with Translation)

### Paths analyzed

| Path | Status | Action |
|------|--------|--------|
| `install.sh` | New file in main, absent in dev-en | **Copy as-is** — no Chinese content (simple bash script) |
| `pyproject.toml` | Identical in both branches | **No action needed** |
| `README.md` | Full Chinese rewrite in main vs English in dev-en | **Translate CN→EN** and apply to dev-en |
| `pydme/` (19 files) | Chinese docstrings/comments + code changes in main vs English in dev-en | **Translate CN→EN docstrings/comments**, port code logic changes |

### pydme/ files affected (19 total)

| File | Type of Change |
|------|---------------|
| `pydme/actions/__init__.py` | Module docstring: `# DME Actions 模块` (trivial CN→EN) |
| `pydme/actions/aiops.py` | All docstrings + comments CN→EN: `alarm_list`, `alarm_ack`, `alarm_unack`, `alarm_clear`, `diagnose_task_create`, `performance_query`, `performance_show_indicators`, `performance_list_object_types` |
| `pydme/actions/backup.py` | Docstrings CN→EN |
| `pydme/actions/fcswitch.py` | Docstrings CN→EN |
| `pydme/actions/gfs.py` | Docstrings CN→EN: `dataspace_show`, `dataspace_site_list`, `namespace_list`, `namespace_show`, `migration_task_list`, `migration_task_show` |
| `pydme/actions/integrate.py` | Docstrings CN→EN |
| `pydme/actions/ipswitch.py` | Docstrings CN→EN |
| `pydme/actions/kube.py` | Docstrings CN→EN |
| `pydme/actions/nas.py` | Docstrings CN→EN (~15 functions: cifs_share, dataturbo_share, quota, filesystem, nfs_share, account, etc.) |
| `pydme/actions/protect.py` | Docstrings CN→EN (~20 functions: protection group, snapshot, clone, replication, etc.) |
| `pydme/actions/san.py` | Docstrings CN→EN (~15 functions: lun, mapping_view, host, port_group, etc.) |
| `pydme/actions/server.py` | Docstrings CN→EN (~6 functions) |
| `pydme/actions/storage.py` | Docstrings CN→EN (~6 functions: storage, disk, pool, controller, etc.) |
| `pydme/actions/system.py` | Docstrings CN→EN + **`task_wait` reconstruction** (logic change — delegate to `client.get_task_result()`) |
| `pydme/actions/tenant.py` | Docstrings CN→EN |
| `pydme/actions/virt.py` | Docstrings CN→EN (~8 functions: vm, cluster, datastore, etc.) |
| `pydme/actions/workflow.py` | Docstrings CN→EN |
| `pydme/cli.py` | Docstrings CN→EN |
| `pydme/client.py` | Docstrings CN→EN |

## Translation Rules — Must Align with `dev-en` Parser Logic

**Critical:** The docstring parser in `pydme/cli.py:272` (`parse_docstring`) only recognizes the **English keyword** to enter format-block nesting mode. Chinese keywords will cause parser-silent failure (format blocks not detected, inner keys leaked as fake CLI params). Every translation must match what the CLI parser actually looks for.

### Parser Mechanics (pydme/cli.py:195–310)

| Parser Aspect | Implementation | Translation Implication |
|---------------|---------------|------------------------|
| **Format block entry** | `cli.py:272` — checks `'parameter format:' in stripped` (English only) | `参数格式如下：[{` → **must** become `parameter format: [{` |
| **Nested entry** | `cli.py:272` — `attribute format:` is **NOT** checked; brace-depth handles it inside already-open blocks | `属性格式如下：{` → `attribute format: {` (appears inside format block, brace-depth tracks it) |
| **Brace-depth tracking** | `in_format_block += stripped.count('{') - stripped.count('}')` at `cli.py:275` | `{` / `}` count must match for proper nesting exit |
| **Returns section** | `cli.py:288-302` — plain text accumulation from `Returns:` onward. No format block detection — it just collects all lines until next section (`Raises:`/`Note:`/`Example:`) | Returns must open with `{` (no prefix text like `响应数据格式：{`), all lines accumulated into one string |
| **Field line comma** | Parser stores lines with `\n'.join()`, doesn't check for trailing comma. But `check_e_format_block_keys.py` re-implements same brace-depth logic and expects `,` at field boundaries | Keep `,` at end of each field line for downstream tool compatibility |
| **No quotes on keys** | `param_match = re.match(r'^(\w+)\s*:\s*(.+)$', stripped)` at `cli.py:244` — `\w+` matches word chars only | Keys like `"name"` would NOT match. **Must** be `name:` without quotes |

### Parser Alignment — Keyword Translation Map

| Chinese (main) | English (dev-en parser expects) | Notes |
|----------------|---------------------------------|-------|
| `参数格式如下：[{` | `parameter format: [{` | **Must match exactly** — parser checks `'parameter format:' in stripped` |
| `参数格式如下：{` | `parameter format: {` | Same rule for dict-style (non-list) format blocks |
| `属性格式如下：{` | `attribute format: {` | Inside format blocks, brace-depth handles it |
| `参数格式如下：[{<indented lines>}, ...]` | `parameter format: [{<indented lines>}, ...]` | Keep closing `}, ...]` / `}` for brace-depth balance |
| Returns prefix like `响应数据格式：{` | **Remove prefix**, start with `{` directly | Parser just collects text after `Returns:`, no format-block detection |
| Field lines: `名称: 描述 (string),` | `name: description (string),` | No quotes, `,` at end, constraints in `()` |
| Enum values: `可选值：val (desc),` | `valid values: val (desc),` | Must keep English `:` after `valid values` |

### General Translation Patterns

| Chinese | English |
|---------|---------|
| `DME API 客户端` | DME API client |
| `(必选)` | (Required) |
| `(可选)` | (Optional) |
| `取值范围:` | valid values: |
| `默认` | default |
| `是否开启` | whether to enable |
| `支持模糊匹配` | supports fuzzy match |
| `查询...信息` | query ... info |
| `列表` | list |
| `操作结果` | operation result |

### Docstring Structure Rules (from existing memory)

- **Args format block**: `param_key: <description> (<restrictions>)。valid values: <enum> (<desc>), ...。parameter format: [{...}, ...]`
- **Returns**: Direct JSON-style `{ key: type (description), ... }` — **no prefix text**, open with `{`. The parser just collects plain text.
- All field lines end with `,`
- No quotes around keys (`\w+:` regex constraint in parser)
- Constraints in English parentheses `()`

## Implementation Steps

### Step 1: Copy `install.sh` to dev-en

**Action:** Copy `install.sh` from main — no translation needed (pure bash, no Chinese).

**Risk:** low

### Step 2: Translate and sync `README.md`

**Action:** Take `README.md` from main (Chinese), translate all sections/descriptions to English. The main branch has these structural differences from dev-en's current English README:
- Added `pip install git+...` commands for default and dev branches
- Removed `git checkout main-en` from editable install
- Full Chinese section headings (`## 简介` → `## Introduction`, `## 如何使用` → `## How to Use`, etc.)
- Chinese comments in code blocks
- Chinese table content

**Risk:** low (doc-only)

### Step 3: Sync `task_wait` reconstruction in `system.py`

**Action:** Port the code logic change from main's `7f41a12` — replace manual polling loop in `task_wait` with `client.get_task_result()` delegation. Translate Chinese docstring additions (Returns schema + Raises section) to English.

**Risk:** medium — code logic change; verify with smoke test.

### Step 4: Translate Returns docstrings in all pydme/ files

**Action:** For each of the 19 files, take the Chinese structured Returns schemas from main, translate to English, and apply on top of dev-en's English docstrings.

**Note:** For files where **only** docstrings/comments changed (most files), the change is Chinese labels replacing English labels. The approach is:
1. Read the main branch version of the file
2. Identify all Chinese strings in docstrings and comments
3. Translate them to English
4. Apply to dev-en

For files where English→Chinese was the only change (no code logic change), we can also work directly from the diff.

**Risk:** low for most files (docstring-only), high volume (~80+ functions across 19 files).

### Step 5: Verify

- [ ] `python3 -m pydme --list-topics` — CLI loads all modules
- [ ] `python3 -m pydme system --help` — `task_wait` shows correct English docstring
- [ ] `git diff dev-en main -- pydme/` — only shows semantic English→English differences (translation choices), no Chinese remnants
- [ ] Spot-check 3-4 files for translation quality

## Risks & Open Questions

1. **Volume risk:** ~80+ function return schemas across 19 files (~7,500 lines changed). Consider batch processing per file.
2. **Translation consistency:** Use the translation table from `001-plan-update-cn-to-en.md` as reference to maintain consistency with previous translations.
3. **`task_wait` reconstruction:** Only `system.py` has a code logic change — all other files are docstring/comment-only. Must be careful to port the Python logic exactly while only translating the docstring.
4. **Code comments vs docstrings:** Inline comments (`# 查询当前告警`) also need translation — they're part of the source code that developers read.

## When to Re-plan

- If additional commits land on `main` touching `pydme/`, `README.md`, or `install.sh`, re-assess before starting implementation.
- If pyproject.toml has diverged (currently identical), it may need attention later.
