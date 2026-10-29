#!/usr/bin/env bash
# 106 计划 M4：遍历 49 个新增动作的 --help（zh_CN / en_US），验证渲染与 Risk Level
# 用法: bash .reasonix/scripts/106-verify-new-actions.sh
set -u
cd "$(dirname "$0")/../.."
export HOME=/tmp/fakehome
OUT=".reasonix/output/106-verify.md"
: > "$OUT"

fail=0
total=0

run_help() {
    local lang="$1"; shift
    local cmd_desc="$1"; shift
    local expect_risk="$1"; shift
    total=$((total+1))
    local out err rc
    out=$(DME_CLI_LANG="$lang" python3 -m pydme.cli "$@" --help 2>&1)
    rc=$?
    local risk
    risk=$(printf '%s' "$out" | grep -o 'Risk Level: [A-Za-z]*' | head -1 | awk '{print $3}')
    if [ $rc -ne 0 ]; then
        echo "FAIL [$lang] $cmd_desc: exit=$rc" | tee -a "$OUT"; fail=$((fail+1)); return
    fi
    if [ "$risk" != "$expect_risk" ]; then
        echo "FAIL [$lang] $cmd_desc: risk=$risk expect=$expect_risk" | tee -a "$OUT"; fail=$((fail+1)); return
    fi
    if ! printf '%s' "$out" | grep -q 'Description:'; then
        echo "FAIL [$lang] $cmd_desc: no Description section" | tee -a "$OUT"; fail=$((fail+1)); return
    fi
    echo "PASS [$lang] $cmd_desc (risk=$risk)" >> "$OUT"
}

# hci: 5 个 direct actions（全 Low）
for a in list show cluster_list vswitch_list storage_list; do
    run_help zh_CN "hci $a" Low hci "$a"
    run_help en_US "hci $a" Low hci "$a"
done

# virt: 44 个（高风险 21 个 High，其余 Low）
declare -A RISK=(
  [vdisk_modify]=High [vdisk_expand]=High [vdisk_delete]=High [vdisk_detach]=High
  [vm_modify]=High [vm_delete]=High [vm_power_off]=High [vm_hibernate]=High [vm_reboot]=High
  [vm_migrate]=High [vm_migrate_host]=High [vm_migrate_storage]=High [vm_umount_tools]=High
  [vm_nic_modify]=High [vm_nic_change_portgroup]=High [vm_nic_delete]=High [vm_nic_change_linkstatus]=High
  [vm_snapshot_delete]=High [vm_snapshot_recover]=High
  [vswitch_portgroup_modify]=High [vswitch_portgroup_delete]=High
)
# (subtopic, action, key)
VIRT_CMDS="
datastore host_relations datastore_host_relations
host port_list host_port_list
host aggr_port_list host_aggr_port_list
host logic_port_list host_logic_port_list
vdisk create_attach vdisk_create_attach
vdisk attach vdisk_attach
vdisk detach vdisk_detach
vdisk modify vdisk_modify
vdisk expand vdisk_expand
vdisk delete vdisk_delete
vm create vm_create
vm clone vm_clone
vm modify vm_modify
vm power_on vm_power_on
vm power_off vm_power_off
vm hibernate vm_hibernate
vm reboot vm_reboot
vm delete vm_delete
vm vnc_info vm_vnc_info
vm mount_tools vm_mount_tools
vm umount_tools vm_umount_tools
vm migrate vm_migrate
vm migrate_host vm_migrate_host
vm migrate_storage vm_migrate_storage
vm import vm_import
vm nic_list vm_nic_list
vm nic_modify vm_nic_modify
vm nic_change_portgroup vm_nic_change_portgroup
vm nic_add vm_nic_add
vm nic_delete vm_nic_delete
vm nic_change_linkstatus vm_nic_change_linkstatus
vm snapshot_list vm_snapshot_list
vm snapshot_show vm_snapshot_show
vm snapshot_create vm_snapshot_create
vm snapshot_delete vm_snapshot_delete
vm snapshot_recover vm_snapshot_recover
vswitch list vswitch_list
vswitch show vswitch_show
vswitch portgroup_list vswitch_portgroup_list
vswitch portgroup_create vswitch_portgroup_create
vswitch portgroup_modify vswitch_portgroup_modify
vswitch portgroup_delete vswitch_portgroup_delete
secgroup list secgroup_list
gpu list gpu_list
"
while read -r st a key; do
    [ -z "$st" ] && continue
    r=${RISK[$key]:-Low}
    run_help zh_CN "virt $st $a" "$r" virt "$st" "$a"
    run_help en_US "virt $st $a" "$r" virt "$st" "$a"
done <<< "$VIRT_CMDS"

echo "" >> "$OUT"
echo "TOTAL: $total runs, FAIL: $fail" | tee -a "$OUT"
[ $fail -eq 0 ]
