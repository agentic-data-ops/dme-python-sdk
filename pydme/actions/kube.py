"""
Kubernetes operations
"""

import sys
import os

from pydme.client import DMEAPIClient


def cluster_list(client: DMEAPIClient, name: str = None,
                  page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询Container cluster list
    
    Args:
        client: DME API client
        name: 容器集群名称（Optional，supports fuzzy search）
        page_no: 分页查询的Start page，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        {
            total: 集群Total count (integer),
            clusters: Container cluster list。参数格式如下：[{
                id: 集群ID (string),
                name: 集群名称 (string),
                status: 状态 (string),
            }, ...],
        }
    """
    url = "/rest/dmecaasmgmt/v1/clusters/query-list"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if name is not None:
        payload['name'] = name
    
    response = client.post(url, body=payload)
    return response


def node_list(client: DMEAPIClient, cluster_id: str = None,
               name: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询Container node list
    
    Args:
        client: DME API client
        cluster_id: 容器集群 ID（Optional）
        name: 容器节点名称（Optional，supports fuzzy search）
        page_no: 分页查询的Start page，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        {
            nodes: Container node list。参数格式如下：[{
                id: 节点ID (string),
                name: 节点名称 (string),
                status: 状态 (string),
            }, ...],
        }
    """
    url = "/rest/dmecaasmgmt/v1/nodes/query-list"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if cluster_id is not None:
        payload['cluster_id'] = cluster_id
    if name is not None:
        payload['name'] = name
    
    response = client.post(url, body=payload)
    return response


def pod_list(client: DMEAPIClient, cluster_id: str = None,
              namespace: str = None, name: str = None,
              page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询Pod list
    
    查询容器组（Pod）列表，支持按集群 ID、命名空间和名称过滤。
    
    Args:
        client: DME API client
        cluster_id: 容器集群 ID（Optional）
        namespace: 容器命名空间（Optional）
        name: 容器组名称（Optional，supports fuzzy search）
        page_no: 分页查询的Start page，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        {
            pods: Pod list。参数格式如下：[{
                name: 容器组名称 (string),
                status: 状态 (string),
                node: 所在节点 (string),
            }, ...],
        }
    """
    url = "/rest/dmecaasmgmt/v1/pods/query-list"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if cluster_id is not None:
        payload['cluster_id'] = cluster_id
    if namespace is not None:
        payload['namespace'] = namespace
    if name is not None:
        payload['name'] = name
    
    response = client.post(url, body=payload)
    return response


def namespace_list(client: DMEAPIClient, cluster_id: str = None,
                    name: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询容器命名空间列表
    
    Args:
        client: DME API client
        cluster_id: 容器集群 ID（Optional）
        name: Namespace name（Optional，supports fuzzy search）
        page_no: 分页查询的Start page，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        {
            namespaces: 命名空间列表 (List<string>),
        }
    """
    url = "/rest/dmecaasmgmt/v1/namespaces/query-list"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if cluster_id is not None:
        payload['cluster_id'] = cluster_id
    if name is not None:
        payload['name'] = name
    
    response = client.post(url, body=payload)
    return response


def pvc_list(client: DMEAPIClient, cluster_id: str = None,
              namespace: str = None, name: str = None,
              page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询容器PVC list
    
    Args:
        client: DME API client
        cluster_id: 容器集群 ID（Optional）
        namespace: 容器命名空间（Optional）
        name: 持久卷声明名称（Optional，supports fuzzy search）
        page_no: 分页查询的Start page，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        {
            pvcs: PVC list。参数格式如下：[{
                name: PVC名称 (string),
                status: 状态 (string),
                capacity: 容量 (string),
            }, ...],
        }
    """
    url = "/rest/dmecaasmgmt/v1/pvcs/query-list"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if cluster_id is not None:
        payload['cluster_id'] = cluster_id
    if namespace is not None:
        payload['namespace'] = namespace
    if name is not None:
        payload['name'] = name
    
    response = client.post(url, body=payload)
    return response


def pv_list(client: DMEAPIClient, cluster_id: str = None,
             name: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询容器PV list
    
    查询容器持久卷（PV）列表，支持按集群 ID 和名称过滤。
    
    Args:
        client: DME API client
        cluster_id: 容器集群 ID（Optional）
        name: 持久卷名称（Optional，supports fuzzy search）
        page_no: 分页查询的Start page，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        {
            pvs: PV list。参数格式如下：[{
                name: PV名称 (string),
                status: 状态 (string),
                capacity: 容量 (string),
            }, ...],
        }
    """
    url = "/rest/dmecaasmgmt/v1/pvs/query-list"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if cluster_id is not None:
        payload['cluster_id'] = cluster_id
    if name is not None:
        payload['name'] = name
    
    response = client.post(url, body=payload)
    return response


# Action list for CLI help
ACTIONS = {
    # 集群管理
    'cluster_list': {
        'func': cluster_list,
        'description': '查询Container cluster list',
        'params': ['name', 'page_no', 'page_size'],
        'subtopic': 'cluster'
    },
    # 节点管理
    'node_list': {
        'func': node_list,
        'description': '查询Container node list',
        'params': ['cluster_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'node'
    },
    # 容器组管理
    'pod_list': {
        'func': pod_list,
        'description': '查询Pod list',
        'params': ['cluster_id', 'namespace', 'name', 'page_no', 'page_size'],
        'subtopic': 'pod'
    },
    # 命名空间管理
    'namespace_list': {
        'func': namespace_list,
        'description': '查询容器命名空间列表',
        'params': ['cluster_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'namespace'
    },
    # 持久卷声明管理
    'pvc_list': {
        'func': pvc_list,
        'description': '查询容器PVC list',
        'params': ['cluster_id', 'namespace', 'name', 'page_no', 'page_size'],
        'subtopic': 'pvc'
    },
    # 持久卷管理
    'pv_list': {
        'func': pv_list,
        'description': '查询容器PV list',
        'params': ['cluster_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'pv'
    },
}
