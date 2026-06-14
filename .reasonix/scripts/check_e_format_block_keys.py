"""
Check E: Compare nested parameter format block keys between main and current branch.
Line-by-line parser to avoid regex timeout on large files.
"""
import glob, re, subprocess

def extract_format_block_keys(content):
    """State-machine parser for parameter format blocks."""
    results = {}
    in_format = False
    brace_depth = 0
    current_parent = None
    current_keys = set()
    
    for line in content.split('\n'):
        stripped = line.strip()
        
        # Detect format block entry
        if not in_format:
            m = re.match(r'^(\w+)\s*:\s*(.+)', stripped)
            if m:
                desc = m.group(2)
                if 'parameter format:' in desc or 'attribute format:' in desc:
                    current_parent = m.group(1)
                    current_keys = set()
                    in_format = True
                    brace_depth = stripped.count('{') - stripped.count('}')
                    if brace_depth < 0:
                        brace_depth = 0
                    # Extract keys from the description itself (before the brace)
                    continue
        
        if in_format:
            # Track brace depth
            brace_depth += stripped.count('{') - stripped.count('}')
            
            # Check if this line defines a key (not entering another format block)
            if brace_depth == 1 and not stripped.startswith('}'):
                km = re.match(r'^(\w+)\s*:', stripped)
                if km and 'parameter format:' not in stripped and 'attribute format:' not in stripped:
                    current_keys.add(km.group(1))
            
            # Check if we've exited the format block
            if brace_depth <= 0:
                if current_parent and current_keys:
                    results[current_parent] = current_keys
                in_format = False
                current_parent = None
                current_keys = set()
    
    return results


def get_content(branch, filepath):
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


action_files = sorted(glob.glob("pydme/actions/*.py"))

print("=" * 100)
print("CHECK E: Format block inner keys: main vs current branch")
print("=" * 100)

total_diffs = 0

for f in action_files:
    main_content = get_content("main", f)
    cur_content = get_content("HEAD", f)
    
    if not main_content or not cur_content:
        continue
    
    main_keys = extract_format_block_keys(main_content)
    cur_keys = extract_format_block_keys(cur_content)
    
    all_parents = sorted(set(list(main_keys.keys()) + list(cur_keys.keys())))
    
    for parent in all_parents:
        mk = main_keys.get(parent, set())
        ck = cur_keys.get(parent, set())
        
        if mk != ck:
            only_main = mk - ck
            only_cur = ck - mk
            
            print(f"\n{f}")
            print(f"  Parent param: '{parent}'")
            if only_main:
                print(f"  [main only]  keys: {sorted(only_main)}")
            if only_cur:
                print(f"  [current only] keys: {sorted(only_cur)}")
            
            total_diffs += 1

print(f"\n{'=' * 100}")
print(f"Total parent params with different format block keys: {total_diffs}")
