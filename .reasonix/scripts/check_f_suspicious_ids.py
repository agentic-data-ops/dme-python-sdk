"""
Check F: Scan for suspicious identifier patterns that suggest
translation corruption:
- Duplicated substrings (maintenance + tenance = maintenanceetenance)
- Truncated endings (info -> infor)
- Fused words (disk_domain + maintenance = disk_domaintenancee)
- CamelCase vs snake_case inconsistencies in same file
- Unusual identifier length anomalies
"""
import ast, glob, re, subprocess

def get_func_bodies(filepath, branch="HEAD"):
    """Get all function bodies as text."""
    if branch == "HEAD":
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        result = subprocess.run(
            ["git", "show", f"{branch}:{filepath}"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return result.stdout
        return ""

def extract_identifiers(content):
    """Extract all Python identifiers from code (not docstrings)."""
    identifiers = set()
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                identifiers.add(node.id)
            elif isinstance(node, ast.FunctionDef):
                identifiers.add(node.name)
                for arg in node.args.args:
                    if arg.arg != 'self':
                        identifiers.add(arg.arg)
                for arg in node.args.kwonlyargs:
                    identifiers.add(arg.arg)
            elif isinstance(node, ast.arg):
                identifiers.add(node.arg)
    except SyntaxError:
        pass
    return identifiers

# Suspicious patterns
# 1. Duplicated substrings: e.g., "maintenance" appearing twice in fused form
def has_duplicate_substring(s):
    """Check if identifier has duplicated substrings like 'maintenanceetenance'."""
    s_lower = s.lower()
    # Look for repeated substrings of length 3+
    for i in range(len(s_lower)):
        for j in range(i+3, len(s_lower)):
            substr = s_lower[i:j]
            remaining = s_lower[j:]
            if substr and remaining.startswith(substr):
                return True, substr
    return False, ""

# 2. Truncation patterns: "info" -> "infor", "list" -> "lis" etc.
TRUNCATION_PATTERNS = [
    (r'infor$', 'info'),
    (r'liss$', 'list'),
    (r'creat$', 'create'),
    (r'del$', 'delete'),
    (r'modi$', 'modify'),
]

def has_truncation(s):
    for pattern, expected in TRUNCATION_PATTERNS:
        if re.search(pattern, s):
            return True, expected
    return False, ""

# 3. Fused words: check if identifier contains recognizable components
# that don't make sense together
COMMON_WORDS = ['maintenance', 'domain', 'storage', 'service', 'volume', 
                'snapshot', 'tenant', 'filesystem', 'namespace', 'partition']

def has_fused_words(s):
    s_lower = s.lower()
    found_words = [w for w in COMMON_WORDS if w in s_lower]
    if len(found_words) >= 2:
        # Check if they're truly fused (no separator)
        for w1 in found_words:
            for w2 in found_words:
                if w1 != w2 and w1 + w2 in s_lower:
                    return True, f"{w1}+{w2}"
    return False, ""


action_files = sorted(glob.glob("pydme/actions/*.py"))

print("=" * 100)
print("CHECK F: Suspicious identifier scan")
print("=" * 100)

all_issues = []

for f in action_files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    identifiers = extract_identifiers(content)
    
    for ident in sorted(identifiers):
        dup, dup_str = has_duplicate_substring(ident)
        if dup:
            all_issues.append((f, ident, f"Duplicated substring: '{dup_str}'"))
            continue
        
        trunc, expected = has_truncation(ident)
        if trunc:
            all_issues.append((f, ident, f"Possible truncation: expected '{expected}'"))
            continue
        
        fused, fused_str = has_fused_words(ident)
        if fused:
            all_issues.append((f, ident, f"Fused words: '{fused_str}'"))

# Also scan identifier references in string literals (payload keys, registry entries)
# for the same patterns
for f in action_files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # Find all string literals that look like identifiers
    string_idents = set(re.findall(r"'(\w+)'", content))
    
    for ident in sorted(string_idents):
        if len(ident) < 3:
            continue
        dup, dup_str = has_duplicate_substring(ident)
        if dup:
            all_issues.append((f, f"'{ident}' (string)", f"Duplicated substring: '{dup_str}'"))
            continue
        
        trunc, expected = has_truncation(ident)
        if trunc:
            all_issues.append((f, f"'{ident}' (string)", f"Possible truncation: expected '{expected}'"))
            continue

# Print results
for f, ident, reason in sorted(all_issues):
    print(f"{f}: {ident}  [{reason}]")

if not all_issues:
    print("No suspicious identifiers found!")
else:
    print(f"\n{'=' * 100}")
    print(f"Total suspicious identifiers: {len(all_issues)}")
