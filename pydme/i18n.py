#!/usr/bin/env python
"""
pydme i18n: load action comment resources by language (pydme/config/i18n/<lang>.yaml).

Simplified format (zero-dependency lightweight parser; only supports this
repo's self-produced format):

    topics:
      <topic>:
        description: '<module docstring first line>'
        actions:
          <action-func>:
            docstring: |    # the full function docstring, verbatim

Language selection: CLI argument --lang > environment variable DME_LANG >
default zh_CN.
"""
import os
import sys
from pathlib import Path

SUPPORTED_LANGS = ('zh_CN', 'en_US')
DEFAULT_LANG = 'zh_CN'

_CACHE = {}


def _unquote(value):
    """Remove single-quote wrapping (single-line values are serialized with single quotes)."""
    if value.startswith("'") and value.endswith("'") and len(value) >= 2:
        return value[1:-1]
    return value


def parse_yaml(text: str) -> dict:
    """Parse the simplified i18n YAML: {topics: {topic: {description, actions}}}.

    Block content lines with indent >= the docstring header indent + 2 belong
    to the docstring block; blank lines are kept inside the block.
    """
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


def resolve_lang(cli_lang=None) -> str:
    """CLI argument > DME_LANG env var > default zh_CN; an invalid value falls
    back to the default with a warning."""
    lang = cli_lang or os.environ.get('DME_LANG') or DEFAULT_LANG
    if lang not in SUPPORTED_LANGS:
        print(f"Warning: unknown language '{lang}', falling back to {DEFAULT_LANG}", file=sys.stderr)
        lang = DEFAULT_LANG
    return lang


def _yaml_path(lang: str) -> Path:
    return Path(__file__).resolve().parent / 'config' / 'i18n' / f'{lang}.yaml'


def load_i18n(lang=None) -> dict:
    """Load {topics: {...}} by language, cached per process; a missing file
    returns an empty structure with a warning."""
    lang = resolve_lang(lang)
    if lang in _CACHE:
        return _CACHE[lang]
    path = _yaml_path(lang)
    data = {'topics': {}}
    if path.exists():
        data = parse_yaml(path.read_text(encoding='utf-8'))
    else:
        print(f"Warning: i18n resource {path} not found, comments will fall back to the function docstring",
              file=sys.stderr)
    _CACHE[lang] = data
    return data


def get_topic_description(topic: str, lang=None) -> str:
    """Topic description (first line of the module docstring)."""
    return load_i18n(lang)['topics'].get(topic, {}).get('description', '')


def get_action_entry(topic: str, action: str, lang=None):
    """The action entry (None if missing)."""
    return load_i18n(lang)['topics'].get(topic, {}).get('actions', {}).get(action)


def get_action_doc(topic: str, action: str, lang=None):
    """The full docstring text for parse_docstring; returns None if the
    resource is missing."""
    entry = get_action_entry(topic, action, lang)
    return entry.get('docstring') if entry else None


def get_action_description(topic: str, action: str, lang=None) -> str:
    """Action description (first line of the docstring, for list views)."""
    doc = get_action_doc(topic, action, lang) or ""
    return doc.split('\n')[0] if doc else ''
