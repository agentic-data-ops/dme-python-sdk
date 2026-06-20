"""
Kubernetes operations
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
    Query container cluster list

    Args:
        client: DME API client
        id: Cluster ID (Optional)
        name: Cluster name(Optional, supports fuzzy query）
        version: Version (Optional)
        ip_address: Container cluster IP address(Optional, supports fuzzy query）
        status: Status (Optional)，valid values：abnormal（Abnormal）, normal（Normal）
        sync_status: Sync status list (Optional)，valid values：unsync（Unsync）, sync（Syncing）, normal（Synced）, failed（Sync failed）, partial（Partially synced）
        platform_id: Container platform ID (Optional)
        platform_name: Container platform name(Optional, supports fuzzy query）
        sort_key: Sort key (Optional)，valid values：node_number, total_cpu, total_memory, cpu_allocation_rate, memory_allocation_rate, name
        sort_dir: Sort direction (Optional)，valid values：asc (ascending), desc (descending)
        page_no: Pagination page number，1~2147483647，default 1
        page_size: Items per page，1~1000，default 20

    Returns:
        {
            total: Total clusters (integer),
            clusters_resp: Container cluster list (List<ClustersBaseResponse>)。parameter format: [{
                id: Cluster ID (string),
                neId: Device ID (string),
                name: Cluster name (string),
                version: Version (string),
                ip_address: Container cluster IP address (string),
                status: Connection status (string),
                sync_status: Sync status (string),
                platform_id: Container platform ID (string),
                platform_name: Container platform name (string),
                node_number: Total nodes (int32),
                total_cpu: Total CPU (int64),
                total_memory: Total memory (int64),
                cpu_allocation_rate: CPU allocation rate (number),
                memory_allocation_rate: Memory allocation rate (number),
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
    Query container node list

    Args:
        client: DME API client
        id: Node ID (Optional)
        name: Node name(Optional, supports fuzzy query）
        cluster_id: Container cluster ID (Optional)
        pool_id: Node pool ID (Optional)
        ip_address: Node IP address(Optional, supports fuzzy query）
        ready_status: Ready status (Optional)，valid values：ready（Ready）, not-ready（Not ready）
        scheduling_status: Scheduling status (Optional)，valid values：schedule（Schedulable）, not-schedule（Not schedulable）
        pool_name: Node pool name(Optional, supports fuzzy query）
        sort_key: Sort key (Optional)，valid values：pod_count, create_time, total_cpu, total_memory, cpu_allocation_rate, memory_allocation_rate
        sort_dir: Sort direction (Optional)，valid values：asc (ascending), desc (descending)
        page_no: Pagination page number，1~2147483647，default 1
        page_size: Items per page，1~1000，default 20

    Returns:
        {
            total: Total nodes (int32),
            nodes_resp: Container node list (List<NodesBaseResponse>)。parameter format: [{
                id: Node ID (string),
                name: Node name (string),
                ip_address: Node IP address (string),
                ready_status: Ready status (string),
                scheduling_status: Scheduling status (string),
                pool_name: Node pool name (string),
                pool_id: Node pool ID (string),
                pod_count: Total pods (int32),
                total_cpu: Total CPU (int64),
                total_memory: Total memory (int64),
                cpu_allocation_rate: CPU allocation rate (number),
                memory_allocation_rate: Memory allocation rate (number),
                create_time: Creation timestamp (int64),
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
    Query container pod list

    Query container pod list, supports filtering by cluster ID, namespace and name.

    Args:
        client: DME API client
        id: Pod ID (Optional)
        name: Pod name(Optional, supports fuzzy query）
        workload_id: Workload ID (Optional)
        node_id: Container node ID (Optional)
        namespace_name: Namespace name (Optional)
        cluster_name: Cluster name(Optional, supports fuzzy query）
        cluster_id: Container cluster ID (Optional)
        platform_id: Container platform ID (Optional)
        platform_name: Container platform name (Optional)
        namespace_id: Namespace unique ID (Optional)
        ip_address: Pod IP address(Optional, supports fuzzy query）
        node_name: Node name (Optional)
        running_status: Running status list (Optional)，valid values：running（Running）, pending, succeeded（Succeeded）, failed（Failed）, unknown（Unknown）
        controller: Controller (Optional)
        sort_key: Sort key (Optional)，valid values：reboot_time, create_time
        sort_dir: Sort direction (Optional)，valid values：asc (ascending), desc (descending)
        page_no: Pagination page number，1~2147483647，default 1
        page_size: Items per page，1~1000，default 20

    Returns:
        {
            total: Total pods (int32),
            pods_resp: Pod list (List<PodsBaseResponse>)。parameter format: [{
                id: Pod ID (string),
                name: Pod name (string),
                cluster_id: Cluster ID (string),
                cluster_name: Cluster name (string),
                ip_address: Pod IP address (string),
                namespace_id: Namespace ID (string),
                namespace_name: Namespace name (string),
                node_name: Node name (string),
                running_status: Running status (string),
                controller: Controller (string),
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
    Query container namespace list

    Args:
        client: DME API client
        name: Namespace name(Optional, supports fuzzy query）
        cluster_id: Container cluster ID (Optional)
        status: Namespace status list (Optional)，valid values：active（Active）, terminating（Terminating）, unknown（Unknown）
        sort_key: Sort key (Optional)，valid values：create_time
        sort_dir: Sort direction (Optional)，valid values：asc (ascending), desc (descending)
        page_no: Pagination page number，1~2147483647，default 1
        page_size: Items per page，1~1000，default 20

    Returns:
        {
            total: Total namespaces (int32),
            namespaces_resp: Namespace list (List<NamespacesBaseResponse>)。parameter format: [{
                id: Namespace ID (string),
                name: Namespace name (string),
                status: Status (string),
                create_time: Creation timestamp (int64),
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
    Query container PVC list

    Args:
        client: DME API client
        name: PVC name(Optional, supports fuzzy query）
        namespace_name: Namespace name(Optional, supports fuzzy query）
        cluster_name: Cluster name(Optional, supports fuzzy query）
        cluster_id: Cluster ID (Optional)
        platform_id: Container platform ID (Optional)
        platform_name: Container platform name(Optional, supports fuzzy query）
        namespace_id: Namespace unique ID (Optional)
        status: Status list (Optional)，valid values：pending, bound, lost
        access_mode: Access mode list (Optional)，valid values：read_write_many, read_write_once, read_only_many, read_write_once_pod
        storage_class_name: Storage class name(Optional, supports fuzzy query）
        sort_key: Sort key (Optional)，valid values：capacity, create_time
        sort_dir: Sort direction (Optional)，valid values：asc (ascending), desc (descending)
        page_no: Pagination page number，1~2147483647，default 1
        page_size: Items per page，1~1000，default 20

    Returns:
        {
            total: Total PVCs (int32),
            pvcs_resp: PVC list (List<PvcsBaseResponse>)。parameter format: [{
                id: PVC ID (string),
                name: PVC name (string),
                cluster_id: Cluster ID (string),
                cluster_name: Cluster name (string),
                namespace_id: Namespace ID (string),
                namespace_name: Namespace name (string),
                status: Status (string),
                pv_name: PV name (string),
                access_mode: Access mode (string),
                storage_class_name: Storage class name (string),
                capacity: Capacity (GB) (number),
                create_time: Creation timestamp (int64),
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
    Query container PV list

    Query container PV list。

    Args:
        client: DME API client
        id: PV ID (Optional)
        name: PV name(Optional, supports fuzzy query）
        cluster_name: Cluster name(Optional, supports fuzzy query）
        cluster_id: Cluster ID (Optional)
        platform_id: Container platform ID (Optional)
        platform_name: Container platform name(Optional, supports fuzzy query）
        status: Status list (Optional)，valid values：available, pending, bound（bound）, released（released）, failed（Failed）
        access_mode: Access mode list (Optional)，valid values：read_write_many, read_write_once, read_only_many, read_write_once_pod
        storage_class_name: Storage class name(Optional, supports fuzzy query）
        sort_key: Sort key (Optional)，valid values：capacity, create_time
        sort_dir: Sort direction (Optional)，valid values：asc (ascending), desc (descending)
        page_no: Pagination page number，1~2147483647，default 1
        page_size: Items per page，1~1000，default 20

    Returns:
        {
            total: Total PVs (int32),
            pvs_resp: PV list (List<PvsBaseResponse>)。parameter format: [{
                id: PV ID (string),
                name: PV name (string),
                cluster_id: Cluster ID (string),
                cluster_name: Cluster name (string),
                status: Status (string),
                pvc_name: PVC name (string),
                access_mode: Access mode (string),
                storage_class_name: Storage class name (string),
                capacity: Capacity (GB) (number),
                create_time: Creation timestamp (int64),
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


# Action list for CLI help
ACTIONS = {
    # Cluster management
    'cluster_list': {
        'func': cluster_list,
        'description': 'Query container cluster list',
        'params': ['id', 'name', 'version', 'ip_address', 'status',
                   'sync_status', 'platform_id', 'platform_name',
                   'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'cluster'
    },
    # Node management
    'node_list': {
        'func': node_list,
        'description': 'Query container node list',
        'params': ['id', 'name', 'cluster_id', 'pool_id', 'ip_address',
                   'ready_status', 'scheduling_status', 'pool_name',
                   'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'node'
    },
    # Pod management
    'pod_list': {
        'func': pod_list,
        'description': 'Query container pod list',
        'params': ['id', 'name', 'workload_id', 'node_id', 'namespace_name',
                   'cluster_name', 'cluster_id', 'platform_id', 'platform_name',
                   'namespace_id', 'ip_address', 'node_name', 'running_status',
                   'controller', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'pod'
    },
    # Namespace management
    'namespace_list': {
        'func': namespace_list,
        'description': 'Query container namespace list',
        'params': ['name', 'cluster_id', 'status', 'sort_key', 'sort_dir',
                   'page_no', 'page_size'],
        'subtopic': 'namespace'
    },
    # PVC management
    'pvc_list': {
        'func': pvc_list,
        'description': 'Query container PVC list',
        'params': ['name', 'namespace_name', 'cluster_name', 'cluster_id',
                   'platform_id', 'platform_name', 'namespace_id', 'status',
                   'access_mode', 'storage_class_name', 'sort_key', 'sort_dir',
                   'page_no', 'page_size'],
        'subtopic': 'pvc'
    },
    # PV management
    'pv_list': {
        'func': pv_list,
        'description': 'Query container PV list',
        'params': ['id', 'name', 'cluster_name', 'cluster_id', 'platform_id',
                   'platform_name', 'status', 'access_mode', 'storage_class_name',
                   'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'pv'
    },
}
