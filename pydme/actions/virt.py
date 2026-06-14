"""
Virtualization service (Virtualization) operations
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
     queryVM list
    
    Args:
        client: DME API client
        site_id: Virtual machine site ID
        cluster_id: Virtual machine cluster ID (HCS  scenario not support) 
        dc_id: Data center ID (FusionCompute only) 
        cluster_name: Virtual machineCluster name (supports fuzzy search, HCS  scenario not support) 
        host_id: Virtual machinePhysical hostUnique identifier
        host_name: Virtual machineHost name (supports fuzzy search) 
        name: Virtual machine name (supports fuzzy search) 
        ip_address: Virtual machine IP  address (supports fuzzy search) 
        status: Virtual machinestatus list
                 value: running, stopped, unknown, hibernated, creating, shutting-down,
                     migrating, fault-resuming, starting, stopping, hibernating, pause,
                     recycling, deactivated, active, saving, deleted, other, uploading,
                     pending_delete, queued, importing, killed, storage_migrating,
                     building, error
        is_template:  whether template (true/false) 
        os_type: OS type list (Windows, Linux, Other) 
        vr_type: Virtualization platform type (FUSIONCOMPUTE, VMWARE, HCS) 
        datacenter_id: Datastore data center ID (vCenter only) 
        sort_key: Sort field (name, cpu_core, memory_size, disk_total_size, create_time, ip_address) 
        sort_dir: Sort direction (asc, desc) , default asc
        page_no: Page queryStart page, default 1
        page_size: per pagecount, 1~1000, default 20
    
    Returns:
        {
            total: Virtual machineTotal count (integer),
            vms: VM list (List<VmInfo>).  parameter format: [{
                id: Virtual machineID (string),
                name: Virtual machine name (string),
                status:  status (string),
                cpu: CPUcount (integer),
                memory:  memory size (integer),
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
    QueryVirtual machine details
    
     Query virtual machine details.
    
    Args:
        client: DME API client
        vm_id: Virtual machine ID (Required) 
        vr_type: Virtualization platform type (Optional) 
    
    Returns:
        Virtual machineDetails, includes  CPU,  memory,  disk,  NIC etcConfiguration info
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
    Query datastore list
    
    Args:
        client: DME API client
        site_id: Datastore located site ID
        cluster_id: Datastoreassociated clusters ID
        host_id: Datastoreassociated hosts ID
        dc_id: Datastore data center ID
        name: Datastore name (supports fuzzy search) 
        status: Datastorestatus list
                 value: NORMAL, ABNORMAL, CREATING, DELETING, READONLY, EXPANDING,
                     RESTORING, WARNING, ALERT, UNKNOWN, WRITE_PROTECT
        storage_type:  dataStorage class型 list
                       value: LOCAL, SAN, ADVANCESAN, DSWARE, NAS, LOCALPOME, LUNPOME,
                           LUN, iotailor, CIFS, NFS, NFS41, PMEM, VFFS, VMFS, VSAN, VVOL, OTHER
        allocate_type: supports精简 mode (FusionCompute only) 
        vr_type: Virtualization platform type (FUSIONCOMPUTE, VMWARE, HCS) 
        datacenter_id: Datastore的 vCenter Data center ID (vCenter only) 
        sort_key: Sort field (name, host_num, vm_num, total_capacity, used_size, free_capacity, lun_count, used_rate) 
        sort_dir: Sort direction (asc, desc) , default asc
        page_no: Page queryStart page, default 1
        page_size: per pagecount, 1~1000, default 20
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes  total 和 datastores  field
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
    QueryDatastore details
    
     queryDatastore的Details. 
    
    Args:
        client: DME API client
        datastore_id: Datastore ID (Required) 
        vr_type: Virtualization platform type (Optional) 
    
    Returns:
        DatastoreDetails
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
    Query host list
    
     queryPhysical host list, supports multiple filter criteria. 
    
    Args:
        client: DME API client
        site_id: Host site ID
        cluster_id: Host cluster ID
        dc_id: Data center ID
        host_name: Host name (supports fuzzy search) 
        ip_address:  host IP  address
        status: Host status list
        vr_type: Virtualization platform type
        page_no: Page queryStart page, default 1
        page_size: per pagecount, 1~1000, default 20
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes host list
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
    QueryHost details
    
     queryPhysical host的Details. 
    
    Args:
        client: DME API client
        host_id:  host ID (Required) 
        vr_type: Virtualization platform type (Optional) 
    
    Returns:
         hostDetails
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
    Query cluster list
    
    Args:
        client: DME API client
        site_id: Cluster site ID
        dc_id: Data center ID
        name: Cluster name (supports fuzzy search) 
        vr_type: Virtualization platform type
        page_no: Page queryStart page, default 1
        page_size: per pagecount, 1~1000, default 20
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes cluster list
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
    Query cluster details
    
     query cluster的Details. 
    
    Args:
        client: DME API client
        cluster_id:  cluster ID (Required) 
        vr_type: Virtualization platform type (Optional) 
    
    Returns:
         clusterDetails
    """
    url = "/rest/vmmgmt/v1/clusters/{cluster_id}"
    
    params_dict = {}
    if vr_type is not None:
        params_dict['vr_type'] = vr_type
    
    response = client.get(url, params=params_dict)
    return response


def site_list(client: DMEAPIClient) -> dict:
    """
    Query site list
    
    Query allVirtualization site list. 
    
    Args:
        client: DME API client
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes site list
    """
    url = "/rest/vmmgmt/v1/sites/query"
    
    response = client.post(url, body={})
    return response


def site_show(client: DMEAPIClient, site_id: str) -> dict:
    """
    Query site details
    
    Query virtualization siteDetails. 
    
    Args:
        client: DME API client
        site_id:  site ID (Required) 
    
    Returns:
         siteDetails
    """
    url = "/rest/vmmgmt/v1/sites/{site_id}"
    
    response = client.get(url, params={"site_id": site_id})
    return response




def host_adapter_list(client: DMEAPIClient, host_id: str) -> dict:
    """
    QueryHost storage adapter list
    
     queryPhysical host的Storage adapter list. 
    
    Args:
        client: DME API client
        host_id:  host ID (Required) 
    
    Returns:
        Storage adapter list
    """
    url = "/rest/vmmgmt/v1/hosts/{host_id}/storage-adapters"
    
    response = client.get(url, params={"host_id": host_id})
    return response


def disk_list(client: DMEAPIClient, site_id: str = None,
                         host_id: str = None, name: str = None,
                         disk_type: list = None, status: list = None,
                         page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query physical disk info
    
    Query physical disk list, supports multiple filter criteria. 
    
    Args:
        client: DME API client
        site_id: Physical disk site ID (Optional) 
        host_id:  physical diskHost ID (Optional) 
        name:  physical disk name (Optional) 
        disk_type: Disk type list (Optional) 
        status: Disk status list (Optional) 
        page_no: Page queryStart page, default 1
        page_size: per pagecount, 1~1000, default 20
    
    Returns:
        Physical disk list
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
    Query virtual disk info list
    
     queryVirtual disk list, supports multiple filter criteria. 
    
    Args:
        client: DME API client
        site_id: Virtual disk site ID (Optional) 
        vm_id: Virtual diskVirtual machine ID (Optional) 
        name: Virtual disk name (Optional) 
        disk_type: Disk type list (Optional) 
        status: Disk status list (Optional) 
        page_no: Page queryStart page, default 1
        page_size: per pagecount, 1~1000, default 20
    
    Returns:
        Virtual disk list
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
    QueryVirtual disk info
    
     queryVirtual disk的Details. 
    
    Args:
        client: DME API client
        virtual_disk_id: Virtual disk ID (Required) 
    
    Returns:
        Virtual diskDetails
    """
    url = "/rest/vmmgmt/v1/vdisks/{virtual_disk_id}"
    
    response = client.get(url, params={"virtual_disk_id": virtual_disk_id})
    return response


# Action list for CLI help
ACTIONS = {
    # Virtual machinemanagement 
    'vm_list': {
        'func': vm_list,
        'description': ' queryVM list',
        'params': ['site_id', 'cluster_id', 'dc_id', 'cluster_name', 'host_id', 
                   'host_name', 'name', 'ip_address', 'status', 'is_template', 
                   'os_type', 'vr_type', 'datacenter_id', 'sort_key', 'sort_dir', 
                   'page_no', 'page_size'],
        'subtopic': 'vm'
    },
    'vm_show': {
        'func': vm_show,
        'description': 'QueryVirtual machine details',
        'params': ['vm_id', 'vr_type'],
        'subtopic': 'vm'
    },
    # Datastoremanagement 
    'datastore_list': {
        'func': datastore_list,
        'description': 'Query datastore list',
        'params': ['site_id', 'cluster_id', 'host_id', 'dc_id', 'name', 
                   'status', 'storage_type', 'allocate_type', 'vr_type',
                   'datacenter_id', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'datastore'
    },
    'datastore_show': {
        'func': datastore_show,
        'description': 'QueryDatastore details',
        'params': ['datastore_id', 'vr_type'],
        'subtopic': 'datastore'
    },
    #  hostmanagement 
    'host_list': {
        'func': host_list,
        'description': 'Query host list',
        'params': ['site_id', 'cluster_id', 'dc_id', 'host_name', 'ip_address',
                   'status', 'vr_type', 'page_no', 'page_size'],
        'subtopic': 'host'
    },
    'host_show': {
        'func': host_show,
        'description': 'QueryHost details',
        'params': ['host_id', 'vr_type'],
        'subtopic': 'host'
    },
    'host_adapter_list': {
        'func': host_adapter_list,
        'description': 'QueryHost storage adapter list',
        'params': ['host_id'],
        'subtopic': 'host'
    },
    #  clustermanagement 
    'cluster_list': {
        'func': cluster_list,
        'description': 'Query cluster list',
        'params': ['site_id', 'dc_id', 'name', 'vr_type', 'page_no', 'page_size'],
        'subtopic': 'cluster'
    },
    'cluster_show': {
        'func': cluster_show,
        'description': 'Query cluster details',
        'params': ['cluster_id', 'vr_type'],
        'subtopic': 'cluster'
    },
    #  sitemanagement 
    'site_list': {
        'func': site_list,
        'description': 'Query site list',
        'params': [],
        'subtopic': 'site'
    },
    'site_show': {
        'func': site_show,
        'description': 'Query site details',
        'params': ['site_id'],
        'subtopic': 'site'
    },
    #  physical diskmanagement 
    'disk_list': {
        'func': disk_list,
        'description': 'Query physical disk info',
        'params': ['site_id', 'host_id', 'name', 'disk_type', 'status', 'page_no', 'page_size'],
        'subtopic': 'disk'
    },
    # Virtual diskmanagement 
    'vdisk_list': {
        'func': vdisk_list,
        'description': 'Query virtual disk info list',
        'params': ['site_id', 'vm_id', 'name', 'disk_type', 'status', 'page_no', 'page_size'],
        'subtopic': 'vdisk'
    },
    'vdisk_show': {
        'func': vdisk_show,
        'description': 'QueryVirtual disk info',
        'params': ['virtual_disk_id'],
        'subtopic': 'vdisk'
    },
}
