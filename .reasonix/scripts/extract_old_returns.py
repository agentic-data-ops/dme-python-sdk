"""Extract old Returns text from diff for a specific file, without complex parsing."""
import sys

target = sys.argv[1]  # e.g., "nas"
diff = open('.reasonix/main-commit-diff.txt').read()
lines = diff.split('\n')

# Find the file section in the diff
start = -1
end = -1
for i, l in enumerate(lines):
    if l.startswith('diff --git a/pydme/actions/') and target in l:
        start = i
    elif start >= 0 and l.startswith('diff --git a/') and i > start:
        end = i
        break
if end == -1:
    end = len(lines)

section = lines[start:end]

# Find old Returns: lines
print(f"=== OLD Returns sections in {target} ===")
for i, l in enumerate(section):
    if '-    Returns:' in l and not l.startswith('++'):
        # Print context: the Returns line and subsequent old lines
        print(f"\n--- Returns at relative line {i} ---")
        j = i
        while j < len(section):
            sl = section[j]
            if sl.startswith('-') and not sl.startswith('--- '):
                print(sl[1:])  # strip leading '-'
            elif sl.startswith('+') and not sl.startswith('+++'):
                break
            elif not sl.startswith('--') and not sl.startswith('@@'):
                # reached context line that's neither old nor new - stop
                if not sl.startswith('+') and not sl.startswith('-'):
                    break
            j += 1
