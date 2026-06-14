# 翻译计划：将所有文件中的中文翻译为英文

## 概述

将本仓库中所有源代码文件（`pydme/` 和根目录文件）中的中文文本（注释、docstring、CLI help 文本、错误消息等）翻译为英文，保留代码逻辑不变。

## 涉及文件

| 文件 | 中文匹配数 | 优先级 |
|------|-----------|--------|
| 文件 | 原始中文 | 当前残留 | 状态 |
|------|---------|---------|------|
| `__init__.py` | ~1 | 0 | ✅ 完成 |
| `README.md` | ~103 | 0 | ✅ 完成 |
| `cli.py` | ~195 | 0 | ✅ 完成 |
| `san.py` | ~949 | 0 | ✅ 完成 (有碎片需修复) |
| `nas.py` | ~1262 | 0 | ✅ 完成 |
| `protect.py` | ~727 | 0 | ✅ 完成 |
| `storage.py` | ~1067 | 0 | ✅ 完成 (有碎片需修复) |
| `aiops.py` | ~453 | 0 | ✅ 完成 |
| `system.py` | ~389 | 0 | ✅ 完成 |
| `fcswitch.py` | ~203 | 0 | ✅ 完成 |
| `gfs.py` | ~184 | 0 | ✅ 完成 |
| `virt.py` | ~160 | 0 | ✅ 完成 |
| `tenant.py` | ~103 | 0 | ✅ 完成 |
| `server.py` | ~88 | 0 | ✅ 完成 |
| `kube.py` | ~75 | 0 | ✅ 完成 |
| `ipswitch.py` | ~61 | 0 | ✅ 完成 |
| `integrate.py` | ~54 | 0 | ✅ 完成 |
| `backup.py` | ~36 | 0 | ✅ 完成 |
| `workflow.py` | ~81 | 0 | ✅ 完成 |

## 翻译范围

每文件中的中文内容类型：
1. **函数/方法 docstring** — Args/Returns 参数描述、示例说明
2. **CLI help 文本** — `add_help`、`epilog` 中的命令说明
3. **注释** — 行内注释 `#` 和块注释
4. **错误/提示消息** — `raise ValueError(...)`、`print(...)`、`click.echo(...)` 等中的中文字符串
5. **README.md** — 项目文档中的中文描述

## 翻译要求

### Docstring 格式
- Args/Returns 中的字段名（`param_key`、`attr_key`）仍保持英文（原始命名）
- 描述部分的中文翻译为英文
- 约束格式 `(1~255个字符)` → `(1-255 characters)`
- 枚举值 `可选值：...` → `Options: ...`
- 入口标记 `参数格式如下：[{` 保留不翻译（解析器依赖此关键词）
- 入口标记 `属性格式如下：{` 保留不翻译（解析器依赖此关键词）

### 代码标记保留
- 不翻译代码中的标识符、变量名、函数名、类名
- 不翻译 API 路径、HTTP 方法、JSON 字段名
- 不改变代码缩进和空格

### 特殊字符串
- CLI help 中的中文命令描述翻译为英文
- 错误消息翻译为英文
- 注释翻译为英文
- README.md 中的中文部分翻译为英文

## 执行步骤

```bash
# 1. 安装中文检测工具（可选）
pip install chardet

# 2. 翻译 cli.py（入口文件，最先翻译以验证流程）
# 3. 按优先级翻译 actions/ 中各模块
# 4. 翻译 README.md
# 5. 测试 CLI 是否正常运行
python -m pydme.cli --help
python -m pydme.cli --list-topics
# 6. 提交并推送
git add -A && git commit -m "feat: translate all Chinese comments and docs to English" && git push
```

## 质量检查 (QA) 任务

### 检查方法
对比 `main` 分支的中文原文与 `main-en-dev` 分支的英文翻译，验证：
1. **语义正确性** — 中英文意思是否一致，有无漏译、错译
2. **替换残留** — 批量替换导致的碎片（如 `prefetchetch`、`characteracter`）
3. **语法问题** — 冠词、单复数、介词、语态是否合理
4. **标点清理** — 中文句号 `。`、逗号 `，` 是否已替换为英文 `.` `,`

### 检查命令

```bash
# 对比指定文件的全部翻译变更
git diff main..HEAD -- pydme/actions/san.py

# 查看中文残留
git diff main..HEAD -- pydme/actions/*.py | grep '^-.*[\u4e00-\u9fff]' | wc -l

# 检查碎片（重复单词、缺失空格）
git diff main..HEAD -- pydme/actions/*.py | grep -E '(prefetchetch|characteracter|controllerr|maintenancee)'

# 检查中文标点
git diff main..HEAD -- pydme/actions/*.py | grep '[，。；：]'
```

### 已发现的碎片问题

| 文件 | 行 | 原文 | 问题 | 修复方法 |
|------|-----|------|------|---------|
| `san.py` lun_create | count | `created per diskLUNcount` | 缺少空格 | `LUNs created per disk` |
| `san.py` lun_create | prefetch | `variable prefetch prefetchvalue` | 重复 | `variable prefetch; value range` |
| `san.py` lun_create | initial_distribute | `onlyries not support` | 碎片 | `only; Dorado series not supported` |
| `cli.py` | comment | `parameter formatblock` | 缺少空格 | `parameter format block` |
| `cli.py` | comment | `skip internal attribute parsing` | 原意偏差 | `当>0时跳过内部属性解析` |

### 后续计划
- [ ] 修复已发现的碎片问题
- [ ] 逐文件对比 main 分支，检查语义错误
- [ ] 不一致的 `(Optional)` / `可选` 统一
- [ ] 验证 CLI 功能正常

## 注意事项

1. **保留互斥标记**：docstring 中的 `与XXX互斥` 翻译为 `mutually exclusive with XXX`
2. **保留约束描述**：`1~255个字符` 翻译为 `1-255 characters`
3. **入口标记保留中文**：`参数格式如下：[{` 和 `属性格式如下：{` 保留原文，因为 `parse_docstring` 依赖这些中文关键词来跳过内部字段
4. **分块翻译**：每个文件建议分多次编辑，避免 SEARCH/REPLACE 块过大导致匹配失败
5. **翻译后验证**：每个文件翻译完成后运行 `python -m pydme.cli <topic> --help` 确认 CLI 正常工作
