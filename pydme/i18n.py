#!/usr/bin/env python
"""
pydme i18n：按语言加载 action 注释资源（pydme/config/i18n/<lang>.yaml）。

v2 结构化格式（零依赖轻量解析，仅支持本仓库自产格式）：

    topics:
      <topic>:
        description: |            # 模块 docstring 首行
        actions:
          <action-func>:
            description: |        # 函数注释第一段
            detail: |             # Args 之前其余段落（'' 表示无）
            parameters:
              <arg>: |            # 参数描述（多行）
            outputs: |            # Returns 段内容（'' 表示无）

语言选择：CLI 参数 --lang > 环境变量 DME_LANG > 默认 zh_CN。
"""
import os
import sys
from pathlib import Path

SUPPORTED_LANGS = ('zh_CN', 'en_US')
DEFAULT_LANG = 'zh_CN'

_CACHE = {}


def parse_yaml(text: str) -> dict:
    """解析 v2 i18n YAML：{topics: {topic: {description, actions: {action: entry}}}}。

    block 内容行缩进 >= 块头缩进 + 2 即归入当前块；空行保留在块内。
    空值字段以 `key: ''` 内联表示。
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
            # 单行 topic 描述：description: xxx
            topics[cur_topic]['description'] = stripped.partition(':')[2].strip()
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
            # 单行 action 字段：description: xxx / detail: xxx / outputs: xxx
            key, _, val = stripped.partition(':')
            topics[cur_topic]['actions'][cur_action][key.strip()] = val.strip()
        elif indent == 10 and stripped.endswith(': |'):
            begin('param', key_=stripped[:-3].strip(), indent_=indent)
        elif indent == 10:
            # 单行参数：arg: xxx
            key, _, val = stripped.partition(':')
            topics[cur_topic]['actions'][cur_action]['parameters'][key.strip()] = val.strip()
    save()
    return {'topics': topics}


def build_docstring(entry: dict) -> str:
    """结构化字段重组为 docstring 文本（与拆分前语义一致，供 parse_docstring 使用）。

    仅用 detail（已含完整说明）重组，description 只供 --list-topics 使用。
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
    """CLI 参数 > DME_LANG 环境变量 > 默认 zh_CN；非法值回退默认并警告。"""
    lang = cli_lang or os.environ.get('DME_LANG') or DEFAULT_LANG
    if lang not in SUPPORTED_LANGS:
        print(f"警告：未知语言 '{lang}'，回退为 {DEFAULT_LANG}", file=sys.stderr)
        lang = DEFAULT_LANG
    return lang


def _yaml_path(lang: str) -> Path:
    return Path(__file__).resolve().parent / 'config' / 'i18n' / f'{lang}.yaml'


def load_i18n(lang=None) -> dict:
    """按语言加载 {topics: {...}}，进程内缓存；文件缺失返回空结构并警告。"""
    lang = resolve_lang(lang)
    if lang in _CACHE:
        return _CACHE[lang]
    path = _yaml_path(lang)
    data = {'topics': {}}
    if path.exists():
        data = parse_yaml(path.read_text(encoding='utf-8'))
    else:
        print(f"警告：未找到 i18n 资源 {path}，注释将回退函数 docstring", file=sys.stderr)
    _CACHE[lang] = data
    return data


def get_topic_description(topic: str, lang=None) -> str:
    """topic 描述（模块 docstring 首行）。"""
    return load_i18n(lang)['topics'].get(topic, {}).get('description', '')


def get_action_entry(topic: str, action: str, lang=None):
    """action 结构化字段（无则 None）。"""
    return load_i18n(lang)['topics'].get(topic, {}).get('actions', {}).get(action)


def get_action_description(topic: str, action: str, lang=None) -> str:
    """action 描述（函数注释第一段）。"""
    entry = get_action_entry(topic, action, lang)
    return entry.get('description', '') if entry else ''


def get_action_doc(topic: str, action: str, lang=None):
    """重组 docstring 文本供 parse_docstring 解析；资源缺失返回 None。"""
    entry = get_action_entry(topic, action, lang)
    return build_docstring(entry) if entry else None
