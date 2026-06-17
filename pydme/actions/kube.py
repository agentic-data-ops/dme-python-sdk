"""
Kubernetes operations
"""

import sys
import os

from pydme.client import DMEAPIClient


def cluster_list(client: DMEAPIClient, name: str = None,
                  page_no: int = 1, page_size: int = 20) -> dict:
    """
    query容器clusterlist
    
    Args:
        client: DME API client
        name: 容器cluster name (可选, supports fuzzy query)
        page_no: pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            total: total clusters (integer),
            clusters: 容器clusterlist. parameter format: [{
                id: clusterID (string),
                name: cluster name (string),
                status: status (string),
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
    query容器节点list
    
    Args:
        client: DME API client
        cluster_id: 容器cluster ID(Optional)
        name: 容器节点name (可选, supports fuzzy query)
        page_no: pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            nodes: 容器节点list. parameter format: [{
                id: 节点ID (string),
                name: 节点name (string),
                status: status (string),
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
    query容器组list
    
    query容器组 (Pod)list, 支持按cluster ID、Namespace和name过滤. 
    
    Args:
        client: DME API client
        cluster_id: 容器cluster ID(Optional)
        namespace: 容器Namespace(Optional)
        name: 容器组name (可选, supports fuzzy query)
        page_no: pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            pods: 容器组list. parameter format: [{
                name: 容器组name (string),
                status: status (string),
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
    query容器Namespacelist
    
    Args:
        client: DME API client
        cluster_id: 容器cluster ID(Optional)
        name: namespace name (可选, supports fuzzy query)
        page_no: pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            namespaces: Namespacelist (List<string>),
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
    query容器持久卷声明list
    
    Args:
        client: DME API client
        cluster_id: 容器cluster ID(Optional)
        namespace: 容器Namespace(Optional)
        name: 持久卷声明name (可选, supports fuzzy query)
        page_no: pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            pvcs: 持久卷声明list. parameter format: [{
                name: PVCname (string),
                status: status (string),
                capacity: capacity (string),
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
    query容器持久卷list
    
    query容器持久卷 (PV)list, 支持按cluster ID 和name过滤. 
    
    Args:
        client: DME API client
        cluster_id: 容器cluster ID(Optional)
        name: 持久卷name (可选, supports fuzzy query)
        page_no: pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            pvs: 持久卷list. parameter format: [{
                name: PVname (string),
                status: status (string),
                capacity: capacity (string),
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


# action list, for CLI help
ACTIONS = {
    # cluster管理
    'cluster_list': {
        'func': cluster_list,
        'description': '查询容器集群列表',
        'params': ['name', 'page_no', 'page_size'],
        'subtopic': 'cluster'
    },
    # 节点管理
    'node_list': {
        'func': node_list,
        'description': '查询容器节点列表',
        'params': ['cluster_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'node'
    },
    # 容器组管理
    'pod_list': {
        'func': pod_list,
        'description': '查询容器组列表',
        'params': ['cluster_id', 'namespace', 'name', 'page_no', 'page_size'],
        'subtopic': 'pod'
    },
    # Namespace管理
    'namespace_list': {
        'func': namespace_list,
        'description': '查询容器命名空间列表',
        'params': ['cluster_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'namespace'
    },
    # 持久卷声明管理
    'pvc_list': {
        'func': pvc_list,
        'description': '查询容器持久卷声明列表',
        'params': ['cluster_id', 'namespace', 'name', 'page_no', 'page_size'],
        'subtopic': 'pvc'
    },
    # 持久卷管理
    'pv_list': {
        'func': pv_list,
        'description': '查询容器持久卷列表',
        'params': ['cluster_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'pv'
    },
}
