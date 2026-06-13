#!/usr/bin/env python
"""读取 API 文档，获取 API 描述、方法、URI、参数、响应，以 markdown 格式输出"""

import os
import re
import sys
import glob
from pathlib import Path


def remove_spaces(text: str) -> str:
    """移除中英文、数字之间的多余空格"""
    # 中文与英文之间的空格
    text = re.sub(r'([\u4e00-\u9fa5])\s+([a-zA-Z])', r'\1\2', text)
    text = re.sub(r'([a-zA-Z])\s+([\u4e00-\u9fa5])', r'\1\2', text)

    # 中文与数字之间的空格
    text = re.sub(r'([\u4e00-\u9fa5])\s+(\d)', r'\1\2', text)
    text = re.sub(r'(\d)\s+([\u4e00-\u9fa5])', r'\1\2', text)

    return text


def normalize_path(path: str) -> str:
    """规范化路径，删除中英文之间的空格"""
    return remove_spaces(path)


def extract_text(html: str) -> str:
    """从 HTML 中提取纯文本"""
    # 移除 HTML 标签
    text = re.sub(r'<[^>]+>', ' ', html)
    # 移除列表标记
    text = re.sub(r'<li[^>]*>(.*?)</li>', r'\1\n', text, flags=re.DOTALL)
    # 清理空白字符
    text = ' '.join(text.split())
    return text.strip()


def extract_table_content(content: str) -> str:
    """提取完整的表格内容（支持嵌套表格）"""
    # 使用计数法匹配完整的<table>...</table>
    start = content.find('<table>')
    if start == -1:
        return ''

    depth = 0
    pos = start
    while pos < len(content):
        if content[pos:pos+7] == '<table>':
            depth += 1
            pos += 7
        elif content[pos:pos+8] == '</table>':
            depth -= 1
            if depth == 0:
                return content[start:pos+8]
            pos += 8
        else:
            pos += 1
    return content[start:]


def parse_param_table(table_html: str) -> list:
    """解析参数表格，提取参数详细信息"""
    params = []

    # 提取表格行
    row_pattern = r'<tr[^>]*>\s*(.*?)\s*</tr>'
    rows = re.findall(row_pattern, table_html, re.DOTALL)

    for row in rows:
        # 跳过表头
        if '<th' in row:
            continue

        # 提取单元格内容
        cells = re.findall(r'<td[^>]*>\s*(.*?)\s*</td>', row, re.DOTALL)
        if len(cells) >= 5:
            param = {
                'name': extract_text(cells[0]),
                'required': extract_text(cells[1]) == '是',
                'type': extract_text(cells[2]),
                'range': extract_text(cells[3]),
                'description': extract_text(cells[4])
            }
            params.append(param)

    return params


def extract_param_object_section(content: str, start_pos: int) -> tuple:
    """从指定位置提取参数引用对象定义（表格及其标题）

    Args:
        content: 文档内容
        start_pos: 起始位置

    Returns:
        (object_name, object_title, table_html, end_pos) 或 (None, None, None, -1)
    """
    # 匹配模式："XXX 对象包含如下属性：" 或 "XXX 包含如下属性："
    pattern = r'([a-zA-Z_][a-zA-Z0-9_]*)\s*对象？\s*包含如下属性：'
    match = re.search(pattern, content[start_pos:])
    if not match:
        return None, None, None, -1

    object_name = match.group(1)
    title_start = start_pos + match.start()
    title_end = start_pos + match.end()

    # 提取标题行（包括后面的空行）
    title_line_end = content.find('\n', title_end)
    if title_line_end == -1:
        return None, None, None, -1

    # 查找紧随其后的表格
    table_start = content.find('<table>', title_line_end)
    if table_start == -1:
        return None, None, None, -1

    # 提取完整的表格
    table_html = extract_table_content(content[table_start:])
    if not table_html:
        return None, None, None, -1

    end_pos = table_start + len(table_html)
    object_title = content[title_start:title_end].strip()

    return object_name, object_title, table_html, end_pos


def parse_param_objects(content: str) -> dict:
    """解析文档中所有的参数引用对象定义

    Args:
        content: 文档内容

    Returns:
        字典，键为对象名称，值为对象定义（包含标题和参数列表）
    """
    param_objects = {}

    # 循环查找所有对象定义：XXX 对象包含如下属性：
    # 注意：对象名和"对象"之间可能有空格，使用\s*来匹配
    pattern = r'([a-zA-Z_][a-zA-Z0-9_]*)\s*对象包含如下属性：'

    for match in re.finditer(pattern, content):
        object_name = match.group(1)
        object_title = match.group(0).strip()
        title_end = match.end()

        # 查找紧随其后的表格
        table_start = content.find('<table>', title_end)
        if table_start == -1:
            continue

        table_html = extract_table_content(content[table_start:])
        if not table_html:
            continue

        params = parse_param_table(table_html)
        param_objects[object_name] = {
            'title': object_title,
            'params': params
        }

    return param_objects


def parse_api_content(content: str, file_path: str) -> dict:
    """解析 API 文档内容，提取 API 信息"""
    api_info = {
        'title': '',
        'description': '',
        'method': '',
        'uri': '',
        'path_params': [],
        'query_params': [],
        'request_header_params': [],
        'request_body_params': [],
        'response_params': [],
        'response_nested_objects': {},  # 响应中引用的嵌套对象，键为对象名，值为参数列表
        'status_codes': [],
        'danger_level': '',
        'param_objects': {}  # 存储参数引用对象的定义
    }

    # 提取标题
    title_match = re.search(r'^#\s+(.+?)(?:<a|$)', content, re.MULTILINE)
    if title_match:
        api_info['title'] = title_match.group(1).strip()

    # 提取功能描述（排除 SLA 表格）
    func_match = re.search(r'##\s+功能(?:<[^>]*>)*\s*\n\n(.+?)(?=##|$)', content, re.DOTALL)
    if func_match:
        func_text = func_match.group(1).strip()
        # 移除表格内容
        func_text = re.sub(r'<table>.*?</table>', '', func_text, flags=re.DOTALL)
        # 移除 "服务SLA" 及其后的内容
        func_text = re.sub(r'__\s*服务SLA.*', '', func_text, flags=re.DOTALL)
        func_text = re.sub(r'<[^>]+>', ' ', func_text)
        api_info['description'] = ' '.join(func_text.split()).strip()

    # 提取调用方法（兼容标题后可能有 <a name="..."> 锚点标签的情况）
    method_match = re.search(r'##\s+调用方法(?:<[^>]*>)*\s*\n\n(\w+)', content)
    if method_match:
        api_info['method'] = method_match.group(1).upper()

    # 提取 URI
    uri_match = re.search(r'##\s+URI.*?\n\n(.+?)(?=##|$)', content, re.DOTALL)
    if uri_match:
        uri_text = uri_match.group(1)
        # 提取 URI 路径（支持转义的花括号 \{ 和 \}，以及下划线）
        # 匹配以 / 开头，包含字母、数字、斜杠、连字符、下划线、花括号及其转义形式的字符串
        uri_path_match = re.search(r'^(/[a-zA-Z0-9/_\-\{\}\\\\]+)', uri_text, re.MULTILINE)
        if uri_path_match:
            uri_path = uri_path_match.group(1).strip()
            # 移除转义字符：\{ -> {, \} -> }, \_ -> _
            uri_path = uri_path.replace('\\{', '{').replace('\\}', '}').replace('\\_', '_')
            api_info['uri'] = uri_path

    # 提取路径参数
    path_params_section = re.search(
        r'\*\*路径参数\*\*(.*?)(?=\*\*查询参数\*\*|\*\*请求\*\*|##\s+请求)',
        content, re.DOTALL
    )
    if path_params_section:
        path_content = path_params_section.group(1).strip()
        # 检查是否只有"无"（没有表格）
        if path_content != '无' and '<table>' in path_content:
            table_match = re.search(r'<table>', path_content)
            if table_match:
                table_html = extract_table_content(path_content[table_match.start():])
                if table_html:
                    api_info['path_params'] = parse_param_table(table_html)

    # 提取查询参数
    query_params_section = re.search(
        r'\*\*查询参数\*\*(.*?)(?=\*\*请求\*\*|##\s+请求)',
        content, re.DOTALL
    )
    if query_params_section:
        query_content = query_params_section.group(1).strip()
        # 检查是否只有"无"（没有表格）
        if query_content != '无' and '<table>' in query_content:
            table_match = re.search(r'<table>', query_content)
            if table_match:
                table_html = extract_table_content(query_content[table_match.start():])
                if table_html:
                    api_info['query_params'] = parse_param_table(table_html)

    # 提取请求部分（header 和 body 参数）
    request_section = re.search(
        r'##\s+请求\s*(.*?)\n\n##\s+响应',
        content, re.DOTALL
    )
    if request_section:
        request_content = request_section.group(1)

        # 提取 header 参数表格
        header_match = re.search(r'\*\*请求.*?header.*?参数\*\*', request_content, re.IGNORECASE)
        if header_match:
            header_table = extract_table_content(request_content[header_match.start():])
            if header_table:
                api_info['request_header_params'] = parse_param_table(header_table)

        # 提取 body 参数表格
        body_match = re.search(r'\*\*请求.*?body.*?参数\*\*', request_content, re.IGNORECASE)
        if body_match:
            body_table = extract_table_content(request_content[body_match.start():])
            if body_table:
                api_info['request_body_params'] = parse_param_table(body_table)

    # 提取响应参数
    response_section = re.search(
        r'##\s+响应\s*(.*?)\n\n##\s+状态码',
        content, re.DOTALL
    )
    if response_section:
        response_content = response_section.group(1)

        # 查找响应参数中的对象引用定义（嵌套对象）
        # 模式："XXX对象包含如下属性：" 出现在响应参数表格之后
        nested_objects = {}
        obj_pattern = r'([a-zA-Z_][a-zA-Z0-9_]*)\s*对象包含如下属性：'

        for match in re.finditer(obj_pattern, response_content):
            object_name = match.group(1)
            object_title = match.group(0).strip()
            title_end = match.end()

            # 查找紧随其后的表格
            table_start = response_content.find('<table>', title_end)
            if table_start == -1:
                continue

            table_html = extract_table_content(response_content[table_start:])
            if not table_html:
                continue

            params = parse_param_table(table_html)
            nested_objects[object_name] = {
                'title': object_title,
                'params': params
            }

        api_info['response_nested_objects'] = nested_objects

        # 提取第一层响应参数（只取第一个表格，即最外层的响应参数表格）
        # 跳过 "响应参数" 标题后的描述文字，找到第一个表格
        first_table_start = response_content.find('<table>')
        if first_table_start != -1:
            first_table_html = extract_table_content(response_content[first_table_start:])
            if first_table_html:
                api_info['response_params'] = parse_param_table(first_table_html)

    # 提取状态码
    status_codes = []
    status_match = re.search(r'##\s+状态码\s*\n.*?(?=##|$)', content, re.DOTALL)
    if status_match:
        status_section = status_match.group(0)
        status_pattern = r'<td[^>]*>\s*<p>(\d+)</p>.*?</td>\s*<td[^>]*>\s*<p>(.+?)</p>'
        codes = re.findall(status_pattern, status_section, re.DOTALL)
        for code, desc in codes:
            status_codes.append({
                'code': code.strip(),
                'description': extract_text(desc)
            })
    api_info['status_codes'] = status_codes

    # 提取操作危险级别
    danger_match = re.search(r'##\s+操作危险级别\s*\n\n(\w+)', content)
    if danger_match:
        api_info['danger_level'] = danger_match.group(1).strip()

    # 提取参数引用对象定义
    api_info['param_objects'] = parse_param_objects(content)

    return api_info


def format_api_markdown(api_info: dict, source_file: str) -> str:
    """将 API 信息格式化为 markdown 输出"""
    output = []

    output.append(f"**名称**")
    output.append(api_info['title'])
    output.append("")

    if api_info['description']:
        output.append("**描述**")
        output.append(api_info['description'])
        output.append("")

    output.append("**基本信息**")
    output.append(f"- **方法**: {api_info['method']}")
    output.append(f"- **URI**: {api_info['uri']}")
    # 不输出源文件路径
    if api_info['danger_level']:
        output.append(f"- **危险级别**: {api_info['danger_level']}")
    output.append("")

    # 路径参数
    if api_info['path_params']:
        output.append("**路径参数**")
        output.append("| 参数名 | 是否必选 | 类型 | 值域 | 说明 |")
        output.append("|--------|----------|------|------|------|")
        for param in api_info['path_params']:
            required = "是" if param['required'] else "否"
            output.append(
                f"| {param['name']} | {required} | {param['type']} | "
                f"{param['range']} | {param['description']} |"
            )
        output.append("")
    else:
        output.append("**路径参数**")
        output.append("无")
        output.append("")

    # 查询参数
    if api_info['query_params']:
        output.append("**查询参数**")
        output.append("| 参数名 | 是否必选 | 类型 | 值域 | 说明 |")
        output.append("|--------|----------|------|------|------|")
        for param in api_info['query_params']:
            required = "是" if param['required'] else "否"
            output.append(
                f"| {param['name']} | {required} | {param['type']} | "
                f"{param['range']} | {param['description']} |"
            )
        output.append("")
    else:
        output.append("**查询参数**")
        output.append("无")
        output.append("")

    # 请求 Body 参数
    if api_info['request_body_params']:
        output.append("**请求 Body 参数**")
        output.append("| 参数名 | 是否必选 | 类型 | 值域 | 说明 |")
        output.append("|--------|----------|------|------|------|")
        for param in api_info['request_body_params']:
            required = "是" if param['required'] else "否"
            output.append(
                f"| {param['name']} | {required} | {param['type']} | "
                f"{param['range']} | {param['description']} |"
            )
        output.append("")
    elif not api_info['request_header_params']:
        # 如果没有 header 和 body 参数，显示无
        output.append("**请求 Body 参数**")
        output.append("无")
        output.append("")

    # 响应字段
    if api_info['response_params']:
        output.append("**响应字段**")
        output.append("| 字段名 | 是否必选 | 类型 | 值域 | 说明 |")
        output.append("|--------|----------|------|------|------|")
        for param in api_info['response_params']:
            required = "是" if param['required'] else "否"
            output.append(
                f"| {param['name']} | {required} | {param['type']} | "
                f"{param['range']} | {param['description']} |"
            )
        output.append("")

        # 如果有嵌套对象（超过1个对象定义），输出"响应引用对象"
        # 第一个对象是第一层响应字段（已经在"响应字段"中展示了），
        # 其余的是嵌套对象
        if len(api_info['response_nested_objects']) > 1:
            # 获取所有嵌套对象（跳过第一个，即第一层响应对象）
            nested_items = list(api_info['response_nested_objects'].items())
            first_obj_name = nested_items[0][0]
            nested_objects = dict(nested_items[1:])
            output.append("**响应引用对象**")
            output.append("")
            for obj_name, obj_def in nested_objects.items():
                output.append(f"**{obj_def['title']}**")
                output.append("")
                if obj_def['params']:
                    output.append("| 参数名 | 是否必选 | 类型 | 值域 | 说明 |")
                    output.append("|--------|----------|------|------|------|")
                    for param in obj_def['params']:
                        required = "是" if param['required'] else "否"
                        output.append(
                            f"| {param['name']} | {required} | {param['type']} | "
                            f"{param['range']} | {param['description']} |"
                        )
                else:
                    output.append("无")
                output.append("")
    else:
        output.append("**响应字段**")
        output.append("无")
        output.append("")

    # 状态码
    if api_info['status_codes']:
        output.append("**状态码**")
        output.append("| 状态码 | 说明 |")
        output.append("|--------|------|")
        for code in api_info['status_codes']:
            output.append(f"| {code['code']} | {code['description']} |")
        output.append("")

    # 参数引用对象（排除响应中已处理的嵌套对象）
    # 如果响应有嵌套对象（>1），排除第一个对象（已在响应字段展示）和后续嵌套对象
    # 如果响应只有一个对象，排除它（已在响应字段展示）
    response_obj_names = set(api_info['response_nested_objects'].keys())
    # 只输出非响应引用的参数对象
    param_objects_to_show = {}
    for obj_name, obj_def in api_info['param_objects'].items():
        if obj_name not in response_obj_names:
            param_objects_to_show[obj_name] = obj_def

    if param_objects_to_show:
        output.append("**参数引用对象**")
        output.append("")
        for obj_name, obj_def in param_objects_to_show.items():
            output.append(f"**{obj_def['title']}**")
            output.append("")
            if obj_def['params']:
                output.append("| 参数名 | 是否必选 | 类型 | 值域 | 说明 |")
                output.append("|--------|----------|------|------|------|")
                for param in obj_def['params']:
                    required = "是" if param['required'] else "否"
                    output.append(
                        f"| {param['name']} | {required} | {param['type']} | "
                        f"{param['range']} | {param['description']} |"
                    )
            else:
                output.append("无")
            output.append("")

    return '\n'.join(output)


def is_topic_directory(file_path: str) -> bool:
    """检查文件是否是主题目录的索引文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 主题目录文件通常只包含链接列表，没有详细的 API 定义
    has_links = re.search(r'-\s+\*\*\[.*?\]\(.*?\)\*\*', content)
    has_api_details = re.search(r'##\s+调用方法', content)

    return bool(has_links and not has_api_details)


def get_linked_files(topic_file: str, base_dir: str) -> list:
    """从主题目录文件中提取链接指向的文件路径"""
    linked_files = []

    with open(topic_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取 markdown 链接
    link_pattern = r'\[.*?\]\(([^)]+)\)'
    links = re.findall(link_pattern, content)

    for link in links:
        # 处理相对路径
        if not link.startswith('http'):
            file_name = link
            full_path = os.path.join(os.path.dirname(topic_file), file_name)
            if os.path.exists(full_path):
                linked_files.append(full_path)

    return linked_files


def process_api_file(file_path: str) -> str:
    """处理单个 API 文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    api_info = parse_api_content(content, file_path)
    return format_api_markdown(api_info, file_path)


def process_topic_directory(topic_dir: str) -> str:
    """处理主题目录，输出 API 文件列表"""
    output = []

    topic_name = os.path.basename(topic_dir)
    output.append(f"# {topic_name} API 列表")
    output.append("")

    # 查找该主题目录下的所有 API 文件
    api_files = []
    for item in os.listdir(topic_dir):
        item_path = os.path.join(topic_dir, item)
        if os.path.isfile(item_path) and item.endswith('.md'):
            # 检查是否是 API 定义文件
            with open(item_path, 'r', encoding='utf-8') as f:
                content = f.read()
            if re.search(r'##\s+调用方法', content):
                api_files.append(item_path)

    if api_files:
        output.append("## API 文件列表")
        output.append("")
        for api_file in sorted(api_files):
            api_name = os.path.basename(api_file)
            output.append(f"- [{api_name}]({api_file})")
        output.append("")
    else:
        # 尝试从索引文件获取链接
        index_file = os.path.join(topic_dir, f"{topic_name}.md")
        if os.path.exists(index_file):
            linked_files = get_linked_files(index_file, topic_dir)
            if linked_files:
                output.append("## API 文件列表")
                output.append("")
                for api_file in sorted(linked_files):
                    api_name = os.path.basename(api_file)
                    output.append(f"- [{api_name}]({api_file})")
                output.append("")

    return '\n'.join(output)


def scan_reference_directory(ref_dir: str) -> str:
    """扫描参考目录，处理所有主题和 API 文件"""
    output = []

    if not os.path.exists(ref_dir):
        return f"错误：目录不存在 - {ref_dir}"

    output.append("# DME API 参考文档索引")
    output.append("")

    # 遍历目录中的所有文件
    for item in sorted(os.listdir(ref_dir)):
        item_path = os.path.join(ref_dir, item)

        if os.path.isdir(item_path):
            # 处理主题目录
            topic_output = process_topic_directory(item_path)
            output.append(topic_output)
        elif os.path.isfile(item_path) and item.endswith('.md'):
            # 检查是否是主题索引文件
            if is_topic_directory(item_path):
                # 处理主题索引文件
                linked_files = get_linked_files(item_path, ref_dir)
                output.append(f"## {item.replace('.md', '')}")
                output.append("")
                if linked_files:
                    for api_file in sorted(linked_files):
                        api_name = os.path.basename(api_file)
                        output.append(f"- [{api_name}]({api_file})")
                else:
                    output.append(f"- 无链接文件")
                output.append("")
            else:
                # 处理 API 定义文件
                api_output = process_api_file(item_path)
                output.append(api_output)

    return '\n'.join(output)


def main(file_path: str):
    """主函数

    Args:
        file_path: API 文档路径或参考目录路径
    """
    # 规范化路径，删除中英文之间的空格
    normalized_path = normalize_path(file_path)

    # 尝试使用通配符展开路径
    expanded_paths = glob.glob(normalized_path)

    if not expanded_paths:
        print(f"错误：路径不存在 - {normalized_path}")
        sys.exit(1)

    # 如果匹配到多个文件，逐个处理
    if len(expanded_paths) > 1:
        for path in expanded_paths:
            process_single_path(path)
    else:
        process_single_path(expanded_paths[0])


def process_single_path(path: str):
    """处理单个路径（文件或目录）"""
    if os.path.isdir(path):
        # 处理目录
        output = scan_reference_directory(path)
    elif os.path.isfile(path):
        # 检查是否是主题索引文件
        if is_topic_directory(path):
            output = process_topic_directory(os.path.dirname(path))
        else:
            # 处理单个 API 文件
            output = process_api_file(path)
    else:
        print(f"错误：未知的路径类型 - {path}")
        return

    print(output)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # 从命令行参数获取文件路径
        file_path = ' '.join(sys.argv[1:])
        main(file_path)
    else:
        # 默认扫描 reference/dme_api_reference 目录
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ref_dir = os.path.join(base_dir, 'reference', 'dme_api_reference')
        main(ref_dir)

