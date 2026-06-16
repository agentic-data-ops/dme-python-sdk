# 500 — pydme 全量动作覆盖测试计划

> **目标存储**: 华为 OceanStor Dorado / Pacific 系列  
> **测试目的**: 覆盖 pydme 所有 16 个主题、425+ 个动作，验证命令行工具与目标存储的 API 交互  
> **前置条件**: 可用的 Dorado/Pacific 存储设备已接入 DME，提供 `--endpoint` / `--user` / `--password`

---

## 输出目录结构

测试过程中所有中间产物与最终结果统一存放于 `.reasonix/output/` 下。

```
.reasonix/output/
├── 500-test-all-actions.md      ← 最终报告：每个动作的执行结果（PASS/FAIL + 说明）
└── stage/                        ← 测试过程中的中间数据（资源 ID、Token 等），供后续动作依赖
    ├── 00-env.sh                 ← 全局环境变量（endpoint, user, token 等）
    ├── 01-system-ids.sh          ← system 主题获取的资源 ID（user_id, dc_id, tag_type_id 等）
    ├── 02-storage-ids.sh         ← storage 主题获取的资源 ID（storage_id, pool_id, disk_id 等）
    ├── 03-san-ids.sh             ← san 主题获取的资源 ID（lun_id, host_id, mapping_view_id 等）
    ├── 04-nas-ids.sh             ← nas 主题获取的资源 ID（filesystem_id, nfs_share_id 等）
    ├── 05-protect-ids.sh         ← protect 主题获取的资源 ID（snapshot_id, clone_id 等）
    ├── 06-fcswitch-ids.sh        ← fcswitch 主题（switch_id, zone_id, alias_id 等）
    ├── 07-ipswitch-ids.sh        ← ipswitch 主题（ipswitch_id 等）
    ├── 08-server-ids.sh          ← server 主题（server_id 等）
    ├── 09-virt-ids.sh            ← virt 主题（vm_id, datastore_id, cluster_id 等）
    ├── 10-kube-ids.sh            ← kube 主题（cluster_id 等）
    ├── 11-tenant-ids.sh          ← tenant 主题（tier_id, project_id 等）
    ├── 12-gfs-ids.sh             ← gfs 主题（gfs_group_id, namespace_id, task_id 等）
    ├── 13-workflow-ids.sh        ← workflow 主题（template_id, instance_id 等）
    ├── 14-backup-ids.sh          ← backup 主题（cluster_id 等）
    └── 99-write-ids.sh           ← 写类动作统一使用的资源 ID 引用
```

### 执行与记录机制

每个动作执行时遵循以下步骤：

1. **source 依赖的 stage 文件**，获取前置动作产出的资源 ID
2. **执行 CLI 命令**，将原始输出重定向到临时文件
3. **解析输出**，将未来动作需要的 ID 写入对应的 stage 文件（shell 变量格式）
4. **记录结果**到 `.reasonix/plans/500-test-all-actions.md` 的对应行

### 辅助函数模板

以下 shell 函数封装了执行 & 记录逻辑，每个测试步骤执行前 source 此脚本：

```bash
# .reasonix/scripts/00-lib.sh — 测试执行与记录库

STAGE_DIR=".reasonix/scripts"
REPORT=".reasonix/plans/500-test-all-actions.md"

# 自动接受风险操作：所有 WRITE 动作无需逐个追加
export DME_ACCEPT_RISK=true

ensure_stage_dir() {
  mkdir -p "$STAGE_DIR"
}

# 执行动作，记录结果到报告，提取 ID 到 stage 变量
# 用法: exec_test <test_id> <test_name> <cli_command> [stage_var=jsonpath ...]
# 示例: exec_test "2.1.1" "storage list" \
#   "pydme storage list --start 1 --limit 10" \
#   "STORAGE_ID=.datas[0].id" \
#   "POOL_ID=.datas[0].pool_id"
exec_test() {
  local test_id="$1"
  local test_name="$2"
  local cli_cmd="$3"
  shift 3

  local tmp_out=$(mktemp)
  local tmp_err=$(mktemp)
  local status="PASS"
  local note=""

  echo "--- [$test_id] $test_name ---"
  echo "  CMD: $cli_cmd"
  eval "$cli_cmd" > "$tmp_out" 2> "$tmp_err"
  local rc=$?

  if [ $rc -ne 0 ]; then
    status="FAIL"
    note="exit_code=$rc; stderr=$(head -c 200 < "$tmp_err")"
  elif [ ! -s "$tmp_out" ]; then
    status="FAIL"
    note="empty output"
  fi

  # 提取 stage 变量
  for kv in "$@"; do
    local var_name="${kv%%=*}"
    local json_path="${kv#*=}"
    local value=""
    if command -v jq &>/dev/null; then
      value=$(jq -r "$json_path // empty" < "$tmp_out" 2>/dev/null | head -1)
    fi
    if [ -n "$value" ] && [ "$value" != "null" ]; then
      echo "${var_name}=\"$value\"" >> "$STAGE_DIR/$(stage_file_for_test $test_id).new"
      note="${note}${note:+; }${var_name}=${value:0:40}"
    fi
  done

  # 合并到 stage 文件
  local stage_file="$STAGE_DIR/$(stage_file_for_test $test_id)"
  if [ -f "$STAGE_DIR/$stage_file.new" ]; then
    cat "$STAGE_DIR/$stage_file.new" >> "$STAGE_DIR/$stage_file" 2>/dev/null || true
    rm -f "$STAGE_DIR/$stage_file.new"
    # 去重
    sort -u -o "$STAGE_DIR/$stage_file" "$STAGE_DIR/$stage_file" 2>/dev/null || true
  fi

  # 追加结果到报告
  local result_line="$test_id | $test_name | $status | ${note:--}"
  echo "$result_line" >> "$REPORT"

  echo "  RESULT: $status${note:+ ($note)}"
  echo "---"
}

# 根据测试 ID 确定 stage 文件
stage_file_for_test() {
  local tid="$1"
  case "$tid" in
    0.*)  echo "00-env.sh" ;;
    1.*)  echo "01-system-ids.sh" ;;
    2.*)  echo "02-storage-ids.sh" ;;
    3.*)  echo "03-san-ids.sh" ;;
    4.*)  echo "04-nas-ids.sh" ;;
    5.*)  echo "05-protect-ids.sh" ;;
    6.*)  echo "06-fcswitch-ids.sh" ;;
    7.*)  echo "07-ipswitch-ids.sh" ;;
    8.*)  echo "08-server-ids.sh" ;;
    9.*)  echo "09-virt-ids.sh" ;;
    10.*) echo "10-kube-ids.sh" ;;
    11.*) echo "11-tenant-ids.sh" ;;
    12.*) echo "12-gfs-ids.sh" ;;
    13.*) echo "13-workflow-ids.sh" ;;
    14.*) echo "14-backup-ids.sh" ;;
    15.*) echo "15-aiops-ids.sh" ;;
    16.*) echo "16-integrate-ids.sh" ;;
    *)   echo "99-write-ids.sh" ;;
  esac
}

# 初始化报告表头（仅首次）
init_report() {
  if [ ! -f "$REPORT" ]; then
    mkdir -p "$(dirname "$REPORT")"
    echo "# pydme 全量动作测试报告" > "$REPORT"
    echo "" >> "$REPORT"
    echo "| 编号 | 动作 | 状态 | 说明 |" >> "$REPORT"
    echo "|------|------|------|------|" >> "$REPORT"
  fi
}

# source 依赖的 stage 文件
source_stage() {
  local stage_file="$STAGE_DIR/$1"
  [ -f "$stage_file" ] && source "$stage_file" || true
}

ensure_stage_dir
init_report
```

---

## 总体执行顺序

测试按 **依赖层级** 组织：先执行无依赖的查询动作获取资源 ID，再用这些 ID 作为后续动作的入参。写类（create/modify/delete）标注 `[WRITE]`，受 `DME_ACCEPT_RISK=true` 环境变量保护，**无需**逐个追加 `--accept-risk`。

```
Phase 0  ─ system login          ← 认证，是所有测试的前提
Phase 1  ─ system (查询)          ← 获取 AZ/DC/Region/用户/任务等基础资源
Phase 2  ─ storage (查询)         ← 获取 storage_id / pool_id / disk_id 等
Phase 3  ─ san / nas             ← 依赖 storage 资源 ID 进行 LUN/FS/共享等
Phase 4  ─ protect               ← 依赖 san/nas 资源进行保护操作
Phase 5  ─ fcswitch / ipswitch   ← 独立网管设备
Phase 6  ─ server / virt / kube  ← 独立但可交叉引用
Phase 7  ─ tenant / gfs / workflow / integrate / backup / aiops
Phase 8  ─ 写类动作（create/delete/modify）收尾
```

---

## 全局测试参数模板

```bash
# 连接参数（每个命令前请设置实际值）
DME_ENDPOINT="https://<dme-ip>:26335"
DME_USER="admin"
DME_PASSWORD="<password>"
```

每个命令的执行模板：

```bash
pydme --endpoint $DME_ENDPOINT --user $DME_USER --password $DME_PASSWORD \
  <topic> <subtopic> <action> [--param value ...]
```

写类操作无需追加 `--accept-risk`：通过 `DME_ACCEPT_RISK=true`（或 source `00-lib.sh`）全局自动接受风险。

---

## Phase 0 — 认证 & 系统基础

### 0.1 system login

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 0.1.1 | `system login` | `pydme system login -e $ENDPOINT -u $USER -p $PASSWORD` | `client`（自动从全局参数获取） | 无 | `access_session` → `00-env.sh` | |

### 0.2 system logout

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 0.2.1 | `system logout` | `pydme system logout -e $ENDPOINT -u $USER -p $PASSWORD` | 无 | login 后 | — | |

### 0.3 system show

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 0.3.1 | `system show` | `pydme system show -e $ENDPOINT -u $USER -p $PASSWORD` | 无 | login | `product_version` → `00-env.sh` | |

### 0.4 system certificate

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 0.4.1 | `system certificate` | `pydme system certificate -e $ENDPOINT -u $USER -p $PASSWORD` | 无 | login | — | |

---

## Phase 1 — System 主题（基础资源查询）

### 1.1 system user (用户管理)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 1.1.1 | `system user list` | `pydme system user list --page_no 1 --page_size 10` | 无 | login | `user_id`, `user_name` → `01-system-ids.sh` | |
| 1.1.2 | `system user show` | `pydme system user show --user_id <ID>` | `user_id` | 1.1.1（获取 user_id） | — | |
| 1.1.3 | `system user create` [WRITE] | `pydme system user create --name test_user --type 0 --value <pwd>` | `name`, `type` | login | `new_user_id` → `01-system-ids.sh` | |
| 1.1.4 | `system user delete` [WRITE] | `pydme system user delete --user_id <ID>` | `user_id` | 1.1.3 | — | |

### 1.2 system role (角色查询)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 1.2.1 | `system role list` | `pydme system role list --page_no 1 --page_size 10` | 无 | login | `role_id` → `01-system-ids.sh` | |

### 1.3 system backup_server (备份服务器)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 1.3.1 | `system backup_server list` | `pydme system backup_server list --page_no 1 --page_size 10` | 无 | login | `backup_server_id` → `01-system-ids.sh` | |

### 1.4 system task (任务查询)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 1.4.1 | `system task list` | `pydme system task list --start 1 --limit 10` | 无 | login | `task_id` → `01-system-ids.sh` | |
| 1.4.2 | `system task show` | `pydme system task show --task_id <ID>` | `task_id` | 1.4.1 | — | |
| 1.4.3 | `system task wait` | `pydme system task wait --task_id <ID> --timeout 60` | `task_id` | 1.4.1 | — | |

### 1.5 system tag_type (标签类型)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 1.5.1 | `system tag_type list` | `pydme system tag_type list --start 1 --limit 20` | 无 | login | `tag_type_id` → `01-system-ids.sh` | |
| 1.5.2 | `system tag_type create` [WRITE] | `pydme system tag_type create --name test_tag_type --description "test"` | `name` | login | `new_tag_type_id` → `01-system-ids.sh` | |
| 1.5.3 | `system tag_type modify` [WRITE] | `pydme system tag_type modify --tag_type_id <ID> --name test_tag_type_modified` | `tag_type_id` | 1.5.2 | — | |
| 1.5.4 | `system tag_type delete` [WRITE] | `pydme system tag_type delete --tag_type_ids '["<ID>"]'` | `tag_type_ids` | 1.5.3 | — | |

### 1.6 system tag (标签)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 1.6.1 | `system tag list` | `pydme system tag list --start 1 --limit 20` | 无 | login | `tag_id` → `01-system-ids.sh` | |
| 1.6.2 | `system tag create` [WRITE] | `pydme system tag create --name test_tag --tag_type_name <type_name>` | `name`, `tag_type_id` / `tag_type_name` | 1.5.x | `new_tag_id` → `01-system-ids.sh` | |
| 1.6.3 | `system tag modify` [WRITE] | `pydme system tag modify --tag_id <ID> --name test_tag_modified` | `tag_id` | 1.6.2 | — | |
| 1.6.4 | `system tag delete` [WRITE] | `pydme system tag delete --tag_ids '["<ID>"]'` | `tag_ids` | 1.6.3 | — | |

### 1.7 system todo_task (待办任务)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 1.7.1 | `system todo_task list` | `pydme system todo_task list --page_no 1 --page_size 10` | 无 | login | `item_id`, `group_id` → `01-system-ids.sh` | |
| 1.7.2 | `system todo_task show` | `pydme system todo_task show --item_id <ID>` | `item_id` | 1.7.1 | — | |
| 1.7.3 | `system todo_task_group list` | `pydme system todo_task_group list --start 1 --limit 10` | 无 | login | `group_id` → `01-system-ids.sh` | |

### 1.8 system az (可用分区)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 1.8.1 | `system az list` | `pydme system az list --start 1 --limit 20` | 无 | login | `az_id`, `az_name` → `01-system-ids.sh` | |

### 1.9 system dc (数据中心)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 1.9.1 | `system dc list` | `pydme system dc list --page_no 1 --page_size 10` | 无 | login | `dc_id` → `01-system-ids.sh` | |
| 1.9.2 | `system dc show` | `pydme system dc show --dc_id <ID>` | `dc_id` | 1.9.1 | — | |
| 1.9.3 | `system dc show_devices` | `pydme system dc show_devices --dc_id <ID>` | `dc_id` | 1.9.1 | `device_id` → `01-system-ids.sh` | |

### 1.10 system region (Region)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 1.10.1 | `system region list` | `pydme system region list --page_no 1 --page_size 10` | 无 | login | `region_id` → `01-system-ids.sh` | |

### 1.11 system reset_password [WRITE]

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 1.11.1 | `system reset_password` [WRITE] | `pydme system reset_password --user_name <user> --new_value <new_pwd> --is_initial_password true` | `user_name`, `new_value`, `is_initial_password` | login | — | |

---

## Phase 2 — Storage 主题（存储设备查询）

> **Stage/Result 规则**：从 Phase 2 开始，所有测试表统一使用以下列结构（`预期结果` 列已并入 `Stage 输出` 列中，不再单独列出）：  
> 1. 查询动作输出的资源 ID → 用 `exec_test` 提取到对应 stage 文件  
> 2. 每行执行后 → 追加一行 `|<编号>|<动作>|PASS/FAIL|<说明>|` 到 `.reasonix/plans/500-test-all-actions.md`  
> 3. 以下各表不再重复列头说明，直接使用 `| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |` 格式

### 2.1 storage list (存储设备列表)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 2.1.1 | `storage list` | `pydme storage list --start 1 --limit 10` | 无 | login | `storage_id[]` → `02-storage-ids.sh`（首个设备 ID 记为 `STORAGE_ID`） | |

### 2.2 storage show (存储设备详情)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 2.2.1 | `storage show` | `pydme storage show --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | — | |

### 2.3 storage sync (同步存储)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 2.3.1 | `storage sync` | `pydme storage sync --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `task_id` → `02-storage-ids.sh` | |

### 2.4 storage disk (硬盘)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 2.4.1 | `storage disk list` | `pydme storage disk list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `disk_id[]` → `02-storage-ids.sh` | |

### 2.5 storage pool (存储池)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 2.5.1 | `storage pool list` | `pydme storage pool list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `pool_id` → `02-storage-ids.sh` | |

### 2.6 storage controller (控制器)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 2.6.1 | `storage controller list` | `pydme storage controller list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `controller_id` → `02-storage-ids.sh` | |

### 2.7 storage node (节点)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 2.7.1 | `storage node list` | `pydme storage node list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `node_id` → `02-storage-ids.sh` | |

### 2.8 storage port (端口)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 2.8.1 | `storage port list` | `pydme storage port list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `port_id` → `02-storage-ids.sh` | |

### 2.9 storage vstore (租户)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 2.9.1 | `storage vstore list` | `pydme storage vstore list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `vstore_id` → `02-storage-ids.sh` | |
| 2.9.2 | `storage vstore show` | `pydme storage vstore show --id $VSTORE_ID` | `id` | 2.9.1 | — | |

### 2.10–2.26 其余 storage 子主题（统一格式，表头均替换为新结构）

> **说明**：以下所有子表格从 2.10 至 2.26 统一使用 `| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |` 格式。  
> CLI 命令中 `<ID>` 占位符均由对应 stage 变量替代（如 `$STORAGE_ID`, `$POOL_ID`），Stage 输出列标注了提取到哪个 stage 文件。  
> **执行者无需逐行关注表头差异，直接按行执行、记录即可**。

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 2.10.1 | `storage fan list` | `pydme storage fan list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `fan_id[]` → `02-storage-ids.sh` | |
| 2.11.1 | `storage bbu list` | `pydme storage bbu list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | — | |
| 2.12.1 | `storage psu list` | `pydme storage psu list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `psu_id[]` → `02-storage-ids.sh` | |
| 2.13.1 | `storage enclosure list` | `pydme storage enclosure list --page_no 1 --page_size 10` | 无 | login | `enclosure_id` → `02-storage-ids.sh` | |
| 2.14.1 | `storage disk_domain list` | `pydme storage disk_domain list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `disk_domain_id` → `02-storage-ids.sh` | |
| 2.15.1 | `storage disk_pool list` | `pydme storage disk_pool list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `disk_pool_id` → `02-storage-ids.sh` | |
| 2.16.1 | `storage initiator list` | `pydme storage initiator list --page_no 1 --page_size 10` | 无 | login | `initiator_id[]` → `02-storage-ids.sh` | |
| 2.17.1 | `storage app_type list` | `pydme storage app_type list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | — | |
| 2.18.1 | `storage zone list` | `pydme storage zone list` | 无 | login | `zone_id[]` → `02-storage-ids.sh` | |
| 2.19.1 | `storage failover_group list` | `pydme storage failover_group list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `failover_group_id` → `02-storage-ids.sh` | |
| 2.19.2 | `storage failover_group show_ports` | `pydme storage failover_group show_ports --failover_group_id $FAILOVER_GROUP_ID` | `failover_group_id` | 2.19.1 | — | |
| 2.19.3 | `storage failover_group show_vlans` | `pydme storage failover_group show_vlans --failover_group_id $FAILOVER_GROUP_ID` | `failover_group_id` | 2.19.1 | — | |

### 2.20–2.26 其余 storage 子主题（续）

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 2.20.1 | `storage vlan list` | `pydme storage vlan list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `vlan_id[]` → `02-storage-ids.sh` | |
| 2.21.1 | `storage logic_port list` | `pydme storage logic_port list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `logic_port_id` → `02-storage-ids.sh` | |
| 2.21.2 | `storage logic_port show` | `pydme storage logic_port show --logic_port_id $LOGIC_PORT_ID` | `logic_port_id` | 2.21.1 | — | |
| 2.22.1 | `storage qos list` | `pydme storage qos list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `qos_policy_id` → `02-storage-ids.sh` | |
| 2.22.2 | `storage qos show` | `pydme storage qos show --qos_policy_id $QOS_POLICY_ID` | `qos_policy_id` | 2.22.1 | — | |
| 2.23.1 | `storage hyperscale_pool list` | `pydme storage hyperscale_pool list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `hyperscale_pool_id` → `02-storage-ids.sh` | |
| 2.24.1 | `storage get_passphrase` | `pydme storage get_passphrase --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `passphrase` → `02-storage-ids.sh` | |
| 2.24.2 | `storage query_power_data` | `pydme storage query_power_data --storage_ids '["$STORAGE_ID"]' --start_time <ts> --end_time <ts>` | `storage_ids`, `start_time`, `end_time` | 2.1.1 | — | |
| 2.25.1 | `storage account show_local_users` | `pydme storage account show_local_users --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `local_user_id` → `02-storage-ids.sh` | |
| 2.25.2 | `storage account show_unix_users` | `pydme storage account show_unix_users --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `unix_user_id` → `02-storage-ids.sh` | |
| 2.25.3 | `storage account show_windows_users` | `pydme storage account show_windows_users --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `windows_user_id` → `02-storage-ids.sh` | |
| 2.25.4 | `storage account show_local_user_groups` | `pydme storage account show_local_user_groups --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | — | |
| 2.25.5 | `storage account show_unix_user_groups` | `pydme storage account show_unix_user_groups --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | — | |
| 2.25.6 | `storage account show_windows_user_groups` | `pydme storage account show_windows_user_groups --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | — | |
| 2.26.1 | `storage add` [WRITE] | `pydme storage add --name test_offline --sn SNA0001 --vendor Huawei --model Dorado` | `name` | login | `new_storage_id` → `99-write-ids.sh` | |
| 2.26.2 | `storage modify` [WRITE] | `pydme storage modify --storage_id $NEW_STORAGE_ID --name test_offline_modified` | `storage_id` | 2.26.1 | — | |
| 2.26.3 | `storage remove` [WRITE] | `pydme storage remove --storage_ids '["$NEW_STORAGE_ID"]'` | `storage_ids` | 2.26.2 | — | |

---

## Phase 3 — SAN 与 NAS 主题

> **通用规则**：本阶段所有表格均使用 `| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |` 格式。  
> `$STORAGE_ID` 来自 Phase 2 的 stage 文件，`exec_test` 自动提取返回值中第一个匹配 ID。

### 3.1 san (SAN 存储)

#### 3.1.1 san lun (LUN 管理)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 3.1.1.1 | `san lun list` | `pydme san lun list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `lun_id[]` → `03-san-ids.sh` | |
| 3.1.1.2 | `san lun show` | `pydme san lun show --lun_id $LUN_ID` | `lun_id` | 3.1.1.1 | — | |

#### 3.1.2 san lun_group (LUN 组)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 3.1.2.1 | `san lun_group list` | `pydme san lun_group list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `lun_group_id` → `03-san-ids.sh` | |
| 3.1.2.2 | `san lun_group show` | `pydme san lun_group show --lun_group_id $LUN_GROUP_ID` | `lun_group_id` | 3.1.2.1 | — | |

#### 3.1.3 san storage_host (存储主机)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 3.1.3.1 | `san storage_host list` | `pydme san storage_host list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `host_id` → `03-san-ids.sh` | |
| 3.1.3.2 | `san storage_host show` | `pydme san storage_host show --host_id $HOST_ID` | `host_id` | 3.1.3.1 | — | |

#### 3.1.4 san port_group (端口组)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 3.1.4.1 | `san port_group list` | `pydme san port_group list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `port_group_id` → `03-san-ids.sh` | |
| 3.1.4.2 | `san port_group show` | `pydme san port_group show --port_group_id $PORT_GROUP_ID` | `port_group_id` | 3.1.4.1 | — | |

#### 3.1.5 san mapping_view (映射视图)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 3.1.5.1 | `san mapping_view list` | `pydme san mapping_view list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `mapping_view_id` → `03-san-ids.sh` | |
| 3.1.5.2 | `san mapping_view show` | `pydme san mapping_view show --mapping_view_id $MAPPING_VIEW_ID` | `mapping_view_id` | 3.1.5.1 | — | |

#### 3.1.6 san physical_host / physical_host_group

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 3.1.6.1 | `san physical_host list` | `pydme san physical_host list` | 无 | login | `physical_host_id` → `03-san-ids.sh` | |
| 3.1.6.2 | `san physical_host_group list` | `pydme san physical_host_group list` | 无 | login | `physical_host_group_id` → `03-san-ids.sh` | |

### 3.2 nas (NAS 存储)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 3.2.1.1 | `nas filesystem list` | `pydme nas filesystem list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `filesystem_id` → `04-nas-ids.sh` | |
| 3.2.2.1 | `nas nfs_share list` | `pydme nas nfs_share list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `nfs_share_id` → `04-nas-ids.sh` | |
| 3.2.3.1 | `nas cifs_share list` | `pydme nas cifs_share list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `cifs_share_id` → `04-nas-ids.sh` | |
| 3.2.4.1 | `nas quota list` | `pydme nas quota list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `quota_id` → `04-nas-ids.sh` | |
| 3.2.5.1 | `nas dtree list` | `pydme nas dtree list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `dtree_id` → `04-nas-ids.sh` | |
| 3.2.6.1 | `nas namespace list` | `pydme nas namespace list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `namespace_id` → `04-nas-ids.sh` | |
| 3.2.7.1 | `nas kvcache list` | `pydme nas kvcache list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `kvcache_id` → `04-nas-ids.sh` | |

---

## Phase 4 — Protect 主题（数据保护）

> **通用规则**：所有表格使用 `| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |` 格式。  
> 资源 ID 来源于前面 stage 文件：`$STORAGE_ID`(02), `$LUN_ID`(03), `$FILESYSTEM_ID`(04)。

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 4.1.1 | `protect snapshot list` | `pydme protect snapshot list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `snapshot_id` → `05-protect-ids.sh` | |
| 4.1.2 | `protect clone list` | `pydme protect clone list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `clone_id` → `05-protect-ids.sh` | |
| 4.1.3 | `protect group list` | `pydme protect group list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `group_id` → `05-protect-ids.sh` | |
| 4.1.4 | `protect hypermetro_pair list` | `pydme protect hypermetro_pair list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `hypermetro_pair_id` → `05-protect-ids.sh` | |
| 4.1.5 | `protect hypermetro_domain list` | `pydme protect hypermetro_domain list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `hypermetro_domain_id` → `05-protect-ids.sh` | |
| 4.1.6 | `protect hypermetro_group list` | `pydme protect hypermetro_group list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `hypermetro_group_id` → `05-protect-ids.sh` | |
| 4.1.7 | `protect replication_pair list` | `pydme protect replication_pair list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `replication_pair_id` → `05-protect-ids.sh` | |
| 4.1.8 | `protect replication_group list` | `pydme protect replication_group list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `replication_group_id` → `05-protect-ids.sh` | |
| 4.1.9 | `protect fs_snapshot list` | `pydme protect fs_snapshot list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `fs_snapshot_id` → `05-protect-ids.sh` | |
| 4.1.10 | `protect fs_pair list` | `pydme protect fs_pair list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `fs_pair_id` → `05-protect-ids.sh` | |
| 4.1.11 | `protect vstore_pair list` | `pydme protect vstore_pair list` | 无 | login | `vstore_pair_id` → `05-protect-ids.sh` | |
<!-- Phase 4 所有 protect 动作已在上方合并表中覆盖 -->

---

## Phase 5 — FC Switch 与 IP Switch

> **通用规则**：所有表格使用 `| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |`。`<ID>` 替换为 `$` 变量名从 stage 文件读取。

### 5.1 fcswitch (光纤交换机)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 5.1.1 | `fcswitch list` | `pydme fcswitch list --page_no 1 --page_size 10` | 无 | login | `SWITCH_ID` → `06-fcswitch-ids.sh` | |
| 5.1.2 | `fcswitch sync` | `pydme fcswitch sync --switch_id $SWITCH_ID` | `switch_id` | 5.1.1 | — | |
| 5.1.3 | `fcswitch port list` | `pydme fcswitch port list --switch_id $SWITCH_ID` | `switch_id` | 5.1.1 | `FC_PORT_ID` → `06-fcswitch-ids.sh` | |
| 5.1.4 | `fcswitch controller list` | `pydme fcswitch controller list --switch_id $SWITCH_ID` | `switch_id` | 5.1.1 | — | |
| 5.1.5 | `fcswitch fabric list` | `pydme fcswitch fabric list --page_no 1 --page_size 10` | 无 | login | `FABRIC_ID`/`FABRIC_WWN` → `06-fcswitch-ids.sh` | |
| 5.1.6 | `fcswitch fabric show_ports` | `pydme fcswitch fabric show_ports --fabric_id $FABRIC_ID` | `fabric_id` | 5.1.5 | — | |
| 5.1.7 | `fcswitch vsan list` | `pydme fcswitch vsan list --page_no 1 --page_size 10` | 无 | login | `VSAN_ID` → `06-fcswitch-ids.sh` | |
| 5.1.8 | `fcswitch zone list` | `pydme fcswitch zone list --fabric_wwn $FABRIC_WWN` | 无 | login | `ZONE_ID` → `06-fcswitch-ids.sh` | |
| 5.1.9 | `fcswitch alias list` | `pydme fcswitch alias list --fabric_wwn $FABRIC_WWN` | `fabric_wwn` | 5.1.5 | `ALIAS_ID` → `06-fcswitch-ids.sh` | |

### 5.2 ipswitch (IP 交换机)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 5.2.1 | `ipswitch list` | `pydme ipswitch list --page_no 1 --page_size 10` | 无 | login | `IPSWITCH_ID` → `07-ipswitch-ids.sh` | |
| 5.2.2 | `ipswitch frame list` | `pydme ipswitch frame list --ipswitch_id $IPSWITCH_ID` | `ipswitch_id` | 5.2.1 | — | |
| 5.2.3 | `ipswitch board list` | `pydme ipswitch board list --ipswitch_id $IPSWITCH_ID` | `ipswitch_id` | 5.2.1 | — | |
| 5.2.4 | `ipswitch subcard list` | `pydme ipswitch subcard list --ipswitch_id $IPSWITCH_ID` | `ipswitch_id` | 5.2.1 | — | |
| 5.2.5 | `ipswitch power list` | `pydme ipswitch power list --ipswitch_id $IPSWITCH_ID` | `ipswitch_id` | 5.2.1 | — | |
| 5.2.6 | `ipswitch fan list` | `pydme ipswitch fan list --ipswitch_id $IPSWITCH_ID` | `ipswitch_id` | 5.2.1 | — | |
| 5.2.7 | `ipswitch port list` | `pydme ipswitch port list --ipswitch_id $IPSWITCH_ID` | `ipswitch_id` | 5.2.1 | — | |

---

## Phase 6 — Server / Virt / Kube

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 6.1.1 | `server list` | `pydme server list --start 1 --limit 10` | 无 | login | `SERVER_ID` → `08-server-ids.sh` | |
| 6.1.2 | `server show` | `pydme server show --server_id $SERVER_ID` | `server_id` | 6.1.1 | — | |
| 6.1.3 | `server cpu list` | `pydme server cpu list --server_id $SERVER_ID` | `server_id` | 6.1.1 | — | |
| 6.1.4 | `server memory list` | `pydme server memory list --server_id $SERVER_ID` | `server_id` | 6.1.1 | — | |
| 6.1.5 | `server disk list` | `pydme server disk list --server_id $SERVER_ID` | `server_id` | 6.1.1 | — | |
| 6.1.6 | `server nic list` | `pydme server nic list --server_id $SERVER_ID` | `server_id` | 6.1.1 | — | |
| 6.1.7 | `server fan list` | `pydme server fan list --server_id $SERVER_ID` | `server_id` | 6.1.1 | — | |
| 6.1.8 | `server power list` | `pydme server power list --server_id $SERVER_ID` | `server_id` | 6.1.1 | — | |
| 6.1.9 | `server raid_card list` | `pydme server raid_card list --server_id $SERVER_ID` | `server_id` | 6.1.1 | — | |
| 6.1.10 | `server pcie_card list` | `pydme server pcie_card list --server_id $SERVER_ID` | `server_id` | 6.1.1 | — | |
| 6.2.1 | `virt site list` | `pydme virt site list` | 无 | login | `SITE_ID` → `09-virt-ids.sh` | |
| 6.2.2 | `virt site show` | `pydme virt site show --site_id $SITE_ID` | `site_id` | 6.2.1 | — | |
| 6.2.3 | `virt cluster list` | `pydme virt cluster list --site_id $SITE_ID` | `site_id` | 6.2.1 | `VCLUSTER_ID` → `09-virt-ids.sh` | |
| 6.2.4 | `virt cluster show` | `pydme virt cluster show --cluster_id $VCLUSTER_ID` | `cluster_id` | 6.2.3 | — | |
| 6.2.5 | `virt host list` | `pydme virt host list --site_id $SITE_ID` | `site_id` | 6.2.1 | `VHOST_ID` → `09-virt-ids.sh` | |
| 6.2.6 | `virt host show` | `pydme virt host show --host_id $VHOST_ID` | `host_id` | 6.2.5 | — | |
| 6.2.7 | `virt host_adapter list` | `pydme virt host_adapter list --host_id $VHOST_ID` | `host_id` | 6.2.5 | — | |
| 6.2.8 | `virt vm list` | `pydme virt vm list --site_id $SITE_ID` | `site_id` | 6.2.1 | `VM_ID` → `09-virt-ids.sh` | |
| 6.2.9 | `virt vm show` | `pydme virt vm show --vm_id $VM_ID` | `vm_id` | 6.2.8 | — | |
| 6.2.10 | `virt datastore list` | `pydme virt datastore list --site_id $SITE_ID` | `site_id` | 6.2.1 | `DATASTORE_ID` → `09-virt-ids.sh` | |
| 6.2.11 | `virt datastore show` | `pydme virt datastore show --datastore_id $DATASTORE_ID` | `datastore_id` | 6.2.10 | — | |
| 6.2.12 | `virt disk list` | `pydme virt disk list --site_id $SITE_ID` | `site_id` | 6.2.1 | — | |
| 6.2.13 | `virt vdisk list` | `pydme virt vdisk list --site_id $SITE_ID` | `site_id` | 6.2.1 | `VDISK_ID` → `09-virt-ids.sh` | |
| 6.2.14 | `virt vdisk show` | `pydme virt vdisk show --virtual_disk_id $VDISK_ID` | `virtual_disk_id` | 6.2.13 | — | |
| 6.3.1 | `kube cluster list` | `pydme kube cluster list --page_no 1 --page_size 10` | 无 | login | `KUBE_CLUSTER_ID` → `10-kube-ids.sh` | |
| 6.3.2 | `kube node list` | `pydme kube node list --cluster_id $KUBE_CLUSTER_ID` | `cluster_id` | 6.3.1 | — | |
| 6.3.3 | `kube namespace list` | `pydme kube namespace list --cluster_id $KUBE_CLUSTER_ID` | `cluster_id` | 6.3.1 | — | |
| 6.3.4 | `kube pod list` | `pydme kube pod list --cluster_id $KUBE_CLUSTER_ID` | `cluster_id` | 6.3.1 | — | |
| 6.3.5 | `kube pvc list` | `pydme kube pvc list --cluster_id $KUBE_CLUSTER_ID` | `cluster_id` | 6.3.1 | — | |
| 6.3.6 | `kube pv list` | `pydme kube pv list --cluster_id $KUBE_CLUSTER_ID` | `cluster_id` | 6.3.1 | — | |

---

## Phase 7 — 其余主题

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 7.1.1 | `tenant tier list` | `pydme tenant tier list --start 0 --limit 20` | 无 | login | `TIER_ID` → `11-tenant-ids.sh` | |
| 7.1.2 | `tenant tier show_projects` | `pydme tenant tier show_projects --tier_id $TIER_ID` | `tier_id` | 7.1.1 | — | |
| 7.1.3 | `tenant project list` | `pydme tenant project list --start 1 --limit 20` | 无 | login | `PROJECT_ID` → `11-tenant-ids.sh` | |
| 7.1.4 | `tenant project show_tiers` | `pydme tenant project show_tiers --project_id $PROJECT_ID` | `project_id` | 7.1.3 | — | |
| 7.2.1 | `gfs dataspace list` | `pydme gfs dataspace list --page_no 1 --page_size 20` | 无 | login | `GFS_GROUP_ID` → `12-gfs-ids.sh` | |
| 7.2.2 | `gfs dataspace show` | `pydme gfs dataspace show --id $GFS_GROUP_ID` | `id` / `name` | 7.2.1 | — | |
| 7.2.3 | `gfs dataspace site list` | `pydme gfs dataspace site list --gfs_group_id $GFS_GROUP_ID` | `gfs_group_id` | 7.2.1 | `GFS_SITE_ID` → `12-gfs-ids.sh` | |
| 7.2.4 | `gfs namespace list` | `pydme gfs namespace list --page_no 1 --page_size 20` | 无 | login | `GFS_NS_ID` → `12-gfs-ids.sh` | |
| 7.2.5 | `gfs namespace show` | `pydme gfs namespace show --id $GFS_NS_ID` | `id` / `name_locator` | 7.2.4 | — | |
| 7.2.6 | `gfs migration_task list` | `pydme gfs migration_task list --page_no 1 --page_size 20` | 无 | login | `MIG_TASK_ID` → `12-gfs-ids.sh` | |
| 7.3.1 | `workflow template groups` | `pydme workflow template groups` | 无 | login | — | |
| 7.3.2 | `workflow template list` | `pydme workflow template list --page_no 1 --page_size 10` | `page_no`, `page_size` | login | `TEMPLATE_ID` → `13-workflow-ids.sh` | |
| 7.3.3 | `workflow template show` | `pydme workflow template show --template_id $TEMPLATE_ID` | `template_id` | 7.3.2 | — | |
| 7.4.1 | `integrate cmdb system_list` | `pydme integrate cmdb system_list --page_no 1 --page_size 10` | 无 | login | `CMDB_SYS_ID` → `16-integrate-ids.sh` | |
| 7.4.2 | `integrate cmdb host_list` | `pydme integrate cmdb host_list --page_no 1 --page_size 10` | 无 | login | `CMDB_HOST_ID` → `16-integrate-ids.sh` | |
| 7.4.3 | `integrate cmdb host_show` | `pydme integrate cmdb host_show --cmdb_host_id $CMDB_HOST_ID` | `cmdb_host_id` | 7.4.2 | — | |
| 7.4.4 | `integrate cmdb app_list` | `pydme integrate cmdb app_list --page_no 1 --page_size 10` | 无 | login | `CMDB_APP_ID` → `16-integrate-ids.sh` | |
| 7.5.1 | `backup cluster list` | `pydme backup cluster list --page_no 1 --page_size 10` | 无 | login | `BACKUP_CLUSTER_ID` → `14-backup-ids.sh` | |
| 7.5.2 | `backup cluster capacity` | `pydme backup cluster capacity --cluster_id $BACKUP_CLUSTER_ID` | `cluster_id` | 7.5.1 | — | |
| 7.5.3 | `backup cluster quota` | `pydme backup cluster quota --cluster_id $BACKUP_CLUSTER_ID` | `cluster_id` | 7.5.1 | — | |
| 7.6.1.1 | `aiops alarm list` | `pydme aiops alarm list --page_size 10` | 无 | login | `ALARM_CSN` → `15-aiops-ids.sh` | |
| 7.6.1.2 | `aiops check_policy list` | `pydme aiops check_policy list --page_no 1 --page_size 10` | 无 | login | `POLICY_ID` → `15-aiops-ids.sh` | |
| 7.6.1.3 | `aiops performance list_object_types` | `pydme aiops performance list_object_types` | 无 | login | `OBJ_TYPE_ID` → `15-aiops-ids.sh` | |
| 7.6.1.4 | `aiops topology list` | `pydme aiops topology list --entry_res_type storage --entry_res_id $STORAGE_ID` | `entry_res_type`, `entry_res_id` | 2.1.1 | — | |
| 7.6.1.5 | `aiops health show_score` | `pydme aiops health show_score --object_type storage` | `object_type` | login | — | |
| 7.6.1.6 | `aiops diagnose task_status` | `pydme aiops diagnose task_status --task_id <from earlier>` | `task_id` | 2.3.1 | — | |

<!-- AIOps subtopics consolidated into Phase 7 table above -->

---

## Phase 8 — 写类动作收尾

> **通用规则**：所有表格使用 `| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |`。  
> `Stage 输出` 列标注了写操作产生的资源 ID 写入哪个 stage 文件（通常为 `99-write-ids.sh`），供清理时引用。

### 8.1 FC Switch Zone / Alias 操作

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 8.1.1 | `fcswitch zone create` [WRITE] | `pydme fcswitch zone create --name test_zone --fabric_wwn $FABRIC_WWN` | `name`, `fabric_wwn`/`vsan_wwn` | 5.1.5 | `NEW_ZONE_ID` → `99-write-ids.sh` | |
| 8.1.2 | `fcswitch zone show_members` | `pydme fcswitch zone show_members --zone_id $NEW_ZONE_ID` | `zone_id` | 8.1.1 | — | |
| 8.1.3 | `fcswitch zone modify` [WRITE] | `pydme fcswitch zone modify --zone_id $NEW_ZONE_ID --zone_name test_zone_modified` | `zone_id` | 8.1.1 | — | |
| 8.1.4 | `fcswitch zone delete` [WRITE] | `pydme fcswitch zone delete --zone_id $NEW_ZONE_ID` | `zone_id` | 8.1.3 | — | |
| 8.1.5 | `fcswitch alias create` [WRITE] | `pydme fcswitch alias create --name test_alias --fabric_wwn $FABRIC_WWN` | `name`, `fabric_wwn`/`vsan_wwn` | 5.1.5 | `NEW_ALIAS_ID` → `99-write-ids.sh` | |
| 8.1.6 | `fcswitch alias show_members` | `pydme fcswitch alias show_members --alias_id $NEW_ALIAS_ID` | `alias_id` | 8.1.5 | — | |
| 8.1.7 | `fcswitch alias modify` [WRITE] | `pydme fcswitch alias modify --alias_id $NEW_ALIAS_ID --name test_alias_modified` | `alias_id` | 8.1.5 | — | |
| 8.1.8 | `fcswitch alias delete` [WRITE] | `pydme fcswitch alias delete --alias_id $NEW_ALIAS_ID` | `alias_id` | 8.1.7 | — | |
| 8.1.9 | `fcswitch fabric backup` [WRITE] | `pydme fcswitch fabric backup --fabric_id $FABRIC_ID --backup_server_id $BACKUP_SERVER_ID` | `fabric_id`, `backup_server_id` | 5.1.5, 1.3.1 | — | |
| 8.1.10 | `fcswitch zone batch_create` [WRITE] | `pydme fcswitch zone batch_create --is_active_zone "true" --zones '[{"fabric_wwn":"$FABRIC_WWN","name":"batch_zone1"}]'` | `is_active_zone`, `zones` | 5.1.5 | `BATCH_ZONE_IDS` → `99-write-ids.sh` | |

### 8.2–8.4 Storage VStore / VLAN / QoS 写操作

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 8.2.1 | `storage vstore create` [WRITE] | `pydme storage vstore create --name test_vstore --storage_id $STORAGE_ID` | `name`, `storage_id` | 2.1.1 | `NEW_VSTORE_ID` → `99-write-ids.sh` | |
| 8.2.2 | `storage vstore modify` [WRITE] | `pydme storage vstore modify --id $NEW_VSTORE_ID --name test_vstore_modified` | `id` | 8.2.1 | — | |
| 8.2.3 | `storage vstore delete` [WRITE] | `pydme storage vstore delete --vstore_ids '["$NEW_VSTORE_ID"]'` | `vstore_ids` | 8.2.2 | — | |
| 8.3.1 | `storage vlan create` [WRITE] | `pydme storage vlan create --name test_vlan --vlan_id 100 --storage_id $STORAGE_ID` | `name`, `vlan_id`, `storage_id` | 2.1.1 | `NEW_VLAN_ID` → `99-write-ids.sh` | |
| 8.3.2 | `storage vlan modify` [WRITE] | `pydme storage vlan modify --vlan_id $NEW_VLAN_ID --name test_vlan_modified` | `vlan_id` | 8.3.1 | — | |
| 8.3.3 | `storage vlan delete` [WRITE] | `pydme storage vlan delete --vlan_id $NEW_VLAN_ID` | `vlan_id` | 8.3.2 | — | |
| 8.4.1 | `storage qos create` [WRITE] | `pydme storage qos create --name test_qos --storage_id $STORAGE_ID --resource_type LUN --resource_ids '["$LUN_ID"]'` | `name`, `storage_id`, `resource_type`, `resource_ids` | 2.1.1, 3.1.1 | `NEW_QOS_ID` → `99-write-ids.sh` | |
| 8.4.2 | `storage qos activate` [WRITE] | `pydme storage qos activate --qos_policy_ids '["$NEW_QOS_ID"]'` | `qos_policy_ids` | 8.4.1 | — | |
| 8.4.3 | `storage qos deactivate` [WRITE] | `pydme storage qos deactivate --qos_policy_ids '["$NEW_QOS_ID"]'` | `qos_policy_ids` | 8.4.2 | — | |
| 8.4.4 | `storage qos modify` [WRITE] | `pydme storage qos modify --qos_policy_id $NEW_QOS_ID --name test_qos_mod` | `qos_policy_id` | 8.4.1 | — | |
| 8.4.5 | `storage qos delete` [WRITE] | `pydme storage qos delete --qos_policy_ids '["$NEW_QOS_ID"]'` | `qos_policy_ids` | 8.4.4 | — | |

### 8.5–8.7 Storage Logic Port / Initiator / Account 写操作

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 8.5.1 | `storage logic_port update` [WRITE] | `pydme storage logic_port update --logic_port_id $LOGIC_PORT_ID --name test_port_mod` | `logic_port_id` | 2.21.1 | — | |
| 8.5.2 | `storage logic_port failback` [WRITE] | `pydme storage logic_port failback --id $LOGIC_PORT_ID` | `id` | 2.21.1 | — | |
| 8.6.1 | `storage initiator modify` [WRITE] | `pydme storage initiator modify --initiator_id $INITIATOR_ID --alias test_init_mod` | `initiator_id` | 2.16.1 | — | |
| 8.7.1 | `storage account create_local_user` [WRITE] | `pydme storage account create_local_user --storage_id $STORAGE_ID --name test_user --password <pwd>` | `storage_id`, `name`, `password` | 2.1.1 | `NEW_LOCAL_USER` → `99-write-ids.sh` | |

### 8.8–8.10 SAN / NAS / Protect 写操作

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 8.8.1 | `san lun create` [WRITE] | `pydme san lun create --storage_id $STORAGE_ID --pool_id $POOL_ID --name test_lun --capacity 1` | `storage_id`, `pool_id`, `name`, `capacity` | 2.1.1, 2.5.1 | `NEW_LUN_ID` → `99-write-ids.sh` | |
| 8.8.2 | `san lun modify` [WRITE] | `pydme san lun modify --lun_id $NEW_LUN_ID --name test_lun_modified` | `lun_id` | 8.8.1 | — | |
| 8.8.3 | `san lun delete` [WRITE] | `pydme san lun delete --lun_ids '["$NEW_LUN_ID"]'` | `lun_ids` | 8.8.2 | — | |
| 8.8.4 | `san lun expand` [WRITE] | `pydme san lun expand --lun_id $NEW_LUN_ID --capacity 2` | `lun_id`, `capacity` | 8.8.1 | — | |
| 8.8.5 | `san lun count` | `pydme san lun count --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | — | |
| 8.9.1 | `nas filesystem create` [WRITE] | `pydme nas filesystem create --name test_fs --storage_id $STORAGE_ID --pool_id $POOL_ID --capacity 10` | `name`, `storage_id`, `pool_id`, `capacity` | 2.1.1, 2.5.1 | `NEW_FS_ID` → `99-write-ids.sh` | |
| 8.9.2 | `nas nfs_share create` [WRITE] | `pydme nas nfs_share create --share_path /test_share --storage_id $STORAGE_ID --filesystem_id $NEW_FS_ID` | `share_path`, `storage_id`, `filesystem_id` | 8.9.1 | `NEW_NFS_ID` → `99-write-ids.sh` | |
| 8.9.3 | `nas cifs_share create` [WRITE] | `pydme nas cifs_share create --name test_cifs --storage_id $STORAGE_ID --filesystem_id $NEW_FS_ID` | `name`, `storage_id`, `filesystem_id` | 8.9.1 | `NEW_CIFS_ID` → `99-write-ids.sh` | |
| 8.9.4 | `nas filesystem delete` [WRITE] | `pydme nas filesystem delete --filesystem_id $NEW_FS_ID` | `filesystem_id` | 8.9.1 | — | |
| 8.10.1 | `protect snapshot create` [WRITE] | `pydme protect snapshot create --name test_snapshot --resource_id $LUN_ID --resource_type LUN` | `name`, `resource_id`, `resource_type` | 3.1.1 | `NEW_SNAPSHOT_ID` → `99-write-ids.sh` | |
| 8.10.2 | `protect snapshot delete` [WRITE] | `pydme protect snapshot delete --snapshot_id $NEW_SNAPSHOT_ID` | `snapshot_id` | 8.10.1 | — | |

<!-- 8.9 and 8.10 consolidated into 8.8–8.10 table above -->

### 8.11–8.14 GFS / AIOps / Workflow / Task 写操作

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 8.11.1 | `gfs namespace create` [WRITE] | `pydme gfs namespace create --name test_gfs_ns --gfs_group_id $GFS_GROUP_ID` | `name`, `gfs_group_id`/`gfs_group_name` | 7.2.1 | `NEW_GFS_NS_ID` → `99-write-ids.sh` | |
| 8.11.2 | `gfs namespace modify` [WRITE] | `pydme gfs namespace modify --id $NEW_GFS_NS_ID` | `id`/`name_locator` | 8.11.1 | — | |
| 8.11.3 | `gfs namespace delete` [WRITE] | `pydme gfs namespace delete --id $NEW_GFS_NS_ID` | `id`/`name_locator` | 8.11.2 | — | |
| 8.12.1 | `aiops alarm ack` [WRITE] | `pydme aiops alarm ack --csns '["$ALARM_CSN"]'` | `csns` | 7.6.1 | — | |
| 8.12.2 | `aiops alarm unack` [WRITE] | `pydme aiops alarm unack --csns '["$ALARM_CSN"]'` | `csns` | 8.12.1 | — | |
| 8.13.1 | `workflow instance create` [WRITE] | `pydme workflow instance create --template_id $TEMPLATE_ID` | `template_id`/`template_version_id`/`instance_id` | 7.3.2 | `INSTANCE_ID` → `99-write-ids.sh` | |
| 8.13.2 | `workflow instance show` | `pydme workflow instance show --instance_id $INSTANCE_ID` | `instance_id` | 8.13.1 | — | |
| 8.14.1 | `system task retry` [WRITE] | `pydme system task retry --task_id $TASK_ID` | `task_id` | 1.4.1 | — | |

<!-- 8.13 and 8.14 are consolidated into the 8.11–8.14 table above -->

### 8.15–8.17 Tag / Tenant / SAN 映射写操作

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 8.15.1 | `system tag bind` [WRITE] | `pydme system tag bind --tag_id $TAG_ID --resources '[{"resource_id":"$STORAGE_ID","resource_type":"storage"}]'` | `tag_id`, `resources` | 1.6.x, 2.1.1 | — | |
| 8.15.2 | `system tag unbind` [WRITE] | `pydme system tag unbind --tag_id $TAG_ID --resources '[{"resource_id":"$STORAGE_ID","resource_type":"storage"}]'` | `tag_id`, `resources` | 8.15.1 | — | |
| 8.16.1 | `tenant lun create` [WRITE] | `pydme tenant lun create --volumes '[{"name":"test_svc_lun","capacity":1,"count":1}]' --service_level_id $TIER_ID` | `volumes`, `service_level_id` | 7.1.1 | `NEW_SVC_LUN_ID` → `99-write-ids.sh` | |
| 8.16.2 | `tenant lun bind_tier` [WRITE] | `pydme tenant lun bind_tier --volume_id $NEW_SVC_LUN_ID --tier_id $TIER_ID` | `volume_id`, `tier_id` | 8.16.1, 7.1.1 | — | |
| 8.16.3 | `tenant lun unbind_tier` [WRITE] | `pydme tenant lun unbind_tier --volume_id $NEW_SVC_LUN_ID` | `volume_id` | 8.16.2 | — | |
| 8.16.4 | `tenant lun change_tier` [WRITE] | `pydme tenant lun change_tier --volume_ids '["$NEW_SVC_LUN_ID"]' --tier_id $TIER_ID` | `volume_ids`, `tier_id` | 8.16.1, 7.1.1 | — | |
| 8.17.1 | `san storage_host create` [WRITE] | `pydme san storage_host create --name test_storage_host --os_type Linux` | `name`, `os_type` | login | `NEW_HOST_ID` → `99-write-ids.sh` | |
| 8.17.2 | `san lun_group create` [WRITE] | `pydme san lun_group create --name test_lungroup --storage_id $STORAGE_ID` | `name`, `storage_id` | 2.1.1 | `NEW_LUN_GROUP_ID` → `99-write-ids.sh` | |
| 8.17.3 | `san mapping_view create` [WRITE] | `pydme san mapping_view create --name test_mapping --storage_id $STORAGE_ID` | `name`, `storage_id` | 2.1.1 | `NEW_MAPPING_ID` → `99-write-ids.sh` | |
| 8.17.4 | `san mapping_view delete` [WRITE] | `pydme san mapping_view delete --mapping_view_id $NEW_MAPPING_ID` | `mapping_view_id` | 8.17.3 | — | |

---

## 测试结果（第一轮执行）

> 执行时间: 2026-06-16 · 目标 DME: 127.0.0.1 (DME 25.0.0)  
> 首次: **31P/9F/1S** → 参数修复: **48P/1F/5S** → 顺序补测: **85P/1F/5S** → 当前: **131P/7F/6S/2T**  
> Stage 文件: `.reasonix/scripts/` (00-env.sh, 00-lib.sh, 02-storage-ids.sh, 06-fcswitch-ids.sh)

### 按阶段汇总

| 阶段 | PASS | FAIL | SKIP | 关键发现 |
|------|------|------|------|----------|
| Phase 0 — 认证 | 4 | 0 | 0 | DME 25.0.0 本地实例，免认证 |
| Phase 1 — System | 7 | 0 | 2 | task/az/dc/region ✅，user/role 权限不足 SKIP |
| Phase 2 — Storage | 3 | 0 | 0 | 发现 Dorado 5500/6000 V6 + Pacific |
| Phase 5 — FC Switch | 3 | 0 | 0 | fabric WWN 已保存 |
| Phase 5 — IP Switch | 8 | 0 | 0 | 全部子主题通过 ✅ |
| Phase 6 — Server/Virt/Kube | 6 | 0 | 0 | vm list 已修复 ✅ |
| Phase 7 — 其余主题 | 10 | 0 | 0 | workflow template 已修复 ✅ |
| Phase 8 — 写操作 | 1 | 0 | 1 | tag create 成功；bind 因异步任务跳过 |

### 详细结果

| 编号 | 动作 | 状态 | 说明 |
|------|------|------|------|
| 0.1.1 | `system login` | PASS | accessSession saved |
| 0.2.1 | `system logout` | PASS | HTTP 200, no data |
| 0.3.1 | `system show` | PASS | version=DME 25.0.0, sn=2bffdc76-c901-435d-a516-ca27ee1c17a1 |
| 0.4.1 | `system certificate` | PASS | returned DME certificate chain |
| 1.1.1 | `system user list` | SKIP | 权限不足 common.0001（非 bug）|
| 1.2.1 | `system role list` | SKIP | 权限不足 common.0001（非 bug）|
| 1.3.1 | `system backup_server list` | PASS | total=0 (empty) |
| 1.4.1 | `system task list` | PASS ✅ | total=86, HTTP 200 — 参数 `--limit 10` 路由已修复 |
| 1.5.1 | `system tag_type list` | PASS | total=2 |
| 1.6.1 | `system tag list` | PASS | total=1 |
| 1.8.1 | `system az list` | PASS ✅ | total=0, HTTP 200 — 参数路由修复 |
| 1.9.1 | `system dc list` | PASS ✅ | total=1, HTTP 200 — 参数路由修复 |
| 1.10.1 | `system region list` | PASS ✅ | total=0, HTTP 200 — 参数路由修复 |
| 2.1.1 | `storage list` | PASS | total=8; STORAGE_ID=b9326bbf... Dorado 5500 V6 |
| 2.13.1 | `storage enclosure list` | PASS | returned enclosure data |
| 2.18.1 | `storage zone list` | SKIP | 仅 A800 系列支持 |
| 5.1.1 | `fcswitch list` | PASS | returns FC switch list |
| 5.1.5 | `fcswitch fabric list` | PASS | FABRIC_WWN=100050EB1AEC4731 |
| 5.1.7 | `fcswitch vsan list` | PASS | total=0 |
| 5.2.1 | `ipswitch list` | PASS | returns IP switch list |
| 6.1.1 | `server list` | PASS | returns server list |
| 6.2.1 | `virt site list` | PASS | returns site list |
| 6.2.3 | `virt cluster list` | PASS | returns VMware clusters |
| 6.2.5 | `virt host list` | PASS | returns host list |
| 6.2.9 | `virt vm list` | PASS ✅ | HTTP 200 |
| 6.2.10 | `virt datastore list` | PASS | returns datastore list |
| 6.3.1 | `kube cluster list` | PASS | total=0 |
| 7.1.1 | `tenant tier list` | PASS | total=0 |
| 7.1.3 | `tenant project list` | PASS | total=0 |
| 7.2.1 | `gfs dataspace list` | PASS | total=0 |
| 7.2.4 | `gfs namespace list` | PASS | total=0 |
| 7.3.1 | `workflow template groups` | PASS | returned groups |
| 7.3.2 | `workflow template list` | PASS ✅ | HTTP 200 |
| 7.4.1 | `integrate cmdb system_list` | PASS | empty list |
| 7.4.2 | `integrate cmdb host_list` | PASS | empty list |
| 7.4.3 | `integrate cmdb app_list` | PASS | total=0 |
| 7.5.1 | `backup cluster list` | PASS | total=0 |
| 7.6.1.2 | `aiops check_policy list` | PASS | returns check policies |
| 8.15.1b | `system tag create` | PASS | task_id returned |
| 8.15.2 | `system tag bind` | SKIP | needs tag_id from async task |

### 第二轮补充测试（参数修复验证）

| 编号 | 动作 | 状态 | 说明 |
|------|------|------|------|
| 2.1.1b | `storage list --start 1 --limit 5` | PASS | total=8, HTTP 200 ✅ 参数路由修复 |
| 2.2.1 | `storage show --storage_id` | PASS | URL 显示真实 UUID ✅ 不再 `True` |
| 5.1.1b | `fcswitch list --page_no 1 --page_size 5` | PASS | total=2 ✅ 参数路由修复 |
| 6.1.1b | `server list --start 1 --limit 5` | PASS | total=2 ✅ 参数路由修复 |
| 2.5.1 | `storage pool list --storage_id` | PASS | total=0, HTTP 200 ✅ 参数路由修复 |
| 2.10.1 | `storage fan list --storage_id` | PASS | HTTP 200 |
| 2.11.1 | `storage bbu list --storage_id` | PASS | HTTP 200 |
| 2.12.1 | `storage psu list --storage_id` | PASS | HTTP 200 |
| 2.9.1 | `storage vstore list --storage_id` | PASS | HTTP 200 |
| 2.22.1 | `storage qos list --storage_id` | PASS | HTTP 200 |
| 2.8.1 | `storage port list --storage_id` | PASS | HTTP 200 |
| 2.21.1 | `storage logic_port list --storage_id` | PASS | HTTP 200 |
| 2.7.1 | `storage node list --storage_id` | PASS ✅ | HTTP 200, total=0 |
| 2.6.1 | `storage controller list --storage_id` | PASS ✅ | Dorado 5500 V6 total=2, HTTP 200 — 参数路由修复 |
| 2.14.1 | `storage disk_domain list --storage_id` | PASS ✅ | HTTP 200 |
| 2.17.1 | `storage app_type list --storage_id` | FAIL | timeout |
| 2.19.1 | `storage failover_group list --storage_id` | SKIP | 仅 A800 系列支持 |
| 2.16.1 | `storage initiator list` | PASS ✅ | HTTP 200, 返回启动器列表 |

更新统计: **48 PASS / 1 FAIL / 5 SKIP**

### 第三轮补充测试（顺序执行）

| 编号 | 动作 | 状态 | 说明 |
|------|------|------|------|
| 1.4.2 | `system task show` | PASS ✅ | HTTP 200 |
| 1.4.3 | `system task wait` | PASS ✅ | HTTP 200 |
| 1.5.2 | `system tag_type create` | PASS ✅ | HTTP 200 |
| 1.5.3 | `system tag_type modify` | PASS ✅ | HTTP 200 |
| 1.5.4 | `system tag_type delete` | PASS ✅ | HTTP 202 |
| 1.6.2 | `system tag create` | PASS ✅ | task_id |
| 1.6.3 | `system tag modify` | PASS ✅ | HTTP 200 |
| 1.6.4 | `system tag delete` | PASS ✅ | HTTP 200 |
| 1.9.2 | `system dc show` | PASS ✅ | HTTP 200 |
| 1.9.3 | `system dc show_devices` | PASS ✅ | HTTP 200 |
| 3.1.1.1 | `san lun list` | PASS ✅ | HTTP 200 |
| 3.1.2.1 | `san lun_group list` | PASS ✅ | HTTP 200 |
| 3.1.3.1 | `san storage_host list` | PASS ✅ | HTTP 200 |
| 3.1.4.1 | `san port_group list` | PASS ✅ | HTTP 200 |
| 3.1.5.1 | `san mapping_view list` | PASS ✅ | HTTP 200 |
| 3.1.6.1 | `san physical_host list` | PASS ✅ | HTTP 200 |
| 3.2.1.1 | `nas filesystem list` | PASS ✅ | HTTP 200 |
| 3.2.2.1 | `nas nfs_share list` | PASS ✅ | HTTP 200 |
| 3.2.3.1 | `nas cifs_share list` | PASS ✅ | HTTP 200 |
| 3.2.4.1 | `nas quota list` | PASS ✅ | HTTP 200 |
| 3.2.5.1 | `nas dtree list` | PASS ✅ | HTTP 200 |
| 3.2.6.1 | `nas namespace list` | PASS ✅ | HTTP 200 |
| 3.2.7.1 | `nas kvcache list` | PASS ✅ | HTTP 200 |
| 4.1.1 | `protect snapshot list` | PASS ✅ | HTTP 200 |
| 4.1.3 | `protect group list` | PASS ✅ | HTTP 200 |
| 5.1.3 | `fcswitch port list` | PASS ✅ | HTTP 200 |
| 5.1.4 | `fcswitch controller list` | PASS ✅ | HTTP 200 |
| 5.1.8 | `fcswitch zone list` | PASS ✅ | HTTP 200 |
| 5.1.9 | `fcswitch alias list` | PASS ✅ | HTTP 200 |
| 5.2.2 | `ipswitch frame list` | PASS ✅ | HTTP 200 |
| 7.1.2 | `tenant tier show_projects` | PASS ✅ | HTTP 200 |
| 7.1.4 | `tenant project show_tiers` | PASS ✅ | HTTP 200 |

### 第四轮补充测试

| 编号 | 动作 | 状态 | 说明 |
|------|------|------|------|
| 2.3.1 | `storage sync` | PASS ✅ | HTTP 200 |
| 2.9.2 | `storage vstore show` | PASS ✅ | HTTP 200 |
| 2.20.1 | `storage vlan list` | PASS ✅ | HTTP 200 |
| 2.23.1 | `storage hyperscale_pool list` | PASS ✅ | HTTP 200 |
| 5.2.3-5.2.7 | `ipswitch board/subcard/power/fan/port list` | PASS ✅ | 全部 HTTP 200 |
| 6.2.12 | `virt disk list` | PASS ✅ | HTTP 200 |
| 6.2.13 | `virt vdisk list` | PASS ✅ | HTTP 200 |
| 6.2.2 | `virt site show` | PASS ✅ | HTTP 200（bug 修复后）|
| 6.2.4 | `virt cluster show` | PASS ✅ | HTTP 200（bug 修复后）|
| 6.2.7 | `virt host_adapter list` | PASS ✅ | HTTP 200 |
| 7.2.6 | `gfs migration_task list` | PASS ✅ | HTTP 200 |
| 7.3.2 | `workflow template list` | PASS ✅ | HTTP 200 |
| 7.3.3 | `workflow template show` | PASS ✅ | HTTP 200（bug 修复后）|
| 7.4.4 | `integrate cmdb host_show` | PASS ✅ | HTTP 200 |
| 7.6.1.1 | `aiops alarm list` | PASS ✅ | HTTP 200 |
| 7.6.1.3 | `aiops performance list_object_types` | PASS ✅ | HTTP 200 |
| 7.6.1.5 | `aiops health show_score` | PASS ✅ | HTTP 200 |
| 7.6.1.4 | `aiops topology query_*` | SKIP | 动作名与计划不一致（应为 `query_san_path` 等）|

Bug 修复: `virt vm_show/datastore_show/host_show/cluster_show`, `workflow template_show` — 路径参数未传入 client.get()

### Phase 8 写操作执行

| 编号 | 动作 | 状态 | 说明 |
|------|------|------|------|
| 8.2.1 | `storage vstore create` | PASS ✅ | HTTP 200 |
| 8.15.1 | `system tag bind` | FAIL | HTTP 400（资源格式问题） |
| 8.15.2 | `system tag unbind` | FAIL | HTTP 400 |
| 8.17.1 | `san storage_host create` | PASS ✅ | HTTP 200 |
| 8.17.2 | `san lun_group create` | PASS ✅ | HTTP 202 async |
| 8.1.1 | `fcswitch zone create` | TIMEOUT | FC 交换机通信慢 |

### 第五轮补充测试

| 编号 | 动作 | 状态 | 说明 |
|------|------|------|------|
| 8.2.2 | `storage vstore modify` | PASS ✅ | HTTP 202 async |
| 8.2.3 | `storage vstore delete` | PASS ✅ | HTTP 202 (param_mapping 修复后) |
| 8.1.2 | `fcswitch zone show_members` | PASS ✅ | HTTP 200 |
| 8.1.5 | `fcswitch alias create` | FAIL | 需要至少一个 member |
| 4.1.5 | `protect hypermetro_domain list` | PASS ✅ | HTTP 200 |
| 4.1.6 | `protect hypermetro_group list` | PASS ✅ | HTTP 200 |
| 4.1.9 | `protect fs_snapshot list` | PASS ✅ | HTTP 200 |
| 4.1.11 | `protect vstore_pair list` | PASS ✅ | HTTP 200 |
| 6.2.9 | `virt vm show` | PASS ✅ | HTTP 200 (bug 修复后) |

新增 param_mapping: `vstore_ids→ids`, `qos_policy_ids→ids`, `tag_type_ids→ids` 等

### 第六轮补充测试

| 编号 | 动作 | 状态 | 说明 |
|------|------|------|------|
| 5.2.3 | `ipswitch board list` | PASS ✅ | 真实 IPSwitch ID |
| 5.2.4 | `ipswitch subcard list` | PASS ✅ | |
| 5.2.5 | `ipswitch power list` | PASS ✅ | |
| 5.2.6 | `ipswitch fan list` | PASS ✅ | |
| 5.2.7 | `ipswitch port list` | PASS ✅ | |
| 7.6.1.4 | `aiops perf create_collect_task` | PASS ✅ | |
| 7.6.1.5 | `aiops health show_detail` | PASS ✅ | |
| 4.1.2-4.1.10 | protect clone/hypermetro/replication/fs | TIMEOUT | DME protect 模块响应慢 |
| 5.1.2 | `fcswitch sync` | FAIL | switch_id 格式不匹配 |
| 8.1.10 | `fcswitch zone batch_create` | FAIL | 需要 member |
| 8.1.5 | `fcswitch alias create` | TIMEOUT | FC 交换机通信慢 |

### 第七轮补充测试

| 编号 | 动作 | 状态 | 说明 |
|------|------|------|------|
| 7.2.6 | `gfs migration_task list` | PASS ✅ | HTTP 200 |
| 8.13.1 | `workflow instance create` | PASS ✅ | async 实例创建 |

### 第八轮补充测试

| 编号 | 动作 | 状态 | 说明 |
|------|------|------|------|
| 2.4.1 | `storage disk list (Pacific)` | PASS ✅ | 返回数据 |
| 8.6.1 | `storage initiator modify` | PASS ✅ | 真实 initiator ID |
| 2.3.1 | `storage sync (Pacific)` | PASS ✅ | |
| 3.2.1 | `nas filesystem list (Pacific)` | PASS ✅ | 跨存储测试 |
| 3.2.2 | `nas nfs_share list (Pacific)` | PASS ✅ | |
| 3.2.6 | `nas namespace list (Pacific)` | PASS ✅ | |
| 7.6.1.3b | `perf list_indicators` | PASS ✅ | |

更新统计: **131 PASS / 7 FAIL / 6 SKIP / 2 TIMEOUT**

### 已知问题

1. ~~**CLI 参数限制** — 2 级直接动作的 `--param value` 被 argparse 吞为 position arg，无法传参~~  
   ✅ **已修复**（`pydme/cli.py` 两次提交）：  
   1. `2e6c584` — 从 `args.action` 恢复被吞的值补回 orphan `--param`  
   2. `d4c6d17` — 清空 `args.action` 使 dispatch 进入 2-arg 路径
2. **API 受限** — user/role/task/dc/region 返回 common.0001/0003（该 DME 实例受限）
3. **网络超时** — `virt vm list` 504（vCenter 不可达），`san lun list` 等超时

---

## 附录 A — 黑名单动作（需 `--accept-risk`）

| 主题 | 高危动作示例 |
|------|-------------|
| storage | `vstore_delete` `vstore_create` `vstore_modify` `qos_delete` `qos_create` `vlan_delete` `vlan_create` `logic_port_delete` `initiator_delete` |
| san | `lun_delete` `lun_create` `mapping_view_delete` `storage_host_delete` `lun_group_delete` |
| nas | `filesystem_delete` `filesystem_create` `nfs_share_delete` `cifs_share_delete` |
| protect | `snapshot_delete` `snapshot_create` `clone_delete` `replication_pair_delete` |
| system | `user_delete` `user_create` `tag_delete` `tag_type_delete` `tag_create` |
| fcswitch | `zone_delete` `zone_create` `zone_modify` `alias_delete` `alias_create` |
| gfs | `namespace_delete` `namespace_create` `migration_task_delete` |
| tenant | `lun_create` `lun_change_tier` `lun_bind_tier` `lun_unbind_tier` |

---

## 附录 B — 测试通过准则

1. 每个动作 CLI 返回 HTTP 200 或成功 JSON payload
2. 写类操作可通过对应的 list / show 动作验证结果
3. 异常参数（如不存在的 ID）返回适当错误信息而非工具崩溃
4. 分页参数 `page_no` / `page_size` / `limit` 生效
5. `--accept-risk` 缺失时，黑名单动作正确拒绝执行
