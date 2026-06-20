#!/usr/bin/env python
"""
DME 运维命令行工具
提供存储运维操作的命令行入口，支持参数解析和帮助
"""

import argparse
import json
import os
import sys
import importlib
import pkgutil
import re
import inspect
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydme.client import DMEAPIClient


CACHE_DIR = os.path.expanduser("~/.config/pydme")
CACHE_FILE = os.path.join(CACHE_DIR, "cache.json")


def _load_cache() -> list:
    """Load cached auth tokens from cache.json."""
    if not os.path.isfile(CACHE_FILE):
        return []
    try:
        with open(CACHE_FILE) as f:
            data = json.load(f)
        return data.get("dme", [])
    except (json.JSONDecodeError, OSError):
        return []


def _save_cache(entries: list):
    """Save auth tokens to cache.json, creating directories if needed."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump({"dme": entries}, f, indent=2)


def _update_cache(endpoint: str, username: str, auth_token: str):
    """Add or update a cached token entry for (endpoint, username)."""
    entries = _load_cache()
    entries = [
        e for e in entries
        if not (e.get("endpoint") == endpoint and e.get("username") == username)
    ]
    entries.append({
        "endpoint": endpoint,
        "username": username,
        "auth_token": auth_token,
    })
    _save_cache(entries)


def _find_cached_token(endpoint: str, username: str) -> str:
    """Look up a cached token for (endpoint, username). Returns empty string if not found."""
    for entry in _load_cache():
        if entry.get("endpoint") == endpoint and entry.get("username") == username:
            return entry.get("auth_token", "")
    return ""


def load_blacklist() -> Dict[str, list]:
    """
    加载风险操作黑名单。

    优先级：
    1. 用户自定义 ~/.config/pydme/blacklist.json
    2. 如果不存在，从包内 pydme/config/blacklist.json 复制生成

    Returns:
        { topic: [action_key, ...] }
    """
    user_path = Path.home() / '.config' / 'pydme' / 'blacklist.json'

    if not user_path.exists():
        # 尝试从包内复制默认黑名单
        try:
            # Python 3.9+: importlib.resources.files
            from importlib.resources import files as res_files
            src = res_files('pydme.config').joinpath('blacklist.json')
            default_data = src.read_text(encoding='utf-8')
        except (ImportError, TypeError, FileNotFoundError, ModuleNotFoundError):
            # 回退：基于 __file__ 路径（兼容 Python 3.8 / 开发模式）
            try:
                pkg_dir = Path(__file__).resolve().parent / 'config'
                default_data = (pkg_dir / 'blacklist.json').read_text(encoding='utf-8')
            except FileNotFoundError:
                print('警告：未找到 blacklist.json，跳过风险检查', file=sys.stderr)
                return {}

        # 写入用户目录
        try:
            user_path.parent.mkdir(parents=True, exist_ok=True)
            user_path.write_text(default_data, encoding='utf-8')
        except (OSError, PermissionError):
            # 用户目录不可写（如 CI 环境），直接用包内数据
            return json.loads(default_data)

    try:
        return json.loads(user_path.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, OSError) as e:
        print(f'警告：读取 blacklist.json 失败 ({e})，跳过风险检查', file=sys.stderr)
        return {}


def _accepts_risk(args) -> bool:
    """检查用户是否确认接受风险（通过 CLI 参数或环境变量）。"""
    return args.accept_risk or os.environ.get('DME_ACCEPT_RISK', '').lower() in ('true', '1', 'yes')


def _check_risk(topic: str, action_key: str, args, *,
                cmd_parts: list = None) -> None:
    """如果 action 在黑名单中且用户未确认风险，则拒绝执行。

    Args:
        topic: 主题名（如 san）
        action_key: 黑名单中的完整动作 key（如 lun_delete）
        args: CLI 解析后的参数
        cmd_parts: 原始命令的各部分，用于显示（如 ["san", "lun", "delete"]）
    """
    blacklist = load_blacklist()
    if topic not in blacklist or action_key not in blacklist[topic]:
        return  # 不在黑名单中，安全

    cmd_display = ' '.join(cmd_parts) if cmd_parts else f'{topic} {action_key}'

    print(f'\n⚠️  风险操作警告："{cmd_display}" 是高风险操作（可能造成数据丢失或服务中断）')

    if _accepts_risk(args):
        print(f'   ✅ 风险已确认（--accept-risk / DME_ACCEPT_RISK），继续执行...\n')
        return

    print(f'   ❌ 已拒绝执行。如确认要继续，请添加 --accept-risk 参数')
    print(f'      或设置环境变量 DME_ACCEPT_RISK=true\n')
    sys.exit(1)


class DMECLI:
    """DME 运维命令行工具"""

    def __init__(self):
        self.client: Optional[DMEAPIClient] = None
        self.actions_module = None

    def load_actions(self):
        """加载 actions 模块中的所有动作"""
        if self.actions_module is None:
            from pydme import actions
            self.actions_module = actions

    def get_available_topics(self) -> Dict[str, Dict[str, List[str]]]:
        """
        获取所有可用的主题和子主题及动作

        Returns:
            主题 -> 子主题 -> 动作列表的映射
        """
        topics = {}
        self.load_actions()

        if self.actions_module is None:
            return topics

        actions_path = os.path.join(os.path.dirname(__file__), 'actions')
        if not os.path.exists(actions_path):
            return topics

        for importer, modname, ispkg in pkgutil.iter_modules([actions_path]):
            if modname.startswith('_'):
                continue
            topic = modname
            topics[topic] = {'_direct': [], '_subtopics': {}}

            try:
                module = importlib.import_module(f'pydme.actions.{modname}')
                
                if hasattr(module, 'ACTIONS'):
                    for action_key, action_info in module.ACTIONS.items():
                        subtopic = action_info.get('subtopic')
                        action_name = action_key
                        
                        # 如果有 module 字段，说明是子主题声明（不直接执行），跳过
                        if 'module' in action_info:
                            # 注册子主题
                            if subtopic not in topics[topic]['_subtopics']:
                                topics[topic]['_subtopics'][subtopic] = []
                            # 从指定模块获取动作列表
                            try:
                                sub_module = importlib.import_module(action_info['module'])
                                if hasattr(sub_module, 'ACTIONS'):
                                    for sub_action_key, sub_action_info in sub_module.ACTIONS.items():
                                        sub_subtopic = sub_action_info.get('subtopic')
                                        if sub_subtopic == subtopic or sub_subtopic == action_key:
                                            sub_action_name = sub_action_key
                                            prefix_space = f"{subtopic} "
                                            prefix_underscore = f"{subtopic}_"
                                            prefix_action_space = f"{action_key} "
                                            prefix_action_underscore = f"{action_key}_"
                                            if sub_action_key.startswith(prefix_space):
                                                sub_action_name = sub_action_key[len(prefix_space):]
                                            elif sub_action_key.startswith(prefix_underscore):
                                                sub_action_name = sub_action_key[len(prefix_underscore):]
                                            elif sub_action_key.startswith(prefix_action_space):
                                                sub_action_name = sub_action_key[len(prefix_action_space):]
                                            elif sub_action_key.startswith(prefix_action_underscore):
                                                sub_action_name = sub_action_key[len(prefix_action_underscore):]
                                            if sub_action_name not in topics[topic]['_subtopics'][subtopic]:
                                                topics[topic]['_subtopics'][subtopic].append(sub_action_name)
                            except ImportError:
                                pass
                            continue
                        
                        if subtopic:
                            # 子主题动作（三级结构）
                            if subtopic not in topics[topic]['_subtopics']:
                                topics[topic]['_subtopics'][subtopic] = []
                            # 提取动作名（去掉子主题前缀，支持空格或下划线分隔）
                            action_name = action_key
                            prefix_space = f"{subtopic} "
                            prefix_underscore = f"{subtopic}_"
                            if action_key.startswith(prefix_space):
                                action_name = action_key[len(prefix_space):]
                            elif action_key.startswith(prefix_underscore):
                                action_name = action_key[len(prefix_underscore):]
                            topics[topic]['_subtopics'][subtopic].append(action_name)
                        else:
                            # 直接动作（两级结构）
                            topics[topic]['_direct'].append(action_key)
                            
            except ImportError as e:
                print(f"警告：无法导入 actions.{modname}: {e}")

        return topics

    def parse_docstring(self, doc: str) -> Dict[str, str]:
        """
        解析函数 docstring，提取描述和参数信息

        Args:
            doc: 函数 docstring

        Returns:
            包含 'description' 和 'params' 的字典
        """
        result = {
            'description': '',
            'params': {},
            'returns': ''
        }

        if not doc:
            return result

        lines = doc.strip().split('\n')
        
        # 提取函数描述（Args 之前的部分），保留缩进和换行
        description_lines = []
        in_params = False
        in_returns = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('Args:'):
                in_params = True
                break
            if stripped.startswith('Returns:'):
                in_returns = True
                break
            if stripped:
                description_lines.append(line)  # 保留原始缩进
        
        if description_lines:
            # 计算基准缩进（第一行的缩进量）
            base_indent = len(description_lines[0]) - len(description_lines[0].lstrip())
            # 去除基准缩进，保留相对缩进（最小为 0）
            formatted = []
            for line in description_lines:
                indent = len(line) - len(line.lstrip())
                relative_indent = max(0, indent - base_indent)
                formatted.append(' ' * relative_indent + line.strip())
            result['description'] = '\n'.join(formatted)

        # 提取参数信息
        if in_params:
            current_param = None
            param_lines = []
            in_format_block = 0  # 参数格式块嵌套深度，>0 时跳过内部属性解析
            
            for line in lines:
                raw = line  # 保留原始缩进
                stripped = line.strip()
                
                # 检查是否是 Returns 或后续部分
                if stripped.startswith(('Returns:', 'Raises:', 'Note:', 'Example:')):
                    break
                
                # 在格式块内部：不解析新参数，追加到当前参数描述
                if in_format_block > 0:
                    old_depth = in_format_block
                    in_format_block += stripped.count('{') - stripped.count('}')
                    if in_format_block < 0:
                        in_format_block = 0
                    # 显示缩进：进入嵌套块时用当前深度，离开时用新深度
                    display_depth = in_format_block if stripped.count('}') > stripped.count('{') else old_depth
                    indent = '    ' * display_depth
                    if current_param:
                        param_lines.append(indent + stripped)
                    continue
                
                # 检查是否是参数定义行（如 "param_name: 描述"）
                param_match = re.match(r'^(\w+)\s*:\s*(.+)$', stripped)
                
                if param_match:
                    # 保存前一个参数
                    if current_param and param_lines:
                        result['params'][current_param] = '\n'.join(param_lines)
                    
                    current_param = param_match.group(1)
                    param_lines = [param_match.group(2)]
                    
                    # 如果该参数行同时进入参数格式/属性格式描述块，跟踪嵌套深度
                    if '参数格式如下：' in stripped or '属性格式如下：{' in stripped:
                        in_format_block = stripped.count('{') - stripped.count('}')
                        if in_format_block < 0:
                            in_format_block = 0
                
                elif current_param and stripped:
                    # 参数描述的 continuation（缩进的行）
                    param_lines.append(stripped)
            
            # 保存最后一个参数
            if current_param and param_lines:
                result['params'][current_param] = '\n'.join(param_lines)

        # 提取返回信息
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('Returns:'):
                in_returns = True
                rest = stripped[len('Returns:'):].strip()
                if rest:
                    result['returns'] = rest
                continue

            if in_returns:
                if stripped.startswith(('Raises:', 'Note:', 'Example:')):
                    break
                if stripped:
                    if result['returns']:
                        result['returns'] += '\n' + stripped
                    else:
                        result['returns'] = stripped

        return result

    def get_topic_actions(self, topic: str) -> Optional[Dict[str, Dict]]:
        """
        获取指定主题的所有动作信息

        Args:
            topic: 主题名称

        Returns:
            动作键到详细信息的映射
        """
        self.load_actions()

        if self.actions_module is None:
            return None

        try:
            module = importlib.import_module(f'pydme.actions.{topic}')
        except ImportError:
            return None

        if not hasattr(module, 'ACTIONS'):
            return None

        actions_info = {}
        for action_key, action_data in module.ACTIONS.items():
            func = action_data.get('func')
            
            # 如果有 module 字段，说明是子主题声明，跳过
            if 'module' in action_data:
                # 从子模块加载动作
                subtopic = action_data.get('subtopic')
                try:
                    sub_module = importlib.import_module(action_data['module'])
                    if hasattr(sub_module, 'ACTIONS'):
                        for sub_action_key, sub_action_data in sub_module.ACTIONS.items():
                            sub_subtopic = sub_action_data.get('subtopic')
                            if sub_subtopic == subtopic or sub_subtopic == action_key:
                                sub_func = sub_action_data.get('func')
                                if sub_func:
                                    sub_doc = inspect.getdoc(sub_func) or ""
                                    sub_parsed = self.parse_docstring(sub_doc)
                                    # 使用原始的 action_key 作为键（如 lun_list）
                                    actions_info[sub_action_key] = {
                                        'description': sub_action_data.get('description', ''),
                                        'params': sub_action_data.get('params', []),
                                        'parsed': sub_parsed,
                                        'subtopic': subtopic,
                                        'func': sub_func
                                    }
                except ImportError:
                    pass
                continue
            
            # 支持 func 为字符串（未解析）或函数对象（已解析）
            if func:
                # 如果 func 是字符串，保留原值，稍后解析
                if isinstance(func, str):
                    doc = ""
                else:
                    doc = inspect.getdoc(func) or ""
                parsed = self.parse_docstring(doc)

                actions_info[action_key] = {
                    'description': action_data.get('description', ''),
                    'params': action_data.get('params', []),
                    'parsed': parsed,
                    'subtopic': action_data.get('subtopic'),
                    'func': func
                }

        return actions_info

    def get_module_doc(self, topic: str) -> Optional[str]:
        """
        获取主题模块的整体描述

        Args:
            topic: 主题名称

        Returns:
            模块文档字符串
        """
        try:
            module = importlib.import_module(f'pydme.actions.{topic}')
            return module.__doc__ or ""
        except ImportError:
            return None

    def execute_action(self, topic: str, action_key: str, params: Dict[str, Any]) -> bool:
        """
        执行指定动作

        Args:
            topic: 主题名称
            action_key: 动作键（如 "disk_list" 或 "list"）
            params: 动作参数

        Returns:
            执行结果
        """
        self.load_actions()

        if self.actions_module is None:
            print(f"错误：无法加载 actions 模块")
            return False

        try:
            module = importlib.import_module(f'pydme.actions.{topic}')
        except ImportError:
            print(f"错误：未找到主题 '{topic}'")
            return False

        if not hasattr(module, 'ACTIONS') or action_key not in module.ACTIONS:
            print(f"错误：主题 '{topic}' 中未找到动作 '{action_key}'")
            return False

        action_info = module.ACTIONS[action_key]
        func = action_info.get('func')
        
        # 如果 func 为空，说明可能是子主题声明，需要从子模块加载
        if not func and 'module' in action_info:
            subtopic = action_info.get('subtopic')
            # 尝试从子模块获取动作
            try:
                sub_module = importlib.import_module(action_info['module'])
                if hasattr(sub_module, 'ACTIONS'):
                    for sub_action_key, sub_action_data in sub_module.ACTIONS.items():
                        sub_subtopic = sub_action_data.get('subtopic')
                        if sub_subtopic == subtopic or sub_subtopic == action_key:
                            if sub_action_key == action_key or sub_action_key.endswith(f"_{action_key}"):
                                func = sub_action_data.get('func')
                                if func:
                                    break
            except ImportError:
                pass
        
        if not func:
            print(f"错误：主题 '{topic}' 中未找到动作 '{action_key}'")
            return False

        try:
            result = func(self.client, **params)
            if result is not None:
                import json
                print(json.dumps(result, indent=2, ensure_ascii=False))
            return True
        except Exception as e:
            print(f"执行动作失败：{e}")
            import traceback
            traceback.print_exc()
            return False


def print_topic_help(cli: DMECLI, topic: str):
    """
    打印主题的帮助信息

    Args:
        cli: DMECLI 实例
        topic: 主题名称
    """
    actions_info = cli.get_topic_actions(topic)
    module_doc = cli.get_module_doc(topic)

    print(f"\n{'='*60}")
    print(f"主题：{topic}")
    print(f"{'='*60}")

    if module_doc:
        print(f"\n{module_doc.strip()}")

    if actions_info:
        # 分离直接动作和子主题动作
        direct_actions = {}
        subtopics = {}
        
        for action_key, info in actions_info.items():
            subtopic = info.get('subtopic')
            if subtopic:
                if subtopic not in subtopics:
                    subtopics[subtopic] = {}
                # 提取动作名（去掉子主题前缀）
                action_name = action_key[len(subtopic) + 1:] if action_key.startswith(f"{subtopic}_") else action_key
                subtopics[subtopic][action_name] = info
            else:
                direct_actions[action_key] = info

        # 显示直接动作（两级结构）
        if direct_actions:
            print(f"\n直接动作（<topic> <action>）:")
            print(f"{'-'*60}")
            for action_name in sorted(direct_actions.keys()):
                info = direct_actions[action_name]
                print(f"\n  {action_name}")
                print(f"    {info['description']}")

        # 显示子主题动作（三级结构）
        for subtopic in sorted(subtopics.keys()):
            print(f"\n子主题：{subtopic}（<topic> <action>）")
            print(f"{'-'*60}")
            for action_name in sorted(subtopics[subtopic].keys()):
                info = subtopics[subtopic][action_name]
                print(f"\n  {action_name}")
                print(f"    {info['description']}")

    print(f"\n{'='*60}")
    print(f"使用示例:")
    print(f"  pydme {topic} --help              # 查看主题帮助")
    print(f"  pydme {topic} <action>            # 执行直接动作")
    print(f"  pydme {topic} <subtopic> --help   # 查看子主题帮助")
    print(f"  pydme {topic} <subtopic> <action> # 执行子主题动作")
    print(f"{'='*60}\n")


def print_subtopic_help(cli: DMECLI, topic: str, subtopic: str):
    """
    打印子主题的帮助信息

    Args:
        cli: DMECLI 实例
        topic: 主题名称
        subtopic: 子主题名称
    """
    import importlib
    try:
        module = importlib.import_module(f'pydme.actions.{topic}')
    except ImportError:
        pass

    actions_info = cli.get_topic_actions(topic)

    if not actions_info:
        print(f"错误：未找到主题 '{topic}'")
        return

    print(f"\n{'='*60}")
    print(f"主题：{topic}  子主题：{subtopic}")
    print(f"{'='*60}")

    # 查找该子主题下的所有动作
    subtopic_actions = {}
    for action_key, info in actions_info.items():
        if info.get('subtopic') == subtopic:
            action_name = action_key[len(subtopic) + 1:] if action_key.startswith(f"{subtopic}_") else action_key
            subtopic_actions[action_name] = info

    if subtopic_actions:
        print(f"\n可用动作（<topic> {subtopic} <action>）:")
        print(f"{'-'*60}")
        for action_name in sorted(subtopic_actions.keys()):
            info = subtopic_actions[action_name]
            print(f"\n  {action_name}")
            print(f"    {info['description']}")
    else:
        print(f"\n未找到子主题 '{subtopic}' 下的动作")

    print(f"\n{'='*60}")
    print(f"使用示例:")
    print(f"  pydme {topic} {subtopic} --help")
    print(f"  pydme {topic} {subtopic} list --help")
    print(f"  pydme {topic} {subtopic} list --limit 10")
    print(f"{'='*60}\n")


def print_action_help(cli: DMECLI, topic: str, action_key: str, subtopic: str = None, action: str = None):
    """
    打印指定动作的详细帮助信息

    Args:
        cli: DMECLI 实例
        topic: 主题名称
        action_key: 动作键（如 "hyperscale_list"）
        subtopic: 子主题名称（可选，如 "hyperscale"）
        action: 动作名称（可选，如 "list"）
    """
    actions_info = cli.get_topic_actions(topic)

    if not actions_info or action_key not in actions_info:
        print(f"错误：未找到动作 '{topic} {action_key}'")
        return

    info = actions_info[action_key]

    # 构造显示用的命令（如果是三级结构，显示为 "topic subtopic action"）
    if subtopic and action:
        display_cmd = f"{topic} {subtopic} {action}"
    else:
        display_cmd = f"{topic} {action_key}"

    print(f"\n{'='*60}")
    print(f"动作：{display_cmd}")
    print(f"{'='*60}")

    if info['description']:
        print(f"\n描述:")
        print(f"  {info['description']}")

    if info['parsed']['description']:
        print(f"\n详细说明:")
        for line in info['parsed']['description'].split('\n'):
            print(f"  {line}")

    print(f"\n参数说明:")
    print(f"{'-'*60}")

    params = info['parsed'].get('params', {})
    if params:
        for param_name, param_desc in params.items():
            if param_name != 'client':
                print(f"\n  --{param_name}")
                for line in param_desc.split('\n'):
                    print(f"      {line}")
    else:
        print("  无参数")

    returns = info['parsed'].get('returns', '')
    if returns:
        print(f"\n输出说明:")
        print(f"{'-'*60}")
        brace_depth = 1
        for line in returns.split('\n'):
            stripped = line.strip()
            close_count = stripped.count('}')
            open_count = stripped.count('{')
            display_depth = brace_depth - close_count
            if display_depth < 0:
                display_depth = 0
            indent = '    ' * display_depth
            print(f"{indent}{stripped}")
            brace_depth += open_count - close_count
            if brace_depth < 0:
                brace_depth = 0

    print(f"\n{'='*60}")
    print(f"使用示例:")
    print(f"  pydme {display_cmd}")
    if params:
        param_str = ' '.join([f"--{p} <value>" for p in params.keys() if p != 'client'])
        print(f"  pydme {display_cmd} {param_str}")
    print(f"{'='*60}\n")


def create_parser(cli: DMECLI) -> argparse.ArgumentParser:
    """创建命令行解析器"""
    parser = argparse.ArgumentParser(
        prog='pydme',
        description='DME 运维命令行工具 - 用于存储设备的日常运维操作',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,  # 禁用内置的 --help，自定义处理
        epilog='''
使用示例:
  # 查看所有动作主题
  pydme --help

  # 查看特定主题的所有动作
  pydme storage --help

  # 查看特定子主题的所有动作
  pydme storage disk --help

  # 查看特定动作的详细帮助
  pydme storage disk list --help

  # 执行两级结构动作
  pydme storage list --limit 20

  # 执行三级结构动作
  pydme storage disk list --storage_id <id>

  # 使用环境变量设置 DME 连接信息
  export DME_API_ENDPOINT=https://192.168.1.100:26335
  export DME_API_USERNAME=admin
  export DME_API_PASSWORD=password
  pydme storage list

格式:
  topic: 动作主题，如 storage, storagepool, lun, filesystem, host, task, system
  subtopic: 子主题（可选），如 disk, fan, node, pool, snapshot, initiator
  action: 动作名称，如 list, create, delete, show, modify
        '''
    )

    # DME 连接参数（可通过环境变量设置）
    parser.add_argument('--endpoint', '-e',
                        help='DME API 端点地址，格式：https://<ip>:<port>',
                        default=os.environ.get('DME_API_ENDPOINT'))
    parser.add_argument('--user', '-u',
                        help='DME API 用户名',
                        default=os.environ.get('DME_API_USERNAME'))
    parser.add_argument('--password', '-p',
                        help='DME API 密码',
                        default=os.environ.get('DME_API_PASSWORD'))
    parser.add_argument('--token', help='DME API 认证密钥（可选，提供则跳过登录）',
                        default=os.environ.get('DME_API_AUTH_TOKEN'))
    parser.add_argument('--timeout', type=int, default=90,
                        help='API 请求超时时间（秒），默认 90 秒')
    parser.add_argument('--no-cache-auth-token', action='store_false', dest='cache_auth_token',
                        default=True, help='禁用认证密钥缓存（默认启用缓存）')

    # 全局选项
    parser.add_argument('--list-topics', action='store_true',
                        help='列出所有可用的主题')

    # 主题参数
    parser.add_argument('topic', nargs='?', help='动作主题')
    parser.add_argument('subtopic', nargs='?', help='子主题（可选）')
    parser.add_argument('action', nargs='?', help='动作名称（可选）')
    parser.add_argument('action_args', nargs='*', help='动作参数（可选）')
    parser.add_argument('--accept-risk', action='store_true',
                        help='确认接受风险，允许执行有风险的操作（如删除、修改等）')

    return parser


def main():
    """主入口函数"""
    cli = DMECLI()
    parser = create_parser(cli)

    # 使用 parse_known_args 来捕获未知参数（动作参数）
    args, unknown = parser.parse_known_args()

    # 解析未知参数为动作参数
    action_params = {}
    show_help = False  # 是否显示帮助（由 -h, --help 控制）

    i = 0
    while i < len(unknown):
        if unknown[i] in ('-h', '--help'):
            show_help = True
            i += 1
        elif unknown[i].startswith('--'):
            param_name = unknown[i][2:]  # 去掉 --
            if i + 1 < len(unknown) and not unknown[i + 1].startswith('--'):
                action_params[param_name] = unknown[i + 1]
                i += 2
            else:
                # 参数值可能被 argparse 吞为 action position 参数
                # 如 pydme storage show --storage_id XXX
                #   → argparse 把 XXX 吃进 args.action
                #   → unknown = ['--storage_id']（值丢失）
                # 此时 args.action 中有被误吞的原始值，用它补位
                action_params[param_name] = True
                i += 1
        else:
            i += 1

    # 修正：orphan --param 的值被 argparse 吃掉后，用被吞的值补位
    # 值可能被吞入 args.action（2 级命令）或 args.action_args（3 级命令）
    # 例如: pydme storage show --storage_id X  → args.action = "X"
    # 例如: pydme system task list --limit 10  → action_args = ["10"]
    # 注意：当有多个 orphan param 时，从 args.action_args 和 args.action 中逐个取补位
    orphan_params = [p for p, v in action_params.items() if v is True]
    if orphan_params:
        # args.action 先被 argparse 吃掉（更靠前），后吃的 action_args 追加在其后
        stolen_values = []
        if args.action:
            stolen_values.append(args.action)
            args.action = None
        if args.action_args:
            stolen_values.extend(args.action_args)
        args.action_args = []
        for i, pname in enumerate(orphan_params):
            if i < len(stolen_values):
                action_params[pname] = stolen_values[i]

    # 处理位置参数（如 host_id 等）
    if hasattr(args, 'action_args') and args.action_args:
        # 将第一个位置参数作为 host_id
        if len(args.action_args) >= 1 and 'host_id' not in action_params:
            action_params['host_id'] = args.action_args[0]

    # 处理全局选项
    if args.list_topics:
        topics = cli.get_available_topics()
        print("\n可用的动作主题（树形结构）:")
        print(f"{'='*70}")

        for topic in sorted(topics.keys()):
            topic_info = topics[topic]
            module_doc = cli.get_module_doc(topic)

            # 提取模块描述（第一行或前几行）
            topic_desc = ""
            if module_doc:
                first_line = module_doc.strip().split('\n')[0].strip()
                if first_line and not first_line.startswith('"""'):
                    topic_desc = first_line

            # 显示主题名称和描述
            if topic_desc:
                print(f"\n📁 {topic} - {topic_desc}")
            else:
                print(f"\n📁 {topic}")

            # 显示直接动作
            direct_actions = topic_info.get('_direct', [])
            if direct_actions:
                print(f"  ├── 直接动作:")
                for action_key in sorted(direct_actions):
                    action_desc = ""
                    # 获取动作描述
                    try:
                        module = importlib.import_module(f'pydme.actions.{topic}')
                        if hasattr(module, 'ACTIONS') and action_key in module.ACTIONS:
                            action_desc = module.ACTIONS[action_key].get('description', '')
                    except ImportError:
                        pass

                    if action_desc:
                        print(f"  │     ├── {action_key} - {action_desc}")
                    else:
                        print(f"  │     ├── {action_key}")

            # 显示子主题及其动作
            subtopics = topic_info.get('_subtopics', {})
            for subtopic in sorted(subtopics.keys()):
                actions_list = subtopics[subtopic]
                print(f"  ├── 📂 {subtopic}")

                for action_name in sorted(actions_list):
                    action_desc = ""
                    # 获取动作描述
                    try:
                        module = importlib.import_module(f'pydme.actions.{topic}')
                        # 构造完整的 action_key，支持空格和下划线分隔
                        # 例如: subtopic="cluster", action_name="list" -> "cluster_list" 或 "cluster list"
                        full_action_key_space = f"{subtopic} {action_name}"
                        full_action_key_underscore = f"{subtopic}_{action_name}"
                        
                        # 先尝试从主模块获取
                        if hasattr(module, 'ACTIONS'):
                            # 尝试多种key格式
                            for key_format in [full_action_key_space, full_action_key_underscore]:
                                if key_format in module.ACTIONS:
                                    action_desc = module.ACTIONS[key_format].get('description', '')
                                    break
                            else:
                                # 尝试从子模块获取（支持子主题模块引用）
                                for ak, ai in module.ACTIONS.items():
                                    if ai.get('module') and ai.get('subtopic') == subtopic:
                                        try:
                                            sub_module = importlib.import_module(ai['module'])
                                            for key_format in [full_action_key_space, full_action_key_underscore]:
                                                if hasattr(sub_module, 'ACTIONS') and key_format in sub_module.ACTIONS:
                                                    action_desc = sub_module.ACTIONS[key_format].get('description', '')
                                                    break
                                            if action_desc:
                                                break
                                        except ImportError:
                                            pass
                    except ImportError:
                        pass

                    if action_desc:
                        print(f"  │       ├─── {action_name} - {action_desc}")
                    else:
                        print(f"  │       ├─── {action_name}")

        print(f"\n{'='*70}")
        print("\n说明:")
        print("  📁 主题 - 主题描述")
        print("  │     ├── 直接动作 - 动作描述")
        print("  ├── 📂 子主题")
        print("  │       ├── 动作 - 动作描述")
        print(f"{'='*70}\n")
        return

    # 1. 未指定 <topic> 参数，显示全局帮助
    if not args.topic:
        parser.print_help()
        return

    # 获取主题动作信息
    actions_info = cli.get_topic_actions(args.topic)

    if not actions_info:
        print(f"错误：未找到主题 '{args.topic}'")
        return

    # 修正：argparse 将直接动作的参数值误吞为 action position 参数
    # 值已在未知参数解析阶段（745-749 行）通过 orphan 检测补回到 action_params，
    # 此处只需清空 args.action，确保 dispatch 进入 2-arg 路径
    if args.action and args.subtopic in actions_info:
        _direct_info = actions_info.get(args.subtopic, {})
        if _direct_info.get('subtopic') is None:
            args.action = None

    # 2. 只指定了 <topic>，显示主题帮助
    if not args.subtopic and not args.action:
        print_topic_help(cli, args.topic)
        return

    # 3. 指定了 <topic> <subtopic>，检查 subtopic 是直接动作还是子主题
    if args.subtopic and not args.action:
        # 检查 subtopic 是否是直接动作
        if args.subtopic in actions_info:
            # 是直接动作
            action_key = args.subtopic
            # 如果指定了 --help，显示帮助
            if show_help:
                print_action_help(cli, args.topic, action_key)
                return

            # 没有指定 --help，执行动作（需要登录）

            # 风险操作检查
            _check_risk(args.topic, action_key, args,
                        cmd_parts=[args.topic, action_key])

            endpoint = args.endpoint or os.environ.get('DME_API_ENDPOINT')
            username = args.user or os.environ.get('DME_API_USERNAME')
            password = args.password or os.environ.get('DME_API_PASSWORD')
            auth_token = args.token or os.environ.get('DME_API_AUTH_TOKEN')

            if not auth_token and not (endpoint and username and password):
                print("错误：必须提供 endpoint、user 和 password 参数，或者使用 --token 提供认证密钥")
                print("可通过 --endpoint, --user, --password, --token 或环境变量设置")
                parser.print_help()
                sys.exit(1)

            # 尝试从缓存加载 token
            if not auth_token and args.cache_auth_token and endpoint and username:
                cached = _find_cached_token(endpoint, username)
                if cached:
                    auth_token = cached

            # 创建客户端
            client = DMEAPIClient(
                endpoint=endpoint,
                username=username,
                password=password,
                auth_token=auth_token,
                timeout=args.timeout,
            )

            # 检查客户端是否已有 token，没有再登录
            if not client.headers.get("X-Auth-Token"):
                print(f"正在连接 DME: {endpoint}")
                client.login()
                # 登录成功后缓存 token
                if args.cache_auth_token and endpoint and username:
                    _update_cache(endpoint, username, client.headers.get("X-Auth-Token", ""))
            elif auth_token and args.cache_auth_token and endpoint and username:
                # 传入的 token（非缓存加载）写入缓存
                _update_cache(endpoint, username, auth_token)

            cli.client = client

            action_info = actions_info[action_key]
            func = action_info['func']

            print(f"执行：{args.topic} {action_key}")
            print(f"描述：{action_info.get('description', '')}")
            print("-" * 60)

            try:
                import inspect
                import builtins
                sig = inspect.signature(func)
                typed_params = {}

                # 参数名映射：CLI 参数名 -> 函数参数名
                param_mapping = {
                    'name': 'name',
                    'alias_name': 'name',
                    'zone_name': 'name',
                    'fabric_id': 'fabric_id',
                    'fabric_wwn': 'fabric_wwn',
                    'vsan_wwn': 'vsan_wwn',
                    'description': 'description',
                    'members': 'wwn_members',
                    'wwn_members': 'wwn_members',
                    'fwwn_members': 'fwwn_members',
                    'port_members': 'port_members',
                    'fcid_members': 'fcid_members',
                    'device_alias_members': 'device_alias_members',
                    'alias_id': 'alias_id',
                    'alias_ids': 'alias_ids',
                    'zone_id': 'zone_id',
                    'zone_ids': 'zone_ids',
                    'switch_id': 'switch_id',
                    'storageId': 'storageId',
                }

                for param_name, param_value in action_params.items():
                    # 尝试直接匹配或映射后匹配
                    func_param_name = param_mapping.get(param_name, param_name)
                    if func_param_name in sig.parameters:
                        param_type = sig.parameters[func_param_name].annotation
                        if param_type != inspect.Parameter.empty and param_value is not None:
                            if param_type in (int, float):
                                try:
                                    param_value = param_type(param_value)
                                except ValueError:
                                    print(f"警告：参数 {param_name} 无法转换为 {param_type.__name__}")
                            elif param_type in (list, builtins.list) or (hasattr(param_type, '__name__') and param_type.__name__ == 'list'):
                                import json
                                try:
                                    param_value = json.loads(param_value)
                                except (ValueError, json.JSONDecodeError):
                                    param_value = [x.strip() for x in param_value.split(',')]
                            elif param_type in (dict, builtins.dict) or (hasattr(param_type, '__name__') and param_type.__name__ == 'dict'):
                                import json
                                try:
                                    param_value = json.loads(param_value)
                                except (ValueError, json.JSONDecodeError):
                                    print(f"警告：参数 {param_name} 需要 JSON 格式")
                            elif param_type in (bool, builtins.bool):
                                if isinstance(param_value, str):
                                    param_value = param_value.lower() in ('true', '1', 'yes')

                        typed_params[func_param_name] = param_value



                # 检查函数是否需要 client 参数
                sig_params = sig.parameters
                if sig_params and 'client' in sig_params:
                    result = func(client, **typed_params)
                else:
                    result = func(**typed_params)
                import json
                if result:
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                else:
                    print("无返回数据")
            except Exception as e:
                print(f"执行失败：{e}")
                import traceback
                traceback.print_exc()
            return
        else:
            # 是子主题，显示子主题帮助
            print_subtopic_help(cli, args.topic, args.subtopic)
            return

    # 4. 指定了 <topic> <subtopic> <action>，显示动作帮助或执行动作
    if args.subtopic and args.action:
        # 尝试组合为 action_key（三级结构：<topic> <subtopic> <action>）
        # 先尝试 subtopic_action 格式（支持带空格的动作名，如 "frame list"）
        action_key = f"{args.subtopic}_{args.action}"
        
        # 如果找不到，尝试 subtopic action 格式（空格分隔）
        if action_key not in actions_info:
            # 尝试将 subtopic 和 action 组合成带空格的形式
            space_action_key = f"{args.subtopic} {args.action}"
            if space_action_key in actions_info:
                action_key = space_action_key
            else:
                # 仍然找不到，显示错误
                print(f"错误：未找到动作 '{args.topic} {args.subtopic} {args.action}'")
                available = [k for k in actions_info.keys() if k.startswith(args.subtopic + '_') or k.startswith(args.subtopic + ' ')]
                if available:
                    print(f"提示：可用动作包括：{', '.join(available)}")
                return

        # 如果指定了 --help，显示帮助；否则执行动作
        if show_help:
            # 显示帮助（不需要登录）
            print_action_help(cli, args.topic, action_key, args.subtopic, args.action)
            return

        # 执行动作（需要登录）

        # 风险操作检查
        _check_risk(args.topic, action_key, args,
                    cmd_parts=[args.topic, args.subtopic, args.action])

        endpoint = args.endpoint or os.environ.get('DME_API_ENDPOINT')
        username = args.user or os.environ.get('DME_API_USERNAME')
        password = args.password or os.environ.get('DME_API_PASSWORD')
        auth_token = args.token or os.environ.get('DME_API_AUTH_TOKEN')

        if not auth_token and not (endpoint and username and password):
            print("错误：必须提供 endpoint、user 和 password 参数，或者使用 --token 提供认证密钥")
            print("可通过 --endpoint, --user, --password, --token 或环境变量设置")
            parser.print_help()
            sys.exit(1)

        # 尝试从缓存加载 token
        if not auth_token and args.cache_auth_token and endpoint and username:
            cached = _find_cached_token(endpoint, username)
            if cached:
                auth_token = cached

        # 创建客户端
        client = DMEAPIClient(
            endpoint=endpoint,
            username=username,
            password=password,
            auth_token=auth_token,
            timeout=args.timeout,
        )

        # 检查客户端是否已有 token，没有再登录
        if not client.headers.get("X-Auth-Token"):
            print(f"正在连接 DME: {endpoint}")
            client.login()
            # 登录成功后缓存 token
            if args.cache_auth_token and endpoint and username:
                _update_cache(endpoint, username, client.headers.get("X-Auth-Token", ""))
        elif auth_token and args.cache_auth_token and endpoint and username:
            # 传入的 token（非缓存加载）写入缓存
            _update_cache(endpoint, username, auth_token)

        cli.client = client

        action_info = actions_info[action_key]
        func = action_info['func']

        # 三级结构显示为 "topic subtopic action"
        print(f"执行：{args.topic} {args.subtopic} {args.action}")
        print(f"描述：{action_info.get('description', '')}")
        print("-" * 60)

        try:
            import inspect
            import builtins
            sig = inspect.signature(func)
            typed_params = {}

            # 参数名映射：CLI 参数名 -> 函数参数名
            param_mapping = {
                'name': 'name',
                'alias_name': 'name',
                'fabric_id': 'fabric_id',
                'fabric_wwn': 'fabric_wwn',
                'vsan_wwn': 'vsan_wwn',
                'description': 'description',
                'members': 'wwn_members',
                'wwn_members': 'wwn_members',
                'fwwn_members': 'fwwn_members',
                'port_members': 'port_members',
                'fcid_members': 'fcid_members',
                'device_alias_members': 'device_alias_members',
                'alias_id': 'alias_id',
                'alias_ids': 'alias_ids',
                'zone_name': 'name',
                'zone_id': 'zone_id',
                'zone_ids': 'zone_ids',
                'switch_id': 'switch_id',
                'storageId': 'storageId',
                'vstore_ids': 'ids',
                'initiator_ids': 'initiator_ids',
                'qos_policy_ids': 'qos_policy_ids',
                'tag_ids': 'tag_ids',
                'storage_ids': 'storage_ids',
                'account_password': 'password',
                'volume_ids': 'volume_ids',
                'lun_ids': 'lun_ids',
                'zone_ids': 'zone_ids',
            }

            for param_name, param_value in action_params.items():
                # 尝试直接匹配或映射后匹配
                func_param_name = param_mapping.get(param_name, param_name)
                if func_param_name in sig.parameters:
                    param_type = sig.parameters[func_param_name].annotation
                    if param_type != inspect.Parameter.empty and param_value is not None and isinstance(param_value, str):
                        if param_type == bool:
                            if param_value.lower() in ('true', 'yes', '1', 'on'):
                                param_value = True
                            elif param_value.lower() in ('false', 'no', '0', 'off'):
                                param_value = False
                        elif param_type in (int, float):
                            try:
                                param_value = param_type(param_value)
                            except ValueError:
                                print(f"警告：参数 {param_name} 无法转换为 {param_type.__name__}")
                        elif param_type in (list, builtins.list) or (hasattr(param_type, '__name__') and param_type.__name__ == 'list'):
                            import json
                            try:
                                param_value = json.loads(param_value)
                            except (ValueError, json.JSONDecodeError):
                                param_value = [x.strip() for x in param_value.split(',')]
                        elif param_type in (dict, builtins.dict) or (hasattr(param_type, '__name__') and param_type.__name__ == 'dict'):
                            import json
                            try:
                                param_value = json.loads(param_value)
                            except (ValueError, json.JSONDecodeError):
                                print(f"警告：参数 {param_name} 需要 JSON 格式")
                        elif param_type in (bool, builtins.bool):
                            if isinstance(param_value, str):
                                param_value = param_value.lower() in ('true', '1', 'yes')

                    typed_params[func_param_name] = param_value

            result = func(client, **typed_params)
            import json
            if result:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print("无返回数据")
        except Exception as e:
            print(f"执行失败：{e}")
            import traceback
            traceback.print_exc()
        return

    parser.print_help()


if __name__ == '__main__':
    main()
