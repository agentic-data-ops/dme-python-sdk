"""
Virtualization service (Virtualization) related operations
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


def datastore_host_relations(client: DMEAPIClient, ds_id: str = None,
                             host_id: str = None, page_no: int = 1,
                             page_size: int = 20) -> dict:
    url = "/rest/vmmgmt/v1/datastores/datastore-host-relations/query"

    body_params = {
        'page_no': page_no,
        'page_size': page_size
    }

    if ds_id is not None:
        body_params['ds_id'] = ds_id
    if host_id is not None:
        body_params['host_id'] = host_id

    response = client.post(url, body=body_params)
    return response


def host_port_list(client: DMEAPIClient, host_id: str,
                   uplinkportaggrs_id: str = None) -> dict:
    url = "/rest/vmmgmt/v1/hosts/{host_id}/ports"

    params_dict = {"host_id": host_id}
    if uplinkportaggrs_id is not None:
        params_dict['uplinkportaggrs_id'] = uplinkportaggrs_id

    response = client.get(url, params=params_dict)
    return response


def host_aggr_port_list(client: DMEAPIClient, host_id: str) -> dict:
    url = "/rest/vmmgmt/v1/hosts/{host_id}/uplink-port-aggrs"

    response = client.get(url, params={"host_id": host_id})
    return response


def host_logic_port_list(client: DMEAPIClient, host_id: str) -> dict:
    url = "/rest/vmmgmt/v1/hosts/{host_id}/system-intfs"

    response = client.get(url, params={"host_id": host_id})
    return response


def vdisk_create_attach(client: DMEAPIClient, vm_id: str, datastore_id: str,
                        capacity: int, share_type: str,
                        pci_type: str = "VIRTIO",
                        scsi_command_passthrough: bool = False,
                        io_mode: str = "threads", name: str = None,
                        is_thin: bool = False, allocate_type: int = 0,
                        is_indep_disk: bool = True,
                        is_persistent_disk: bool = True,
                        metadata_preallocate: bool = None) -> dict:
    url = "/rest/vmmgmt/v2/vms/{vm_id}/vdisk/create-and-attach"

    body_params = {
        'datastore_id': datastore_id,
        'capacity': capacity,
        'share_type': share_type,
        'pci_type': pci_type,
        'scsi_command_passthrough': scsi_command_passthrough,
        'io_mode': io_mode,
        'is_thin': is_thin,
        'allocate_type': allocate_type,
        'is_indep_disk': is_indep_disk,
        'is_persistent_disk': is_persistent_disk
    }

    if name is not None:
        body_params['name'] = name
    if metadata_preallocate is not None:
        body_params['metadata_preallocate'] = metadata_preallocate

    response = client.post(url, params={"vm_id": vm_id}, body=body_params)
    return response


def vdisk_attach(client: DMEAPIClient, vm_id: str, vdisk_id: str,
                 pci_type: str = "VIRTIO",
                 scsi_command_passthrough: bool = True,
                 io_mode: str = None) -> dict:
    url = "/rest/vmmgmt/v1/vms/{vm_id}/vdisk/attach"

    body_params = {
        'vdisk_id': vdisk_id,
        'pci_type': pci_type,
        'scsi_command_passthrough': scsi_command_passthrough
    }

    if io_mode is not None:
        body_params['io_mode'] = io_mode

    response = client.post(url, params={"vm_id": vm_id}, body=body_params)
    return response


def vdisk_detach(client: DMEAPIClient, vm_id: str, vdisk_id: str) -> dict:
    url = "/rest/vmmgmt/v1/vms/{vm_id}/vdisk/detach"

    body_params = {
        'vdisk_id': vdisk_id
    }

    response = client.post(url, params={"vm_id": vm_id}, body=body_params)
    return response


def vdisk_modify(client: DMEAPIClient, virtual_disk_id: str,
                 name: str = None, is_indep_disk: bool = None,
                 is_persistent_disk: bool = None) -> dict:
    url = "/rest/vmmgmt/v1/vdisks/{virtual_disk_id}"

    body_params = {}

    if name is not None:
        body_params['name'] = name
    if is_indep_disk is not None:
        body_params['is_indep_disk'] = is_indep_disk
    if is_persistent_disk is not None:
        body_params['is_persistent_disk'] = is_persistent_disk

    response = client.put(url, params={"virtual_disk_id": virtual_disk_id},
                          body=body_params)
    return response


def vdisk_expand(client: DMEAPIClient, vm_id: str, vdisk_id: str,
                 capacity: int) -> dict:
    url = "/rest/vmmgmt/v1/vms/{vm_id}/vdisk/expand"

    body_params = {
        'vdisk_id': vdisk_id,
        'capacity': capacity
    }

    response = client.post(url, params={"vm_id": vm_id}, body=body_params)
    return response


def vdisk_delete(client: DMEAPIClient, virtual_disk_id: str) -> dict:
    url = "/rest/vmmgmt/v1/vdisks/{virtual_disk_id}"

    response = client.delete(url, params={"virtual_disk_id": virtual_disk_id})
    return response


def vswitch_list(client: DMEAPIClient, host_id: str = None,
                 site_id: str = None, site_ip: str = None,
                 cluster_id: str = None, dc_id: str = None, name: str = None,
                 type: list = None, sort_dir: str = "asc",
                 sort_key: str = None, page_no: int = 1,
                 page_size: int = 20) -> dict:
    url = "/rest/vmmgmt/v1/dvswitchs/query"

    body_params = {
        'page_no': page_no,
        'page_size': page_size,
        'sort_dir': sort_dir
    }

    if host_id is not None:
        body_params['host_id'] = host_id
    if site_id is not None:
        body_params['site_id'] = site_id
    if site_ip is not None:
        body_params['site_ip'] = site_ip
    if cluster_id is not None:
        body_params['cluster_id'] = cluster_id
    if dc_id is not None:
        body_params['dc_id'] = dc_id
    if name is not None:
        body_params['name'] = name
    if type is not None:
        body_params['type'] = type
    if sort_key is not None:
        body_params['sort_key'] = sort_key

    response = client.post(url, body=body_params)
    return response


def vswitch_show(client: DMEAPIClient, dvswitch_id: str) -> dict:
    url = "/rest/vmmgmt/v1/dvswitchs/{dvswitch_id}"

    response = client.get(url, params={"dvswitch_id": dvswitch_id})
    return response


def vswitch_portgroup_list(client: DMEAPIClient, dvswitch_id: str,
                           name: str = None, port_type: list = None,
                           sort_dir: str = "asc", sort_key: str = None,
                           page_no: int = 1, page_size: int = 1000) -> dict:
    url = "/rest/vmmgmt/v1/dvswitchs/{dvswitch_id}/portgroups/query"

    body_params = {
        'page_no': page_no,
        'page_size': page_size,
        'sort_dir': sort_dir
    }

    if name is not None:
        body_params['name'] = name
    if port_type is not None:
        body_params['port_type'] = port_type
    if sort_key is not None:
        body_params['sort_key'] = sort_key

    response = client.post(url, params={"dvswitch_id": dvswitch_id},
                           body=body_params)
    return response


def vswitch_portgroup_create(client: DMEAPIClient, dvswitch_id: str,
                             name: str, port_type: int,
                             vlan_id: int = None, vlan_range: str = None,
                             description: str = None,
                             is_ip_mac_bind: bool = None,
                             is_dhcp_isolation: bool = None,
                             is_calc_tcp_check_sum: bool = None,
                             ip_bcst_suppress: bool = None,
                             tx_limit: int = None, tx_peak_limit: int = None,
                             tx_burst_size: int = None, priority: int = 7,
                             rx_limit: int = None, rx_peak_limit: int = None,
                             rx_burst_size: int = None) -> dict:
    url = "/rest/vmmgmt/v1/dvswitchs/{dvswitch_id}/portgroups"

    body_params = {
        'name': name,
        'port_type': port_type,
        'priority': priority
    }

    if vlan_id is not None:
        body_params['vlan_id'] = vlan_id
    if vlan_range is not None:
        body_params['vlan_range'] = vlan_range
    if description is not None:
        body_params['description'] = description
    if is_ip_mac_bind is not None:
        body_params['is_ip_mac_bind'] = is_ip_mac_bind
    if is_dhcp_isolation is not None:
        body_params['is_dhcp_isolation'] = is_dhcp_isolation
    if is_calc_tcp_check_sum is not None:
        body_params['is_calc_tcp_check_sum'] = is_calc_tcp_check_sum
    if ip_bcst_suppress is not None:
        body_params['ip_bcst_suppress'] = ip_bcst_suppress
    if tx_limit is not None:
        body_params['tx_limit'] = tx_limit
    if tx_peak_limit is not None:
        body_params['tx_peak_limit'] = tx_peak_limit
    if tx_burst_size is not None:
        body_params['tx_burst_size'] = tx_burst_size
    if rx_limit is not None:
        body_params['rx_limit'] = rx_limit
    if rx_peak_limit is not None:
        body_params['rx_peak_limit'] = rx_peak_limit
    if rx_burst_size is not None:
        body_params['rx_burst_size'] = rx_burst_size

    response = client.post(url, params={"dvswitch_id": dvswitch_id},
                           body=body_params)
    return response


def vswitch_portgroup_modify(client: DMEAPIClient, dvswitch_id: str,
                             portgroup_id: str, name: str, port_type: int,
                             vlan_id: int = None, vlan_range: str = None,
                             description: str = None,
                             is_ip_mac_bind: bool = None,
                             is_dhcp_isolation: bool = None,
                             is_calc_tcp_check_sum: bool = None,
                             ip_bcst_suppress: bool = None,
                             tx_limit: int = None, tx_peak_limit: int = None,
                             tx_burst_size: int = None, priority: int = 7,
                             rx_limit: int = None, rx_peak_limit: int = None,
                             rx_burst_size: int = None) -> dict:
    url = "/rest/vmmgmt/v1/dvswitchs/{dvswitch_id}/portgroups/{portgroup_id}"

    body_params = {
        'name': name,
        'port_type': port_type,
        'priority': priority
    }

    if vlan_id is not None:
        body_params['vlan_id'] = vlan_id
    if vlan_range is not None:
        body_params['vlan_range'] = vlan_range
    if description is not None:
        body_params['description'] = description
    if is_ip_mac_bind is not None:
        body_params['is_ip_mac_bind'] = is_ip_mac_bind
    if is_dhcp_isolation is not None:
        body_params['is_dhcp_isolation'] = is_dhcp_isolation
    if is_calc_tcp_check_sum is not None:
        body_params['is_calc_tcp_check_sum'] = is_calc_tcp_check_sum
    if ip_bcst_suppress is not None:
        body_params['ip_bcst_suppress'] = ip_bcst_suppress
    if tx_limit is not None:
        body_params['tx_limit'] = tx_limit
    if tx_peak_limit is not None:
        body_params['tx_peak_limit'] = tx_peak_limit
    if tx_burst_size is not None:
        body_params['tx_burst_size'] = tx_burst_size
    if rx_limit is not None:
        body_params['rx_limit'] = rx_limit
    if rx_peak_limit is not None:
        body_params['rx_peak_limit'] = rx_peak_limit
    if rx_burst_size is not None:
        body_params['rx_burst_size'] = rx_burst_size

    response = client.put(url, params={"dvswitch_id": dvswitch_id,
                                       "portgroup_id": portgroup_id},
                          body=body_params)
    return response


def vswitch_portgroup_delete(client: DMEAPIClient, dvswitch_id: str,
                             portgroup_id: str) -> dict:
    url = "/rest/vmmgmt/v1/dvswitchs/{dvswitch_id}/portgroups/{portgroup_id}"

    response = client.delete(url, params={"dvswitch_id": dvswitch_id,
                                          "portgroup_id": portgroup_id})
    return response


def secgroup_list(client: DMEAPIClient, dc_id: str, page_size: int = 20,
                  page_no: int = 1) -> dict:
    url = "/rest/vmmgmt/v1/secgroups/query"

    body_params = {
        'dc_id': dc_id,
        'page_size': page_size,
        'page_no': page_no
    }

    response = client.post(url, body=body_params)
    return response


def gpu_list(client: DMEAPIClient, site_id: str = None,
             vendor_name: str = None, product_name: str = None,
             host_id: str = None, vm_id: str = None, page_no: int = 1,
             page_size: int = 20, sort_dir: str = "asc",
             sort_key: str = "pci_address") -> dict:
    url = "/rest/vmmgmt/v1/host-gpus/query"

    body_params = {
        'page_no': page_no,
        'page_size': page_size,
        'sort_dir': sort_dir,
        'sort_key': sort_key
    }

    if site_id is not None:
        body_params['site_id'] = site_id
    if vendor_name is not None:
        body_params['vendor_name'] = vendor_name
    if product_name is not None:
        body_params['product_name'] = product_name
    if host_id is not None:
        body_params['host_id'] = host_id
    if vm_id is not None:
        body_params['vm_id'] = vm_id

    response = client.post(url, body=body_params)
    return response


def vm_create(client: DMEAPIClient, name: str, location: str, auto_boot: bool,
              os_options: dict, vm_config: dict,
              externalUuid: str = None, floppy_file: str = None,
              floppy_protocol: str = "unMount", description: str = None,
              is_binding_host: bool = False, tag_ids: list = None,
              group_id: str = None) -> dict:
    url = "/rest/vmmgmt/v1/vms"

    body_params = {
        'name': name,
        'location': location,
        'auto_boot': auto_boot,
        'os_options': os_options,
        'vm_config': vm_config
    }

    if externalUuid is not None:
        body_params['externalUuid'] = externalUuid
    if floppy_file is not None:
        body_params['floppy_file'] = floppy_file
    if floppy_protocol is not None:
        body_params['floppy_protocol'] = floppy_protocol
    if description is not None:
        body_params['description'] = description
    if is_binding_host is not None:
        body_params['is_binding_host'] = is_binding_host
    if tag_ids is not None:
        body_params['tag_ids'] = tag_ids
    if group_id is not None:
        body_params['group_id'] = group_id

    response = client.post(url, body=body_params)
    return response


def vm_clone(client: DMEAPIClient, vm_id: str, name: str, location: str,
             description: str = None, is_binding_host: bool = False,
             vm_num: int = 1, name_postfix_index: int = 0,
             is_auto_boot: bool = False, os_options: dict = None,
             guest_customization: dict = None,
             guest_customizations: list = None,
             vm_config: dict = None) -> dict:
    url = "/rest/vmmgmt/v1/vms/{vm_id}/clone"

    body_params = {
        'name': name,
        'location': location
    }

    if description is not None:
        body_params['description'] = description
    if is_binding_host is not None:
        body_params['is_binding_host'] = is_binding_host
    if vm_num is not None:
        body_params['vm_num'] = vm_num
    if name_postfix_index is not None:
        body_params['name_postfix_index'] = name_postfix_index
    if is_auto_boot is not None:
        body_params['is_auto_boot'] = is_auto_boot
    if os_options is not None:
        body_params['os_options'] = os_options
    if guest_customization is not None:
        body_params['guest_customization'] = guest_customization
    if guest_customizations is not None:
        body_params['guest_customizations'] = guest_customizations
    if vm_config is not None:
        body_params['vm_config'] = vm_config

    response = client.post(url, params={"vm_id": vm_id}, body=body_params)
    return response


def vm_modify(client: DMEAPIClient, vm_id: str, name: str = None,
              description: str = None, cpu: dict = None,
              memory: dict = None, os_options: dict = None) -> dict:
    url = "/rest/vmmgmt/v1/vms/{vm_id}"

    body_params = {}

    if name is not None:
        body_params['name'] = name
    if description is not None:
        body_params['description'] = description
    if cpu is not None:
        body_params['cpu'] = cpu
    if memory is not None:
        body_params['memory'] = memory
    if os_options is not None:
        body_params['os_options'] = os_options

    response = client.put(url, params={"vm_id": vm_id}, body=body_params)
    return response


def vm_power_on(client: DMEAPIClient, vm_ids: list) -> dict:
    url = "/rest/vmmgmt/v1/vms/batch-power-on"

    body_params = {
        'vm_ids': vm_ids
    }

    response = client.post(url, body=body_params)
    return response


def vm_power_off(client: DMEAPIClient, vm_ids: list,
                 mode: str = "safe") -> dict:
    url = "/rest/vmmgmt/v1/vms/batch-power-off"

    body_params = {
        'vm_ids': vm_ids,
        'mode': mode
    }

    response = client.post(url, body=body_params)
    return response


def vm_hibernate(client: DMEAPIClient, vm_ids: list) -> dict:
    url = "/rest/vmmgmt/v1/vms/batch-hibernate"

    body_params = {
        'vm_ids': vm_ids
    }

    response = client.post(url, body=body_params)
    return response


def vm_reboot(client: DMEAPIClient, vm_ids: list,
              mode: str = None) -> dict:
    url = "/rest/vmmgmt/v1/vms/batch-reboot"

    body_params = {
        'vm_ids': vm_ids
    }

    if mode is not None:
        body_params['mode'] = mode

    response = client.post(url, body=body_params)
    return response


def vm_delete(client: DMEAPIClient, vm_ids: list,
              hold_time: int = None) -> dict:
    url = "/rest/vmmgmt/v1/vms/batch-delete"

    body_params = {
        'vm_ids': vm_ids
    }

    if hold_time is not None:
        body_params['hold_time'] = hold_time

    response = client.post(url, body=body_params)
    return response


def vm_vnc_info(client: DMEAPIClient, vm_id: str) -> dict:
    url = "/rest/vmmgmt/v1/vms/{vm_id}/vnc"

    response = client.get(url, params={"vm_id": vm_id})
    return response


def vm_mount_tools(client: DMEAPIClient, vm_id: str) -> dict:
    url = "/rest/vmmgmt/v1/vms/{vm_id}/install-tools"

    response = client.post(url, params={"vm_id": vm_id}, body={})
    return response


def vm_umount_tools(client: DMEAPIClient, vm_id: str) -> dict:
    url = "/rest/vmmgmt/v1/vms/{vm_id}/uninstall-tools"

    response = client.post(url, params={"vm_id": vm_id}, body={})
    return response


def vm_migrate(client: DMEAPIClient, vm_id: str, location: str, speed: str,
               disks: list, remote_site_urn: str = None,
               des_cluster_urn: str = None, is_binding_host: bool = False,
               migrate_vm_time_out: int = 0,
               is_frequency_reduce: bool = False, nics: list = None,
               migrate_transmit_policy: str = None) -> dict:
    url = "/rest/vmmgmt/v1/vms/{vm_id}/fullmigrate"

    body_params = {
        'location': location,
        'speed': speed,
        'disks': disks
    }

    if remote_site_urn is not None:
        body_params['remote_site_urn'] = remote_site_urn
    if des_cluster_urn is not None:
        body_params['des_cluster_urn'] = des_cluster_urn
    if is_binding_host is not None:
        body_params['is_binding_host'] = is_binding_host
    if migrate_vm_time_out is not None:
        body_params['migrate_vm_time_out'] = migrate_vm_time_out
    if is_frequency_reduce is not None:
        body_params['is_frequency_reduce'] = is_frequency_reduce
    if nics is not None:
        body_params['nics'] = nics
    if migrate_transmit_policy is not None:
        body_params['migrate_transmit_policy'] = migrate_transmit_policy

    response = client.post(url, params={"vm_id": vm_id}, body=body_params)
    return response


def vm_migrate_host(client: DMEAPIClient, vm_id: str, location: str,
                    is_binding_host: bool = False,
                    migrate_vm_time_out: int = 0,
                    is_frequency_reduce: bool = False,
                    migrate_transmit_policy: str = None,
                    nics: list = None) -> dict:
    url = "/rest/vmmgmt/v1/vms/{vm_id}/migrate"

    body_params = {
        'location': location
    }

    if is_binding_host is not None:
        body_params['is_binding_host'] = is_binding_host
    if migrate_vm_time_out is not None:
        body_params['migrate_vm_time_out'] = migrate_vm_time_out
    if is_frequency_reduce is not None:
        body_params['is_frequency_reduce'] = is_frequency_reduce
    if migrate_transmit_policy is not None:
        body_params['migrate_transmit_policy'] = migrate_transmit_policy
    if nics is not None:
        body_params['nics'] = nics

    response = client.post(url, params={"vm_id": vm_id}, body=body_params)
    return response


def vm_migrate_storage(client: DMEAPIClient, vm_id: str, speed: int,
                       disks: list) -> dict:
    url = "/rest/vmmgmt/v1/vms/{vm_id}/migratevol"

    body_params = {
        'speed': speed,
        'disks': disks
    }

    response = client.post(url, params={"vm_id": vm_id}, body=body_params)
    return response


def vm_import(client: DMEAPIClient, name: str, url: str, os_options: dict,
              res_config: list, arch: str = "x86", description: str = None,
              file_items: list = None, protocol: str = "cifs",
              username: str = None, password: str = None,
              guest_customization: dict = None, is_template: bool = False,
              tag_ids: list = None, image_format: str = None) -> dict:
    url_path = "/rest/vmmgmt/v1/vms/import"

    body_params = {
        'name': name,
        'url': url,
        'os_options': os_options,
        'res_config': res_config
    }

    if arch is not None:
        body_params['arch'] = arch
    if description is not None:
        body_params['description'] = description
    if file_items is not None:
        body_params['file_items'] = file_items
    if protocol is not None:
        body_params['protocol'] = protocol
    if username is not None:
        body_params['username'] = username
    if password is not None:
        body_params['password'] = password
    if guest_customization is not None:
        body_params['guest_customization'] = guest_customization
    if is_template is not None:
        body_params['is_template'] = is_template
    if tag_ids is not None:
        body_params['tag_ids'] = tag_ids
    if image_format is not None:
        body_params['image_format'] = image_format

    response = client.post(url_path, body=body_params)
    return response


def vm_nic_list(client: DMEAPIClient, vm_id: str) -> dict:
    url = "/rest/vmmgmt/v1/vms/{vm_id}/nics"

    response = client.get(url, params={"vm_id": vm_id})
    return response


def vm_nic_modify(client: DMEAPIClient, vm_id: str, nic_id: str,
                  mac: str = None, vringbuf: int = None,
                  queues: int = None) -> dict:
    url = "/rest/vmmgmt/v1/vms/{vm_id}/nics/{nic_id}"

    body_params = {}

    if mac is not None:
        body_params['mac'] = mac
    if vringbuf is not None:
        body_params['vringbuf'] = vringbuf
    if queues is not None:
        body_params['queues'] = queues

    response = client.put(url, params={"vm_id": vm_id, "nic_id": nic_id},
                          body=body_params)
    return response


def vm_nic_change_portgroup(client: DMEAPIClient, vm_id: str, nic_id: str,
                            port_group_urn: str) -> dict:
    url = "/rest/vmmgmt/v1/vms/{vm_id}/nics/{nic_id}/port-group"

    body_params = {
        'port_group_urn': port_group_urn
    }

    response = client.put(url, params={"vm_id": vm_id, "nic_id": nic_id},
                          body=body_params)
    return response


def vm_nic_add(client: DMEAPIClient, vm_id: str, port_group_urn: str,
               type: int = None, virt_io: str = "1", vringbuf: int = None,
               queues: int = None, enable_security_group: bool = False,
               security_group_id: int = None,
               connect_at_power_on: bool = True,
               link_status: str = None) -> dict:
    url = "/rest/vmmgmt/v1/vms/{vm_id}/nics"

    body_params = {
        'port_group_urn': port_group_urn
    }

    if type is not None:
        body_params['type'] = type
    if virt_io is not None:
        body_params['virt_io'] = virt_io
    if vringbuf is not None:
        body_params['vringbuf'] = vringbuf
    if queues is not None:
        body_params['queues'] = queues
    if enable_security_group is not None:
        body_params['enable_security_group'] = enable_security_group
    if security_group_id is not None:
        body_params['security_group_id'] = security_group_id
    if connect_at_power_on is not None:
        body_params['connect_at_power_on'] = connect_at_power_on
    if link_status is not None:
        body_params['link_status'] = link_status

    response = client.post(url, params={"vm_id": vm_id}, body=body_params)
    return response


def vm_nic_delete(client: DMEAPIClient, vm_id: str, nic_id: str) -> dict:
    url = "/rest/vmmgmt/v1/vms/{vm_id}/nics/{nic_id}"

    response = client.delete(url, params={"vm_id": vm_id, "nic_id": nic_id})
    return response


def vm_nic_change_linkstatus(client: DMEAPIClient, vm_id: str,
                             nic_ids: list,
                             connect_at_power_on: bool = True,
                             link_status: str = None) -> dict:
    url = "/rest/vmmgmt/v1/vms/{vm_id}/nics-linkstatus"

    body_params = {
        'nic_ids': nic_ids
    }

    if connect_at_power_on is not None:
        body_params['connect_at_power_on'] = connect_at_power_on
    if link_status is not None:
        body_params['link_status'] = link_status

    response = client.put(url, params={"vm_id": vm_id}, body=body_params)
    return response


def vm_snapshot_list(client: DMEAPIClient, vm_id: str) -> dict:
    url = "/rest/vmmgmt/v1/vms/{vm_id}/snapshots"

    response = client.get(url, params={"vm_id": vm_id})
    return response


def vm_snapshot_show(client: DMEAPIClient, vm_id: str, snapshot_id: str,
                     is_refresh: bool = True) -> dict:
    url = "/rest/vmmgmt/v1/vms/{vm_id}/snapshots/{snapshot_id}"

    params_dict = {"vm_id": vm_id, "snapshot_id": snapshot_id}
    if is_refresh is not None:
        params_dict['is_refresh'] = is_refresh

    response = client.get(url, params=params_dict)
    return response


def vm_snapshot_create(client: DMEAPIClient, vm_id: str, name: str,
                       description: str = None, type: str = None,
                       need_memory_shot: bool = False,
                       is_consistent: bool = False,
                       protect_period: int = None,
                       is_support_auto_delete: bool = None) -> dict:
    url = "/rest/vmmgmt/v1/vms/{vm_id}/snapshots"

    body_params = {
        'name': name
    }

    if description is not None:
        body_params['description'] = description
    if type is not None:
        body_params['type'] = type
    if need_memory_shot is not None:
        body_params['need_memory_shot'] = need_memory_shot
    if is_consistent is not None:
        body_params['is_consistent'] = is_consistent
    if protect_period is not None:
        body_params['protect_period'] = protect_period
    if is_support_auto_delete is not None:
        body_params['is_support_auto_delete'] = is_support_auto_delete

    response = client.post(url, params={"vm_id": vm_id}, body=body_params)
    return response


def vm_snapshot_delete(client: DMEAPIClient, vm_id: str, snapshot_id: str,
                       speed: int) -> dict:
    url = "/rest/vmmgmt/v1/vms/{vm_id}/snapshots/{snapshot_id}"

    params_dict = {"vm_id": vm_id, "snapshot_id": snapshot_id, "speed": speed}

    response = client.delete(url, params=params_dict)
    return response


def vm_snapshot_recover(client: DMEAPIClient, vm_id: str,
                        snapshot_id: str) -> dict:
    url = "/rest/vmmgmt/v1/vms/{vm_id}/snapshots/resume-vm"

    body_params = {
        'snapshot_id': snapshot_id
    }

    response = client.post(url, params={"vm_id": vm_id}, body=body_params)
    return response
