# Plan: Verify Parameter Key Consistency Between main and main-en-dev

## Objective
Compare the current branch (`main-en-dev`) against `main` to find parameter keys inside `parameter format:` / `attribute format:` docstring blocks and function signatures that were incorrectly modified during the Chinese-to-English translation process.

## Background
During translation, some identifier names were damaged by overly-aggressive find-and-replace. Known example:
- `maintenance_start` → `maintenanceetenance_start` (the word "maintenance" was doubled/fused)
- `snapshots_info` → `snapshots_infor` (truncation)
- `disk_domain_list` → `disk_domaintenancee_list` (function name mangled)

Similar undetected corruptions may still exist in other files.

## Scope

### What to check

| Check | Method | Files |
|-------|--------|-------|
| **A. Function signature params** | Extract param names from both branches via AST, diff them | `pydme/actions/*.py` |
| **B. Docstring param keys vs signature** | Parse docstring `Args:` section, cross-reference with actual function params — report keys in docstring that don't exist in the signature | `pydme/actions/*.py` |
| **C. Payload dict keys vs param names** | In function body, check `payload['key'] = key` — flag when payload key != param name | `pydme/actions/*.py` |
| **D. Registry `params` vs actual signature** | Compare `actions` dict's `'params': [...]` lists against actual function signature params | `pydme/actions/*.py` |
| **E. Nested format block inner keys** | Inside `parameter format: { ... }` blocks, check inner attribute keys against what main branch has — these are the most likely to have been corrupted | `pydme/actions/*.py` |
| **F. Unusual identifier patterns** | Scan for identifiers containing suspicious substrings (e.g. duplicated words, truncated endings, fused tokens) | All Python files |

### Risk levels
- **High**: Param in signature doesn't match main → API call sends wrong key → runtime failure
- **Medium**: Docstring key doesn't match signature → CLI `--help` shows wrong param name → user confusion
- **Low**: Registry params list stale but unused at runtime

## Steps

### Step 1 — Run existing param diff (Check A)
Re-run `.reasonix/scripts/compare_params.py` to confirm no additional signature-level differences exist beyond the already-fixed ones.

### Step 2 — Docstring vs signature cross-check (Check B)
For each function, extract the list of parameter names from its `Args:` docstring section and compare against the actual function signature. Flag any key that appears in the docstring but not in the signature (or vice versa).

### Step 3 — Payload key consistency (Check C)
Find all `payload['xxx'] = xxx` patterns and verify the dict key matches the variable name. Report mismatches.

### Step 4 — Registry params audit (Check D)
Compare each action's `'params': [...]` list against the function's actual parameter list. Report missing or extra entries.

### Step 5 — Nested format block audit (Check E)
Parse the `parameter format: { ... }` / `attribute format: { ... }` blocks from docstrings in both branches. Compare the inner attribute key names between main and current branch to detect corruption inside format blocks.

### Step 6 — Suspicious identifier scan (Check F)
Scan all identifiers for common corruption patterns:
- Duplicated substrings (`maintenanceetenance` from `maintenance` + `tenance`)
- Truncated endings (`snapshots_infor` vs `snapshots_info`)
- Typo patterns common in AI translation passes
- Report any suspicious identifiers for manual review

### Step 7 — Report & fix
Compile findings into a fix list. For each confirmed issue:
1. Revert the param/attribute key to match `main`
2. Update docstring, payload keys, and registry entries
3. Verify with `cli.py --help`

## Output
Findings will be documented in `.reasonix/output/findings-param-keys.md` with:
- File:line
- Current (incorrect) key
- Main (correct) key
- Context (signature / docstring / payload / registry)
- Fix applied (Yes/No)
