# DME Python SDK

## 简介
- 提供 Python 客户端（`pydme/client.py`）访问 DME RESTful API
- 支持通过 DME 获取的令牌自动登录华为闪存存储，无需记忆每台存储的用户名和密码
- 提供 DME RESTful API 的动作模块

## 项目结构

```
.
├── pydme/                  # Python 包
│   ├── client.py           # DME API 客户端
│   ├── cli.py              # 命令行接口
│   └── actions/            # 动作模块（每个主题一个文件）
│       ├── aiops.py
│       ├── backup.py
│       ├── fc_switch.py
│       ├── gfs.py
│       ├── ip_switch.py
│       ├── kubernetes.py
│       ├── nas.py
│       ├── protection.py
│       ├── san.py
│       ├── self_service.py
│       ├── server.py
│       ├── storage.py
│       ├── system.py
│       ├── virtualization.py
│       └── workflow.py
├── pyproject.toml
└── README.md
```

## 如何使用

### 安装

从默认分支安装（稳定版，中文注释）：

```bash
pip install git+https://github.com/agentic-data-ops/dme-python-sdk.git
```

从开发分支安装（最新功能，中文注释）：

```bash
pip install git+https://github.com/agentic-data-ops/dme-python-sdk.git@dev
```

从英文分支安装（稳定版，英文注释）：

```bash
pip install git+https://github.com/agentic-data-ops/dme-python-sdk.git@en
```

或以可编辑模式安装用于开发：

```bash
git clone https://github.com/agentic-data-ops/dme-python-sdk.git
cd dme-python-sdk
pip install -e .
```


### 环境配置

```
# 在 DME 上创建"第三方系统接入"用户并添加"北向用户组"角色
DME_API_ENDPOINT=https://dme-float-ip:26335
DME_API_USERNAME=your-username
DME_API_PASSWORD=your-password

# 或使用认证令牌代替用户名/密码：
# DME_API_AUTH_TOKEN=your-token
```


### 使用命令行

安装后，`pydme` 命令全局可用：

```bash
# 查看所有可用主题和动作
pydme --list-topics

# 查看指定主题的帮助
pydme storage --help

# 查看指定子主题的帮助
pydme storage disk --help

# 查看指定动作的帮助
pydme storage disk list --help

# 执行动作
pydme storage list --limit 20

# 执行子主题动作
pydme storage disk list --storage_id <id>
```

可用主题：

| 主题 | 描述 |
|-------|-------------|
| `aiops` | AIOps 智能运维（告警/性能/健康度/拓扑） |
| `backup` | 数据备份管理 |
| `fc_switch` | FC 光纤交换机管理 |
| `gfs` | GFS 全局文件系统 |
| `ip_switch` | IP 交换机管理 |
| `kubernetes` | Kubernetes 容器管理 |
| `nas` | NAS 相关操作（NFS/CIFS/文件系统/配额） |
| `protection` | 保护（快照/双活/远程复制/保护组） |
| `san` | SAN 相关操作（LUN/LUN组/映射视图/主机） |
| `self_service` | 租户自助服务（服务化 LUN/业务群组） |
| `server` | 服务器管理（CPU/内存/RAID） |
| `storage` | 存储设备管理（磁盘/端口/控制器/QoS） |
| `system` | 系统管理（用户/标签/任务/证书） |
| `virtualization` | 虚拟化服务（VM/集群/数据存储） |
| `workflow` | 工作流管理 |

DME 连接信息也可通过命令行参数传递：

```bash
pydme --endpoint https://dme-float-ip:26335 --user admin --password pass storage list
```


### 使用动作模块

每个动作模块提供主题相关的函数，这些函数以已认证的 `DMEAPIClient` 实例作为第一个参数。

#### 导入所有模块

```python
from pydme.actions import *

client = DMEAPIClient()
client.login()

# 通过模块名调用函数
disks = storage.disk_list(client, storage_id="your-storage-id")
alarms = aiops.alarm_list(client)
luns = san.lun_list(client)
```

#### 导入指定模块

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

#### 导入单个函数

```python
from pydme.actions.storage import disk_list
from pydme.actions.aiops import alarm_list

disks = disk_list(client, storage_id="your-storage-id")
alarms = alarm_list(client)
```

所有动作函数遵循相同模式：

- **第一个参数**：已认证的 `DMEAPIClient` 实例
- **关键字参数**：动作特定参数（详见函数文档）
- **返回值**：包含 API 响应的 `dict`

可用主题模块及常用函数：

| 模块 | 示例函数 | 描述 |
|--------|-----------------|-------------|
| `aiops` | `aiops.alarm_list()` | AIOps 智能运维（告警/性能/健康度/拓扑） |
| `backup` | `backup.cluster_list()` | 数据备份管理 |
| `fc_switch` | `fc_switch.zone_list()` | FC 光纤交换机管理 |
| `gfs` | `gfs.namespace_list()` | 全局文件系统 |
| `ip_switch` | `ip_switch.list()` | IP 交换机管理 |
| `kubernetes` | `kubernetes.cluster_list()` | Kubernetes 容器管理 |
| `nas` | `nas.nfs_share_list()` | NAS 相关操作（NFS/CIFS/文件系统/配额） |
| `protection` | `protection.snapshot_list()` | 保护（快照/双活/远程复制） |
| `san` | `san.lun_list()` | SAN 相关操作（LUN/映射视图/主机） |
| `self_service` | `self_service.lun_create()` | 租户自助服务（服务化 LUN/业务群组） |
| `server` | `server.list()` | 服务器管理（CPU/内存/RAID） |
| `storage` | `storage.disk_list()` | 存储设备管理（磁盘/端口/控制器/QoS） |
| `system` | `system.task_list()` | 系统管理（用户/标签/任务/证书） |
| `virtualization` | `virtualization.vm_list()` | 虚拟化服务（VM/集群/数据存储） |
| `workflow` | `workflow.template_list()` | 工作流管理 |

通过 CLI 浏览可用动作：

```bash
pydme --list-topics                    # 列出所有主题
pydme <topic> --help                   # 查看主题下的动作
```


### 使用 Python 客户端

#### 初始化客户端

```python
from pydme.client import DMEAPIClient

client = DMEAPIClient()
client.login()
```

#### 查询并分类存储设备

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

#### 查询存储设备详情

```python
storage_id = dorado_storage_list[0].get("id")
storage_detail = client.get(
    "/rest/storagemgmt/v1/storages/{storage_id}/detail",
    params={"storage_id": storage_id}
)
print(json.dumps(storage_detail, indent=2))
```

#### 调用存储设备原生 API

```python
# 获取指定存储设备的令牌认证客户端
storage_client = client.get_storage_client(storage_id)
lun_list = storage_client.get("/lun", params={"filter": "NAME:lun"}).get("data", [])
print(json.dumps(lun_list, indent=2))
```
