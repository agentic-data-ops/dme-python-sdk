# Plan: Fix Parameter Keys to Match main Branch

## Background
During the Chinese-to-English translation, some function parameter keys were incorrectly renamed in the `main-en-dev` branch. This plan systematically compares all function parameters against the `main` branch and fixes discrepancies.

## Diff Results

Script: `.reasonix/scripts/compare_params.py`

### Functions with parameter differences

| File | Function | Issue | Fix |
|------|----------|-------|-----|
| `pydme/actions/storage.py` | `add()` | `maintenanceetenance_start` → `maintenance_start`, `maintenanceetenance_overtime` → `maintenance_overtime` | Renamed in signature, docstring, payload, and registry entry |
| `pydme/actions/storage.py` | `modify()` | Same `maintenanceetenance_*` issue | Same fix |
| `pydme/actions/storage.py` | `disk_domaintenancee_list()` | Function name mangled from `disk_domain_list` | Renamed function + registry entry |
| `pydme/actions/protect.py` | `snapshot_create()` | `snapshots_infor` → `snapshots_info` | Renamed in signature, docstring, payload, and registry entry |

## Root Cause
The word "maintenance" was incorrectly doubled during a search-and-replace translation pass: `maintenance` → `maintenanceetenance` (likely from a bad regex that treated "maintenance" as overlapping with another token).

Similarly, `snapshots_info` was truncated to `snapshots_infor`, and `disk_domain` became `disk_domaintenancee`.

## Changes Made

### `pydme/actions/storage.py`
- `add()`: Fixed parameter names in function signature, docstring, payload dict keys, and action registry params list
- `modify()`: Fixed parameter names in function signature, docstring, payload dict keys
- `disk_domaintenancee_list()` → `disk_domain_list()`: Renamed function and all references including the action registry and subtopic name

### `pydme/actions/protect.py`
- `snapshot_create()`: `snapshots_infor` → `snapshots_info` in function signature, docstring, payload dict key, and action registry params list

## Verification
- `python3 .reasonix/scripts/compare_params.py` — 0 parameter differences remaining
- `python pydme/cli.py storage --help` — works, shows `disk_domain` subtopic
- `python pydme/cli.py storage disk_domain list --help` — works
- `python pydme/cli.py protect snapshot create --help` — shows `snapshots_info`
- No Chinese keywords (`参数格式如下`, `属性格式如下`) remain in pydme/
