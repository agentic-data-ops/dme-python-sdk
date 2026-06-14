"""
Kubernetes operations
"""

import sys
import os

from pydme.client import DMEAPIClient


def cluster_list(client: DMEAPIClient, name: str = None,
                  page_no: int = 1, page_size: int = 20) -> dict:
    """
     query container cluster list
    
    Args:
        client: DME API client
        name: Container cluster name (Optional, supports fuzzy search) 
        page_no: Page queryStart page, default 1
        page_size: per pagecount, 1~1000, default 20
    
    Returns:
        {
            total:  clusterTotal count (integer),
            clusters: Container cluster list. 参数格式如下：[{
                id:  clusterID (string),
                name: Cluster name (string),
                status:  status (string),
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
     query container node list
    
    Args:
        client: DME API client
        cluster_id: Container cluster ID (Optional) 
        name: Container node name (Optional, supports fuzzy search) 
        page_no: Page queryStart page, default 1
        page_size: per pagecount, 1~1000, default 20
    
    Returns:
        {
            nodes: Container node list. 参数格式如下：[{
                id:  nodeID (string),
                name: Node name (string),
                status:  status (string),
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
     query pod list
    
     Query pod list,  supports filtering by cluster ID, namespace and name. 
    
    Args:
        client: DME API client
        cluster_id: Container cluster ID (Optional) 
        namespace: Container namespace (Optional) 
        name: Pod name (Optional, supports fuzzy search) 
        page_no: Page queryStart page, default 1
        page_size: per pagecount, 1~1000, default 20
    
    Returns:
        {
            pods: Pod list. 参数格式如下：[{
                name: Pod name (string),
                status:  status (string),
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
    Query container namespace list
    
    Args:
        client: DME API client
        cluster_id: Container cluster ID (Optional) 
        name: Namespace name (Optional, supports fuzzy search) 
        page_no: Page queryStart page, default 1
        page_size: per pagecount, 1~1000, default 20
    
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
    Query containerPVC list
    
    Args:
        client: DME API client
        cluster_id: Container cluster ID (Optional) 
        namespace: Container namespace (Optional) 
        name: Persistent volume claim name (Optional, supports fuzzy search) 
        page_no: Page queryStart page, default 1
        page_size: per pagecount, 1~1000, default 20
    
    Returns:
        {
            pvcs: PVC list. 参数格式如下：[{
                name: PVC name (string),
                status:  status (string),
                capacity:  capacity (string),
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
    Query containerPV list
    
    Query container PV list,  supports filtering by cluster ID and name. 
    
    Args:
        client: DME API client
        cluster_id: Container cluster ID (Optional) 
        name: Persistent volume name (Optional, supports fuzzy search) 
        page_no: Page queryStart page, default 1
        page_size: per pagecount, 1~1000, default 20
    
    Returns:
        {
            pvs: PV list. 参数格式如下：[{
                name: PV name (string),
                status:  status (string),
                capacity:  capacity (string),
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
    #  clustermanagement 
    'cluster_list': {
        'func': cluster_list,
        'description': ' query container cluster list',
        'params': ['name', 'page_no', 'page_size'],
        'subtopic': 'cluster'
    },
    # Node management
    'node_list': {
        'func': node_list,
        'description': ' query container node list',
        'params': ['cluster_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'node'
    },
    # Podmanagement 
    'pod_list': {
        'func': pod_list,
        'description': ' query pod list',
        'params': ['cluster_id', 'namespace', 'name', 'page_no', 'page_size'],
        'subtopic': 'pod'
    },
    # Namespacemanagement 
    'namespace_list': {
        'func': namespace_list,
        'description': 'Query container namespace list',
        'params': ['cluster_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'namespace'
    },
    # Persistent volume claimmanagement 
    'pvc_list': {
        'func': pvc_list,
        'description': 'Query containerPVC list',
        'params': ['cluster_id', 'namespace', 'name', 'page_no', 'page_size'],
        'subtopic': 'pvc'
    },
    # Persistent volumemanagement 
    'pv_list': {
        'func': pv_list,
        'description': 'Query containerPV list',
        'params': ['cluster_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'pv'
    },
}
