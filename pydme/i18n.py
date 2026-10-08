#!/usr/bin/env python
"""
pydme i18n: load action comment resources by language (pydme/config/i18n/<lang>.yaml).

v2 structured format (zero-dependency lightweight parser; only supports this
repo's self-produced format):

    topics:
      <topic>:
        description: |            # first line of the module docstring
        actions:
          <action-func>:
            description: |        # first paragraph of the function comments
            detail: |             # remaining paragraphs before Args ('' means none)
            parameters:
              <arg>: |            # parameter description (multi-line)
            outputs: |            # Returns section content ('' means none)

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
    """Parse v2 i18n YAML: {topics: {topic: {description, actions: {action: entry}}}}.

    Block content lines with indent >= block header indent + 2 belong to the
    current block; blank lines are kept inside the block. Empty values are
    inlined as `key: ''`.
    """
    topics = {}
    cur_topic = cur_action = None
    section = None          # 'topic_desc' | 'field' | 'param'
    field = None
    param_key = None
    block_indent = None
    block = []

    def save():
        nonlocal section, field, param_key, block_indent, block
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


def build_docstring(entry: dict) -> str:
    """Rebuild docstring text from structured fields (semantically identical to
    the pre-split text, for parse_docstring).

    Only detail (which contains the full description) is used for the rebuild;
    description is only consumed by --list-topics.
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
    """Structured fields of an action (None if missing)."""
    return load_i18n(lang)['topics'].get(topic, {}).get('actions', {}).get(action)


def get_action_description(topic: str, action: str, lang=None) -> str:
    """Action description (first paragraph of the function comments)."""
    entry = get_action_entry(topic, action, lang)
    return entry.get('description', '') if entry else ''


def get_action_doc(topic: str, action: str, lang=None):
    """Rebuild the docstring text for parse_docstring; returns None if the
    resource is missing."""
    entry = get_action_entry(topic, action, lang)
    return build_docstring(entry) if entry else None
