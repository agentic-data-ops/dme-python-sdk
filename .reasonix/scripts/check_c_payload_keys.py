"""
Check C: Payload dict key vs variable name consistency.
Find patterns like payload['xxx'] = yyy where xxx != yyy.
"""
import ast, glob, re

def check_payload_keys(filepath):
    """Find payload['key'] = variable patterns where key != variable name."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith('_'):
                    continue
                for child in ast.walk(node):
                    if isinstance(child, ast.Assign):
                        for target in child.targets:
                            if isinstance(target, ast.Subscript):
                                # payload['key'] = something
                                if (isinstance(target.value, ast.Name) and 
                                    isinstance(target.slice, ast.Constant) and
                                    isinstance(target.slice.value, str)):
                                    key_name = target.slice.value
                                    if isinstance(child.value, ast.Name):
                                        var_name = child.value.id
                                        if key_name != var_name:
                                            issues.append({
                                                'func': node.name,
                                                'line': child.lineno,
                                                'payload_key': key_name,
                                                'variable': var_name
                                            })
    except SyntaxError as e:
        pass
    
    return issues


action_files = sorted(glob.glob("pydme/actions/*.py"))

print("=" * 100)
print("CHECK C: Payload dict key vs variable name mismatch")
print("=" * 100)

total_issues = 0

for f in action_files:
    issues = check_payload_keys(f)
    for iss in issues:
        print(f"{f}:{iss['line']}: {iss['func']}()  payload['{iss['payload_key']}'] = {iss['variable']}")
        total_issues += 1

print(f"\n{'=' * 100}")
print(f"Total payload key/variable mismatches: {total_issues}")
