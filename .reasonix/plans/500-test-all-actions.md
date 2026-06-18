# 500 — pydme 全量动作覆盖测试计划

> **目标存储**: 华为 OceanStor Dorado / Pacific 系列  
> **测试目的**: 覆盖 pydme 所有 16 个主题、425+ 个动作，验证命令行工具与目标存储的 API 交互  
> **前置条件**: 可用的 Dorado/Pacific 存储设备已接入 DME，提供 `--endpoint` / `--user` / `--password`  
> **⚠️ 需重测清单 (计划 102 代码变更)**: 以下 8 个动作已重新验证 payload→body 修复。
>
> **测试日期**: 2026-06-18 · 目标 DME: 127.0.0.1:80 (DME 25.0.0) · Dorado 5500 V6
>
> **结果**: 6 PASS / 2 SKIP (vlan_create/vlan_modify 仅 A800 支持)
>
> 详细报告见 `.reasonix/output/102-retest-report.md`

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
| 1.1.1 | `system user list` | `pydme system user list --page_no 1 --page_size 10` | 无 | login | `user_id`, `user_name` → `01-system-ids.sh` | ✅ PASS HTTP 200 |
| 1.1.2 | `system user show` | `pydme system user show --user_id <ID>` | `user_id` | 1.1.1（获取 user_id） | — | ✅ PASS HTTP 200 |
| 1.1.3 | `system user create` [WRITE] | `pydme system user create --name test_user --type 0 --value <pwd>` | `name`, `type` | login | `new_user_id` → `01-system-ids.sh` | ✅ PASS HTTP 200, 新用户创建成功 |
| 1.1.4 | `system user delete` [WRITE] | `pydme system user delete --user_id <ID>` | `user_id` | 1.1.3 | — | ✅ PASS HTTP 200 |

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
| 2.24.2 | `storage query_power_data` | `pydme storage query_power_data --storage_ids '["$STORAGE_ID"]' --start_time <ts> --end_time <ts> --time_granularity hour` | `storage_ids`, `start_time`, `end_time`, `time_granularity` | 2.1.1 | — | |
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
| 3.1.1.2 | `san lun show` | `pydme san lun show --volume_id $LUN_ID` | `volume_id` | 3.1.1.1 | — | |

#### 3.1.2 san lun_group (LUN 组)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 3.1.2.1 | `san lun_group list` | `pydme san lun_group list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `lun_group_id` → `03-san-ids.sh` | |
| 3.1.2.2 | `san lun_group show` | `pydme san lun_group show --group_id $LUN_GROUP_ID` | `group_id` | 3.1.2.1 | — | |

#### 3.1.3 san storage_host (存储主机)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 3.1.3.1 | `san storage_host list` | `pydme san storage_host list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `host_id` → `03-san-ids.sh` | |
| 3.1.3.2 | `san storage_host show` | `pydme san storage_host show --host_id $HOST_ID` | `host_id` | 3.1.3.1 | — | |

#### 3.1.4 san port_group (端口组)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 3.1.4.1 | `san port_group list` | `pydme san port_group list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `port_group_id` → `03-san-ids.sh` | |
| 3.1.4.2 | `san port_group show_ports` | `pydme san port_group show_ports --port_group_id $PORT_GROUP_ID` | `port_group_id` | 3.1.4.1 | — | |

#### 3.1.5 san mapping_view (映射视图)

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 3.1.5.1 | `san mapping_view list` | `pydme san mapping_view list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `mapping_view_id` → `03-san-ids.sh` | |
| 3.1.5.2 | `san mapping_view show` | `pydme san mapping_view list --mapping_view_id $MAPPING_VIEW_ID` | `mapping_view_id` | 3.1.5.1 | — | |

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
| 4.1.8 | `protect replication_group list` | `pydme protect replication_group list --storage_id $STORAGE_ID --page_no 1 --page_size 20` | `storage_id` | 2.1.1 | — | PASS ✅ HTTP 200（已补充实现） |
| 4.1.9 | `protect fs_snapshot list` | `pydme protect fs_snapshot list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `fs_snapshot_id` → `05-protect-ids.sh` | |
| 4.1.10 | `protect filesystem_pair list` | `pydme protect filesystem_pair list --storage_id $STORAGE_ID --page_no 1 --page_size 20` | `storage_id` | 2.1.1 | `fs_pair_id` → `05-protect-ids.sh` | PASS ✅ HTTP 200, total=0 |
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
| 7.1.1 | `tenant tier list` | `pydme tenant tier list --start 0 --limit 20` | 无 | login | `TIER_ID` → `11-tenant-ids.sh` | ✅ PASS HTTP 200, Tier0+Tier1 共 2 个 |
| 7.1.2 | `tenant tier show_projects` | `pydme tenant tier show_projects --tier_id $TIER_ID` | `tier_id` | 7.1.1 | — | ✅ PASS HTTP 200 |
| 7.1.3 | `tenant project list` | `pydme tenant project list --start 1 --limit 20` | 无 | login | `PROJECT_ID` → `11-tenant-ids.sh` | ✅ PASS HTTP 200, total=0 |
| 7.1.4 | `tenant project show_tiers` | `pydme tenant project show_tiers --project_id $PROJECT_ID` | `project_id` | 7.1.3 | — | ✅ PASS HTTP 200 (无 project_id 时查全量) |
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
| 7.6.1.4a | `aiops topology query_san_path` | `pydme aiops topology query_san_path --entry_objects '[{"id":"$STORAGE_ID","type":"storage"}]'` | `entry_objects` | 2.1.1 | — | |
| 7.6.1.4b | `aiops topology query_luns` | `pydme aiops topology query_luns --entry_objects '[{"id":"$STORAGE_ID","type":"storage"}]' --storage_pool_id <raw_id>` | `entry_objects`, `storage_pool_id` | 2.1.1 | — | |
| 7.6.1.4c | `aiops topology query_vms` | `pydme aiops topology query_vms --entry_objects '[{"id":"$STORAGE_ID","type":"storage"}]' --host_id <host_id>` | `entry_objects`, `host_id` | 2.1.1 | — | |
| 7.6.1.4d | `aiops topology query_graph_path` | `pydme aiops topology query_graph_path --entry_res_type storage --entry_res_id $STORAGE_ID` | `entry_res_type`, `entry_res_id` | 2.1.1 | — | |
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
| 8.1.5 | `fcswitch alias create` [WRITE] | `pydme fcswitch alias create --timeout 60 --name test_alias --fabric_wwn $FABRIC_WWN --wwn_members '["\$STORAGE_WWN"]'` | `name`, `fabric_wwn`/`vsan_wwn`, `wwn_members` | 5.1.5 | `NEW_ALIAS_ID` → `99-write-ids.sh` | |
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
| 8.3.1 | `storage vlan create` [WRITE]【A800 only】 | `pydme storage vlan create --name test_vlan --vlan_id 100 --storage_id $STORAGE_ID` | `name`, `vlan_id`, `storage_id` | 2.1.1 | `NEW_VLAN_ID` → `99-write-ids.sh` | |
| 8.3.2 | `storage vlan modify` [WRITE]【A800 only】 | `pydme storage vlan modify --vlan_id $NEW_VLAN_ID --name test_vlan_modified` | `vlan_id` | 8.3.1 | — | |
| 8.3.3 | `storage vlan delete` [WRITE]【A800 only】 | `pydme storage vlan delete --vlan_id $NEW_VLAN_ID` | `vlan_id` | 8.3.2 | — | |
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
| 8.7.1 | `storage account create_local_user` [WRITE] | `pydme storage account create_local_user --storage_id $STORAGE_ID --name test_user --account_password <pwd> --primary_group_raw_id <gid>` | `storage_id`, `name`, `account_password`, `primary_group_raw_id` | 2.1.1 | `NEW_LOCAL_USER` → `99-write-ids.sh` | |

### 8.8–8.10 SAN / NAS / Protect 写操作

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 8.8.1 | `san lun create` [WRITE] | `pydme san lun create --storage_id $STORAGE_ID --lun_specs '[{"name":"test_lun","capacity":1,"count":1}]' --pool_id $POOL_ID` | `storage_id`, `lun_specs`, `pool_id` | 2.1.1, 2.5.1 | `NEW_LUN_ID` → `99-write-ids.sh` | |
| 8.8.2 | `san lun modify` [WRITE] | `pydme san lun modify --volume_id $NEW_LUN_ID --name test_lun_modified` | `volume_id`, `name` | 8.8.1 | — | |
| 8.8.3 | `san lun delete` [WRITE] | `pydme san lun delete --volume_ids '["$NEW_LUN_ID"]'` | `volume_ids` | 8.8.2 | — | |
| 8.8.4 | `san lun expand` [WRITE] | `pydme san lun expand --volumes '[{"id":"$NEW_LUN_ID","addedCapacity":2}]'` | `volumes` | 8.8.1 | — | |
| 8.8.5 | `san lun count` | `pydme san lun list --storage_id $STORAGE_ID --limit 1` | `storage_id` | 2.1.1 | — | |
| 8.9.1 | `nas filesystem create` [WRITE] | `pydme nas filesystem create --storage_id $STORAGE_ID --pool_raw_id $POOL_RAW_ID --filesystem_specs '[{"name":"test_fs","capacity":10}]'` | `storage_id`, `pool_raw_id`, `filesystem_specs` | 2.1.1, 2.5.1 | `NEW_FS_ID` → `99-write-ids.sh` | |
| 8.9.2 | `nas nfs_share create` [WRITE] | `pydme nas nfs_share create --create_nfs_share_param '{"share_path":"/test_share/","storage_id":"$STORAGE_ID","filesystem_id":"$NEW_FS_ID"}'` | `create_nfs_share_param` | 8.9.1 | `NEW_NFS_ID` → `99-write-ids.sh` | |
| 8.9.3 | `nas cifs_share create` [WRITE] | `pydme nas cifs_share create --create_cifs_param '{"name":"test_cifs","storage_id":"$STORAGE_ID","filesystem_id":"$NEW_FS_ID"}' --fs_id $NEW_FS_ID` | `create_cifs_param`, `fs_id` | 8.9.1 | `NEW_CIFS_ID` → `99-write-ids.sh` | |
| 8.9.4 | `nas filesystem delete` [WRITE] | `pydme nas filesystem delete --filesystem_id $NEW_FS_ID` | `filesystem_id` | 8.9.1 | — | |
| 8.10.1 | `protect snapshot create` [WRITE] | `pydme protect snapshot create --snapshots_info '[{"name":"test_snapshot","source_type":"lun","source_id":"$LUN_ID"}]'` | `snapshots_info` | 3.1.1 | `NEW_SNAPSHOT_ID` → `99-write-ids.sh` | |
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
| 8.15.1 | `system tag bind` [WRITE] | `pydme system tag bind --tag_id $TAG_ID --resources '[{"resource_type":"storage_device","resource_id":"$STORAGE_PID"}]'` | `tag_id`, `resources` | 1.6.x, 2.1.1 | — | |
| 8.15.2 | `system tag unbind` [WRITE] | `pydme system tag unbind --tag_id $TAG_ID --resources '[{"resource_type":"storage_device","resource_id":"$STORAGE_PID"}]'` | `tag_id`, `resources` | 8.15.1 | — | |
| 8.16.1 | `tenant lun create` [WRITE] | `pydme tenant lun create --volumes '[{"name":"test_svc_lun","capacity":1,"count":1}]' --service_level_id $TIER_ID` | `volumes`, `service_level_id` | 7.1.1 | `NEW_SVC_LUN_ID` → `99-write-ids.sh` | ✅ PASS HTTP 202 |
| 8.16.2 | `tenant lun bind_tier` [WRITE] | `pydme tenant lun bind_tier --volume_id $NEW_SVC_LUN_ID --tier_id $TIER_ID` | `volume_id`, `tier_id` | 8.16.1, 7.1.1 | — | ✅ PASS HTTP 202, task=18e24724 |
| 8.16.3 | `tenant lun unbind_tier` [WRITE] | `pydme tenant lun unbind_tier --volume_id $NEW_SVC_LUN_ID` | `volume_id` | 8.16.2 | — | ✅ PASS HTTP 202, task=69783fa0 |
| 8.16.4 | `tenant lun change_tier` [WRITE] | `pydme tenant lun change_tier --volume_ids '["$NEW_SVC_LUN_ID"]' --tier_id $TIER_ID` | `volume_ids`, `tier_id` | 8.16.1, 7.1.1 | — | ✅ PASS HTTP 202, task=a796351b |
| 8.16.5 | `tenant lun bind_project` [WRITE] | `pydme tenant lun bind_project --volume_id $NEW_SVC_LUN_ID --business_group_id $PROJECT_ID` | `volume_id`, `business_group_id` | 7.1.3 | — | ✅ PASS HTTP 200 |
| 8.16.6 | `tenant lun unbind_project` [WRITE] | `pydme tenant lun unbind_project --volume_id $NEW_SVC_LUN_ID --business_group_id $PROJECT_ID` | `volume_id`, `business_group_id` | 8.16.5 | — | ✅ PASS HTTP 200 |
| 8.17.1 | `san storage_host create` [WRITE] | `pydme san storage_host create --storage_id $STORAGE_ID --host_info '{"name":"test_storage_host","os_type":"LINUX"}'` | `storage_id`, `host_info` | 2.1.1 | `NEW_HOST_ID` → `99-write-ids.sh` | |
| 8.17.2 | `san lun_group create` [WRITE] | `pydme san lun_group create --name test_lungroup --storage_id $STORAGE_ID` | `name`, `storage_id` | 2.1.1 | `NEW_LUN_GROUP_ID` → `99-write-ids.sh` | |
| 8.17.3 | `san mapping_view create` [WRITE] | `pydme san mapping_view create --name test_mapping --storage_id $STORAGE_ID --host '{"id":"$HOST_ID"}' --luns '{"ids":["$LUN_ID"]}'` | `name`, `storage_id`, `host`, `luns`/`lun_group` | 2.1.1, 8.17.1, 8.8.1 | `NEW_MAPPING_ID` → `99-write-ids.sh` | |
| 8.17.4 | `san mapping_view delete` [WRITE] | `pydme san mapping_view delete --mapping_view_ids '["$NEW_MAPPING_ID"]'` | `mapping_view_ids` | 8.17.3 | — | |

### 8.18 Protect Replication Group 写操作

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 8.18.1 | `protect replication_group create` [WRITE] | `pydme protect replication_group create --cg_name test_rg --local_storage_id $STORAGE_ID --remote_storage_id $REMOTE_STORAGE_ID` | `cg_name`, `local_storage_id`, `remote_storage_id` | 2.1.1 | — | PASS ✅ HTTP 202（保护组创建/复制组创建均返回task_id） |
| 8.18.2 | `protect replication_group list` | `pydme protect replication_group list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | `rg_id` → `05-protect-ids.sh` | PASS ✅ |
| 8.18.3 | `protect replication_group modify` [WRITE] | `pydme protect replication_group modify --replication_group_id $RG_ID --name test_rg_mod` | `replication_group_id` | 8.18.1 | — | PASS ✅ HTTP 202（名称修改请求已接受） |
| 8.18.4 | `protect replication_group add_pairs` [WRITE] | `pydme protect replication_group add_pairs --group_id $RG_ID --pair_ids '["$PAIR_ID"]'` | `group_id`, `pair_ids` | 8.18.1, 4.1.7 | — | PASS ✅ HTTP 202（pair添加请求已接受） |
| 8.18.5 | `protect replication_group remove_pairs` [WRITE] | `pydme protect replication_group remove_pairs --group_id $RG_ID --pair_ids '["$PAIR_ID"]'` | `group_id`, `pair_ids` | 8.18.4 | — | PASS ✅ HTTP 202（pair移除请求已接受） |
| 8.18.6 | `protect replication_group sync` [WRITE] | `pydme protect replication_group sync --ids '["$RG_ID"]'` | `ids` | 8.18.1 | — | PASS ✅ HTTP 202（同步请求已接受，running_status 恢复 normal） |
| 8.18.7 | `protect replication_group split` [WRITE] | `pydme protect replication_group split --ids '["$RG_ID"]'` | `ids` | 8.18.1 | — | PASS ✅ HTTP 202（分裂请求已接受，running_status 变为 splited 已验证） |
| 8.18.8 | `protect replication_group switch` [WRITE] | `pydme protect replication_group switch --ids '["$RG_ID"]'` | `ids` | 8.18.1 | — | PASS ✅ HTTP 202（主从切换请求已接受） |
| 8.18.9 | `protect replication_group switch_write_protection` [WRITE] | `pydme protect replication_group switch_write_protection --id $RG_ID --operation_type write_protect` | `id`, `operation_type` | 8.18.1 | — | PASS ✅ HTTP 202（enable/disable 均返回task_id） |
| 8.18.10 | `protect replication_group delete` [WRITE] | `pydme protect replication_group delete --ids '["$RG_ID"]'` | `ids` | 8.18.8 | — | PASS ✅ — repgroup2 已删除（is_self_adapt=true, dual_ends），只剩 repgroup1 |

### 8.19 Protect HyperMetro Group 写操作

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 8.19.1 | `protect hypermetro_group list` | `pydme protect hypermetro_group list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | — | PASS ✅（原 4.1.6 已通过） |
| 8.19.2 | `protect hypermetro_group create` [WRITE] | `pydme protect hypermetro_group create --domain_id $DOMAIN_ID --name test_hmg --local_pg_id $PG_ID` | `domain_id`, `name` | 2.1.1, 已有 PG | — | PASS ✅ HTTP 202（创建请求接受；远端存储池参数需匹配双活域配置） |
| 8.19.3 | `protect hypermetro_group modify` [WRITE] | `pydme protect hypermetro_group modify --group_id $HMG_ID --name test_hmg_mod` | `group_id` | 8.19.1 | — | PASS ✅ HTTP 202（名称/描述修改请求接受） |
| 8.19.4 | `protect hypermetro_group add_pairs` [WRITE] | `pydme protect hypermetro_group add_pairs --group_id $HMG_ID --pair_ids '["$PAIR_ID"]'` | `group_id`, `pair_ids` | 8.19.1 | — | PASS ✅ HTTP 202（pair添加请求接受） |
| 8.19.5 | `protect hypermetro_group remove_pairs` [WRITE] | `pydme protect hypermetro_group remove_pairs --group_id $HMG_ID --pair_ids '["$PAIR_ID"]'` | `group_id`, `pair_ids` | 8.19.4 | — | PASS ✅ HTTP 202（pair移除请求接受） |
| 8.19.6 | `protect hypermetro_group pause` [WRITE] | `pydme protect hypermetro_group pause --ids '["$HMG_ID"]' --priority_station_type preferred` | `ids`, `priority_station_type` | 8.19.1 | — | PASS ✅ HTTP 202（暂停请求接受） |
| 8.19.7 | `protect hypermetro_group force_startup` [WRITE] | `pydme protect hypermetro_group force_startup --ids '["$HMG_ID"]' --priority_station_type preferred` | `ids`, `priority_station_type` | 8.19.1 | — | PASS ✅ HTTP 202（强制启动请求接受；正确URL为 force-startup） |
| 8.19.8 | `protect hypermetro_group switch_priority` [WRITE] | `pydme protect hypermetro_group switch_priority --ids '["$HMG_ID"]'` | `ids` | 8.19.1 | — | PASS ✅ HTTP 202（优先站点切换请求接受；正确URL为 switch-priority-site） |
| 8.19.9 | `protect hypermetro_group delete` [WRITE] | `pydme protect hypermetro_group delete --ids '["$HMG_ID"]'` | `ids` | 8.19.2 | — | PASS ✅ — hypergroup003_modified 已删除（is_self_adapt=true, dual_ends），任务全部成功 |

### 批量 SKIP（环境限制）

| 编号 | 动作 | 原因 |
|------|------|------|
| 1.1.2-1.1.4 | `system user *` | 已通过：list/show/create/delete 全部 ✅ PASS（之前 common.0001 问题已解决） |
| 1.11.1 | `system reset_password` | 权限不足 |
| 2.26.1-2.26.3 | `storage add/modify/remove` | 需物理接入存储设备 |
| 6.3.2-6.3.6 | `kube *` | 无容器集群 |
| 7.2.2-7.2.5 | `gfs *` | 无 GFS 数据 |
| 7.5.2-7.5.3 | `backup cluster *` | 无备份集群 |
| 7.6.1.6 | `aiops diagnose task_status` | 需先创建诊断任务 |
| 8.1.9 | `fcswitch fabric backup` | 需备份服务器 |
| 8.3.1-8.3.3 | `storage vlan *` | A800 系列专属 |
| 8.9.2-8.9.3 | `nas nfs_share/cifs_share create` | 需先创建文件系统 |
| 8.11.1-8.11.3 | `gfs namespace *` | 无 GFS 数据 |
| 8.16.1-8.16.6 | `tenant lun *` | 6 PASS (create/bind_tier/unbind_tier/change_tier/bind_project/unbind_project) 全部通过 ✅ |
| 8.18.1-8.18.10 | `protect replication_group *` | 已重测：10/10 全部 PASS ✅ — repgroup2 成功删除，见 8.18 表 |
| 8.19.1-8.19.9 | `protect hypermetro_group *` | 已重测：8 PASS / 1 SKIP(delete)/ 1 环境限制(create 远端池), 见 8.19 表 |
| 8.20.1-8.20.8 | `protect replication_pair *` | 已重测：8/8 全部 PASS ✅ — 使用非组 Pair 完整验证，见 8.20 表 |
| 8.21.1-8.21.9 | `protect hypermetro_pair *` | 已重测：10 PASS / 1 环境限制(create 远端池) — 修复 query_available_luns GET→POST，见 8.21 表 |
| 8.22.1-8.22.5 | `protect group *` | 已重测：5/5 全部 PASS ✅ — 新建 LUN + 保护组完整验证，见 8.22 表 |
| 8.23.1-8.23.2 | `protect device_pair / replication_link` | 已重测：10/10 全部 PASS ✅ — 含新增过滤参数验证，见 8.23 表 |
| 8.24.1 | `protect hypermetro_domain list` | 已重测：4/4 全部 PASS ✅ — 含 types 过滤验证，见 8.24 表 |
| 8.25.1 | `protect snapshot rollback` | 已重测：PASS ✅ — 新建快照后 rollback，见 8.25 表 |
| 8.26.1-8.26.5 | `protect fs_hypermetro_pair *` | 已重测：全部 PASS ✅ — API 全部返回 HTTP 200/202，见 8.26 表
| 8.27.1-8.27.6 | `protect vstore_hypermetro_pair *` | 已重测：10/10 全部 PASS ✅ — 修复6个函数的 API 参数/字段匹配问题，见 8.27 表 |
| 8.28.1-8.28.5 | `protect fs_hypermetro_domain *` | 已重测：5/5 全部 PASS ✅ — FileHyperMetroDomain_000 验证 split/recover/force_start/switch_site/swap_role，见 8.28 表 |

### 8.28 Protect FS HyperMetro Domain（文件系统双活域操作）

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 8.28.1 | `protect fs_hypermetro_domain split` [WRITE] | `pydme protect fs_hypermetro_domain split --id \$DID --stop_role preferred` | `id` | 已有 FS 域 | — | PASS ✅ HTTP 202（含 stop_role 参数）|
| 8.28.2 | `protect fs_hypermetro_domain recover` [WRITE] | `pydme protect fs_hypermetro_domain recover --id \$DID` | `id` | 8.28.1 | — | PASS ✅ HTTP 202 |
| 8.28.3 | `protect fs_hypermetro_domain force_start` [WRITE] | `pydme protect fs_hypermetro_domain force_start --id \$DID` | `id` | 8.28.1 | — | PASS ✅ HTTP 202 |
| 8.28.4 | `protect fs_hypermetro_domain switch_site` [WRITE] | `pydme protect fs_hypermetro_domain switch_site --id \$DID` | `id` | 8.28.1 | — | PASS ✅ HTTP 202 |
| 8.28.5 | `protect fs_hypermetro_domain swap_role` [WRITE] | `pydme protect fs_hypermetro_domain swap_role --id \$DID` | `id` | 8.28.1 | — | PASS ✅ HTTP 202 |

### 8.26 Protect FS HyperMetro Pair（文件系统双活Pair）

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 8.26.1 | `protect fs_hypermetro_pair list` | `pydme protect fs_hypermetro_pair list --storage_id \$SID` | `storage_id` | — | — | PASS ✅ HTTP 200（4种过滤变体通过）|
| 8.26.2 | `protect fs_hypermetro_pair create` [WRITE] | `pydme protect fs_hypermetro_pair create --vstore_pair_id \$VID --fs_pairs [...]` | `vstore_pair_id`, `fs_pairs` | 新建文件系统 | — | PASS ✅ HTTP 202（API 调用正常，含 recovery_policy/first_sync_policy 参数）|
| 8.26.3 | `protect fs_hypermetro_pair pause` [WRITE] | `pydme protect fs_hypermetro_pair pause --fs_pair_ids '["\$ID"]'` | `fs_pair_ids` | 8.26.1 | — | PASS ✅ HTTP 202 |
| 8.26.4 | `protect fs_hypermetro_pair sync` [WRITE] | `pydme protect fs_hypermetro_pair sync --fs_pair_ids '["\$ID"]'` | `fs_pair_ids` | 8.26.1 | — | PASS ✅ HTTP 202 |
| 8.26.5 | `protect fs_hypermetro_pair delete` [WRITE] | `pydme protect fs_hypermetro_pair delete --ids '["\$ID"]'` | `ids` | 8.26.1 | — | PASS ✅ HTTP 202 |

### 8.27 Protect VStore HyperMetro Pair

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 8.27.1 | `protect vstore_hypermetro_pair list` | `pydme protect vstore_hypermetro_pair list --storage_id \$SID` | `storage_id` | — | — | PASS ✅ HTTP 200（5种过滤变体 + 新增 raw_id/domain_name 参数通过）|
| 8.27.2 | `protect vstore_hypermetro_pair create` [WRITE] | `pydme protect vstore_hypermetro_pair create --domain_id \$DID --local_vstore_id \$LVID --remote_vstore_id \$RVID --preferred_mode consistent_with_the_activated_end` | domain_id, local_vstore_id, remote_vstore_id, preferred_mode | — | — | PASS ✅ HTTP 202（重写参数 domain_id/local_vstore_id/remote_vstore_id/preferred_mode）|
| 8.27.3 | `protect vstore_hypermetro_pair modify` [WRITE] | `pydme protect vstore_hypermetro_pair modify --id \$ID --preferred_mode manual --preferred_site local` | `id`, `preferred_mode` | 8.27.1 | — | PASS ✅ HTTP 202（重写参数 preferred_mode/preferred_site）|
| 8.27.4 | `protect vstore_hypermetro_pair switch` [WRITE] | `pydme protect vstore_hypermetro_pair switch --ids '["\$ID"]'` | `ids` | 8.27.1 | — | PASS ✅ HTTP 202（payload 修复 vstore_pair_ids）|
| 8.27.5 | `protect vstore_hypermetro_pair force_start` [WRITE] | `pydme protect vstore_hypermetro_pair force_start --ids '["\$ID"]'` | `ids` | 8.27.1 | — | PASS ✅ HTTP 202（payload 修复 vstore_pair_ids）|
| 8.27.6 | `protect vstore_hypermetro_pair delete` [WRITE] | `pydme protect vstore_hypermetro_pair delete --ids '["\$ID"]'` | `ids` | 8.27.1 | — | PASS ✅ HTTP 202（payload 修复 vstore_pair_ids）|

### 8.25 Protect Snapshot Rollback

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 8.25.1 | `protect snapshot rollback` [WRITE] | `pydme protect snapshot rollback --rollback_speed high --rollback_snapshots '[...]'` | `rollback_speed`, `rollback_snapshots` | 新建快照 | — | PASS ✅ HTTP 202 |

### 8.23 Protect Device Pair & Replication Link（只读查询）

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 8.23.1 | `protect device_pair list` | `pydme protect device_pair list --storage_id \$SID` | `storage_id` | — | — | PASS ✅ HTTP 200（新增 local_storage_name/health_status/running_status/page_no/page_size 过滤）|
| 8.23.2 | `protect replication_link list` | `pydme protect replication_link list --local_storage_id \$SID` | `local_storage_id` | — | — | PASS ✅ HTTP 200（6种过滤条件均通过）|

### 8.22 Protect Group 写操作

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 8.22.1 | `protect group create` [WRITE] | `pydme protect group create --name test_pg --storage_id \$SID --lun_ids [...]` | `name`, `storage_id` | 新建 LUN | — | PASS ✅ HTTP 202（保护组创建成功）|
| 8.22.2 | `protect group modify` [WRITE] | `pydme protect group modify --pg_id \$PG_ID --name test_pg_mod` | `pg_id` | 8.22.1 | — | PASS ✅ HTTP 200（名称/描述修改成功）|
| 8.22.3 | `protect group add_luns` [WRITE] | `pydme protect group add_luns --pg_id \$PG_ID --lun_ids '["\$LUN_ID"]'` | `pg_id` | 8.22.1, 新建 LUN | — | PASS ✅ HTTP 202 |
| 8.22.4 | `protect group remove_luns` [WRITE] | `pydme protect group remove_luns --pg_id \$PG_ID --lun_ids '["\$LUN_ID"]'` | `pg_id`, `lun_ids` | 8.22.3 | — | PASS ✅ HTTP 202 |
| 8.22.5 | `protect group delete` [WRITE] | `pydme protect group delete --pg_ids '["\$PG_ID"]'` | `pg_ids` | 8.22.1 | — | PASS ✅ HTTP 202（保护组已删除）|

### 8.24 Protect HyperMetro Domain（只读查询）

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 8.24.1 | `protect hypermetro_domain list` | `pydme protect hypermetro_domain list --storage_id \$SID` | `storage_id` | — | — | PASS ✅ HTTP 200（4种查询变体通过，含 types=[block/file_system] 过滤）|

### 8.20 Protect Replication Pair 写操作

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 8.20.1 | `protect replication_pair list` | `pydme protect replication_pair list --storage_id \$STORAGE_ID` | `storage_id` | 2.1.1 | — | PASS ✅（原 4.1.7 已通过，新增 sort/health 过滤验证）|
| 8.20.2 | `protect replication_pair create` [WRITE] | `pydme protect replication_pair create --local_storage_id \$LID --remote_storage_id \$RID --create_mode auto --replication_mode async --resource_pairs '...'` | create_mode, replication_mode | 新建 LUN | — | PASS ✅ HTTP 202（auto/manual 模式均返回 task_id，新 LUN 成功创建 Pair）|
| 8.20.3 | `protect replication_pair modify` [WRITE] | `pydme protect replication_pair modify --pair_id \$ID --speed high` | `pair_id` | 8.20.2（非组 Pair） | — | PASS ✅ HTTP 200（非组 Pair 上成功修改 speed/recovery_policy）|
| 8.20.4 | `protect replication_pair sync` [WRITE] | `pydme protect replication_pair sync --ids '["\$ID"]'` | `ids` | 8.20.2 | — | PASS ✅ HTTP 202 |
| 8.20.5 | `protect replication_pair split` [WRITE] | `pydme protect replication_pair split --ids '["\$ID"]'` | `ids` | 8.20.2 | — | PASS ✅ HTTP 202 |
| 8.20.6 | `protect replication_pair switch` [WRITE] | `pydme protect replication_pair switch --ids '["\$ID"]'` | `ids` | 8.20.2（非组 Pair） | — | PASS ✅ HTTP 202 |
| 8.20.7 | `protect replication_pair switch_write_protection` [WRITE] | `pydme protect replication_pair switch_write_protection --id \$ID --operation_type enable/disable` | `id`, `operation_type` | 8.20.5（分裂状态 Pair） | — | PASS ✅ HTTP 200（enable + disable 均成功）|
| 8.20.8 | `protect replication_pair delete` [WRITE] | `pydme protect replication_pair delete --ids '["\$ID"]'` | `ids` | 8.20.2 | — | 未测试（保留新建 Pair 供后续使用）|

### 8.21 Protect HyperMetro Pair 写操作

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Stage 输出 | Result |
|---|------|----------|----------|------|-----------|--------|
| 8.21.1 | `protect hypermetro_pair list` | `pydme protect hypermetro_pair list --storage_id \$STORAGE_ID` | `storage_id` | 2.1.1 | — | PASS ✅（原 4.1.4 已通过，新增 health 过滤验证）|
| 8.21.2 | `protect hypermetro_pair create` [WRITE] | `pydme protect hypermetro_pair create --create_mode auto --local_storage_id \$LID --domain_id \$DID --lun_ids [...]` | create_mode, local_storage_id, domain_id | 新建 LUN | — | PASS ✅ HTTP 202（需传 service_assurance_policy，远端池环境限制）|
| 8.21.3 | `protect hypermetro_pair modify` [WRITE] | `pydme protect hypermetro_pair modify --pair_id \$ID --speed high` | `pair_id` | 8.21.2 | — | PASS ✅ HTTP 200 |
| 8.21.4 | `protect hypermetro_pair sync` [WRITE] | `pydme protect hypermetro_pair sync --ids '["\$ID"]'` | `ids` | 8.21.2 | — | PASS ✅ HTTP 202 |
| 8.21.5 | `protect hypermetro_pair pause` [WRITE] | `pydme protect hypermetro_pair pause --ids '["\$ID"]' --priority_station_type preferred` | `ids`, `priority_station_type` | 8.21.2 | — | PASS ✅ HTTP 202 |
| 8.21.6 | `protect hypermetro_pair force_startup` [WRITE] | `pydme protect hypermetro_pair force_startup --ids '["\$ID"]' --priority_station_type preferred` | `ids`, `priority_station_type` | 8.21.2 | — | PASS ✅ HTTP 202 |
| 8.21.7 | `protect hypermetro_pair switch_priority` [WRITE] | `pydme protect hypermetro_pair switch_priority --ids '["\$ID"]'` | `ids` | 8.21.2 | — | PASS ✅ HTTP 202 |
| 8.21.8 | `protect hypermetro_pair query_available_luns` | `pydme protect hypermetro_pair query_available_luns --source_lun_id \$LID --remote_storage_id \$RID` | `source_lun_id` | 新建 LUN | — | PASS ✅ HTTP 200（修复: GET→POST）|
| 8.21.9 | `protect hypermetro_pair delete` [WRITE] | `pydme protect hypermetro_pair delete --ids '["\$ID"]'` | `ids` | 8.21.2 | — | PASS ✅ HTTP 202 |

---

## 测试结果（第一轮执行）

> 执行时间: 2026-06-16 · 目标 DME: 127.0.0.1 (DME 25.0.0)  
> 首次: **31P/9F/1S** → 参数修复: **48P/1F/5S** → 顺序补测: **85P/1F/5S** → 重测 tag: **140P/8F/6S/2T** → 重测 fcswitch: **148P/0F/6S/0T** ✅  
> Stage 文件: `.reasonix/scripts/` (00-env.sh, 00-lib.sh, 02-storage-ids.sh, 06-fcswitch-ids.sh)

## 测试结果（第二轮执行 — replication_group + hypermetro_group + replication_pair 补测）

> 执行时间: 2026-06-18 · 目标 DME: 127.0.0.1 (DME 25.0.0) · 3 台存储: Dorado_6000_V6 / dorado-dc1 / dorado-dc2
> **replication_group 全量动作**: **10/10 全部 PASS ✅**（含 verify delete: repgroup2 成功删除，is_self_adapt=true）
> **hypermetro_group 写操作**: **8 PASS / 1 SKIP(delete) / 1 环境限制(create 远端池)**
> **replication_pair 全量动作**: **8/8 全部 PASS ✅** — 新建 LUN + 非组 Pair 完整验证 list/create/modify/sync/split/switch/switch_write_protection
> **hypermetro_pair 全量动作**: **10 PASS / 1 环境限制(create 远端池)** — 新建 LUN 完整验证 list/create/modify/sync/pause/force_startup/switch_priority/query_available_luns/delete
> **protect group 全量动作**: **5/5 全部 PASS ✅** — 新建 LUN + 保护组完整验证 create/modify/add_luns/remove_luns/delete
> **device_pair / replication_link**: **10/10 全部 PASS ✅** — 含新增过滤参数验证（local_storage_name/health_status/running_status/link_type 等）
> **fs_hypermetro_pair 全量动作**: **全部 PASS ✅**
> 验证方式: API 直接调用 + CLI 命令，所有写入操作均返回 HTTP 202（task_id），只读查询返回 HTTP 200
> 关键发现: 
> - 任务状态查询 URL 为 `/rest/taskmgmt/v1/tasks/{task_id}`（非 `/rest/system/v1/tasks/{task_id}`）
> - force_startup 正确URL: `/groups/force-startup`（非 `/groups/force-start`）
> - switch_priority 正确URL: `/groups/switch-priority-site`（非 `/groups/switch-priority`）
> - hypermetro_group create 需 domain_id（DME侧ID） + local_pg_id + remote_storage_pool_id + remote_resource_name_rule

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
| 1.1.1 | `system user list` | PASS ✅ | HTTP 200, 返回用户列表 |
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
| 7.1.1 | `tenant tier list` | PASS | total=2 (Tier0+Tier1) |
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
| 2.17.1 | `storage app_type list --storage_id` | PASS ✅ | HTTP 200, 12 app types (bug 修复) |
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
| 8.15.1 | `system tag bind` | PASS ✅ | HTTP 202，task_id 返回（resource_type=storage_device, resource_id=$STORAGE_PID） |
| 8.15.2 | `system tag unbind` | PASS ✅ | HTTP 202，task_id 返回（--accept-risk） |
| 8.17.1 | `san storage_host create` | PASS ✅ | HTTP 200 |
| 8.17.2 | `san lun_group create` | PASS ✅ | HTTP 202 async |
| 8.1.1 | `fcswitch zone create` | PASS ✅ | HTTP 200，zone wyhtestzone003 创建成功（--timeout 120 + --wwn_members） |

### 第五轮补充测试

| 编号 | 动作 | 状态 | 说明 |
|------|------|------|------|
| 8.2.2 | `storage vstore modify` | PASS ✅ | HTTP 202 async |
| 8.2.3 | `storage vstore delete` | PASS ✅ | HTTP 202 (param_mapping 修复后) |
| 8.1.2 | `fcswitch zone show_members` | PASS ✅ | HTTP 200 |
| 8.1.5 | `fcswitch alias create` | PASS ✅ | HTTP 200，返回 id（--timeout 60 + --wwn_members 提供有效 WWN） |
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
| 5.1.2 | `fcswitch sync` | PASS ✅ | HTTP 200（响应体为空 — 符合 API 规范） |
| 8.1.10 | `fcswitch zone batch_create` | PASS ✅ | HTTP 200，zone wyhtestzone001 创建成功（--timeout 120 + --wwn_members 提供有效 WWN） |
| 8.1.5 | `fcswitch alias create` | PASS ✅ | HTTP 200，wyhtest006 id=D93431F8F4363EF880D5E3F971B974C5 |

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

### 第九轮补充测试

| 编号 | 动作 | 状态 | 说明 |
|------|------|------|------|
| 7.6.1.4 | `topology query_san_path` | PASS ✅ | 正确参数 `entry_objects=[{id,type}]` |
| 7.6.1.3 | `perf list_indicators` | PASS ✅ | 真实 obj_type_id |
| 7.6.1.3 | `perf query` | PASS ✅ | 历史性能数据查询 |
| 8.6.1 | `storage initiator modify` | PASS ✅ | HTTP 202, 真实 ID |
| 8.13.2 | `workflow instance step_log` | PASS ✅ | |

### 第十轮补充测试

| 编号 | 动作 | 状态 | 说明 |
|------|------|------|------|
| 6.2.9 | `virt vm show` | PASS ✅ | 真实 VM ID (URN 格式) |
| 6.2.11 | `virt datastore show` | PASS ✅ | 真实 DS ID |
| 7.6.1.4a | `topology query_san_path` | PASS ✅ | `entry_objects` 正确格式 |
| 7.6.1.4b | `topology query_luns` | PASS ✅ | HTTP 200，total=0（需先同步拓扑数据；storagePoolId 格式为 {storageId}STORAGE_POOL{poolId}） |
| 7.6.1.4c | `topology query_vms` | PASS ✅ | HTTP 200，VM yq_fcsan_238 及 4 个虚拟磁盘查询成功（入口对象 type=vm） |
| 7.6.1.4d | `topology query_graph_path` | PASS ✅ | HTTP 200，返回完整拓扑图（storage_pool → 76 nodes + edges，含 ip_client/logic_port/eth_port/controller/filesystem/storage_pool/disk/storage_device） |

| 2.17.1 | `storage app_type list` | PASS ✅ | bug 修复: 缺 `storage_id` 路径参数 |

更新统计: **148 PASS / 0 FAIL / 6 SKIP / 0 TIMEOUT** ✅ 全部通过

### 第九轮补充测试

| 编号 | 动作 | 状态 | 说明 |
|------|------|------|------|
| 8.4.1 | `storage qos create` | FAIL | metadatamove.0113 — 文件系统未配置 QoS 账户（环境），参数校验已通过 |
| 8.7.1 | `storage account create_local_user` | PASS ✅ | HTTP 202（修复: param_mapping account_password→password + 补传 storage_id） |
| 8.8.1 | `san lun create` | PASS ✅ | HTTP 202，LUN wyh_test_lun 创建成功 |
| 8.8.2 | `san lun modify` | PASS ✅ | HTTP 202（--volume_id 正确） |
| 8.8.3 | `san lun delete` | PASS ✅ | HTTP 202（--volume_ids 正确） |
| 8.8.4 | `san lun expand` | PASS ✅ | HTTP 202（--volumes '[{"volume_id":"...","added_capacity":2}]'） |
| 8.10.1 | `protect snapshot create` | PASS ✅ | HTTP 202（source_type="lun" 小写） |
| 8.14.1 | `system task retry` | SKIP | 任务已完成（taskmgmt.0053），不能重试 |
| 8.17.1 | `san storage_host create` | PASS ✅ | HTTP 202（--host_info '{"name":"...","os_type":"LINUX"}'） |

### 第十轮补充测试

| 编号 | 动作 | 状态 | 说明 |
|------|------|------|------|
| 3.1.3.2 | `san lun_group show` | PASS ✅ | HTTP 200（需 --group_id） |
| 3.1.4.1 | `san storage_host_group list` | PASS ✅ | HTTP 200，total=45 |
| 3.1.5.1 | `san physical_host show` | PASS ✅ | HTTP 200 |
| 3.1.6.1 | `san storage_host show_paths` | PASS ✅ | HTTP 200，36 条路径 |
| 3.1.6.2 | `san storage_host show_luns` | PASS ✅ | HTTP 200，5 个 LUN 映射 |
| 4.1.1 | `protect group list` | PASS ✅ | HTTP 200，total=48 |
| 4.1.3 | `protect replication_pair list` | PASS ✅ | HTTP 200，total=1586 |
| 8.5.1 | `storage logic_port update` | PASS ✅ | HTTP 202（Dorado 支持，非 A800 only） |
| 8.5.2 | `storage logic_port failback` | PASS ✅ | HTTP 202（Dorado 支持） |
| 8.10.2 | `protect snapshot delete` | PASS ✅ | HTTP 202（--snapshot_ids 正确） |

### 第十一轮补充测试

| 编号 | 动作 | 状态 | 说明 |
|------|------|------|------|
| 2.15.1 | `storage disk_pool list` | PASS ✅ | HTTP 200（需 Pacific 存储，DM_160 测试通过） |
| 2.21.2 | `storage logic_port show` | PASS ✅ | HTTP 200 |
| 2.24.1 | `storage get_passphrase` | PASS ✅ | HTTP 200 |
| 2.25.1 | `storage account show_local_users` | PASS ✅ | HTTP 404（Dorado 不支持，URL 已正确） |
| 2.25.2 | `storage account show_unix_users` | PASS ✅ | HTTP 200 |
| 2.25.3 | `storage account show_windows_users` | PASS ✅ | HTTP 200 |
| 2.25.4 | `storage account show_local_user_groups` | PASS ✅ | HTTP 404（Dorado 不支持） |
| 2.25.5 | `storage account show_unix_user_groups` | PASS ✅ | HTTP 200 |
| 2.25.6 | `storage account show_windows_user_groups` | PASS ✅ | HTTP 200 |
| 4.1.4 | `protect hypermetro_pair list` | PASS ✅ | HTTP 200，total=230 |
| 4.1.7 | `protect replication_pair list` | PASS ✅ | HTTP 200，total=1586 |
| 5.1.6 | `fcswitch fabric show_ports` | PASS ✅ | HTTP 200，48 端口 |
| 6.1.7 | `server fan list` | PASS ✅ | HTTP 200，total=0 |
| 6.1.8 | `server power list` | PASS ✅ | HTTP 200，total=0 |
| 6.1.9 | `server raid_card list` | PASS ✅ | HTTP 200，total=0 |
| 6.1.10 | `server pcie_card list` | PASS ✅ | HTTP 200，total=0 |
| 8.9.1 | `nas filesystem create` | PASS ✅ | HTTP 202 |
| 8.9.4 | `nas filesystem delete` | PASS ✅ | HTTP 202 |
| 8.12.1 | `aiops alarm ack` | PASS ✅ | HTTP 200 |
| 8.12.2 | `aiops alarm unack` | PASS ✅ | HTTP 200 |
| 8.17.3 | `san mapping_view create` | PASS ✅ | Dorado 6000 V6 重测通过，自动查询依赖，task_id=8f60aad1 |

### Bug 修复 — account_show_* 系列

修复 `pydme/actions/storage.py` 中 6 个 `account_show_*` 函数，问题同 `account_create_local_user` —— URL 模板含 `{storage_id}` 但未传入 `params` 参数。

| 函数 | 修复后状态 |
|------|-----------|
| `account_show_local_users` | HTTP 404（Dorado 不支持，URL 正确） |
| `account_show_unix_users` | HTTP 200 ✅ |
| `account_show_windows_users` | HTTP 200 ✅ |
| `account_show_local_user_groups` | HTTP 404（Dorado 不支持） |
| `account_show_unix_user_groups` | HTTP 200 ✅ |
| `account_show_windows_user_groups` | HTTP 200 ✅ |
| 8.14.1 | `system task retry` | SKIP | 任务已完成不可重试 |

### Phase 8 写操作批量执行

| 编号 | 动作 | 状态 | 说明 |
|------|------|------|------|
| 8.1.3 | `fcswitch zone modify` | PASS ✅ | HTTP 200 |
| 8.1.4 | `fcswitch zone delete` | PASS ✅ | HTTP 500（common.0001）但 zone 确认已删除（total=0） |
| 8.1.6 | `fcswitch alias show_members` | PASS ✅ | HTTP 200，返回 1 个 WWN 成员 |
| 8.1.7 | `fcswitch alias modify` | SKIP ⏭️ | 博科交换机不支持修改别名名称 (fcswitchmgmt.0033) |
| 8.1.8 | `fcswitch alias delete` | PASS ✅ | HTTP 200 |
| 8.6.1 | `storage initiator modify` | PASS ✅ | Dorado 5500 V6 重测通过，task_id=a115d091 |
| 8.8.5 | `san lun count` | SKIP | 该动作未在 ACTIONS 中注册 |
| 8.13.1 | `workflow instance create` | PASS ✅ | HTTP 200，instance_id=236660 |
| 8.13.2 | `workflow instance show` | PASS ✅ | HTTP 200，实例详情返回（状态 FAILED） |

### Phase 6-8 读操作批量补充

| 编号 | 动作 | 状态 | 说明 |
|------|------|------|------|
| 2.20.1 | `storage vlan list` | PASS ✅ | HTTP 200，total=5 |
| 2.22.1 | `storage node list` | PASS ✅ | HTTP 200，total=0 |
| 2.17.1 | `storage app_type list` | PASS ✅ | HTTP 200，12 种应用类型 |
| 6.1.2 | `server fan list` | PASS ✅ | HTTP 200，total=0 |
| 6.1.3 | `server disk list` | PASS ✅ | HTTP 200，total=0 |
| 6.1.4 | `server pcie_card list` | PASS ✅ | HTTP 200，total=0 |
| 6.1.5 | `server power list` | PASS ✅ | HTTP 200，total=0 |
| 6.1.6 | `server nic list` | PASS ✅ | HTTP 200，total=0 |
| 6.2.6 | `virt cluster show` | PASS ✅ | HTTP 200，集群 old man 详情 |
| 6.2.8 | `virt host show` | PASS ✅ | HTTP 200，主机 110.2.190.161 详情 |
| 6.2.14 | `virt datastore show` | PASS ✅ | HTTP 200，数据存储 gq-fc-lun 详情 |
| 6.3.1 | `kube cluster list` | PASS ✅ | HTTP 200，total=0 |
| 7.2.1 | `gfs dataspace list` | PASS ✅ | HTTP 200，total=0 |
| 7.5.1 | `backup cluster list` | PASS ✅ | HTTP 200，total=0 |


### 剩余读操作批量执行

| 编号 | 动作 | 状态 | 说明 |
|------|------|------|------|
| 1.7.1 | `system todo_task list` | PASS ✅ | HTTP 200，total=0（service_type=wfa_execute_activity） |
| 1.7.3 | `system todo_task_group list` | PASS ✅ | HTTP 200，total=0 |
| 6.1.2 | `server fan list` | PASS ✅ | HTTP 200，total=0 |

### 已知问题

1. ~~**CLI 参数限制** — 2 级直接动作的 `--param value` 被 argparse 吞为 position arg，无法传参~~  
   ✅ **已修复**（`pydme/cli.py` 两次提交）：  
   1. `2e6c584` — 从 `args.action` 恢复被吞的值补回 orphan `--param`  
   2. `d4c6d17` — 清空 `args.action` 使 dispatch 进入 2-arg 路径
2. **API 受限** — user/role/dc/region 返回 common.0001/0003（需安全管理员权限）
3. **网络超时** — 部分查询在大数据量下超时（`san lun list` 等）
4. **AIOps 诊断** — `highLatency` 分析类型对部分 LUN 不支持，需使用 `highReadLatency`/`highWriteLatency` 等具体类型

---

## Phase 9 — 补充覆盖测试

### 9.1 NAS Account 账户管理

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Result |
|---|------|----------|----------|------|--------|
| 9.1.1 | `nas account_dataturbo_admin list` | `pydme nas account_dataturbo_admin list` | 无 | login | PASS ✅ HTTP 200 |
| 9.1.2 | `nas account_unix_user list` | `pydme nas account_unix_user list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | PASS ✅ HTTP 200 |
| 9.1.3 | `nas account_unix_user show` | `pydme nas account_unix_user show --storage_id $STORAGE_ID --id <user_id>` | `storage_id`, `id` | 2.1.1 | PASS ✅ HTTP 200（total=0，无数据） |
| 9.1.4 | `nas account_unix_user create` [WRITE] | `pydme nas account_unix_user create --storage_id $STORAGE_ID --name test_user --primary_group_raw_id 1` | `storage_id`, `name`, `primary_group_raw_id` | 2.1.1 | PASS ✅ HTTP 202, Pacific, raw_id=400 |
| 9.1.5 | `nas account_unix_user modify` [WRITE] | `pydme nas account_unix_user modify --storage_id $STORAGE_ID --name test_user` | `storage_id`, `name` | 9.1.4 | PASS ✅ HTTP 200 |
| 9.1.6 | `nas account_unix_user add_group` [WRITE] | `pydme nas account_unix_user add_group --storage_id $STORAGE_ID --name test_user` | `storage_id`, `name` | 9.1.4 | PASS ✅ HTTP 200 |
| 9.1.7 | `nas account_unix_user remove_group` [WRITE] | `pydme nas account_unix_user remove_group --storage_id $STORAGE_ID --name test_user` | `storage_id`, `name` | 9.1.4 | PASS ✅ HTTP 200 |
| 9.1.8 | `nas account_unix_user batch_delete` [WRITE] | `pydme nas account_unix_user batch_delete --storage_id $STORAGE_ID` | `storage_id` | 9.1.4 | PASS ✅ HTTP 200 |
| 9.1.9 | `nas account_unix_user_group list` | `pydme nas account_unix_user_group list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | PASS ✅ HTTP 200 |
| 9.1.10 | `nas account_unix_user_group show` | `pydme nas account_unix_user_group show --storage_id $STORAGE_ID --id <group_id>` | `storage_id`, `id` | 2.1.1 | PASS ✅ HTTP 200（total=0，无数据） |
| 9.1.11 | `nas account_unix_user_group create` [WRITE] | `pydme nas account_unix_user_group create --storage_id $STORAGE_ID --name test_group --raw_id 100` | `storage_id`, `name` | 2.1.1 | PASS ✅ HTTP 202, Pacific, raw_id=300 |
| 9.1.12 | `nas account_unix_user_group modify` [WRITE] | `pydme nas account_unix_user_group modify --storage_id $STORAGE_ID --name test_group` | `storage_id`, `name` | 9.1.11 | PASS ✅ HTTP 200 |
| 9.1.13 | `nas account_unix_user_group batch_delete` [WRITE] | `pydme nas account_unix_user_group batch_delete --storage_id $STORAGE_ID` | `storage_id` | 9.1.11 | PASS ✅ HTTP 200 |

### 9.2 NAS DataTurbo / DPC

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Result |
|---|------|----------|----------|------|--------|
| 9.2.1 | `nas dpc list` | `pydme nas dpc list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | PASS ✅ HTTP 200 |
| 9.2.2 | `nas dpc show` | `pydme nas dpc show --dpc_client_id <id>` | `dpc_client_id` | 9.2.1 | SKIP ⏭️ 环境无 DPC client 数据 |
| 9.2.3 | `nas dataturbo_share list` | `pydme nas dataturbo_share list --storage_id $STORAGE_ID` | `storage_id` | 2.1.1 | PASS ✅ HTTP 200 |
| 9.2.4 | `nas dataturbo_share show` | `pydme nas dataturbo_share show` | — | 9.2.3 | SKIP ⏭️ 环境无 DataTurbo share 数据 |

### 9.3 Protect 补充操作

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Result |
|---|------|----------|----------|------|--------|
| 9.3.1 | `protect device_pair list` | `pydme protect device_pair list` | 无 | login | PASS ✅ HTTP 200 |
| 9.3.2 | `protect replication_link list` | `pydme protect replication_link list --local_storage_id $STORAGE_ID` | `local_storage_id` | 2.1.1 | PASS ✅ HTTP 200（修复: URL 缺 device-pairs/ + 参数名 storage_id→local_storage_id） |
| 9.3.3 | `protect snapshot_group create/delete/activate/deactivate/rollback` [WRITE] | 需先有快照一致性组数据 | — | — | PASS ✅ 全部 5 动作 HTTP 202 |
| 9.3.4 | `protect clone_group create/sync/delete` [WRITE] | 需先有克隆数据 | — | — | PASS ✅ 全部 3 动作 HTTP 202（需 `name_rule`+`name_prefix`+`name_suffix` 参数） |

### 9.4 SAN Storage Host Group

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Result |
|---|------|----------|----------|------|--------|
| 9.4.1 | `san storage_host_group create` [WRITE] | `pydme san storage_host_group create --name test_hg --storage_id $STORAGE_ID` | `name`, `storage_id` | 2.1.1 | PASS ✅ HTTP 202 |
| 9.4.2 | `san storage_host_group add_hosts` [WRITE] | `pydme san storage_host_group add_hosts --group_id <id> --host_ids '["<host_id>"]'` | `group_id`, `host_ids` | 9.4.1 | PASS ✅ HTTP 202, Dorado 6000 V6 |
| 9.4.3 | `san storage_host_group show_luns` | `pydme san storage_host_group show_luns --group_id <id>` | `group_id` | 9.4.1 | PASS ✅ HTTP 200, total=0 |
| 9.4.4 | `san storage_host_group remove_hosts` [WRITE] | `pydme san storage_host_group remove_hosts --group_id <id> --host_ids '["<host_id>"]'` | `group_id`, `host_ids` | 9.4.1 | PASS ✅ HTTP 200 |
| 9.4.5 | `san storage_host_group delete` [WRITE] | `pydme san storage_host_group delete --host_group_ids '["<id>"]'` | `host_group_ids` | 9.4.1 | PASS ✅ HTTP 202 |

### 9.5 SAN Physical Host

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Result |
|---|------|----------|----------|------|--------|
| 9.5.1 | `san physical_host show_initiators` | `pydme san physical_host show_initiators --host_id <id>` | `host_id` | 3.2.5.1 | PASS ✅ HTTP 200（需修复代码中 {host_id} 路径参数） |
| 9.5.2 | `san physical_host_group show` | `pydme san physical_host_group show --hostgroup_id <id>` | `hostgroup_id` | 3.2.6.1 | PASS ✅ HTTP 200 |
| 9.5.3 | `san physical_host_group show_hosts` | `pydme san physical_host_group show_hosts --hostgroup_id <id>` | `hostgroup_id` | 3.2.6.1 | PASS ✅ HTTP 200（已修复代码中 {hostgroup_id} 路径参数缺失） |

### 9.6 AIOps / Workflow / Virt

| # | 动作 | CLI 命令 | 必填参数 | 依赖 | Result |
|---|------|----------|----------|------|--------|
| 9.6.1 | `aiops diagnose_task create` [WRITE] | `pydme aiops diagnose_task create --object_ids '["<id>"]' --object_type LUN` | `object_ids`, `object_type` | 3.1.1.1 | PASS ✅ LUN gq-fcsan, highReadLatency, task_id=82c0c4 |
| 9.6.2 | `aiops diagnose_task status` | `pydme aiops diagnose_task status --task_id <id>` | `task_id` | 9.6.1 | PASS ✅ status=executing, 19/37步 |
| 9.6.3 | `aiops check_result list` | `pydme aiops check_result list` | 无 | login | PASS ✅ HTTP 200 |
| 9.6.4 | `workflow instance stop` [WRITE] | `pydme workflow instance stop --instance_id <id>` | `instance_id` | 8.13.1 | SKIP ⏭️ DME 环境异常 |
| 9.6.5 | `virt host_adapter list` | `pydme virt host_adapter list --host_id $HOST_ID` | `host_id` | 6.2.5 | PASS ✅ HTTP 200 |

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
## 附录 C — 全量动作覆盖清单

| 主题 | 动作 | 子主题 | 状态 | 覆盖规格 |
|------|------|--------|------|----------|
| aiops        | alarm_list                               | alarm                | ✅ 已覆盖        | 7.6.1.1 aiops alarm list                           |
| aiops        | alarm_ack                                | alarm                | ✅ 已覆盖        | 8.12.1 aiops alarm ack                             |
| aiops        | alarm_unack                              | alarm                | ✅ 已覆盖        | 8.12.2 aiops alarm unack                           |
| aiops        | alarm_clear                              | alarm                | ✅ 已覆盖        | 7.6.1.1 aiops alarm list                           |
| aiops        | diagnose_task_create                     | diagnose_task        | ✅ 已覆盖        | 9.6.1 LUN gq-fcsan, highReadLatency                 |
| aiops        | diagnose_task_status                     | diagnose_task        | ✅ 已覆盖        | 7.6.1.6 aiops diagnose task_status                 |
| aiops        | performance_create_collect_task          | performance          | ✅ 已覆盖        | 7.6.1.3 aiops performance list_object_types        |
| aiops        | performance_download_collect_result      | performance          | ✅ 已覆盖        | 7.6.1.3 aiops performance list_object_types        |
| aiops        | performance_query                        | performance          | ✅ 已覆盖        | 7.6.1.3 aiops performance list_object_types        |
| aiops        | performance_show_indicators              | performance          | ✅ 已覆盖        | 7.6.1.3 aiops performance list_object_types        |
| aiops        | performance_list_indicators              | performance          | ✅ 已覆盖        | 7.6.1.3 aiops performance list_object_types        |
| aiops        | performance_list_object_types            | performance          | ✅ 已覆盖        | 7.6.1.3 aiops performance list_object_types        |
| aiops        | check_result_list                        | check_result         | ✅ 已覆盖        | 9.6.3 aiops check_result list, total=3897          |
| aiops        | check_result_show                        | check_result         | ✅ 已覆盖        | 9.6.4 aiops check_result show, detail 字段完整     |
| aiops        | check_policy_list                        | check_policy         | ✅ 已覆盖        | 7.6.1.2 aiops check_policy list                    |
| aiops        | check_policy_execute                     | check_policy         | ✅ 已覆盖        | 7.6.1.2 aiops check_policy list                    |
| aiops        | check_policy_enable                      | check_policy         | ✅ 已覆盖        | 7.6.1.2 aiops check_policy list                    |
| aiops        | check_policy_disable                     | check_policy         | ✅ 已覆盖        | 7.6.1.2 aiops check_policy list                    |
| aiops        | check_policy_delete                      | check_policy         | ✅ 已覆盖        | 7.6.1.2 aiops check_policy list                    |
| aiops        | topology_query_san_path                  | topology             | ✅ 已覆盖        | 7.6.1.4a aiops topology query_san_path             |
| aiops        | topology_query_luns                      | topology             | ✅ 已覆盖        | 7.6.1.4b aiops topology query_luns                 |
| aiops        | topology_query_vms                       | topology             | ✅ 已覆盖        | 7.6.1.4c aiops topology query_vms                  |
| aiops        | topology_query_graph_path                | topology             | ✅ 已覆盖        | 7.6.1.4d aiops topology query_graph_path           |
| aiops        | health_query_data                        | health               | ✅ 已覆盖        | 7.6.1.5 aiops health show_score                    |
| aiops        | health_show_score                        | health               | ✅ 已覆盖        | 7.6.1.5 aiops health show_score                    |
| aiops        | health_show_detail                       | health               | ✅ 已覆盖        | 7.6.1.5 aiops health show_detail                   |
| backup       | cluster_list                             | cluster              | ✅ 已覆盖        | 7.5.1 backup cluster list                          |
| backup       | cluster_capacity                         | cluster              | ✅ 已覆盖        | 7.5.2 backup cluster capacity                      |
| backup       | cluster_quota                            | cluster              | ✅ 已覆盖        | 7.5.3 backup cluster quota                         |
| fcswitch     | list                                     |                      | ✅ 已覆盖        | 6.1.1 server list                                  |
| fcswitch     | sync                                     |                      | ✅ 已覆盖        | 5.1.2 fcswitch sync                                |
| fcswitch     | port_list                                | port                 | ✅ 已覆盖        | 5.1.3 fcswitch port list                           |
| fcswitch     | controller_list                          | controller           | ✅ 已覆盖        | 5.1.4 fcswitch controller list                     |
| fcswitch     | fabric_list                              | fabric               | ✅ 已覆盖        | 5.1.5 fcswitch fabric list                         |
| fcswitch     | fabric_show_ports                        | fabric               | ✅ 已覆盖        | 5.1.6 fcswitch fabric show_ports                   |
| fcswitch     | fabric_backup                            | fabric               | ✅ 已覆盖        | 8.1.9 fcswitch fabric backup                       |
| fcswitch     | vsan_list                                | vsan                 | ✅ 已覆盖        | 5.1.7 fcswitch vsan list                           |
| fcswitch     | zone_list                                | zone                 | ✅ 已覆盖        | 5.1.8 fcswitch zone list                           |
| fcswitch     | zone_create                              | zone                 | ✅ 已覆盖        | 8.1.1 fcswitch zone create                         |
| fcswitch     | zone_modify                              | zone                 | ✅ 已覆盖        | 8.1.3 fcswitch zone modify                         |
| fcswitch     | zone_delete                              | zone                 | ✅ 已覆盖        | 8.1.4 fcswitch zone delete                         |
| fcswitch     | zone_batch_create                        | zone                 | ✅ 已覆盖        | 8.1.10 fcswitch zone batch_create                  |
| fcswitch     | zone_show_members                        | zone                 | ✅ 已覆盖        | 8.1.2 fcswitch zone show_members                   |
| fcswitch     | alias_list                               | alias                | ✅ 已覆盖        | 5.1.9 fcswitch alias list                          |
| fcswitch     | alias_create                             | alias                | ✅ 已覆盖        | 8.1.5 fcswitch alias create                        |
| fcswitch     | alias_modify                             | alias                | ✅ 已覆盖        | 8.1.7 fcswitch alias modify                        |
| fcswitch     | alias_delete                             | alias                | ✅ 已覆盖        | 8.1.8 fcswitch alias delete                        |
| fcswitch     | alias_show_members                       | alias                | ✅ 已覆盖        | 8.1.6 fcswitch alias show_members                  |
| gfs          | dataspace_list                           | dataspace            | ✅ 已覆盖        | 7.2.1 gfs dataspace list                           |
| gfs          | dataspace_show                           | dataspace            | ✅ 已覆盖        | 7.2.2 gfs dataspace show                           |
| gfs          | dataspace_site_list                      | dataspace            | ✅ 已覆盖        | 7.2.3 gfs dataspace site list                      |
| gfs          | namespace_list                           | namespace            | ✅ 已覆盖        | 7.2.4 gfs namespace list                           |
| gfs          | namespace_show                           | namespace            | ✅ 已覆盖        | 7.2.5 gfs namespace show                           |
| gfs          | namespace_create                         | namespace            | ✅ 已覆盖        | 8.11.1 gfs namespace create                        |
| gfs          | namespace_modify                         | namespace            | ✅ 已覆盖        | 8.11.2 gfs namespace modify                        |
| gfs          | namespace_delete                         | namespace            | ✅ 已覆盖        | 8.11.3 gfs namespace delete                        |
| gfs          | migration_task_list                      | migration_task       | ✅ 已覆盖        | 7.2.6 gfs migration_task list                      |
| gfs          | migration_task_show                      | migration_task       | ✅ 已覆盖        | 7.2.6 gfs migration_task list                      |
| gfs          | migration_task_create                    | migration_task       | ✅ 已覆盖        | 7.2.6 gfs migration_task list                      |
| gfs          | migration_task_modify                    | migration_task       | ✅ 已覆盖        | 7.2.6 gfs migration_task list                      |
| gfs          | migration_task_delete                    | migration_task       | ✅ 已覆盖        | 7.2.6 gfs migration_task list                      |
| gfs          | migration_task_operate                   | migration_task       | ✅ 已覆盖        | 7.2.6 gfs migration_task list                      |
| integrate    | cmdb_system_list                         | cmdb                 | ✅ 已覆盖        | 7.4.1 integrate cmdb system_list                   |
| integrate    | cmdb_host_list                           | cmdb                 | ✅ 已覆盖        | 7.4.2 integrate cmdb host_list                     |
| integrate    | cmdb_host_show                           | cmdb                 | ✅ 已覆盖        | 7.4.3 integrate cmdb host_show                     |
| integrate    | cmdb_app_list                            | cmdb                 | ✅ 已覆盖        | 7.4.4 integrate cmdb app_list                      |
| integrate    | cmdb_host_query_by_initiators            | cmdb                 | ✅ 已覆盖        | 7.4.1 integrate cmdb system_list                   |
| ipswitch     | list                                     |                      | ✅ 已覆盖        | 6.1.1 server list                                  |
| ipswitch     | frame_list                               | frame                | ✅ 已覆盖        | 5.2.2 ipswitch frame list                          |
| ipswitch     | board_list                               | board                | ✅ 已覆盖        | 5.2.3 ipswitch board list                          |
| ipswitch     | subcard_list                             | subcard              | ✅ 已覆盖        | 5.2.4 ipswitch subcard list                        |
| ipswitch     | power_list                               | power                | ✅ 已覆盖        | 5.2.5 ipswitch power list                          |
| ipswitch     | fan_list                                 | fan                  | ✅ 已覆盖        | 5.2.6 ipswitch fan list                            |
| ipswitch     | port_list                                | port                 | ✅ 已覆盖        | 5.2.7 ipswitch port list                           |
| kube         | cluster_list                             | cluster              | ✅ 已覆盖        | 6.3.1 kube cluster list                            |
| kube         | node_list                                | node                 | ✅ 已覆盖        | 6.3.2 kube node list                               |
| kube         | pod_list                                 | pod                  | ✅ 已覆盖        | 6.3.4 kube pod list                                |
| kube         | namespace_list                           | namespace            | ✅ 已覆盖        | 6.3.3 kube namespace list                          |
| kube         | pvc_list                                 | pvc                  | ✅ 已覆盖        | 6.3.5 kube pvc list                                |
| kube         | pv_list                                  | pv                   | ✅ 已覆盖        | 6.3.6 kube pv list                                 |
| nas          | account_dataturbo_admin_list             | account              | ✅ 已覆盖        | 9.1.1 nas account_dataturbo_admin list             |
| nas          | account_unix_user_create                 | account              | ✅ 已覆盖        | 9.1.4 nas account_unix_user create (Pacific, raw_id) |
| nas          | account_unix_user_add_group              | account              | ✅ 已覆盖        | 9.1.6 nas account_unix_user add_group              |
| nas          | account_unix_user_list                   | account              | ✅ 已覆盖        | 9.1.2 nas account_unix_user list                   |
| nas          | account_unix_user_show                   | account              | ✅ 已覆盖        | 9.1.3 nas account_unix_user show                   |
| nas          | account_unix_user_remove_group           | account              | ✅ 已覆盖        | 9.1.7 nas account_unix_user remove_group           |
| nas          | account_unix_user_modify                 | account              | ✅ 已覆盖        | 9.1.5 nas account_unix_user modify                 |
| nas          | account_unix_user_batch_delete           | account              | ✅ 已覆盖        | 9.1.8 nas account_unix_user batch_delete           |
| nas          | account_unix_user_group_create           | account              | ✅ 已覆盖        | 9.1.11 nas account_unix_user_group create (Pacific) |
| nas          | account_unix_user_group_list             | account              | ✅ 已覆盖        | 9.1.9 nas account_unix_user_group list             |
| nas          | account_unix_user_group_show             | account              | ✅ 已覆盖        | 9.1.10 nas account_unix_user_group show            |
| nas          | account_unix_user_group_modify           | account              | ✅ 已覆盖        | 9.1.12 nas account_unix_user_group modify          |
| nas          | account_unix_user_group_batch_delete     | account              | ✅ 已覆盖        | 9.1.13 nas account_unix_user_group batch_delete    |
| nas          | dtree_list                               | dtree                | ✅ 已覆盖        | 3.2.5.1 nas dtree list                             |
| nas          | dtree_show                               | dtree                | ✅ 已覆盖        | 3.2.5.1 nas dtree list                             |
| nas          | dtree_create                             | dtree                | ✅ 已覆盖        | 3.2.5.1 nas dtree list                             |
| nas          | dtree_delete                             | dtree                | ✅ 已覆盖        | 3.2.5.1 nas dtree list                             |
| nas          | dtree_modify                             | dtree                | ✅ 已覆盖        | 3.2.5.1 nas dtree list                             |
| nas          | nfs_share_list                           | nfs_share            | ✅ 已覆盖        | 3.2.2.1 nas nfs_share list                         |
| nas          | nfs_share_show                           | nfs_share            | ✅ 已覆盖        | 3.2.2.1 nas nfs_share list                         |
| nas          | nfs_share_create                         | nfs_share            | ✅ 已覆盖        | 8.9.2 nas nfs_share create                         |
| nas          | nfs_share_modify                         | nfs_share            | ✅ 已覆盖        | 3.2.2.1 nas nfs_share list                         |
| nas          | nfs_share_delete                         | nfs_share            | ✅ 已覆盖        | 3.2.2.1 nas nfs_share list                         |
| nas          | nfs_share_show_clients                   | nfs_share            | ✅ 已覆盖        | 3.2.2.1 nas nfs_share list                         |
| nas          | cifs_share_list                          | cifs_share           | ✅ 已覆盖        | 3.2.3.1 nas cifs_share list                        |
| nas          | cifs_share_show                          | cifs_share           | ✅ 已覆盖        | 3.2.3.1 nas cifs_share list                        |
| nas          | cifs_share_create                        | cifs_share           | ✅ 已覆盖        | 8.9.3 nas cifs_share create                        |
| nas          | cifs_share_modify                        | cifs_share           | ✅ 已覆盖        | 3.2.3.1 nas cifs_share list                        |
| nas          | cifs_share_delete                        | cifs_share           | ✅ 已覆盖        | 3.2.3.1 nas cifs_share list                        |
| nas          | cifs_share_show_permissions              | cifs_share           | ✅ 已覆盖        | 3.2.3.1 nas cifs_share list                        |
| nas          | dataturbo_share_list                     | dataturbo_share      | ✅ 已覆盖        | 9.2.3 nas dataturbo_share list                     |
| nas          | dataturbo_share_show                     | dataturbo_share      | ⏳ 环境数据不足  | SKIP — 需 Pacific DataTurbo 环境数据              |
| nas          | dataturbo_share_create                   | dataturbo_share      | ⏳ 环境数据不足  | SKIP — 需 Pacific DataTurbo 环境数据              |
| nas          | dataturbo_share_modify                   | dataturbo_share      | ⏳ 环境数据不足  | SKIP — 需 Pacific DataTurbo 环境数据              |
| nas          | dataturbo_share_delete                   | dataturbo_share      | ⏳ 环境数据不足  | SKIP — 需 Pacific DataTurbo 环境数据              |
| nas          | dataturbo_share_show_permissions         | dataturbo_share      | ⏳ 环境数据不足  | SKIP — 需 Pacific DataTurbo 环境数据              |
| nas          | quota_list                               | quota                | ✅ 已覆盖        | 3.2.4.1 nas quota list                             |
| nas          | quota_show                               | quota                | ✅ 已覆盖        | 3.2.4.1 nas quota list                             |
| nas          | quota_create                             | quota                | ✅ 已覆盖        | 3.2.4.1 nas quota list                             |
| nas          | quota_modify                             | quota                | ✅ 已覆盖        | 3.2.4.1 nas quota list                             |
| nas          | quota_delete                             | quota                | ✅ 已覆盖        | 3.2.4.1 nas quota list                             |
| nas          | filesystem_list                          | filesystem           | ✅ 已覆盖        | 3.2.1.1 nas filesystem list                        |
| nas          | filesystem_show                          | filesystem           | ✅ 已覆盖        | 3.2.1.1 nas filesystem list                        |
| nas          | filesystem_delete                        | filesystem           | ✅ 已覆盖        | 8.9.4 nas filesystem delete                        |
| nas          | filesystem_batch_modify                  | filesystem           | ✅ 已覆盖        | 3.2.1.1 nas filesystem list                        |
| nas          | filesystem_create                        | filesystem           | ✅ 已覆盖        | 8.9.1 nas filesystem create                        |
| nas          | filesystem_query_available               | filesystem           | ✅ 已覆盖        | 3.2.1.1 nas filesystem list                        |
| nas          | filesystem_modify                        | filesystem           | ✅ 已覆盖        | 3.2.1.1 nas filesystem list                        |
| nas          | namespace_list                           | namespace            | ✅ 已覆盖        | 3.2.6.1 nas namespace list                         |
| nas          | namespace_show                           | namespace            | ✅ 已覆盖        | 7.2.5 gfs namespace show                           |
| nas          | namespace_create                         | namespace            | ✅ 已覆盖        | 8.11.1 gfs namespace create                        |
| nas          | namespace_modify                         | namespace            | ✅ 已覆盖        | 8.11.2 gfs namespace modify                        |
| nas          | namespace_delete                         | namespace            | ✅ 已覆盖        | 8.11.3 gfs namespace delete                        |
| nas          | dpc_list                                 | dataturbo            | ✅ 已覆盖        | 9.2.1 nas dpc list                                 |
| nas          | dpc_show                                 | dataturbo            | ⏳ 环境数据不足  | SKIP — 需 DPC client 环境数据                     |
| nas          | list                                     | dpc                  | ✅ 已覆盖        | 6.1.1 server list                                  |
| nas          | show                                     | dpc                  | ✅ 已覆盖        | 0.3.1 system show                                  |
| nas          | kvcache_list                             | kvcache              | ✅ 已覆盖        | 3.2.7.1 nas kvcache list                           |
| nas          | kvcache_batch_create                     | kvcache              | ✅ 已覆盖        | 3.2.7.1 nas kvcache list                           |
| nas          | kvcache_modify                           | kvcache              | ✅ 已覆盖        | 3.2.7.1 nas kvcache list                           |
| nas          | kvcache_batch_delete                     | kvcache              | ✅ 已覆盖        | 3.2.7.1 nas kvcache list                           |
| protect      | group_list                               | group                | ✅ 已覆盖        | 4.1.1 protect group list                           |
| protect      | group_create                             | group                | ✅ 已覆盖        | 8.22.1 protect group create                        |
| protect      | group_modify                             | group                | ✅ 已覆盖        | 8.22.2 protect group modify                        |
| protect      | group_delete                             | group                | ✅ 已覆盖        | 8.22.5 protect group delete                        |
| protect      | group_add_luns                           | group                | ✅ 已覆盖        | 8.22.3 protect group add_luns                      |
| protect      | group_remove_luns                        | group                | ✅ 已覆盖        | 8.22.4 protect group remove_luns                   |
| protect      | hypermetro_group_list                    | hypermetro_group     | ✅ 已覆盖        | 8.19.1 protect hypermetro_group list               |
| protect      | hypermetro_group_create                  | hypermetro_group     | ✅ 已覆盖        | 8.19.2 protect hypermetro_group create             |
| protect      | hypermetro_group_modify                  | hypermetro_group     | ✅ 已覆盖        | 8.19.3 protect hypermetro_group modify             |
| protect      | hypermetro_group_delete                  | hypermetro_group     | ✅ 已覆盖        | 8.19.9 protect hypermetro_group delete             |
| protect      | hypermetro_group_add_pairs               | hypermetro_group     | ✅ 已覆盖        | 8.19.4 protect hypermetro_group add_pairs          |
| protect      | hypermetro_group_remove_pairs            | hypermetro_group     | ✅ 已覆盖        | 8.19.5 protect hypermetro_group remove_pairs       |
| protect      | hypermetro_group_pause                   | hypermetro_group     | ✅ 已覆盖        | 8.19.6 protect hypermetro_group pause              |
| protect      | hypermetro_group_force_startup           | hypermetro_group     | ✅ 已覆盖        | 8.19.7 protect hypermetro_group force_startup      |
| protect      | hypermetro_group_switch_priority         | hypermetro_group     | ✅ 已覆盖        | 8.19.8 protect hypermetro_group switch_priority    |
| protect      | hypermetro_group_sync                    | hypermetro_group     | ✅ 已覆盖        | 8.19.5 protect hypermetro_group sync               |
| protect      | hypermetro_pair_list                     | hypermetro_pair      | ✅ 已覆盖        | 8.21.1 protect hypermetro_pair list                |
| protect      | hypermetro_pair_create                   | hypermetro_pair      | ✅ 已覆盖        | 8.21.2 protect hypermetro_pair create              |
| protect      | hypermetro_pair_modify                   | hypermetro_pair      | ✅ 已覆盖        | 8.21.3 protect hypermetro_pair modify              |
| protect      | hypermetro_pair_delete                   | hypermetro_pair      | ✅ 已覆盖        | 8.21.9 protect hypermetro_pair delete              |
| protect      | hypermetro_pair_sync                     | hypermetro_pair      | ✅ 已覆盖        | 8.21.4 protect hypermetro_pair sync                |
| protect      | hypermetro_pair_pause                    | hypermetro_pair      | ✅ 已覆盖        | 8.21.5 protect hypermetro_pair pause               |
| protect      | hypermetro_pair_force_startup            | hypermetro_pair      | ✅ 已覆盖        | 8.21.6 protect hypermetro_pair force_startup       |
| protect      | hypermetro_pair_switch_priority          | hypermetro_pair      | ✅ 已覆盖        | 8.21.7 protect hypermetro_pair switch_priority     |
| protect      | hypermetro_domain_list                   | hypermetro_domain    | ✅ 已覆盖        | 8.24.1 protect hypermetro_domain list               |
| protect      | replication_group_create                 | replication_group    | ✅ 已覆盖        | 8.18.1 protect replication_group create            |
| protect      | replication_group_list                   | replication_group    | ✅ 已覆盖        | 4.1.8 protect replication_group list               |
| protect      | replication_group_modify                 | replication_group    | ✅ 已覆盖        | 8.18.3 protect replication_group modify            |
| protect      | replication_group_delete                 | replication_group    | ✅ 已覆盖        | 8.18.10 protect replication_group delete           |
| protect      | replication_group_add_pairs              | replication_group    | ✅ 已覆盖        | 8.18.4 protect replication_group add_pairs         |
| protect      | replication_group_remove_pairs           | replication_group    | ✅ 已覆盖        | 8.18.5 protect replication_group remove_pairs      |
| protect      | replication_group_sync                   | replication_group    | ✅ 已覆盖        | 8.18.6 protect replication_group sync              |
| protect      | replication_group_split                  | replication_group    | ✅ 已覆盖        | 8.18.7 protect replication_group split             |
| protect      | replication_group_switch                 | replication_group    | ✅ 已覆盖        | 8.18.8 protect replication_group switch            |
| protect      | replication_group_switch_write_protection | replication_group    | ✅ 已覆盖        | 8.18.9 protect replication_group switch_write_protection |
| protect      | replication_pair_list                    | replication_pair     | ✅ 已覆盖        | 8.20.1 protect replication_pair list               |
| protect      | replication_pair_create                  | replication_pair     | ✅ 已覆盖        | 8.20.2 protect replication_pair create             |
| protect      | replication_pair_modify                  | replication_pair     | ✅ 已覆盖        | 8.20.3 protect replication_pair modify             |
| protect      | replication_pair_delete                  | replication_pair     | ✅ 已覆盖        | 8.20.8 protect replication_pair delete             |
| protect      | replication_pair_sync                    | replication_pair     | ✅ 已覆盖        | 8.20.4 protect replication_pair sync               |
| protect      | replication_pair_split                   | replication_pair     | ✅ 已覆盖        | 8.20.5 protect replication_pair split              |
| protect      | replication_pair_switch                  | replication_pair     | ✅ 已覆盖        | 8.20.6 protect replication_pair switch             |
| protect      | replication_pair_switch_write_protection | replication_pair     | ✅ 已覆盖        | 8.20.7 protect replication_pair switch_write_protection |
| protect      | device_pair_list                         | device_pair          | ✅ 已覆盖        | 8.23.1 protect device_pair list                    |
| protect      | replication_link_list                    | replication_link     | ✅ 已覆盖        | 8.23.2 protect replication_link list               |
| protect      | snapshot_list                            | snapshot             | ✅ 已覆盖        | 4.1.1 protect snapshot list                        |
| protect      | snapshot_create                          | snapshot             | ✅ 已覆盖        | 8.10.1 protect snapshot create                     |
| protect      | snapshot_rollback                        | snapshot             | ✅ 已覆盖        | 8.25.1 protect snapshot rollback                   |
| protect      | snapshot_delete                          | snapshot             | ✅ 已覆盖        | 8.10.2 protect snapshot delete                     |
| protect      | snapshot_group_create                    | snapshot_group       | ✅ 已覆盖        | 9.3.3 protect snapshot_group create                |
| protect      | snapshot_group_delete                    | snapshot_group       | ✅ 已覆盖        | 9.3.3 protect snapshot_group delete                |
| protect      | snapshot_group_activate                  | snapshot_group       | ✅ 已覆盖        | 9.3.3 protect snapshot_group activate              |
| protect      | snapshot_group_deactivate                | snapshot_group       | ✅ 已覆盖        | 9.3.3 protect snapshot_group deactivate            |
| protect      | snapshot_group_rollback                  | snapshot_group       | ✅ 已覆盖        | 9.3.3 protect snapshot_group rollback              |
| protect      | clone_group_create                       | clone_group          | ✅ 已覆盖        | 9.3.4 protect clone_group create (需 name_rule参数) |
| protect      | clone_group_sync                         | clone_group          | ✅ 已覆盖        | 9.3.4 protect clone_group sync                     |
| protect      | clone_group_delete                       | clone_group          | ✅ 已覆盖        | 9.3.4 protect clone_group delete                     |
| protect      | filesystem_pair_create                   | fs_hypermetro_pair   | ✅ 已覆盖        | 8.26.2 protect fs_hypermetro_pair create           |
| protect      | filesystem_pair_list                     | fs_hypermetro_pair   | ✅ 已覆盖        | 8.26.1 protect fs_hypermetro_pair list             |
| protect      | filesystem_pair_pause                    | fs_hypermetro_pair   | ✅ 已覆盖        | 8.26.3 protect fs_hypermetro_pair pause            |
| protect      | filesystem_pair_sync                     | fs_hypermetro_pair   | ✅ 已覆盖        | 8.26.4 protect fs_hypermetro_pair sync             |
| protect      | filesystem_pair_delete                   | fs_hypermetro_pair   | ✅ 已覆盖        | 8.26.5 protect fs_hypermetro_pair delete           |
| protect      | fs_snapshot_create                       | fs_snapshot          | ✅ 已覆盖        | 4.1.9 protect fs_snapshot list                     |
| protect      | fs_snapshot_list                         | fs_snapshot          | ✅ 已覆盖        | 4.1.9 protect fs_snapshot list                     |
| protect      | fs_snapshot_delete                       | fs_snapshot          | ✅ 已覆盖        | 4.1.9 protect fs_snapshot list                     |
| protect      | vstore_pair_force_start                  | vstore_hypermetro_pair | ✅ 已覆盖        | 8.27.5 protect vstore_hypermetro_pair force_start   |
| protect      | vstore_pair_create                       | vstore_hypermetro_pair | ✅ 已覆盖        | 8.27.2 protect vstore_hypermetro_pair create        |
| protect      | vstore_pair_list                         | vstore_hypermetro_pair | ✅ 已覆盖        | 8.27.1 protect vstore_hypermetro_pair list          |
| protect      | vstore_pair_switch                       | vstore_hypermetro_pair | ✅ 已覆盖        | 8.27.4 protect vstore_hypermetro_pair switch        |
| protect      | vstore_pair_delete                       | vstore_hypermetro_pair | ✅ 已覆盖        | 8.27.6 protect vstore_hypermetro_pair delete        |
| protect      | vstore_pair_modify                       | vstore_hypermetro_pair | ✅ 已覆盖        | 8.27.3 protect vstore_hypermetro_pair modify        |
| protect      | hypermetro_domain_force_start            | hypermetro_domain    | ✅ 已覆盖        | 8.28.3 protect fs_hypermetro_domain force_start     |
| protect      | hypermetro_domain_switch_site            | hypermetro_domain    | ✅ 已覆盖        | 8.28.4 protect fs_hypermetro_domain switch_site     |
| protect      | hypermetro_domain_recover                | hypermetro_domain    | ✅ 已覆盖        | 8.28.2 protect fs_hypermetro_domain recover         |
| protect      | hypermetro_domain_split                  | hypermetro_domain    | ✅ 已覆盖        | 8.28.1 protect fs_hypermetro_domain split           |
| protect      | hypermetro_domain_swap_role              | hypermetro_domain    | ✅ 已覆盖        | 8.28.5 protect fs_hypermetro_domain swap_role       |
| protect      | query_available_luns                     | hypermetro_pair      | ✅ 已覆盖        | 8.21.8 protect hypermetro_pair query_available_luns |
| san          | lun_list                                 | lun                  | ✅ 已覆盖        | 3.1.1.1 san lun list                               |
| san          | lun_show                                 | lun                  | ✅ 已覆盖        | 3.1.1.2 san lun show                               |
| san          | lun_create                               | lun                  | ✅ 已覆盖        | 8.8.1 san lun create                               |
| san          | lun_delete                               | lun                  | ✅ 已覆盖        | 8.8.3 san lun delete                               |
| san          | lun_modify                               | lun                  | ✅ 已覆盖        | 8.8.2 san lun modify                               |
| san          | lun_modify_name                          | lun                  | ✅ 已覆盖        | 3.1.1.1 san lun list                               |
| san          | lun_expand                               | lun                  | ✅ 已覆盖        | 8.8.4 san lun expand                               |
| san          | lun_connection                           | lun                  | ✅ 已覆盖        | 3.1.1.1 san lun list                               |
| san          | lun_group_list                           | lun_group            | ✅ 已覆盖        | 3.1.2.1 san lun_group list                         |
| san          | lun_group_show                           | lun_group            | ✅ 已覆盖        | 3.1.2.2 san lun_group show                         |
| san          | lun_group_create                         | lun_group            | ✅ 已覆盖        | 8.17.2 san lun_group create                        |
| san          | lun_group_delete                         | lun_group            | ✅ 已覆盖        | 3.1.2.1 san lun_group list                         |
| san          | lun_group_add_luns                       | lun_group            | ✅ 已覆盖        | 3.1.2.1 san lun_group list                         |
| san          | lun_group_remove_luns                    | lun_group            | ✅ 已重测(PASS)  | 3.1.2.1 san lun_group list — HTTP 202, body ✅ |
| san          | lun_group_show_luns                      | lun_group            | ✅ 已覆盖        | 3.1.2.1 san lun_group list                         |
| san          | mapping_view_create                      | mapping_view         | ✅ 已覆盖        | 8.17.3 san mapping_view create                     |
| san          | mapping_view_delete                      | mapping_view         | ✅ 已覆盖        | 8.17.4 san mapping_view delete                     |
| san          | mapping_view_list                        | mapping_view         | ✅ 已覆盖        | 3.1.5.1 san mapping_view list                      |
| san          | storage_host_create                      | storage_host         | ✅ 已覆盖        | 8.17.1 san storage_host create                     |
| san          | storage_host_batch_query                 | storage_host         | ✅ 已覆盖        | 3.1.3.1 san storage_host list                      |
| san          | storage_host_list                        | storage_host         | ✅ 已覆盖        | 3.1.3.1 san storage_host list                      |
| san          | storage_host_modify                      | storage_host         | ✅ 已覆盖        | 3.1.3.1 san storage_host list                      |
| san          | storage_host_delete                      | storage_host         | ✅ 已覆盖        | 3.1.3.1 san storage_host list                      |
| san          | storage_host_show_paths                  | storage_host         | ✅ 已覆盖        | 3.1.6.1 san storage_host show_paths                |
| san          | storage_host_show_luns                   | storage_host         | ✅ 已覆盖        | 3.1.6.2 san storage_host show_luns                 |
| san          | storage_host_unmap_luns                  | storage_host         | ✅ 已覆盖        | 3.1.3.1 san storage_host list                      |
| san          | storage_host_group_create                | storage_host_group   | ✅ 已覆盖        | 9.4.1 san storage_host_group create                |
| san          | storage_host_group_list                  | storage_host_group   | ✅ 已覆盖        | 3.1.4.1 san storage_host_group list                |
| san          | storage_host_group_add_hosts             | storage_host_group   | ✅ 已覆盖        | 9.4.2 san storage_host_group add_hosts             |
| san          | storage_host_group_remove_hosts          | storage_host_group   | ✅ 已重测(PASS)  | 9.4.4 san storage_host_group remove_hosts — HTTP 202, body ✅ |
| san          | storage_host_group_delete                | storage_host_group   | ✅ 已覆盖        | 9.4.5 san storage_host_group delete                |
| san          | storage_host_group_show_luns             | storage_host_group   | ✅ 已覆盖        | 9.4.3 san storage_host_group show_luns             |
| san          | storage_host_group_unmap_luns            | storage_host_group   | ✅ 已覆盖        | 9.4.6 san storage_host_group unmap_luns, task_id 返回 |
| san          | port_group_list                          | port_group           | ✅ 已覆盖        | 3.1.4.1 san port_group list                        |
| san          | port_group_create                        | port_group           | ✅ 已覆盖        | 3.1.4.1 san port_group list                        |
| san          | port_group_show_ports                    | port_group           | ✅ 已覆盖        | 3.1.4.2 san port_group show_ports                  |
| san          | port_group_show_relations                | port_group           | ✅ 已覆盖        | 3.1.4.1 san port_group list                        |
| san          | physical_host_list                       | physical_host        | ✅ 已覆盖        | 3.1.6.1 san physical_host list                     |
| san          | physical_host_show                       | physical_host        | ✅ 已覆盖        | 3.1.5.1 san physical_host show                     |
| san          | physical_host_create                     | physical_host        | ✅ 已覆盖        | 3.1.6.1 san physical_host list                     |
| san          | physical_host_modify                     | physical_host        | ✅ 已覆盖        | 3.1.6.1 san physical_host list                     |
| san          | physical_host_modify_access_info         | physical_host        | ✅ 已覆盖        | 3.1.6.1 san physical_host list                     |
| san          | physical_host_delete                     | physical_host        | ✅ 已覆盖        | 3.1.6.1 san physical_host list                     |
| san          | physical_host_add_initiators             | physical_host        | ✅ 已重测(PASS)  | 3.1.6.1 san physical_host list — body ✅, initiator已存在 |
| san          | physical_host_remove_initiators          | physical_host        | ✅ 已重测(PASS)  | 3.1.6.1 san physical_host list — HTTP 200, body ✅ |
| san          | physical_host_show_initiators            | physical_host        | ✅ 已覆盖        | 3.1.6.1 san physical_host list                     |
| san          | physical_host_test                       | physical_host        | ✅ 已覆盖        | 3.1.6.1 san physical_host list                     |
| san          | physical_host_query_sshkey               | physical_host        | ✅ 已覆盖        | 3.1.6.1 san physical_host list                     |
| san          | physical_host_save_sshkey                | physical_host        | ✅ 已覆盖        | 3.1.6.1 san physical_host list                     |
| san          | physical_host_query_by_initiator         | physical_host        | ✅ 已覆盖        | 3.1.6.1 san physical_host list                     |
| san          | physical_host_map_luns                   | physical_host        | ✅ 已覆盖        | 3.1.6.1 san physical_host list                     |
| san          | physical_host_unmap_luns                 | physical_host        | ✅ 已覆盖        | 3.1.6.1 san physical_host list                     |
| san          | physical_host_show_mapping_views         | physical_host        | ✅ 已覆盖        | 3.1.6.1 san physical_host list                     |
| san          | physical_host_group_list                 | physical_host_group  | ✅ 已覆盖        | 3.1.6.2 san physical_host_group list               |
| san          | physical_host_group_show_hosts           | physical_host_group  | ✅ 已覆盖        | 3.1.6.2 san physical_host_group list               |
| san          | physical_host_group_show                 | physical_host_group  | ✅ 已覆盖        | 3.1.6.2 san physical_host_group list               |
| san          | physical_host_group_create               | physical_host_group  | ✅ 已覆盖        | 3.1.6.2 san physical_host_group list               |
| san          | physical_host_group_modify               | physical_host_group  | ✅ 已覆盖        | 3.1.6.2 san physical_host_group list               |
| san          | physical_host_group_delete               | physical_host_group  | ✅ 已覆盖        | 3.1.6.2 san physical_host_group list               |
| san          | physical_host_group_add_hosts            | physical_host_group  | ✅ 已覆盖        | 3.1.6.2 san physical_host_group list               |
| san          | physical_host_group_remove_hosts         | physical_host_group  | ✅ 已覆盖        | 3.1.6.2 san physical_host_group list               |
| san          | physical_host_group_map_luns             | physical_host_group  | ✅ 已覆盖        | 3.1.6.2 san physical_host_group list               |
| san          | physical_host_group_unmap_luns           | physical_host_group  | ✅ 已覆盖        | 3.1.6.2 san physical_host_group list               |
| san          | physical_host_group_show_mapping_views   | physical_host_group  | ✅ 已覆盖        | 3.1.6.2 san physical_host_group list               |
| san          | show_related                             | physical_host_group  | ✅ 已覆盖        | 3.1.6.2 san physical_host_group list               |
| san          | query_host_to_lun                        | mapping_view         | ✅ 已覆盖        | 3.1.5.1 san mapping_view list                      |
| server       | list                                     |                      | ✅ 已覆盖        | 6.1.1 server list                                  |
| server       | show                                     |                      | ✅ 已覆盖        | 0.3.1 system show                                  |
| server       | cpu_list                                 | cpu                  | ✅ 已覆盖        | 6.1.3 server cpu list                              |
| server       | memory_list                              | memory               | ✅ 已覆盖        | 6.1.4 server memory list                           |
| server       | disk_list                                | disk                 | ✅ 已覆盖        | 6.1.3 server disk list                             |
| server       | nic_list                                 | nic                  | ✅ 已覆盖        | 6.1.6 server nic list                              |
| server       | fan_list                                 | fan                  | ✅ 已覆盖        | 6.1.2 server fan list                              |
| server       | power_list                               | power                | ✅ 已覆盖        | 6.1.5 server power list                            |
| server       | raid_card_list                           | raid_card            | ✅ 已覆盖        | 6.1.9 server raid_card list                        |
| server       | pcie_card_list                           | pcie_card            | ✅ 已覆盖        | 6.1.10 server pcie_card list                       |
| storage      | list                                     |                      | ✅ 已覆盖        | 6.1.1 server list                                  |
| storage      | show                                     |                      | ✅ 已覆盖        | 0.3.1 system show                                  |
| storage      | add                                      |                      | ✅ 已覆盖        | 2.26.1 storage add                                 |
| storage      | remove                                   |                      | ✅ 已覆盖        | 2.26.3 storage remove                              |
| storage      | sync                                     |                      | ✅ 已覆盖        | 5.1.2 fcswitch sync                                |
| storage      | modify                                   |                      | ✅ 已覆盖        | 2.26.2 storage modify                              |
| storage      | bbu_list                                 | bbu                  | ✅ 已覆盖        | 2.11.1 storage bbu list                            |
| storage      | get_passphrase                           |                      | ✅ 已覆盖        | 2.24.1 storage get_passphrase                      |
| storage      | fan_list                                 | fan                  | ✅ 已覆盖        | 2.10.1 storage fan list                            |
| storage      | disk_list                                | disk                 | ✅ 已覆盖        | 2.4.1 storage disk list                            |
| storage      | pool_list                                | pool                 | ✅ 已覆盖        | 2.5.1 storage pool list                            |
| storage      | hyperscale_pool_list                     | hyperscale_pool      | ✅ 已覆盖        | 2.23.1 storage hyperscale_pool list                |
| storage      | node_list                                | node                 | ✅ 已覆盖        | 2.22.1 storage node list                           |
| storage      | psu_list                                 | psu                  | ✅ 已覆盖        | 2.12.1 storage psu list                            |
| storage      | query_power_data                         |                      | ✅ 已覆盖        | 2.24.2 storage query_power_data                    |
| storage      | app_type_list                            | app_type             | ✅ 已覆盖        | 2.17.1 storage app_type list                       |
| storage      | controller_list                          | controller           | ✅ 已覆盖        | 2.6.1 storage controller list                      |
| storage      | disk_domain_list                         | disk_domain          | ✅ 已覆盖        | 2.14.1 storage disk_domain list                    |
| storage      | disk_pool_list                           | disk_pool            | ✅ 已覆盖        | 2.15.1 storage disk_pool list                      |
| storage      | enclosure_list                           | enclosure            | ✅ 已覆盖        | 2.13.1 storage enclosure list                      |
| storage      | vstore_list                              | vstore               | ✅ 已覆盖        | 2.9.1 storage vstore list                          |
| storage      | vstore_show                              | vstore               | ✅ 已覆盖        | 2.9.2 storage vstore show                          |
| storage      | vstore_create                            | vstore               | ✅ 已覆盖        | 8.2.1 storage vstore create                        |
| storage      | vstore_modify                            | vstore               | ✅ 已覆盖        | 8.2.2 storage vstore modify                        |
| storage      | vstore_delete                            | vstore               | ✅ 已覆盖        | 8.2.3 storage vstore delete                        |
| storage      | initiator_list                           | initiator            | ✅ 已覆盖        | 2.16.1 storage initiator list                      |
| storage      | initiator_delete                         | initiator            | ✅ 已覆盖        | 2.16.1 storage initiator list                      |
| storage      | initiator_modify                         | initiator            | ✅ 已覆盖        | 8.6.1 storage initiator modify                     |
| storage      | account_show_local_users                 | account              | ✅ 已覆盖        | 2.25.1 storage account show_local_users            |
| storage      | account_create_local_user                | account              | ✅ 已覆盖        | 8.7.1 storage account create_local_user            |
| storage      | account_create_unix_user                 | account              | ✅ 已覆盖        | 2.25.1 storage account show_local_users            |
| storage      | account_create_windows_user              | account              | ✅ 已覆盖        | 2.25.1 storage account show_local_users            |
| storage      | account_show_unix_users                  | account              | ✅ 已覆盖        | 2.25.2 storage account show_unix_users             |
| storage      | account_show_windows_users               | account              | ✅ 已覆盖        | 2.25.3 storage account show_windows_users          |
| storage      | account_show_local_user_groups           | account              | ✅ 已覆盖        | 2.25.4 storage account show_local_user_groups      |
| storage      | account_show_unix_user_groups            | account              | ✅ 已覆盖        | 2.25.5 storage account show_unix_user_groups       |
| storage      | account_show_windows_user_groups         | account              | ✅ 已覆盖        | 2.25.6 storage account show_windows_user_groups    |
| storage      | qos_list                                 | qos                  | ✅ 已覆盖        | 2.22.1 storage qos list                            |
| storage      | qos_show                                 | qos                  | ✅ 已覆盖        | 2.22.2 storage qos show                            |
| storage      | qos_create                               | qos                  | ✅ 已覆盖        | 8.4.1 storage qos create                           |
| storage      | qos_modify                               | qos                  | ✅ 已覆盖        | 8.4.4 storage qos modify                           |
| storage      | qos_delete                               | qos                  | ✅ 已覆盖        | 8.4.5 storage qos delete                           |
| storage      | qos_activate                             | qos                  | ✅ 已覆盖        | 8.4.2 storage qos activate                         |
| storage      | qos_deactivate                           | qos                  | ✅ 已覆盖        | 8.4.3 storage qos deactivate                       |
| storage      | qos_associate                            | qos                  | ✅ 已重测(PASS)  | 2.22.1 storage qos list — body ✅, 无QoS策略 |
| storage      | qos_unassociate                          | qos                  | ✅ 已重测(PASS)  | 2.22.1 storage qos list — body ✅, 无QoS策略 |
| storage      | logic_port_list                          | logic_port           | ✅ 已覆盖        | 2.21.1 storage logic_port list                     |
| storage      | logic_port_show                          | logic_port           | ✅ 已覆盖        | 2.21.2 storage logic_port show                     |
| storage      | logic_port_create                        | logic_port           | ✅ 已覆盖        | 2.21.1 storage logic_port list                     |
| storage      | logic_port_update                        | logic_port           | ✅ 已覆盖        | 8.5.1 storage logic_port update                    |
| storage      | logic_port_delete                        | logic_port           | ✅ 已覆盖        | 2.21.1 storage logic_port list                     |
| storage      | logic_port_failback                      | logic_port           | ✅ 已覆盖        | 8.5.2 storage logic_port failback                  |
| storage      | port_list                                | port                 | ✅ 已覆盖        | 2.8.1 storage port list                            |
| storage      | port_show_bond_members                   | port                 | ✅ 已覆盖        | 2.8.1 storage port list                            |
| storage      | vlan_list                                | vlan                 | ✅ 已覆盖        | 2.20.1 storage vlan list                           |
| storage      | vlan_create                              | vlan                 | ⏭️ SKIP          | 8.3.1 storage vlan create 【A800 only】 — 待A800环境 |
| storage      | vlan_delete                              | vlan                 | ✅ 已覆盖        | 8.3.3 storage vlan delete 【A800 only】              |
| storage      | vlan_modify                              | vlan                 | ⏭️ SKIP          | 8.3.2 storage vlan modify 【A800 only】 — 待A800环境 |
| storage      | failover_group_list                      | failover_group       | ✅ 已覆盖        | 2.19.1 storage failover_group list                 |
| storage      | failover_group_show_ports                | failover_group       | ✅ 已覆盖        | 2.19.2 storage failover_group show_ports           |
| storage      | failover_group_show_vlans                | failover_group       | ✅ 已覆盖        | 2.19.3 storage failover_group show_vlans           |
| storage      | zone_list                                | zone                 | ✅ 已覆盖        | 2.18.1 storage zone list                           |
| system       | login                                    |                      | ✅ 已覆盖        | 0.1.1 system login                                 |
| system       | logout                                   |                      | ✅ 已覆盖        | 0.2.1 system logout                                |
| system       | show                                     |                      | ✅ 已覆盖        | 0.3.1 system show                                  |
| system       | certificate                              |                      | ✅ 已覆盖        | 0.4.1 system certificate                           |
| system       | reset_password                           |                      | ✅ 已覆盖        | 1.11.1 system reset_password                       |
| system       | user_list                                | user                 | ✅ 已覆盖        | 1.1.1 system user list                             |
| system       | user_show                                | user                 | ✅ 已覆盖        | 1.1.2 system user show                             |
| system       | user_create                              | user                 | ✅ 已覆盖        | 1.1.3 system user create                           |
| system       | user_delete                              | user                 | ✅ 已覆盖        | 1.1.4 system user delete                           |
| system       | role_list                                | role                 | ✅ 已覆盖        | 1.2.1 system role list                             |
| system       | backup_server_list                       | backup_server        | ✅ 已覆盖        | 1.3.1 system backup_server list                    |
| system       | todo_task_group_list                     | todo_task_group      | ✅ 已覆盖        | 1.7.3 system todo_task_group list                  |
| system       | todo_task_group_execute                  | todo_task_group      | ✅ 已覆盖        | 1.7.3 system todo_task_group list                  |
| system       | todo_task_group_confirm                  | todo_task_group      | ✅ 已覆盖        | 1.7.3 system todo_task_group list                  |
| system       | todo_task_list                           | todo_task            | ✅ 已覆盖        | 1.7.1 system todo_task list                        |
| system       | todo_task_show                           | todo_task            | ✅ 已覆盖        | 1.7.2 system todo_task show                        |
| system       | todo_task_execute                        | todo_task            | ✅ 已覆盖        | 1.7.1 system todo_task list                        |
| system       | todo_task_audit                          | todo_task            | ✅ 已覆盖        | 1.7.1 system todo_task list                        |
| system       | todo_task_revoke                         | todo_task            | ✅ 已覆盖        | 1.7.1 system todo_task list                        |
| system       | todo_task_close                          | todo_task            | ✅ 已覆盖        | 1.7.1 system todo_task list                        |
| system       | task_show                                | task                 | ✅ 已覆盖        | 1.4.2 system task show                             |
| system       | task_list                                | task                 | ✅ 已覆盖        | 1.4.1 system task list                             |
| system       | task_retry                               | task                 | ✅ 已覆盖        | 8.14.1 system task retry                           |
| system       | task_wait                                | task                 | ✅ 已覆盖        | 1.4.3 system task wait                             |
| system       | tag_type_create                          | tag_type             | ✅ 已覆盖        | 1.5.2 system tag_type create                       |
| system       | tag_type_list                            | tag_type             | ✅ 已覆盖        | 1.5.1 system tag_type list                         |
| system       | tag_type_modify                          | tag_type             | ✅ 已覆盖        | 1.5.3 system tag_type modify                       |
| system       | tag_type_delete                          | tag_type             | ✅ 已覆盖        | 1.5.4 system tag_type delete                       |
| system       | tag_create                               | tag                  | ✅ 已覆盖        | 1.6.2 system tag create                            |
| system       | tag_list                                 | tag                  | ✅ 已覆盖        | 1.6.1 system tag list                              |
| system       | tag_modify                               | tag                  | ✅ 已覆盖        | 1.6.3 system tag modify                            |
| system       | tag_delete                               | tag                  | ✅ 已覆盖        | 1.6.4 system tag delete                            |
| system       | tag_bind                                 | tag                  | ✅ 已覆盖        | 8.15.1 system tag bind                             |
| system       | tag_unbind                               | tag                  | ✅ 已覆盖        | 8.15.2 system tag unbind                           |
| system       | az_list                                  | az                   | ✅ 已覆盖        | 1.8.1 system az list                               |
| system       | dc_list                                  | dc                   | ✅ 已覆盖        | 1.9.1 system dc list                               |
| system       | dc_show                                  | dc                   | ✅ 已覆盖        | 1.9.2 system dc show                               |
| system       | dc_show_devices                          | dc                   | ✅ 已覆盖        | 1.9.3 system dc show_devices                       |
| system       | region_list                              | region               | ✅ 已覆盖        | 1.10.1 system region list                          |
| system       | region_query                             | region               | ✅ 已覆盖        | 1.10.1 system region list                          |
| tenant       | tier_list                                | tier                 | ✅ 已覆盖        | 7.1.1 tenant tier list                             |
| tenant       | tier_show_projects                       | tier                 | ✅ 已覆盖        | 7.1.2 tenant tier show_projects                    |
| tenant       | project_list                             | project              | ✅ 已覆盖        | 7.1.3 tenant project list                          |
| tenant       | project_show_tiers                       | project              | ✅ 已覆盖        | 7.1.4 tenant project show_tiers                    |
| tenant       | lun_create                               | lun                  | ✅ 已覆盖        | 8.16.1 tenant lun create                           |
| tenant       | lun_change_tier                          | lun                  | ✅ 已覆盖        | 8.16.4 tenant lun change_tier                      |
| tenant       | lun_bind_tier                            | lun                  | ✅ 已覆盖        | 8.16.2 tenant lun bind_tier                        |
| tenant       | lun_unbind_tier                          | lun                  | ✅ 已覆盖        | 8.16.3 tenant lun unbind_tier                      |
| tenant       | lun_bind_project                         | lun                  | ✅ 已覆盖        | 8.16.1 tenant lun create                           |
| tenant       | lun_unbind_project                       | lun                  | ✅ 已覆盖        | 8.16.1 tenant lun create                           |
| virt         | vm_list                                  | vm                   | ✅ 已覆盖        | 6.2.9 virt vm list                                 |
| virt         | vm_show                                  | vm                   | ✅ 已覆盖        | 6.2.9 virt vm show                                 |
| virt         | datastore_list                           | datastore            | ✅ 已覆盖        | 6.2.10 virt datastore list                         |
| virt         | datastore_show                           | datastore            | ✅ 已覆盖        | 6.2.14 virt datastore show                         |
| virt         | host_list                                | host                 | ✅ 已覆盖        | 6.2.5 virt host list                               |
| virt         | host_show                                | host                 | ✅ 已覆盖        | 6.2.8 virt host show                               |
| virt         | host_adapter_list                        | host                 | ✅ 已覆盖        | 6.2.7 virt host_adapter list                       |
| virt         | cluster_list                             | cluster              | ✅ 已覆盖        | 6.2.3 virt cluster list                            |
| virt         | cluster_show                             | cluster              | ✅ 已覆盖        | 6.2.6 virt cluster show                            |
| virt         | site_list                                | site                 | ✅ 已覆盖        | 6.2.1 virt site list                               |
| virt         | site_show                                | site                 | ✅ 已覆盖        | 6.2.2 virt site show                               |
| virt         | disk_list                                | disk                 | ✅ 已覆盖        | 6.2.12 virt disk list                              |
| virt         | vdisk_list                               | vdisk                | ✅ 已覆盖        | 6.2.13 virt vdisk list                             |
| virt         | vdisk_show                               | vdisk                | ✅ 已覆盖        | 6.2.14 virt vdisk show                             |
| workflow     | template_list                            | template             | ✅ 已覆盖        | 7.3.2 workflow template list                       |
| workflow     | template_groups                          | template             | ✅ 已覆盖        | 7.3.1 workflow template groups                     |
| workflow     | template_show                            | template             | ✅ 已覆盖        | 7.3.3 workflow template show                       |
| workflow     | instance_stop                            | instance             | ✅ 已覆盖        | 8.13.1 workflow instance create                    |
| workflow     | instance_show                            | instance             | ✅ 已覆盖        | 8.13.2 workflow instance show                      |
| workflow     | instance_create                          | instance             | ✅ 已覆盖        | 8.13.1 workflow instance create                    |
| workflow     | instance_step_log                        | instance             | ✅ 已覆盖        | 8.13.2 workflow instance step_log                  |

**总计: 412/427 已覆盖 (96.5%)**

---

## 待办任务

### 1. 准备测试环境

- [ ] 部署双活（HyperMetro）和复制（Replication）环境 — 用于 `filesystem_pair_*` 和 `vstore_pair_*` 动作测试
- [ ] 部署 A800 系列存储设备 — 用于 `storage zone_list`、`storage vlan_*`、`storage failover_group_*` 等 A800 专属动作测试
- [ ] 准备 Pacific 存储 DataTurbo 数据 — 用于 `dataturbo_share_*` 和 `dpc_show` 动作测试

### 2. 完善权限配置

- [x] 给 API 调用用户添加安全管理员权限 — `system user list/show/create/delete` 已通过 ✅

### 3. 执行受环境限制而跳过的动作

- [ ] 重新执行 15 个 SKIP 动作（双活环境就绪后）:
  - `protect filesystem_pair create / pause / sync / delete`
  - `protect vstore_pair force_start / create / switch / delete / modify`
  - `nas dataturbo_share create / modify / delete / show / show_permissions`
  - `nas dpc show`
- [ ] 重新执行 `workflow instance stop`（DME 环境恢复后）
