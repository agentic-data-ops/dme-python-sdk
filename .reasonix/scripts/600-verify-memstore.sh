#!/usr/bin/env bash
# 600 计划 M4：memstore topic 验证
#   1) 10 个动作 x zh_CN/en_US 的 --help 遍历（Risk Level 断言）
#   2) 隔离 HOME 的 mock 全链路（无需 DME 参数/环境）
#   3) 回归：其他 topic 仍要求 DME 参数
# 用法: bash .reasonix/scripts/600-verify-memstore.sh
set -u
cd "$(dirname "$0")/../.."
OUT=".reasonix/output/600-verify.md"
: > "$OUT"

export HOME="$(mktemp -d)"
export DME_ACCEPT_RISK=true
CLI="python3 -m pydme.cli"

fail=0
total=0
pass() { total=$((total+1)); echo "PASS $*" >> "$OUT"; }
bad()  { total=$((total+1)); fail=$((fail+1)); echo "FAIL $*" >> "$OUT"; }

# ---------- 1. help 遍历 ----------
run_help() {
    local lang="$1" expect="$2" desc="$3"; shift 3
    local out risk
    out=$(DME_CLI_LANG="$lang" $CLI "$@" --help 2>&1)
    if [ $? -ne 0 ]; then bad "[help] $desc ($lang): non-zero exit"; return; fi
    risk=$(printf '%s' "$out" | grep -o 'Risk Level: [A-Za-z]*' | head -1 | awk '{print $3}')
    if [ "$risk" = "$expect" ]; then
        pass "[help] $desc ($lang, risk=$risk)"
    else
        bad "[help] $desc ($lang, risk=$risk expect=$expect)"
    fi
}

while IFS='|' read -r line expect; do
    [ -z "$line" ] && continue
    read -ra parts <<< "$line"
    run_help zh_CN "$expect" "memstore $line" memstore "${parts[@]}"
    run_help en_US "$expect" "memstore $line" memstore "${parts[@]}"
done <<'EOF'
add|Low
list|Low
delete|High
disk list|Low
pool create|Low
pool list|Low
pool delete|High
namespace create|Low
namespace list|Low
namespace delete|High
EOF

# ---------- 2. mock 全链路（隔离 HOME，subprocess 调 CLI） ----------
python3 - "$OUT" <<'PYEOF'
import json
import os
import subprocess
import sys

OUT = sys.argv[1]
HOME = os.environ['HOME']
CLI = [sys.executable, '-m', 'pydme.cli']
MOCK_FILE = os.path.join(HOME, '.config', 'pydme', 'mock', 'memstore.json')

def run(*args):
    p = subprocess.run(CLI + list(args), capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr

def payload(out):
    idx = out.find('{')
    if idx < 0:
        raise ValueError('no JSON payload in output: %s' % out[:200])
    return json.loads(out[idx:])

def record(name, ok, note=''):
    line = 'PASS [mock] %s' % name if ok else 'FAIL [mock] %s %s' % (name, note)
    print(line, file=open(OUT, 'a'))
    if not ok:
        sys.exit(1)

def read_raw():
    return json.load(open(MOCK_FILE))

# seed: 首次 list 自动创建示例数据，返回摘要（不含盘/池列表）
rc, out, err = run('memstore', 'list')
seed = payload(out)['memstores'][0]
record('seed list', rc == 0 and os.path.exists(MOCK_FILE) and len(payload(out)['memstores']) == 1)
record('seed summary',
       seed['name'] == 'demo-memstore' and seed['raw_capacity'] == 65536
       and seed['pool_capacity'] == 2048 and seed['pool_used_capacity'] == 512
       and 'disks' not in seed and 'pools' not in seed)

# add: 每个记忆存储 FRAME 独立编号（新存储从 FRAME0 重新开始）；响应为摘要
rc, out, err = run('memstore', 'add', '--name', 'ms01', '--num_of_disks', '2', '--disk_size', '16384')
ms = payload(out)
record('add summary', rc == 0 and ms['name'] == 'ms01'
       and ms['raw_capacity'] == 32768 and ms['pool_capacity'] == 0
       and ms['pool_used_capacity'] == 0 and 'disks' not in ms and 'pools' not in ms)
raw = read_raw()
ms_obj = next(m for m in raw if m['id'] == ms['id'])
locs = [d['location'] for d in ms_obj['disks']]
record('add FRAME independent', len(locs) == 2 and locs == ['FRAME0.SLOT0', 'FRAME0.SLOT1'])

# list 过滤
rc, out, _ = run('memstore', 'list', '--name', 'ms01')
record('list filter', rc == 0 and len(payload(out)['memstores']) == 1
       and payload(out)['memstores'][0]['id'] == ms['id'])

# disk list: storage_id/storage_name/capacity/allocated_capacity/pools
rc, out, _ = run('memstore', 'disk', 'list')
disks = payload(out)['disks']
record('disk list fields', rc == 0 and len(disks) == 4
       and all('storage_id' in d and 'storage_name' in d and 'capacity' in d
               and 'allocated_capacity' in d and 'pools' in d for d in disks))
demo_disk = next(d for d in disks if d['storage_name'] == 'demo-memstore')
record('disk list pools', demo_disk['capacity'] == 32768
       and demo_disk['allocated_capacity'] == 1024
       and demo_disk['pools'] == [{'pool_id': demo_disk['pools'][0]['pool_id'],
                                   'pool_name': 'demo-pool',
                                   'allocated_capacity': 1024}])
rc, out, _ = run('memstore', 'disk', 'list', '--storage_id', ms['id'])
disks = payload(out)['disks']
record('disk list by storage', rc == 0 and len(disks) == 2
       and all(d['storage_id'] == ms['id'] and d['storage_name'] == 'ms01' for d in disks))

# pool create: storage_id + capacity + num_of_disks，选分配容量低的盘均分
rc, out, _ = run('memstore', 'pool', 'create', '--storage_id', ms['id'],
                 '--name', 'pool02', '--capacity', '1000', '--num_of_disks', '2')
pool = payload(out)
record('pool create split', rc == 0 and sum(d['capacity'] for d in pool['disks']) == 1000
       and all(d['capacity'] == 500 for d in pool['disks']))
disk_map = {d['id']: d for m in read_raw() for d in m['disks']}
record('pool<->disk sync',
       all(any(e['pool'] == pool['id'] for e in disk_map[d['disk']]['pools'])
           for d in pool['disks']))

# pool list: storage_id 过滤 + capacity/used_capacity
rc, out, _ = run('memstore', 'pool', 'list', '--storage_id', ms['id'])
pools = payload(out)['pools']
record('pool list by storage', rc == 0 and len(pools) == 1
       and pools[0]['name'] == 'pool02' and pools[0]['capacity'] == 1000
       and pools[0]['used_capacity'] == 0)
rc, out, _ = run('memstore', 'pool', 'list', '--name', 'demo-pool')
record('pool list demo', rc == 0 and payload(out)['pools'][0]['capacity'] == 2048
       and payload(out)['pools'][0]['used_capacity'] == 512)
pool_id = pools[0]['id']

# namespace create: capacity 参数，used_capacity 初始 0
clients = [{'ip': '192.168.1.10', 'type': 'ip'}, {'ip': '10.0.0.0/24', 'type': 'ip_segment'}]
rc, out, _ = run('memstore', 'namespace', 'create', '--pool_id', pool_id, '--name', 'ns02',
                 '--capacity', '300', '--eviction', '80', '--retention', '24',
                 '--clients', json.dumps(clients))
ns = payload(out)
record('namespace create', rc == 0 and ns['name'] == 'ns02' and ns['capacity'] == 300
       and ns['used_capacity'] == 0 and len(ns['clients']) == 2)
rc, out, _ = run('memstore', 'pool', 'list', '--storage_id', ms['id'])
record('pool used_capacity', payload(out)['pools'][0]['used_capacity'] == 300)

# namespace list: 全局 / storage_id / name / pool_id；capacity/used_capacity
rc, out, _ = run('memstore', 'namespace', 'list')
all_ns = payload(out)['namespaces']
record('ns list global', rc == 0 and len(all_ns) == 2
       and all('capacity' in n and 'used_capacity' in n for n in all_ns))
record('ns list by storage', rc == 0 and len(payload(out)['namespaces']) == 2
       and all(n['pool_name'] in ('demo-pool', 'pool02') for n in all_ns))
rc, out, _ = run('memstore', 'namespace', 'list', '--storage_id', ms['id'])
lst = payload(out)['namespaces']
record('ns list by storage filter', rc == 0 and len(lst) == 1 and lst[0]['name'] == 'ns02')
rc, out, _ = run('memstore', 'namespace', 'list', '--name', 'ns02')
record('ns list by name', rc == 0 and len(payload(out)['namespaces']) == 1
       and payload(out)['namespaces'][0]['id'] == ns['id'])
rc, out, _ = run('memstore', 'namespace', 'list', '--pool_id', pool_id)
record('ns list by pool', rc == 0 and len(payload(out)['namespaces']) == 1
       and payload(out)['namespaces'][0]['pool_name'] == 'pool02')
record('ns pool_name', lst[0]['pool_name'] == 'pool02')

# 负例：非法输入给出明确报错且不破坏文件
before = open(MOCK_FILE).read()
neg = [
    (('memstore', 'add', '--name', 'x', '--num_of_disks', '1', '--disk_size', '1000'), 'disk_size'),
    (('memstore', 'namespace', 'create', '--pool_id', pool_id, '--name', 'ns03',
      '--capacity', '99999', '--eviction', '80', '--retention', '24'), 'capacity over pool'),
    (('memstore', 'pool', 'delete', '--id', pool_id), 'pool delete with ns'),
    (('memstore', 'namespace', 'delete', '--id', 'nope'), 'ns not found'),
    (('memstore', 'pool', 'create', '--storage_id', ms['id'], '--name', 'p',
      '--capacity', '99999', '--num_of_disks', '2'), 'free capacity'),
    (('memstore', 'pool', 'create', '--storage_id', ms['id'], '--name', 'p',
      '--capacity', '100', '--num_of_disks', '99'), 'num_of_disks over disk count'),
    (('memstore', 'pool', 'create', '--name', 'p', '--capacity', '100',
      '--num_of_disks', '1'), 'storage_id required'),
]
neg_ok = True
for args, why in neg:
    rc, out, _ = run(*args)
    if rc != 0 or 'Execution failed' not in out or 'No data returned' in out:
        neg_ok = False
        record('negative %s' % why, False, out[:200])
record('negative cases rejected cleanly', neg_ok)
record('mock file intact after negatives', open(MOCK_FILE).read() == before)

# 删除链路：ns -> pool -> memstore（释放盘容量）
rc, out, _ = run('memstore', 'namespace', 'delete', '--id', ns['id'])
r = payload(out)
record('ns delete', rc == 0 and r['success'] is True
       and r['message'] == 'namespace deleted: ns02')
rc, out, _ = run('memstore', 'pool', 'delete', '--id', pool_id)
record('pool delete', rc == 0 and payload(out)['success'] is True)
rc, out, _ = run('memstore', 'disk', 'list', '--storage_id', ms['id'])
disks = payload(out)['disks']
record('disk capacity released', all(d['allocated_capacity'] == 0 for d in disks))
rc, out, _ = run('memstore', 'delete', '--id', ms['id'])
r = payload(out)
record('memstore delete', rc == 0 and r['success'] is True
       and r['message'] == 'memstore deleted: ms01')

# 文件始终是合法 JSON 数组
json.load(open(MOCK_FILE))
record('mock file valid JSON', True)
PYEOF
if [ $? -ne 0 ]; then
    fail=$((fail+1))
fi

# ---------- 3. 回归：其他 topic 行为不变 ----------
out=$(env -u DME_API_ENDPOINT -u DME_API_USERNAME -u DME_API_PASSWORD \
     python3 -m pydme.cli storage list 2>&1)
if printf '%s' "$out" | grep -q 'endpoint, user and password arguments are required'; then
    pass "[regression] storage list without DME params still rejected"
else
    bad "[regression] storage list without DME params: unexpected output"
fi
out=$(python3 -m pydme.cli hci list --help 2>&1)
if printf '%s' "$out" | grep -q 'Risk Level'; then
    pass "[regression] hci list --help renders"
else
    bad "[regression] hci list --help renders"
fi

rm -rf "$HOME"

echo ""
echo "==== 600-verify: $((total-fail))/$total PASS, $fail FAIL ===="
tail -3 "$OUT"
[ "$fail" -eq 0 ]
