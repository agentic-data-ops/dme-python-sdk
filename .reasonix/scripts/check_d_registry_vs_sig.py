"""
Check D: Compare actions registry 'params' lists against actual function signatures.
"""
import ast, glob, re, subprocess

def get_func_params(filepath, branch="HEAD"):
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
                result[node.name] = params
    except SyntaxError:
        pass
    return result


def parse_registry_params(filepath):
    """Extract registry entries and their params lists."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    entries = {}
    
    # Find the actions dict - look for top-level dict with string keys
    # Pattern: 'action_name': { 'func': ..., 'params': [...], ... }
    # Use regex to find func name and params list
    pattern = r"'(\w+)':\s*\{[^}]*?'func':\s*(\w+),[^}]*?'params':\s*\[([^\]]*)\][^}]*?\}"
    
    for m in re.finditer(pattern, content, re.DOTALL):
        entry_name = m.group(1)
        func_name = m.group(2)
        params_str = m.group(3)
        params = [p.strip().strip("'\"") for p in params_str.split(',') if p.strip()]
        entries[entry_name] = {'func': func_name, 'params': params}
    
    return entries


action_files = sorted(glob.glob("pydme/actions/*.py"))

print("=" * 120)
print("CHECK D: Registry params vs actual function signature")
print("=" * 120)

total_issues = 0

for f in action_files:
    sig_params = get_func_params(f, "HEAD")
    registry = parse_registry_params(f)
    
    for entry_name, entry in registry.items():
        func_name = entry['func']
        reg_params = entry['params']
        
        if func_name not in sig_params:
            print(f"{f}: {entry_name} -> func '{func_name}' not found in file!")
            total_issues += 1
            continue
        
        actual_params = sig_params[func_name]
        
        # Skip 'client' in comparison - it's in signature but usually not in registry
        actual_no_client = [p for p in actual_params if p != 'client']
        
        if set(reg_params) != set(actual_no_client):
            missing_in_reg = set(actual_no_client) - set(reg_params)
            extra_in_reg = set(reg_params) - set(actual_no_client)
            
            if missing_in_reg or extra_in_reg:
                print(f"\n{f}: {entry_name} ({func_name})")
                if missing_in_reg:
                    print(f"  [MISSING] Registry missing params: {sorted(missing_in_reg)}")
                if extra_in_reg:
                    print(f"  [EXTRA]   Registry has extra params: {sorted(extra_in_reg)}")
                total_issues += 1

print(f"\n{'=' * 120}")
print(f"Total registry/signature mismatches: {total_issues}")
