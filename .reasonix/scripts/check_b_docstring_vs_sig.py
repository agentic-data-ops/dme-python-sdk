"""
Check B: Docstring Args: keys vs actual function signature params.
For each function, extract param names from Args: section and
compare against the function's actual parameter list.
"""
import ast, glob, subprocess, re, sys

def get_func_params_from_sig(filepath, branch="HEAD"):
    """Extract function name -> set of param names from AST."""
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
                params = set()
                for arg in node.args.args:
                    if arg.arg != 'self':
                        params.add(arg.arg)
                for arg in node.args.kwonlyargs:
                    params.add(arg.arg)
                if params:
                    result[node.name] = params
    except SyntaxError:
        pass
    return result


def get_func_params_from_docstring(filepath, branch="HEAD"):
    """Extract function name -> set of param keys mentioned in Args: section."""
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
                if node.name.startswith('_') or not node.body:
                    continue
                # Get docstring
                docstring = ast.get_docstring(node)
                if not docstring:
                    continue
                
                # Parse Args: section
                lines = docstring.split('\n')
                in_args = False
                args_keys = set()
                
                for line in lines:
                    stripped = line.strip()
                    if stripped.startswith('Args:'):
                        in_args = True
                        continue
                    if stripped.startswith(('Returns:', 'Raises:', 'Note:', 'Example:')):
                        in_args = False
                        continue
                    
                    if in_args:
                        # Match "param_name: description"
                        m = re.match(r'^(\w+)\s*:', stripped)
                        if m:
                            args_keys.add(m.group(1))
                
                if args_keys:
                    result[node.name] = args_keys
    except SyntaxError:
        pass
    return result


action_files = sorted(glob.glob("pydme/actions/*.py"))

print("=" * 100)
print("CHECK B: Docstring Args: keys vs function signature params")
print("=" * 100)

total_issues = 0

for f in action_files:
    sig_params = get_func_params_from_sig(f, "HEAD")
    doc_params = get_func_params_from_docstring(f, "HEAD")
    
    all_funcs = sorted(set(list(sig_params.keys()) + list(doc_params.keys())))
    
    for func in all_funcs:
        sp = sig_params.get(func, set())
        dp = doc_params.get(func, set())
        
        if not dp:
            continue
        
        # Keys in docstring but not in signature
        extra_in_doc = dp - sp
        # Keys in signature but not in docstring
        missing_in_doc = sp - dp
        
        if extra_in_doc or missing_in_doc:
            print(f"\n{f}:{func}")
            if extra_in_doc:
                print(f"  [WARN] Docstring has extra keys not in signature: {sorted(extra_in_doc)}")
            if missing_in_doc:
                # Skip 'client' as it's often in signature but not always documented
                real_missing = missing_in_doc - {'client'}
                if real_missing:
                    print(f"  [WARN] Signature has keys missing from docstring: {sorted(real_missing)}")
            total_issues += 1

print(f"\n{'=' * 100}")
print(f"Total functions with docstring/signature mismatch: {total_issues}")
