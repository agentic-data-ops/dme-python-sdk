"""
存储设备 (Storage) 相关操作
"""

import sys
import os

from pydme.client import DMEAPIClient

# ============================================================================
# VStore (租户) 子主题函数
# ============================================================================


def vstore_list(client: DMEAPIClient, storage_id: str, name: str = None, page_no: int = 1, page_size: int = 100) -> dict:
    """
    批量查询存储设备租户信息

    查询存储设备上的租户列表。

    Args:
        client: DME API 客户端
        storage_id: 存储设备 ID（可选）
        name: 租户名称（可选，支持模糊查询）
        page_no: 分页查询的页码，默认 1，范围 1~10000000
        page_size: 每页数量，1~1000，默认 100

    Returns:
        响应数据，包含 total 和 vstores 字段
    """
    url = "/rest/fileservice/v1/vstores/query"

    payload = {}

    if storage_id is not None:
        payload['storage_id'] = storage_id
    if name is not None:
        payload['name'] = name
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size

    response = client.post(url, body=payload)
    return response


def vstore_show(client: DMEAPIClient, vstore_id: str) -> dict:
    """
    查询租户详情
    
    查询指定租户的详细信息。
    
    Args:
        client: DME API 客户端
        vstore_id: 租户 ID（必选）
    
    Returns:
        租户详细信息
    """
    url = "/rest/fileservice/v1/vstores/{vstore_id}"
    
    response = client.get(url, params={"vstore_id": vstore_id})
    return response


def vstore_create(client: DMEAPIClient, name: str, storage_id: str, san_capacity_quota: str = None,
                  nas_capacity_quota: str = None, description: str = None,
                  nas_capacity_quota_alarm_switch: bool = None,
                  nas_capacity_quota_alarm_threshold: int = None,
                  associate_pool_ids: list = None) -> dict:
    """
    创建租户

    创建新的存储租户。

    Args:
        client: DME API 客户端
        name: 租户名称（必选，1~256 个字符）
        storage_id: 存储设备 ID（必选，1~36 个字符，UUID 格式）
        san_capacity_quota: SAN 容量配额（可选，单位：扇区）
        nas_capacity_quota: NAS 容量配额（可选，单位：扇区）
        description: 租户描述（可选，0~255 个字符）
        nas_capacity_quota_alarm_switch: NAS 容量配额告警开关（可选，仅 A800 设备支持）
        nas_capacity_quota_alarm_threshold: NAS 容量配额告警阈值（可选，仅 A800 设备支持）
        associate_pool_ids: 关联存储池 ID 列表（可选，仅 A 系列设备支持）

    Returns:
        响应数据，包含 task_id
    """
    url = "/rest/fileservice/v1/vstores"

    if not storage_id:
        raise ValueError("参数 storage_id 是必填的")

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


def vstore_modify(client: DMEAPIClient, vstore_id: str, name: str = None,
                  san_capacity_quota: str = None, nas_capacity_quota: str = None,
                  description: str = None, nas_capacity_quota_alarm_switch: bool = None,
                  nas_capacity_quota_alarm_threshold: int = None) -> dict:
    """
    修改指定租户
    
    修改存储设备上指定的租户。
    
    Args:
        client: DME API 客户端
        vstore_id: 租户 ID（必选）
        name: 租户名称（可选）
        san_capacity_quota: SAN 容量配额（可选，单位：扇区）
        nas_capacity_quota: NAS 容量配额（可选，单位：扇区）
        description: 租户描述（可选）
        nas_capacity_quota_alarm_switch: NAS 容量配额告警开关（可选，仅 A800 设备支持）
        nas_capacity_quota_alarm_threshold: NAS 容量配额告警阈值（可选，仅 A800 设备支持）
    
    Returns:
        响应数据，包含 task_id
    """
    url = "/rest/fileservice/v1/vstores/{vstore_id}"
    
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
    
    response = client.put(url, body=payload, params={"vstore_id": vstore_id})
    return response


def vstore_delete(client: DMEAPIClient, vstore_ids: list) -> dict:
    """
    批量删除租户
    
    注：该 API 可能会直接或间接影响现网业务运行，导致业务中断、关键数据丢失等，请谨慎操作。
    
    Args:
        client: DME API 客户端
        vstore_ids: 租户 ID 列表（必选，1~100 个）
    
    Returns:
        响应数据，包含 task_id
    """
    url = "/rest/fileservice/v1/vstores/delete"
    
    payload = {
        'ids': vstore_ids
    }
    
    response = client.post(url, body=payload)
    return response



def list(client: DMEAPIClient, az: str = None, source: str = None,
         dc_id: str = None, tag_ids: str = None, start: int = 1, 
         limit: int = 20, ext_attrs: str = None) -> dict:
    """
    批量查询存储设备
    
    支持分页查询，过滤。
    
    Args:
        client: DME API 客户端。
        az: 可用分区 ID (可选, 1~64个字符)。
        source: 存储设备的来源 (可选)。可选值：add (接入), record (录入), all (所有)。默认查询接入设备。
        dc_id: 存储设备所属数据中心的ID (可选, 1~32个字符)。
        tag_ids: 标签过滤列表 (可选)。最多支持10个标签ID组合过滤，多个过滤条件之间为且关系。
        start: 分页查询的起始位置 (可选, 1~10000, 默认值: 1)。
        limit: 分页查询的个数 (可选, 1~1000, 默认值: 20)。
        ext_attrs: 扩展属性过滤列表 (可选, 1~3000个字符)。最多支持10个扩展属性组合过滤，多个过滤条件之间为且关系。例如：{"extAttr1":"value1","extAttr2":"value2"}。
    
    Returns:
        响应数据，包含 total 和 datas 字段
        - total: 存储设备总数
        - datas: 存储设备列表，包含 id, pid, name, ip, status, sn, vendor, model 等信息
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
    查询指定存储设备
    
    Args:
        client: DME API 客户端
        storage_id: 存储设备 ID（必选，1~36 个字符，UUID 格式或 32 位十六进制）
    
    Returns:
        存储设备详细信息，包含 id, name, ip, status, sn, vendor, model 等
    """
    url = "/rest/storagemgmt/v1/storages/{storage_id}/detail"
    
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
    添加存储设备（仅支持录入离线存储设备信息）

    通过离线方式添加存储设备信息到 DME 系统。

    Args:
        client: DME API 客户端。
        name: 设备名称 (1~256个字符)。只能包含半角字母、半角数字、\"_\"、\"-\"、\".\"、中文字符。
        sn: 设备序列号 (正则表达式为^[a-zA-Z0-9]{1,128}$)。
        ip: 设备IP地址 (可选, 0~128个字符, 支持IPv4与IPv6格式, 也可为空字符串)。
        dc_id: 所属数据中心ID (可选, 正则表达式为^[a-zA-Z0-9]{1,128}$)。
        vendor: 厂商 (可选, 0~128个字符)。
        model: 产品型号 (可选, 0~128个字符)。
        version: 版本信息 (可选, 0~64个字符)。
        patch_version: 补丁版本信息 (可选, 0~64个字符)。
        location: 设备位置 (可选, 0~512个字符)。
        maintenance_start: 维护开始时间 (可选, 格式是毫秒级时间戳)。需要和维护过保时间一起出现并且数值小于维护过保时间。
        maintenance_overtime: 维护过保时间 (可选, 格式是毫秒级时间戳)。需要和维护开始时间一起出现并且数值大于维护开始时间。
        total_capacity: 裸容量 (可选, 0~2147483647, 单位MB)。
        total_effective_capacity: 可得容量 (可选, 0~2147483647, 单位MB)。
        total_pool_capacity: 可用容量 (可选, 0~2147483647, 单位MB)。
        used_capacity: 已用容量 (可选, 0~2147483647, 单位MB)。
        free_capacity: 空闲容量 (可选, 0~2147483647, 单位MB)。
        subscription_capacity: 已订阅容量 (可选, 0~2147483647, 单位MB)。
        tag_ids: 标签ID列表 (可选, List<string>, 数组最大成员个数: 10, 数组最小成员个数: 0)。
    
    Returns:
        响应数据，包含 id（存储设备 ID）

    Raises:
        ValueError: 必填参数缺失
    """
    # 验证必填参数
    if not name:
        raise ValueError("参数 name 是必填的")
    if not sn:
        raise ValueError("参数 sn 是必填的")

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
    批量移除存储设备

    Args:
        client: DME API 客户端
        ids: 存储设备 ID 列表（1~100 个）

    Returns:
        响应数据，包含 task_id（异步任务）
    """
    url = "/rest/storagemgmt/v2/storages/delete"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def sync(client: DMEAPIClient, storage_id: str) -> dict:
    """
    同步存储设备信息
    
    Args:
        client: DME API 客户端
        storage_id: 存储设备 ID
    
    Returns:
        响应数据，包含 task_id（异步任务）
    """
    url = "/rest/storagemgmt/v1/storages/refresh"
    
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
    查询存储设备的 BBU 信息列表

    Args:
        client: DME API 客户端。
        storage_id: BBU所属存储设备的id (可选, 1~64个字符)。
        health_status: 健康状态 (可选)。可选值：unknown (未知), normal (正常), faulty (故障), about_to_fail (即将故障), low_battery (电量不足)。
        running_status: 运行状态 (可选)。可选值：unknown (未知), normal (正常), running (运行), online (在线), offline (离线), charging (正在充电), charging_completed (充电完成), discharging (正在放电)。
        enclosure_name: 所属机框名称 (可选, 1~256个字符)。支持模糊匹配。
        location: 位置 (可选, 1~256个字符)。支持模糊匹配。
        zone_id: 所属Zone ID (可选, 1~255个字符)。仅OceanStor A800系列存储支持。
        page_no: 分页查询的页码 (可选, 1~2147483647, 默认值: 1)。
        page_size: 分页查询的每页大小 (可选, 1~1000, 默认值: 20)。
    
    Returns:
        {
            backup_powers: BBU列表 (List<StorageBackupPowerInfo>)。参数格式如下：[{
                name: 名称 (1~255个字符),
                location: 位置 (1~255个字符),
                health_status: 健康状态。可选值：unknown (未知), normal (正常), faulty (故障), about_to_fail (即将故障), low_battery (电量不足),
                running_status: 运行状态。可选值：unknown (未知), normal (正常), running (运行), online (在线), offline (离线), charging (正在充电), charging_completed (充电完成), discharging (正在放电),
                charge_times: 放电次数 (int64),
                firmware_version: 固件版本号 (1~255个字符),
                manufactured_date: 出厂日期 (1~255个字符),
                enclosure_id: 所属机框在存储设备上ID (1~255个字符),
                enclosure_name: 所属机框名称 (1~255个字符),
                zone_id: 所属Zone ID (1~255个字符)，仅OceanStor A800系列存储支持,
                zone_ip: 所属Zone IP地址 (1~255个字符)，仅OceanStor A800系列存储支持,
                zone_name: 所属Zone名称 (1~255个字符)，仅OceanStor A800系列存储支持,
            }, ...],
            total: BBU的数量 (int32),
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
    获取存储设备访问的令牌

    Args:
        client: DME API 客户端
        storage_id: 存储设备ID（必选）

    Returns:
        {
            ip: 存储设备IP地址,
            passphrase: 访问存储设备的令牌,
            port: 访问存储设备的端口 (int32),
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
    查询存储设备的风扇信息

    Args:
        client: DME API 客户端
        storage_id: 所属存储设备ID（可选，1~64个字符）
        health_status: 健康状态（可选）。可选值：unknown (未知), normal (正常), faulty (故障)
        running_status: 运行状态（可选）。可选值：unknown (未知), normal (正常), running (运行), not_running (未运行), spin_down (休眠), online (在线), offline (离线)
        run_level: 运行档位（可选）。可选值：low (低), normal (正常), high (高)
        enclosure_name: 所属机框名称（可选，1~256个字符），支持模糊匹配
        location: 位置（可选，1~256个字符），支持模糊匹配
        zone_id: 所属Zone ID（可选，1~255个字符），仅OceanStor A800系列存储支持
        page_no: 分页查询的页码（可选，1~2147483647，默认 1）
        page_size: 分页查询的每页大小（可选，1~1000，默认 20）

    Returns:
        {
            total: 风扇数量 (integer),
            fans: 风扇列表 (List<StorageFanInfo>)。参数格式如下：[{
                name: 名称 (1~128个字符),
                location: 位置 (1~256个字符),
                health_status: 健康状态。可选值：unknown (未知), normal (正常), faulty (故障),
                running_status: 运行状态。可选值：unknown (未知), normal (正常), running (运行), not_running (未运行), spin_down (休眠), online (在线), offline (离线),
                run_level: 运行档位。可选值：low (低), normal (正常), high (高),
                enclosure_id: 所属机框在存储设备上ID (1~255个字符),
                enclosure_name: 所属机框名称 (1~255个字符),
                zone_id: 所属Zone ID (1~255个字符)，仅OceanStor A800系列存储支持,
                zone_ip: 所属Zone IP地址 (1~255个字符)，仅OceanStor A800系列存储支持,
                zone_name: 所属Zone名称 (1~255个字符)，仅OceanStor A800系列存储支持,
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
    查询存储设备的硬盘信息列表

    Args:
        client: DME API 客户端。
        storage_id: 存储设备ID (1~36个字符, 满足uuid格式)。
        ids: 端口ID列表 (可选, List<string>, 数组最大成员个数: 100, 数组最小成员个数: 0)。
        name: 硬盘名称 (可选, 1~256个字符)。
        slot_number: 槽位号，位置 (可选, 1~256个字符)。支持模糊搜索。
        bom_id: BOM ID (可选, 1~256个字符)。
        health_status: 健康状态 (可选)。可选值：unknown (未知), normal (正常), fault (故障), pre_fail (即将故障), degraded (降级), single_link (单链路), no_redundant_link (无冗余链路), subhealthy (亚健康), offline (离线)。
        physical_type: 硬盘类型 (可选)。可选值：unknown (未知), sata (SATA), sas (SAS), nl_sas (NL-SAS), ssd (SSD), ssd_card (SSD卡), scm (SCM), nl_ssd (NL-SSD), fc (FC), lun (LUN), ata (ATA), flash (FLASH), vmdisk (VMDISK), sas_flash_vp (SAS-FLASH-VP), hdd (HDD)。
        new_physical_type: 真实的硬盘类型 (可选)。可选值：SAS, SATA, SSD, NL_SAS, SLC_SSD, MLC_SSD, FC_SED, SAS_SED, SATA_SED, SSD_SED, SCM_SED, NL_SAS_SED, SLC_SSD_SED, MLC_SSD_SED, NVMe_SSD, NVMe_SSD_SED, SCM, CAPACITY_OPTIMIZED_SSD, CAPACITY_OPTIMIZED_SSD_SED, unknown, sas_disk, sata_disk, ssd_card, ssd_card_virtual, ssd_disk, m2_disk, FC, ATA, FLASH, VMDISK, SAS_FLASH_VP, HDD。
        capacity: 总容量 (可选, 最大值: 9223372036854775807, 单位: GB)。
        role: 硬盘角色 (可选)。可选值：unknown (未知), free (空闲), member (成员), hotSpare (热备), cache (缓存), aggregate (聚合), broken (断开), foreign (外部), labelmaint (标签维护), maintenance (维护), shared (共享), spare (备用), unassigned (未分配), unsupported (不支持), remote (远程), mediator (中介)。
        disk_pool_name: 所属硬盘域名称 (可选, 1~256个字符)。支持模糊搜索。
        disk_pool_id: 硬盘池或硬盘域ID (可选, 1~64个字符)。仅华为存储设备，第三方设备支持该字段。
        storage_pool_id: 存储池ID (可选, 1~64个字符)。
        bar_code: 硬盘条码 (可选, 1~256个字符)。
        sn: 硬盘序列号 (可选, 1~256个字符)。仅华为存储设备，第三方设备支持该字段。
        speed: 转速 (可选, 最大值: 2147483647, 单位: RPM)。
        storage_ip: 所属设备ip地址 (可选, 1~255个字符)。
        management_ip: 管理设备ip地址 (可选, 1~256个字符)。
        node_name: 所属节点名称 (可选, 1~256个字符)。
        virtual_disk: 虚拟盘 (可选)。可选值：true, false。
        status: 运行状态 (可选)。可选值：unknown (未知), normal (正常), abnormal (故障), online (在线), offline (离线)。
        enclosure_name: 风扇所属存储设备的机框名称 (可选, 1~255个字符)。支持模糊搜索。
        zone_id: 所属存储设备的Zone id (可选, 1~255个字符)。仅OceanStor A800存储支持。
        sort_key: 排序字段 (可选)。可选值：capacity (总容量), speed (转速), remainLife (剩余寿命), name (硬盘名称), management_ip (管理设备ip地址), slot_number (位置)。
        sort_dir: 排序方向 (可选)。可选值：asc (升序), desc (降序)。
        page_no: 分页查询的页码 (可选, 1~2147483647, 默认值: 1)。
        page_size: 分页查询的每页大小 (可选, 1~1000, 默认值: 20)。

    Returns:
        DiskQueryResponse 对象，包含：
        - disks: 硬盘列表
        - total: 硬盘的数量
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
    查询存储设备存储池列表

    Args:
        client: DME API 客户端
        storage_id: 存储设备的ID（可选，1~64个字符）
        raw_id: 存储池在存储设备上的ID（可选，1~64个字符）
        zone_id: 所属Zone的ID（可选，1~256个字符），支持精确搜索，仅OceanStor A800存储支持
        page_no: 分页查询的页码（可选，1~10000，默认 1）
        page_size: 分页查询的每页大小（可选，1~1000，默认 10）
        sort_key: 排序字段（可选）。可选值：total_capacity (存储池总容量), consumed_capacity (存储池已用容量), free_capacity (存储池空闲容量，仅闪存存储), replication_capacity (存储池保护容量)
        sort_dir: 排序方向（可选）。可选值：asc (升序), desc (降序)

    Returns:
        {
            total: 存储池数量 (int32),
            datas: 存储池基础信息列表 (List<StoragePoolBasicInfo>)。参数格式如下：[{
                id: 存储池ID (1~32个字符),
                name: 存储池名称 (1~31个字符),
                raw_id: 存储池在存储设备上的ID (1~64个字符),
                storage_id: 存储设备ID (1~64个字符),
                storage_name: 存储设备名称 (1~127个字符),
                usage_type: 存储池用途。可选值：block-and-file (LUN/文件系统), block (块), file (文件), object (对象), hdfs (hdfs), converged (融合),
                total_capacity: 总容量，单位MB (number),
                free_capacity: 空闲容量，单位MB (number)，仅闪存存储、OceanStor A800设备支持,
                consumed_capacity: 已用容量，单位MB (number),
                replication_capacity: 数据保护容量，单位MB (number)，仅闪存存储支持,
                subscribed_capacity: 总订阅容量，单位MB (number)，仅闪存存储、分布式设备支持,
                lun_subscribed_capacity: LUN的订阅容量，单位MB (number)，仅闪存存储支持,
                filesystem_subscribed_capacity: 文件系统总订阅容量，单位MB (number)，仅OceanStor Dorado V6存储6.1.0及以上版本支持,
                health_status: 健康状态。可选值：normal (正常), fault (故障), degraded (降级), unknown (未知)。仅闪存存储及第三方存储支持,
                running_status: 运行状态。可选值：pre-copy (预拷贝), rebuilt (重构), online (在线), offline (离线), balancing (正在均衡), initializing (初始化中), deleting (删除中), unknown (未知)。仅闪存存储支持,
                pool_status: 存储池状态。可选值：normal (正常), fault (故障), write-protect (写保护), stopped (停止), fault-and-write-protect (故障且写保护), migrating-data (数据迁移), degraded (降级), rebuilding-data (数据重构), migrating-services (服务迁移), all-copies-failed (全副本故障), all-copies-failed-and-write-protect (全副本故障且写保护), deleting (删除中), deletion-failed (删除失败), unknown (未知)。仅分布式存储支持,
                disk_types: 硬盘类型列表 (List<string>)，仅闪存存储支持,
                capacity_usage: 容量利用率,
                redundancy_policy: 冗余策略。可选值：replication (副本), ec (EC)。仅FusionStorage、OceanStor 100D和OceanStor Pacific系列设备支持,
                num_data_units: EC数据块个数 (integer)，仅当冗余策略为ec时有效,
                num_fault_tolerance: EC允许故障节点数 (integer)，仅当冗余策略为ec时有效,
                num_parity_units: EC校验块个数 (integer)，仅当冗余策略为ec时有效,
                cache_media_type: 存储池缓存类型。可选值：ssd_card (SSD卡&NVMe SSD), ssd_disk (SSD盘), none (无缓存)。仅FusionStorage、OceanStor 100D、OceanStor A310和OceanStor Pacific系列设备支持,
                zone_id: 所属Zone的ID (1~64个字符)，仅OceanStor A800系列存储支持,
                zone_ip: 所属Zone的IP (1~256个字符)，仅OceanStor A800系列存储支持,
                zone_name: 所属Zone的名称 (1~256个字符)，仅OceanStor A80系列存储支持,
                raid_level: RAID级别列表 (List<string>)。可选值：RAID0, RAID1, RAID2, RAID3, RAID5, RAID6, RAID10, RAID50, RAID_TP。仅闪存存储、OceanDisk、OceanStor A800设备支持,
                disk_pool_id: 硬盘池或硬盘域ID (1~64个字符)。所属硬盘域支持闪存设备，所属硬盘池支持Pacific、A310设备，OceanStor A800设备支持,
                disk_pool_name: 硬盘池或硬盘域名称 (1~256个字符),
                media_type: 存储池主存类型。可选值：sas_disk (SAS盘), sata_disk (SATA盘), ssd_card (SSD卡&NVMe SSD), ssd_disk (SSD盘)。仅OceanStor Pacific、OceanStor A310、OceanStor 100D设备支持,
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
    查询 HyperScale 存储池列表

    Args:
        client: DME API 客户端
        raw_id: 存储池在存储设备上的ID（可选，1~64个字符），支持精确搜索
        name: HyperScale存储池名称（可选，1~256个字符），支持模糊搜索
        local_pool_id: HyperScale存储池下本地存储池ID（可选，0~64个字符），支持过滤指定本地存储池关联的HyperScale存储池
        health_status: 健康状态（可选）。可选值：normal (正常), faulty (故障), degraded (降级)
        running_status: 运行状态（可选）。可选值：pre_copy (预拷贝), rebuilding (重构), online (在线), offline (离线), balancing (正在均衡), initializing (初始化中), deleting (删除中)
        storage_id: 存储设备ID（可选，0~64个字符）
        description: HyperScale存储池描述（可选，0~256个字符）
        page_no: 分页查询的页码（可选，1~10000，默认 1）
        page_size: 分页查询的每页大小（可选，1~1000，默认 20）
        sort_key: 排序字段（可选）。可选值：raw_id (ID), total_capacity (存储池总容量), consumed_capacity (已用容量), capacity_usage (容量利用率), free_capacity (空闲容量), subscribed_capacity_percentage (订阅率)
        sort_dir: 排序方向（可选）。可选值：asc (升序), desc (降序)

    Returns:
        {
            total: HyperScale存储池总数 (int32),
            data: HyperScale存储池列表 (List<HyperScalePoolInfo>)。参数格式如下：[{
                id: HyperScale存储池ID (1~64个字符),
                raw_id: 存储池在存储设备上的ID (1~64个字符),
                name: HyperScale存储池名称 (1~256个字符),
                description: HyperScale存储池描述 (1~256个字符),
                storage_id: 存储设备ID (1~64个字符),
                storage_ip: 存储设备IP (1~255个字符),
                storage_name: 存储设备名称 (1~127个字符),
                health_status: 健康状态。可选值：normal (正常), faulty (故障), degraded (降级),
                running_status: 运行状态。可选值：pre_copy (预拷贝), rebuilding (重构), online (在线), offline (离线), balancing (正在均衡), initializing (初始化中), deleting (删除中),
                total_capacity: 总容量，单位MB (number),
                consumed_capacity: 已用容量，单位MB (number),
                capacity_usage: 容量利用率 (number),
                free_capacity: 空闲容量，单位MB (number),
                subscribed_capacity_percentage: 订阅率 (number),
                subscribed_capacity: 总订阅容量，单位MB (number),
                used_subscribed_capacity: 已使用订阅容量，单位MB (number),
                redundancy_strategy: 冗余策略。可选值：disk (盘级冗余), distributed_ec (分布式EC),
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
    查询存储设备的节点列表

    Args:
        client: DME API 客户端
        storage_id: 所属存储设备id（可选，1~64个字符），支持过滤
        raw_id: 节点在存储设备上的ID（可选，1~64个字符）
        storage_name: 所属存储设备名称（可选，1~255个字符），支持过滤
        name: 节点名称（可选，1~256个字符），支持模糊查询（不区分大小写）
        ids: 节点ID列表（可选，List<string>，数组最大成员个数：100）
        mgmt_ip: 节点管理IP地址（可选，1~256个字符），支持模糊查询（不区分大小写）
        frame_number: 机柜/机架号（可选，1~256个字符），支持模糊查询（不区分大小写）
        slot_number: 槽位/机架内槽位号（可选，1~256个字符），支持模糊查询（不区分大小写）
        status: 节点状态（可选）。可选值：UNKNOWN (未知), NORMAL (正常), FAULT (故障), PRE_FAIL (即将故障), PARTIALLY_DAMAGED (部分损坏), DEGRADED (降级), BAD_SECTORS_FOUND (有坏块), BIT_ERRORS_FOUND (有误码), CONSISTENT (一致), INCONSISTENT (不一致), BUSY (繁忙), NO_INPUT (无输入), LOW_BATTERY (电量不足), SINGLE_LINK_FAULT (单链路故障)
        roles: 节点角色列表（可选，List<string>，数组最大成员个数：10）。可选值：management (管理), storage (存储), compute (VBS计算), replication (复制), paxos (控制), dpc_compute (DPC计算)
        page_no: 分页查询的页码（可选，1~10000，默认 1）
        page_size: 分页查询的每页大小（可选，1~1000，默认 20）
        sort_key: 排序字段（可选）。可选值：name (节点名称), mgmt_ip (节点管理IP地址)
        sort_dir: 排序方向（可选）。可选值：asc (升序), desc (降序)

    Returns:
        {
            total: 节点的数量 (integer),
            nodes: 节点列表 (List<StorageNodeBaseInfo>)。参数格式如下：[{
                id: 节点id (1~64个字符),
                name: 节点名称 (1~255个字符),
                raw_id: 节点在存储设备上的ID (1~64个字符),
                mgmt_ip: 节点管理IP地址 (1~255个字符),
                status: 节点状态 (1~255个字符)。可选值：UNKNOWN (未知), NORMAL (正常), FAULT (故障), PARTIALLY_DAMAGED (部分损坏),
                node_model: 节点型号 (1~255个字符)。例如：DataTurbo，OceanStor Pacific，RH5288 V3,
                frame_number: 机柜/机架号 (1~255个字符),
                slot_number: 槽位/机架内槽位号 (1~255个字符),
                roles: 节点角色列表 (List<string>)。可选值：management (管理), storage (存储), compute (VBS计算), replication (复制), paxos (控制), dpc_compute (DPC计算),
                node_sn: 序列号信息 (1~255个字符),
                storage_id: 所属存储设备id (1~64个字符),
                storage_name: 所属存储设备名称 (1~255个字符),
                eos_time: 存储EOS时间 (int64)，格林威治时间1970年01月01日00时00分00秒起至现在的总毫秒数,
                installation_status: 存储软件安装状态。可选值：installed (已安装存储软件), not_installed (未安装存储软件),
                ip_address_list: 节点IP地址列表 (List<StorageNodeIpInfo>)。参数格式如下：[{
                    ip_address: 节点IP地址 (1~256个字符),
                    usage: 节点IP地址用途列表 (List<string>)。可选值：storage_frontend (存储前端网络IP), storage_backend (存储后端网络IP), management_external_float (管理外部网络浮动IP), management_internal_float (管理内部网络浮动IP), management_external (管理外部网络IP), management_internal (管理内部网络IP), replication (复制网络IP), quorum (仲裁网络IP), iscsi (ISCSI网络IP),
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
    查询存储设备电源详情信息，仅支持OceanStor A800存储。

    Args:
        client: DME API 客户端
        storage_id: 所属存储设备ID（必选，1~64个字符）
        health_status: 健康状态（可选）。可选值：unknown (未知), normal (正常), faulty (故障), inconsistent (不一致), no_input (无输入)
        running_status: 运行状态（可选）。可选值：unknown (未知), normal (正常), running (运行), online (在线), offline (离线)
        power_type: 电源类型（可选）。可选值：dc (直流电源), ac (交流电源), hv (高压直流电源)
        power_mode: 电源模式（可选）。可选值：balanced_power (均衡电源), active_power (主电源), standby_power (备电源)
        location: 位置（可选，1~256个字符），支持模糊匹配
        model: 型号（可选，1~256个字符），支持模糊匹配
        sn: 序列号（可选，1~256个字符），支持模糊匹配
        enclosure_name: 所属机框名称（可选，1~256个字符），支持模糊匹配
        zone_id: 所属Zone ID（可选，1~64个字符），仅OceanStor A800系列存储支持
        page_no: 分页查询的页码（可选，1~2147483647，默认 1）
        page_size: 分页查询的每页大小（可选，1~1000，默认 20）

    Returns:
        {
            total: 电源的数量 (int32),
            storage_powers: 电源列表 (List<StoragePowerInfo>)。参数格式如下：[{
                name: 名称 (1~255个字符),
                location: 位置 (1~255个字符),
                health_status: 健康状态。可选值：unknown (未知), normal (正常), faulty (故障), inconsistent (不一致), no_input (无输入),
                running_status: 运行状态。可选值：unknown (未知), normal (正常), running (运行), online (在线), offline (离线),
                power_type: 电源类型。可选值：dc (直流电源), ac (交流电源), hv (高压直流电源),
                model: 型号 (1~255个字符),
                sn: 序列号 (1~255个字符),
                manufacturer: 生产厂商 (1~255个字符),
                enclosure_name: 所属机框名称 (1~255个字符),
                production_date: 生产日期 (1~255个字符),
                version: 版本 (1~255个字符),
                bom_code: 电源模块BOM编码 (1~255个字符),
                power_mode: 电源模式。可选值：balanced_power (均衡电源), active_power (主电源), standby_power (备电源),
                zone_name: 所属Zone名称 (1~255个字符)，仅OceanStor A800系列存储支持,
                zone_id: 所属Zone ID (1~255个字符)，仅OceanStor A800系列存储支持,
                zone_ip: 所属Zone IP地址 (1~255个字符)，仅OceanStor A800系列存储支持,
                storage_id: 所属存储设备ID (1~64个字符),
                storage_name: 所属存储设备名称 (1~128个字符),
                storage_ip: 所属存储设备IP地址 (1~32个字符),
                storage_sn: 所属存储设备序列号 (1~64个字符),
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
    查询存储设备功率数据

    Args:
        client: DME API 客户端
        start_time: 开始时间戳（必选，13位数字毫秒时间戳，正则 ^([0-9]){13}$）
        end_time: 结束时间戳（必选，13位数字毫秒时间戳，正则 ^([0-9]){13}$）
        storage_ids: 存储ID列表（必选，List<string>，数组最大成员个数：300）
        time_granularity: 时间粒度（必选）。可选值：HOUR (小时), DAY (天), MONTH (月)

    Returns:
        {
            storage_power_list: 存储功率列表 (List<StoragePower>)。参数格式如下：[{
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
    修改存储设备（仅支持修改录入的离线存储设备信息）

    Args:
        client: DME API 客户端。
        storage_id: 存储设备 ID（必填）。
        name: 设备名称 (可选, 1~256个字符)。只能包含半角字母、半角数字、"_"、"-"、"."、中文字符。
        ip: 设备IP地址 (可选, 0~128个字符, 支持IPv4与IPv6格式, 也可为空字符串)。
        vendor: 厂商 (可选, 0~128个字符)。
        model: 产品型号 (可选, 0~128个字符)。
        version: 版本信息 (可选, 0~64个字符)。
        patch_version: 补丁版本信息 (可选, 0~64个字符)。
        location: 设备位置 (可选, 0~512个字符)。
        maintenance_start: 维护开始时间 (可选, 格式是毫秒级时间戳)。需要和维护过保时间一起出现并且数值小于维护过保时间。
        maintenance_overtime: 维护过保时间 (可选, 格式是毫秒级时间戳)。需要和维护开始时间一起出现并且数值大于维护开始时间。
        total_capacity: 裸容量 (可选, -1~2147483647, 单位MB)。存储设备中所有硬盘的物理容量之和，-1表示无裸容量。
        total_effective_capacity: 可得容量 (可选, -1~2147483647, 单位MB)。存储设备可写入的用户数据总量，-1表示无可得容量。
        total_pool_capacity: 可用容量 (可选, -1~2147483647, 单位MB)。存储设备实际可用的硬盘物理空间（扣除RAID、元数据等消耗），-1表示无可用容量。
        used_capacity: 已用容量 (可选, -1~2147483647, 单位MB)。存储设备中所有存储池的已使用容量之和，-1表示无已用容量。
        free_capacity: 空闲容量 (可选, -1~2147483647, 单位MB)。存储设备的可用容量与已用容量的差值，-1表示无空闲容量。
        subscription_capacity: 订阅容量 (可选, -1~2147483647, 单位MB)。存储设备中所有存储池的订阅容量之和，-1表示无已订阅容量。
        tag_ids: 标签ID列表 (可选, string, 0~512个字符)。数组格式字符串，最多支持10个标签，空数组代表移除存储设备关联的所有标签。

    Returns:
        响应数据（修改成功返回空字典）

    Raises:
        ValueError: 必填参数缺失
    """
    if not storage_id:
        raise ValueError("参数 storage_id 是必填的")

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
    # 修改接口返回空响应，返回空字典表示成功
    return response if response else {}


def app_type_list(client: DMEAPIClient, storage_id: str, 
                 create_type: int = None, template_type: int = None, 
                 pool_id: str = None) -> dict:
    """
    查询指定存储设备的应用类型
    
    仅 Dorado 类型设备支持。
    
    Args:
        client: DME API 客户端。
        storage_id: 存储设备 id (1~36个字符, 满足uuid格式)。
        create_type: 创建类型 (可选, 0~1)。可选值：0 (系统预置), 1 (用户定义)。不传返回所有类型。
        template_type: 应用类型分类 (可选, 0~1)。可选值：0 (LUN类型), 1 (NAS类型)。不传默认LUN类型。
        pool_id: 存储池id (可选, 1~64个字符, 字母和数字)。
    
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
    查询指定存储设备的控制器信息
    
    查询存储设备的控制器列表信息。
    
    Args:
        client: DME API 客户端
        storage_id: 存储设备 ID（必选，1~36 个字符，UUID 格式或 32 位十六进制）
    
    Returns:
        响应数据，包含 total 和 controllers 字段
        - total: 控制器总数
        - controllers: 控制器列表，包含 id, name, status, type 等信息
    """
    url = "/rest/storagemgmt/v1/storages/{storage_id}/controllers"
    
    response = client.get(url, params={"storage_id": storage_id})
    return response


def disk_pool_list(client: DMEAPIClient, storage_id: str = None, page_no: int = 1,
                   page_size: int = 20) -> dict:
    """
    批量查询硬盘域

    Args:
        client: DME API 客户端
        storage_id: 存储设备 ID（可选，1~64 个字符），支持过滤
        page_no: 分页查询的页码（可选，1~2147483647，默认 1）
        page_size: 分页查询的每页大小（可选，1~1000，默认 20）

    Returns:
        {
            total: 硬盘域数量 (int32),
            disk_pools: 硬盘域列表 (List<DiskPoolInfo>)。参数格式如下：[{
                    id: 硬盘域id (1~64个字符),
                    raw_id: 硬盘域在设备上的id (1~64个字符),
                    name: 硬盘域名称 (1~128个字符),
                    running_status: 运行状态。可选值：online (在线), offline (离线), pre_copy (预拷贝), reconstruction (重构), balancing (正在均衡), initializing (初始化中), deleting (删除中), unknown (未知),
                    health_status: 健康状态。可选值：normal (正常), fault (故障), degraded (降级), unknown (未知),
                    total_capacity: 总可用裸容量，单位MB (number),
                    spare_capacity: 总热备裸容量，单位MB (number),
                    used_capacity: 已分配裸容量，单位MB (number),
                    used_spare_capacity: 已用热备裸容量，单位MB (number),
                    free_capacity: 空闲容量，单位MB (number),
                    storage_id: 所属存储设备id (1~64个字符),
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


def enclosure_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 20,
                   storage_id: str = None, name: str = None, location: str = None,
                   health_status: list = None, zone_name: str = None,
                   zone_id: list = None, running_status: list = None,
                   power_mode: list = None, esn: str = None, mac: str = None,
                   sort_key: str = None, sort_dir: str = None) -> dict:
    """
    批量查询机框信息

    Args:
        client: DME API 客户端
        page_no: 分页查询的页码（可选，1~2147483647，默认 1）
        page_size: 分页查询的每页大小（可选，1~1000，默认 20）
        storage_id: 所属存储设备ID（可选，1~64个字符）
        name: 名称（可选，1~256个字符），支持模糊匹配
        location: 位置（可选，1~256个字符），支持模糊匹配
        health_status: 健康状态列表（可选，List<string>，数组最大成员个数：3）。可选值：unknown (未知), normal (正常), faulty (故障)
        zone_name: 所属Zone名称（可选，1~255个字符），仅OceanStor A800系列存储支持，支持模糊匹配
        zone_id: 所属Zone ID列表（可选，List<string>，数组最大成员个数：100），仅OceanStor A800系列存储支持
        running_status: 运行状态列表（可选，List<string>，数组最大成员个数：7）。可选值：unknown (未知), normal (正常), running (运行), sleep_in_high_temperature (高温休眠), online (在线), offline (离线)
        power_mode: 电源模式列表（可选，List<string>，数组最大成员个数：2）。可选值：load_balance (负载均衡模式), active_standby_power (主备供电模式)
        esn: 机框序列号（可选，1~256个字符），支持模糊匹配
        mac: MAC地址（可选，1~256个字符），支持模糊匹配
        sort_key: 排序字段（可选）。可选值：temperature (温度)
        sort_dir: 排序方向（可选）。可选值：asc (升序), desc (降序)。默认按升序返回

    Returns:
        {
            total: 机框数量 (integer),
            data: 机框列表 (List<EnclosureItem>)。参数格式如下：[{
                    id: 机框ID (1~64个字符),
                    raw_id: 机框在存储设备上ID (1~64个字符),
                    name: 名称 (1~256个字符),
                    model: 型号 (1~32个字符)。可选值：0 (BMC控制框), 1 (2U 双控 6Gbit/s SAS 12盘位 3.5英寸控制框), 2 (2U 双控 6Gbit/s SAS 24盘位 2.5英寸控制框), 16 (2U 6Gbit/s SAS 12盘位 3.5英寸硬盘框), 17 (2U SAS 24盘级联框), 18 (4U 6Gbit/s SAS 24盘位 3.5英寸硬盘框), 19 (4U FC 24盘级联框), 20 (1U PCIe数据交换机), 21 (4U 6Gbit/s SAS 75盘位 3.5英寸硬盘框), 22 (SVP), 23 (2U 双控 6Gbit/s SAS 12盘位 3.5英寸控制框), 24 (2U 6Gbit/s SAS 25盘位 2.5英寸硬盘框), 25 (4U 6Gbit/s SAS 24盘位 3.5英寸硬盘框), 26 (2U 双控 6Gbit/s SAS 25盘位 2.5英寸控制框), 37 (2U 双控 6Gbit/s SAS 12盘位 3.5英寸控制框), 38 (2U 双控 6Gbit/s SAS 25盘位 2.5英寸控制框), 39 (4U 12Gbit/s SAS 75盘位 3.5英寸硬盘框), 40 (2U 双控 12Gbit/s SAS 25盘位 2.5英寸控制框), 65 (2U 12Gbit/s SAS 25盘位 2.5英寸硬盘框), 66 (4U 12Gbit/s SAS 24盘位 3.5英寸硬盘框), 67 (2U SAS 25盘位 2.5英寸硬盘框), 69 (4U SAS 24盘位 3.5英寸硬盘框), 96 (3U 双控控制框), 97 (6U 四控控制框), 98 (2U SSD 25盘级联框), 99 (2U 双控 12Gbit/s NVMe 25盘位 2.5英寸控制框), 101 (2U SSD NVMe 25盘位 2.5英寸硬盘框), 112 (4U 四控控制框), 113 (2U 双控 SAS 25盘位 2.5英寸控制框), 114 (2U 双控 SAS 12盘位 3.5英寸控制框), 115 (2U 双控 NVMe 36盘位控制框), 116 (2U 双控 SAS 25盘位 2.5英寸控制框), 117 (2U 双控 SAS 12盘位 3.5英寸控制框), 118 (2U SAS 25盘位 2.5英寸智能硬盘框), 119 (2U SAS 12盘位 3.5英寸智能硬盘框), 120 (2U NVMe 36盘位智能硬盘框), 122 (2U 双控 NVMe 25盘位 2.5英寸控制框), 132 (4U 双控 4盘位2.5英寸 6盘位3.5英寸 控制框), 133 (4U 双控 NVMe 12盘位 2.5英寸 控制框), 135 (4U 双控 10盘位 2.5英寸控制框), 143 (8U NVME 双控 64盘位 2.5英寸 控制框),
                    height: 高度，单位U (integer),
                    location: 机框的位置 (1~128个字符),
                    logic_type: 类型。可选值：disk_enclosure (硬盘框), controller_enclosure (控制框), data_switch (数据交换机), management_switch (管理交换机), management_server (管理服务器),
                    health_status: 健康状态。可选值：unknown (未知), normal (正常), faulty (故障),
                    running_status: 运行状态。可选值：unknown (未知), normal (正常), running (运行), sleep_in_high_temperature (高温休眠), online (在线), offline (离线), abnormal (异常),
                    storage_id: 所属存储设备ID (1~64个字符),
                    storage_name: 所属存储设备名称 (1~128个字符),
                    storage_ip: 所属存储设备IP地址 (1~32个字符),
                    storage_sn: 所属存储设备序列号 (1~64个字符),
                    storage_location: 所属存储设备的位置 (0~512个字符),
                    zone_name: 所属Zone名称 (0~512个字符)，仅OceanStor A800系列存储支持,
                    zone_ip: 所属Zone IP地址 (1~128个字符)，仅OceanStor A800系列存储支持,
                    zone_id: 所属Zone ID (0~512个字符)，仅OceanStor A800存储支持,
                    esn: 机框序列号 (0~512个字符),
                    mac: MAC地址 (0~512个字符),
                    power_mode: 电源模式。可选值：load_balance (负载均衡模式), active_standby_power (主备供电模式),
                    bar_code: 条形码 (0~256个字符),
                    board_type: 单板类型 (0~128个字符),
                    description: 描述 (0~1024个字符),
                    temperature: 温度，单位°C (0~128个字符),
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
    批量查询存储侧启动器对象

    批量查询存储侧的启动器对象列表。

    Args:
        client: DME API 客户端
        page_size: 分页查询的个数 (可选, 1~1000, 默认100)
        page_no: 分页查询的页码 (可选, 最小值1, 默认1)
        raw_id: 启动器WWPN/IQN/NQN (可选, 0~256个字符, 支持模糊匹配)
        alias: 启动器别名 (可选, 0~256个字符, 支持模糊匹配)
        status: 启动器状态 (可选)。可选值：unknown (未知), online (在线), offline (离线)
        associated_host_name: 启动器关联主机名称 (可选, 0~256个字符, 支持模糊匹配)
        associated_host_id: 启动器关联主机ID (可选, 0~64个字符; 空字段查询未添加到主机的启动器)
        multipath_type: 第三方多路径策略 (可选, 仅针对非Dorado V6产品)。可选值：default (默认), third_party (第三方多路径)
        protocol: 启动器类型 (可选)。可选值：fc, iscsi, nvme_over_roce, sas, nvme_over_fabric, unknown
        support_provisioning: 是否支持发放 (可选)。可选值：true, false
        vstore_raw_id: 租户ID (可选)
        vstore_name: 租户名称 (可选)
        storage_id: 存储设备ID (可选, 0~64个字符)

    Returns:
        启动器列表
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
    批量删除存储设备的启动器对象

    Args:
        client: DME API 客户端
        initiator_ids: 启动器 ID 列表（必选，1~100 个）
        task_remarks: 任务备注（可选，最多 1024 字符）

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
    修改存储侧启动器对象

    修改启动器，该操作会修改存储设备上指定的启动器。

    Args:
        client: DME API 客户端
        initiator_id: 启动器 ID (必选)
        vstore_id: 租户ID (可选, 1~64个字符; 设备为OceanStor V300R006C30/V500R007C20/Dorado 6.1.3及以上时有效)
        alias: 启动器别名 (可选, 0~31个字符, 支持字母数字._-和中文字符)
        multi_path: ModifyMultiPathRequestParam对象 (可选; 设备为OceanStor V300R003C20/V500R007C20/Dorado V300R001C01及以上支持)。属性格式如下：{
                multi_path_type: 启动器多路径类型 (可选)。可选值：default (默认), third_party (第三方多路径),
                path_type: 启动器路径类型 (条件必传, 当multi_path_type为third_party时必传)。可选值：optimal_path (优选路径), non_optimal_path (非优选路径),
                failover_mode: 启动器切换模式 (条件必传, 当multi_path_type为third_party时必传)。可选值：early_version_alua, common_alua, alua_not_used, special_alua,
                special_mode_type: 特殊模式类型 (可选, 切换模式为特殊模式时有效)。可选值：0 (特殊模式0), 1 (特殊模式1), 2 (特殊模式2), 3 (特殊模式3)
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


# ============ 认证用户 (account) 子主题函数 ============


def account_show_local_users(client: DMEAPIClient, storage_id: str, vstore_raw_id: str = None,
                     name: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询指定存储设备本地认证用户的信息

    Args:
        client: DME API 客户端
        storage_id: 存储设备 ID（必填，1~36 个字符）
        vstore_raw_id: 本地认证用户所属租户在设备上 ID（可选）
        name: 本地认证用户名称，支持模糊查询（可选）
        page_no: 分页查询的页码，默认 1（可选）
        page_size: 分页查询的每页大小，默认 20（可选）

    Returns:
        本地认证用户信息列表，包含 total 和 local_users
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
    创建本地认证用户

    Args:
        client: DME API 客户端
        storage_id: 创建本地认证用户所属存储设备 ID (1~36个字符, 必填)
        name: 本地认证用户名称 (1~255个字符, 必填)
        description: 本地认证用户描述 (1~255个字符, 可选)
        password: 本地认证用户密码 (1~255个字符, 必填)
        primary_group_raw_id: 本地认证用户所归属的用户组在设备上 ID (1~64个字符, 必填)
        group_names: 创建的本地认证用户所属的临时用户组名称列表 (List<string>, 数组最小成员个数: 0, 数组最大成员个数: 31, 可选)
        vstore_id: 本地认证用户所属的租户 ID (1~64个字符, 可选。条件必传，当创建的本地认证用户属于租户时必传)

    Returns:
        创建结果
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
    创建指定存储设备 UNIX 认证用户

    Args:
        client: DME API 客户端
        storage_id: 创建 UNIX 认证用户所属存储设备 ID (1~36个字符, 必填)
        name: UNIX 认证用户名称 (1~255个字符, 必填)
        raw_id: UNIX 认证用户在设备上 ID (int64, 0~4294967295, 可选)
        description: UNIX 认证用户描述 (1~255个字符, 可选)
        password: UNIX 认证用户密码 (1~255个字符, 可选)
        status_enabled: UNIX 认证用户状态 (boolean, 可选)。可选值：true (启动), false (锁定)
        primary_group_raw_id: 创建的 UNIX 认证用户所归属的用户组在设备上 ID (1~64个字符, 必填)
        vstore_raw_id: UNIX 认证用户所属的租户在设备上 ID (1~64个字符, 可选。条件必传，当创建的 UNIX 认证用户属于租户时必传)

    Returns:
        创建结果
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
    创建指定存储设备 Windows 认证用户

    Args:
        client: DME API 客户端
        storage_id: 创建 Windows 认证用户所属存储设备 ID (1~36个字符, 必填)
        name: Windows 认证用户名称 (1~255个字符, 必填)
        raw_id: Windows 认证用户在设备上 ID (int64, 1000~4294967295, 可选)
        description: Windows 认证用户描述 (1~255个字符, 可选)
        password: Windows 认证用户密码 (1~255个字符, 必填)
        status_enabled: Windows 认证用户状态 (boolean, 可选)。可选值：true (启用), false (锁定)
        vstore_raw_id: 创建的 Windows 认证用户所属的租户在设备上 ID (1~64个字符, 可选。条件必传，当 Windows 认证用户属于租户时必传)

    Returns:
        创建结果
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
    查询指定存储设备 UNIX 认证用户的信息

    Args:
        client: DME API 客户端
        storage_id: 存储设备 ID（必填，1~36 个字符）
        vstore_raw_id: UNIX 认证用户所属租户在设备上 ID（可选）
        name: UNIX 认证用户名称，支持模糊查询（可选）
        page_no: 分页查询的页码，默认 1（可选）
        page_size: 分页查询的每页大小，默认 20（可选）

    Returns:
        UNIX 认证用户信息列表，包含 total 和 unix_users
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
    查询指定存储设备 Windows 认证用户的信息

    Args:
        client: DME API 客户端
        storage_id: 存储设备 ID（必填，1~36 个字符）
        vstore_raw_id: Windows 认证用户所属租户在设备上 ID（可选）
        name: Windows 认证用户名称，支持模糊查询（可选）
        page_no: 分页查询的页码，默认 1（可选）
        page_size: 分页查询的每页大小，默认 20（可选）

    Returns:
        Windows 认证用户信息列表，包含 total 和 windows_users
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
    查询指定存储设备本地认证用户组的信息

    Args:
        client: DME API 客户端
        storage_id: 存储设备 ID（必填，1~36 个字符）
        vstore_raw_id: 本地认证用户组所属租户在设备上 ID（可选）
        name: 本地认证用户组名称，支持模糊查询（可选）
        page_no: 分页查询的页码，默认 1（可选）
        page_size: 分页查询的每页大小，默认 20（可选）

    Returns:
        本地认证用户组信息列表，包含 total 和 local_user_groups
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
    查询指定存储设备 UNIX 认证用户组的信息

    Args:
        client: DME API 客户端
        storage_id: 存储设备 ID（必填，1~36 个字符）
        vstore_raw_id: UNIX 认证用户组所属租户在设备上 ID（可选）
        name: UNIX 认证用户组名称，支持模糊查询（可选）
        page_no: 分页查询的页码，默认 1（可选）
        page_size: 分页查询的每页大小，默认 20（可选）

    Returns:
        UNIX 认证用户组信息列表，包含 total 和 unix_user_groups
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
    查询指定存储设备 Windows 认证用户组的信息

    Args:
        client: DME API 客户端
        storage_id: 存储设备 ID（必填，1~36 个字符）
        vstore_raw_id: Windows 认证用户组所属租户在设备上 ID（可选）
        name: Windows 认证用户组名称，支持模糊查询（可选）
        page_no: 分页查询的页码，默认 1（可选）
        page_size: 分页查询的每页大小，默认 20（可选）

    Returns:
        Windows 认证用户组信息列表，包含 total 和 windows_user_groups
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


# ============ QoS 子主题函数 ============


def qos_list(client: DMEAPIClient, storage_id: str, name: str = None,
             raw_id: str = None, enable_status: bool = None,
             running_status: str = None, zone_id: str = None,
             resource_type_list: list = None, vstore_id: str = None,
             vstore_name: str = None, alarm_status: str = None,
             io_policy_type: str = None, page_no: int = 1,
             page_size: int = 10, sort_key: str = None,
             sort_dir: str = None) -> dict:
    """
    批量查询 QoS 策略

    Args:
        client: DME API 客户端
        storage_id: 存储设备 ID（必选）
        name: QoS 策略名称（可选，1~256 字符）
        raw_id: QoS 策略设备侧 ID（可选）
        enable_status: 激活状态（可选，true/false）
        running_status: 运行状态（可选，running/inactive/waiting）
        zone_id: 所属 ZONE 的 ID（可选）
        resource_type_list: 控制的资源类型列表（可选，file_system/vstore/none）
        vstore_id: 所属租户 ID（可选）
        vstore_name: 所属租户名称（可选）
        alarm_status: 告警状态（可选，normal/event/alarm/invalid）
        io_policy_type: IO 策略类型（可选，total_perf_upper_limit/read_or_write_upper_limit）
        page_no: 页码（可选，默认 1）
        page_size: 每页数量（可选，默认 10，最大 1000）
        sort_key: 排序字段（可选，name/raw_id）
        sort_dir: 排序方式（可选，asc/desc）
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
    查询指定 QoS 策略详情

    Args:
        client: DME API 客户端
        qos_policy_id: QoS 策略 ID（必选）
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
        client: DME API 客户端
        name: QoS 策略名称（必选，1~31 字符）
        storage_id: 存储设备 ID（必选）
        resource_type: 控制的资源类型（必选，file_system/vstore）
        resource_ids: 控制的资源 ID 列表（必选，数组 1~512 个成员）
        description: 描述（可选，1~255 字符）
        zone_id: 所属 ZONE 的 ID（可选，A 系列存储必选）
        vstore_id: 所属租户 ID（可选，resource_type 为 file_system 时必选）
        enable_status: 激活状态（可选，enable/disable，默认 enable）
        io_policy_type: IO 策略类型（可选，total_perf_upper_limit/read_or_write_upper_limit）
        min_bandwidth: 最小带宽 MB/s（可选）
        max_bandwidth: 最大带宽 MB/s（可选）
        burst_bandwidth: 突发带宽 MB/s（可选，需大于 max_bandwidth）
        min_iops: 最小 IOPS（可选）
        max_iops: 最大 IOPS（可选）
        burst_iops: 突发 IOPS（可选，需大于 max_iops）
        burst_time: 最大突发持续时间秒（可选，1~999999999）
        latency: IO 时延指标微秒（可选，500/1500）
        max_read_bandwidth: 最大读带宽 MB/s（可选）
        max_write_bandwidth: 最大写带宽 MB/s（可选）
        burst_read_bandwidth: 突发读带宽 MB/s（可选）
        burst_write_bandwidth: 突发写带宽 MB/s（可选）
        max_read_iops: 最大读 IOPS（可选）
        max_write_iops: 最大写 IOPS（可选）
        burst_read_iops: 突发读 IOPS（可选）
        burst_write_iops: 突发写 IOPS（可选）
        alarm_switch: 告警开关（可选，on/off）
        alarm_level: 告警级别（可选，event/alarm）
        alarm_threshold: 告警阈值%（可选，0~100）
        resume_threshold: 恢复阈值%（可选，0~100）
        schedule_policy: 调度策略（可选，once/daily/weekly）
        schedule_start_date: 生效开始日期（可选，yyyy-MM-dd）
        start_time: 生效开始时间（可选，hh:mm）
        duration: 生效持续时间秒（可选，1800~86400）
        weekly_days: 周调度策略（可选，[0-6] 对应周日到周六）
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
        client: DME API 客户端
        qos_policy_id: QoS 策略 ID（必选）
        name: QoS 策略名称（可选）
        description: 描述（可选）
        io_policy_type: IO 策略类型（可选）
        min_bandwidth: 最小带宽 MB/s（可选）
        max_bandwidth: 最大带宽 MB/s（可选）
        burst_bandwidth: 突发带宽 MB/s（可选）
        min_iops: 最小 IOPS（可选）
        max_iops: 最大 IOPS（可选）
        burst_iops: 突发 IOPS（可选）
        burst_time: 最大突发持续时间秒（可选）
        latency: IO 时延指标微秒（可选）
        max_read_bandwidth: 最大读带宽 MB/s（可选）
        max_write_bandwidth: 最大写带宽 MB/s（可选）
        burst_read_bandwidth: 突发读带宽 MB/s（可选）
        burst_write_bandwidth: 突发写带宽 MB/s（可选）
        max_read_iops: 最大读 IOPS（可选）
        max_write_iops: 最大写 IOPS（可选）
        burst_read_iops: 突发读 IOPS（可选）
        burst_write_iops: 突发写 IOPS（可选）
        alarm_switch: 告警开关（可选）
        alarm_level: 告警级别（可选）
        alarm_threshold: 告警阈值%（可选）
        resume_threshold: 恢复阈值%（可选）
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
        client: DME API 客户端
        qos_policy_ids: QoS 策略 ID 列表（必选，1~100 个）
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
        client: DME API 客户端
        qos_policy_ids: QoS 策略 ID 列表（必选）
    """
    url = "/rest/storagepolicy/v1/qos/active"

    payload = {
        'qos_ids': qos_policy_ids
    }

    response = client.post(url, body=payload)
    return response


def qos_deactivate(client: DMEAPIClient, qos_policy_ids: list) -> dict:
    """
    批量取消激活 QoS 策略

    取消激活一个或多个 QoS 策略。

    Args:
        client: DME API 客户端
        qos_policy_ids: QoS 策略 ID 列表（必选）
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
    QoS 策略关联控制资源

    将一个或多个资源关联到 QoS 策略。

    Args:
        client: DME API 客户端
        qos_policy_id: QoS 策略 ID（必选）
        resource_ids: 资源 ID 列表（必选）
        resource_type: 资源类型（必选，file_system/vstore）
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
    QoS 策略解关联控制资源

    将资源从 QoS 策略解关联。

    Args:
        client: DME API 客户端
        qos_policy_id: QoS 策略 ID（必选）
        resource_ids: 资源 ID 列表（必选）
        resource_type: 资源类型（必选）
    """
    url = "/rest/storagepolicy/v1/qos/{qos_policy_id}/resources/unassociate"

    payload = {
        'resource_ids': resource_ids,
        'resource_type': resource_type
    }

    response = client.post(url, params={"qos_policy_id": qos_policy_id})
    return response


# ============ 存储逻辑端口 (logic_port) 子主题函数 ============


def logic_port_list(client: DMEAPIClient, storage_id: str = None, vstore_raw_id: str = None,
                    zone_raw_id: str = None, scope: str = None, page_no: int = 1,
                    page_size: int = 100) -> dict:
    """
    查询存储设备的逻辑端口列表

    Args:
        client: DME API 客户端
        storage_id: 存储设备ID（可选，1~64个字符）
        vstore_raw_id: vStore在存储设备上的id（可选，1~64个字符）
        zone_raw_id: 所属Zone在设备上的ID（可选，1~64个字符），仅OceanStor A800系列存储支持
        scope: 范围（可选）。可选值：hyperscale (全局), default (本地)。仅OceanStor A800系列存储支持
        page_no: 分页查询的页码（可选，1~10000，默认 1）
        page_size: 分页查询的每页大小（可选，1~1000，默认 100）

    Returns:
        {
            total: 逻辑端口的数量 (integer),
            logic_ports: 逻辑端口列表 (List<StorageLogicPortResp>)。参数格式如下：[{
                id: 逻辑端口ID (1~255个字符),
                raw_id: 逻辑端口在存储设备上的ID (1~255个字符),
                name: 逻辑端口名称 (1~255个字符),
                running_status: 运行状态。可选值：UNKNOWN (未知), NORMAL (正常), RUNNING (运行), LINK_UP (已连接), LINK_DOWN (未连接), TO_BE_RECOVERED (待恢复), INITIALIZING (初始化中), STANDBY (待工作), POWERING_ON (正在上电), POWERED_OFF (已下电), POWER_ON_FAILED (上电失败),
                operational_status: 是否激活状态。可选值：ACTIVATED (激活), NOT_ACTIVATED (未激活),
                mgmt_ip: ipv4地址 (1~255个字符),
                ipv4_gateway: 逻辑端口网关IP地址(IPV4) (1~64个字符),
                ipv4_mask: 逻辑端口IP地址掩码(IPV4) (1~64个字符),
                mgmt_ipv6: ipv6地址 (1~255个字符),
                ipv6_mask: 逻辑端口IP地址掩码(IPV6) (1~128个字符),
                ipv6_gateway: 逻辑端口网关IP地址(IPV6) (1~128个字符),
                home_port_raw_id: 父端口在存储设备上的ID (1~255个字符),
                home_port_name: 父端口名称 (1~255个字符),
                home_port_type: 父端口类型。可选值：ETHERNET_PORT (以太网端口和RoCE端口), BOND (绑定), VLAN (VLAN), VIP (VIP), SIP (SIP), IB (IB),
                home_controller_raw_id: 存储设备上主控制器的ID (1~256个字符),
                current_port_raw_id: 逻辑端口所在当前物理端口在存储设备上的ID (1~255个字符),
                current_port_name: 逻辑端口所在当前物理端口名称 (1~255个字符),
                role: 端口角色 (1~10个字符)。可选值：0 (未知), 1 (管理), 2 (数据), 3 (管理+数据), 4 (复制), 6 (当前无意义), 7 (当前无意义), 8 (客户端), 9 (VTEP), 10 (健康检查), 11 (数据备份), 12 (系统管理), 100 (集群), 101 (集群间),
                ddns_status: 动态DNS开启状态。可选值：INVALID (无效的), ENABLE (启用), DISABLED (未启用),
                failover_group_raw_id: 漂移组在存储设备上的ID (1~255个字符),
                failover_group_name: 漂移组名称 (1~255个字符),
                support_protocol: 逻辑端口支持的数据访问协议。可选值：NONE (无协议), NFS (NFS协议), CIFS (CIFS协议), NFS_AND_CIFS (NFS和CIFS协议), NFS_OVER_RDMA (NFS over RDMA协议), iSCSI (iSCSI协议), FC/FCoE (FC/FCoE协议), NVME_OVER_ROCE (NVME over ROCE协议), BGP (BGP协议), DATA_TURBO (DataTurbo协议), DATA_TURBO_OVER_ROCE (DataTurbo over ROCE协议), S3 (S3协议), NFS_OVER_IB (NFS over IB协议), DATA_TURBO_OVER_IB (DataTurbo over IB协议), DATA_TURBO_OVER_ROCE_AND_TCP (DataTurbo over ROCE和TCP协议), OBJECT (S3协议), NAS_AND_OBJECT (NAS与对象存储协议), KB_OVER_TCP (KnowledgeBase over TCP协议),
                logical_type: 逻辑类型。可选值：SERVICE (主机端口/业务端口), MANAGEMENT (管理端口), MAINTENANCE (维护端口),
                listen_dns_query_enabled: 是否监听DNS查询请求 (1~255个字符)。可选值：NO (关闭), YES (打开),
                management_access: 管理访问方式 (1~255个字符),
                vstore_raw_id: 逻辑端口所属vStore在设备上分配的id (1~255个字符),
                vstore_name: 逻辑端口所属vStore的名称 (1~255个字符),
                storage_id: 存储设备ID (1~255个字符),
                storage_name: 存储设备名称 (1~255个字符),
                zone_raw_id: 所属Zone在设备上的ID (1~255个字符)，仅OceanStor A800系列存储支持,
                zone_id: 所属Zone ID (1~64个字符)，仅OceanStor A800系列存储支持,
                zone_name: 所属zone名称 (1~255个字符)，仅OceanStor A800系列存储支持,
                zone_ip: 所属zone IP (1~255个字符),
                dns_zone_name: DNS Zone名称 (1~255个字符),
                current_port_type: 逻辑端口所在物理端口的类型。可选值：ETHERNET_PORT (以太网端口和RoCE端口), BOND (绑定), VLAN (VLAN), VIP (VIP), SIP (SIP), IB (IB),
                address_family: IP协议版本。可选值：IPv4 (IPv4), IPv6 (IPv6),
                can_failover: 是否启用IP地址漂移 (boolean)。可选值：true, false,
                failback_mode: 回漂模式。可选值：not_support (不支持该功能), manual (手动), automatic (自动),
                scope: 范围。可选值：hyperscale (全局), default (本地)。仅OceanStor A800系列存储支持,
                logicPortTags: 关联标签集合 (List<Tag>)。参数格式如下：[{
                    id: 标签的ID (1~32个字符),
                    tag_type_name: 标签类型名称 (1~64个字符),
                    name: 标签名称 (1~128个字符),
                }, ...],
                manufacturer: 厂商 (1~32个字符),
                storage_model: 型号 (1~64个字符),
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
    查询存储设备的逻辑端口详情

    Args:
        client: DME API 客户端
        logic_port_id: 逻辑端口的 ID（必填，1~64 个字符，UUID 格式或 32 位十六进制）

    Returns:
        {
            id: 逻辑端口ID (1~255个字符),
            raw_id: 逻辑端口在存储设备上的ID (1~255个字符),
            name: 逻辑端口名称 (1~255个字符),
            running_status: 运行状态。可选值：UNKNOWN (未知), NORMAL (正常), RUNNING (运行), LINK_UP (已连接), LINK_DOWN (未连接), TO_BE_RECOVERED (待恢复), INITIALIZING (初始化中), STANDBY (待工作), POWERING_ON (正在上电), POWERED_OFF (已下电), POWER_ON_FAILED (上电失败),
            operational_status: 是否激活状态。可选值：ACTIVATED (激活), NOT_ACTIVATED (未激活),
            mgmt_ip: ipv4地址 (1~255个字符),
            ipv4_gateway: 逻辑端口网关IP地址(IPV4) (1~64个字符),
            ipv4_mask: 逻辑端口IP地址掩码(IPV4) (1~64个字符),
            mgmt_ipv6: ipv6地址 (1~255个字符),
            ipv6_mask: 逻辑端口IP地址掩码(IPV6) (1~128个字符),
            ipv6_gateway: 逻辑端口网关IP地址(IPV6) (1~128个字符),
            home_port_raw_id: 父端口在存储设备上的ID (1~255个字符),
            home_port_name: 父端口名称 (1~255个字符),
            home_port_type: 父端口类型。可选值：ETHERNET_PORT (以太网端口和RoCE端口), BOND (绑定), VLAN (VLAN), VIP (VIP), SIP (SIP), IB (IB),
            home_controller_raw_id: 存储设备上主控制器的ID (1~256个字符),
            current_port_raw_id: 逻辑端口所在当前物理端口在存储设备上的ID (1~255个字符),
            current_port_name: 逻辑端口所在当前物理端口名称 (1~255个字符),
            role: 端口角色 (1~10个字符)。可选值：0 (未知), 1 (管理), 2 (数据), 3 (管理+数据), 4 (复制), 6 (当前无意义), 7 (当前无意义), 8 (客户端), 9 (VTEP), 10 (健康检查), 11 (数据备份), 12 (系统管理), 100 (集群), 101 (集群间),
            ddns_status: 动态DNS开启状态。可选值：INVALID (无效的), ENABLE (启用), DISABLED (未启用),
            failover_group_raw_id: 漂移组在存储设备上的ID (1~255个字符),
            failover_group_name: 漂移组名称 (1~255个字符),
            support_protocol: 逻辑端口支持的数据访问协议。可选值：NONE (无协议), NFS (NFS协议), CIFS (CIFS协议), NFS_AND_CIFS (NFS和CIFS协议), NFS_OVER_RDMA (NFS over RDMA协议), iSCSI (iSCSI协议), FC/FCoE (FC/FCoE协议), NVME_OVER_ROCE (NVME over ROCE协议), BGP (BGP协议), DATA_TURBO (DataTurbo协议), DATA_TURBO_OVER_ROCE (DataTurbo over ROCE协议), S3 (S3协议), NFS_OVER_IB (NFS over IB协议), DATA_TURBO_OVER_IB (DataTurbo over IB协议), DATA_TURBO_OVER_ROCE_AND_TCP (DataTurbo over ROCE和TCP协议), OBJECT (S3协议), NAS_AND_OBJECT (NAS与对象存储协议), KB_OVER_TCP (KnowledgeBase over TCP协议),
            logical_type: 逻辑类型。可选值：SERVICE (主机端口/业务端口), MANAGEMENT (管理端口), MAINTENANCE (维护端口),
            listen_dns_query_enabled: 是否监听DNS查询请求 (1~255个字符)。可选值：NO (关闭), YES (打开),
            management_access: 管理访问方式 (1~255个字符),
            vstore_raw_id: 逻辑端口所属vStore在设备上分配的id (1~255个字符),
            vstore_name: 逻辑端口所属vStore的名称 (1~255个字符),
            storage_id: 存储设备ID (1~255个字符),
            storage_name: 存储设备名称 (1~255个字符),
            zone_raw_id: 所属Zone在设备上的ID (1~255个字符)，仅OceanStor A800系列存储支持,
            zone_id: 所属Zone ID (1~64个字符)，仅OceanStor A800系列存储支持,
            zone_name: 所属zone名称 (1~255个字符)，仅OceanStor A800系列存储支持,
            zone_ip: 所属zone IP (1~255个字符),
            dns_zone_name: DNS Zone名称 (1~255个字符),
            current_port_type: 逻辑端口所在物理端口的类型。可选值：ETHERNET_PORT (以太网端口和RoCE端口), BOND (绑定), VLAN (VLAN), VIP (VIP), SIP (SIP), IB (IB),
            address_family: IP协议版本。可选值：IPv4 (IPv4), IPv6 (IPv6),
            can_failover: 是否启用IP地址漂移 (boolean)。可选值：true, false,
            failback_mode: 回漂模式。可选值：not_support (不支持该功能), manual (手动), automatic (自动),
            scope: 范围。可选值：hyperscale (全局), default (本地)。仅OceanStor A800系列存储支持,
            logicPortTags: 关联标签集合 (List<Tag>)。参数格式如下：[{
                id: 标签的ID (1~32个字符),
                tag_type_name: 标签类型名称 (1~64个字符),
                name: 标签名称 (1~128个字符),
            }, ...],
            manufacturer: 厂商 (1~32个字符),
            storage_model: 型号 (1~64个字符),
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
    创建存储设备的逻辑端口（仅 OceanStor A800 系列存储支持）

    Args:
        client: DME API 客户端
        storage_id: 存储设备ID（必选，1~64个字符）
        name: 端口名称（必选，1~255个字符）。只允许包含字母、数字、"_"、"-"、"."和中文字符
        address_family: IP协议版本（必选）。可选值：IPv4 (IPv4), IPv6 (IPv6)
        home_port_type: 父端口类型（必选）。可选值：ETHERNET_PORT (以太网端口和RoCE端口), BOND (绑定), VLAN (VLAN), VIP (VIP), SIP (SIP), IB (IB)
        zone_raw_id: 所属Zone在设备上的ID（必选，1~64个字符），仅OceanStor A800系列存储支持
        scope: 范围（必选）。可选值：hyperscale (全局), default (本地)。仅OceanStor A800系列存储支持。数据访问协议为KB_OVER_TCP时取值仅支持default
        mgmt_ip: 逻辑端口IP地址(IPV4)（可选，最多64个字符，IPv4格式）
        ipv4_mask: 逻辑端口IP地址掩码(IPV4)（可选，最多64个字符）
        ipv4_gateway: 逻辑端口网关IP地址(IPV4)（可选，最多64个字符）
        mgmt_ipv6: 逻辑端口IP地址(IPV6)（可选，最多128个字符）
        ipv6_mask: 逻辑端口IP地址掩码(IPV6)（可选，最多128个字符）
        ipv6_gateway: 逻辑端口网关IP地址(IPV6)（可选，最多128个字符）
        home_port_raw_id: 父端口在存储设备上的ID（可选，1~64个字符）
        support_protocol: 逻辑端口支持的数据访问协议（可选）。可选值：NFS (NFS协议), DATA_TURBO_OVER_ROCE (DataTurbo over RoCE协议), NFS_OVER_RDMA (NFS over RDMA协议), NFS_OVER_IB (NFS over IB协议), DATA_TURBO_OVER_IB (DataTurbo over IB协议), DATA_TURBO_OVER_ROCE_AND_TCP (DataTurbo over RoCE和TCP协议), OBJECT (S3协议), NAS_AND_OBJECT (NAS与对象存储协议), KB_OVER_TCP (KnowledgeBase over TCP协议)。角色为CLIENT时，不支持下发此字段
        operational_status: 激活状态（可选）。可选值：ACTIVATED (激活), NOT_ACTIVATED (未激活)
        home_controller_id: 控制器ID（可选，1~64个字符）。角色为HEALTH_CHECK时，该字段必须配置
        failover_group_raw_id: 漂移组在存储设备上的ID（可选，最多64个字符）。数据访问协议为KB_OVER_TCP时，该字段必须配置
        vstore_raw_id: 逻辑端口所属vStore在设备上分配的id（可选，最多64个字符）。角色为CLIENT时，不支持下发此字段
        role: 逻辑端口角色（可选，默认 DATA）。可选值：MANAGEMENT (管理), DATA (数据), VTEP (VTEP), HEALTH_CHECK (健康检查), MANAGEMENT_AND_DATA (管理+数据), CLIENT (客户端)
        dns_zone_name: DNS Zone名称（可选，最多255个字符）。角色为CLIENT或数据访问协议为KB_OVER_TCP时，不支持下发此字段
        listen_dns_query_enabled: 是否侦听DNS查询请求（可选，正则 NO|YES）。可选值：NO (关闭), YES (打开)。角色为CLIENT或数据访问协议为KB_OVER_TCP时，不支持下发此字段
        can_failover: 是否启用IP地址漂移（可选，boolean）。可选值：true, false。数据访问协议为KB_OVER_TCP时，不支持下发此字段
        failback_mode: 回漂模式（可选）。可选值：not_support (不支持该功能), manual (手动), automatic (自动)。数据访问协议为KB_OVER_TCP时，不支持下发此字段

    Returns:
        {
            task_id: 任务Id (1~64个字符),
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
    修改存储设备的逻辑端口（仅 OceanStor A800 系列存储支持）

    Args:
        client: DME API 客户端
        logic_port_id: 逻辑端口 ID（必填，1~128 个字符）
        name: 端口名称（可选）
        address_family: IP 协议版本（可选）
        mgmt_ip: 逻辑端口 IP 地址 (IPV4)（可选）
        ipv4_mask: 逻辑端口 IP 地址掩码 (IPV4)（可选）
        ipv4_gateway: 逻辑端口网关 IP 地址 (IPV4)（可选）
        mgmt_ipv6: 逻辑端口 IP 地址 (IPV6)（可选）
        ipv6_mask: 逻辑端口 IP 地址掩码 (IPV6)（可选）
        ipv6_gateway: 逻辑端口网关 IP 地址 (IPV6)（可选）
        home_port_raw_id: 父端口在存储设备上的 ID（可选）
        home_port_type: 父端口类型（可选）
        operational_status: 激活状态（可选）
        failover_group_raw_id: 漂移组在存储设备上的 ID（可选）
        dns_zone_name: DNS Zone 名称（可选）
        listen_dns_query_enabled: 是否侦听 DNS 查询请求（可选）
        can_failover: 是否启用 IP 地址漂移（可选）
        failback_mode: 回漂模式（可选）

    Returns:
        响应数据，包含 task_id
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
    删除存储设备的逻辑端口（仅 OceanStor A800 系列存储支持）

    Args:
        client: DME API 客户端
        ids: 逻辑端口 ID 列表（必填，1~1000 个 ID）

    Returns:
        响应数据，包含 task_id
    """
    url = "/rest/storagemgmt/v1/logic-ports/delete"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def logic_port_failback(client: DMEAPIClient, id: str) -> dict:
    """
    回切存储设备的逻辑端口（仅 OceanStor A800 系列存储支持）

    Args:
        client: DME API 客户端
        id: 逻辑端口 ID（必填，1~64 个字符）

    Returns:
        响应数据，包含 task_id
    """
    url = "/rest/storagemgmt/v1/logic-ports/failback"

    payload = {
        'id': id
    }

    response = client.post(url, body=payload)
    return response


# ============ 存储端口 (port) 子主题函数 ============


def port_list(client: DMEAPIClient, storage_id: str = None, port_type: str = None,
              location: str = None, ipv4: str = None, ipv6: str = None,
              port_name: str = None, zone_id: str = None,
              page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询存储设备端口信息，支持 ETH、FC、IB、Bond、SAS 五种类型

    Args:
        client: DME API 客户端
        storage_id: 存储设备 ID（可选，1~36 个字符）
        port_type: 端口类型（可选，eth/fc/ib/bond/sas，不指定则返回所有类型）
        location: 位置（可选，仅 ETH 端口支持，1~255 个字符）
        ipv4: IPv4 地址（可选，仅 ETH 端口支持，1~255 个字符）
        ipv6: IPv6 地址（可选，仅 ETH 端口支持，1~255 个字符）
        port_name: 端口名称（可选，仅 ETH 端口支持，1~255 个字符）
        zone_id: 所属存储设备的 Zone ID（可选，仅 Bond 端口支持，1~36 个字符）
        page_no: 分页查询的页码（可选，FC/SAS 端口支持，1~10000，默认 1）
        page_size: 每页数量（可选，FC/SAS 端口支持，1~1000，默认 20）

    Returns:
        响应数据，包含端口列表
    """
    if port_type is not None and port_type.lower() == 'eth':
        # ETH 端口查询
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
        # Bond 端口查询
        url = "/rest/storagemgmt/v1/bond-ports/query"
        payload = {'storage_id': storage_id}
        if zone_id is not None:
            payload['zone_id'] = zone_id
        response = client.post(url, body=payload)
        return response
    elif port_type is not None and port_type.lower() == 'fc':
        # FC 端口查询
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
        # IB 端口查询
        url = "/rest/storagemgmt/v1/storages/ib-ports/query"
        payload = {}
        if storage_id is not None:
            payload['storage_id'] = storage_id
        response = client.post(url, body=payload)
        return response
    elif port_type is not None and port_type.lower() == 'sas':
        # SAS 端口查询
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
    查询指定绑定端口的成员列表信息

    Args:
        client: DME API 客户端
        bond_port_id: 绑定端口 id（必填，1~64 个字符）

    Returns:
        响应数据，包含 total 和 eth_ports 字段
    """
    url = "/rest/storagemgmt/v1/bond-ports/{bond_port_id}/eth-ports"

    response = client.get(url, params={"bond_port_id": bond_port_id})
    return response


# ============ 存储端口组 (port_group) 子主题函数 ============


# ============ 存储 VLAN 子主题函数 ============


def vlan_list(client: DMEAPIClient, name: str = None, storage_id: str = None,
              page_no: int = 1, page_size: int = 100) -> dict:
    """
    批量查询 VLAN 列表

    Args:
        client: DME API 客户端
        name: VLAN 名称（支持模糊查询）
        storage_id: 存储设备 ID
        page_no: 分页查询的起始页码，默认 1
        page_size: 每页数量，1~1000，默认 100

    Returns:
        响应数据，包含 VLAN 列表
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

    注意：仅支持 OceanStor A800、A600 系列存储。

    Args:
        client: DME API 客户端
        name: VLAN 名称（必选）
        vlan_id: VLAN ID（必选，1~4094）
        storage_id: 存储设备 ID（必选）
        description: VLAN 描述（可选）

    Returns:
        响应数据，包含新创建的 VLAN ID
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

    注意：仅支持 OceanStor A800、A600 系列存储。

    Args:
        client: DME API 客户端
        vlan_id: VLAN ID

    Returns:
        响应数据
    """
    url = "/rest/vlanmgmt/v1/vlans/{vlan_id}"

    response = client.delete(url, params={"vlan_id": vlan_id})
    return response


def vlan_modify(client: DMEAPIClient, vlan_id: str, name: str = None,
                description: str = None) -> dict:
    """
    修改 VLAN

    注意：仅支持 OceanStor A800、A600 系列存储。

    Args:
        client: DME API 客户端
        vlan_id: VLAN ID
        name: VLAN 名称（可选）
        description: VLAN 描述（可选）

    Returns:
        响应数据
    """
    url = "/rest/vlanmgmt/v1/vlans/{vlan_id}"

    body_params = {}
    if name is not None:
        body_params['name'] = name
    if description is not None:
        body_params['description'] = description

    response = client.put(url, params={"vlan_id": vlan_id})
    return response


# ============ 存储漂移组 (failover_group) 子主题函数 ============


def failover_group_list(client: DMEAPIClient, storage_id: str,
                        failover_group_type: str = None,
                        zone_id: str = None,
                        failover_group_service_type: list = None) -> dict:
    """
    查询漂移组列表

    Args:
        client: DME API 客户端
        storage_id: 存储设备ID（必选，1~36个字符，且满足正则 ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$）
        failover_group_type: 漂移组类型（可选）。可选值：system, VLAN, customized
        zone_id: 所属Zone ID（可选，1~255个字符），仅OceanStor A800系列存储支持
        failover_group_service_type: 漂移组业务类型列表（可选，List<string>，数组最大成员个数：10）。可选值：NAS (用于关联NFS、CIFS、NFS and OBJECT协议类型逻辑端口的漂移组), BGP (用于关联VIP类型逻辑端口的漂移组), RDMA (用于关联NFS over RDMA、NFS、OBJECT协议逻辑端口的漂移组), IB (用于关联NAS over IB协议类型逻辑端口的漂移组), KB (用于关联KnowledgeBase over TCP协议类型逻辑端口的漂移组)

    Returns:
        {
            total: 漂移组数量 (int32),
            failover_groups: 漂移组列表 (List<FailoverGroupResp>)。参数格式如下：[{
                id: 漂移组id (1~64个字符),
                name: 漂移组名称 (1~64个字符),
                failover_group_type: 漂移组类型 (1~255个字符)。可选值：system, VLAN, customized,
                raw_id: 漂移组在存储设备上的ID (1~255个字符),
                zone_name: 所属Zone名称 (1~255个字符)，仅OceanStor A800系列存储支持,
                zone_raw_id: 所属Zone在存储设备上分配的ID (1~255个字符)，仅OceanStor A800系列存储支持,
                zone_id: 所属存储设备的Zone ID (1~255个字符)，仅OceanStor A800系列存储支持,
                failover_group_service_type: 漂移组业务类型。可选值：NAS (用于关联NFS、CIFS、NFS and OBJECT协议类型逻辑端口的漂移组), BGP (用于关联VIP类型逻辑端口的漂移组), RDMA (用于关联NFS over RDMA、NFS、OBJECT协议逻辑端口的漂移组), IB (用于关联NAS over IB协议类型逻辑端口的漂移组), KB (用于关联KnowledgeBase over TCP协议类型逻辑端口的漂移组),
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
    查询漂移组下的端口（支持 bond、eth、ib 三种类型）

    Args:
        client: DME API 客户端
        failover_group_id: 漂移组 id（必填，1~64 个字符）
        port_type: 端口类型（可选，bond/eth/ib，不指定则返回所有类型）

    Returns:
        响应数据，结构一致：{"total": x, "bond_ports": [], "eth_ports": [], "ib_ports": []}
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
        # 不指定类型，返回所有三种类型的端口，扁平化结构
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
    查询漂移组下的 VLAN

    Args:
        client: DME API 客户端
        failover_group_id: 漂移组 id（必填，1~64 个字符）

    Returns:
        响应数据，包含 vlans 字段
    """
    url = "/rest/storagemgmt/v1/failover-groups/{failover_group_id}/vlans"

    response = client.get(url, params={"failover_group_id": failover_group_id})
    return response


# ============ Zone (OceanStor A800 集群 zone) 子主题函数 ============


def zone_list(client: DMEAPIClient, name: str = None, ip: str = None,
              status: list = None, sync_status: list = None,
              sn: str = None, storage_ids: list = None) -> dict:
    """
    查询OceanStor A800集群中zone信息

    Args:
        client: DME API 客户端
        name: zone名称（可选，1~256个字符），精确查询
        ip: zone ip地址名称（可选，1~256个字符），精确查询
        status: Zone状态列表（可选，List<string>，数组最大成员个数：6）。可选值：OFFLINE (离线), NORMAL (正常), FAULT (故障), DEGRADED (降级), ABNORMAL (未管理), UNKNOWN (未知)
        sync_status: Zone同步状态列表（可选，List<string>，数组最大成员个数：5）。可选值：UNSYNC (未同步), SYNC (同步中), NORMAL (同步完成), FAILED (同步失败), UNKNOWN (未知)
        sn: Zone序列号（可选，1~128个字符），精确查询
        storage_ids: OceanStor A800集群id列表（可选，List<string>，数组最大成员个数：100，最小成员个数：1），精确查询

    Returns:
        {
            total: Zone总数 (int32),
            datas: Zone列表 (List<OceanStorA800ZoneInfo>)。参数格式如下：[{
                id: Zone在CMDB中的ID (1~64个字符),
                native_id: native id (1~64个字符),
                name: Zone名称 (1~128个字符),
                ip: Zone IP地址 (1~32个字符),
                status: 状态 (1~32个字符)。可选值：OFFLINE (离线), NORMAL (正常), FAULT (故障), DEGRADED (降级), ABNORMAL (未管理),
                sync_status: 同步状态 (1~32个字符)。可选值：UNSYNC (未同步), SYNC (同步中), NORMAL (同步完成), FAILED (同步失败),
                sn: Zone设备序列号 (1~64个字符),
                wwn: Zone设备WWN号 (1~32个字符),
                vendor: Zone厂商 (1~32个字符),
                model: Zone产品型号 (1~64个字符),
                owning_ne_type: 存储设备网元类型。可选值：dorado (dorado系列存储), OceanStor A800 (OceanStor A800),
                location: Zone位置信息 (0~512个字符),
                version: 版本信息 (0~64个字符),
                patch_version: 补丁版本信息 (0~64个字符),
                add_time: 接入设备时间 (0~32个字符)，UTC时间戳（精确到毫秒）,
                last_sync_time: 上一次同步时间 (0~32个字符)，UTC时间戳（精确到毫秒）,
                sync_process: 同步进度 (int32),
                alarm_num: 告警数量 (number),
                parent_id: 集群id,
                zone_raw_id: zone raw id,
                is_core_zone: 是否是核心控制节点所在的zone (boolean)。可选值：true, false,
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


# 动作列表，用于 CLI 帮助
# 格式：action_key: {func, description, params, subtopic}
# subtopic 表示该动作属于哪个子主题，None 表示直接动作

ACTIONS = {
    # 直接动作（两级结构：<topic> <action>）
    'list': {
        'func': list,
        'description': '批量查询存储设备',
        'params': ['az', 'source', 'dc_id', 'tag_ids', 'start', 'limit', 'ext_attrs'],
        'subtopic': None
    },
    'show': {
        'func': show,
        'description': '查询指定存储设备',
        'params': ['storage_id'],
        'subtopic': None
    },
    'add': {
        'func': add,
        'description': '添加存储设备（仅支持录入离线存储设备信息）',
        'params': ['name', 'sn', 'ip', 'vendor', 'model', 'version', 'patch_version', 'dc_id', 'az', 'location', 'maintenance_start', 'maintenance_overtime', 'total_capacity', 'total_effective_capacity', 'total_pool_capacity', 'used_capacity', 'free_capacity', 'subscription_capacity', 'tag_ids'],
        'subtopic': None
    },
    'remove': {
        'func': remove,
        'description': '批量移除存储设备',
        'params': ['storage_ids'],
        'subtopic': None
    },
    'sync': {
        'func': sync,
        'description': '同步存储设备信息',
        'params': ['storage_id'],
        'subtopic': None
    },
    'modify': {
        'func': modify,
        'description': '修改存储设备（仅支持修改录入的离线存储设备信息）',
        'params': ['storage_id', 'name', 'location', 'ext_attrs'],
        'subtopic': None
    },
    # 子主题动作（三级结构：<topic> <subtopic> <action>）
    'bbu_list': {
        'func': bbu_list,
        'description': '查询存储设备的 BBU 信息列表',
        'params': ['storage_id', 'health_status', 'running_status', 'enclosure_name',
                   'location', 'zone_id', 'page_no', 'page_size'],
        'subtopic': 'bbu'
    },
    'get_passphrase': {
        'func': get_passphrase,
        'description': '获取存储设备访问的令牌',
        'params': ['storage_id'],
    },
    'fan_list': {
        'func': fan_list,
        'description': '查询存储设备的风扇信息',
        'params': ['storage_id', 'health_status', 'running_status', 'run_level',
                   'enclosure_name', 'location', 'zone_id', 'page_no', 'page_size'],
        'subtopic': 'fan'
    },
    'disk_list': {
        'func': disk_list,
        'description': '查询存储设备的硬盘信息列表',
        'params': ['storage_id'],
        'subtopic': 'disk'
    },
    'pool_list': {
        'func': pool_list,
        'description': '查询存储设备存储池列表',
        'params': ['storage_id', 'raw_id', 'zone_id', 'page_no', 'page_size', 'sort_key', 'sort_dir'],
        'subtopic': 'pool'
    },
    'hyperscale_pool_list': {
        'func': hyperscale_pool_list,
        'description': '查询 HyperScale 存储池列表',
        'params': ['raw_id', 'name', 'local_pool_id', 'health_status', 'running_status', 'storage_id', 'description', 'page_no', 'page_size', 'sort_key', 'sort_dir'],
        'subtopic': 'hyperscale_pool'
    },
    'node_list': {
        'func': node_list,
        'description': '查询存储设备的节点列表',
        'params': ['storage_id', 'raw_id', 'storage_name', 'name', 'ids',
                   'mgmt_ip', 'frame_number', 'slot_number', 'status', 'roles',
                   'page_no', 'page_size', 'sort_key', 'sort_dir'],
        'subtopic': 'node'
    },
    'psu_list': {
        'func': psu_list,
        'description': '获取存储设备电源（PSU）列表',
        'params': ['storage_id', 'health_status', 'running_status', 'power_type',
                   'power_mode', 'location', 'model', 'sn', 'enclosure_name',
                   'zone_id', 'page_no', 'page_size'],
        'subtopic': 'psu'
    },
    'query_power_data': {
        'func': query_power_data,
        'description': '查询存储设备功率数据',
        'params': ['start_time', 'end_time', 'storage_ids', 'time_granularity'],
    },
    'app_type_list': {
        'func': app_type_list,
        'description': '查询指定存储设备的应用类型',
        'params': ['storage_id'],
        'subtopic': 'app_type'
    },
    'controller_list': {
        'func': controller_list,
        'description': '查询指定存储设备的控制器信息',
        'params': ['storage_id'],
        'subtopic': 'controller'
    },
    'disk_pool_list': {
        'func': disk_pool_list,
        'description': '批量查询硬盘域',
        'params': ['storage_id', 'page_no', 'page_size'],
        'subtopic': 'disk_pool'
    },
    'enclosure_list': {
        'func': enclosure_list,
        'description': '批量查询机框信息',
        'params': ['page_no', 'page_size', 'storage_id', 'name', 'location',
                   'health_status', 'zone_name', 'zone_id', 'running_status',
                   'power_mode', 'esn', 'mac', 'sort_key', 'sort_dir'],
        'subtopic': 'enclosure'
    },
    'vstore_list': {
        'func': vstore_list,
        'description': '批量查询存储设备租户信息',
        'params': ['storage_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'vstore'
    },
    'vstore_show': {
        'func': vstore_show,
        'description': '查询租户详情',
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
        'description': '修改指定租户',
        'params': ['vstore_id', 'name', 'san_capacity_quota', 'nas_capacity_quota', 'description', 'nas_capacity_quota_alarm_switch', 'nas_capacity_quota_alarm_threshold'],
        'subtopic': 'vstore'
    },
    'vstore_delete': {
        'func': vstore_delete,
        'description': '批量删除租户',
        'params': ['vstore_ids'],
        'subtopic': 'vstore'
    },
    'initiator_list': {
        'func': initiator_list,
        'description': '批量查询存储侧启动器对象',
        'params': ['page_size', 'page_no', 'raw_id', 'alias', 'status',
                   'associated_host_name', 'associated_host_id', 'multipath_type',
                   'protocol', 'support_provisioning', 'vstore_raw_id',
                   'vstore_name', 'storage_id'],
        'subtopic': 'initiator'
    },
    'initiator_delete': {
        'func': initiator_delete,
        'description': '批量删除存储设备的启动器对象',
        'params': ['initiator_ids', 'task_remarks'],
        'subtopic': 'initiator'
    },
    'initiator_modify': {
        'func': initiator_modify,
        'description': '修改存储侧启动器对象',
        'params': ['initiator_id', 'vstore_id', 'alias', 'multi_path'],
        'subtopic': 'initiator'
    },
    # account 子主题动作（认证用户）
    'account_show_local_users': {
        'func': account_show_local_users,
        'description': '查询指定存储设备本地认证用户的信息',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_create_local_user': {
        'func': account_create_local_user,
        'description': '创建本地认证用户',
        'params': ['storage_id', 'name', 'password', 'primary_group_raw_id', 'description', 'group_names', 'vstore_id'],
        'subtopic': 'account'
    },
    'account_create_unix_user': {
        'func': account_create_unix_user,
        'description': '创建指定存储设备 UNIX 认证用户',
        'params': ['storage_id', 'name', 'primary_group_raw_id', 'raw_id', 'description', 'password', 'status_enabled', 'vstore_raw_id'],
        'subtopic': 'account'
    },
    'account_create_windows_user': {
        'func': account_create_windows_user,
        'description': '创建指定存储设备 Windows 认证用户',
        'params': ['storage_id', 'name', 'password', 'raw_id', 'description', 'status_enabled', 'vstore_raw_id'],
        'subtopic': 'account'
    },
    'account_show_unix_users': {
        'func': account_show_unix_users,
        'description': '查询指定存储设备 UNIX 认证用户的信息',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_show_windows_users': {
        'func': account_show_windows_users,
        'description': '查询指定存储设备 Windows 认证用户的信息',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_show_local_user_groups': {
        'func': account_show_local_user_groups,
        'description': '查询指定存储设备本地认证用户组的信息',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_show_unix_user_groups': {
        'func': account_show_unix_user_groups,
        'description': '查询指定存储设备 UNIX 认证用户组的信息',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_show_windows_user_groups': {
        'func': account_show_windows_user_groups,
        'description': '查询指定存储设备 Windows 认证用户组的信息',
        'params': ['storage_id', 'vstore_raw_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    # qos 子主题动作
    'qos_list': {
        'func': qos_list,
        'description': '批量查询 QoS 策略',
        'params': ['storage_id', 'name', 'raw_id', 'enable_status', 'running_status',
                   'zone_id', 'resource_type_list', 'vstore_id', 'vstore_name',
                   'alarm_status', 'io_policy_type', 'page_no', 'page_size',
                   'sort_key', 'sort_dir'],
        'subtopic': 'qos'
    },
    'qos_show': {
        'func': qos_show,
        'description': '查询指定 QoS 策略详情',
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
        'description': '批量取消激活 QoS 策略',
        'params': ['qos_policy_ids'],
        'subtopic': 'qos'
    },
    'qos_associate': {
        'func': qos_associate,
        'description': 'QoS 策略关联控制资源',
        'params': ['qos_policy_id', 'resource_ids', 'resource_type'],
        'subtopic': 'qos'
    },
    'qos_unassociate': {
        'func': qos_unassociate,
        'description': 'QoS 策略解关联控制资源',
        'params': ['qos_policy_id', 'resource_ids', 'resource_type'],
        'subtopic': 'qos'
    },
    # logic_port 子主题动作（存储逻辑端口）
    'logic_port_list': {
        'func': logic_port_list,
        'description': '查询存储设备的逻辑端口列表',
        'params': ['storage_id', 'vstore_raw_id', 'zone_raw_id', 'scope', 'page_no', 'page_size'],
        'subtopic': 'logic_port'
    },
    'logic_port_show': {
        'func': logic_port_show,
        'description': '查询存储设备的逻辑端口详情',
        'params': ['logic_port_id'],
        'subtopic': 'logic_port'
    },
    'logic_port_create': {
        'func': logic_port_create,
        'description': '创建存储设备的逻辑端口（仅 OceanStor A800 系列存储支持）',
        'params': ['storage_id', 'name', 'address_family', 'home_port_type', 'zone_raw_id', 'scope',
                   'mgmt_ip', 'ipv4_mask', 'ipv4_gateway', 'mgmt_ipv6', 'ipv6_mask', 'ipv6_gateway',
                   'home_port_raw_id', 'support_protocol', 'operational_status', 'home_controller_id',
                   'failover_group_raw_id', 'vstore_raw_id', 'role', 'dns_zone_name',
                   'listen_dns_query_enabled', 'can_failover', 'failback_mode'],
        'subtopic': 'logic_port'
    },
    'logic_port_update': {
        'func': logic_port_update,
        'description': '修改存储设备的逻辑端口（仅 OceanStor A800 系列存储支持）',
        'params': ['logic_port_id', 'name', 'address_family', 'mgmt_ip', 'ipv4_mask', 'ipv4_gateway',
                   'mgmt_ipv6', 'ipv6_mask', 'ipv6_gateway', 'home_port_raw_id', 'home_port_type',
                   'operational_status', 'failover_group_raw_id', 'dns_zone_name',
                   'listen_dns_query_enabled', 'can_failover', 'failback_mode'],
        'subtopic': 'logic_port'
    },
    'logic_port_delete': {
        'func': logic_port_delete,
        'description': '删除存储设备的逻辑端口（仅 OceanStor A800 系列存储支持）',
        'params': ['ids'],
        'subtopic': 'logic_port'
    },
    'logic_port_failback': {
        'func': logic_port_failback,
        'description': '回切存储设备的逻辑端口（仅 OceanStor A800 系列存储支持）',
        'params': ['id'],
        'subtopic': 'logic_port'
    },
    # port 子主题动作（存储端口）
    'port_list': {
        'func': port_list,
        'description': '查询存储设备端口信息，支持 ETH、FC、IB、Bond 四种类型',
        'params': ['storage_id', 'port_type', 'location', 'ipv4', 'ipv6', 'port_name', 'zone_id', 'page_no', 'page_size'],
        'subtopic': 'port'
    },
    'port_show_bond_members': {
        'func': port_show_bond_members,
        'description': '查询指定绑定端口的成员列表信息',
        'params': ['bond_port_id'],
        'subtopic': 'port'
    },
    # vlan 子主题动作（存储 VLAN）
    'vlan_list': {
        'func': vlan_list,
        'description': '批量查询 VLAN 列表',
        'params': ['name', 'storage_id', 'page_no', 'page_size'],
        'subtopic': 'vlan'
    },
    'vlan_create': {
        'func': vlan_create,
        'description': '创建 VLAN（仅支持 OceanStor A800、A600 系列存储）',
        'params': ['name', 'vlan_id', 'storage_id', 'description'],
        'subtopic': 'vlan'
    },
    'vlan_delete': {
        'func': vlan_delete,
        'description': '删除 VLAN（仅支持 OceanStor A800、A600 系列存储）',
        'params': ['vlan_id'],
        'subtopic': 'vlan'
    },
    'vlan_modify': {
        'func': vlan_modify,
        'description': '修改 VLAN（仅支持 OceanStor A800、A600 系列存储）',
        'params': ['vlan_id', 'name', 'description'],
        'subtopic': 'vlan'
    },
    # failover_group 子主题动作（存储漂移组）
    'failover_group_list': {
        'func': failover_group_list,
        'description': '查询漂移组列表',
        'params': ['storage_id', 'failover_group_type', 'zone_id', 'failover_group_service_type'],
        'subtopic': 'failover_group'
    },
    'failover_group_show_ports': {
        'func': failover_group_show_ports,
        'description': '查询漂移组下的端口（支持 bond、eth、ib 三种类型）',
        'params': ['failover_group_id', 'port_type'],
        'subtopic': 'failover_group'
    },
    'failover_group_show_vlans': {
        'func': failover_group_show_vlans,
        'description': '查询漂移组下的 VLAN',
        'params': ['failover_group_id'],
        'subtopic': 'failover_group'
    },
    # zone 子主题动作（OceanStor A800 集群 zone）
    'zone_list': {
        'func': zone_list,
        'description': '查询OceanStor A800集群中zone信息',
        'params': ['name', 'ip', 'status', 'sync_status', 'sn', 'storage_ids'],
        'subtopic': 'zone'
    },
}
