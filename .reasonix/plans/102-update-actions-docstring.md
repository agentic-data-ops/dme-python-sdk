# 计划 102：遍历所有动作 help 信息，校验参数/响应格式与 API 参考一致性

## 概述

本计划的目标是**实际运行 CLI 帮助信息**，逐动作检查 docstring 中定义的参数格式和 Returns 段是否与 API 参考文档一致——而非仅凭代码静态推测。

## 背景

当前 16 个 topic、425 个动作的 docstring 大部分已包含格式化的 `Args` 和 `Returns` 段，但存在以下隐患：

| 问题类型 | 举例 |
|---------|------|
| **参数格式入口标记错误** | 使用 `格式：{` 而非 `参数格式如下：{`，导致 `--help` 中泄露内部字段 |
| **嵌套字段缺失/多余** | docstring 中列的字段数与 API 实际参数不符 |
| **字段名不匹配** | docstring 用的 `count`，API 实际是 `total` |
| **Returns 字段不完整** | 只列了 5~6 个核心字段，API 实际返回 20~30+ 字段 |
| **引用对象未展开** | 嵌套对象（如 Volume→Attachment）在 docstring 中未按格式展开 |
| **约束不一致** | docstring 写的 `(1~64)`，API 参考实际是 `(1~255)` |
| **枚举值缺失/过时** | docstring 枚举列表不全或已废弃值未移除 |
| **纯文本 Returns 无结构** | "返回任务列表" 既无字段名也无类型 |
| **动作描述不完整** | 动作描述过于简略，未涵盖 API 参考文档中的功能描述 |

## 校验方法

### 第一步：运行 help 获取当前输出

```bash
pydme <topic> --help                      # 列出 topic 下所有动作
pydme <topic> <action> --help            # 查看单个动作的参数和响应
```

### 第二步：从 `--help` 输出识别问题模式

通过 `--help` 输出，可以直接发现：

- **参数泄露**：`--help` 中出现了不应有的 `--name`、`--type`、`--mode` 等参数 → 说明 docstring 中某处用了 `格式：{` 而非 `参数格式如下：{`
- **多余参数**：`--help` 中多出了预期之外的参数 → 格式块入口标记错误导致内部字段外泄
- **缺失参数**：`--help` 中没有预期应有的参数 → docstring 定义不完整
- **类型/约束错误**：参数类型或约束与 API 参考不符

### 第三步：对照 `.reasonix/reference/dme-api-reference.md` 校验

对每个动作，在参考文档中查找对应的 API 定义（通过函数体中的 URI 匹配），检查：

1. **动作描述完整性** — 动作的 `description`（docstring 第一行）是否涵盖了 API 参考文档中的功能描述；如果过于简略，补充完整
2. **参数完整性和正确性** — docstring 中的每个参数是否对应 API 的请求参数
3. **嵌套对象格式** — 是否使用了正确的入口标记（`参数格式如下：[{` / `属性格式如下：{`）
4. **字段约束** — 长度、取值范围、枚举值是否一致
5. **Returns 段** — 响应字段是否完整、嵌套对象是否展开、类型是否正确

## 校验规则

### 参数格式规则

| 规则 | 要求 |
|------|------|
| 入口标记 | 复杂参数必须用 `参数格式如下：[{`（列表）或 `参数格式如下：{`（字典） |
| 禁止标记 | 不得使用 `格式：{`、`格式：[{`、`数据格式：` 等其它标记 |
| 嵌套入口 | 内部嵌套对象必须用 `属性格式如下：{` |
| 字段分隔 | 格式块内每个字段行末添加 `,` |
| 约束格式 | 英文括号 `()` 包裹，如 `(1~255个字符)` |
| 枚举格式 | `可选值：enum1 (描述), enum2 (描述)` 英文括号 |
| 句号结尾 | 每个参数描述以中文句号 `。` 结尾 |

### Returns 格式规则

| 响应复杂度 | 格式 | 示例 |
|-----------|------|------|
| **简单结构**（1-3 个普通字段，无嵌套） | 文本描述 | `Returns: 任务ID。` |
| **复杂结构**（多个字段 + 嵌套对象/列表） | JSON 风格 | `Returns:\n    {\n        total: ...` |
| **无返回值**（delete/refresh） | 文本描述 | `Returns: 无。` |

**JSON 风格 Returns 约定**：
- 以 `{` 开头，不加前缀文字
- 嵌套列表用 `参数格式如下：[{` 标记
- 嵌套对象用 `属性格式如下：{` 标记
- 无引号，英文括号约束
- 字段行末加 `,`
- `}` 平衡

## 分批执行计划（含动作 ↔ API URI 对照表）

每批包含：运行 help → 校验参数 → 校验 Returns → 修复 → 提交。

对照表中的 API 章节可通过以下方式定位：在 `.reasonix/reference/dme-api-reference.md` 中搜索 URI 路径（如 `/rest/protection/v1/protection-groups/query`）或 HTTP 方法+URI 组合，即可找到对应的参数表和响应字段定义。

---

### 第 1 批：`protect.py`（75 个动作）

**文件**：`pydme/actions/protect.py`
**API 章节搜索关键词**：`/rest/protection/v1/`

| 动作名 | HTTP 方法 | URI 路径 | 对应 API 章节关键词 |
|--------|----------|----------|-------------------|
| `group_list` | POST | `/rest/protection/v1/protection-groups/query` | protection-groups |
| `group_create` | POST | `/rest/protection/v1/protection-groups` | protection-groups |
| `group_modify` | PUT | `/rest/protection/v1/protection-groups/{pg_id}` | protection-groups |
| `group_delete` | POST | `/rest/protection/v1/protection-groups/delete` | protection-groups/delete |
| `group_add_luns` | POST | `/rest/protection/v1/protection-groups/{pg_id}/add-luns` | add-luns |
| `group_remove_luns` | POST | `/rest/protection/v1/protection-groups/{pg_id}/remove-luns` | remove-luns |
| `hypermetro_group_list` | POST | `/rest/protection/v1/metro/groups/query` | metro/groups |
| `hypermetro_group_create` | POST | `/rest/protection/v1/metro/groups` | metro/groups |
| `hypermetro_group_modify` | PUT | `/rest/protection/v1/metro/groups/{group_id}` | metro/groups |
| `hypermetro_group_delete` | POST | `/rest/protection/v1/metro/groups/delete` | metro/groups/delete |
| `hypermetro_group_add_pairs` | POST | `/rest/protection/v1/metro/groups/{group_id}/add-pairs` | add-pairs |
| `hypermetro_group_remove_pairs` | POST | `/rest/protection/v1/metro/groups/{group_id}/remove-pairs` | remove-pairs |
| `hypermetro_group_pause` | POST | `/rest/protection/v1/metro/groups/pause` | pause |
| `hypermetro_group_force_startup` | POST | `/rest/protection/v1/metro/groups/force-startup` | force-startup |
| `hypermetro_group_switch_priority` | POST | `/rest/protection/v1/metro/groups/switch-priority-site` | switch-priority-site |
| `hypermetro_group_sync` | POST | `/rest/protection/v1/metro/groups/sync` | sync |
| `hypermetro_pair_list` | POST | `/rest/protection/v1/metro/lun-pairs/query` | metro/lun-pairs |
| `hypermetro_pair_create` | POST | `/rest/protection/v1/metro/lun-pairs` | metro/lun-pairs |
| `hypermetro_pair_modify` | PUT | `/rest/protection/v1/metro/lun-pairs/{pair_id}` | metro/lun-pairs |
| `hypermetro_pair_delete` | POST | `/rest/protection/v1/metro/lun-pairs/delete` | lun-pairs/delete |
| `hypermetro_pair_sync` | POST | `/rest/protection/v1/metro/lun-pairs/sync` | lun-pairs/sync |
| `hypermetro_pair_pause` | POST | `/rest/protection/v1/metro/lun-pairs/pause` | lun-pairs/pause |
| `hypermetro_pair_force_startup` | POST | `/rest/protection/v1/metro/lun-pairs/force-startup` | force-startup |
| `hypermetro_pair_switch_priority` | POST | `/rest/protection/v1/metro/lun-pairs/switch-priority-site` | switch-priority-site |
| `hypermetro_domain_list` | POST | `/rest/protection/v1/hyper-metro-domains/query` | hyper-metro-domains |
| `replication_group_create` | POST | `/rest/protection/v1/replication/groups` | replication/groups |
| `replication_group_list` | POST | `/rest/protection/v1/replication/groups/query` | replication/groups |
| `replication_group_modify` | PUT | `/rest/protection/v1/replication/groups/{replication_group_id}` | replication/groups |
| `replication_group_delete` | POST | `/rest/protection/v1/replication/groups/delete` | groups/delete |
| `replication_group_add_pairs` | POST | `/rest/protection/v1/replication/groups/{group_id}/add-pairs` | add-pairs |
| `replication_group_remove_pairs` | POST | `/rest/protection/v1/replication/groups/{group_id}/remove-pairs` | remove-pairs |
| `replication_group_sync` | POST | `/rest/protection/v1/replication/groups/sync` | sync |
| `replication_group_split` | POST | `/rest/protection/v1/replication/groups/split` | split |
| `replication_group_switch` | POST | `/rest/protection/v1/replication/groups/switch` | switch |
| `replication_group_switch_write_protection` | POST | `/rest/protection/v1/replication/groups/{id}/switch-write-protection` | switch-write-protection |
| `replication_pair_list` | POST | `/rest/protection/v1/replication/pairs/query` | replication/pairs |
| `replication_pair_create` | POST | `/rest/protection/v1/replication/pairs` | replication/pairs |
| `replication_pair_modify` | PUT | `/rest/protection/v1/replication/pairs/{pair_id}` | replication/pairs |
| `replication_pair_delete` | POST | `/rest/protection/v1/replication/pairs/delete` | pairs/delete |
| `replication_pair_sync` | POST | `/rest/protection/v1/replication/pairs/sync` | pairs/sync |
| `replication_pair_split` | POST | `/rest/protection/v1/replication/pairs/split` | split |
| `replication_pair_switch` | POST | `/rest/protection/v1/replication/pairs/switch` | switch |
| `replication_pair_switch_write_protection` | POST | `/rest/protection/v1/replication/pairs/{id}/switch-write-protection` | switch-write-protection |
| `device_pair_list` | POST | `/rest/protection/v1/device-pairs/query` | device-pairs |
| `replication_link_list` | POST | `/rest/protection/v1/device-pairs/replication-links/query` | replication-links |
| `snapshot_list` | POST | `/rest/protection/v1/lun-snapshots/query` | lun-snapshots |
| `snapshot_create` | POST | `/rest/protection/v1/lun-snapshots` | lun-snapshots |
| `snapshot_rollback` | POST | `/rest/protection/v1/lun-snapshots/batch-rollback` | batch-rollback |
| `snapshot_delete` | POST | `/rest/protection/v1/lun-snapshots/batch-delete` | batch-delete |
| `snapshot_group_create` | POST | `/rest/protection/v1/snapshot-consistency-groups` | snapshot-consistency-groups |
| `snapshot_group_delete` | POST | `/rest/protection/v1/snapshot-consistency-groups/batch-delete` | batch-delete |
| `snapshot_group_activate` | POST | `/rest/protection/v1/snapshot-consistency-groups/{snapshot_cg_id}/activate` | activate |
| `snapshot_group_deactivate` | POST | `/rest/protection/v1/snapshot-consistency-groups/batch-deactivate` | batch-deactivate |
| `snapshot_group_rollback` | POST | `/rest/protection/v1/snapshot-consistency-groups/{snapshot_cg_id}/rollback` | rollback |
| `clone_group_create` | POST | `/rest/protection/v1/clone-consistency-groups` | clone-consistency-groups |
| `clone_group_sync` | POST | `/rest/protection/v1/clone-consistency-groups/{clone_cg_id}/synchronize` | synchronize |
| `clone_group_delete` | POST | `/rest/protection/v1/clone-consistency-groups/batch-delete` | batch-delete |
| `filesystem_pair_create` | POST | `/rest/protection/v1/hypermetro/filesystem-pairs` | filesystem-pairs |
| `filesystem_pair_list` | POST | `/rest/protection/v1/hypermetro/filesystem-pairs/query` | filesystem-pairs |
| `filesystem_pair_pause` | POST | `/rest/protection/v1/hypermetro/filesystem-pairs/pause` | pause |
| `filesystem_pair_sync` | POST | `/rest/protection/v1/hypermetro/filesystem-pairs/sync` | sync |
| `filesystem_pair_delete` | POST | `/rest/protection/v1/hypermetro/filesystem-pairs/delete` | delete |
| `fs_snapshot_create` | POST | `/rest/protection/v1/filesystem-snapshots` | filesystem-snapshots |
| `fs_snapshot_list` | POST | `/rest/protection/v1/filesystem-snapshots/query` | filesystem-snapshots |
| `fs_snapshot_delete` | POST | `/rest/protection/v1/filesystem-snapshots/delete` | delete |
| `vstore_pair_force_start` | POST | `/rest/protection/v1/metro/vstore-pairs/force-start` | vstore-pairs |
| `vstore_pair_create` | POST | `/rest/protection/v1/metro/vstore-pairs` | vstore-pairs |
| `vstore_pair_list` | POST | `/rest/protection/v1/metro/vstore-pairs/query` | vstore-pairs |
| `vstore_pair_switch` | POST | `/rest/protection/v1/metro/vstore-pairs/switch` | switch |
| `vstore_pair_split` | POST | `/rest/protection/v1/metro/vstore-pairs/split` | split |
| `vstore_pair_sync` | POST | `/rest/protection/v1/metro/vstore-pairs/sync` | sync |
| `vstore_pair_delete` | POST | `/rest/protection/v1/metro/vstore-pairs/delete` | delete |

---

### 第 2 批：`san.py`（66 个动作）

**文件**：`pydme/actions/san.py`
**API 章节搜索关键词**：`/rest/blockservice/v1/` `/rest/hostmgmt/v1/` `/rest/storagemgmt/v1/port-groups/`

| 动作名 | HTTP 方法 | URI 路径 | 对应 API 章节关键词 |
|--------|----------|----------|-------------------|
| `lun_list` | GET | `/rest/blockservice/v1/volumes` | blockservice/volumes |
| `lun_show` | GET | `/rest/blockservice/v1/volumes/{volume_id}` | blockservice/volumes |
| `lun_create` | POST | `/rest/blockservice/v1/volumes/customize` | volumes/customize |
| `lun_delete` | POST | `/rest/blockservice/v1/volumes/delete` | volumes/delete |
| `lun_modify` | PUT | `/rest/blockservice/v1/volumes/{volume_id}` | blockservice/volumes |
| `lun_modify_name` | PUT | `/rest/blockservice/v1/volumes` | blockservice/volumes |
| `lun_expand` | POST | `/rest/blockservice/v1/volumes/expand` | volumes/expand |
| `lun_connection` | POST | `/rest/blockservice/v1/volumes/connection-infos-query` | connection-infos |
| `lun_group_list` | POST | `/rest/blockservice/v1/lun-groups/query` | lun-groups |
| `lun_group_show` | GET | `/rest/blockservice/v1/lun-groups/{group_id}` | lun-groups |
| `lun_group_create` | POST | `/rest/blockservice/v1/lun-groups` | lun-groups |
| `lun_group_delete` | POST | `/rest/blockservice/v1/lun-groups/delete` | lun-groups/delete |
| `lun_group_add_luns` | POST | `/rest/blockservice/v1/lun-groups/{group_id}/add-luns` | add-luns |
| `lun_group_remove_luns` | POST | `/rest/blockservice/v1/lun-groups/{group_id}/remove-luns` | remove-luns |
| `lun_group_show_luns` | POST | `/rest/blockservice/v1/lun-groups/{group_id}/luns/query` | luns/query |
| `mapping_view_create` | POST | `/rest/blockservice/v1/mapping-views` | mapping-views |
| `mapping_view_delete` | POST | `/rest/blockservice/v1/mapping-views/batch-delete` | batch-delete |
| `mapping_view_list` | POST | `/rest/blockservice/v1/mapping-views/query` | mapping-views |
| `storage_host_create` | POST | `/rest/hostmgmt/v1/storage-hosts` | hostmgmt/storage-hosts |
| `storage_host_batch_query` | POST | `/rest/hostmgmt/v1/storage-hosts/query-by-ids` | query-by-ids |
| `storage_host_list` | POST | `/rest/hostmgmt/v1/storage-hosts/query` | storage-hosts |
| `storage_host_modify` | PUT | `/rest/hostmgmt/v1/storage-hosts/{storage_host_id}` | storage-hosts |
| `storage_host_delete` | POST | `/rest/hostmgmt/v1/storage-hosts/delete` | delete |
| `storage_host_show_paths` | POST | `/rest/hostmgmt/v1/host-links/query` | host-links |
| `storage_host_show_luns` | POST | `/rest/blockservice/v1/lun-mapping/query` | lun-mapping |
| `storage_host_unmap_luns` | POST | `/rest/blockservice/v1/volumes/host-unmapping` | host-unmapping |
| `storage_host_group_create` | POST | `/rest/hostmgmt/v1/storage-hostgroups` | storage-hostgroups |
| `storage_host_group_list` | POST | `/rest/hostmgmt/v1/storage-hostgroups/query` | storage-hostgroups |
| `storage_host_group_add_hosts` | PUT | `/rest/hostmgmt/v1/storage-hostgroups/{storage_host_group_id}/hosts/add` | hosts/add |
| `storage_host_group_remove_hosts` | PUT | `/rest/hostmgmt/v1/storage-hostgroups/{storage_host_group_id}/hosts/remove` | hosts/remove |
| `storage_host_group_delete` | POST | `/rest/hostmgmt/v1/storage-hostgroups/delete` | delete |
| `storage_host_group_show_luns` | POST | `/rest/blockservice/v1/lun-mapping/query` | lun-mapping |
| `storage_host_group_unmap_luns` | POST | `/rest/blockservice/v1/volumes/hostgroup-unmapping` | hostgroup-unmapping |
| `port_group_list` | POST | `/rest/storagemgmt/v1/port-groups/query` | port-groups |
| `port_group_create` | POST | `/rest/storagemgmt/v1/port-groups` | port-groups |
| `port_group_show_ports` | POST | `/rest/storagemgmt/v1/port-groups/{port_group_id}/ports/query` | ports/query |
| `port_group_show_relations` | POST | `/rest/storagemgmt/v1/port-groups/ports/relations/query` | relations |
| `physical_host_list` | POST | `/rest/hostmgmt/v1/hosts/summary` | hosts/summary |
| `physical_host_show` | GET | `/rest/hostmgmt/v1/hosts/{host_id}/summary` | hosts/summary |
| `physical_host_create` | POST | `/rest/hostmgmt/v1/hosts` | hostmgmt/hosts |
| `physical_host_modify` | PUT | `/rest/hostmgmt/v1/hosts/{host_id}/general` | hosts/general |
| `physical_host_modify_access_info` | PUT | `/rest/hostmgmt/v1/hosts/{host_id}/accessinfo` | accessinfo |
| `physical_host_delete` | DELETE | `/rest/hostmgmt/v1/hosts/{host_id}` | hostmgmt/hosts |
| `physical_host_add_initiators` | PUT | `/rest/hostmgmt/v1/hosts/{host_id}/initiators/add` | initiators/add |
| `physical_host_remove_initiators` | PUT | `/rest/hostmgmt/v1/hosts/{host_id}/initiators/remove` | initiators/remove |
| `physical_host_show_initiators` | GET | `/rest/hostmgmt/v1/hosts/{host_id}/initiators` | initiators |
| `physical_host_test` | POST | `/rest/hostmgmt/v1/connectivity/host-and-storage` | connectivity |
| `physical_host_query_sshkey` | GET | `/rest/hostmgmt/v1/host-keys` | host-keys |
| `physical_host_save_sshkey` | PUT | `/rest/hostmgmt/v1/host-keys` | host-keys |
| `physical_host_query_by_initiator` | POST | `/rest/hostmgmt/v1/hosts/query-by-initiator` | query-by-initiator |
| `physical_host_map_luns` | POST | `/rest/blockservice/v1/volumes/host-mapping` | host-mapping |
| `physical_host_unmap_luns` | POST | `/rest/blockservice/v1/volumes/host-unmapping` | host-unmapping |
| `physical_host_show_mapping_views` | POST | `/rest/blockservice/v1/volumes/mapping-view/query` | mapping-view |
| `physical_host_group_list` | POST | `/rest/hostmgmt/v1/hostgroups/summary` | hostgroups |
| `physical_host_group_show_hosts` | POST | `/rest/hostmgmt/v1/hostgroups/{hostgroup_id}/hosts/list` | hosts/list |
| `physical_host_group_show` | GET | `/rest/hostmgmt/v1/hostgroups/{hostgroup_id}/summary` | hostgroups/summary |
| `physical_host_group_create` | POST | `/rest/hostmgmt/v1/hostgroups` | hostmgmt/hostgroups |
| `physical_host_group_modify` | PUT | `/rest/hostmgmt/v1/hostgroups/{hostgroup_id}/general` | hostgroups/general |
| `physical_host_group_delete` | DELETE | `/rest/hostmgmt/v1/hostgroups/{hostgroup_id}` | hostmgmt/hostgroups |
| `physical_host_group_add_hosts` | PUT | `/rest/hostmgmt/v1/hostgroups/{hostgroup_id}/hosts/add` | hosts/add |
| `physical_host_group_remove_hosts` | PUT | `/rest/hostmgmt/v1/hostgroups/{hostgroup_id}/hosts/remove` | hosts/remove |
| `physical_host_group_map_luns` | POST | `/rest/blockservice/v1/volumes/hostgroup-mapping` | hostgroup-mapping |
| `physical_host_group_unmap_luns` | POST | `/rest/blockservice/v1/volumes/hostgroup-unmapping` | hostgroup-unmapping |
| `physical_host_group_show_mapping_views` | POST | `/rest/blockservice/v1/volumes/mapping-view/query` | mapping-view |
| `show_related` | GET | `/rest/hostmgmt/v1/hostgroups/{hostgroup_id}/related-storage-hostgroups` | related-storage-hostgroups |
| `query_host_to_lun` | POST | `/rest/blockservice/v1/mapping-views/query_for_host_to_lun` | query_for_host_to_lun |

---

### 第 3 批：`nas.py`（61 个动作）

**文件**：`pydme/actions/nas.py`
**API 章节搜索关键词**：`/rest/fileservice/v1/` `/rest/kvcachemgmt/v1/` `/rest/dpc-mgmt/v1/`

| 动作名 | HTTP 方法 | URI 路径 | 对应 API 章节关键词 |
|--------|----------|----------|-------------------|
| `account_dataturbo_admin_list` | POST | `/rest/fileservice/v1/dpc-administrators/query` | dpc-administrators |
| `account_unix_user_create` | POST | `/rest/fileservice/v1/unix-users` | unix-users |
| `account_unix_user_add_group` | POST | `/rest/fileservice/v1/unix-users/{user_id}/add-secondary-group` | add-secondary-group |
| `account_unix_user_list` | POST | `/rest/fileservice/v1/unix-users/query` | unix-users |
| `account_unix_user_show` | GET | `/rest/fileservice/v1/unix-users/{id}` | unix-users |
| `account_unix_user_remove_group` | POST | `/rest/fileservice/v1/unix-users/{user_id}/remove-secondary-group` | remove-secondary-group |
| `account_unix_user_modify` | PUT | `/rest/fileservice/v1/unix-users/{id}` | unix-users |
| `account_unix_user_batch_delete` | POST | `/rest/fileservice/v1/unix-users/delete` | unix-users/delete |
| `account_unix_user_group_create` | POST | `/rest/fileservice/v1/unix-user-groups` | unix-user-groups |
| `account_unix_user_group_list` | POST | `/rest/fileservice/v1/unix-user-groups/query` | unix-user-groups |
| `account_unix_user_group_show` | GET | `/rest/fileservice/v1/unix-user-groups/{id}` | unix-user-groups |
| `account_unix_user_group_modify` | PUT | `/rest/fileservice/v1/unix-user-groups/{id}` | unix-user-groups |
| `account_unix_user_group_batch_delete` | POST | `/rest/fileservice/v1/unix-user-groups/delete` | unix-user-groups/delete |
| `dtree_list` | POST | `/rest/fileservice/v1/dtrees/query` | dtrees |
| `dtree_show` | GET | `/rest/fileservice/v1/dtrees/{dtree_id}` | dtrees |
| `dtree_create` | POST | `/rest/fileservice/v1/dtrees` | dtrees |
| `dtree_delete` | POST | `/rest/fileservice/v1/dtrees/delete` | dtrees/delete |
| `dtree_modify` | PUT | `/rest/fileservice/v1/dtrees/{dtree_id}` | dtrees |
| `nfs_share_list` | POST | `/rest/fileservice/v1/nfs-shares/query` | nfs-shares |
| `nfs_share_show` | GET | `/rest/fileservice/v1/nfs-shares/{nfs_share_id}` | nfs-shares |
| `nfs_share_create` | POST | `/rest/fileservice/v2/nfs-shares` | v2/nfs-shares |
| `nfs_share_modify` | PUT | `/rest/fileservice/v2/nfs-shares/{nfs_share_id}` | v2/nfs-shares |
| `nfs_share_delete` | POST | `/rest/fileservice/v1/nfs-shares/delete` | nfs-shares/delete |
| `nfs_share_show_clients` | POST | `/rest/fileservice/v2/nfs-auth-clients/query` | nfs-auth-clients |
| `cifs_share_list` | POST | `/rest/fileservice/v1/cifs-shares/query` | cifs-shares |
| `cifs_share_show` | GET | `/rest/fileservice/v1/cifs-shares/{cifs_share_id}` | cifs-shares |
| `cifs_share_create` | POST | `/rest/fileservice/v1/cifs-shares` | cifs-shares |
| `cifs_share_modify` | PUT | `/rest/fileservice/v1/cifs-shares/{cifs_share_id}` | cifs-shares |
| `cifs_share_delete` | POST | `/rest/fileservice/v1/cifs-shares/delete` | cifs-shares/delete |
| `cifs_share_show_permissions` | POST (多路) | `/rest/fileservice/v1/cifs-shares/{id}/auth-users/query` 等 | auth-users |
| `dataturbo_share_list` | POST | `/rest/fileservice/v1/dpc-shares/query` | dpc-shares |
| `dataturbo_share_show` | GET | `/rest/fileservice/v1/dpc-shares/{dataturbo_share_id}` | dpc-shares |
| `dataturbo_share_create` | POST | `/rest/fileservice/v1/dpc-shares` | dpc-shares |
| `dataturbo_share_modify` | PUT | `/rest/fileservice/v1/dpc-shares/{dataturbo_share_id}` | dpc-shares |
| `dataturbo_share_delete` | POST | `/rest/fileservice/v1/dpc-shares/delete` | dpc-shares/delete |
| `dataturbo_share_show_permissions` | POST | `/rest/fileservice/v1/dpc-shares/{id}/dpc-share-auths/query` | dpc-share-auths |
| `quota_list` | POST | `/rest/fileservice/v1/quotas/query` | quotas |
| `quota_show` | POST | `/rest/fileservice/v1/quotas/query` | quotas（带过滤参数） |
| `quota_create` | POST | `/rest/fileservice/v1/quotas` | quotas |
| `quota_modify` | PUT | `/rest/fileservice/v1/quotas/{quota_id}` | quotas |
| `quota_delete` | POST | `/rest/fileservice/v1/quotas/delete` | quotas/delete |
| `filesystem_list` | POST | `/rest/fileservice/v1/filesystems/query` | filesystems |
| `filesystem_show` | GET | `/rest/fileservice/v1/filesystems/{filesystem_id}` | filesystems |
| `filesystem_delete` | POST | `/rest/fileservice/v1/filesystems/delete` | filesystems/delete |
| `filesystem_batch_modify` | POST | `/rest/fileservice/v1/filesystems/modify` | filesystems/modify |
| `filesystem_create` | POST | `/rest/fileservice/v1/filesystems/customize-filesystems` | customize-filesystems |
| `filesystem_query_available` | POST | `/rest/fileservice/v1/filesystems/available-filesystems/query` | available-filesystems |
| `filesystem_modify` | PUT | `/rest/fileservice/v1/filesystems/{file_system_id}` | filesystems |
| `namespace_list` | POST | `/rest/fileservice/v1/namespaces/query` | namespaces |
| `namespace_show` | GET | `/rest/fileservice/v1/namespaces/{namespace_id}` | namespaces |
| `namespace_create` | POST | `/rest/fileservice/v1/namespaces` | namespaces |
| `namespace_modify` | PUT | `/rest/fileservice/v1/namespaces/{namespace_id}` | namespaces |
| `namespace_delete` | POST | `/rest/fileservice/v1/namespaces/delete` | namespaces/delete |
| `dpc_list` | POST | `/rest/dpc-mgmt/v1/dpcs/query` | dpcs |
| `dpc_show` | GET | `/rest/dpc-mgmt/v1/dpcs/{dpc_id}` | dpcs |
| `list` | POST | `/rest/fileservice/v1/dpc-clients/query` | dpc-clients |
| `show` | GET | `/rest/fileservice/v1/dpc-clients/{id}` | dpc-clients |
| `kvcache_list` | POST | `/rest/kvcachemgmt/v1/kv-cache-stores/query` | kv-cache-stores |
| `kvcache_batch_create` | POST | `/rest/kvcachemgmt/v1/kv-cache-stores` | kv-cache-stores |
| `kvcache_modify` | PUT | `/rest/kvcachemgmt/v1/kv-cache-stores/{kv_cache_stores_id}` | kv-cache-stores |
| `kvcache_batch_delete` | POST | `/rest/kvcachemgmt/v1/kv-cache-stores/delete` | kv-cache-stores/delete |

---

### 第 4 批：`storage.py`（62 个动作）

**文件**：`pydme/actions/storage.py`
**API 章节搜索关键词**：`/rest/storagemgmt/v1/` `/rest/storagemgmt/v2/` `/rest/blockservice/v1/` `/rest/fileservice/v1/` `/rest/hostmgmt/v1/` `/rest/storagepolicy/v1/`

| 动作名 | HTTP 方法 | URI 路径 | 对应 API 章节关键词 |
|--------|----------|----------|-------------------|
| `list` | GET | `/rest/storagemgmt/v1/storages` | storages |
| `show` | GET | `/rest/storagemgmt/v1/storages/{storage_id}/detail` | storages/detail |
| `add` | POST | `/rest/storagemgmt/v2/storages/offline-storages` | v2/storages |
| `remove` | POST | `/rest/storagemgmt/v2/storages/delete` | v2/storages/delete |
| `sync` | POST | `/rest/storagemgmt/v1/storages/refresh` | storages/refresh |
| `modify` | PUT | `/rest/storagemgmt/v2/storages/offline-storages/{storage_id}` | v2/storages |
| `bbu_list` | POST | `/rest/storagemgmt/v1/backup-powers/query` | backup-powers |
| `get_passphrase` | GET | `/rest/storagemgmt/v1/storages/{storage_id}/passphrase` | passphrase |
| `fan_list` | POST | `/rest/storagemgmt/v1/fans/query` | fans |
| `disk_list` | POST | `/rest/storagemgmt/v2/storages/{storage_id}/disk` | v2/disk |
| `pool_list` | POST | `/rest/storagemgmt/v1/storagepools/query` | storagepools |
| `hyperscale_pool_list` | POST | `/rest/storagemgmt/v1/hyperscale-pools/query` | hyperscale-pools |
| `node_list` | POST | `/rest/storagemgmt/v1/storage-nodes/query` | storage-nodes |
| `psu_list` | POST | `/rest/storagemgmt/v1/storage-powers/query` | storage-powers |
| `query_power_data` | POST | `/rest/metrics/v1/storage/power/query` | power/query |
| `app_type_list` | GET | `/rest/storagemgmt/v1/storages/{storage_id}/workloads` | workloads |
| `controller_list` | GET | `/rest/storagemgmt/v1/storages/{storage_id}/controllers` | controllers |
| `disk_domain_list` | POST | `/rest/storagemgmt/v1/disk-pools/query` | disk-pools |
| `disk_pool_list` | POST | `/rest/storagemgmt/v1/diskpools/query` | diskpools |
| `enclosure_list` | POST | `/rest/storagemgmt/v1/enclosures/query` | enclosures |
| `vstore_list` | POST | `/rest/fileservice/v1/vstores/query` | vstores |
| `vstore_show` | GET | `/rest/fileservice/v1/vstores/{id}` | vstores |
| `vstore_create` | POST | `/rest/fileservice/v1/vstores` | vstores |
| `vstore_modify` | PUT | `/rest/fileservice/v1/vstores/{id}` | vstores |
| `vstore_delete` | POST | `/rest/fileservice/v1/vstores/delete` | vstores/delete |
| `initiator_list` | POST | `/rest/hostmgmt/v1/storage-initiators/query` | storage-initiators |
| `initiator_delete` | POST | `/rest/hostmgmt/v1/storage-initiators/delete` | storage-initiators/delete |
| `initiator_modify` | PUT | `/rest/hostmgmt/v1/storage-initiators/{initiator_id}` | storage-initiators |
| `account_show_local_users` | POST | `/rest/fileservice/v1/storages/{storage_id}/local-users/query` | local-users |
| `account_create_local_user` | POST | `/rest/fileservice/v1/storages/{storage_id}/local-users` | local-users |
| `account_create_unix_user` | POST | `/rest/fileservice/v1/storages/{storage_id}/unix-users` | unix-users |
| `account_create_windows_user` | POST | `/rest/fileservice/v1/storages/{storage_id}/windows-users` | windows-users |
| `account_show_unix_users` | POST | `/rest/fileservice/v1/storages/{storage_id}/unix-users/query` | unix-users/query |
| `account_show_windows_users` | POST | `/rest/fileservice/v1/storages/{storage_id}/windows-users/query` | windows-users/query |
| `account_show_local_user_groups` | POST | `/rest/fileservice/v1/storages/{storage_id}/local-user-groups/query` | local-user-groups |
| `account_show_unix_user_groups` | POST | `/rest/fileservice/v1/storages/{storage_id}/unix-user-groups/query` | unix-user-groups |
| `account_show_windows_user_groups` | POST | `/rest/fileservice/v1/storages/{storage_id}/windows-user-groups/query` | windows-user-groups |
| `qos_list` | POST | `/rest/storagepolicy/v1/qos/query` | qos |
| `qos_show` | GET | `/rest/storagepolicy/v1/qos/{qos_policy_id}/detail` | qos/detail |
| `qos_create` | POST | `/rest/storagepolicy/v1/qos` | qos |
| `qos_modify` | PUT | `/rest/storagepolicy/v1/qos/{qos_policy_id}` | qos |
| `qos_delete` | POST | `/rest/storagepolicy/v1/qos/delete` | qos/delete |
| `qos_activate` | POST | `/rest/storagepolicy/v1/qos/active` | qos/active |
| `qos_deactivate` | POST | `/rest/storagepolicy/v1/qos/inactive` | qos/inactive |
| `qos_associate` | POST | `/rest/storagepolicy/v1/qos/{qos_policy_id}/resources/associate` | resources/associate |
| `qos_unassociate` | POST | `/rest/storagepolicy/v1/qos/{qos_policy_id}/resources/unassociate` | resources/unassociate |
| `logic_port_list` | POST | `/rest/storagemgmt/v2/logic-ports/query` | v2/logic-ports |
| `logic_port_show` | GET | `/rest/storagemgmt/v1/logic-ports/{logic_port_id}` | logic-ports |
| `logic_port_create` | POST | `/rest/storagemgmt/v1/logic-ports` | logic-ports |
| `logic_port_update` | PUT | `/rest/storagemgmt/v1/logic-ports/{logic_port_id}` | logic-ports |
| `logic_port_delete` | POST | `/rest/storagemgmt/v1/logic-ports/delete` | logic-ports/delete |
| `logic_port_failback` | POST | `/rest/storagemgmt/v1/logic-ports/failback` | failback |
| `port_list` | POST (多路) | `/rest/storagemgmt/v1/storages/eth-ports/query` 等 (eth/bond/fc/ib/sas) | ports |
| `port_show_bond_members` | GET | `/rest/storagemgmt/v1/bond-ports/{bond_port_id}/eth-ports` | bond-ports |
| `vlan_list` | POST | `/rest/vlanmgmt/v1/vlans/query` | vlans |
| `vlan_create` | POST | `/rest/vlanmgmt/v1/vlans` | vlans |
| `vlan_delete` | DELETE | `/rest/vlanmgmt/v1/vlans/{vlan_id}` | vlans |
| `vlan_modify` | PUT | `/rest/vlanmgmt/v1/vlans/{vlan_id}` | vlans |
| `failover_group_list` | POST | `/rest/storagemgmt/v1/failover-groups/query` | failover-groups |
| `failover_group_show_ports` | GET (多路) | `/rest/storagemgmt/v1/failover-groups/{id}/bond-ports` 等 | failover-groups/ports |
| `failover_group_show_vlans` | GET | `/rest/storagemgmt/v1/failover-groups/{failover_group_id}/vlans` | failover-groups/vlans |
| `zone_list` | POST | `/rest/storageclusterservice/v1/zones/query` | zones |

---

### 第 5 批：`system.py`（40 个动作）

**文件**：`pydme/actions/system.py`
**API 章节搜索关键词**：`/rest/usermgmt/v1/` `/rest/taskmgmt/v1/` `/rest/tagmgmt/v1/` `/rest/azmgmt/v1/` `/rest/dcmgmt/v1/` `/rest/regionmgmt/v1/`

| 动作名 | HTTP 方法 | URI 路径 | 对应 API 章节关键词 |
|--------|----------|----------|-------------------|
| `login` | POST (隐式) | 调用 `client.login()` | sessions |
| `logout` | DELETE | `/rest/plat/smapp/v1/sessions` | sessions |
| `reset_password` | PUT | `/rest/usm/v1/users/{user_name}/reset-credentials` | reset-credentials |
| `user_delete` | DELETE | `/rest/usermgmt/v1/users/{user_id}` | users |
| `user_create` | POST | `/rest/usermgmt/v1/users` | users |
| `user_list` | GET | `/rest/usermgmt/v1/users` | users |
| `user_show` | GET | `/rest/usermgmt/v1/users/{user_id}` | users |
| `role_list` | GET | `/rest/usermgmt/v1/roles` | roles |
| `show` | GET | `/rest/productmgmt/v1/system-info` | system-info |
| `certificate` | GET | `/rest/certmgmt/v1/certs` | certs |
| `backup_server_list` | GET | `/rest/configmgmt/v1/backup-servers` | backup-servers |
| `todo_task_group_list` | GET | `/rest/taskmgmt/v1/todo-groups` | todo-groups |
| `todo_task_group_execute` | PUT | `/rest/taskmgmt/v1/todo-groups/{group_id}/execute` | todo-groups/execute |
| `todo_task_group_confirm` | PUT | `/rest/taskmgmt/v1/todo-groups/{group_id}/confirm` | todo-groups/confirm |
| `todo_task_list` | POST | `/rest/taskmgmt/v1/todo-items/query` | todo-items |
| `todo_task_show` | GET | `/rest/taskmgmt/v1/todo-items/{item_id}` | todo-items |
| `todo_task_execute` | PUT | `/rest/taskmgmt/v1/todo-items/{item_id}/execute` | todo-items/execute |
| `todo_task_audit` | POST | `/rest/taskmgmt/v1/todo-items/{item_id}/audit` | todo-items/audit |
| `todo_task_revoke` | PUT | `/rest/taskmgmt/v1/todo-items/{item_id}/revoke-audit` | revoke-audit |
| `todo_task_close` | PUT | `/rest/taskmgmt/v1/todo-items/{item_id}/close` | todo-items/close |
| `task_show` | GET | `/rest/taskmgmt/v1/tasks/{task_id}` | tasks |
| `task_list` | GET | `/rest/taskmgmt/v1/tasks` | tasks |
| `task_retry` | POST | `/rest/taskmgmt/v1/tasks/{task_id}/retry` | tasks/retry |
| `task_wait` | 轮询 | 调用 `client.get_task_result()` | — |
| `tag_type_create` | POST | `/rest/tagmgmt/v1/tag-types` | tag-types |
| `tag_type_list` | POST | `/rest/tagmgmt/v1/tag-types/query` | tag-types |
| `tag_type_modify` | PUT | `/rest/tagmgmt/v1/tag-types/{tag_type_id}` | tag-types |
| `tag_type_delete` | POST | `/rest/tagmgmt/v1/tag-types/delete` | tag-types/delete |
| `tag_create` | POST | `/rest/tagmgmt/v1/tags` | tags |
| `tag_list` | POST | `/rest/tagmgmt/v1/tags/query` | tags |
| `tag_modify` | PUT | `/rest/tagmgmt/v1/tags/{tag_id}` | tags |
| `tag_delete` | POST | `/rest/tagmgmt/v1/tags/delete` | tags/delete |
| `tag_bind` | POST | `/rest/tagmgmt/v1/tags/{tag_id}/resources/bind` | resources/bind |
| `tag_unbind` | POST | `/rest/tagmgmt/v1/tags/{tag_id}/resources/unbind` | resources/unbind |
| `az_list` | GET | `/rest/azmgmt/v1/availability-zones` | availability-zones |
| `dc_list` | POST | `/rest/dcmgmt/v1/data-centers` | data-centers |
| `dc_show` | GET | `/rest/dcmgmt/v1/data-centers/{dc_id}` | data-centers |
| `dc_show_devices` | POST | `/rest/dcmgmt/v1/data-centers/{dc_id}/device-list` | device-list |
| `region_list` | POST | `/rest/regionmgmt/v1/regions` | regions |
| `region_query` | POST | `/rest/regionmgmt/v1/regions/{region_id}/action/query` | regions/query |

---

### 第 6 批：`aiops.py`（26 个动作）

**文件**：`pydme/actions/aiops.py`
**API 章节搜索关键词**：`/rest/alarmmgmt/v1/` `/rest/diagnosis/v1/` `/rest/pmmgmt/v1/` `/rest/metrics/v1/` `/rest/policymgmt/v1/` `/rest/topomgmt/v1/` `/rest/healthmgmt/v1/`

| 动作名 | HTTP 方法 | URI 路径 | 对应 API 章节关键词 |
|--------|----------|----------|-------------------|
| `alarm_list` | POST | `/rest/alarmmgmt/v1/alarms/current-alarm/query` (current) / `.../history-alarms/query` (history) | alarms |
| `alarm_ack` | POST | `/rest/alarmmgmt/v1/alarms/operation` (`operation_type: "ACK"`) | alarms/operation |
| `alarm_unack` | POST | `/rest/alarmmgmt/v1/alarms/operation` (`operation_type: "UNACK"`) | alarms/operation |
| `alarm_clear` | POST | `/rest/alarmmgmt/v1/alarms/operation` (`operation_type: "CLEAR"`) | alarms/operation |
| `diagnose_task_create` | POST | `/rest/diagnosis/v1/tasks` | diagnosis/tasks |
| `diagnose_task_status` | POST | `/rest/dmegraphanalysis/v1/perf-tasks/query-status` | perf-tasks |
| `performance_create_collect_task` | POST | `/rest/pmmgmt/v1/performance-data/collection-task` | collection-task |
| `performance_download_collect_result` | GET | `/rest/pmmgmt/v1/performance-data/download/{task_id}` | download |
| `performance_query` | POST | `/rest/metrics/v1/data-svc/history-data/action/query` | history-data |
| `performance_show_indicators` | POST | `/rest/metrics/v1/mgr-svc/indicators` | indicators |
| `performance_list_indicators` | GET | `/rest/metrics/v1/mgr-svc/obj-types/{obj_type_id}/indicators` | obj-types/indicators |
| `performance_list_object_types` | GET | `/rest/metrics/v1/mgr-svc/obj-types` | obj-types |
| `check_result_list` | POST | `/rest/policymgmt/v1/abnormal-check-results/query` | check-results |
| `check_result_show` | GET | `/rest/policymgmt/v1/abnormal-check-results/{check_result_id}` | check-results |
| `check_policy_list` | POST | `/rest/policymgmt/v2/policies/query` | v2/policies |
| `check_policy_execute` | POST | `/rest/policymgmt/v1/policies/{policy_id}/execute` | policies/execute |
| `check_policy_enable` | POST | `/rest/policymgmt/v1/policies/{policy_id}/enable` | policies/enable |
| `check_policy_disable` | POST | `/rest/policymgmt/v1/policies/{policy_id}/disable` | policies/disable |
| `check_policy_delete` | DELETE | `/rest/policymgmt/v1/policies/{policy_id}` | policies |
| `topology_query_luns` | POST | `/rest/topomgmt/v1/topo-data/luns/query` | topo-data/luns |
| `topology_query_san_path` | POST | `/rest/topomgmt/v1/topo-data/ipsan/host-storage/query` (ip) / `.../host-storage/query` (fc) | topo-data/host-storage |
| `topology_query_vms` | POST | `/rest/topomgmt/v1/topo-data/vms/query` | topo-data/vms |
| `topology_query_graph_path` | POST | `/rest/dmegraphanalysis/v1/topo-data/query` | topo-data/query |
| `health_query_data` | POST | `/rest/pmmgmt/v1/prediction/query-capacity-predict` 等 (3 路由) | prediction |
| `health_show_score` | POST | `/rest/healthmgmt/v1/health-result/query` | health-result |
| `health_show_detail` | POST | `/rest/healthmgmt/v1/health-result/dimension-score/query` | dimension-score |

---

### 第 7 批：`fcswitch.py` + `gfs.py`（19 + 14 = 33 个动作）

#### `fcswitch.py`（19 个动作）

**文件**：`pydme/actions/fcswitch.py`
**API 章节搜索关键词**：`/rest/fcswitchmgmt/v1/`

| 动作名 | HTTP 方法 | URI 路径 | 对应 API 章节关键词 |
|--------|----------|----------|-------------------|
| `list` | POST | `/rest/fcswitchmgmt/v1/fcswitches/list` | fcswitches |
| `sync` | POST | `/rest/fcswitchmgmt/v1/fcswitches/{switch_id}/sync` | fcswitches/sync |
| `port_list` | POST | `/rest/fcswitchmgmt/v1/fcswitches/ports/query` | ports |
| `controller_list` | POST | `/rest/fcswitchmgmt/v1/fcswitches/controllers/query` | controllers |
| `fabric_list` | POST | `/rest/fcswitchmgmt/v1/fabrics/list` | fabrics |
| `fabric_show_ports` | POST | `/rest/fcswitchmgmt/v1/fabrics/{fabric_id}/ports/list` | fabrics/ports |
| `fabric_backup` | POST | `/rest/fcswitchmgmt/v1/fabrics/{fabric_id}/backup` | fabrics/backup |
| `vsan_list` | POST | `/rest/fcswitchmgmt/v1/vsans/query` | vsans |
| `zone_list` | POST | `/rest/fcswitchmgmt/v1/zones/list` | zones |
| `zone_create` | POST | `/rest/fcswitchmgmt/v1/zones` | zones |
| `zone_modify` | PUT | `/rest/fcswitchmgmt/v1/zones/{zone_id}` | zones |
| `zone_delete` | DELETE | `/rest/fcswitchmgmt/v1/zones/{zone_id}` | zones |
| `zone_batch_create` | POST | `/rest/fcswitchmgmt/v1/zones/batch-create` | batch-create |
| `zone_show_members` | POST/GET (多路) | `/rest/fcswitchmgmt/v1/zones/{zone_id}/port-members/list` 等 | zone-members |
| `alias_list` | POST | `/rest/fcswitchmgmt/v1/aliases/list` | aliases |
| `alias_create` | POST | `/rest/fcswitchmgmt/v1/aliases` | aliases |
| `alias_modify` | PUT | `/rest/fcswitchmgmt/v1/aliases/{alias_id}` | aliases |
| `alias_delete` | DELETE | `/rest/fcswitchmgmt/v1/aliases/{alias_id}` | aliases |
| `alias_show_members` | POST/GET (多路) | `/rest/fcswitchmgmt/v1/aliases/{alias_id}/port-members/list` 等 | alias-members |

#### `gfs.py`（14 个动作）

**文件**：`pydme/actions/gfs.py`
**API 章节搜索关键词**：`/rest/fileservice/v1/gfs` `/rest/fileservice/v1/gfs-groups/` `/rest/fileservice/v1/data-service-sites/`

| 动作名 | HTTP 方法 | URI 路径 | 对应 API 章节关键词 |
|--------|----------|----------|-------------------|
| `dataspace_list` | POST | `/rest/fileservice/v1/gfs-groups/query` | gfs-groups |
| `dataspace_show` | POST | `/rest/fileservice/v1/gfs-groups/query-summary` | gfs-groups/summary |
| `dataspace_site_list` | POST | `/rest/fileservice/v1/data-service-sites/query` | data-service-sites |
| `namespace_list` | POST | `/rest/fileservice/v1/gfs/query` | gfs |
| `namespace_show` | POST | `/rest/fileservice/v1/gfs/detail/query` | gfs/detail |
| `namespace_create` | POST | `/rest/fileservice/v1/gfs` | gfs |
| `namespace_modify` | POST | `/rest/fileservice/v1/gfs/modify` | gfs/modify |
| `namespace_delete` | POST | `/rest/fileservice/v1/gfs/delete` | gfs/delete |
| `migration_task_list` | POST | `/rest/fileservice/v1/gfs/migration-tasks/query` | migration-tasks |
| `migration_task_show` | GET | `/rest/fileservice/v1/gfs/migration-tasks/{id}` | migration-tasks |
| `migration_task_create` | POST | `/rest/fileservice/v1/gfs/migration-tasks` | migration-tasks |
| `migration_task_modify` | PUT | `/rest/fileservice/v1/gfs/migration-tasks/{id}` | migration-tasks |
| `migration_task_delete` | POST | `/rest/fileservice/v1/gfs/migration-tasks/delete` | migration-tasks/delete |
| `migration_task_operate` | POST | `/rest/fileservice/v1/gfs/migration-tasks/operate` | migration-tasks/operate |

---

### 第 8 批：`virt.py` + `server.py` + `tenant.py`（14 + 10 + 10 = 34 个动作）

#### `virt.py`（14 个动作）

**文件**：`pydme/actions/virt.py`
**API 章节搜索关键词**：`/rest/vmmgmt/v1/`

| 动作名 | HTTP 方法 | URI 路径 | 对应 API 章节关键词 |
|--------|----------|----------|-------------------|
| `vm_list` | POST | `/rest/vmmgmt/v1/vms/query` | vms |
| `vm_show` | GET | `/rest/vmmgmt/v1/vms/{vm_id}` | vms |
| `datastore_list` | POST | `/rest/vmmgmt/v1/datastores/query` | datastores |
| `datastore_show` | GET | `/rest/vmmgmt/v1/datastores/{datastore_id}` | datastores |
| `host_list` | POST | `/rest/vmmgmt/v1/hosts/query` | vmmgmt/hosts |
| `host_show` | GET | `/rest/vmmgmt/v1/hosts/{host_id}` | vmmgmt/hosts |
| `cluster_list` | POST | `/rest/vmmgmt/v1/clusters/query` | vmmgmt/clusters |
| `cluster_show` | GET | `/rest/vmmgmt/v1/clusters/{cluster_id}` | vmmgmt/clusters |
| `site_list` | POST | `/rest/vmmgmt/v1/sites/query` | sites |
| `site_show` | GET | `/rest/vmmgmt/v1/sites/{site_id}` | sites |
| `host_adapter_list` | GET | `/rest/vmmgmt/v1/hosts/{host_id}/storage-adapters` | storage-adapters |
| `disk_list` | POST | `/rest/vmmgmt/v1/vdisks/pdisks` | pdisks |
| `vdisk_list` | POST | `/rest/vmmgmt/v1/vdisks/query` | vdisks |
| `vdisk_show` | GET | `/rest/vmmgmt/v1/vdisks/{virtual_disk_id}` | vdisks |

#### `server.py`（10 个动作）

**文件**：`pydme/actions/server.py`
**API 章节搜索关键词**：`/rest/servermgmt/v1/`

| 动作名 | HTTP 方法 | URI 路径 | 对应 API 章节关键词 |
|--------|----------|----------|-------------------|
| `list` | POST | `/rest/servermgmt/v1/servers/query` | servers |
| `show` | GET | `/rest/servermgmt/v1/servers/{server_id}/summary` | servers/summary |
| `cpu_list` | POST | `/rest/servermgmt/v1/processors/query` | processors |
| `memory_list` | POST | `/rest/servermgmt/v1/memories/query` | memories |
| `disk_list` | POST | `/rest/servermgmt/v1/disks/query` | servermgmt/disks |
| `nic_list` | POST | `/rest/servermgmt/v1/network-adapters/query` | network-adapters |
| `fan_list` | POST | `/rest/servermgmt/v1/fans/query` | servermgmt/fans |
| `power_list` | POST | `/rest/servermgmt/v1/powers/query` | servermgmt/powers |
| `raid_card_list` | POST | `/rest/servermgmt/v1/raid-cards/query` | raid-cards |
| `pcie_card_list` | POST | `/rest/servermgmt/v1/pcies/query` | pcies |

#### `tenant.py`（10 个动作）

**文件**：`pydme/actions/tenant.py`
**API 章节搜索关键词**：`/rest/blockservice/v1/volumes` `/rest/service-policy/v1/` `/rest/projectmgmt/v1/`

| 动作名 | HTTP 方法 | URI 路径 | 对应 API 章节关键词 |
|--------|----------|----------|-------------------|
| `lun_create` | POST | `/rest/blockservice/v1/volumes` | tenant/volumes |
| `lun_change_tier` | POST | `/rest/blockservice/v1/volumes/update-service-level` | update-service-level |
| `lun_bind_tier` | POST | `/rest/blockservice/v1/volumes/add-to-service-level` | add-to-service-level |
| `lun_unbind_tier` | POST | `/rest/blockservice/v1/volumes/remove-service-level` | remove-service-level |
| `lun_bind_project` | PUT | `/rest/blockservice/v1/projects/{business_group_id}/volumes/bound` | volumes/bound |
| `lun_unbind_project` | PUT | `/rest/blockservice/v1/projects/{business_group_id}/volumes/unbound` | volumes/unbound |
| `tier_list` | GET | `/rest/service-policy/v1/service-levels` | service-levels |
| `tier_show_projects` | GET | `/rest/service-policy/v1/service-levels/projects/relations` | projects/relations |
| `project_list` | GET | `/rest/projectmgmt/v1/projects` | projects |
| `project_show_tiers` | GET | `/rest/service-policy/v1/service-levels/projects/relations` | projects/relations |

---

### 第 9 批：`ipswitch.py` + `workflow.py` + `kube.py`（7 + 7 + 6 = 20 个动作）

#### `ipswitch.py`（7 个动作）

**文件**：`pydme/actions/ipswitch.py`
**API 章节搜索关键词**：`/rest/switchmgmt/`

| 动作名 | HTTP 方法 | URI 路径 | 对应 API 章节关键词 |
|--------|----------|----------|-------------------|
| `list` | POST | `/rest/switchmgmt/v1/switchs/query` | switchs |
| `frame_list` | POST | `/rest/switchmgmt/switchmgmtservice/v1/switchs/frames/query` | frames |
| `board_list` | POST | `/rest/switchmgmt/switchmgmtservice/v1/switchs/boards/query` | boards |
| `subcard_list` | POST | `/rest/switchmgmt/switchmgmtservice/v1/switchs/subcards/query` | subcards |
| `power_list` | POST | `/rest/switchmgmt/switchmgmtservice/v1/switchs/powers/query` | powers |
| `fan_list` | POST | `/rest/switchmgmt/switchmgmtservice/v1/switchs/fans/query` | fans |
| `port_list` | POST | `/rest/switchmgmt/switchmgmtservice/v1/switchs/ports/query` | ports |

#### `workflow.py`（7 个动作）

**文件**：`pydme/actions/workflow.py`
**API 章节搜索关键词**：`/rest/wfamgmt/v1/workflow/`

| 动作名 | HTTP 方法 | URI 路径 | 对应 API 章节关键词 |
|--------|----------|----------|-------------------|
| `template_list` | POST | `/rest/wfamgmt/v1/workflow/templates/query` | templates |
| `template_groups` | POST | `/rest/wfamgmt/v1/workflow/templates/groups/query` | templates/groups |
| `template_show` | GET | `/rest/wfamgmt/v1/workflow/templates/{template_id}` | templates |
| `instance_stop` | POST | `/rest/wfamgmt/v1/workflow/instances/{instance_id}/stop` | instances/stop |
| `instance_show` | GET | `/rest/wfamgmt/v1/workflow/instances/{instance_id}` | instances |
| `instance_create` | POST | `/rest/wfamgmt/v1/workflow/instances` | instances |
| `instance_step_log` | GET | `/rest/wfamgmt/v1/workflow/instances/{instance_id}/steps/{step_id}/log` | steps/log |

#### `kube.py`（6 个动作）

**文件**：`pydme/actions/kube.py`
**API 章节搜索关键词**：`/rest/dmecaasmgmt/v1/`

| 动作名 | HTTP 方法 | URI 路径 | 对应 API 章节关键词 |
|--------|----------|----------|-------------------|
| `cluster_list` | POST | `/rest/dmecaasmgmt/v1/clusters/query-list` | clusters |
| `node_list` | POST | `/rest/dmecaasmgmt/v1/nodes/query-list` | nodes |
| `pod_list` | POST | `/rest/dmecaasmgmt/v1/pods/query-list` | pods |
| `namespace_list` | POST | `/rest/dmecaasmgmt/v1/namespaces/query-list` | namespaces |
| `pvc_list` | POST | `/rest/dmecaasmgmt/v1/pvcs/query-list` | pvcs |
| `pv_list` | POST | `/rest/dmecaasmgmt/v1/pvs/query-list` | pvs |

---

### 第 10 批：`integrate.py` + `backup.py`（5 + 3 = 8 个动作）

#### `integrate.py`（5 个动作）

**文件**：`pydme/actions/integrate.py`
**API 章节搜索关键词**：`/rest/appmgmt/v1/`

| 动作名 | HTTP 方法 | URI 路径 | 对应 API 章节关键词 |
|--------|----------|----------|-------------------|
| `cmdb_system_list` | POST | `/rest/appmgmt/v1/cmdb-systems/query` | cmdb-systems |
| `cmdb_host_list` | POST | `/rest/appmgmt/v1/cmdb-hosts/query` | cmdb-hosts |
| `cmdb_host_show` | GET | `/rest/appmgmt/v1/cmdb-hosts/{cmdb_host_id}` | cmdb-hosts |
| `cmdb_app_list` | POST | `/rest/appmgmt/v1/applications/query` | applications |
| `cmdb_host_query_by_initiators` | POST | `/rest/appmgmt/v1/cmdb-hosts/query-by-initiators` | query-by-initiators |

#### `backup.py`（3 个动作）

**文件**：`pydme/actions/backup.py`
**API 章节搜索关键词**：`/rest/dmebackupsoftmgmtservice/v1/`

| 动作名 | HTTP 方法 | URI 路径 | 对应 API 章节关键词 |
|--------|----------|----------|-------------------|
| `cluster_list` | POST | `/rest/dmebackupsoftmgmtservice/v1/clusters/query` | clusters |
| `cluster_capacity` | GET | `/rest/dmebackupsoftmgmtservice/v1/clusters/{cluster_id}/capacity` | capacity |
| `cluster_quota` | POST | `/rest/dmebackupsoftmgmtservice/v1/clusters/{cluster_id}/tenant-quotas/query` | tenant-quotas |

---

## 常见问题修复速查表

| 症状 | 根因 | 修复方法 |
|------|------|---------|
| `--help` 出现预期外的 `--name`、`--type` 等参数 | `格式：{` 泄露内部字段 | 将 `格式：{` → `参数格式如下：{` |
| `--help` 缺少应有参数 | docstring 未定义该参数 | 补充参数定义 |
| Returns 显示纯文字但 API 返回复杂结构 | 未按 JSON 格式编写 | 参考 API 文档编写结构化 Returns |
| 嵌套对象显示不完整（如只列了 id/name） | 引用对象未展开 | 按 `属性格式如下：{` 展开 |
| 动作描述过于简略（如"查询XXX"无细分） | 未参考 API 功能描述 | 将 API 参考中的"描述"段内容提炼为动作描述 |
| 字段约束与 API 参考不匹配 | docstring 写错 | 对照 API 参考修正 `(约束)` |
| 枚举值不全 | docstring 枚举列表不完整 | 补充缺失枚举值 |

## 执行的辅助脚本

如需批量提取当前 help 输出进行分析，可使用：

```bash
# 列出所有 topic 及其动作数
pydme --list-topics

# 查看单 topic 下所有动作
pydme <topic> --help

# 查看单个动作的参数帮助（含参数名/类型/约束/枚举）
pydme <topic> <action> --help
```

## 统计

| 指标 | 数值 |
|------|------|
| 总动作数 | 425 |
| 总函数数 | 429 |
| API 参考文档大小 | 1.7 MB（225 引用对象类型） |
| 批次数 | 10（按 topic 文件分批） |
| 每批预计工作量 | 8~75 个动作/批 |

## 执行顺序

1. 按 1→10 批顺序执行
2. 每批先提交子计划获取批准
3. 每批完成后提交 commit（如 `docs(protect): 校验并修复 Returns 和参数格式`）
4. 每次运行 `pydme <topic> <action> --help` 前，确保环境变量 `DME_API_*` 已配置（或使用 `--endpoint` 等参数）—— help 信息来自 docstring 解析，不依赖实际 API 连通性
