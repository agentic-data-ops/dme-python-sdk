# pydme 测试执行与记录库
# source 此文件后使用 exec_test 执行动作并自动记录结果

STAGE_DIR=".reasonix/scripts"
REPORT=".reasonix/plans/500-test-all-actions.md"

# 自动接受风险操作：所有 WRITE 动作无需逐个追加 --accept-risk
export DME_ACCEPT_RISK=true

ensure_stage_dir() {
  mkdir -p "$STAGE_DIR"
}

# 执行动作，记录结果到报告，提取 ID 到 stage 变量
# 用法: exec_test <test_id> <test_name> <cli_command> [stage_var=jsonpath ...]
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
