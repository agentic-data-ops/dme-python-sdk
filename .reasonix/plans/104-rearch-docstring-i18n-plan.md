# 计划 104：rearch docstring i18n —— 将 action 函数注释提取为国际化 YAML

## 概述

将全部 action 函数的 docstring 注释从代码中**提取为标准的国际化（i18n）资源文件**，按分支语言各生成一份：

| 语言 | 来源分支 | 生成文件 |
|------|---------|---------|
| 中文（zh_CN） | dev（本分支，注释为中文） | `pydme/config/i18n/zh_CN.yaml` |
| 英文（en_US） | dev-en（注释为英文翻译版） | `pydme/config/i18n/en_US.yaml` |

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

- 现状：16 个 topic、427 个 action 的 docstring 直接写在 `pydme/actions/*.py` 的函数体内，由 `cli.py` 的 `parse_docstring` 解析生成 `--help` 输出。中文注释在 dev/main 分支，英文翻译注释在 dev-en 分支。
- 痛点：中英文注释是**两份代码内文本**，靠人工或词表替换脚本（`.reasonix/scripts/translate_cn_to_en.py`）同步，改一处需双分支重复维护，极易漂移。
- 目标：先把注释**外置为 i18n 资源文件**，作为注释的单一权威来源，为后续 `cli.py` 按语言加载（见"后续阶段"）铺路。本次**只做提取**，不改动任何 `pydme/actions/*.py` 源码与 `cli.py` 行为。
- 已核实事实：
  - dev 分支：16 个 topic、**427 个 action**（以各模块底部 `ACTIONS` dict 为准）；模块内另有少量辅助函数（如下划线开头的 `_build_*` 等，非 action，不提取）。
  - dev-en 分支：注释为英文，但**落后于 dev**——如 `protect.py` 动作集与 dev 不一致（dev-en 用旧的 `hypermetro_domain_*` 命名，dev 已重构）。因此 `en_US.yaml` 与 `zh_CN.yaml` 的 key 集合**允许不同**，各自以所在分支的 `ACTIONS` 为准；待 dev-en 同步 dev 后重新提取对齐。
  - `ast.get_docstring(node, clean=True)` 的输出（去公共缩进、去首尾空行）与上述示例格式逐字一致，可直接作为 YAML 内容。
  - 当前环境无 PyYAML，提取脚本需**零依赖**（纯 `ast` + 手写 YAML block scalar 序列化 + 内置 round-trip 自校验）。

## 实施步骤

### 第一步：编写提取脚本 `.reasonix/scripts/extract_docstrings.py`

零依赖、纯 Python 3 标准库实现：

1. **收集**：遍历 `pydme/actions/*.py`（排除 `__init__.py`）；用 `ast` 解析每个文件，收集全部 `FunctionDef` 与模块底部 `ACTIONS` dict 的 key。
2. **过滤**：只提取 `ACTIONS` 中注册的 action 函数（排除辅助函数）。
3. **取文本**：`ast.get_docstring(node, clean=True)` 得到标准 docstring 文本（无 `"""`、无首尾空行、Args 段保留相对缩进）。
4. **序列化**：手写 YAML 输出，格式严格为 `<topic>:\n  <action-func>: |\n` + 内容每行前缀 4 空格；action 按定义顺序输出。
5. **自校验**：从生成的 YAML 文本回读解析，与 AST 提取的 docstring **逐字比对**（round-trip），不一致立即报错退出。
6. **命令行**：
   - `python3 .reasonix/scripts/extract_docstrings.py -o <输出路径>`：提取当前工作树
   - `python3 .reasonix/scripts/extract_docstrings.py --ref dev-en -o <输出路径>`：通过 `git show <ref>:<path>` 取指定分支/commit 的模块源码再提取（工作树无需切换）

### 第二步：生成 zh_CN.yaml（dev 分支）

```bash
python3 .reasonix/scripts/extract_docstrings.py -o pydme/config/i18n/zh_CN.yaml
```

预期：16 个 topic、427 个 action 全部覆盖，round-trip 通过。

### 第三步：生成 en_US.yaml（dev-en 分支）

```bash
python3 .reasonix/scripts/extract_docstrings.py --ref dev-en -o /tmp/en_US.yaml
```

生成物先放临时目录；在 dev-en 分支上运行工具重新生成并提交，确保与 dev-en 代码一致（见第五步）。

### 第四步：独立校验

1. `yaml.safe_load` 能解析两个文件且结构合法（topic → action-func → str）。当前环境无 PyYAML，可 `pip install pyyaml` 后校验，或依赖脚本内置 round-trip。
2. 脚本 round-trip 断言通过（zh_CN ↔ dev 逐字一致；en_US ↔ dev-en 逐字一致）。
3. 统计核对：topic 数 = 16；zh_CN action 数 = 427；en_US action 数 = dev-en 各模块 ACTIONS 实际数。
4. 抽查 `--help` 输出与提取前后一致（CLI 行为不受影响）。

### 第五步：提交

- **dev 分支**：提交 `.reasonix/scripts/extract_docstrings.py` + `pydme/config/i18n/zh_CN.yaml`。
- **dev-en 分支**：提交 `pydme/config/i18n/en_US.yaml`（在 dev-en 工作树上生成后提交；工具脚本可从 dev 分支 `git show dev:.reasonix/scripts/extract_docstrings.py` 取得）。`en_US.yaml` 不入 dev 分支，`zh_CN.yaml` 不入 dev-en 分支——各分支只维护自己语言的资源。

## 验收标准

| # | 标准 |
|---|------|
| 1 | `zh_CN.yaml` 与 dev 分支各 action 的 docstring 逐字一致（round-trip 通过） |
| 2 | `en_US.yaml` 与 dev-en 分支各 action 的 docstring 逐字一致（round-trip 通过） |
| 3 | 两个文件均可被 `yaml.safe_load` 解析，结构为 `topic → action-func → str` |
| 4 | key 覆盖与各分支 `ACTIONS` 注册集合完全一致：无遗漏、无辅助函数混入 |
| 5 | topic 覆盖 16 个模块；zh_CN 含 427 个 action |
| 6 | 不修改任何 `pydme/actions/*.py` 与 `cli.py`，`pydme --help` 行为不变 |

## 注意与风险

- **YAML 合法性**：docstring 文本将整体放入 block scalar，内部 `: `、`{`、`[`、`#` 等均安全；但需确认全部 docstring 中不存在以 `---` / `...` / `"""` 开头的内容行（已抽查无此类情况，提取脚本应加断言兜底）。
- **key 集合差异是预期的**：dev-en 落后于 dev，`en_US.yaml` 与 `zh_CN.yaml` 动作集不同属正常；dev-en 同步 dev 后重新提取即可对齐。
- **缩进一致性**：block scalar 内容固定 4 空格缩进，docstring 内部原有相对缩进（Args/Returns 嵌套）在 clean 后已归一，round-trip 校验兜底。
- **打包**：`pyproject.toml` 的 `package-data` 目前仅含 `*.json`；若后续需要 i18n 资源随 wheel 发布，需增加 `"*.yaml"`（阶段 2 处理，本次不改）。

## 后续阶段（本次不做，仅为方向）

1. `cli.py` / `parse_docstring` 改为按语言从 i18n YAML 加载注释（如环境变量 `DME_LANG` 或配置文件切换 zh_CN/en_US），docstring 逐步精简为占位或移除。
2. 中英双语资源随发行版发布，dev-en 分支仅保留代码逻辑差异，注释统一走 i18n 资源。
