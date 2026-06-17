# Plan: Sync dev-en → main-en

## Objective

Compare `dev-en` (source) with `main-en` (target) and sync all changes from `dev-en` to `main-en` for `pydme/`, `install.sh`, `pyproject.toml`, and `README.md`.

## Branch Status

| Aspect | `dev-en` (source) | `main-en` (target) |
|--------|-------------------|---------------------|
| Language | English (clean, up-to-date) | English (older, partially broken) |
| Docstrings | Proper English translations | Broken translations (e.g. "Acknowledgege alarm", "queryCurrent alarm") |
| `install.sh` | Present | Missing |
| `pyproject.toml` | Identical | Identical |
| `README.md` | English with default/dev branch install commands | Older English without default/dev branch info |
| Merge base | `c4c59e0` | same |

## Commit Analysis

**123 commits** on `dev-en` not on `main-en` — all related to English translation cleanup, from initial translation through ~80 rounds of fixes. The net effect is that `dev-en` has clean, properly-translated English docstrings while `main-en` has older, broken English.

## Scope — Files to Sync

| Path | Status | Action |
|------|--------|--------|
| `install.sh` | Missing in main-en | **Copy from dev-en** (no translation needed) |
| `pyproject.toml` | Identical in both branches | **No action needed** |
| `README.md` | dev-en has newer English version | **Sync from dev-en** (adds default/dev branch install commands, fixes `：` colons, adds missing `workflow` topic row) |
| `pydme/` (19 files) | dev-en has cleaner English | **Sync from dev-en** |

### Differences in pydme/ docstrings

The diff `dev-en..main-en` shows main-en has **regressions** compared to dev-en:

| Aspect | dev-en (clean) | main-en (broken) |
|--------|----------------|-------------------|
| Function descriptions | "Query alarm info" | "Query alarm info" (same) |
| Args descriptions | "alarm_id: alarm ID, supports fuzzy match" | "alarm_id: alarm ID,supports fuzzy match" (missing space) |
| Returns field names | "alarm_id: alarm ID (string)" | "alarm_id: Alarm ID (string)" (capitalization) |
| Inline comments | "# Query current alarm (always queried by default)" | "#  queryCurrent alarm(Always query by default)" (broken English) |
| Print statements | 'print(f"Request URL: {url}")' | 'print(f" request URL: {url}")' (extra space) |
| Error messages | 'raise ValueError("csns must be a list of 1-30 elements")' | 'raise ValueError("csns must be a list containing 1-30 elements")' |
| ACTIONS descriptions | "Batch query FC switches" | "批量查询光纤交换机" (Chinese!) |

## Implementation

Simply checkout `pydme/`, `install.sh`, and `README.md` from `dev-en`:

```bash
git checkout dev-en -- pydme/ install.sh README.md
```

No translation needed — both branches are English. The only risk is if there are any main-en-specific code changes that should be preserved. Verify after checkout.

## Verification

- [ ] `python3 -m pydme --list-topics` — CLI loads all modules
- [ ] `python3 -m pydme aiops --help` — check English docstrings render correctly
- [ ] `git diff dev-en -- pydme/` — confirm zero diff (dev-en content fully applied)
- [ ] No syntax errors in any file
