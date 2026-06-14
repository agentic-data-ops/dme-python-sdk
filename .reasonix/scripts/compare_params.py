import ast, glob, subprocess, sys

def get_func_params(filepath, branch="HEAD"):
    """Extract function name -> [param names] from a file at a given branch."""
    content = None
    if branch == "HEAD":
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        result = subprocess.run(
            ["git", "show", f"{branch}:{filepath}"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            return {}
        content = result.stdout

    result = {}
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith('_'):
                    continue
                params = [arg.arg for arg in node.args.args if arg.arg != 'self']
                params += [arg.arg for arg in node.args.kwonlyargs]
                if params:
                    result[node.name] = params
    except SyntaxError as e:
        print(f"  [SYNTAX ERROR] {filepath}: {e}")
    return result

action_files = sorted(glob.glob("pydme/actions/*.py"))

print("=" * 120)
print(f"{'File':<30} {'Function':<30} {'main params':<40} {'current params':<40}")
print("=" * 120)

total_diffs = 0

for f in action_files:
    main_params = get_func_params(f, "main")
    cur_params = get_func_params(f, "HEAD")
    
    all_funcs = sorted(set(list(main_params.keys()) + list(cur_params.keys())))
    
    for func in all_funcs:
        mp = main_params.get(func, [])
        cp = cur_params.get(func, [])
        
        if mp != cp:
            max_len = max(len(mp), len(cp))
            diffs = []
            for i in range(max_len):
                pm = mp[i] if i < len(mp) else "(missing)"
                pc = cp[i] if i < len(cp) else "(missing)"
                if pm != pc:
                    diffs.append(f"  >>> Arg {i}: main='{pm}'  cur='{pc}'")
            
            print(f"{f:<30} {func:<30} {str(mp):<40} {str(cp):<40}")
            for d in diffs:
                print(d)
            total_diffs += 1

print("=" * 120)
print(f"差异函数总数: {total_diffs}")
