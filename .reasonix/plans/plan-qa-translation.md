# QA 计划：英文注释质量检查与语义纠错

## 目标

对比 `main` 分支中的原始中文注释与 `main-en-dev` 分支的英文翻译，逐行确认：
1. **语义一致性** — 中英文意思是否一致，有无漏译、错译、过度翻译
2. **替换残留** — 批量替换导致的碎片（如 `prefetchetch`、`controlleroller`）
3. **语法规范性** — 冠词、单复数、介词、时态、语态是否正确
4. **格式一致性** — `Options:` / `(Optional)` / `参数格式如下：[{` 等格式标记是否统一

## 对比方法

```bash
# 查看单文件全部翻译变更
git diff main..HEAD -- pydme/actions/san.py

# 查看单函数变更（按函数名过滤）
git diff main..HEAD -- pydme/actions/san.py | grep -A60 "def lun_create"

# 查看特定行的中英文对照
git diff main..HEAD -- pydme/actions/storage.py | grep -B2 -A2 "变更内容"
```

## 检查清单

### 1. 片段级：每文件抽检 3-5 个核心函数

| 文件 | 函数 | 关键检查点 |
|------|------|-----------|
| `cli.py` | `parse_docstring`, `execute_action`, `print_action_help` | 注释语义、解析器逻辑 |
| `san.py` | `lun_list`, `lun_create`, `lun_modify`, `mapping_view_create` | 参数描述、枚举值 |
| `nas.py` | `nfs_share_create`, `cifs_share_create`, `filesystem_create` | 嵌套参数格式 |
| `storage.py` | `storage_list`, `disk_list`, `fan_list`, `power_list` | 状态枚举翻译 |
| `protect.py` | `保护组创建`, `双活Pair创建`, `快照操作` | 条件参数描述 |
| `aiops.py` | `告警查询`, `性能数据查询`, `健康检查` | 时间范围/聚合描述 |
| `system.py` | `用户管理`, `角色管理`, `任务管理` | 密码策略/状态 |

### 2. 句子级：检查常见语法问题

- [ ] 首字母大写：参数描述首单词是否大写
- [ ] 冠词：`a` / `an` / `the` 使用是否正确
- [ ] 单复数：参数值（`Options`）、列表（`list` vs `lists`）
- [ ] 介词：`on the device` / `in the pool` / `of the storage`
- [ ] 语态：主动语态优于被动语态

### 3. 术语级：一致性检查

| 中文原文 | 推荐英文 | 避免 |
|---------|---------|------|
| 可选 | Optional | optional（小写） |
| 必选/必填 | Required | Must, mandatory |
| 条件必传 | Conditionally required | required when... |
| 可选值 | Options | Available values |
| 默认 | Default | default（小写） |
| 互斥 | mutually exclusive with | 不要混用 exclusive 和 mutex |
| 支持模糊查询 | supports fuzzy search | fuzzy query |
| 支持精确匹配 | exact match | precise match |
| UUID格式或32位十六进制 | UUID format or 32-bit hex | UUID/hex |

### 4. 残留碎片检查

用以下模式扫描所有文件：

```python
# 重复单词碎片（如 prefetchetch）
re.findall(r'([a-zA-Z]{3,})\1', text)

# 缺失空格（如 formatblock）
re.findall(r'[a-z][A-Z]', text)

# 中文标点（如 。，）
re.findall(r'[\u3002\uff0c\uff1b]', text)

# 错误消息中残留中文
re.findall(r'raise ValueError\(.*[\u4e00-\u9fff]', text)
```

## 已知问题状态

| 文件 | 函数 | 问题 | 状态 |
|------|------|------|------|
| `san.py` | `lun_create` | count 描述缺少空格 | ✅ 已修复 |
| `san.py` | `lun_create` | prefetch_value 重复 | ✅ 已修复 |
| `san.py` | `lun_create` | initial_distribute 碎片 | ✅ 已修复 |
| `san.py` | `lun_create` | Options 多余括号描述 | ✅ 已修复 |
| `cli.py` | parse_docstring | formatblock 缺空格 | ✅ 已修复 |
| `aiops.py` | module | operations 重复 | ✅ 已修复 |
| `protect.py` | 多处 | pair creationtion 重复 | ✅ 已修复 |
| `storage.py` | 多处 | controlleroller 重复 | ✅ 已修复 |
| `gfs.py` | 多处 | immediateediate 重复 | ✅ 已修复 |

## 执行步骤

```bash
# 1. 差异总览
git diff main..HEAD --stat

# 2. 逐一检查核心文件
for f in pydme/cli.py pydme/actions/san.py pydme/actions/nas.py pydme/actions/storage.py; do
    echo "=== Checking $f ==="
    git diff main..HEAD -- "$f" | head -100
done

# 3. 扫描残留问题
git diff main..HEAD -- pydme/actions/*.py | python3 -c "
import sys, re
content = sys.stdin.read()
# 找碎片
for m in re.finditer(r'([a-zA-Z]{3,})\1', content):
    print(f'DOUBLED: {m.group()}')
# 找中文标点
for ch in ['。','，','；','：']:
    if ch in content:
        print(f'CN-PUNCT: {ch}')
"

# 4. 提交修复
git commit -m "fix: correct [file] [issue description]"
git push
```

## 输出标准

- 每个检查的文件记录发现的 issue 数量
- 严重 issue（语义错误）必须修复
- 轻微 issue（格式/冠词）可选修复
- 确保 `参数格式如下：[{` / `属性格式如下：{` 标记不受影响
- 确保 `cli.py` 解析器中的对应检查行不受影响
