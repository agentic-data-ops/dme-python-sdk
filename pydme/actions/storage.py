"""
Storage device related operations
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
    Batch query Storage device tenant info.

    Args:
        client: DME API client
        raw_id: The ID of the tenant on the device (Optional, string, 1~256 characters)
        vstore_id: tenant ID (Optional, string, 1~64 characters)
        qos_id: QoS policy ID (Optional, string, 1~64 characters)
        is_associated_qos: Whether the tenant is associated with QoS (Optional, boolean, true,false)
        name: Tenant name, supports fuzzy query (Optional, string, 1~256 characters)
        storage_id: storage device ID (Optional, string, 1~255 characters)
        storage_ip: Storage device IP (Optional, string, 1~255 characters)
        storage_name: storage device name (Optional, string, 1~255 characters)
        zone_id: zone ID (Optional, string, 1~64 characters). Only supported by OceanStor A series storage.
        status: Tenant status (Optional, string). valid values: active, inactive
        nas_capacity_quota_alarm_switch: NAS capacity quota alarm switch (Optional, boolean, true,false). Only supported by OceanStor A series storage.
        sort_key: Sort field (Optional, string)
        sort_dir: Sort direction (Optional, string). valid values: asc, desc
        page_no: Start page for paginated query (Optional, int32, 1~10000000). default value: 1
        page_size: Number of items per page (Optional, int32, 1~1000). default value: 100

    Returns:
        {
            total: Total count of tenants (integer),
            vstores: List of tenants (List<VstoreResp>, max array members: 1000). parameter format: [{
                id: Unique identifier of the tenant (string, 1~64 characters),
                qos_id: QoS policy ID (string, 1~64 characters),
                raw_id: Tenant ID on the device (string, 1~64 characters),
                storage_sn: Storage device SN (string, 1~64 characters),
                storage_id: Device ID (string, 1~64 characters),
                storage_ip: Device IP (string, 1~255 characters),
                storage_name: Device name (string, 1~255 characters),
                name: Tenant name (string, 1~256 characters),
                description: Tenant description (string, 0~255 characters),
                running_status: running status (string). valid values: normal, initializing,
                status: Tenant status (string). valid values: active, inactive,
                encrypt_option: Encryption option of the tenant (boolean, true,false),
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
        id: Tenant id (Required, string, 1~256 characters). Must satisfy UUID format or 32-bit hexadecimal

    Returns:
        {
            id: Unique identifier of the tenant (string, 1~64 characters),
            name: Tenant name (string, 1~256 characters),
            description: Tenant description (string, 0~255 characters),
            storage_id: Device ID (string, 1~64 characters),
            status: Tenant status (string). valid values: active, inactive,
            running_status: running status (string). valid values: normal, initializing,
        }
    """
    url = "/rest/fileservice/v1/vstores/{id}"

    # Parameter validation
    if not id:
        raise ValueError("id is a required parameter")

    response = client.get(url, params={"id": id})
    return response


def vstore_create(client: DMEAPIClient, name: str, storage_id: str,
                  san_capacity_quota: str = None,
                  nas_capacity_quota: str = None, description: str = None,
                  nas_capacity_quota_alarm_switch: bool = None,
                  nas_capacity_quota_alarm_threshold: int = None,
                  associate_pool_ids: list = None) -> dict:
    """
    Create tenant. OceanStor Dorado v3 devices do not support this feature.

    Args:
        client: DME API client
        storage_id: storage device ID (Required, string, 1~36 characters). Must satisfy UUID format or 32-bit hexadecimal
        name: Tenant name (Required, string, 1~256 characters). Only contains letters, digits, "_", "-", "." and Chinese characters
        san_capacity_quota: SAN capacity quota (Optional, unit: sectors)
        nas_capacity_quota: NAS capacity quota (Optional, unit: sectors)
        description: Tenant description (Optional, 0~255 characters)
        nas_capacity_quota_alarm_switch: NAS capacity quota alarm switch (Optional, only supported by A800 devices)
        nas_capacity_quota_alarm_threshold: NAS capacity quota alarm threshold (Optional, only supported by A800 devices)
        associate_pool_ids: Associated Storage pool ID list (Optional, only supported by A series devices)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/fileservice/v1/vstores"

    if not storage_id:
        raise ValueError("storage_id is a required parameter")

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
    Modify the specified tenant. This operation will modify the specified tenant on the Storage device.

    Args:
        client: DME API client
        id: Tenant ID (Required, string, 1~64 characters). Must satisfy UUID format or 32-bit hexadecimal
        name: Tenant name (Optional, string, 1~256 characters). name contains letters, digits, "_", "-", "." and Chinese characters
        san_capacity_quota: SAN capacity quota (Optional, string, 1~20 characters)
        nas_capacity_quota: NAS capacity quota (Optional, string, 1~20 characters)
        description: Tenant description (Optional, string, 0~255 characters)
        nas_capacity_quota_alarm_switch: NAS capacity quota alarm switch (Optional, boolean, true,false). Only supported by A800 devices
        nas_capacity_quota_alarm_threshold: NAS capacity quota alarm threshold (Optional, int32, 50~100). Only supported by A800 devices

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/fileservice/v1/vstores/{id}"

    # Parameter validation
    if not id:
        raise ValueError("id is a required parameter")

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
    Batch delete tenants. This operation will delete the specified tenants on the Storage device.
    This API may directly or indirectly affect current network operations, cause service interruption,
    critical data loss, etc. Please proceed with caution.

    Args:
        client: DME API client
        ids: List of tenant IDs (Required, List[string], max array members: 100, min array members: 1)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/fileservice/v1/vstores/delete"

    # Parameter validation
    if not ids or len(ids) == 0:
        raise ValueError("ids is a required parameter, at least 1 tenant ID is needed")

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response



def list(client: DMEAPIClient, az: str = None, source: str = None,
         dc_id: str = None, tag_ids: str = None, start: int = 1, 
         limit: int = 20, ext_attrs: str = None) -> dict:
    """
    Batch query Storage devices: supports paginated query and filtering.

    Args:
        client: DME API client.
        az: Availability zone ID (Optional, string, 1~64 characters)
        source: Source of the Storage device (Optional, string). valid values: add, record, all. default queries connected devices
        dc_id: ID of the data center the Storage device belongs to (Optional, string, 1~32 characters)
        tag_ids: Tag filter list (Optional, string). Supports up to 10 tag IDs combined for filtering, multiple filter conditions are AND relations
        start: Start page for paginated query (Optional, int32, 1~10000). default value: 1
        limit: Number of items per page (Optional, int32, 1~1000). default value: 20
        ext_attrs: Extended attribute filter list (Optional, string, 1~3000 characters). Supports up to 10 extended attributes combined for filtering

    Returns:
        {
            total: Storage device total (int32),
            datas: Storage device list (List<StorageSummaryInfo>). parameter format: [{
                id: storage device ID (string),
                name: storage device name (string),
                ip: IP address (string),
                status: running status (string),
                sn: Device serial number (string),
                vendor: Vendor (string),
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
    Query the specified Storage device.

    Args:
        client: DME API client
        storage_id: storage device ID, Required (Required, string, 1~36 characters). Must satisfy UUID format or 32-bit hexadecimal

    Returns:
        {
            id: storage device ID (string),
            name: storage device name (string),
            ip: IP address (string),
            status: running status (string),
            sn: Device serial number (string),
            vendor: Vendor (string),
            model: Product model (string),
        }
    """
    url = "/rest/storagemgmt/v1/storages/{storage_id}/detail"

    if not storage_id:
        raise ValueError("storage_id is a required parameter")

    response = client.get(url, params={"storage_id": storage_id})
    return response


def add(client: DMEAPIClient, name: str = None, sn: str = None, ip: str = None,
        vendor: str = None, model: str = None, version: str = None,
        patch_version: str = None, dc_id: str = None, az: str = None,
        location: str = None, maintenance_start: int = None,
        maintenance_overtime: int = None, total_capacity: float = None,
        total_effective_capacity: float = None, total_pool_capacity: float = None,
        used_capacity: float = None, free_capacity: float = None,
        subscription_capacity: float = None, tag_ids: list = None) -> dict:
    """
    Add a Storage device (only supports recording offline Storage device info)

    Add Storage device info to the DME system in an offline manner.

    Args:
        client: DME API client.
        name: Device name (1~256 characters). Can only contain half-width letters, half-width digits, \"_\", \"-\", \".\", and Chinese characters.
        sn: Device serial number (regex pattern ^[a-zA-Z0-9]{1,128}$).
        ip: Device IP address (Optional, 0~128 characters, supports IPv4 and IPv6 formats, can also be an empty string).
        dc_id: Data center ID (Optional, regex pattern ^[a-zA-Z0-9]{1,128}$).
        az: Availability zone (Optional, string).
        vendor: Vendor (Optional, 0~128 characters).
        model: Product model (Optional, 0~128 characters).
        version: Version info (Optional, 0~64 characters).
        patch_version: Patch version info (Optional, 0~64 characters).
        location: Device location (Optional, 0~512 characters).
        maintenance_start: Maintenance start time (Optional, format is millisecond timestamp). Must appear together with maintenance overtime and the value must be less than maintenance overtime.
        maintenance_overtime: Maintenance overtime (Optional, format is millisecond timestamp). Must appear together with maintenance start time and the value must be greater than maintenance start time.
        total_capacity: Raw capacity (Optional, 0~2147483647, unit MB).
        total_effective_capacity: Effective capacity (Optional, 0~2147483647, unit MB).
        total_pool_capacity: Available capacity (Optional, 0~2147483647, unit MB).
        used_capacity: Used capacity (Optional, 0~2147483647, unit MB).
        free_capacity: Free capacity (Optional, 0~2147483647, unit MB).
        subscription_capacity: Subscribed capacity (Optional, 0~2147483647, unit MB).
        tag_ids: Tag ID list (Optional, List<string>, max array members: 10, min array members: 0).
    
    Returns:
        {
            id: storage device ID (string, 1~64 characters),
        }
    """
    if not name:
        raise ValueError("name is a required parameter")
    if not sn:
        raise ValueError("sn is a required parameter")

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
    if maintenance_start is not None:
        payload['maintenance_start'] = maintenance_start
    if maintenance_overtime is not None:
        payload['maintenance_overtime'] = maintenance_overtime
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
    Batch remove Storage devices.

    Args:
        client: DME API client
        ids: List of storage device IDs (Required, List[string], max array members: 100, min array members: 1)

    Returns:
        {
            task_id: Task Id (string, 1~64 characters),
        }
    """
    url = "/rest/storagemgmt/v2/storages/delete"

    if not ids or len(ids) == 0:
        raise ValueError("ids is a required parameter, at least 1 storage device ID is needed")

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def sync(client: DMEAPIClient, storage_id: str) -> dict:
    """
    Sync Storage device info. This interface is an asynchronous message.

    Args:
        client: DME API client
        storage_id: Storage device Id (Required, string, 1~64 characters). Obtained via the batch query Storage device interface

    Returns:
        None
    """
    url = "/rest/storagemgmt/v1/storages/refresh"

    if not storage_id:
        raise ValueError("storage_id is a required parameter")

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
    Query the BBU info list of a Storage device

    Args:
        client: DME API client.
        storage_id: The id of the BBU storage device (Optional, 1~64 characters).
        health_status: health status (Optional). valid values: unknown, normal, faulty, about_to_fail, low_battery.
        running_status: running status (Optional). valid values: unknown, normal, running, online, offline, charging, charging_completed, discharging.
        enclosure_name: Name of the enclosure it belongs to (Optional, 1~256 characters). supports fuzzy match.
        location: location (Optional, 1~256 characters). supports fuzzy match.
        zone_id: Zone ID (Optional, 1~255 characters). Only supported by OceanStor A800 series storage.
        page_no: Page number for paginated query (Optional, 1~2147483647, default value: 1).
        page_size: Page size for paginated query (Optional, 1~1000, default value: 20).
    
    Returns:
        {
            backup_powers: BBU list (List<StorageBackupPowerInfo>). parameter format: [{
                name: name (1~255 characters),
                location: location (1~255 characters),
                health_status: health status. valid values: unknown, normal, faulty, about_to_fail, low_battery,
                running_status: running status. valid values: unknown, normal, running, online, offline, charging, charging_completed, discharging,
                charge_times: Number of discharge cycles (int64),
                firmware_version: Firmware version number (1~255 characters),
                manufactured_date: Manufacture date (1~255 characters),
                enclosure_id: ID of the enclosure on the Storage device (1~255 characters),
                enclosure_name: Name of the enclosure (1~255 characters),
                zone_id: Zone ID (1~255 characters), only supported by OceanStor A800 series storage,
                zone_ip: Zone IP address (1~255 characters), only supported by OceanStor A800 series storage,
                zone_name: Zone name (1~255 characters), only supported by OceanStor A800 series storage,
            }, ...],
            total: Count of BBUs (int32),
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
    Get the access token for a Storage device

    Args:
        client: DME API client
        storage_id: storage device ID(Required)

    Returns:
        {
            ip: Storage device IP address,
            passphrase: Token to access the Storage device,
            port: Port to access the Storage device (int32),
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
    Query the fan info of a Storage device

    Args:
        client: DME API client
        storage_id: ID of the storage device (Optional, 1~64 characters)
        health_status: health status(Optional). valid values: unknown, normal, faulty
        running_status: running status(Optional). valid values: unknown, normal, running, not_running, spin_down, online, offline
        run_level: Run level(Optional). valid values: low, normal, high
        enclosure_name: Name of the enclosure (Optional, 1~256 characters), supports fuzzy match
        location: location (Optional, 1~256 characters), supports fuzzy match
        zone_id: Zone ID (Optional, 1~255 characters), only supported by OceanStor A800 series storage
        page_no: Page number for paginated query (Optional, 1~2147483647, default 1)
        page_size: Page size for paginated query (Optional, 1~1000, default 20)

    Returns:
        {
            total: Fan count (integer),
            fans: Fan list (List<StorageFanInfo>). parameter format: [{
                name: name (1~128 characters),
                location: location (1~256 characters),
                health_status: health status. valid values: unknown, normal, faulty,
                running_status: running status. valid values: unknown, normal, running, not_running, spin_down, online, offline,
                run_level: Run level. valid values: low, normal, high,
                enclosure_id: ID of the enclosure on the Storage device (1~255 characters),
                enclosure_name: Name of the enclosure (1~255 characters),
                zone_id: Zone ID (1~255 characters), only supported by OceanStor A800 series storage,
                zone_ip: Zone IP address (1~255 characters), only supported by OceanStor A800 series storage,
                zone_name: Zone name (1~255 characters), only supported by OceanStor A800 series storage,
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
    Query the disk info list of a Storage device

    Args:
        client: DME API client.
        storage_id: storage device ID (1~36 characters, must satisfy uuid format).
        ids: Port ID list (Optional, List<string>, max array members: 100, min array members: 0).
        name: Disk name (Optional, 1~256 characters).
        slot_number: Slot number, location (Optional, 1~256 characters). Supports fuzzy search.
        bom_id: BOM ID (Optional, 1~256 characters).
        health_status: health status (Optional). valid values: unknown, normal, fault, pre_fail, degraded, single_link, no_redundant_link, subhealthy, offline.
        physical_type: Disk type (Optional). valid values: unknown, sata (SATA), sas (SAS), nl_sas (NL-SAS), ssd (SSD), ssd_card (SSD card), scm (SCM), nl_ssd (NL-SSD), fc (FC), lun (LUN), ata (ATA), flash (FLASH), vmdisk (VMDISK), sas_flash_vp (SAS-FLASH-VP), hdd (HDD).
        new_physical_type: Actual disk type (Optional). valid values: SAS, SATA, SSD, NL_SAS, SLC_SSD, MLC_SSD, FC_SED, SAS_SED, SATA_SED, SSD_SED, SCM_SED, NL_SAS_SED, SLC_SSD_SED, MLC_SSD_SED, NVMe_SSD, NVMe_SSD_SED, SCM, CAPACITY_OPTIMIZED_SSD, CAPACITY_OPTIMIZED_SSD_SED, unknown, sas_disk, sata_disk, ssd_card, ssd_card_virtual, ssd_disk, m2_disk, FC, ATA, FLASH, VMDISK, SAS_FLASH_VP, HDD.
        capacity: total capacity (Optional, max: 9223372036854775807, unit: GB).
        role: Disk role (Optional). valid values: unknown, free, member, hotSpare, cache, aggregate, broken, foreign, labelmaint, maintenance, shared, spare, unassigned, unsupported, remote, mediator.
        disk_pool_name: Name of the disk domain it belongs to (Optional, 1~256 characters). Supports fuzzy search.
        disk_pool_id: Disk pool or disk domain ID (Optional, 1~64 characters). Only supported by Huawei Storage devices and third-party devices.
        storage_pool_id: storage pool ID (Optional, 1~64 characters).
        bar_code: Disk barcode (Optional, 1~256 characters).
        sn: Disk serial number (Optional, 1~256 characters). Only supported by Huawei Storage devices and third-party devices.
        speed: Rotational speed (Optional, max: 2147483647, unit: RPM).
        storage_ip: IP address of the device (Optional, 1~255 characters).
        management_ip: Management device IP address (Optional, 1~256 characters).
        node_name: Node name (Optional, 1~256 characters).
        virtual_disk: Virtual disk (Optional). valid values: true, false.
        status: running status (Optional). valid values: unknown, normal, abnormal, online, offline.
        enclosure_name: Enclosure name of the fan storage device (Optional, 1~255 characters). Supports fuzzy search.
        zone_id: zone id of the storage device (Optional, 1~255 characters). Only supported by OceanStor A800 storage.
        sort_key: Sort field (Optional). valid values: capacity (total capacity), speed, remainLife, name (disk name), management_ip, slot_number (location).
        sort_dir: Sort direction (Optional). valid values: asc, desc.
        page_no: Page number for paginated query (Optional, 1~2147483647, default value: 1).
        page_size: Page size for paginated query (Optional, 1~1000, default value: 20).

    Returns:
        {
            total: Disk count (integer),
            disks: Disk list (List<DiskInfo>). parameter format: [{
                id: Disk ID (string),
                name: Disk name (string),
                health_status: health status (string),
                physical_type: Disk type (string),
                capacity: total capacity (integer),
                sn: Disk serial number (string),
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
    Query Storage device Storage pool list

    Args:
        client: DME API client
        storage_id: Storage device ID (Optional, 1~64 characters)
        raw_id: Storage pool ID on the Storage device (Optional, 1~64 characters)
        zone_id: Zone ID (Optional, 1~256 characters), supports exact search, only supported by OceanStor A800 storage
        page_no: Page number for paginated query (Optional, 1~10000, default 1)
        page_size: Page size for paginated query (Optional, 1~1000, default 10)
        sort_key: Sort field(Optional). valid values: total_capacity (Storage pool total capacity), consumed_capacity (Storage pool used capacity), free_capacity (Storage pool free capacity, only flash storage), replication_capacity (Storage pool protection capacity)
        sort_dir: Sort direction(Optional). valid values: asc, desc

    Returns:
        {
            total: Storage pool count (int32),
            datas: Storage pool basic info list (List<StoragePoolBasicInfo>). parameter format: [{
                id: storage pool ID (1~32 characters),
                name: storage pool name (1~31 characters),
                raw_id: Storage pool ID on the Storage device (1~64 characters),
                storage_id: storage device ID (1~64 characters),
                storage_name: storage device name (1~127 characters),
                usage_type: Storage pool usage. valid values: block-and-file (LUN/Filesystem), block, file, object, hdfs, converged,
                total_capacity: total capacity, unit MB (number),
                free_capacity: free capacity, unit MB (number), only supported by flash storage and OceanStor A800 devices,
                consumed_capacity: used capacity, unit MB (number),
                replication_capacity: Data protection capacity, unit MB (number), only supported by flash storage,
                subscribed_capacity: Total subscribed capacity, unit MB (number), only supported by flash storage and distributed devices,
                lun_subscribed_capacity: LUN subscribed capacity, unit MB (number), only supported by flash storage,
                filesystem_subscribed_capacity: Filesystem total subscribed capacity, unit MB (number), only supported by OceanStor Dorado V6 storage version 6.1.0 and above,
                health_status: health status. valid values: normal, fault, degraded, unknown. Only supported by flash storage and third-party storage,
                running_status: running status. valid values: pre-copy, rebuilt, online, offline, balancing, initializing, deleting, unknown. Only supported by flash storage,
                pool_status: Storage pool status. valid values: normal, fault, write-protect, stopped, fault-and-write-protect, migrating-data, degraded, rebuilding-data, migrating-services, all-copies-failed, all-copies-failed-and-write-protect, deleting, deletion-failed, unknown. Only supported by distributed storage,
                disk_types: Disk type list (List<string>), only supported by flash storage,
                capacity_usage: Capacity utilization,
                redundancy_policy: Redundancy policy. valid values: replication, ec (EC). Only supported by FusionStorage, OceanStor 100D and OceanStor Pacific series devices,
                num_data_units: Number of EC data blocks (integer), only valid when redundancy policy is ec,
                num_fault_tolerance: Number of EC allowable faulty nodes (integer), only valid when redundancy policy is ec,
                num_parity_units: Number of EC parity blocks (integer), only valid when redundancy policy is ec,
                cache_media_type: Storage pool cache type. valid values: ssd_card (SSD card & NVMe SSD), ssd_disk (SSD disk), none. Only supported by FusionStorage, OceanStor 100D, OceanStor A310 and OceanStor Pacific series devices,
                zone_id: Zone ID (1~64 characters), only supported by OceanStor A800 series storage,
                zone_ip: Zone IP (1~256 characters), only supported by OceanStor A800 series storage,
                zone_name: Zone name (1~256 characters), only supported by OceanStor A800 series storage,
                raid_level: RAID level list (List<string>). valid values: RAID0, RAID1, RAID2, RAID3, RAID5, RAID6, RAID10, RAID50, RAID_TP. Only supported by flash storage, OceanDisk, OceanStor A800 devices,
                disk_pool_id: Disk pool or disk domain ID (1~64 characters). The disk domain supports flash devices, the disk pool supports Pacific, A310 devices, OceanStor A800 devices support,
                disk_pool_name: Disk pool or disk domain name (1~256 characters),
                media_type: Storage pool primary storage type. valid values: sas_disk (SAS disk), sata_disk (SATA disk), ssd_card (SSD card & NVMe SSD), ssd_disk (SSD disk). Only supported by OceanStor Pacific, OceanStor A310, OceanStor 100D devices,
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
    Query HyperScale Storage pool list

    Args:
        client: DME API client
        raw_id: Storage pool ID on the Storage device (Optional, 1~64 characters), supports exact search
        name: HyperScale storage pool name (Optional, 1~256 characters), supports fuzzy search
        local_pool_id: Local storage pool ID under HyperScale Storage pool (Optional, 0~64 characters), supports filtering HyperScale Storage pool associated with the specified local Storage pool
        health_status: health status(Optional). valid values: normal, faulty, degraded
        running_status: running status(Optional). valid values: pre_copy, rebuilding, online, offline, balancing, initializing, deleting
        storage_id: storage device ID (Optional, 0~64 characters)
        description: HyperScale Storage pool description (Optional, 0~256 characters)
        page_no: Page number for paginated query (Optional, 1~10000, default 1)
        page_size: Page size for paginated query (Optional, 1~1000, default 20)
        sort_key: Sort field(Optional). valid values: raw_id (ID), total_capacity (Storage pool total capacity), consumed_capacity (used capacity), capacity_usage, free_capacity, subscribed_capacity_percentage
        sort_dir: Sort direction(Optional). valid values: asc, desc

    Returns:
        {
            total: HyperScale Storage pool total (int32),
            data: HyperScale Storage pool list (List<HyperScalePoolInfo>). parameter format: [{
                id: HyperScale storage pool ID (1~64 characters),
                raw_id: Storage pool ID on the Storage device (1~64 characters),
                name: HyperScale storage pool name (1~256 characters),
                description: HyperScale Storage pool description (1~256 characters),
                storage_id: storage device ID (1~64 characters),
                storage_ip: Storage device IP (1~255 characters),
                storage_name: storage device name (1~127 characters),
                health_status: health status. valid values: normal, faulty, degraded,
                running_status: running status. valid values: pre_copy, rebuilding, online, offline, balancing, initializing, deleting,
                total_capacity: total capacity, unit MB (number),
                consumed_capacity: used capacity, unit MB (number),
                capacity_usage: Capacity utilization (number),
                free_capacity: free capacity, unit MB (number),
                subscribed_capacity_percentage: Subscription ratio (number),
                subscribed_capacity: Total subscribed capacity, unit MB (number),
                used_subscribed_capacity: Used subscribed capacity, unit MB (number),
                redundancy_strategy: Redundancy strategy. valid values: disk (disk-level redundancy), distributed_ec (distributed EC),
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
    Query the node list of a Storage device

    Args:
        client: DME API client
        storage_id: storage device id (Optional, 1~64 characters), supports filtering
        raw_id: Node ID on the Storage device (Optional, 1~64 characters)
        storage_name: Storage device name (Optional, 1~255 characters), supports filtering
        name: Node name (Optional, 1~256 characters), supports fuzzy query (case insensitive)
        ids: Node ID list (Optional, List<string>, max array members: 100)
        mgmt_ip: Node management IP address (Optional, 1~256 characters), supports fuzzy query (case insensitive)
        frame_number: Cabinet/rack number (Optional, 1~256 characters), supports fuzzy query (case insensitive)
        slot_number: Slot/position within rack (Optional, 1~256 characters), supports fuzzy query (case insensitive)
        status: Node status(Optional). valid values: UNKNOWN, NORMAL, FAULT, PRE_FAIL, PARTIALLY_DAMAGED, DEGRADED, BAD_SECTORS_FOUND, BIT_ERRORS_FOUND, CONSISTENT, INCONSISTENT, BUSY, NO_INPUT, LOW_BATTERY, SINGLE_LINK_FAULT
        roles: Node role list (Optional, List<string>, max array members: 10). valid values: management, storage, compute (VBS computing), replication, paxos, dpc_compute (DPC computing)
        page_no: Page number for paginated query (Optional, 1~10000, default 1)
        page_size: Page size for paginated query (Optional, 1~1000, default 20)
        sort_key: Sort field(Optional). valid values: name (node name), mgmt_ip (node management IP address)
        sort_dir: Sort direction(Optional). valid values: asc, desc

    Returns:
        {
            total: Node count (integer),
            nodes: Node list (List<StorageNodeBaseInfo>). parameter format: [{
                id: Node id (1~64 characters),
                name: Node name (1~255 characters),
                raw_id: Node ID on the Storage device (1~64 characters),
                mgmt_ip: Node management IP address (1~255 characters),
                status: Node status (1~255 characters). valid values: UNKNOWN, NORMAL, FAULT, PARTIALLY_DAMAGED,
                node_model: Node model (1~255 characters). e.g.: DataTurbo, OceanStor Pacific, RH5288 V3,
                frame_number: Cabinet/rack number (1~255 characters),
                slot_number: Slot/position within rack (1~255 characters),
                roles: Node role list (List<string>). valid values: management, storage, compute (VBS computing), replication, paxos, dpc_compute (DPC computing),
                node_sn: Serial number info (1~255 characters),
                storage_id: storage device id (1~64 characters),
                storage_name: Storage device name (1~255 characters),
                eos_time: Storage EOS time (int64), total milliseconds from 1970-01-01 00:00:00 GMT to the present,
                installation_status: Storage software installation status. valid values: installed, not_installed,
                ip_address_list: Node IP address list (List<StorageNodeIpInfo>). parameter format: [{
                    ip_address: Node IP address (1~256 characters),
                    usage: Node IP address usage list (List<string>). valid values: storage_frontend, storage_backend, management_external_float, management_internal_float, management_external, management_internal, replication, quorum, iscsi,
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
    Query Storage device power supply details info, only supported by OceanStor A800 storage.

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, 1~64 characters)
        health_status: health status(Optional). valid values: unknown, normal, faulty, inconsistent, no_input
        running_status: running status(Optional). valid values: unknown, normal, running, online, offline
        power_type: Power supply type(Optional). valid values: dc (DC power supply), ac (AC power supply), hv (high-voltage DC power supply)
        power_mode: Power mode(Optional). valid values: balanced_power, active_power, standby_power
        location: location (Optional, 1~256 characters), supports fuzzy match
        model: model (Optional, 1~256 characters), supports fuzzy match
        sn: Serial number (Optional, 1~256 characters), supports fuzzy match
        enclosure_name: Enclosure name (Optional, 1~256 characters), supports fuzzy match
        zone_id: Zone ID (Optional, 1~64 characters), only supported by OceanStor A800 series storage
        page_no: Page number for paginated query (Optional, 1~2147483647, default 1)
        page_size: Page size for paginated query (Optional, 1~1000, default 20)

    Returns:
        {
            total: Power supply count (int32),
            storage_powers: Power supply list (List<StoragePowerInfo>). parameter format: [{
                name: name (1~255 characters),
                location: location (1~255 characters),
                health_status: health status. valid values: unknown, normal, faulty, inconsistent, no_input,
                running_status: running status. valid values: unknown, normal, running, online, offline,
                power_type: Power supply type. valid values: dc (DC power supply), ac (AC power supply), hv (high-voltage DC power supply),
                model: model (1~255 characters),
                sn: Serial number (1~255 characters),
                manufacturer: Manufacturer (1~255 characters),
                enclosure_name: Enclosure name (1~255 characters),
                production_date: Production date (1~255 characters),
                version: version (1~255 characters),
                bom_code: Power module BOM code (1~255 characters),
                power_mode: Power mode. valid values: balanced_power, active_power, standby_power,
                zone_name: Zone name (1~255 characters), only supported by OceanStor A800 series storage,
                zone_id: Zone ID (1~255 characters), only supported by OceanStor A800 series storage,
                zone_ip: Zone IP address (1~255 characters), only supported by OceanStor A800 series storage,
                storage_id: Storage device ID (1~64 characters),
                storage_name: Storage device name (1~128 characters),
                storage_ip: Storage device IP address (1~32 characters),
                storage_sn: Storage device serial number (1~64 characters),
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
    Query Storage device power data

    Args:
        client: DME API client
        start_time: Start time stamp (Required, 13-digit millisecond timestamp, pattern ^([0-9]){13}$)
        end_time: End time stamp (Required, 13-digit millisecond timestamp, pattern ^([0-9]){13}$)
        storage_ids: Storage ID list (Required, List<string>, max array members: 300)
        time_granularity: Time granularity(Required). valid values: HOUR, DAY, MONTH

    Returns:
        {
            storage_power_list: Storage power list (List<StoragePower>). parameter format: [{
                storage_id: Storage ID,
                power: Storage power, unit kilowatt (number),
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
           location: str = None, maintenance_start: int = None,
           maintenance_overtime: int = None, total_capacity: float = None,
           total_effective_capacity: float = None, total_pool_capacity: float = None,
           used_capacity: float = None, free_capacity: float = None,
           subscription_capacity: float = None, tag_ids: list = None) -> dict:
    """
    Modify a Storage device (only supports modifying recorded offline Storage device info)

    Args:
        client: DME API client.
        storage_id: Storage device ID (Required).
        name: Device name (Optional, 1~256 characters). Can only contain half-width letters, half-width digits, "_", "-", ".", and Chinese characters.
        ip: Device IP address (Optional, 0~128 characters, supports IPv4 and IPv6 formats, can also be an empty string).
        vendor: Vendor (Optional, 0~128 characters).
        model: Product model (Optional, 0~128 characters).
        version: Version info (Optional, 0~64 characters).
        patch_version: Patch version info (Optional, 0~64 characters).
        location: Device location (Optional, 0~512 characters).
        maintenance_start: Maintenance start time (Optional, format is millisecond timestamp). Must appear together with maintenance overtime and the value must be less than maintenance overtime.
        maintenance_overtime: Maintenance overtime (Optional, format is millisecond timestamp). Must appear together with maintenance start time and the value must be greater than maintenance start time.
        total_capacity: raw capacity (Optional, -1~2147483647, unit MB). The sum of physical capacities of all disks in the Storage device, -1 means no raw capacity.
        total_effective_capacity: effective capacity (Optional, -1~2147483647, unit MB). The total amount of user data that can be written to the Storage device, -1 means no effective capacity.
        total_pool_capacity: available capacity (Optional, -1~2147483647, unit MB). The actual usable disk physical space of the Storage device (after deducting RAID, metadata, etc.), -1 means no available capacity.
        used_capacity: used capacity (Optional, -1~2147483647, unit MB). The sum of used capacities of all Storage pools in the Storage device, -1 means no used capacity.
        free_capacity: free capacity (Optional, -1~2147483647, unit MB). The difference between the available capacity and used capacity of the Storage device, -1 means no free capacity.
        subscription_capacity: subscribed capacity (Optional, -1~2147483647, unit MB). The sum of subscribed capacities of all Storage pools in the Storage device, -1 means no subscribed capacity.
        tag_ids: tag ID list (Optional, string, 0~512 characters). Array format string, supports up to 10 tags, empty array means removing all tags associated with the Storage device.

    Returns:
        None
    """
    if not storage_id:
        raise ValueError("storage_id is a required parameter")

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
    if maintenance_start is not None:
        payload['maintenance_start'] = maintenance_start
    if maintenance_overtime is not None:
        payload['maintenance_overtime'] = maintenance_overtime
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
    # The modify interface returns an empty response, return an empty dict to indicate success
    return response if response else {}


def app_type_list(client: DMEAPIClient, storage_id: str, 
                 create_type: int = None, template_type: int = None, 
                 pool_id: str = None) -> dict:
    """
    Query the application types of a specified Storage device
    
    Only supported by Dorado type devices.
    
    Args:
        client: DME API client.
        storage_id: Storage device id (1~36 characters, must satisfy uuid format).
        create_type: create type (Optional, 0~1). valid values: 0 (system preset), 1 (user defined). Returns all types if not provided.
        template_type: Application type category (Optional, 0~1). valid values: 0 (LUN type), 1 (NAS type). Default is LUN type if not provided.
        pool_id: Storage pool id (Optional, 1~64 characters, letters and digits).
    
    Returns:
        {
            datas: Application type list (List<AppTypeInfo>). parameter format: [{
                id: workload type ID (string),
                name: Application type name (string),
                block_size: Block size (string),
            }, ...],
        }
        Fields include: enable_compress, enable_dedup, create_type, etc.
    """
    url = "/rest/storagemgmt/v1/storages/{storage_id}/workloads"
    
    query_params = {"storage_id": storage_id}
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
    Query the Controller info of a specified Storage device
    
    Query the Controller list info of a Storage device.
    
    Args:
        client: DME API client
        storage_id: Storage device ID (Required, 1~36 characters, UUID format or 32-bit hexadecimal)
    
    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, includes total and controllers fields
        - total: Controller total
        - controllers: Controller list, includes id, name, status, type and other info
    """
    url = "/rest/storagemgmt/v1/storages/{storage_id}/controllers"
    
    response = client.get(url, params={"storage_id": storage_id})
    return response


def disk_domain_list(client: DMEAPIClient, storage_id: str = None, page_no: int = 1,
                   page_size: int = 20) -> dict:
    """
    Batch query disk domains

    Args:
        client: DME API client
        storage_id: Storage device ID (Optional, 1~64 characters), supports filtering
        page_no: Page number for paginated query (Optional, 1~2147483647, default 1)
        page_size: Page size for paginated query (Optional, 1~1000, default 20)

    Returns:
        {
            total: Disk domain count (int32),
            disk_pools: Disk domain list (List<DiskPoolInfo>). parameter format: [{
                    id: Disk domain id (1~64 characters),
                    raw_id: Disk domain id on the device (1~64 characters),
                    name: Disk domain name (1~128 characters),
                    running_status: running status. valid values: online, offline, pre_copy, reconstruction, balancing, initializing, deleting, unknown,
                    health_status: health status. valid values: normal, fault, degraded, unknown,
                    total_capacity: Total available raw capacity, unit MB (number),
                    spare_capacity: Total hot spare raw capacity, unit MB (number),
                    used_capacity: Allocated raw capacity, unit MB (number),
                    used_spare_capacity: Used hot spare raw capacity, unit MB (number),
                    free_capacity: free capacity, unit MB (number),
                    storage_id: storage device id (1~64 characters),
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
    Batch query disk pools of distributed Storage devices. Only supported by OceanStor Pacific and OceanStor A310 storage.

    Args:
        client: DME API client
        storage_id: Storage device id (Optional, string, 1~64 characters). Non-OceanStor Pacific or A310 devices will report a parameter error
        page_no: Page number for paginated query (Optional, int32, 1~2147483647). default value: 1
        page_size: Page size for paginated query (Optional, int32, 1~1000). default value: 20

    Returns:
        {
            total: total (int32),
            disk_pools: Disk pool list. parameter format: [{
                id: Disk pool ID (string),
                name: Disk pool name (string),
                status: status (string),
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
    Batch query enclosure info

    Args:
        client: DME API client
        page_no: Page number for paginated query (Optional, 1~2147483647, default 1)
        page_size: Page size for paginated query (Optional, 1~1000, default 20)
        storage_id: Storage device ID (Optional, 1~64 characters)
        name: name (Optional, 1~256 characters), supports fuzzy match
        location: location (Optional, 1~256 characters), supports fuzzy match
        health_status: health status list (Optional, List<string>, max array members: 3). valid values: unknown, normal, faulty
        zone_name: Zone name (Optional, 1~255 characters), only supported by OceanStor A800 series storage, supports fuzzy match
        zone_id: Zone ID list (Optional, List<string>, max array members: 100), only supported by OceanStor A800 series storage
        running_status: running status list (Optional, List<string>, max array members: 7). valid values: unknown, normal, running, sleep_in_high_temperature, online, offline
        power_mode: Power mode list (Optional, List<string>, max array members: 2). valid values: load_balance, active_standby_power
        esn: Enclosure serial number (Optional, 1~256 characters), supports fuzzy match
        mac: MAC address (Optional, 1~256 characters), supports fuzzy match
        sort_key: Sort field(Optional). valid values: temperature
        sort_dir: Sort direction(Optional). valid values: asc, desc. default returns in ascending order

    Returns:
        {
            total: Enclosure count (integer),
            data: Enclosure list (List<EnclosureItem>). parameter format: [{
                    id: Enclosure ID (1~64 characters),
                    raw_id: Enclosure ID on the Storage device (1~64 characters),
                    name: name (1~256 characters),
                    model: model (1~32 characters). valid values: 0 (BMC control box), 1 (2U dual-controller 6Gbit/s SAS 12-bay 3.5-inch control box), 2 (2U dual-controller 6Gbit/s SAS 24-bay 2.5-inch control box), 16 (2U 6Gbit/s SAS 12-bay 3.5-inch disk enclosure), 17 (2U SAS 24-bay cascade box), 18 (4U 6Gbit/s SAS 24-bay 3.5-inch disk enclosure), 19 (4U FC 24-bay cascade box), 20 (1U PCIe data switch), 21 (4U 6Gbit/s SAS 75-bay 3.5-inch disk enclosure), 22 (SVP), 23 (2U dual-controller 6Gbit/s SAS 12-bay 3.5-inch control box), 24 (2U 6Gbit/s SAS 25-bay 2.5-inch disk enclosure), 25 (4U 6Gbit/s SAS 24-bay 3.5-inch disk enclosure), 26 (2U dual-controller 6Gbit/s SAS 25-bay 2.5-inch control box), 37 (2U dual-controller 6Gbit/s SAS 12-bay 3.5-inch control box), 38 (2U dual-controller 6Gbit/s SAS 25-bay 2.5-inch control box), 39 (4U 12Gbit/s SAS 75-bay 3.5-inch disk enclosure), 40 (2U dual-controller 12Gbit/s SAS 25-bay 2.5-inch control box), 65 (2U 12Gbit/s SAS 25-bay 2.5-inch disk enclosure), 66 (4U 12Gbit/s SAS 24-bay 3.5-inch disk enclosure), 67 (2U SAS 25-bay 2.5-inch disk enclosure), 69 (4U SAS 24-bay 3.5-inch disk enclosure), 96 (3U dual-controller control box), 97 (6U quad-controller control box), 98 (2U SSD 25-bay cascade box), 99 (2U dual-controller 12Gbit/s NVMe 25-bay 2.5-inch control box), 101 (2U SSD NVMe 25-bay 2.5-inch disk enclosure), 112 (4U quad-controller control box), 113 (2U dual-controller SAS 25-bay 2.5-inch control box), 114 (2U dual-controller SAS 12-bay 3.5-inch control box), 115 (2U dual-controller NVMe 36-bay control box), 116 (2U dual-controller SAS 25-bay 2.5-inch control box), 117 (2U dual-controller SAS 12-bay 3.5-inch control box), 118 (2U SAS 25-bay 2.5-inch smart disk enclosure), 119 (2U SAS 12-bay 3.5-inch smart disk enclosure), 120 (2U NVMe 36-bay smart disk enclosure), 122 (2U dual-controller NVMe 25-bay 2.5-inch control box), 132 (4U dual-controller 4-bay 2.5-inch 6-bay 3.5-inch control box), 133 (4U dual-controller NVMe 12-bay 2.5-inch control box), 135 (4U dual-controller 10-bay 2.5-inch control box), 143 (8U NVME dual-controller 64-bay 2.5-inch control box),
                    height: Height, unit U (integer),
                    location: Enclosure location (1~128 characters),
                    logic_type: type. valid values: disk_enclosure, controller_enclosure, data_switch, management_switch, management_server,
                    health_status: health status. valid values: unknown, normal, faulty,
                    running_status: running status. valid values: unknown, normal, running, sleep_in_high_temperature, online, offline, abnormal,
                    storage_id: Storage device ID (1~64 characters),
                    storage_name: Storage device name (1~128 characters),
                    storage_ip: Storage device IP address (1~32 characters),
                    storage_sn: Storage device serial number (1~64 characters),
                    storage_location: Storage device location (0~512 characters),
                    zone_name: Zone name (0~512 characters), only supported by OceanStor A800 series storage,
                    zone_ip: Zone IP address (1~128 characters), only supported by OceanStor A800 series storage,
                    zone_id: Zone ID (0~512 characters), only supported by OceanStor A800 storage,
                    esn: Enclosure serial number (0~512 characters),
                    mac: MAC address (0~512 characters),
                    power_mode: Power mode. valid values: load_balance, active_standby_power,
                    bar_code: Barcode (0~256 characters),
                    board_type: Board type (0~128 characters),
                    description: description (0~1024 characters),
                    temperature: Temperature, unit °C (0~128 characters),
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
    Batch query storage-side initiator objects

    Batch query the list of initiator objects on the storage side.

    Args:
        client: DME API client
        page_size: Number of items per page (Optional, 1~1000, default 100)
        page_no: Page number for paginated query (Optional, min 1, default 1)
        raw_id: Initiator WWPN/IQN/NQN (Optional, 0~256 characters, supports fuzzy match)
        alias: Initiator alias (Optional, 0~256 characters, supports fuzzy match)
        status: Initiator status (Optional). valid values: unknown, online, offline
        associated_host_name: Host name associated with the initiator (Optional, 0~256 characters, supports fuzzy match)
        associated_host_id: Host ID associated with the initiator (Optional, 0~64 characters; empty field queries initiators not added to a host)
        multipath_type: Third-party multipath policy (Optional, only for non-Dorado V6 products). valid values: default, third_party
        protocol: Initiator type (Optional). valid values: fc, iscsi, nvme_over_roce, sas, nvme_over_fabric, unknown
        support_provisioning: Whether provisioning is supported (Optional). valid values: true, false
        vstore_raw_id: tenant ID (Optional)
        vstore_name: Tenant name (Optional)
        storage_id: storage device ID (Optional, 0~64 characters)

    Returns:
        {
            total: Initiator count (int32),
            initiators: Initiator list (List<InitiatorInfo>). parameter format: [{
                id: Initiator ID (string),
                port_name: Port name (string),
                status: status (string),
            }, ...],
        }
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
    Batch delete initiator objects from a Storage device

    Args:
        client: DME API client
        initiator_ids: List of initiator IDs (Required, 1~100)
        task_remarks: Task remarks (Optional, up to 1024 characters)

    Returns:
        Task ID
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
    Modify the storage-side initiator object

    Modify the initiator. This operation will modify the specified initiator on the Storage device.

    Args:
        client: DME API client
        initiator_id: Initiator ID (Required)
        vstore_id: tenant ID (Optional, 1~64 characters; valid when device is OceanStor V300R006C30/V500R007C20/Dorado 6.1.3 or above)
        alias: Initiator alias (Optional, 0~31 characters, supports letters, digits, ._- and Chinese characters)
        multi_path: ModifyMultiPathRequestParam object (Optional; supported when device is OceanStor V300R003C20/V500R007C20/Dorado V300R001C01 or above). attribute format: {
                multi_path_type: Initiator multipath type (Optional). valid values: default, third_party,
                path_type: Initiator path type (Conditional required, required when multi_path_type is third_party). valid values: optimal_path, non_optimal_path,
                failover_mode: Initiator failover mode (Conditional required, required when multi_path_type is third_party). valid values: early_version_alua, common_alua, alua_not_used, special_alua,
                special_mode_type: Special mode type (Optional, valid when failover mode is special mode). valid values: 0 (special mode 0), 1 (special mode 1), 2 (special mode 2), 3 (special mode 3)
             }

    Returns:
        Task ID
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


# ============ Authentication user (account) subtopic functions ============


def account_show_local_users(client: DMEAPIClient, storage_id: str, vstore_raw_id: str = None,
                     name: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query the info of local authentication users on a specified Storage device

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, 1~36 characters)
        vstore_raw_id: ID of the tenant on the device that the local authentication user belongs to(Optional)
        name: Local authentication user name, supports fuzzy query(Optional)
        page_no: Page number for paginated query, default 1(Optional)
        page_size: Page size for paginated query, default 20(Optional)

    Returns:
        {
            total: User count (int32),
            local_users: Local authentication user list (List<LocalUserInfo>). parameter format: [{
                id: user ID (string),
                name: Username (string),
                type: User type (string),
            }, ...],
        }
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

    response = client.post(url, body=payload, params={"storage_id": storage_id})
    return response


def account_create_local_user(client: DMEAPIClient, storage_id: str, name: str, password: str,
                      primary_group_raw_id: str, description: str = None,
                      group_names: list = None, vstore_id: str = None) -> dict:
    """
    Create a local authentication user

    Args:
        client: DME API client
        storage_id: Storage device ID for creating local authentication user (1~36 characters, Required)
        name: Local authentication user name (1~255 characters, Required)
        description: Local authentication user description (1~255 characters, Optional)
        password: Local authentication user password (1~255 characters, Required)
        primary_group_raw_id: ID of the user group on the device that the local authentication user belongs to (1~64 characters, Required)
        group_names: List of temporary user group names that the created local authentication user belongs to (List<string>, min array members: 0, max array members: 31, Optional)
        vstore_id: Tenant ID that the local authentication user belongs to (1~64 characters, Optional. Conditional required, required when the created local authentication user belongs to a tenant)

    Returns:
        create result
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

    response = client.post(url, body=payload, params={"storage_id": storage_id})
    return response


def account_create_unix_user(client: DMEAPIClient, storage_id: str, name: str,
                      primary_group_raw_id: str, raw_id: int = None,
                      description: str = None, password: str = None,
                      status_enabled: bool = None, vstore_raw_id: str = None) -> dict:
    """
    Create a UNIX authentication user on a specified Storage device

    Args:
        client: DME API client
        storage_id: Storage device ID for creating UNIX authentication user (1~36 characters, Required)
        name: UNIX authentication user name (1~255 characters, Required)
        raw_id: ID of the UNIX authentication user on the device (int64, 0~4294967295, Optional)
        description: UNIX authentication user description (1~255 characters, Optional)
        password: UNIX authentication user password (1~255 characters, Optional)
        status_enabled: UNIX authentication user status (boolean, Optional). valid values: true (enabled), false (locked)
        primary_group_raw_id: ID of the user group on the device that the created UNIX authentication user belongs to (1~64 characters, Required)
        vstore_raw_id: ID of the tenant on the device that the UNIX authentication user belongs to (1~64 characters, Optional. Conditional required, required when the created UNIX authentication user belongs to a tenant)

    Returns:
        create result
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

    response = client.post(url, body=payload, params={"storage_id": storage_id})
    return response


def account_create_windows_user(client: DMEAPIClient, storage_id: str, name: str, password: str,
                                 raw_id: int = None, description: str = None,
                                 status_enabled: bool = None,
                                 vstore_raw_id: str = None) -> dict:
    """
    Create a Windows authentication user on a specified Storage device

    Args:
        client: DME API client
        storage_id: Storage device ID for creating Windows authentication user (1~36 characters, Required)
        name: Windows authentication user name (1~255 characters, Required)
        raw_id: ID of the Windows authentication user on the device (int64, 1000~4294967295, Optional)
        description: Windows authentication user description (1~255 characters, Optional)
        password: Windows authentication user password (1~255 characters, Required)
        status_enabled: Windows authentication user status (boolean, Optional). valid values: true (enabled), false (locked)
        vstore_raw_id: ID of the tenant on the device that the created Windows authentication user belongs to (1~64 characters, Optional. Conditional required, required when the Windows authentication user belongs to a tenant)

    Returns:
        create result
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
    Query the info of UNIX authentication users on a specified Storage device

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, 1~36 characters)
        vstore_raw_id: ID of the tenant on the device that the UNIX authentication user belongs to(Optional)
        name: UNIX authentication user name, supports fuzzy query(Optional)
        page_no: Page number for paginated query, default 1(Optional)
        page_size: Page size for paginated query, default 20(Optional)

    Returns:
        {
            total: User count (int32),
            unix_users: UNIX authentication user list (List<UnixUserInfo>). parameter format: [{
                id: user ID (string),
                name: Username (string),
                uid: UID (int32),
            }, ...],
        }
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

    response = client.post(url, body=payload, params={"storage_id": storage_id})
    return response


def account_show_windows_users(client: DMEAPIClient, storage_id: str, vstore_raw_id: str = None,
                       name: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query the info of Windows authentication users on a specified Storage device

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, 1~36 characters)
        vstore_raw_id: ID of the tenant on the device that the Windows authentication user belongs to(Optional)
        name: Windows authentication user name, supports fuzzy query(Optional)
        page_no: Page number for paginated query, default 1(Optional)
        page_size: Page size for paginated query, default 20(Optional)

    Returns:
        {
            total: User count (int32),
            windows_users: Windows authentication user list (List<WindowsUserInfo>). parameter format: [{
                id: user ID (string),
                name: Username (string),
            }, ...],
        }
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

    response = client.post(url, body=payload, params={"storage_id": storage_id})
    return response


def account_show_local_user_groups(client: DMEAPIClient, storage_id: str, vstore_raw_id: str = None,
                           name: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query the info of local authentication user groups on a specified Storage device

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, 1~36 characters)
        vstore_raw_id: ID of the tenant on the device that the local authentication user group belongs to(Optional)
        name: Local authentication user group name, supports fuzzy query(Optional)
        page_no: Page number for paginated query, default 1(Optional)
        page_size: Page size for paginated query, default 20(Optional)

    Returns:
        {
            total: User group count (int32),
            local_user_groups: Local authentication user group list (List<LocalUserGroupInfo>). parameter format: [{
                id: User group ID (string),
                name: User group name (string),
            }, ...],
        }
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

    response = client.post(url, body=payload, params={"storage_id": storage_id})
    return response


def account_show_unix_user_groups(client: DMEAPIClient, storage_id: str, vstore_raw_id: str = None,
                          name: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query the info of UNIX authentication user groups on a specified Storage device

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, 1~36 characters)
        vstore_raw_id: ID of the tenant on the device that the UNIX authentication user group belongs to(Optional)
        name: UNIX authentication user group name, supports fuzzy query(Optional)
        page_no: Page number for paginated query, default 1(Optional)
        page_size: Page size for paginated query, default 20(Optional)

    Returns:
        {
            total: User group count (int32),
            unix_user_groups: UNIX authentication user group list (List<UnixUserGroupInfo>). parameter format: [{
                id: User group ID (string),
                name: User group name (string),
                gid: GID (int32),
            }, ...],
        }
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

    response = client.post(url, body=payload, params={"storage_id": storage_id})
    return response


def account_show_windows_user_groups(client: DMEAPIClient, storage_id: str, vstore_raw_id: str = None,
                             name: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query the info of Windows authentication user groups on a specified Storage device

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, 1~36 characters)
        vstore_raw_id: ID of the tenant on the device that the Windows authentication user group belongs to(Optional)
        name: Windows authentication user group name, supports fuzzy query(Optional)
        page_no: Page number for paginated query, default 1(Optional)
        page_size: Page size for paginated query, default 20(Optional)

    Returns:
        {
            total: User group count (int32),
            windows_user_groups: Windows authentication user group list (List<WindowsUserGroupInfo>). parameter format: [{
                id: User group ID (string),
                name: User group name (string),
            }, ...],
        }
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

    response = client.post(url, body=payload, params={"storage_id": storage_id})
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
    Batch query QoS policies

    Args:
        client: DME API client
        storage_id: Storage device ID(Required)
        name: QoS policy name (Optional, 1~256 characters)
        raw_id: QoS policy device-side ID(Optional)
        enable_status: Activation status (Optional, true/false)
        running_status: running status (Optional, running/inactive/waiting)
        zone_id: Zone ID(Optional)
        resource_type_list: Controlled resource type list (Optional, file_system/vstore/none)
        vstore_id: Tenant ID(Optional)
        vstore_name: Tenant name(Optional)
        alarm_status: Alarm status (Optional, normal/event/alarm/invalid)
        io_policy_type: IO policy type (Optional, total_perf_upper_limit/read_or_write_upper_limit)
        page_no: Page number (Optional, default 1)
        page_size: items per page (Optional, default 10, max 1000)
        sort_key: Sort field (Optional, name/raw_id)
        sort_dir: Sort direction (Optional, asc/desc)

    Returns:
        {
            total: QoS policy total (int32),
            datas: QoS policy list (List<qosDetailResponse>). parameter format: [{
                id: QoS policy ID (string, 1~32 characters),
                name: QoS policy name (string, 1~31 characters),
                description: description (string, 1~255 characters),
                raw_id: QoS policy device-side ID (string, 1~64 characters),
                enable_status: Activation status. valid values: true, false,
            }, ...],
        }
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
    Query the details of a specified QoS policy

    Args:
        client: DME API client
        qos_policy_id: QoS policy ID(Required)
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
    Create a QoS policy

    Create a new QoS policy, can configure performance limits, alarm parameters and scheduled scheduling.

    Args:
        client: DME API client
        name: QoS policy name (Required, 1~31 characters)
        storage_id: Storage device ID(Required)
        resource_type: Controlled resource type (Required, file_system/vstore)
        resource_ids: Controlled resource ID list (Required, array of 1~512 members)
        description: description (Optional, 1~255 characters)
        zone_id: Zone ID (Optional, required for A series storage)
        vstore_id: Tenant ID (Optional, required when resource_type is file_system)
        enable_status: Activation status (Optional, enable/disable, default enable)
        io_policy_type: IO policy type (Optional, total_perf_upper_limit/read_or_write_upper_limit)
        min_bandwidth: min bandwidth MB/s(Optional)
        max_bandwidth: max bandwidth MB/s(Optional)
        burst_bandwidth: Burst bandwidth MB/s (Optional, must be greater than max_bandwidth)
        min_iops: Min IOPS(Optional)
        max_iops: Max IOPS(Optional)
        burst_iops: Burst IOPS (Optional, must be greater than max_iops)
        burst_time: Max burst duration in seconds (Optional, 1~999999999)
        latency: IO latency target in microseconds (Optional, 500/1500)
        max_read_bandwidth: Max read bandwidth MB/s(Optional)
        max_write_bandwidth: Max write bandwidth MB/s(Optional)
        burst_read_bandwidth: Burst read bandwidth MB/s(Optional)
        burst_write_bandwidth: Burst write bandwidth MB/s(Optional)
        max_read_iops: Max read IOPS(Optional)
        max_write_iops: Max write IOPS(Optional)
        burst_read_iops: Burst read IOPS(Optional)
        burst_write_iops: Burst write IOPS(Optional)
        alarm_switch: Alarm switch (Optional, on/off)
        alarm_level: severity (Optional, event/alarm)
        alarm_threshold: Alarm threshold % (Optional, 0~100)
        resume_threshold: Resume threshold % (Optional, 0~100)
        schedule_policy: Schedule policy (Optional, once/daily/weekly)
        schedule_start_date: Effective start date (Optional, yyyy-MM-dd)
        start_time: Effective start time (Optional, hh:mm)
        duration: Effective duration in seconds (Optional, 1800~86400)
        weekly_days: Weekly schedule days (Optional, [0-6] for Sunday to Saturday)
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
    Modify a QoS policy

    Modify the configuration of an existing QoS policy.

    Args:
        client: DME API client
        qos_policy_id: QoS policy ID(Required)
        name: QoS policy name(Optional)
        description: description(Optional)
        io_policy_type: IO policy type(Optional)
        min_bandwidth: min bandwidth MB/s(Optional)
        max_bandwidth: max bandwidth MB/s(Optional)
        burst_bandwidth: Burst bandwidth MB/s(Optional)
        min_iops: Min IOPS(Optional)
        max_iops: Max IOPS(Optional)
        burst_iops: Burst IOPS(Optional)
        burst_time: Max burst duration in seconds(Optional)
        latency: IO latency target in microseconds(Optional)
        max_read_bandwidth: Max read bandwidth MB/s(Optional)
        max_write_bandwidth: Max write bandwidth MB/s(Optional)
        burst_read_bandwidth: Burst read bandwidth MB/s(Optional)
        burst_write_bandwidth: Burst write bandwidth MB/s(Optional)
        max_read_iops: Max read IOPS(Optional)
        max_write_iops: Max write IOPS(Optional)
        burst_read_iops: Burst read IOPS(Optional)
        burst_write_iops: Burst write IOPS(Optional)
        alarm_switch: Alarm switch(Optional)
        alarm_level: severity(Optional)
        alarm_threshold: Alarm threshold %(Optional)
        resume_threshold: Resume threshold %(Optional)
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
        # DME API requires camelCase naming for fields inside io_param
        import re
        def _to_camel(snake):
            parts = snake.split('_')
            return parts[0] + ''.join(p.capitalize() for p in parts[1:])
        payload['io_param'] = {_to_camel(k): v for k, v in io_param.items()}

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
    Delete QoS policies

    Delete one or more QoS policies.

    Args:
        client: DME API client
        qos_policy_ids: List of QoS policy IDs (Required, 1~100)
    """
    url = "/rest/storagepolicy/v1/qos/delete"

    payload = {
        'ids': qos_policy_ids
    }

    response = client.post(url, body=payload)
    return response


def qos_activate(client: DMEAPIClient, qos_policy_ids: list) -> dict:
    """
    Batch activate QoS policies

    Activate one or more QoS policies.

    Args:
        client: DME API client
        qos_policy_ids: List of QoS policy IDs(Required)
    """
    url = "/rest/storagepolicy/v1/qos/active"

    payload = {
        'qos_ids': qos_policy_ids
    }

    response = client.post(url, body=payload)
    return response


def qos_deactivate(client: DMEAPIClient, qos_policy_ids: list) -> dict:
    """
    Batch deactivate QoS policies

    Deactivate one or more QoS policies.

    Args:
        client: DME API client
        qos_policy_ids: List of QoS policy IDs(Required)
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
    Associate QoS policy with controlled resources

    Associate one or more resources with a QoS policy.

    Args:
        client: DME API client
        qos_policy_id: QoS policy ID(Required)
        resource_ids: List of resource IDs(Required)
        resource_type: resource type (Required, file_system/vstore)
    """
    url = "/rest/storagepolicy/v1/qos/{qos_policy_id}/resources/associate"

    payload = {
        'resource_ids': resource_ids,
        'resource_type': resource_type
    }

    response = client.post(url, body=payload, params={"qos_policy_id": qos_policy_id})
    return response


def qos_unassociate(client: DMEAPIClient, qos_policy_id: str,
                    resource_ids: list, resource_type: str) -> dict:
    """
    Disassociate QoS policy from controlled resources

    Disassociate resources from a QoS policy.

    Args:
        client: DME API client
        qos_policy_id: QoS policy ID(Required)
        resource_ids: List of resource IDs(Required)
        resource_type: resource type(Required)
    """
    url = "/rest/storagepolicy/v1/qos/{qos_policy_id}/resources/unassociate"

    payload = {
        'resource_ids': resource_ids,
        'resource_type': resource_type
    }

    response = client.post(url, body=payload, params={"qos_policy_id": qos_policy_id})
    return response


# ============ Storage Logic port (logic_port) subtopic functions ============


def logic_port_list(client: DMEAPIClient, storage_id: str = None, vstore_raw_id: str = None,
                    zone_raw_id: str = None, scope: str = None, page_no: int = 1,
                    page_size: int = 100) -> dict:
    """
    Query the Logic port list of a Storage device

    Args:
        client: DME API client
        storage_id: storage device ID (Optional, 1~64 characters)
        vstore_raw_id: vStore id on the Storage device (Optional, 1~64 characters)
        zone_raw_id: Zone ID on the device (Optional, 1~64 characters), only supported by OceanStor A800 series storage
        scope: Scope(Optional). valid values: hyperscale, default. Only supported by OceanStor A800 series storage
        page_no: Page number for paginated query (Optional, 1~10000, default 1)
        page_size: Page size for paginated query (Optional, 1~1000, default 100)

    Returns:
        {
            total: Logic port count (integer),
            logic_ports: Logic port list (List<StorageLogicPortResp>). parameter format: [{
                id: Logic port ID (1~255 characters),
                raw_id: Logic port ID on the Storage device (1~255 characters),
                name: Logic port name (1~255 characters),
                running_status: running status. valid values: UNKNOWN, NORMAL, RUNNING, LINK_UP, LINK_DOWN, TO_BE_RECOVERED, INITIALIZING, STANDBY, POWERING_ON, POWERED_OFF, POWER_ON_FAILED,
                operational_status: Activation status. valid values: ACTIVATED, NOT_ACTIVATED,
                mgmt_ip: ipv4 address (1~255 characters),
                ipv4_gateway: Logic port gateway IP address (IPV4) (1~64 characters),
                ipv4_mask: Logic port IP address mask (IPV4) (1~64 characters),
                mgmt_ipv6: ipv6 address (1~255 characters),
                ipv6_mask: Logic port IP address mask (IPV6) (1~128 characters),
                ipv6_gateway: Logic port gateway IP address (IPV6) (1~128 characters),
                home_port_raw_id: Parent port ID on the Storage device (1~255 characters),
                home_port_name: Parent port name (1~255 characters),
                home_port_type: Parent port type. valid values: ETHERNET_PORT (Ethernet port and RoCE port), BOND, VLAN, VIP, SIP, IB,
                home_controller_raw_id: Main Controller ID on the Storage device (1~256 characters),
                current_port_raw_id: Current physical port ID on the Storage device (1~255 characters),
                current_port_name: Current physical port name (1~255 characters),
                role: Port role (1~10 characters). valid values: 0 (unknown), 1 (management), 2 (data), 3 (management+data), 4 (replication), 6 (currently meaningless), 7 (currently meaningless), 8 (client), 9 (VTEP), 10 (health check), 11 (data backup), 12 (system management), 100 (cluster), 101 (inter-cluster),
                ddns_status: Dynamic DNS true status. valid values: INVALID, ENABLE, DISABLED,
                failover_group_raw_id: Failover group ID on the Storage device (1~255 characters),
                failover_group_name: Failover group name (1~255 characters),
                support_protocol: Data access protocol supported by Logic port. valid values: NONE (no protocol), NFS, CIFS, NFS_AND_CIFS, NFS_OVER_RDMA, iSCSI, FC/FCoE, NVME_OVER_ROCE, BGP, DATA_TURBO, DATA_TURBO_OVER_ROCE, S3, NFS_OVER_IB, DATA_TURBO_OVER_IB, DATA_TURBO_OVER_ROCE_AND_TCP, OBJECT, NAS_AND_OBJECT, KB_OVER_TCP,
                logical_type: Logical type. valid values: SERVICE (host port/service port), MANAGEMENT, MAINTENANCE,
                listen_dns_query_enabled: Whether to listen to DNS query requests (1~255 characters). valid values: NO (false), YES (enabled),
                management_access: Management access method (1~255 characters),
                vstore_raw_id: vStore id assigned on the device (1~255 characters),
                vstore_name: vStore name (1~255 characters),
                storage_id: storage device ID (1~255 characters),
                storage_name: storage device name (1~255 characters),
                zone_raw_id: Zone ID on the device (1~255 characters), only supported by OceanStor A800 series storage,
                zone_id: Zone ID (1~64 characters), only supported by OceanStor A800 series storage,
                zone_name: Zone name (1~255 characters), only supported by OceanStor A800 series storage,
                zone_ip: Zone IP (1~255 characters),
                dns_zone_name: DNS zone name (1~255 characters),
                current_port_type: Physical port type. valid values: ETHERNET_PORT (Ethernet port and RoCE port), BOND, VLAN, VIP, SIP, IB,
                address_family: IP protocol version. valid values: IPv4, IPv6,
                can_failover: Whether to enable IP address drift (boolean). valid values: true, false,
                failback_mode: Failback mode. valid values: not_support, manual, automatic,
                scope: Scope. valid values: hyperscale, default. Only supported by OceanStor A800 series storage,
                logicPortTags: Associated tag collection (List<Tag>). parameter format: [{
                    id: Tag ID (1~32 characters),
                    tag_type_name: tag type name (1~64 characters),
                    name: tag name (1~128 characters),
                }, ...],
                manufacturer: Manufacturer (1~32 characters),
                storage_model: model (1~64 characters),
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
    Query the Logic port details of a Storage device

    Args:
        client: DME API client
        logic_port_id: Logic port ID (Required, 1~64 characters, UUID format or 32-bit hexadecimal)

    Returns:
        {
            id: Logic port ID (1~255 characters),
            raw_id: Logic port ID on the Storage device (1~255 characters),
            name: Logic port name (1~255 characters),
            running_status: running status. valid values: UNKNOWN, NORMAL, RUNNING, LINK_UP, LINK_DOWN, TO_BE_RECOVERED, INITIALIZING, STANDBY, POWERING_ON, POWERED_OFF, POWER_ON_FAILED,
            operational_status: Activation status. valid values: ACTIVATED, NOT_ACTIVATED,
            mgmt_ip: ipv4 address (1~255 characters),
            ipv4_gateway: Logic port gateway IP address (IPV4) (1~64 characters),
            ipv4_mask: Logic port IP address mask (IPV4) (1~64 characters),
            mgmt_ipv6: ipv6 address (1~255 characters),
            ipv6_mask: Logic port IP address mask (IPV6) (1~128 characters),
            ipv6_gateway: Logic port gateway IP address (IPV6) (1~128 characters),
            home_port_raw_id: Parent port ID on the Storage device (1~255 characters),
            home_port_name: Parent port name (1~255 characters),
            home_port_type: Parent port type. valid values: ETHERNET_PORT (Ethernet port and RoCE port), BOND, VLAN, VIP, SIP, IB,
            home_controller_raw_id: Main Controller ID on the Storage device (1~256 characters),
            current_port_raw_id: Current physical port ID on the Storage device (1~255 characters),
            current_port_name: Current physical port name (1~255 characters),
            role: Port role (1~10 characters). valid values: 0 (unknown), 1 (management), 2 (data), 3 (management+data), 4 (replication), 6 (currently meaningless), 7 (currently meaningless), 8 (client), 9 (VTEP), 10 (health check), 11 (data backup), 12 (system management), 100 (cluster), 101 (inter-cluster),
            ddns_status: Dynamic DNS true status. valid values: INVALID, ENABLE, DISABLED,
            failover_group_raw_id: Failover group ID on the Storage device (1~255 characters),
            failover_group_name: Failover group name (1~255 characters),
            support_protocol: Data access protocol supported by Logic port. valid values: NONE (no protocol), NFS, CIFS, NFS_AND_CIFS, NFS_OVER_RDMA, iSCSI, FC/FCoE, NVME_OVER_ROCE, BGP, DATA_TURBO, DATA_TURBO_OVER_ROCE, S3, NFS_OVER_IB, DATA_TURBO_OVER_IB, DATA_TURBO_OVER_ROCE_AND_TCP, OBJECT, NAS_AND_OBJECT, KB_OVER_TCP,
            logical_type: Logical type. valid values: SERVICE (host port/service port), MANAGEMENT, MAINTENANCE,
            listen_dns_query_enabled: Whether to listen to DNS query requests (1~255 characters). valid values: NO (false), YES (enabled),
            management_access: Management access method (1~255 characters),
            vstore_raw_id: vStore id assigned on the device (1~255 characters),
            vstore_name: vStore name (1~255 characters),
            storage_id: storage device ID (1~255 characters),
            storage_name: storage device name (1~255 characters),
            zone_raw_id: Zone ID on the device (1~255 characters), only supported by OceanStor A800 series storage,
            zone_id: Zone ID (1~64 characters), only supported by OceanStor A800 series storage,
            zone_name: Zone name (1~255 characters), only supported by OceanStor A800 series storage,
            zone_ip: Zone IP (1~255 characters),
            dns_zone_name: DNS zone name (1~255 characters),
            current_port_type: Physical port type. valid values: ETHERNET_PORT (Ethernet port and RoCE port), BOND, VLAN, VIP, SIP, IB,
            address_family: IP protocol version. valid values: IPv4, IPv6,
            can_failover: Whether to enable IP address drift (boolean). valid values: true, false,
            failback_mode: Failback mode. valid values: not_support, manual, automatic,
            scope: Scope. valid values: hyperscale, default. Only supported by OceanStor A800 series storage,
            logicPortTags: Associated tag collection (List<Tag>). parameter format: [{
                id: Tag ID (1~32 characters),
                tag_type_name: tag type name (1~64 characters),
                name: tag name (1~128 characters),
            }, ...],
            manufacturer: Manufacturer (1~32 characters),
            storage_model: model (1~64 characters),
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
    Create a Logic port on a Storage device (only supported by OceanStor A800 series storage)

    Args:
        client: DME API client
        storage_id: storage device ID (Required, 1~64 characters)
        name: Port name (Required, 1~255 characters). Only allows letters, digits, "_", "-", "." and Chinese characters
        address_family: IP protocol version(Required). valid values: IPv4, IPv6
        home_port_type: Parent port type(Required). valid values: ETHERNET_PORT (Ethernet port and RoCE port), BOND, VLAN, VIP, SIP, IB
        zone_raw_id: Zone ID on the device (Required, 1~64 characters), only supported by OceanStor A800 series storage
        scope: Scope(Required). valid values: hyperscale, default. Only supported by OceanStor A800 series storage. When data access protocol is KB_OVER_TCP, only default is supported
        mgmt_ip: Logic port IP address (IPV4) (Optional, up to 64 characters, IPv4 format)
        ipv4_mask: Logic port IP address mask (IPV4) (Optional, up to 64 characters)
        ipv4_gateway: Logic port gateway IP address (IPV4) (Optional, up to 64 characters)
        mgmt_ipv6: Logic port IP address (IPV6) (Optional, up to 128 characters)
        ipv6_mask: Logic port IP address mask (IPV6) (Optional, up to 128 characters)
        ipv6_gateway: Logic port gateway IP address (IPV6) (Optional, up to 128 characters)
        home_port_raw_id: Parent port ID on the Storage device (Optional, 1~64 characters)
        support_protocol: Data access protocol supported by Logic port(Optional). valid values: NFS, DATA_TURBO_OVER_ROCE, NFS_OVER_RDMA, NFS_OVER_IB, DATA_TURBO_OVER_IB, DATA_TURBO_OVER_ROCE_AND_TCP, OBJECT, NAS_AND_OBJECT, KB_OVER_TCP. When role is CLIENT, this field cannot be provided
        operational_status: Activation status(Optional). valid values: ACTIVATED, NOT_ACTIVATED
        home_controller_id: Controller ID (Optional, 1~64 characters). When role is HEALTH_CHECK, this field must be configured
        failover_group_raw_id: Failover group ID on the Storage device (Optional, up to 64 characters). When data access protocol is KB_OVER_TCP, this field must be configured
        vstore_raw_id: vStore id assigned on the device (Optional, up to 64 characters). When role is CLIENT, this field cannot be provided
        role: Logic port role (Optional, default DATA). valid values: MANAGEMENT, DATA, VTEP, HEALTH_CHECK, MANAGEMENT_AND_DATA, CLIENT
        dns_zone_name: DNS zone name (Optional, up to 255 characters). When role is CLIENT or data access protocol is KB_OVER_TCP, this field cannot be provided
        listen_dns_query_enabled: Whether to listen for DNS query requests (Optional, pattern NO|YES). valid values: NO (false), YES (enabled). When role is CLIENT or data access protocol is KB_OVER_TCP, this field cannot be provided
        can_failover: Whether to enable IP address drift (Optional, boolean). valid values: true, false. When data access protocol is KB_OVER_TCP, this field cannot be provided
        failback_mode: Failback mode(Optional). valid values: not_support, manual, automatic. When data access protocol is KB_OVER_TCP, this field cannot be provided

    Returns:
        {
            task_id: Task Id (1~64 characters),
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
    Modify a Logic port on a Storage device (only supported by OceanStor A800 series storage)

    Args:
        client: DME API client
        logic_port_id: Logic port ID (Required, 1~128 characters)
        name: Port name(Optional)
        address_family: IP protocol version(Optional)
        mgmt_ip: Logic port IP address (IPV4)(Optional)
        ipv4_mask: Logic port IP address mask (IPV4)(Optional)
        ipv4_gateway: Logic port gateway IP address (IPV4)(Optional)
        mgmt_ipv6: Logic port IP address (IPV6)(Optional)
        ipv6_mask: Logic port IP address mask (IPV6)(Optional)
        ipv6_gateway: Logic port gateway IP address (IPV6)(Optional)
        home_port_raw_id: Parent port ID on the Storage device(Optional)
        home_port_type: Parent port type(Optional)
        operational_status: Activation status(Optional)
        failover_group_raw_id: Failover group ID on the Storage device(Optional)
        dns_zone_name: DNS zone name(Optional)
        listen_dns_query_enabled: Whether to listen for DNS query requests(Optional)
        can_failover: Whether to enable IP address drift(Optional)
        failback_mode: Failback mode(Optional)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
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
    Delete Logic ports from a Storage device (only supported by OceanStor A800 series storage)

    Args:
        client: DME API client
        ids: List of Logic port IDs (Required, 1~1000 IDs)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
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
    Failback a Logic port on a Storage device (only supported by OceanStor A800 series storage)

    Args:
        client: DME API client
        id: Logic port ID (Required, 1~64 characters)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
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
    Query Storage device port info, supports ETH, FC, IB, Bond, SAS five types

    Args:
        client: DME API client
        storage_id: Storage device ID (Optional, 1~36 characters)
        port_type: Port type (Optional, eth/fc/ib/bond/sas, returns all types if not specified)
        location: location (Optional, only supported by ETH ports, 1~255 characters)
        ipv4: IPv4 address (Optional, only supported by ETH ports, 1~255 characters)
        ipv6: IPv6 address (Optional, only supported by ETH ports, 1~255 characters)
        port_name: Port name (Optional, only supported by ETH ports, 1~255 characters)
        zone_id: storage device zone ID (Optional, only supported by Bond ports, 1~36 characters)
        page_no: Page number for paginated query (Optional, supported by FC/SAS ports, 1~10000, default 1)
        page_size: items per page (Optional, supported by FC/SAS ports, 1~1000, default 20)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
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
        # Return all types of ports (ETH + FC + IB + SAS)
        all_eth_ports = []
        all_fc_ports = []
        all_ib_ports = []
        all_sas_ports = []
        total_count = 0

        # Query ETH ports
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
        # ETH port API returns structure: {'total': N, 'eth_ports': [...]}
        if 'eth_ports' in eth_response:
            all_eth_ports = eth_response.get('eth_ports', [])
            total_count += len(all_eth_ports)

        # Query FC port
        fc_url = "/rest/storagemgmt/v1/frontend-ports/fc-ports/query"
        fc_payload = {
            'page_no': page_no,
            'page_size': page_size
        }
        if storage_id is not None:
            fc_payload['storage_id'] = storage_id
        fc_response = client.post(fc_url, body=fc_payload)
        # FC port API returns structure: {'total': N, 'ports': [...]}
        if 'ports' in fc_response:
            all_fc_ports = fc_response.get('ports', [])
            total_count += len(all_fc_ports)

        # Query IB ports
        ib_url = "/rest/storagemgmt/v1/storages/ib-ports/query"
        ib_payload = {}
        if storage_id is not None:
            ib_payload['storage_id'] = storage_id
        ib_response = client.post(ib_url, body=ib_payload)
        # IB port API returns structure: {'ib_ports': [...]}
        if 'ib_ports' in ib_response:
            all_ib_ports = ib_response.get('ib_ports', [])
            total_count += len(all_ib_ports)

        # Query SAS ports
        sas_url = "/rest/storagemgmt/v1/backend-ports/sas-ports/query"
        sas_payload = {
            'page_no': page_no,
            'page_size': page_size
        }
        if storage_id is not None:
            sas_payload['storage_id'] = storage_id
        sas_response = client.post(sas_url, body=sas_payload)
        # SAS port API returns structure: {'total': N, 'ports': [...]}
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
    Query the member list info of a specified bond port

    Args:
        client: DME API client
        bond_port_id: Bond port id (Required, 1~64 characters)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, includes total and eth_ports fields
    """
    url = "/rest/storagemgmt/v1/bond-ports/{bond_port_id}/eth-ports"

    response = client.get(url, params={"bond_port_id": bond_port_id})
    return response


# ============ Storage port group (port_group) subtopic functions ============


# ============ Storage VLAN subtopic functions ============


def vlan_list(client: DMEAPIClient, name: str = None, storage_id: str = None,
              page_no: int = 1, page_size: int = 100) -> dict:
    """
    Batch query VLAN list

    Args:
        client: DME API client
        name: VLAN name (supports fuzzy query)
        storage_id: Storage device ID
        page_no: pagination start page, default 1
        page_size: items per page, 1~1000, default 100

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, includes VLAN list
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
    Create a VLAN

    Note: Only supported by OceanStor A800, A600 series storage.

    Args:
        client: DME API client
        name: VLAN name(Required)
        vlan_id: VLAN ID (Required, 1~4094)
        storage_id: Storage device ID(Required)
        description: VLAN description(Optional)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, includes the newly created VLAN ID
    """
    url = "/rest/vlanmgmt/v1/vlans"

    body_params = {
        'name': name,
        'vlan_id': vlan_id,
        'storage_id': storage_id
    }

    if description is not None:
        body_params['description'] = description

    response = client.post(url, body=body_params)
    return response


def vlan_delete(client: DMEAPIClient, vlan_id: str) -> dict:
    """
    Delete a VLAN

    Note: Only supported by OceanStor A800, A600 series storage.

    Args:
        client: DME API client
        vlan_id: VLAN ID

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/vlanmgmt/v1/vlans/{vlan_id}"

    response = client.delete(url, params={"vlan_id": vlan_id})
    return response


def vlan_modify(client: DMEAPIClient, vlan_id: str, name: str = None,
                description: str = None) -> dict:
    """
    Modify a VLAN

    Note: Only supported by OceanStor A800, A600 series storage.

    Args:
        client: DME API client
        vlan_id: VLAN ID
        name: VLAN name(Optional)
        description: VLAN description(Optional)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/vlanmgmt/v1/vlans/{vlan_id}"

    body_params = {}
    if name is not None:
        body_params['name'] = name
    if description is not None:
        body_params['description'] = description

    response = client.put(url, body=body_params, params={"vlan_id": vlan_id})
    return response


# ============ Storage failover group (failover_group) subtopic functions ============


def failover_group_list(client: DMEAPIClient, storage_id: str,
                        failover_group_type: str = None,
                        zone_id: str = None,
                        failover_group_service_type: list = None) -> dict:
    """
    Query failover group list

    Args:
        client: DME API client
        storage_id: storage device ID (Required, 1~36 characters, must satisfy regex ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$)
        failover_group_type: Failover group type(Optional). valid values: system, VLAN, customized
        zone_id: Zone ID (Optional, 1~255 characters), only supported by OceanStor A800 series storage
        failover_group_service_type: Failover group service type list (Optional, List<string>, max array members: 10). valid values: NAS (for failover groups associated with NFS, CIFS, NFS and OBJECT protocol type Logic ports), BGP (for failover groups associated with VIP type Logic ports), RDMA (for failover groups associated with NFS over RDMA, NFS, OBJECT protocol Logic ports), IB (for failover groups associated with NAS over IB protocol type Logic ports), KB (for failover groups associated with KnowledgeBase over TCP protocol type Logic ports)

    Returns:
        {
            total: Failover group count (int32),
            failover_groups: Failover group list (List<FailoverGroupResp>). parameter format: [{
                id: Failover group id (1~64 characters),
                name: Failover group name (1~64 characters),
                failover_group_type: Failover group type (1~255 characters). valid values: system, VLAN, customized,
                raw_id: Failover group ID on the Storage device (1~255 characters),
                zone_name: Zone name (1~255 characters), only supported by OceanStor A800 series storage,
                zone_raw_id: Zone ID assigned on the Storage device (1~255 characters), only supported by OceanStor A800 series storage,
                zone_id: storage device zone ID (1~255 characters), only supported by OceanStor A800 series storage,
                failover_group_service_type: Failover group service type. valid values: NAS (for failover groups associated with NFS, CIFS, NFS and OBJECT protocol type Logic ports), BGP (for failover groups associated with VIP type Logic ports), RDMA (for failover groups associated with NFS over RDMA, NFS, OBJECT protocol Logic ports), IB (for failover groups associated with NAS over IB protocol type Logic ports), KB (for failover groups associated with KnowledgeBase over TCP protocol type Logic ports),
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
    if failover_group_service_type is not None:
        payload['failover_group_service_type'] = failover_group_service_type

    response = client.post(url, body=payload)
    return response


def failover_group_show_ports(client: DMEAPIClient, failover_group_id: str,
                               port_type: str = None) -> dict:
    """
    Query ports under a failover group (supports bond, eth, ib three types)

    Args:
        client: DME API client
        failover_group_id: Failover group id (Required, 1~64 characters)
        port_type: Port type (Optional, bond/eth/ib, returns all types if not specified)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, consistent structure: {"total": x, "bond_ports": [], "eth_ports": [], "ib_ports": []}
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
        # No type specified, return all three types of ports in a flattened structure
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
    Query VLANs under a failover group

    Args:
        client: DME API client
        failover_group_id: Failover group id (Required, 1~64 characters)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, includes vlans field
    """
    url = "/rest/storagemgmt/v1/failover-groups/{failover_group_id}/vlans"

    response = client.get(url, params={"failover_group_id": failover_group_id})
    return response


# ============ zone (OceanStor A800 cluster zone) subtopic functions ============


def zone_list(client: DMEAPIClient, name: str = None, ip: str = None,
              status: list = None, sync_status: list = None,
              sn: str = None, storage_ids: list = None) -> dict:
    """
    Query zone info in an OceanStor A800 cluster

    Args:
        client: DME API client
        name: zone name (Optional, 1~256 characters), exact query
        ip: zone ip address name (Optional, 1~256 characters), exact query
        status: zone status list (Optional, List<string>, max array members: 6). valid values: OFFLINE, NORMAL, FAULT, DEGRADED, ABNORMAL, UNKNOWN
        sync_status: zone sync status list (Optional, List<string>, max array members: 5). valid values: UNSYNC, SYNC, NORMAL, FAILED, UNKNOWN
        sn: zone serial number (Optional, 1~128 characters), exact query
        storage_ids: OceanStor A800 cluster id list (Optional, List<string>, max array members: 100, min members: 1), exact query

    Returns:
        {
            total: zone total (int32),
            datas: zone list (List<OceanStorA800 zone info>). parameter format: [{
                id: zone ID in CMDB (1~64 characters),
                native_id: native id (1~64 characters),
                name: zone name (1~128 characters),
                ip: zone IP address (1~32 characters),
                status: status (1~32 characters). valid values: OFFLINE, NORMAL, FAULT, DEGRADED, ABNORMAL,
                sync_status: Sync status (1~32 characters). valid values: UNSYNC, SYNC, NORMAL, FAILED,
                sn: zone device serial number (1~64 characters),
                wwn: zone device WWN (1~32 characters),
                vendor: zone vendor (1~32 characters),
                model: zone product model (1~64 characters),
                owning_ne_type: Storage device network element type. valid values: dorado (dorado series storage), OceanStor A800,
                location: zone location info (0~512 characters),
                version: version info (0~64 characters),
                patch_version: Patch version info (0~64 characters),
                add_time: Device access time (0~32 characters), UTC timestamp (milliseconds),
                last_sync_time: Last sync time (0~32 characters), UTC timestamp (milliseconds),
                sync_process: Sync progress (int32),
                alarm_num: Alarm count (number),
                parent_id: cluster id,
                zone_raw_id: zone raw id,
                is_core_zone: Whether it is the zone where the core control node is located (boolean). valid values: true, false,
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


# action list, for CLI help
# format: action_key: {func, description, params, subtopic}
# subtopic indicates which subtopic the action belongs to, None means direct action

ACTIONS = {
    # Direct actions (two-level structure: <topic> <action>)
    'list': {
        'func': list,
        'description': 'Batch query storage devices',
        'params': ['az', 'source', 'dc_id', 'tag_ids', 'start', 'limit', 'ext_attrs'],
        'subtopic': None
    },
    'show': {
        'func': show,
        'description': 'Query the specified storage device',
        'params': ['storage_id'],
        'subtopic': None
    },
    'add': {
        'func': add,
        'description': 'Add a storage device (only supports recording offline storage device info)',
        'params': ['name', 'sn', 'ip', 'vendor', 'model', 'version', 'patch_version', 'dc_id', 'az', 'location', 'maintenance_start', 'maintenance_overtime', 'total_capacity', 'total_effective_capacity', 'total_pool_capacity', 'used_capacity', 'free_capacity', 'subscription_capacity', 'tag_ids'],
        'subtopic': None
    },
    'remove': {
        'func': remove,
        'description': 'Batch remove storage devices',
        'params': ['storage_ids'],
        'subtopic': None
    },
    'sync': {
        'func': sync,
        'description': 'Sync storage device info',
        'params': ['storage_id'],
        'subtopic': None
    },
    'modify': {
        'func': modify,
        'description': 'Modify a storage device (only supports modifying recorded offline storage device info)',
        'params': ['storage_id', 'name', 'location', 'ext_attrs'],
        'subtopic': None
    },
    # subtopic action (three-level structure: <topic> <subtopic> <action>)
    'bbu_list': {
        'func': bbu_list,
        'description': 'Query the BBU info list of a storage device',
        'params': ['storage_id', 'health_status', 'running_status', 'enclosure_name',
                   'location', 'zone_id', 'page_no', 'page_size'],
        'subtopic': 'bbu'
    },
    'get_passphrase': {
        'func': get_passphrase,
        'description': 'Get the access token for a storage device',
        'params': ['storage_id'],
    },
    'fan_list': {
        'func': fan_list,
        'description': 'Query the fan info of a storage device',
        'params': ['storage_id', 'health_status', 'running_status', 'run_level',
                   'enclosure_name', 'location', 'zone_id', 'page_no', 'page_size'],
        'subtopic': 'fan'
    },
    'disk_list': {
        'func': disk_list,
        'description': 'Query the disk info list of a storage device',
        'params': ['storage_id'],
        'subtopic': 'disk'
    },
    'pool_list': {
        'func': pool_list,
        'description': 'Query the storage pool list of a storage device',
        'params': ['storage_id', 'raw_id', 'zone_id', 'page_no', 'page_size', 'sort_key', 'sort_dir'],
        'subtopic': 'pool'
    },
    'hyperscale_pool_list': {
        'func': hyperscale_pool_list,
        'description': 'Query the HyperScale storage pool list',
        'params': ['raw_id', 'name', 'local_pool_id', 'health_status', 'running_status', 'storage_id', 'description', 'page_no', 'page_size', 'sort_key', 'sort_dir'],
        'subtopic': 'hyperscale_pool'
    },
    'node_list': {
        'func': node_list,
        'description': 'Query the node list of a storage device',
        'params': ['storage_id', 'raw_id', 'storage_name', 'name', 'ids',
                   'mgmt_ip', 'frame_number', 'slot_number', 'status', 'roles',
                   'page_no', 'page_size', 'sort_key', 'sort_dir'],
        'subtopic': 'node'
    },
    'psu_list': {
        'func': psu_list,
        'description': 'Get the power supply (PSU) list of a storage device',
        'params': ['storage_id', 'health_status', 'running_status', 'power_type',
                   'power_mode', 'location', 'model', 'sn', 'enclosure_name',
                   'zone_id', 'page_no', 'page_size'],
        'subtopic': 'psu'
    },
    'query_power_data': {
        'func': query_power_data,
        'description': 'Query storage device power data',
        'params': ['start_time', 'end_time', 'storage_ids', 'time_granularity'],
    },
    'app_type_list': {
        'func': app_type_list,
        'description': 'Query the application types of a specified storage device',
        'params': ['storage_id'],
        'subtopic': 'app_type'
    },
    'controller_list': {
        'func': controller_list,
        'description': 'Query the controller info of a specified storage device',
        'params': ['storage_id'],
        'subtopic': 'controller'
    },
    'disk_domain_list': {
        'func': disk_domain_list,
        'description': 'Batch query disk domains',
        'params': ['storage_id', 'page_no', 'page_size'],
        'subtopic': 'disk_domain'
    },
    'disk_pool_list': {
        'func': disk_pool_list,
        'description': 'Batch query disk pools of distributed storage devices',
        'params': ['storage_id', 'page_no', 'page_size'],
        'subtopic': 'disk_pool'
    },
    'enclosure_list': {
        'func': enclosure_list,
        'description': 'Batch query enclosure info',
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
        'description': 'Create a tenant',
        'params': ['name', 'storage_id', 'san_capacity_quota', 'nas_capacity_quota', 'description', 'nas_capacity_quota_alarm_switch', 'nas_capacity_quota_alarm_threshold', 'associate_pool_ids'],
        'subtopic': 'vstore'
    },
    'vstore_modify': {
        'func': vstore_modify,
        'description': 'Modify the specified tenant',
        'params': ['vstore_id', 'name', 'san_capacity_quota', 'nas_capacity_quota', 'description', 'nas_capacity_quota_alarm_switch', 'nas_capacity_quota_alarm_threshold'],
        'subtopic': 'vstore'
    },
    'vstore_delete': {
        'func': vstore_delete,
        'description': 'Batch delete tenants',
        'params': ['vstore_ids'],
        'subtopic': 'vstore'
    },
    'initiator_list': {
        'func': initiator_list,
        'description': 'Batch query storage-side initiator objects',
        'params': ['page_size', 'page_no', 'raw_id', 'alias', 'status',
                   'associated_host_name', 'associated_host_id', 'multipath_type',
                   'protocol', 'support_provisioning', 'vstore_raw_id',
                   'vstore_name', 'storage_id'],
        'subtopic': 'initiator'
    },
    'initiator_delete': {
        'func': initiator_delete,
        'description': 'Batch delete initiator objects from a storage device',
        'params': ['initiator_ids', 'task_remarks'],
        'subtopic': 'initiator'
    },
    'initiator_modify': {
        'func': initiator_modify,
        'description': 'Modify the storage-side initiator object',
        'params': ['initiator_id', 'vstore_id', 'alias', 'multi_path'],
        'subtopic': 'initiator'
    },
    # account subtopic action (authentication users)
    'account_show_local_users': {
        'func': account_show_local_users,
        'description': 'Query the info of local authentication users on a specified storage device',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_create_local_user': {
        'func': account_create_local_user,
        'description': 'Create a local authentication user',
        'params': ['storage_id', 'name', 'account_password', 'primary_group_raw_id', 'description', 'group_names', 'vstore_id'],
        'subtopic': 'account'
    },
    'account_create_unix_user': {
        'func': account_create_unix_user,
        'description': 'Create a UNIX authentication user on a specified storage device',
        'params': ['storage_id', 'name', 'primary_group_raw_id', 'raw_id', 'description', 'password', 'status_enabled', 'vstore_raw_id'],
        'subtopic': 'account'
    },
    'account_create_windows_user': {
        'func': account_create_windows_user,
        'description': 'Create a Windows authentication user on a specified storage device',
        'params': ['storage_id', 'name', 'password', 'raw_id', 'description', 'status_enabled', 'vstore_raw_id'],
        'subtopic': 'account'
    },
    'account_show_unix_users': {
        'func': account_show_unix_users,
        'description': 'Query the info of UNIX authentication users on a specified storage device',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_show_windows_users': {
        'func': account_show_windows_users,
        'description': 'Query the info of Windows authentication users on a specified storage device',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_show_local_user_groups': {
        'func': account_show_local_user_groups,
        'description': 'Query the info of local authentication user groups on a specified storage device',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_show_unix_user_groups': {
        'func': account_show_unix_user_groups,
        'description': 'Query the info of UNIX authentication user groups on a specified storage device',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_show_windows_user_groups': {
        'func': account_show_windows_user_groups,
        'description': 'Query the info of Windows authentication user groups on a specified storage device',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    # qos subtopic action
    'qos_list': {
        'func': qos_list,
        'description': 'Batch query QoS policies',
        'params': ['storage_id', 'name', 'raw_id', 'enable_status', 'running_status',
                   'zone_id', 'resource_type_list', 'vstore_id', 'vstore_name',
                   'alarm_status', 'io_policy_type', 'page_no', 'page_size',
                   'sort_key', 'sort_dir'],
        'subtopic': 'qos'
    },
    'qos_show': {
        'func': qos_show,
        'description': 'Query the details of a specified QoS policy',
        'params': ['qos_policy_id'],
        'subtopic': 'qos'
    },
    'qos_create': {
        'func': qos_create,
        'description': 'Create a QoS policy',
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
        'description': 'Modify a QoS policy',
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
        'description': 'Delete QoS policies',
        'params': ['qos_policy_ids'],
        'subtopic': 'qos'
    },
    'qos_activate': {
        'func': qos_activate,
        'description': 'Batch activate QoS policies',
        'params': ['qos_policy_ids'],
        'subtopic': 'qos'
    },
    'qos_deactivate': {
        'func': qos_deactivate,
        'description': 'Batch deactivate QoS policies',
        'params': ['qos_policy_ids'],
        'subtopic': 'qos'
    },
    'qos_associate': {
        'func': qos_associate,
        'description': 'Associate QoS policy with controlled resources',
        'params': ['qos_policy_id', 'resource_ids', 'resource_type'],
        'subtopic': 'qos'
    },
    'qos_unassociate': {
        'func': qos_unassociate,
        'description': 'Disassociate QoS policy from controlled resources',
        'params': ['qos_policy_id', 'resource_ids', 'resource_type'],
        'subtopic': 'qos'
    },
    # logic_port subtopic action (Storage Logic port)
    'logic_port_list': {
        'func': logic_port_list,
        'description': 'Query the logic port list of a storage device',
        'params': ['storage_id', 'vstore_raw_id', 'zone_raw_id', 'scope', 'page_no', 'page_size'],
        'subtopic': 'logic_port'
    },
    'logic_port_show': {
        'func': logic_port_show,
        'description': 'Query the logic port details of a storage device',
        'params': ['logic_port_id'],
        'subtopic': 'logic_port'
    },
    'logic_port_create': {
        'func': logic_port_create,
        'description': 'Create a logic port on a storage device (only supported by OceanStor A800 series storage)',
        'params': ['storage_id', 'name', 'address_family', 'home_port_type', 'zone_raw_id', 'scope',
                   'mgmt_ip', 'ipv4_mask', 'ipv4_gateway', 'mgmt_ipv6', 'ipv6_mask', 'ipv6_gateway',
                   'home_port_raw_id', 'support_protocol', 'operational_status', 'home_controller_id',
                   'failover_group_raw_id', 'vstore_raw_id', 'role', 'dns_zone_name',
                   'listen_dns_query_enabled', 'can_failover', 'failback_mode'],
        'subtopic': 'logic_port'
    },
    'logic_port_update': {
        'func': logic_port_update,
        'description': 'Modify a logic port on a storage device (only supported by OceanStor A800 series storage)',
        'params': ['logic_port_id', 'name', 'address_family', 'mgmt_ip', 'ipv4_mask', 'ipv4_gateway',
                   'mgmt_ipv6', 'ipv6_mask', 'ipv6_gateway', 'home_port_raw_id', 'home_port_type',
                   'operational_status', 'failover_group_raw_id', 'dns_zone_name',
                   'listen_dns_query_enabled', 'can_failover', 'failback_mode'],
        'subtopic': 'logic_port'
    },
    'logic_port_delete': {
        'func': logic_port_delete,
        'description': 'Delete logic ports from a storage device (only supported by OceanStor A800 series storage)',
        'params': ['ids'],
        'subtopic': 'logic_port'
    },
    'logic_port_failback': {
        'func': logic_port_failback,
        'description': 'Failback a logic port on a storage device (only supported by OceanStor A800 series storage)',
        'params': ['id'],
        'subtopic': 'logic_port'
    },
    # port subtopic action (storage port)
    'port_list': {
        'func': port_list,
        'description': 'Query storage device port info, supports ETH, FC, IB, Bond four types',
        'params': ['storage_id', 'port_type', 'location', 'ipv4', 'ipv6', 'port_name', 'zone_id', 'page_no', 'page_size'],
        'subtopic': 'port'
    },
    'port_show_bond_members': {
        'func': port_show_bond_members,
        'description': 'Query the member list info of a specified bond port',
        'params': ['bond_port_id'],
        'subtopic': 'port'
    },
    # vlan subtopic action (storage VLAN)
    'vlan_list': {
        'func': vlan_list,
        'description': 'Batch query VLAN list',
        'params': ['name', 'storage_id', 'page_no', 'page_size'],
        'subtopic': 'vlan'
    },
    'vlan_create': {
        'func': vlan_create,
        'description': 'Create a VLAN (only supported by OceanStor A800, A600 series storage)',
        'params': ['name', 'vlan_id', 'storage_id', 'description'],
        'subtopic': 'vlan'
    },
    'vlan_delete': {
        'func': vlan_delete,
        'description': 'Delete a VLAN (only supported by OceanStor A800, A600 series storage)',
        'params': ['vlan_id'],
        'subtopic': 'vlan'
    },
    'vlan_modify': {
        'func': vlan_modify,
        'description': 'Modify a VLAN (only supported by OceanStor A800, A600 series storage)',
        'params': ['vlan_id', 'name', 'description'],
        'subtopic': 'vlan'
    },
    # failover_group subtopic action (storage failover group)
    'failover_group_list': {
        'func': failover_group_list,
        'description': 'Query failover group list',
        'params': ['storage_id', 'failover_group_type', 'zone_id', 'failover_group_service_type'],
        'subtopic': 'failover_group'
    },
    'failover_group_show_ports': {
        'func': failover_group_show_ports,
        'description': 'Query ports under a failover group (supports bond, eth, ib three types)',
        'params': ['failover_group_id', 'port_type'],
        'subtopic': 'failover_group'
    },
    'failover_group_show_vlans': {
        'func': failover_group_show_vlans,
        'description': 'Query VLANs under a failover group',
        'params': ['failover_group_id'],
        'subtopic': 'failover_group'
    },
    # zone subtopic action (OceanStor A800 cluster zone)
    'zone_list': {
        'func': zone_list,
        'description': 'Query zone info in an OceanStor A800 cluster',
        'params': ['name', 'ip', 'status', 'sync_status', 'sn', 'storage_ids'],
        'subtopic': 'zone'
    },
}
