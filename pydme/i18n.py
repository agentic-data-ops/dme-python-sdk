#!/usr/bin/env python3
"""
pydme i18n: load structured action/function resources by language.

Two resource files per language under pydme/config/i18n/:

  actions_<lang>.yaml -- topic tree: name/description/actions/subtopics with
                         per-action {name, description, func, params}
  funcs_<lang>.yaml   -- <topic>.<func>: |  full function docstring (verbatim)

Zero-dependency lightweight parser; only supports this repo's self-produced
formats (no PyYAML dependency).

Language selection: CLI argument --lang > environment variable DME_CLI_LANG >
default zh_CN.
"""
import importlib
import os
import sys
from pathlib import Path

SUPPORTED_LANGS = ('zh_CN', 'en_US')
DEFAULT_LANG = 'zh_CN'

_ACTIONS_CACHE = {}
_FUNCS_CACHE = {}
_REGISTRY_CACHE = {}


# ---------------------------------------------------------------------------
# parsing the repo's self-produced YAML formats
# ---------------------------------------------------------------------------

def _unquote(value):
    """Remove single-quote wrapping, undoing '' escaping."""
    if len(value) >= 2 and value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    return value


def parse_actions_yaml(text: str) -> dict:
    """Parse actions_<lang>.yaml -> {topics: {topic: {description, actions, subtopics}}}."""
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
    return {'topics': topics}


def _parse_action_entry(name_line, lines, idx, indent):
    """Parse one action list item {name, description, func, params}."""
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


def parse_funcs_yaml(text: str) -> dict:
    """Parse funcs_<lang>.yaml -> {<topic>.<func>: docstring}."""
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
# language resolution and loading
# ---------------------------------------------------------------------------

def resolve_lang(cli_lang=None) -> str:
    """CLI argument > DME_CLI_LANG env var > default zh_CN; an invalid value falls
    back to the default with a warning."""
    lang = cli_lang or os.environ.get('DME_CLI_LANG') or DEFAULT_LANG
    if lang not in SUPPORTED_LANGS:
        print(f"Warning: unknown language '{lang}', falling back to {DEFAULT_LANG}", file=sys.stderr)
        lang = DEFAULT_LANG
    return lang


def _resource_path(lang: str, prefix: str) -> Path:
    return Path(__file__).resolve().parent / 'config' / 'i18n' / f'{prefix}_{lang}.yaml'


def load_actions(lang=None) -> dict:
    """Load {topics: {...}} from actions_<lang>.yaml, cached per process."""
    lang = resolve_lang(lang)
    if lang in _ACTIONS_CACHE:
        return _ACTIONS_CACHE[lang]
    path = _resource_path(lang, 'actions')
    data = {'topics': {}}
    if path.exists():
        data = parse_actions_yaml(path.read_text(encoding='utf-8'))
    else:
        print(f"Warning: i18n resource {path} not found, please generate it "
              f"with .reasonix/scripts/gen_actions_i18n.py", file=sys.stderr)
    _ACTIONS_CACHE[lang] = data
    return data


def load_funcs(lang=None) -> dict:
    """Load {<topic>.<func>: docstring} from funcs_<lang>.yaml, cached per process."""
    lang = resolve_lang(lang)
    if lang in _FUNCS_CACHE:
        return _FUNCS_CACHE[lang]
    path = _resource_path(lang, 'funcs')
    data = {}
    if path.exists():
        data = parse_funcs_yaml(path.read_text(encoding='utf-8'))
    else:
        print(f"Warning: i18n resource {path} not found, comments will fall back "
              f"to the function docstring", file=sys.stderr)
    _FUNCS_CACHE[lang] = data
    return data


# ---------------------------------------------------------------------------
# lookup helpers
# ---------------------------------------------------------------------------

def _action_key_for(entry, subtopic):
    """Rebuild the full action key from a short name (mirror of the generator)."""
    return f"{subtopic}_{entry['name']}" if subtopic else entry['name']


def get_action_entry(topic: str, action: str, lang=None):
    """The action entry dict {name, description, func, params} by full action key
    (None if missing). `action` is the full key (e.g. 'cluster_list')."""
    data = load_actions(lang)['topics'].get(topic)
    if not data:
        return None
    for a in data['actions']:
        if a['name'] == action:
            return a
    for st, sd in data['subtopics'].items():
        for a in sd['actions']:
            if f"{st}_{a['name']}" == action:
                return a
    return None


def get_action_doc(topic: str, action_key: str, lang=None):
    """The full docstring text from funcs_<lang>.yaml, resolved via the action's
    func name; returns None if the resource is missing."""
    entry = get_action_entry(topic, action_key, lang)
    if not entry or not entry.get('func'):
        return None
    return load_funcs(lang).get(f"{topic}.{entry['func']}")


def get_action_description(topic: str, action_key: str, lang=None) -> str:
    """Action description (first line of the docstring, for list views)."""
    entry = get_action_entry(topic, action_key, lang)
    return entry.get('description', '') if entry else ''


def get_topic_description(topic: str, lang=None) -> str:
    """Topic description (module description in the current language)."""
    return load_actions(lang)['topics'].get(topic, {}).get('description', '')


def get_subtopic_description(topic: str, subtopic: str, lang=None) -> str:
    """Subtopic description (summarized from its actions, current language)."""
    return (load_actions(lang)['topics'].get(topic, {})
            .get('subtopics', {}).get(subtopic, {}).get('description', ''))


# ---------------------------------------------------------------------------
# action registry (language-independent structure with resolved function objects)
# ---------------------------------------------------------------------------

def _resolve_func(topic: str, func_name: str):
    """Resolve a func name to the callable in pydme.actions.<topic> (None on failure)."""
    try:
        module = importlib.import_module(f'pydme.actions.{topic}')
    except ImportError as e:
        print(f"Warning: unable to import pydme.actions.{topic}: {e}", file=sys.stderr)
        return None
    func = getattr(module, func_name, None)
    if not callable(func):
        print(f"Warning: func {topic}.{func_name} not callable in the actions module, "
              f"please update the corresponding YAML", file=sys.stderr)
        return None
    return func


def load_actions_registry(lang=None) -> dict:
    """Build {topic: {action_key: {func, params, subtopic}}} from actions_<lang>.yaml,
    with func resolved to the callable. Cached per process."""
    lang = resolve_lang(lang)
    if lang in _REGISTRY_CACHE:
        return _REGISTRY_CACHE[lang]
    data = load_actions(lang)['topics']
    registry = {}
    for topic, tdata in data.items():
        reg = {}
        for a in tdata['actions']:
            reg[a['name']] = {'func': _resolve_func(topic, a['func']),
                              'params': a['params'], 'subtopic': None}
        for st, sd in tdata['subtopics'].items():
            for a in sd['actions']:
                key = f"{st}_{a['name']}"
                reg[key] = {'func': _resolve_func(topic, a['func']),
                            'params': a['params'], 'subtopic': st}
        registry[topic] = reg
    _REGISTRY_CACHE[lang] = registry
    return registry


# keep the legacy name working for any external importer of load_i18n
load_i18n = load_actions
