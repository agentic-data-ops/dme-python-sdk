# 计划 000：同步 dev 分支变更到 main

## 目标

将 `dev` 分支上 `pydme/` 目录的变更同步到 `main` 分支，使用 checkout 覆盖方式（不产生 merge commit），**仅一次 commit**。忽略 `.reasonix/` 和 `REASONIX.md`。

## 差异分析

`origin/main` vs `origin/dev` 在同步范围内的差异：

| 文件 | 变更 |
|------|------|
| `pydme/actions/protect.py` | +1140 / -484 |
| `pydme/actions/backup.py` | +31 / -24 |
| `pydme/actions/tenant.py` | +29 / -11 |
| `pydme/actions/ipswitch.py` | +17 / -13 |
| `pydme/actions/fcswitch.py` | +14 / -11 |
| `pydme/client.py` | +14 / -8 |
| `pydme/actions/aiops.py` | +10 / -8 |
| `pydme/actions/workflow.py` | +8 / -8 |
| `pydme/actions/virt.py` | +11 / -9 |
| `pydme/cli.py` | +25 / -12 |
| **合计** | **10 文件，+947 / -456** |

`README.md`、`install.sh`、`pyproject.toml` 已同步，无差异。

## 同步步骤

```bash
# 1. 切到 main 并拉取最新
git checkout main
git pull origin main

# 2. 从 dev checkout 变更文件（覆盖本地，不产生 merge commit）
git checkout origin/dev -- pydme/

# 3. 提交（仅一次）
git commit -m "sync: merge pydme/ updates from dev (10 files, +947/-456)

同步 dev 分支 123 个 commit 中对 pydme/ 的变更。"

# 4. 推送
git push origin main
```

## 完成标准

- [ ] `git status` 干净
- [ ] 仅一个 commit，无 merge commit
- [ ] `git push origin main` 成功
- [ ] `git diff origin/main..origin/dev -- pydme/` 返回空（已同步）
