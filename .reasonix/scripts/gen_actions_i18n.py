#!/usr/bin/env python3
"""Generate structured i18n resources from ACTIONS dicts and the existing i18n YAML.

Produces (per language lang in {zh_CN, en_US}):
  pydme/config/i18n/actions_<lang>.yaml  -- topic tree: name/description/actions/subtopics
  pydme/config/i18n/funcs_<lang>.yaml    -- <topic>.<func>: |  full function docstring

Zero-dependency (stdlib only). Self-checks round-trip consistency against the
code-side ACTIONS dicts before writing anything:

  * rebuilt action_key set == ACTIONS key set (427, incl. nas dataturbo/dpc nesting)
  * every action func resolvable in its module; funcs key set == func set
  * every action description == first line of its funcs docstring
  * zh_CN / en_US structural fields (name/func/params/subtopic) identical

Usage:
  python3 .reasonix/scripts/gen_actions_i18n.py
"""
import argparse
import ast
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)  # allow `import pydme.actions.<topic>` in checks
ACTIONS_DIR = os.path.join(BASE_DIR, 'pydme', 'actions')
I18N_DIR = os.path.join(BASE_DIR, 'pydme', 'config', 'i18n')
LANGS = ('zh_CN', 'en_US')


# ---------------------------------------------------------------------------
# code side: parse ACTIONS dicts via ast
# ---------------------------------------------------------------------------

def _assign_named(node, name):
    return isinstance(node, ast.Assign) and any(
        isinstance(t, ast.Name) and t.id == name for t in node.targets)


def extract_actions():
    """{topic: [ {key, func, params, subtopic}, ... ]} in ACTIONS definition order."""
    topics = {}
    for fn in sorted(os.listdir(ACTIONS_DIR)):
        if not fn.endswith('.py') or fn == '__init__.py':
            continue
        topic = fn[:-3]
        tree = ast.parse(open(os.path.join(ACTIONS_DIR, fn), encoding='utf-8').read())
        actions = []
        for node in ast.walk(tree):
            if _assign_named(node, 'ACTIONS') and isinstance(node.value, ast.Dict):
                for k, v in zip(node.value.keys, node.value.values):
                    if not isinstance(k, ast.Constant) or not isinstance(v, ast.Dict):
                        continue
                    entry = {'key': k.value, 'func': None, 'params': [], 'subtopic': None}
                    for fk, fv in zip(v.keys, v.values):
                        if not isinstance(fk, ast.Constant):
                            continue
                        if fk.value == 'func' and isinstance(fv, ast.Name):
                            entry['func'] = fv.id
                        elif fk.value == 'params' and isinstance(fv, ast.List):
                            entry['params'] = [e.value for e in fv.elts
                                               if isinstance(e, ast.Constant)]
                        elif fk.value == 'subtopic':
                            if isinstance(fv, ast.Constant):
                                entry['subtopic'] = fv.value
                            elif isinstance(fv, ast.Name) and fv.id == 'None':
                                entry['subtopic'] = None
                    actions.append(entry)
        topics[topic] = actions
    return topics


def short_name(entry):
    """Short action name, mirroring cli.py get_available_topics: direct actions
    keep the key; subtopic actions strip the '<subtopic>_' prefix."""
    st = entry['subtopic']
    if not st:
        return entry['key']
    prefix = st + '_'
    return entry['key'][len(prefix):] if entry['key'].startswith(prefix) else entry['key']


# ---------------------------------------------------------------------------
# old i18n side: parse the legacy topics.<topic>.actions.<action>.docstring YAML
# ---------------------------------------------------------------------------

def _unquote(value):
    if len(value) >= 2 and value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    return value


def parse_legacy_yaml(text):
    """{topic: {description, actions: {key: docstring}}} for the legacy format."""
    topics = {}
    cur_topic = cur_action = None
    section = None
    block_indent = None
    block = []

    def save():
        nonlocal section, block_indent, block
        if section == 'docstring' and cur_topic is not None and cur_action is not None:
            topics[cur_topic]['actions'][cur_action] = '\n'.join(block).rstrip('\n')
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
        if indent == 2 and stripped.endswith(':'):
            cur_topic = stripped[:-1]
            cur_action = None
            topics.setdefault(cur_topic, {'description': '', 'actions': {}})
        elif indent == 4 and stripped.startswith('description:'):
            topics[cur_topic]['description'] = _unquote(stripped.partition(':')[2].strip())
        elif indent == 6 and stripped.endswith(':'):
            cur_action = stripped[:-1]
            topics[cur_topic]['actions'].setdefault(cur_action, '')
        elif indent == 8 and stripped == 'docstring: |':
            section = 'docstring'
            block_indent = indent + 2
            block = []
    save()
    return topics


def load_legacy(lang):
    path = os.path.join(I18N_DIR, f'{lang}.yaml')
    if not os.path.exists(path):
        sys.exit(f"error: legacy i18n file not found: {path}")
    return parse_legacy_yaml(open(path, encoding='utf-8').read())


# ---------------------------------------------------------------------------
# serialization (strict, self-produced formats)
# ---------------------------------------------------------------------------

def quote(v):
    """Single-line scalar, single-quoted with '' escaping (round-trippable)."""
    return "'" + str(v).replace("'", "''") + "'"


def params_flow(params):
    return '[' + ', '.join(params) + ']'


def _action_block(entries, base_indent):
    """Serialize action list items under 'actions:' with the given base indent."""
    lines = []
    for e in entries:
        ind = ' ' * base_indent
        lines.append(f"{ind}- name: {e['name']}")
        lines.append(f"{ind}  description: {quote(e['description'])}")
        lines.append(f"{ind}  func: {e['func']}")
        lines.append(f"{ind}  params: {params_flow(e['params'])}")
    return lines


def build_actions_yaml(topic_tree):
    """Serialize {topic: {description, actions, subtopics}} to the list format."""
    lines = ['topics:']
    for t, data in topic_tree.items():
        lines.append(f"    - name: {t}")
        lines.append(f"      description: {quote(data['description'])}")
        lines.append('      actions:')
        lines += _action_block(data['actions'], 10)
        lines.append('      subtopics:')
        for st, stdata in data['subtopics'].items():
            lines.append(f"        - name: {st}")
            lines.append(f"          description: {quote(stdata['description'])}")
            lines.append('          actions:')
            lines += _action_block(stdata['actions'], 12)
    return '\n'.join(lines) + '\n'


def build_funcs_yaml(docs):
    """Serialize {key(topic.func): docstring} as block scalars (blank lines kept empty)."""
    lines = []
    for key, doc in docs.items():
        lines.append(f"{key}: |")
        for ln in doc.split('\n'):
            lines.append(('    ' + ln) if ln.strip() else '')
    return '\n'.join(lines) + '\n'


# ---------------------------------------------------------------------------
# parsing back the produced files (round-trip)
# ---------------------------------------------------------------------------

def parse_actions_yaml(text):
    """Parse the produced actions_<lang>.yaml back into topic_tree structure."""
    topics = {}
    cur_topic = None
    cur_sub = None
    lines = text.split('\n')
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        indent = len(line) - len(line.lstrip())
        if indent == 4 and stripped.startswith('- name:'):
            cur_topic = stripped.partition(':')[2].strip()
            cur_sub = None
            topics[cur_topic] = {'description': '', 'actions': [], 'subtopics': {}}
        elif indent == 6 and stripped.startswith('description:'):
            topics[cur_topic]['description'] = _unquote(stripped.partition(':')[2].strip())
        elif indent == 6 and stripped == 'subtopics:':
            cur_sub = None
        elif indent == 8 and stripped.startswith('- name:'):
            cur_sub = stripped.partition(':')[2].strip()
            topics[cur_topic]['subtopics'][cur_sub] = {'description': '', 'actions': []}
        elif indent == 10 and stripped.startswith('description:') and cur_sub:
            topics[cur_topic]['subtopics'][cur_sub]['description'] = \
                _unquote(stripped.partition(':')[2].strip())
        elif indent == 10 and stripped.startswith('- name:'):
            topics[cur_topic]['actions'].append(_parse_action_entry(line, lines, idx, indent))
        elif indent == 12 and stripped.startswith('- name:'):
            topics[cur_topic]['subtopics'][cur_sub]['actions'].append(
                _parse_action_entry(line, lines, idx, indent))
    return topics


def _parse_action_entry(name_line, lines, idx, indent):
    """Parse one action list item (name/description/func/params) at a given indent."""
    entry = {'name': name_line.strip().partition(':')[2].strip(),
             'description': '', 'func': '', 'params': []}
    for i in range(idx + 1, len(lines)):
        ln = lines[i]
        if not ln.strip() or len(ln) - len(ln.lstrip()) <= indent:
            break
        stripped = ln.strip()
        if stripped.startswith('description:'):
            entry['description'] = _unquote(stripped.partition(':')[2].strip())
        elif stripped.startswith('func:'):
            entry['func'] = stripped.partition(':')[2].strip()
        elif stripped.startswith('params:'):
            raw = stripped.partition(':')[2].strip()
            entry['params'] = [p.strip() for p in raw.strip('[]').split(',') if p.strip()]
    return entry


def parse_funcs_yaml(text):
    """Parse funcs_<lang>.yaml into {key: docstring}."""
    docs = {}
    cur_key = None
    block = []
    block_indent = None
    for line in text.split('\n'):
        stripped = line.strip()
        if not stripped:
            if cur_key is not None:
                block.append('')
            continue
        indent = len(line) - len(line.lstrip())
        if cur_key is not None and indent >= block_indent:
            block.append(line[block_indent:])
            continue
        if cur_key is not None:
            docs[cur_key] = '\n'.join(block).rstrip('\n')
        if stripped.endswith(': |'):
            cur_key = stripped[:-3].strip()
            block_indent = indent + 4
            block = []
        else:
            cur_key = None
    if cur_key is not None:
        docs[cur_key] = '\n'.join(block).rstrip('\n')
    return docs


# ---------------------------------------------------------------------------
# orchestration + round-trip checks
# ---------------------------------------------------------------------------

def build_trees(actions, legacy):
    """Build per-lang topic_tree and funcs dict from code ACTIONS + legacy i18n."""
    trees, funcs = {}, {}
    for lang in LANGS:
        tree, fd = {}, {}
        for topic, entries in actions.items():
            desc = legacy[lang].get(topic, {}).get('description', '')
            actions_list, subtopics = [], {}
            for e in entries:
                doc = legacy[lang].get(topic, {}).get('actions', {}).get(e['key'], '')
                entry = {'name': short_name(e), 'func': e['func'],
                         'params': list(e['params']),
                         'description': (doc.split('\n')[0].strip() if doc else '')}
                if e['subtopic']:
                    subtopics.setdefault(e['subtopic'], []).append(entry)
                else:
                    actions_list.append(entry)
            tree[topic] = {'description': desc, 'actions': actions_list,
                           'subtopics': {k: {'description': '', 'actions': v}
                                         for k, v in subtopics.items()}}
            for e in entries:
                doc = legacy[lang].get(topic, {}).get('actions', {}).get(e['key'], '')
                fd[f'{topic}.{e["func"]}'] = doc
        trees[lang], funcs[lang] = tree, fd
    return trees, funcs


def check(actions, trees, funcs):
    errs = []
    mods = {t: __import__(f'pydme.actions.{t}', fromlist=['*']) for t in actions}
    for lang in LANGS:
        tree, fd = trees[lang], funcs[lang]
        # 1) rebuilt action_key set == ACTIONS key set
        rebuilt = set()
        for t, data in tree.items():
            for a in data['actions']:
                rebuilt.add(a['name'])
            for st, sd in data['subtopics'].items():
                for a in sd['actions']:
                    rebuilt.add(f'{st}_{a["name"]}')
        code_keys = {e['key'] for e in sum(actions.values(), [])}
        if rebuilt != code_keys:
            errs.append(f'[{lang}] rebuilt action keys mismatch: '
                        f'extra={sorted(rebuilt - code_keys)[:5]} missing={sorted(code_keys - rebuilt)[:5]}')
        # 2) func resolvable; funcs key set == func set
        func_set = set()
        for t, entries in actions.items():
            for e in entries:
                if e['func'] is None or not callable(getattr(mods[t], e['func'], None)):
                    errs.append(f'[{lang}] func not resolvable: {t}.{e["func"]}')
                func_set.add(f'{t}.{e["func"]}')
        if set(fd) != func_set:
            errs.append(f'[{lang}] funcs key set mismatch')
        # 3) action description == first line of funcs docstring
        for t, data in tree.items():
            for a in data['actions']:
                first = fd[f'{t}.{a["func"]}'].split('\n')[0].strip()
                if a['description'] != first:
                    errs.append(f'[{lang}] {t}.{a["name"]} description != docstring first line')
            for st, sd in data['subtopics'].items():
                for a in sd['actions']:
                    first = fd[f'{t}.{a["func"]}'].split('\n')[0].strip()
                    if a['description'] != first:
                        errs.append(f'[{lang}] {t}.{st}.{a["name"]} description != docstring first line')
    # 4) zh/en structural fields identical
    z, e = trees['zh_CN'], trees['en_US']
    for t in z:
        zs = [(a['name'], a['func'], tuple(a['params']))
              for a in z[t]['actions']] + [
            (f'{st}_{a["name"]}', a['func'], tuple(a['params']))
            for st, sd in z[t]['subtopics'].items() for a in sd['actions']]
        es = [(a['name'], a['func'], tuple(a['params']))
              for a in e[t]['actions']] + [
            (f'{st}_{a["name"]}', a['func'], tuple(a['params']))
            for st, sd in e[t]['subtopics'].items() for a in sd['actions']]
        if zs != es:
            errs.append(f'[{t}] zh/en structural mismatch')
    if set(trees['zh_CN']) != set(actions):
        errs.append('topic set mismatch vs modules')
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=I18N_DIR, help='output directory')
    args = ap.parse_args()

    actions = extract_actions()
    legacy = {lang: load_legacy(lang) for lang in LANGS}
    trees, funcs = build_trees(actions, legacy)

    errs = check(actions, trees, funcs)
    if errs:
        print('\n'.join(f'CHECK FAILED: {e}' for e in errs), file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.out, exist_ok=True)
    for lang in LANGS:
        apath = os.path.join(args.out, f'actions_{lang}.yaml')
        fpath = os.path.join(args.out, f'funcs_{lang}.yaml')
        with open(apath, 'w', encoding='utf-8') as f:
            f.write(build_actions_yaml(trees[lang]))
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(build_funcs_yaml(funcs[lang]))
        # parse-back round trip
        rt = parse_actions_yaml(open(apath, encoding='utf-8').read())
        if rt != trees[lang]:
            sys.exit(f'error: actions_{lang}.yaml parse-back mismatch')
        rtf = parse_funcs_yaml(open(fpath, encoding='utf-8').read())
        if rtf != funcs[lang]:
            sys.exit(f'error: funcs_{lang}.yaml parse-back mismatch')
        print(f'wrote {apath} ({sum(len(v["actions"]) + sum(len(sd["actions"]) for sd in v["subtopics"].values()) for v in trees[lang].values())} actions)')
        print(f'wrote {fpath} ({len(funcs[lang])} docstrings)')


if __name__ == '__main__':
    main()
