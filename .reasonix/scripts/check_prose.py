import os
for f in ["fcswitch.py", "ipswitch.py", "kube.py", "tenant.py", "workflow.py", "integrate.py", "backup.py"]:
    path = f"pydme/actions/{f}"
    if not os.path.exists(path):
        print(f"=== {f} (not found) ===")
        continue
    with open(path) as fh:
        lines = fh.readlines()
    print(f"=== {f} ===")
    func_name = ''
    c = 0
    for i, l in enumerate(lines):
        if l.startswith('def '):
            func_name = l.split('(')[0].replace('def ', '')
        if 'Returns:' in l:
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            if j < len(lines) and not lines[j].strip().startswith('{') and not lines[j].strip().startswith('任务ID'):
                c += 1
                print(f"  {func_name}: {lines[j].strip()[:60]}")
    if c == 0:
        print("  (all JSON)")
    print()
