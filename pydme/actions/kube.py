"""
Kubernetes 相关操作
"""

import sys
import os

from pydme.client import DMEAPIClient


def cluster_list(client: DMEAPIClient, name: str = None,
                  id: str = None, version: str = None,
                  ip_address: str = None, status: str = None,
                  sync_status: list = None, platform_id: str = None,
                  platform_name: str = None, sort_key: str = None,
                  sort_dir: str = None,
                  page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询容器集群列表

    Args:
        client: DME API 客户端
        id: 集群 ID（可选）
        name: 集群名称（可选，支持模糊查询）
        version: 版本（可选）
        ip_address: 容器集群 IP 地址（可选，支持模糊查询）
        status: 状态（可选），可选值：abnormal（异常）, normal（正常）
        sync_status: 同步状态列表（可选），可选值：unsync（未同步）, sync（同步中）, normal（已同步）, failed（同步失败）, partial（部分已同步）
        platform_id: 所属容器平台的 ID（可选）
        platform_name: 所属容器平台名称（可选，支持模糊查询）
        sort_key: 排序字段（可选），可选值：node_number, total_cpu, total_memory, cpu_allocation_rate, memory_allocation_rate, name
        sort_dir: 排序方向（可选），可选值：asc（升序）, desc（降序）
        page_no: 分页查询的页码，1~2147483647，默认 1
        page_size: 每页数量，1~1000，默认 20

    Returns:
        {
            total: 集群总数 (integer),
            clusters_resp: 容器集群列表 (List<ClustersBaseResponse>)。参数格式如下：[{
                id: 集群ID (string),
                neId: 设备ID (string),
                name: 集群名称 (string),
                version: 版本 (string),
                ip_address: 容器集群IP地址 (string),
                status: 连接状态 (string),
                sync_status: 同步状态 (string),
                platform_id: 所属容器平台ID (string),
                platform_name: 所属容器平台名称 (string),
                node_number: 节点数量 (int32),
                total_cpu: CPU总量 (int64),
                total_memory: 内存总量 (int64),
                cpu_allocation_rate: CPU分配率 (number),
                memory_allocation_rate: 内存分配率 (number),
            }, ...],
        }
    """
    url = "/rest/dmecaasmgmt/v1/clusters/query-list"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if id is not None:
        payload['id'] = id
    if name is not None:
        payload['name'] = name
    if version is not None:
        payload['version'] = version
    if ip_address is not None:
        payload['ip_address'] = ip_address
    if status is not None:
        payload['status'] = status
    if sync_status is not None:
        payload['sync_status'] = sync_status
    if platform_id is not None:
        payload['platform_id'] = platform_id
    if platform_name is not None:
        payload['platform_name'] = platform_name
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def node_list(client: DMEAPIClient, cluster_id: str = None,
               name: str = None, id: str = None,
               pool_id: str = None, ip_address: str = None,
               ready_status: str = None, scheduling_status: str = None,
               pool_name: str = None, sort_key: str = None,
               sort_dir: str = None,
               page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询容器节点列表

    Args:
        client: DME API 客户端
        id: 节点 ID（可选）
        name: 节点名称（可选，支持模糊查询）
        cluster_id: 容器集群 ID（可选）
        pool_id: 容器节点所属节点池 ID（可选）
        ip_address: 容器节点 IP 地址（可选，支持模糊查询）
        ready_status: 就绪状态（可选），可选值：ready（就绪）, not-ready（未就绪）
        scheduling_status: 调度状态（可选），可选值：schedule（可调度）, not-schedule（不可调度）
        pool_name: 所属节点池名称（可选，支持模糊查询）
        sort_key: 排序字段（可选），可选值：pod_count, create_time, total_cpu, total_memory, cpu_allocation_rate, memory_allocation_rate
        sort_dir: 排序方向（可选），可选值：asc（升序）, desc（降序）
        page_no: 分页查询的页码，1~2147483647，默认 1
        page_size: 每页数量，1~1000，默认 20

    Returns:
        {
            total: 节点数量 (int32),
            nodes_resp: 容器节点列表 (List<NodesBaseResponse>)。参数格式如下：[{
                id: 节点ID (string),
                name: 节点名称 (string),
                ip_address: 容器节点IP地址 (string),
                ready_status: 就绪状态 (string),
                scheduling_status: 调度状态 (string),
                pool_name: 所属节点池名称 (string),
                pool_id: 节点池ID (string),
                pod_count: 容器组数量 (int32),
                total_cpu: CPU总量 (int64),
                total_memory: 内存总量 (int64),
                cpu_allocation_rate: CPU分配率 (number),
                memory_allocation_rate: 内存分配率 (number),
                create_time: 创建时间戳 (int64),
            }, ...],
        }
    """
    url = "/rest/dmecaasmgmt/v1/nodes/query-list"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if id is not None:
        payload['id'] = id
    if name is not None:
        payload['name'] = name
    if cluster_id is not None:
        payload['cluster_id'] = cluster_id
    if pool_id is not None:
        payload['pool_id'] = pool_id
    if ip_address is not None:
        payload['ip_address'] = ip_address
    if ready_status is not None:
        payload['ready_status'] = ready_status
    if scheduling_status is not None:
        payload['scheduling_status'] = scheduling_status
    if pool_name is not None:
        payload['pool_name'] = pool_name
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def pod_list(client: DMEAPIClient, cluster_id: str = None,
              namespace_name: str = None, name: str = None,
              id: str = None, workload_id: str = None,
              node_id: str = None, cluster_name: str = None,
              platform_id: str = None, platform_name: str = None,
              namespace_id: str = None, ip_address: str = None,
              node_name: str = None, running_status: list = None,
              controller: str = None, sort_key: str = None,
              sort_dir: str = None,
              page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询容器组列表

    查询容器组（Pod）列表，支持按集群 ID、命名空间和名称过滤。

    Args:
        client: DME API 客户端
        id: 容器组 ID（可选）
        name: 容器组名称（可选，支持模糊查询）
        workload_id: 所属工作负载 ID（可选）
        node_id: 所属容器节点 ID（可选）
        namespace_name: 容器命名空间（可选）
        cluster_name: 所属集群名称（可选，支持模糊查询）
        cluster_id: 容器集群 ID（可选）
        platform_id: 所属容器平台的 ID（可选）
        platform_name: 所属容器平台的名称（可选）
        namespace_id: 所属命名空间唯一标识 ID（可选）
        ip_address: 容器组 IP 地址（可选，支持模糊查询）
        node_name: 所在节点名称（可选）
        running_status: 运行状态列表（可选），可选值：running（运行中）, pending（悬决）, succeeded（成功）, failed（失败）, unknown（未知）
        controller: 控制者（可选）
        sort_key: 排序字段（可选），可选值：reboot_time, create_time
        sort_dir: 排序方向（可选），可选值：asc（升序）, desc（降序）
        page_no: 分页查询的页码，1~2147483647，默认 1
        page_size: 每页数量，1~1000，默认 20

    Returns:
        {
            total: 容器组数量 (int32),
            pods_resp: 容器组列表 (List<PodsBaseResponse>)。参数格式如下：[{
                id: 容器组ID (string),
                name: 容器组名称 (string),
                cluster_id: 所属集群ID (string),
                cluster_name: 所属集群名称 (string),
                ip_address: 容器组IP地址 (string),
                namespace_id: 命名空间ID (string),
                namespace_name: 命名空间名称 (string),
                node_name: 所在节点名称 (string),
                running_status: 运行状态 (string),
                controller: 控制者 (string),
            }, ...],
        }
    """
    url = "/rest/dmecaasmgmt/v1/pods/query-list"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if id is not None:
        payload['id'] = id
    if name is not None:
        payload['name'] = name
    if workload_id is not None:
        payload['workload_id'] = workload_id
    if node_id is not None:
        payload['node_id'] = node_id
    if namespace_name is not None:
        payload['namespace_name'] = namespace_name
    if cluster_name is not None:
        payload['cluster_name'] = cluster_name
    if cluster_id is not None:
        payload['cluster_id'] = cluster_id
    if platform_id is not None:
        payload['platform_id'] = platform_id
    if platform_name is not None:
        payload['platform_name'] = platform_name
    if namespace_id is not None:
        payload['namespace_id'] = namespace_id
    if ip_address is not None:
        payload['ip_address'] = ip_address
    if node_name is not None:
        payload['node_name'] = node_name
    if running_status is not None:
        payload['running_status'] = running_status
    if controller is not None:
        payload['controller'] = controller
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def namespace_list(client: DMEAPIClient, cluster_id: str = None,
                    name: str = None, status: list = None,
                    sort_key: str = None, sort_dir: str = None,
                    page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询容器命名空间列表

    Args:
        client: DME API 客户端
        name: 命名空间名称（可选，支持模糊查询）
        cluster_id: 所属容器集群 ID（可选）
        status: 命名空间状态列表（可选），可选值：active（激活）, terminating（终止）, unknown（未知）
        sort_key: 排序字段（可选），可选值：create_time
        sort_dir: 排序方向（可选），可选值：asc（升序）, desc（降序）
        page_no: 分页查询的页码，1~2147483647，默认 1
        page_size: 每页数量，1~1000，默认 20

    Returns:
        {
            total: 命名空间数量 (int32),
            namespaces_resp: 容器命名空间列表 (List<NamespacesBaseResponse>)。参数格式如下：[{
                id: 命名空间ID (string),
                name: 命名空间名称 (string),
                status: 状态 (string),
                create_time: 创建时间戳 (int64),
            }, ...],
        }
    """
    url = "/rest/dmecaasmgmt/v1/namespaces/query-list"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if name is not None:
        payload['name'] = name
    if cluster_id is not None:
        payload['cluster_id'] = cluster_id
    if status is not None:
        payload['status'] = status
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def pvc_list(client: DMEAPIClient, cluster_id: str = None,
              namespace_name: str = None, name: str = None,
              cluster_name: str = None, platform_id: str = None,
              platform_name: str = None, namespace_id: str = None,
              status: list = None, access_mode: list = None,
              storage_class_name: str = None, sort_key: str = None,
              sort_dir: str = None,
              page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询容器持久卷声明列表

    Args:
        client: DME API 客户端
        name: 持久卷声明名称（可选，支持模糊查询）
        namespace_name: 所属命名空间名称（可选，支持模糊查询）
        cluster_name: 所属集群名称（可选，支持模糊查询）
        cluster_id: 所属集群 ID（可选）
        platform_id: 所属容器平台的 ID（可选）
        platform_name: 所属容器平台名称（可选，支持模糊查询）
        namespace_id: 所属命名空间唯一标识 ID（可选）
        status: 状态列表（可选），可选值：pending（悬决）, bound（边界）, lost（丢失）
        access_mode: 访问模式列表（可选），可选值：read_write_many, read_write_once, read_only_many, read_write_once_pod
        storage_class_name: 存储类名称（可选，支持模糊查询）
        sort_key: 排序字段（可选），可选值：capacity, create_time
        sort_dir: 排序方向（可选），可选值：asc（升序）, desc（降序）
        page_no: 分页查询的页码，1~2147483647，默认 1
        page_size: 每页数量，1~1000，默认 20

    Returns:
        {
            total: 持久卷声明数量 (int32),
            pvcs_resp: 容器持久卷声明列表 (List<PvcsBaseResponse>)。参数格式如下：[{
                id: 持久卷声明ID (string),
                name: 持久卷声明名称 (string),
                cluster_id: 所属集群ID (string),
                cluster_name: 所属集群名称 (string),
                namespace_id: 所属命名空间ID (string),
                namespace_name: 所属命名空间名称 (string),
                status: 状态 (string),
                pv_name: 持久卷名称 (string),
                access_mode: 访问模式 (string),
                storage_class_name: 存储类名称 (string),
                capacity: 容量GB (number),
                create_time: 创建时间戳 (int64),
            }, ...],
        }
    """
    url = "/rest/dmecaasmgmt/v1/pvcs/query-list"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if name is not None:
        payload['name'] = name
    if namespace_name is not None:
        payload['namespace_name'] = namespace_name
    if cluster_name is not None:
        payload['cluster_name'] = cluster_name
    if cluster_id is not None:
        payload['cluster_id'] = cluster_id
    if platform_id is not None:
        payload['platform_id'] = platform_id
    if platform_name is not None:
        payload['platform_name'] = platform_name
    if namespace_id is not None:
        payload['namespace_id'] = namespace_id
    if status is not None:
        payload['status'] = status
    if access_mode is not None:
        payload['access_mode'] = access_mode
    if storage_class_name is not None:
        payload['storage_class_name'] = storage_class_name
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def pv_list(client: DMEAPIClient, cluster_id: str = None,
             name: str = None, id: str = None,
             cluster_name: str = None, platform_id: str = None,
             platform_name: str = None, status: list = None,
             access_mode: list = None, storage_class_name: str = None,
             sort_key: str = None, sort_dir: str = None,
             page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询容器持久卷列表

    查询容器持久卷（PV）列表。

    Args:
        client: DME API 客户端
        id: 持久卷 ID（可选）
        name: 持久卷名称（可选，支持模糊查询）
        cluster_name: 所属集群名称（可选，支持模糊查询）
        cluster_id: 所属集群 ID（可选）
        platform_id: 所属容器平台的 ID（可选）
        platform_name: 所属容器平台的名称（可选，支持模糊查询）
        status: 状态列表（可选），可选值：available（空闲）, pending（悬决）, bound（已绑定）, released（释放）, failed（失败）
        access_mode: 访问模式列表（可选），可选值：read_write_many, read_write_once, read_only_many, read_write_once_pod
        storage_class_name: 存储类名称（可选，支持模糊查询）
        sort_key: 排序字段（可选），可选值：capacity, create_time
        sort_dir: 排序方向（可选），可选值：asc（升序）, desc（降序）
        page_no: 分页查询的页码，1~2147483647，默认 1
        page_size: 每页数量，1~1000，默认 20

    Returns:
        {
            total: 持久卷数量 (int32),
            pvs_resp: 容器持久卷列表 (List<PvsBaseResponse>)。参数格式如下：[{
                id: 持久卷ID (string),
                name: 持久卷名称 (string),
                cluster_id: 所属集群ID (string),
                cluster_name: 所属集群名称 (string),
                status: 状态 (string),
                pvc_name: 持久卷声明名称 (string),
                access_mode: 访问模式 (string),
                storage_class_name: 存储类名称 (string),
                capacity: 容量GB (number),
                create_time: 创建时间戳 (int64),
            }, ...],
        }
    """
    url = "/rest/dmecaasmgmt/v1/pvs/query-list"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if id is not None:
        payload['id'] = id
    if name is not None:
        payload['name'] = name
    if cluster_name is not None:
        payload['cluster_name'] = cluster_name
    if cluster_id is not None:
        payload['cluster_id'] = cluster_id
    if platform_id is not None:
        payload['platform_id'] = platform_id
    if platform_name is not None:
        payload['platform_name'] = platform_name
    if status is not None:
        payload['status'] = status
    if access_mode is not None:
        payload['access_mode'] = access_mode
    if storage_class_name is not None:
        payload['storage_class_name'] = storage_class_name
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


# 动作列表，用于 CLI 帮助
ACTIONS = {
    # 集群管理
    'cluster_list': {
        'func': cluster_list,
        'description': '查询容器集群列表',
        'params': ['id', 'name', 'version', 'ip_address', 'status',
                   'sync_status', 'platform_id', 'platform_name',
                   'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'cluster'
    },
    # 节点管理
    'node_list': {
        'func': node_list,
        'description': '查询容器节点列表',
        'params': ['id', 'name', 'cluster_id', 'pool_id', 'ip_address',
                   'ready_status', 'scheduling_status', 'pool_name',
                   'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'node'
    },
    # 容器组管理
    'pod_list': {
        'func': pod_list,
        'description': '查询容器组列表',
        'params': ['id', 'name', 'workload_id', 'node_id', 'namespace_name',
                   'cluster_name', 'cluster_id', 'platform_id', 'platform_name',
                   'namespace_id', 'ip_address', 'node_name', 'running_status',
                   'controller', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'pod'
    },
    # 命名空间管理
    'namespace_list': {
        'func': namespace_list,
        'description': '查询容器命名空间列表',
        'params': ['name', 'cluster_id', 'status', 'sort_key', 'sort_dir',
                   'page_no', 'page_size'],
        'subtopic': 'namespace'
    },
    # 持久卷声明管理
    'pvc_list': {
        'func': pvc_list,
        'description': '查询容器持久卷声明列表',
        'params': ['name', 'namespace_name', 'cluster_name', 'cluster_id',
                   'platform_id', 'platform_name', 'namespace_id', 'status',
                   'access_mode', 'storage_class_name', 'sort_key', 'sort_dir',
                   'page_no', 'page_size'],
        'subtopic': 'pvc'
    },
    # 持久卷管理
    'pv_list': {
        'func': pv_list,
        'description': '查询容器持久卷列表',
        'params': ['id', 'name', 'cluster_name', 'cluster_id', 'platform_id',
                   'platform_name', 'status', 'access_mode', 'storage_class_name',
                   'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'pv'
    },
}
