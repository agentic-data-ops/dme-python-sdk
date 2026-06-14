#!/usr/bin/env python
"""
DME Command Line Interface
Provides the CLI entry point for storage O&M operations with argument parsing and help
"""

import argparse
import os
import sys
import importlib
import pkgutil
import re
import inspect
from typing import Optional, Dict, Any, List, Tuple

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydme.client import DMEAPIClient


class DMECLI:
    """DME CLI main controller"""

    def __init__(self):
        self.client: Optional[DMEAPIClient] = None
        self.actions_module = None

    def load_actions(self):
        """Load all actions from the actions module"""
        if self.actions_module is None:
            from pydme import actions
            self.actions_module = actions

    def get_available_topics(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Get all available topics with subtopics and actions

        Returns:
            Mapping of topic -> subtopic -> action list
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
                        
                        # If 'module' field exists, it's a subtopic declaration (not directly executed), skip
                        if 'module' in action_info:
                            # Register subtopic
                            if subtopic not in topics[topic]['_subtopics']:
                                topics[topic]['_subtopics'][subtopic] = []
                            # Get action list from the specified module
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
                            # subtopic actions (three-level structure)
                            if subtopic not in topics[topic]['_subtopics']:
                                topics[topic]['_subtopics'][subtopic] = []
                            # extract action name (Remove subtopic prefix, Supports space or underscore separator) 
                            action_name = action_key
                            prefix_space = f"{subtopic} "
                            prefix_underscore = f"{subtopic}_"
                            if action_key.startswith(prefix_space):
                                action_name = action_key[len(prefix_space):]
                            elif action_key.startswith(prefix_underscore):
                                action_name = action_key[len(prefix_underscore):]
                            topics[topic]['_subtopics'][subtopic].append(action_name)
                        else:
                            # Direct action (Two-level structure) 
                            topics[topic]['_direct'].append(action_key)
                            
            except ImportError as e:
                print(f"Warning: unable to import actions.{modname}: {e}")

        return topics

    def parse_docstring(self, doc: str) -> Dict[str, str]:
        """
        Parse function docstring, extract description and parameter info

        Args:
            doc: Function docstring

        Returns:
            Dictionary with 'description' and 'params'
        """
        result = {
            'description': '',
            'params': {},
            'returns': ''
        }

        if not doc:
            return result

        lines = doc.strip().split('\n')
        
        # Extract function description (before Args section)
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
                description_lines.append(stripped)
        
        result['description'] = ' '.join(description_lines)

        # Extract parameter information
        if in_params:
            current_param = None
            param_lines = []
            in_format_block = 0  # parameter format block nesting depth, >0 skip internal attribute parsing
            
            for line in lines:
                raw = line  # preserve original indentation
                stripped = line.strip()
                
                # Check if it's Returns or later section
                if stripped.startswith(('Returns:', 'Raises:', 'Note:', 'Example:')):
                    break
                
                # Inside format block: don't parse new params, append to current param description
                if in_format_block > 0:
                    old_depth = in_format_block
                    in_format_block += stripped.count('{') - stripped.count('}')
                    if in_format_block < 0:
                        in_format_block = 0
                    # Show indentation: use current depth when entering nested block, new depth when leaving
                    display_depth = in_format_block if stripped.count('}') > stripped.count('{') else old_depth
                    indent = '    ' * display_depth
                    if current_param:
                        param_lines.append(indent + stripped)
                    continue
                
                # Check if it's a parameter definition line (e.g. "param_name: description")
                param_match = re.match(r'^(\w+)\s*:\s*(.+)$', stripped)
                
                if param_match:
                    # Save previous parameter
                    if current_param and param_lines:
                        result['params'][current_param] = '\n'.join(param_lines)
                    
                    current_param = param_match.group(1)
                    param_lines = [param_match.group(2)]
                    
                    # If this param line enters a  parameter format/ format description block, track nesting depth
                    if '参数格式如下：' in stripped or '属性格式如下：{' in stripped:
                        in_format_block = stripped.count('{') - stripped.count('}')
                        if in_format_block < 0:
                            in_format_block = 0
                
                elif current_param and stripped:
                    # Continuation of parameter description (indented lines)
                    param_lines.append(stripped)
            
            # Save the last parameter
            if current_param and param_lines:
                result['params'][current_param] = '\n'.join(param_lines)

        # Extract return information
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
        Get all action information for a specified topic

        Args:
            topic: Topic name

        Returns:
            Mapping of action keys to detailed info
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
            
            # If 'module' field exists, it's a subtopic declaration, skip
            if 'module' in action_data:
                # Load actions from sub-module
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
                                    # Use the original action_key as the key (e.g. lun_list)
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
            
            # Support func as string (unresolved) or function object (resolved)
            if func:
                # If func is a string, keep original value, parse later
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
        Get the overall description of a topic module

        Args:
            topic: Topic name

        Returns:
            Module docstring
        """
        try:
            module = importlib.import_module(f'pydme.actions.{topic}')
            return module.__doc__ or ""
        except ImportError:
            return None

    def execute_action(self, topic: str, action_key: str, params: Dict[str, Any]) -> bool:
        """
        Execute a specified action

        Args:
            topic: Topic name
            action_key: Action key (e.g. "disk_list" or "list")
            params: Action parameters

        Returns:
            Execution result
        """
        self.load_actions()

        if self.actions_module is None:
            print(f"Error: unable to load actions module")
            return False

        try:
            module = importlib.import_module(f'pydme.actions.{topic}')
        except ImportError:
            print(f"Error: topic '{topic}' not found")
            return False

        if not hasattr(module, 'ACTIONS') or action_key not in module.ACTIONS:
            print(f"Error: action '{action_key}' not found in topic '{topic}'")
            return False

        action_info = module.ACTIONS[action_key]
        func = action_info.get('func')
        
        # If func is empty, it may be a subtopic declaration, load from sub-module
        if not func and 'module' in action_info:
            subtopic = action_info.get('subtopic')
            # Try to get the action from sub-module
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
            print(f"Error: action '{action_key}' not found in topic '{topic}'")
            return False

        try:
            result = func(self.client, **params)
            if result is not None:
                import json
                print(json.dumps(result, indent=2, ensure_ascii=False))
            return True
        except Exception as e:
            print(f"Action execution failed: {e}")
            import traceback
            traceback.print_exc()
            return False


def print_topic_help(cli: DMECLI, topic: str):
    """
    Print help information for a topic

    Args:
        cli: DMECLI instance
        topic: Topic name
    """
    actions_info = cli.get_topic_actions(topic)
    module_doc = cli.get_module_doc(topic)

    print(f"\n{'='*60}")
    print(f"Topic: {topic}")
    print(f"{'='*60}")

    if module_doc:
        print(f"\n{module_doc.strip()}")

    if actions_info:
        # Separate direct actions and subtopic actions
        direct_actions = {}
        subtopics = {}
        
        for action_key, info in actions_info.items():
            subtopic = info.get('subtopic')
            if subtopic:
                if subtopic not in subtopics:
                    subtopics[subtopic] = {}
                # Extract action name (remove subtopic prefix)
                action_name = action_key[len(subtopic) + 1:] if action_key.startswith(f"{subtopic}_") else action_key
                subtopics[subtopic][action_name] = info
            else:
                direct_actions[action_key] = info

        # Display direct actions (two-level structure)
        if direct_actions:
            print(f"\nDirect actions (<topic> <action>):")
            print(f"{'-'*60}")
            for action_name in sorted(direct_actions.keys()):
                info = direct_actions[action_name]
                print(f"\n  {action_name}")
                print(f"    {info['description']}")

        # Display subtopic actions (three-level structure)
        for subtopic in sorted(subtopics.keys()):
            print(f"\nSubtopic: {subtopic} (<topic> <action>)")
            print(f"{'-'*60}")
            for action_name in sorted(subtopics[subtopic].keys()):
                info = subtopics[subtopic][action_name]
                print(f"\n  {action_name}")
                print(f"    {info['description']}")

    print(f"\n{'='*60}")
    print(f"Usage:")
    print(f"  pydme {topic} --help              # View topic help")
    print(f"  pydme {topic} <action>            # Execute direct action")
    print(f"  pydme {topic} <subtopic> --help   # View subtopic help")
    print(f"  pydme {topic} <subtopic> <action> # Execute subtopic action")
    print(f"{'='*60}\n")


def print_subtopic_help(cli: DMECLI, topic: str, subtopic: str):
    """
    Print help information for a subtopic

    Args:
        cli: DMECLI instance
        topic: Topic name
        subtopic: Subtopic name
    """
    import importlib
    try:
        module = importlib.import_module(f'pydme.actions.{topic}')
    except ImportError:
        pass

    actions_info = cli.get_topic_actions(topic)

    if not actions_info:
        print(f"Error: topic '{topic}' not found")
        return

    print(f"\n{'='*60}")
    print(f"Topic: {topic}  Subtopic: {subtopic}")
    print(f"{'='*60}")

    # Find all actions under this subtopic
    subtopic_actions = {}
    for action_key, info in actions_info.items():
        if info.get('subtopic') == subtopic:
            action_name = action_key[len(subtopic) + 1:] if action_key.startswith(f"{subtopic}_") else action_key
            subtopic_actions[action_name] = info

    if subtopic_actions:
        print(f"\nAvailable actions (<topic> {subtopic} <action>):")
        print(f"{'-'*60}")
        for action_name in sorted(subtopic_actions.keys()):
            info = subtopic_actions[action_name]
            print(f"\n  {action_name}")
            print(f"    {info['description']}")
    else:
        print(f"\nNo actions found under subtopic '{subtopic}'")

    print(f"\n{'='*60}")
    print(f"Usage:")
    print(f"  pydme {topic} {subtopic} --help")
    print(f"  pydme {topic} {subtopic} list --help")
    print(f"  pydme {topic} {subtopic} list --limit 10")
    print(f"{'='*60}\n")


def print_action_help(cli: DMECLI, topic: str, action_key: str, subtopic: str = None, action: str = None):
    """
    Print detailed help for a specific action

    Args:
        cli: DMECLI instance
        topic: Topic name
        action_key: Action key (e.g. "hyperscale_list")
        subtopic: Subtopic name (optional, e.g. "hyperscale")
        action: Action name (optional, e.g. "list")
    """
    actions_info = cli.get_topic_actions(topic)

    if not actions_info or action_key not in actions_info:
        print(f"Error: action '{topic} {action_key}' not found")
        return

    info = actions_info[action_key]

    # Construct display command (if three-level structure, show as "topic subtopic action")
    if subtopic and action:
        display_cmd = f"{topic} {subtopic} {action}"
    else:
        display_cmd = f"{topic} {action_key}"

    print(f"\n{'='*60}")
    print(f"Action: {display_cmd}")
    print(f"{'='*60}")

    if info['description']:
        print(f"\nDescription:")
        print(f"  {info['description']}")

    if info['parsed']['description']:
        print(f"\nDetails:")
        print(f"  {info['parsed']['description']}")

    print(f"\nParameters:")
    print(f"{'-'*60}")

    params = info['parsed'].get('params', {})
    if params:
        for param_name, param_desc in params.items():
            if param_name != 'client':
                print(f"\n  --{param_name}")
                for line in param_desc.split('\n'):
                    print(f"      {line}")
    else:
        print("  No parameters")

    returns = info['parsed'].get('returns', '')
    if returns:
        print(f"\nOutput:")
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
    print(f"Usage:")
    print(f"  pydme {display_cmd}")
    if params:
        param_str = ' '.join([f"--{p} <value>" for p in params.keys() if p != 'client'])
        print(f"  pydme {display_cmd} {param_str}")
    print(f"{'='*60}\n")


def create_parser(cli: DMECLI) -> argparse.ArgumentParser:
    """Create the CLI argument parser"""
    parser = argparse.ArgumentParser(
        prog='pydme',
        description='DME O&M CLI tool - for daily storage device operations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,  # Disable built-in --help, handle it custom
        epilog='''
Usage:
  # View all action topics
  pydme --help

  # View all actions for a specific topic
  pydme storage --help

  # View all actions for a specific subtopic
  pydme storage disk --help

  # View detailed help for a specific action
  pydme storage disk list --help

  # Execute a two-level action
  pydme storage list --limit 20

  # Execute a three-level action
  pydme storage disk list --storage_id <id>

  # Use environment variables to set DME connection info
  export DME_API_ENDPOINT=https://192.168.1.100:26335
  export DME_API_USERNAME=admin
  export DME_API_PASSWORD=password
  pydme storage list

Format:
  topic: Action topic, e.g. storage, storagepool, lun, filesystem, host, task, system
  subtopic: Subtopic (optional), e.g. disk, fan, node, pool, snapshot, initiator
  action: Action name, e.g. list, create, delete, show, modify
        '''
    )

    # DME connection parameters (can be set via environment variables)
    parser.add_argument('--endpoint', '-e',
                        help='DME API endpoint URL, format: https://<ip>:<port>',
                        default=os.environ.get('DME_API_ENDPOINT'))
    parser.add_argument('--user', '-u',
                        help='DME API username',
                        default=os.environ.get('DME_API_USERNAME'))
    parser.add_argument('--password', '-p',
                        help='DME API password',
                        default=os.environ.get('DME_API_PASSWORD'))
    parser.add_argument('--token', help='DME API auth token (optional, skips login if provided)',
                        default=os.environ.get('DME_API_AUTH_TOKEN'))
    parser.add_argument('--timeout', type=int, default=30,
                        help='API request timeout in seconds, default 30s')

    # Global options
    parser.add_argument('--list-topics', action='store_true',
                        help='List all available topics')

    # Topic parameters
    parser.add_argument('topic', nargs='?', help='Action topic')
    parser.add_argument('subtopic', nargs='?', help='Subtopic (optional)')
    parser.add_argument('action', nargs='?', help='Action name (optional)')
    parser.add_argument('action_args', nargs='*', help='Action arguments (optional)')

    return parser


def main():
    """Main entry point"""
    cli = DMECLI()
    parser = create_parser(cli)

    # Use parse_known_args to capture unknown args (action parameters)
    args, unknown = parser.parse_known_args()

    # Parse unknown args into action parameters
    action_params = {}
    show_help = False  # Whether to show help (controlled by -h, --help)

    i = 0
    while i < len(unknown):
        if unknown[i] in ('-h', '--help'):
            show_help = True
            i += 1
        elif unknown[i].startswith('--'):
            param_name = unknown[i][2:]  # Strip -- prefix
            if i + 1 < len(unknown) and not unknown[i + 1].startswith('--'):
                action_params[param_name] = unknown[i + 1]
                i += 2
            else:
                action_params[param_name] = True
                i += 1
        else:
            i += 1

    # Handle positional arguments (e.g. host_id)
    if hasattr(args, 'action_args') and args.action_args:
        # Use the first positional argument as host_id
        if len(args.action_args) >= 1 and 'host_id' not in action_params:
            action_params['host_id'] = args.action_args[0]

    # Handle global options
    if args.list_topics:
        topics = cli.get_available_topics()
        print("\nAvailable action topics (tree view):")
        print(f"{'='*70}")

        for topic in sorted(topics.keys()):
            topic_info = topics[topic]
            module_doc = cli.get_module_doc(topic)

            # Extract module description (first line or few lines)
            topic_desc = ""
            if module_doc:
                first_line = module_doc.strip().split('\n')[0].strip()
                if first_line and not first_line.startswith('"""'):
                    topic_desc = first_line

            # Display topic name and description
            if topic_desc:
                print(f"\n📁 {topic} - {topic_desc}")
            else:
                print(f"\n📁 {topic}")

            # Display direct actions
            direct_actions = topic_info.get('_direct', [])
            if direct_actions:
                print(f"  ├── Direct actions:")
                for action_key in sorted(direct_actions):
                    action_desc = ""
                    # Get action description
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

            # Display subtopics and their actions
            subtopics = topic_info.get('_subtopics', {})
            for subtopic in sorted(subtopics.keys()):
                actions_list = subtopics[subtopic]
                print(f"  ├── 📂 {subtopic}")

                for action_name in sorted(actions_list):
                    action_desc = ""
                    # Get action description
                    try:
                        module = importlib.import_module(f'pydme.actions.{topic}')
                        # Construct the full action_key, supporting space or underscore separator
                        # e.g. subtopic="cluster", action_name="list" -> "cluster_list" or "cluster list"
                        full_action_key_space = f"{subtopic} {action_name}"
                        full_action_key_underscore = f"{subtopic}_{action_name}"
                        
                        # Try getting from main module first
                        if hasattr(module, 'ACTIONS'):
                            # Try multiple key formats
                            for key_format in [full_action_key_space, full_action_key_underscore]:
                                if key_format in module.ACTIONS:
                                    action_desc = module.ACTIONS[key_format].get('description', '')
                                    break
                            else:
                                # Try getting from sub-module (supporting subtopic module references)
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
        print("\nLegend:")
        print("  📁 Topic - Topic description")
        print("  │     ├── Direct action - Action description")
        print("  ├── 📂 Subtopic")
        print("  │       ├── Action - Action description")
        print(f"{'='*70}\n")
        return

    # 1. No <topic> specified, show global help
    if not args.topic:
        parser.print_help()
        return

    # Get topic action information
    actions_info = cli.get_topic_actions(args.topic)

    if not actions_info:
        print(f"Error: topic '{args.topic}' not found")
        return

    # 2. Only <topic> specified, show topic help
    if not args.subtopic and not args.action:
        print_topic_help(cli, args.topic)
        return

    # 3. <topic> <subtopic> specified, check if subtopic is a direct action or a subtopic
    if args.subtopic and not args.action:
        # Check if subtopic is a direct action
        if args.subtopic in actions_info:
            # Is a direct action
            action_key = args.subtopic
            # If --help is specified, show help
            if show_help:
                print_action_help(cli, args.topic, action_key)
                return

            # No --help specified, execute the action (login required)
            endpoint = args.endpoint or os.environ.get('DME_API_ENDPOINT')
            username = args.user or os.environ.get('DME_API_USERNAME')
            password = args.password or os.environ.get('DME_API_PASSWORD')
            auth_token = args.token or os.environ.get('DME_API_AUTH_TOKEN')

            if not auth_token and not (endpoint and username and password):
                print("Error: must provide endpoint, user, and password, or use --token for auth")
                print("Can be set via --endpoint, --user, --password, --token or environment variables")
                parser.print_help()
                sys.exit(1)

            # Create client and login
            client = DMEAPIClient(
                endpoint=endpoint,
                username=username,
                password=password,
                auth_token=auth_token,
                timeout=args.timeout,
            )

            if not auth_token:
                print(f"Connecting to DME: {endpoint}")
                client.login()

            cli.client = client

            action_info = actions_info[action_key]
            func = action_info['func']

            print(f"Executing: {args.topic} {action_key}")
            print(f"Description: {action_info.get('description', '')}")
            print("-" * 60)

            try:
                import inspect
                import builtins
                sig = inspect.signature(func)
                typed_params = {}

                # Parameter name mapping: CLI param name -> function param name
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
                    # try direct match or mapped match
                    func_param_name = param_mapping.get(param_name, param_name)
                    if func_param_name in sig.parameters:
                        param_type = sig.parameters[func_param_name].annotation
                        if param_type != inspect.Parameter.empty and param_value is not None:
                            if param_type in (int, float):
                                try:
                                    param_value = param_type(param_value)
                                except ValueError:
                                    print(f" warning:  parameter {param_name} cannot convert to {param_type.__name__}")
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
                                    print(f" warning:  parameter {param_name}  need JSON  format")

                        typed_params[func_param_name] = param_value

                # Check if function requires client  parameter
                sig_params = sig.parameters
                if sig_params and 'client' in sig_params:
                    result = func(client, **typed_params)
                else:
                    result = func(**typed_params)
                import json
                if result:
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                else:
                    print("No return data")
            except Exception as e:
                print(f"Execution failed: {e}")
                import traceback
                traceback.print_exc()
            return
        else:
            # is subtopic, show subtopic help
            print_subtopic_help(cli, args.topic, args.subtopic)
            return

    # 4.  specified topic, subtopic, action, Show action help or execute action
    if args.subtopic and args.action:
        # try to combine as action_key (Three-level structure: <topic> <subtopic> <action>) 
        #  try subtopic_action format first (supports spaces in action names), e.g. "frame list") 
        action_key = f"{args.subtopic}_{args.action}"
        
        # if not found, try subtopic action format (space-separated)
        if action_key not in actions_info:
            #  try to combine subtopic and action into space-separated format
            space_action_key = f"{args.subtopic} {args.action}"
            if space_action_key in actions_info:
                action_key = space_action_key
            else:
                # still not found, show error
                print(f" error: Action not found '{args.topic} {args.subtopic} {args.action}'")
                available = [k for k in actions_info.keys() if k.startswith(args.subtopic + '_') or k.startswith(args.subtopic + ' ')]
                if available:
                    print(f"Tip: Available actions include: {', '.join(available)}")
                return

        # if specified --help, Show help; otherwise execute action
        if show_help:
            # Show help (no login needed) 
            print_action_help(cli, args.topic, action_key, args.subtopic, args.action)
            return

        #  Execute action (login required) 
        endpoint = args.endpoint or os.environ.get('DME_API_ENDPOINT')
        username = args.user or os.environ.get('DME_API_USERNAME')
        password = args.password or os.environ.get('DME_API_PASSWORD')
        auth_token = args.token or os.environ.get('DME_API_AUTH_TOKEN')

        if not auth_token and not (endpoint and username and password):
            print(" Error: endpoint, user and password must be provided, or use --token to provide auth token")
            print(" can pass --endpoint, --user, --password, --token or set via environment variables")
            parser.print_help()
            sys.exit(1)

        # Create client and login
        client = DMEAPIClient(
            endpoint=endpoint,
            username=username,
            password=password,
            auth_token=auth_token,
            timeout=args.timeout,
        )

        if not auth_token:
            print(f"Connecting to DME: {endpoint}")
            client.login()

        cli.client = client

        action_info = actions_info[action_key]
        func = action_info['func']

        # three-level structure shown as "topic subtopic action"
        print(f" execute: {args.topic} {args.subtopic} {args.action}")
        print(f" description: {action_info.get('description', '')}")
        print("-" * 60)

        try:
            import inspect
            import builtins
            sig = inspect.signature(func)
            typed_params = {}

            #  Parameter name mapping: CLI param name -> function param name
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
            }

            for param_name, param_value in action_params.items():
                # try direct match or mapped match
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
                                print(f" warning:  parameter {param_name} cannot convert to {param_type.__name__}")
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
                                print(f" warning:  parameter {param_name}  need JSON  format")

                    typed_params[func_param_name] = param_value

            result = func(client, **typed_params)
            import json
            if result:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print("No return data")
        except Exception as e:
            print(f"Execution failed: {e}")
            import traceback
            traceback.print_exc()
        return

    parser.print_help()


if __name__ == '__main__':
    main()
