# 计划 104：rearch docstring i18n —— 注释外置 i18n YAML 并按语言加载

> **v2 补充（见文末「v2 结构化 i18n 格式」）**：i18n YAML 改为 `topics` 包裹的结构化格式
> （topic 的 `description` + 每个 action 的 `description/detail/parameters/outputs`），
> `ACTIONS` dict 的 `description` 字段移除，`--list-topics` 等从 i18n 读取描述。
> 原四阶段中 M1–M3 已完成，M4（废弃 dev-en/main-en）暂缓。

## 概述

将全部 action 函数的 docstring 注释从代码中**提取为标准的国际化（i18n）资源文件**，`cli.py` 改为**按语言从 i18n YAML 加载注释**（`DME_LANG` 环境变量或 `--lang` CLI 参数切换 zh_CN/en_US），**验证通过后移除函数内 docstring**，并**废弃 dev-en / main-en 分支**，双语注释统一在 dev/main 单分支维护。

| 语言 | 来源 | 资源文件（均在 dev/main 分支维护） |
|------|------|----------------------------------|
| 中文（zh_CN） | dev 分支函数 docstring（注释为中文） | `pydme/config/i18n/zh_CN.yaml` |
| 英文（en_US） | dev-en 分支函数 docstring（注释为英文翻译版） | `pydme/config/i18n/en_US.yaml` |

文件标准格式：

```yaml
<topic>:
  <action-func>: |
    <func-comments>
```

即：顶层 key 为 topic（模块名，如 `aiops`），二级 key 为 action 函数名（如 `alarm_list`），值为 YAML block scalar（`|`），内容为该函数 docstring 的完整文本（不含 `"""` 包裹符，含 Args/Returns 段）。

完整示例（`aiops.alarm_list`，与源码 docstring 逐字一致）：

```yaml
aiops:
  alarm_list: |
    查询告警信息

    查询当前告警,可选择是否同时查询历史告警.

    Args:
        client: DME API 客户端
        alarm_id: 告警 ID,支持模糊匹配
        severity: 告警级别列表,取值:critical, major, minor, warning, indeterminate, cleared
        mo_dn: 被管理对象 DN,支持 inc 操作符匹配
        alarm_group_id: 告警组 ID
        dc_id: 数据中心 ID
        product_name: 产品名称
        alarm_name: 告警名称,支持模糊匹配
        occur_utc_start: 告警发生开始时间(毫秒时间戳)
        occur_utc_end: 告警发生结束时间(毫秒时间戳)
        fields: 指定返回的字段列表
        page_no: 分页查询的起始页码,默认 1
        page_size: 每页数量,1~1000,默认 100(当前告警查询用)
        cleared: 是否已清除,true/false(历史告警查询用)
        size: 返回的结果集最大条数,1~1000,默认 100(历史告警查询用)
        iterator: 迭代子,首次查询无需传入,后续查询使用上次返回的 iterator(历史告警查询用)
        include_history: 开关参数,指定则同时查询历史告警

    Returns:
        {
            current_alarms: 当前告警列表 (List<AlarmInfo>)。参数格式如下：[{
                alarm_id: 告警ID (string),
                alarm_name: 告警名称 (string),
                severity: 告警级别 (string),
                status: 状态 (string),
            }, ...],
            total: 告警总数 (integer),
        }
```

## 背景

- 现状：16 个 topic、427 个 action 的 docstring 直接写在 `pydme/actions/*.py` 的函数体内，由 `cli.py` 的 `parse_docstring` 解析生成 `--help` 输出。中文注释在 dev/main 分支，英文翻译注释在 dev-en/main-en 分支，靠人工或词表替换脚本（`.reasonix/scripts/translate_cn_to_en.py`）同步。
- 痛点：中英文注释是**两份代码内文本**，双语靠双分支反复 sync 维护，改动需跨分支翻译同步，成本高、易漂移；`DMEAPIClient` 等公共代码的双分支演进也互相拖累。
- 目标（三阶段）：
  1. **外置**：注释提取为 i18n 资源文件，作为注释的单一权威来源；
  2. **加载**：`cli.py` 按语言从 YAML 加载注释（`DME_LANG` / `--lang`），CLI 行为不变；
  3. **收敛**：验证通过后移除函数内 docstring，废弃 dev-en/main-en 分支，双语注释统一在 dev/main 分支的 YAML 上维护。
- 已核实事实：
  - dev 分支：16 个 topic、**427 个 action**（以各模块底部 `ACTIONS` dict 为准）；模块内另有少量辅助函数（如下划线开头的 `_build_*` 等，非 action，不提取）。
  - `pydme/actions/` 为单层结构（无子目录），ACTIONS 中无 `module` 字段在用 → i18n key `(topic=文件名, action=ACTIONS key)` 与 `cli.py` 的加载路径完全对齐（`load_actions` 中 `module.ACTIONS.items()` 处即可取得 topic 与 action_key）。
  - dev-en 分支注释为英文，但**落后于 dev**（如 `protect.py` 动作集与 dev 不一致：dev-en 用旧的 `hypermetro_domain_*` 命名，dev 已重构）。`en_US.yaml` 从 dev-en 提取时以 dev-en 的 `ACTIONS` 为准，提取完成后即与 dev 对齐（后续英文新增动作直接在 YAML 上补译）。
  - `ast.get_docstring(node, clean=True)` 的输出（去公共缩进、去首尾空行）与上述示例格式逐字一致，可直接作为 YAML 内容。
  - 当前环境无 PyYAML，提取脚本与 SDK 运行时均需**零依赖**（纯 `ast` / 手写 block scalar 序列化与解析）。

## 阶段 1：提取 docstring → i18n YAML

### 1.1 编写提取脚本 `.reasonix/scripts/extract_docstrings.py`

零依赖、纯 Python 3 标准库实现：

1. **收集**：遍历 `pydme/actions/*.py`（排除 `__init__.py`）；用 `ast` 解析每个文件，收集全部 `FunctionDef` 与模块底部 `ACTIONS` dict 的 key。
2. **过滤**：只提取 `ACTIONS` 中注册的 action 函数（排除辅助函数）。
3. **取文本**：`ast.get_docstring(node, clean=True)` 得到标准 docstring 文本（无 `"""`、无首尾空行、Args 段保留相对缩进）。
4. **序列化**：手写 YAML 输出，格式严格为 `<topic>:\n  <action-func>: |\n` + 内容每行前缀 4 空格；action 按定义顺序输出。
5. **自校验**：从生成的 YAML 文本回读解析，与 AST 提取的 docstring **逐字比对**（round-trip），不一致立即报错退出。
6. **命令行**：
   - `python3 .reasonix/scripts/extract_docstrings.py -o <输出路径>`：提取当前工作树
   - `python3 .reasonix/scripts/extract_docstrings.py --ref dev-en -o <输出路径>`：通过 `git show <ref>:<path>` 取指定分支/commit 的模块源码再提取（工作树无需切换）

### 1.2 生成并提交

```bash
python3 .reasonix/scripts/extract_docstrings.py -o pydme/config/i18n/zh_CN.yaml
python3 .reasonix/scripts/extract_docstrings.py --ref dev-en -o pydme/config/i18n/en_US.yaml
```

预期：zh_CN 为 16 个 topic、427 个 action；en_US 以 dev-en 的 ACTIONS 为准（动作集可能少于 dev，属预期）。

**提交到 dev 分支**：脚本 + 两个 YAML 一起提交（`pydme/config/i18n/zh_CN.yaml`、`pydme/config/i18n/en_US.yaml`）。**en_US.yaml 不再提交到 dev-en**——dev-en 仅作为提取来源，提取完成即完成使命（见阶段 4）。将来 dev-en 同步 dev 后如需刷新英文资源，仅需重新执行 `--ref dev-en` 提取。

## 阶段 2：cli.py 按语言加载 i18n 注释

### 2.1 语言选择

- 环境变量 `DME_LANG`：取值 `zh_CN` / `en_US`，默认 `zh_CN`。
- CLI 全局参数 `--lang {zh_CN,en_US}`（加在主 parser 上，如 `pydme --lang en_US <topic> <action> ...`）。
- 优先级：`--lang` 显式参数 > `DME_LANG` 环境变量 > 默认 `zh_CN`。
- 非法值：CLI 报错并提示合法取值；环境变量非法时回退默认并打印 warning。

### 2.2 YAML 加载

- 新增 `pydme/config/i18n.py`（或并入 `cli.py`）：**轻量 YAML 子集解析器**（零依赖）。文件格式自产且受控（`<topic>:` / `  <action>: |` / 4 空格缩进内容块），解析规则：
  - 无缩进且以 `:` 结尾 → topic key；
  - 2 空格缩进且以 `: |` 结尾 → action key，后续 4 空格缩进行（含空行）为 block 内容，直到遇到缩进 ≤2 的非空行结束；
  - 加载后按 `(topic, action)` 建索引并模块级缓存（每次进程仅解析一次）。
- 备选（若未来 i18n 文件由外部工具生成、格式不可控）：改依赖 PyYAML，需新增运行时依赖并更新 `pyproject.toml`。默认不采用。
- **打包（i18n 全部 YAML 作为发布内容）**：`pyproject.toml` 的 `package-data` 修改为 `"pydme.config" = ["*.json", "i18n/*.yaml"]`，将 **`pydme/config/i18n/` 下所有 YAML 文件**纳入发布内容（wheel + sdist）：
  - 实测确认：setuptools 支持相对包目录的子目录 glob，`i18n/*.yaml` 会把 `pydme/config/i18n/` 下的 `zh_CN.yaml`、`en_US.yaml` 及未来新增的全部语言文件（如 `fr_FR.yaml`）一并打入，且不会误收其它扩展名文件；i18n 目录**无需** `__init__.py`，package-data 的 key 保持 `"pydme.config"` 即可。
  - 新增语言资源时**无需再改** `pyproject.toml`。
  - 仓库无 `MANIFEST.in`，sdist 由 setuptools 默认规则处理，无需额外配置。
  - 打包验证：`pip wheel . --no-deps` 后检查 wheel 内包含 `pydme/config/i18n/*.yaml`（对应验收标准 #7）。

### 2.3 parse_docstring 改造

- `load_actions()` 中解析处（现为 `doc = inspect.getdoc(func) or ""` 后 `parse_docstring(doc)`）改为：
  1. 按当前语言查 i18n：`text = i18n.get(topic, {}).get(action_key)`；
  2. 命中 → `parse_docstring(text)`；
  3. 未命中（过渡期）→ 回退 `parse_docstring(inspect.getdoc(func) or "")`；
  4. 阶段 3 移除 docstring 后，未命中即资源缺失 → 报错提示「i18n 资源缺少 <lang>.<topic>.<action>，请更新对应 YAML」。
- `parse_docstring` 本体**不改**：i18n 文本与 docstring 同构（同一 Args/Returns 格式），解析逻辑复用。
- 子模块分支（`module` 字段，当前未使用）同样按 `(topic, sub_action_key)` 查 i18n，行为一致。
- 模块级 topic 描述（`get_module_doc`，读 `module.__doc__`）不在本次范围，保持代码内。

### 2.4 阶段验证

- `DME_LANG=zh_CN` 与默认下，全量 427 个 action 的 `pydme <topic> <action> --help` 输出与改造前**逐字一致**。
- `DME_LANG=en_US` / `--lang en_US` 下，输出为英文注释解析结果（与 `en_US.yaml` 内容一致）。
- 自动化：比对脚本遍历全部 action，比较「改造前 docstring 解析结果」与「i18n 加载解析结果」。

## 阶段 3：验证通过后移除函数 docstring

1. **验证通过标准**（阶段 2 验收全绿 + 现有端到端测试回归通过，见验收标准）。
2. **移除范围**：`pydme/actions/*.py` 中**所有 action 函数的 docstring**（`"""..."""` 块整体删除，保留函数签名、参数默认值、`-> dict` 注解与函数体）。
3. **保留**：模块级 docstring（topic 描述，`get_module_doc` 仍依赖）、辅助函数与其余代码不动。
4. 移除后 `inspect.getdoc(func)` 返回空 → i18n 成为注释唯一来源（阶段 2 的缺失报错逻辑兜底）。
5. 提取脚本保留在 `.reasonix/scripts/`，作为日后重新生成/刷新 i18n 资源的工具（docstring 移除后，新增 action 的注释直接在 YAML 上编写，不再写回代码）。

## 阶段 4：废弃 dev-en / main-en 分支

1. **前提**：阶段 1 已从 dev-en 提取 `en_US.yaml`；阶段 2/3 完成后英文注释权威源已迁至 dev/main 的 `pydme/config/i18n/en_US.yaml`。
2. **停止同步**：不再向 dev-en / main-en 执行 sync / merge 操作。
3. **归档**：为 dev-en、main-en 打归档 tag（如 `archive/dev-en-final`、`archive/main-en-final`）保留历史。
4. **删除**：确认归档后删除 remote 分支 `dev-en`、`main-en`（破坏性操作，执行前需确认）。
5. 后续双语维护流程：中文/英文注释均在 dev/main 分支的对应 YAML 上维护；新增或修改 action 注释时同步更新两个 YAML（英文可人工翻译或借助词表脚本辅助）。

## 验收标准

| # | 标准 |
|---|------|
| 1 | `zh_CN.yaml` 与 dev 分支各 action 的 docstring 逐字一致（round-trip 通过） |
| 2 | `en_US.yaml` 与 dev-en 分支各 action 的 docstring 逐字一致（round-trip 通过） |
| 3 | 两个文件结构合法：`topic → action-func → str`；topic 覆盖 16 个模块；zh_CN 含 427 个 action；key 与 `ACTIONS` 注册集合完全一致（无遗漏、无辅助函数混入） |
| 4 | 阶段 1 提交后 `pydme --help` / `--list-topics` 行为不变（未改 cli.py） |
| 5 | `DME_LANG` 与 `--lang` 切换生效；zh_CN 下全量 427 个 `--help` 输出与改造前逐字一致；en_US 下输出与 `en_US.yaml` 一致 |
| 6 | 阶段 3 移除 docstring 后，上述 help 输出仍逐字一致（回归脚本 + 现有 `.reasonix/scripts` 端到端测试通过） |
| 7 | wheel 与 sdist 打包含 `pydme/config/i18n/` 下**全部** YAML 文件（`package-data` 用 `"pydme.config" = ["*.json", "i18n/*.yaml"]`，`pip wheel . --no-deps` 实测验证） |
| 8 | dev-en / main-en 已归档；仓库后续不在双分支维护注释 |

## 注意与风险

- **YAML 合法性**：docstring 文本将整体放入 block scalar，内部 `: `、`{`、`[`、`#` 等均安全；但需确认全部 docstring 中不存在以 `---` / `...` / `"""` 开头的内容行（提取脚本应加断言兜底）。
- **en_US 与 zh_CN 的 key 集合在阶段 1 可能不同**（dev-en 落后于 dev）；阶段 3 移除 docstring 后 i18n 是唯一来源，若两份 YAML 不同步会导致某语言下缺注释 → 由 2.3 的缺失报错兜底，日常维护保证两文件同步更新。
- **轻量解析器正确性**：只支持自产 block scalar 格式；若将来引入锚点/引号/多文档等复杂 YAML 特性，需切换 PyYAML。
- **回归范围**：docstring 移除是纯删除，不影响函数行为；重点回归 `--help` 渲染与测试脚本（`.reasonix/scripts`）端到端用例。
- **删除分支不可逆**：remote 分支删除前必须先打归档 tag 并经确认。

## 执行顺序（里程碑）

- **M1**（阶段 1）：提取脚本 + `zh_CN.yaml` + `en_US.yaml` 提交 dev；验收 1~4。
- **M2**（阶段 2）：`cli.py` 加载改造 + `package-data` 改为 `["*.json", "i18n/*.yaml"]` 并 `pip wheel . --no-deps` 实测 i18n 全部 YAML 入包；验收 5、7。
- **M3**（阶段 3）：移除 docstring + 全量回归；验收 6。
- **M4**（阶段 4）：归档并删除 dev-en / main-en；验收 8。**（暂缓：用户 2026-10-08 决定先不做；本地归档 tag `archive/dev-en-final`、`archive/main-en-final` 已打）**

---

## v2 结构化 i18n 格式（2026-10-08，用户补充）

### 目标

将 i18n YAML 从「topic → action → 整段 docstring」改为**结构化字段**；移除 `ACTIONS` dict 的 `description` 字段；`--list-topics` 等描述改从 i18n 读取。

### 新文件格式

```yaml
topics:
  <topic>:
    description: <topic-description>      # 模块 docstring 首行（与 --list-topics 同源）；多行用 |
    actions:
      <action-func>:
        description: <func 注释第一段>     # 多行用 |
        detail: <func 注释第二段>          # Args 之前其余段落；无则留空 ''；多行用 |
        parameters:
          <arg1>: <arg1 描述>             # 多行用 |
          <arg2>: <arg2 描述>
        outputs: |
          <Returns 段内容>                # 无 Returns 则留空 ''
```

- 顶层新增 `topics` 包裹（为将来扩展元数据留位）。
- `<topic-description>`：模块 docstring 的 strip 后首行；中文内容取 dev 分支模块 docstring，英文内容取 dev-en 分支模块 docstring（英文翻译版）。
- action 的 `description` / `detail` / `parameters` / `outputs` 由原 docstring 拆分，**拆分可无损重组回原 docstring 文本**（逐字一致），使 `parse_docstring` 输出不变。

### 拆分/重组规则

| 字段 | 拆分（来自原 docstring） | 重组（build_docstring） |
|------|--------------------------|--------------------------|
| description | Args/Returns 之前的第一段（首行起至首个空行） | 作为首段 |
| detail | Args 之前第二段及以后（无则空） | 作为第二段 |
| parameters | Args 段按 `name: desc` 解析，描述保留格式块相对缩进 | 生成 `Args:` 段：参数行 4 空格、多行描述续行 4 空格前缀 |
| outputs | Returns 段内容去公共缩进 | 生成 `Returns:` 段：内容 4 空格缩进 |

重组仅输出非空段，段间空行分隔；重组文本与原始 docstring（clean 后）**逐字一致**。

### 实施改动

1. `.reasonix/scripts/extract_docstrings.py`：改生成 v2 格式；topic 的 description 取模块 docstring 首行（`--ref` 时取该 ref 的模块 docstring）。
2. `pydme/i18n.py`：解析 v2 结构；新增 `build_docstring(topic, action)` 无损重组、`get_action_description(topic, action)`、`get_topic_description(topic)`。
3. `pydme/cli.py`：
   - `get_topic_actions`：`actions_info[action]['description']` 改从 i18n 取；`_doc_for` 改为用 i18n 结构化字段重组文本（缺失回退逻辑保留）；
   - `--list-topics`：`topic_desc` 从 i18n `topics.<topic>.description` 取，`action_desc` 从 i18n `actions.<action>.description` 取（不再读 ACTIONS dict）；
   - `print_topic_help` / `print_subtopic_help` / `print_action_help` / 执行时打印的 description 均经 `get_topic_actions` 的 `actions_info['description']` 自动生效。
4. 移除 16 个 `pydme/actions/*.py` 中 `ACTIONS` 各条目的 `description` 字段。
5. 重新生成 `pydme/config/i18n/zh_CN.yaml`（dev）与 `en_US.yaml`（dev-en 英文 + protect 改名动作映射，与 zh_CN 对齐 427 keys）。

### 验收（v2）

| # | 标准 |
|---|------|
| V1 | 两个 YAML 结构为 `topics.<topic>.actions.<action>.{description,detail,parameters,outputs}`，解析合法 |
| V2 | 拆分→重组 round-trip 逐字一致（重组文本 == 提取前 docstring） |
| V3 | 默认 zh_CN 全量 427 个 `--help` 与 v2 改造前逐字一致 |
| V4 | `--list-topics` 输出与 v2 改造前一致（topic 描述与 action 描述内容不变） |
| V5 | `ACTIONS` dict 无 `description` 字段残留；en_US 全量 help 无缺失警告；wheel 打包正常 |

---

## 待修复清单：Returns 规范审计（2026-10-08）

对全部 427 个动作的 `Returns` 段按以下规范审计（zh_CN 源，en_US 需同步修改）：

1. 返回结构体 → 用 `{}` 包裹描述结构体内的字段；
2. 返回单个值 → 直接描述返回值含义；
3. 返回为空 → 直接说明无返回；
4. 根据不同条件返回多种格式的结构体 → 分情况描述结构体内的字段。

共发现 **17 个不符合项**（A/B/C/D/E 五类），状态：**待手动审计如何修复**（用户逐项决定修复方式后实施，zh_CN/en_US 两文件同步，结构体展开以 `.reasonix/reference/dme-api-reference.md` 为准）。

### A. 无 Returns 段（8 个）

| 动作 | 问题 | 建议方向 |
|------|------|---------|
| `storage.qos_show` | 无 Returns；API 返回 `total` + `datas`（List\<qosDetailResponse\>）结构体 | 展开结构体 |
| `storage.qos_create` / `qos_modify` / `qos_delete` / `qos_activate` / `qos_deactivate` / `qos_associate` / `qos_unassociate` | 无 Returns | 补"无"或返回的任务 ID（按 API 确认） |

### B. 空返回用 `{}` 包裹（2 个）

| 动作 | 问题 | 建议方向 |
|------|------|---------|
| `protect.group_modify` | `{ 无返回数据。HTTP 200 表示修改成功。 }` | 改直接文本（规范 3） |
| `protect.hypermetro_pair_modify` | 同 | 同 |

### C. 返回结构体但仅文本描述（3 个，已对照 API 参考确认）

| 动作 | 现状 | API 实际返回 | 建议方向 |
|------|------|-------------|---------|
| `san.physical_host_group_show` | "物理主机组详细信息" | summary：id/name/description/host_count/source_type/managed_status/takeover_failed_reason/project_id/az_ids（+ TakeoverFailedReason 嵌套） | 展开结构体 |
| `san.physical_host_group_create` | "创建的物理主机组信息" | id/name/description | 展开结构体 |
| `aiops.performance_list_indicators` | "监控指标信息,包含 indicator_ids 列表" | status_code/error_code/error_msg/data（IndicatorIdBody：indicator_ids） | 展开结构体 |

### D. 结构体含占位符未展开（1 个）

| 动作 | 问题 | 建议方向 |
|------|------|---------|
| `aiops.topology_query_san_path` | `san_type=None` 分情况中 `ip_san: { IP_SAN 返回数据 }`、`fc_san: { FC_SAN 返回数据 }` 为占位符 | 展开 ip_san/fc_san 字段（按 API 参考）或按规范简化 |

### E. 嵌套标记混用（3 个，格式小瑕疵）

| 动作 | 问题 | 建议方向 |
|------|------|---------|
| `aiops.topology_query_san_path` / `topology_query_luns` / `topology_query_vms` | `属性格式如下：[{`（列表对象展开标记混用） | 统一为 `参数格式如下：[{` |

### 合规情况（无需处理）

- 其余 352 个结构体：括号平衡、字段行逗号齐全；
- 67 个文本描述大多符合规范 2/3（如"操作结果""任务 ID""无。"）；
- 多情况描述（规范 4）：`topology_query_san_path` 前两段、`tenant.lun_change_tier` 格式正确；
- `tenant.lun_bind_project` / `lun_unbind_project`："无返回数据。HTTP 200 ..." 符合规范 3。

---

## 待确认清单：未展开的结构体（2026-10-08 二次审计）

对全部 427 个动作的 **Args 与 Returns 段**再次审计（zh_CN 源，en_US 同步），发现 **34 条对象类型字段无展开标记**（`属性格式如下：{` / `参数格式如下：{` / `parameter format: {` 等），涉及 **12 个 action**。状态：**待手工确认是否修复**（展开需查 `.reasonix/reference/dme-api-reference.md` 对应对象定义；深层嵌套如 topology_query_san_path 是否展开多层由人工决定）。

### Returns 段（5 个 action，21 条）

| 动作 | 字段 | 未展开类型 |
|------|------|-----------|
| `aiops.topology_query_san_path` | fabrics / switches(2) / switch_links(2) / hosts(3) / storages(3) / controllers / disks / host_groups / pools / ports / right_port | `List<HostToStoragePoolFabric>`、`List<SwitchItem>`、`List<SwitchLinkItem>`、`List<HostToStoragePoolHost>`、`List<HostToStoragePoolStorage>`、`List<HostToStoragePoolController>`、`List<HostToStorageDiskDisks>`、`List<HostToStoragePoolHostGroup>`、`List<HostToStoragePoolPool>`、`List<HostToStoragePoolPort>`、`PortNodeItem` |
| `aiops.performance_query` | data | `Map<object, Map<object, HistoryPerfData>>` |
| `aiops.performance_show_indicators` | data | `Map<object, SimpleIndicator>` |
| `san.mapping_view_query_host_to_lun` | host_info / lun_info | `HostInfoRespParam对象` / `LunInfoRespParam对象` |

### Args 段（7 个 action，13 条）

| 动作 | 字段 | 未展开类型 |
|------|------|-----------|
| `fcswitch.alias_modify` / `fcswitch.zone_modify` | removed_members | `List<PortMemberRequest>` |
| `protect.replication_group_create` / `replication_group_modify` | sync_schedule | `CustomSyncSchedule` |
| `protect.replication_pair_create` | consistency_group_info / snap_tag_list / sync_schedule | `RepConsistencyGroup` / `List<snapTagDetail>` / `CustomSyncSchedule` |
| `protect.replication_pair_modify` | snap_tag_list / sync_schedule | `List<snapTagDetail>` / `CustomSyncSchedule` |
| `protect.snapshot_group_rollback` | target_snapshot_objects | `List<TargetSnapshotObject>` / `TargetSnapshot对象` |
| `protect.snapshot_rollback` | rollback_snapshots | `List<LunSnapshotRollbackResource>` |
| `san.mapping_view_query_host_to_lun` | host_info / lun_info | `LunToHostQueryParam对象` / `HostToLunQueryParam对象` |

### API 参考核对（2026-10-08）

已逐个核对清单中 25 个对象类型（HostToStoragePoolFabric、SwitchItem、SwitchLinkItem、PortLinkItem、HostToStoragePoolHost/Storage/Controller/DiskDisks/HostGroup/Pool/Port、PortNodeItem、SwitchPortItem、HistoryPerfData、SimpleIndicator、HostInfoRespParam、LunInfoRespParam、LunToHostQueryParam、HostToLunQueryParam、PortMemberRequest、CustomSyncSchedule、RepConsistencyGroup、snapTagDetail、TargetSnapshotObject、LunSnapshotRollbackResource）在 `.reasonix/reference/dme-api-reference.md` 中**均有定义**（`Xxx对象包含如下属性` 章节）。**无动作需要从清单移除**，12 个 action 全部保留（展开依据齐全）。

### en_US 参数缺失差异（2026-10-08，展开时发现）

zh_CN 存在但 en_US **缺失的参数行**（en 翻译版本参数不完整，本次未补全，待人工确认）：

| 动作 | 缺失参数行（zh 有 en 无） |
|------|--------------------------|
| `protect.replication_group_create` | `sync_schedule`（一致性组同步计划 CustomSyncSchedule） |
| `protect.replication_pair_create` | `consistency_group_info`（RepConsistencyGroup）、`snap_tag_list`（List<snapTagDetail>） |
| `protect.replication_pair_modify` | `snap_tag_list`（List<snapTagDetail>） |

修复时需从 zh_CN 对应 docstring 翻译补全到 en_US。

### 说明

- 已排除：基础类型（string/int32/…）、`List<string>` 等、枚举"可选值"列表、已带展开标记的字段（含 `参数格式如下：{` 单对象形式）。
- `topology_query_san_path` 为深层嵌套拓扑结构（fabrics 已展开 3 层），其余引用对象是否逐层展开由人工决定。
- 修复时 zh_CN/en_US 同步，展开后需通过 round-trip 校验与全量 help 回归。
