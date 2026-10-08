#!/usr/bin/env python3
"""Extract action docstrings into the simplified i18n YAML format.

Zero-dependency (stdlib only). Produces the strict format:

    topics:
      <topic>:
        description: '<module docstring first line>'
        actions:
          <action-func>:
            docstring: |      # the full function docstring (clean), verbatim

Only functions registered in each module's ACTIONS dict are extracted
(helper functions such as _build_* are excluded).

Usage:
    python3 extract_docstrings.py -o pydme/config/i18n/zh_CN.yaml
    python3 extract_docstrings.py --ref main-en -o pydme/config/i18n/en_US.yaml
"""
import argparse
import ast
import glob
import os
import subprocess
import sys

ACTIONS_DIR = 'pydme/actions'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ACTIONS_DIR_ABS = os.path.join(BASE_DIR, ACTIONS_DIR)


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


def module_description(src):
    """First line of the module docstring (same logic as cli --list-topics)."""
    tree = ast.parse(src)
    doc = ast.get_docstring(tree, clean=True) or ""
    for line in doc.split('\n'):
        s = line.strip()
        if s and not s.startswith('"""'):
            return s
    return ''


def _quote(value):
    """Wrap a single-line value in single quotes; inner ' is replaced with "."""
    return "'" + value.replace(chr(39), chr(34)) + "'"


def _unquote(value):
    """Remove single-quote wrapping."""
    if value.startswith("'") and value.endswith("'") and len(value) >= 2:
        return value[1:-1]
    return value


def serialize_yaml(entries, topics_desc):
    """Serialize [(topic, action, docstring), ...] to the simplified YAML text."""
    out = ['topics:']
    prev_topic = None
    for topic, action, doc in entries:
        if topic != prev_topic:
            if prev_topic is not None:
                out.append('')
            out.append(f'  {topic}:')
            out.append(f"    description: {_quote(topics_desc[topic])}")
            out.append('    actions:')
            prev_topic = topic
        out.append(f'      {action}:')
        out.append('        docstring: |')
        for line in doc.split('\n'):
            out.append(f'          {line}')
    # Strip trailing blank lines at the end of the file
    while out and out[-1] == '':
        out.pop()
    return '\n'.join(out) + '\n'


def parse_yaml(text):
    """Round-trip parse of the YAML we generate: {topics: {topic: {description, actions}}}."""
    topics = {}
    cur_topic = cur_action = None
    section = None          # 'docstring'
    block_indent = None
    block = []

    def save():
        nonlocal section, block_indent, block
        if section == 'docstring' and cur_topic is not None and cur_action is not None:
            topics[cur_topic]['actions'][cur_action]['docstring'] = '\n'.join(block).rstrip('\n')
        section = None
        block_indent = None
        block = []

    for line in text.split('\n'):
        stripped = line.strip()
        if not stripped:
            if section is not None:
                block.append('')
            continue
        indent = len(line) - len(line.lstrip())
        if section is not None and indent >= block_indent:
            block.append(line[block_indent:])
            continue
        save()
        if indent == 0:
            pass  # topics:
        elif indent == 2 and stripped.endswith(':'):
            cur_topic = stripped[:-1]
            cur_action = None
            topics.setdefault(cur_topic, {'description': '', 'actions': {}})
        elif indent == 4 and stripped == 'actions:':
            pass
        elif indent == 4 and stripped.startswith('description:'):
            # single-line topic description: description: 'xxx'
            topics[cur_topic]['description'] = _unquote(stripped.partition(':')[2].strip())
        elif indent == 6 and stripped.endswith(':'):
            cur_action = stripped[:-1]
            topics[cur_topic]['actions'].setdefault(cur_action, {'docstring': ''})
        elif indent == 8 and stripped == 'docstring: |':
            section = 'docstring'
            block_indent = indent + 2
            block = []
    save()
    return {'topics': topics}


def extract(ref=None):
    """Return (entries=[(topic, action, docstring)], topics_desc={topic: desc})."""
    entries = []
    topics_desc = {}
    for path in sorted(glob.glob(os.path.join(ACTIONS_DIR_ABS, '*.py'))):
        if path.endswith('__init__.py'):
            continue
        topic = os.path.basename(path)[:-3]
        rel = os.path.join(ACTIONS_DIR, os.path.basename(path))
        src = read_source(rel if ref else path, ref=ref)
        topics_desc[topic] = module_description(src)
        action_funcs = get_action_funcs(src)
        for action, node in action_funcs.items():
            doc = ast.get_docstring(node, clean=True) or ""
            entries.append((topic, action, doc))
    return entries, topics_desc


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('-o', '--output', required=True, help='output YAML file path')
    ap.add_argument('--ref', default=None, help='git ref (branch/commit); extract sources from this ref (e.g. main-en)')
    args = ap.parse_args()

    entries, topics_desc = extract(ref=args.ref)
    if not entries:
        sys.exit("error: no actions extracted")

    # Validation: parse back and compare verbatim
    yaml_text = serialize_yaml(entries, topics_desc)
    parsed = parse_yaml(yaml_text)
    problems = []
    for topic, action, doc in entries:
        if parsed['topics'][topic]['actions'][action]['docstring'] != doc:
            problems.append(f"{topic}.{action}")
        if parsed['topics'][topic]['description'] != topics_desc[topic]:
            problems.append(f"{topic}.description")
    if problems:
        sys.exit(f"error: round-trip validation failed: {problems[:10]} ... ({len(problems)} total)")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(yaml_text)

    topics = len(topics_desc)
    print(f"OK: {len(entries)} actions / {topics} topics -> {args.output}"
          + (f" (ref={args.ref})" if args.ref else ""))


if __name__ == '__main__':
    main()
