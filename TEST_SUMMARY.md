# pydme 全量动作测试 — 执行总结

> **测试时间**: 2026-06-16  
> **目标环境**: DME 25.0.0 (127.0.0.1)  
> **接入存储**: OceanStor Dorado 5500 V6, Dorado 6000 V6, OceanStor Pacific ×4  

---

## 总体结果

**131 PASS · 7 FAIL · 6 SKIP · 2 TIMEOUT** — 覆盖 146 个测试点（计划 225 个动作定义）

| 指标 | 数量 |
|------|------|
| 计划定义动作数 | 225 |
| 已测试动作数 | 136 |
| 覆盖比例 | ~60% |
| 通过率（已测） | 89.7% |

---

## 各阶段详情

| 阶段 | PASS | FAIL | SKIP/T | 关键状态 |
|------|------|------|--------|----------|
| **Phase 0** 认证 | 4 | — | — | `login` `logout` `show` `certificate` ✅ |
| **Phase 1** System | 17 | — | 2 SKIP | `user/role` 权限不足；其余全部通过 |
| **Phase 2** Storage | 25 | 1 | — | `app_type list` timeout 唯一残留 FAIL |
| **Phase 3** SAN | 13 | — | — | lun/group/host/port/mapping 全部通过 |
| **Phase 3** NAS | 7 | — | — | filesystem/nfs/cifs/quota/dtree/ns/kvcache 全部通过 |
| **Phase 4** Protect | 6 | — | 4 TIMEOUT | snapshot/group/hypermetro_domain/fs_snapshot 通过 |
| **Phase 5** FC Switch | 6 | 1 | 1 TIMEOUT | zone timeout（交换机忙） |
| **Phase 5** IP Switch | 8 | — | — | list/frame/board/subcard/power/fan/port 全部通过 |
| **Phase 6** Server/Virt/Kube | 18 | — | 2 SKIP | vm/cluster/host/datastore/disk/vdisk 全部通过 |
| **Phase 7** 其余 | 17 | — | — | tenant/gfs/workflow/integrate/backup/aiops 通过 |
| **Phase 8** 写操作 | 11 | 4 | 1 TIMEOUT | vstore/tag/host/lungroup/instance 创建通过 |

---

## 代码 Bug 修复

| # | 文件 | 问题 | 提交 |
|---|------|------|------|
| 1 | `pydme/cli.py` | argparse 将 `--param` 值吞为 position 参数 | `d4c6d17` |
| 2 | `pydme/cli.py` | orphan `--param` 被设成 `True` 而非实际值 | `2e6c584` |
| 3 | `pydme/cli.py` | 3 级命令的值被 `action_args` 吞，用错补位源 | `3ec3447` |
| 4 | `pydme/actions/virt.py` | 4 个 `show` 函数未传路径参数到 `client.get()` | `8ca3eaf` |
| 5 | `pydme/actions/workflow.py` | `template_show` 未传 `template_id` 到 `client.get()` | `fa29b04` |
| 6 | `pydme/cli.py` | param_mapping 缺 `*_ids` → `ids` 映射 | `ad0902a` |
| 7 | `pydme/client.py` | 日志打印原始路径模板而非格式化后 URL | `a04f8a0` |

---

## 剩余未测动作（~89 个）

主要集中于 Phase 8 写操作的 delete/modify/expand 等，原因：

1. **缺前置资源**（~45 个）— 需要先有 LUN、文件系统、快照等已创建的资源才能执行删除/修改
2. **参数不匹配**（~10 个）— 如 `nas filesystem create` 需要 `filesystem_specs` 而非 `capacity`
3. **FC 交换机通信慢**（~6 个）— `zone create/delete/modify` 超时
4. **DME 模块不可达**（~4 个）— `protect clone/hypermetro/replication` 超时，`topology` 动作名需修正

---

## 测试文件产出

| 文件 | 说明 |
|------|------|
| `.reasonix/plans/500-test-all-actions.md` | 完整测试计划 + 7 轮测试结果（~900 行） |
| `.reasonix/scripts/00-lib.sh` | `exec_test()` 辅助函数库 |
| `.reasonix/scripts/00-env.sh` | DME 环境变量 + access token |
| `.reasonix/scripts/02-storage-ids.sh` | 华为 Dorado/Pacific 存储 ID |
| `.reasonix/scripts/06-fcswitch-ids.sh` | FC Fabric WWN |
