#!/usr/bin/env python
"""
pydme i18n：按语言加载 action 注释资源（pydme/config/i18n/<lang>.yaml）。

零依赖轻量 YAML 子集解析，仅支持本仓库自产的固定格式：

    <topic>:
      <action-func>: |
        <func-comments>

语言选择：CLI 参数 --lang > 环境变量 DME_LANG > 默认 zh_CN。
"""
import os
import sys
from pathlib import Path

SUPPORTED_LANGS = ('zh_CN', 'en_US')
DEFAULT_LANG = 'zh_CN'

_CACHE = {}


def parse_yaml(text: str) -> dict:
    """解析自产 i18n YAML 文本：{topic: {action: text}}。

    block scalar 内容行以 4 空格缩进；空行属于 block 内容；遇到新的
    topic/action 行时结束当前 block 并去掉尾部空行（action 间分隔行）。
    """
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
    """按语言加载注释资源 {topic: {action: text}}，进程内缓存。

    资源文件缺失时返回空 dict 并打印警告（调用方回退 docstring）。
    """
    lang = resolve_lang(lang)
    if lang in _CACHE:
        return _CACHE[lang]
    path = _yaml_path(lang)
    data = {}
    if path.exists():
        data = parse_yaml(path.read_text(encoding='utf-8'))
    else:
        print(f"警告：未找到 i18n 资源 {path}，注释将回退函数 docstring", file=sys.stderr)
    _CACHE[lang] = data
    return data
