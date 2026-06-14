"""
Storage device (Storage) operations
"""

import sys
import os

from pydme.client import DMEAPIClient

# ============================================================================
# VStore (tenant) subtopic functions
# ============================================================================


def vstore_list(client: DMEAPIClient, storage_id: str = None, name: str = None,
                page_no: int = 1, page_size: int = 100,
                raw_id: str = None, vstore_id: str = None,
                qos_id: str = None, is_associated_qos: bool = None,
                storage_ip: str = None, storage_name: str = None,
                zone_id: str = None, status: str = None,
                nas_capacity_quota_alarm_switch: bool = None,
                sort_key: str = None, sort_dir: str = None) -> dict:
    """
    Batch query storage device tenant info. 

    Args:
        client: DME API client
        raw_id: Tenant on device ID (Optional, string, 1~256 characters)
        vstore_id: Tenant ID (Optional, string, 1~64 characters)
        qos_id: QoS policy ID (Optional, string, 1~64 characters)
        is_associated_qos: Tenant associated with QoS (Optional, boolean, true,false)
        name: Tenant name, supports fuzzy search (Optional, string, 1~256 characters)
        storage_id: Storage device ID (Optional, string, 1~255 characters)
        storage_ip: Storage device IP (Optional, string, 1~255 characters)
        storage_name: Storage device name (Optional, string, 1~255 characters)
        zone_id: Zone ID (Optional, string, 1~64 characters). OceanStor A series only. 
        status: Tenant status (Optional, string). Options: active (activated), inactive (inactive)
        nas_capacity_quota_alarm_switch: NAS capacity quota alarm switch (Optional, boolean, true,false). OceanStor A series only. 
        sort_key: Sort field (Optional, string)
        sort_dir: Sort direction (Optional, string). Options: asc (ascending), desc (descending)
        page_no: Page number (Optional, int32, 1~10000000). Default: 1
        page_size: Items per page (Optional, int32, 1~1000). Default: 100

    Returns:
        {
            total: TenantTotal count (integer),
            vstores: Tenant list (List<VstoreResp>, max array members: 1000). 参数格式如下：[{
                id: Tenant unique identifier (string, 1~64 characters),
                qos_id: QoS policy ID (string, 1~64 characters),
                raw_id: tenant ID on device (string, 1~64 characters),
                storage_sn: Storage deviceSN (string, 1~64 characters),
                storage_id: Device ID (string, 1~64 characters),
                storage_ip: Device IP (string, 1~255 characters),
                storage_name: Device name (string, 1~255 characters),
                name: Tenant name (string, 1~256 characters),
                description: Tenant description (string, 0~255 characters),
                running_status: Running status (string). Options: normal, initializing ( initialize),
                status: Tenant status (string). Options: active (activated), inactive (inactive),
                encrypt_option: Tenant encryption options (boolean, true,false),
            }, ...]
        }
    """
    url = "/rest/fileservice/v1/vstores/query"

    payload = {}
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if vstore_id is not None:
        payload['id'] = vstore_id
    if qos_id is not None:
        payload['qos_id'] = qos_id
    if is_associated_qos is not None:
        payload['is_associated_qos'] = is_associated_qos
    if name is not None:
        payload['name'] = name
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if storage_ip is not None:
        payload['storage_ip'] = storage_ip
    if storage_name is not None:
        payload['storage_name'] = storage_name
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if status is not None:
        payload['status'] = status
    if nas_capacity_quota_alarm_switch is not None:
        payload['nas_capacity_quota_alarm_switch'] = nas_capacity_quota_alarm_switch
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size

    response = client.post(url, body=payload)
    return response


def vstore_show(client: DMEAPIClient, id: str) -> dict:
    """
    Query tenant details. 

    Args:
        client: DME API client
        id:  tenantid (Required, string, 1~256 characters). must satisfy UUID format or 32-bit hex

    Returns:
        {
            id: Tenant unique identifier (string, 1~64 characters),
            name: Tenant name (string, 1~256 characters),
            description: Tenant description (string, 0~255 characters),
            storage_id: Device ID (string, 1~64 characters),
            status: Tenant status (string). Options: active (activated), inactive (inactive),
            running_status: Running status (string). Options: normal, initializing ( initialize),
        }
    """
    url = "/rest/fileservice/v1/vstores/{id}"

    # Parameter validation
    if not id:
        raise ValueError("id is required")

    response = client.get(url, params={"id": id})
    return response


def vstore_create(client: DMEAPIClient, name: str, storage_id: str,
                  san_capacity_quota: str = None,
                  nas_capacity_quota: str = None, description: str = None,
                  nas_capacity_quota_alarm_switch: bool = None,
                  nas_capacity_quota_alarm_threshold: int = None,
                  associate_pool_ids: list = None) -> dict:
    """
    Create tenant. OceanStor Dorado v3 devicefeature not supported. 

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, string, 1~36 characters). must satisfy UUID format or 32-bit hex
        name: Tenant name (Required, string, 1~256 characters). Supports letters, digits, underscores, hyphens, dots and Chinese characters
        san_capacity_quota: SAN Capacity quota(Optional, unit :  sector) 
        nas_capacity_quota: NAS Capacity quota(Optional, unit :  sector) 
        description: Tenant description(Optional, 0~255  characters) 
        nas_capacity_quota_alarm_switch: NAS Capacity quota alarm switch(Optional, A800 device only) 
        nas_capacity_quota_alarm_threshold: NAS Capacity quota alarmthreshold(Optional, A800 device only) 
        associate_pool_ids: Related storage pool ID list (Optional, A series device only) 

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/fileservice/v1/vstores"

    if not storage_id:
        raise ValueError("storage_id is required")

    payload = {
        'storage_id': storage_id,
        'name': name
    }

    if san_capacity_quota is not None:
        payload['san_capacity_quota'] = san_capacity_quota
    if nas_capacity_quota is not None:
        payload['nas_capacity_quota'] = nas_capacity_quota
    if description is not None:
        payload['description'] = description
    if nas_capacity_quota_alarm_switch is not None:
        payload['nas_capacity_quota_alarm_switch'] = nas_capacity_quota_alarm_switch
    if nas_capacity_quota_alarm_threshold is not None:
        payload['nas_capacity_quota_alarm_threshold'] = nas_capacity_quota_alarm_threshold
    if associate_pool_ids is not None:
        payload['associate_pool_ids'] = associate_pool_ids

    response = client.post(url, body=payload)
    return response


def vstore_modify(client: DMEAPIClient, id: str, name: str = None,
                  san_capacity_quota: str = None, nas_capacity_quota: str = None,
                  description: str = None, nas_capacity_quota_alarm_switch: bool = None,
                  nas_capacity_quota_alarm_threshold: int = None) -> dict:
    """
    Modify tenant, This operation modifies storage devicetenant specified on. 

    Args:
        client: DME API client
        id:  tenant ID (Required, string, 1~64 characters). must satisfy UUID format or 32-bit hex
        name: Tenant name (Optional, string, 1~256 characters). Name supports letters, digits, underscores, hyphens, dots and Chinese characters
        san_capacity_quota: SANCapacity quota (Optional, string, 1~20 characters)
        nas_capacity_quota: NAS capacity quota (Optional, string, 1~20 characters)
        description: Tenant description (Optional, string, 0~255 characters)
        nas_capacity_quota_alarm_switch: NAS capacity quota alarm switch (Optional, boolean, true,false). A800 device only
        nas_capacity_quota_alarm_threshold: NAS capacity quota alarmthreshold (Optional, int32, 50~100). A800 device only

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/fileservice/v1/vstores/{id}"

    # Parameter validation
    if not id:
        raise ValueError("id is required")

    payload = {}
    if name is not None:
        payload['name'] = name
    if san_capacity_quota is not None:
        payload['san_capacity_quota'] = san_capacity_quota
    if nas_capacity_quota is not None:
        payload['nas_capacity_quota'] = nas_capacity_quota
    if description is not None:
        payload['description'] = description
    if nas_capacity_quota_alarm_switch is not None:
        payload['nas_capacity_quota_alarm_switch'] = nas_capacity_quota_alarm_switch
    if nas_capacity_quota_alarm_threshold is not None:
        payload['nas_capacity_quota_alarm_threshold'] = nas_capacity_quota_alarm_threshold

    response = client.put(url, body=payload, params={"id": id})
    return response


def vstore_delete(client: DMEAPIClient, ids: list) -> dict:
    """
    Batch delete tenant, This operation will delete storage device tenant specified on. This API may directly or indirectly affect production services, causing service interruption or data loss. Proceed with caution.. 

    Args:
        client: DME API client
        ids:  tenantID list (Required, List[string], max array members: 100, min array members: 1)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/fileservice/v1/vstores/delete"

    # Parameter validation
    if not ids or len(ids) == 0:
        raise ValueError("ids is required, at least 1 tenant ID is required")

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response



def list(client: DMEAPIClient, az: str = None, source: str = None,
         dc_id: str = None, tag_ids: str = None, start: int = 1, 
         limit: int = 20, ext_attrs: str = None) -> dict:
    """
    Batch query storage devices:  supports pagination,  filter. 

    Args:
        client: DME API client. 
        az: Availability zone ID (Optional, string, 1~64 characters)
        source: Storage device source (Optional, string). Options: add, record, all. Queries access devices by default
        dc_id: Storage deviceData center ID (Optional, string, 1~32 characters)
        tag_ids: Tag filter list (Optional, string). supports up to 10 tag IDs combined filter, Multiple filter conditions are AND-related
        start: Page query start position (Optional, int32, 1~10000). Default: 1
        limit: Items per page (Optional, int32, 1~1000). Default: 20
        ext_attrs: Extended attribute filter list (Optional, string, 1~3000 characters). supports up to10extended attributes combined filter

    Returns:
        {
            total: Storage device total count (int32),
            datas: Storage device list (List<StorageSummaryInfo>). 参数格式如下：[{
                id: Storage device ID (string),
                name: Storage device name (string),
                ip: IP  address (string),
                status: Running status (string),
                sn: Device serial number (string),
                vendor:  vendor (string),
                model: Product model (string),
            }, ...]
        }
    """
    url = "/rest/storagemgmt/v1/storages"
    
    query_params = {}
    if az is not None:
        query_params['az'] = az
    if source is not None:
        query_params['source'] = source
    if dc_id is not None:
        query_params['dc_id'] = dc_id
    if tag_ids is not None:
        query_params['tag_ids'] = tag_ids
    if start is not None:
        query_params['start'] = start
    if limit is not None:
        query_params['limit'] = limit
    if ext_attrs is not None:
        query_params['ext_attrs'] = ext_attrs
    
    response = client.get(url, params=query_params)
    return response


def show(client: DMEAPIClient, storage_id: str) -> dict:
    """
    Query storage device. 

    Args:
        client: DME API client
        storage_id: Storage device ID, Required (Required, string, 1~36 characters). must satisfy UUID format or 32-bit hex

    Returns:
        {
            id: Storage device ID (string),
            name: Storage device name (string),
            ip: IP  address (string),
            status: Running status (string),
            sn: Device serial number (string),
            vendor:  vendor (string),
            model: Product model (string),
        }
    """
    url = "/rest/storagemgmt/v1/storages/{storage_id}/detail"

    if not storage_id:
        raise ValueError("storage_id is required")

    response = client.get(url, params={"storage_id": storage_id})
    return response


def add(client: DMEAPIClient, name: str = None, sn: str = None, ip: str = None,
        vendor: str = None, model: str = None, version: str = None,
        patch_version: str = None, dc_id: str = None, az: str = None,
        location: str = None, maintenanceetenance_start: int = None,
        maintenanceetenance_overtime: int = None, total_capacity: float = None,
        total_effective_capacity: float = None, total_pool_capacity: float = None,
        used_capacity: float = None, free_capacity: float = None,
        subscription_capacity: float = None, tag_ids: list = None) -> dict:
    """
    Add storage device (offline info entry only) 

    Add storage device info to DME system via offline method. 

    Args:
        client: DME API client. 
        name: Device name (1~256 characters). Supports half-width letters, digits, underscores, hyphens, dots and Chinese characters. 
        sn: Device serial number (regex is^[a-zA-Z0-9]{1,128}$). 
        ip: Device IP address (Optional, 0~128 characters,  supports IPv4 and IPv6, can also be empty). 
        dc_id: Data center ID (Optional, regex is^[a-zA-Z0-9]{1,128}$). 
        az: Availability zone (Optional, string). 
        vendor:  vendor (Optional, 0~128 characters). 
        model: Product model (Optional, 0~128 characters). 
        version: Version info (Optional, 0~64 characters). 
        patch_version: Patch version info (Optional, 0~64 characters). 
        location: Device location (Optional, 0~512 characters). 
        maintenanceetenance_start:  Maintenance start time (Optional, format is ms-level timestamp). must appear with warranty expiration time and value must be less. 
        maintenanceetenance_overtime: Warranty expiration time (Optional, format is ms-level timestamp). Must appear with maintenanceetenance start time and value must be greater. 
        total_capacity: Raw capacity (Optional, 0~2147483647, in MB). 
        total_effective_capacity: Available capacity (Optional, 0~2147483647, in MB). 
        total_pool_capacity: Available capacity (Optional, 0~2147483647, in MB). 
        used_capacity: Used capacity (Optional, 0~2147483647, in MB). 
        free_capacity: Free capacity (Optional, 0~2147483647, in MB). 
        subscription_capacity: Subscribed capacity (Optional, 0~2147483647, in MB). 
        tag_ids: Tag ID list (Optional, List<string>, max array members: 10, min array members: 0). 
    
    Returns:
        {
            id: Storage device ID (string, 1~64 characters),
        }
    """
        raise ValueError("name is required")
        raise ValueError("name is required")
    if not sn:
        raise ValueError("sn is required")

    url = "/rest/storagemgmt/v2/storages/offline-storages"

    payload = {
        'name': name,
        'sn': sn
    }
    
    if ip is not None:
        payload['ip'] = ip
    if vendor is not None:
        payload['vendor'] = vendor
    if model is not None:
        payload['model'] = model
    if version is not None:
        payload['version'] = version
    if patch_version is not None:
        payload['patch_version'] = patch_version
    if dc_id is not None:
        payload['dc_id'] = dc_id
    if az is not None:
        payload['az'] = az
    if location is not None:
        payload['location'] = location
    if maintenanceetenance_start is not None:
        payload['maintenanceetenance_start'] = maintenanceetenance_start
    if maintenanceetenance_overtime is not None:
        payload['maintenanceetenance_overtime'] = maintenanceetenance_overtime
    if total_capacity is not None:
        payload['total_capacity'] = total_capacity
    if total_effective_capacity is not None:
        payload['total_effective_capacity'] = total_effective_capacity
    if total_pool_capacity is not None:
        payload['total_pool_capacity'] = total_pool_capacity
    if used_capacity is not None:
        payload['used_capacity'] = used_capacity
    if free_capacity is not None:
        payload['free_capacity'] = free_capacity
    if subscription_capacity is not None:
        payload['subscription_capacity'] = subscription_capacity
    if tag_ids is not None:
        payload['tag_ids'] = tag_ids
    
    response = client.post(url, body=payload)
    return response


def remove(client: DMEAPIClient, ids: list) -> dict:
    """
    batchRemove storage device. 

    Args:
        client: DME API client
        ids: Storage device ID list (Required, List[string], max array members: 100, min array members: 1)

    Returns:
        {
            task_id: task Id (string, 1~64 characters),
        }
    """
    url = "/rest/storagemgmt/v2/storages/delete"

    if not ids or len(ids) == 0:
        raise ValueError("ids is required, at least 1 storage device ID needed")

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def sync(client: DMEAPIClient, storage_id: str) -> dict:
    """
    SyncStorage device info, This API is async. 

    Args:
        client: DME API client
        storage_id: Storage deviceId (Required, string, 1~64 characters). obtained via Batch query storage devices API

    Returns:
        N/A
    """
    url = "/rest/storagemgmt/v1/storages/refresh"

    if not storage_id:
        raise ValueError("storage_id is required")

    payload = {
        'id': storage_id
    }

    response = client.post(url, body=payload)
    return response


def bbu_list(client: DMEAPIClient, storage_id: str = None,
             health_status: str = None, running_status: str = None,
             enclosure_name: str = None, location: str = None,
             zone_id: str = None, page_no: int = 1,
             page_size: int = 20) -> dict:
    """
    query storage device BBU info list

    Args:
        client: DME API client. 
        storage_id: BBU storage device ID (Optional, 1~64 characters). 
        health_status: Health status (Optional). Options: unknown, normal, faulty ( fault), about_to_fail (Impending failure), low_battery (Low battery). 
        running_status: Running status (Optional). Options: unknown, normal, running, online, offline, charging, charging_completed, discharging. 
        enclosure_name: Enclosure name (Optional, 1~256 characters). supports fuzzy match. 
        location: location (Optional, 1~256 characters). supports fuzzy match. 
        zone_id: Zone ID (Optional, 1~255 characters). OceanStor A800 series only. 
        page_no: Page number (Optional, 1~2147483647, Default: 1). 
        page_size: Page size (Optional, 1~1000, Default: 20). 
    
    Returns:
        {
            backup_powers: BBU list (List<StorageBackupPowerInfo>). 参数格式如下：[{
                name:  name (1~255 characters),
                location: location (1~255 characters),
                health_status: Health status. Options: unknown, normal, faulty, about_to_fail, low_battery,
                running_status: Running status. Options: unknown, normal, running, online, offline, charging, charging_completed, discharging,
                charge_times: Discharge count (int64),
                firmware_version: Firmware version (1~255 characters),
                manufactured_date: Manufacture date (1~255 characters),
                enclosure_id: Enclosure ID on storage device (1~255 characters),
                enclosure_name: Enclosure name (1~255 characters),
                zone_id: Zone ID (1~255 characters), OceanStor A800 series only,
                zone_ip: Zone IP address (1~255 characters), OceanStor A800 series only,
                zone_name: Zone name (1~255 characters), OceanStor A800 series only,
            }, ...],
            total: BBU count (int32),
        }
    """
    url = "/rest/storagemgmt/v1/backup-powers/query"
    
    payload = {}
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if health_status is not None:
        payload['health_status'] = health_status
    if running_status is not None:
        payload['running_status'] = running_status
    if enclosure_name is not None:
        payload['enclosure_name'] = enclosure_name
    if location is not None:
        payload['location'] = location
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size
    
    response = client.post(url, body=payload)
    return response


def get_passphrase(client: DMEAPIClient, storage_id: str) -> dict:
    """
    getStorage device access token

    Args:
        client: DME API client
        storage_id: Storage device ID (Required) 

    Returns:
        {
            ip: Storage device IP address,
            passphrase: Storage device access token,
            port: Storage device access port (int32),
        }
    """
    url = "/rest/storagemgmt/v1/storages/{storage_id}/passphrase"
    
    response = client.get(url, params={"storage_id": storage_id})
    return response


def fan_list(client: DMEAPIClient, storage_id: str = None,
             health_status: str = None, running_status: str = None,
             run_level: str = None, enclosure_name: str = None,
             location: str = None, zone_id: str = None,
             page_no: int = 1, page_size: int = 20) -> dict:
    """
    query storage deviceFan info

    Args:
        client: DME API client
        storage_id: Storage deviceID(Optional, 1~64 characters) 
        health_status: Health status (Optional). Options: unknown, normal, faulty
        running_status: Running status (Optional). Options: unknown, normal, running, not_running, spin_down, online, offline
        run_level: Running level(Optional). Options: low, normal, high
        enclosure_name: EnclosureName (Optional,1~256 characters) , supports fuzzy match
        location: location(Optional, 1~256 characters) , supports fuzzy match
        zone_id: Zone ID (Optional, 1~255 characters), OceanStor A800 series only
        page_no: Page number (Optional, 1~2147483647, default 1)
        page_size: Page size (Optional, 1~1000, default 20) 

    Returns:
        {
            total: Fan count (integer),
            fans: Fan list (List<StorageFanInfo>). 参数格式如下：[{
                name:  name (1~128 characters),
                location: location (1~256 characters),
                health_status: Health status. Options: unknown, normal, faulty ( fault),
                running_status: Running status. Options: unknown, normal, running, not_running, spin_down, online, offline,
                run_level: Running level. Options: low, normal, high,
                enclosure_id: Enclosure ID on storage device (1~255 characters),
                enclosure_name: Enclosure name (1~255 characters),
                zone_id: Zone ID (1~255 characters), OceanStor A800 series only,
                zone_ip: Zone IP address (1~255 characters), OceanStor A800 series only,
                zone_name: Zone name (1~255 characters), OceanStor A800 series only,
            }, ...],
        }
    """
    url = "/rest/storagemgmt/v1/fans/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size,
    }

    param_map = {
        'storage_id': storage_id,
        'health_status': health_status,
        'running_status': running_status,
        'run_level': run_level,
        'enclosure_name': enclosure_name,
        'location': location,
        'zone_id': zone_id,
    }

    for key, value in param_map.items():
        if value is not None:
            payload[key] = value

    response = client.post(url, body=payload)
    return response


def disk_list(client: DMEAPIClient, storage_id: str, ids: list = None,
              name: str = None, slot_number: str = None, bom_id: str = None,
              health_status: str = None, physical_type: str = None,
              new_physical_type: str = None, capacity: int = None,
              role: str = None, disk_pool_name: str = None,
              disk_pool_id: str = None, storage_pool_id: str = None,
              bar_code: str = None, sn: str = None, speed: int = None,
              storage_ip: str = None, management_ip: str = None,
              node_name: str = None, virtual_disk: bool = None,
              status: str = None, enclosure_name: str = None,
              zone_id: str = None, sort_key: str = None,
              sort_dir: str = None, page_no: int = 1,
              page_size: int = 20) -> dict:
    """
    query storage deviceDisk info list

    Args:
        client: DME API client. 
        storage_id: Storage device ID (1~36 characters, must satisfy UUID format). 
        ids: Port ID list (Optional, List<string>, max array members: 100, min array members: 0). 
        name: disk name (Optional, 1~256 characters). 
        slot_number: Slot number, location (Optional, 1~256 characters). supports fuzzy search. 
        bom_id: BOM ID (Optional, 1~256 characters). 
        health_status: Health status (Optional). Options: unknown, normal, fault ( fault), pre_fail (Impending failure), degraded ( degraded), single_link ( single link), no_redundant_link ( no redundant link), subhealthy ( sub-health), offline. 
        physical_type: Disk type (Optional). Options: unknown, sata (SATA), sas (SAS), nl_sas (NL-SAS), ssd (SSD), ssd_card, scm, nl_ssd (NL-SSD), fc (FC), lun (LUN), ata (ATA), flash (FLASH), vmdisk (VMDISK), sas_flash_vp (SAS-FLASH-VP), hdd (HDD). 
        new_physical_type: Actual disk type (Optional). Options: SAS, SATA, SSD, NL_SAS, SLC_SSD, MLC_SSD, FC_SED, SAS_SED, SATA_SED, SSD_SED, SCM_SED, NL_SAS_SED, SLC_SSD_SED, MLC_SSD_SED, NVMe_SSD, NVMe_SSD_SED, SCM, CAPACITY_OPTIMIZED_SSD, CAPACITY_OPTIMIZED_SSD_SED, unknown, sas_disk, sata_disk, ssd_card, ssd_card_virtual, ssd_disk, m2_disk, FC, ATA, FLASH, VMDISK, SAS_FLASH_VP, HDD. 
        capacity: Total capacity (Optional, max: 9223372036854775807, unit : GB). 
        role:  disk role (Optional). Options: unknown, free, member, hotSpare, cache, aggregate, broken, foreign, labelmaint, maintenance), shared ( share), spare, unassigned ( unallocated), unsupported, remote, mediator. 
        disk_pool_name: Disk pool name (Optional, 1~256 characters). supports fuzzy search. 
        disk_pool_id: Disk pool ID (Optional, 1~64 characters).  Huawei storage device only, third-party device supports this field. 
        storage_pool_id: Storage pool ID (Optional, 1~64 characters). 
        bar_code:  Disk barcode (Optional, 1~256 characters). 
        sn:  diskSerial number (Optional, 1~256 characters).  Huawei storage device only, third-party device supports this field. 
        speed: Rotation speed (Optional, max: 2147483647, in RPM). 
        storage_ip:  deviceip address (Optional, 1~255 characters). 
        management_ip: management  deviceip address (Optional, 1~256 characters). 
        node_name: Node name (Optional, 1~256 characters). 
        virtual_disk: Virtual disk (Optional). Options: true, false. 
        status: Running status (Optional). Options: unknown, normal, abnormal ( fault), online, offline. 
        enclosure_name: Fan enclosure name on storage device (Optional, 1~255 characters). supports fuzzy search. 
        zone_id: Storage device zone ID (Optional, 1~255 characters). OceanStor A800 series only. 
        sort_key: Sort field (Optional). Options: capacity (Total capacity), speed, remaintenanceeLife, name (disk name), management_ip (management  deviceip address), slot_number (location). 
        sort_dir: Sort direction (Optional). Options: asc (ascending), desc (descending). 
        page_no: Page number (Optional, 1~2147483647, Default: 1). 
        page_size: Page size (Optional, 1~1000, Default: 20). 

    Returns:
        {
            total:  Disk count (integer),
            disks: Disk list (List<DiskInfo>). 参数格式如下：[{
                id:  diskID (string),
                name: disk name (string),
                health_status: Health status (string),
                physical_type: Disk type (string),
                capacity: Total capacity (integer),
                sn:  diskSerial number (string),
            }, ...],
        }
    """
    url = "/rest/storagemgmt/v2/storages/{storage_id}/disk"

    payload = {}
    if ids is not None:
        payload['ids'] = ids
    if name is not None:
        payload['name'] = name
    if slot_number is not None:
        payload['slot_number'] = slot_number
    if bom_id is not None:
        payload['bom_id'] = bom_id
    if health_status is not None:
        payload['health_status'] = health_status
    if physical_type is not None:
        payload['physical_type'] = physical_type
    if new_physical_type is not None:
        payload['new_physical_type'] = new_physical_type
    if capacity is not None:
        payload['capacity'] = capacity
    if role is not None:
        payload['role'] = role
    if disk_pool_name is not None:
        payload['disk_pool_name'] = disk_pool_name
    if disk_pool_id is not None:
        payload['disk_pool_id'] = disk_pool_id
    if storage_pool_id is not None:
        payload['storage_pool_id'] = storage_pool_id
    if bar_code is not None:
        payload['bar_code'] = bar_code
    if sn is not None:
        payload['sn'] = sn
    if speed is not None:
        payload['speed'] = speed
    if storage_ip is not None:
        payload['storage_ip'] = storage_ip
    if management_ip is not None:
        payload['management_ip'] = management_ip
    if node_name is not None:
        payload['node_name'] = node_name
    if virtual_disk is not None:
        payload['virtual_disk'] = virtual_disk
    if status is not None:
        payload['status'] = status
    if enclosure_name is not None:
        payload['enclosure_name'] = enclosure_name
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size

    response = client.post(url, body=payload, params={"storage_id": storage_id})
    return response


def pool_list(client: DMEAPIClient, storage_id: str = None, raw_id: str = None,
              zone_id: str = None, page_no: int = 1, page_size: int = 10,
              sort_key: str = None, sort_dir: str = None) -> dict:
    """
     query storage deviceStorage pool list

    Args:
        client: DME API client
        storage_id: Storage device ID(Optional, 1~64 characters) 
        raw_id: Storage poolon the storage deviceID(Optional, 1~64 characters) 
        zone_id: Zone ID(Optional, 1~256 characters) , supports exact search, OceanStor A800 series only
        page_no: Page number(Optional, 1~10000, default 1) 
        page_size: Page size(Optional, 1~1000, default 10) 
        sort_key: Sort field(Optional). Options: total_capacity, consumed_capacity (Storage poolUsed capacity), free_capacity (Storage poolFree capacity, Flash storage only), replication_capacity (Storage poolProtection capacity)
        sort_dir: Sort direction(Optional). Options: asc (ascending), desc (descending)

    Returns:
        {
            total: Storage poolcount (int32),
            datas: Storage pool basic info list (List<StoragePoolBasicInfo>). 参数格式如下：[{
                id: Storage pool ID (1~32 characters),
                name: Storage pool name (1~31 characters),
                raw_id: Storage poolon the storage deviceID (1~64 characters),
                storage_id: Storage device ID (1~64 characters),
                storage_name: Storage device name (1~127 characters),
                usage_type: Storage pool usage. Options: block-and-file, block, file, object, hdfs, converged,
                total_capacity: Total capacity, in MB (number),
                free_capacity: Free capacity, in MB (number), Flash storage only, OceanStor A800Device support,
                consumed_capacity: Used capacity, in MB (number),
                replication_capacity:  dataProtection capacity, in MB (number), flash storage only,
                subscribed_capacity: Total subscribed capacity, in MB (number), Flash storage only, DistributedDevice support,
                lun_subscribed_capacity: LUN subscribed capacity, in MB (number), flash storage only,
                filesystem_subscribed_capacity: Filesystem total subscribed capacity, in MB (number), OceanStor Dorado V6 6.1.0+ onlysion,
                health_status: Health status. Options: normal, fault ( fault), degraded ( degraded), unknown. flash and third-party storage only,
                running_status: Running status. Options: pre-copy (Pre-copy), rebuilt ( refactor), online, offline, balancing (Balancing), initializing (Initializing), deleting (Deleting), unknown. flash storage only,
                pool_status: Storage pool status. Options: normal, fault ( fault), write-protect ( write protect), stopped ( stop), fault-and-write-protect (Fault with write protection), migrating-data (Data migration), degraded ( degraded), rebuilding-data ( data refactor), migrating-services ( service migration), all-copies-failed ( all replicas fault), all-copies-failed-and-write-protect (All replicas failed with write protection), deleting (Deleting), deletion-failed (delete  failure), unknown. distributed storage only,
                disk_types: Disk type list (List<string>), flash storage only,
                capacity_usage: Capacity utilization,
                redundancy_policy: Redundancy policy. Options: replication, ec. FusionStorage, OceanStor 100D and OceanStor Pacific series onlyt,
                num_data_units: EC data block count (integer), effective when redundancy policy is EC,
                num_fault_tolerance: ECAllowed faulty node count (integer), effective when redundancy policy is EC,
                num_parity_units: EC parity block count (integer), effective when redundancy policy is EC,
                cache_media_type: Storage pool cache type. Options: ssd_card, ssd_disk, none. FusionStorage, OceanStor 100D, OceanStor A310 and OceanStor Pacificseries device support,
                zone_id: Zone ID (1~64 characters), OceanStor A800 series only,
                zone_ip: Zone IP (1~256 characters), OceanStor A800 series only,
                zone_name: Zone name (1~256 characters), OceanStor A800 series only,
                raid_level: RAID level list (List<string>). Options: RAID0, RAID1, RAID2, RAID3, RAID5, RAID6, RAID10, RAID50, RAID_TP. Flash storage only, OceanDisk, OceanStor A800Device support,
                disk_pool_id: Disk pool ID (1~64 characters). Supports flash devices, Pacific, A310 and OceanStor A800Device support,
                disk_pool_name: Disk pool name (1~256 characters),
                media_type: Storage pool maintenancee memory type. Options: sas_disk, sata_disk, ssd_card, ssd_disk. OceanStor Pacific, OceanStor A310, OceanStor 100DDevice support,
            }, ...]
        }
    """
    url = "/rest/storagemgmt/v1/storagepools/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size,
    }

    param_map = {
        'storage_id': storage_id,
        'raw_id': raw_id,
        'zone_id': zone_id,
        'sort_key': sort_key,
        'sort_dir': sort_dir,
    }

    for key, value in param_map.items():
        if value is not None:
            payload[key] = value

    response = client.post(url, body=payload)
    return response


def hyperscale_pool_list(client: DMEAPIClient, raw_id: str = None, name: str = None,
                         local_pool_id: str = None, health_status: str = None,
                         running_status: str = None, storage_id: str = None,
                         description: str = None, page_no: int = 1, page_size: int = 20,
                         sort_key: str = None, sort_dir: str = None) -> dict:
    """
     query HyperScale Storage pool list

    Args:
        client: DME API client
        raw_id: Storage poolon the storage deviceID(Optional, 1~64 characters) , supports exact search
        name: HyperScaleStorage pool name(Optional, 1~256 characters) , supports fuzzy search
        local_pool_id: Local storage pool ID under HyperScale storage pool(Optional, 0~64 characters) , supports filtering by local storage poolyperScaleStorage pool
        health_status: Health status(Optional). Options: normal, faulty ( fault), degraded ( degraded)
        running_status: Running status(Optional). Options: pre_copy (Pre-copy), rebuilding ( refactor), online, offline, balancing (Balancing), initializing (Initializing), deleting (Deleting)
        storage_id: Storage device ID(Optional, 0~64 characters) 
        description: HyperScaleStorage pool description(Optional, 0~256 characters) 
        page_no: Page number(Optional, 1~10000, default 1) 
        page_size: Page size(Optional, 1~1000, default 20) 
        sort_key: Sort field(Optional). Options: raw_id, total_capacity, consumed_capacity, capacity_usage (Capacity utilization), free_capacity (Free capacity), subscribed_capacity_percentage (Subscription rate)
        sort_dir: Sort direction(Optional). Options: asc (ascending), desc (descending)

    Returns:
        {
            total: HyperScaleStorage poolTotal count (int32),
            data: HyperScale storage pool list (List<HyperScalePoolInfo>). 参数格式如下：[{
                id: HyperScaleStorage pool ID (1~64 characters),
                raw_id: Storage poolon the storage deviceID (1~64 characters),
                name: HyperScaleStorage pool name (1~256 characters),
                description: HyperScaleStorage pool description (1~256 characters),
                storage_id: Storage device ID (1~64 characters),
                storage_ip: Storage device IP (1~255 characters),
                storage_name: Storage device name (1~127 characters),
                health_status: Health status. Options: normal, faulty ( fault), degraded ( degraded),
                running_status: Running status. Options: pre_copy (Pre-copy), rebuilding ( refactor), online, offline, balancing (Balancing), initializing (Initializing), deleting (Deleting),
                total_capacity: Total capacity, in MB (number),
                consumed_capacity: Used capacity, in MB (number),
                capacity_usage: Capacity utilization (number),
                free_capacity: Free capacity, in MB (number),
                subscribed_capacity_percentage: Subscription rate (number),
                subscribed_capacity: Total subscribed capacity, in MB (number),
                used_subscribed_capacity: Used subscribed capacity, in MB (number),
                redundancy_strategy: Redundancy policy. Options: disk, distributed_ec,
            }, ...]
        }
    """
    url = "/rest/storagemgmt/v1/hyperscale-pools/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size,
    }

    param_map = {
        'raw_id': raw_id,
        'name': name,
        'local_pool_id': local_pool_id,
        'health_status': health_status,
        'running_status': running_status,
        'storage_id': storage_id,
        'description': description,
        'sort_key': sort_key,
        'sort_dir': sort_dir,
    }

    for key, value in param_map.items():
        if value is not None:
            payload[key] = value

    response = client.post(url, body=payload)
    return response


def node_list(client: DMEAPIClient, storage_id: str = None, raw_id: str = None,
              storage_name: str = None, name: str = None, ids: list = None,
              mgmt_ip: str = None, frame_number: str = None,
              slot_number: str = None, status: str = None, roles: list = None,
              page_no: int = 1, page_size: int = 20,
              sort_key: str = None, sort_dir: str = None) -> dict:
    """
    query storage deviceNode list

    Args:
        client: DME API client
        storage_id: Storage device ID(Optional, 1~64 characters) , supports filtering
        raw_id:  nodeon the storage deviceID(Optional, 1~64 characters) 
        storage_name: Storage deviceName (Optional,1~255 characters) , supports filtering
        name:  nodeName (Optional,1~256 characters) , supports fuzzy search (case-insensitive) 
        ids:  nodeID list(Optional, List<string>, max array members: 100) 
        mgmt_ip: Node managementIP address(Optional, 1~256 characters) , supports fuzzy search (case-insensitive) 
        frame_number: Rack/ rack number(Optional, 1~256 characters) , supports fuzzy search (case-insensitive) 
        slot_number: Slot number in rack(Optional, 1~256 characters) , supports fuzzy search (case-insensitive) 
        status: Node status(Optional). Options: UNKNOWN, NORMAL, FAULT, PRE_FAIL, PARTIALLY_DAMAGED, DEGRADED, BAD_SECTORS_FOUND, BIT_ERRORS_FOUND ( has error code), CONSISTENT, INCONSISTENT, BUSY, NO_INPUT, LOW_BATTERY, SINGLE_LINK_FAULT
        roles:  nodeRole list(Optional, List<string>, max array members: 10). Options: management (management ), storage ( storage), compute (VBS compute), replication ( replication), paxos ( control), dpc_compute (DPC compute)
        page_no: Page number(Optional, 1~10000, default 1) 
        page_size: Page size(Optional, 1~1000, default 20) 
        sort_key: Sort field(Optional). Options: name (Node name), mgmt_ip (Node managementIP address)
        sort_dir: Sort direction(Optional). Options: asc (ascending), desc (descending)

    Returns:
        {
            total:  Node count (integer),
            nodes: Node list (List<StorageNodeBaseInfo>). 参数格式如下：[{
                id:  nodeid (1~64 characters),
                name: Node name (1~255 characters),
                raw_id:  nodeon the storage deviceID (1~64 characters),
                mgmt_ip: Node managementIP address (1~255 characters),
                status: Node status (1~255 characters). Options: UNKNOWN, NORMAL, FAULT, PARTIALLY_DAMAGED,
                node_model:  Node model (1~255 characters). E.g.: DataTurbo, OceanStor Pacific, RH5288 V3,
                frame_number: Rack/ rack number (1~255 characters),
                slot_number: Slot number in rack (1~255 characters),
                roles:  nodeRole list (List<string>). Options: management (management ), storage ( storage), compute (VBS compute), replication ( replication), paxos ( control), dpc_compute (DPC compute),
                node_sn: Serial number info (1~255 characters),
                storage_id: Storage device ID (1~64 characters),
                storage_name: Storage device name (1~255 characters),
                eos_time:  Storage EOS time (int64), GMT: Jan 1, 1970 00:00:00 - total ms to present,
                installation_status: Storage software installation status. Options: installed (Storage software installed), not_installed (Storage software not installed),
                ip_address_list: Node IP address list (List<StorageNodeIpInfo>). 参数格式如下：[{
                    ip_address: Node IP address (1~256 characters),
                    usage: Node IP address purpose list (List<string>). Options: storage_frontend (Storage frontend network IP), storage_backend (Storage backend network IP), management_external_float (Management external network floating IP), management_internal_float (Management internal network floating IP), management_external (Management external network IP), management_internal (Management internal network IP), replication ( replication network IP), quorum (arbitration network IP), iscsi (iSCSI network IP),
                }, ...],
            }, ...]
        }
    """
    url = "/rest/storagemgmt/v1/storage-nodes/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size,
    }

    param_map = {
        'storage_id': storage_id,
        'raw_id': raw_id,
        'storage_name': storage_name,
        'name': name,
        'ids': ids,
        'mgmt_ip': mgmt_ip,
        'frame_number': frame_number,
        'slot_number': slot_number,
        'status': status,
        'roles': roles,
        'sort_key': sort_key,
        'sort_dir': sort_dir,
    }

    for key, value in param_map.items():
        if value is not None:
            payload[key] = value

    response = client.post(url, body=payload)
    return response


def psu_list(client: DMEAPIClient, storage_id: str,
             health_status: str = None, running_status: str = None,
             power_type: str = None, power_mode: str = None,
             location: str = None, model: str = None, sn: str = None,
             enclosure_name: str = None, zone_id: str = None,
             page_no: int = 1, page_size: int = 20) -> dict:
    """
     query storage devicePower supplyDetails info, only supportsOceanStor A800 storage. 

    Args:
        client: DME API client
        storage_id: Storage deviceID (Required, 1~64 characters) 
        health_status: Health status(Optional). Options: unknown, normal, faulty ( fault), inconsistent ( inconsistent), no_input ( no input)
        running_status: Running status(Optional). Options: unknown, normal, running, online, offline
        power_type: Power supply type(Optional). Options: dc, ac, hv
        power_mode: Power supply mode(Optional). Options: balanced_power ( balanced power supply), active_power (primary power supply), standby_power (standby power supply)
        location: location(Optional, 1~256 characters) , supports fuzzy match
        model:  model(Optional, 1~256 characters) , supports fuzzy match
        sn: Serial number(Optional, 1~256 characters) , supports fuzzy match
        enclosure_name: EnclosureName (Optional,1~256 characters) , supports fuzzy match
        zone_id: Zone ID(Optional, 1~64 characters) , OceanStor A800 series only
        page_no: Page number(Optional, 1~2147483647, default 1) 
        page_size: Page size(Optional, 1~1000, default 20) 

    Returns:
        {
            total: Power supply count (int32),
            storage_powers: Power list (List<StoragePowerInfo>). 参数格式如下：[{
                name:  name (1~255 characters),
                location: location (1~255 characters),
                health_status: Health status. Options: unknown, normal, faulty ( fault), inconsistent ( inconsistent), no_input ( no input),
                running_status: Running status. Options: unknown, normal, running, online, offline,
                power_type: Power supply type. Options: dc, ac, hv,
                model:  model (1~255 characters),
                sn: Serial number (1~255 characters),
                manufacturer: Manufacturer (1~255 characters),
                enclosure_name: Enclosure name (1~255 characters),
                production_date:  production date (1~255 characters),
                version:  version (1~255 characters),
                bom_code: Power supply module BOM code (1~255 characters),
                power_mode: Power supply mode. Options: balanced_power ( balanced power supply), active_power (primary power supply), standby_power (standby power supply),
                zone_name: Zone name (1~255 characters), OceanStor A800 series only,
                zone_id: Zone ID (1~255 characters), OceanStor A800 series only,
                zone_ip: Zone IP address (1~255 characters), OceanStor A800 series only,
                storage_id: Storage deviceID (1~64 characters),
                storage_name: Storage device name (1~128 characters),
                storage_ip: Storage deviceIP address (1~32 characters),
                storage_sn: Storage deviceSerial number (1~64 characters),
            }, ...],
        }
    """
    url = "/rest/storagemgmt/v1/storage-powers/query"

    payload = {
        'storage_id': storage_id,
        'page_no': page_no,
        'page_size': page_size,
    }

    param_map = {
        'health_status': health_status,
        'running_status': running_status,
        'power_type': power_type,
        'power_mode': power_mode,
        'location': location,
        'model': model,
        'sn': sn,
        'enclosure_name': enclosure_name,
        'zone_id': zone_id,
    }

    for key, value in param_map.items():
        if value is not None:
            payload[key] = value

    response = client.post(url, body=payload)
    return response


def query_power_data(client: DMEAPIClient, start_time: str, end_time: str,
                      storage_ids: list, time_granularity: str) -> dict:
    """
     Query storage device power data

    Args:
        client: DME API client
        start_time: Start timestamp (Required, 13-digit ms timestamp,  regex ^([0-9]){13}$) 
        end_time: End timestamp (Required, 13-digit ms timestamp,  regex ^([0-9]){13}$) 
        storage_ids:  storageID list (Required, List<string>, max array members: 300) 
        time_granularity: Time granularity (Required). Options: HOUR (hour(s)), DAY (day(s)), MONTH ( months)

    Returns:
        {
            storage_power_list: Storage power list (List<StoragePower>). 参数格式如下：[{
                storage_id:  storageID,
                power:  Storage power in kW (number),
            }, ...],
        }
    """
    url = "/rest/metrics/v1/storage/power/query"

    payload = {
        'storage_ids': storage_ids,
        'time_granularity': time_granularity,
        'start_time': start_time,
        'end_time': end_time,
    }

    response = client.post(url, body=payload)
    return response


def modify(client: DMEAPIClient, storage_id: str = None, name: str = None,
           ip: str = None, vendor: str = None, model: str = None,
           version: str = None, patch_version: str = None,
           location: str = None, maintenanceetenance_start: int = None,
           maintenanceetenance_overtime: int = None, total_capacity: float = None,
           total_effective_capacity: float = None, total_pool_capacity: float = None,
           used_capacity: float = None, free_capacity: float = None,
           subscription_capacity: float = None, tag_ids: list = None) -> dict:
    """
    Modify storage device (only supportsModify recorded offlineStorage device info) 

    Args:
        client: DME API client. 
        storage_id: Storage device ID (Required) . 
        name: Device name (Optional, 1~256 characters). supports half-width letters, digits, underscores, hyphens, dots and Chinese characters. 
        ip: Device IP address (Optional, 0~128 characters,  supports IPv4 and IPv6, can also be empty). 
        vendor:  vendor (Optional, 0~128 characters). 
        model: Product model (Optional, 0~128 characters). 
        version: Version info (Optional, 0~64 characters). 
        patch_version: Patch version info (Optional, 0~64 characters). 
        location:  devicelocation (Optional, 0~512 characters). 
        maintenanceetenance_start:  Maintenance start time (Optional, format is ms-level timestamp). must appear with warranty expiration time and value must be less. 
        maintenanceetenance_overtime: Warranty expiration time (Optional, format is ms-level timestamp).  Must appear with maintenanceetenance start time and value greater thanStart time. 
        total_capacity: Raw capacity (Optional, -1~2147483647, in MB). Storage devicesum of all disk physical capacities, -1Indicates no raw capacity. 
        total_effective_capacity: Available capacity (Optional, -1~2147483647, in MB). Storage device writable user data total, -1Indicates no available capacity. 
        total_pool_capacity: Available capacity (Optional, -1~2147483647, in MB). Actual available disk physical space (Excluding RAID, metadata consumption) , -1Indicates N/AAvailable capacity. 
        used_capacity: Used capacity (Optional, -1~2147483647, in MB). Sum of used capacity across all storage pools, -1N/A for used capacity. 
        free_capacity: Free capacity (Optional, -1~2147483647, in MB). Difference between available and used capacity, -1N/A for free capacity. 
        subscription_capacity: Subscribed capacity (Optional, -1~2147483647, in MB). Sum of subscribed capacity across all storage pools, -1Indicates no subscribed capacity. 
        tag_ids:  Tag ID list (Optional, string, 0~512 characters). Array format string, supports up to 10 tags,  empty array meansRemove all storage device tagsassociated tags. 

    Returns:
        N/A
    """
    if not storage_id:
        raise ValueError("storage_id is required")

    url = "/rest/storagemgmt/v2/storages/offline-storages/{storage_id}"

    payload = {}
    if name is not None:
        payload['name'] = name
    if ip is not None:
        payload['ip'] = ip
    if vendor is not None:
        payload['vendor'] = vendor
    if model is not None:
        payload['model'] = model
    if version is not None:
        payload['version'] = version
    if patch_version is not None:
        payload['patch_version'] = patch_version
    if location is not None:
        payload['location'] = location
    if maintenanceetenance_start is not None:
        payload['maintenanceetenance_start'] = maintenanceetenance_start
    if maintenanceetenance_overtime is not None:
        payload['maintenanceetenance_overtime'] = maintenanceetenance_overtime
    if total_capacity is not None:
        payload['total_capacity'] = total_capacity
    if total_effective_capacity is not None:
        payload['total_effective_capacity'] = total_effective_capacity
    if total_pool_capacity is not None:
        payload['total_pool_capacity'] = total_pool_capacity
    if used_capacity is not None:
        payload['used_capacity'] = used_capacity
    if free_capacity is not None:
        payload['free_capacity'] = free_capacity
    if subscription_capacity is not None:
        payload['subscription_capacity'] = subscription_capacity
    if tag_ids is not None:
        import json
        payload['tag_ids'] = json.dumps(tag_ids) if isinstance(tag_ids, list) else tag_ids

    response = client.put(url, body=payload, params={"storage_id": storage_id})
    # modify API returns empty response, Returns empty dict on success
    return response if response else {}


def app_type_list(client: DMEAPIClient, storage_id: str, 
                 create_type: int = None, template_type: int = None, 
                 pool_id: str = None) -> dict:
    """
    Query storage device application type
    
    Dorado series only. 
    
    Args:
        client: DME API client. 
        storage_id: Storage device id (1~36 characters, must satisfy UUID format). 
        create_type: Create type (Optional, 0~1). Options: 0 ( system preset), 1 (user defined). returns all types if not provided. 
        template_type: Application type category (Optional, 0~1). Options: 0 (LUN), 1 (NAS). default: LUN if not specified. 
        pool_id: Storage poolid (Optional, 1~64 characters,  letters and digits). 
    
    Returns:
        Application type info, includes  datas  list, Each element contains id, name, block_size, 
        enable_compress, enable_dedup, create_type and other fields
    """
    url = "/rest/storagemgmt/v1/storages/{storage_id}/workloads"
    
    query_params = {}
    if create_type is not None:
        query_params['create_type'] = create_type
    if template_type is not None:
        query_params['template_type'] = template_type
    if pool_id is not None:
        query_params['pool_id'] = pool_id
    
    
    query_params = {}
    if create_type is not None:
        query_params['create_type'] = create_type
    if template_type is not None:
        query_params['template_type'] = template_type
    if pool_id is not None:
        query_params['pool_id'] = pool_id
    
    response = client.get(url, params=query_params)
    return response


def controller_list(client: DMEAPIClient, storage_id: str) -> dict:
    """
    Query storage devicecontroller info
    
    query storage deviceControllerList info. 
    
    Args:
        client: DME API client
        storage_id: Storage device ID (Required, 1~36  characters, UUID format or 32-bit hex) 
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes total and controllers fields
        - total: ControllerTotal count
        - controllers: Controller list, includes id, name, status, type and other info
    """
    url = "/rest/storagemgmt/v1/storages/{storage_id}/controllers"
    
    response = client.get(url, params={"storage_id": storage_id})
    return response


def disk_domaintenancee_list(client: DMEAPIClient, storage_id: str = None, page_no: int = 1,
                   page_size: int = 20) -> dict:
    """
    Batch query disk pools

    Args:
        client: DME API client
        storage_id: Storage device ID(Optional, 1~64  characters) , supports filtering
        page_no: Page number(Optional, 1~2147483647, default 1) 
        page_size: Page size(Optional, 1~1000, default 20) 

    Returns:
        {
            total: Disk poolcount (int32),
            disk_pools: Disk pool list (List<DiskPoolInfo>). 参数格式如下：[{
                    id: Disk poolid (1~64 characters),
                    raw_id: Disk poolon the deviceid (1~64 characters),
                    name: Disk pool name (1~128 characters),
                    running_status: Running status. Options: online, offline, pre_copy (Pre-copy), reconstruction ( refactor), balancing (Balancing), initializing (Initializing), deleting (Deleting), unknown,
                    health_status: Health status. Options: normal, fault ( fault), degraded ( degraded), unknown,
                    total_capacity: Total available raw capacity, in MB (number),
                    spare_capacity: Total hot spare raw capacity, in MB (number),
                    used_capacity: Allocated raw capacity, in MB (number),
                    used_spare_capacity: Used hot spare raw capacity, in MB (number),
                    free_capacity: Free capacity, in MB (number),
                    storage_id: Storage device ID (1~64 characters),
                 }, ...]
        }
    """
    url = "/rest/storagemgmt/v1/disk-pools/query"

    payload = {}

    if storage_id is not None:
        payload['storage_id'] = storage_id
    payload['page_no'] = page_no
    payload['page_size'] = page_size

    response = client.post(url, body=payload)
    return response


def disk_pool_list(client: DMEAPIClient, storage_id: str = None,
                   page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch query distributed storage device disk pools. OceanStor Pacific and A310 only. 

    Args:
        client: DME API client
        storage_id: Storage device ID (Optional, string, 1~64 characters). Non-Pacific/A310 device reports parameter error
        page_no: Page number (Optional, int32, 1~2147483647). Default: 1
        page_size: Page size (Optional, int32, 1~1000). Default: 20

    Returns:
        {
            total: Total count (int32),
            disk_pools: Disk pool list. 参数格式如下：[{
                id: Disk poolID (string),
                name: Disk pool name (string),
                status:  status (string),
            }, ...],
        }
    """
    url = "/rest/storagemgmt/v1/diskpools/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    if storage_id is not None:
        payload['storage_id'] = storage_id

    response = client.post(url, body=payload)
    return response


def enclosure_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 20,
                   storage_id: str = None, name: str = None, location: str = None,
                   health_status: list = None, zone_name: str = None,
                   zone_id: list = None, running_status: list = None,
                   power_mode: list = None, esn: str = None, mac: str = None,
                   sort_key: str = None, sort_dir: str = None) -> dict:
    """
    Batch query enclosures info

    Args:
        client: DME API client
        page_no: Page number(Optional, 1~2147483647, default 1) 
        page_size: Page size(Optional, 1~1000, default 20) 
        storage_id: Storage deviceID(Optional, 1~64 characters) 
        name: Name (Optional,1~256 characters) , supports fuzzy match
        location: location(Optional, 1~256 characters) , supports fuzzy match
        health_status: Health status list(Optional, List<string>, max array members: 3). Options: unknown, normal, faulty ( fault)
        zone_name: ZoneName (Optional,1~255 characters) , OceanStor A800 series only, supports fuzzy match
        zone_id: Zone ID list(Optional, List<string>, max array members: 100) , OceanStor A800 series only
        running_status: Running status list(Optional, List<string>, max array members: 7). Options: unknown, normal, running, sleep_in_high_temperature, online, offline
        power_mode: Power supply mode list(Optional, List<string>, max array members: 2). Options: load_balance (Load balancing mode), active_standby_power (Primary/standby power mode)
        esn: EnclosureSerial number(Optional, 1~256 characters) , supports fuzzy match
        mac: MAC address(Optional, 1~256 characters) , supports fuzzy match
        sort_key: Sort field(Optional). Options: temperature
        sort_dir: Sort direction(Optional). Options: asc (ascending), desc (descending). Returns ascending by default

    Returns:
        {
            total: Enclosurecount (integer),
            data: Enclosure list (List<EnclosureItem>). 参数格式如下：[{
                    id: EnclosureID (1~64 characters),
                    raw_id: Enclosure ID on storage device (1~64 characters),
                    name:  name (1~256 characters),
                    model:  Model (1~32 characters). Options: 0 (BMC controller enclosure), 1 (2U dual controller 6Gbps SAS 12-disk 3.5-inch controller enclosure), 2 (2U dual controller 6Gbit/s SAS 24disk slot 2.5inch controller enclosure), 16 (2U 6Gbit/s SAS 12disk slot 3.5inch disk enclosure), 17 (2U SAS 24disk cascading enclosure), 18 (4U 6Gbit/s SAS 24disk slot 3.5inch disk enclosure), 19 (4U FC 24disk cascading enclosure), 20 (1U PCIe dataSwitch), 21 (4U 6Gbit/s SAS 75disk slot 3.5inch disk enclosure), 22 (SVP), 23 (2U dual controller 6Gbps SAS 12-disk 3.5-inch controller enclosure), 24 (2U 6Gbit/s SAS 25disk slot 2.5inch disk enclosure), 25 (4U 6Gbit/s SAS 24disk slot 3.5inch disk enclosure), 26 (2U dual controller 6Gbit/s SAS 25disk slot 2.5inch controller enclosure), 37 (2U dual controller 6Gbps SAS 12-disk 3.5-inch controller enclosure), 38 (2U dual controller 6Gbit/s SAS 25disk slot 2.5inch controller enclosure), 39 (4U 12Gbit/s SAS 75disk slot 3.5inch disk enclosure), 40 (2U dual controller 12Gbit/s SAS 25disk slot 2.5inch controller enclosure), 65 (2U 12Gbit/s SAS 25disk slot 2.5inch disk enclosure), 66 (4U 12Gbit/s SAS 24disk slot 3.5inch disk enclosure), 67 (2U SAS 25disk slot 2.5inch disk enclosure), 69 (4U SAS 24disk slot 3.5inch disk enclosure), 96 (3U dual controllerController enclosure), 97 (6U quad-controllerController enclosure), 98 (2U SSD 25disk cascading enclosure), 99 (2U dual controller 12Gbit/s NVMe 25disk slot 2.5inch controller enclosure), 101 (2U SSD NVMe 25disk slot 2.5inch disk enclosure), 112 (4U quad-controllerController enclosure), 113 (2U dual controller SAS 25disk slot 2.5inch controller enclosure), 114 (2U dual controller SAS 12disk slot 3.5inch controller enclosure), 115 (2U dual controller NVMe 36disk slotController enclosure), 116 (2U dual controller SAS 25disk slot 2.5inch controller enclosure), 117 (2U dual controller SAS 12disk slot 3.5inch controller enclosure), 118 (2U SAS 25disk slot 2.5 inchsmartDisk enclosure), 119 (2U SAS 12disk slot 3.5 inchsmartDisk enclosure), 120 (2U NVMe 36disk slotsmartDisk enclosure), 122 (2U dual controller NVMe 25disk slot 2.5inch controller enclosure), 132 (4U dual controller 4disk slot2.5 inch 6disk slot3.5 inch Controller enclosure), 133 (4U dual controller NVMe 12disk slot 2.5 inch Controller enclosure), 135 (4U dual controller 10disk slot 2.5inch controller enclosure), 143 (8U NVME dual controller 64disk slot 2.5 inch Controller enclosure),
                    height: Height in U (integer),
                    location: Enclosure location (1~128 characters),
                    logic_type:  type. Options: disk_enclosure (Disk enclosure), controller_enclosure (Controller enclosure), data_switch ( dataSwitch), management_switch (management Switch), management_server (management Server),
                    health_status: Health status. Options: unknown, normal, faulty ( fault),
                    running_status: Running status. Options: unknown, normal, running, sleep_in_high_temperature, online, offline, abnormalxception),
                    storage_id: Storage deviceID (1~64 characters),
                    storage_name: Storage device name (1~128 characters),
                    storage_ip: Storage deviceIP address (1~32 characters),
                    storage_sn: Storage deviceSerial number (1~64 characters),
                    storage_location: Storage device location (0~512 characters),
                    zone_name: Zone name (0~512 characters), OceanStor A800 series only,
                    zone_ip: Zone IP address (1~128 characters), OceanStor A800 series only,
                    zone_id: Zone ID (0~512 characters), OceanStor A800 series only,
                    esn: EnclosureSerial number (0~512 characters),
                    mac: MAC address (0~512 characters),
                    power_mode: Power supply mode. Options: load_balance (Load balancing mode), active_standby_power (Primary/standby power mode),
                    bar_code:  barcode (0~256 characters),
                    board_type: Board type (0~128 characters),
                    description:  description (0~1024 characters),
                    temperature: Temperature in °C (0~128 characters),
                 }, ...]
        }
    """
    url = "/rest/storagemgmt/v1/enclosures/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    param_map = {
        'storage_id': storage_id,
        'name': name,
        'location': location,
        'health_status': health_status,
        'zone_name': zone_name,
        'zone_id': zone_id,
        'running_status': running_status,
        'power_mode': power_mode,
        'esn': esn,
        'mac': mac,
        'sort_key': sort_key,
        'sort_dir': sort_dir,
    }

    for key, value in param_map.items():
        if value is not None:
            payload[key] = value

    response = client.post(url, body=payload)
    return response


def initiator_list(client: DMEAPIClient, page_size: int = None, page_no: int = None,
                   raw_id: str = None, alias: str = None, status: str = None,
                   associated_host_name: str = None, associated_host_id: str = None,
                   multipath_type: str = None, protocol: str = None,
                   support_provisioning: bool = None, vstore_raw_id: str = None,
                   vstore_name: str = None, storage_id: str = None) -> dict:
    """
    Batch query storage initiator objects

    Batch query storage initiator object list. 

    Args:
        client: DME API client
        page_size: Items per page (Optional, 1~1000, default 100)
        page_no: Page number (Optional, min1, default1)
        raw_id: InitiatorWWPN/IQN/NQN (Optional, 0~256 characters, supports fuzzy match)
        alias: Initiator alias (Optional, 0~256 characters, supports fuzzy match)
        status: Initiator status (Optional). Options: unknown, online, offline
        associated_host_name: Initiator associatedHost name (Optional, 0~256 characters, supports fuzzy match)
        associated_host_id: Initiator associatedHost ID (Optional, 0~64 characters; Empty field queries hosts not addedInitiator)
        multipath_type: Third-party multipath policy (Optional, only for non-Dorado V6 product). Options: default (default), third_party (Third-party multipath)
        protocol: Initiator type (Optional). Options: fc, iscsi, nvme_over_roce, sas, nvme_over_fabric, unknown
        support_provisioning: Supports provisioning (Optional). Options: true, false
        vstore_raw_id: Tenant ID (Optional)
        vstore_name: Tenant name (Optional)
        storage_id: Storage device ID (Optional, 0~64 characters)

    Returns:
        Initiator list
    """
    url = "/rest/hostmgmt/v1/storage-initiators/query"

    payload = {}

    if page_size is not None:
        payload['page_size'] = page_size
    if page_no is not None:
        payload['page_no'] = page_no
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if alias is not None:
        payload['alias'] = alias
    if status is not None:
        payload['status'] = status
    if associated_host_name is not None:
        payload['associated_host_name'] = associated_host_name
    if associated_host_id is not None:
        payload['associated_host_id'] = associated_host_id
    if multipath_type is not None:
        payload['multipath_type'] = multipath_type
    if protocol is not None:
        payload['protocol'] = protocol
    if support_provisioning is not None:
        payload['support_provisioning'] = support_provisioning
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if vstore_name is not None:
        payload['vstore_name'] = vstore_name
    if storage_id is not None:
        payload['storage_id'] = storage_id

    response = client.post(url, body=payload)
    return response


def initiator_delete(client: DMEAPIClient, initiator_ids: list,
                     task_remarks: str = None) -> dict:
    """
    Batch delete storage device initiator objects

    Args:
        client: DME API client
        initiator_ids: Initiator ID  list (Required, 1-100) 
        task_remarks: Task remark(Optional, max 1024  character) 

    Returns:
        task  ID
    """
    url = "/rest/hostmgmt/v1/storage-initiators/delete"

    payload = {
        'initiator_ids': initiator_ids
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def initiator_modify(client: DMEAPIClient, initiator_id: str,
                     vstore_id: str = None, alias: str = None,
                     multi_path: dict = None) -> dict:
    """
    modify  storage initiatorobject

    modify Initiator, This operation modifies storage specified on the deviceInitiator. 

    Args:
        client: DME API client
        initiator_id: Initiator ID (Required)
        vstore_id: Tenant ID (Optional, 1~64 characters;  effective for OceanStor V300R006C30/V500R007C20/Dorado 6.1.3+ when)
        alias: Initiator alias (Optional, 0~31 characters, supports alphanumeric._-and Chinese characters)
        multi_path: ModifyMultiPathRequestParam object (Optional;  effective for OceanStor V300R003C20/V500R007C20/Dorado V300R001C01+above support).  format: {
                multi_path_type: InitiatorMultipath type (Optional). Options: default (default), third_party (Third-party multipath),
                path_type: Initiator path type (conditionally required, required when multi_path_type is third_party). Options: optimal_path (Preferred path), non_optimal_path (non-preferred path),
                failover_mode: Initiator switch mode (conditionally required, required when multi_path_type is third_party). Options: early_version_alua, common_alua, alua_not_used, special_alua,
                special_mode_type: Special mode type (Optional, effective when failover mode is special). Options: 0 (Special mode0), 1 (Special mode1), 2 (Special mode2), 3 (Special mode3)
             }

    Returns:
        task  ID
    """
    url = "/rest/hostmgmt/v1/storage-initiators/{initiator_id}"

    payload = {}

    if vstore_id is not None:
        payload['vstore_id'] = vstore_id
    if alias is not None:
        payload['alias'] = alias
    if multi_path is not None:
        payload['multi_path'] = multi_path

    payload = {}

    if vstore_id is not None:
        payload['vstore_id'] = vstore_id
    if alias is not None:
        payload['alias'] = alias
    if multi_path is not None:
        payload['multi_path'] = multi_path

    response = client.put(url, body=payload, params={"initiator_id": initiator_id})
    return response


# ============ auth user (account) subtopic functions ============


def account_show_local_users(client: DMEAPIClient, storage_id: str, vstore_raw_id: str = None,
                     name: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query storage devicelocal Auth user info

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, 1~36  characters) 
        vstore_raw_id: local auth userTenanton device ID(Optional) 
        name: local Auth user name, supports fuzzy search(Optional) 
        page_no: Page number, default 1(Optional) 
        page_size: Page size, default 20(Optional) 

    Returns:
        local Auth user info list, includes total and local_users
    """
    url = "/rest/fileservice/v1/storages/{storage_id}/local-users/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if name is not None:
        payload['name'] = name

    response = client.post(url, body=payload)
    return response


def account_create_local_user(client: DMEAPIClient, storage_id: str, name: str, password: str,
                      primary_group_raw_id: str, description: str = None,
                      group_names: list = None, vstore_id: str = None) -> dict:
    """
    Create local auth user

    Args:
        client: DME API client
        storage_id: Create local auth userStorage device ID (1~36 characters, Required)
        name: local Auth user name (1~255 characters, Required)
        description: local Auth user description (1~255 characters, Optional)
        password: local Auth user password (1~255 characters, Required)
        primary_group_raw_id: local auth user group ID on device (1~64 characters, Required)
        group_names: create  local auth usertemporary user group name list (List<string>, min array members: 0, max array members: 31, Optional)
        vstore_id: local auth usertenant ID (1~64 characters, Optional. conditionally required, required when creating local auth user belongs to tenant)

    Returns:
        creation result
    """
    url = "/rest/fileservice/v1/storages/{storage_id}/local-users"

    payload = {
        'name': name,
        'password': password,
        'primary_group_raw_id': primary_group_raw_id,
    }

    if description is not None:
        payload['description'] = description

    payload = {
        'name': name,
        'password': password,
        'primary_group_raw_id': primary_group_raw_id,
    }

    if description is not None:
        payload['description'] = description
    if group_names is not None:
        payload['group_names'] = group_names
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id

    response = client.post(url, body=payload)
    return response


def account_create_unix_user(client: DMEAPIClient, storage_id: str, name: str,
                      primary_group_raw_id: str, raw_id: int = None,
                      description: str = None, password: str = None,
                      status_enabled: bool = None, vstore_raw_id: str = None) -> dict:
    """
    Create storage device UNIX auth user

    Args:
        client: DME API client
        storage_id: create  UNIX auth userStorage device ID (1~36 characters, Required)
        name: UNIX Auth user name (1~255 characters, Required)
        raw_id: UNIX Auth user on device ID (int64, 0~4294967295, Optional)
        description: UNIX Auth user description (1~255 characters, Optional)
        password: UNIX Auth user password (1~255 characters, Optional)
        status_enabled: UNIX Auth user status (boolean, Optional). Options: true ( start), false ( lock)
        primary_group_raw_id: create UNIX auth user group ID on device (1~64 characters, Required)
        vstore_raw_id: UNIX Auth user tenant on device ID (1~64 characters, Optional. conditionally required, when creating UNIXd when auth user belongs to tenant)

    Returns:
        creation result
    """
    url = "/rest/fileservice/v1/storages/{storage_id}/unix-users"

    payload = {
        'name': name,
        'primary_group_raw_id': primary_group_raw_id,
    }

    if raw_id is not None:
        payload['raw_id'] = raw_id
    if description is not None:
        payload['description'] = description
    if password is not None:
        payload['password'] = password
    if status_enabled is not None:
        payload['status_enabled'] = status_enabled
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id

    response = client.post(url, body=payload)
    return response


def account_create_windows_user(client: DMEAPIClient, storage_id: str, name: str, password: str,
                                 raw_id: int = None, description: str = None,
                                 status_enabled: bool = None,
                                 vstore_raw_id: str = None) -> dict:
    """
    Create storage device Windows auth user

    Args:
        client: DME API client
        storage_id: create  Windows auth userStorage device ID (1~36 characters, Required)
        name: Windows Auth user name (1~255 characters, Required)
        raw_id: Windows Auth user on device ID (int64, 1000~4294967295, Optional)
        description: Windows Auth user description (1~255 characters, Optional)
        password: Windows Auth user password (1~255 characters, Required)
        status_enabled: Windows Auth user status (boolean, Optional). Options: true ( enable), false ( lock)
        vstore_raw_id: create Windows Auth user tenant on device ID (1~64 characters, Optional. conditionally required, when creating Windowsrequired when auth user belongs to tenant)

    Returns:
        creation result
    """
    url = "/rest/fileservice/v1/storages/{storage_id}/windows-users"

    payload = {
        'name': name,
        'password': password,
    }

    if raw_id is not None:
        payload['raw_id'] = raw_id
    if description is not None:
        payload['description'] = description
    if status_enabled is not None:
        payload['status_enabled'] = status_enabled
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id

    response = client.post(url, body=payload)
    return response


def account_show_unix_users(client: DMEAPIClient, storage_id: str, vstore_raw_id: str = None,
                    name: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query storage device UNIX Auth user info

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, 1~36  characters) 
        vstore_raw_id: UNIX auth userTenanton device ID(Optional) 
        name: UNIX Auth user name, supports fuzzy search(Optional) 
        page_no: Page number, default 1(Optional) 
        page_size: Page size, default 20(Optional) 

    Returns:
        UNIX Auth user info list, includes total and unix_users
    """
    url = "/rest/fileservice/v1/storages/{storage_id}/unix-users/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if name is not None:
        payload['name'] = name

    response = client.post(url, body=payload)
    return response


def account_show_windows_users(client: DMEAPIClient, storage_id: str, vstore_raw_id: str = None,
                       name: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query storage device Windows Auth user info

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, 1~36  characters) 
        vstore_raw_id: Windows auth userTenanton device ID(Optional) 
        name: Windows Auth user name, supports fuzzy search(Optional) 
        page_no: Page number, default 1(Optional) 
        page_size: Page size, default 20(Optional) 

    Returns:
        Windows Auth user info list, includes total and windows_users
    """
    url = "/rest/fileservice/v1/storages/{storage_id}/windows-users/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if name is not None:
        payload['name'] = name

    response = client.post(url, body=payload)
    return response


def account_show_local_user_groups(client: DMEAPIClient, storage_id: str, vstore_raw_id: str = None,
                           name: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query storage devicelocal Auth user group info

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, 1~36  characters) 
        vstore_raw_id: local  authUser groupTenanton device ID(Optional) 
        name: local Auth user group name, supports fuzzy search(Optional) 
        page_no: Page number, default 1(Optional) 
        page_size: Page size, default 20(Optional) 

    Returns:
        local Auth user group info list, includes total and local_user_groups
    """
    url = "/rest/fileservice/v1/storages/{storage_id}/local-user-groups/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if name is not None:
        payload['name'] = name

    response = client.post(url, body=payload)
    return response


def account_show_unix_user_groups(client: DMEAPIClient, storage_id: str, vstore_raw_id: str = None,
                          name: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query storage device UNIX Auth user group info

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, 1~36  characters) 
        vstore_raw_id: UNIX  authUser groupTenanton device ID(Optional) 
        name: UNIX Auth user group name, supports fuzzy search(Optional) 
        page_no: Page number, default 1(Optional) 
        page_size: Page size, default 20(Optional) 

    Returns:
        UNIX Auth user group info list, includes total and unix_user_groups
    """
    url = "/rest/fileservice/v1/storages/{storage_id}/unix-user-groups/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if name is not None:
        payload['name'] = name

    response = client.post(url, body=payload)
    return response


def account_show_windows_user_groups(client: DMEAPIClient, storage_id: str, vstore_raw_id: str = None,
                             name: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query storage device Windows Auth user group info

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, 1~36  characters) 
        vstore_raw_id: Windows  authUser groupTenanton device ID(Optional) 
        name: Windows Auth user group name, supports fuzzy search(Optional) 
        page_no: Page number, default 1(Optional) 
        page_size: Page size, default 20(Optional) 

    Returns:
        Windows Auth user group info list, includes total and windows_user_groups
    """
    url = "/rest/fileservice/v1/storages/{storage_id}/windows-user-groups/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if name is not None:
        payload['name'] = name

    response = client.post(url, body=payload)
    return response


# ============ QoS subtopic functions ============


def qos_list(client: DMEAPIClient, storage_id: str, name: str = None,
             raw_id: str = None, enable_status: bool = None,
             running_status: str = None, zone_id: str = None,
             resource_type_list: list = None, vstore_id: str = None,
             vstore_name: str = None, alarm_status: str = None,
             io_policy_type: str = None, page_no: int = 1,
             page_size: int = 10, sort_key: str = None,
             sort_dir: str = None) -> dict:
    """
    Batch query QoS  policy

    Args:
        client: DME API client
        storage_id: Storage device ID (Required) 
        name: QoS  policyName (Optional,1~256  character) 
        raw_id: QoS  policydevice side ID(Optional) 
        enable_status: Active status(Optional, true/false) 
        running_status: Running status(Optional, running/inactive/waiting) 
        zone_id:  ZONE ID(Optional) 
        resource_type_list:  Controlled resource type list(Optional, file_system/vstore/none) 
        vstore_id: Tenant ID(Optional) 
        vstore_name: Tenant name(Optional) 
        alarm_status: Alarm status(Optional, normal/event/alarm/invalid) 
        io_policy_type: IO Policy type(Optional, total_perf_upper_limit/read_or_write_upper_limit) 
        page_no: Page number(Optional, default 1) 
        page_size: per pagecount(Optional, default 10,  max 1000) 
        sort_key: Sort field(Optional, name/raw_id) 
        sort_dir: Sort method(Optional, asc/desc) 
    """
    url = "/rest/storagepolicy/v1/qos/query"

    payload = {
        'storage_id': storage_id,
        'page_no': page_no,
        'page_size': page_size
    }

    if name is not None:
        payload['name'] = name
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if enable_status is not None:
        payload['enable_status'] = enable_status
    if running_status is not None:
        payload['running_status'] = running_status
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if resource_type_list is not None:
        payload['resource_type_list'] = resource_type_list
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id
    if vstore_name is not None:
        payload['vstore_name'] = vstore_name
    if alarm_status is not None:
        payload['alarm_status'] = alarm_status
    if io_policy_type is not None:
        payload['io_policy_type'] = io_policy_type
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def qos_show(client: DMEAPIClient, qos_policy_id: str) -> dict:
    """
    Query QoS  policy details

    Args:
        client: DME API client
        qos_policy_id: QoS  policy ID (Required) 
    """
    url = "/rest/storagepolicy/v1/qos/{qos_policy_id}/detail"
    response = client.get(url, params={"qos_policy_id": qos_policy_id})
    return response


def qos_create(client: DMEAPIClient, name: str, storage_id: str,
               resource_type: str, resource_ids: list,
               description: str = None, zone_id: str = None,
               vstore_id: str = None, enable_status: str = 'enable',
               io_policy_type: str = None, min_bandwidth: int = None,
               max_bandwidth: int = None, burst_bandwidth: int = None,
               min_iops: int = None, max_iops: int = None,
               burst_iops: int = None, burst_time: int = None,
               latency: int = None, max_read_bandwidth: int = None,
               max_write_bandwidth: int = None,
               burst_read_bandwidth: int = None,
               burst_write_bandwidth: int = None,
               max_read_iops: int = None, max_write_iops: int = None,
               burst_read_iops: int = None, burst_write_iops: int = None,
               alarm_switch: str = None, alarm_level: str = None,
               alarm_threshold: int = None, resume_threshold: int = None,
               schedule_policy: str = None, schedule_start_date: str = None,
               start_time: str = None, duration: int = None,
               weekly_days: list = None) -> dict:
    """
    create  QoS  policy

    create a new QoS  policy, Can configure performance limits, Alarm parameters and scheduled scheduling. 

    Args:
        client: DME API client
        name: QoS Policy name (Required, 1~31  character) 
        storage_id: Storage device ID (Required) 
        resource_type:  Controlled resource type (Required, file_system/vstore) 
        resource_ids:  controllerd resource ID  list (Required, array of 1-512 members) 
        description:  description(Optional, 1~255  character) 
        zone_id:  ZONE ID(Optional, A series storageRequired) 
        vstore_id: Tenant ID(Optional, required when resource_type is file_system) 
        enable_status: Active status(Optional, enable/disable, default enable) 
        io_policy_type: IO Policy type(Optional, total_perf_upper_limit/read_or_write_upper_limit) 
        min_bandwidth: Min bandwidth MB/s(Optional) 
        max_bandwidth: Max bandwidth MB/s(Optional) 
        burst_bandwidth: Burst bandwidth MB/s(Optional, must be greater than max_bandwidth) 
        min_iops:  min IOPS(Optional) 
        max_iops:  max IOPS(Optional) 
        burst_iops: burst IOPS(Optional, must be greater than max_iops) 
        burst_time:  maxburstduration seconds(Optional, 1~999999999) 
        latency: IO  latency metric micro seconds(Optional, 500/1500) 
        max_read_bandwidth:  maxRead bandwidth MB/s(Optional) 
        max_write_bandwidth:  maxWrite bandwidth MB/s(Optional) 
        burst_read_bandwidth: burstRead bandwidth MB/s(Optional) 
        burst_write_bandwidth: burstWrite bandwidth MB/s(Optional) 
        max_read_iops:  Max read IOPS(Optional) 
        max_write_iops:  Max write IOPS(Optional) 
        burst_read_iops: Burst read IOPS(Optional) 
        burst_write_iops: Burst write IOPS(Optional) 
        alarm_switch: alarm switch(Optional, on/off) 
        alarm_level: Alarm severity(Optional, event/alarm) 
        alarm_threshold: alarmthreshold%(Optional, 0~100) 
        resume_threshold:  resumethreshold%(Optional, 0~100) 
        schedule_policy: Scheduling policy(Optional, once/daily/weekly) 
        schedule_start_date: Effective start date(Optional, yyyy-MM-dd) 
        start_time: effectiveStart time(Optional, hh:mm) 
        duration: effectiveduration seconds(Optional, 1800~86400) 
        weekly_days: Weekly scheduling policy(Optional, [0-6]  corresponding to Sunday to Saturday) 
    """
    url = "/rest/storagepolicy/v1/qos"

    payload = {
        'name': name,
        'storage_id': storage_id,
        'resource_type': resource_type,
        'resource_ids': resource_ids
    }

    if description is not None:
        payload['description'] = description
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id
    if enable_status is not None:
        payload['enable_status'] = enable_status

    io_param = {}
    if io_policy_type is not None:
        io_param['io_policy_type'] = io_policy_type
    if min_bandwidth is not None:
        io_param['min_bandwidth'] = min_bandwidth
    if max_bandwidth is not None:
        io_param['max_bandwidth'] = max_bandwidth
    if burst_bandwidth is not None:
        io_param['burst_bandwidth'] = burst_bandwidth
    if min_iops is not None:
        io_param['min_iops'] = min_iops
    if max_iops is not None:
        io_param['max_iops'] = max_iops
    if burst_iops is not None:
        io_param['burst_iops'] = burst_iops
    if burst_time is not None:
        io_param['burst_time'] = burst_time
    if latency is not None:
        io_param['latency'] = latency
    if max_read_bandwidth is not None:
        io_param['max_read_bandwidth'] = max_read_bandwidth
    if max_write_bandwidth is not None:
        io_param['max_write_bandwidth'] = max_write_bandwidth
    if burst_read_bandwidth is not None:
        io_param['burst_read_bandwidth'] = burst_read_bandwidth
    if burst_write_bandwidth is not None:
        io_param['burst_write_bandwidth'] = burst_write_bandwidth
    if max_read_iops is not None:
        io_param['max_read_iops'] = max_read_iops
    if max_write_iops is not None:
        io_param['max_write_iops'] = max_write_iops
    if burst_read_iops is not None:
        io_param['burst_read_iops'] = burst_read_iops
    if burst_write_iops is not None:
        io_param['burst_write_iops'] = burst_write_iops

    if io_param:
        payload['io_param'] = io_param

    if alarm_switch is not None:
        payload['alarm_switch'] = alarm_switch
    if alarm_level is not None:
        payload['alarm_level'] = alarm_level
    if alarm_threshold is not None:
        payload['alarm_threshold'] = alarm_threshold
    if resume_threshold is not None:
        payload['resume_threshold'] = resume_threshold

    if schedule_policy is not None or schedule_start_date is not None or \
       start_time is not None or duration is not None or weekly_days is not None:
        schedule_start_time = {}
        if schedule_policy is not None:
            schedule_start_time['schedule_policy'] = schedule_policy
        if schedule_start_date is not None:
            schedule_start_time['schedule_start_date'] = schedule_start_date
        if start_time is not None:
            schedule_start_time['start_time'] = start_time
        if duration is not None:
            schedule_start_time['duration'] = duration
        if weekly_days is not None:
            schedule_start_time['weekly_days'] = weekly_days
        payload['schedule_start_time'] = schedule_start_time

    response = client.post(url, body=payload)
    return response


def qos_modify(client: DMEAPIClient, qos_policy_id: str,
               name: str = None, description: str = None,
               io_policy_type: str = None, min_bandwidth: int = None,
               max_bandwidth: int = None, burst_bandwidth: int = None,
               min_iops: int = None, max_iops: int = None,
               burst_iops: int = None, burst_time: int = None,
               latency: int = None, max_read_bandwidth: int = None,
               max_write_bandwidth: int = None,
               burst_read_bandwidth: int = None,
               burst_write_bandwidth: int = None,
               max_read_iops: int = None, max_write_iops: int = None,
               burst_read_iops: int = None, burst_write_iops: int = None,
               alarm_switch: str = None, alarm_level: str = None,
               alarm_threshold: int = None, resume_threshold: int = None) -> dict:
    """
    modify  QoS  policy

    Modify existing QoS policy configuration. 

    Args:
        client: DME API client
        qos_policy_id: QoS  policy ID (Required) 
        name: QoS Policy name(Optional) 
        description:  description(Optional) 
        io_policy_type: IO Policy type(Optional) 
        min_bandwidth: Min bandwidth MB/s(Optional) 
        max_bandwidth: Max bandwidth MB/s(Optional) 
        burst_bandwidth: Burst bandwidth MB/s(Optional) 
        min_iops:  min IOPS(Optional) 
        max_iops:  max IOPS(Optional) 
        burst_iops: burst IOPS(Optional) 
        burst_time:  maxburstduration seconds(Optional) 
        latency: IO  latency metric micro seconds(Optional) 
        max_read_bandwidth:  maxRead bandwidth MB/s(Optional) 
        max_write_bandwidth:  maxWrite bandwidth MB/s(Optional) 
        burst_read_bandwidth: burstRead bandwidth MB/s(Optional) 
        burst_write_bandwidth: burstWrite bandwidth MB/s(Optional) 
        max_read_iops:  Max read IOPS(Optional) 
        max_write_iops:  Max write IOPS(Optional) 
        burst_read_iops: Burst read IOPS(Optional) 
        burst_write_iops: Burst write IOPS(Optional) 
        alarm_switch: alarm switch(Optional) 
        alarm_level: Alarm severity(Optional) 
        alarm_threshold: alarmthreshold%(Optional) 
        resume_threshold:  resumethreshold%(Optional) 
    """
    url = "/rest/storagepolicy/v1/qos/{qos_policy_id}"

    payload = {}

    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description

    io_param = {}

    payload = {}

    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description

    io_param = {}
    if io_policy_type is not None:
        io_param['io_policy_type'] = io_policy_type
    if min_bandwidth is not None:
        io_param['min_bandwidth'] = min_bandwidth
    if max_bandwidth is not None:
        io_param['max_bandwidth'] = max_bandwidth
    if burst_bandwidth is not None:
        io_param['burst_bandwidth'] = burst_bandwidth
    if min_iops is not None:
        io_param['min_iops'] = min_iops
    if max_iops is not None:
        io_param['max_iops'] = max_iops
    if burst_iops is not None:
        io_param['burst_iops'] = burst_iops
    if burst_time is not None:
        io_param['burst_time'] = burst_time
    if latency is not None:
        io_param['latency'] = latency
    if max_read_bandwidth is not None:
        io_param['max_read_bandwidth'] = max_read_bandwidth
    if max_write_bandwidth is not None:
        io_param['max_write_bandwidth'] = max_write_bandwidth
    if burst_read_bandwidth is not None:
        io_param['burst_read_bandwidth'] = burst_read_bandwidth
    if burst_write_bandwidth is not None:
        io_param['burst_write_bandwidth'] = burst_write_bandwidth
    if max_read_iops is not None:
        io_param['max_read_iops'] = max_read_iops
    if max_write_iops is not None:
        io_param['max_write_iops'] = max_write_iops
    if burst_read_iops is not None:
        io_param['burst_read_iops'] = burst_read_iops
    if burst_write_iops is not None:
        io_param['burst_write_iops'] = burst_write_iops

    if io_param:
        payload['io_param'] = io_param

    if alarm_switch is not None:
        payload['alarm_switch'] = alarm_switch
    if alarm_level is not None:
        payload['alarm_level'] = alarm_level
    if alarm_threshold is not None:
        payload['alarm_threshold'] = alarm_threshold
    if resume_threshold is not None:
        payload['resume_threshold'] = resume_threshold

    response = client.put(url, body=payload, params={"qos_policy_id": qos_policy_id})
    return response


def qos_delete(client: DMEAPIClient, qos_policy_ids: list) -> dict:
    """
    delete  QoS  policy

    Delete one or more QoS  policy. 

    Args:
        client: DME API client
        qos_policy_ids: QoS  policy ID  list (Required, 1-100) 
    """
    url = "/rest/storagepolicy/v1/qos/delete"

    payload = {
        'ids': qos_policy_ids
    }

    response = client.post(url, body=payload)
    return response


def qos_activate(client: DMEAPIClient, qos_policy_ids: list) -> dict:
    """
    batch activate QoS  policy

    Activate one or more QoS  policy. 

    Args:
        client: DME API client
        qos_policy_ids: QoS  policy ID  list (Required) 
    """
    url = "/rest/storagepolicy/v1/qos/active"

    payload = {
        'qos_ids': qos_policy_ids
    }

    response = client.post(url, body=payload)
    return response


def qos_deactivate(client: DMEAPIClient, qos_policy_ids: list) -> dict:
    """
    Batch deactivate QoS  policy

    Deactivateone or more QoS  policy. 

    Args:
        client: DME API client
        qos_policy_ids: QoS  policy ID  list (Required) 
    """
    url = "/rest/storagepolicy/v1/qos/inactive"

    payload = {
        'qos_ids': qos_policy_ids
    }

    response = client.post(url, body=payload)
    return response


def qos_associate(client: DMEAPIClient, qos_policy_id: str,
                  resource_ids: list, resource_type: str) -> dict:
    """
    QoS Associate policy with control resource

    One or more resourcesassociated with QoS  policy. 

    Args:
        client: DME API client
        qos_policy_id: QoS  policy ID (Required) 
        resource_ids:  resource ID  list (Required) 
        resource_type: Resource type (Required, file_system/vstore) 
    """
    url = "/rest/storagepolicy/v1/qos/{qos_policy_id}/resources/associate"

    payload = {
        'resource_ids': resource_ids,
        'resource_type': resource_type
    }

    response = client.post(url, params={"qos_policy_id": qos_policy_id})
    return response


def qos_unassociate(client: DMEAPIClient, qos_policy_id: str,
                    resource_ids: list, resource_type: str) -> dict:
    """
    QoS Disassociate policy from control resource

    Disassociate resource from QoS policy. 

    Args:
        client: DME API client
        qos_policy_id: QoS  policy ID (Required) 
        resource_ids:  resource ID  list (Required) 
        resource_type: Resource type (Required) 
    """
    url = "/rest/storagepolicy/v1/qos/{qos_policy_id}/resources/unassociate"

    payload = {
        'resource_ids': resource_ids,
        'resource_type': resource_type
    }

    response = client.post(url, params={"qos_policy_id": qos_policy_id})
    return response


# ============  storageLogic port (logic_port) subtopic functions ============


def logic_port_list(client: DMEAPIClient, storage_id: str = None, vstore_raw_id: str = None,
                    zone_raw_id: str = None, scope: str = None, page_no: int = 1,
                    page_size: int = 100) -> dict:
    """
    query storage deviceLogic port list

    Args:
        client: DME API client
        storage_id: Storage device ID(Optional, 1~64 characters) 
        vstore_raw_id: vStoreon the storage deviceid(Optional, 1~64 characters) 
        zone_raw_id: Zoneon the deviceID(Optional, 1~64 characters) , OceanStor A800 series only
        scope:  range(Optional). Options: hyperscale, default. OceanStor A800 series only
        page_no: Page number(Optional, 1~10000, default 1) 
        page_size: Page size(Optional, 1~1000, default 100) 

    Returns:
        {
            total: Logic port count (integer),
            logic_ports: Logic port list (List<StorageLogicPortResp>). 参数格式如下：[{
                id:  logicalPort ID (1~255 characters),
                raw_id: Logic porton the storage deviceID (1~255 characters),
                name:  logicalPort name (1~255 characters),
                running_status: Running status. Options: UNKNOWN, NORMAL, RUNNING, LINK_UP, LINK_DOWNconnected), TO_BE_RECOVERED (pendingsume), INITIALIZING (Initializing), STANDBY ( pending), POWERING_ON ( powering on), POWERED_OFF ( powered off), POWER_ON_FAILED ( power on failure),
                operational_status: Active status. Options: ACTIVATED ( activate), NOT_ACTIVATED (inactive),
                mgmt_ip: ipv4 address (1~255 characters),
                ipv4_gateway: Logic port gatewayIP address(IPV4) (1~64 characters),
                ipv4_mask: Logic portIPNetmask(IPV4) (1~64 characters),
                mgmt_ipv6: ipv6 address (1~255 characters),
                ipv6_mask: Logic portIPNetmask(IPV6) (1~128 characters),
                ipv6_gateway: Logic port gatewayIP address(IPV6) (1~128 characters),
                home_port_raw_id: Parent porton the storage deviceID (1~255 characters),
                home_port_name: Parent port name (1~255 characters),
                home_port_type: Parent port type. Options: ETHERNET_PORT, BOND, VLAN, VIPIP), SIP (SIP), IB (IB),
                home_controller_raw_id: Storage deviceon primary controllerID (1~256 characters),
                current_port_raw_id: Logic portCurrent physical porton the storage deviceID (1~255 characters),
                current_port_name: Logic portcurrent physicalPort name (1~255 characters),
                role:  port role (1~10 characters). Options: 0 (unknown), 1 (management ), 2 ( data), 3 (management + data), 4 (replication), 6 (currently, 6 (currently meaningless), 7 (currently meaningless)), 7 (currently meaningless), 8 (Client), 9 (VTEP), 10 (Health check), 11 ( data backup), 12 (System management), 100 ( cluster), 101 ( inter-cluster),
                ddns_status: Dynamic DNS status. Options: INVALID, ENABLE, DISABLED,
                failover_group_raw_id: Failover group ID on storage device (1~255 characters),
                failover_group_name: Failover group busi failover group name (1~255 characters),
                support_protocol: Logic port supported protocols. Options: NONE, NFS (NFS protocol), CIFS, NFS_AND_CIFS (NFS and CIFS protocol), NFS_OVER_RDMA (NFS over RDMA protocol), iSCSI (iSCSI protocol), FC/FCoE (FC/FCoE protocol), NVME_OVER_ROCE (NVME over ROCE protocol), BGP (BGP protocol), DATA_TURBO (DataTurbo protocol), DATA_TURBO_OVER_ROCE (DataTurbo over ROCE protocol), S3 (S3 protocol), NFS_OVER_IB (NFS over IB protocol), DATA_TURBO_OVER_IB (DataTurbo over IB protocol), DATA_TURBO_OVER_ROCE_AND_TCP (DataTurbo over ROCE and TCP protocol), OBJECT (S3 protocol), NAS_AND_OBJECT (NAS and objectStorage protocol), KB_OVER_TCP (KnowledgeBase over TCP protocol),
                logical_type:  logical type. Options: SERVICE, MANAGEMENT, MAINTENANCEaintenance port),
                listen_dns_query_enabled:  Whether to listen for DNS queries (1~255 characters). Options: NO, YES,
                management_access: Management access method (1~255 characters),
                vstore_raw_id: Logic port vStore ID on device (1~255 characters),
                vstore_name: Logic portvStore name (1~255 characters),
                storage_id: Storage device ID (1~255 characters),
                storage_name: Storage device name (1~255 characters),
                zone_raw_id: Zoneon the deviceID (1~255 characters), OceanStor A800 series only,
                zone_id: Zone ID (1~64 characters), OceanStor A800 series only,
                zone_name: zone name (1~255 characters), OceanStor A800 series only,
                zone_ip: zone IP (1~255 characters),
                dns_zone_name: DNS Zone name (1~255 characters),
                current_port_type: Logic portPhysical port type. Options: ETHERNET_PORT, BOND, VLAN, VIPIP), SIP (SIP), IB (IB),
                address_family: IPProtocol version. Options: IPv4 (IPv4), IPv6 (IPv6),
                can_failover: Enable IP address drift (boolean). Options: true, false,
                failback_mode: Drift-back mode. Options: not_support, manual, automatic,
                scope:  range. Options: hyperscale, default. OceanStor A800 series only,
                logicPortTags: Associated tag set (List<Tag>). 参数格式如下：[{
                    id:  tag ID (1~32 characters),
                    tag_type_name: Tag type name (1~64 characters),
                    name: Tag name (1~128 characters),
                }, ...],
                manufacturer:  vendor (1~32 characters),
                storage_model:  model (1~64 characters),
            }, ...]
        }
    """
    url = "/rest/storagemgmt/v2/logic-ports/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if storage_id is not None:
        payload['storage_id'] = storage_id
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if zone_raw_id is not None:
        payload['zone_raw_id'] = zone_raw_id
    if scope is not None:
        payload['scope'] = scope

    response = client.post(url, body=payload)
    return response


def logic_port_show(client: DMEAPIClient, logic_port_id: str) -> dict:
    """
    query storage deviceLogic port details

    Args:
        client: DME API client
        logic_port_id: Logic port ID (Required, 1~64  characters, UUID format or 32-bit hex) 

    Returns:
        {
            id:  logicalPort ID (1~255 characters),
            raw_id: Logic porton the storage deviceID (1~255 characters),
            name:  logicalPort name (1~255 characters),
            running_status: Running status. Options: UNKNOWN, NORMAL, RUNNING, LINK_UP, LINK_DOWNconnected), TO_BE_RECOVERED (pendingsume), INITIALIZING (Initializing), STANDBY ( pending), POWERING_ON ( powering on), POWERED_OFF ( powered off), POWER_ON_FAILED ( power on failure),
            operational_status: Active status. Options: ACTIVATED ( activate), NOT_ACTIVATED (inactive),
            mgmt_ip: ipv4 address (1~255 characters),
            ipv4_gateway: Logic port gatewayIP address(IPV4) (1~64 characters),
            ipv4_mask: Logic portIPNetmask(IPV4) (1~64 characters),
            mgmt_ipv6: ipv6 address (1~255 characters),
            ipv6_mask: Logic portIPNetmask(IPV6) (1~128 characters),
            ipv6_gateway: Logic port gatewayIP address(IPV6) (1~128 characters),
            home_port_raw_id: Parent porton the storage deviceID (1~255 characters),
            home_port_name: Parent port name (1~255 characters),
            home_port_type: Parent port type. Options: ETHERNET_PORT, BOND, VLAN, VIPIP), SIP (SIP), IB (IB),
            home_controller_raw_id: Storage deviceon primary controllerID (1~256 characters),
            current_port_raw_id: Logic portCurrent physical porton the storage deviceID (1~255 characters),
            current_port_name: Logic portcurrent physicalPort name (1~255 characters),
            role:  port role (1~10 characters). Options: 0 (unknown), 1 (management ), 2 ( data), 3 (management + data), 4 (replication), 6 (currently, 6 (currently meaningless), 7 (currently meaningless)), 7 (currently meaningless), 8 (Client), 9 (VTEP), 10 (Health check), 11 ( data backup), 12 (System management), 100 ( cluster), 101 ( inter-cluster),
            ddns_status: Dynamic DNS status. Options: INVALID, ENABLE, DISABLED,
            failover_group_raw_id: Failover group ID on storage device (1~255 characters),
            failover_group_name: Failover group busi failover group name (1~255 characters),
            support_protocol: Logic port supported protocols. Options: NONE, NFS (NFS protocol), CIFS, NFS_AND_CIFS (NFS and CIFS protocol), NFS_OVER_RDMA (NFS over RDMA protocol), iSCSI (iSCSI protocol), FC/FCoE (FC/FCoE protocol), NVME_OVER_ROCE (NVME over ROCE protocol), BGP (BGP protocol), DATA_TURBO (DataTurbo protocol), DATA_TURBO_OVER_ROCE (DataTurbo over ROCE protocol), S3 (S3 protocol), NFS_OVER_IB (NFS over IB protocol), DATA_TURBO_OVER_IB (DataTurbo over IB protocol), DATA_TURBO_OVER_ROCE_AND_TCP (DataTurbo over ROCE and TCP protocol), OBJECT (S3 protocol), NAS_AND_OBJECT (NAS and objectStorage protocol), KB_OVER_TCP (KnowledgeBase over TCP protocol),
            logical_type:  logical type. Options: SERVICE, MANAGEMENT, MAINTENANCEaintenance port),
            listen_dns_query_enabled:  Whether to listen for DNS queries (1~255 characters). Options: NO, YES,
            management_access: Management access method (1~255 characters),
            vstore_raw_id: Logic port vStore ID on device (1~255 characters),
            vstore_name: Logic portvStore name (1~255 characters),
            storage_id: Storage device ID (1~255 characters),
            storage_name: Storage device name (1~255 characters),
            zone_raw_id: Zoneon the deviceID (1~255 characters), OceanStor A800 series only,
            zone_id: Zone ID (1~64 characters), OceanStor A800 series only,
            zone_name: zone name (1~255 characters), OceanStor A800 series only,
            zone_ip: zone IP (1~255 characters),
            dns_zone_name: DNS Zone name (1~255 characters),
            current_port_type: Logic portPhysical port type. Options: ETHERNET_PORT, BOND, VLAN, VIPIP), SIP (SIP), IB (IB),
            address_family: IPProtocol version. Options: IPv4 (IPv4), IPv6 (IPv6),
            can_failover: Enable IP address drift (boolean). Options: true, false,
            failback_mode: Drift-back mode. Options: not_support, manual, automatic,
            scope:  range. Options: hyperscale, default. OceanStor A800 series only,
            logicPortTags: Associated tag set (List<Tag>). 参数格式如下：[{
                id:  tag ID (1~32 characters),
                tag_type_name: Tag type name (1~64 characters),
                name: Tag name (1~128 characters),
            }, ...],
            manufacturer:  vendor (1~32 characters),
            storage_model:  model (1~64 characters),
        }
    """
    url = "/rest/storagemgmt/v1/logic-ports/{logic_port_id}"

    response = client.get(url, params={"logic_port_id": logic_port_id})
    return response


def logic_port_create(client: DMEAPIClient, storage_id: str, name: str, address_family: str,
                      home_port_type: str, zone_raw_id: str, scope: str,
                      mgmt_ip: str = None, ipv4_mask: str = None, ipv4_gateway: str = None,
                      mgmt_ipv6: str = None, ipv6_mask: str = None, ipv6_gateway: str = None,
                      home_port_raw_id: str = None, support_protocol: str = None,
                      operational_status: str = None, home_controller_id: str = None,
                      failover_group_raw_id: str = None, vstore_raw_id: str = None,
                      role: str = None, dns_zone_name: str = None,
                      listen_dns_query_enabled: str = None, can_failover: bool = None,
                      failback_mode: str = None) -> dict:
    """
    Create logic port (OceanStor A800 only) 

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, 1~64 characters) 
        name: Port name (Required, 1~255 characters) . Only letters and digits allowed, "_", "-", "."and Chinese characters
        address_family: IPProtocol version (Required). Options: IPv4 (IPv4), IPv6 (IPv6)
        home_port_type: Parent port type (Required). Options: ETHERNET_PORT, BOND, VLAN, VIPIP), SIP (SIP), IB (IB)
        zone_raw_id: Zoneon the deviceID (Required, 1~64 characters) , OceanStor A800 series only
        scope:  range (Required). Options: hyperscale, default. OceanStor A800 series only. Data access protocol is KB_OVER_TCP when value only supportsfault
        mgmt_ip: Logic portIP address(IPV4)(Optional, max64 characters, IPv4 format) 
        ipv4_mask: Logic portIPNetmask(IPV4)(Optional, max64 characters) 
        ipv4_gateway: Logic port gatewayIP address(IPV4)(Optional, max64 characters) 
        mgmt_ipv6: Logic portIP address(IPV6)(Optional, max128 characters) 
        ipv6_mask: Logic portIPNetmask(IPV6)(Optional, max128 characters) 
        ipv6_gateway: Logic port gatewayIP address(IPV6)(Optional, max128 characters) 
        home_port_raw_id: Parent porton the storage deviceID(Optional, 1~64 characters) 
        support_protocol: Logic port supported protocols(Optional). Options: NFS (NFS protocol), DATA_TURBO_OVER_ROCE (DataTurbo over RoCE protocol), NFS_OVER_RDMA (NFS over RDMA protocol), NFS_OVER_IB (NFS over IB protocol), DATA_TURBO_OVER_IB (DataTurbo over IB protocol), DATA_TURBO_OVER_ROCE_AND_TCP (DataTurbo over RoCE and TCP protocol), OBJECT (S3 protocol), NAS_AND_OBJECT (NAS and objectStorage protocol), KB_OVER_TCP (KnowledgeBase over TCP protocol). when role is CLIENT, do not send this field
        operational_status: Active status(Optional). Options: ACTIVATED ( activate), NOT_ACTIVATED (inactive)
        home_controller_id: ControllerID(Optional, 1~64 characters) . when role is HEALTH_CHECK, this field is required
        failover_group_raw_id: Failover group ID on storage device(Optional, max64 characters) . when data access protocol is KB_OVER_TCP, this field is required
        vstore_raw_id: Logic port vStore ID on device(Optional, max64 characters) . when role is CLIENT, do not send this field
        role: Logic port role(Optional, default DATA). Options: MANAGEMENT (management ), DATA ( data), VTEP (VTEP), HEALTH_CHECK (Health check), MANAGEMENT_AND_DATA (management + data), CLIENT (Client)
        dns_zone_name: DNS zone name (Optional, max255 characters) . when role is CLIENT or data access protocol is KB_OVER_TCP, do not send this field
        listen_dns_query_enabled:  Whether to listen for DNS queries(Optional,  regex: NO|YES). Options: NO, YES. when role is CLIENT or data access protocol is KB_OVER_TCP, do not send this field
        can_failover: Enable IP address drift(Optional, boolean). Options: true, false. when data access protocol is KB_OVER_TCP, do not send this field
        failback_mode: Drift-back mode(Optional). Options: not_support, manual, automatic. when data access protocol is KB_OVER_TCP, do not send this field

    Returns:
        {
            task_id: task Id (1~64 characters),
        }
    """
    url = "/rest/storagemgmt/v1/logic-ports"

    payload = {
        'storage_id': storage_id,
        'name': name,
        'address_family': address_family,
        'home_port_type': home_port_type,
        'zone_raw_id': zone_raw_id,
        'scope': scope
    }

    if mgmt_ip is not None:
        payload['mgmt_ip'] = mgmt_ip
    if ipv4_mask is not None:
        payload['ipv4_mask'] = ipv4_mask
    if ipv4_gateway is not None:
        payload['ipv4_gateway'] = ipv4_gateway
    if mgmt_ipv6 is not None:
        payload['mgmt_ipv6'] = mgmt_ipv6
    if ipv6_mask is not None:
        payload['ipv6_mask'] = ipv6_mask
    if ipv6_gateway is not None:
        payload['ipv6_gateway'] = ipv6_gateway
    if home_port_raw_id is not None:
        payload['home_port_raw_id'] = home_port_raw_id
    if support_protocol is not None:
        payload['support_protocol'] = support_protocol
    if operational_status is not None:
        payload['operational_status'] = operational_status
    if home_controller_id is not None:
        payload['home_controller_id'] = home_controller_id
    if failover_group_raw_id is not None:
        payload['failover_group_raw_id'] = failover_group_raw_id
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if role is not None:
        payload['role'] = role
    if dns_zone_name is not None:
        payload['dns_zone_name'] = dns_zone_name
    if listen_dns_query_enabled is not None:
        payload['listen_dns_query_enabled'] = listen_dns_query_enabled
    if can_failover is not None:
        payload['can_failover'] = can_failover
    if failback_mode is not None:
        payload['failback_mode'] = failback_mode

    response = client.post(url, body=payload)
    return response


def logic_port_update(client: DMEAPIClient, logic_port_id: str,
                      name: str = None, address_family: str = None,
                      mgmt_ip: str = None, ipv4_mask: str = None, ipv4_gateway: str = None,
                      mgmt_ipv6: str = None, ipv6_mask: str = None, ipv6_gateway: str = None,
                      home_port_raw_id: str = None, home_port_type: str = None,
                      operational_status: str = None, failover_group_raw_id: str = None,
                      dns_zone_name: str = None, listen_dns_query_enabled: str = None,
                      can_failover: bool = None, failback_mode: str = None) -> dict:
    """
    Modify logic port (OceanStor A800 only) 

    Args:
        client: DME API client
        logic_port_id: Logic port ID (Required, 1~128  characters) 
        name: Port name(Optional) 
        address_family: IP Protocol version(Optional) 
        mgmt_ip: Logic port IP  address (IPV4)(Optional) 
        ipv4_mask: Logic port IP Netmask (IPV4)(Optional) 
        ipv4_gateway: Logic port gateway IP  address (IPV4)(Optional) 
        mgmt_ipv6: Logic port IP  address (IPV6)(Optional) 
        ipv6_mask: Logic port IP Netmask (IPV6)(Optional) 
        ipv6_gateway: Logic port gateway IP  address (IPV6)(Optional) 
        home_port_raw_id: Parent porton the storage device ID(Optional) 
        home_port_type: Parent port type(Optional) 
        operational_status: Active status(Optional) 
        failover_group_raw_id: Failover group busi failover groupon the storage device ID(Optional) 
        dns_zone_name: DNS Zone  name(Optional) 
        listen_dns_query_enabled:  whether listen DNS Query request(Optional) 
        can_failover: Enable IP Address drift(Optional) 
        failback_mode: Drift-back mode(Optional) 

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/storagemgmt/v1/logic-ports/{logic_port_id}"

    payload = {}

    if name is not None:
        payload['name'] = name
    if address_family is not None:
        payload['address_family'] = address_family
    if mgmt_ip is not None:
        payload['mgmt_ip'] = mgmt_ip

    payload = {}

    if name is not None:
        payload['name'] = name
    if address_family is not None:
        payload['address_family'] = address_family
    if mgmt_ip is not None:
        payload['mgmt_ip'] = mgmt_ip
    if ipv4_mask is not None:
        payload['ipv4_mask'] = ipv4_mask
    if ipv4_gateway is not None:
        payload['ipv4_gateway'] = ipv4_gateway
    if mgmt_ipv6 is not None:
        payload['mgmt_ipv6'] = mgmt_ipv6
    if ipv6_mask is not None:
        payload['ipv6_mask'] = ipv6_mask
    if ipv6_gateway is not None:
        payload['ipv6_gateway'] = ipv6_gateway
    if home_port_raw_id is not None:
        payload['home_port_raw_id'] = home_port_raw_id
    if home_port_type is not None:
        payload['home_port_type'] = home_port_type
    if operational_status is not None:
        payload['operational_status'] = operational_status
    if failover_group_raw_id is not None:
        payload['failover_group_raw_id'] = failover_group_raw_id
    if dns_zone_name is not None:
        payload['dns_zone_name'] = dns_zone_name
    if listen_dns_query_enabled is not None:
        payload['listen_dns_query_enabled'] = listen_dns_query_enabled
    if can_failover is not None:
        payload['can_failover'] = can_failover
    if failback_mode is not None:
        payload['failback_mode'] = failback_mode

    response = client.put(url, body=payload, params={"logic_port_id": logic_port_id})
    return response


def logic_port_delete(client: DMEAPIClient, ids: list) -> dict:
    """
    Delete logic port (OceanStor A800 only) 

    Args:
        client: DME API client
        ids: Logic port ID  list (Required, 1-1000 IDs) 

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/storagemgmt/v1/logic-ports/delete"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def logic_port_failback(client: DMEAPIClient, id: str) -> dict:
    """
    Failback logic port (OceanStor A800 only) 

    Args:
        client: DME API client
        id: Logic port ID (Required, 1~64  characters) 

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/storagemgmt/v1/logic-ports/failback"

    payload = {
        'id': id
    }

    response = client.post(url, body=payload)
    return response


# ============ Storage port (port) subtopic functions ============


def port_list(client: DMEAPIClient, storage_id: str = None, port_type: str = None,
              location: str = None, ipv4: str = None, ipv6: str = None,
              port_name: str = None, zone_id: str = None,
              page_no: int = 1, page_size: int = 20) -> dict:
    """
     Query storage device port info,  supports ETH, FC, IB, Bond, SAS types

    Args:
        client: DME API client
        storage_id: Storage device ID(Optional, 1~36  characters) 
        port_type: Port type(Optional, eth/fc/ib/bond/sas, returns all types if not specified) 
        location: location(Optional, ETH port only, 1~255  characters) 
        ipv4: IPv4  address(Optional, ETH port only, 1~255  characters) 
        ipv6: IPv6  address(Optional, ETH port only, 1~255  characters) 
        port_name: Port name(Optional, ETH port only, 1~255  characters) 
        zone_id: Storage device zone ID(Optional, Bond port only, 1~36  characters) 
        page_no: Page number(Optional, FC/SAS port support, 1~10000, default 1) 
        page_size: per pagecount(Optional, FC/SAS port support, 1~1000, default 20) 

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes port list
    """
    if port_type is not None and port_type.lower() == 'eth':
        # ETH port query
        url = "/rest/storagemgmt/v1/storages/eth-ports/query"
        payload = {}
        if storage_id is not None:
            payload['storage_id'] = storage_id
        if location is not None:
            payload['location'] = location
        if ipv4 is not None:
            payload['ipv4'] = ipv4
        if ipv6 is not None:
            payload['ipv6'] = ipv6
        if port_name is not None:
            payload['port_name'] = port_name
        response = client.post(url, body=payload)
        return response
    elif port_type is not None and port_type.lower() == 'bond':
        # Bond port query
        url = "/rest/storagemgmt/v1/bond-ports/query"
        payload = {'storage_id': storage_id}
        if zone_id is not None:
            payload['zone_id'] = zone_id
        response = client.post(url, body=payload)
        return response
    elif port_type is not None and port_type.lower() == 'fc':
        # FC port query
        url = "/rest/storagemgmt/v1/frontend-ports/fc-ports/query"
        payload = {
            'page_no': page_no,
            'page_size': page_size
        }
        if storage_id is not None:
            payload['storage_id'] = storage_id
        response = client.post(url, body=payload)
        return response
    elif port_type is not None and port_type.lower() == 'ib':
        # IB port query
        url = "/rest/storagemgmt/v1/storages/ib-ports/query"
        payload = {}
        if storage_id is not None:
            payload['storage_id'] = storage_id
        response = client.post(url, body=payload)
        return response
    elif port_type is not None and port_type.lower() == 'sas':
        # SAS port query
        url = "/rest/storagemgmt/v1/backend-ports/sas-ports/query"
        payload = {
            'page_no': page_no,
            'page_size': page_size
        }
        if storage_id is not None:
            payload['storage_id'] = storage_id
        response = client.post(url, body=payload)
        return response
    else:
        # Returns all port types (ETH + FC + IB + SAS) 
        all_eth_ports = []
        all_fc_ports = []
        all_ib_ports = []
        all_sas_ports = []
        total_count = 0

        #  query ETH  port
        eth_url = "/rest/storagemgmt/v1/storages/eth-ports/query"
        eth_payload = {}
        if storage_id is not None:
            eth_payload['storage_id'] = storage_id
        if location is not None:
            eth_payload['location'] = location
        if ipv4 is not None:
            eth_payload['ipv4'] = ipv4
        if ipv6 is not None:
            eth_payload['ipv6'] = ipv6
        if port_name is not None:
            eth_payload['port_name'] = port_name
        eth_response = client.post(eth_url, body=eth_payload)
        # ETH  port API Return structure: {'total': N, 'eth_ports': [...]}
        if 'eth_ports' in eth_response:
            all_eth_ports = eth_response.get('eth_ports', [])
            total_count += len(all_eth_ports)

        #  query FC  port
        fc_url = "/rest/storagemgmt/v1/frontend-ports/fc-ports/query"
        fc_payload = {
            'page_no': page_no,
            'page_size': page_size
        }
        if storage_id is not None:
            fc_payload['storage_id'] = storage_id
        fc_response = client.post(fc_url, body=fc_payload)
        # FC  port API Return structure: {'total': N, 'ports': [...]}
        if 'ports' in fc_response:
            all_fc_ports = fc_response.get('ports', [])
            total_count += len(all_fc_ports)

        #  query IB  port
        ib_url = "/rest/storagemgmt/v1/storages/ib-ports/query"
        ib_payload = {}
        if storage_id is not None:
            ib_payload['storage_id'] = storage_id
        ib_response = client.post(ib_url, body=ib_payload)
        # IB  port API Return structure: {'ib_ports': [...]}
        if 'ib_ports' in ib_response:
            all_ib_ports = ib_response.get('ib_ports', [])
            total_count += len(all_ib_ports)

        #  query SAS  port
        sas_url = "/rest/storagemgmt/v1/backend-ports/sas-ports/query"
        sas_payload = {
            'page_no': page_no,
            'page_size': page_size
        }
        if storage_id is not None:
            sas_payload['storage_id'] = storage_id
        sas_response = client.post(sas_url, body=sas_payload)
        # SAS  port API Return structure: {'total': N, 'ports': [...]}
        if 'ports' in sas_response:
            all_sas_ports = sas_response.get('ports', [])
            total_count += len(all_sas_ports)

        return {
            'total': total_count,
            'eth_ports': all_eth_ports,
            'fc_ports': all_fc_ports,
            'ib_ports': all_ib_ports,
            'sas_ports': all_sas_ports
        }


def port_show_bond_members(client: DMEAPIClient, bond_port_id: str) -> dict:
    """
    QueryBound port member list info

    Args:
        client: DME API client
        bond_port_id:  bind port id (Required, 1~64  characters) 

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes total and eth_ports  field
    """
    url = "/rest/storagemgmt/v1/bond-ports/{bond_port_id}/eth-ports"

    response = client.get(url, params={"bond_port_id": bond_port_id})
    return response


# ============  storagePort group (port_group) subtopic functions ============


# ============  storage VLAN subtopic functions ============


def vlan_list(client: DMEAPIClient, name: str = None, storage_id: str = None,
              page_no: int = 1, page_size: int = 100) -> dict:
    """
    Batch query VLAN  list

    Args:
        client: DME API client
        name: VLAN  name (supports fuzzy search) 
        storage_id: Storage device ID
        page_no: Page queryStart page, default 1
        page_size: per pagecount, 1~1000, default 100

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes  VLAN  list
    """
    url = "/rest/vlanmgmt/v1/vlans/query"

    body_params = {
        'page_no': page_no,
        'page_size': page_size
    }

    if name is not None:
        body_params['name'] = name
    if storage_id is not None:
        body_params['storage_id'] = storage_id

    response = client.post(url, body=body_params)
    return response


def vlan_create(client: DMEAPIClient, name: str, vlan_id: int,
                storage_id: str, description: str = None) -> dict:
    """
    create  VLAN

     note: only supports OceanStor A800, A600 series storage. 

    Args:
        client: DME API client
        name: VLAN  name (Required) 
        vlan_id: VLAN ID (Required, 1~4094) 
        storage_id: Storage device ID (Required) 
        description: VLAN  description(Optional) 

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes newly created VLAN ID
    """
    url = "/rest/vlanmgmt/v1/vlans"

    body_params = {
        'name': name,
        'vlan_id': vlan_id,
        'storage_id': storage_id
    }

    if description is not None:
        body_params['description'] = description

    response = client.post(url, data=body_params)
    return response


def vlan_delete(client: DMEAPIClient, vlan_id: str) -> dict:
    """
    delete  VLAN

     note: only supports OceanStor A800, A600 series storage. 

    Args:
        client: DME API client
        vlan_id: VLAN ID

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/vlanmgmt/v1/vlans/{vlan_id}"

    response = client.delete(url, params={"vlan_id": vlan_id})
    return response


def vlan_modify(client: DMEAPIClient, vlan_id: str, name: str = None,
                description: str = None) -> dict:
    """
    modify  VLAN

     note: only supports OceanStor A800, A600 series storage. 

    Args:
        client: DME API client
        vlan_id: VLAN ID
        name: VLAN  name(Optional) 
        description: VLAN  description(Optional) 

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/vlanmgmt/v1/vlans/{vlan_id}"

    body_params = {}
    if name is not None:
        body_params['name'] = name
    if description is not None:
        body_params['description'] = description

    response = client.put(url, params={"vlan_id": vlan_id})
    return response


# ============  storageFailover group busi failover group (failover_group) subtopic functions ============


def failover_group_list(client: DMEAPIClient, storage_id: str,
                        failover_group_type: str = None,
                        zone_id: str = None,
                        failover group service type: list = None) -> dict:
    """
     query failover group busi failover group list

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, 1~36 characters, must satisfy regex ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$) 
        failover_group_type: Failover group busi failover group type(Optional). Options: system, VLAN, customized
        zone_id: Zone ID(Optional, 1~255 characters) , OceanStor A800 series only
        failover group service type: Failover group business type list(Optional, List<string>, max array members: 10). Options: NAS, BGP (used toassociate VIP typeLogic port failover group), RDMA (used to associateNFS over RDMA, NFS, OBJECT protocolLogic port failover group), IB (used to associate NAS over IBProtocol typeLogic port failover group), KB (used to associate KnowledgeBase over TCPProtocol typeLogic port failover group)

    Returns:
        {
            total: Failover group busi failover groupcount (int32),
            failover_groups: Failover group busi failover group list (List<Failover group business typeloverGroupResp>). 参数格式如下：[{
                id: Failover group busi failover groupid (1~64 characters),
                name: Failover group busi failover group name (1~64 characters),
                failover_group_type: Failover group busi failover group type (1~255 characters). Options: system, VLAN, customized,
                raw_id: Failover group ID on storage device (1~255 characters),
                zone_name: Zone name (1~255 characters), OceanStor A800 series only,
                zone_raw_id: Zone ID assigned on storage device (1~255 characters), OceanStor A800 series only,
                zone_id: Storage device zone ID (1~255 characters), OceanStor A800 series only,
                failover group service type: Failover group business type. Options: NAS, BGP (used toassociate VIP typeLogic port failover group), RDMA (used to associateNFS over RDMA, NFS, OBJECT protocolLogic port failover group), IB (used to associate NAS over IBProtocol typeLogic port failover group), KB (used to associate KnowledgeBase over TCPProtocol typeLogic port failover group),
            }, ...]
        }
    """
    url = "/rest/storagemgmt/v1/failover-groups/query"

    payload = {
        'storage_id': storage_id
    }

    if failover_group_type is not None:
        payload['failover_group_type'] = failover_group_type
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if failover group service type is not None:
        payload['failover group service type'] = failover group service type

    response = client.post(url, body=payload)
    return response


def failover_group_show_ports(client: DMEAPIClient, failover_group_id: str,
                               port_type: str = None) -> dict:
    """
     Query failover group under port ( supports bond, eth, ib types) 

    Args:
        client: DME API client
        failover_group_id: Failover group busi failover group id (Required, 1~64  characters) 
        port_type: Port type(Optional, bond/eth/ib, returns all types if not specified) 

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        },  consistent structure: {"total": x, "bond_ports": [], "eth_ports": [], "ib_ports": []}
    """
    import concurrent.futures

    def query_port_type(ptype: str):
        if ptype == 'bond':
            url = "/rest/storagemgmt/v1/failover-groups/{failover_group_id}/bond-ports"
        elif ptype == 'eth':
            url = "/rest/storagemgmt/v1/failover-groups/{failover_group_id}/eth-ports"
        elif ptype == 'ib':
            url = "/rest/storagemgmt/v1/failover-groups/{failover_group_id}/ib-ports"
        else:
            return (ptype, {'error': f'Invalid port_type: {ptype}'})
        resp = client.get(url, params={"failover_group_id": failover_group_id})
        return (ptype, resp)

    if port_type is None:
        # type not specified, Returns all three port types,  flat structure
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(query_port_type, 'bond'),
                      executor.submit(query_port_type, 'eth'),
                      executor.submit(query_port_type, 'ib')]
            result = {'total': 0, 'bond_ports': [], 'eth_ports': [], 'ib_ports': []}
            for future in concurrent.futures.as_completed(futures):
                ptype, resp = future.result()
                if isinstance(resp, dict) and 'bond_ports' in resp:
                    result[f'{ptype}_ports'] = resp.get('bond_ports', [])
                    result['total'] += resp.get('total', 0)
                elif isinstance(resp, dict) and 'eth_ports' in resp:
                    result[f'{ptype}_ports'] = resp.get('eth_ports', [])
                    result['total'] += resp.get('total', 0)
                elif isinstance(resp, dict) and 'ib_ports' in resp:
                    result[f'{ptype}_ports'] = resp.get('ib_ports', [])
                    result['total'] += resp.get('total', 0)
        return result
    elif port_type in ('bond', 'eth', 'ib'):
        _, resp = query_port_type(port_type)
        return resp
    else:
        return {'error': f'Invalid port_type: {port_type}, must be one of: bond, eth, ib'}


def failover_group_show_vlans(client: DMEAPIClient, failover_group_id: str) -> dict:
    """
     query failover group busi failover group under VLAN

    Args:
        client: DME API client
        failover_group_id: Failover group busi failover group id (Required, 1~64  characters) 

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes  vlans  field
    """
    url = "/rest/storagemgmt/v1/failover-groups/{failover_group_id}/vlans"

    response = client.get(url, params={"failover_group_id": failover_group_id})
    return response


# ============ Zone (OceanStor A800  cluster zone) subtopic functions ============


def zone_list(client: DMEAPIClient, name: str = None, ip: str = None,
              status: list = None, sync_status: list = None,
              sn: str = None, storage_ids: list = None) -> dict:
    """
     Query zone info in OceanStor A800 cluster

    Args:
        client: DME API client
        name: zoneName (Optional,1~256 characters) , exact match
        ip: zone ip addressName (Optional,1~256 characters) , exact match
        status: Zone status list(Optional, List<string>, max array members: 6). Options: OFFLINE, NORMAL, FAULT, DEGRADED, ABNORMAL, UNKNOWN
        sync_status: Zone sync status list(Optional, List<string>, max array members: 5). Options: UNSYNC, SYNC, NORMAL, FAILED (Sync failure), UNKNOWN
        sn: ZoneSerial number(Optional, 1~128 characters) , exact match
        storage_ids: OceanStor A800 clusterid list(Optional, List<string>, max array members: 100,  min membercount: 1) , exact match

    Returns:
        {
            total: ZoneTotal count (int32),
            datas: Zone list (List<OceanStorA800ZoneInfo>). 参数格式如下：[{
                id: Zone CMDB ID (1~64 characters),
                native_id: native id (1~64 characters),
                name: Zone name (1~128 characters),
                ip: Zone IP address (1~32 characters),
                status:  status (1~32 characters). Options: OFFLINE, NORMAL, FAULT, DEGRADED, ABNORMAL,
                sync_status: Sync status (1~32 characters). Options: UNSYNC, SYNC, NORMAL, FAILED (Sync failure),
                sn: ZoneDevice serial number (1~64 characters),
                wwn: Zone device WWN (1~32 characters),
                vendor: Zone vendor (1~32 characters),
                model: ZoneProduct model (1~64 characters),
                owning_ne_type: Storage device NE type. Options: dorado, OceanStor A800,
                location: Zonelocation info (0~512 characters),
                version: Version info (0~64 characters),
                patch_version: Patch version info (0~64 characters),
                add_time: Device access time (0~32 characters), UTCTimestamp ( precise to ms seconds) ,
                last_sync_time:  lastSync time (0~32 characters), UTCTimestamp ( precise to ms seconds) ,
                sync_process: Sync progress (int32),
                alarm_num: alarmcount (number),
                parent_id:  clusterid,
                zone_raw_id: zone raw id,
                is_core_zone: Whether it is the core controller nodezone (boolean). Options: true, false,
            }, ...]
        }
    """
    url = "/rest/storageclusterservice/v1/zones/query"

    payload = {}

    param_map = {
        'name': name,
        'ip': ip,
        'status': status,
        'sync_status': sync_status,
        'sn': sn,
        'storage_ids': storage_ids,
    }

    for key, value in param_map.items():
        if value is not None:
            payload[key] = value

    response = client.post(url, body=payload)
    return response


# Action list for CLI help
#  format: action_key: {func, description, params, subtopic}
# subtopic Indicates which subtopic the action belongs to, None = direct action

ACTIONS = {
    # Direct action (Two-level structure: <topic> <action>) 
    'list': {
        'func': list,
        'description': 'Batch query storage devices',
        'params': ['az', 'source', 'dc_id', 'tag_ids', 'start', 'limit', 'ext_attrs'],
        'subtopic': None
    },
    'show': {
        'func': show,
        'description': 'Query storage device',
        'params': ['storage_id'],
        'subtopic': None
    },
    'add': {
        'func': add,
        'description': 'Add storage device (offline info entry only) ',
        'params': ['name', 'sn', 'ip', 'vendor', 'model', 'version', 'patch_version', 'dc_id', 'az', 'location', 'maintenanceetenance_start', 'maintenanceetenance_overtime', 'total_capacity', 'total_effective_capacity', 'total_pool_capacity', 'used_capacity', 'free_capacity', 'subscription_capacity', 'tag_ids'],
        'subtopic': None
    },
    'remove': {
        'func': remove,
        'description': 'batchRemove storage device',
        'params': ['storage_ids'],
        'subtopic': None
    },
    'sync': {
        'func': sync,
        'description': 'SyncStorage device info',
        'params': ['storage_id'],
        'subtopic': None
    },
    'modify': {
        'func': modify,
        'description': 'Modify storage device (only supportsModify recorded offlineStorage device info) ',
        'params': ['storage_id', 'name', 'location', 'ext_attrs'],
        'subtopic': None
    },
    # subtopic actions (Three-level structure: <topic> <subtopic> <action>) 
    'bbu_list': {
        'func': bbu_list,
        'description': 'query storage device BBU info list',
        'params': ['storage_id', 'health_status', 'running_status', 'enclosure_name',
                   'location', 'zone_id', 'page_no', 'page_size'],
        'subtopic': 'bbu'
    },
    'get_passphrase': {
        'func': get_passphrase,
        'description': 'getStorage device access token',
        'params': ['storage_id'],
    },
    'fan_list': {
        'func': fan_list,
        'description': 'query storage deviceFan info',
        'params': ['storage_id', 'health_status', 'running_status', 'run_level',
                   'enclosure_name', 'location', 'zone_id', 'page_no', 'page_size'],
        'subtopic': 'fan'
    },
    'disk_list': {
        'func': disk_list,
        'description': 'query storage deviceDisk info list',
        'params': ['storage_id'],
        'subtopic': 'disk'
    },
    'pool_list': {
        'func': pool_list,
        'description': ' query storage deviceStorage pool list',
        'params': ['storage_id', 'raw_id', 'zone_id', 'page_no', 'page_size', 'sort_key', 'sort_dir'],
        'subtopic': 'pool'
    },
    'hyperscale_pool_list': {
        'func': hyperscale_pool_list,
        'description': ' query HyperScale Storage pool list',
        'params': ['raw_id', 'name', 'local_pool_id', 'health_status', 'running_status', 'storage_id', 'description', 'page_no', 'page_size', 'sort_key', 'sort_dir'],
        'subtopic': 'hyperscale_pool'
    },
    'node_list': {
        'func': node_list,
        'description': 'query storage deviceNode list',
        'params': ['storage_id', 'raw_id', 'storage_name', 'name', 'ids',
                   'mgmt_ip', 'frame_number', 'slot_number', 'status', 'roles',
                   'page_no', 'page_size', 'sort_key', 'sort_dir'],
        'subtopic': 'node'
    },
    'psu_list': {
        'func': psu_list,
        'description': 'getStorage devicePower supply (PSU)  list',
        'params': ['storage_id', 'health_status', 'running_status', 'power_type',
                   'power_mode', 'location', 'model', 'sn', 'enclosure_name',
                   'zone_id', 'page_no', 'page_size'],
        'subtopic': 'psu'
    },
    'query_power_data': {
        'func': query_power_data,
        'description': ' Query storage device power data',
        'params': ['start_time', 'end_time', 'storage_ids', 'time_granularity'],
    },
    'app_type_list': {
        'func': app_type_list,
        'description': 'Query storage device application type',
        'params': ['storage_id'],
        'subtopic': 'app_type'
    },
    'controller_list': {
        'func': controller_list,
        'description': 'Query storage devicecontroller info',
        'params': ['storage_id'],
        'subtopic': 'controller'
    },
    'disk_domaintenancee_list': {
        'func': disk_domaintenancee_list,
        'description': 'Batch query disk pools',
        'params': ['storage_id', 'page_no', 'page_size'],
        'subtopic': 'disk_domaintenancee'
    },
    'disk_pool_list': {
        'func': disk_pool_list,
        'description': 'Batch query distributed storage device disk pools',
        'params': ['storage_id', 'page_no', 'page_size'],
        'subtopic': 'disk_pool'
    },
    'enclosure_list': {
        'func': enclosure_list,
        'description': 'Batch query enclosures info',
        'params': ['page_no', 'page_size', 'storage_id', 'name', 'location',
                   'health_status', 'zone_name', 'zone_id', 'running_status',
                   'power_mode', 'esn', 'mac', 'sort_key', 'sort_dir'],
        'subtopic': 'enclosure'
    },
    'vstore_list': {
        'func': vstore_list,
        'description': 'Batch query storage device tenant info',
        'params': ['storage_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'vstore'
    },
    'vstore_show': {
        'func': vstore_show,
        'description': 'Query tenant details',
        'params': ['vstore_id'],
        'subtopic': 'vstore'
    },
    'vstore_create': {
        'func': vstore_create,
        'description': 'Create tenant',
        'params': ['name', 'storage_id', 'san_capacity_quota', 'nas_capacity_quota', 'description', 'nas_capacity_quota_alarm_switch', 'nas_capacity_quota_alarm_threshold', 'associate_pool_ids'],
        'subtopic': 'vstore'
    },
    'vstore_modify': {
        'func': vstore_modify,
        'description': 'Modify tenant',
        'params': ['vstore_id', 'name', 'san_capacity_quota', 'nas_capacity_quota', 'description', 'nas_capacity_quota_alarm_switch', 'nas_capacity_quota_alarm_threshold'],
        'subtopic': 'vstore'
    },
    'vstore_delete': {
        'func': vstore_delete,
        'description': 'Batch delete tenant',
        'params': ['vstore_ids'],
        'subtopic': 'vstore'
    },
    'initiator_list': {
        'func': initiator_list,
        'description': 'Batch query storage initiator objects',
        'params': ['page_size', 'page_no', 'raw_id', 'alias', 'status',
                   'associated_host_name', 'associated_host_id', 'multipath_type',
                   'protocol', 'support_provisioning', 'vstore_raw_id',
                   'vstore_name', 'storage_id'],
        'subtopic': 'initiator'
    },
    'initiator_delete': {
        'func': initiator_delete,
        'description': 'Batch delete storage device initiator objects',
        'params': ['initiator_ids', 'task_remarks'],
        'subtopic': 'initiator'
    },
    'initiator_modify': {
        'func': initiator_modify,
        'description': 'modify  storage initiatorobject',
        'params': ['initiator_id', 'vstore_id', 'alias', 'multi_path'],
        'subtopic': 'initiator'
    },
    # account subtopic actions (auth user) 
    'account_show_local_users': {
        'func': account_show_local_users,
        'description': 'Query storage devicelocal Auth user info',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_create_local_user': {
        'func': account_create_local_user,
        'description': 'Create local auth user',
        'params': ['storage_id', 'name', 'password', 'primary_group_raw_id', 'description', 'group_names', 'vstore_id'],
        'subtopic': 'account'
    },
    'account_create_unix_user': {
        'func': account_create_unix_user,
        'description': 'Create storage device UNIX auth user',
        'params': ['storage_id', 'name', 'primary_group_raw_id', 'raw_id', 'description', 'password', 'status_enabled', 'vstore_raw_id'],
        'subtopic': 'account'
    },
    'account_create_windows_user': {
        'func': account_create_windows_user,
        'description': 'Create storage device Windows auth user',
        'params': ['storage_id', 'name', 'password', 'raw_id', 'description', 'status_enabled', 'vstore_raw_id'],
        'subtopic': 'account'
    },
    'account_show_unix_users': {
        'func': account_show_unix_users,
        'description': 'Query storage device UNIX Auth user info',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_show_windows_users': {
        'func': account_show_windows_users,
        'description': 'Query storage device Windows Auth user info',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_show_local_user_groups': {
        'func': account_show_local_user_groups,
        'description': 'Query storage devicelocal Auth user group info',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_show_unix_user_groups': {
        'func': account_show_unix_user_groups,
        'description': 'Query storage device UNIX Auth user group info',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_show_windows_user_groups': {
        'func': account_show_windows_user_groups,
        'description': 'Query storage device Windows Auth user group info',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    # qos subtopic actions
    'qos_list': {
        'func': qos_list,
        'description': 'Batch query QoS  policy',
        'params': ['storage_id', 'name', 'raw_id', 'enable_status', 'running_status',
                   'zone_id', 'resource_type_list', 'vstore_id', 'vstore_name',
                   'alarm_status', 'io_policy_type', 'page_no', 'page_size',
                   'sort_key', 'sort_dir'],
        'subtopic': 'qos'
    },
    'qos_show': {
        'func': qos_show,
        'description': 'Query QoS  policy details',
        'params': ['qos_policy_id'],
        'subtopic': 'qos'
    },
    'qos_create': {
        'func': qos_create,
        'description': 'create  QoS  policy',
        'params': ['name', 'storage_id', 'resource_type', 'resource_ids', 'description', 'zone_id', 'vstore_id', 'enable_status', 'io_policy_type',
                   'min_bandwidth', 'max_bandwidth', 'burst_bandwidth', 'min_iops',
                   'max_iops', 'burst_iops', 'burst_time', 'latency',
                   'max_read_bandwidth', 'max_write_bandwidth',
                   'burst_read_bandwidth', 'burst_write_bandwidth',
                   'max_read_iops', 'max_write_iops', 'burst_read_iops',
                   'burst_write_iops', 'alarm_switch', 'alarm_level',
                   'alarm_threshold', 'resume_threshold', 'schedule_policy',
                   'schedule_start_date', 'start_time', 'duration', 'weekly_days'],
        'subtopic': 'qos'
    },
    'qos_modify': {
        'func': qos_modify,
        'description': 'modify  QoS  policy',
        'params': ['qos_policy_id', 'name', 'description', 'io_policy_type',
                   'min_bandwidth', 'max_bandwidth', 'burst_bandwidth', 'min_iops',
                   'max_iops', 'burst_iops', 'burst_time', 'latency',
                   'max_read_bandwidth', 'max_write_bandwidth',
                   'burst_read_bandwidth', 'burst_write_bandwidth',
                   'max_read_iops', 'max_write_iops', 'burst_read_iops',
                   'burst_write_iops', 'alarm_switch', 'alarm_level',
                   'alarm_threshold', 'resume_threshold'],
        'subtopic': 'qos'
    },
    'qos_delete': {
        'func': qos_delete,
        'description': 'delete  QoS  policy',
        'params': ['qos_policy_ids'],
        'subtopic': 'qos'
    },
    'qos_activate': {
        'func': qos_activate,
        'description': 'batch activate QoS  policy',
        'params': ['qos_policy_ids'],
        'subtopic': 'qos'
    },
    'qos_deactivate': {
        'func': qos_deactivate,
        'description': 'Batch deactivate QoS  policy',
        'params': ['qos_policy_ids'],
        'subtopic': 'qos'
    },
    'qos_associate': {
        'func': qos_associate,
        'description': 'QoS Associate policy with control resource',
        'params': ['qos_policy_id', 'resource_ids', 'resource_type'],
        'subtopic': 'qos'
    },
    'qos_unassociate': {
        'func': qos_unassociate,
        'description': 'QoS Disassociate policy from control resource',
        'params': ['qos_policy_id', 'resource_ids', 'resource_type'],
        'subtopic': 'qos'
    },
    # logic_port subtopic actions ( storageLogic port) 
    'logic_port_list': {
        'func': logic_port_list,
        'description': 'query storage deviceLogic port list',
        'params': ['storage_id', 'vstore_raw_id', 'zone_raw_id', 'scope', 'page_no', 'page_size'],
        'subtopic': 'logic_port'
    },
    'logic_port_show': {
        'func': logic_port_show,
        'description': 'query storage deviceLogic port details',
        'params': ['logic_port_id'],
        'subtopic': 'logic_port'
    },
    'logic_port_create': {
        'func': logic_port_create,
        'description': 'Create logic port (OceanStor A800 only) ',
        'params': ['storage_id', 'name', 'address_family', 'home_port_type', 'zone_raw_id', 'scope',
                   'mgmt_ip', 'ipv4_mask', 'ipv4_gateway', 'mgmt_ipv6', 'ipv6_mask', 'ipv6_gateway',
                   'home_port_raw_id', 'support_protocol', 'operational_status', 'home_controller_id',
                   'failover_group_raw_id', 'vstore_raw_id', 'role', 'dns_zone_name',
                   'listen_dns_query_enabled', 'can_failover', 'failback_mode'],
        'subtopic': 'logic_port'
    },
    'logic_port_update': {
        'func': logic_port_update,
        'description': 'Modify logic port (OceanStor A800 only) ',
        'params': ['logic_port_id', 'name', 'address_family', 'mgmt_ip', 'ipv4_mask', 'ipv4_gateway',
                   'mgmt_ipv6', 'ipv6_mask', 'ipv6_gateway', 'home_port_raw_id', 'home_port_type',
                   'operational_status', 'failover_group_raw_id', 'dns_zone_name',
                   'listen_dns_query_enabled', 'can_failover', 'failback_mode'],
        'subtopic': 'logic_port'
    },
    'logic_port_delete': {
        'func': logic_port_delete,
        'description': 'Delete logic port (OceanStor A800 only) ',
        'params': ['ids'],
        'subtopic': 'logic_port'
    },
    'logic_port_failback': {
        'func': logic_port_failback,
        'description': 'Failback logic port (OceanStor A800 only) ',
        'params': ['id'],
        'subtopic': 'logic_port'
    },
    # port subtopic actions (Storage port) 
    'port_list': {
        'func': port_list,
        'description': ' Query storage device port info,  support ETH, FC, IB, Bond four types type',
        'params': ['storage_id', 'port_type', 'location', 'ipv4', 'ipv6', 'port_name', 'zone_id', 'page_no', 'page_size'],
        'subtopic': 'port'
    },
    'port_show_bond_members': {
        'func': port_show_bond_members,
        'description': 'QueryBound port member list info',
        'params': ['bond_port_id'],
        'subtopic': 'port'
    },
    # vlan subtopic actions ( storage VLAN) 
    'vlan_list': {
        'func': vlan_list,
        'description': 'Batch query VLAN  list',
        'params': ['name', 'storage_id', 'page_no', 'page_size'],
        'subtopic': 'vlan'
    },
    'vlan_create': {
        'func': vlan_create,
        'description': 'create  VLAN (only supports OceanStor A800, A600 series storage) ',
        'params': ['name', 'vlan_id', 'storage_id', 'description'],
        'subtopic': 'vlan'
    },
    'vlan_delete': {
        'func': vlan_delete,
        'description': 'delete  VLAN (only supports OceanStor A800, A600 series storage) ',
        'params': ['vlan_id'],
        'subtopic': 'vlan'
    },
    'vlan_modify': {
        'func': vlan_modify,
        'description': 'modify  VLAN (only supports OceanStor A800, A600 series storage) ',
        'params': ['vlan_id', 'name', 'description'],
        'subtopic': 'vlan'
    },
    # failover_group subtopic actions ( storageFailover group busi failover group) 
    'failover_group_list': {
        'func': failover_group_list,
        'description': ' query failover group busi failover group list',
        'params': ['storage_id', 'failover_group_type', 'zone_id', 'failover group service type'],
        'subtopic': 'failover_group'
    },
    'failover_group_show_ports': {
        'func': failover_group_show_ports,
        'description': ' Query failover group under port ( supports bond, eth, ib types) ',
        'params': ['failover_group_id', 'port_type'],
        'subtopic': 'failover_group'
    },
    'failover_group_show_vlans': {
        'func': failover_group_show_vlans,
        'description': ' query failover group busi failover group under VLAN',
        'params': ['failover_group_id'],
        'subtopic': 'failover_group'
    },
    # zone subtopic actions (OceanStor A800  cluster zone) 
    'zone_list': {
        'func': zone_list,
        'description': ' Query zone info in OceanStor A800 cluster',
        'params': ['name', 'ip', 'status', 'sync_status', 'sn', 'storage_ids'],
        'subtopic': 'zone'
    },
}
