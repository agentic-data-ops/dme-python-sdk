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
    """模块 docstring 首行（与 cli --list-topics 逻辑一致）。"""
    tree = ast.parse(src)
    doc = ast.get_docstring(tree, clean=True) or ""
    for line in doc.split('\n'):
        s = line.strip()
        if s and not s.startswith('"""'):
            return s
    return ''


def _dedent4(line):
    """去 Args/Returns 段内容的公共 4 空格基准缩进（保留相对缩进）。"""
    return line[4:] if line.startswith('    ') else line.strip()


def split_docstring(doc):
    """将 clean docstring 无损拆分为结构化字段。

    Returns:
        {'description', 'detail', 'parameters', 'outputs'}；
        拆分可经 build_docstring() 逐字重组还原。
    """
    lines = doc.split('\n')
    args_idx = ret_idx = None
    for i, line in enumerate(lines):
        s = line.strip()
        if args_idx is None and s.startswith('Args:'):
            args_idx = i
        elif ret_idx is None and s.startswith('Returns:'):
            ret_idx = i

    # 前段（Args/Returns 之前）：首段=description，其余段=detail
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

    # parameters：Args 段。参数定义行缩进 <= 4 且匹配 `name: desc`；
    # 其余行（含空行/注释/格式块续行）归入当前参数描述，保留相对缩进。
    # 空行先入 pending：遇到下一参数/续行时并入前一参数描述；
    # 段尾（Args 与 Returns 之间）的空行属于段间分隔，不并入任何参数。
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
                # 值取自原始行（保留行尾空格），去掉名字前缀与左侧空白
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
        # 段尾 pending 丢弃（段间分隔空行）
        if cur_name is not None:
            parameters[cur_name] = '\n'.join(cur_desc)

    # outputs：Returns 段之后全部内容（含 Raises/Note 等后续段与空行），去公共 4 空格基准
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

    return {'description': description, 'detail': detail,
            'parameters': parameters, 'outputs': outputs}


def build_docstring(entry):
    """将结构化字段无损重组为原 docstring 文本。

    重组后与原始 docstring 仅可能在「非标准 0 缩进行」上相差 4 空格
    （parse_docstring 输出不受影响）；round-trip 校验使用缩进归一化比较。
    """
    parts = []
    if entry.get('description'):
        parts.append(entry['description'])
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


def normalize(text):
    """round-trip 校验用的归一化：去行尾空白、连续空行压缩为单个空行、
    段头（Args/Returns/Raises/Note/Example）与参数行行首缩进统一 4 空格。
    parse_docstring 对空行数量与行首缩进不敏感，故这些差异视为等价。"""
    out = []
    prev_blank = False
    for line in text.split('\n'):
        s = line.rstrip()
        if not s.strip():
            if not prev_blank:
                out.append('')
            prev_blank = True
            continue
        prev_blank = False
        stripped = s.lstrip()
        if re.match(r'^(Args|Returns|Raises|Note|Example):', stripped):
            out.append('    ' + stripped)
        elif re.match(r'^(\w+): ', stripped) and len(s) - len(s.lstrip()) <= 4:
            out.append('    ' + stripped)
        else:
            out.append(s)
    return '\n'.join(out).rstrip('\n')


def serialize_yaml(entries, topics_desc):
    """Serialize [(topic, action, doc), ...] to v2 structured YAML text."""
    out = ['topics:']
    prev_topic = None
    for topic, action, doc in entries:
        if topic != prev_topic:
            if prev_topic is not None:
                out.append('')
            out.append(f'  {topic}:')
            out.append('    description: |')
            for line in topics_desc[topic].split('\n'):
                out.append(f'      {line}')
            out.append('    actions:')
            prev_topic = topic
        entry = split_docstring(doc)
        out.append(f'      {action}:')
        out.append('        description: |')
        for line in entry['description'].split('\n'):
            out.append(f'          {line}')
        if entry['detail']:
            out.append('        detail: |')
            for line in entry['detail'].split('\n'):
                out.append(f'          {line}')
        else:
            out.append("        detail: ''")
        if entry['parameters']:
            out.append('        parameters:')
            for name, desc in entry['parameters'].items():
                out.append(f'          {name}: |')
                for line in desc.split('\n'):
                    out.append(f'            {line}')
        if entry['outputs']:
            out.append('        outputs: |')
            for line in entry['outputs'].split('\n'):
                out.append(f'          {line}')
        else:
            out.append("        outputs: ''")
    # 去掉文件末尾多余空行
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
        # 保留块内容尾部空行（参数间分隔是真实内容）；整体尾部空行由
        # normalize() 忽略，且不影响 parse_docstring 输出。
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
        elif indent == 10 and stripped.endswith(': |'):
            begin('param', key_=stripped[:-3].strip(), indent_=indent)
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
    ap.add_argument('-o', '--output', required=True, help='输出 YAML 文件路径')
    ap.add_argument('--ref', default=None, help='git ref（分支/commit），从该 ref 提取源码（如 dev-en）')
    args = ap.parse_args()

    entries, topics_desc = extract(ref=args.ref)
    if not entries:
        sys.exit("error: 未提取到任何 action")

    # 校验：拆分→序列化→解析→重组（缩进归一化后逐字还原）
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
        sys.exit(f"error: round-trip 校验失败: {problems[:10]} ... (共 {len(problems)})")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(yaml_text)

    topics = len(topics_desc)
    print(f"OK: {len(entries)} actions / {topics} topics -> {args.output}"
          + (f" (ref={args.ref})" if args.ref else ""))


if __name__ == '__main__':
    main()
