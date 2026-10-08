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
    url = "/rest/vmmgmt/v1/hosts/{host_id}"
    
    params_dict = {"host_id": host_id}
    if vr_type is not None:
        params_dict['vr_type'] = vr_type
    
    response = client.get(url, params=params_dict)
    return response


def cluster_list(client: DMEAPIClient, site_id: str = None, dc_id: str = None,
                  name: str = None, vr_type: str = None,
                  page_no: int = 1, page_size: int = 20) -> dict:
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
    url = "/rest/vmmgmt/v1/clusters/{cluster_id}"
    
    params_dict = {"cluster_id": cluster_id}
    if vr_type is not None:
        params_dict['vr_type'] = vr_type
    
    response = client.get(url, params=params_dict)
    return response


def site_list(client: DMEAPIClient) -> dict:
    url = "/rest/vmmgmt/v1/sites/query"
    
    response = client.post(url, body={})
    return response


def site_show(client: DMEAPIClient, site_id: str) -> dict:
    url = "/rest/vmmgmt/v1/sites/{site_id}"
    
    response = client.get(url, params={"site_id": site_id})
    return response




def host_adapter_list(client: DMEAPIClient, host_id: str) -> dict:
    url = "/rest/vmmgmt/v1/hosts/{host_id}/storage-adapters"
    
    response = client.get(url, params={"host_id": host_id})
    return response


def disk_list(client: DMEAPIClient, site_id: str = None,
                         host_id: str = None, name: str = None,
                         disk_type: list = None, status: list = None,
                         page_no: int = 1, page_size: int = 20) -> dict:
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
    url = "/rest/vmmgmt/v1/vdisks/{virtual_disk_id}"
    
    response = client.get(url, params={"virtual_disk_id": virtual_disk_id})
    return response


# 动作列表，用于 CLI 帮助
ACTIONS = {
    # 虚拟机管理
    'vm_list': {
        'func': vm_list,
        'params': ['site_id', 'cluster_id', 'dc_id', 'cluster_name', 'host_id', 
                   'host_name', 'name', 'ip_address', 'status', 'is_template', 
                   'os_type', 'vr_type', 'datacenter_id', 'sort_key', 'sort_dir', 
                   'page_no', 'page_size'],
        'subtopic': 'vm'
    },
    'vm_show': {
        'func': vm_show,
        'params': ['vm_id', 'vr_type'],
        'subtopic': 'vm'
    },
    # 数据存储管理
    'datastore_list': {
        'func': datastore_list,
        'params': ['site_id', 'cluster_id', 'host_id', 'dc_id', 'name', 
                   'status', 'storage_type', 'allocate_type', 'vr_type',
                   'datacenter_id', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'datastore'
    },
    'datastore_show': {
        'func': datastore_show,
        'params': ['datastore_id', 'vr_type'],
        'subtopic': 'datastore'
    },
    # 主机管理
    'host_list': {
        'func': host_list,
        'params': ['site_id', 'cluster_id', 'dc_id', 'host_name', 'ip_address',
                   'status', 'vr_type', 'page_no', 'page_size'],
        'subtopic': 'host'
    },
    'host_show': {
        'func': host_show,
        'params': ['host_id', 'vr_type'],
        'subtopic': 'host'
    },
    'host_adapter_list': {
        'func': host_adapter_list,
        'params': ['host_id'],
        'subtopic': 'host'
    },
    # 集群管理
    'cluster_list': {
        'func': cluster_list,
        'params': ['site_id', 'dc_id', 'name', 'vr_type', 'page_no', 'page_size'],
        'subtopic': 'cluster'
    },
    'cluster_show': {
        'func': cluster_show,
        'params': ['cluster_id', 'vr_type'],
        'subtopic': 'cluster'
    },
    # 站点管理
    'site_list': {
        'func': site_list,
        'params': [],
        'subtopic': 'site'
    },
    'site_show': {
        'func': site_show,
        'params': ['site_id'],
        'subtopic': 'site'
    },
    # 物理盘管理
    'disk_list': {
        'func': disk_list,
        'params': ['site_id', 'host_id', 'name', 'disk_type', 'status', 'page_no', 'page_size'],
        'subtopic': 'disk'
    },
    # 虚拟磁盘管理
    'vdisk_list': {
        'func': vdisk_list,
        'params': ['site_id', 'vm_id', 'name', 'disk_type', 'status', 'page_no', 'page_size'],
        'subtopic': 'vdisk'
    },
    'vdisk_show': {
        'func': vdisk_show,
        'params': ['virtual_disk_id'],
        'subtopic': 'vdisk'
    },
}
