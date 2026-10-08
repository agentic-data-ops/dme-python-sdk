"""
SAN (Storage Area Network) 相关操作
包含LUN、LUN组、映射视图、存储主机、存储主机组、端口组等子主题
"""

import sys
import os

from pydme.client import DMEAPIClient

# ============================================================================
# LUN 子主题函数
# ============================================================================

"""
LUN (Volume) 相关操作
"""

import sys
import os

from pydme.client import DMEAPIClient


def lun_list(client: DMEAPIClient, limit: int = 1000, offset: int = 0,
                 sort_dir: str = None, sort_key: str = None, name: str = None,
                 vstore_raw_id: str = None, vstore_name: str = None,
                 status: str = None, health_status: str = None,
                 service_level_id: str = None, volume_wwn: str = None,
                 storage_id: str = None, pool_raw_id: str = None,
                 host_id: str = None, hostgroup_id: str = None,
                 unmapped_host_id: str = None, unmapped_hostgroup_id: str = None,
                 project_id: str = None, allocate_type: str = None,
                 attached: bool = None, query_mode: str = None,
                 protected: bool = None, pg_id: str = None,
                 usage_type: str = None,
                 support_provisioning: bool = None) -> dict:
    url = "/rest/blockservice/v1/volumes"
    
    query_params = {
        'limit': limit,
        'offset': offset
    }
    
    if sort_dir is not None:
        query_params['sort_dir'] = sort_dir
    if sort_key is not None:
        query_params['sort_key'] = sort_key
    if name is not None:
        query_params['name'] = name
    if vstore_raw_id is not None:
        query_params['vstore_raw_id'] = vstore_raw_id
    if vstore_name is not None:
        query_params['vstore_name'] = vstore_name
    if status is not None:
        query_params['status'] = status
    if health_status is not None:
        query_params['health_status'] = health_status
    if service_level_id is not None:
        query_params['service_level_id'] = service_level_id
    if volume_wwn is not None:
        query_params['volume_wwn'] = volume_wwn
    if storage_id is not None:
        query_params['storage_id'] = storage_id
    if pool_raw_id is not None:
        query_params['pool_raw_id'] = pool_raw_id
    if host_id is not None:
        query_params['host_id'] = host_id
    if hostgroup_id is not None:
        query_params['hostgroup_id'] = hostgroup_id
    if unmapped_host_id is not None:
        query_params['unmapped_host_id'] = unmapped_host_id
    if unmapped_hostgroup_id is not None:
        query_params['unmapped_hostgroup_id'] = unmapped_hostgroup_id
    if project_id is not None:
        query_params['project_id'] = project_id
    if allocate_type is not None:
        query_params['allocate_type'] = allocate_type
    if attached is not None:
        query_params['attached'] = attached
    if query_mode is not None:
        query_params['query_mode'] = query_mode
    if protected is not None:
        query_params['protected'] = protected
    if pg_id is not None:
        query_params['pg_id'] = pg_id
    if usage_type is not None:
        query_params['usage_type'] = usage_type
    if support_provisioning is not None:
        query_params['support_provisioning'] = support_provisioning
    
    response = client.get(url, params=query_params)
    return response


def lun_show(client: DMEAPIClient, volume_id: str) -> dict:
    url = "/rest/blockservice/v1/volumes/{volume_id}"

    if not volume_id:
        raise ValueError("volume_id 是必选参数")

    response = client.get(url, params={"volume_id": volume_id})
    return response


def lun_create(client: DMEAPIClient, storage_id: str, lun_specs: list = None,
                  lun_specs_pass_through: list = None, pool_id: str = None,
                  vstore_id: str = None, owner_controller: str = None,
                  initial_distribute_policy: str = None, prefetch_policy: str = None,
                  prefetch_value: int = None, tuning: dict = None,
                  mapping: dict = None, task_remarks: str = None) -> dict:
    url = "/rest/blockservice/v1/volumes/customize"

    if not storage_id:
        raise ValueError("storage_id 是必选参数")

    payload = {
        'storage_id': storage_id
    }

    if lun_specs is not None:
        payload['lun_specs'] = lun_specs
    if lun_specs_pass_through is not None:
        payload['lun_specs_pass_through'] = lun_specs_pass_through
    if pool_id is not None:
        payload['pool_id'] = pool_id
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id
    if owner_controller is not None:
        payload['owner_controller'] = owner_controller
    if initial_distribute_policy is not None:
        payload['initial_distribute_policy'] = initial_distribute_policy
    if prefetch_policy is not None:
        payload['prefetch_policy'] = prefetch_policy
    if prefetch_value is not None:
        payload['prefetch_value'] = prefetch_value
    if tuning is not None:
        payload['tuning'] = tuning
    if mapping is not None:
        payload['mapping'] = mapping
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def lun_delete(client: DMEAPIClient, volume_ids: list, task_remarks: str = None) -> dict:
    url = "/rest/blockservice/v1/volumes/delete"

    if not volume_ids or len(volume_ids) == 0:
        raise ValueError("volume_ids 是必选参数")

    payload = {
        'volume_ids': volume_ids
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def lun_modify(client: DMEAPIClient, volume_id: str, name: str = None,
                  description: str = None, owner_controller: str = None,
                  prefetch_policy: str = None, prefetch_value: int = None,
                  tuning: dict = None, task_remarks: str = None) -> dict:
    url = "/rest/blockservice/v1/volumes/{volume_id}"

    if not volume_id:
        raise ValueError("volume_id 是必选参数")

    volume = {}
    if name is not None:
        volume['name'] = name
    if description is not None:
        volume['description'] = description
    if owner_controller is not None:
        volume['owner_controller'] = owner_controller
    if prefetch_policy is not None:
        volume['prefetch_policy'] = prefetch_policy
    if prefetch_value is not None:
        volume['prefetch_value'] = prefetch_value
    if tuning is not None:
        volume['tuning'] = tuning

    payload = {
        'volume': volume
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.put(url, body=payload, params={"volume_id": volume_id})
    return response


def lun_modify_name(client: DMEAPIClient, volumes: list) -> dict:
    url = "/rest/blockservice/v1/volumes"

    if not volumes or len(volumes) == 0:
        raise ValueError("volumes 是必选参数")

    payload = {
        'volumes': volumes
    }

    response = client.put(url, body=payload)
    return response


def lun_expand(client: DMEAPIClient, volumes: list, task_remarks: str = None) -> dict:
    url = "/rest/blockservice/v1/volumes/expand"

    if not volumes or len(volumes) == 0:
        raise ValueError("volumes 是必选参数")

    payload = {
        'volumes': volumes
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response



def lun_connection(client: DMEAPIClient, volume_ids: list) -> dict:
    url = "/rest/blockservice/v1/volumes/connection-infos-query"

    if not volume_ids or len(volume_ids) == 0:
        raise ValueError("volume_ids 是必选参数")

    payload = {
        'lun_ids': volume_ids
    }

    response = client.post(url, body=payload)
    return response


def lun_group_list(client: DMEAPIClient, page_size: int = 20, page_no: int = 1,
                    sort_dir: str = None, sort_key: str = None,
                    name: str = None, vstore_raw_id: str = None,
                    vstore_name: str = None, storage_id: str = None,
                    storage_name: str = None, raw_id: str = None,
                    attached: bool = None,
                    protection_group_raw_id: str = None,
                    avaiable_mapping_for_host_id: str = None,
                    avaiable_mapping_for_host_group_id: str = None,
                    support_provisioning: bool = None) -> dict:
    url = "/rest/blockservice/v1/lun-groups/query"

    body_params = {
        'page_no': page_no,
        'page_size': page_size
    }

    if sort_dir is not None:
        body_params['sort_dir'] = sort_dir
    if sort_key is not None:
        body_params['sort_key'] = sort_key
    if name is not None:
        body_params['name'] = name
    if vstore_raw_id is not None:
        body_params['vstore_raw_id'] = vstore_raw_id
    if vstore_name is not None:
        body_params['vstore_name'] = vstore_name
    if storage_id is not None:
        body_params['storage_id'] = storage_id
    if storage_name is not None:
        body_params['storage_name'] = storage_name
    if raw_id is not None:
        body_params['raw_id'] = raw_id
    if attached is not None:
        body_params['attached'] = attached
    if protection_group_raw_id is not None:
        body_params['protection_group_raw_id'] = protection_group_raw_id
    if avaiable_mapping_for_host_id is not None:
        body_params['avaiable_mapping_for_host_id'] = avaiable_mapping_for_host_id
    if avaiable_mapping_for_host_group_id is not None:
        body_params['avaiable_mapping_for_host_group_id'] = avaiable_mapping_for_host_group_id
    if support_provisioning is not None:
        body_params['support_provisioning'] = support_provisioning

    response = client.post(url, body=body_params)
    return response


def lun_group_show(client: DMEAPIClient, group_id: str, storage_id: str = None) -> dict:
    url = "/rest/blockservice/v1/lun-groups/{group_id}"

    response = client.get(url, params={"group_id": group_id})
    return response


def lun_group_create(client: DMEAPIClient, storage_id: str, name: str,
                     description: str = None, existing_lun_ids: list = None,
                     customize_volumes: dict = None, task_remarks: str = None,
                     vstore_id: str = None, zoning_info: dict = None,
                     mapping_view: dict = None) -> dict:
    url = "/rest/blockservice/v1/lun-groups"

    if not storage_id or not name:
        raise ValueError("storage_id 和 name 是必选参数")

    body_params = {
        'storage_id': storage_id,
        'name': name
    }

    if description is not None:
        body_params['description'] = description
    if existing_lun_ids is not None:
        body_params['existing_lun_ids'] = existing_lun_ids
    if customize_volumes is not None:
        body_params['customize_volumes'] = customize_volumes
    if task_remarks is not None:
        body_params['task_remarks'] = task_remarks
    if vstore_id is not None:
        body_params['vstore_id'] = vstore_id
    if zoning_info is not None:
        body_params['zoning_info'] = zoning_info
    if mapping_view is not None:
        body_params['mapping_view'] = mapping_view

    response = client.post(url, body=body_params)
    return response


def lun_group_delete(client: DMEAPIClient, lun_group_ids: list,
                     task_remarks: str = None) -> dict:
    url = "/rest/blockservice/v1/lun-groups/delete"

    if not lun_group_ids or len(lun_group_ids) == 0:
        raise ValueError("lun_group_ids 是必选参数")

    body_params = {
        'lun_group_ids': lun_group_ids
    }

    if task_remarks is not None:
        body_params['task_remarks'] = task_remarks

    response = client.post(url, body=body_params)
    return response


def lun_group_add_luns(client: DMEAPIClient, group_id: str,
                       existing_lun_ids: list = None,
                       customize_volumes: dict = None,
                       host_lun_id_infos: list = None,
                       host_lun_id_verify: bool = False,
                       task_remarks: str = None) -> dict:
    url = "/rest/blockservice/v1/lun-groups/{group_id}/add-luns"

    body_params = {}

    if existing_lun_ids is not None:
        body_params['existing_lun_ids'] = existing_lun_ids
    if customize_volumes is not None:
        body_params['customize_volumes'] = customize_volumes
    if host_lun_id_infos is not None:
        body_params['host_lun_id_infos'] = host_lun_id_infos

    body_params = {}

    if existing_lun_ids is not None:
        body_params['existing_lun_ids'] = existing_lun_ids
    if customize_volumes is not None:
        body_params['customize_volumes'] = customize_volumes
    if host_lun_id_infos is not None:
        body_params['host_lun_id_infos'] = host_lun_id_infos
    if host_lun_id_verify is not False:
        body_params['host_lun_id_verify'] = host_lun_id_verify
    if task_remarks is not None:
        body_params['task_remarks'] = task_remarks

    response = client.post(url, body=body_params)
    return response


def lun_group_remove_luns(client: DMEAPIClient, group_id: str,
                           lun_ids: list, task_remarks: str = None) -> dict:
    url = "/rest/blockservice/v1/lun-groups/{group_id}/remove-luns"

    body_params = {
        'lun_ids': lun_ids
    }

    if task_remarks is not None:
        body_params['task_remarks'] = task_remarks

    response = client.post(url, body=body_params, params={"group_id": group_id})
    return response


def lun_group_show_luns(client: DMEAPIClient, group_id: str,
                         page_size: int = 100, page_no: int = 1,
                         health_status: str = None) -> dict:
    url = "/rest/blockservice/v1/lun-groups/{group_id}/luns/query"

    body_params = {
        'page_size': page_size,
        'page_no': page_no
    }

    if health_status is not None:
        body_params['health_status'] = health_status


    body_params = {
        'page_size': page_size,
        'page_no': page_no
    }

    if health_status is not None:
        body_params['health_status'] = health_status

    response = client.post(url, body=body_params)
    return response


# 动作列表，用于 CLI 帮助

# ============================================================================
# 映射视图 (mapping_view) 子主题函数
# ============================================================================



import sys
import os

from pydme.client import DMEAPIClient


def mapping_view_create(
    client: DMEAPIClient,
    storage_id: str, name: str = None,
    port_group_id: str = None,
    start_host_lun_id: int = None,
    host: dict = None, vbs: dict = None,
    host_group: dict = None,
    lun_group: dict = None,
    luns: dict = None,
    task_remarks: str = None
) -> dict:
    url = "/rest/blockservice/v1/mapping-views"

    body_params = {
        'storage_id': storage_id
    }

    if name is not None:
        body_params['name'] = name
    if port_group_id is not None:
        body_params['port_group_id'] = port_group_id
    if start_host_lun_id is not None:
        body_params['start_host_lun_id'] = start_host_lun_id
    if host is not None:
        body_params['host'] = host
    if vbs is not None:
        body_params['vbs'] = vbs
    if host_group is not None:
        body_params['host_group'] = host_group
    if lun_group is not None:
        body_params['lun_group'] = lun_group
    if luns is not None:
        body_params['luns'] = luns
    if task_remarks is not None:
        body_params['task_remarks'] = task_remarks

    response = client.post(url, body=body_params)
    return response


def mapping_view_delete(client: DMEAPIClient, ids: list) -> dict:
    url = "/rest/blockservice/v1/mapping-views/batch-delete"

    if not ids or len(ids) == 0:
        raise ValueError("ids 是必选参数")

    body_params = {
        'ids': ids
    }

    response = client.post(url, body=body_params)
    return response


def mapping_view_list(
    client: DMEAPIClient,
    page_size: int = 100,
    page_no: int = 1,
    name: str = None,
    raw_id: str = None,
    storage_id: str = None,
    lun_id: str = None,
    lun_name: str = None,
    lun_group_id: str = None,
    lun_group_raw_id: str = None,
    lun_group_name: str = None,
    storage_host_id: str = None,
    storage_host_name: str = None,
    storage_host_group_id: str = None,
    storage_host_group_name: str = None,
    storage_host_group_raw_id: str = None,
    port_group_id: str = None,
    port_group_raw_id: str = None,
    port_group_name: str = None,
    sort_key: str = None,
    sort_dir: str = None
) -> dict:
    url = "/rest/blockservice/v1/mapping-views/query"

    body_params = {
        'page_size': page_size,
        'page_no': page_no
    }

    if name is not None:
        body_params['name'] = name

    if raw_id is not None:
        body_params['raw_id'] = raw_id

    if storage_id is not None:
        body_params['storage_id'] = storage_id

    if lun_id is not None:
        body_params['lun_id'] = lun_id

    if lun_name is not None:
        body_params['lun_name'] = lun_name

    if lun_group_id is not None:
        body_params['lun_group_id'] = lun_group_id

    if lun_group_raw_id is not None:
        body_params['lun_group_raw_id'] = lun_group_raw_id

    if lun_group_name is not None:
        body_params['lun_group_name'] = lun_group_name

    if storage_host_id is not None:
        body_params['storage_host_id'] = storage_host_id

    if storage_host_name is not None:
        body_params['storage_host_name'] = storage_host_name

    if storage_host_group_id is not None:
        body_params['storage_host_group_id'] = storage_host_group_id

    if storage_host_group_name is not None:
        body_params['storage_host_group_name'] = storage_host_group_name

    if storage_host_group_raw_id is not None:
        body_params['storage_host_group_raw_id'] = storage_host_group_raw_id

    if port_group_id is not None:
        body_params['port_group_id'] = port_group_id

    if port_group_raw_id is not None:
        body_params['port_group_raw_id'] = port_group_raw_id

    if port_group_name is not None:
        body_params['port_group_name'] = port_group_name

    if sort_key is not None:
        body_params['sort_key'] = sort_key

    if sort_dir is not None:
        body_params['sort_dir'] = sort_dir

    response = client.post(url, body=body_params)
    return response




def mapping_view_query(
    client: DMEAPIClient,
    type: str,
    request_id: str,
    storage_id: str
) -> dict:
    """
    查询物理主机（组）关联的映射关系

    根据物理主机/主机组 ID 过滤查询指定存储设备上的映射视图。

    Args:
        client: DME API 客户端
        type: 查询类别 (必选)。可选值：host (物理主机), host_group (主机组)
        request_id: 物理主机/主机组 ID (必选, 1~64个字符)
        storage_id: 存储设备 ID (必选, 1~64个字符)

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }，包含映射视图列表
    """
    url = "/rest/blockservice/v1/volumes/mapping-view/query"

    body_params = {
        'type': type,
        'request_id': request_id,
        'storage_id': storage_id
    }

    response = client.post(url, body=body_params)
    return response


def physical_host_show_mapping_views(client: DMEAPIClient, host_id: str,
                                      storage_id: str) -> dict:
    return mapping_view_query(
        client=client, type="host",
        request_id=host_id, storage_id=storage_id
    )


def physical_host_group_show_mapping_views(client: DMEAPIClient, host_group_id: str,
                                            storage_id: str) -> dict:
    return mapping_view_query(
        client=client, type="host_group",
        request_id=host_group_id, storage_id=storage_id
    )


# ============================================================================
# 存储主机 (storage_host) 子主题函数
# ============================================================================

def storage_host_create(client: DMEAPIClient, storage_id: str,
                host_info: dict, task_remarks: str = None,
                vstore_id: str = None) -> dict:
    url = "/rest/hostmgmt/v1/storage-hosts"

    payload = {
        'storage_id': storage_id,
        'host_info': host_info
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id

    response = client.post(url, body=payload)
    return response


def storage_host_batch_query(client: DMEAPIClient, ids: list) -> dict:
    url = "/rest/hostmgmt/v1/storage-hosts/query-by-ids"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def storage_host_list(client: DMEAPIClient, page_size: int = None, page_no: int = None,
              sort_key: str = None, sort_dir: str = None, name: str = None,
              raw_id: str = None, host_group_id: str = None,
              avaliable_add_to_host_group_id: str = None, host_group_name: str = None,
              ip: str = None, health_status: str = None, os_type: str = None,
              storage_id: str = None, avaiable_mapping_for_lun_group_id: str = None,
              avaiable_mapping_for_lun_id: str = None, support_provisioning: bool = None,
              manufacturer: str = None, vstore_raw_id: str = None,
              vstore_name: str = None) -> dict:
    url = "/rest/hostmgmt/v1/storage-hosts/query"

    payload = {}

    if page_size is not None:
        payload['page_size'] = page_size
    if page_no is not None:
        payload['page_no'] = page_no
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if name is not None:
        payload['name'] = name
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if host_group_id is not None:
        payload['host_group_id'] = host_group_id
    if avaliable_add_to_host_group_id is not None:
        payload['avaliable_add_to_host_group_id'] = avaliable_add_to_host_group_id
    if host_group_name is not None:
        payload['host_group_name'] = host_group_name
    if ip is not None:
        payload['ip'] = ip
    if health_status is not None:
        payload['health_status'] = health_status
    if os_type is not None:
        payload['os_type'] = os_type
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if avaiable_mapping_for_lun_group_id is not None:
        payload['avaiable_mapping_for_lun_group_id'] = avaiable_mapping_for_lun_group_id
    if avaiable_mapping_for_lun_id is not None:
        payload['avaiable_mapping_for_lun_id'] = avaiable_mapping_for_lun_id
    if support_provisioning is not None:
        payload['support_provisioning'] = support_provisioning
    if manufacturer is not None:
        payload['manufacturer'] = manufacturer
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if vstore_name is not None:
        payload['vstore_name'] = vstore_name

    response = client.post(url, body=payload)
    return response


def storage_host_modify(client: DMEAPIClient, storage_host_id: str,
                storage_host_name: str = None, storage_host_description: str = None,
                storage_host_ip: str = None, storage_host_os_type: str = None,
                add_initiators: list = None, remove_initiators: list = None,
                multipath: dict = None, access_mode: str = None,
                hyper_metro_path_optimized: bool = None, task_remarks: str = None) -> dict:
    url = "/rest/hostmgmt/v1/storage-hosts/{storage_host_id}"

    payload = {}

    if storage_host_name is not None:
        payload['storage_host_name'] = storage_host_name
    if storage_host_description is not None:
        payload['storage_host_description'] = storage_host_description
    if storage_host_ip is not None:
        payload['storage_host_ip'] = storage_host_ip

    payload = {}

    if storage_host_name is not None:
        payload['storage_host_name'] = storage_host_name
    if storage_host_description is not None:
        payload['storage_host_description'] = storage_host_description
    if storage_host_ip is not None:
        payload['storage_host_ip'] = storage_host_ip
    if storage_host_os_type is not None:
        payload['storage_host_os_type'] = storage_host_os_type
    if add_initiators is not None:
        payload['add_initiators'] = add_initiators
    if remove_initiators is not None:
        payload['remove_initiators'] = remove_initiators
    if multipath is not None:
        payload['multipath'] = multipath
    if access_mode is not None:
        payload['access_mode'] = access_mode
    if hyper_metro_path_optimized is not None:
        payload['hyper_metro_path_optimized'] = hyper_metro_path_optimized
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.put(url, body=payload, params={"storage_host_id": storage_host_id})
    return response


def storage_host_delete(client: DMEAPIClient, host_ids: list) -> dict:
    url = "/rest/hostmgmt/v1/storage-hosts/delete"

    payload = {
        'host_ids': host_ids
    }

    response = client.post(url, body=payload)
    return response


def storage_host_show_paths(client: DMEAPIClient, page_no: int = None, page_size: int = None,
                    storage_id: str = None, storage_host_ids: list = None,
                    storage_host_raw_ids: list = None, health_status: str = None,
                    running_status: str = None, initiator_type: str = None) -> dict:
    url = "/rest/hostmgmt/v1/host-links/query"

    payload = {}

    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if storage_host_ids is not None:
        payload['storage_host_ids'] = storage_host_ids
    if storage_host_raw_ids is not None:
        payload['storage_host_raw_ids'] = storage_host_raw_ids
    if health_status is not None:
        payload['health_status'] = health_status
    if running_status is not None:
        payload['running_status'] = running_status
    if initiator_type is not None:
        payload['initiator_type'] = initiator_type

    response = client.post(url, body=payload)
    return response
# ============================================================================
# 存储主机组 (storage_host_group) 子主题函数
# ============================================================================

def storage_host_group_create(client: DMEAPIClient, storage_id: str, name: str,
                      description: str = None, exist_host_ids: list = None,
                      create_storage_host_params: dict = None,
                      task_remarks: str = None, vstore_id: str = None) -> dict:
    url = "/rest/hostmgmt/v1/storage-hostgroups"

    payload = {
        'storage_id': storage_id,
        'name': name
    }

    if description is not None:
        payload['description'] = description
    if exist_host_ids is not None:
        payload['exist_host_ids'] = exist_host_ids
    if create_storage_host_params is not None:
        payload['create_storage_host_params'] = create_storage_host_params
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id

    response = client.post(url, body=payload)
    return response


def storage_host_group_list(client: DMEAPIClient, storage_id: str = None, name: str = None,
                    raw_id: str = None, vstore_id: str = None,
                    vstore_name: str = None, page_no: int = None,
                    page_size: int = None, sort_key: str = None,
                    sort_dir: str = None, avaiable_mapping_for_lun_group_id: str = None,
                    avaiable_mapping_for_lun_id: str = None,
                    support_provisioning: bool = None) -> dict:
    url = "/rest/hostmgmt/v1/storage-hostgroups/query"

    payload = {}

    if storage_id is not None:
        payload['storage_id'] = storage_id
    if name is not None:
        payload['name'] = name
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id
    if vstore_name is not None:
        payload['vstore_name'] = vstore_name
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if avaiable_mapping_for_lun_group_id is not None:
        payload['avaiable_mapping_for_lun_group_id'] = avaiable_mapping_for_lun_group_id
    if avaiable_mapping_for_lun_id is not None:
        payload['avaiable_mapping_for_lun_id'] = avaiable_mapping_for_lun_id
    if support_provisioning is not None:
        payload['support_provisioning'] = support_provisioning

    response = client.post(url, body=payload)
    return response


def storage_host_group_add_hosts(client: DMEAPIClient, storage_host_group_id: str,
                         storage_host_id_ids: list = None,
                         create_storage_host_params: dict = None,
                         task_remarks: str = None) -> dict:
    url = "/rest/hostmgmt/v1/storage-hostgroups/{storage_host_group_id}/hosts/add"

    payload = {}

    if storage_host_id_ids is not None:
        payload['storage_host_id_ids'] = storage_host_id_ids
    if create_storage_host_params is not None:
        payload['create_storage_host_params'] = create_storage_host_params
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    payload = {}

    if storage_host_id_ids is not None:
        payload['storage_host_id_ids'] = storage_host_id_ids
    if create_storage_host_params is not None:
        payload['create_storage_host_params'] = create_storage_host_params
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.put(url, body=payload, params={"storage_host_group_id": storage_host_group_id})
    return response


def storage_host_group_remove_hosts(client: DMEAPIClient, storage_host_group_id: str,
                            storage_host_ids: list,
                            task_remarks: str = None) -> dict:
    url = "/rest/hostmgmt/v1/storage-hostgroups/{storage_host_group_id}/hosts/remove"

    payload = {
        'storage_host_ids': storage_host_ids
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.put(url, body=payload, params={"storage_host_group_id": storage_host_group_id})
    return response


def storage_host_group_delete(client: DMEAPIClient, host_group_ids: list,
                      task_remarks: str = None) -> dict:
    url = "/rest/hostmgmt/v1/storage-hostgroups/delete"

    payload = {
        'host_group_ids': host_group_ids
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def storage_host_show_luns(client: DMEAPIClient, storage_host_id: str,
                   name: str = None, page_size: int = 20,
                   page_no: int = 1, sort_key: str = None,
                   sort_dir: str = None) -> dict:
    url = "/rest/blockservice/v1/lun-mapping/query"

    payload = {
        'storage_host_id': storage_host_id,
        'page_size': page_size,
        'page_no': page_no
    }

    if name is not None:
        payload['name'] = name
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def storage_host_group_show_luns(client: DMEAPIClient, storage_host_group_id: str,
                         name: str = None, page_size: int = 20,
                         page_no: int = 1, sort_key: str = None,
                         sort_dir: str = None) -> dict:
    url = "/rest/blockservice/v1/lun-mapping/query"

    payload = {
        'storage_host_group_id': storage_host_group_id,
        'page_size': page_size,
        'page_no': page_no
    }

    if name is not None:
        payload['name'] = name
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response
# ============================================================================
# 端口组 (port_group) 子主题函数
# ============================================================================

def port_group_list(client: DMEAPIClient, storage_id: str = None,
                    page_no: int = 1, page_size: int = 20) -> dict:
    url = "/rest/storagemgmt/v1/port-groups/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if storage_id is not None:
        payload['storage_id'] = storage_id

    response = client.post(url, body=payload)
    return response


def port_group_create(client: DMEAPIClient, storage_id: str, name: str,
                      description: str = None, port_ids: list = None) -> dict:
    url = "/rest/storagemgmt/v1/port-groups"

    body_params = {
        'storage_id': storage_id,
        'name': name
    }

    if description is not None:
        body_params['description'] = description
    if port_ids is not None:
        body_params['port_ids'] = port_ids

    response = client.post(url, body=body_params)
    return response


def port_group_show_ports(client: DMEAPIClient, port_group_id: str,
                          type: str = None, page_no: int = 1,
                          page_size: int = 20) -> dict:
    url = "/rest/storagemgmt/v1/port-groups/{port_group_id}/ports/query"

    payload = {}

    if type is not None:
        payload['type'] = type
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size

    payload = {}

    if type is not None:
        payload['type'] = type
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size

    response = client.post(url, body=payload, params={"port_group_id": port_group_id})
    return response


def port_group_show_relations(client: DMEAPIClient, page_no: int = 1,
                              page_size: int = 20) -> dict:
    url = "/rest/storagemgmt/v1/port-groups/ports/relations/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    response = client.post(url, body=payload)
    return response




# ============================================================================
# 动作列表，用于 CLI 帮助
# ============================================================================


# ============================================================================
# 物理主机 (physical_host) 子主题函数
# ============================================================================

def physical_host_list(client: DMEAPIClient, limit: int = None, start: int = None,
               sort_key: str = None, sort_dir: str = None, name: str = None,
               host_group_name: str = None, ip: str = None,
               display_status: str = None, managed_status: list = None,
               os_type: str = None, access_mode: str = None,
               az_id: str = None, az_ids: list = None,
               project_id: str = None) -> dict:
    url = "/rest/hostmgmt/v1/hosts/summary"

    payload = {}

    if limit is not None:
        payload['limit'] = limit
    if start is not None:
        payload['start'] = start
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if name is not None:
        payload['name'] = name
    if host_group_name is not None:
        payload['host_group_name'] = host_group_name
    if ip is not None:
        payload['ip'] = ip
    if display_status is not None:
        payload['display_status'] = display_status
    if managed_status is not None:
        payload['managed_status'] = managed_status
    if os_type is not None:
        payload['os_type'] = os_type
    if access_mode is not None:
        payload['access_mode'] = access_mode
    if az_id is not None:
        payload['az_id'] = az_id
    if az_ids is not None:
        payload['az_ids'] = az_ids
    if project_id is not None:
        payload['project_id'] = project_id

    response = client.post(url, body=payload)
    return response


def physical_host_show(client: DMEAPIClient, host_id: str) -> dict:
    url = "/rest/hostmgmt/v1/hosts/{host_id}/summary"

    response = client.get(url, params={"host_id": host_id})
    return response


def physical_host_create(client: DMEAPIClient, access_mode: str, type: str,
                host_name: str = None, ip: str = None, port: int = None,
                username: str = None, password: str = None,
                description: str = None, initiator: list = None,
                azs: list = None, project_id: str = None,
                sync_to_storage: bool = False, multipath_type: str = None,
                path_type: str = None, failover_mode: str = None,
                special_mode_type: str = None, save_public_key: bool = False) -> dict:
    url = "/rest/hostmgmt/v1/hosts"

    payload = {
        'access_mode': access_mode,
        'type': type
    }

    if host_name is not None:
        payload['host_name'] = host_name
    if ip is not None:
        payload['ip'] = ip
    if port is not None:
        payload['port'] = port
    if username is not None:
        payload['username'] = username
    if password is not None:
        payload['password'] = password
    if description is not None:
        payload['description'] = description
    if initiator is not None:
        payload['initiator'] = initiator
    if azs is not None:
        payload['azs'] = azs
    if project_id is not None:
        payload['project_id'] = project_id
    if sync_to_storage is not None:
        payload['sync_to_storage'] = sync_to_storage
    if multipath_type is not None:
        payload['multipath_type'] = multipath_type
    if path_type is not None:
        payload['path_type'] = path_type
    if failover_mode is not None:
        payload['failover_mode'] = failover_mode
    if special_mode_type is not None:
        payload['special_mode_type'] = special_mode_type
    if save_public_key is not None:
        payload['save_public_key'] = save_public_key

    response = client.post(url, body=payload)
    return response


def physical_host_modify(client: DMEAPIClient, host_id: str,
                ip: str = None, host_name: str = None,
                os_type: str = None, azs: list = None,
                project_id: str = None) -> dict:
    url = "/rest/hostmgmt/v1/hosts/{host_id}/general"

    payload = {}

    if ip is not None:
        payload['ip'] = ip
    if host_name is not None:
        payload['host_name'] = host_name
    if os_type is not None:
        payload['os_type'] = os_type

    payload = {}

    if ip is not None:
        payload['ip'] = ip
    if host_name is not None:
        payload['host_name'] = host_name
    if os_type is not None:
        payload['os_type'] = os_type
    if azs is not None:
        payload['azs'] = azs
    if project_id is not None:
        payload['project_id'] = project_id

    response = client.put(url, body=payload, params={"host_id": host_id})
    return response


def physical_host_modify_access_info(client: DMEAPIClient, host_id: str,
                ip: str = None, port: int = None, username: str = None,
                password: str = None, project_id: str = None,
                azs: list = None, sync_to_storage: bool = False,
                description: str = None, multipath_type: str = None,
                path_type: str = None, failover_mode: str = None,
                special_mode_type: str = None) -> dict:
    url = "/rest/hostmgmt/v1/hosts/{host_id}/accessinfo"

    payload = {}

    if ip is not None:
        payload['ip'] = ip
    if port is not None:
        payload['port'] = port
    if username is not None:
        payload['username'] = username

    payload = {}

    if ip is not None:
        payload['ip'] = ip
    if port is not None:
        payload['port'] = port
    if username is not None:
        payload['username'] = username
    if password is not None:
        payload['password'] = password
    if project_id is not None:
        payload['project_id'] = project_id
    if azs is not None:
        payload['azs'] = azs
    if sync_to_storage is not None:
        payload['sync_to_storage'] = sync_to_storage
    if description is not None:
        payload['description'] = description
    if multipath_type is not None:
        payload['multipath_type'] = multipath_type
    if path_type is not None:
        payload['path_type'] = path_type
    if failover_mode is not None:
        payload['failover_mode'] = failover_mode
    if special_mode_type is not None:
        payload['special_mode_type'] = special_mode_type

    response = client.put(url, body=payload, params={"host_id": host_id})
    return response


def physical_host_delete(client: DMEAPIClient, host_id: str,
                sync_to_storage: bool = False) -> dict:
    url = "/rest/hostmgmt/v1/hosts/{host_id}"

    response = client.delete(url, params={"host_id": host_id, "sync_to_storage": str(sync_to_storage).lower()})
    return response


def physical_host_add_initiators(client: DMEAPIClient, host_id: str,
                  initiators: list) -> dict:
    url = "/rest/hostmgmt/v1/hosts/{host_id}/initiators/add"

    payload = {
        'initiators': initiators
    }

    response = client.put(url, body=payload, params={"host_id": host_id})
    return response


def physical_host_remove_initiators(client: DMEAPIClient, host_id: str,
                     initiators: list) -> dict:
    url = "/rest/hostmgmt/v1/hosts/{host_id}/initiators/remove"

    payload = {
        'initiators': initiators
    }

    response = client.put(url, body=payload, params={"host_id": host_id})
    return response


def physical_host_show_initiators(client: DMEAPIClient, host_id: str,
                   port_name: str = None, protocol: str = None,
                   status: str = None) -> dict:
    url = "/rest/hostmgmt/v1/hosts/{host_id}/initiators"

    params = {}
    if port_name is not None:
        params['port_name'] = port_name
    if protocol is not None:
        params['protocol'] = protocol
    if status is not None:
        params['status'] = status


    params = {}
    if port_name is not None:
        params['port_name'] = port_name
    if protocol is not None:
        params['protocol'] = protocol
    if status is not None:
        params['status'] = status

    response = client.get(url, params=params)
    return response


def physical_host_test(client: DMEAPIClient, storage_id: str,
         host_ids: list = None, hostgroup_id: str = None,
         auto_zoning: bool = False,
         target_fcports: list = None,
         target_fcportgroups: list = None) -> dict:
    url = "/rest/hostmgmt/v1/connectivity/host-and-storage"

    payload = {
        'storage_id': storage_id
    }

    if host_ids is not None:
        payload['host_ids'] = host_ids
    if hostgroup_id is not None:
        payload['hostgroup_id'] = hostgroup_id
    if auto_zoning is not None:
        payload['auto_zoning'] = auto_zoning
    if target_fcports is not None:
        payload['target_fcports'] = target_fcports
    if target_fcportgroups is not None:
        payload['target_fcportgroups'] = target_fcportgroups

    response = client.post(url, body=payload)
    return response


def physical_host_save_sshkey(client: DMEAPIClient, ip: str, key: str,
                port: int = None) -> dict:
    url = "/rest/hostmgmt/v1/host-keys"

    payload = {
        'ip': ip,
        'key': key
    }

    if port is not None:
        payload['port'] = port

    response = client.put(url, body=payload)
    return response


def physical_host_query_sshkey(client: DMEAPIClient, ip: str,
                 port: int = None) -> dict:
    url = "/rest/hostmgmt/v1/host-keys"

    params = {
        'ip': ip
    }

    if port is not None:
        params['port'] = port

    response = client.get(url, params=params)
    return response


def physical_host_query_by_initiator(client: DMEAPIClient, initiator_id: str = None,
                         raw_id: str = None, protocol: str = None) -> dict:
    url = "/rest/hostmgmt/v1/hosts/query-by-initiator"

    payload = {}

    if initiator_id is not None:
        payload['initiator_id'] = initiator_id
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if protocol is not None:
        payload['protocol'] = protocol

    response = client.post(url, body=payload)
    return response


def physical_host_map_luns(client: DMEAPIClient, volume_ids: list, host_id: str,
            mapping_policy: list = None, task_remarks: str = None) -> dict:
    url = "/rest/blockservice/v1/volumes/host-mapping"

    payload = {
        'volume_ids': volume_ids,
        'host_id': host_id
    }

    if mapping_policy is not None:
        payload['mapping_policy'] = mapping_policy

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def physical_host_unmap_luns(client: DMEAPIClient, volume_ids: list, host_id: str,
              task_remarks: str = None) -> dict:
    url = "/rest/blockservice/v1/volumes/host-unmapping"

    payload = {
        'volume_ids': volume_ids,
        'host_id': host_id,
        'host_type': "host"
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def storage_host_unmap_luns(client: DMEAPIClient, volume_ids: list, host_id: str,
              task_remarks: str = None) -> dict:
    url = "/rest/blockservice/v1/volumes/host-unmapping"

    payload = {
        'volume_ids': volume_ids,
        'host_id': host_id,
        'host_type': "storage_host"
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


# ============================================================================
# 物理主机组 (physical_host_group) 子主题函数
# ============================================================================

def physical_host_group_list(client: DMEAPIClient, limit: int = None, start: int = None,
         sort_dir: str = None, sort_key: str = None, name: str = None,
         project_id: str = None, az_ids: list = None,
         managed_status: list = None) -> dict:
    url = "/rest/hostmgmt/v1/hostgroups/summary"

    payload = {}

    if limit is not None:
        payload['limit'] = limit
    if start is not None:
        payload['start'] = start
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if name is not None:
        payload['name'] = name
    if project_id is not None:
        payload['project_id'] = project_id
    if az_ids is not None:
        payload['az_ids'] = az_ids
    if managed_status is not None:
        payload['managed_status'] = managed_status

    response = client.post(url, body=payload)
    return response


def physical_host_group_show_hosts(client: DMEAPIClient, hostgroup_id: str,
                name: str = None, ip: str = None,
                display_status: list = None, managed_status: list = None,
                os_type: list = None, sort_key: str = None,
                sort_dir: str = None, page_size: int = 1024,
                page_no: int = 1) -> dict:
    url = "/rest/hostmgmt/v1/hostgroups/{hostgroup_id}/hosts/list"

    payload = {}

    if name is not None:
        payload['name'] = name
    if ip is not None:
        payload['ip'] = ip
    if display_status is not None:
        payload['display_status'] = display_status

    payload = {}

    if name is not None:
        payload['name'] = name
    if ip is not None:
        payload['ip'] = ip
    if display_status is not None:
        payload['display_status'] = display_status
    if managed_status is not None:
        payload['managed_status'] = managed_status
    if os_type is not None:
        payload['os_type'] = os_type
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if page_size is not None:
        payload['page_size'] = page_size
    if page_no is not None:
        payload['page_no'] = page_no

    response = client.post(url, body=payload, params={"hostgroup_id": hostgroup_id})
    return response


def physical_host_group_show(client: DMEAPIClient, hostgroup_id: str) -> dict:
    url = "/rest/hostmgmt/v1/hostgroups/{hostgroup_id}/summary"

    response = client.get(url, params={"hostgroup_id": hostgroup_id})
    return response


def physical_host_group_create(client: DMEAPIClient, name: str, host_ids: list,
           azs: list = None, project_id: str = None,
           description: str = None) -> dict:
    url = "/rest/hostmgmt/v1/hostgroups"

    payload = {
        'name': name,
        'host_ids': host_ids
    }

    if azs is not None:
        payload['azs'] = azs
    if project_id is not None:
        payload['project_id'] = project_id
    if description is not None:
        payload['description'] = description

    response = client.post(url, body=payload)
    return response


def physical_host_group_modify(client: DMEAPIClient, hostgroup_id: str,
           name: str = None, description: str = None,
           azs: list = None, project_id: str = None) -> dict:
    url = "/rest/hostmgmt/v1/hostgroups/{hostgroup_id}/general"

    payload = {}

    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description
    if azs is not None:
        payload['azs'] = azs

    payload = {}

    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description
    if azs is not None:
        payload['azs'] = azs
    if project_id is not None:
        payload['project_id'] = project_id

    response = client.put(url, body=payload, params={"hostgroup_id": hostgroup_id})
    return response


def physical_host_group_delete(client: DMEAPIClient, hostgroup_id: str,
           sync_to_storage: bool = False) -> dict:
    url = "/rest/hostmgmt/v1/hostgroups/{hostgroup_id}"

    response = client.delete(url, params={"hostgroup_id": hostgroup_id, "sync_to_storage": str(sync_to_storage).lower()})
    return response


def physical_host_group_add_hosts(client: DMEAPIClient, hostgroup_id: str,
             host_ids: list, sync_to_storage: bool = False) -> dict:
    url = "/rest/hostmgmt/v1/hostgroups/{hostgroup_id}/hosts/add"

    payload = {
        'host_ids': host_ids
    }

    response = client.put(url, body=payload, params={"hostgroup_id": hostgroup_id, "sync_to_storage": str(sync_to_storage).lower()})
    return response


def physical_host_group_remove_hosts(client: DMEAPIClient, hostgroup_id: str,
                host_ids: list, sync_to_storage: bool = False) -> dict:
    url = "/rest/hostmgmt/v1/hostgroups/{hostgroup_id}/hosts/remove"

    payload = {
        'host_ids': host_ids
    }

    response = client.put(url, body=payload, params={"hostgroup_id": hostgroup_id, "sync_to_storage": str(sync_to_storage).lower()})
    return response


def physical_host_group_map_luns(client: DMEAPIClient, volume_ids: list, hostgroup_id: str,
            mapping_policy: list = None, task_remarks: str = None) -> dict:
    url = "/rest/blockservice/v1/volumes/hostgroup-mapping"

    payload = {
        'volume_ids': volume_ids,
        'hostgroup_id': hostgroup_id
    }

    if mapping_policy is not None:
        payload['mapping_policy'] = mapping_policy

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def physical_host_group_unmap_luns(client: DMEAPIClient, volume_ids: list, hostgroup_id: str,
              task_remarks: str = None) -> dict:
    url = "/rest/blockservice/v1/volumes/hostgroup-unmapping"

    payload = {
        'volume_ids': volume_ids,
        'hostgroup_id': hostgroup_id,
        'host_group_type': "host_group"
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def storage_host_group_unmap_luns(client: DMEAPIClient, volume_ids: list, hostgroup_id: str,
              task_remarks: str = None) -> dict:
    url = "/rest/blockservice/v1/volumes/hostgroup-unmapping"

    payload = {
        'volume_ids': volume_ids,
        'hostgroup_id': hostgroup_id,
        'host_group_type': "storage_host_group"
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


# ============================================================================


def physical_host_group_show_related(client: DMEAPIClient, hostgroup_id: str,
                                       storage_ip: str = None,
                                       storage_name: str = None) -> dict:
    url = "/rest/hostmgmt/v1/hostgroups/{hostgroup_id}/related-storage-hostgroups"

    if not hostgroup_id:
        raise ValueError("hostgroup_id 是必选参数")

    params = {
        'hostgroup_id': hostgroup_id
    }
    if storage_ip is not None:
        params['storage_ip'] = storage_ip
    if storage_name is not None:
        params['storage_name'] = storage_name

    response = client.get(url, params=params)
    return response


def mapping_view_query_host_to_lun(client: DMEAPIClient, storage_id: str,
                                     name: str = None, mapping_type: str = None,
                                     host_info: dict = None, lun_info: dict = None,
                                     sort_key: str = None, sort_dir: str = None,
                                     page_size: int = 100, page_no: int = 1) -> dict:
    url = "/rest/blockservice/v1/mapping-views/query_for_host_to_lun"

    if not storage_id:
        raise ValueError("storage_id 是必选参数")

    payload = {
        'storage_id': storage_id,
        'page_size': page_size,
        'page_no': page_no
    }
    if name is not None:
        payload['name'] = name
    if mapping_type is not None:
        payload['mapping_type'] = mapping_type
    if host_info is not None:
        payload['host_info'] = host_info
    if lun_info is not None:
        payload['lun_info'] = lun_info
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


# ============================================================================
# 动作列表，用于 CLI 帮助
# ============================================================================

ACTIONS = {
    # LUN 子主题动作（san lun xxx）
    'lun_list': {
        'func': lun_list,
        'params': ['limit', 'offset', 'sort_dir', 'sort_key', 'name', 'vstore_raw_id', 'vstore_name', 'status', 'health_status', 'service_level_id', 'volume_wwn', 'storage_id', 'pool_raw_id', 'host_id', 'hostgroup_id', 'unmapped_host_id', 'unmapped_hostgroup_id', 'project_id', 'allocate_type', 'attached', 'query_mode', 'protected', 'pg_id', 'usage_type', 'support_provisioning'],
        'subtopic': 'lun'
    },
    'lun_show': {
        'func': lun_show,
        'params': ['volume_id'],
        'subtopic': 'lun'
    },
    'lun_create': {
        'func': lun_create,
        'params': ['storage_id', 'lun_specs', 'lun_specs_pass_through', 'pool_id', 'vstore_id', 'owner_controller', 'initial_distribute_policy', 'prefetch_policy', 'prefetch_value', 'tuning', 'mapping', 'task_remarks'],
        'subtopic': 'lun'
    },
    'lun_delete': {
        'func': lun_delete,
        'params': ['volume_ids', 'task_remarks'],
        'subtopic': 'lun'
    },
    'lun_modify': {
        'func': lun_modify,
        'params': ['volume_id', 'name', 'description', 'owner_controller', 'prefetch_policy', 'prefetch_value', 'tuning', 'task_remarks'],
        'subtopic': 'lun'
    },
    'lun_modify_name': {
        'func': lun_modify_name,
        'params': ['volumes'],
        'subtopic': 'lun'
    },
    'lun_expand': {
        'func': lun_expand,
        'params': ['volumes', 'task_remarks'],
        'subtopic': 'lun'
    },
    'lun_connection': {
        'func': lun_connection,
        'params': ['volume_ids'],
        'subtopic': 'lun'
    },

    # LUN 组子主题动作（san lun_group xxx）
    'lun_group_list': {
        'func': lun_group_list,
        'params': ['page_size', 'page_no', 'sort_dir', 'sort_key', 'name', 'vstore_raw_id', 'vstore_name', 'storage_id', 'storage_name', 'raw_id', 'attached', 'protection_group_raw_id', 'avaiable_mapping_for_host_id', 'avaiable_mapping_for_host_group_id', 'support_provisioning'],
        'subtopic': 'lun_group'
    },
    'lun_group_show': {
        'func': lun_group_show,
        'params': ['group_id', 'storage_id'],
        'subtopic': 'lun_group'
    },
    'lun_group_create': {
        'func': lun_group_create,
        'params': ['storage_id', 'name', 'description', 'existing_lun_ids', 'customize_volumes', 'task_remarks', 'vstore_id', 'zoning_info', 'mapping_view'],
        'subtopic': 'lun_group'
    },
    'lun_group_delete': {
        'func': lun_group_delete,
        'params': ['lun_group_ids', 'task_remarks'],
        'subtopic': 'lun_group'
    },
    'lun_group_add_luns': {
        'func': lun_group_add_luns,
        'params': ['group_id', 'existing_lun_ids', 'customize_volumes', 'host_lun_id_infos', 'host_lun_id_verify', 'task_remarks'],
        'subtopic': 'lun_group'
    },
    'lun_group_remove_luns': {
        'func': lun_group_remove_luns,
        'params': ['group_id', 'lun_ids', 'task_remarks'],
        'subtopic': 'lun_group'
    },
    'lun_group_show_luns': {
        'func': lun_group_show_luns,
        'params': ['group_id', 'page_size', 'page_no', 'health_status'],
        'subtopic': 'lun_group'
    },
    # 映射视图子主题动作（san mapping_view xxx）
    'mapping_view_create': {
        'func': mapping_view_create,
        'params': ['storage_id', 'name', 'port_group_id', 'start_host_lun_id',
                   'host', 'vbs', 'host_group', 'lun_group', 'luns',
                   'task_remarks'],
        'subtopic': 'mapping_view'
    },
    'mapping_view_delete': {
        'func': mapping_view_delete,
        'params': ['mapping_view_ids'],
        'subtopic': 'mapping_view'
    },
    'mapping_view_list': {
        'func': mapping_view_list,
        'params': ['page_size', 'page_no', 'name', 'raw_id', 'storage_id',
                   'lun_id', 'lun_name', 'lun_group_id', 'lun_group_raw_id',
                   'lun_group_name', 'storage_host_id', 'storage_host_name',
                   'storage_host_group_id', 'storage_host_group_name',
                   'storage_host_group_raw_id', 'port_group_id', 'port_group_raw_id',
                   'port_group_name', 'sort_key', 'sort_dir'],
        'subtopic': 'mapping_view'
    },

    # 存储主机子主题动作（san storage_host xxx）
    'storage_host_create': {
        'func': storage_host_create,
        'params': ['storage_id', 'host_info', 'task_remarks', 'vstore_id'],
        'subtopic': 'storage_host'
    },
    'storage_host_batch_query': {
        'func': storage_host_batch_query,
        'params': ['ids'],
        'subtopic': 'storage_host'
    },
    'storage_host_list': {
        'func': storage_host_list,
        'params': ['page_size', 'page_no', 'sort_key', 'sort_dir', 'name', 'raw_id', 'host_group_id',
                   'avaliable_add_to_host_group_id', 'host_group_name', 'ip', 'health_status', 'os_type',
                   'storage_id', 'avaiable_mapping_for_lun_group_id', 'avaiable_mapping_for_lun_id',
                   'support_provisioning', 'manufacturer', 'vstore_raw_id', 'vstore_name'],
        'subtopic': 'storage_host'
    },
    'storage_host_modify': {
        'func': storage_host_modify,
        'params': ['storage_host_id', 'storage_host_name', 'storage_host_description', 'storage_host_ip',
                   'storage_host_os_type', 'add_initiators', 'remove_initiators', 'multipath', 'access_mode',
                   'hyper_metro_path_optimized', 'task_remarks'],
        'subtopic': 'storage_host'
    },
    'storage_host_delete': {
        'func': storage_host_delete,
        'params': ['host_ids'],
        'subtopic': 'storage_host'
    },
    'storage_host_show_paths': {
        'func': storage_host_show_paths,
        'params': ['page_no', 'page_size', 'storage_id', 'storage_host_ids', 'storage_host_raw_ids',
                   'health_status', 'running_status', 'initiator_type'],
        'subtopic': 'storage_host'
    },
    'storage_host_show_luns': {
        'func': storage_host_show_luns,
        'params': ['storage_host_id', 'name', 'page_size', 'page_no', 'sort_key', 'sort_dir'],
        'subtopic': 'storage_host'
    },
    'storage_host_unmap_luns': {
        'func': storage_host_unmap_luns,
        'params': ['volume_ids', 'host_id', 'task_remarks'],
        'subtopic': 'storage_host'
    },
    # 存储主机组子主题动作（san storage_host_group xxx）
    'storage_host_group_create': {
        'func': storage_host_group_create,
        'params': ['storage_id', 'name', 'description', 'exist_host_ids', 'create_storage_host_params', 'task_remarks', 'vstore_id'],
        'subtopic': 'storage_host_group'
    },
    'storage_host_group_list': {
        'func': storage_host_group_list,
        'params': ['storage_id', 'name', 'raw_id', 'vstore_id', 'vstore_name', 'page_no', 'page_size',
                   'sort_key', 'sort_dir', 'avaiable_mapping_for_lun_group_id', 'avaiable_mapping_for_lun_id',
                   'support_provisioning'],
        'subtopic': 'storage_host_group'
    },
    'storage_host_group_add_hosts': {
        'func': storage_host_group_add_hosts,
        'params': ['storage_host_group_id', 'storage_host_id_ids', 'create_storage_host_params', 'task_remarks'],
        'subtopic': 'storage_host_group'
    },
    'storage_host_group_remove_hosts': {
        'func': storage_host_group_remove_hosts,
        'params': ['storage_host_group_id', 'storage_host_ids', 'task_remarks'],
        'subtopic': 'storage_host_group'
    },
    'storage_host_group_delete': {
        'func': storage_host_group_delete,
        'params': ['host_group_ids', 'task_remarks'],
        'subtopic': 'storage_host_group'
    },
    'storage_host_group_show_luns': {
        'func': storage_host_group_show_luns,
        'params': ['storage_host_group_id', 'name', 'page_size', 'page_no', 'sort_key', 'sort_dir'],
        'subtopic': 'storage_host_group'
    },
    'storage_host_group_unmap_luns': {
        'func': storage_host_group_unmap_luns,
        'params': ['volume_ids', 'hostgroup_id', 'task_remarks'],
        'subtopic': 'storage_host_group'
    },
    # 端口组子主题动作（san port_group xxx）
    'port_group_list': {
        'func': port_group_list,
        'params': ['storage_id', 'page_no', 'page_size'],
        'subtopic': 'port_group'
    },
    'port_group_create': {
        'func': port_group_create,
        'params': ['storage_id', 'name', 'description', 'port_ids'],
        'subtopic': 'port_group'
    },
    'port_group_show_ports': {
        'func': port_group_show_ports,
        'params': ['port_group_id', 'type', 'page_no', 'page_size'],
        'subtopic': 'port_group'
    },
    'port_group_show_relations': {
        'func': port_group_show_relations,
        'params': ['page_no', 'page_size'],
        'subtopic': 'port_group'
    },
    # 物理主机子主题动作（san physical_host xxx）
    'physical_host_list': {
        'func': physical_host_list,
        'params': ['limit', 'start', 'sort_key', 'sort_dir', 'name',
                   'host_group_name', 'ip', 'display_status', 'managed_status',
                   'os_type', 'access_mode', 'az_id', 'az_ids', 'project_id'],
        'subtopic': 'physical_host'
    },
    'physical_host_show': {
        'func': physical_host_show,
        'params': ['host_id'],
        'subtopic': 'physical_host'
    },
    'physical_host_create': {
        'func': physical_host_create,
        'params': ['access_mode', 'type', 'host_name', 'ip', 'port',
                   'username', 'password', 'description', 'initiator',
                   'azs', 'project_id', 'sync_to_storage', 'multipath_type',
                   'path_type', 'failover_mode', 'special_mode_type', 'save_public_key'],
        'subtopic': 'physical_host'
    },
    'physical_host_modify': {
        'func': physical_host_modify,
        'params': ['host_id', 'ip', 'host_name', 'os_type', 'azs', 'project_id'],
        'subtopic': 'physical_host'
    },
    'physical_host_modify_access_info': {
        'func': physical_host_modify_access_info,
        'params': ['host_id', 'ip', 'port', 'username', 'password', 'project_id', 'azs', 'sync_to_storage', 'description', 'multipath_type', 'path_type', 'failover_mode', 'special_mode_type'],
        'subtopic': 'physical_host'
    },
    'physical_host_delete': {
        'func': physical_host_delete,
        'params': ['host_id', 'sync_to_storage'],
        'subtopic': 'physical_host'
    },
    'physical_host_add_initiators': {
        'func': physical_host_add_initiators,
        'params': ['host_id', 'initiators'],
        'subtopic': 'physical_host'
    },
    'physical_host_remove_initiators': {
        'func': physical_host_remove_initiators,
        'params': ['host_id', 'initiators'],
        'subtopic': 'physical_host'
    },
    'physical_host_show_initiators': {
        'func': physical_host_show_initiators,
        'params': ['host_id', 'port_name', 'protocol', 'status'],
        'subtopic': 'physical_host'
    },
    'physical_host_test': {
        'func': physical_host_test,
        'params': ['storage_id', 'host_ids', 'hostgroup_id', 'auto_zoning', 'target_fcports', 'target_fcportgroups'],
        'subtopic': 'physical_host'
    },
    'physical_host_query_sshkey': {
        'func': physical_host_query_sshkey,
        'params': ['ip', 'port'],
        'subtopic': 'physical_host'
    },
    'physical_host_save_sshkey': {
        'func': physical_host_save_sshkey,
        'params': ['ip', 'key', 'port'],
        'subtopic': 'physical_host'
    },
    'physical_host_query_by_initiator': {
        'func': physical_host_query_by_initiator,
        'params': ['initiator_id', 'raw_id', 'protocol'],
        'subtopic': 'physical_host'
    },
    'physical_host_map_luns': {
        'func': physical_host_map_luns,
        'params': ['volume_ids', 'host_id', 'mapping_policy', 'task_remarks'],
        'subtopic': 'physical_host'
    },
    'physical_host_unmap_luns': {
        'func': physical_host_unmap_luns,
        'params': ['volume_ids', 'host_id', 'task_remarks'],
        'subtopic': 'physical_host'
    },
    'physical_host_show_mapping_views': {
        'func': physical_host_show_mapping_views,
        'params': ['host_id', 'storage_id'],
        'subtopic': 'physical_host'
    },
    # 物理主机组子主题动作（san physical_host_group xxx）
    'physical_host_group_list': {
        'func': physical_host_group_list,
        'params': ['limit', 'start', 'sort_dir', 'sort_key', 'name', 'project_id', 'az_ids', 'managed_status'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_show_hosts': {
        'func': physical_host_group_show_hosts,
        'params': ['hostgroup_id', 'name', 'ip', 'display_status', 'managed_status', 'os_type', 'sort_key', 'sort_dir', 'page_size', 'page_no'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_show': {
        'func': physical_host_group_show,
        'params': ['hostgroup_id'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_create': {
        'func': physical_host_group_create,
        'params': ['name', 'host_ids', 'azs', 'project_id', 'description'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_modify': {
        'func': physical_host_group_modify,
        'params': ['hostgroup_id', 'name', 'description', 'azs', 'project_id'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_delete': {
        'func': physical_host_group_delete,
        'params': ['hostgroup_id', 'sync_to_storage'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_add_hosts': {
        'func': physical_host_group_add_hosts,
        'params': ['hostgroup_id', 'host_ids', 'sync_to_storage'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_remove_hosts': {
        'func': physical_host_group_remove_hosts,
        'params': ['hostgroup_id', 'host_ids', 'sync_to_storage'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_map_luns': {
        'func': physical_host_group_map_luns,
        'params': ['volume_ids', 'hostgroup_id', 'mapping_policy', 'task_remarks'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_unmap_luns': {
        'func': physical_host_group_unmap_luns,
        'params': ['volume_ids', 'hostgroup_id', 'task_remarks'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_show_mapping_views': {
        'func': physical_host_group_show_mapping_views,
        'params': ['host_group_id', 'storage_id'],
        'subtopic': 'physical_host_group'
    },
    'show_related': {
        'func': physical_host_group_show_related,
        'params': ['hostgroup_id', 'storage_ip', 'storage_name'],
        'subtopic': 'physical_host_group'
    },
    'query_host_to_lun': {
        'func': mapping_view_query_host_to_lun,
        'params': ['storage_id', 'name', 'mapping_type', 'host_info', 'lun_info', 'sort_key', 'sort_dir', 'page_size', 'page_no'],
        'subtopic': 'mapping_view'
    }
}
