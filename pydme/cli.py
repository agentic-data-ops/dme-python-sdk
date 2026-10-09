#!/usr/bin/env python
"""
DME O&M command-line tool
Provides the command-line entry for storage O&M operations, with argument parsing and help
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

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydme.client import DMEAPIClient
from pydme.i18n import (resolve_lang, DEFAULT_LANG, get_action_description,
                        get_action_doc, get_topic_description)


def load_blacklist() -> Dict[str, list]:
    """
    Load the risk-operation blacklist.

    Priority:
    1. User-defined ~/.config/pydme/blacklist.json
    2. If absent, copy the packaged pydme/config/blacklist.json

    Returns:
        { topic: [action_key, ...] }
    """
    user_path = Path.home() / '.config' / 'pydme' / 'blacklist.json'

    if not user_path.exists():
        # Try to copy the default blacklist from the package
        try:
            # Python 3.9+: importlib.resources.files
            from importlib.resources import files as res_files
            src = res_files('pydme.config').joinpath('blacklist.json')
            default_data = src.read_text(encoding='utf-8')
        except (ImportError, TypeError, FileNotFoundError, ModuleNotFoundError):
            # Fallback: use the __file__-based path (compatible with Python 3.8 / dev mode)
            try:
                pkg_dir = Path(__file__).resolve().parent / 'config'
                default_data = (pkg_dir / 'blacklist.json').read_text(encoding='utf-8')
            except FileNotFoundError:
                print('Warning: blacklist.json not found, skipping risk check', file=sys.stderr)
                return {}

        # Write to the user directory
        try:
            user_path.parent.mkdir(parents=True, exist_ok=True)
            user_path.write_text(default_data, encoding='utf-8')
        except (OSError, PermissionError):
            # User directory is not writable (e.g. CI environment), use the packaged data directly
            return json.loads(default_data)

    try:
        return json.loads(user_path.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, OSError) as e:
        print(f'Warning: failed to read blacklist.json ({e}), skipping risk check', file=sys.stderr)
        return {}


def _accepts_risk(args) -> bool:
    """Check whether the user has confirmed risk acceptance (via CLI argument or environment variable)."""
    return args.accept_risk or os.environ.get('DME_ACCEPT_RISK', '').lower() in ('true', '1', 'yes')


def _check_risk(topic: str, action_key: str, args, *,
                cmd_parts: list = None) -> None:
    """Refuse to execute if the action is blacklisted and the user has not confirmed the risk.

    Args:
        topic: the topic name (e.g. san)
        action_key: the full action key in the blacklist (e.g. lun_delete)
        args: the parsed CLI arguments
        cmd_parts: the parts of the original command, for display (e.g. ["san", "lun", "delete"])
    """
    blacklist = load_blacklist()
    if topic not in blacklist or action_key not in blacklist[topic]:
        return  # not blacklisted, safe

    cmd_display = ' '.join(cmd_parts) if cmd_parts else f'{topic} {action_key}'

    print(f'\n⚠️  Risk operation warning: "{cmd_display}" is a high-risk operation (may cause data loss or service interruption)')

    if _accepts_risk(args):
        print(f'   ✅ Risk confirmed (--accept-risk / DME_ACCEPT_RISK), continuing...\n')
        return

    print(f'   ❌ Execution rejected. To continue, add the --accept-risk argument')
    print(f'      or set the environment variable DME_ACCEPT_RISK=true\n')
    sys.exit(1)


class DMECLI:
    """DME O&M command-line tool"""

    def __init__(self):
        self.client: Optional[DMEAPIClient] = None
        self.actions_module = None
        self.lang = DEFAULT_LANG  # comment language (--lang / DME_CLI_LANG), resolved in main()

    def _doc_for(self, topic: str, action_key: str, func) -> str:
        """Get the action comment text in the current language.

        Prefers the docstring rebuilt from the i18n resource by (topic, action_key);
        falls back to the function docstring when missing (warns if empty after
        docstring removal).
        """
        doc = get_action_doc(topic, action_key, self.lang)
        if doc is not None:
            return doc
        fallback = inspect.getdoc(func) or ""
        if not fallback:
            print(f"Warning: i18n resource is missing comments for {self.lang}.{topic}.{action_key}, please update the corresponding YAML",
                  file=sys.stderr)
        return fallback

    def load_actions(self):
        """Load all actions in the actions module"""
        if self.actions_module is None:
            from pydme import actions
            self.actions_module = actions

    def get_available_topics(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Get all available topics, subtopics and actions

        Returns:
            A mapping of topic -> subtopic -> action list
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
                        
                        # A 'module' field means a subtopic declaration (not directly executable), skip it
                        if 'module' in action_info:
                            # Register the subtopic
                            if subtopic not in topics[topic]['_subtopics']:
                                topics[topic]['_subtopics'][subtopic] = []
                            # Get the action list from the specified module
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
                            # Subtopic action (three-level structure)
                            if subtopic not in topics[topic]['_subtopics']:
                                topics[topic]['_subtopics'][subtopic] = []
                            # Extract the action name (strip the subtopic prefix, separated by space or underscore)
                            action_name = action_key
                            prefix_space = f"{subtopic} "
                            prefix_underscore = f"{subtopic}_"
                            if action_key.startswith(prefix_space):
                                action_name = action_key[len(prefix_space):]
                            elif action_key.startswith(prefix_underscore):
                                action_name = action_key[len(prefix_underscore):]
                            topics[topic]['_subtopics'][subtopic].append(action_name)
                        else:
                            # Direct action (two-level structure)
                            topics[topic]['_direct'].append(action_key)
                            
            except ImportError as e:
                print(f"Warning: unable to import actions.{modname}: {e}")

        return topics

    def parse_docstring(self, doc: str) -> Dict[str, str]:
        """
        Parse a function docstring and extract the description and parameter information

        Args:
            doc: the function docstring

        Returns:
            A dict containing 'description' and 'params'
        """
        result = {
            'description': '',
            'params': {},
            'returns': ''
        }

        if not doc:
            return result

        lines = doc.strip().split('\n')
        
        # Extract the function description (the part before Args), keeping indentation and line breaks
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
                description_lines.append(line)  # keep the original indentation
        
        if description_lines:
            # Compute the base indentation (indentation of the first line)
            base_indent = len(description_lines[0]) - len(description_lines[0].lstrip())
            # Strip the base indentation, keeping the relative indentation (minimum 0)
            formatted = []
            for line in description_lines:
                indent = len(line) - len(line.lstrip())
                relative_indent = max(0, indent - base_indent)
                formatted.append(' ' * relative_indent + line.strip())
            result['description'] = '\n'.join(formatted)

        # Extract the parameter information
        if in_params:
            current_param = None
            param_lines = []
            in_format_block = 0  # nesting depth of the parameter format block; skip inner attribute parsing when > 0
            
            for line in lines:
                raw = line  # keep the original indentation
                stripped = line.strip()
                
                # Check whether this is the Returns section or later
                if stripped.startswith(('Returns:', 'Raises:', 'Note:', 'Example:')):
                    break
                
                # Inside a format block: do not parse new parameters, append to the current parameter description
                if in_format_block > 0:
                    old_depth = in_format_block
                    in_format_block += stripped.count('{') - stripped.count('}')
                    if in_format_block < 0:
                        in_format_block = 0
                    # Display indentation: use the current depth when entering a nested block,
                    # the new depth when leaving it
                    display_depth = in_format_block if stripped.count('}') > stripped.count('{') else old_depth
                    indent = '    ' * display_depth
                    if current_param:
                        param_lines.append(indent + stripped)
                    continue
                
                # Check whether this is a parameter definition line (e.g. "param_name: description")
                param_match = re.match(r'^(\w+)\s*:\s*(.+)$', stripped)
                
                if param_match:
                    # Save the previous parameter
                    if current_param and param_lines:
                        result['params'][current_param] = '\n'.join(param_lines)
                    
                    current_param = param_match.group(1)
                    param_lines = [param_match.group(2)]
                    
                    # If the parameter line enters a parameter-format/attribute-format block,
                    # track the nesting depth (both zh_CN and en_US markers)
                    if ('参数格式如下' in stripped or '属性格式如下' in stripped
                            or 'parameter format' in stripped or 'attribute format' in stripped):
                        in_format_block = stripped.count('{') - stripped.count('}')
                        if in_format_block < 0:
                            in_format_block = 0
                
                elif current_param and stripped:
                    # Continuation of the parameter description (indented lines)
                    param_lines.append(stripped)
            
            # Save the last parameter
            if current_param and param_lines:
                result['params'][current_param] = '\n'.join(param_lines)

        # Extract the return information (reset in_returns: without an Args section the
        # previous loop may have set it when hitting Returns:)
        in_returns = False
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
        Get the information for all actions of the specified topic

        Args:
            topic: the topic name

        Returns:
            A mapping from action keys to detailed information
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
            
            # A 'module' field means a subtopic declaration, skip it
            if 'module' in action_data:
                # Load actions from the submodule
                subtopic = action_data.get('subtopic')
                try:
                    sub_module = importlib.import_module(action_data['module'])
                    if hasattr(sub_module, 'ACTIONS'):
                        for sub_action_key, sub_action_data in sub_module.ACTIONS.items():
                            sub_subtopic = sub_action_data.get('subtopic')
                            if sub_subtopic == subtopic or sub_subtopic == action_key:
                                sub_func = sub_action_data.get('func')
                                if sub_func:
                                    sub_doc = self._doc_for(topic, sub_action_key, sub_func)
                                    sub_parsed = self.parse_docstring(sub_doc)
                                    # Use the original action_key as the key (e.g. lun_list)
                                    actions_info[sub_action_key] = {
                                        'description': (get_action_description(topic, sub_action_key, self.lang)
                                                        or sub_action_data.get('description', '')),
                                        'params': sub_action_data.get('params', []),
                                        'parsed': sub_parsed,
                                        'subtopic': subtopic,
                                        'func': sub_func
                                    }
                except ImportError:
                    pass
                continue
            
            # Support func being a string (unresolved) or a function object (resolved)
            if func:
                # If func is a string, keep the original value and parse it later
                if isinstance(func, str):
                    doc = ""
                else:
                    doc = self._doc_for(topic, action_key, func)
                parsed = self.parse_docstring(doc)

                actions_info[action_key] = {
                    'description': (get_action_description(topic, action_key, self.lang)
                                    or action_data.get('description', '')),
                    'params': action_data.get('params', []),
                    'parsed': parsed,
                    'subtopic': action_data.get('subtopic'),
                    'func': func
                }

        return actions_info

    def get_module_doc(self, topic: str) -> Optional[str]:
        """
        Get the overall description of the topic module

        Args:
            topic: the topic name

        Returns:
            The module docstring
        """
        try:
            module = importlib.import_module(f'pydme.actions.{topic}')
            return module.__doc__ or ""
        except ImportError:
            return None

    def execute_action(self, topic: str, action_key: str, params: Dict[str, Any]) -> bool:
        """
        Execute the specified action

        Args:
            topic: the topic name
            action_key: the action key (e.g. "disk_list" or "list")
            params: the action parameters

        Returns:
            The execution result
        """
        self.load_actions()

        if self.actions_module is None:
            print(f"Error: unable to load the actions module")
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
        
        # If func is empty, it may be a subtopic declaration; load from the submodule
        if not func and 'module' in action_info:
            subtopic = action_info.get('subtopic')
            # Try to get the action from the submodule
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
    Print the help information of a topic

    Args:
        cli: a DMECLI instance
        topic: the topic name
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
                # Extract the action name (strip the subtopic prefix)
                action_name = action_key[len(subtopic) + 1:] if action_key.startswith(f"{subtopic}_") else action_key
                subtopics[subtopic][action_name] = info
            else:
                direct_actions[action_key] = info

        # Show direct actions (two-level structure)
        if direct_actions:
            print(f"\nDirect actions (<topic> <action>):")
            print(f"{'-'*60}")
            for action_name in sorted(direct_actions.keys()):
                info = direct_actions[action_name]
                print(f"\n  {action_name}")
                for line in info['description'].split('\n'):
                    print(f"    {line}")

        # Show subtopic actions (three-level structure)
        for subtopic in sorted(subtopics.keys()):
            print(f"\nSubtopic: {subtopic} (<topic> <action>)")
            print(f"{'-'*60}")
            for action_name in sorted(subtopics[subtopic].keys()):
                info = subtopics[subtopic][action_name]
                print(f"\n  {action_name}")
                for line in info['description'].split('\n'):
                    print(f"    {line}")

    print(f"\n{'='*60}")
    print(f"Usage:")
    print(f"  pydme {topic} --help              # view topic help")
    print(f"  pydme {topic} <action>            # execute a direct action")
    print(f"  pydme {topic} <subtopic> --help   # view subtopic help")
    print(f"  pydme {topic} <subtopic> <action> # execute a subtopic action")
    print(f"{'='*60}\n")


def print_subtopic_help(cli: DMECLI, topic: str, subtopic: str):
    """
    Print the help information of a subtopic

    Args:
        cli: a DMECLI instance
        topic: the topic name
        subtopic: the subtopic name
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
            for line in info['description'].split('\n'):
                print(f"    {line}")
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
    Print the detailed help information of the specified action

    Args:
        cli: a DMECLI instance
        topic: the topic name
        action_key: the action key (e.g. "hyperscale_list")
        subtopic: the subtopic name (optional, e.g. "hyperscale")
        action: the action name (optional, e.g. "list")
    """
    actions_info = cli.get_topic_actions(topic)

    if not actions_info or action_key not in actions_info:
        print(f"Error: action '{topic} {action_key}' not found")
        return

    info = actions_info[action_key]

    # Build the command used for display (for a three-level structure, show "topic subtopic action")
    if subtopic and action:
        display_cmd = f"{topic} {subtopic} {action}"
    else:
        display_cmd = f"{topic} {action_key}"

    print(f"\n{'='*60}")
    print(f"Action: {display_cmd}")
    print(f"{'='*60}")

    if info['parsed']['description']:
        print(f"\nDescription:")
        for line in info['parsed']['description'].split('\n'):
            print(f"  {line}")

    print(f"\nParameters:")
    print(f"{'-'*60}")

    params = info['parsed'].get('params', {})
    if params:
        for param_name, param_desc in params.items():
            if param_name != 'client':  # client is injected by the caller, not a CLI parameter
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
    """Create the command-line parser"""
    parser = argparse.ArgumentParser(
        prog='pydme',
        description='DME O&M command-line tool - for daily storage O&M operations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,  # disable the built-in --help, handled manually
        epilog='''
Usage:
  # view all action topics
  pydme --help

  # view all actions of a specific topic
  pydme storage --help

  # view all actions of a specific subtopic
  pydme storage disk --help

  # view the detailed help of a specific action
  pydme storage disk list --help

  # execute a two-level structure action
  pydme storage list --limit 20

  # execute a three-level structure action
  pydme storage disk list --storage_id <id>

  # configure the DME connection via environment variables
  export DME_API_ENDPOINT=https://192.168.1.100:26335
  export DME_API_USERNAME=admin
  export DME_API_PASSWORD=password
  pydme storage list

Format:
  topic: the action topic, e.g. storage, storagepool, lun, filesystem, host, task, system
  subtopic: the subtopic (optional), e.g. disk, fan, node, pool, snapshot, initiator
  action: the action name, e.g. list, create, delete, show, modify
        '''
    )

    # DME connection parameters (can also be set via environment variables)
    parser.add_argument('--endpoint', '-e',
                        help='DME API endpoint, format: https://<ip>:<port>',
                        default=os.environ.get('DME_API_ENDPOINT'))
    parser.add_argument('--user', '-u',
                        help='DME API username',
                        default=os.environ.get('DME_API_USERNAME'))
    parser.add_argument('--password', '-p',
                        help='DME API password',
                        default=os.environ.get('DME_API_PASSWORD'))
    parser.add_argument('--token', help='DME API auth token (optional; skips login when provided)',
                        default=os.environ.get('DME_API_AUTH_TOKEN'))
    parser.add_argument('--timeout', type=int, default=90,
                        help='API request timeout in seconds (default: 90)')
    parser.add_argument('--no-cache-auth-token', action='store_false', dest='cache_auth_token',
                        default=True, help='disable auth token caching (caching enabled by default)')

    # Global options
    parser.add_argument('--list-topics', action='store_true',
                        help='list all available topics')
    parser.add_argument('--lang', choices=['zh_CN', 'en_US'], default=None,
                        help='comment language: zh_CN (default) or en_US; can also be set via the DME_CLI_LANG environment variable')

    # Topic parameters
    parser.add_argument('topic', nargs='?', help='action topic')
    parser.add_argument('subtopic', nargs='?', help='subtopic (optional)')
    parser.add_argument('action', nargs='?', help='action name (optional)')
    parser.add_argument('action_args', nargs='*', help='action arguments (optional)')
    parser.add_argument('--accept-risk', action='store_true',
                        help='confirm risk acceptance, allowing risky operations (e.g. delete, modify)')

    return parser


def main():
    """Main entry function"""
    cli = DMECLI()
    parser = create_parser(cli)

    # Use parse_known_args to capture unknown arguments (action parameters)
    args, unknown = parser.parse_known_args()

    # Comment language: --lang first, then DME_CLI_LANG, default zh_CN
    cli.lang = resolve_lang(args.lang)

    # Parse unknown arguments as action parameters
    action_params = {}
    show_help = False  # whether to show help (controlled by -h, --help)

    i = 0
    while i < len(unknown):
        if unknown[i] in ('-h', '--help'):
            show_help = True
            i += 1
        elif unknown[i].startswith('--'):
            param_name = unknown[i][2:]  # strip the leading --
            if i + 1 < len(unknown) and not unknown[i + 1].startswith('--'):
                action_params[param_name] = unknown[i + 1]
                i += 2
            else:
                # The value may have been swallowed by argparse as an action position argument
                # e.g. pydme storage show --storage_id XXX
                #   -> argparse puts XXX into args.action
                #   -> unknown = ['--storage_id'] (value lost)
                # In this case args.action holds the original swallowed value; use it as a placeholder
                action_params[param_name] = True
                i += 1
        else:
            i += 1

    # Fix: restore values swallowed by argparse for orphan --params
    # Values may have been swallowed into args.action (2-level command) or args.action_args (3-level command)
    # e.g. pydme storage show --storage_id X  -> args.action = "X"
    # e.g. pydme system task list --limit 10  -> action_args = ["10"]
    # Note: when there are multiple orphan params, restore them one by one from args.action_args and args.action
    orphan_params = [p for p, v in action_params.items() if v is True]
    if orphan_params:
        # args.action is swallowed first (more upfront), action_args appended after it
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
            # Module description is read from the i18n resource (same source as the module docstring first line)
            topic_desc = get_topic_description(topic, cli.lang)

            # Show the topic name and description
            if topic_desc:
                print(f"\n📁 {topic} - {topic_desc}")
            else:
                print(f"\n📁 {topic}")

            # Show direct actions
            direct_actions = topic_info.get('_direct', [])
            if direct_actions:
                print(f"  ├── Direct actions:")
                for action_key in sorted(direct_actions):
                    # Action description is read from the i18n resource (list view shows only the first line)
                    action_desc = get_action_description(topic, action_key, cli.lang).split('\n')[0]

                    if action_desc:
                        print(f"  │     ├── {action_key} - {action_desc}")
                    else:
                        print(f"  │     ├── {action_key}")

            # Show subtopics and their actions
            subtopics = topic_info.get('_subtopics', {})
            for subtopic in sorted(subtopics.keys()):
                actions_list = subtopics[subtopic]
                print(f"  ├── 📂 {subtopic}")

                for action_name in sorted(actions_list):
                    # Build the full action key, supporting space- and underscore-separated forms
                    # e.g. subtopic="cluster", action_name="list" -> "cluster_list" or "cluster list"
                    full_action_key_space = f"{subtopic} {action_name}"
                    full_action_key_underscore = f"{subtopic}_{action_name}"

                    # Action description is read from the i18n resource (list view shows only the first line)
                    action_desc = ""
                    for key_format in [full_action_key_space, full_action_key_underscore]:
                        action_desc = get_action_description(topic, key_format, cli.lang).split('\n')[0]
                        if action_desc:
                            break

                    if action_desc:
                        print(f"  │       ├─── {action_name} - {action_desc}")
                    else:
                        print(f"  │       ├─── {action_name}")

        print(f"\n{'='*70}")
        print("\nLegend:")
        print("  📁 topic - topic description")
        print("  │     ├── direct action - action description")
        print("  ├── 📂 subtopic")
        print("  │       ├── action - action description")
        print(f"{'='*70}\n")
        return

    # 1. No <topic> specified: show the global help
    if not args.topic:
        parser.print_help()
        return

    # Get the topic action information
    actions_info = cli.get_topic_actions(args.topic)

    if not actions_info:
        print(f"Error: topic '{args.topic}' not found")
        return

    # Fix: argparse may swallow the value of a direct action parameter as an action position argument
    # The value was already restored to action_params by the orphan detection in the unknown-args
    # parsing stage; here only clear args.action to make the dispatch enter the 2-arg path
    if args.action and args.subtopic in actions_info:
        _direct_info = actions_info.get(args.subtopic, {})
        if _direct_info.get('subtopic') is None:
            args.action = None

    # 2. Only <topic> specified: show the topic help
    if not args.subtopic and not args.action:
        print_topic_help(cli, args.topic)
        return

    # 3. <topic> <subtopic> specified: check whether subtopic is a direct action or a subtopic
    if args.subtopic and not args.action:
        # Check whether subtopic is a direct action
        if args.subtopic in actions_info:
            # It is a direct action
            action_key = args.subtopic
            # If --help is specified, show the help
            if show_help:
                print_action_help(cli, args.topic, action_key)
                return

            # --help not specified: execute the action (requires login)

            # Risk-operation check
            _check_risk(args.topic, action_key, args,
                        cmd_parts=[args.topic, action_key])

            endpoint = args.endpoint or os.environ.get('DME_API_ENDPOINT')
            username = args.user or os.environ.get('DME_API_USERNAME')
            password = args.password or os.environ.get('DME_API_PASSWORD')
            auth_token = args.token or os.environ.get('DME_API_AUTH_TOKEN')

            if not auth_token and not (endpoint and username and password):
                print("Error: endpoint, user and password arguments are required, or use --token to provide an auth token")
                print("Set them via --endpoint, --user, --password, --token or environment variables")
                parser.print_help()
                sys.exit(1)

            # Create the client (loads/saves the token cache internally)
            client = DMEAPIClient(
                endpoint=endpoint,
                username=username,
                password=password,
                auth_token=auth_token,
                timeout=args.timeout,
                cache_token=args.cache_auth_token,
            )

            # Check whether the client already has a token; log in otherwise
            if not client.headers.get("X-Auth-Token"):
                print(f"Connecting to DME: {endpoint}")
                try:
                    client.login()
                except Exception as e:
                    print(f"Login failed: {e}")
                    sys.exit(1)

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

                # Parameter name mapping: CLI parameter name -> function parameter name
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
                    # Try a direct match or a mapped match
                    func_param_name = param_mapping.get(param_name, param_name)
                    if func_param_name in sig.parameters:
                        param_type = sig.parameters[func_param_name].annotation
                        if param_type != inspect.Parameter.empty and param_value is not None:
                            if param_type in (int, float):
                                try:
                                    param_value = param_type(param_value)
                                except ValueError:
                                    print(f"Warning: parameter {param_name} cannot be converted to {param_type.__name__}")
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
                                    print(f"Warning: parameter {param_name} requires JSON format")
                            elif param_type in (bool, builtins.bool):
                                if isinstance(param_value, str):
                                    param_value = param_value.lower() in ('true', '1', 'yes')

                        typed_params[func_param_name] = param_value



                # Check whether the function requires the client parameter
                sig_params = sig.parameters
                if sig_params and 'client' in sig_params:
                    result = func(client, **typed_params)
                else:
                    result = func(**typed_params)
                import json
                if result:
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                else:
                    print("No data returned")
            except Exception as e:
                print(f"Execution failed: {e}")
                import traceback
                traceback.print_exc()
            return
        else:
            # It is a subtopic, show the subtopic help
            print_subtopic_help(cli, args.topic, args.subtopic)
            return

    # 4. <topic> <subtopic> <action> specified: show action help or execute the action
    if args.subtopic and args.action:
        # Try to build the action_key (three-level structure: <topic> <subtopic> <action>)
        # First try the subtopic_action format (supports space-separated action names, e.g. "frame list")
        action_key = f"{args.subtopic}_{args.action}"
        
        # If not found, try the "subtopic action" format (space-separated)
        if action_key not in actions_info:
            # Try combining subtopic and action with a space
            space_action_key = f"{args.subtopic} {args.action}"
            if space_action_key in actions_info:
                action_key = space_action_key
            else:
                # Still not found, show an error
                print(f"Error: action '{args.topic} {args.subtopic} {args.action}' not found")
                available = [k for k in actions_info.keys() if k.startswith(args.subtopic + '_') or k.startswith(args.subtopic + ' ')]
                if available:
                    print(f"Hint: available actions include: {', '.join(available)}")
                return

        # If --help is specified, show the help; otherwise execute the action
        if show_help:
            # Show the help (no login required)
            print_action_help(cli, args.topic, action_key, args.subtopic, args.action)
            return

        # Execute the action (requires login)

        # Risk-operation check
        _check_risk(args.topic, action_key, args,
                    cmd_parts=[args.topic, args.subtopic, args.action])

        endpoint = args.endpoint or os.environ.get('DME_API_ENDPOINT')
        username = args.user or os.environ.get('DME_API_USERNAME')
        password = args.password or os.environ.get('DME_API_PASSWORD')
        auth_token = args.token or os.environ.get('DME_API_AUTH_TOKEN')

        if not auth_token and not (endpoint and username and password):
            print("Error: endpoint, user and password arguments are required, or use --token to provide an auth token")
            print("Set them via --endpoint, --user, --password, --token or environment variables")
            parser.print_help()
            sys.exit(1)

        # Create the client (loads/saves the token cache internally)
        client = DMEAPIClient(
            endpoint=endpoint,
            username=username,
            password=password,
            auth_token=auth_token,
            timeout=args.timeout,
            cache_token=args.cache_auth_token,
        )

        # Check whether the client already has a token; log in otherwise
        if not client.headers.get("X-Auth-Token"):
            print(f"Connecting to DME: {endpoint}")
            try:
                client.login()
            except Exception as e:
                print(f"Login failed: {e}")
                sys.exit(1)

        cli.client = client

        action_info = actions_info[action_key]
        func = action_info['func']

        # The three-level structure is displayed as "topic subtopic action"
        print(f"Executing: {args.topic} {args.subtopic} {args.action}")
        print(f"Description: {action_info.get('description', '')}")
        print("-" * 60)

        try:
            import inspect
            import builtins
            sig = inspect.signature(func)
            typed_params = {}

            # Parameter name mapping: CLI parameter name -> function parameter name
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
                # Try a direct match or a mapped match
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
                                print(f"Warning: parameter {param_name} cannot be converted to {param_type.__name__}")
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
                                print(f"Warning: parameter {param_name} requires JSON format")
                        elif param_type in (bool, builtins.bool):
                            if isinstance(param_value, str):
                                param_value = param_value.lower() in ('true', '1', 'yes')

                    typed_params[func_param_name] = param_value

            result = func(client, **typed_params)
            import json
            if result:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print("No data returned")
        except Exception as e:
            print(f"Execution failed: {e}")
            import traceback
            traceback.print_exc()
        return

    parser.print_help()


if __name__ == '__main__':
    main()
