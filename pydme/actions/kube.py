"""
Kubernetes related operations
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


# Action list for CLI help
ACTIONS = {
    # Cluster management
    'cluster_list': {
        'func': cluster_list,
        'params': ['id', 'name', 'version', 'ip_address', 'status',
                   'sync_status', 'platform_id', 'platform_name',
                   'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'cluster'
    },
    # Node management
    'node_list': {
        'func': node_list,
        'params': ['id', 'name', 'cluster_id', 'pool_id', 'ip_address',
                   'ready_status', 'scheduling_status', 'pool_name',
                   'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'node'
    },
    # Pod management
    'pod_list': {
        'func': pod_list,
        'params': ['id', 'name', 'workload_id', 'node_id', 'namespace_name',
                   'cluster_name', 'cluster_id', 'platform_id', 'platform_name',
                   'namespace_id', 'ip_address', 'node_name', 'running_status',
                   'controller', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'pod'
    },
    # Namespace management
    'namespace_list': {
        'func': namespace_list,
        'params': ['name', 'cluster_id', 'status', 'sort_key', 'sort_dir',
                   'page_no', 'page_size'],
        'subtopic': 'namespace'
    },
    # Persistent volume claim management
    'pvc_list': {
        'func': pvc_list,
        'params': ['name', 'namespace_name', 'cluster_name', 'cluster_id',
                   'platform_id', 'platform_name', 'namespace_id', 'status',
                   'access_mode', 'storage_class_name', 'sort_key', 'sort_dir',
                   'page_no', 'page_size'],
        'subtopic': 'pvc'
    },
    # Persistent volume management
    'pv_list': {
        'func': pv_list,
        'params': ['id', 'name', 'cluster_name', 'cluster_id', 'platform_id',
                   'platform_name', 'status', 'access_mode', 'storage_class_name',
                   'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'pv'
    },
}
