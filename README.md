# DME Python SDK

## Introduction
- Python client (`pydme/client.py`) for accessing DME RESTful API
- Auto-login to Huawei flash storage using DME tokens, no need to remember per-storage credentials
- Action modules for DME RESTful API

## Project Structure

```
.
├── pydme/                  # Python package
│   ├── client.py           # DME API client
│   ├── cli.py              # CLI entry point
│   └── actions/            # Action modules (one file per topic)
│       ├── aiops.py         # AIOps intelligent operations
│       ├── backup.py         # Backup management
│       ├── fcswitch.py       # FC switch management
│       ├── gfs.py            # Global file system
│       ├── integrate.py      # Third-party integration (CMDB)
│       ├── ipswitch.py       # IP switch management
│       ├── kube.py           # Kubernetes management
│       ├── nas.py            # NAS file storage
│       ├── protect.py        # Data protection
│       ├── san.py            # SAN block storage
│       ├── server.py         # Server management
│       ├── storage.py        # Storage device management
│       ├── system.py         # System management
│       ├── tenant.py         # Tenant self-service
│       ├── virt.py           # Virtualization services
│       └── workflow.py       # Workflow management
├── pyproject.toml
└── README.md
```

## How to Use

### Installation

Install from default branch (stable, Chinese comments):

```bash
pip install git+https://github.com/agentic-data-ops/dme-python-sdk.git
```

Install from dev branch (latest features, Chinese comments):

```bash
pip install git+https://github.com/agentic-data-ops/dme-python-sdk.git@dev
```

Or install from english branch (stable, english comments):

```bash
pip install git+https://github.com/agentic-data-ops/dme-python-sdk.git@main-en
```

Or install in editable mode for development:

```bash
git clone https://github.com/agentic-data-ops/dme-python-sdk.git
cd dme-python-sdk
pip install -e .
```


### Environment Configuration

```
# Create a "third-party system access" user in DME with "northbound user group" role
DME_API_ENDPOINT=https://dme-float-ip:26335
DME_API_USERNAME=your-username
DME_API_PASSWORD=your-password

# Or use an auth token instead of username/password:
# DME_API_AUTH_TOKEN=your-token
```


### Using the CLI

After installation, the `pydme` command is available globally:

```bash
# View all available topics and actions
pydme --list-topics

# View help for a specific topic
pydme storage --help

# View help for a specific subtopic
pydme storage disk --help

# View help for a specific action
pydme storage disk list --help

# Execute an action
pydme storage list --limit 20

# Execute a subtopic action
pydme storage disk list --storage_id <id>
```

Available topics:

| Topic | Description |
|-------|-------------|
| `protect` | Data protection (protection groups/active-active/replication/snapshots/clones) |
| `san` | SAN block storage (LUNs/mapping views/hosts/port groups) |
| `nas` | NAS file storage (NFS/CIFS/DPC/filesystems/quotas) |
| `storage` | Storage device management (tenants/disks/pools/ports/controllers) |
| `system` | System management (users/tags/tasks/regions/certificates) |
| `aiops` | AIOps (alerts/performance/health/topology) |
| `fcswitch` | FC switch management |
| `gfs` | Global file system (GFS) |
| `virt` | Virtualization services (VMs/clusters/datastores) |
| `server` | Server management (CPU/memory/RAID) |
| `tenant` | Tenant self-service (service LUNs/project groups) |
| `ipswitch` | IP switch management |
| `workflow` | Workflow management |
| `kube` | Kubernetes management |
| `integrate` | Third-party integration (CMDB) |
| `backup` | Backup management |

DME connection info can also be passed via CLI arguments:

```bash
pydme --endpoint https://dme-float-ip:26335 --user admin --password pass storage list
```


## High-Risk Operation Control

To prevent accidental data loss or service interruption, the CLI has a built-in **high-risk operation blacklist** mechanism.

### How It Works

High-risk operations include: `delete`, `modify`, `remove`, `unmap`, `split`, `stop`, `rollback`, `switch`, etc.

When a risky command is detected, the CLI intercepts and prompts for confirmation:

```
⚠️  Risk operation warning: "san lun delete" is a high-risk operation (may cause data loss or service interruption)
   ❌ Execution refused. To proceed, add --accept-risk or set DME_ACCEPT_RISK=true
```

### How to Accept Risk

**Option 1: CLI flag** (single invocation)

```bash
pydme san lun delete --id <lun_id> --accept-risk
```

**Option 2: Environment variable** (session-wide)

```bash
export DME_ACCEPT_RISK=true
pydme san lun delete --id <lun_id>
```

### Blacklist Configuration File

On first risky command execution, the CLI automatically generates a blacklist file:

- **Linux**: `~/.config/pydme/blacklist.json`
- **Windows**: `C:\Users\<username>\.config\pydme\blacklist.json`

You can edit this file to customize the risk policy:

```json
{
  "san": ["lun_delete", "lun_expand", "lun_modify"],
  "storage": ["remove", "modify", "vstore_delete"]
}
```

> **Tip**: To completely disable risk checks, set the file content to `{}`. Not recommended in production.

### Covered Risk Actions

Covers **10 topics, 122 high-risk actions**:

| Topic | Risky Actions | Examples |
|-------|---------------|----------|
| `san` | 22 | `lun_delete`, `lun_expand`, `storage_host_unmap_luns` |
| `protect` | 40 | `snapshot_rollback`, `hypermetro_domain_split`, `replication_group_switch` |
| `nas` | 22 | `cifs_share_delete`, `filesystem_modify`, `quota_delete` |
| `storage` | 13 | `remove`, `qos_deactivate`, `vstore_delete` |
| `system` | 9 | `user_delete`, `tag_unbind`, `reset_password` |
| `fcswitch` | 4 | `zone_delete`, `alias_modify` |
| `gfs` | 4 | `namespace_delete`, `migration_task_modify` |
| `tenant` | 3 | `lun_change_tier`, `lun_unbind_project` |
| `aiops` | 1 | `alarm_clear` |
| `workflow` | 1 | `instance_stop` |


### Using Action Modules

Each action module provides topic-specific functions. These functions take an authenticated `DMEAPIClient` instance as the first parameter.

#### Import all modules

```python
from pydme.actions import *

client = DMEAPIClient()
client.login()

# Call functions by module name
disks = storage.disk_list(client, storage_id="your-storage-id")
alarms = aiops.alarm_list(client)
luns = san.lun_list(client)
```

#### Import specific modules

```python
from pydme.actions import storage, aiops, san

client = DMEAPIClient()
client.login()

# Query storage device disks
disks = storage.disk_list(client, storage_id="your-storage-id")
print(disks)

# Query alarms
alarms = aiops.alarm_list(client)
print(alarms)

# Query SAN LUNs
luns = san.lun_list(client, limit=20)
print(luns)
```

#### Import a single function

```python
from pydme.actions.storage import disk_list
from pydme.actions.aiops import alarm_list

disks = disk_list(client, storage_id="your-storage-id")
alarms = alarm_list(client)
```

All action functions follow the same pattern:

- **First parameter**: An authenticated `DMEAPIClient` instance
- **Keyword arguments**: Action-specific parameters (see function documentation)
- **Return value**: A `dict` containing the API response

Browse available actions via CLI:

```bash
pydme --list-topics                    # List all topics
pydme <topic> --help                   # View actions under a topic
```


### Using the Python Client

#### Initializing the Client

```python
from pydme.client import DMEAPIClient

client = DMEAPIClient()
client.login()
```

#### Query and classify storage devices

```python
import json

# Query storage device list
storage_list = client.get("/rest/storagemgmt/v1/storages").get("datas", [])
print(json.dumps(storage_list, indent=2))

# Classify by type
dorado_storage_list = [
    storage for storage in storage_list if storage.get("owning_ne_type") == "dorado"
]
pacific_storage_list = [
    storage for storage in storage_list if storage.get("owning_ne_type") == "OceanStorPacific"
]
```

#### Query storage device details

```python
storage_id = dorado_storage_list[0].get("id")
storage_detail = client.get(
    "/rest/storagemgmt/v1/storages/{storage_id}/detail",
    params={"storage_id": storage_id}
)
print(json.dumps(storage_detail, indent=2))
```

#### Call storage device native API

```python
# Get a token-authenticated client for a specific storage device
storage_client = client.get_storage_client(storage_id)
lun_list = storage_client.get("/lun", params={"filter": "NAME:lun"}).get("data", [])
print(json.dumps(lun_list, indent=2))
```
