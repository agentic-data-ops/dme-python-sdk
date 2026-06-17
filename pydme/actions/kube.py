"""
Kubernetes operations
"""

import sys
import os

from pydme.client import DMEAPIClient


def cluster_list(client: DMEAPIClient, name: str = None,
                  page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query container cluster list
    
    Args:
        client: DME API client
        name: Container cluster name (optional, supports fuzzy query)
        page_no: Pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            total: total clusters (integer),
            clusters: Container cluster list. parameter format: [{
                id: Cluster ID (string),
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
    Query container node list
    
    Args:
        client: DME API client
        cluster_id: Container cluster ID (Optional)
        name: Container node name (optional, supports fuzzy query)
        page_no: Pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            nodes: Container node list. parameter format: [{
                id: Node ID (string),
                name: Node name (string),
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
    Query container pod list
    
    Query pod list, supports filtering by cluster ID, Namespace and name.
    
    Args:
        client: DME API client
        cluster_id: Container cluster ID (Optional)
        namespace: Container Namespace (Optional)
        name: Pod name (optional, supports fuzzy query)
        page_no: Pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            pods: Pod list. parameter format: [{
                name: Pod name (string),
                status: status (string),
                node: Node (string),
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
    Query container Namespace list
    
    Args:
        client: DME API client
        cluster_id: Container cluster ID (Optional)
        name: namespace name (optional, supports fuzzy query)
        page_no: Pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            namespaces: Namespace list (List<string>),
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
    Query container persistent volume claim list
    
    Args:
        client: DME API client
        cluster_id: Container cluster ID (Optional)
        namespace: Container Namespace (Optional)
        name: Persistent volume claim name (optional, supports fuzzy query)
        page_no: Pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            pvcs: Persistent volume claim list. parameter format: [{
                name: PVC name (string),
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
    Query container persistent volume list
    
    Query container persistent volume (PV) list, supports filtering by cluster ID and name.
    
    Args:
        client: DME API client
        cluster_id: Container cluster ID (Optional)
        name: Persistent volume name (optional, supports fuzzy query)
        page_no: Pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            pvs: Persistent volume list. parameter format: [{
                name: PV name (string),
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
    # Cluster management
    'cluster_list': {
        'func': cluster_list,
        'description': 'Query container cluster list',
        'params': ['name', 'page_no', 'page_size'],
        'subtopic': 'cluster'
    },
    # Node management
    'node_list': {
        'func': node_list,
        'description': 'Query container node list',
        'params': ['cluster_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'node'
    },
    # Pod management
    'pod_list': {
        'func': pod_list,
        'description': 'Query container pod list',
        'params': ['cluster_id', 'namespace', 'name', 'page_no', 'page_size'],
        'subtopic': 'pod'
    },
    # Namespace management
    'namespace_list': {
        'func': namespace_list,
        'description': 'Query container namespace list',
        'params': ['cluster_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'namespace'
    },
    # Persistent volume claim management
    'pvc_list': {
        'func': pvc_list,
        'description': 'Query container persistent volume claim list',
        'params': ['cluster_id', 'namespace', 'name', 'page_no', 'page_size'],
        'subtopic': 'pvc'
    },
    # Persistent volume management
    'pv_list': {
        'func': pv_list,
        'description': 'Query container persistent volume list',
        'params': ['cluster_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'pv'
    },
}
