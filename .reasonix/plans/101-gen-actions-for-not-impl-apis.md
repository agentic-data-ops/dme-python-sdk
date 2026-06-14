# 计划：为未实现的API生成动作函数

## 概述

参考文档中共有 **517** 个API定义，已有 **399** 个通过URI匹配到动作文件，**116** 个未实现。
请在执行前手动检查以下列表，确认是否需要为每个API创建动作函数。

---

## storage（存储管理）

> 以下storage主题下的待实现动作已全部移入例外列表，理由见例外列表。

| # | 名称 | 方法 | URI | 说明 |
|---|------|------|-----|------|
| 1 | 批量查询分布式存储设备的硬盘池 | POST | `/rest/storagemgmt/v1/diskpools/query` | `disk_pool_list` | disk |
> **注：** 已有 `disk_pool_list`（对应 `disk-pools` 硬盘域）需**重命名为 `disk_domain_list`**，腾出 `disk_pool_list` 名称给分布式硬盘池新接口。 |

---

## nas（文件存储）

> **注：** 已有 `dpc` 子主题（`dpc_list`/`dpc_show`）对应的是 `dataturbo/DPC` 并行客户端管理，应**重命名为 `dataturbo`** 子主题。下方仅保留真正的 DPC 客户端动作。

| # | 名称 | 方法 | URI | 建议动作名 | 子主题 |
|---|------|------|-----|-----------|-------|
| 1 | 批量查询DPC客户端 | POST | `/rest/fileservice/v1/dpc-clients/query` | `list` | dpc |
| 2 | 查询DPC客户端详情 | GET | `/rest/fileservice/v1/dpc-clients/{id}` | `show` | dpc |

---



---

## protect（数据保护）

| # | 名称 | 方法 | URI | 建议动作名 | 子主题 |
|---|------|------|-----|-----------|-------|
| 1 | 查询可创建双活Pair的目标LUN | POST | `/rest/protection/v1/metro/lun-pairs/{source_lun_id}/optional-target-luns` | `query_available_luns` | hypermetro_pair |
> 注：原有replication子主题条目已移除。**已实现的 `replication_pair_*` 函数应升级URI**：从 `/rest/protection/v1/replication/lun-pairs` 改为 `/rest/protection/v1/replication/pairs`，参数 `lun_pairs`/`lun_ids` 调整为 `resource_pairs`。新版 `pairs` API 同时支持 LUN 和文件系统，无需新建 `fs_replication_pair` 动作。
| 2 | 创建文件系统双活Pair | POST | `/rest/protection/v1/hypermetro/filesystem-pairs` | `filesystem_pair_create` | fs_hypermetro_pair |
| 3 | 查询文件系统双活Pair列表 | POST | `/rest/protection/v1/hypermetro/filesystem-pairs/query` | `filesystem_pair_list` | fs_hypermetro_pair |
| 4 | 批量暂停文件系统双活Pair | POST | `/rest/protection/v1/hypermetro/filesystem-pairs/pause` | `filesystem_pair_pause` | fs_hypermetro_pair |
| 5 | 批量同步文件系统双活Pair | POST | `/rest/protection/v1/hypermetro/filesystem-pairs/sync` | `filesystem_pair_sync` | fs_hypermetro_pair |
| 6 | 批量删除文件系统双活Pair | POST | `/rest/protection/v1/hypermetro/filesystem-pairs/delete` | `filesystem_pair_delete` | fs_hypermetro_pair |
| 7 | 创建文件系统快照 | POST | `/rest/protection/v1/filesystem-snapshots` | `fs_snapshot_create` | fs_snapshot |
| 8 | 批量查询文件系统快照 | POST | `/rest/protection/v1/filesystem-snapshots/query` | `fs_snapshot_list` | fs_snapshot |
| 9 | 批量删除文件系统快照 | POST | `/rest/protection/v1/filesystem-snapshots/delete` | `fs_snapshot_delete` | fs_snapshot |
| 10 | 批量强制启动双活租户Pair | POST | `/rest/protection/v1/metro/vstore-pairs/force-start` | `vstore_pair_force_start` | vstore_hypermetro_pair |
| 11 | 创建双活租户Pair | POST | `/rest/protection/v1/metro/vstore-pairs` | `vstore_pair_create` | vstore_hypermetro_pair |
| 12 | 查询双活租户Pair列表 | POST | `/rest/protection/v1/metro/vstore-pairs/query` | `vstore_pair_list` | vstore_hypermetro_pair |
| 13 | 批量主从切换双活租户Pair | POST | `/rest/protection/v1/metro/vstore-pairs/switch` | `vstore_pair_switch` | vstore_hypermetro_pair |
| 14 | 批量删除双活租户Pair | POST | `/rest/protection/v1/metro/vstore-pairs/delete` | `vstore_pair_delete` | vstore_hypermetro_pair |
| 15 | 修改指定双活租户pair | PUT | `/rest/protection/v1/metro/vstore-pairs/{id}` | `vstore_pair_modify` | vstore_hypermetro_pair |
| 16 | 强制启动文件系统双活域 | POST | `/rest/protection/v1/hyper-metro-domains/{id}/force-start` | `hypermetro_domain_force_start` | hypermetro_domain |
| 17 | 优先站点切换文件系统双活域 | POST | `/rest/protection/v1/hyper-metro-domains/{id}/switch-priority-site` | `hypermetro_domain_switch_site` | hypermetro_domain |
| 18 | 恢复文件系统双活域 | POST | `/rest/protection/v1/hyper-metro-domains/{id}/recover` | `hypermetro_domain_recover` | hypermetro_domain |
| 19 | 分裂文件系统双活域 | POST | `/rest/protection/v1/hyper-metro-domains/{id}/split` | `hypermetro_domain_split` | hypermetro_domain |
| 20 | 主从切换文件系统双活域 | POST | `/rest/protection/v1/hyper-metro-domains/{id}/swap-role` | `hypermetro_domain_swap_role` | hypermetro_domain |

---



---

## system（系统管理）

| # | 名称 | 方法 | URI | 建议动作名 | 子主题 |
|---|------|------|-----|-----------|-------|
| 1 | 批量查询Region | POST | `/rest/regionmgmt/v1/regions/query` | `region_list` | region |
| 2 | 查询下级Region资源信息 | POST | `/rest/regionmgmt/v1/regions/{region_id}/resources/query` | `region_query` | region |

---

## san（块存储 / 主机管理）

| # | 名称 | 方法 | URI | 建议动作名 | 子主题 |
|---|------|------|-----|-----------|-------|
| 1 | 查询物理主机组关联的存储主机组列表 | GET | `/rest/hostmgmt/v1/hostgroups/{hostgroup_id}/related-storage-hostgroups` | `show_related` | physical_host_group |
| 2 | 查询存储主机和LUN映射关系 | POST | `/rest/blockservice/v1/mapping-views/query_for_host_to_lun` | `query_host_to_lun` | mapping_view |

---

## integrate（三方系统集成）

| # | 名称 | 方法 | URI | 建议动作名 | 子主题 |
|---|------|------|-----|-----------|-------|
| 1 | 查询CMDB系统列表 | POST | `/rest/appmgmt/v1/cmdb-systems/query` | `cmdb_system_list` | cmdb |
| 2 | 查询CMDB系统中的主机列表 | POST | `/rest/appmgmt/v1/cmdb-hosts/query` | `cmdb_host_list` | cmdb |
| 3 | 查询指定CMDB主机详情 | GET | `/rest/appmgmt/v1/cmdb-hosts/{cmdb_host_id}` | `cmdb_host_show` | cmdb |
| 4 | 查询CMDB系统中的应用列表 | POST | `/rest/appmgmt/v1/applications/query` | `cmdb_app_list` | cmdb |
| 5 | 根据启动器列表查询CMDB主机列表 | POST | `/rest/appmgmt/v1/cmdb-hosts/query-by-initiators` | `cmdb_host_query_by_initiators` | cmdb |

---

## 例外列表（无需实现）

以下API无需生成动作函数，原因标注在说明中。

| # | 名称 | 方法 | URI | 原因 |
|---|------|------|-----|------|
| 1 | 查询单个资源实例 | GET | `/rest/resourcedb/v1/instances/{className}/{instanceId}` | CMDB资源查询，拓扑函数已覆盖 |
| 2 | 条件查询某类型关系的所有实例 | GET | `/rest/resourcedb/v1/relations/{relationName}/instances` | CMDB关系查询，拓扑函数已覆盖 |
| 3 | 查询单个资源关系的实例 | GET | `/rest/resourcedb/v1/relations/{relationName}/instances/{instanceId}` | CMDB关系查询，拓扑函数已覆盖 |
| 4 | 注册北向订阅系统 | POST | `/rest/djaianalysisservice/northbound-subscription-mgmt/v1/northbound-subscription-systems` | 北向订阅管理，非通用场景 |
| 5 | 查询北向订阅系统列表 | GET | `/rest/djaianalysisservice/northbound-subscription-mgmt/v1/northbound-subscription-systems` | 同上 |
| 6 | 查询指定北向订阅系统 | GET | `/rest/djaianalysisservice/northbound-subscription-mgmt/v1/northbound-subscription-systems/{system_id}` | 同上 |
| 7 | 更新指定北向订阅系统 | PUT | `/rest/djaianalysisservice/northbound-subscription-mgmt/v1/northbound-subscription-systems/{system_id}` | 同上 |
| 8 | 删除指定北向订阅系统 | DELETE | `/rest/djaianalysisservice/northbound-subscription-mgmt/v1/northbound-subscription-systems/{system_id}` | 同上 |
| 9 | 查询告警订阅记录 | GET | `/rest/djaianalysisservice/northbound-subscription-mgmt/v1/northbound-subscription-systems/{system_id}/alarm-subscriptions` | 同上 |
| 10 | 设置告警订阅记录 | PUT | `/rest/djaianalysisservice/northbound-subscription-mgmt/v1/northbound-subscription-systems/{system_id}/alarm-subscriptions` | 同上 |
| 11 | 对接主Region | POST | `/rest/regionmgmt/v1/parent-regions` | Region配置操作，需手动配置而非API调用 |
| 12 | 修改主Region | PUT | `/rest/regionmgmt/v1/parent-regions/{parent_region_id}` | 同上 |
| 13 | 删除指定的主Region | DELETE | `/rest/regionmgmt/v1/parent-regions/{parent_region_id}` | 同上 |
| 14 | 查询指定交换机的端口列表 | POST | `/rest/fcswitchmgmt/v1/fcswitches/{id}/ports/list` | 已有 `port_list` 支持 `switch_id` 参数过滤 |
| 15 | 批量查看创建Zone的操作命令 | POST | `/rest/fcswitchmgmt/v1/zones/create-commands/show` | Zone操作已有 `zone_create`/`zone_list` 等动作覆盖 |
| 16 | 批量上电存储设备 | POST | `/rest/storagemgmt/v1/storages/power-on` | 运维操作，非自动化场景 |
| 17 | 批量下电存储设备 | POST | `/rest/storagemgmt/v1/storages/power-off` | 同上 |
| 18 | 批量重启存储设备 | POST | `/rest/storagemgmt/v1/storages/reboot` | 同上 |
| 19 | 导入/导出License | POST | `/rest/storagemgmt/v1/storage-license/upload` `/rest/storagemgmt/v1/storage-license/export` | License操作，非日常场景 |
| 20 | 发送请求给第三方存储 | POST | `/rest/3rdsystemmgmt/v1/3rd-systems/transmission` | 第三方存储透传，非通用场景 |
| 21 | LLD文件/集群开局/重试 | 3 POST | `/rest/storageclustermgmt/v1/configs/upload` `/configs/init` `/configs/reinit` | A800集群操作，非通用场景 |
| 22 | 数据流动/线缆检测/配置收集 | 7个API | `/rest/storagemgmt/v1/smart-migration-*` `/rest/storageclusterservice/v1/cable-*` `/rest/storagemgmt/v1/storage-config/*` | 专用运维场景，非通用查询 |
| 23 | 硬盘列表/指标 | 5个API | `/rest/storagemgmt/v1/storages/{id}/disks` `/rest/diskanalysismgmt/v1/storages/*` `/rest/diskexporter/v1/disks/metrics` | 已有 `disk_list`(v2) 综合过滤覆盖 |
| 24 | 并行客户端注册/取消注册 | 2 POST | `/rest/dpc-mgmt/v2/dpcs/register` `/deregister` | DPC注册操作，已通过设备纳管流程覆盖 |
| 25 | DPC授权IP管理 | 3个API | `/rest/fileservice/v1/namespaces/dpc-auth-clients/*` | DPC授权管理，非通用场景 |
| 26 | 数据流动模板下载/文件上传下载 | 3 POST | `/rest/fileservice/v1/datamotion/*` | 数据流动模板操作，专用场景 |
| 27 | WORM文件系统诉讼保留 | 3 POST | `/rest/fileservice/v1/filesystems/{id}/worm-file-legalhold/*` | WORM诉讼保留，合规专用场景 |
| 28 | 批量查询分布式存储设备的硬盘池 | POST | `/rest/storagemgmt/v1/diskpools/query` | 保留为新动作 |
| 24 | 透传设备请求 | POST | `/rest/storagemgmt/v1/transmit-huawei-storage-request` | 设备透传，非通用场景 |
| 25 | 查询秒级历史性能数据 | POST | `/rest/metrics/v1/data-svc/second-data/action/query` | 已有 `performance_history_data` 等覆盖性能查询 |
| 17 | 创建并行客户端性能文件收集任务 | POST | `/rest/dpc-mgmt/v1/performance-data/collection-task` | DPC性能收集，非通用场景 |
| 18 | 查询并行客户端性能文件收集进度 | GET | `/rest/dpc-mgmt/v1/performance-data/collection-task` | 同上 |
| 19 | 下载并行客户端性能文件 | GET | `/rest/dpc-mgmt/v1/performance-data/download` | 同上 |
| 20 | 清理并行客户端性能文件收集结果 | POST | `/rest/dpc-mgmt/v1/performance-data/cleanup` | 同上 |
| 21 | 查询数据集统计信息 | POST | `/rest/metrics/v1/datasets/{dataset}/statistics` | 已有 `performance_history_data` 等覆盖 |
| 22 | 迭代查询当前告警信息 | POST | `/rest/alarmmgmt/v1/alarms/current-alarm/query` | 已有 `alarm_list` 覆盖 |
| 23 | 历史告警迭代查询 | POST | `/rest/alarmmgmt/v1/alarms/history-alarms/query` | 已有 `alarm_list` 通过 `include_history` 参数覆盖 |

---

## 统计

- 总API数: 517
- 已实现: 399
- **待实现: 32**（protect 20个 + storage 1个 + nas 2个 + integrate 5个 + system 2个 + san 2个）
- **例外（无需实现）: 76**
- **升级任务（无需新建函数）: 1**（replication_pair URI升级）
- **重命名任务: 2**（已有 `dpc` 子主题 → `dataturbo`；已有 `disk_pool_list` → `disk_domain_list`）

## 处理建议

1. 按章节分批处理，每批实现 5-10 个API
2. 创建函数后注册到 ACTIONS 字典
3. 按照项目约定的 docstring 格式编写 Args 和 Returns
