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

## 如何使用

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

可用主题：

| 主题 | 描述 |
|-------|-------------|
| `protect` | Data protection（保护组/双活/复制/快照/克隆） |
| `san` | SAN block storage（LUN/映射视图/主机/端口组） |
| `nas` | NAS file storage（NFS/CIFS/DPC/文件系统/配额） |
| `storage` | Storage device management（租户/磁盘/池/端口/控制器） |
| `system` | System management（用户/标签/任务/Region/证书） |
| `aiops` | AIOps (alerts/performance/health/topology)（告警/性能/健康度/拓扑） |
| `fcswitch` | FC switch management管理 |
| `gfs` | Global file system (GFS) |
| `virt` | Virtualization services（VM/集群/数据存储） |
| `server` | Server management（CPU/内存/RAID） |
| `tenant` | Tenant self-service（服务化LUN/业务群组） |
| `ipswitch` | IP switch management管理 |
| `workflow` | Workflow management |
| `kube` | Kubernetes management管理 |
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

# 通过模块名调用函数
disks = storage.disk_list(client, storage_id="your-storage-id")
alarms = aiops.alarm_list(client)
luns = san.lun_list(client)
```

#### Import specific modules

```python
from pydme.actions import storage, aiops, san

client = DMEAPIClient()
client.login()

# 查询存储设备磁盘
disks = storage.disk_list(client, storage_id="your-storage-id")
print(disks)

# 查询告警
alarms = aiops.alarm_list(client)
print(alarms)

# 查询 SAN LUN
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

可用主题模块及常用函数：

| Module | Example function | Description |
|--------|-----------------|-------------|
| `aiops` | `aiops.alarm_list()` | AIOps (alerts/performance/health/topology)（告警/性能/健康度/拓扑） |
| `backup` | `backup.cluster_list()` | Backup management |
| `fc_switch` | `fc_switch.zone_list()` | FC switch management管理 |
| `gfs` | `gfs.namespace_list()` | Global file system (GFS) |
| `ip_switch` | `ip_switch.list()` | IP switch management管理 |
| `kubernetes` | `kubernetes.cluster_list()` | Kubernetes management管理 |
| `nas` | `nas.nfs_share_list()` | NAS operations (NFS/CIFS/filesystems/quotas) |
| `protection` | `protection.snapshot_list()` | Protection (snapshots/active-active/replication) |
| `san` | `san.lun_list()` | SAN operations (LUNs/mapping views/hosts) |
| `self_service` | `self_service.lun_create()` | Tenant self-service（服务化 LUN/业务群组） |
| `server` | `server.list()` | Server management（CPU/内存/RAID） |
| `storage` | `storage.disk_list()` | Storage device management（磁盘/端口/控制器/QoS） |
| `system` | `system.task_list()` | System management（用户/标签/任务/证书） |
| `virtualization` | `virtualization.vm_list()` | Virtualization services（VM/集群/数据存储） |
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

# 查询存储设备列表
storage_list = client.get("/rest/storagemgmt/v1/storages").get("datas", [])
print(json.dumps(storage_list, indent=2))

# 按类型分类
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
