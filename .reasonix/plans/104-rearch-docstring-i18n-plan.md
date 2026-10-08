# 计划 104：rearch docstring i18n —— 注释外置 i18n YAML 并按语言加载

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
- **打包**：`pyproject.toml` 的 `package-data` 增加 `"pydme.config" = ["*.json", "*.yaml"]`，确保 i18n 资源随 wheel 发布（阶段 2 提交时一并修改）。

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
| 7 | wheel 打包含 `pydme/config/i18n/*.yaml`（`package-data` 已加 `*.yaml`） |
| 8 | dev-en / main-en 已归档；仓库后续不在双分支维护注释 |

## 注意与风险

- **YAML 合法性**：docstring 文本将整体放入 block scalar，内部 `: `、`{`、`[`、`#` 等均安全；但需确认全部 docstring 中不存在以 `---` / `...` / `"""` 开头的内容行（提取脚本应加断言兜底）。
- **en_US 与 zh_CN 的 key 集合在阶段 1 可能不同**（dev-en 落后于 dev）；阶段 3 移除 docstring 后 i18n 是唯一来源，若两份 YAML 不同步会导致某语言下缺注释 → 由 2.3 的缺失报错兜底，日常维护保证两文件同步更新。
- **轻量解析器正确性**：只支持自产 block scalar 格式；若将来引入锚点/引号/多文档等复杂 YAML 特性，需切换 PyYAML。
- **回归范围**：docstring 移除是纯删除，不影响函数行为；重点回归 `--help` 渲染与测试脚本（`.reasonix/scripts`）端到端用例。
- **删除分支不可逆**：remote 分支删除前必须先打归档 tag 并经确认。

## 执行顺序（里程碑）

- **M1**（阶段 1）：提取脚本 + `zh_CN.yaml` + `en_US.yaml` 提交 dev；验收 1~4。
- **M2**（阶段 2）：`cli.py` 加载改造 + `package-data` 加 `*.yaml`；验收 5、7。
- **M3**（阶段 3）：移除 docstring + 全量回归；验收 6。
- **M4**（阶段 4）：归档并删除 dev-en / main-en；验收 8。
