"""
存储设备 (Storage) 相关操作
"""

import sys
import os

from pydme.client import DMEAPIClient

# ============================================================================
# VStore (租户) 子主题函数
# ============================================================================


def vstore_list(client: DMEAPIClient, storage_id: str = None, name: str = None,
                page_no: int = 1, page_size: int = 100,
                raw_id: str = None, vstore_id: str = None,
                qos_id: str = None, is_associated_qos: bool = None,
                storage_ip: str = None, storage_name: str = None,
                zone_id: str = None, status: str = None,
                nas_capacity_quota_alarm_switch: bool = None,
                sort_key: str = None, sort_dir: str = None) -> dict:
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
    url = "/rest/fileservice/v1/vstores/{id}"

    # 参数校验
    if not id:
        raise ValueError("id 是必选参数")

    response = client.get(url, params={"id": id})
    return response


def vstore_create(client: DMEAPIClient, name: str, storage_id: str,
                  san_capacity_quota: str = None,
                  nas_capacity_quota: str = None, description: str = None,
                  nas_capacity_quota_alarm_switch: bool = None,
                  nas_capacity_quota_alarm_threshold: int = None,
                  associate_pool_ids: list = None) -> dict:
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


def vstore_modify(client: DMEAPIClient, id: str, name: str = None,
                  san_capacity_quota: str = None, nas_capacity_quota: str = None,
                  description: str = None, nas_capacity_quota_alarm_switch: bool = None,
                  nas_capacity_quota_alarm_threshold: int = None) -> dict:
    url = "/rest/fileservice/v1/vstores/{id}"

    # 参数校验
    if not id:
        raise ValueError("id 是必选参数")

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
    url = "/rest/fileservice/v1/vstores/delete"

    # 参数校验
    if not ids or len(ids) == 0:
        raise ValueError("ids 是必选参数，至少需要1个租户ID")

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response



def list(client: DMEAPIClient, az: str = None, source: str = None,
         dc_id: str = None, tag_ids: str = None, start: int = 1, 
         limit: int = 20, ext_attrs: str = None) -> dict:
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
    url = "/rest/storagemgmt/v1/storages/{storage_id}/detail"

    if not storage_id:
        raise ValueError("storage_id 是必选参数")

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
    if not name:
        raise ValueError("name 是必选参数")
    if not sn:
        raise ValueError("sn 是必选参数")

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
    url = "/rest/storagemgmt/v2/storages/delete"

    if not ids or len(ids) == 0:
        raise ValueError("ids 是必选参数，至少需要1个存储设备ID")

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def sync(client: DMEAPIClient, storage_id: str) -> dict:
    url = "/rest/storagemgmt/v1/storages/refresh"

    if not storage_id:
        raise ValueError("storage_id 是必选参数")

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
    url = "/rest/storagemgmt/v1/storages/{storage_id}/passphrase"
    
    response = client.get(url, params={"storage_id": storage_id})
    return response


def fan_list(client: DMEAPIClient, storage_id: str = None,
             health_status: str = None, running_status: str = None,
             run_level: str = None, enclosure_name: str = None,
             location: str = None, zone_id: str = None,
             page_no: int = 1, page_size: int = 20) -> dict:
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
    if not storage_id:
        raise ValueError("storage_id 是必选参数")

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
    url = "/rest/storagemgmt/v1/storages/{storage_id}/controllers"
    
    response = client.get(url, params={"storage_id": storage_id})
    return response


def disk_domain_list(client: DMEAPIClient, storage_id: str = None, page_no: int = 1,
                   page_size: int = 20) -> dict:
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


# ============ QoS 子主题函数 ============


def qos_list(client: DMEAPIClient, storage_id: str, name: str = None,
             raw_id: str = None, enable_status: bool = None,
             running_status: str = None, zone_id: str = None,
             resource_type_list: list = None, vstore_id: str = None,
             vstore_name: str = None, alarm_status: str = None,
             io_policy_type: str = None, page_no: int = 1,
             page_size: int = 10, sort_key: str = None,
             sort_dir: str = None) -> dict:
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
        # DME API 要求 io_param 内的字段使用驼峰命名
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
    url = "/rest/storagepolicy/v1/qos/delete"

    payload = {
        'ids': qos_policy_ids
    }

    response = client.post(url, body=payload)
    return response


def qos_activate(client: DMEAPIClient, qos_policy_ids: list) -> dict:
    url = "/rest/storagepolicy/v1/qos/active"

    payload = {
        'qos_ids': qos_policy_ids
    }

    response = client.post(url, body=payload)
    return response


def qos_deactivate(client: DMEAPIClient, qos_policy_ids: list) -> dict:
    url = "/rest/storagepolicy/v1/qos/inactive"

    payload = {
        'qos_ids': qos_policy_ids
    }

    response = client.post(url, body=payload)
    return response


def qos_associate(client: DMEAPIClient, qos_policy_id: str,
                  resource_ids: list, resource_type: str) -> dict:
    url = "/rest/storagepolicy/v1/qos/{qos_policy_id}/resources/associate"

    payload = {
        'resource_ids': resource_ids,
        'resource_type': resource_type
    }

    response = client.post(url, body=payload, params={"qos_policy_id": qos_policy_id})
    return response


def qos_unassociate(client: DMEAPIClient, qos_policy_id: str,
                    resource_ids: list, resource_type: str) -> dict:
    url = "/rest/storagepolicy/v1/qos/{qos_policy_id}/resources/unassociate"

    payload = {
        'resource_ids': resource_ids,
        'resource_type': resource_type
    }

    response = client.post(url, body=payload, params={"qos_policy_id": qos_policy_id})
    return response


# ============ 存储逻辑端口 (logic_port) 子主题函数 ============


def logic_port_list(client: DMEAPIClient, storage_id: str = None, vstore_raw_id: str = None,
                    zone_raw_id: str = None, scope: str = None, page_no: int = 1,
                    page_size: int = 100) -> dict:
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
    url = "/rest/storagemgmt/v1/logic-ports/delete"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def logic_port_failback(client: DMEAPIClient, id: str) -> dict:
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
    url = "/rest/storagemgmt/v1/bond-ports/{bond_port_id}/eth-ports"

    response = client.get(url, params={"bond_port_id": bond_port_id})
    return response


# ============ 存储端口组 (port_group) 子主题函数 ============


# ============ 存储 VLAN 子主题函数 ============


def vlan_list(client: DMEAPIClient, name: str = None, storage_id: str = None,
              page_no: int = 1, page_size: int = 100) -> dict:
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
    url = "/rest/vlanmgmt/v1/vlans/{vlan_id}"

    response = client.delete(url, params={"vlan_id": vlan_id})
    return response


def vlan_modify(client: DMEAPIClient, vlan_id: str, name: str = None,
                description: str = None) -> dict:
    url = "/rest/vlanmgmt/v1/vlans/{vlan_id}"

    body_params = {}
    if name is not None:
        body_params['name'] = name
    if description is not None:
        body_params['description'] = description

    response = client.put(url, body=body_params, params={"vlan_id": vlan_id})
    return response


# ============ 存储漂移组 (failover_group) 子主题函数 ============


def failover_group_list(client: DMEAPIClient, storage_id: str,
                        failover_group_type: str = None,
                        zone_id: str = None,
                        failover_group_service_type: list = None) -> dict:
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
    url = "/rest/storagemgmt/v1/failover-groups/{failover_group_id}/vlans"

    response = client.get(url, params={"failover_group_id": failover_group_id})
    return response


# ============ Zone (OceanStor A800 集群 zone) 子主题函数 ============


def zone_list(client: DMEAPIClient, name: str = None, ip: str = None,
              status: list = None, sync_status: list = None,
              sn: str = None, storage_ids: list = None) -> dict:
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
    'disk_domain_list': {
        'func': disk_domain_list,
        'description': '批量查询硬盘域',
        'params': ['storage_id', 'page_no', 'page_size'],
        'subtopic': 'disk_domain'
    },
    'disk_pool_list': {
        'func': disk_pool_list,
        'description': '批量查询分布式存储设备的硬盘池',
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
        'params': ['storage_id', 'name', 'account_password', 'primary_group_raw_id', 'description', 'group_names', 'vstore_id'],
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
