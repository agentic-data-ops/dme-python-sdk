with open('README.md') as f:
    content = f.read()

fixes = {
    # Project structure
    'Python 包': 'Python package',
    'DME API 客户端': 'DME API client',
    '命令行接口': 'CLI entry point',
    '动作模块（每个主题一个文件）': 'Action modules (one file per topic)',
    'AIOps 智能运维': 'AIOps (alerts/performance/health/topology)',
    '数据备份管理': 'Backup management',
    'FC 光纤交换机': 'FC switch management',
    '全局文件系统': 'Global file system',
    '三方系统集成(CMDB)': 'Third-party integration (CMDB)',
    'IP 交换机': 'IP switch management',
    'Kubernetes 容器': 'Kubernetes management',
    'NAS 文件存储': 'NAS file storage',
    '数据保护': 'Data protection',
    'SAN 块存储': 'SAN block storage',
    '服务器管理': 'Server management',
    '租户自助服务': 'Tenant self-service',
    '虚拟化服务': 'Virtualization services',
    '工作流管理': 'Workflow management',
    'Storage Device Management': 'Storage device management',
    'System Management': 'System management',
    
    # Sections
    '### 环境配置\n': '### Environment Configuration\n',
    '使用命令行': 'Using the CLI',
    '使用动作模块': 'Using Action Modules',
    '使用 Python 客户端': 'Using the Python Client',
    
    # Installation
    '从默认分支安装（稳定版，中文注释）：': 'Install from default branch (stable, Chinese comments):',
    '从开发分支安装（最新功能，中文注释）：': 'Install from dev branch (latest features, Chinese comments):',
    '从英文分支安装（稳定版，英文注释）：': 'Install from English branch (stable, English comments):',
    '或以可编辑模式安装用于开发：': 'Or install in editable mode for development:',
    
    # Env
    '在 DME 上创建"第三方系统接入"用户并添加"北向用户组"角色': 'Create a "third-party system access" user in DME with "northbound user group" role',
    '或使用认证令牌代替用户名/密码：': 'Or use an auth token instead of username/password:',
    
    # CLI
    '安装后，`pydme` 命令全局可用：': 'After installation, the `pydme` command is available globally:',
    '查看所有可用主题和动作': 'View all available topics and actions',
    '查看指定主题的帮助': 'View help for a specific topic',
    '查看指定子主题的帮助': 'View help for a specific subtopic',
    '查看指定动作的帮助': 'View help for a specific action',
    '执行动作': 'Execute an action',
    '执行子主题动作': 'Execute a subtopic action',
    'DME 连接信息也可通过命令行参数传递：': 'DME connection info can also be passed via CLI arguments:',

    # Topic descriptions
    '数据保护（保护组/双活/复制/快照/克隆）': 'Protection (groups/active-active/replication/snapshots/clones)',
    'SAN 块存储（LUN/映射视图/主机/端口组）': 'SAN block storage (LUNs/mapping views/hosts/port groups)',
    'NAS 文件存储（NFS/CIFS/DPC/文件系统/配额）': 'NAS file storage (NFS/CIFS/DPC/filesystems/quotas)',
    'Storage Device Management（租户/磁盘/池/端口/控制器）': 'Storage device management (tenants/disks/pools/ports/controllers)',
    'System Management（用户/标签/任务/Region/证书）': 'System management (users/tags/tasks/regions/certificates)',
    'AIOps 智能运维（告警/性能/健康度/拓扑）': 'AIOps (alerts/performance/health/topology)',
    'FC 光纤交换机管理': 'FC switch management',
    '虚拟化服务（VM/集群/数据存储）': 'Virtualization (VMs/clusters/datastores)',
    '服务器管理（CPU/内存/RAID）': 'Server management (CPU/memory/RAID)',
    '租户自助服务（服务化LUN/业务群组）': 'Tenant self-service (service LUNs/project groups)',
    'IP 交换机管理': 'IP switch management',
    'Kubernetes 容器管理': 'Kubernetes management',
    '三方系统集成（CMDB）': 'Third-party integration (CMDB)',
    
    # Action modules text
    '每个动作模块提供主题相关的函数，这些函数以已认证的 `DMEAPIClient` 实例作为第一个参数。': 'Each action module provides topic-specific functions. These functions take an authenticated `DMEAPIClient` instance as the first parameter.',
    '导入所有模块': 'Import all modules',
    '导入指定模块': 'Import specific modules',
    '导入单个函数': 'Import a single function',
    '所有动作函数遵循相同模式：': 'All action functions follow the same pattern:',
    '第一个参数': 'First parameter',
    '已认证的 `DMEAPIClient` 实例': 'An authenticated `DMEAPIClient` instance',
    '关键字参数': 'Keyword arguments',
    '动作特定参数（详见函数文档）': 'Action-specific parameters (see function documentation)',
    '返回值': 'Return value',
    '包含 API 响应的 `dict`': 'A `dict` containing the API response',
    '通过 CLI 浏览可用动作：': 'Browse available actions via CLI:',
    '列出所有主题': 'List all topics',
    '查看主题下的动作': 'View actions under a topic',

    # Table header
    '模块 | 示例函数 | 描述': 'Module | Example function | Description',
    
    # Module table descriptions
    'AIOps 智能运维（告警/性能/健康度/拓扑）': 'AIOps (alerts/performance/health/topology)',
    'FC 光纤交换机管理': 'FC switch management',
    '全局文件系统': 'Global file system (GFS)',
    'IP 交换机管理': 'IP switch management',
    'Kubernetes 容器管理': 'Kubernetes management',
    'NAS 相关操作（NFS/CIFS/文件系统/配额）': 'NAS operations (NFS/CIFS/filesystems/quotas)',
    '保护（快照/双活/远程复制）': 'Protection (snapshots/active-active/replication)',
    'SAN 相关操作（LUN/映射视图/主机）': 'SAN operations (LUNs/mapping views/hosts)',
    '租户自助服务（服务化 LUN/业务群组）': 'Tenant self-service (service LUNs/project groups)',
    '服务器管理（CPU/内存/RAID）': 'Server management (CPU/memory/RAID)',
    'Storage Device Management（磁盘/端口/控制器/QoS）': 'Storage device management (disks/ports/controllers/QoS)',
    'System Management（用户/标签/任务/证书）': 'System management (users/tags/tasks/certificates)',
    '虚拟化服务（VM/集群/数据存储）': 'Virtualization (VMs/clusters/datastores)',
    '工作流管理': 'Workflow management',
    '数据备份管理': 'Backup management',
    '三方系统集成（CMDB）': 'Third-party integration (CMDB)',
    
    # Python client
    'Initialization客户端': 'Initializing the Client',
    '查询并分类存储设备': 'Query and classify storage devices',
    '查询存储设备详情': 'Query storage device details',
    '调用存储设备原生 API': 'Call storage device native API',
    '获取指定存储设备的令牌认证客户端': 'Get a token-authenticated client for a specific storage device',
}

for old, new in fixes.items():
    content = content.replace(old, new)

# Manual fix for the table header
content = content.replace('| Module | 示例函数 | 描述 |', '| Module | Example function | Description |')

with open('README.md', 'w') as f:
    f.write(content)
print('Done')
