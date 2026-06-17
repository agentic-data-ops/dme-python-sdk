# 计划 000：同步 dev 分支到 main（pydme/ + 根目录文件）

## 目标

将 `dev` 分支上对以下目录和文件的全部变更一次性同步到 `main` 分支，**仅产生一次 commit + push**。

| 路径 | 类型 | 说明 |
|------|------|------|
| `pydme/` | 目录 | 核心 SDK 包（12 个文件变更：+725 / -308） |
| `README.md` | 文件 | 项目说明文档 |
| `install.sh` | 文件 | **新文件**（仅 dev 存在） |
| `pyproject.toml` | 文件 | 项目打包配置 |

## 背景

- `main` 本地已检出，远程 `origin/main` 与本地同步
- `origin/dev` 领先 `origin/main` 共 **118 个 commit**
- 共同祖先 commit：`3efa69eecf516404a20e55af54bcb1a30dea1240`
- sync 范围外的文件（如 `.reasonix/`、测试脚本、英文分支文件等）**不包含**

## 同步策略

使用 **checkout + 路径限定 merge**（`git checkout dev -- <paths>` 方式），不进行 full-branch merge，避免引入无关变更。

### 步骤

```bash
# 1. 确保本地 main 已拉取最新
git checkout main
git pull origin main

# 2. 从 dev 提取指定路径的最新内容到暂存区
git checkout origin/dev -- pydme/ README.md install.sh pyproject.toml

# 3. 提交（仅一次 commit）
git commit -m "sync: merge pydme/, README.md, install.sh, pyproject.toml from dev

同步 dev 分支 118 个 commit 中对以下路径的变更：
- pydme/ (12 文件变更: +725 / -308)
- README.md
- install.sh (新文件)
- pyproject.toml"

# 4. 推送
git push origin main
```

## 风险与注意事项

| 风险 | 等级 | 缓解措施 |
|------|------|----------|
| 路径覆盖丢失 main 特有修改 | 中 | 确认 main 无以上路径的专属变更（`git diff origin/main..origin/dev -- <paths>` 已验证） |
| 冲突需要手动解决 | 低 | `checkout --` 覆盖策略无冲突，直接以 dev 版本为准 |
| 测试环境未验证 | 低 | 仅同步代码，实际测试由后续计划（如 500）覆盖 |

## 完成标准

- [ ] `git status` 干净，无未跟踪/未暂存文件
- [ ] `git log -1` 显示 commit message 正确
- [ ] `git push origin main` 成功，远程仓库已更新
- [ ] `git diff origin/main..origin/dev -- pydme/ README.md install.sh pyproject.toml` 返回空（已同步）
