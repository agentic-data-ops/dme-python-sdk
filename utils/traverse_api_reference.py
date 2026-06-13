#!/usr/bin/env python
"""遍历 dme-api-reference 目录，生成汇总的 API 参考文档"""

import os
import re
import sys
import glob
from pathlib import Path

# 将项目根目录加入 sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from utils.read_api_reference import main as read_api_main, process_api_file

# 过期的关键词列表
EXPIRED_KEYWORDS = [
    '已过期',
    '不再维护',
    '请避免使用',
    '（该接口已过期',
    '(已过期)',
    '过期接口',
]

# 跳过层级深度低于此层级的中间文件
# 目录中的叶节点（最深层级的.md文件）才会被处理
MIN_DEPTH = 1  # 目录.md 中最深层级是至少 3 级缩进，但文件系统深度不定


def is_expired_file(file_path: str) -> bool:
    """判断文件是否标记为过期接口"""
    file_name = os.path.basename(file_path)
    # 先通过文件名判断
    for kw in EXPIRED_KEYWORDS:
        if kw in file_name:
            return True
    return False


def get_link_depth(line: str) -> int:
    """计算目录行中的缩进深度（以 - 前面的空格数计算）"""
    # 计算行首空格数，每 4 个空格为一级
    stripped = line.lstrip()
    indent = len(line) - len(stripped)
    # 每个缩进级别对应 4 个空格
    return indent // 4


def parse_toc(content: str, toc_dir: str) -> list:
    """解析目录.md，提取 API 层级结构

    Args:
        content: 目录.md 内容
        toc_dir: 目录.md 所在目录

    Returns:
        章节层级列表：[(depth, title, file_path_or_None), ...]
        - depth: 缩进层级（0 为根）
        - title: 章节标题
        - file_path: 对应的 .md 文件路径，如果是中间节点则为 None
    """
    sections = []
    lines = content.split('\n')

    for line in lines:
        # 匹配 markdown 链接行：-   [标题](文件.md)
        match = re.match(r'^(\s*)-\s+\*?\*?\[([^\]]+)\]\(([^)]+\.md)\)', line)
        if match:
            indent_str = match.group(1)
            title = match.group(2).strip()
            link = match.group(3).strip()

            # 计算缩进深度
            depth = len(indent_str) // 4  # 每 4 个空格算一级

            # 跳过根标题行
            if depth == 0 and '#' in title:
                continue

            # 构建完整文件路径
            full_path = os.path.normpath(os.path.join(toc_dir, link))

            sections.append({
                'depth': depth,
                'title': title,
                'file_path': full_path if os.path.exists(full_path) else None,
                'is_leaf': False,  # 稍后判断
            })

    # 判断叶节点：没有子节点的节点才是叶节点
    for i, section in enumerate(sections):
        current_depth = section['depth']
        has_child = False
        for j in range(i + 1, len(sections)):
            if sections[j]['depth'] > current_depth:
                has_child = True
            elif sections[j]['depth'] <= current_depth:
                break
        section['is_leaf'] = not has_child

    return sections


def get_markdown_heading(level: int) -> str:
    """根据层级返回 Markdown 标题标记"""
    # level 0 -> "#", level 1 -> "##", level 2 -> "###"
    actual_level = min(level + 1, 6)  # Markdown 最多 6 级标题
    return '#' * actual_level


def generate_reference_doc(sections: list, toc_dir: str) -> str:
    """生成汇总的 API 参考文档

    Args:
        sections: 解析后的章节层级列表
        toc_dir: 目录所在目录

    Returns:
        汇总的 Markdown 文档内容
    """
    output_lines = []

    # 记录已处理的 API 文件，避免重复处理
    processed_files = set()
    expired_count = 0
    no_uri_count = 0
    processed_count = 0
    skipped_leaf = []  # 记录跳过的文件

    for section in sections:
        depth = section['depth']
        title = section['title']
        file_path = section['file_path']
        is_leaf = section['is_leaf']

        # 输出章节标题
        heading = get_markdown_heading(depth)
        output_lines.append(f'{heading} {title}')
        output_lines.append('')

        if file_path and is_leaf:
            # 检查文件是否已处理
            if file_path in processed_files:
                continue

            # 检查是否过期接口
            if is_expired_file(file_path):
                output_lines.append(f'> ⚠️ 该接口已过期，不再维护，已跳过。')
                output_lines.append('')
                expired_count += 1
                skipped_leaf.append(f'{title} - 过期接口')
                continue

            # 检查文件是否有 URI 定义（是否是 API 接口文件）
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                has_uri = bool(re.search(r'##\s+URI', content))
                has_method = bool(re.search(r'##\s+调用方法', content))
            except Exception:
                has_uri = False
                has_method = False

            if not has_uri and not has_method:
                output_lines.append(f'> 该文件无 URI 定义，非 API 接口定义，已跳过。')
                output_lines.append('')
                no_uri_count += 1
                skipped_leaf.append(f'{title} - 非 API 接口')
                continue

            # 处理 API 文件
            try:
                api_md = process_api_file(file_path)
                output_lines.append(api_md)
                output_lines.append('')
                processed_files.add(file_path)
                processed_count += 1
            except Exception as e:
                output_lines.append(f'> 处理失败: {e}')
                output_lines.append('')

    # 添加统计信息
    output_lines.append('---')
    output_lines.append('')
    output_lines.append('## 统计信息')
    output_lines.append('')
    output_lines.append(f'- 总 API 数: {processed_count}')
    output_lines.append(f'- 跳过过期接口: {expired_count}')
    output_lines.append(f'- 跳过非 API 接口: {no_uri_count}')

    return '\n'.join(output_lines)


def main():
    """主函数"""
    # 确定目录路径
    base_dir = BASE_DIR
    ref_dir = os.path.join(base_dir, 'reference', 'dme-api-reference')
    toc_file = os.path.join(ref_dir, '目录.md')

    if not os.path.exists(toc_file):
        print(f'错误：目录.md 不存在 - {toc_file}')
        sys.exit(1)

    print(f'📖 读取目录文件: {toc_file}')

    # 读取目录.md
    with open(toc_file, 'r', encoding='utf-8') as f:
        toc_content = f.read()

    # 解析目录
    sections = parse_toc(toc_content, ref_dir)
    print(f'📋 解析出 {len(sections)} 个章节/文件')

    leaf_count = sum(1 for s in sections if s['is_leaf'])
    print(f'🍃 叶节点(API文件): {leaf_count}')

    # 生成汇总文档
    output = generate_reference_doc(sections, ref_dir)

    # 写入输出文件
    output_file = os.path.join(base_dir, 'reference', 'dme-api-reference.md')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f'✅ 汇总文档已生成: {output_file}')


if __name__ == '__main__':
    main()

