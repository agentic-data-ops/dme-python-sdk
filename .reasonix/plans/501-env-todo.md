# 待办：环境准备与剩余用例执行

## 环境准备

- [ ] 部署双活（HyperMetro）和复制（Replication）环境
  - 用于：`filesystem_pair_*`、`vstore_pair_*` 共 9 个动作
- [ ] 部署 A800 系列存储设备
  - 用于：`storage zone_list`、`storage vlan_*`、`storage failover_group_*` 等 A800 专属动作
- [ ] 准备 Pacific 存储 DataTurbo 数据
  - 用于：`dataturbo_share_*`、`dpc_show` 共 6 个动作

## 权限配置

- [ ] 给 API 调用用户（`wyhapi`）添加**安全管理员**权限
  - 解决：`system user list`、`system role list` 等 common.0001 权限不足问题
  - 预计可恢复：~5 个 SKIP 动作

## 执行顺序

1. 环境准备 → 2. 补测双活相关动作 → 3. 补测 DataTurbo 动作 → 4. 补测 A800 动作
