# Plan: 300-add-action-risk-blacklist

## Objective

Add a risk confirmation mechanism to `pydme/cli.py` that detects destructive operations (delete, modify, remove, unmap, split, etc.) and either warns-and-executes or refuses based on user consent.

## Background

`pydme/config/blacklist.json` already exists with 122 risky action keys organized per topic. The CLI currently executes any valid action without risk awareness — a user could run `pydme storage vstore delete` or `pydme san lun delete` without any second warning.

## Design

### Risk check flow

```
User runs: pydme san lun delete --id xxx

                    ┌─────────────────────┐
                    │  Parse topic/subtopic │
                    │  / action from argv   │
                    └────────┬────────────┘
                             │
                             ▼
                    ┌──────────────────────┐
                    │ Reconstruct action_key│
                    │ (e.g. "lun_delete")   │
                    └────────┬─────────────┘
                             │
                             ▼
                    ┌──────────────────────────────┐
                    │ Load blacklist:               │
                    │ 1. ~/.config/pydme/blacklist  │
                    │    .json (user override)      │
                    │ 2. Fallback: copy from        │
                    │    pydme/config/blacklist.json │
                    └────────┬─────────────────────┘
                             │
                             ▼
                    ┌──────────────────────────────┐
                    │ Is action_key in blacklist?   │
                    └────────┬─────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              │ YES (risky)                 │ NO (safe)
              ▼                             ▼
    ┌──────────────────────┐      ┌──────────────────┐
    │ Check --accept-risk  │      │ Execute directly │
    │ or DME_ACCEPT_RISK   │      └──────────────────┘
    └────────┬─────────────┘
             │
    ┌────────┴────────────┐
    │ SET                 │ NOT SET
    ▼                     ▼
┌──────────────┐  ┌──────────────────────┐
│ Print warning│  │ Print warning +      │
│ + Execute    │  │ Refuse + show how to │
└──────────────┘  │ accept risk          │
                  └──────────────────────┘
```

### Implementation steps

#### Step 1: Add `--accept-risk` CLI argument

**File:** `pydme/cli.py`

Add a global flag `--accept-risk` to `create_parser()`. This is a `store_true` boolean flag.

Also read `DME_ACCEPT_RISK` environment variable — if set to `"true"` / `"1"` / `"yes"`, treat as accept-risk.

```python
# In create_parser()
parser.add_argument('--accept-risk', action='store_true',
                    help='Acknowledge and accept risk for destructive operations')
```

#### Step 2: Create `load_blacklist()` helper

**File:** `pydme/cli.py` (new method on `DMECLI` or module-level function)

Logic:
1. Determine user config dir: `Path.home() / ".config" / "pydme" / "blacklist.json"`
   - Cross-platform: `pathlib.Path.home()` works on Windows (`C:\Users\<user>\.config\pydme\blacklist.json`) and Linux (`/home/<user>/.config/pydme/blacklist.json`)
2. Check if user config file exists
   - If YES → load it
   - If NO → ensure parent dir exists, copy from `pydme/config/blacklist.json` (relative to the installed package), then load it
3. Return the parsed dict `{ topic: [action_key, ...] }`

```python
import json
from pathlib import Path
from importlib.resources import files  # Python 3.9+

def load_blacklist():
    user_path = Path.home() / ".config" / "pydme" / "blacklist.json"
    if not user_path.exists():
        user_path.parent.mkdir(parents=True, exist_ok=True)
        # Copy from package default
        src = files("pydme.config").joinpath("blacklist.json")
        user_path.write_text(src.read_text(), encoding="utf-8")
    return json.loads(user_path.read_text(encoding="utf-8"))
```

**Note:** For `importlib.resources.files`, need `python 3.9+`. For broader compatibility, use `pkgutil.get_data` or `__file__`-based path resolution as fallback.

#### Step 3: Resolve action_key from CLI arguments

**File:** `pydme/cli.py` in `main()`

After parsing args, determine the full action key:

```python
# After parse_known_args, before execution
topic = args.topic  # from positional args
subtopic = getattr(args, 'subtopic', None)
action = args.action  # from positional args

if subtopic:
    action_key = f"{subtopic}_{action}"
else:
    action_key = action
```

Check the actual CLI argument parsing to confirm how topic/subtopic/action are captured.

#### Step 4: Risk check & gate

**File:** `pydme/cli.py` in `main()`, before calling `cli.execute_action(...)`

```python
blacklist = load_blacklist()
accept_risk = args.accept_risk or os.environ.get("DME_ACCEPT_RISK", "").lower() in ("true", "1", "yes")

if topic in blacklist and action_key in blacklist[topic]:
    print(f"⚠️  WARNING: '{action_key}' is a destructive/risky operation.")
    if accept_risk:
        print(f"   Risk accepted (--accept-risk or DME_ACCEPT_RISK). Executing...")
        # proceed to execute
    else:
        print(f"   Execution refused. To proceed, add --accept-risk or set DME_ACCEPT_RISK=true")
        sys.exit(1)

# proceed to execute
```

#### Step 5: Update `--help` output

**File:** `pydme/cli.py`

Add a note in the help text about `--accept-risk` and the blacklist mechanism.

### Files touched

| File | Change |
|------|--------|
| `pydme/cli.py` | Add `--accept-risk` arg, `load_blacklist()`, risk check gate |
| `pydme/config/blacklist.json` | Already exists, no change needed |

### Risks & considerations

1. **Performance:** `load_blacklist()` is called once per CLI invocation. JSON load is negligible (~5KB file).
2. **First-run UX:** The first time a user runs any risky command, the blacklist is auto-copied to `~/.config/pydme/blacklist.json`. If the user's home directory is read-only (CI/CD), the copy step could fail — handle with `try/except` and fall back to reading directly from the package.
3. **Windows path:** `Path.home() / ".config" / "pydme"` works fine on Windows → `C:\Users\<user>\.config\pydme`. This is acceptable; Windows tools like `git` and `ssh` use similar `.config` conventions.
4. **Environment variable precedence:** `--accept-risk` CLI flag takes precedence over `DME_ACCEPT_RISK` env var. If both are set, CLI flag wins.
5. **Testing:** After implementation, test with:
   - `pydme san lun delete --id xxx` → should refuse
   - `pydme san lun delete --id xxx --accept-risk` → should warn + execute
   - `DME_ACCEPT_RISK=true pydme san lun delete --id xxx` → should warn + execute
   - `pydme san lun list` → should execute directly (safe action)

### Verification

```bash
# Safe action — no risk prompt
python pydme/cli.py san lun list

# Risky action — should refuse
python pydme/cli.py san lun delete --id test
# Expected: refuse with message about --accept-risk

# Risky action with flag — should warn + execute
python pydme/cli.py san lun delete --id test --accept-risk
# Expected: warning + execute

# Risky action with env var — should warn + execute
DME_ACCEPT_RISK=true python pydme/cli.py san lun delete --id test
# Expected: warning + execute
```

---

*Plan generated: 2026-06-15*
