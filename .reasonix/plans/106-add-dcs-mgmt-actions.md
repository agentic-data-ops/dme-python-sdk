# 计划 106：新增 DCS 管理动作 —— hci topic（5 actions）+ virt topic 扩展（44 actions），含 blacklist / README / REASONIX 同步

## 概述

参考 `.reasonix/reference/dme-api-reference.md`（以下称 API 参考）最新更新，为 dme-python-sdk 补充 **49 个新动作**：

- 新建 **`hci` topic**（`pydme/actions/hci.py`，5 个 direct actions）：超融合（Hyper Converged Infrastructure）列表/详情/虚拟集群/虚拟交换机/存储设备查询；
- **`virt` topic 扩展 44 个动作**：datastore/host/vdisk/vm/vswitch/secgroup/gpu 子主题的创建、删除、修改、电源、迁移、快照、网卡、端口组等管理操作。

每个动作包含：动作函数代码（`pydme/actions/*.py`）+ 注册条目（`actions_zh_CN.yaml` / `actions_en_US.yaml`）+ 中英文 docstring（`funcs_zh_CN.yaml` / `funcs_en_US.yaml`）。随后：将删除/修改/变更/重启/关机/恢复等高危动作刷新进 `pydme/config/blacklist.json`；遍历全部新增动作 `--help` 与 API 参考交叉验证；同步更新 `README.md` / `README_zh.md` 与 `REASONIX.md`。

**不在范围**：真实网络 E2E 执行（无 DME 环境，新增动作仅做静态 help/参数验证）；`dme-mcp-server` / `dme-skills` 仓库。

## 背景与现状（已核实）

- `pydme/actions/` 现有 **16 个模块、427 个动作**；`virt.py`（275 行）现有 14 个查询类动作（vm/datastore/host/cluster/site/disk/vdisk 的 list/show 类），**无 hci.py**。
- 动作注册表权威源是 `pydme/config/i18n/actions_<lang>.yaml`（105 计划产物）；`pydme/i18n.py` 的 `load_actions_registry()` 自动从 YAML 构建注册表、`_resolve_func` 用 `getattr(import_module(topic), func)` 解析函数 → **新增动作只需：① 模块加函数 ② YAML 加注册条目 ③ funcs YAML 加 docstring，无需改 cli.py**。
- 短名规则（`cli.py get_available_topics`）：direct action 用 action_key 原样；subtopic action 剥离 `<subtopic>_` 前缀。故 `virt` 新条目在 YAML 中 `name` 用短名（如 `nic_list`），`func` 用 `vm_nic_list`，注册表重建 key 为 `vm_nic_list`。
- 黑名单 `pydme/config/blacklist.json`：`{topic: [完整 action_key 列表]}`，当前 **10 topics、122 个 key**，无 `virt` / `hci` 条目；匹配逻辑见 `cli.py _check_risk(topic, action_key)`（action_key 为去 topic 前缀的完整 key，如 `lun_delete`）。用户覆盖文件 `~/.config/pydme/blacklist.json` 存在时优先（包内默认文件仍须更新）。
- docstring 约定（REASONIX.md）：`funcs_<lang>.yaml` 的 key 为 `<topic>.<func>`；`Args:` 每参数一行 `param: desc (约束)。可选值：enum (desc), …`；`Returns:` 下一行以 `{` 开头（JSON 风格）；**行内嵌套字段必须用 `参数格式如下：[{` / `属性格式如下：{` 标记**，裸 `格式：{` 会导致嵌套字段泄漏为 CLI 参数；所有字段行以 `,` 结尾。函数签名参数名与 YAML `params` 数组、docstring `Args:` 一一对应。
- API 参考已包含全部 49 个目标 API（危险级别均为 Minor，含请求/响应字段详表），文档行号见下节清单。
- README 需更新点：`Project Structure`（"one file per topic, 427 actions" 注释 + 模块列表）、`Available topics` 表（总数 427→476、`virt` 14→58、新增 `hci` 5）、`Covered Risk Actions` 表（10 topics 122 → 含 `virt` 新行）；`README_zh.md` 同步。REASONIX.md 需更新点：16→17 topic modules、427→476、blacklist 122→新值、E2E 覆盖行（新增 49 个无 E2E，静态 help 验证）。
- 现有工具：`.reasonix/scripts/00-lib.sh`（`exec_test` 执行记录）、`gen_actions_i18n.py`（105 一次性生成脚本，YAML 现为手工维护权威源，不依赖它）、`check_prose.py`（文案检查）。

## 新增动作清单（49 个，API 参考行号已核实）

### hci（新 topic，5 个 direct actions；无 subtopic）

| action | func | API | 文档行 |
|--------|------|-----|--------|
| list | list | POST /rest/hcimgmt/v1/hcis/query | 33667 |
| show | show | GET /rest/hcimgmt/v1/hcis/{hci_id} | 33736 |
| cluster_list | cluster_list | POST /rest/vmmgmt/v1/hci-vm-clusters/query | 33805 |
| vswitch_list | vswitch_list | POST /rest/vmmgmt/v1/hci-dvswitchs/query | 33874 |
| storage_list | storage_list | POST /rest/storagemgmt/v2/hci-storages/query | 33929 |

### virt 扩展（44 个，按 subtopic 分组；YAML 短名 = action 列，func 带前缀）

| subtopic | action | func | API | 文档行 |
|----------|--------|------|-----|--------|
| datastore | host_relations | datastore_host_relations | POST /rest/vmmgmt/v1/datastores/datastore-host-relations/query | 31291 |
| host | port_list | host_port_list | GET /rest/vmmgmt/v1/hosts/{id}/ports | 30633 |
| host | aggr_port_list | host_aggr_port_list | GET /rest/vmmgmt/v1/hosts/{id}/uplink-port-aggrs | 30689 |
| host | logic_port_list | host_logic_port_list | GET /rest/vmmgmt/v1/hosts/{id}/system-intfs | 30734 |
| vdisk | create_attach | vdisk_create_attach | POST /rest/vmmgmt/v2/vms/{id}/vdisk/create-and-attach | 32752 |
| vdisk | attach | vdisk_attach | POST /rest/vmmgmt/v1/vms/{id}/vdisk/attach | 32852 |
| vdisk | detach | vdisk_detach | POST /rest/vmmgmt/v1/vms/{id}/vdisk/detach | 32973 |
| vdisk | modify | vdisk_modify | PUT /rest/vmmgmt/v1/vdisks/{id} | 32894 |
| vdisk | expand | vdisk_expand | POST /rest/vmmgmt/v1/vms/{id}/vdisk/expand | 32933 |
| vdisk | delete | vdisk_delete | DELETE /rest/vmmgmt/v1/vdisks/{id} | 33012 |
| vm | create | vm_create | POST /rest/vmmgmt/v1/vms | 32477 |
| vm | clone | vm_clone | POST /rest/vmmgmt/v1/vms/{id}/clone | （见 vms/{id}/clone） |
| vm | modify | vm_modify | PUT /rest/vmmgmt/v1/vms/{id} | 32604 附近 |
| vm | power_on | vm_power_on | POST /rest/vmmgmt/v1/vms/batch-power-on | 31813 |
| vm | power_off | vm_power_off | POST /rest/vmmgmt/v1/vms/batch-power-off | 31850 |
| vm | hibernate | vm_hibernate | POST /rest/vmmgmt/v1/vms/batch-hibernate | 31888 |
| vm | reboot | vm_reboot | POST /rest/vmmgmt/v1/vms/batch-reboot | 31925 |
| vm | delete | vm_delete | POST /rest/vmmgmt/v1/vms/batch-delete | 31963 |
| vm | vnc_info | vm_vnc_info | GET /rest/vmmgmt/v1/vms/{id}/vnc | （vnc） |
| vm | mount_tools | vm_mount_tools | POST /rest/vmmgmt/v1/vms/{id}/install-tools | 32042 |
| vm | umount_tools | vm_umount_tools | POST /rest/vmmgmt/v1/vms/{id}/uninstall-tools | 32079 |
| vm | migrate | vm_migrate | POST /rest/vmmgmt/v1/vms/{id}/fullmigrate | 32160 |
| vm | migrate_host | vm_migrate_host | POST /rest/vmmgmt/v1/vms/{id}/migrate | 32116 |
| vm | migrate_storage | vm_migrate_storage | POST /rest/vmmgmt/v1/vms/{id}/migratevol | 32208 |
| vm | import | vm_import | POST /rest/vmmgmt/v1/vms/import | （vms/import） |
| vm | nic_list | vm_nic_list | GET /rest/vmmgmt/v1/vms/{id}/nics | （nics） |
| vm | nic_modify | vm_nic_modify | PUT /rest/vmmgmt/v1/vms/{vm_id}/nics/{nic_id} | （nics/{nic_id}） |
| vm | nic_change_portgroup | vm_nic_change_portgroup | PUT /rest/vmmgmt/v1/vms/{vm_id}/nics/{nic_id}/port-group | 33053 |
| vm | nic_add | vm_nic_add | POST /rest/vmmgmt/v1/vms/{id}/nics | （nics） |
| vm | nic_delete | vm_nic_delete | DELETE /rest/vmmgmt/v1/vms/{vm_id}/nics/{nic_id} | （nics/{nic_id}） |
| vm | nic_change_linkstatus | vm_nic_change_linkstatus | PUT /rest/vmmgmt/v1/vms/{vm_id}/nics-linkstatus | 33279 |
| vm | snapshot_list | vm_snapshot_list | GET /rest/vmmgmt/v1/vms/{vm_id}/snapshots | （snapshots） |
| vm | snapshot_show | vm_snapshot_show | GET /rest/vmmgmt/v1/vms/{vm_id}/snapshots/{snapshot_id} | 33368 |
| vm | snapshot_create | vm_snapshot_create | POST /rest/vmmgmt/v1/vms/{vm_id}/snapshots | （snapshots） |
| vm | snapshot_delete | vm_snapshot_delete | DELETE /rest/vmmgmt/v1/vms/{vm_id}/snapshots/{snapshot_id} | 33471 |
| vm | snapshot_recover | vm_snapshot_recover | POST /rest/vmmgmt/v1/vms/{vm_id}/snapshots/resume-vm | 33511 |
| vswitch | list | vswitch_list | POST /rest/vmmgmt/v1/dvswitchs/query | 30838 |
| vswitch | show | vswitch_show | GET /rest/vmmgmt/v1/dvswitchs/{id} | 30899 |
| vswitch | portgroup_list | vswitch_portgroup_list | POST /rest/vmmgmt/v1/dvswitchs/{dvswitch_id}/portgroups/query | 30948 |
| vswitch | portgroup_create | vswitch_portgroup_create | POST /rest/vmmgmt/v1/dvswitchs/{dvswitch_id}/portgroups | 31000 |
| vswitch | portgroup_modify | vswitch_portgroup_modify | PUT /rest/vmmgmt/v1/dvswitchs/{dvswitch_id}/portgroups/{portgroup_id} | 31054 |
| vswitch | portgroup_delete | vswitch_portgroup_delete | DELETE /rest/vmmgmt/v1/dvswitchs/{dvswitch_id}/portgroups/{portgroup_id} | 31109 |
| secgroup | list | secgroup_list | POST /rest/vmmgmt/v1/secgroups/query | 33552 |
| gpu | list | gpu_list | POST /rest/vmmgmt/v1/host-gpus/query | 33605 |

注：表中"（…）"标注的 API 已确认存在于 API 参考（clone/import/nics/vnc/snapshots 相关 URI 均 grep 命中），实施时以 `grep -n "URI.*<api>"` 定位具体行号再提取参数。

## 阶段与里程碑

### M1：动作函数代码（hci.py 新建 + virt.py 扩展）

1. **新建 `pydme/actions/hci.py`**：模块 docstring（topic 描述，中英双语由 M2 YAML 提供，模块 docstring 用英文如现有模块风格）；按 API 参考实现 5 个函数 `list / show / cluster_list / vswitch_list / storage_list`。函数风格对齐现有代码：`client` 为首参，URL 路径占位符经 `client.get/post(url, params={...})` 传参（参照 REASONIX.md 中 cifs_share_show_permissions 的先例），body 参数仅组装非 None 字段，分页默认值按 API 参考（如 hcis/query `page_no=1, page_size=1000, sort_dir=desc, sort_key=last_modified`）。
2. **扩展 `pydme/actions/virt.py`**：新增 44 个函数，命名严格按上表 func 列；URL 占位符参数名与 API 参考路径参数一致（`{id}`、`{vm_id}`、`{dvswitch_id}`、`{portgroup_id}`、`{virtual_disk_id}` 等，与函数签名参数名对齐，见现有 `vdisk_show(virtual_disk_id)` 风格）。
3. **注意**：`vm_create` / `vm_modify` / `vm_import` / `vdisk_create_attach` 等 body 为复杂嵌套对象（`create_vm_param`、`import_vm_param` 等），按 API 参考"请求 Body 参数"逐字段映射为函数参数（嵌套对象用 `dict` 参数或扁平参数 + 组装，与现有 `protect.py` / `nas.py` 嵌套 body 的处理方式保持一致，实施时先看同仓库先例再定）。
4. 静态校验：`python3 -c "import pydme.actions.hci, pydme.actions.virt"` 无语法错误；`virt.py` 与 `hci.py` 的每个新增函数可通过 `getattr` 解析。

### M2：i18n 注册与 docstring（4 个 YAML）

1. **`actions_zh_CN.yaml` / `actions_en_US.yaml`**：
   - 新增 `hci` topic 条目（direct actions，`actions:` 下列 5 项，`subtopics:` 留空列表）；topic 描述：中文「超融合 (HCI) 相关操作」、英文「Hyper-converged infrastructure (HCI) related operations」；
   - `virt` topic：`datastore` / `host` / `vdisk` / `vm` 子主题追加新 action 条目；**新增 `vswitch` / `secgroup` / `gpu` 子主题**（含中英文 description）；现有子主题 description 如需覆盖新动作语义（如 `vm` 从「列表与详情查询」扩展为「虚拟机生命周期管理」）一并更新；
   - 每条目：`name` 用短名（hci 用 action key 原样）、`description` = docstring 首行（中英各自）、`func` = 上表 func、`params` = 函数签名参数列表（不含 `client`）；
   - 两份文件结构（name/func/params/subtopic）必须完全一致，仅 description 语言不同。
2. **`funcs_zh_CN.yaml` / `funcs_en_US.yaml`**：为 49 个 `<topic>.<func>` key 补充完整 docstring，格式遵循 REASONIX.md 约定（`Args:` 逐参数 + `Returns:` 以 `{` 开头 + 嵌套字段用 `参数格式如下：[{` / `属性格式如下：{` 标记 + 字段行以 `,` 结尾）。内容从 API 参考对应章节提取：请求参数（名称/必选/类型/值域/说明）、响应字段与引用对象（含嵌套结构）。中文 docstring 为权威源，英文由中文翻译（参照现有 en_US 风格）。
3. **round-trip 校验**（手写 stdlib 校验或复用 `check_prose.py`，不引入 PyYAML 依赖之外的解析）：重建 action_key 集合 == 49 新增 + 427 现有；每个新增 action 的 `func` 可在对应模块解析；`description` == docstring 首行；两份 actions 文件结构一致；`virt` / `hci` 的 `params` 与函数签名一致。

### M3：blacklist.json 更新

按「删除 / 修改 / 变更 / 重启 / 关机 / 恢复」语义 + 参照现有先例（`san` 含 `lun_delete` / `lun_expand`），新增 `virt` 条目，候选如下：

`vdisk_modify, vdisk_expand, vdisk_delete, vdisk_detach, vm_modify, vm_delete, vm_power_off, vm_hibernate, vm_reboot, vm_migrate, vm_migrate_host, vm_migrate_storage, vm_umount_tools, vm_nic_modify, vm_nic_change_portgroup, vm_nic_delete, vm_nic_change_linkstatus, vm_snapshot_delete, vm_snapshot_recover, vswitch_portgroup_modify, vswitch_portgroup_delete`

（共 21 个候选，实施时逐项按语义定夺：查询类、`*_add`/`*_create`/`*_mount_tools`/`power_on` 等非破坏操作不列入；`hci` 5 个全为查询类不列入。最终数量以 diff 为准，README 数量同步。）

更新 `pydme/config/blacklist.json` 后，确认用户覆盖文件 `~/.config/pydme/blacklist.json`（若存在）是否需要同步（包内文件是默认，用户文件优先——REASONIX.md 约定，实施时提示用户）。

### M4：CLI help 遍历 + 与 API 参考交叉验证（静态）

1. 遍历 49 个新增动作，执行 `pydme <topic> <subtopic> <action> --help`（hci 为 `pydme hci list --help` 二级命令）与 `pydme <topic> <action> --help`，zh_CN 与 en_US 各跑一遍（`--lang` 切换），确认：
   - help 正常渲染、无解析报错；`Risk Level` 输出符合 blacklist（黑名单动作 High，否则 Low，对齐 cd5754f 行为）；
   - `Args:` 参数与 API 参考"请求 Body 参数/路径参数"逐项一致（名称、必选、类型、值域、默认值）；
   - `Returns:` 字段与 API 参考"响应字段/响应引用对象"一致。
2. 交叉验证脚本：新增 `.reasonix/scripts/106-verify-new-actions.sh`（复用 `00-lib.sh` 的 `exec_test` 模式或独立 shell 循环），输出记录到 `.reasonix/output/106-verify.md`；无需真实网络（help 渲染不触网）。
3. 与 API 参考的行号表（上文清单）逐条核对 API URI 与函数内 `url` 字面量一致。

### M5：README.md / README_zh.md 更新

1. `Project Structure`：`actions/` 注释 `427 actions` → `476 actions`；模块列表新增 `hci.py` 行（按字母序，如 `gfs.py` 后）。
2. `Available topics` 表：总数 427 → 476；`virt` 动作数 14 → 58、描述补充（如 "(VMs/clusters/datastores/vswitches)"）；新增 `hci` 行（5 actions，描述 "Hyper-converged infrastructure (HCI)"）；`98.4% test coverage` 表述改为区分 E2E（420/427，新增 49 个无环境待验）与静态 help 验证（476 全量通过），或按实施时实测更新。
3. `Covered Risk Actions` 表：`Covers **10 topics, 122 high-risk actions**` → 更新数量；新增 `virt` 行（数量 + 示例如 `vm_delete`, `vdisk_delete`, `vm_snapshot_recover`）；README_zh.md 同步全部改动。

### M6：REASONIX.md 更新

- Layout：`16 topic modules` → `17 topic modules`（加 hci）；`427 action functions` → `476`；
- `blacklist.json — 122 destructive/risky action keys` → 按 M3 最终数量；
- End-to-end test status 行：更新为「420/427 E2E（新增 49 个无环境待验），476 全量静态 help 验证通过」；
- Watch out for：补充本次发现的新坑（如 hci 为 direct-action topic、`vm_create`/`vdisk_create_attach` 嵌套 body 的组装方式、`vm_snapshot_recover` URL 无 `{snapshot_id}` 等，按实施实际情况补记）。

## 验收标准

| # | 标准 |
|---|------|
| 1 | `pydme/actions/hci.py` 新建、`virt.py` 新增 44 函数；`python3 -c "import pydme.actions.hci, pydme.actions.virt"` 通过；49 个 func 全部可 `getattr` 解析 |
| 2 | 4 个 YAML 更新完成；round-trip 校验通过（427+49=476 个 action_key 重建一致、双语结构一致、func 可解析、description==docstring 首行、params==签名） |
| 3 | blacklist.json 更新完成，`virt` 高危动作全部覆盖；`pydme virt vm delete --help` 等显示 Risk Level: High，查询类显示 Low |
| 4 | 49 个新增动作 × zh_CN/en_US 的 `--help` 遍历无报错；参数/返回与 API 参考逐项一致（交叉验证记录在 `.reasonix/output/106-verify.md`） |
| 5 | README.md / README_zh.md：structure、topics 表（476 / virt 58 / hci 5）、risk actions 表（数量与示例）三处全部更新且中英文一致 |
| 6 | REASONIX.md 同步（17 topics / 476 actions / blacklist 数量 / E2E 状态），无 427/122/16 等过期数字残留 |
| 7 | 既有 427 个动作的 `--help` 渲染与行为不回归（抽查代表性子主题） |

## 注意与风险

- **docstring 解析约束**：嵌套字段泄漏风险（裸 `格式：{`）；`Returns:` 必须 `{` 开头；字段行逗号结尾——新增 49 份 docstring 全部遵循，M4 遍历可发现泄漏（表现为多余 CLI 参数）。
- **URL 占位符与路径参数**：`{hci_id}` / `{vm_id}` / `{dvswitch_id}` / `{portgroup_id}` / `{virtual_disk_id}` / `{id}` 必须与函数签名参数名一致并经 `params=` 传入，否则 KeyError（参照 a2430ad 修复先例）。
- **短名与 func 分离**：`virt` 44 个新动作的 YAML `name` 为短名、`func` 带 `vm_/vdisk_/host_/datastore_/vswitch_/secgroup_/gpu_` 前缀；注册表重建 key = `<subtopic>_<name>`，必须与 blacklist key、funcs YAML key（`<topic>.<func>`）三处对齐。
- **hci 为 direct-action topic**：`--list-topics` / `--help` 层级为 2 级（`pydme hci list`），与 subtopic 型 3 级命令不同；YAML 中 `actions:` 下直接列 5 项。
- **嵌套 body**：`vm_create` / `vm_modify` / `vm_import` / `vdisk_create_attach` / `vdisk_modify` 等含嵌套对象参数，组装方式需参照仓库内先例（如 `protect.py` / `nas.py`），避免把嵌套对象拆成过多 CLI 参数导致 help 过长或语义丢失；如嵌套对象无法合理拆参，可保持单 `dict` 参数并在 docstring 中用 `参数格式如下：{` 描述内部字段（此时 `params` 数组只含该 dict 参数名，内部字段不会泄漏——REASONIX.md 警告的是裸 `格式：{` 标记，非 `属性格式如下：{`）。
- **英文 docstring 质量**：避免机械直译，技术术语（HCI、dvswitch、portgroup、uplink 等）保持原文。
- **用户黑名单覆盖文件**：`~/.config/pydme/blacklist.json` 优先于包内默认文件，若用户机器存在旧副本，新高危动作需重新生成或手动合并（实施时提醒，不修改用户文件）。

## 执行顺序

M1（代码）→ M2（YAML 注册 + docstring）→ M3（blacklist）→ M4（help 遍历交叉验证）→ M5（README）→ M6（REASONIX.md）

---

## 实施完成记录

| 里程碑 | 状态 | 说明 |
|--------|------|------|
| M1 | ✅ | 新建 `pydme/actions/hci.py`（5 函数）+ `virt.py` 追加 44 函数（共 831 行新增）；import/getattr 校验通过 |
| M2 | ✅ | `actions_zh_CN/en_US.yaml` 注册 49 条目（hci topic 5 direct + virt 44，新增 vswitch/secgroup/gpu 子主题，4 个子主题描述更新）；`funcs_zh_CN/en_US.yaml` 新增 49 份 docstring；round-trip 校验通过（17 topics / 476 actions / 双语结构一致 / params 与签名一致 / description==docstring 首行） |
| M3 | ✅ | `blacklist.json` 新增 `virt` 21 个高危动作（122→141，11 topics）；Risk Level 验证 High/Low 正确（注：本机 `~/.config/pydme/blacklist.json` 用户覆盖文件无 virt，CLI 实测需隔离 HOME） |
| M4 | ✅ | `.reasonix/scripts/106-verify-new-actions.sh`：49×2（zh/en）help 遍历 98 次全 PASS，Risk Level 全部正确；49 个函数 URL 与 API 参考逐条核对一致（`vm_import` 用 `url_path` 变量命名）；记录见 `.reasonix/output/106-verify.md` |
| M5 | ✅ | README.md / README_zh.md：structure 476+hci.py、topics 表（476 / hci 5 / virt 58）、risk 表（11 topics / 141 / virt 21）中英同步 |
| M6 | ✅ | REASONIX.md：17 topics / 476 actions / blacklist 141 / E2E 状态行更新；Watch out for 新增 5 条（hci direct-action 缩进、virt 嵌套 body、vm_snapshot 系列参数位置、vm_import url_path、type 参数遮蔽） |
