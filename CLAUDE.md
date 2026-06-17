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
    ├── nas.py         # NAS (NFS/CIFS/filesystem/quota/DPC→dataturbo)
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

## `.reasonix/` Directory — Development Support Files

Reasonix 工具在 `.reasonix/` 目录下维护辅助文件，已被 `.gitignore` 排除，不会提交到版本库中。

```
.reasonix/
├── plans/                       # 计划文档
│   ├── 001-generate-traverse-api-script.md
│   ├── 100.rewrite-action-funcs-to-follow-api-ref.md
│   ├── 101-gen-actions-for-not-impl-apis.md
│   ├── 102-update-actions-returns-docstring.md
│   ├── 300-add-action-risk-blacklist.md
│   ├── 500-test-all-actions.md
│   ├── 501-env-todo.md              # 待办：准备双活/A800环境 + 执行跳过用例
│   └── .gitkeep
├── reference/
│   ├── dme-api-reference/
│   │   └── .gitkeep              # 预留目录
│   └── dme-api-reference.md      # 结构化 API 参考文档（1.7MB，517+ API，225 引用对象）
├── scripts/                      # 辅助脚本
│   ├── 00-env.sh                 # 测试环境变量模板
│   ├── 00-lib.sh                 # 测试执行与记录库（exec_test 等函数）
│   ├── 02-storage-ids.sh         # storage 主题测试资源 ID
│   ├── 06-fcswitch-ids.sh        # fcswitch 主题测试资源 ID
│   ├── check_prose.py            # 检查 docstring 中的中文标点/错别字
│   ├── read_api_reference.py     # 读取原始 API 文档，提取结构化信息
│   └── traverse_api_reference.py # 遍历 dme-api-reference 目录生成汇总文档
└── output/                       # 中间产物（空，.gitkeep，运行时生成测试产物）
```

### 工具脚本说明

| 脚本 | 用途 |
|------|------|
| `scripts/read_api_reference.py` | 读取原始 HTML/Markdown API 文档，提取方法、URI、参数表格、响应字段、状态码等结构化信息，以 Markdown 格式输出 |
| `scripts/traverse_api_reference.py` | 遍历 `reference/dme-api-reference/` 目录，读取 `目录.md` 中的层级结构，调用 `read_api_reference.py` 处理每个叶节点 API 文件，生成汇总文档 |
| `scripts/00-lib.sh` | 测试执行与记录库 — `exec_test` 函数封装了 CLI 执行、输出解析、结果记录到报告的全流程 |
| `scripts/00-env.sh` | 测试环境变量模板 — endpoint, user, password 等全局配置 |
| `scripts/check_prose.py` | docstring 语言检查 — 自动扫描中文标点、错别字、格式一致性 |

### 计划文档索引

| 文件 | 状态 | 内容 |
|------|------|------|
| `plans/001-generate-traverse-api-script.md` | ✅ 完成 | 生成 `traverse_api_reference.py` 脚本遍历 API 文档 |
| `plans/100.rewrite-action-funcs-to-follow-api-ref.md` | ✅ 完成 | 按 API 参考文档重写所有 action 函数的 docstring、参数校验和响应描述 |
| `plans/101-gen-actions-for-not-impl-apis.md` | ✅ 完成 | 为未实现的 32 个 API 生成动作函数（含例外/升级/重命名任务） |
| `plans/102-update-actions-returns-docstring.md` | ⏳ 待执行 | 按 API 参考文档统一更新所有 action 函数的 Returns 段（10 批，~417 函数） |
| `plans/300-add-action-risk-blacklist.md` | ⏳ 待执行 | 在 `cli.py` 中增加风险确认机制，对 destructive 操作警告/拦截 |
| `plans/500-test-all-actions.md` | ✅ 完成 | 全量 427 动作覆盖测试计划 — **412/427 已覆盖（96.5%）**，200+ PASS，20+ 代码 Bug 修复 |

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

### Testing Tasks

- [x] 执行测试用例：test/todo.md
- [ ] test/ 目录已移除 — 后续如需测试需重新搭建测试框架

## Current Project Status

**Package**: `pydme` (installable via `pip install -e .`)
**Active Topics**: 16
**Total Actions**: 425 (注册在 ACTIONS 字典中的动作数)
**Total Functions**: 429 (包括 ACTIONS 引用的函数 + `__init__.py` 中的工具函数)

### Topic Structure

| # | Topic | Actions | Funcs | File | Description |
|---|-------|---------|-------|------|-------------|
| 1 | **protect** | 75 | 75 | `protect.py` | Protection (group/hypermetro/replication/snapshot/clone) |
| 2 | **san** | 66 | 67 | `san.py` | Storage area network (LUN/mapping/host/port_group) |
| 3 | **storage** | 62 | 63 | `storage.py` | Storage device management (vstore/disk/pool/license/account) |
| 4 | **nas** | 61 | 61 | `nas.py` | Network attached storage (NFS/CIFS/DPC/quota/filesystem) |
| 5 | **system** | 40 | 40 | `system.py` | System management (user/task/tag/region/cert/az/dc) |
| 6 | **aiops** | 26 | 28 | `aiops.py` | AIOps (alarm/performance/topology/health/diagnose) |
| 7 | **fcswitch** | 19 | 19 | `fcswitch.py` | FC fiber switch (port/zone/vsan/alias) |
| 8 | **gfs** | 14 | 14 | `gfs.py` | Global file system (namespace/migration) |
| 9 | **virt** | 14 | 14 | `virt.py` | Virtualization services (vm/datastore/host) |
| 10 | **server** | 10 | 10 | `server.py` | Server management (fan/disk/PCIe/power/NIC) |
| 11 | **tenant** | 10 | 10 | `tenant.py` | Tenant self service (LUN/tier/project) |
| 12 | **ipswitch** | 7 | 7 | `ipswitch.py` | IP switch (frame/board/port/power/fan) |
| 13 | **workflow** | 7 | 7 | `workflow.py` | Workflow management (template/instance) |
| 14 | **kube** | 6 | 6 | `kube.py` | Kubernetes management (cluster/node/pod) |
| 15 | **integrate** | 5 | 5 | `integrate.py` | Third-party integration (CMDB systems/hosts/apps) |
| 16 | **backup** | 3 | 3 | `backup.py` | Data backup management (cluster/capacity/quota) |
| | **Total** | **425** | **429** | 16 files | |

> **注意**：Functions 列可能多于 Actions 列（如 `aiops` 28 funcs vs 26 actions，`san` 67 funcs vs 66 actions），原因是有少数辅助/工具函数未注册到 ACTIONS 字典。

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
pydme nas dataturbo list
pydme san physical_host_group show_related --hostgroup_id xxx
```

## Config

`pydme/config/` 中存放运行时可配置的数据文件：

| 文件 | 用途 |
|------|------|
| `blacklist.json` | 风险操作黑名单 — 定义了 122 个 destructive/risky 动作，按 topic 组织。配合 `--accept-risk` 标志或 `DME_ACCEPT_RISK` 环境变量使用 |

### Reference Documents

- `.reasonix/reference/dme-api-reference.md` — 结构化 API 参考文档（78 个 H2 章节、240 个 H3 章节、263 个 H4 子章节，涵盖 DME 所有 API 定义：方法/URI/参数/响应/状态码，225 个引用对象类型）
- `.reasonix/plans/101-gen-actions-for-not-impl-apis.md` — 未实现 API 的生成计划（517 总 API 中 32 个待实现、76 个例外跳过、2 个重命名任务）
- `.reasonix/plans/500-test-all-actions.md` — 全量动作覆盖测试计划与执行报告（412/427 已覆盖，96.5%）

**Documentation**:
- `CLAUDE.md` — Development guide and task tracking (this file)
- `README.md` — Installation, CLI, and SDK usage documentation

### 待办任务 (TODOs)

- [ ] **完成剩余因环境限制跳过的测试用例** — 15 个 SKIP 动作需待双活环境、A800 环境、Pacific DataTurbo 数据就绪后执行（详见 `.reasonix/plans/501-env-todo.md`）
- [ ] **遍历所有动作的帮助信息，检查参数内部格式和响应体格式是否与 API 参考文档一致** — 参考 `102-update-actions-returns-docstring.md` 计划，按主题分批审核 docstring 中的 Returns 段和嵌套参数格式，确保与 `.reasonix/reference/dme-api-reference.md` 一致

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
- **`.reasonix/` directory setup**: Plans, scripts, and output files organized under `.reasonix/` (gitignored)
- **API reference migration**: Raw `reference/dme-api-stormgmt.md` cleaned and consolidated into `.reasonix/reference/dme-api-reference.md`
- **`reference/` directory removed**: Contents migrated to `.reasonix/reference/`
- **storage topic update**: Increased from 60→62 actions, 63 functions (account actions + cleanup)
- **Config system**: Added `pydme/config/blacklist.json` with 122 risky action keys for destructive operation safety
- **New plan — 102**: `update-actions-returns-docstring` — 待执行：按 API 参考统一更新 417 个函数的 Returns 段
- **New plan — 300**: `add-action-risk-blacklist` — 待执行：增加 `--accept-risk` 标志 + 风险拦截门
- **New plan — 500**: `test-all-actions` — 已完成：全量 427 ACTIONS 覆盖测试，374 已覆盖（88%）
- **Test infrastructure**: Added `.reasonix/scripts/00-lib.sh` (exec_test 库), `00-env.sh`, `02-storage-ids.sh`, `06-fcswitch-ids.sh` 等测试辅助脚本
- **Docstring quality**: Added `.reasonix/scripts/check_prose.py` for automated docstring language/style check
- **`install.sh`**: Added root-level install script (`git pull → pip uninstall → pip install -e .`)
- **Bug fixes**: 修复 `pydme/cli.py` 中 5 处 param_mapping 错误；修复 `pydme/actions/storage.py` 中 7 处 `{storage_id}` 路径参数缺失；修复 `pydme/actions/san.py` 中 3 处路径参数缺失（port_group、physical_host_group）；修复 `pydme/actions/protect.py` 中 `replication_link_list` URL 路径错误 + 参数名错误；新增 `replication_group_list` 和 `hypermetro_group_sync` 函数
- **新增 Phase 9**: 补充 53 个覆盖测试用例（NAS account/DPC、protect device_pair/replication_link、SAN storage_host_group、physical_host_group 等），实测 14+ PASS
- **测试结果**: 374/427 ACTIONS 覆盖（88%），200+ 用例 PASS，新增附录 C 全量动作覆盖清单

## Generated Files Convention

Reasonix 工具生成的辅助文件遵循以下目录约定：

| 类型 | 目录 |
|------|------|
| 计划文档 | `.reasonix/plans/` |
| 脚本文件 | `.reasonix/scripts/` |
| 输出文件 | `.reasonix/output/` |

