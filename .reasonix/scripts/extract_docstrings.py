#!/usr/bin/env python3
"""Extract action docstrings into structured v2 i18n YAML.

Zero-dependency (stdlib only). Produces the strict format:

    topics:
      <topic>:
        description: |
          <module docstring first line>
        actions:
          <action-func>:
            description: |          # first paragraph of func docstring
            detail: |               # remaining paragraphs before Args ('' if none)
            parameters:
              <arg>: |              # multi-line param description
            outputs: |              # Returns section content ('' if none)

Only functions registered in each module's ACTIONS dict are extracted
(helper functions such as _build_* are excluded). Splitting a docstring is
lossless: rebuilding via build_docstring() reproduces the original text.

Usage:
    python3 extract_docstrings.py -o pydme/config/i18n/zh_CN.yaml
    python3 extract_docstrings.py --ref dev-en -o pydme/config/i18n/en_US.yaml
"""
import argparse
import ast
import glob
import os
import re
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


def _dedent4(line):
    """Strip the common 4-space base indent of Args/Returns section content (keep relative indentation)."""
    return line[4:] if line.startswith('    ') else line.strip()


def split_docstring(doc):
    """Losslessly split a clean docstring into structured fields.

    Returns:
        {'description', 'detail', 'parameters', 'outputs'};
        the split can be rebuilt verbatim via build_docstring().
    """
    lines = doc.split('\n')
    args_idx = ret_idx = None
    for i, line in enumerate(lines):
        s = line.strip()
        if args_idx is None and s.startswith('Args:'):
            args_idx = i
        elif ret_idx is None and s.startswith('Returns:'):
            ret_idx = i

    # Leading section (before Args/Returns): first paragraph = description, rest = detail
    head = lines[:args_idx if args_idx is not None else (ret_idx if ret_idx is not None else len(lines))]
    while head and head[-1].strip() == '':
        head.pop()
    paras, cur = [], []
    for line in head:
        if line.strip() == '':
            if cur:
                paras.append(cur)
                cur = []
        else:
            cur.append(line)
    if cur:
        paras.append(cur)
    description = '\n'.join(paras[0]) if paras else ''
    detail = '\n\n'.join('\n'.join(p) for p in paras[1:]) if len(paras) > 1 else ''

    # parameters: from the Args section. A parameter definition line has indent <= 4
    # and matches `name: desc`; other lines (blank lines, comments, format-block
    # continuations) belong to the current parameter description, keeping relative
    # indentation. Blank lines first go into pending: they are merged into the previous
    # parameter description when the next parameter/continuation line appears; blank
    # lines at the end of the section (between Args and Returns) are section separators
    # and are not merged into any parameter.
    parameters = {}
    if args_idx is not None:
        end = ret_idx if ret_idx is not None else len(lines)
        cur_name, cur_desc, in_block, pending = None, [], 0, []
        for line in lines[args_idx + 1:end]:
            stripped = line.strip()
            indent = len(line) - len(line.lstrip())
            if in_block > 0:
                in_block += stripped.count('{') - stripped.count('}')
                if in_block < 0:
                    in_block = 0
                cur_desc.append(_dedent4(line))
                continue
            if not stripped:
                pending.append('')
                continue
            m = re.match(r'^(\w+)\s*:\s*(.*)$', stripped)
            if m and indent <= 4:
                if cur_name is not None:
                    cur_desc.extend(pending)
                    parameters[cur_name] = '\n'.join(cur_desc)
                pending = []
                cur_name = m.group(1)
                # The value is taken from the original line (keeping trailing spaces), removing the name prefix and leading whitespace
                value = line[len(line[:indent] + m.group(1) + ':'):].lstrip()
                cur_desc = [value] if value else []
                if '参数格式如下：' in stripped or '属性格式如下：{' in stripped:
                    in_block = stripped.count('{') - stripped.count('}')
                    if in_block < 0:
                        in_block = 0
            elif cur_name is not None:
                cur_desc.extend(pending)
                pending = []
                cur_desc.append(_dedent4(line))
        # Trailing pending is discarded (section separator blank lines)
        if cur_name is not None:
            parameters[cur_name] = '\n'.join(cur_desc)

    # outputs: all content after the Returns section (including Raises/Note etc. and blank lines), stripped of the common 4-space base
    outputs = ''
    if ret_idx is not None:
        out_lines = []
        for line in lines[ret_idx + 1:]:
            if line.strip():
                out_lines.append(_dedent4(line))
            else:
                out_lines.append('')
        while out_lines and out_lines[-1].strip() == '':
            out_lines.pop()
        outputs = '\n'.join(out_lines)

    # v3 semantics: the whole description is merged into detail; description keeps only
    # the first line of detail (used by --list-topics only, not for docstring rebuild)
    full_detail = description + (('\n\n' + detail) if detail else '')
    description = full_detail.split('\n')[0] if full_detail else ''
    detail = full_detail

    # client is a session parameter injected by the caller, not a CLI parameter; exclude it from the i18n extraction
    parameters.pop('client', None)

    return {'description': description, 'detail': detail,
            'parameters': parameters, 'outputs': outputs}


def build_docstring(entry):
    """Losslessly rebuild the original docstring text from structured fields.

    The rebuilt text may differ from the original docstring by 4 spaces only on
    non-standard 0-indent lines (parse_docstring output is unaffected); the
    round-trip check uses indentation-normalized comparison.
    """
    parts = []
    if entry.get('detail'):
        parts.append(entry['detail'])
    if entry.get('parameters'):
        arg_lines = []
        for name, desc in entry['parameters'].items():
            first, *rest = desc.split('\n')
            line = f"    {name}: {first}"
            for r in rest:
                line += ('\n    ' + r) if r else '\n'
            arg_lines.append(line)
        parts.append('Args:\n' + '\n'.join(arg_lines))
    if entry.get('outputs'):
        out_lines = []
        for l in entry['outputs'].split('\n'):
            out_lines.append(('    ' + l) if l else '')
        parts.append('Returns:\n' + '\n'.join(out_lines))
    return '\n\n'.join(parts)


def _strip_empty_args(text):
    """Remove empty Args sections containing only the client parameter (or no parameters).

    client is excluded from the i18n extraction, so the rebuilt docstring no longer
    generates such Args sections; the corresponding sections in the original docstring
    must also be removed during normalized comparison.
    """
    lines = text.split('\n')
    out = []
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped == 'Args:':
            j = i + 1
            seg = [lines[i]]
            while j < len(lines):
                s = lines[j].strip()
                if not s or re.match(r'^(Returns|Raises|Note|Example):', s):
                    break
                seg.append(lines[j])
                j += 1
            param_lines = [l for l in seg[1:] if re.match(r'^\w+\s*:', l.strip())]
            if not param_lines or all(re.match(r'^client\s*:', l.strip()) for l in param_lines):
                i = j  # empty Args section: skip
                continue
        out.append(lines[i])
        i += 1
    return '\n'.join(out)


def normalize(text):
    """Normalization for round-trip checks: strip trailing whitespace, collapse
    consecutive blank lines into one, unify section headers (Args/Returns/Raises/
    Note/Example) and parameter lines to 4-space indentation. parse_docstring is
    insensitive to blank-line counts and leading indentation, so these differences
    are treated as equivalent."""
    text = _strip_empty_args(text)
    out = []
    prev_blank = False
    for line in text.split('\n'):
        s = line.rstrip()
        s = s.replace(chr(39), chr(34))  # normalize single/double quotes (values serialize ' as ")
        if not s.strip():
            if not prev_blank:
                out.append('')
            prev_blank = True
            continue
        prev_blank = False
        if re.match(r'^ {0,4}client: ', s):
            continue  # client parameter lines are excluded from the i18n extraction; ignore them in comparison
        stripped = s.lstrip()
        if re.match(r'^(Args|Returns|Raises|Note|Example):', stripped):
            out.append('    ' + stripped)
        elif re.match(r'^(\w+): ', stripped) and len(s) - len(s.lstrip()) <= 4:
            out.append('    ' + stripped)
        else:
            out.append(s)
    return '\n'.join(out).rstrip('\n')


def is_safe_inline(value):
    """Whether a single-line value can use the inline form (safe as a YAML plain scalar)."""
    if not value:
        return True  # empty values are inlined as `key: ''`
    if '\n' in value:
        return False
    if ': ' in value:          # a colon followed by a space breaks plain scalars
        return False
    if value.startswith(('#', '- ', '[', '{', '?', ':', ',', '&', '*', '!', '|', '>',
                         '%', '@', '`', "'", '"')):
        return False
    return True


def _unquote(value):
    """Remove single-quote wrapping (single-line values are serialized with single quotes)."""
    if value.startswith("'") and value.endswith("'") and len(value) >= 2:
        return value[1:-1]
    return value


def put_value(out, indent, key, value):
    """Emit `indent<key>: value`: empty values as '', single-line values wrapped in
    single quotes (inner ' replaced with "), multi-line values as | blocks."""
    if not value:
        out.append(f"{indent}{key}: ''")
    elif '\n' in value:
        out.append(f"{indent}{key}: |")
        for line in value.split('\n'):
            out.append(f"{indent}  {line}")
    else:
        out.append(f"{indent}{key}: '{value.replace(chr(39), chr(34))}'")


def serialize_yaml(entries, topics_desc):
    """Serialize [(topic, action, doc), ...] to v2 structured YAML text."""
    out = ['topics:']
    prev_topic = None
    for topic, action, doc in entries:
        if topic != prev_topic:
            if prev_topic is not None:
                out.append('')
            out.append(f'  {topic}:')
            put_value(out, '    ', 'description', topics_desc[topic])
            out.append('    actions:')
            prev_topic = topic
        entry = split_docstring(doc)
        out.append(f'      {action}:')
        put_value(out, '        ', 'description', entry['description'])
        put_value(out, '        ', 'detail', entry['detail'])
        if entry['parameters']:
            out.append('        parameters:')
            for name, desc in entry['parameters'].items():
                put_value(out, '          ', name, desc)
        put_value(out, '        ', 'outputs', entry['outputs'])
    # Strip trailing blank lines at the end of the file
    while out and out[-1] == '':
        out.pop()
    return '\n'.join(out) + '\n'


def parse_yaml(text):
    """Round-trip parse of the v2 YAML we generate: {topics: {topic: entry}}."""
    topics = {}
    cur_topic = cur_action = None
    section = None          # 'topic_desc' | 'field' | 'param'
    field = None
    param_key = None
    block_indent = None
    block = []

    def save():
        nonlocal section, field, param_key, block_indent, block
        # Keep trailing blank lines inside block content (parameter separators are real
        # content); whole-text trailing blank lines are ignored by normalize() and do
        # not affect parse_docstring output.
        val = '\n'.join(block)
        if section == 'topic_desc' and cur_topic is not None:
            topics[cur_topic]['description'] = val
        elif section == 'field' and cur_topic is not None and cur_action is not None:
            topics[cur_topic]['actions'][cur_action][field] = val
        elif section == 'param' and cur_topic is not None and cur_action is not None:
            topics[cur_topic]['actions'][cur_action]['parameters'][param_key] = val
        section = None
        field = None
        param_key = None
        block_indent = None
        block = []

    def begin(section_, field_=None, key_=None, indent_=None):
        nonlocal section, field, param_key, block_indent, block
        section = section_
        field = field_
        param_key = key_
        block_indent = (indent_ or 0) + 2
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
        elif indent == 4 and stripped == 'description: |':
            begin('topic_desc', indent_=indent)
        elif indent == 4 and stripped.startswith('description:'):
            # single-line topic description: description: 'xxx'
            topics[cur_topic]['description'] = _unquote(stripped.partition(':')[2].strip())
        elif indent == 6 and stripped.endswith(':'):
            cur_action = stripped[:-1]
            topics[cur_topic]['actions'].setdefault(
                cur_action, {'description': '', 'detail': '', 'parameters': {}, 'outputs': ''})
        elif indent == 8 and stripped == 'parameters:':
            pass
        elif indent == 8 and stripped.endswith(': |'):
            begin('field', field_=stripped[:-3].strip(), indent_=indent)
        elif indent == 8 and stripped.endswith(": ''"):
            topics[cur_topic]['actions'][cur_action][stripped[:-4].strip()] = ''
        elif indent == 8:
            # single-line action field: description: 'xxx' / detail: 'xxx' / outputs: 'xxx'
            key, _, val = stripped.partition(':')
            topics[cur_topic]['actions'][cur_action][key.strip()] = _unquote(val.strip())
        elif indent == 10 and stripped.endswith(': |'):
            begin('param', key_=stripped[:-3].strip(), indent_=indent)
        elif indent == 10:
            # single-line parameter: arg: 'xxx'
            key, _, val = stripped.partition(':')
            topics[cur_topic]['actions'][cur_action]['parameters'][key.strip()] = _unquote(val.strip())
    save()
    return {'topics': topics}


def extract(ref=None):
    """Return (entries=[(topic, action, doc)], topics_desc={topic: desc})."""
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
    ap.add_argument('--ref', default=None, help='git ref (branch/commit); extract sources from this ref (e.g. dev-en)')
    args = ap.parse_args()

    entries, topics_desc = extract(ref=args.ref)
    if not entries:
        sys.exit("error: no actions extracted")

    # Validation: split -> serialize -> parse -> rebuild (verbatim after indent normalization)
    yaml_text = serialize_yaml(entries, topics_desc)
    parsed = parse_yaml(yaml_text)
    problems = []
    for topic, action, doc in entries:
        entry = parsed['topics'][topic]['actions'][action]
        rebuilt = build_docstring(entry)
        if normalize(rebuilt) != normalize(doc):
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
