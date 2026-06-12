"""
虚拟化服务 (Virtualization) 相关操作
"""

import sys
import os

from pydme.client import DMEAPIClient


def vm_list(client: DMEAPIClient, site_id: str = None, cluster_id: str = None,
             dc_id: str = None, cluster_name: str = None, host_id: str = None,
             host_name: str = None, name: str = None, ip_address: str = None,
             status: list = None, is_template: bool = None, os_type: list = None,
             vr_type: str = None, datacenter_id: str = None, sort_key: str = None,
             sort_dir: str = "asc", page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询虚拟机列表
    
    查询虚拟机列表，支持多种过滤条件和分页。
    
    Args:
        client: DME API 客户端
        site_id: 虚拟机所属站点 ID
        cluster_id: 虚拟机所属集群 ID（HCS 场景不支持）
        dc_id: 数据中心 ID（仅 FusionCompute 场景支持）
        cluster_name: 虚拟机所属集群名称（支持模糊搜索，HCS 场景不支持）
        host_id: 虚拟机所属物理主机唯一标识
        host_name: 虚拟机所属主机名称（支持模糊搜索）
        name: 虚拟机名称（支持模糊搜索）
        ip_address: 虚拟机 IP 地址（支持模糊搜索）
        status: 虚拟机状态列表
                取值：running, stopped, unknown, hibernated, creating, shutting-down,
                     migrating, fault-resuming, starting, stopping, hibernating, pause,
                     recycling, deactivated, active, saving, deleted, other, uploading,
                     pending_delete, queued, importing, killed, storage_migrating,
                     building, error
        is_template: 是否是模板（true/false）
        os_type: 操作系统类型列表（Windows, Linux, Other）
        vr_type: 虚拟化平台类型（FUSIONCOMPUTE, VMWARE, HCS）
        datacenter_id: 数据存储所属数据中心 ID（仅 vCenter 场景支持）
        sort_key: 排序字段（name, cpu_core, memory_size, disk_total_size, create_time, ip_address）
        sort_dir: 排序方向（asc, desc），默认 asc
        page_no: 分页查询的起始页码，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        响应数据，包含 total 和 vms 字段
    """
    url = "/rest/vmmgmt/v1/vms/query"
    
    body_params = {
        'page_no': page_no,
        'page_size': page_size,
        'sort_dir': sort_dir
    }
    
    if sort_key is not None:
        body_params['sort_key'] = sort_key
    
    if site_id is not None:
        body_params['site_id'] = site_id
    if cluster_id is not None:
        body_params['cluster_id'] = cluster_id
    if dc_id is not None:
        body_params['dc_id'] = dc_id
    if cluster_name is not None:
        body_params['cluster_name'] = cluster_name
    if host_id is not None:
        body_params['host_id'] = host_id
    if host_name is not None:
        body_params['host_name'] = host_name
    if name is not None:
        body_params['name'] = name
    if ip_address is not None:
        body_params['ip_address'] = ip_address
    if status is not None:
        body_params['status'] = status
    if is_template is not None:
        body_params['is_template'] = is_template
    if os_type is not None:
        body_params['os_type'] = os_type
    if vr_type is not None:
        body_params['vr_type'] = vr_type
    if datacenter_id is not None:
        body_params['datacenter_id'] = datacenter_id
    
    response = client.post(url, body=body_params)
    return response


def vm_show(client: DMEAPIClient, vm_id: str, vr_type: str = None) -> dict:
    """
    查询指定虚拟机详情
    
    查询虚拟机的详细信息。
    
    Args:
        client: DME API 客户端
        vm_id: 虚拟机 ID（必选）
        vr_type: 虚拟化平台类型（可选）
    
    Returns:
        虚拟机详细信息，包含 CPU、内存、磁盘、网卡等配置信息
    """
    url = "/rest/vmmgmt/v1/vms/{vm_id}"
    
    params_dict = {}
    if vr_type is not None:
        params_dict['vr_type'] = vr_type
    
    response = client.get(url, params=params_dict)
    return response


def datastore_list(client: DMEAPIClient, site_id: str = None, cluster_id: str = None,
                    host_id: str = None, dc_id: str = None, name: str = None,
                    status: list = None, storage_type: list = None,
                    allocate_type: bool = None, vr_type: str = None,
                    datacenter_id: str = None, sort_key: str = "name",
                    sort_dir: str = "asc", page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询数据存储列表
    
    查询数据存储列表，支持多种过滤条件和分页。
    
    Args:
        client: DME API 客户端
        site_id: 数据存储所在的站点 ID
        cluster_id: 数据存储所关联的集群 ID
        host_id: 数据存储所关联的主机 ID
        dc_id: 数据存储所在数据中心 ID
        name: 数据存储名称（支持模糊查询）
        status: 数据存储状态列表
                取值：NORMAL, ABNORMAL, CREATING, DELETING, READONLY, EXPANDING,
                     RESTORING, WARNING, ALERT, UNKNOWN, WRITE_PROTECT
        storage_type: 数据存储类型列表
                      取值：LOCAL, SAN, ADVANCESAN, DSWARE, NAS, LOCALPOME, LUNPOME,
                           LUN, iotailor, CIFS, NFS, NFS41, PMEM, VFFS, VMFS, VSAN, VVOL, OTHER
        allocate_type: 是否支持精简模式（仅 FusionCompute 场景支持）
        vr_type: 虚拟化平台类型（FUSIONCOMPUTE, VMWARE, HCS）
        datacenter_id: 数据存储所属的 vCenter 数据中心 ID（仅 vCenter 场景支持）
        sort_key: 排序字段（name, host_num, vm_num, total_capacity, used_size, free_capacity, lun_count, used_rate）
        sort_dir: 排序方向（asc, desc），默认 asc
        page_no: 分页查询的起始页码，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        响应数据，包含 total 和 datastores 字段
    """
    url = "/rest/vmmgmt/v1/datastores/query"
    
    body_params = {
        'page_no': page_no,
        'page_size': page_size,
        'sort_dir': sort_dir,
        'sort_key': sort_key
    }
    
    if site_id is not None:
        body_params['site_id'] = site_id
    if cluster_id is not None:
        body_params['cluster_id'] = cluster_id
    if host_id is not None:
        body_params['host_id'] = host_id
    if dc_id is not None:
        body_params['dc_id'] = dc_id
    if name is not None:
        body_params['name'] = name
    if status is not None:
        body_params['status'] = status
    if storage_type is not None:
        body_params['storage_type'] = storage_type
    if allocate_type is not None:
        body_params['allocate_type'] = allocate_type
    if vr_type is not None:
        body_params['vr_type'] = vr_type
    if datacenter_id is not None:
        body_params['datacenter_id'] = datacenter_id
    
    response = client.post(url, body=body_params)
    return response


def datastore_show(client: DMEAPIClient, datastore_id: str, vr_type: str = None) -> dict:
    """
    查询指定数据存储详情
    
    查询数据存储的详细信息。
    
    Args:
        client: DME API 客户端
        datastore_id: 数据存储 ID（必选）
        vr_type: 虚拟化平台类型（可选）
    
    Returns:
        数据存储详细信息
    """
    url = "/rest/vmmgmt/v1/datastores/{datastore_id}"
    
    params_dict = {}
    if vr_type is not None:
        params_dict['vr_type'] = vr_type
    
    response = client.get(url, params=params_dict)
    return response


def host_list(client: DMEAPIClient, site_id: str = None, cluster_id: str = None,
               dc_id: str = None, host_name: str = None, ip_address: str = None,
               status: list = None, vr_type: str = None,
               page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询主机列表
    
    查询物理主机列表，支持多种过滤条件。
    
    Args:
        client: DME API 客户端
        site_id: 主机所属站点 ID
        cluster_id: 主机所属集群 ID
        dc_id: 数据中心 ID
        host_name: 主机名称（支持模糊搜索）
        ip_address: 主机 IP 地址
        status: 主机状态列表
        vr_type: 虚拟化平台类型
        page_no: 分页查询的起始页码，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        响应数据，包含主机列表
    """
    url = "/rest/vmmgmt/v1/hosts/query"
    
    body_params = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if site_id is not None:
        body_params['site_id'] = site_id
    if cluster_id is not None:
        body_params['cluster_id'] = cluster_id
    if dc_id is not None:
        body_params['dc_id'] = dc_id
    if host_name is not None:
        body_params['host_name'] = host_name
    if ip_address is not None:
        body_params['ip_address'] = ip_address
    if status is not None:
        body_params['status'] = status
    if vr_type is not None:
        body_params['vr_type'] = vr_type
    
    response = client.post(url, body=body_params)
    return response


def host_show(client: DMEAPIClient, host_id: str, vr_type: str = None) -> dict:
    """
    查询指定主机详情
    
    查询物理主机的详细信息。
    
    Args:
        client: DME API 客户端
        host_id: 主机 ID（必选）
        vr_type: 虚拟化平台类型（可选）
    
    Returns:
        主机详细信息
    """
    url = "/rest/vmmgmt/v1/hosts/{host_id}"
    
    params_dict = {}
    if vr_type is not None:
        params_dict['vr_type'] = vr_type
    
    response = client.get(url, params=params_dict)
    return response


def cluster_list(client: DMEAPIClient, site_id: str = None, dc_id: str = None,
                  name: str = None, vr_type: str = None,
                  page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询集群列表
    
    查询集群列表，支持多种过滤条件。
    
    Args:
        client: DME API 客户端
        site_id: 集群所属站点 ID
        dc_id: 数据中心 ID
        name: 集群名称（支持模糊搜索）
        vr_type: 虚拟化平台类型
        page_no: 分页查询的起始页码，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        响应数据，包含集群列表
    """
    url = "/rest/vmmgmt/v1/clusters/query"
    
    body_params = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if site_id is not None:
        body_params['site_id'] = site_id
    if dc_id is not None:
        body_params['dc_id'] = dc_id
    if name is not None:
        body_params['name'] = name
    if vr_type is not None:
        body_params['vr_type'] = vr_type
    
    response = client.post(url, body=body_params)
    return response


def cluster_show(client: DMEAPIClient, cluster_id: str, vr_type: str = None) -> dict:
    """
    查询指定集群详情
    
    查询集群的详细信息。
    
    Args:
        client: DME API 客户端
        cluster_id: 集群 ID（必选）
        vr_type: 虚拟化平台类型（可选）
    
    Returns:
        集群详细信息
    """
    url = "/rest/vmmgmt/v1/clusters/{cluster_id}"
    
    params_dict = {}
    if vr_type is not None:
        params_dict['vr_type'] = vr_type
    
    response = client.get(url, params=params_dict)
    return response


def site_list(client: DMEAPIClient) -> dict:
    """
    查询站点列表
    
    查询所有虚拟化站点列表。
    
    Args:
        client: DME API 客户端
    
    Returns:
        响应数据，包含站点列表
    """
    url = "/rest/vmmgmt/v1/sites/query"
    
    response = client.post(url, body={})
    return response


def site_show(client: DMEAPIClient, site_id: str) -> dict:
    """
    查询指定站点详情
    
    查询虚拟化站点的详细信息。
    
    Args:
        client: DME API 客户端
        site_id: 站点 ID（必选）
    
    Returns:
        站点详细信息
    """
    url = "/rest/vmmgmt/v1/sites/{site_id}"
    
    response = client.get(url, params={"site_id": site_id})
    return response


def get_vm_performance(client: DMEAPIClient, vm_id: str,
                       indicators: list = None,
                       range: str = "LAST_1_HOUR") -> dict:
    """
    查询虚拟机性能数据
    
    便捷方法，查询虚拟机的性能数据。
    
    Args:
        client: DME API 客户端
        vm_id: 虚拟机 ID
        indicators: 性能指标列表（可选）
        range: 时间范围，默认 LAST_1_HOUR
    
    Returns:
        性能数据响应
    """
    from performance import query_history_data_by_name
    
    if indicators is None:
        indicators = [
            'cpuUsage',
            'memoryUsage',
            'diskReadIOPS',
            'diskWriteIOPS',
            'diskReadThroughput',
            'diskWriteThroughput',
            'networkRxThroughput',
            'networkTxThroughput'
        ]
    
    return query_history_data_by_name(
        client=client,
        obj_type='VirtualMachine',
        obj_ids=[vm_id],
        indicators=indicators,
        range=range
    )


def get_datastore_performance(client: DMEAPIClient, datastore_id: str,
                               indicators: list = None,
                               range: str = "LAST_1_HOUR") -> dict:
    """
    查询数据存储性能数据
    
    便捷方法，查询数据存储的性能数据。
    
    Args:
        client: DME API 客户端
        datastore_id: 数据存储 ID
        indicators: 性能指标列表（可选）
        range: 时间范围，默认 LAST_1_HOUR
    
    Returns:
        性能数据响应
    """
    from performance import query_history_data_by_name
    
    if indicators is None:
        indicators = [
            'readIOPS',
            'writeIOPS',
            'readThroughput',
            'writeThroughput',
            'responseTime'
        ]
    
    return query_history_data_by_name(
        client=client,
        obj_type='Datastore',
        obj_ids=[datastore_id],
        indicators=indicators,
        range=range
    )


def host_adapter_list(client: DMEAPIClient, host_id: str) -> dict:
    """
    查询指定主机存储适配器列表
    
    查询物理主机的存储适配器列表。
    
    Args:
        client: DME API 客户端
        host_id: 主机 ID（必选）
    
    Returns:
        存储适配器列表
    """
    url = "/rest/vmmgmt/v1/hosts/{host_id}/storage-adapters"
    
    response = client.get(url, params={"host_id": host_id})
    return response


def disk_list(client: DMEAPIClient, site_id: str = None,
                         host_id: str = None, name: str = None,
                         disk_type: list = None, status: list = None,
                         page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询物理盘信息
    
    查询物理磁盘列表，支持多种过滤条件。
    
    Args:
        client: DME API 客户端
        site_id: 物理盘所属站点 ID（可选）
        host_id: 物理盘所属主机 ID（可选）
        name: 物理盘名称（可选）
        disk_type: 磁盘类型列表（可选）
        status: 磁盘状态列表（可选）
        page_no: 分页查询的起始页码，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        物理磁盘列表
    """
    url = "/rest/vmmgmt/v1/vdisks/pdisks"
    
    body_params = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if site_id is not None:
        body_params['site_id'] = site_id
    if host_id is not None:
        body_params['host_id'] = host_id
    if name is not None:
        body_params['name'] = name
    if disk_type is not None:
        body_params['disk_type'] = disk_type
    if status is not None:
        body_params['status'] = status
    
    response = client.post(url, body=body_params)
    return response


def vdisk_list(client: DMEAPIClient, site_id: str = None,
                        vm_id: str = None, name: str = None,
                        disk_type: list = None, status: list = None,
                        page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询虚拟磁盘信息列表
    
    查询虚拟磁盘列表，支持多种过滤条件。
    
    Args:
        client: DME API 客户端
        site_id: 虚拟磁盘所属站点 ID（可选）
        vm_id: 虚拟磁盘所属虚拟机 ID（可选）
        name: 虚拟磁盘名称（可选）
        disk_type: 磁盘类型列表（可选）
        status: 磁盘状态列表（可选）
        page_no: 分页查询的起始页码，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        虚拟磁盘列表
    """
    url = "/rest/vmmgmt/v1/vdisks/query"
    
    body_params = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if site_id is not None:
        body_params['site_id'] = site_id
    if vm_id is not None:
        body_params['vm_id'] = vm_id
    if name is not None:
        body_params['name'] = name
    if disk_type is not None:
        body_params['disk_type'] = disk_type
    if status is not None:
        body_params['status'] = status
    
    response = client.post(url, body=body_params)
    return response


def vdisk_show(client: DMEAPIClient, virtual_disk_id: str) -> dict:
    """
    查询指定虚拟磁盘信息
    
    查询虚拟磁盘的详细信息。
    
    Args:
        client: DME API 客户端
        virtual_disk_id: 虚拟磁盘 ID（必选）
    
    Returns:
        虚拟磁盘详细信息
    """
    url = "/rest/vmmgmt/v1/vdisks/{virtual_disk_id}"
    
    response = client.get(url, params={"virtual_disk_id": virtual_disk_id})
    return response


# 动作列表，用于 CLI 帮助
ACTIONS = {
    # 虚拟机管理
    'vm_list': {
        'func': vm_list,
        'description': '查询虚拟机列表',
        'params': ['site_id', 'cluster_id', 'dc_id', 'cluster_name', 'host_id', 
                   'host_name', 'name', 'ip_address', 'status', 'is_template', 
                   'os_type', 'vr_type', 'datacenter_id', 'sort_key', 'sort_dir', 
                   'page_no', 'page_size'],
        'subtopic': 'vm'
    },
    'vm_show': {
        'func': vm_show,
        'description': '查询指定虚拟机详情',
        'params': ['vm_id', 'vr_type'],
        'subtopic': 'vm'
    },
    # 数据存储管理
    'datastore_list': {
        'func': datastore_list,
        'description': '查询数据存储列表',
        'params': ['site_id', 'cluster_id', 'host_id', 'dc_id', 'name', 
                   'status', 'storage_type', 'allocate_type', 'vr_type',
                   'datacenter_id', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'datastore'
    },
    'datastore_show': {
        'func': datastore_show,
        'description': '查询指定数据存储详情',
        'params': ['datastore_id', 'vr_type'],
        'subtopic': 'datastore'
    },
    # 主机管理
    'host_list': {
        'func': host_list,
        'description': '查询主机列表',
        'params': ['site_id', 'cluster_id', 'dc_id', 'host_name', 'ip_address',
                   'status', 'vr_type', 'page_no', 'page_size'],
        'subtopic': 'host'
    },
    'host_show': {
        'func': host_show,
        'description': '查询指定主机详情',
        'params': ['host_id', 'vr_type'],
        'subtopic': 'host'
    },
    'host_adapter_list': {
        'func': host_adapter_list,
        'description': '查询指定主机存储适配器列表',
        'params': ['host_id'],
        'subtopic': 'host'
    },
    # 集群管理
    'cluster_list': {
        'func': cluster_list,
        'description': '查询集群列表',
        'params': ['site_id', 'dc_id', 'name', 'vr_type', 'page_no', 'page_size'],
        'subtopic': 'cluster'
    },
    'cluster_show': {
        'func': cluster_show,
        'description': '查询指定集群详情',
        'params': ['cluster_id', 'vr_type'],
        'subtopic': 'cluster'
    },
    # 站点管理
    'site_list': {
        'func': site_list,
        'description': '查询站点列表',
        'params': [],
        'subtopic': 'site'
    },
    'site_show': {
        'func': site_show,
        'description': '查询指定站点详情',
        'params': ['site_id'],
        'subtopic': 'site'
    },
    # 物理盘管理
    'disk_list': {
        'func': disk_list,
        'description': '查询物理盘信息',
        'params': ['site_id', 'host_id', 'name', 'disk_type', 'status', 'page_no', 'page_size'],
        'subtopic': 'disk'
    },
    # 虚拟磁盘管理
    'vdisk_list': {
        'func': vdisk_list,
        'description': '查询虚拟磁盘信息列表',
        'params': ['site_id', 'vm_id', 'name', 'disk_type', 'status', 'page_no', 'page_size'],
        'subtopic': 'vdisk'
    },
    'vdisk_show': {
        'func': vdisk_show,
        'description': '查询指定虚拟磁盘信息',
        'params': ['virtual_disk_id'],
        'subtopic': 'vdisk'
    },
}
