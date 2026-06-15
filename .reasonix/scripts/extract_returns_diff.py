"""Extract old and new Returns sections from the commit diff, per file."""
import sys

diff = open('.reasonix/main-commit-diff.txt').read()
lines = diff.split('\n')

target_file = sys.argv[1] if len(sys.argv) > 1 else None

in_target = False
old_returns = []
current_old = None
new_returns = []
current_new = None

for line in lines:
    # Detect file boundaries
    if line.startswith('diff --git a/'):
        fname = line.split(' ')[2][2:]  # "a/pydme/actions/foo.py" → "pydme/actions/foo.py"
        if in_target:
            if current_old:
                old_returns.append('\n'.join(current_old))
            if current_new:
                new_returns.append('\n'.join(current_new))
            break
        if target_file and target_file in fname:
            in_target = True
            old_returns = []
            new_returns = []
            current_old = None
            current_new = None
        continue

    if not in_target:
        continue

    # Track Returns: sections
    stripped = line.lstrip()
    is_old = line.startswith('-') and not line.startswith('---')
    is_new = line.startswith('+') and not line.startswith('+++')

    if '-    Returns:' in line:
        if current_old:
            old_returns.append('\n'.join(current_old))
        current_old = [line[1:]]  # strip the '-' prefix
    elif current_old is not None:
        if is_old:
            current_old.append(line[1:])
        elif is_new or line.startswith('@@') or (not line.startswith('-') and not line.startswith('+')):
            old_returns.append('\n'.join(current_old))
            current_old = None

    if '+    Returns:' in line:
        if current_new:
            new_returns.append('\n'.join(current_new))
        current_new = [line[1:]]
    elif current_new is not None:
        if is_new:
            current_new.append(line[1:])
        elif is_old or line.startswith('@@') or (not line.startswith('-') and not line.startswith('+')):
            new_returns.append('\n'.join(current_new))
            current_new = None

print(f"=== {target_file} ===")
print(f"\n--- OLD Returns sections ({len(old_returns)} found) ---")
for i, r in enumerate(old_returns):
    print(f"\n--- Old #{i+1} ---")
    print(r)

print(f"\n--- NEW Returns sections ({len(new_returns)} found) ---")
for i, r in enumerate(new_returns):
    print(f"\n--- New #{i+1} ---")
    print(r)
