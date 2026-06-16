# pydme 全量动作测试 — 最终报告

## 测试结果

**131 PASS · 7 FAIL · 6 SKIP · 2 TIMEOUT**

覆盖 **146 / 225** 个计划动作（65%），已测用例通过率 **89.7%**

---

## 代码 Bug 修复清单

| # | 文件 | 问题描述 | 提交 |
|---|------|----------|------|
| 1 | `pydme/cli.py` | **argparse 参数吞没**: `--param value` 的值被 position arg 吃掉 | `d4c6d17` |
| 2 | `pydme/cli.py` | **orphan 值变 True**: 3 级命令的 `--limit 10` 值为被 `action_args` 吞 | `3ec3447` |
| 3 | `pydme/actions/virt.py` | **4 个 show 函数缺路径参数**: 未将 ID 传给 `client.get()` | `8ca3eaf` |
| 4 | `pydme/actions/workflow.py` | **template_show 缺路径参数**: 同上 | `fa29b04` |
| 5 | `pydme/cli.py` | **param_mapping 缺失**: `vstore_ids` 等未映射到函数参数 `ids` | `ad0902a` |
| 6 | `pydme/client.py` | **日志打印模板而非真实 URL**: 路径中 `{id}` 未替换 | `a04f8a0` |
| 7 | `pydme/cli.py` | **initiator_ids 等映射缺失**: 补充了 8 组映射 | `592654c` |

---

## 剩余测试（~79 个）为何不能在此环境完成

### 需要前置资源（~53 个）
这些操作需要先在存储上创建 LUN、文件系统等资源，但当前测试环境 Dorado 5500 V6 上：

- **LUN 创建任务提交成功但存储侧未实际创建**: `lun_create` 返回 202 task_id，任务完成后 LUN 数为 0
- **NAS 文件系统无法创建**: 函数需要 `filesystem_specs` 复杂参数
- **FC 交换机超时**: 真实交换机通信慢，`fcswitch sync/zone create` 超时

### 需要特殊环境（~20 个）
- **保护组/双活/远程复制**: 需要至少两台存储设备配对
- **A800 存储特有功能**: `storage zone list`, `failover_group` 仅 OceanStor A800 支持
- **无服务器接入**: `server cpu/memory/disk` 等因无服务器设备 SKIP

### 需要修正计划（~6 个）
- **AIOPs topology 动作名**: 计划写 `topology list`，实际动作为 `topology_query_san_path` 等
- **nas filesystem create 参数**: 计划用 `--capacity`，实际需 `filesystem_specs`

---

## 产出文件

| 文件 | 内容 |
|------|------|
| `.reasonix/plans/500-test-all-actions.md` | 完整测试计划 + 8 轮执行结果 |
| `.reasonix/scripts/00-lib.sh` | `exec_test()` 执行/记录辅助库 |
| `.reasonix/scripts/00-env.sh` | DME 环境变量 + access token |
| `.reasonix/scripts/02-storage-ids.sh` | 华为 Dorado 5500 V6 + Pacific 存储 ID |
| `.reasonix/scripts/06-fcswitch-ids.sh` | FC Fabric WWN = 100050EB1AEC4731 |
| `TEST_SUMMARY.md` | 本报告 |
