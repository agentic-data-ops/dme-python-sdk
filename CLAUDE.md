# Claude Code: dme-python-sdk

This project is a **Python package** (`pydme`) for the operation and maintenance (O&M) of Huawei DME (Data Management Engine) storage management software. It provides a modular CLI and SDK for managing SAN, NAS, alarms, health, and other storage-related tasks via the DME REST API.

## Project Overview

- **Core Goal**: Automate and simplify DME storage O&M tasks through a structured CLI + Python SDK.
- **Key Technologies**: Python 3, `argparse`, `requests`.
- **Primary Entry Point**: `pydme` CLI command (installed via `pyproject.toml`), or `pydme/cli.py` directly.
- **Package Layout**: `pydme/` — installable via `pip install -e .`

## Architecture

```
pydme/
├── __init__.py        # Exports: DMEAPIClient, StorageAPIClient, BaseClient
├── cli.py             # CLI controller — loads topics from actions/ and dispatches commands
├── client.py          # DME REST API client (auth, CRUD, task polling, storage proxy)
└── actions/           # Topic-specific action modules (auto-loaded via pkgutil)
    ├── __init__.py    # Auto-imports all action modules
    ├── aiops.py       # AIOps (alerts/performance/health/topology)
    ├── backup.py      # Backup management
    ├── fcswitch.py    # FC switch management
    ├── gfs.py         # Global file system
    ├── integrate.py   # Third-party system integration (CMDB)
    ├── ipswitch.py    # IP switch management
    ├── kube.py        # Kubernetes management
    ├── nas.py         # NAS (NFS/CIFS/filesystem/quota/DPC)
    ├── protect.py     # Protection (snapshot/dual-active/replication)
    ├── san.py         # SAN (LUN/mapping view/host)
    ├── server.py      # Server management
    ├── storage.py     # Storage device management
    ├── system.py      # System management (user/task/region/cert)
    ├── tenant.py      # Tenant self service
    ├── virt.py        # Virtualization services
    └── workflow.py    # Workflow management
```

- **`pydme/cli.py`** (`DMECLI`): The central CLI controller. Dynamically loads action modules from `pydme.actions` and dispatches commands.
- **`pydme/client.py`**: Provides `DMEAPIClient` (REST client with auto-login & session), `StorageAPIClient` (device-native API proxy), and `BaseClient`.
- **`pydme/actions/`**: Each module defines an `ACTIONS` dictionary mapping CLI action names to implementation functions + parameter specs. Auto-imported by `__init__.py`.
- **`pyproject.toml`**: Package metadata + `pydme` CLI entry point.

## Installation

```bash
# Stable branch (稳定版，中文注释)
pip install git+https://github.com/agentic-data-ops/dme-python-sdk.git

# Dev branch (开发分支，最新功能，中文注释)
pip install git+https://github.com/agentic-data-ops/dme-python-sdk.git@dev

# Editable install for development
git clone https://github.com/agentic-data-ops/dme-python-sdk.git
cd dme-python-sdk
pip install -e .
```

## Running the CLI

### Configuration

The CLI uses environment variables for authentication:

```bash
export DME_API_ENDPOINT="https://your-dme-ip:port"
export DME_API_USERNAME="admin"
export DME_API_PASSWORD="your-password"
# Optional: export DME_API_AUTH_TOKEN="your-token"
```

Or pass via CLI arguments: `pydme --endpoint <url> --user <user> --password <pass> <topic> <action>`

### Usage Examples

```bash
# List all available topics and actions
pydme --list-topics

# Check help for a specific topic
pydme storage --help

# List storage devices
pydme storage list

# Wait for an asynchronous task
pydme system task wait --task_id <id>

# Directly via python module
python -m pydme.cli --list-topics
```

## Development Conventions

- **Action Implementation**:
  - Each action file in `pydme/actions/` should define functions that take a `DMEAPIClient` instance as the first argument.
  - Actions must be registered in a global `ACTIONS` dictionary at the end of the file.
- **Naming Convention**:
  - Topics correspond to filenames in `pydme/actions/`.
  - Actions within a topic are either "direct" (e.g., `storage list`) or grouped under a "subtopic" (e.g., `storage disk list`).
- **Error Handling**: Use the response from `DMEAPIClient` which returns JSON data from the API. Raise `ValueError` for missing required parameters before making API calls.
- **Import**: Action modules are auto-imported via `pydme/actions/__init__.py` — no manual registration needed in `cli.py`.

## 函数参数帮助文档格式约定

对于具有内部结构的复杂参数（列表/字典），在 docstring 中使用以下格式描述。

### 模板

```
param_key: <param_description> (<param_restrictions>)。可选值：<param_option_enum> (<param_option_description>), ...。参数格式如下：[{
                attr_key1: <attr_description> (<attr_restrictions>)。可选值：<enum> (<desc>), ...。属性格式如下：{
                    sub_key1: <sub_description> (<sub_restrictions>)。可选值：<enum> (<desc>), ...。
                    sub_key2: ...
                },
                attr_key2: ...
             }, ...]
```

### 规则

1. **无引号** — attribute_key 和 description 不使用双引号，纯文本格式
2. **约束** — 使用英文括号 `()` 包裹，如 `(1~255个字符)`
3. **枚举值** — `可选值：enum1 (desc1), enum2 (desc2)`（英文括号）
4. **嵌套对象** — 使用 `属性格式如下：{ ... }` 递归表达
5. **外层包裹** — 列表用 `[{ ... }, ...]`，字典用 `{ ... }`
6. **句号结尾** — 每个参数描述以中文句号 `。` 结尾
7. **关键词约定** — 必须使用 `参数格式如下：[{` 或 `参数格式如下：{` 作为格式块入口标记，CLI 解析器依赖此关键词跳过内部 `key: desc` 行，避免误解析为函数参数
8. **嵌套关键词** — 内部嵌套对象必须使用 `属性格式如下：{` 作为入口标记
9. **大括号平衡** — `{` 和 `}` 必须匹配，解析器通过计数自动退出格式块
10. **字段逗号分隔** — 格式块内每个字段行末添加 `,` 分隔。即使被 `parse_docstring` 压成单行，大模型也能通过 `,` 清晰识别字段边界。

### 示例

```
volumes: 待创建 LUN 基本参数列表 (List<ServiceVolumeBasicParams>, 数组最大成员个数: 1000)。参数格式如下：[{
        name: LUN名称 (1~255个字符, 支持字母数字._-和中文字符),
        capacity: 容量GB (1~262144),
        count: 创建数量 (1~500),
        description: 描述 (0~255个字符),
        start_suffix: 起始后缀编号 (0~9999),
        suffix_length: 后缀长度规则 (1~4, 名称长度+后缀长度<=255),
     }, ...]

scheduler_hints: 调度策略 (可选, SchedulerHints 对象)。参数格式如下：{
        affinity: 是否开启亲和性。可选值：true (开启), false (不开启)。默认不开启,
        affinity_volume: 待亲和的 LUN ID (可选, 0~64个字符),
     }

tuning: 调优属性 (可选), CustomizeLunTuning 对象。参数格式如下：{
        smart_tier: 数据迁移策略。可选值：no_migration (不迁移), automatic_migration (自动迁移), migration_to_higher (向高性能层迁移), migration_to_lower (向低性能层迁移)。默认no_migration,
        deduplication_enabled: 重复数据删除 (仅Thin LUN支持)。可选值：true (开启), false (关闭),
        compression_enabled: 数据压缩 (仅Thin LUN支持)。可选值：true (开启), false (关闭),
        alloction_type: LUN分配类型。可选值：thin, thick,
        smart_qos: Smart QoS对象。属性格式如下：{
                max_bandwidth: 最大带宽 (1~999999999Mbit/s; 与min_bandwidth/min_iops互斥),
                max_iops: 最大IOPS (1~999999999; 与min_bandwidth/min_iops互斥),
                min_bandwidth: 最小带宽 (1~999999999Mbit/s; 与max_bandwidth/max_iops互斥),
                min_iops: 最小IOPS (1~999999999; 与max_bandwidth/max_iops互斥),
                latency: 时延 (1~999999999ms; Dorado V6系列单位为us, 可选值为500/1500; 与max_bandwidth/max_iops互斥),
        },
        workload_type_raw_id: 应用类型ID (0~4294967295; 通过查询指定存储设备上应用类型接口获取),
     }
```

### ⚠️ 常见错误（务必避免）

```diff
- BAD: 格式：{  或  格式：[{    ← 内部字段会泄露为顶层 CLI 参数（如 --name、--type）
+ GOOD: 参数格式如下：{  或  参数格式如下：[{   ← 解析器自动跳过内部字段
```

**错误后果**：使用 `格式：{` 时，`parse_docstring` 会把内部的 `key: desc` 行解析为顶层参数，
在 `--help` 中出现 `--name`、`--type`、`--mode`、`--tag_ids` 等不应出现的参数名。
修复方法：将 `格式：{` 替换为 `参数格式如下：{`，将 `格式：[{` 替换为 `参数格式如下：[{`。

### Returns 格式约定

`Returns:` 段直接输出 JSON 风格的格式内容，**不加任何前缀文字**，以 `{` 开头：

```
Returns:
    {
        total: 硬盘域数量 (int32),
        disk_pools: 硬盘域列表 (List<DiskPoolInfo>)。参数格式如下：[{
            id: 硬盘域id (1~64个字符),
            ...
        }, ...]
    }
```

规则：
- 入口标记：直接以 **`{`** 开头，不使用 `响应数据格式：{`、`返回 XXX 对象。` 等前缀
- 嵌套列表：使用 `参数格式如下：[{` 标记
- 所有字段行末添加 `,` 分隔
- 其余规则与 Args 参数格式块一致（无引号、英文括号约束、枚举值格式、句号结尾等）

## Todo Tasks

When user ask to finish todo tasks, sequentially execute the unfinished todo tasks step by step. When each task finished, update the todo task checkbox, and execute git commit and push.

### Code Refactoring and Consolidation Tasks

**Notes**:
- Do not create dependencies during migration and consolidation. After each topic migration is completed, test whether the migrated command help is correct.
- List topics: `pydme --list-topics`
- Topic help: `pydme <topic> --help`

#### Package Restructuring
- [x] Migrated from `scripts/` flat layout to `pydme/` Python package structure
- [x] Created `pyproject.toml` with `pydme` CLI entry point and package metadata
- [x] Created `pydme/__init__.py` exports: `DMEAPIClient`, `StorageAPIClient`, `BaseClient`
- [x] Created `pydme/actions/__init__.py` with auto-import of all action modules
- [x] Created comprehensive `README.md` with installation, CLI, and SDK usage documentation
- [x] Removed `scripts/util/` (read_api_reference.py no longer needed)
- [x] Removed `SKILL.md` and `param-doc-format.md` (content consolidated into CLAUDE.md)
- [x] Removed `test/` directory

#### san topic
- [x] Migrate physical_host topic to san subtopic: physical_host => san physical_host
- [x] Migrate physical_host_group topic to san subtopic: physical_host_group => san physical_host_group
- [x] Migrate lun_group topic to san subtopic: lun_group => san lun_group
- [x] Migrate mapping_view topic to san subtopic: mapping_view => san mapping_view
- [x] Migrate storage host subtopic to san and rename to storage_host: storage host => san storage_host
- [x] Migrate storage host_group subtopic to san and rename to storage_host_group: storage host_group => san storage_host_group
- [x] Migrate storage port_group subtopic to san: storage port_group => san port_group
- [x] Delete migrated topics

#### aiops topic
- [x] Migrate alarm topic to aiops subtopic: alarm => aiops alarm
- [x] Migrate diagnose task to aiops: diagnose task => aiops diagnose_task
- [x] Migrate performance actions to aiops
- [x] Migrate policy result to aiops: policy result show/list => aiops check_result show/list
- [x] Migrate policy topic to aiops subtopic: policy => aiops check_policy
- [x] Migrate topology topic to aiops subtopic: topology => aiops topology
- [x] Migrate health topic to aiops subtopic
- [x] Delete migrated topics
- [x] Remove redundant topology subtopics and merge into main topology subtopic

### Code Review & Fix Task

- [x] san.py: 完成检查和修复
- [x] nas.py: 完成检查和修复，新增 account(13) 和 kvcache(4) 子主题动作
- [x] gfs.py: 完成检查和修复，更新 namespace 和 migration_task 参数文档
- [ ] storage.py: 完成检查和修复，account 动作重命名 + 新增 create 动作 + 清理孤立函数
- [ ] self_service.py: 完成检查和修复：服务化创建LUN
- [ ] aiops.py: 完成检查和修复

### Testing Tasks

- [x] 执行测试用例：test/todo.md
- [ ] test/ 目录已移除 — 后续如需测试需重新搭建测试框架


### API reference clean task

- [x] 处理文件中的格式问题：reference/dme-api-stormgmt.md — 已完成全部格式修复

	该文件是通过PDF转换成的markdown，未正确将PDF中的表格转为Markdown格式，且未识别PDF表格中单元格内的换行
	请遍历文件中的所有API章节，按如下方式处理：
	- SLA在SLA项前添加行：**SLA**
	- 将SLA项和描述转换为Markdown表格
	- 将路径参数、查询参数、请求body参数、响应参数、内部对象属性、状态码表格内容转换为Markdown表格，请识别未被正确处理的单元格内的换行
	- 删除请求header参数
	- 格式化请求示例，按如下方式换行处理，并对请求body中的json格式进行格式化
	<METHOD> <URL> HTTP/1.1
	<HEADERS> （每个HEADER一行，请注意通过占位符<auth-token>替换X-Auth-Token的实际值）
	<BODY>
	- 格式化响应示例，按如下方式换行处理，并对响应body中的json格式进行格式化	
	HTTP/1.1 <状态码>
	<HEADERS>
	<BODY>
	- 状态码改为粗体：**状态码**
	
	注意不要使用脚本批量处理，请调用大模型理解能力，逐个API手动处理

## Current Project Status

**Package**: `pydme` (installable via `pip install -e .`)
**Active Topics**: 16
**Total Actions**: 423
**Total Functions**: 428

### Topic Structure

| # | Topic | Actions | File | Description |
|---|-------|---------|------|-------------|
| 1 | **protect** | 75 | `protect.py` | Protection (group/hypermetro/replication/snapshot/clone) |
| 2 | **san** | 66 | `san.py` | Storage area network (LUN/mapping/host/port_group) |
| 3 | **nas** | 61 | `nas.py` | Network attached storage (NFS/CIFS/DPC/quota/filesystem) |
| 4 | **storage** | 60 | `storage.py` | Storage device management (vstore/disk/pool/license) |
| 5 | **system** | 40 | `system.py` | System management (user/task/tag/region/cert/az/dc) |
| 6 | **aiops** | 26 | `aiops.py` | AIOps (alarm/performance/topology/health/diagnose) |
| 7 | **fcswitch** | 19 | `fcswitch.py` | FC fiber switch (port/zone/vsan/alias) |
| 8 | **gfs** | 14 | `gfs.py` | Global file system (namespace/migration) |
| 9 | **virt** | 14 | `virt.py` | Virtualization services (vm/datastore/host) |
| 10 | **server** | 10 | `server.py` | Server management (fan/disk/PCIe/power/NIC) |
| 11 | **tenant** | 10 | `tenant.py` | Tenant self service (LUN/tier/project) |
| 12 | **ipswitch** | 7 | `ipswitch.py` | IP switch (frame/board/port/power/fan) |
| 13 | **workflow** | 7 | `workflow.py` | Workflow management (template/instance) |
| 14 | **kube** | 6 | `kube.py` | Kubernetes management (cluster/node/pod) |
| 15 | **integrate** | 5 | `integrate.py` | Third-party integration (CMDB systems/hosts/apps) |
| 16 | **backup** | 3 | `backup.py` | Data backup management (cluster/capacity/quota) |

### CLI Command Pattern

```
pydme <topic> <subtopic> <action> [--param value ...]
```

Examples:
```
pydme san lun list --limit 100
pydme system user create --name admin --type 0
pydme protect group list
pydme nas nfs_share create --name share1
pydme system region list
pydme nas dpc list
pydme san physical_host_group show_related --hostgroup_id xxx
```

### Reference Documents

- `reference/dme-api-reference.md` — Structured API definitions (517 APIs, organized by topic)
- `reference/dme-api-stormgmt.md` — Original raw reference document
- `plans/101-gen-actions-for-not-impl-apis.md` — Plan for unimplemented APIs (32 remaining)

**Documentation**:
- `CLAUDE.md` — Development guide and task tracking (this file)
- `README.md` — Installation, CLI, and SDK usage documentation

### Recent Changes

- **Topic module renaming** (6 files): `virtualization→virt`, `kubernetes→kube`, `fc_switch→fcswitch`, `ip_switch→ipswitch`, `protection→protect`, `self_service→tenant`
- **New `integrate` topic**: Created `integrate.py` with 5 CMDB actions for third-party system integration
- **protect expansion**: Added 20 new actions — fs_hypermetro_pair(5), fs_snapshot(3), vstore_hypermetro_pair(6), hypermetro_domain(5), hypermetro_pair(1)
- **system region**: Added `region_list` and `region_query` actions
- **nas dpc**: Added `dpc_client_list` and `dpc_client_show` under new dpc subtopic
- **storage disk**: Added `disk_pool_list` for distributed disk pools; renamed existing `disk_pool_list→disk_domain_list`
- **san**: Added `physical_host_group show_related` and `mapping_view query_host_to_lun`
- **replication_pair upgrade**: URI updated from `lun-pairs` to `pairs` (8 functions)
- **Subtopic rename**: nas `dpc` subtopic → `dataturbo` (existing DPC parallel client actions)
- **Docstring format unification**: All Returns sections converted to JSON-style format
- **Obsolete function cleanup**: Removed 3 unused functions not registered in ACTIONS
- **Scripts cleanup**: Removed `scripts/` directory with temporary processing tools
