# 计划 600：新增 memstore topic（10 个 mock 动作）—— 记忆存储管理

## 概述

新增 **`memstore` topic**（记忆存储管理），包含 3 个 subtopic 与 10 个动作：

- direct actions（2 级命令）：`add` / `list` / `delete`
- subtopic `disk`（1 个）：`memstore disk list`
- subtopic `pool`（3 个）：`memstore pool create/list/delete`
- subtopic `namespace`（3 个）：`memstore namespace create/list/delete`

**所有动作均无真实 DME API**，通过本地 mock 数据实现：数据源为 `~/.config/pydme/mock/memstore.json`，动作函数直接读写该文件并模拟增删改查。

**用户已确认的关键决策**：

1. **memstore topic 默认走 mock，CLI 无条件跳过 DME 环境参数校验与登录**（不引入 `--mock` 开关；其他 topic 行为不变）；
2. **首次运行时预置一份示例数据**（1 个 memstore + 若干 disk/pool/namespace，结构自洽）；
3. 本次范围不含 `dme-mcp-server` / `dme-skills` 仓库同步。

## 背景与现状（已核实）

- 当前注册表：**17 topics / 476 actions**（`pydme.i18n.load_actions_registry()` 实测）；blacklist **11 topics / 141 keys**。
- 动作注册机制（`pydme/i18n.py`）：`actions_<lang>.yaml` 定义 topic 树（每动作 `name` 短名 / `func` / `params`），`funcs_<lang>.yaml` 存 `<topic>.<func>` 完整 docstring；`load_actions_registry()` 用 `getattr(import_module("pydme.actions.<topic>"), func)` 解析 → **新增动作只需：① `pydme/actions/memstore.py` 加函数 ② actions YAML 加注册条目 ③ funcs YAML 加 docstring，无需改 cli.py 的注册逻辑**。
- `pydme/actions/__init__.py` 会 `pkgutil.iter_modules` 自动导入 `pydme/actions/` 下所有非下划线模块 → 新建 `memstore.py` 即自动生效。
- CLI 执行路径（`pydme/cli.py`）有两处，**执行前都强制校验 `endpoint/user/password` 并 `login()`，否则 `sys.exit(1)`**：
  - 2 级命令（direct action）：约 L775–L889，校验在 L780–L784，登录在 L796–L803；
  - 3 级命令（subtopic action）：约 L927–L1049，校验在 L932–L936，登录在 L948–L955。
  - `--help` 路径（`print_action_help` / `print_topic_help` / `print_subtopic_help`）不涉及登录，无需改动。
- 参数注入：CLI 按 `inspect.signature(func)` 注解做类型转换（int/float/list/dict/bool），CLI 未声明的参数按 `param_mapping` 映射；`client` 首参由调用方注入（若签名含 `client` 则 `func(client, **params)`）。
- blacklist 语义（`cli.py _check_risk`）：`{topic: [action_key...]}`，命中且无 `--accept-risk`/`DME_ACCEPT_RISK` 时拒绝执行；用户覆盖文件 `~/.config/pydme/blacklist.json` 优先。
- 现状无任何 mock 机制（全仓库 `mock` 无代码命中）；`~/.config/pydme/` 当前只有 `blacklist.json` / `cache.json`，`mock/` 目录不存在。
- docstring 解析约束（`cli.parse_docstring`，REASONIX.md 已记录）：`Args:` 逐参数一行；`Returns:` 下一行必须 `{` 开头；嵌套结构必须用 `参数格式如下：[{` / `属性格式如下：{` 标记（裸 `格式：{` 会让内部字段泄漏成 CLI 参数）；字段行以 `,` 结尾。
- YAML 缩进规则（106 计划教训）：topic 条目 4 空格、topic 下 `description` 6 空格、direct action 条目 **10 空格**、subtopic 条目 8 空格、subtopic 下 `description` 10 空格、subtopic action 条目 **12 空格**。

## 动作清单（10 个）

| # | 命令 | action_key | func | 参数（不含 client） | mock 行为 |
|---|------|-----------|------|--------------------|-----------|
| 1 | `memstore add` | `add` | `add` | `name, num_of_disks, disk_size` | 新建 memstore（uuid），生成 N 块盘（location 全局未占用、uuid、size=disk_size），pools 为空；返回 memstore 对象 |
| 2 | `memstore list` | `list` | `list` | `name`（可选过滤） | 返回 memstore 数组（含完整 disks/pools），name 支持包含匹配 |
| 3 | `memstore delete` | `delete` | `delete` | `id` | 删除 memstore；若其下存在 pool 则拒绝（提示先删 pool）；返回操作结果 |
| 4 | `memstore disk list` | `disk_list` | `disk_list` | — | 汇总所有 memstore 的盘，返回 `[{id, location, size, allocated_size}]`；`allocated_size = Σ(disk.pools[].space)` |
| 5 | `memstore pool create` | `pool_create` | `pool_create` | `name, size, disks` | 在指定 location 盘上打散创建池：`pool.disks[].space` 之和 = size，且每盘分配 ≤ 剩余空间；同步写回 `disk.pools`；返回 pool 对象 |
| 6 | `memstore pool list` | `pool_list` | `pool_list` | `name`（可选过滤） | 返回 `[{id, name, size, allocated_size}]`；`allocated_size = Σ(namespaces[].space)` |
| 7 | `memstore pool delete` | `pool_delete` | `pool_delete` | `id` | 删除 pool；若其下有 namespace 则拒绝；同时从相关 `disk.pools` 移除分配；返回操作结果 |
| 8 | `memstore namespace create` | `namespace_create` | `namespace_create` | `pool_id, name, space, eviction, retention, clients` | 校验 pool 存在、space ≤ pool 剩余、eviction 1~99、retention >1、clients 元素 `{ip, type}`（type ∈ ip/ip_segment）；追加到 `pool.namespaces`；返回 namespace 对象 |
| 9 | `memstore namespace list` | `namespace_list` | `namespace_list` | `name`（可选）、`pool_id`（可选） | 全局/按名/按池过滤（可组合），返回 `[{id, pool_id, pool_name, name, space, eviction, retention, clients}]` |
| 10 | `memstore namespace delete` | `namespace_delete` | `namespace_delete` | `id` | 从所属 pool 的 namespaces 中删除；返回操作结果 |

命令示例：

```bash
pydme memstore add --name ms01 --num_of_disks 3 --disk_size 32768
pydme memstore list [--name ms01]
pydme memstore delete --id <memstore_id>
pydme memstore disk list
pydme memstore pool create --name pool01 --size 4096 --disks '["FRAME0.SLOT0","FRAME0.SLOT1"]'
pydme memstore pool list [--name pool01]
pydme memstore pool delete --id <pool_id>
pydme memstore namespace create --pool_id <pool_id> --name ns01 --space 1024 --eviction 80 --retention 24 \
  --clients '[{"ip":"192.168.1.10","type":"ip"},{"ip":"192.168.1.0/24","type":"ip_segment"}]'
pydme memstore namespace list [--name ns01] [--pool_id <pool_id>]
pydme memstore namespace delete --id <namespace_id>
```

约定：
- 返回结构：`list` 类动作返回 JSON 数组；`create`/`add` 返回创建的实体对象；`delete` 返回 `{"success": true, "id": "<id>", "message": "..."}`。
- `disks` 参数支持 JSON 数组（首选）或逗号分隔字符串（CLI 已有 list 类型回退逻辑）；`clients` 必须传 JSON（元素为对象，逗号分隔无意义，docstring 中注明）。
- `disk_size` 取值约束 `16384 / 32768 / 65536`（GB）；`num_of_disks` ≥ 1 且不超过可用 location 数。
- 函数签名首参保持 `client: DMEAPIClient = None`（遵循仓库约定，mock 实现不依赖 client；后续接真实 API 时签名不变）。

## mock 数据模型（`~/.config/pydme/mock/memstore.json`）

顶层为 **memstore 数组**，结构如下：

```
[
  {
    "id": "<uuid>", "name": "<1~128 字符>",
    "disks": [
      { "id": "<uuid>", "location": "FRAME<0~47>.SLOT<0~11>",
        "size": 16384|32768|65536,
        "pools": [ { "pool": "<pool_id>", "space": "<GB, 1~size>" } ] }
    ],
    "pools": [
      { "id": "<uuid>", "name": "<1~128 字符>",
        "disks": [ { "disk": "<disk_id>", "space": "<GB, 1~disk_size>" } ],
        "namespaces": [
          { "id": "<uuid>", "name": "<1~128 字符>",
            "space": "<GB, 1~pool_size>", "eviction": "<1~99>", "retention": "<小时, >1>",
            "clients": [ { "ip": "<client_ip>", "type": "ip|ip_segment" } ] }
        ] }
    ]
  }
]
```

关键派生关系（必须始终自洽）：

- `disk.allocated_size`（响应字段，非存储字段）= `Σ(disk.pools[].space)`；
- `pool.allocated_size`（响应字段，非存储字段）= `Σ(pool.namespaces[].space)`；
- `pool.size`（响应字段）= `Σ(pool.disks[].space)`；
- **双向引用**：`pool.disks[].disk` ↔ `disk.pools[].pool` 互为镜像，任何 pool 创建/删除都必须同步两侧；
- location 全局唯一（跨 memstore），分配时扫描 `FRAME0~47 × SLOT0~11`（共 576 个位置）跳过已占用项；无可用位置时报错。

### 预置示例数据（首次运行写入）

文件不存在时自动创建目录并写入以下自洽示例（暴露给 `memstore list`，便于开箱验证）：

```json
[
  {
    "id": "00000000-0000-0000-0000-000000000001",
    "name": "demo-memstore",
    "disks": [
      {"id": "00000000-0000-0000-0000-0000000000d1", "location": "FRAME0.SLOT0", "size": 32768,
       "pools": [{"pool": "00000000-0000-0000-0000-0000000000p1", "space": 1024}]},
      {"id": "00000000-0000-0000-0000-0000000000d2", "location": "FRAME0.SLOT1", "size": 32768,
       "pools": [{"pool": "00000000-0000-0000-0000-0000000000p1", "space": 1024}]}
    ],
    "pools": [
      {"id": "00000000-0000-0000-0000-0000000000p1", "name": "demo-pool",
       "disks": [{"disk": "00000000-0000-0000-0000-0000000000d1", "space": 1024},
                 {"disk": "00000000-0000-0000-0000-0000000000d2", "space": 1024}],
       "namespaces": [
         {"id": "00000000-0000-0000-0000-0000000000n1", "name": "demo-ns", "space": 512,
          "eviction": 80, "retention": 24,
          "clients": [{"ip": "192.168.1.10", "type": "ip"}]}
       ]}
    ]
  }
]
```

（示例中 uuid 形如 `…0001` 仅为可读占位；实际写入时用标准 uuid4 生成的合法 UUID 字符串，p1/d1 等简写同样替换为真实 uuid。pool.size=2048，namespace.space=512 ≤ 2048，自洽。）

## mock 基础设施

新建 **`pydme/mockdata.py`**（与 `client.py` / `i18n.py` 平级，零第三方依赖，仅 stdlib：`json`/`os`/`pathlib`/`uuid`）：

| 函数 | 职责 |
|------|------|
| `MEMSTORE_MOCK_FILE = Path.home()/'.config'/'pydme'/'mock'/'memstore.json'` | 路径常量 |
| `ensure_memstore_mock() -> list` | 文件不存在 → 建目录 + 写入预置示例；返回解析后的数组 |
| `load_memstores() -> list` | 读文件（损坏时回退示例并告警，不覆盖用户文件） |
| `save_memstores(data: list)` | 原子写回（`tmp` + `os.replace`），保证文件权限与编码 utf-8 |
| `new_uuid() -> str` | uuid4 字符串 |
| `iter_locations()` / `alloc_locations(count, used)` | 生成 `FRAME<i>.SLOT<j>`，跳过 used 中已占用的位置 |
| `find_*` 系列 helper | `find_memstore(data, id)` / `find_disk(data, id|location)` / `find_pool(data, id)` / `find_namespace(data, id)`，返回引用以就地修改 |

同时提供最小校验 helper（供动作函数复用）：`validate_name(name)`（1~128）、`validate_disk_size`、`validate_int_range`。

## CLI 改动：memstore 默认跳过 DME 校验

在 `pydme/cli.py` 的 two 处执行路径前加入 topic 判断（推荐抽 helper 便于测试）：

```python
def _requires_dme_login(topic: str) -> bool:
    """memstore 为纯 mock topic，无需 DME endpoint 校验与登录。"""
    return topic != 'memstore'
```

- 2 级路径（约 L775–L805）：`if _requires_dme_login(args.topic):` 包住「endpoint/user/password 校验 + `DMEAPIClient(...)` 创建 + `login()`」；memstore 分支直接 `cli.client = None`，跳过 `Connecting to DME` / `Login failed` 输出。
- 3 级路径（约 L927–L957）：同样处理。
- 其余逻辑（`_check_risk`、参数解析、`Executing:` 打印、`func(client, **typed_params)`）保持不变；memstore 函数收到 `client=None`，内部完全依赖 `pydme/mockdata.py`。
- **不改** `--help` 路径与 `execute_action()`（程序化调用本就不登录）。

## 阶段与里程碑

### M1：mock 基础设施 + 动作函数 + CLI 跳过登录

1. 新建 `pydme/mockdata.py`（上述 helper，含预置示例数据）。
2. 新建 `pydme/actions/memstore.py`：模块 docstring（英文，如 `"""Memory storage (memstore) management operations (mock-backed)"""`）；实现 10 个函数，风格对齐 `hci.py`（client 首参、参数默认 `None`、就地修改后 `save_memstores`）。校验失败统一 `raise ValueError("...")`（CLI 会捕获并打印 `Execution failed: ...`）。
3. 修改 `pydme/cli.py`：新增 `_requires_dme_login()`，两处执行路径按上节改造。
4. 静态校验：`python3 -c "import pydme.actions.memstore, pydme.mockdata"`；隔离 `HOME` 下直接调用 `pydme.actions.memstore` 各函数做一次冒烟（add→list→disk list→pool create→namespace create→delete 链路）。

### M2：i18n 注册与 docstring（4 个 YAML）

1. `actions_zh_CN.yaml` / `actions_en_US.yaml`：新增 `memstore` topic 条目（按字母序插入，`hci` 之后、`integrate` 之前）：
   - topic description：zh「记忆存储 (Memstore) 管理相关操作」/ en `Memory storage (memstore) management related operations`；
   - `actions:` 下 **10 空格缩进**列 direct actions：`add` / `list` / `delete`（`func` 同名，`params` 与签名一致：add→`[name, num_of_disks, disk_size]`，list→`[name]`，delete→`[id]`）；
   - `subtopics:` 下 **8 空格缩进**列 `disk` / `pool` / `namespace`（含 zh/en description），其下 action 条目 **12 空格缩进**，`name` 用短名、`func` 带前缀（`disk_list` / `pool_create` / `pool_list` / `pool_delete` / `namespace_create` / `namespace_list` / `namespace_delete`）；
   - 两份文件除 `description` 外结构完全一致。
2. `funcs_zh_CN.yaml` / `funcs_en_US.yaml`：新增 10 份 `<topic>.<func>` docstring，遵循 REASONIX 约定：
   - `Args:` 逐参数一行，约束写全（如 `disk_size: 单盘大小 (GB)，可选值：16384 / 32768 / 65536`）；
   - `clients` 用 `参数格式如下：[{` 展开 `ip` / `type`（类型说明 `type: 客户端类型，ip 或 ip_segment`）；
   - `Returns:` 下一行以 `{` 开头，字段行逗号结尾；嵌套数组用 `参数格式如下：[{` 标记（如 memstore list 的 `disks` / `pools`、namespace list 的 `clients`）。
   - 中文为权威源，英文翻译、术语保留原文（memstore / pool / namespace / eviction / retention）。
3. round-trip 校验（复用 `.reasonix/scripts/gen_actions_i18n.py` 的解析逻辑或手写 stdlib 脚本）：
   - 重建 action_key 集合 == 476 + 10 = **486**，含 `disk_list` / `pool_create` / `pool_list` / `pool_delete` / `namespace_create` / `namespace_list` / `namespace_delete`；
   - 10 个 `func` 可在 `pydme.actions.memstore` 解析；`description` == docstring 首行；`params` == 函数签名（不含 `client`）；
   - 双语 `actions_*.yaml` 结构一致（name/func/params/subtopic 逐项对齐）。

### M3：blacklist.json 更新

删除类动作列入高危（与现有 `san`/`virt` 先例一致）：

```json
"memstore": ["delete", "pool_delete", "namespace_delete"]
```

- blacklist 从 141 → **144**（topics 11 → 12）；
- 校验 `pydme memstore delete --help` 显示 `Risk Level: High`，`memstore list/pool list` 显示 `Low`；
- 用户覆盖文件 `~/.config/pydme/blacklist.json` 若存在，提示需手动合并（不修改用户文件）。

### M4：验证（CLI help 遍历 + mock 全链路 E2E）

新增 `.reasonix/scripts/600-verify-memstore.sh`（复用 `00-lib.sh` 的 `exec_test` 模式），输出记录到 `.reasonix/output/600-verify.md`：

1. **help 遍历**：10 个动作 × zh_CN/en_US（`--lang`）共 20 次 `--help`，无报错、参数无泄漏、Risk Level 正确；
2. **隔离 HOME 的 mock 全链路**（`HOME=$(mktemp -d)`，不触网、不需 DME 环境）：
   - 首次 `pydme memstore list` → 返回预置示例（1 条 demo-memstore），并确认 `~/.config/pydme/mock/memstore.json` 已创建；
   - `pydme memstore add --name ms01 --num_of_disks 2 --disk_size 16384` → 新 memstore 的 disks 有 2 条、location 不与示例重复；
   - `pydme memstore list --name ms01` → 过滤命中 1 条；
   - `pydme memstore disk list` → `allocated_size` 与 `disk.pools` 求和一致；
   - `pydme memstore pool create --name pool02 --size 4096 --disks '["FRAME0.SLOT2","FRAME0.SLOT3"]'` → `pool.disks` 打散分配之和 = 4096，两侧双向引用同步；
   - `pydme memstore pool list` / `--name pool02` → `allocated_size` = 0；
   - `pydme memstore namespace create --pool_id <id> --name ns02 --space 1024 --eviction 80 --retention 24 --clients '[...]'` → namespace 入库，`pool.allocated_size` = 1024；
   - `pydme memstore namespace list` / `--name` / `--pool_id` → 三种查询均正确，`pool_name` 正确填充；
   - 负例：`disk_size 1000`（非法）、`space 99999`（超池）、`pool delete` 有 namespace（拒绝）、`namespace delete` 不存在的 id（报错）——均应给出明确错误信息且不破坏文件；
   - `pydme memstore delete --id <demo_id>`（带 `--accept-risk`）→ 删除成功；`pool delete` → 释放后 `disk list` 的 `allocated_size` 归零；
3. **回归**：抽查 `pydme storage --help`、`pydme storage disk list --help`、`pydme hci list --help` 等既有 topic，确认 `_requires_dme_login` 改动未影响其他 topic 的登录校验路径（仍要求 DME 参数）。

### M5：README.md / README_zh.md 更新

1. `Project Structure`：`17 topic modules` → `18`，`476 actions` → `486`，模块列表加 `memstore.py`（字母序）；
2. `Available topics` 表：总数 476 → 486，新增 `memstore` 行（10 actions，描述「Memory storage (memstore) management (mock-backed)」/ 中文对应）；
3. 测试覆盖说明：注明 memstore 10 个动作为 **mock 实现、无 API E2E**，验证方式为隔离 HOME 的 mock 链路 + help 遍历（引用 `.reasonix/output/600-verify.md`）；
4. README_zh.md 同步全部改动。

### M6：REASONIX.md 更新

- Layout：`17 topic modules` → `18`、`476 action functions` → `486`；
- `blacklist.json — 141 ...` → `144`（含 memstore 3 个）；
- E2E test status 行：补「memstore 10 个动作为 mock 实现，隔离 HOME 验证通过」；
- `Watch out for` 新增条目：
  - `memstore` 为 **mock topic**：数据源 `~/.config/pydme/mock/memstore.json`，CLI 对 memstore **跳过 DME 参数校验与登录**（`cli._requires_dme_login`），其他 topic 不变；
  - **双向引用一致性**：`pool.disks[].disk` ↔ `disk.pools[].pool` 必须同步维护，否则 `allocated_size` 失真；
  - location 全局唯一（`FRAME0~47.SLOT0~11`，共 576 个），分配需跳过已占用；
  - 删除语义：memstore 有 pool、pool 有 namespace 时拒绝删除（需先清理子资源）。

## 验收标准

| # | 标准 |
|---|------|
| 1 | `pydme/actions/memstore.py` 10 个函数 + `pydme/mockdata.py` 可 import；`pydme.actions.memstore` 的 10 个 func 均可 `getattr` 解析 |
| 2 | `pydme memstore` 在 `--list-topics` 树中显示，含 disk/pool/namespace 3 个 subtopic 与 10 个 action；`pydme memstore --help` / `disk --help` / `pool --help` / `namespace --help` 正常渲染 |
| 3 | **memstore 所有动作（含 3 级命令）在无 `DME_API_ENDPOINT/USERNAME/PASSWORD` 时可直接执行**，不出现 `Error: endpoint, user and password arguments are required`，不尝试连接 DME；其他 topic 仍要求 DME 参数 |
| 4 | 10 个动作 × zh_CN/en_US 的 `--help` 遍历（20 次）零报错、无参数泄漏、Risk Level 正确（delete 类 High） |
| 5 | 隔离 HOME 的 mock 全链路通过：首次自动生成示例数据；add/list/delete、disk list、pool create/list/delete、namespace create/list/delete 行为与本文档约定一致；负例报错清晰且不破坏 JSON 文件 |
| 6 | mock 文件结构自洽：`disk.pools` ↔ `pool.disks` 双向一致；`allocated_size` / `pool.size` 派生值计算正确 |
| 7 | 4 个 i18n YAML 更新完成，round-trip 校验通过（486 个 action_key 重建一致、func 可解析、description==docstring 首行、params==签名、双语结构一致） |
| 8 | `blacklist.json` 含 memstore 3 个删除动作（141→144），`--accept-risk`/`DME_ACCEPT_RISK` 生效 |
| 9 | README.md / README_zh.md / REASONIX.md 同步更新（486、18 topics、144、mock 说明），无 476/17/141 等过期数字残留 |
| 10 | 既有 476 个动作的 `--help` 与登录校验行为不回归（抽查代表性子主题） |

## 注意与风险

- **cli.py 两处路径都要改**：2 级与 3 级执行路径分别有一份「校验 + 登录」代码块，遗漏任一处会导致部分 memstore 命令仍要求 DME 参数（help 路径不受影响，容易误判为完成）。
- **双向引用一致性**：`pool.disks` 与 `disk.pools` 必须在同一事务式函数内同步写；pool delete 需移除盘侧分配，否则 `allocated_size` 越用越大。
- **location 分配**：必须跨 memstore 全局去重；`num_of_disks` 超过剩余位置时报错而非静默截断。
- **整数约束**：`eviction` 1~99、`retention` >1、`space` 1~pool 剩余空间、`disk_size` ∈ {16384,32768,65536} 全部在 `ValueError` 中显式校验，CLI 会打印 `Execution failed: ...`。
- **YAML 缩进**：direct action 10 空格 / subtopic 8 空格 / subtopic action 12 空格——错位会被 `parse_actions_yaml` 归类错误（106 计划已踩坑）。
- **docstring 泄漏**：`clients`、`disks`、`pools`、`namespaces` 等嵌套结构必须用 `参数格式如下：[{` / `属性格式如下：{` 标记；`Returns:` 行后首行必须 `{`。
- **mock 文件损坏**：`load_memstores()` 遇到 JSON 解析失败时告警并回退到示例数据（不覆盖用户原文件），避免 CLI 直接崩溃。
- **并发写**：CLI 单用户场景不考虑文件锁；如后续引入并发，再补 `fcntl` 锁。
- **`client=None`**：memstore 函数签名保留 `client: DMEAPIClient = None`，函数体内不使用；若未来接入真实 API，只需替换函数体，不影响 CLI/注册表。
- **blacklist 用户覆盖文件**：`~/.config/pydme/blacklist.json` 优先，若用户机器已有旧副本，新高危 key 需手动合并（实施时提示，不修改用户文件）。

## 执行顺序

M1（mockdata.py + memstore.py + cli.py 跳过登录）→ M2（actions/funcs YAML ×4 + round-trip 校验）→ M3（blacklist）→ M4（help 遍历 + 隔离 HOME mock E2E + 回归）→ M5（README）→ M6（REASONIX.md）

---

## 实施完成记录

| 里程碑 | 状态 | 说明 |
|--------|------|------|
| M1 | ✅ | 新建 `pydme/mockdata.py`（路径常量/示例数据/读写/校验/location 分配/find/派生值）+ `pydme/actions/memstore.py` 10 函数；`cli.py` 新增 `MOCK_ONLY_TOPICS` 与 `_requires_dme_login()`，2 级/3 级执行路径对 memstore 跳过 DME 参数校验与登录（`cli.client = None`）；**两处 `func(client, …)` 改为 `func(cli.client, …)`**（mock 分支无局部 `client` 变量，已踩坑修复）；`builtins.list` 规避 `def list` 遮蔽（`isinstance` 踩坑修复） |
| M2 | ✅ | `actions_zh_CN/en_US.yaml` 注册 memstore topic（3 direct + 3 subtopic 10 动作）；`funcs_zh_CN/en_US.yaml` 新增 10 份 docstring；round-trip 校验通过（18 topics / 486 actions / func 可解析 / description==首行 / params==签名 / 双语结构一致 / Returns 以 `{` 开头） |
| M3 | ✅ | `blacklist.json` 新增 `memstore` 3 个删除动作（141→144，12 topics） |
| M4 | ✅ | `.reasonix/scripts/600-verify-memstore.sh`：20 次 help 遍历（zh/en，Risk 断言）+ 22 项隔离 HOME mock 全链路（seed/add/list 过滤/disk list 派生/池打散与双向同步/pool list/namespace create/list 三种查询/5 项负例/删除链路/文件完整性）+ 2 项回归（storage 无 DME 参数仍拒绝、hci help 正常），44 项全 PASS；记录见 `.reasonix/output/600-verify.md` |
| M5 | ✅ | README.md / README_zh.md：structure 486+memstore.py、topics 表（486 / memstore 10）、risk 表（12 topics / 144 / memstore 3）、mock 验证说明，中英同步 |
| M6 | ✅ | REASONIX.md：18 topics / 486 actions / mockdata.py 与 `_requires_dme_login` 说明 / blacklist 144 / E2E 状态行；Watch out for 新增 4 条（mock-only topic 注册、双向引用、约束与删除语义、builtins.list 遮蔽） |

**与计划的偏差（1 项）**：list 类动作实际返回 `{"memstores": [...]}` / `{"disks": [...]}` / `{"pools": [...]}` / `{"namespaces": [...]}` 包装对象，而非计划初稿的裸 JSON 数组——为使 `Returns:` 满足「下一行以 `{` 开头」的 docstring 渲染约定并与真实 API 响应风格一致；CLI 输出仍直观。

---

## 后续修订（R2：字段统一为"容量"）

用户要求调整 memstore 实现，要点如下（代码/注册表/docstring/验证脚本/REASONIX 已同步，验证 49 项全 PASS，见 `.reasonix/output/600-verify.md`）：

| 动作 | 变更 |
|------|------|
| `memstore list` / `add` | 响应仅返回摘要 `{id, name, raw_capacity（所有盘容量总和）, pool_capacity（所有池容量总和）, pool_used_capacity（所有池已用容量总和）}`，**不再返回盘列表与池列表** |
| `memstore add` | 每个记忆存储 **FRAME 独立编号**（从 FRAME0 开始，每 FRAME 12 盘，跨存储位置可重复、单存储内唯一）——`mockdata.alloc_locations(used, count)` 改为按单存储已占用位置分配 |
| `memstore delete` | `message` → `memstore deleted: <memstore_name>` |
| `memstore pool create` | 必须指定 `storage_id`；**去掉 `disks`**，新增 `num_of_disks`（自动选分配容量最低的盘，池容量均分，超出所选盘剩余容量报错）；`size` → `capacity` |
| `memstore pool list` | 新增 `storage_id` 过滤；`size` → `capacity`、`allocated_size` → `used_capacity` |
| `memstore namespace create` | `space` → `capacity`（响应含 `used_capacity`，初始 0） |
| `memstore namespace list` | 新增 `storage_id` 过滤；`space` → `capacity`、新增 `used_capacity`（命名空间已用容量，mock 数据中存储） |
| `memstore namespace delete` | `message` → `namespace deleted: <namespace_name>` |
| `memstore disk list` | 新增 `storage_id` 过滤；新增 `storage_id` / `storage_name` 字段；`size` → `capacity`、`allocated_size` → `allocated_capacity`；新增 `pools` 列表（`pool_id` / `pool_name` / `allocated_capacity`） |
| mock 数据模型 | 所有空间/大小字段统一为容量：`disk.size`→`disk.capacity`、`disk.pools[].space`→`.capacity`、`pool.disks[].space`→`.capacity`、`namespace.space`→`namespace.capacity`，新增 `namespace.used_capacity`（示例数据 256）；派生值改名：`disk_allocated_capacity` / `pool_capacity` / `pool_used_capacity` / `memstore_raw_capacity` / `memstore_pool_capacity` / `memstore_pool_used_capacity` |

---

## 后续修订（R3：disk show 新增，disk list 精简）

| 动作 | 变更 |
|------|------|
| `memstore disk list` | 响应**去掉 `pools` 字段**（保留 id / storage_id / storage_name / location / capacity / allocated_capacity） |
| `memstore disk show`（新增） | 按盘 ID 查看详情（`--id`），响应在 disk list 字段基础上增加 `pools` 列表（`pool_id` / `pool_name` / `allocated_capacity`）；不在任何存储中时报错 |

总数更新：18 topics / **487 actions**，memstore 11 个动作；验证脚本 53 项全 PASS（新增 disk show help 遍历、disk show 字段与 pools 断言、disk not found 负例），README / README_zh / REASONIX 数字同步（486→487、10→11）。

---

## 后续修订（R4：pool show 新增，pool create 响应对齐 show）

| 动作 | 变更 |
|------|------|
| `memstore pool show`（新增） | 按存储池 ID 查看详情（`--id`），响应在 pool list 字段（id / name / capacity / used_capacity）基础上增加 `disks` 列表（`disk_id` / `location` / `allocated_capacity`）与 `namespaces` 列表（`id` / `name` / `capacity` / `used_capacity`）；池不存在时报错 |
| `memstore pool create` | 响应字段与 `pool show` 保持一致（同一 `_pool_detail()` helper，创建时 `used_capacity`=0、`namespaces` 为空） |

总数更新：18 topics / **488 actions**，memstore 12 个动作；验证脚本 59 项全 PASS（新增 pool show help 遍历、pool create 响应结构、pool show disks/namespaces 断言、pool not found 负例），README / README_zh / REASONIX 数字同步（487→488、11→12）。

---

## 后续修订（R5：pool list/show/create 增加 storage 归属字段）

| 动作 | 变更 |
|------|------|
| `memstore pool list` / `pool show` / `pool create` | 响应增加 `storage_id`（所属记忆存储 ID）与 `storage_name`（所属记忆存储名称），三处共用同一 `_pool_detail()` / `pool_list` 逻辑 |

动作数不变（488 / memstore 12）；验证脚本 59 项全 PASS（pool create/show/list 的 storage 字段断言），无 README 数字变更。

---

## 后续修订（R6：namespace list 增加 storage 归属，namespace create 响应对齐与可选参数）

| 动作 | 变更 |
|------|------|
| `memstore namespace list` | 响应增加 `storage_id`（所属记忆存储 ID）与 `storage_name`（所属记忆存储名称） |
| `memstore namespace create` | 响应与 `namespace list` 保持一致（同一 `_namespace_detail()` helper，含 `pool_id` / `pool_name` / `storage_id` / `storage_name` 等全部字段）；参数 `eviction`（默认 80）、`retention`（默认 72 小时 = 3 天）、`clients`（默认空）修改为可选 |

动作数不变（488 / memstore 12）；验证脚本 63 项全 PASS（新增默认值断言、create 响应结构断言、显式传参生效与清理、list storage 字段断言），无 README 数字变更。

> 注：用户原文写作 "memstore namespace add"，按现有动作命名统一处理为 `namespace create`。
