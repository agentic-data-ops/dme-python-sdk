# DME Python SDK — Project Guide

## Project Overview

Python SDK (`pydme`) for accessing Huawei DME (Data Management Engine) RESTful API. Provides auto-login to Huawei flash storage via DME tokens and action modules covering storage, protection, NAS, SAN, system, and other management operations.

## Branch Architecture

| Branch | Language | Purpose |
|--------|----------|---------|
| `main` | Chinese | Chinese docstrings and comments |
| `dev-en` | English | English translation of `main` — docstrings, comments, user-facing messages |
| `dev` | Chinese | Active development (Chinese) |
| `main-en` | English | Stable release (English) |

**Sync direction:** `main` → `dev-en` — merge code changes from `main`, translate Chinese to English.

## Project Structure

```
.
├── pydme/                        # Python package
│   ├── __init__.py
│   ├── client.py                 # DME API client (DMEAPIClient)
│   ├── cli.py                    # CLI entry point (DMECLI, parse_docstring)
│   └── actions/                  # Action modules (one file per topic)
│       ├── __init__.py           # Auto-imports all modules
│       ├── aiops.py              # AIOps (alerts, performance, health, topology)
│       ├── backup.py             # Backup management
│       ├── fcswitch.py           # FC switch management
│       ├── gfs.py                # Global file system (GFS / Omni-Dataverse)
│       ├── integrate.py          # Third-party integration (CMDB)
│       ├── ipswitch.py           # IP switch management
│       ├── kube.py               # Kubernetes management
│       ├── nas.py                # NAS file storage (NFS, CIFS, DPC, quotas)
│       ├── protect.py            # Data protection (groups, snapshots, clones, replication)
│       ├── san.py                # SAN block storage (LUNs, mapping views, hosts)
│       ├── server.py             # Server management (CPU, memory, RAID)
│       ├── storage.py            # Storage device management (tenants, disks, pools)
│       ├── system.py             # System management (users, tags, tasks, regions)
│       ├── tenant.py             # Tenant self-service (service LUNs, project groups)
│       ├── virt.py               # Virtualization services (VMs, clusters, datastores)
│       └── workflow.py           # Workflow management
├── install.sh                    # Installation script
├── pyproject.toml                # Package config
├── README.md
└── CLAUDE.md                     # This file
```

## Action Module Convention

Each action module provides topic-specific functions. Every function takes an authenticated `DMEAPIClient` instance as the first parameter (`client`), keyword arguments for parameters, and returns a `dict`.

### ACTIONS Dictionary

Each module exposes an `ACTIONS` dict at module level for CLI registration:

```python
ACTIONS = {
    'action_name': {
        'func': function_reference,
        'description': 'Short English description for --help',
        'params': ['param1', 'param2'],
        'subtopic': 'subtopic_name',   # Optional, for 3-level hierarchy
    },
}
```

## Docstring Format Rules

### Parser Location

The docstring parser is `DMECLI.parse_docstring()` at `pydme/cli.py:195-310`.

### CRITICAL: Format Block Keywords (Parser Alignment)

The parser at `cli.py:272` checks for `'parameter format:' in stripped` (English only). Chinese keywords **will not be detected**, causing format blocks to be ignored and inner keys to leak as fake CLI parameters.

| Parser Aspect | Implementation | Requirement |
|---------------|---------------|-------------|
| Format block entry | `cli.py:272` — `'parameter format:' in stripped` | Use `parameter format: [{` (English) |
| Nested entry | Brace-depth tracking handles it | Use `attribute format: {` (appears inside format blocks) |
| Brace-depth | `in_format_block += count('{') - count('}')` | `{`/`}` must balance |
| Returns section | Plain text accumulation from `Returns:` onward | Open with `{` directly, no prefix text |
| Field key regex | `^(\w+)\s*:\s*(.+)$` at `cli.py:244` | No quotes around keys (`name:` not `"name":`) |
| Field line separator | Lines joined with `\n` | Keep `,` at end of each field line |

### Format Block Structure

```
param_name: Description text (constraints). valid values: enum1 (desc1), enum2 (desc2). parameter format: [{
        field1: Field description (type1, constraints),
        field2: Field description (type2, constraints). attribute format: {
            sub_field1: Sub-field description (type),
        },
     }, ...]
```

### Translation Keyword Map (for main → dev-en sync)

| Chinese (main) | English (dev-en) |
|----------------|------------------|
| `参数格式如下：[{` | `parameter format: [{` |
| `参数格式如下：{` | `parameter format: {` |
| `属性格式如下：{` | `attribute format: {` |
| `可选值：` / `取值范围：` | `valid values: ` |
| `（必选）` | `(Required)` |
| `（可选）` | `(Optional)` |
| `DME API 客户端` | `DME API client` |

## Sync Rules (main → dev-en)

When syncing `main` into `dev-en`:

1. **Port all code logic changes** exactly (function bodies, signatures, payloads, control flow).
2. **Translate docstrings and comments** from Chinese to English following the keyword map above.
3. **Translate user-facing strings**: `raise ValueError(...)` messages, `print(...)` output, ACTIONS `description` values.
4. **Do NOT translate**: Python identifiers, URL paths, API payload keys, enum constant values.
5. **Verify**: All files must compile (`py_compile`), imports must work, parser must detect `parameter format:` keywords.

## Development Commands

```bash
# Run CLI help
pydme --list-topics
pydme storage --help
pydme storage disk list --help

# Execute actions
pydme storage list --limit 20

# Python usage
from pydme.client import DMEAPIClient
from pydme.actions import storage, aiops, san

client = DMEAPIClient()
client.login()
disks = storage.disk_list(client, storage_id="your-storage-id")
```

## High-Risk Operation Protection

The CLI has a built-in high-risk operation blacklist. Risky operations (delete, modify, remove, etc.) require either `--accept-risk` flag or `DME_ACCEPT_RISK=true` environment variable. Blacklist config: `~/.config/pydme/blacklist.json`.
