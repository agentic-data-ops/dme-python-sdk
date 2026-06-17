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
    queryVirtual machinelist
    
    Args:
        client: DME API client
        site_id: Virtual machine所属站点 ID
        cluster_id: Virtual machine所属cluster ID (HCS 场景不支持)
        dc_id: 数据中心 ID (仅 FusionCompute 场景支持)
        cluster_name: Virtual machine所属cluster name (支持模糊搜索, HCS 场景不支持)
        host_id: Virtual machine所属物理主机唯一标识
        host_name: Virtual machine所属host name (支持模糊搜索)
        name: Virtual machinename (支持模糊搜索)
        ip_address: Virtual machine IP 地址 (支持模糊搜索)
        status: Virtual machinestatuslist
                取值: running, stopped, unknown, hibernated, creating, shutting-down,
                     migrating, fault-resuming, starting, stopping, hibernating, pause,
                     recycling, deactivated, active, saving, deleted, other, uploading,
                     pending_delete, queued, importing, killed, storage_migrating,
                     building, error
        is_template: 是否是模板 (true/false)
        os_type: 操作系统typelist (Windows, Linux, Other)
        vr_type: 虚拟化平台type (FUSIONCOMPUTE, VMWARE, HCS)
        datacenter_id: 数据存储所属数据中心 ID (仅 vCenter 场景支持)
        sort_key: 排序字段 (name, cpu_core, memory_size, disk_total_size, create_time, ip_address)
        sort_dir: 排序方向 (asc, desc), default asc
        page_no: pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            total: Virtual machinetotal (integer),
            vms: Virtual machinelist (List<VmInfo>). parameter format: [{
                id: Virtual machineID (string),
                name: Virtual machinename (string),
                status: status (string),
                cpu: CPUcount (integer),
                memory: 内存大小 (integer),
            }, ...],
        }
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
    query指定Virtual machinedetails
    
    queryVirtual machine的详细info. 
    
    Args:
        client: DME API client
        vm_id: Virtual machine ID(Required)
        vr_type: 虚拟化平台type(Optional)
    
    Returns:
        {
            id: Virtual machineID (string),
            name: name (string),
            status: status (string),
            cpu: CPUinfo. attribute format: {
                cores: CPU核数 (int32),
                sockets: CPU插槽数 (int32),
            },
            memory: 内存大小 (int64, MB),
            vm_nics: 网卡list (List<VmNicInfo>). parameter format: [{
                id: 网卡ID (string),
                name: 网卡name (string),
                mac: MAC地址 (string),
            }, ...],
            vm_disks: 磁盘list (List<VmDiskInfo>). parameter format: [{
                id: 磁盘ID (string),
                name: 磁盘name (string),
                capacity: capacity (int64, GB),
            }, ...],
        }
    """
    url = "/rest/vmmgmt/v1/vms/{vm_id}"
    
    params_dict = {"vm_id": vm_id}
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
    query数据存储list
    
    Args:
        client: DME API client
        site_id: 数据存储所在的站点 ID
        cluster_id: 数据存储所关联的cluster ID
        host_id: 数据存储所关联的主机 ID
        dc_id: 数据存储所在数据中心 ID
        name: 数据存储name (supports fuzzy query)
        status: 数据存储statuslist
                取值: NORMAL, ABNORMAL, CREATING, DELETING, READONLY, EXPANDING,
                     RESTORING, WARNING, ALERT, UNKNOWN, WRITE_PROTECT
        storage_type: 数据存储typelist
                      取值: LOCAL, SAN, ADVANCESAN, DSWARE, NAS, LOCALPOME, LUNPOME,
                           LUN, iotailor, CIFS, NFS, NFS41, PMEM, VFFS, VMFS, VSAN, VVOL, OTHER
        allocate_type: 是否支持精简模式 (仅 FusionCompute 场景支持)
        vr_type: 虚拟化平台type (FUSIONCOMPUTE, VMWARE, HCS)
        datacenter_id: 数据存储所属的 vCenter 数据中心 ID (仅 vCenter 场景支持)
        sort_key: 排序字段 (name, host_num, vm_num, total_capacity, used_size, free_capacity, lun_count, used_rate)
        sort_dir: 排序方向 (asc, desc), default asc
        page_no: pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含 total 和 datastores 字段
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
    query指定数据存储details
    
    query数据存储的详细info. 
    
    Args:
        client: DME API client
        datastore_id: 数据存储 ID(Required)
        vr_type: 虚拟化平台type(Optional)
    
    Returns:
        {
            id: 数据存储ID (string),
            name: name (string),
            type: type (string),
            total_capacity: total capacity (int64),
            free_capacity: free capacity (int64),
            status: status (string),
        }
    """
    url = "/rest/vmmgmt/v1/datastores/{datastore_id}"
    
    params_dict = {"datastore_id": datastore_id}
    if vr_type is not None:
        params_dict['vr_type'] = vr_type
    
    response = client.get(url, params=params_dict)
    return response


def host_list(client: DMEAPIClient, site_id: str = None, cluster_id: str = None,
               dc_id: str = None, host_name: str = None, ip_address: str = None,
               status: list = None, vr_type: str = None,
               page_no: int = 1, page_size: int = 20) -> dict:
    """
    query主机list
    
    query物理主机list, 支持多种过滤条件. 
    
    Args:
        client: DME API client
        site_id: 主机所属站点 ID
        cluster_id: 主机所属cluster ID
        dc_id: 数据中心 ID
        host_name: host name (支持模糊搜索)
        ip_address: 主机 IP 地址
        status: 主机statuslist
        vr_type: 虚拟化平台type
        page_no: pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含主机list
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
    query指定主机details
    
    query物理主机的详细info. 
    
    Args:
        client: DME API client
        host_id: 主机 ID(Required)
        vr_type: 虚拟化平台type(Optional)
    
    Returns:
        {
            id: host ID (string),
            name: name (string),
            ip: IP address (string),
            status: status (string),
            cpu_cores: CPU核数 (int32),
            memory: 内存大小 (int64, MB),
            os_type: 操作系统type (string),
        }
    """
    url = "/rest/vmmgmt/v1/hosts/{host_id}"
    
    params_dict = {"host_id": host_id}
    if vr_type is not None:
        params_dict['vr_type'] = vr_type
    
    response = client.get(url, params=params_dict)
    return response


def cluster_list(client: DMEAPIClient, site_id: str = None, dc_id: str = None,
                  name: str = None, vr_type: str = None,
                  page_no: int = 1, page_size: int = 20) -> dict:
    """
    queryclusterlist
    
    Args:
        client: DME API client
        site_id: cluster所属站点 ID
        dc_id: 数据中心 ID
        name: cluster name (支持模糊搜索)
        vr_type: 虚拟化平台type
        page_no: pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含clusterlist
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
    query指定clusterdetails
    
    querycluster的详细info. 
    
    Args:
        client: DME API client
        cluster_id: cluster ID(Required)
        vr_type: 虚拟化平台type(Optional)
    
    Returns:
        {
            id: clusterID (string),
            name: name (string),
            type: type (string),
            host_count: 主机count (int32),
            status: status (string),
        }
    """
    url = "/rest/vmmgmt/v1/clusters/{cluster_id}"
    
    params_dict = {"cluster_id": cluster_id}
    if vr_type is not None:
        params_dict['vr_type'] = vr_type
    
    response = client.get(url, params=params_dict)
    return response


def site_list(client: DMEAPIClient) -> dict:
    """
    query站点list
    
    query所有虚拟化站点list. 
    
    Args:
        client: DME API client
    
    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含站点list
    """
    url = "/rest/vmmgmt/v1/sites/query"
    
    response = client.post(url, body={})
    return response


def site_show(client: DMEAPIClient, site_id: str) -> dict:
    """
    query指定站点details
    
    query虚拟化站点的详细info. 
    
    Args:
        client: DME API client
        site_id: 站点 ID(Required)
    
    Returns:
        {
            id: 站点ID (string),
            name: name (string),
            status: status (string),
        }
    """
    url = "/rest/vmmgmt/v1/sites/{site_id}"
    
    response = client.get(url, params={"site_id": site_id})
    return response




def host_adapter_list(client: DMEAPIClient, host_id: str) -> dict:
    """
    query指定主机存储适配器list
    
    query物理主机的存储适配器list. 
    
    Args:
        client: DME API client
        host_id: 主机 ID(Required)
    
    Returns:
        {
            total: 适配器count (int32),
            adapters: 存储适配器list (List<HostAdapterInfo>). parameter format: [{
                id: 适配器ID (string),
                name: name (string),
                type: type (string),
                wwn: WWN (string),
            }, ...],
        }
    """
    url = "/rest/vmmgmt/v1/hosts/{host_id}/storage-adapters"
    
    response = client.get(url, params={"host_id": host_id})
    return response


def disk_list(client: DMEAPIClient, site_id: str = None,
                         host_id: str = None, name: str = None,
                         disk_type: list = None, status: list = None,
                         page_no: int = 1, page_size: int = 20) -> dict:
    """
    query物理盘info
    
    query物理磁盘list, 支持多种过滤条件. 
    
    Args:
        client: DME API client
        site_id: 物理盘所属站点 ID(Optional)
        host_id: 物理盘所属主机 ID(Optional)
        name: 物理盘name(Optional)
        disk_type: 磁盘typelist(Optional)
        status: 磁盘statuslist(Optional)
        page_no: pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            total: 磁盘count (int32),
            disks: 物理磁盘list (List<PhysicalDiskInfo>). parameter format: [{
                id: 磁盘ID (string),
                name: name (string),
                capacity: capacity (int64),
                status: status (string),
            }, ...],
        }
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
    query虚拟磁盘infolist
    
    query虚拟磁盘list, 支持多种过滤条件. 
    
    Args:
        client: DME API client
        site_id: 虚拟磁盘所属站点 ID(Optional)
        vm_id: 虚拟磁盘所属Virtual machine ID(Optional)
        name: 虚拟磁盘name(Optional)
        disk_type: 磁盘typelist(Optional)
        status: 磁盘statuslist(Optional)
        page_no: pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            total: 虚拟磁盘count (int32),
            vdisks: 虚拟磁盘list (List<VirtualDiskInfo>). parameter format: [{
                id: 虚拟磁盘ID (string),
                name: name (string),
                capacity: capacity (int64, GB),
                status: status (string),
            }, ...],
        }
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
    query指定虚拟磁盘info
    
    query虚拟磁盘的详细info. 
    
    Args:
        client: DME API client
        virtual_disk_id: 虚拟磁盘 ID(Required)
    
    Returns:
        {
            id: 虚拟磁盘ID (string),
            name: name (string),
            capacity: capacity (int64, GB),
            status: status (string),
            datastore_id: 所属数据存储ID (string),
        }
    """
    url = "/rest/vmmgmt/v1/vdisks/{virtual_disk_id}"
    
    response = client.get(url, params={"virtual_disk_id": virtual_disk_id})
    return response


# action list, for CLI help
ACTIONS = {
    # Virtual machine管理
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
    # cluster管理
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
