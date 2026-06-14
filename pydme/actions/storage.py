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
    Batch query storage device tenant info。

    Args:
        client: DME API client
        raw_id: Tenant在设备中的ID (Optional, string, 1~256 characters)
        vstore_id: Tenant ID (Optional, string, 1~64 characters)
        qos_id: QoS policyID (Optional, string, 1~64 characters)
        is_associated_qos: 租户是否已关联QoS (Optional, boolean, true,false)
        name: Tenant名称，supports fuzzy search (Optional, string, 1~256 characters)
        storage_id: Storage device ID (Optional, string, 1~255 characters)
        storage_ip: Storage device IP (Optional, string, 1~255 characters)
        storage_name: Storage device name (Optional, string, 1~255 characters)
        zone_id: Zone ID (Optional, string, 1~64 characters)。仅OceanStor Aseries storage only。
        status: Tenant状态 (Optional, string)。Options：active (已激活), inactive (inactive)
        nas_capacity_quota_alarm_switch: NASCapacity quota alarm switch (Optional, boolean, true,false)。仅OceanStor Aseries storage only。
        sort_key: Sort field (Optional, string)
        sort_dir: Sort direction (Optional, string)。Options：asc (升序), desc (降序)
        page_no: Page number (Optional, int32, 1~10000000). Default: 1
        page_size: Items per page (Optional, int32, 1~1000). Default: 100

    Returns:
        {
            total: TenantTotal count (integer),
            vstores: Tenant列表 (List<VstoreResp>, max array members：1000)。参数格式如下：[{
                id: Tenant的Unique identifier (string, 1~64 characters),
                qos_id: QoS policyID (string, 1~64 characters),
                raw_id: 在设备中的TenantID (string, 1~64 characters),
                storage_sn: Storage deviceSN (string, 1~64 characters),
                storage_id: Device ID (string, 1~64 characters),
                storage_ip: Device IP (string, 1~255 characters),
                storage_name: Device name (string, 1~255 characters),
                name: Tenant名称 (string, 1~256 characters),
                description: Tenant description (string, 0~255 characters),
                running_status: Running status (string)。Options：normal (正常), initializing (初始化),
                status: Tenant状态 (string)。Options：active (已激活), inactive (inactive),
                encrypt_option: Tenant的加密选项 (boolean, true,false),
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
    Query tenant details。

    Args:
        client: DME API client
        id: 租户id (Required, string, 1~256 characters)。需满足UUID format or 32-bit hex

    Returns:
        {
            id: Tenant的Unique identifier (string, 1~64 characters),
            name: Tenant名称 (string, 1~256 characters),
            description: Tenant description (string, 0~255 characters),
            storage_id: Device ID (string, 1~64 characters),
            status: Tenant状态 (string)。Options：active (已激活), inactive (inactive),
            running_status: Running status (string)。Options：normal (正常), initializing (初始化),
        }
    """
    url = "/rest/fileservice/v1/vstores/{id}"

    # Parameter validation
    if not id:
        raise ValueError("id 是Required参数")

    response = client.get(url, params={"id": id})
    return response


def vstore_create(client: DMEAPIClient, name: str, storage_id: str,
                  san_capacity_quota: str = None,
                  nas_capacity_quota: str = None, description: str = None,
                  nas_capacity_quota_alarm_switch: bool = None,
                  nas_capacity_quota_alarm_threshold: int = None,
                  associate_pool_ids: list = None) -> dict:
    """
    创建租户。OceanStor Dorado v3设备feature not supported。

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, string, 1~36 characters)。需满足UUID format or 32-bit hex
        name: Tenant name (Required, string, 1~256 characters)。仅包含字母、数字、"_"、"-"、"."and Chinese characters
        san_capacity_quota: SAN 容量配额（可选，单位：扇区）
        nas_capacity_quota: NAS 容量配额（可选，单位：扇区）
        description: Tenant description（可选，0~255  characters）
        nas_capacity_quota_alarm_switch: NAS Capacity quota alarm switch（可选，仅 A800 Device support）
        nas_capacity_quota_alarm_threshold: NAS Capacity quota alarmthreshold（可选，仅 A800 Device support）
        associate_pool_ids: Related storage池 ID 列表（可选，仅 A series device support）

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/fileservice/v1/vstores"

    if not storage_id:
        raise ValueError("参数 storage_id 是Required的")

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
    Modify租户，该操作会Modify storage devicetenant specified on。

    Args:
        client: DME API client
        id: 租户的ID (Required, string, 1~64 characters)。需满足UUID format or 32-bit hex
        name: Tenant name (Optional, string, 1~256 characters)。名称包含字母、数字、"_"、"-"、"."and Chinese characters
        san_capacity_quota: SAN容量配额 (Optional, string, 1~20 characters)
        nas_capacity_quota: NAS容量配额 (Optional, string, 1~20 characters)
        description: Tenant description (Optional, string, 0~255 characters)
        nas_capacity_quota_alarm_switch: NASCapacity quota alarm switch (Optional, boolean, true,false)。仅A800Device support
        nas_capacity_quota_alarm_threshold: NASCapacity quota alarmthreshold (Optional, int32, 50~100)。仅A800Device support

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/fileservice/v1/vstores/{id}"

    # Parameter validation
    if not id:
        raise ValueError("id 是Required参数")

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
    Batch delete租户，该操作会删除Storage devicetenant specified on。该APIMay directly or indirectly affect production services, causing service interruption or data loss. Proceed with caution.。

    Args:
        client: DME API client
        ids: 租户ID list (Required, List[string], max array members：100, min array members：1)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/fileservice/v1/vstores/delete"

    # Parameter validation
    if not ids or len(ids) == 0:
        raise ValueError("ids 是Required参数，至少需要1个Tenant ID")

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response



def list(client: DMEAPIClient, az: str = None, source: str = None,
         dc_id: str = None, tag_ids: str = None, start: int = 1, 
         limit: int = 20, ext_attrs: str = None) -> dict:
    """
    Batch query storage devices：支持Pagination，过滤。

    Args:
        client: DME API client。
        az: Availability zone ID (Optional, string, 1~64 characters)
        source: Storage device的来源 (Optional, string)。Options：add (接入), record (录入), all (所有)。默认查询接入设备
        dc_id: Storage deviceData center的ID (Optional, string, 1~32 characters)
        tag_ids: Tag filter list (Optional, string)。最多支持10个标签ID组合过滤，多个过滤条件之间为且关系
        start: Page queryStart position (Optional, int32, 1~10000)。Default：1
        limit: Items per page (Optional, int32, 1~1000). Default: 20
        ext_attrs: 扩展属性过滤列表 (Optional, string, 1~3000 characters)。最多支持10extended attributes combined filter

    Returns:
        {
            total: Storage deviceTotal count (int32),
            datas: Storage device list (List<StorageSummaryInfo>)。参数格式如下：[{
                id: Storage device ID (string),
                name: Storage device name (string),
                ip: IP 地址 (string),
                status: Running status (string),
                sn: Device serial number (string),
                vendor: 厂商 (string),
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
    QueryStorage device。

    Args:
        client: DME API client
        storage_id: Storage device ID，Required (Required, string, 1~36 characters)。需满足UUID format or 32-bit hex

    Returns:
        {
            id: Storage device ID (string),
            name: Storage device name (string),
            ip: IP 地址 (string),
            status: Running status (string),
            sn: Device serial number (string),
            vendor: 厂商 (string),
            model: Product model (string),
        }
    """
    url = "/rest/storagemgmt/v1/storages/{storage_id}/detail"

    if not storage_id:
        raise ValueError("storage_id 是Required参数")

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
    添加Storage device（only supports录入离线Storage device信息）

    通过离线方式添加Storage device信息到 DME 系统。

    Args:
        client: DME API client。
        name: Device name (1~256 characters)。can only contain half-width letters、半角数字、\"_\"、\"-\"、\".\"、中文字符。
        sn: Device serial number (regex is^[a-zA-Z0-9]{1,128}$)。
        ip: Device IP地址 (可选, 0~128 characters, 支持IPv4与IPv6格式, 也可为空string)。
        dc_id: 所属Data center ID (Optional, regex is^[a-zA-Z0-9]{1,128}$)。
        az: Availability zone (Optional, string)。
        vendor: 厂商 (可选, 0~128 characters)。
        model: Product model (可选, 0~128 characters)。
        version: 版本信息 (可选, 0~64 characters)。
        patch_version: Patch version info (可选, 0~64 characters)。
        location: 设备位置 (可选, 0~512 characters)。
        maintenance_start: 维护Start time (可选, 格式是毫second(s)级Timestamp)。must appear with warranty expiration time and value must be less。
        maintenance_overtime: Warranty expiration time (可选, 格式是毫second(s)级Timestamp)。需要和维护Start timemust appear together and value greater thanStart time。
        total_capacity: 裸容量 (可选, 0~2147483647, 单位MB)。
        total_effective_capacity: 可得容量 (可选, 0~2147483647, 单位MB)。
        total_pool_capacity: Available capacity (可选, 0~2147483647, 单位MB)。
        used_capacity: Used capacity (可选, 0~2147483647, 单位MB)。
        free_capacity: Free capacity (可选, 0~2147483647, 单位MB)。
        subscription_capacity: 已订阅容量 (可选, 0~2147483647, 单位MB)。
        tag_ids: 标签ID列表 (可选, List<string>, max array members: 10, min array members: 0)。
    
    Returns:
        {
            id: Storage device ID (string, 1~64 characters),
        }
    """
    if not name:
        raise ValueError("name 是Required参数")
    if not sn:
        raise ValueError("sn 是Required参数")

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
    批量Remove storage device。

    Args:
        client: DME API client
        ids: Storage device ID列表 (Required, List[string], max array members：100, min array members：1)

    Returns:
        {
            task_id: 任务Id (string, 1~64 characters),
        }
    """
    url = "/rest/storagemgmt/v2/storages/delete"

    if not ids or len(ids) == 0:
        raise ValueError("ids 是Required参数，至少需要1个Storage device ID")

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def sync(client: DMEAPIClient, storage_id: str) -> dict:
    """
    SyncStorage device信息，该接口为异步消息。

    Args:
        client: DME API client
        storage_id: Storage deviceId (Required, string, 1~64 characters)。通过Batch query storage devices接口获取

    Returns:
        无
    """
    url = "/rest/storagemgmt/v1/storages/refresh"

    if not storage_id:
        raise ValueError("storage_id 是Required参数")

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
        client: DME API client。
        storage_id: BBUStorage device的id (可选, 1~64 characters)。
        health_status: Health status (Optional)。Options：unknown (未知), normal (正常), faulty (故障), about_to_fail (即将故障), low_battery (电量不足)。
        running_status: Running status (Optional)。Options：unknown (未知), normal (正常), running (运行), online (在线), offline (离线), charging (正在充电), charging_completed (充电完成), discharging (正在放电)。
        enclosure_name: Enclosure name (可选, 1~256 characters)。supports fuzzy match。
        location: 位置 (可选, 1~256 characters)。supports fuzzy match。
        zone_id: Zone ID (可选, 1~255 characters)。仅OceanStor A800series storage only。
        page_no: Page number (可选, 1~2147483647, Default: 1)。
        page_size: Page size (可选, 1~1000, Default: 20)。
    
    Returns:
        {
            backup_powers: BBU list (List<StorageBackupPowerInfo>)。参数格式如下：[{
                name: 名称 (1~255 characters),
                location: 位置 (1~255 characters),
                health_status: Health status。Options：unknown (未知), normal (正常), faulty (故障), about_to_fail (即将故障), low_battery (电量不足),
                running_status: Running status. Options：unknown (未知), normal (正常), running (运行), online (在线), offline (离线), charging (正在充电), charging_completed (充电完成), discharging (正在放电),
                charge_times: 放电次数 (int64),
                firmware_version: Firmware version号 (1~255 characters),
                manufactured_date: 出厂日期 (1~255 characters),
                enclosure_id: 所属Enclosure在Storage device上ID (1~255 characters),
                enclosure_name: Enclosure name (1~255 characters),
                zone_id: Zone ID (1~255 characters)，仅OceanStor A800series storage only,
                zone_ip: Zone IP地址 (1~255 characters)，仅OceanStor A800series storage only,
                zone_name: Zone名称 (1~255 characters)，仅OceanStor A800series storage only,
            }, ...],
            total: BBU的count (int32),
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
    获取Storage device访问的令牌

    Args:
        client: DME API client
        storage_id: Storage device ID（Required）

    Returns:
        {
            ip: Storage device IP地址,
            passphrase: 访问Storage device的令牌,
            port: 访问Storage device的端口 (int32),
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
    query storage deviceFan信息

    Args:
        client: DME API client
        storage_id: Storage deviceID（可选，1~64 characters）
        health_status: Health status(Optional). Options：unknown (未知), normal (正常), faulty (故障)
        running_status: Running status(Optional). Options：unknown (未知), normal (正常), running (运行), not_running (未运行), spin_down (休眠), online (在线), offline (离线)
        run_level: 运行档位(Optional). Options：low (低), normal (正常), high (高)
        enclosure_name: 所属EnclosureName (Optional,1~256 characters），supports fuzzy match
        location: 位置（可选，1~256 characters），supports fuzzy match
        zone_id: Zone ID（可选，1~255 characters），仅OceanStor A800series storage only
        page_no: Page number（可选，1~2147483647，默认 1）
        page_size: Page size（可选，1~1000，默认 20）

    Returns:
        {
            total: Fancount (integer),
            fans: Fan list (List<StorageFanInfo>)。参数格式如下：[{
                name: 名称 (1~128 characters),
                location: 位置 (1~256 characters),
                health_status: Health status。Options：unknown (未知), normal (正常), faulty (故障),
                running_status: Running status. Options：unknown (未知), normal (正常), running (运行), not_running (未运行), spin_down (休眠), online (在线), offline (离线),
                run_level: 运行档位。Options：low (低), normal (正常), high (高),
                enclosure_id: 所属Enclosure在Storage device上ID (1~255 characters),
                enclosure_name: Enclosure name (1~255 characters),
                zone_id: Zone ID (1~255 characters)，仅OceanStor A800series storage only,
                zone_ip: Zone IP地址 (1~255 characters)，仅OceanStor A800series storage only,
                zone_name: Zone名称 (1~255 characters)，仅OceanStor A800series storage only,
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
        client: DME API client。
        storage_id: Storage device ID (1~36 characters, 满足uuid格式)。
        ids: Port ID列表 (可选, List<string>, max array members: 100, min array members: 0)。
        name: 硬盘名称 (可选, 1~256 characters)。
        slot_number: Slot number，位置 (可选, 1~256 characters)。supports fuzzy search。
        bom_id: BOM ID (可选, 1~256 characters)。
        health_status: Health status (Optional)。Options：unknown (未知), normal (正常), fault (故障), pre_fail (即将故障), degraded (降级), single_link (单链路), no_redundant_link (无冗余链路), subhealthy (亚健康), offline (离线)。
        physical_type: Disk type (可选)。Options：unknown (未知), sata (SATA), sas (SAS), nl_sas (NL-SAS), ssd (SSD), ssd_card (SSD卡), scm (SCM), nl_ssd (NL-SSD), fc (FC), lun (LUN), ata (ATA), flash (FLASH), vmdisk (VMDISK), sas_flash_vp (SAS-FLASH-VP), hdd (HDD)。
        new_physical_type: 真实的Disk type (可选)。Options：SAS, SATA, SSD, NL_SAS, SLC_SSD, MLC_SSD, FC_SED, SAS_SED, SATA_SED, SSD_SED, SCM_SED, NL_SAS_SED, SLC_SSD_SED, MLC_SSD_SED, NVMe_SSD, NVMe_SSD_SED, SCM, CAPACITY_OPTIMIZED_SSD, CAPACITY_OPTIMIZED_SSD_SED, unknown, sas_disk, sata_disk, ssd_card, ssd_card_virtual, ssd_disk, m2_disk, FC, ATA, FLASH, VMDISK, SAS_FLASH_VP, HDD。
        capacity: Total capacity (可选, max: 9223372036854775807, 单位: GB)。
        role: 硬盘角色 (可选)。Options：unknown (未知), free (空闲), member (成员), hotSpare (热备), cache (缓存), aggregate (聚合), broken (断开), foreign (外部), labelmaint (标签维护), maintenance (维护), shared (共享), spare (备用), unassigned (未分配), unsupported (不支持), remote (远程), mediator (中介)。
        disk_pool_name: 所属Disk pool名称 (可选, 1~256 characters)。supports fuzzy search。
        disk_pool_id: Disk pool或Disk poolID (可选, 1~64 characters)。仅华为Storage device，third-party device supports this field。
        storage_pool_id: Storage pool ID (Optional, 1~64 characters)。
        bar_code: 硬盘条码 (可选, 1~256 characters)。
        sn: 硬盘Serial number (可选, 1~256 characters)。仅华为Storage device，third-party device supports this field。
        speed: 转速 (可选, max: 2147483647, 单位: RPM)。
        storage_ip: 所属设备ip地址 (可选, 1~255 characters)。
        management_ip: 管理设备ip地址 (可选, 1~256 characters)。
        node_name: Node名称 (可选, 1~256 characters)。
        virtual_disk: 虚拟盘 (可选)。Options：true, false。
        status: Running status (Optional)。Options：unknown (未知), normal (正常), abnormal (故障), online (在线), offline (离线)。
        enclosure_name: FanStorage device的Enclosure名称 (可选, 1~255 characters)。supports fuzzy search。
        zone_id: Storage device的Zone id (可选, 1~255 characters)。仅OceanStor A800storage support。
        sort_key: Sort field (Optional)。Options：capacity (Total capacity), speed (转速), remainLife (剩余寿命), name (硬盘名称), management_ip (管理设备ip地址), slot_number (位置)。
        sort_dir: Sort direction (Optional). Options: asc (ascending), desc (descending)。
        page_no: Page number (可选, 1~2147483647, Default: 1)。
        page_size: Page size (可选, 1~1000, Default: 20)。

    Returns:
        {
            total: 硬盘的count (integer),
            disks: Disk list (List<DiskInfo>)。参数格式如下：[{
                id: 硬盘ID (string),
                name: 硬盘名称 (string),
                health_status: Health status (string),
                physical_type: Disk type (string),
                capacity: Total capacity (integer),
                sn: 硬盘Serial number (string),
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
    查询Storage deviceStorage pool列表

    Args:
        client: DME API client
        storage_id: Storage device的ID（可选，1~64 characters）
        raw_id: Storage poolon the storage deviceID（可选，1~64 characters）
        zone_id: Zone的ID（可选，1~256 characters），supports exact search，仅OceanStor A800storage support
        page_no: Page number（可选，1~10000，默认 1）
        page_size: Page size（可选，1~1000，默认 10）
        sort_key: Sort field(Optional). Options：total_capacity (Storage poolTotal capacity), consumed_capacity (Storage poolUsed capacity), free_capacity (Storage poolFree capacity，仅闪存存储), replication_capacity (Storage poolProtection capacity)
        sort_dir: Sort direction(Optional). Options：asc (升序), desc (降序)

    Returns:
        {
            total: Storage poolcount (int32),
            datas: Storage pool basic info list (List<StoragePoolBasicInfo>)。参数格式如下：[{
                id: Storage pool ID (1~32 characters),
                name: Storage pool name (1~31 characters),
                raw_id: Storage poolon the storage deviceID (1~64 characters),
                storage_id: Storage device ID (1~64 characters),
                storage_name: Storage device name (1~127 characters),
                usage_type: Storage pool用途。Options：block-and-file (LUN/Filesystem), block (块), file (文件), object (object), hdfs (hdfs), converged (融合),
                total_capacity: Total capacity，单位MB (number),
                free_capacity: Free capacity，单位MB (number)，仅闪存存储、OceanStor A800Device support,
                consumed_capacity: Used capacity，单位MB (number),
                replication_capacity: 数据Protection capacity，单位MB (number)，flash storage only,
                subscribed_capacity: 总订阅容量，单位MB (number)，仅闪存存储、分布式Device support,
                lun_subscribed_capacity: LUN的订阅容量，单位MB (number)，flash storage only,
                filesystem_subscribed_capacity: Filesystem总订阅容量，单位MB (number)，仅OceanStor Dorado V6存储6.1.0supported in version,
                health_status: Health status。Options：normal (正常), fault (故障), degraded (降级), unknown (未知)。flash and third-party storage only,
                running_status: Running status. Options：pre-copy (预拷贝), rebuilt (重构), online (在线), offline (离线), balancing (正在均衡), initializing (Initializing), deleting (Deleting), unknown (未知)。flash storage only,
                pool_status: Storage pool状态。Options：normal (正常), fault (故障), write-protect (写保护), stopped (停止), fault-and-write-protect (故障且写保护), migrating-data (Data migration), degraded (降级), rebuilding-data (数据重构), migrating-services (服务迁移), all-copies-failed (全副本故障), all-copies-failed-and-write-protect (全副本故障且写保护), deleting (Deleting), deletion-failed (删除失败), unknown (未知)。distributed storage only,
                disk_types: Disk type列表 (List<string>)，flash storage only,
                capacity_usage: 容量利用率,
                redundancy_policy: 冗余策略。Options：replication (副本), ec (EC)。仅FusionStorage、OceanStor 100D和OceanStor Pacificseries device support,
                num_data_units: EC数据块count (integer)，only when redundancy policy iseceffective when,
                num_fault_tolerance: ECAllowed faulty node count (integer)，only when redundancy policy iseceffective when,
                num_parity_units: EC校验块count (integer)，only when redundancy policy iseceffective when,
                cache_media_type: Storage pool缓存类型。Options：ssd_card (SSD卡&NVMe SSD), ssd_disk (SSD盘), none (无缓存)。仅FusionStorage、OceanStor 100D、OceanStor A310和OceanStor Pacificseries device support,
                zone_id: Zone的ID (1~64 characters)，仅OceanStor A800series storage only,
                zone_ip: Zone的IP (1~256 characters)，仅OceanStor A800series storage only,
                zone_name: Zone的名称 (1~256 characters)，仅OceanStor A80series storage only,
                raid_level: RAID level列表 (List<string>)。Options：RAID0, RAID1, RAID2, RAID3, RAID5, RAID6, RAID10, RAID50, RAID_TP。仅闪存存储、OceanDisk、OceanStor A800Device support,
                disk_pool_id: Disk pool或Disk poolID (1~64 characters)。所属Disk pool支持闪存设备，所属Disk pool支持Pacific、A310设备，OceanStor A800Device support,
                disk_pool_name: Disk pool或Disk pool名称 (1~256 characters),
                media_type: Storage pool主存类型。Options：sas_disk (SAS盘), sata_disk (SATA盘), ssd_card (SSD卡&NVMe SSD), ssd_disk (SSD盘)。仅OceanStor Pacific、OceanStor A310、OceanStor 100DDevice support,
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
    查询 HyperScale Storage pool列表

    Args:
        client: DME API client
        raw_id: Storage poolon the storage deviceID（可选，1~64 characters），supports exact search
        name: HyperScaleStorage pool name（可选，1~256 characters），supports fuzzy search
        local_pool_id: HyperScaleStorage pool下本地Storage pool ID（可选，0~64 characters），支持过滤指定本地Storage pool关联的HyperScaleStorage pool
        health_status: Health status(Optional). Options：normal (正常), faulty (故障), degraded (降级)
        running_status: Running status(Optional). Options：pre_copy (预拷贝), rebuilding (重构), online (在线), offline (离线), balancing (正在均衡), initializing (Initializing), deleting (Deleting)
        storage_id: Storage device ID（可选，0~64 characters）
        description: HyperScaleStorage pool描述（可选，0~256 characters）
        page_no: Page number（可选，1~10000，默认 1）
        page_size: Page size（可选，1~1000，默认 20）
        sort_key: Sort field(Optional). Options：raw_id (ID), total_capacity (Storage poolTotal capacity), consumed_capacity (Used capacity), capacity_usage (容量利用率), free_capacity (Free capacity), subscribed_capacity_percentage (订阅率)
        sort_dir: Sort direction(Optional). Options：asc (升序), desc (降序)

    Returns:
        {
            total: HyperScaleStorage poolTotal count (int32),
            data: HyperScale storage pool list (List<HyperScalePoolInfo>)。参数格式如下：[{
                id: HyperScaleStorage pool ID (1~64 characters),
                raw_id: Storage poolon the storage deviceID (1~64 characters),
                name: HyperScaleStorage pool name (1~256 characters),
                description: HyperScaleStorage pool描述 (1~256 characters),
                storage_id: Storage device ID (1~64 characters),
                storage_ip: Storage device IP (1~255 characters),
                storage_name: Storage device name (1~127 characters),
                health_status: Health status。Options：normal (正常), faulty (故障), degraded (降级),
                running_status: Running status. Options：pre_copy (预拷贝), rebuilding (重构), online (在线), offline (离线), balancing (正在均衡), initializing (Initializing), deleting (Deleting),
                total_capacity: Total capacity，单位MB (number),
                consumed_capacity: Used capacity，单位MB (number),
                capacity_usage: 容量利用率 (number),
                free_capacity: Free capacity，单位MB (number),
                subscribed_capacity_percentage: 订阅率 (number),
                subscribed_capacity: 总订阅容量，单位MB (number),
                used_subscribed_capacity: 已使用订阅容量，单位MB (number),
                redundancy_strategy: 冗余策略。Options：disk (盘级冗余), distributed_ec (分布式EC),
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
        storage_id: Storage deviceid（可选，1~64 characters），支持过滤
        raw_id: 节点on the storage deviceID（可选，1~64 characters）
        storage_name: Storage deviceName (Optional,1~255 characters），支持过滤
        name: 节点Name (Optional,1~256 characters），supports fuzzy search（case-insensitive）
        ids: 节点ID列表（可选，List<string>，max array members：100）
        mgmt_ip: 节点管理IP地址（可选，1~256 characters），supports fuzzy search（case-insensitive）
        frame_number: 机柜/机架号（可选，1~256 characters），supports fuzzy search（case-insensitive）
        slot_number: 槽位/机架内Slot number（可选，1~256 characters），supports fuzzy search（case-insensitive）
        status: Node status(Optional). Options：UNKNOWN (未知), NORMAL (正常), FAULT (故障), PRE_FAIL (即将故障), PARTIALLY_DAMAGED (部分损坏), DEGRADED (降级), BAD_SECTORS_FOUND (有坏块), BIT_ERRORS_FOUND (有误码), CONSISTENT (一致), INCONSISTENT (不一致), BUSY (繁忙), NO_INPUT (无输入), LOW_BATTERY (电量不足), SINGLE_LINK_FAULT (单链路故障)
        roles: 节点Role list（可选，List<string>，max array members：10). Options：management (管理), storage (存储), compute (VBS计算), replication (复制), paxos (控制), dpc_compute (DPC计算)
        page_no: Page number（可选，1~10000，默认 1）
        page_size: Page size（可选，1~1000，默认 20）
        sort_key: Sort field(Optional). Options：name (Node name), mgmt_ip (节点管理IP地址)
        sort_dir: Sort direction(Optional). Options：asc (升序), desc (降序)

    Returns:
        {
            total: 节点的count (integer),
            nodes: Node list (List<StorageNodeBaseInfo>)。参数格式如下：[{
                id: 节点id (1~64 characters),
                name: Node name (1~255 characters),
                raw_id: 节点on the storage deviceID (1~64 characters),
                mgmt_ip: 节点管理IP地址 (1~255 characters),
                status: Node status (1~255 characters)。Options：UNKNOWN (未知), NORMAL (正常), FAULT (故障), PARTIALLY_DAMAGED (部分损坏),
                node_model: 节点型号 (1~255 characters)。例如：DataTurbo，OceanStor Pacific，RH5288 V3,
                frame_number: 机柜/机架号 (1~255 characters),
                slot_number: 槽位/机架内Slot number (1~255 characters),
                roles: 节点Role list (List<string>)。Options：management (管理), storage (存储), compute (VBS计算), replication (复制), paxos (控制), dpc_compute (DPC计算),
                node_sn: Serial number信息 (1~255 characters),
                storage_id: Storage deviceid (1~64 characters),
                storage_name: Storage device名称 (1~255 characters),
                eos_time: 存储EOS时间 (int64)，格林威治时间1970year(s)01month(s)01日00时00分00second(s)起至现在的总毫second(s)数,
                installation_status: 存储软件安装状态。Options：installed (已安装存储软件), not_installed (未安装存储软件),
                ip_address_list: Node IP address list (List<StorageNodeIpInfo>)。参数格式如下：[{
                    ip_address: Node IP地址 (1~256 characters),
                    usage: Node IP地址用途列表 (List<string>)。Options：storage_frontend (存储前端网络IP), storage_backend (存储后端网络IP), management_external_float (管理外部网络浮动IP), management_internal_float (管理内部网络浮动IP), management_external (管理外部网络IP), management_internal (管理内部网络IP), replication (复制网络IP), quorum (仲裁网络IP), iscsi (ISCSI网络IP),
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
    查询Storage devicePower supply详情信息，only supportsOceanStor A800存储。

    Args:
        client: DME API client
        storage_id: Storage deviceID（Required，1~64 characters）
        health_status: Health status(Optional). Options：unknown (未知), normal (正常), faulty (故障), inconsistent (不一致), no_input (无输入)
        running_status: Running status(Optional). Options：unknown (未知), normal (正常), running (运行), online (在线), offline (离线)
        power_type: Power supply类型(Optional). Options：dc (直流Power supply), ac (交流Power supply), hv (高压直流Power supply)
        power_mode: Power supply模式(Optional). Options：balanced_power (均衡Power supply), active_power (主Power supply), standby_power (备Power supply)
        location: 位置（可选，1~256 characters），supports fuzzy match
        model: 型号（可选，1~256 characters），supports fuzzy match
        sn: Serial number（可选，1~256 characters），supports fuzzy match
        enclosure_name: 所属EnclosureName (Optional,1~256 characters），supports fuzzy match
        zone_id: Zone ID（可选，1~64 characters），仅OceanStor A800series storage only
        page_no: Page number（可选，1~2147483647，默认 1）
        page_size: Page size（可选，1~1000，默认 20）

    Returns:
        {
            total: Power supply的count (int32),
            storage_powers: Power list (List<StoragePowerInfo>)。参数格式如下：[{
                name: 名称 (1~255 characters),
                location: 位置 (1~255 characters),
                health_status: Health status。Options：unknown (未知), normal (正常), faulty (故障), inconsistent (不一致), no_input (无输入),
                running_status: Running status. Options：unknown (未知), normal (正常), running (运行), online (在线), offline (离线),
                power_type: Power supply类型。Options：dc (直流Power supply), ac (交流Power supply), hv (高压直流Power supply),
                model: 型号 (1~255 characters),
                sn: Serial number (1~255 characters),
                manufacturer: 生产厂商 (1~255 characters),
                enclosure_name: Enclosure name (1~255 characters),
                production_date: 生产日期 (1~255 characters),
                version: 版本 (1~255 characters),
                bom_code: Power supply模块BOM编码 (1~255 characters),
                power_mode: Power supply模式。Options：balanced_power (均衡Power supply), active_power (主Power supply), standby_power (备Power supply),
                zone_name: Zone名称 (1~255 characters)，仅OceanStor A800series storage only,
                zone_id: Zone ID (1~255 characters)，仅OceanStor A800series storage only,
                zone_ip: Zone IP地址 (1~255 characters)，仅OceanStor A800series storage only,
                storage_id: Storage deviceID (1~64 characters),
                storage_name: Storage device名称 (1~128 characters),
                storage_ip: Storage deviceIP地址 (1~32 characters),
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
    查询Storage device功率数据

    Args:
        client: DME API client
        start_time: Start time戳（Required，13位数字毫second(s)Timestamp，正则 ^([0-9]){13}$）
        end_time: End time戳（Required，13位数字毫second(s)Timestamp，正则 ^([0-9]){13}$）
        storage_ids: 存储ID列表（Required，List<string>，max array members：300）
        time_granularity: Time granularity（Required). Options：HOUR (hour(s)), DAY (day(s)), MONTH (month(s))

    Returns:
        {
            storage_power_list: Storage power list (List<StoragePower>)。参数格式如下：[{
                storage_id: 存储ID,
                power: 存储功率，单位千瓦 (number),
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
    Modify storage device（only supportsModify recorded offlineStorage device信息）

    Args:
        client: DME API client。
        storage_id: Storage device ID（Required）。
        name: Device name (可选, 1~256 characters)。can only contain half-width letters、半角数字、"_"、"-"、"."、中文字符。
        ip: Device IP地址 (可选, 0~128 characters, 支持IPv4与IPv6格式, 也可为空string)。
        vendor: 厂商 (可选, 0~128 characters)。
        model: Product model (可选, 0~128 characters)。
        version: 版本信息 (可选, 0~64 characters)。
        patch_version: Patch version info (可选, 0~64 characters)。
        location: 设备位置 (可选, 0~512 characters)。
        maintenance_start: 维护Start time (可选, 格式是毫second(s)级Timestamp)。must appear with warranty expiration time and value must be less。
        maintenance_overtime: Warranty expiration time (可选, 格式是毫second(s)级Timestamp)。需要和维护Start timemust appear together and value greater thanStart time。
        total_capacity: 裸容量 (可选, -1~2147483647, 单位MB)。Storage devicesum of all disk physical capacities，-1表示无裸容量。
        total_effective_capacity: 可得容量 (可选, -1~2147483647, 单位MB)。Storage device可写入的User data总量，-1表示无可得容量。
        total_pool_capacity: Available capacity (可选, -1~2147483647, 单位MB)。Storage device实际可用的硬盘物理空间（扣除RAID、元数据等消耗），-1表示无Available capacity。
        used_capacity: Used capacity (可选, -1~2147483647, 单位MB)。Storage device中所有Storage pool的已使用容量之和，-1表示无Used capacity。
        free_capacity: Free capacity (可选, -1~2147483647, 单位MB)。Storage device的Available capacity与Used capacity的差值，-1表示无Free capacity。
        subscription_capacity: 订阅容量 (可选, -1~2147483647, 单位MB)。Storage device中所有Storage pool的订阅容量之和，-1表示无已订阅容量。
        tag_ids: 标签ID列表 (Optional, string, 0~512 characters)。数组格式string，最多支持10个标签，空数组代表Remove storage device关联的所有标签。

    Returns:
        无
    """
    if not storage_id:
        raise ValueError("storage_id 是Required参数")

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
    # modify API returns empty response，返回空字典表示成功
    return response if response else {}


def app_type_list(client: DMEAPIClient, storage_id: str, 
                 create_type: int = None, template_type: int = None, 
                 pool_id: str = None) -> dict:
    """
    QueryStorage device的应用类型
    
    仅 Dorado 类型Device support。
    
    Args:
        client: DME API client。
        storage_id: Storage device id (1~36 characters, 满足uuid格式)。
        create_type: 创建类型 (可选, 0~1)。Options：0 (系统预置), 1 (用户定义)。returns all types if not provided。
        template_type: 应用类型分类 (可选, 0~1)。Options：0 (LUN类型), 1 (NAS类型)。不传默认LUN类型。
        pool_id: Storage poolid (可选, 1~64 characters, 字母和数字)。
    
    Returns:
        应用类型信息，包含 datas 列表，每个元素包含 id, name, block_size, 
        enable_compress, enable_dedup, create_type 等字段
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
    QueryStorage devicecontroller info
    
    query storage deviceControllerList info。
    
    Args:
        client: DME API client
        storage_id: Storage device ID（Required，1~36  characters，UUID 格式或 32 位十六进制）
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含 total 和 controllers 字段
        - total: ControllerTotal count
        - controllers: Controller列表，包含 id, name, status, type 等信息
    """
    url = "/rest/storagemgmt/v1/storages/{storage_id}/controllers"
    
    response = client.get(url, params={"storage_id": storage_id})
    return response


def disk_domain_list(client: DMEAPIClient, storage_id: str = None, page_no: int = 1,
                   page_size: int = 20) -> dict:
    """
    Batch query disk pools

    Args:
        client: DME API client
        storage_id: Storage device ID（可选，1~64  characters），支持过滤
        page_no: Page number（可选，1~2147483647，默认 1）
        page_size: Page size（可选，1~1000，默认 20）

    Returns:
        {
            total: Disk poolcount (int32),
            disk_pools: Disk pool list (List<DiskPoolInfo>)。参数格式如下：[{
                    id: Disk poolid (1~64 characters),
                    raw_id: Disk poolon the deviceid (1~64 characters),
                    name: Disk pool名称 (1~128 characters),
                    running_status: Running status. Options：online (在线), offline (离线), pre_copy (预拷贝), reconstruction (重构), balancing (正在均衡), initializing (Initializing), deleting (Deleting), unknown (未知),
                    health_status: Health status。Options：normal (正常), fault (故障), degraded (降级), unknown (未知),
                    total_capacity: 总可用裸容量，单位MB (number),
                    spare_capacity: 总热备裸容量，单位MB (number),
                    used_capacity: 已分配裸容量，单位MB (number),
                    used_spare_capacity: 已用热备裸容量，单位MB (number),
                    free_capacity: Free capacity，单位MB (number),
                    storage_id: Storage deviceid (1~64 characters),
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
    Batch query分布式Storage device的Disk pool。only supportsOceanStor Pacific和OceanStor A310存储。

    Args:
        client: DME API client
        storage_id: Storage deviceid (Optional, string, 1~64 characters)。非OceanStor Pacific或A310设备会报参数错误
        page_no: Page number (Optional, int32, 1~2147483647)。Default：1
        page_size: Page size (Optional, int32, 1~1000)。Default：20

    Returns:
        {
            total: Total count (int32),
            disk_pools: Disk pool list。参数格式如下：[{
                id: Disk poolID (string),
                name: Disk pool名称 (string),
                status: 状态 (string),
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
    Batch query enclosures信息

    Args:
        client: DME API client
        page_no: Page number（可选，1~2147483647，默认 1）
        page_size: Page size（可选，1~1000，默认 20）
        storage_id: Storage deviceID（可选，1~64 characters）
        name: Name (Optional,1~256 characters），supports fuzzy match
        location: 位置（可选，1~256 characters），supports fuzzy match
        health_status: Health status列表（可选，List<string>，max array members：3). Options：unknown (未知), normal (正常), faulty (故障)
        zone_name: ZoneName (Optional,1~255 characters），仅OceanStor A800series storage only，supports fuzzy match
        zone_id: Zone ID列表（可选，List<string>，max array members：100），仅OceanStor A800series storage only
        running_status: Running status列表（可选，List<string>，max array members：7). Options：unknown (未知), normal (正常), running (运行), sleep_in_high_temperature (高温休眠), online (在线), offline (离线)
        power_mode: Power supply模式列表（可选，List<string>，max array members：2). Options：load_balance (Load balancing mode), active_standby_power (Primary/standby power mode)
        esn: EnclosureSerial number（可选，1~256 characters），supports fuzzy match
        mac: MAC地址（可选，1~256 characters），supports fuzzy match
        sort_key: Sort field(Optional). Options：temperature (温度)
        sort_dir: Sort direction(Optional). Options：asc (升序), desc (降序)。默认按升序返回

    Returns:
        {
            total: Enclosurecount (integer),
            data: Enclosure list (List<EnclosureItem>)。参数格式如下：[{
                    id: EnclosureID (1~64 characters),
                    raw_id: Enclosure在Storage device上ID (1~64 characters),
                    name: 名称 (1~256 characters),
                    model: 型号 (1~32 characters)。Options：0 (BMCController enclosure), 1 (2U 双控 6Gbit/s SAS 12盘位 3.5inch controller enclosure), 2 (2U 双控 6Gbit/s SAS 24盘位 2.5inch controller enclosure), 16 (2U 6Gbit/s SAS 12盘位 3.5inch disk enclosure), 17 (2U SAS 24盘级联框), 18 (4U 6Gbit/s SAS 24盘位 3.5inch disk enclosure), 19 (4U FC 24盘级联框), 20 (1U PCIe数据Switch), 21 (4U 6Gbit/s SAS 75盘位 3.5inch disk enclosure), 22 (SVP), 23 (2U 双控 6Gbit/s SAS 12盘位 3.5inch controller enclosure), 24 (2U 6Gbit/s SAS 25盘位 2.5inch disk enclosure), 25 (4U 6Gbit/s SAS 24盘位 3.5inch disk enclosure), 26 (2U 双控 6Gbit/s SAS 25盘位 2.5inch controller enclosure), 37 (2U 双控 6Gbit/s SAS 12盘位 3.5inch controller enclosure), 38 (2U 双控 6Gbit/s SAS 25盘位 2.5inch controller enclosure), 39 (4U 12Gbit/s SAS 75盘位 3.5inch disk enclosure), 40 (2U 双控 12Gbit/s SAS 25盘位 2.5inch controller enclosure), 65 (2U 12Gbit/s SAS 25盘位 2.5inch disk enclosure), 66 (4U 12Gbit/s SAS 24盘位 3.5inch disk enclosure), 67 (2U SAS 25盘位 2.5inch disk enclosure), 69 (4U SAS 24盘位 3.5inch disk enclosure), 96 (3U 双控Controller enclosure), 97 (6U 四控Controller enclosure), 98 (2U SSD 25盘级联框), 99 (2U 双控 12Gbit/s NVMe 25盘位 2.5inch controller enclosure), 101 (2U SSD NVMe 25盘位 2.5inch disk enclosure), 112 (4U 四控Controller enclosure), 113 (2U 双控 SAS 25盘位 2.5inch controller enclosure), 114 (2U 双控 SAS 12盘位 3.5inch controller enclosure), 115 (2U 双控 NVMe 36盘位Controller enclosure), 116 (2U 双控 SAS 25盘位 2.5inch controller enclosure), 117 (2U 双控 SAS 12盘位 3.5inch controller enclosure), 118 (2U SAS 25盘位 2.5英寸智能Disk enclosure), 119 (2U SAS 12盘位 3.5英寸智能Disk enclosure), 120 (2U NVMe 36盘位智能Disk enclosure), 122 (2U 双控 NVMe 25盘位 2.5inch controller enclosure), 132 (4U 双控 4盘位2.5英寸 6盘位3.5英寸 Controller enclosure), 133 (4U 双控 NVMe 12盘位 2.5英寸 Controller enclosure), 135 (4U 双控 10盘位 2.5inch controller enclosure), 143 (8U NVME 双控 64盘位 2.5英寸 Controller enclosure),
                    height: 高度，单位U (integer),
                    location: Enclosure的位置 (1~128 characters),
                    logic_type: 类型。Options：disk_enclosure (Disk enclosure), controller_enclosure (Controller enclosure), data_switch (数据Switch), management_switch (管理Switch), management_server (管理Server),
                    health_status: Health status。Options：unknown (未知), normal (正常), faulty (故障),
                    running_status: Running status. Options：unknown (未知), normal (正常), running (运行), sleep_in_high_temperature (高温休眠), online (在线), offline (离线), abnormal (异常),
                    storage_id: Storage deviceID (1~64 characters),
                    storage_name: Storage device名称 (1~128 characters),
                    storage_ip: Storage deviceIP地址 (1~32 characters),
                    storage_sn: Storage deviceSerial number (1~64 characters),
                    storage_location: Storage device的位置 (0~512 characters),
                    zone_name: Zone名称 (0~512 characters)，仅OceanStor A800series storage only,
                    zone_ip: Zone IP地址 (1~128 characters)，仅OceanStor A800series storage only,
                    zone_id: Zone ID (0~512 characters)，仅OceanStor A800storage support,
                    esn: EnclosureSerial number (0~512 characters),
                    mac: MAC地址 (0~512 characters),
                    power_mode: Power supply模式。Options：load_balance (Load balancing mode), active_standby_power (Primary/standby power mode),
                    bar_code: 条形码 (0~256 characters),
                    board_type: 单板类型 (0~128 characters),
                    description: 描述 (0~1024 characters),
                    temperature: 温度，单位°C (0~128 characters),
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
    Batch query存储侧Initiatorobject

    Batch query存储侧的Initiatorobject列表。

    Args:
        client: DME API client
        page_size: Items per page (Optional, 1~1000, default 100)
        page_no: Page number (可选, min1, 默认1)
        raw_id: InitiatorWWPN/IQN/NQN (可选, 0~256 characters, supports fuzzy match)
        alias: Initiator alias (可选, 0~256 characters, supports fuzzy match)
        status: Initiator状态 (可选)。Options：unknown (未知), online (在线), offline (离线)
        associated_host_name: Initiator关联Host name (可选, 0~256 characters, supports fuzzy match)
        associated_host_id: Initiator关联Host ID (可选, 0~64 characters; 空字段查询未添加到主机的Initiator)
        multipath_type: Third-party multipath策略 (可选, 仅针对非Dorado V6产品)。Options：default (默认), third_party (Third-party multipath)
        protocol: Initiator type (可选)。Options：fc, iscsi, nvme_over_roce, sas, nvme_over_fabric, unknown
        support_provisioning: supports发放 (可选)。Options：true, false
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
    Batch deleteStorage device的Initiatorobject

    Args:
        client: DME API client
        initiator_ids: Initiator ID 列表（Required，1~100 个）
        task_remarks: Task remark(Optional, max 1024 字符）

    Returns:
        任务 ID
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
    修改存储侧Initiatorobject

    修改Initiator，该操作会Modify storage device上指定的Initiator。

    Args:
        client: DME API client
        initiator_id: Initiator ID (Required)
        vstore_id: Tenant ID (Optional, 1~64 characters; 设备为OceanStor V300R006C30/V500R007C20/Dorado 6.1.3及以上effective when)
        alias: Initiator alias (可选, 0~31 characters, supports alphanumeric._-and Chinese characters)
        multi_path: ModifyMultiPathRequestParamobject (可选; 设备为OceanStor V300R003C20/V500R007C20/Dorado V300R001C01及以上支持)。属性格式如下：{
                multi_path_type: InitiatorMultipath type (可选)。Options：default (默认), third_party (Third-party multipath),
                path_type: Initiator路径类型 (conditionally required, 当multi_path_type为third_partyrequired when)。Options：optimal_path (优选路径), non_optimal_path (非优选路径),
                failover_mode: Initiator切换模式 (conditionally required, 当multi_path_type为third_partyrequired when)。Options：early_version_alua, common_alua, alua_not_used, special_alua,
                special_mode_type: Special mode type (可选, effective when failover mode is special)。Options：0 (特殊模式0), 1 (特殊模式1), 2 (特殊模式2), 3 (特殊模式3)
             }

    Returns:
        任务 ID
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
    QueryStorage device本地Auth user info

    Args:
        client: DME API client
        storage_id: Storage device ID（Required，1~36  characters）
        vstore_raw_id: 本地auth userTenanton device ID（可选）
        name: 本地Auth user name，supports fuzzy search（可选）
        page_no: Page number，默认 1（可选）
        page_size: Page size，默认 20（可选）

    Returns:
        本地Auth user info list，包含 total 和 local_users
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
        name: 本地Auth user name (1~255 characters, Required)
        description: 本地Auth user description (1~255 characters, Optional)
        password: 本地Auth user password (1~255 characters, Required)
        primary_group_raw_id: 本地auth user所归属的User groupon device ID (1~64 characters, Required)
        group_names: 创建的本地auth user所属的临时User group名称列表 (List<string>, min array members: 0, max array members: 31, Optional)
        vstore_id: 本地auth user所属的租户 ID (1~64 characters, Optional。conditionally required，当创建的本地required when auth user belongs to tenant)

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
    CreateStorage device UNIX auth user

    Args:
        client: DME API client
        storage_id: 创建 UNIX auth userStorage device ID (1~36 characters, Required)
        name: UNIX Auth user name (1~255 characters, Required)
        raw_id: UNIX Auth user on device ID (int64, 0~4294967295, Optional)
        description: UNIX Auth user description (1~255 characters, Optional)
        password: UNIX Auth user password (1~255 characters, Optional)
        status_enabled: UNIX Auth user status (boolean, Optional)。Options：true (启动), false (锁定)
        primary_group_raw_id: 创建的 UNIX auth user所归属的User groupon device ID (1~64 characters, Required)
        vstore_raw_id: UNIX Auth user tenant on device ID (1~64 characters, Optional。conditionally required，当创建的 UNIX required when auth user belongs to tenant)

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
    CreateStorage device Windows auth user

    Args:
        client: DME API client
        storage_id: 创建 Windows auth userStorage device ID (1~36 characters, Required)
        name: Windows Auth user name (1~255 characters, Required)
        raw_id: Windows Auth user on device ID (int64, 1000~4294967295, Optional)
        description: Windows Auth user description (1~255 characters, Optional)
        password: Windows Auth user password (1~255 characters, Required)
        status_enabled: Windows Auth user status (boolean, Optional)。Options：true (启用), false (锁定)
        vstore_raw_id: 创建的 Windows Auth user tenant on device ID (1~64 characters, Optional。conditionally required，当 Windows required when auth user belongs to tenant)

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
    QueryStorage device UNIX Auth user info

    Args:
        client: DME API client
        storage_id: Storage device ID（Required，1~36  characters）
        vstore_raw_id: UNIX auth userTenanton device ID（可选）
        name: UNIX Auth user name，supports fuzzy search（可选）
        page_no: Page number，默认 1（可选）
        page_size: Page size，默认 20（可选）

    Returns:
        UNIX Auth user info list，包含 total 和 unix_users
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
    QueryStorage device Windows Auth user info

    Args:
        client: DME API client
        storage_id: Storage device ID（Required，1~36  characters）
        vstore_raw_id: Windows auth userTenanton device ID（可选）
        name: Windows Auth user name，supports fuzzy search（可选）
        page_no: Page number，默认 1（可选）
        page_size: Page size，默认 20（可选）

    Returns:
        Windows Auth user info list，包含 total 和 windows_users
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
    QueryStorage device本地Auth user group info

    Args:
        client: DME API client
        storage_id: Storage device ID（Required，1~36  characters）
        vstore_raw_id: 本地认证User groupTenanton device ID（可选）
        name: 本地Auth user group name，supports fuzzy search（可选）
        page_no: Page number，默认 1（可选）
        page_size: Page size，默认 20（可选）

    Returns:
        本地Auth user group info list，包含 total 和 local_user_groups
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
    QueryStorage device UNIX Auth user group info

    Args:
        client: DME API client
        storage_id: Storage device ID（Required，1~36  characters）
        vstore_raw_id: UNIX 认证User groupTenanton device ID（可选）
        name: UNIX Auth user group name，supports fuzzy search（可选）
        page_no: Page number，默认 1（可选）
        page_size: Page size，默认 20（可选）

    Returns:
        UNIX Auth user group info list，包含 total 和 unix_user_groups
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
    QueryStorage device Windows Auth user group info

    Args:
        client: DME API client
        storage_id: Storage device ID（Required，1~36  characters）
        vstore_raw_id: Windows 认证User groupTenanton device ID（可选）
        name: Windows Auth user group name，supports fuzzy search（可选）
        page_no: Page number，默认 1（可选）
        page_size: Page size，默认 20（可选）

    Returns:
        Windows Auth user group info list，包含 total 和 windows_user_groups
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
    Batch query QoS 策略

    Args:
        client: DME API client
        storage_id: Storage device ID（Required）
        name: QoS 策略Name (Optional,1~256 字符）
        raw_id: QoS 策略device side ID（可选）
        enable_status: 激活状态（可选，true/false）
        running_status: Running status（可选，running/inactive/waiting）
        zone_id: 所属 ZONE 的 ID（可选）
        resource_type_list: 控制的Resource type列表（可选，file_system/vstore/none）
        vstore_id: Tenant ID（可选）
        vstore_name: Tenant名称（可选）
        alarm_status: Alarm status（可选，normal/event/alarm/invalid）
        io_policy_type: IO Policy type（可选，total_perf_upper_limit/read_or_write_upper_limit）
        page_no: 页码（可选，默认 1）
        page_size: 每页count（可选，默认 10，最大 1000）
        sort_key: Sort field（可选，name/raw_id）
        sort_dir: Sort method（可选，asc/desc）
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
    Query QoS 策略详情

    Args:
        client: DME API client
        qos_policy_id: QoS 策略 ID（Required）
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
    创建 QoS 策略

    创建一个新的 QoS 策略，可以配置性能限制、告警参数和定时调度。

    Args:
        client: DME API client
        name: QoS Policy name（Required，1~31 字符）
        storage_id: Storage device ID（Required）
        resource_type: 控制的Resource type（Required，file_system/vstore）
        resource_ids: 控制的资源 ID 列表（Required，数组 1~512 个成员）
        description: 描述（可选，1~255 字符）
        zone_id: 所属 ZONE 的 ID（可选，A series storageRequired）
        vstore_id: Tenant ID（可选，resource_type 为 file_system 时Required）
        enable_status: 激活状态（可选，enable/disable，默认 enable）
        io_policy_type: IO Policy type（可选，total_perf_upper_limit/read_or_write_upper_limit）
        min_bandwidth: Min bandwidth MB/s（可选）
        max_bandwidth: Max bandwidth MB/s（可选）
        burst_bandwidth: 突发带宽 MB/s（可选，需大于 max_bandwidth）
        min_iops: 最小 IOPS（可选）
        max_iops: 最大 IOPS（可选）
        burst_iops: 突发 IOPS（可选，需大于 max_iops）
        burst_time: 最大突发durationsecond(s)（可选，1~999999999）
        latency: IO 时延指标微second(s)（可选，500/1500）
        max_read_bandwidth: 最大Read bandwidth MB/s（可选）
        max_write_bandwidth: 最大Write bandwidth MB/s（可选）
        burst_read_bandwidth: 突发Read bandwidth MB/s（可选）
        burst_write_bandwidth: 突发Write bandwidth MB/s（可选）
        max_read_iops: 最大读 IOPS（可选）
        max_write_iops: 最大写 IOPS（可选）
        burst_read_iops: 突发读 IOPS（可选）
        burst_write_iops: 突发写 IOPS（可选）
        alarm_switch: 告警开关（可选，on/off）
        alarm_level: Alarm severity（可选，event/alarm）
        alarm_threshold: 告警threshold%（可选，0~100）
        resume_threshold: 恢复threshold%（可选，0~100）
        schedule_policy: Scheduling policy（可选，once/daily/weekly）
        schedule_start_date: Effective start date（可选，yyyy-MM-dd）
        start_time: 生效Start time（可选，hh:mm）
        duration: 生效durationsecond(s)（可选，1800~86400）
        weekly_days: week(s)Scheduling policy（可选，[0-6] 对应week(s)日到week(s)六）
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
    修改 QoS 策略

    修改现有 QoS 策略的配置。

    Args:
        client: DME API client
        qos_policy_id: QoS 策略 ID（Required）
        name: QoS Policy name（可选）
        description: 描述（可选）
        io_policy_type: IO Policy type（可选）
        min_bandwidth: Min bandwidth MB/s（可选）
        max_bandwidth: Max bandwidth MB/s（可选）
        burst_bandwidth: 突发带宽 MB/s（可选）
        min_iops: 最小 IOPS（可选）
        max_iops: 最大 IOPS（可选）
        burst_iops: 突发 IOPS（可选）
        burst_time: 最大突发durationsecond(s)（可选）
        latency: IO 时延指标微second(s)（可选）
        max_read_bandwidth: 最大Read bandwidth MB/s（可选）
        max_write_bandwidth: 最大Write bandwidth MB/s（可选）
        burst_read_bandwidth: 突发Read bandwidth MB/s（可选）
        burst_write_bandwidth: 突发Write bandwidth MB/s（可选）
        max_read_iops: 最大读 IOPS（可选）
        max_write_iops: 最大写 IOPS（可选）
        burst_read_iops: 突发读 IOPS（可选）
        burst_write_iops: 突发写 IOPS（可选）
        alarm_switch: 告警开关（可选）
        alarm_level: Alarm severity（可选）
        alarm_threshold: 告警threshold%（可选）
        resume_threshold: 恢复threshold%（可选）
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
    删除 QoS 策略

    删除一个或多个 QoS 策略。

    Args:
        client: DME API client
        qos_policy_ids: QoS 策略 ID 列表（Required，1~100 个）
    """
    url = "/rest/storagepolicy/v1/qos/delete"

    payload = {
        'ids': qos_policy_ids
    }

    response = client.post(url, body=payload)
    return response


def qos_activate(client: DMEAPIClient, qos_policy_ids: list) -> dict:
    """
    批量激活 QoS 策略

    激活一个或多个 QoS 策略。

    Args:
        client: DME API client
        qos_policy_ids: QoS 策略 ID 列表（Required）
    """
    url = "/rest/storagepolicy/v1/qos/active"

    payload = {
        'qos_ids': qos_policy_ids
    }

    response = client.post(url, body=payload)
    return response


def qos_deactivate(client: DMEAPIClient, qos_policy_ids: list) -> dict:
    """
    Batch deactivate QoS 策略

    Deactivate一个或多个 QoS 策略。

    Args:
        client: DME API client
        qos_policy_ids: QoS 策略 ID 列表（Required）
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

    将一个或多个资源associated with QoS 策略。

    Args:
        client: DME API client
        qos_policy_id: QoS 策略 ID（Required）
        resource_ids: 资源 ID 列表（Required）
        resource_type: Resource type（Required，file_system/vstore）
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

    将资源从 QoS 策略解关联。

    Args:
        client: DME API client
        qos_policy_id: QoS 策略 ID（Required）
        resource_ids: 资源 ID 列表（Required）
        resource_type: Resource type（Required）
    """
    url = "/rest/storagepolicy/v1/qos/{qos_policy_id}/resources/unassociate"

    payload = {
        'resource_ids': resource_ids,
        'resource_type': resource_type
    }

    response = client.post(url, params={"qos_policy_id": qos_policy_id})
    return response


# ============ 存储Logic port (logic_port) subtopic functions ============


def logic_port_list(client: DMEAPIClient, storage_id: str = None, vstore_raw_id: str = None,
                    zone_raw_id: str = None, scope: str = None, page_no: int = 1,
                    page_size: int = 100) -> dict:
    """
    query storage deviceLogic port list

    Args:
        client: DME API client
        storage_id: Storage device ID（可选，1~64 characters）
        vstore_raw_id: vStoreon the storage deviceid（可选，1~64 characters）
        zone_raw_id: Zoneon the deviceID（可选，1~64 characters），仅OceanStor A800series storage only
        scope: 范围(Optional). Options：hyperscale (全局), default (本地)。仅OceanStor A800series storage only
        page_no: Page number（可选，1~10000，默认 1）
        page_size: Page size（可选，1~1000，默认 100）

    Returns:
        {
            total: Logic port的count (integer),
            logic_ports: Logic port list (List<StorageLogicPortResp>)。参数格式如下：[{
                id: 逻辑Port ID (1~255 characters),
                raw_id: Logic porton the storage deviceID (1~255 characters),
                name: 逻辑Port name (1~255 characters),
                running_status: Running status. Options：UNKNOWN (未知), NORMAL (正常), RUNNING (运行), LINK_UP (已连接), LINK_DOWN (未连接), TO_BE_RECOVERED (待恢复), INITIALIZING (Initializing), STANDBY (待工作), POWERING_ON (正在上电), POWERED_OFF (已下电), POWER_ON_FAILED (上电失败),
                operational_status: Active status。Options：ACTIVATED (激活), NOT_ACTIVATED (inactive),
                mgmt_ip: ipv4地址 (1~255 characters),
                ipv4_gateway: Logic port gatewayIP地址(IPV4) (1~64 characters),
                ipv4_mask: Logic portIPNetmask(IPV4) (1~64 characters),
                mgmt_ipv6: ipv6地址 (1~255 characters),
                ipv6_mask: Logic portIPNetmask(IPV6) (1~128 characters),
                ipv6_gateway: Logic port gatewayIP地址(IPV6) (1~128 characters),
                home_port_raw_id: 父端口on the storage deviceID (1~255 characters),
                home_port_name: 父Port name (1~255 characters),
                home_port_type: 父Port type。Options：ETHERNET_PORT (Ethernet port andRoCE端口), BOND (绑定), VLAN (VLAN), VIP (VIP), SIP (SIP), IB (IB),
                home_controller_raw_id: Storage deviceon primary controllerID (1~256 characters),
                current_port_raw_id: Logic portCurrent physical porton the storage deviceID (1~255 characters),
                current_port_name: Logic portcurrent physicalPort name (1~255 characters),
                role: 端口角色 (1~10 characters)。Options：0 (未知), 1 (管理), 2 (数据), 3 (管理+数据), 4 (复制), 6 (currently meaningless), 7 (currently meaningless), 8 (Client), 9 (VTEP), 10 (Health check), 11 (数据备份), 12 (系统管理), 100 (集群), 101 (集群间),
                ddns_status: 动态DNS开启状态。Options：INVALID (无效的), ENABLE (启用), DISABLED (未启用),
                failover_group_raw_id: Failover groupon the storage deviceID (1~255 characters),
                failover_group_name: Failover group名称 (1~255 characters),
                support_protocol: Logic portSupported data access protocols。Options：NONE (无协议), NFS (NFS协议), CIFS (CIFS协议), NFS_AND_CIFS (NFS和CIFS协议), NFS_OVER_RDMA (NFS over RDMA协议), iSCSI (iSCSI协议), FC/FCoE (FC/FCoE协议), NVME_OVER_ROCE (NVME over ROCE协议), BGP (BGP协议), DATA_TURBO (DataTurbo协议), DATA_TURBO_OVER_ROCE (DataTurbo over ROCE协议), S3 (S3协议), NFS_OVER_IB (NFS over IB协议), DATA_TURBO_OVER_IB (DataTurbo over IB协议), DATA_TURBO_OVER_ROCE_AND_TCP (DataTurbo over ROCE和TCP协议), OBJECT (S3协议), NAS_AND_OBJECT (NAS与object存储协议), KB_OVER_TCP (KnowledgeBase over TCP协议),
                logical_type: 逻辑类型。Options：SERVICE (主机端口/业务端口), MANAGEMENT (管理端口), MAINTENANCE (维护端口),
                listen_dns_query_enabled: 是否监听DNS查询请求 (1~255 characters)。Options：NO (关闭), YES (打开),
                management_access: Management access method (1~255 characters),
                vstore_raw_id: Logic port所属vStoreassigned on the deviceid (1~255 characters),
                vstore_name: Logic port所属vStore的名称 (1~255 characters),
                storage_id: Storage device ID (1~255 characters),
                storage_name: Storage device name (1~255 characters),
                zone_raw_id: Zoneon the deviceID (1~255 characters)，仅OceanStor A800series storage only,
                zone_id: Zone ID (1~64 characters)，仅OceanStor A800series storage only,
                zone_name: 所属zone名称 (1~255 characters)，仅OceanStor A800series storage only,
                zone_ip: 所属zone IP (1~255 characters),
                dns_zone_name: DNS Zone名称 (1~255 characters),
                current_port_type: Logic portPhysical port type。Options：ETHERNET_PORT (Ethernet port andRoCE端口), BOND (绑定), VLAN (VLAN), VIP (VIP), SIP (SIP), IB (IB),
                address_family: IPProtocol version。Options：IPv4 (IPv4), IPv6 (IPv6),
                can_failover: EnableIP地址漂移 (boolean)。Options：true, false,
                failback_mode: 回漂模式。Options：not_support (feature not supported), manual (手动), automatic (自动),
                scope: 范围。Options：hyperscale (全局), default (本地)。仅OceanStor A800series storage only,
                logicPortTags: Associated tag set (List<Tag>)。参数格式如下：[{
                    id: 标签的ID (1~32 characters),
                    tag_type_name: Tag type name (1~64 characters),
                    name: 标签名称 (1~128 characters),
                }, ...],
                manufacturer: 厂商 (1~32 characters),
                storage_model: 型号 (1~64 characters),
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
    query storage deviceLogic port详情

    Args:
        client: DME API client
        logic_port_id: Logic port的 ID（Required，1~64  characters，UUID 格式或 32 位十六进制）

    Returns:
        {
            id: 逻辑Port ID (1~255 characters),
            raw_id: Logic porton the storage deviceID (1~255 characters),
            name: 逻辑Port name (1~255 characters),
            running_status: Running status. Options：UNKNOWN (未知), NORMAL (正常), RUNNING (运行), LINK_UP (已连接), LINK_DOWN (未连接), TO_BE_RECOVERED (待恢复), INITIALIZING (Initializing), STANDBY (待工作), POWERING_ON (正在上电), POWERED_OFF (已下电), POWER_ON_FAILED (上电失败),
            operational_status: Active status。Options：ACTIVATED (激活), NOT_ACTIVATED (inactive),
            mgmt_ip: ipv4地址 (1~255 characters),
            ipv4_gateway: Logic port gatewayIP地址(IPV4) (1~64 characters),
            ipv4_mask: Logic portIPNetmask(IPV4) (1~64 characters),
            mgmt_ipv6: ipv6地址 (1~255 characters),
            ipv6_mask: Logic portIPNetmask(IPV6) (1~128 characters),
            ipv6_gateway: Logic port gatewayIP地址(IPV6) (1~128 characters),
            home_port_raw_id: 父端口on the storage deviceID (1~255 characters),
            home_port_name: 父Port name (1~255 characters),
            home_port_type: 父Port type。Options：ETHERNET_PORT (Ethernet port andRoCE端口), BOND (绑定), VLAN (VLAN), VIP (VIP), SIP (SIP), IB (IB),
            home_controller_raw_id: Storage deviceon primary controllerID (1~256 characters),
            current_port_raw_id: Logic portCurrent physical porton the storage deviceID (1~255 characters),
            current_port_name: Logic portcurrent physicalPort name (1~255 characters),
            role: 端口角色 (1~10 characters)。Options：0 (未知), 1 (管理), 2 (数据), 3 (管理+数据), 4 (复制), 6 (currently meaningless), 7 (currently meaningless), 8 (Client), 9 (VTEP), 10 (Health check), 11 (数据备份), 12 (系统管理), 100 (集群), 101 (集群间),
            ddns_status: 动态DNS开启状态。Options：INVALID (无效的), ENABLE (启用), DISABLED (未启用),
            failover_group_raw_id: Failover groupon the storage deviceID (1~255 characters),
            failover_group_name: Failover group名称 (1~255 characters),
            support_protocol: Logic portSupported data access protocols。Options：NONE (无协议), NFS (NFS协议), CIFS (CIFS协议), NFS_AND_CIFS (NFS和CIFS协议), NFS_OVER_RDMA (NFS over RDMA协议), iSCSI (iSCSI协议), FC/FCoE (FC/FCoE协议), NVME_OVER_ROCE (NVME over ROCE协议), BGP (BGP协议), DATA_TURBO (DataTurbo协议), DATA_TURBO_OVER_ROCE (DataTurbo over ROCE协议), S3 (S3协议), NFS_OVER_IB (NFS over IB协议), DATA_TURBO_OVER_IB (DataTurbo over IB协议), DATA_TURBO_OVER_ROCE_AND_TCP (DataTurbo over ROCE和TCP协议), OBJECT (S3协议), NAS_AND_OBJECT (NAS与object存储协议), KB_OVER_TCP (KnowledgeBase over TCP协议),
            logical_type: 逻辑类型。Options：SERVICE (主机端口/业务端口), MANAGEMENT (管理端口), MAINTENANCE (维护端口),
            listen_dns_query_enabled: 是否监听DNS查询请求 (1~255 characters)。Options：NO (关闭), YES (打开),
            management_access: Management access method (1~255 characters),
            vstore_raw_id: Logic port所属vStoreassigned on the deviceid (1~255 characters),
            vstore_name: Logic port所属vStore的名称 (1~255 characters),
            storage_id: Storage device ID (1~255 characters),
            storage_name: Storage device name (1~255 characters),
            zone_raw_id: Zoneon the deviceID (1~255 characters)，仅OceanStor A800series storage only,
            zone_id: Zone ID (1~64 characters)，仅OceanStor A800series storage only,
            zone_name: 所属zone名称 (1~255 characters)，仅OceanStor A800series storage only,
            zone_ip: 所属zone IP (1~255 characters),
            dns_zone_name: DNS Zone名称 (1~255 characters),
            current_port_type: Logic portPhysical port type。Options：ETHERNET_PORT (Ethernet port andRoCE端口), BOND (绑定), VLAN (VLAN), VIP (VIP), SIP (SIP), IB (IB),
            address_family: IPProtocol version。Options：IPv4 (IPv4), IPv6 (IPv6),
            can_failover: EnableIP地址漂移 (boolean)。Options：true, false,
            failback_mode: 回漂模式。Options：not_support (feature not supported), manual (手动), automatic (自动),
            scope: 范围。Options：hyperscale (全局), default (本地)。仅OceanStor A800series storage only,
            logicPortTags: Associated tag set (List<Tag>)。参数格式如下：[{
                id: 标签的ID (1~32 characters),
                tag_type_name: Tag type name (1~64 characters),
                name: 标签名称 (1~128 characters),
            }, ...],
            manufacturer: 厂商 (1~32 characters),
            storage_model: 型号 (1~64 characters),
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
    创建Storage device的Logic port（仅 OceanStor A800 series storage only）

    Args:
        client: DME API client
        storage_id: Storage device ID（Required，1~64 characters）
        name: Port name（Required，1~255 characters）。只允许包含字母、数字、"_"、"-"、"."and Chinese characters
        address_family: IPProtocol version（Required). Options：IPv4 (IPv4), IPv6 (IPv6)
        home_port_type: 父Port type（Required). Options：ETHERNET_PORT (Ethernet port andRoCE端口), BOND (绑定), VLAN (VLAN), VIP (VIP), SIP (SIP), IB (IB)
        zone_raw_id: Zoneon the deviceID（Required，1~64 characters），仅OceanStor A800series storage only
        scope: 范围（Required). Options：hyperscale (全局), default (本地)。仅OceanStor A800series storage only。Data access protocol isKB_OVER_TCP时取值only supportsdefault
        mgmt_ip: Logic portIP地址(IPV4)(Optional, max64 characters，IPv4格式）
        ipv4_mask: Logic portIPNetmask(IPV4)(Optional, max64 characters）
        ipv4_gateway: Logic port gatewayIP地址(IPV4)(Optional, max64 characters）
        mgmt_ipv6: Logic portIP地址(IPV6)(Optional, max128 characters）
        ipv6_mask: Logic portIPNetmask(IPV6)(Optional, max128 characters）
        ipv6_gateway: Logic port gatewayIP地址(IPV6)(Optional, max128 characters）
        home_port_raw_id: 父端口on the storage deviceID（可选，1~64 characters）
        support_protocol: Logic portSupported data access protocols(Optional). Options：NFS (NFS协议), DATA_TURBO_OVER_ROCE (DataTurbo over RoCE协议), NFS_OVER_RDMA (NFS over RDMA协议), NFS_OVER_IB (NFS over IB协议), DATA_TURBO_OVER_IB (DataTurbo over IB协议), DATA_TURBO_OVER_ROCE_AND_TCP (DataTurbo over RoCE和TCP协议), OBJECT (S3协议), NAS_AND_OBJECT (NAS与object存储协议), KB_OVER_TCP (KnowledgeBase over TCP协议)。role isCLIENT时，do not send this field
        operational_status: 激活状态(Optional). Options：ACTIVATED (激活), NOT_ACTIVATED (inactive)
        home_controller_id: ControllerID（可选，1~64 characters）。role isHEALTH_CHECK时，this field is required
        failover_group_raw_id: Failover groupon the storage deviceID(Optional, max64 characters）。Data access protocol isKB_OVER_TCP时，this field is required
        vstore_raw_id: Logic port所属vStoreassigned on the deviceid(Optional, max64 characters）。role isCLIENT时，do not send this field
        role: Logic port角色（可选，默认 DATA). Options：MANAGEMENT (管理), DATA (数据), VTEP (VTEP), HEALTH_CHECK (Health check), MANAGEMENT_AND_DATA (管理+数据), CLIENT (Client)
        dns_zone_name: DNS ZoneName (Optional,最多255 characters）。role isCLIENT或Data access protocol isKB_OVER_TCP时，do not send this field
        listen_dns_query_enabled: 是否侦听DNS查询请求（可选，正则 NO|YES). Options：NO (关闭), YES (打开)。role isCLIENT或Data access protocol isKB_OVER_TCP时，do not send this field
        can_failover: EnableIP地址漂移（可选，boolean). Options：true, false。Data access protocol isKB_OVER_TCP时，do not send this field
        failback_mode: 回漂模式(Optional). Options：not_support (feature not supported), manual (手动), automatic (自动)。Data access protocol isKB_OVER_TCP时，do not send this field

    Returns:
        {
            task_id: 任务Id (1~64 characters),
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
    Modify storage device的Logic port（仅 OceanStor A800 series storage only）

    Args:
        client: DME API client
        logic_port_id: Logic port ID（Required，1~128  characters）
        name: Port name（可选）
        address_family: IP Protocol version（可选）
        mgmt_ip: Logic port IP 地址 (IPV4)（可选）
        ipv4_mask: Logic port IP Netmask (IPV4)（可选）
        ipv4_gateway: Logic port gateway IP 地址 (IPV4)（可选）
        mgmt_ipv6: Logic port IP 地址 (IPV6)（可选）
        ipv6_mask: Logic port IP Netmask (IPV6)（可选）
        ipv6_gateway: Logic port gateway IP 地址 (IPV6)（可选）
        home_port_raw_id: 父端口on the storage device ID（可选）
        home_port_type: 父Port type（可选）
        operational_status: 激活状态（可选）
        failover_group_raw_id: Failover groupon the storage device ID（可选）
        dns_zone_name: DNS Zone 名称（可选）
        listen_dns_query_enabled: 是否侦听 DNS 查询请求（可选）
        can_failover: Enable IP 地址漂移（可选）
        failback_mode: 回漂模式（可选）

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
    删除Storage device的Logic port（仅 OceanStor A800 series storage only）

    Args:
        client: DME API client
        ids: Logic port ID 列表（Required，1~1000 个 ID）

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
    回切Storage device的Logic port（仅 OceanStor A800 series storage only）

    Args:
        client: DME API client
        id: Logic port ID（Required，1~64  characters）

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


# ============ 存储端口 (port) subtopic functions ============


def port_list(client: DMEAPIClient, storage_id: str = None, port_type: str = None,
              location: str = None, ipv4: str = None, ipv6: str = None,
              port_name: str = None, zone_id: str = None,
              page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询Storage device端口信息，支持 ETH、FC、IB、Bond、SAS 五种类型

    Args:
        client: DME API client
        storage_id: Storage device ID（可选，1~36  characters）
        port_type: Port type（可选，eth/fc/ib/bond/sas，returns all types if not specified）
        location: 位置（可选，仅 ETH port support，1~255  characters）
        ipv4: IPv4 地址（可选，仅 ETH port support，1~255  characters）
        ipv6: IPv6 地址（可选，仅 ETH port support，1~255  characters）
        port_name: Port name（可选，仅 ETH port support，1~255  characters）
        zone_id: Storage device的 Zone ID（可选，仅 Bond port support，1~36  characters）
        page_no: Page number（可选，FC/SAS port support，1~10000，默认 1）
        page_size: 每页count（可选，FC/SAS port support，1~1000，默认 20）

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，includes port list
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
        # 返回所有类型端口（ETH + FC + IB + SAS）
        all_eth_ports = []
        all_fc_ports = []
        all_ib_ports = []
        all_sas_ports = []
        total_count = 0

        # 查询 ETH 端口
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
        # ETH 端口 API 返回结构：{'total': N, 'eth_ports': [...]}
        if 'eth_ports' in eth_response:
            all_eth_ports = eth_response.get('eth_ports', [])
            total_count += len(all_eth_ports)

        # 查询 FC 端口
        fc_url = "/rest/storagemgmt/v1/frontend-ports/fc-ports/query"
        fc_payload = {
            'page_no': page_no,
            'page_size': page_size
        }
        if storage_id is not None:
            fc_payload['storage_id'] = storage_id
        fc_response = client.post(fc_url, body=fc_payload)
        # FC 端口 API 返回结构：{'total': N, 'ports': [...]}
        if 'ports' in fc_response:
            all_fc_ports = fc_response.get('ports', [])
            total_count += len(all_fc_ports)

        # 查询 IB 端口
        ib_url = "/rest/storagemgmt/v1/storages/ib-ports/query"
        ib_payload = {}
        if storage_id is not None:
            ib_payload['storage_id'] = storage_id
        ib_response = client.post(ib_url, body=ib_payload)
        # IB 端口 API 返回结构：{'ib_ports': [...]}
        if 'ib_ports' in ib_response:
            all_ib_ports = ib_response.get('ib_ports', [])
            total_count += len(all_ib_ports)

        # 查询 SAS 端口
        sas_url = "/rest/storagemgmt/v1/backend-ports/sas-ports/query"
        sas_payload = {
            'page_no': page_no,
            'page_size': page_size
        }
        if storage_id is not None:
            sas_payload['storage_id'] = storage_id
        sas_response = client.post(sas_url, body=sas_payload)
        # SAS 端口 API 返回结构：{'total': N, 'ports': [...]}
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
        bond_port_id: 绑定端口 id（Required，1~64  characters）

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含 total 和 eth_ports 字段
    """
    url = "/rest/storagemgmt/v1/bond-ports/{bond_port_id}/eth-ports"

    response = client.get(url, params={"bond_port_id": bond_port_id})
    return response


# ============ 存储Port group (port_group) subtopic functions ============


# ============ 存储 VLAN subtopic functions ============


def vlan_list(client: DMEAPIClient, name: str = None, storage_id: str = None,
              page_no: int = 1, page_size: int = 100) -> dict:
    """
    Batch query VLAN 列表

    Args:
        client: DME API client
        name: VLAN 名称（supports fuzzy search）
        storage_id: Storage device ID
        page_no: Page queryStart page，默认 1
        page_size: 每页count，1~1000，默认 100

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含 VLAN 列表
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
    创建 VLAN

    注意：only supports OceanStor A800、A600 series storage。

    Args:
        client: DME API client
        name: VLAN 名称（Required）
        vlan_id: VLAN ID（Required，1~4094）
        storage_id: Storage device ID（Required）
        description: VLAN 描述（可选）

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，includes newly created VLAN ID
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
    删除 VLAN

    注意：only supports OceanStor A800、A600 series storage。

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
    修改 VLAN

    注意：only supports OceanStor A800、A600 series storage。

    Args:
        client: DME API client
        vlan_id: VLAN ID
        name: VLAN 名称（可选）
        description: VLAN 描述（可选）

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


# ============ 存储Failover group (failover_group) subtopic functions ============


def failover_group_list(client: DMEAPIClient, storage_id: str,
                        failover_group_type: str = None,
                        zone_id: str = None,
                        failover_group_service_type: list = None) -> dict:
    """
    查询Failover group list

    Args:
        client: DME API client
        storage_id: Storage device ID（Required，1~36 characters，且满足正则 ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$）
        failover_group_type: Failover group类型(Optional). Options：system, VLAN, customized
        zone_id: Zone ID（可选，1~255 characters），仅OceanStor A800series storage only
        failover_group_service_type: Failover groupBusiness type list（可选，List<string>，max array members：10). Options：NAS (used to associateNFS、CIFS、NFS and OBJECTProtocol typeLogic port的Failover group), BGP (used to associateVIP类型Logic port的Failover group), RDMA (used to associateNFS over RDMA、NFS、OBJECT协议Logic port的Failover group), IB (used to associateNAS over IBProtocol typeLogic port的Failover group), KB (used to associateKnowledgeBase over TCPProtocol typeLogic port的Failover group)

    Returns:
        {
            total: Failover groupcount (int32),
            failover_groups: Failover group list (List<FailoverGroupResp>)。参数格式如下：[{
                id: Failover groupid (1~64 characters),
                name: Failover group名称 (1~64 characters),
                failover_group_type: Failover group类型 (1~255 characters)。Options：system, VLAN, customized,
                raw_id: Failover groupon the storage deviceID (1~255 characters),
                zone_name: Zone名称 (1~255 characters)，仅OceanStor A800series storage only,
                zone_raw_id: Zone在Storage device上分配的ID (1~255 characters)，仅OceanStor A800series storage only,
                zone_id: Storage device的Zone ID (1~255 characters)，仅OceanStor A800series storage only,
                failover_group_service_type: Failover group业务类型。Options：NAS (used to associateNFS、CIFS、NFS and OBJECTProtocol typeLogic port的Failover group), BGP (used to associateVIP类型Logic port的Failover group), RDMA (used to associateNFS over RDMA、NFS、OBJECT协议Logic port的Failover group), IB (used to associateNAS over IBProtocol typeLogic port的Failover group), KB (used to associateKnowledgeBase over TCPProtocol typeLogic port的Failover group),
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
    查询Failover group下的端口（支持 bond、eth、ib 三种类型）

    Args:
        client: DME API client
        failover_group_id: Failover group id（Required，1~64  characters）
        port_type: Port type（可选，bond/eth/ib，returns all types if not specified）

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，结构一致：{"total": x, "bond_ports": [], "eth_ports": [], "ib_ports": []}
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
        # type not specified，返回所有三种类型的端口，扁平化结构
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
    查询Failover group下的 VLAN

    Args:
        client: DME API client
        failover_group_id: Failover group id（Required，1~64  characters）

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含 vlans 字段
    """
    url = "/rest/storagemgmt/v1/failover-groups/{failover_group_id}/vlans"

    response = client.get(url, params={"failover_group_id": failover_group_id})
    return response


# ============ Zone (OceanStor A800 集群 zone) subtopic functions ============


def zone_list(client: DMEAPIClient, name: str = None, ip: str = None,
              status: list = None, sync_status: list = None,
              sn: str = None, storage_ids: list = None) -> dict:
    """
    查询OceanStor A800集群中zone信息

    Args:
        client: DME API client
        name: zoneName (Optional,1~256 characters），exact match
        ip: zone ip地址Name (Optional,1~256 characters），exact match
        status: Zonestatus list（可选，List<string>，max array members：6). Options：OFFLINE (离线), NORMAL (正常), FAULT (故障), DEGRADED (降级), ABNORMAL (未管理), UNKNOWN (未知)
        sync_status: ZoneSyncstatus list（可选，List<string>，max array members：5). Options：UNSYNC (未Sync), SYNC (Syncing), NORMAL (Sync完成), FAILED (Sync失败), UNKNOWN (未知)
        sn: ZoneSerial number（可选，1~128 characters），exact match
        storage_ids: OceanStor A800集群id列表（可选，List<string>，max array members：100，最小成员count：1），exact match

    Returns:
        {
            total: ZoneTotal count (int32),
            datas: Zone list (List<OceanStorA800ZoneInfo>)。参数格式如下：[{
                id: Zone在CMDB中的ID (1~64 characters),
                native_id: native id (1~64 characters),
                name: Zone名称 (1~128 characters),
                ip: Zone IP地址 (1~32 characters),
                status: 状态 (1~32 characters)。Options：OFFLINE (离线), NORMAL (正常), FAULT (故障), DEGRADED (降级), ABNORMAL (未管理),
                sync_status: Sync状态 (1~32 characters)。Options：UNSYNC (未Sync), SYNC (Syncing), NORMAL (Sync完成), FAILED (Sync失败),
                sn: ZoneDevice serial number (1~64 characters),
                wwn: Zone设备WWN号 (1~32 characters),
                vendor: Zone厂商 (1~32 characters),
                model: ZoneProduct model (1~64 characters),
                owning_ne_type: Storage device网元类型。Options：dorado (doradoseries storage), OceanStor A800 (OceanStor A800),
                location: Zone位置信息 (0~512 characters),
                version: 版本信息 (0~64 characters),
                patch_version: Patch version info (0~64 characters),
                add_time: 接入设备时间 (0~32 characters)，UTCTimestamp（精确到毫second(s)）,
                last_sync_time: 上一次Sync time (0~32 characters)，UTCTimestamp（精确到毫second(s)）,
                sync_process: Sync进度 (int32),
                alarm_num: 告警count (number),
                parent_id: 集群id,
                zone_raw_id: zone raw id,
                is_core_zone: 是否是核心控制节点所在的zone (boolean)。Options：true, false,
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
# 格式：action_key: {func, description, params, subtopic}
# subtopic 表示该动作属于哪个Subtopic，None 表示直接动作

ACTIONS = {
    # 直接动作（两级结构：<topic> <action>）
    'list': {
        'func': list,
        'description': 'Batch query storage devices',
        'params': ['az', 'source', 'dc_id', 'tag_ids', 'start', 'limit', 'ext_attrs'],
        'subtopic': None
    },
    'show': {
        'func': show,
        'description': 'QueryStorage device',
        'params': ['storage_id'],
        'subtopic': None
    },
    'add': {
        'func': add,
        'description': '添加Storage device（only supports录入离线Storage device信息）',
        'params': ['name', 'sn', 'ip', 'vendor', 'model', 'version', 'patch_version', 'dc_id', 'az', 'location', 'maintenance_start', 'maintenance_overtime', 'total_capacity', 'total_effective_capacity', 'total_pool_capacity', 'used_capacity', 'free_capacity', 'subscription_capacity', 'tag_ids'],
        'subtopic': None
    },
    'remove': {
        'func': remove,
        'description': '批量Remove storage device',
        'params': ['storage_ids'],
        'subtopic': None
    },
    'sync': {
        'func': sync,
        'description': 'SyncStorage device信息',
        'params': ['storage_id'],
        'subtopic': None
    },
    'modify': {
        'func': modify,
        'description': 'Modify storage device（only supportsModify recorded offlineStorage device信息）',
        'params': ['storage_id', 'name', 'location', 'ext_attrs'],
        'subtopic': None
    },
    # subtopic actions（三级结构：<topic> <subtopic> <action>）
    'bbu_list': {
        'func': bbu_list,
        'description': 'query storage device BBU info list',
        'params': ['storage_id', 'health_status', 'running_status', 'enclosure_name',
                   'location', 'zone_id', 'page_no', 'page_size'],
        'subtopic': 'bbu'
    },
    'get_passphrase': {
        'func': get_passphrase,
        'description': '获取Storage device访问的令牌',
        'params': ['storage_id'],
    },
    'fan_list': {
        'func': fan_list,
        'description': 'query storage deviceFan信息',
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
        'description': '查询Storage deviceStorage pool列表',
        'params': ['storage_id', 'raw_id', 'zone_id', 'page_no', 'page_size', 'sort_key', 'sort_dir'],
        'subtopic': 'pool'
    },
    'hyperscale_pool_list': {
        'func': hyperscale_pool_list,
        'description': '查询 HyperScale Storage pool列表',
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
        'description': '获取Storage devicePower supply（PSU）列表',
        'params': ['storage_id', 'health_status', 'running_status', 'power_type',
                   'power_mode', 'location', 'model', 'sn', 'enclosure_name',
                   'zone_id', 'page_no', 'page_size'],
        'subtopic': 'psu'
    },
    'query_power_data': {
        'func': query_power_data,
        'description': '查询Storage device功率数据',
        'params': ['start_time', 'end_time', 'storage_ids', 'time_granularity'],
    },
    'app_type_list': {
        'func': app_type_list,
        'description': 'QueryStorage device的应用类型',
        'params': ['storage_id'],
        'subtopic': 'app_type'
    },
    'controller_list': {
        'func': controller_list,
        'description': 'QueryStorage devicecontroller info',
        'params': ['storage_id'],
        'subtopic': 'controller'
    },
    'disk_domain_list': {
        'func': disk_domain_list,
        'description': 'Batch query disk pools',
        'params': ['storage_id', 'page_no', 'page_size'],
        'subtopic': 'disk_domain'
    },
    'disk_pool_list': {
        'func': disk_pool_list,
        'description': 'Batch query分布式Storage device的Disk pool',
        'params': ['storage_id', 'page_no', 'page_size'],
        'subtopic': 'disk_pool'
    },
    'enclosure_list': {
        'func': enclosure_list,
        'description': 'Batch query enclosures信息',
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
        'description': '创建租户',
        'params': ['name', 'storage_id', 'san_capacity_quota', 'nas_capacity_quota', 'description', 'nas_capacity_quota_alarm_switch', 'nas_capacity_quota_alarm_threshold', 'associate_pool_ids'],
        'subtopic': 'vstore'
    },
    'vstore_modify': {
        'func': vstore_modify,
        'description': 'Modify租户',
        'params': ['vstore_id', 'name', 'san_capacity_quota', 'nas_capacity_quota', 'description', 'nas_capacity_quota_alarm_switch', 'nas_capacity_quota_alarm_threshold'],
        'subtopic': 'vstore'
    },
    'vstore_delete': {
        'func': vstore_delete,
        'description': 'Batch delete租户',
        'params': ['vstore_ids'],
        'subtopic': 'vstore'
    },
    'initiator_list': {
        'func': initiator_list,
        'description': 'Batch query存储侧Initiatorobject',
        'params': ['page_size', 'page_no', 'raw_id', 'alias', 'status',
                   'associated_host_name', 'associated_host_id', 'multipath_type',
                   'protocol', 'support_provisioning', 'vstore_raw_id',
                   'vstore_name', 'storage_id'],
        'subtopic': 'initiator'
    },
    'initiator_delete': {
        'func': initiator_delete,
        'description': 'Batch deleteStorage device的Initiatorobject',
        'params': ['initiator_ids', 'task_remarks'],
        'subtopic': 'initiator'
    },
    'initiator_modify': {
        'func': initiator_modify,
        'description': '修改存储侧Initiatorobject',
        'params': ['initiator_id', 'vstore_id', 'alias', 'multi_path'],
        'subtopic': 'initiator'
    },
    # account subtopic actions（auth user）
    'account_show_local_users': {
        'func': account_show_local_users,
        'description': 'QueryStorage device本地Auth user info',
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
        'description': 'CreateStorage device UNIX auth user',
        'params': ['storage_id', 'name', 'primary_group_raw_id', 'raw_id', 'description', 'password', 'status_enabled', 'vstore_raw_id'],
        'subtopic': 'account'
    },
    'account_create_windows_user': {
        'func': account_create_windows_user,
        'description': 'CreateStorage device Windows auth user',
        'params': ['storage_id', 'name', 'password', 'raw_id', 'description', 'status_enabled', 'vstore_raw_id'],
        'subtopic': 'account'
    },
    'account_show_unix_users': {
        'func': account_show_unix_users,
        'description': 'QueryStorage device UNIX Auth user info',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_show_windows_users': {
        'func': account_show_windows_users,
        'description': 'QueryStorage device Windows Auth user info',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_show_local_user_groups': {
        'func': account_show_local_user_groups,
        'description': 'QueryStorage device本地Auth user group info',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_show_unix_user_groups': {
        'func': account_show_unix_user_groups,
        'description': 'QueryStorage device UNIX Auth user group info',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_show_windows_user_groups': {
        'func': account_show_windows_user_groups,
        'description': 'QueryStorage device Windows Auth user group info',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    # qos subtopic actions
    'qos_list': {
        'func': qos_list,
        'description': 'Batch query QoS 策略',
        'params': ['storage_id', 'name', 'raw_id', 'enable_status', 'running_status',
                   'zone_id', 'resource_type_list', 'vstore_id', 'vstore_name',
                   'alarm_status', 'io_policy_type', 'page_no', 'page_size',
                   'sort_key', 'sort_dir'],
        'subtopic': 'qos'
    },
    'qos_show': {
        'func': qos_show,
        'description': 'Query QoS 策略详情',
        'params': ['qos_policy_id'],
        'subtopic': 'qos'
    },
    'qos_create': {
        'func': qos_create,
        'description': '创建 QoS 策略',
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
        'description': '修改 QoS 策略',
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
        'description': '删除 QoS 策略',
        'params': ['qos_policy_ids'],
        'subtopic': 'qos'
    },
    'qos_activate': {
        'func': qos_activate,
        'description': '批量激活 QoS 策略',
        'params': ['qos_policy_ids'],
        'subtopic': 'qos'
    },
    'qos_deactivate': {
        'func': qos_deactivate,
        'description': 'Batch deactivate QoS 策略',
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
    # logic_port subtopic actions（存储Logic port）
    'logic_port_list': {
        'func': logic_port_list,
        'description': 'query storage deviceLogic port list',
        'params': ['storage_id', 'vstore_raw_id', 'zone_raw_id', 'scope', 'page_no', 'page_size'],
        'subtopic': 'logic_port'
    },
    'logic_port_show': {
        'func': logic_port_show,
        'description': 'query storage deviceLogic port详情',
        'params': ['logic_port_id'],
        'subtopic': 'logic_port'
    },
    'logic_port_create': {
        'func': logic_port_create,
        'description': '创建Storage device的Logic port（仅 OceanStor A800 series storage only）',
        'params': ['storage_id', 'name', 'address_family', 'home_port_type', 'zone_raw_id', 'scope',
                   'mgmt_ip', 'ipv4_mask', 'ipv4_gateway', 'mgmt_ipv6', 'ipv6_mask', 'ipv6_gateway',
                   'home_port_raw_id', 'support_protocol', 'operational_status', 'home_controller_id',
                   'failover_group_raw_id', 'vstore_raw_id', 'role', 'dns_zone_name',
                   'listen_dns_query_enabled', 'can_failover', 'failback_mode'],
        'subtopic': 'logic_port'
    },
    'logic_port_update': {
        'func': logic_port_update,
        'description': 'Modify storage device的Logic port（仅 OceanStor A800 series storage only）',
        'params': ['logic_port_id', 'name', 'address_family', 'mgmt_ip', 'ipv4_mask', 'ipv4_gateway',
                   'mgmt_ipv6', 'ipv6_mask', 'ipv6_gateway', 'home_port_raw_id', 'home_port_type',
                   'operational_status', 'failover_group_raw_id', 'dns_zone_name',
                   'listen_dns_query_enabled', 'can_failover', 'failback_mode'],
        'subtopic': 'logic_port'
    },
    'logic_port_delete': {
        'func': logic_port_delete,
        'description': '删除Storage device的Logic port（仅 OceanStor A800 series storage only）',
        'params': ['ids'],
        'subtopic': 'logic_port'
    },
    'logic_port_failback': {
        'func': logic_port_failback,
        'description': '回切Storage device的Logic port（仅 OceanStor A800 series storage only）',
        'params': ['id'],
        'subtopic': 'logic_port'
    },
    # port subtopic actions（存储端口）
    'port_list': {
        'func': port_list,
        'description': '查询Storage device端口信息，支持 ETH、FC、IB、Bond 四种类型',
        'params': ['storage_id', 'port_type', 'location', 'ipv4', 'ipv6', 'port_name', 'zone_id', 'page_no', 'page_size'],
        'subtopic': 'port'
    },
    'port_show_bond_members': {
        'func': port_show_bond_members,
        'description': 'QueryBound port member list info',
        'params': ['bond_port_id'],
        'subtopic': 'port'
    },
    # vlan subtopic actions（存储 VLAN）
    'vlan_list': {
        'func': vlan_list,
        'description': 'Batch query VLAN 列表',
        'params': ['name', 'storage_id', 'page_no', 'page_size'],
        'subtopic': 'vlan'
    },
    'vlan_create': {
        'func': vlan_create,
        'description': '创建 VLAN（only supports OceanStor A800、A600 series storage）',
        'params': ['name', 'vlan_id', 'storage_id', 'description'],
        'subtopic': 'vlan'
    },
    'vlan_delete': {
        'func': vlan_delete,
        'description': '删除 VLAN（only supports OceanStor A800、A600 series storage）',
        'params': ['vlan_id'],
        'subtopic': 'vlan'
    },
    'vlan_modify': {
        'func': vlan_modify,
        'description': '修改 VLAN（only supports OceanStor A800、A600 series storage）',
        'params': ['vlan_id', 'name', 'description'],
        'subtopic': 'vlan'
    },
    # failover_group subtopic actions（存储Failover group）
    'failover_group_list': {
        'func': failover_group_list,
        'description': '查询Failover group list',
        'params': ['storage_id', 'failover_group_type', 'zone_id', 'failover_group_service_type'],
        'subtopic': 'failover_group'
    },
    'failover_group_show_ports': {
        'func': failover_group_show_ports,
        'description': '查询Failover group下的端口（支持 bond、eth、ib 三种类型）',
        'params': ['failover_group_id', 'port_type'],
        'subtopic': 'failover_group'
    },
    'failover_group_show_vlans': {
        'func': failover_group_show_vlans,
        'description': '查询Failover group下的 VLAN',
        'params': ['failover_group_id'],
        'subtopic': 'failover_group'
    },
    # zone subtopic actions（OceanStor A800 集群 zone）
    'zone_list': {
        'func': zone_list,
        'description': '查询OceanStor A800集群中zone信息',
        'params': ['name', 'ip', 'status', 'sync_status', 'sn', 'storage_ids'],
        'subtopic': 'zone'
    },
}
