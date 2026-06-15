# 计划：按 API 参考文档更新所有 action 函数的 Returns 段

## 概述

目前 16 个 action 文件中总计 **~417 个函数含 `Returns:` 段**，但 Returns 描述存在以下问题：

| 问题 | 影响 |
|------|------|
| 纯文字 Returns（"任务列表""无"等）无结构描述 | ~93 个函数（22%） |
| JSON 式 Returns 仅列出 5-6 个核心字段，API 实际有 20-30+ | ~324 个函数（78%） |
| 嵌套引用对象（Volume→Attachment、Vm→VMCpu 等）未展开 | 200+ 个函数 |
| 部分字段名不匹配（如 `total` vs `count`） | 少量 |

本计划按 `.reasonix/output/dme-api-reference.md`（517 个 API 定义、225 个引用对象类型）逐 topic 修复所有 Returns 段。

## 规则

| 响应复杂度 | 格式 | 示例 |
|-----------|------|------|
| **简单结构**（1-3 个普通字段，无嵌套） | 文本描述 | `Returns: 任务ID。` |
| **复杂结构**（多个字段 + 嵌套对象/列表） | JSON 风格 + `参数格式如下：[{` | `Returns:\n    {\n        total: ... (int32),\n        volumes: LUN 列表 (List<VolumeInfo>)。参数格式如下：[{\n            ...\n        }, ...]\n    }` |
| **无返回值**（如 delete/refresh） | 文本描述 | `Returns: 无。` |

### JSON 格式约定（复杂结构时使用）

严格遵循 CLAUDE.md 中的 docstring 格式约定：
- 以 `{` 开头，不加前缀文字
- 嵌套列表用 `参数格式如下：[{` 标记
- 嵌套对象用 `属性格式如下：{` 标记
- 无引号，英文括号约束，枚举用 `可选值：enum1 (描述), enum2 (描述)`
- 字段行末加 `,`
- `}` 平衡

## 匹配方法

每个函数已知其调用的 API URI（函数体中的 `self.post/client.post` URL），在 `dme-api-reference.md` 中搜索对应的 `**Method / URI**` 块，然后：
1. 读取 `**响应字段**` 表 → 判断响应复杂度
2. 简单结构 → 文本描述；复杂结构 → 读取 `**响应引用对象**` 表 → 按 JSON 格式编写

## 分批执行计划

### 第 1 批：`protect.py`（75 个 Returns）

**纯文字→补充（7 个）**：`hypermetro_group_list`, `hypermetro_pair_list`, `hypermetro_domain_list`, `replication_pair_list`, `device_pair_list`, `replication_link_list`, `snapshot_list`

**JSON 补全（68 个）**：补齐字段 + 嵌套对象（MetroPairResponse→metro_pair_config_detail 等）

### 第 2 批：`san.py`（67 个 Returns）

**纯文字→补充（~12 个）**：`storage_host_create/modify/delete` 等

**JSON 补全（~55 个）**：如 `lun_list` Volume 对象 5→28 字段 + 嵌套 `attachments`(Attachment)

### 第 3 批：`nas.py`（61 个 Returns）

**纯文字→补充（~11 个）**：`cifs_share_list`, `filesystem_list`, `quota_list`, `namespace_show` 等

**JSON 补全（~50 个）**：CifsShare + CifsAuditItem、FileSystemSummary、NfsShare 等

### 第 4 批：`system.py`（40 个 Returns，纯文字最多）

**纯文字→补充（~27 个）**：所有 `todo_task_*`、`task_*`、`tag_*`、`tag_type_*` + `user_create`, `dc_show` 等

**JSON 补全（~13 个）**：TaskInfo、TodoTask、User、Tag 等

### 第 5 批：`storage.py`（53 个 Returns）

**纯文字→补充（3 个）**：`storage_refresh`, `storage_unmanage`, `storage_list_workload_types`

**JSON 补全（~50 个）**：DiskInfo、StoragePoolBasicInfo、Storage 等

### 第 6~10 批：aiops/gfs/virt/server/其余（~121 个 Returns）

同上逻辑，按 topic 文件逐一处理。

## 统计

| 指标 | 数值 |
|------|------|
| 总函数数 | ~417 |
| 纯文字 Returns（需补充） | ~93（22%） |
| JSON 但字段缺失（需补全） | ~324（78%） |
| API 参考引用对象定义 | 225 |
| 批次数 | 10（按 topic 文件分批） |

## 执行指引

1. 每批使用 `submit_plan` 提子计划，获取批准后执行
2. **每个函数处理流程**：搜函数体内 API URI → 在 `dme-api-reference.md` 中匹配 → 判断复杂度 → 编写文本或 JSON Returns
3. 按 1→10 批顺序，每批完成后提交 commit
