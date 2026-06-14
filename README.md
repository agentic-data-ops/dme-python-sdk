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
│       ├── aiops.py         # AIOps (alerts/performance/health/topology)
│       ├── backup.py         # Backup management
│       ├── fcswitch.py       # FC switch management
│       ├── gfs.py            # Global file system (GFS)
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

Install from English branch (stable, English comments):

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
| `aiops` | AIOps (alerts/performance/health/topology) (alerts/performance/health/topology) |
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
| `workflow` | Workflow management |

DME connection info can also be passed via CLI arguments:

```bash
pydme --endpoint https://dme-float-ip:26335 --user admin --password pass storage list
```


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

- **First parameter**：An authenticated `DMEAPIClient` instance
- **Keyword arguments**：Action-specific parameters (see function documentation)
- **Return value**：A `dict` containing the API response

Available topic modules and common functions:

| Module | Example function | Description |
|--------|-----------------|-------------|
| `aiops` | `aiops.alarm_list()` | AIOps (alerts/performance/health/topology) (alerts/performance/health/topology) |
| `backup` | `backup.cluster_list()` | Backup management |
| `fc_switch` | `fc_switch.zone_list()` | FC switch management |
| `gfs` | `gfs.namespace_list()` | Global file system (GFS) |
| `ip_switch` | `ip_switch.list()` | IP switch management |
| `kubernetes` | `kubernetes.cluster_list()` | Kubernetes management |
| `nas` | `nas.nfs_share_list()` | NAS operations (NFS/CIFS/filesystems/quotas) |
| `protection` | `protection.snapshot_list()` | Protection (snapshots/active-active/replication) |
| `san` | `san.lun_list()` | SAN operations (LUNs/mapping views/hosts) |
| `self_service` | `self_service.lun_create()` | Tenant self-service (service LUNs/project groups) |
| `server` | `server.list()` | Server management (CPU/memory/RAID) |
| `storage` | `storage.disk_list()` | Storage device management (disks/ports/controllers/QoS) |
| `system` | `system.task_list()` | System management (users/tags/tasks/certificates) |
| `virtualization` | `virtualization.vm_list()` | Virtualization services (VMs/clusters/datastores) |
| `workflow` | `workflow.template_list()` | Workflow management |

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
