#!/usr/bin/env python3
"""Extract action function docstrings from pydme/actions/*.py into i18n YAML files.

Zero-dependency (stdlib only). Produces the strict format:

    <topic>:
      <action-func>: |
        <func-comments>

Only functions registered in each module's ACTIONS dict are extracted
(helper functions such as _build_* are excluded).

Usage:
    python3 extract_docstrings.py -o pydme/config/i18n/zh_CN.yaml
    python3 extract_docstrings.py --ref dev-en -o pydme/config/i18n/en_US.yaml
"""
import argparse
import ast
import glob
import os
import subprocess
import sys

ACTIONS_DIR = 'pydme/actions'
ACTIONS_DIR_ABS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', ACTIONS_DIR)


def read_source(path, ref=None):
    """Read module source from working tree (ref=None) or a git ref."""
    if ref:
        proc = subprocess.run(['git', 'show', f'{ref}:{path}'],
                              capture_output=True, text=True)
        if proc.returncode != 0:
            sys.exit(f"error: git show {ref}:{path} failed: {proc.stderr.strip()}")
        return proc.stdout
    with open(path, encoding='utf-8') as f:
        return f.read()


def get_action_funcs(src):
    """Return {action_name(key): FunctionDef node} for ACTIONS-registered functions.

    The ACTIONS dict maps action keys to entries; the docstring comes from the
    function referenced by the entry's 'func' field (may differ from the key,
    e.g. protect.create -> fs_hypermetro_pair_create). String func values
    (unimplemented actions) have no docstring and are skipped.
    """
    tree = ast.parse(src)
    funcs = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            funcs[node.name] = node

    actions = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (isinstance(target, ast.Name) and target.id == 'ACTIONS'
                        and isinstance(node.value, ast.Dict)):
                    for key, val in zip(node.value.keys, node.value.values):
                        if not (isinstance(key, ast.Constant) and isinstance(key.value, str)):
                            continue
                        if not isinstance(val, ast.Dict):
                            continue
                        func_name = None
                        for fk, fv in zip(val.keys, val.values):
                            if isinstance(fk, ast.Constant) and fk.value == 'func':
                                if isinstance(fv, ast.Name):
                                    func_name = fv.id
                                break
                        if func_name and func_name in funcs:
                            actions[key.value] = funcs[func_name]
    return actions


def serialize_yaml(entries):
    """Serialize [(topic, action, text), ...] to strict YAML block scalars."""
    out = []
    for topic, action, text in entries:
        out.append(f"{topic}:")
        out.append(f"  {action}: |")
        for line in text.split('\n'):
            if line:
                out.append(f"    {line}")
            else:
                out.append("")
        out.append("")
    # 去掉文件末尾多余空行
    while out and out[-1] == "":
        out.pop()
    return '\n'.join(out) + '\n'


def parse_yaml_back(text):
    """Round-trip parse of the YAML we generate: {topic: {action: text}}."""
    result = {}
    cur_topic = None
    cur_action = None
    block = []

    def flush():
        nonlocal cur_action, block
        if cur_action is not None:
            result.setdefault(cur_topic, {})[cur_action] = '\n'.join(block).rstrip('\n')
        cur_action = None
        block = []

    for line in text.split('\n'):
        if line.startswith('    '):
            block.append(line[4:])
        elif line == '':
            block.append('')
        elif line.startswith('  ') and line.rstrip().endswith(': |'):
            flush()
            cur_action = line.strip()[:-3].strip()
        elif line and not line.startswith(' ') and line.rstrip().endswith(':'):
            flush()
            cur_topic = line.strip()[:-1].strip()
        else:
            flush()
    flush()
    return result


def extract(ref=None):
    """Return entries=[(topic, action, text)] in module/definition order."""
    entries = []
    for path in sorted(glob.glob(os.path.join(ACTIONS_DIR_ABS, '*.py'))):
        if path.endswith('__init__.py'):
            continue
        topic = os.path.basename(path)[:-3]
        rel = os.path.join(ACTIONS_DIR, os.path.basename(path))
        src = read_source(rel if ref else path, ref=ref)
        action_funcs = get_action_funcs(src)
        for action, node in action_funcs.items():
            doc = ast.get_docstring(node, clean=True) or ""
            entries.append((topic, action, doc))
    return entries


def validate_entries(entries):
    """Assertions guarding YAML legality and round-trip fidelity."""
    for topic, action, text in entries:
        lines = text.split('\n')
        for ln in lines:
            if ln.startswith('---') or ln.startswith('...') or '"""' in ln:
                sys.exit(f"error: {topic}.{action} 含 YAML 非法内容行: {ln!r}")
        if text != text.strip('\n') or not text.strip():
            sys.exit(f"error: {topic}.{action} docstring 首尾空行或为空，与 clean 规范不符")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('-o', '--output', required=True, help='输出 YAML 文件路径')
    ap.add_argument('--ref', default=None, help='git ref（分支/commit），从该 ref 提取源码（如 dev-en）')
    args = ap.parse_args()

    entries = extract(ref=args.ref)
    validate_entries(entries)

    # round-trip 校验：解析回读逐字比对
    yaml_text = serialize_yaml(entries)
    parsed = parse_yaml_back(yaml_text)
    mismatches = []
    for topic, action, text in entries:
        if parsed.get(topic, {}).get(action) != text:
            mismatches.append(f"{topic}.{action}")
    if mismatches:
        sys.exit(f"error: round-trip 校验失败: {mismatches[:10]} ... (共 {len(mismatches)})")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(yaml_text)

    topics = len({t for t, _, _ in entries})
    print(f"OK: {len(entries)} actions / {topics} topics -> {args.output}"
          + (f" (ref={args.ref})" if args.ref else ""))


if __name__ == '__main__':
    main()
