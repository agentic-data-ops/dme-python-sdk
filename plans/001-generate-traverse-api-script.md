# 生成脚本遍历api文档

## 任务目标：

生成python文件utils/traverse_api_reference.py
用于遍历reference/dme-api-reference目录中的文件，获取API层次结构和每个API的定义
输出到reference/dme-api-reference.md

## 生成步骤

1. 读取"目录.md"，生成 “# 目录” 章节，按章节缩进的层次结构，将链接更新为Markdown内部章节引用（根据缩进设置章节标题格式），输出内容
2. 按章节层次结构，输出章节标题，如“# 存储管理”、“## 存储设备”、“### 添加存储设备”
3. 调用utils/read_api_reference.py中的main函数，读取具体API文档，如“添加存储设备.md”，输出具体的API定义，更新到对应章节

注意事项：
1. 排除过期接口
2. 仅目录中最底层级的文件才需要调用utils/read_api_reference.py
3. 排除无URI定义的文件（非API接口定义）

