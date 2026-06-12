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
    ├── fc_switch.py   # FC switch management
    ├── gfs.py         # Global file system
    ├── ip_switch.py   # IP switch management
    ├── kubernetes.py  # Kubernetes management
    ├── nas.py         # NAS (NFS/CIFS/filesystem/quota)
    ├── protection.py  # Protection (snapshot/dual-active/replication)
    ├── san.py         # SAN (LUN/mapping view/host)
    ├── self_service.py# Tenant self service
    ├── server.py      # Server management
    ├── storage.py     # Storage device management
    ├── system.py      # System management
    ├── virtualization.py # Virtualization services
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

### Current Project Status

**Package**: `pydme` (installable via `pip install -e .`)
**Active Topics**: 15
**Total Actions**: 395

**Topic Structure**:
1. system (37 actions) - System management (用户/标签/任务/证书)
2. san (64 actions) - Storage area network
3. storage (60 actions) - Storage device management
4. nas (59 actions) - Network attached storage
5. protection (54 actions) - Protection management
6. aiops (25 actions) - AIOps intelligent operations
7. fc_switch (19 actions) - FC fiber switch management
8. gfs (14 actions) - Global file system
9. virtualization (14 actions) - Virtualization services
10. server (10 actions) - Server management
11. self_service (10 actions) - Tenant self service
12. ip_switch (7 actions) - IP switch management
13. workflow (7 actions) - Workflow management
14. kubernetes (6 actions) - Kubernetes management
15. backup (3 actions) - Data backup management

**Documentation**:
- `CLAUDE.md` — Development guide and task tracking (this file)
- `README.md` — Installation, CLI, and SDK usage documentation

**Recent Changes**:
- **Package restructuring**: Migrated from `scripts/` flat layout to `pydme/` installable package with `pyproject.toml`
- **system.py expansion**: Grew from 8 to 37 actions — significantly expanded system management capabilities
- **nas.py account subtopic**: Added 13 UNIX user/group management actions (create/list/show/modify/batch_delete/add_group/remove_group) plus dataturbo_admin_list
- **nas.py kvcache subtopic**: Added 4 KV Cache management actions (list/batch_create/modify/batch_delete)
- **gfs.py parameter update**: Updated namespace_create/modify/list and migration_task_create/modify/list parameter docs with proper constraint format and types
- **storage.py account cleanup**: Renamed 9 account functions to match ACTIONS keys, added create_local_user/create_unix_user/create_windows_user actions, removed 3 orphaned functions
- **Parameter format refactoring**: Unified structured parameter docstring format across all action modules
- **Removed obsolete files**: `scripts/util/`, `SKILL.md`, `param-doc-format.md`, `test/` directory
