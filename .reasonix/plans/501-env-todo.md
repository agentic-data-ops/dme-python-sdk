# 待办：环境准备与剩余用例执行

## 环境准备

- [x] 部署双活（HyperMetro）和复制（Replication）环境 ✅
  - `protect fs_hypermetro_pair list/create/pause/sync/delete` — **5/5 全部 PASS ✅**（见 8.26）
  - `protect vstore_hypermetro_pair list/create/modify/switch/force_start/delete` — **6/6 全部 PASS ✅**（见 8.27）
- [ ] 部署 A800 系列存储设备
  - 用于：`storage zone_list`、`storage vlan_*`、`storage failover_group_*` 等 A800 专属动作
- [ ] 准备 Pacific 存储 DataTurbo 数据
  - 用于：`dataturbo_share_*`、`dpc_show` 共 6 个动作

## 权限配置

- [x] 给 API 调用用户（`wyhapi`）添加**安全管理员**权限 ✅
  - `system user list/show/create/delete` 已通过
  - 约 5 个 SKIP 动作已恢复

## 执行顺序

1. ✅ 双活环境部署 + 补测（已完成）
2. 补测 DataTurbo 动作（待 Pacific 数据就绪）
3. 补测 A800 动作（待 A800 设备就绪）
