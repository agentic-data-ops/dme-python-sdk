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
│       ├── aiops.py         # AIOps 智能运维
│       ├── backup.py         # 数据备份管理
│       ├── fcswitch.py       # FC 光纤交换机
│       ├── gfs.py            # 全局文件系统
│       ├── integrate.py      # 三方系统集成(CMDB)
│       ├── ipswitch.py       # IP 交换机
│       ├── kube.py           # Kubernetes 容器
│       ├── nas.py            # NAS 文件存储
│       ├── protect.py        # 数据保护
│       ├── san.py            # SAN 块存储
│       ├── server.py         # 服务器管理
│       ├── storage.py        # 存储设备管理
│       ├── system.py         # 系统管理
│       ├── tenant.py         # 租户自助服务
│       ├── virt.py           # 虚拟化服务
│       └── workflow.py       # 工作流管理
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

Or install from english branch (stable, english comments):

```bash
pip install git+https://github.com/agentic-data-ops/dme-python-sdk.git@main-en
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
| `protect` | 数据保护（保护组/双活/复制/快照/克隆） |
| `san` | SAN 块存储（LUN/映射视图/主机/端口组） |
| `nas` | NAS 文件存储（NFS/CIFS/DPC/文件系统/配额） |
| `storage` | 存储设备管理（租户/磁盘/池/端口/控制器） |
| `system` | 系统管理（用户/标签/任务/Region/证书） |
| `aiops` | AIOps 智能运维（告警/性能/健康度/拓扑） |
| `fcswitch` | FC 光纤交换机管理 |
| `gfs` | 全局文件系统 |
| `virt` | 虚拟化服务（VM/集群/数据存储） |
| `server` | 服务器管理（CPU/内存/RAID） |
| `tenant` | 租户自助服务（服务化LUN/业务群组） |
| `ipswitch` | IP 交换机管理 |
| `workflow` | 工作流管理 |
| `kube` | Kubernetes 容器管理 |
| `integrate` | 三方系统集成（CMDB） |
| `backup` | 数据备份管理 |
| `workflow` | 工作流管理 |

DME 连接信息也可通过命令行参数传递：

```bash
pydme --endpoint https://dme-float-ip:26335 --user admin --password pass storage list
```


## 高风险操作控制

为防止误操作导致数据丢失或服务中断，CLI 内置了**高风险操作黑名单**机制。

### 工作机制

高风险操作包括：`delete`（删除）、`modify`（修改）、`remove`（移除）、`unmap`（解除映射）、`split`（分裂）、`stop`（停止）、`rollback`（回滚）、`switch`（切换）等。

执行高风险命令时，CLI 会拦截并提示确认：

```
⚠️  风险操作警告："san lun delete" 是高风险操作（可能造成数据丢失或服务中断）
   ❌ 已拒绝执行。如确认要继续，请添加 --accept-risk 参数
      或设置环境变量 DME_ACCEPT_RISK=true
```

### 接受风险的方式

**方式一：命令行参数**（单次生效）

```bash
pydme san lun delete --id <lun_id> --accept-risk
```

**方式二：环境变量**（会话内生效）

```bash
export DME_ACCEPT_RISK=true
pydme san lun delete --id <lun_id>
```

### 黑名单配置文件

首次执行风险操作时，CLI 会自动在用户目录生成黑名单文件：

- **Linux**: `~/.config/pydme/blacklist.json`
- **Windows**: `C:\Users\<用户名>\.config\pydme\blacklist.json`

你可以编辑此文件以自定义风险策略：

```json
{
  "san": ["lun_delete", "lun_expand", "lun_modify"],
  "storage": ["remove", "modify", "vstore_delete"]
}
```

> **提示**：如果想完全禁用风险检查，可将配置文件内容清空为 `{}`。不推荐在生产环境中禁用。

### 当前覆盖的风险动作

覆盖 **10 个主题、122 个高风险动作**，包括：

| 主题 | 风险动作数 | 示例 |
|------|-----------|------|
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
