"""
Virtualization service related operations
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
    Query virtual machine list
    
    Args:
        client: DME API client
        site_id: Site ID the VM belongs to
        cluster_id: Cluster ID the VM belongs to (not supported in HCS scenario)
        dc_id: Data center ID (only supported in FusionCompute scenario)
        cluster_name: Cluster name the VM belongs to (supports fuzzy search, not supported in HCS scenario)
        host_id: Unique identifier of the physical host the VM belongs to
        host_name: Host name the VM belongs to (supports fuzzy search)
        name: VM name (supports fuzzy search)
        ip_address: VM IP address (supports fuzzy search)
        status: VM status list
                values: running, stopped, unknown, hibernated, creating, shutting-down,
                     migrating, fault-resuming, starting, stopping, hibernating, pause,
                     recycling, deactivated, active, saving, deleted, other, uploading,
                     pending_delete, queued, importing, killed, storage_migrating,
                     building, error
        is_template: Whether it is a template (true/false)
        os_type: OS type list (Windows, Linux, Other)
        vr_type: Virtualization platform type (FUSIONCOMPUTE, VMWARE, HCS)
        datacenter_id: Data store data center ID (only supported in vCenter scenario)
        sort_key: Sort field (name, cpu_core, memory_size, disk_total_size, create_time, ip_address)
        sort_dir: Sort direction (asc, desc), default asc
        page_no: Pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            total: Total number of VMs (integer),
            vms: VM list (List<VmInfo>). parameter format: [{
                id: VM ID (string),
                name: VM name (string),
                status: status (string),
                cpu: CPU core count (integer),
                memory: Memory size (integer),
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
    Query specified VM details
    
    Query detailed info of a virtual machine.
    
    Args:
        client: DME API client
        vm_id: VM ID (Required)
        vr_type: Virtualization platform type (Optional)
    
    Returns:
        {
            id: VM ID (string),
            name: name (string),
            status: status (string),
            cpu: CPU info. attribute format: {
                cores: CPU core count (int32),
                sockets: CPU socket count (int32),
            },
            memory: Memory size (int64, MB),
            vm_nics: NIC list (List<VmNicInfo>). parameter format: [{
                id: NIC ID (string),
                name: NIC name (string),
                mac: MAC address (string),
            }, ...],
            vm_disks: Disk list (List<VmDiskInfo>). parameter format: [{
                id: Disk ID (string),
                name: Disk name (string),
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
    Query data store list
    
    Args:
        client: DME API client
        site_id: Site ID of the data store
        cluster_id: Cluster ID associated with the data store
        host_id: Host ID associated with the data store
        dc_id: Data center ID of the data store
        name: Data store name (supports fuzzy query)
        status: Data store status list
                values: NORMAL, ABNORMAL, CREATING, DELETING, READONLY, EXPANDING,
                     RESTORING, WARNING, ALERT, UNKNOWN, WRITE_PROTECT
        storage_type: Data store type list
                       values: LOCAL, SAN, ADVANCESAN, DSWARE, NAS, LOCALPOME, LUNPOME,
                           LUN, iotailor, CIFS, NFS, NFS41, PMEM, VFFS, VMFS, VSAN, VVOL, OTHER
        allocate_type: Whether thin provisioning is supported (only supported in FusionCompute scenario)
        vr_type: Virtualization platform type (FUSIONCOMPUTE, VMWARE, HCS)
        datacenter_id: vCenter data center ID the data store belongs to (only supported in vCenter scenario)
        sort_key: Sort field (name, host_num, vm_num, total_capacity, used_size, free_capacity, lun_count, used_rate)
        sort_dir: Sort direction (asc, desc), default asc
        page_no: Pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            total: total count (int),
            datastores: datastore list (List),
        }
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
    Query specified data store details
    
    Query detailed info of a data store.
    
    Args:
        client: DME API client
        datastore_id: Data store ID (Required)
        vr_type: Virtualization platform type (Optional)
    
    Returns:
        {
            id: Data store ID (string),
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
    Query host list
    
    Query physical host list, supports multiple filter criteria.
    
    Args:
        client: DME API client
        site_id: Site ID of the host
        cluster_id: Cluster ID of the host
        dc_id: Data center ID
        host_name: Host name (supports fuzzy search)
        ip_address: Host IP address
        status: Host status list
        vr_type: Virtualization platform type
        page_no: Pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            total: total count (int),
            hosts: host list (List),
        }
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
    Query specified host details
    
    Query detailed info of a physical host.
    
    Args:
        client: DME API client
        host_id: Host ID (Required)
        vr_type: Virtualization platform type (Optional)
    
    Returns:
        {
            id: host ID (string),
            name: name (string),
            ip: IP address (string),
            status: status (string),
            cpu_cores: CPU core count (int32),
            memory: Memory size (int64, MB),
            os_type: OS type (string),
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
    Query cluster list
    
    Args:
        client: DME API client
        site_id: Site ID of the cluster
        dc_id: Data center ID
        name: Cluster name (supports fuzzy search)
        vr_type: Virtualization platform type
        page_no: Pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            total: total count (int),
            clusters: cluster list (List),
        }
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
    Query specified cluster details
    
    Query detailed info of a cluster.
    
    Args:
        client: DME API client
        cluster_id: Cluster ID (Required)
        vr_type: Virtualization platform type (Optional)
    
    Returns:
        {
            id: Cluster ID (string),
            name: name (string),
            type: type (string),
            host_count: Host count (int32),
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
    Query site list
    
    Query all virtualization site list.
    
    Args:
        client: DME API client
    
    Returns:
        {
            total: total count (int),
            sites: site list (List),
        }
    """
    url = "/rest/vmmgmt/v1/sites/query"
    
    response = client.post(url, body={})
    return response


def site_show(client: DMEAPIClient, site_id: str) -> dict:
    """
    Query specified site details
    
    Query detailed info of a virtualization site.
    
    Args:
        client: DME API client
        site_id: Site ID (Required)
    
    Returns:
        {
            id: Site ID (string),
            name: name (string),
            status: status (string),
        }
    """
    url = "/rest/vmmgmt/v1/sites/{site_id}"
    
    response = client.get(url, params={"site_id": site_id})
    return response




def host_adapter_list(client: DMEAPIClient, host_id: str) -> dict:
    """
    Query specified host storage adapter list
    
    Query the storage adapters of a physical host.
    
    Args:
        client: DME API client
        host_id: Host ID (Required)
    
    Returns:
        {
            total: Adapter count (int32),
            adapters: Storage adapter list (List<HostAdapterInfo>). parameter format: [{
                id: Adapter ID (string),
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
    Query physical disk info
    
    Query physical disk list, supports multiple filter criteria.
    
    Args:
        client: DME API client
        site_id: Site ID of the physical disk (Optional)
        host_id: Host ID of the physical disk (Optional)
        name: Physical disk name (Optional)
        disk_type: Disk type list (Optional)
        status: Disk status list (Optional)
        page_no: Pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            total: Disk count (int32),
            disks: Physical disk list (List<PhysicalDiskInfo>). parameter format: [{
                id: Disk ID (string),
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
    Query virtual disk info list
    
    Query virtual disk list, supports multiple filter criteria.
    
    Args:
        client: DME API client
        site_id: Site ID of the virtual disk (Optional)
        vm_id: VM ID of the virtual disk (Optional)
        name: Virtual disk name (Optional)
        disk_type: Disk type list (Optional)
        status: Disk status list (Optional)
        page_no: Pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            total: Virtual disk count (int32),
            vdisks: Virtual disk list (List<VirtualDiskInfo>). parameter format: [{
                id: Virtual disk ID (string),
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
    Query specified virtual disk info
    
    Query detailed info of a virtual disk.
    
    Args:
        client: DME API client
        virtual_disk_id: Virtual disk ID (Required)
    
    Returns:
        {
            id: Virtual disk ID (string),
            name: name (string),
            capacity: capacity (int64, GB),
            status: status (string),
            datastore_id: Data store ID (string),
        }
    """
    url = "/rest/vmmgmt/v1/vdisks/{virtual_disk_id}"
    
    response = client.get(url, params={"virtual_disk_id": virtual_disk_id})
    return response


# action list, for CLI help
ACTIONS = {
    # VM management
    'vm_list': {
        'func': vm_list,
        'description': 'Query virtual machine list',
        'params': ['site_id', 'cluster_id', 'dc_id', 'cluster_name', 'host_id', 
                   'host_name', 'name', 'ip_address', 'status', 'is_template', 
                   'os_type', 'vr_type', 'datacenter_id', 'sort_key', 'sort_dir', 
                   'page_no', 'page_size'],
        'subtopic': 'vm'
    },
    'vm_show': {
        'func': vm_show,
        'description': 'Query specified VM details',
        'params': ['vm_id', 'vr_type'],
        'subtopic': 'vm'
    },
    # Data store management
    'datastore_list': {
        'func': datastore_list,
        'description': 'Query data store list',
        'params': ['site_id', 'cluster_id', 'host_id', 'dc_id', 'name', 
                   'status', 'storage_type', 'allocate_type', 'vr_type',
                   'datacenter_id', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'datastore'
    },
    'datastore_show': {
        'func': datastore_show,
        'description': 'Query specified data store details',
        'params': ['datastore_id', 'vr_type'],
        'subtopic': 'datastore'
    },
    # Host management
    'host_list': {
        'func': host_list,
        'description': 'Query host list',
        'params': ['site_id', 'cluster_id', 'dc_id', 'host_name', 'ip_address',
                   'status', 'vr_type', 'page_no', 'page_size'],
        'subtopic': 'host'
    },
    'host_show': {
        'func': host_show,
        'description': 'Query specified host details',
        'params': ['host_id', 'vr_type'],
        'subtopic': 'host'
    },
    'host_adapter_list': {
        'func': host_adapter_list,
        'description': 'Query specified host storage adapter list',
        'params': ['host_id'],
        'subtopic': 'host'
    },
    # Cluster management
    'cluster_list': {
        'func': cluster_list,
        'description': 'Query cluster list',
        'params': ['site_id', 'dc_id', 'name', 'vr_type', 'page_no', 'page_size'],
        'subtopic': 'cluster'
    },
    'cluster_show': {
        'func': cluster_show,
        'description': 'Query specified cluster details',
        'params': ['cluster_id', 'vr_type'],
        'subtopic': 'cluster'
    },
    # Site management
    'site_list': {
        'func': site_list,
        'description': 'Query site list',
        'params': [],
        'subtopic': 'site'
    },
    'site_show': {
        'func': site_show,
        'description': 'Query specified site details',
        'params': ['site_id'],
        'subtopic': 'site'
    },
    # Physical disk management
    'disk_list': {
        'func': disk_list,
        'description': 'Query physical disk info',
        'params': ['site_id', 'host_id', 'name', 'disk_type', 'status', 'page_no', 'page_size'],
        'subtopic': 'disk'
    },
    # Virtual disk management
    'vdisk_list': {
        'func': vdisk_list,
        'description': 'Query virtual disk info list',
        'params': ['site_id', 'vm_id', 'name', 'disk_type', 'status', 'page_no', 'page_size'],
        'subtopic': 'vdisk'
    },
    'vdisk_show': {
        'func': vdisk_show,
        'description': 'Query specified virtual disk info',
        'params': ['virtual_disk_id'],
        'subtopic': 'vdisk'
    },
}
