# 计划 105：rearch help docs —— ACTIONS 字典与 i18n 描述整合为 actions_/funcs_ YAML，帮助系统重构

## 概述

将 `pydme/actions/*.py` 底部 `ACTIONS` 字典（func/params/subtopic 结构）与 `pydme/config/i18n/` 下的中英文描述（topic 描述 + action docstring）**整合为两份结构化配置**：

- `pydme/config/i18n/actions_<lang>.yaml`：topics → actions / subtopics 树形结构，含 topic / action / subtopic 描述、`func`、`params`；
- `pydme/config/i18n/funcs_<lang>.yaml`：`<topic>.<function_name>` → 完整 docstring（逐字迁移现有 docstring）。

随后重构帮助系统：`--list-topics` 只输出 topics + subtopics 描述（树形、不含 actions）；`<topic> --help` / `<topic> <subtopic> --help` 增加 subtopics 描述；action 级 `--help` 从 `funcs_<lang>.yaml` 读取 docstring；**移除代码中全部 `ACTIONS` 字典**，改为从配置文件读取。**dme-mcp-server 不在本次范围**（其 `server_v1.py` 依赖 `module.ACTIONS` 与 `pydme.i18n.get_action_doc`，移除后由用户稍后自行更新适配）。

## 背景与现状（已核实）

- 16 个 topic 模块、**427 个 action**；`ACTIONS` 条目为 `{func, params, subtopic}`（104 计划 v2 已移除 `description` 字段）；模块 docstring 保留（topic 描述），action 函数 docstring 已于 104 M3 移除（i18n YAML 为唯一来源）。
- **15 个 action 的 func 名 ≠ action_key**（别名，集中在 `nas.py` / `protect.py`）；427 个 func 全部可在模块内解析、无两个 action 共用同一 func → `funcs_<lang>.yaml` 的 `<topic>.<func>` key 与 action 一一对应。
- 无 `module` 字段在用（单层目录结构）；**101 个 subtopics**；action key 全部为 underscore 分隔（无 space 形式）。
- 现有 `zh_CN.yaml` / `en_US.yaml`：`topics.<topic>.description` + `topics.<topic>.actions.<action>.docstring`；两份 key 集合完全一致（各 427）。
- `--list-topics` 的短 action 名剥离逻辑（`get_available_topics`）：direct action 用 action_key 原样；subtopic action 剥离 `<subtopic>_` 前缀。特殊嵌套：`nas.dataturbo_dpc_list`（subtopic=`dataturbo`）→ 短名 `dpc_list`；`nas.dpc_list`（subtopic=`dpc`）→ 短名 `list`。
- `pyproject.toml` package-data 已为 `"pydme.config" = ["*.json", "i18n/*.yaml"]` → 新 YAML 自动入包，无需改动。
- **外部依赖提示（不在本次范围）**：独立仓库 `dme-mcp-server` 的 `server_v1.py` 遍历 `module.ACTIONS`（`get_topic_actions`）并调用 `pydme.i18n.get_action_doc / resolve_lang`。本次仅保证 `pydme.i18n` 的 `get_action_doc / resolve_lang / get_topic_description` 等公开接口签名不变（见 M3），`module.ACTIONS` 移除后由用户稍后自行更新 `dme-mcp-server` 适配。
- 现有工具：`.reasonix/scripts/extract_docstrings.py`（104 产出旧格式）、`translate_cn_to_en.py`（中英词表，可辅助 subtopic 英文描述）。

## 目标格式（用户给定）

`config/i18n/actions_<lang>.yaml`：

```yaml
topics:
    - name: <topic>
      description: <topic_description>
      actions:
          - name: <action>          # 只保留短 action 名称，与 --list-topics 输出一致
            description: <action_description>   # action function 的 docstring 首行
            func: <function_name>
            params: [参数列表]
      subtopics:
        - name: <subtopic>
          description: <subtopic_description>   # M1 生成时留空，M2 大模型总结填充
          actions:
              - name: <action>      # 只保留短 action 名称（不带 subtopic 前缀）
                description: <action_description>
                func: <function_name>
                params: [参数列表]
```

`config/i18n/funcs_<lang>.yaml`：

```yaml
<topic>.<function_name>: |
    <function_docstring>
```

## 阶段与里程碑

### M1：生成脚本 + 生成新配置（4 个文件）

**新脚本 `.reasonix/scripts/gen_actions_i18n.py`**（零依赖、纯 stdlib，保留 `extract_docstrings.py` 不动作历史参考）：

1. **代码侧输入**：用 `ast` 解析 16 个 `pydme/actions/*.py` 的 `ACTIONS` dict，取每个 action 的 `func` 名、`params` 列表、`subtopic`、定义顺序。
2. **i18n 侧输入**：读现有 `zh_CN.yaml` / `en_US.yaml`，取 `topics.<topic>.description`（topic 描述）与 `actions.<action>.docstring`（完整 docstring）。
3. **输出**：
   - `actions_zh_CN.yaml` / `actions_en_US.yaml`：按目标格式；topic 描述取现有 i18n 值；action 描述 = docstring 首行（strip 后第一非空行）；subtopic description 留空 `''`；action 顺序保持 `ACTIONS` 定义顺序。
   - `funcs_zh_CN.yaml` / `funcs_en_US.yaml`：key = `<topic>.<func名>`，docstring 逐字迁移（与现有 YAML block 内容一致）。
4. **短名规则**（复刻 cli.py `get_available_topics`）：direct action → name=action_key；subtopic action → 剥离 `<subtopic>_` 前缀得短名。
5. **round-trip 自校验**（不通过即报错退出）：
   - 由配置重建 action_key（direct：`name`；subtopic：`<subtopic>_<name>`）集合 == 代码 `ACTIONS` key 集合（427），含 `dataturbo_dpc_list` / `dpc_list` 特殊嵌套；
   - 每个 action 的 `func` == 代码 `ACTIONS` 的 func，且可在模块解析；
   - 每个 action 的 `description` == `funcs` 中 `<topic>.<func>` docstring 的首行；
   - `funcs` key 集合 == 全部 action func 集合（427）；
   - 两份 `actions_<lang>.yaml` 的 `name/func/params/subtopic` 结构完全一致（仅 `description` 语言不同）；
   - topic 集合 == 16 个模块名。
6. **用法**：`python3 .reasonix/scripts/gen_actions_i18n.py`（输出到 `pydme/config/i18n/`）。

### M2：subtopic description 总结生成

- 对 **101 个 subtopics**，根据其下 actions 的功能（`funcs` docstring 首行/描述）总结中文 description；再生成英文 description（复用 `translate_cn_to_en.py` 词表辅助 + 人工复核技术术语）。
- 写入 `actions_zh_CN.yaml` / `actions_en_US.yaml` 的 `subtopics[].description`（替换 M1 的空值）。
- 验收：101 × 2 条 subtopic 描述全部非空、与 action 功能相符。

### M3：`pydme/i18n.py` 重构（新格式解析 + 注册表 API）

1. **重写解析器**：支持 `actions_<lang>.yaml`（列表格式 `- name:` 条目）与 `funcs_<lang>.yaml`（`key: |` block，逻辑复用现有 block 解析）；删除旧格式（字典格式）解析代码。
2. **文件路径**：`_yaml_path` 拆分为 `actions_<lang>.yaml` / `funcs_<lang>.yaml` 两处读取；`SUPPORTED_LANGS`、`resolve_lang`（`--lang` > `DME_CLI_LANG` > `zh_CN`）不变。
3. **保留公开接口（dme-mcp-server 依赖，签名不变）**：
   - `get_topic_description(topic, lang)`：从 actions 配置读；
   - `get_action_doc(topic, action_key, lang)`：内部两步映射 —— actions 配置 `action_key → func` → `funcs` 配置 `<topic>.<func>` docstring；缺失返回 `None`；
   - `get_action_description(topic, action_key, lang)`：从 actions 配置的 `description` 取首行。
4. **新增注册表 API**：`load_actions_registry(lang)` → `{topic: {action_key: {func(函数对象), params, subtopic}}}`；`func` 名经 `importlib.import_module(f'pydme.actions.{topic}')` + `getattr` 解析为函数对象（覆盖 15 个别名）；提供 `action_key ⇄ (subtopic, 短名)` 反向索引。缓存按进程保留。
5. **缺失兜底**：配置文件缺失/条目缺失时打印警告并返回空结构（行为与现状一致）。

### M4：`pydme/cli.py` 重构

1. **数据来源切换**：
   - `get_available_topics()`：改为从 `load_actions_registry` 读取树结构（topic → subtopic → 短名），不再 `pkgutil.iter_modules` 遍历 + 读 `module.ACTIONS`；加载时校验配置 topic 集合与 `pydme/actions/` 目录模块一致，不一致打印警告；
   - `get_topic_actions(topic)`：改从注册表构建 `{action_key: {description, params, parsed, subtopic, func}}`（`description` 按当前语言从 actions 配置取，`parsed` 由 `parse_docstring(get_action_doc(...))` 得到）——结构与现状一致，`print_*` 函数改动面最小；
   - `execute_action()` 与 `main()` 两条执行路径：从注册表取 func，删除 `module.ACTIONS` / `module` 字段展开逻辑。
2. **`--list-topics` 重构**：读取 `actions_<lang>.yaml`，按树形输出 topics 与 subtopics 的**描述**，**不再输出 actions**（包括 direct actions）；更新 Legend 文案（去掉 action 行）；description 为空时仅输出名称。
3. **`print_topic_help`**：subtopic 标题行增加其 description 输出；topic 描述改用 `get_topic_description`（语言化，替代固定读英文模块 docstring 的 `get_module_doc`，与 `--list-topics` 一致）；`print_subtopic_help` 同样增加 subtopic description 输出。
4. **`print_action_help`**：docstring 经 `get_action_doc`（即 `funcs_<lang>.yaml`），description 从 actions 配置取；渲染逻辑（`parse_docstring`）不变。

### M5：移除 `pydme/actions/*.py` 中的 `ACTIONS` 字典

- 删除 16 个模块底部的 `ACTIONS = {...}` 块（含注释）；保留全部函数定义与模块 docstring。
- 生成脚本的 round-trip 校验改为「配置为权威源」：`actions_<lang>.yaml` topic 集合 == 模块集合、func 均可解析。

### M6：删除旧文件 + 打包验证 + 全量回归

1. 删除 `pydme/config/i18n/zh_CN.yaml`、`en_US.yaml`（信息已迁移，避免双源漂移；git 历史可回溯；已确认无其它引用）。
2. `pip wheel . --no-deps` 验证 wheel 含 `pydme/config/i18n/actions_*.yaml` 与 `funcs_*.yaml`、不含旧文件。
3. 全量回归（见验收标准）。

## 验收标准

| # | 标准 |
|---|------|
| 1 | `actions_zh_CN.yaml` / `actions_en_US.yaml` / `funcs_zh_CN.yaml` / `funcs_en_US.yaml` 生成成功，round-trip 自校验通过（16 topic、427 action、101 subtopic） |
| 2 | 两份 actions 文件 `name/func/params/subtopic` 结构一致，仅 `description` 按语言不同 |
| 3 | 101 个 subtopics 的 zh_CN / en_US 描述全部非空 |
| 4 | `--list-topics` 树形输出 topics + subtopics 描述，**无 actions 行**；内容与配置一致 |
| 5 | `<topic> --help` 与 `<topic> <subtopic> --help` 均输出 subtopic 描述；topic 描述语言化（随 `--lang` 切换） |
| 6 | 全量 427 个 action 的 `<topic> <action> --help`（zh_CN 与 en_US）docstring 内容与改造前逐字一致（来源切换为 `funcs_<lang>.yaml`） |
| 7 | 执行路径（2 级与 3 级命令）func 解析、`--accept-risk` 风险检查、参数类型转换行为不变（无网络环境的静态验证：func 解析 + help 渲染） |
| 8 | `pydme/actions/*.py` 无 `ACTIONS` 残留；`pydme/i18n.py` 无旧格式解析代码 |
| 9 | wheel 含全部新 YAML、不含 `zh_CN.yaml`/`en_US.yaml` |

## 注意与风险

- **15 个别名 action**（func ≠ action_key）：`funcs` key 用 func 名，`get_action_doc` 必须两步映射（action_key → func → docstring）；生成脚本 round-trip 已覆盖。
- **特殊嵌套短名**：`nas` 下 `dataturbo→dpc_list`、`dpc→list` 的短名必须与 `--list-topics` 现状完全一致，round-trip 校验防错。
- **subtopic 描述总结**：大模型按 action 功能总结，技术术语（LUN、Dtree、vStore 等）需人工复核；英文描述避免机械直译。
- **零依赖约束**：新格式为受控自产格式，手写解析器需保证 block scalar 与列表条目解析正确（不引入 PyYAML）。
- **dme-mcp-server 兼容性（不在本次范围）**：`pydme.i18n` 公开接口（`get_action_doc` / `resolve_lang` / `get_topic_description`）签名保持不变，`dme-mcp-server` 只需在 `module.ACTIONS` 移除后改用新的注册表 API（`load_actions_registry`），由用户稍后自行更新；本次不修改该仓库。
- **删除旧文件不可逆于双源**：信息已迁移且 round-trip 验证通过后再删；git 历史可回溯。
- **外部消费者**：除 dme-mcp-server（用户自行适配）外，`dme-skills` / `dme-mcp-server` 目录下无其它 pydme i18n 消费者（已核查）。

## 执行顺序

M1（生成脚本 + 4 个新 YAML）→ M2（subtopic 描述填充）→ M3（i18n.py 新解析器 + 注册表 API）→ M4（cli.py 重构）→ M5（移除 ACTIONS 字典）→ M6（删旧文件 + 打包验证 + 回归）

---

## 实施完成记录（2026-10-10）

| 里程碑 | 状态 | 说明 |
|--------|------|------|
| M1 | ✅ | `.reasonix/scripts/gen_actions_i18n.py` 生成 `actions_zh_CN.yaml` / `actions_en_US.yaml` / `funcs_zh_CN.yaml` / `funcs_en_US.yaml`（各 427 action、16 topic），round-trip 自校验通过（重建 action_key == ACTIONS key、func 可解析、description == docstring 首行、双语结构一致） |
| M2 | ✅ | 116 个 subtopic 条目（101 个 distinct 名）中英文描述已填充，全覆盖校验通过 |
| M3 | ✅ | `pydme/i18n.py` 重写：新格式解析器 + `load_actions_registry`；`get_action_doc` 经 action_key → func → funcs 两步映射；`resolve_lang` / `get_topic_description` 等公开接口签名不变 |
| M4 | ✅ | `pydme/cli.py`：`--list-topics` 树形输出 topics+subtopics 描述（无 actions）；topic/subtopic help 增加 subtopic 描述；action help 从 funcs 读 docstring；执行路径走注册表；移除 `load_actions`/`get_module_doc`/module 展开逻辑 |
| M5 | ✅ | 16 个 `pydme/actions/*.py` 移除 ACTIONS 字典（共 2397 行），语法与 import 验证通过 |
| M6 | ✅ | 删除 `zh_CN.yaml` / `en_US.yaml`；wheel 打包含 4 个新 YAML、无旧文件；全量 427×2 help 回归 0 警告 0 错误；执行路径（risk check / 凭据检查）静态验证通过 |

**dme-mcp-server**：不在本次范围，用户稍后自行适配（`module.ACTIONS` 已移除，改用 `pydme.i18n.load_actions_registry`；`get_action_doc` / `resolve_lang` 接口不变）。
