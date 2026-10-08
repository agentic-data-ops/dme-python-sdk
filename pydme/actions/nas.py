"""
NAS 相关操作
"""

import sys
import os

from pydme.client import DMEAPIClient


# ============================================================================
# DPC (并行客户端) 子主题函数
# ============================================================================


def dpc_list(client: DMEAPIClient, ids: list = None, hostname: str = None, ip: str = None,
             mgmt_status: list = None, status: list = None, sn: str = None,
             storage_id: str = None, dpc_om_id: str = None, dpc_type: list = None,
             client_version: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    url = "/rest/dpc-mgmt/v1/dpcs/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if ids is not None:
        payload['ids'] = ids
    if hostname is not None:
        payload['hostname'] = hostname
    if ip is not None:
        payload['ip'] = ip
    if mgmt_status is not None:
        payload['mgmt_status'] = mgmt_status
    if status is not None:
        payload['status'] = status
    if sn is not None:
        payload['sn'] = sn
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if dpc_om_id is not None:
        payload['dpc_om_id'] = dpc_om_id
    if dpc_type is not None:
        payload['dpc_type'] = dpc_type
    if client_version is not None:
        payload['client_version'] = client_version

    response = client.post(url, body=payload)
    return response


def dpc_show(client: DMEAPIClient, dpc_id: str) -> dict:
    url = "/rest/dpc-mgmt/v1/dpcs/{dpc_id}"

    if not dpc_id:
        raise ValueError("dpc_id 是必选参数")

    response = client.get(url, params={"dpc_id": dpc_id})
    return response


def dpc_client_list(client: DMEAPIClient, storage_id: str = None,
                     process_id: str = None, name: str = None,
                     manage_ip: str = None, version: str = None,
                     status: str = None, switch_status: str = None,
                     upgrade_flag: str = None, sort_key: str = None,
                     sort_dir: str = None,
                     page_no: int = 1, page_size: int = 10) -> dict:
    url = "/rest/fileservice/v1/dpc-clients/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if process_id is not None:
        payload['process_id'] = process_id
    if name is not None:
        payload['name'] = name
    if manage_ip is not None:
        payload['manage_ip'] = manage_ip
    if version is not None:
        payload['version'] = version
    if status is not None:
        payload['status'] = status
    if switch_status is not None:
        payload['switch_status'] = switch_status
    if upgrade_flag is not None:
        payload['upgrade_flag'] = upgrade_flag
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def dpc_client_show(client: DMEAPIClient, id: str) -> dict:
    url = "/rest/fileservice/v1/dpc-clients/{id}"

    if not id:
        raise ValueError("id 是必选参数")

    response = client.get(url, params={"id": id})
    return response


def dtree_list(client: DMEAPIClient, id_in_storage: str = None, name: str = None,
               device_name: str = None, storage_id: str = None, zone_id: str = None,
               manufacturer: str = None, tier_name: str = None, fs_name: str = None,
               fs_id: str = None, namespace_name: str = None, namespace_id: str = None,
               quota_switch: bool = None, security_mode: str = None,
               nas_locking_policy: str = None, sort_key: str = None,
               sort_dir: str = None, page_no: int = 1, page_size: int = 20,
               dc_id: str = None, dc_name: str = None) -> dict:
    url = "/rest/fileservice/v1/dtrees/query"

    payload = {}

    if id_in_storage is not None:
        payload['id_in_storage'] = id_in_storage
    if name is not None:
        payload['name'] = name
    if device_name is not None:
        payload['device_name'] = device_name
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if manufacturer is not None:
        payload['manufacturer'] = manufacturer
    if tier_name is not None:
        payload['tier_name'] = tier_name
    if fs_name is not None:
        payload['fs_name'] = fs_name
    if fs_id is not None:
        payload['fs_id'] = fs_id
    if namespace_name is not None:
        payload['namespace_name'] = namespace_name
    if namespace_id is not None:
        payload['namespace_id'] = namespace_id
    if quota_switch is not None:
        payload['quota_switch'] = quota_switch
    if security_mode is not None:
        payload['security_mode'] = security_mode
    if nas_locking_policy is not None:
        payload['nas_locking_policy'] = nas_locking_policy
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size
    if dc_id is not None:
        payload['dc_id'] = dc_id
    if dc_name is not None:
        payload['dc_name'] = dc_name

    response = client.post(url, body=payload)
    return response


def dtree_show(client: DMEAPIClient, dtree_id: str) -> dict:
    url = "/rest/fileservice/v1/dtrees/{dtree_id}"

    if not dtree_id:
        raise ValueError("dtree_id 是必选参数")

    response = client.get(url, params={"dtree_id": dtree_id})
    return response


def dtree_create(client: DMEAPIClient, storage_id: str, create_dtrees_param: list,
                 fs_id: str = None, namespace_id: str = None, zone_id: str = None,
                 parent_dir: str = None, quota_switch: bool = None,
                 security_mode: str = None, nas_locking_policy: str = None,
                 create_nfs_share_param: dict = None, create_cifs_share_param: dict = None,
                 dataturbo_share: dict = None, create_worm_param: dict = None,
                 unix_permissions: str = None, task_remarks: str = None) -> dict:
    url = "/rest/fileservice/v1/dtrees"

    if not storage_id or not create_dtrees_param:
        raise ValueError("storage_id 和 create_dtrees_param 是必选参数")

    payload = {
        'storage_id': storage_id,
        'create_dtrees_param': create_dtrees_param
    }

    if fs_id is not None:
        payload['fs_id'] = fs_id
    if namespace_id is not None:
        payload['namespace_id'] = namespace_id
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if parent_dir is not None:
        payload['parent_dir'] = parent_dir
    if quota_switch is not None:
        payload['quota_switch'] = quota_switch
    if security_mode is not None:
        payload['security_mode'] = security_mode
    if nas_locking_policy is not None:
        payload['nas_locking_policy'] = nas_locking_policy
    if create_nfs_share_param is not None:
        payload['create_nfs_share_param'] = create_nfs_share_param
    if create_cifs_share_param is not None:
        payload['create_cifs_share_param'] = create_cifs_share_param
    if dataturbo_share is not None:
        payload['dataturbo_share'] = dataturbo_share
    if create_worm_param is not None:
        payload['create_worm_param'] = create_worm_param
    if unix_permissions is not None:
        payload['unix_permissions'] = unix_permissions
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def dtree_delete(client: DMEAPIClient, dtree_ids: list, task_remarks: str = None) -> dict:
    url = "/rest/fileservice/v1/dtrees/delete"

    if not dtree_ids or len(dtree_ids) == 0:
        raise ValueError("dtree_ids 是必选参数")

    payload = {
        'dtree_ids': dtree_ids
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def dtree_modify(client: DMEAPIClient, dtree_id: str, name: str = None,
                 quota_switch: bool = None, security_mode: str = None,
                 nas_locking_policy: str = None, unix_permissions: str = None,
                 task_remarks: str = None) -> dict:
    url = "/rest/fileservice/v1/dtrees/{dtree_id}"

    payload = {}

    if name is not None:
        payload['name'] = name
    if quota_switch is not None:
        payload['quota_switch'] = quota_switch
    if security_mode is not None:
        payload['security_mode'] = security_mode

    payload = {}

    if name is not None:
        payload['name'] = name
    if quota_switch is not None:
        payload['quota_switch'] = quota_switch
    if security_mode is not None:
        payload['security_mode'] = security_mode
    if nas_locking_policy is not None:
        payload['nas_locking_policy'] = nas_locking_policy
    if unix_permissions is not None:
        payload['unix_permissions'] = unix_permissions
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.put(url, body=payload, params={"dtree_id": dtree_id})
    return response


# ============================================================================
# NFS 共享子主题相关动作
# ============================================================================

def nfs_share_list(client: DMEAPIClient, id_in_storage: str = None, name: str = None,
                   share_path: str = None, exact_share_path: str = None,
                   device_name: str = None, manufacturer: str = None,
                   storage_id: str = None, tier_name: str = None,
                   owning_dtree_name: str = None, fs_name: str = None,
                   fs_id: str = None, owning_dtree_id: str = None,
                   vstore_name: str = None, page_no: int = 1,
                   page_size: int = 20, sort_key: str = None,
                   sort_dir: str = None, support_provisioning: bool = None,
                   namespace_id: str = None, namespace_name: str = None,
                   dc_id: str = None, dc_name: str = None,
                   zone_id: str = None, zone_name: str = None,
                   zone_ip: str = None, scope: str = None) -> dict:
    url = "/rest/fileservice/v1/nfs-shares/query"

    payload = {}

    if id_in_storage is not None:
        payload['id_in_storage'] = id_in_storage
    if name is not None:
        payload['name'] = name
    if share_path is not None:
        payload['share_path'] = share_path
    if exact_share_path is not None:
        payload['exact_share_path'] = exact_share_path
    if device_name is not None:
        payload['device_name'] = device_name
    if manufacturer is not None:
        payload['manufacturer'] = manufacturer
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if tier_name is not None:
        payload['tier_name'] = tier_name
    if owning_dtree_name is not None:
        payload['owning_dtree_name'] = owning_dtree_name
    if fs_name is not None:
        payload['fs_name'] = fs_name
    if fs_id is not None:
        payload['fs_id'] = fs_id
    if owning_dtree_id is not None:
        payload['owning_dtree_id'] = owning_dtree_id
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
    if support_provisioning is not None:
        payload['support_provisioning'] = support_provisioning
    if namespace_id is not None:
        payload['namespace_id'] = namespace_id
    if namespace_name is not None:
        payload['namespace_name'] = namespace_name
    if dc_id is not None:
        payload['dc_id'] = dc_id
    if dc_name is not None:
        payload['dc_name'] = dc_name
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if zone_name is not None:
        payload['zone_name'] = zone_name
    if zone_ip is not None:
        payload['zone_ip'] = zone_ip
    if scope is not None:
        payload['scope'] = scope

    response = client.post(url, body=payload)
    return response


def nfs_share_show(client: DMEAPIClient, nfs_share_id: str) -> dict:
    url = "/rest/fileservice/v1/nfs-shares/{nfs_share_id}"

    if not nfs_share_id:
        raise ValueError("nfs_share_id 是必选参数")

    response = client.get(url, params={"nfs_share_id": nfs_share_id})
    return response


def nfs_share_create(client: DMEAPIClient, create_nfs_share_param: dict,
                     task_remarks: str = None) -> dict:
    url = "/rest/fileservice/v2/nfs-shares"

    payload = {
        'create_nfs_share_param': create_nfs_share_param
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def nfs_share_modify(client: DMEAPIClient, nfs_share_id: str,
                     description: str = None, character_encoding: str = None,
                     audit_items: list = None, show_snapshot_enable: bool = None,
                     nfs_share_client_addition: list = None,
                     nfs_share_client_modification: list = None,
                     nfs_share_client_deletion: list = None,
                     file_name_ex_filters: list = None,
                     task_remarks: str = None) -> dict:
    url = "/rest/fileservice/v2/nfs-shares/{nfs_share_id}"

    payload = {}

    if description is not None:
        payload['description'] = description
    if character_encoding is not None:
        payload['character_encoding'] = character_encoding
    if audit_items is not None:
        payload['audit_items'] = audit_items

    payload = {}

    if description is not None:
        payload['description'] = description
    if character_encoding is not None:
        payload['character_encoding'] = character_encoding
    if audit_items is not None:
        payload['audit_items'] = audit_items
    if show_snapshot_enable is not None:
        payload['show_snapshot_enable'] = show_snapshot_enable
    if nfs_share_client_addition is not None:
        payload['nfs_share_client_addition'] = nfs_share_client_addition
    if nfs_share_client_modification is not None:
        payload['nfs_share_client_modification'] = nfs_share_client_modification
    if nfs_share_client_deletion is not None:
        payload['nfs_share_client_deletion'] = nfs_share_client_deletion
    if file_name_ex_filters is not None:
        payload['file_name_ex_filters'] = file_name_ex_filters
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.put(url, body=payload, params={"nfs_share_id": nfs_share_id})
    return response


def nfs_share_delete(client: DMEAPIClient, nfs_share_ids: list,
                     task_remarks: str = None) -> dict:
    url = "/rest/fileservice/v1/nfs-shares/delete"

    payload = {
        'nfs_share_ids': nfs_share_ids
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


# ============================================================================
# CIFS 共享子主题相关动作
# ============================================================================

def cifs_share_list(client: DMEAPIClient, raw_id: str = None, name: str = None,
              share_path: str = None, exact_share_path: str = None,
              fs_id: str = None, fs_name: str = None, dtree_id: str = None,
              dtree_name: str = None, storage_id: str = None,
              storage_name: str = None, vstore_raw_id: str = None,
              vstore_name: str = None, manufacturer: str = None,
              op_lock_enabled: bool = None, notify_enabled: bool = None,
              offline_file_modes: list = None, file_extension_filter_enabled: bool = None,
              abe_enabled: bool = None, page_no: int = 1, page_size: int = 10,
              sort_key: str = None, sort_dir: str = None,
              namespace_id: str = None, namespace_name: str = None,
              support_provisioning: bool = None, dc_id: str = None,
              dc_name: str = None) -> dict:
    url = "/rest/fileservice/v1/cifs-shares/query"

    payload = {}

    if raw_id is not None:
        payload['raw_id'] = raw_id
    if name is not None:
        payload['name'] = name
    if share_path is not None:
        payload['share_path'] = share_path
    if exact_share_path is not None:
        payload['exact_share_path'] = exact_share_path
    if fs_id is not None:
        payload['fs_id'] = fs_id
    if fs_name is not None:
        payload['fs_name'] = fs_name
    if dtree_id is not None:
        payload['dtree_id'] = dtree_id
    if dtree_name is not None:
        payload['dtree_name'] = dtree_name
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if storage_name is not None:
        payload['storage_name'] = storage_name
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if vstore_name is not None:
        payload['vstore_name'] = vstore_name
    if manufacturer is not None:
        payload['manufacturer'] = manufacturer
    if op_lock_enabled is not None:
        payload['op_lock_enabled'] = op_lock_enabled
    if notify_enabled is not None:
        payload['notify_enabled'] = notify_enabled
    if offline_file_modes is not None:
        payload['offline_file_modes'] = offline_file_modes
    if file_extension_filter_enabled is not None:
        payload['file_extension_filter_enabled'] = file_extension_filter_enabled
    if abe_enabled is not None:
        payload['abe_enabled'] = abe_enabled
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if namespace_id is not None:
        payload['namespace_id'] = namespace_id
    if namespace_name is not None:
        payload['namespace_name'] = namespace_name
    if support_provisioning is not None:
        payload['support_provisioning'] = support_provisioning
    if dc_id is not None:
        payload['dc_id'] = dc_id
    if dc_name is not None:
        payload['dc_name'] = dc_name

    response = client.post(url, body=payload)
    return response


def cifs_share_show(client: DMEAPIClient, cifs_share_id: str) -> dict:
    url = "/rest/fileservice/v1/cifs-shares/{cifs_share_id}"

    response = client.get(url, params={"cifs_share_id": cifs_share_id})
    return response


def cifs_share_create(client: DMEAPIClient, create_cifs_param: dict, fs_id: str = None,
                namespace_id: str = None, task_remarks: str = None) -> dict:
    url = "/rest/fileservice/v1/cifs-shares"

    payload = {
        'create_cifs_param': create_cifs_param
    }

    if fs_id is not None:
        payload['fs_id'] = fs_id
    if namespace_id is not None:
        payload['namespace_id'] = namespace_id
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def cifs_share_modify(client: DMEAPIClient, cifs_share_id: str, description: str = None,
                op_lock_enabled: bool = None, notify_enabled: bool = None,
                ca_enabled: bool = None, offline_file_mode: str = None,
                ip_control_enabled: bool = None, abe_enabled: bool = None,
                audititem_list: list = None, apply_default_acl: bool = None,
                file_extension_filter_enabled: bool = None,
                show_previous_versions_enabled: bool = None,
                show_snapshot_enabled: bool = None,
                user_and_user_group_info: list = None,
                ip_and_segments: list = None,
                file_name_ex_filters: list = None,
                task_remarks: str = None, smb3_encryption_enable: bool = None,
                unencrypted_access: bool = None, enable_lease: bool = None) -> dict:
    url = "/rest/fileservice/v1/cifs-shares/{cifs_share_id}"

    payload = {}

    if description is not None:
        payload['description'] = description
    if op_lock_enabled is not None:
        payload['op_lock_enabled'] = op_lock_enabled
    if notify_enabled is not None:
        payload['notify_enabled'] = notify_enabled

    payload = {}

    if description is not None:
        payload['description'] = description
    if op_lock_enabled is not None:
        payload['op_lock_enabled'] = op_lock_enabled
    if notify_enabled is not None:
        payload['notify_enabled'] = notify_enabled
    if ca_enabled is not None:
        payload['ca_enabled'] = ca_enabled
    if offline_file_mode is not None:
        payload['offline_file_mode'] = offline_file_mode
    if ip_control_enabled is not None:
        payload['ip_control_enabled'] = ip_control_enabled
    if abe_enabled is not None:
        payload['abe_enabled'] = abe_enabled
    if audititem_list is not None:
        payload['audititem_list'] = audititem_list
    if apply_default_acl is not None:
        payload['apply_default_acl'] = apply_default_acl
    if file_extension_filter_enabled is not None:
        payload['file_extension_filter_enabled'] = file_extension_filter_enabled
    if show_previous_versions_enabled is not None:
        payload['show_previous_versions_enabled'] = show_previous_versions_enabled
    if show_snapshot_enabled is not None:
        payload['show_snapshot_enabled'] = show_snapshot_enabled
    if user_and_user_group_info is not None:
        payload['user_and_user_group_info'] = user_and_user_group_info
    if ip_and_segments is not None:
        payload['ip_and_segments'] = ip_and_segments
    if file_name_ex_filters is not None:
        payload['file_name_ex_filters'] = file_name_ex_filters
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks
    if smb3_encryption_enable is not None:
        payload['smb3_encryption_enable'] = smb3_encryption_enable
    if unencrypted_access is not None:
        payload['unencrypted_access'] = unencrypted_access
    if enable_lease is not None:
        payload['enable_lease'] = enable_lease

    response = client.put(url, body=payload, params={"cifs_share_id": cifs_share_id})
    return response


def cifs_share_delete(client: DMEAPIClient, cifs_share_ids: list, task_remarks: str = None) -> dict:
    url = "/rest/fileservice/v1/cifs-shares/delete"

    payload = {
        'cifs_share_ids': cifs_share_ids
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def cifs_share_show_permissions(client: DMEAPIClient, cifs_share_id: str,
                          type: str = None, user_filter: dict = None,
                          ip_filter: dict = None,
                          file_filter: dict = None,
                          sort_key: str = None, sort_dir: str = None,
                          page_no: int = 1, page_size: int = 10) -> dict:
    result = {'user': [], 'ip': [], 'file': []}

    # 根据 type 参数查询对应类型的权限
    if type is None or type == 'user':
        url = "/rest/fileservice/v1/cifs-shares/{cifs_share_id}/auth-users/query"
        payload = {}
        if user_filter is not None:
            for key, value in user_filter.items():
                if value is not None:
                    payload[key] = value
        if sort_key is not None:
            payload['sort_key'] = sort_key
        if sort_dir is not None:
            payload['sort_dir'] = sort_dir
        if page_no is not None:
            payload['page_no'] = page_no
        if page_size is not None:
            payload['page_size'] = page_size
        response = client.post(url, body=payload, params={"cifs_share_id": cifs_share_id})
        if response.get('auth_users'):
            result['user'] = response.get('auth_users')

    if type is None or type == 'ip':
        url = "/rest/fileservice/v1/cifs-shares/{cifs_share_id}/ip-access-rules/query"
        payload = {}
        if ip_filter is not None:
            for key, value in ip_filter.items():
                if value is not None:
                    payload[key] = value
        if sort_key is not None:
            payload['sort_key'] = sort_key
        if sort_dir is not None:
            payload['sort_dir'] = sort_dir
        if page_no is not None:
            payload['page_no'] = page_no
        if page_size is not None:
            payload['page_size'] = page_size
        response = client.post(url, body=payload, params={"cifs_share_id": cifs_share_id})
        if response.get('ip_access_rules'):
            result['ip'] = response.get('ip_access_rules')

    if type is None or type == 'file':
        url = "/rest/fileservice/v1/cifs-shares/{cifs_share_id}/file-filter-rules/query"
        payload = {}
        if file_filter is not None:
            for key, value in file_filter.items():
                if value is not None:
                    payload[key] = value
        if sort_key is not None:
            payload['sort_key'] = sort_key
        if sort_dir is not None:
            payload['sort_dir'] = sort_dir
        if page_no is not None:
            payload['page_no'] = page_no
        if page_size is not None:
            payload['page_size'] = page_size
        response = client.post(url, body=payload, params={"cifs_share_id": cifs_share_id})
        if response.get('file_filter_rules'):
            result['file'] = response.get('file_filter_rules')

    # 如果指定了 type，只返回对应类型的权限
    if type == 'user':
        return {'user_permissions': result['user']}
    elif type == 'ip':
        return {'ip_permissions': result['ip']}
    elif type == 'file':
        return {'file_permissions': result['file']}
    else:
        # 返回所有权限
        return {'user_permissions': result['user'], 'ip_permissions': result['ip'], 'file_permissions': result['file']}


# ============================================================================
# dataturbo_share (DataTurbo 共享) 子主题相关动作
# ============================================================================

def dataturbo_share_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 10,
                   raw_id: str = None, share_path: str = None, fs_id: str = None,
                   fs_name: str = None, dtree_id: str = None, dtree_name: str = None,
                   vstore_id: str = None, vstore_raw_id: str = None, vstore_name: str = None,
                   storage_id: str = None, storage_name: str = None, zone_id: str = None,
                   zone_name: str = None, scope: str = None, sort_key: str = None,
                   sort_dir: str = None) -> dict:
    url = "/rest/fileservice/v1/dpc-shares/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if raw_id is not None:
        payload['raw_id'] = raw_id
    if share_path is not None:
        payload['share_path'] = share_path
    if fs_id is not None:
        payload['fs_id'] = fs_id
    if fs_name is not None:
        payload['fs_name'] = fs_name
    if dtree_id is not None:
        payload['dtree_id'] = dtree_id
    if dtree_name is not None:
        payload['dtree_name'] = dtree_name
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if vstore_name is not None:
        payload['vstore_name'] = vstore_name
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if storage_name is not None:
        payload['storage_name'] = storage_name
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if zone_name is not None:
        payload['zone_name'] = zone_name
    if scope is not None:
        payload['scope'] = scope
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def dataturbo_share_show(client: DMEAPIClient, dataturbo_share_id: str) -> dict:
    url = "/rest/fileservice/v1/dpc-shares/{dataturbo_share_id}"

    response = client.get(url, params={"dataturbo_share_id": dataturbo_share_id})
    return response


def dataturbo_share_create(client: DMEAPIClient, charset: str, fs_id: str = None,
                     dtree_id: str = None, description: str = None,
                     dataturbo_share_auth: list = None, task_remarks: str = None) -> dict:
    url = "/rest/fileservice/v1/dpc-shares"

    payload = {
        'charset': charset
    }

    if fs_id is not None:
        payload['fs_id'] = fs_id
    if dtree_id is not None:
        payload['dtree_id'] = dtree_id
    if description is not None:
        payload['description'] = description
    if dataturbo_share_auth is not None:
        payload['dpc_share_auth'] = dataturbo_share_auth
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def dataturbo_share_modify(client: DMEAPIClient, dataturbo_share_id: str, description: str = None,
                     dataturbo_share_auth_addition: list = None,
                     dataturbo_share_auth_deletion: list = None,
                     task_remarks: str = None) -> dict:
    url = "/rest/fileservice/v1/dpc-shares/{dataturbo_share_id}"

    payload = {}

    if description is not None:
        payload['description'] = description
    if dataturbo_share_auth_addition is not None:
        payload['dpc_share_auth_addition'] = dataturbo_share_auth_addition
    if dataturbo_share_auth_deletion is not None:
        payload['dpc_share_auth_deletion'] = dataturbo_share_auth_deletion

    payload = {}

    if description is not None:
        payload['description'] = description
    if dataturbo_share_auth_addition is not None:
        payload['dpc_share_auth_addition'] = dataturbo_share_auth_addition
    if dataturbo_share_auth_deletion is not None:
        payload['dpc_share_auth_deletion'] = dataturbo_share_auth_deletion
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.put(url, body=payload, params={"dataturbo_share_id": dataturbo_share_id})
    return response


def dataturbo_share_delete(client: DMEAPIClient, dataturbo_share_ids: list,
                     task_remarks: str = None) -> dict:
    url = "/rest/fileservice/v1/dpc-shares/delete"

    payload = {
        'dpc_share_ids': dataturbo_share_ids
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def dataturbo_share_show_permissions(client: DMEAPIClient, dataturbo_share_id: str,
                                      page_no: int = 1, page_size: int = 10,
                                      user_id: str = None, user_name: str = None,
                                      permission: str = None) -> dict:
    url = "/rest/fileservice/v1/dpc-shares/{dataturbo_share_id}/dpc-share-auths/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if user_id is not None:
        payload['user_id'] = user_id
    if user_name is not None:
        payload['user_name'] = user_name
    if permission is not None:
        payload['permission'] = permission

    response = client.post(url, body=payload)
    return response


# ============================================================================
# Quota (配额) 子主题相关动作
# ============================================================================

def quota_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 20,
               ids: list = None, raw_ids: list = None, quota_type: str = None,
               parent_type: str = None, parent_raw_id: str = None,
               owner_name: str = None, vstore_id: str = None,
               vstore_raw_id: str = None, storage_id: str = None,
               sort_key: str = None, sort_dir: str = None,
               zone_id: str = None) -> dict:
    url = "/rest/fileservice/v1/quotas/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if ids is not None:
        payload['ids'] = ids
    if raw_ids is not None:
        payload['raw_ids'] = raw_ids
    if quota_type is not None:
        payload['quota_type'] = quota_type
    if parent_type is not None:
        payload['parent_type'] = parent_type
    if parent_raw_id is not None:
        payload['parent_raw_id'] = parent_raw_id
    if owner_name is not None:
        payload['owner_name'] = owner_name
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if zone_id is not None:
        payload['zone_id'] = zone_id

    response = client.post(url, body=payload)
    return response


def quota_show(client: DMEAPIClient, quota_id: str) -> dict:
    url = "/rest/fileservice/v1/quotas/query"

    payload = {
        'ids': [quota_id],
        'page_no': 1,
        'page_size': 1
    }

    response = client.post(url, body=payload)
    return response


def quota_create(client: DMEAPIClient, parent_id: str, parent_type: str,
                 quota_type: str, space_soft_quota: int = -1,
                 space_hard_quota: int = -1, space_advisory_quota: int = -1,
                 file_soft_quota: int = -1, file_hard_quota: int = -1,
                 file_advisory_quota: int = -1, snap_space_switch: bool = False,
                 soft_grace_time: int = None, quota_owner: dict = None,
                 dir_quota_target: str = None, task_remarks: str = None) -> dict:
    url = "/rest/fileservice/v1/quotas"

    payload = {
        'parent_id': parent_id,
        'parent_type': parent_type,
        'quota_type': quota_type,
        'space_soft_quota': space_soft_quota,
        'space_hard_quota': space_hard_quota,
        'space_advisory_quota': space_advisory_quota,
        'file_soft_quota': file_soft_quota,
        'file_hard_quota': file_hard_quota,
        'file_advisory_quota': file_advisory_quota,
        'snap_space_switch': snap_space_switch
    }

    if soft_grace_time is not None:
        payload['soft_grace_time'] = soft_grace_time
    if quota_owner is not None:
        payload['quota_owner'] = quota_owner
    if dir_quota_target is not None:
        payload['dir_quota_target'] = dir_quota_target
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def quota_modify(client: DMEAPIClient, quota_id: str,
                 space_soft_quota: int = None, space_hard_quota: int = None,
                 space_advisory_quota: int = None, file_soft_quota: int = None,
                 file_hard_quota: int = None, file_advisory_quota: int = None,
                 snap_space_switch: bool = None, soft_grace_time: int = None,
                 task_remarks: str = None) -> dict:
    url = "/rest/fileservice/v1/quotas/{quota_id}"

    payload = {}

    if space_soft_quota is not None:
        payload['space_soft_quota'] = space_soft_quota
    if space_hard_quota is not None:
        payload['space_hard_quota'] = space_hard_quota
    if space_advisory_quota is not None:
        payload['space_advisory_quota'] = space_advisory_quota

    payload = {}

    if space_soft_quota is not None:
        payload['space_soft_quota'] = space_soft_quota
    if space_hard_quota is not None:
        payload['space_hard_quota'] = space_hard_quota
    if space_advisory_quota is not None:
        payload['space_advisory_quota'] = space_advisory_quota
    if file_soft_quota is not None:
        payload['file_soft_quota'] = file_soft_quota
    if file_hard_quota is not None:
        payload['file_hard_quota'] = file_hard_quota
    if file_advisory_quota is not None:
        payload['file_advisory_quota'] = file_advisory_quota
    if snap_space_switch is not None:
        payload['snap_space_switch'] = snap_space_switch
    if soft_grace_time is not None:
        payload['soft_grace_time'] = soft_grace_time
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.put(url, body=payload, params={"quota_id": quota_id})
    return response


def quota_delete(client: DMEAPIClient, quota_ids: list,
                 task_remarks: str = None) -> dict:
    url = "/rest/fileservice/v1/quotas/delete"

    payload = {
        'ids': quota_ids
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


# ============================================================================
# filesystem (文件系统) 子主题相关动作
# ============================================================================

def filesystem_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 100,
                     sort_dir: str = None, sort_key: str = None, name: str = None,
                     is_associated_qos: bool = None, qos_id: str = None,
                     storage_name: str = None, manufacturer: str = None,
                     storage_pool_name: str = None, storage_pool_id: str = None,
                     tier_name: str = None, tier_id: str = None,
                     vstore_name: str = None, vstore_raw_id: str = None,
                     project_name: str = None, project_id: str = None,
                     storage_id: str = None, fs_raw_id: str = None,
                     health_status: str = None, running_status: str = None,
                     alloc_type: str = None, type: str = None,
                     protection: str = None, dc_id: str = None,
                     dc_name: str = None, zone_id: str = None,
                     product_name: str = None, description: str = None,
                     tag_filters: list = None) -> dict:
    url = "/rest/fileservice/v1/filesystems/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if name is not None:
        payload['name'] = name
    if is_associated_qos is not None:
        payload['is_associated_qos'] = is_associated_qos
    if qos_id is not None:
        payload['qos_id'] = qos_id
    if storage_name is not None:
        payload['storage_name'] = storage_name
    if manufacturer is not None:
        payload['manufacturer'] = manufacturer
    if storage_pool_name is not None:
        payload['storage_pool_name'] = storage_pool_name
    if storage_pool_id is not None:
        payload['storage_pool_id'] = storage_pool_id
    if tier_name is not None:
        payload['tier_name'] = tier_name
    if tier_id is not None:
        payload['tier_id'] = tier_id
    if vstore_name is not None:
        payload['vstore_name'] = vstore_name
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if project_name is not None:
        payload['project_name'] = project_name
    if project_id is not None:
        payload['project_id'] = project_id
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if fs_raw_id is not None:
        payload['fs_raw_id'] = fs_raw_id
    if health_status is not None:
        payload['health_status'] = health_status
    if running_status is not None:
        payload['running_status'] = running_status
    if alloc_type is not None:
        payload['alloc_type'] = alloc_type
    if type is not None:
        payload['type'] = type
    if protection is not None:
        payload['protection'] = protection
    if dc_id is not None:
        payload['dc_id'] = dc_id
    if dc_name is not None:
        payload['dc_name'] = dc_name
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if product_name is not None:
        payload['product_name'] = product_name
    if description is not None:
        payload['description'] = description
    if tag_filters is not None:
        payload['tag_filters'] = tag_filters

    response = client.post(url, body=payload)
    return response


def filesystem_show(client: DMEAPIClient, filesystem_id: str) -> dict:
    url = "/rest/fileservice/v1/filesystems/{filesystem_id}"

    response = client.get(url, params={"filesystem_id": filesystem_id})
    return response


def filesystem_delete(client: DMEAPIClient, filesystem_ids: list, task_remarks: str = None) -> dict:
    url = "/rest/fileservice/v1/filesystems/delete"

    payload = {
        'file_system_ids': filesystem_ids
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def filesystem_batch_modify(client: DMEAPIClient, filesystems: list, task_remarks: str = None) -> dict:
    url = "/rest/fileservice/v1/filesystems/modify"

    payload = {
        'filesystems': filesystems
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def filesystem_create(client: DMEAPIClient, storage_id: str, pool_raw_id: str,
                                 filesystem_specs: list, vstore_id: str = None,
                                 zone_id: str = None, task_remarks: str = None,
                                 gfs_group_id: str = None, automatic_update_time: bool = None,
                                 atime_update_mode: str = None, schedule_name: str = None,
                                 quota_switch: bool = None, vaai_switch: bool = None,
                                 initial_distribute_policy: str = None,
                                 capacity_threshold: int = None,
                                 tuning: dict = None,
                                 create_cifs_share_param: dict = None,
                                 create_nfs_share_param: dict = None,
                                 create_dpc_share_param: dict = None,
                                 owning_controller: str = None,
                                 snapshot_expired_enabled: bool = None,
                                 checksum_enabled: bool = None,
                                 ads_enabled: bool = None,
                                 security_mode: str = None,
                                 nas_locking_policy: str = None,
                                 capacity_autonegotiation: dict = None,
                                 worm: dict = None,
                                 snapshot_reserved_space_percentage: int = None,
                                 periodic_snapshots_limit: int = None,
                                 snapshot_dir_visible: bool = None,
                                 object_service_optimization: bool = None,
                                 case_sensitive: bool = None,
                                 audit_log_rules: list = None,
                                 unix_permissions: str = None) -> dict:
    url = "/rest/fileservice/v1/filesystems/customize-filesystems"

    payload = {
        'storage_id': storage_id,
        'pool_raw_id': pool_raw_id,
        'filesystem_specs': filesystem_specs
    }

    if vstore_id is not None:
        payload['vstore_id'] = vstore_id
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks
    if gfs_group_id is not None:
        payload['gfs_group_id'] = gfs_group_id
    if automatic_update_time is not None:
        payload['automatic_update_time'] = automatic_update_time
    if atime_update_mode is not None:
        payload['atime_update_mode'] = atime_update_mode
    if schedule_name is not None:
        payload['schedule_name'] = schedule_name
    if quota_switch is not None:
        payload['quota_switch'] = quota_switch
    if vaai_switch is not None:
        payload['vaai_switch'] = vaai_switch
    if initial_distribute_policy is not None:
        payload['initial_distribute_policy'] = initial_distribute_policy
    if capacity_threshold is not None:
        payload['capacity_threshold'] = capacity_threshold
    if tuning is not None:
        payload['tuning'] = tuning
    if create_cifs_share_param is not None:
        payload['create_cifs_share_param'] = create_cifs_share_param
    if create_nfs_share_param is not None:
        payload['create_nfs_share_param'] = create_nfs_share_param
    if create_dpc_share_param is not None:
        payload['create_dpc_share_param'] = create_dpc_share_param
    if owning_controller is not None:
        payload['owning_controller'] = owning_controller
    if snapshot_expired_enabled is not None:
        payload['snapshot_expired_enabled'] = snapshot_expired_enabled
    if checksum_enabled is not None:
        payload['checksum_enabled'] = checksum_enabled
    if ads_enabled is not None:
        payload['ads_enabled'] = ads_enabled
    if security_mode is not None:
        payload['security_mode'] = security_mode
    if nas_locking_policy is not None:
        payload['nas_locking_policy'] = nas_locking_policy
    if capacity_autonegotiation is not None:
        payload['capacity_autonegotiation'] = capacity_autonegotiation
    if worm is not None:
        payload['worm'] = worm
    if snapshot_reserved_space_percentage is not None:
        payload['snapshot_reserved_space_percentage'] = snapshot_reserved_space_percentage
    if periodic_snapshots_limit is not None:
        payload['periodic_snapshots_limit'] = periodic_snapshots_limit
    if snapshot_dir_visible is not None:
        payload['snapshot_dir_visible'] = snapshot_dir_visible
    if object_service_optimization is not None:
        payload['object_service_optimization'] = object_service_optimization
    if case_sensitive is not None:
        payload['case_sensitive'] = case_sensitive
    if audit_log_rules is not None:
        payload['audit_log_rules'] = audit_log_rules
    if unix_permissions is not None:
        payload['unix_permissions'] = unix_permissions

    response = client.post(url, body=payload)
    return response


def filesystem_query_available(client: DMEAPIClient, feature_type: str,
                                local_storage_id: str, remote_storage_id: str = None,
                                name: str = None, page_no: int = 1,
                                page_size: int = 20, sort_key: str = None,
                                sort_dir: str = None) -> dict:
    url = "/rest/fileservice/v1/filesystems/available-filesystems/query"

    payload = {
        'feature_type': feature_type,
        'local_storage_id': local_storage_id
    }

    if remote_storage_id is not None:
        payload['remote_storage_id'] = remote_storage_id
    if name is not None:
        payload['name'] = name
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def filesystem_modify(client: DMEAPIClient, file_system_id: str, name: str = None,
           description: str = None, capacity: int = None,
           capacity_threshold: int = None, initial_distribute_policy: str = None,
           automatic_update_time: bool = None, atime_update_mode: str = None,
           quota_switch: bool = None, vaai_switch: bool = None,
           owning_controller: str = None,
           snapshot_expired_enabled: bool = None,
           checksum_enabled: bool = None, ads_enabled: bool = None,
           security_mode: str = None, nas_locking_policy: str = None,
           snapshot_reserved_space_percentage: int = None,
           periodic_snapshots_limit: int = None,
           snapshot_dir_visible: bool = None, tuning: dict = None,
           capacity_autonegotiation: dict = None, worm: dict = None,
           task_remarks: str = None, audit_log_rules: list = None,
           unix_permissions: str = None) -> dict:
    url = "/rest/fileservice/v1/filesystems/{file_system_id}"

    payload = {}

    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description
    if capacity is not None:
        payload['capacity'] = capacity

    payload = {}

    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description
    if capacity is not None:
        payload['capacity'] = capacity
    if capacity_threshold is not None:
        payload['capacity_threshold'] = capacity_threshold
    if initial_distribute_policy is not None:
        payload['initial_distribute_policy'] = initial_distribute_policy
    if automatic_update_time is not None:
        payload['automatic_update_time'] = automatic_update_time
    if atime_update_mode is not None:
        payload['atime_update_mode'] = atime_update_mode
    if quota_switch is not None:
        payload['quota_switch'] = quota_switch
    if vaai_switch is not None:
        payload['vaai_switch'] = vaai_switch
    if owning_controller is not None:
        payload['owning_controller'] = owning_controller
    if snapshot_expired_enabled is not None:
        payload['snapshot_expired_enabled'] = snapshot_expired_enabled
    if checksum_enabled is not None:
        payload['checksum_enabled'] = checksum_enabled
    if ads_enabled is not None:
        payload['ads_enabled'] = ads_enabled
    if security_mode is not None:
        payload['security_mode'] = security_mode
    if nas_locking_policy is not None:
        payload['nas_locking_policy'] = nas_locking_policy
    if snapshot_reserved_space_percentage is not None:
        payload['snapshot_reserved_space_percentage'] = snapshot_reserved_space_percentage
    if periodic_snapshots_limit is not None:
        payload['periodic_snapshots_limit'] = periodic_snapshots_limit
    if snapshot_dir_visible is not None:
        payload['snapshot_dir_visible'] = snapshot_dir_visible
    if tuning is not None:
        payload['tuning'] = tuning
    if capacity_autonegotiation is not None:
        payload['capacity_autonegotiation'] = capacity_autonegotiation
    if worm is not None:
        payload['worm'] = worm
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks
    if audit_log_rules is not None:
        payload['audit_log_rules'] = audit_log_rules
    if unix_permissions is not None:
        payload['unix_permissions'] = unix_permissions

    response = client.put(url, body=payload, params={"file_system_id": file_system_id})
    return response



# ============================================================================
# namespace (命名空间) 子主题相关动作
# ============================================================================

def namespace_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 100,
         sort_dir: str = None, sort_key: str = None, name: str = None,
         vstore_name: str = None, vstore_raw_id: str = None, vstore_id: str = None,
         raw_id: str = None, pool_name: str = None, storage_id: str = None,
         enable_encrypt: bool = None, support_provisioning: bool = None,
         gfs_id: str = None, gfs_name: str = None, has_gfs: bool = None) -> dict:
    url = "/rest/fileservice/v1/namespaces/query"
    
    payload = {}
    
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if name is not None:
        payload['name'] = name
    if vstore_name is not None:
        payload['vstore_name'] = vstore_name
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if pool_name is not None:
        payload['pool_name'] = pool_name
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if enable_encrypt is not None:
        payload['enable_encrypt'] = enable_encrypt
    if support_provisioning is not None:
        payload['support_provisioning'] = support_provisioning
    if gfs_id is not None:
        payload['gfs_id'] = gfs_id
    if gfs_name is not None:
        payload['gfs_name'] = gfs_name
    if has_gfs is not None:
        payload['has_gfs'] = has_gfs
    
    response = client.post(url, body=payload)
    return response


def namespace_show(client: DMEAPIClient, namespace_id: str) -> dict:
    url = "/rest/fileservice/v1/namespaces/{namespace_id}"
    
    response = client.get(url, params={"namespace_id": namespace_id})
    return response


def namespace_create(client: DMEAPIClient, storage_id: str, pool_raw_id: str,
           namespace_specs: list = None, enable_update_atime: bool = None,
           trash_visible: bool = None, trash_enable: bool = None,
           interval_trash: int = None, dps_switch: bool = None,
           forbidden_dpc: bool = None, audit_log_switch: bool = None,
           audit_log_rule: list = None, atime_update_mode: int = None,
           acl_policy_type: str = None, enable_encrypt: bool = None,
           crypt_alg: str = None, case_sensitive: bool = None,
           show_snap_dir: bool = None, rdc: str = None, worm: dict = None,
           qos_policy: dict = None, public_network_qos_policy: dict = None,
           private_network_qos_policy: dict = None,
           create_s3_param: dict = None, application_type: str = None,
           task_remarks: str = None) -> dict:
    url = "/rest/fileservice/v1/namespaces"
    
    payload = {
        'storage_id': storage_id,
        'pool_raw_id': pool_raw_id
    }
    
    if namespace_specs is not None:
        payload['namespace_specs'] = namespace_specs
    if enable_update_atime is not None:
        payload['enable_update_atime'] = enable_update_atime
    if trash_visible is not None:
        payload['trash_visible'] = trash_visible
    if trash_enable is not None:
        payload['trash_enable'] = trash_enable
    if interval_trash is not None:
        payload['interval_trash'] = interval_trash
    if dps_switch is not None:
        payload['dps_switch'] = dps_switch
    if forbidden_dpc is not None:
        payload['forbidden_dpc'] = forbidden_dpc
    if audit_log_switch is not None:
        payload['audit_log_switch'] = audit_log_switch
    if audit_log_rule is not None:
        payload['audit_log_rule'] = audit_log_rule
    if atime_update_mode is not None:
        payload['atime_update_mode'] = atime_update_mode
    if acl_policy_type is not None:
        payload['acl_policy_type'] = acl_policy_type
    if enable_encrypt is not None:
        payload['enable_encrypt'] = enable_encrypt
    if crypt_alg is not None:
        payload['crypt_alg'] = crypt_alg
    if case_sensitive is not None:
        payload['case_sensitive'] = case_sensitive
    if show_snap_dir is not None:
        payload['show_snap_dir'] = show_snap_dir
    if rdc is not None:
        payload['rdc'] = rdc
    if worm is not None:
        payload['worm'] = worm
    if qos_policy is not None:
        payload['qos_policy'] = qos_policy
    if public_network_qos_policy is not None:
        payload['public_network_qos_policy'] = public_network_qos_policy
    if private_network_qos_policy is not None:
        payload['private_network_qos_policy'] = private_network_qos_policy
    if create_s3_param is not None:
        payload['create_s3_param'] = create_s3_param
    if application_type is not None:
        payload['application_type'] = application_type
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks
    
    response = client.post(url, body=payload)
    return response


def namespace_modify(client: DMEAPIClient, namespace_id: str,
           enable_update_atime: bool = None, show_snap_dir: bool = None,
           trash_visible: bool = None, trash_enable: bool = None,
           interval_trash: int = None, dps_switch: bool = None,
           forbidden_dpc: bool = None, audit_log_switch: bool = None,
           audit_log_rule: list = None, atime_update_mode: int = None,
           acl_policy_type: str = None, enable_encrypt: bool = None,
           qos_policy: dict = None, public_network_qos_policy: dict = None,
           private_network_qos_policy: dict = None,
           application_type: str = None, task_remarks: str = None) -> dict:
    url = "/rest/fileservice/v1/namespaces/{namespace_id}"
    
    payload = {}
    
    if enable_update_atime is not None:
        payload['enable_update_atime'] = enable_update_atime
    if show_snap_dir is not None:
        payload['show_snap_dir'] = show_snap_dir
    if trash_visible is not None:
        payload['trash_visible'] = trash_visible
    
    payload = {}
    
    if enable_update_atime is not None:
        payload['enable_update_atime'] = enable_update_atime
    if show_snap_dir is not None:
        payload['show_snap_dir'] = show_snap_dir
    if trash_visible is not None:
        payload['trash_visible'] = trash_visible
    if trash_enable is not None:
        payload['trash_enable'] = trash_enable
    if interval_trash is not None:
        payload['interval_trash'] = interval_trash
    if dps_switch is not None:
        payload['dps_switch'] = dps_switch
    if forbidden_dpc is not None:
        payload['forbidden_dpc'] = forbidden_dpc
    if audit_log_switch is not None:
        payload['audit_log_switch'] = audit_log_switch
    if audit_log_rule is not None:
        payload['audit_log_rule'] = audit_log_rule
    if atime_update_mode is not None:
        payload['atime_update_mode'] = atime_update_mode
    if acl_policy_type is not None:
        payload['acl_policy_type'] = acl_policy_type
    if enable_encrypt is not None:
        payload['enable_encrypt'] = enable_encrypt
    if qos_policy is not None:
        payload['qos_policy'] = qos_policy
    if public_network_qos_policy is not None:
        payload['public_network_qos_policy'] = public_network_qos_policy
    if private_network_qos_policy is not None:
        payload['private_network_qos_policy'] = private_network_qos_policy
    if application_type is not None:
        payload['application_type'] = application_type
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks
    
    response = client.put(url, body=payload, params={"namespace_id": namespace_id})
    return response


def namespace_delete(client: DMEAPIClient, namespace_ids: list, task_remarks: str = None) -> dict:
    url = "/rest/fileservice/v1/namespaces/delete"
    
    payload = {
        'namespace_ids': namespace_ids
    }
    
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks
    
    response = client.post(url, body=payload)
    return response


def nfs_share_show_clients(client: DMEAPIClient, page_no: int = 1, page_size: int = 20,
                           nfs_share_id: str = None, storage_id: str = None,
                           vstore_id_in_storage: str = None, name: str = None,
                           client_id_in_storage: str = None, sort_key: str = None,
                           sort_dir: str = None) -> dict:
    url = "/rest/fileservice/v2/nfs-auth-clients/query"

    payload = {}

    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size
    if nfs_share_id is not None:
        payload['nfs_share_id'] = nfs_share_id
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if vstore_id_in_storage is not None:
        payload['vstore_id_in_storage'] = vstore_id_in_storage
    if name is not None:
        payload['name'] = name
    if client_id_in_storage is not None:
        payload['client_id_in_storage'] = client_id_in_storage
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def account_dataturbo_admin_list(client: DMEAPIClient, storage_id: str = None, vstore_id: str = None,
                   vstore_name: str = None, zone_id: str = None, name: str = None,
                   online_status: str = None, lock_status: str = None,
                   account_state: str = None, sort_key: str = None,
                   sort_dir: str = None, page_no: int = 1,
                   page_size: int = 20) -> dict:
    url = "/rest/fileservice/v1/dpc-administrators/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if storage_id is not None:
        payload['storage_id'] = storage_id
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id
    if vstore_name is not None:
        payload['vstore_name'] = vstore_name
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if name is not None:
        payload['name'] = name
    if online_status is not None:
        payload['online_status'] = online_status
    if lock_status is not None:
        payload['lock_status'] = lock_status
    if account_state is not None:
        payload['account_state'] = account_state
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def account_unix_user_modify(client: DMEAPIClient, id: str, raw_id: int = None,
                              description: str = None, primary_group_name: str = None,
                              primary_group_raw_id: int = None,
                              status_enable: bool = None) -> dict:
    url = "/rest/fileservice/v1/unix-users/{id}"

    payload = {}

    if raw_id is not None:
        payload['raw_id'] = raw_id
    if description is not None:
        payload['description'] = description
    if primary_group_name is not None:
        payload['primary_group_name'] = primary_group_name

    payload = {}

    if raw_id is not None:
        payload['raw_id'] = raw_id
    if description is not None:
        payload['description'] = description
    if primary_group_name is not None:
        payload['primary_group_name'] = primary_group_name
    if primary_group_raw_id is not None:
        payload['primary_group_raw_id'] = primary_group_raw_id
    if status_enable is not None:
        payload['status_enable'] = status_enable

    response = client.put(url, body=payload, params={"id": id})
    return response


def account_unix_user_group_create(client: DMEAPIClient, storage_id: str, name: str,
                                    vstore_raw_id: str, raw_id: int = None,
                                    description: str = None,
                                    zone_id: str = None) -> dict:
    url = "/rest/fileservice/v1/unix-user-groups"

    payload = {
        'storage_id': storage_id,
        'name': name,
        'vstore_raw_id': vstore_raw_id,
    }

    if raw_id is not None:
        payload['raw_id'] = raw_id
    if description is not None:
        payload['description'] = description
    if zone_id is not None:
        payload['zone_id'] = zone_id

    response = client.post(url, body=payload)
    return response


def account_unix_user_batch_delete(client: DMEAPIClient, ids: list) -> dict:
    url = "/rest/fileservice/v1/unix-users/delete"

    payload = {
        'ids': ids,
    }

    response = client.post(url, body=payload)
    return response


def account_unix_user_group_list(client: DMEAPIClient, storage_id: str = None,
                                   storage_name: str = None,
                                   vstore_raw_id: str = None,
                                   vstore_name: str = None, name: str = None,
                                   raw_id: str = None, zone_id: str = None,
                                   sort_key: str = None, sort_dir: str = None,
                                   page_no: int = 1,
                                   page_size: int = 100) -> dict:
    url = "/rest/fileservice/v1/unix-user-groups/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size,
    }

    if storage_name is not None:
        payload['storage_name'] = storage_name
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if vstore_name is not None:
        payload['vstore_name'] = vstore_name
    if name is not None:
        payload['name'] = name
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def account_unix_user_group_show(client: DMEAPIClient, id: str) -> dict:
    url = "/rest/fileservice/v1/unix-user-groups/{id}"

    response = client.get(url, params={"id": id})
    return response


def account_unix_user_group_modify(client: DMEAPIClient, id: str,
                                    raw_id: int = None,
                                    description: str = None) -> dict:
    url = "/rest/fileservice/v1/unix-user-groups/{id}"

    payload = {}

    if raw_id is not None:
        payload['raw_id'] = raw_id
    if description is not None:
        payload['description'] = description

    response = client.put(url, body=payload, params={"id": id})
    return response


def account_unix_user_group_batch_delete(client: DMEAPIClient, ids: list) -> dict:
    url = "/rest/fileservice/v1/unix-user-groups/delete"

    payload = {
        'ids': ids,
    }

    response = client.post(url, body=payload)
    return response


def account_unix_user_remove_group(client: DMEAPIClient, user_id: str,
                                    secondary_group_name_list: list) -> dict:
    url = "/rest/fileservice/v1/unix-users/{user_id}/remove-secondary-group"

    payload = {
        'secondary_group_name_list': secondary_group_name_list,
    }

    response = client.post(url, body=payload, params={"user_id": user_id})
    return response


def account_unix_user_show(client: DMEAPIClient, id: str) -> dict:
    url = "/rest/fileservice/v1/unix-users/{id}"

    response = client.get(url, params={"id": id})
    return response


def account_unix_user_list(client: DMEAPIClient, storage_id: str = None,
                             storage_name: str = None, vstore_raw_id: str = None,
                             vstore_name: str = None, name: str = None,
                             primary_group_name: str = None, raw_id: str = None,
                             zone_id: str = None, user_status: str = None,
                             sort_key: str = None, sort_dir: str = None,
                             page_no: int = 1, page_size: int = 100) -> dict:
    url = "/rest/fileservice/v1/unix-users/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size,
    }

    if storage_name is not None:
        payload['storage_name'] = storage_name
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if vstore_name is not None:
        payload['vstore_name'] = vstore_name
    if name is not None:
        payload['name'] = name
    if primary_group_name is not None:
        payload['primary_group_name'] = primary_group_name
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if user_status is not None:
        payload['user_status'] = user_status
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def account_unix_user_add_group(client: DMEAPIClient, user_id: str,
                                 secondary_group_name_list: list) -> dict:
    url = "/rest/fileservice/v1/unix-users/{user_id}/add-secondary-group"

    payload = {
        'secondary_group_name_list': secondary_group_name_list,
    }

    response = client.post(url, body=payload, params={"user_id": user_id})
    return response


def account_unix_user_create(client: DMEAPIClient, storage_id: str, name: str, vstore_raw_id: str,
                              raw_id: int = None, description: str = None,
                              primary_group_raw_id: int = None,
                              primary_group_name: str = None, zone_id: str = None,
                              status: bool = None,
                              secondary_group_name_list: list = None) -> dict:
    url = "/rest/fileservice/v1/unix-users"

    payload = {
        'storage_id': storage_id,
        'name': name,
        'vstore_raw_id': vstore_raw_id,
    }

    if raw_id is not None:
        payload['raw_id'] = raw_id
    if description is not None:
        payload['description'] = description
    if primary_group_raw_id is not None:
        payload['primary_group_raw_id'] = primary_group_raw_id
    if primary_group_name is not None:
        payload['primary_group_name'] = primary_group_name
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if status is not None:
        payload['status'] = status
    if secondary_group_name_list is not None:
        payload['secondary_group_name_list'] = secondary_group_name_list

    response = client.post(url, body=payload)
    return response


def kvcache_batch_create(client: DMEAPIClient, storage_id: str, zone_id: str,
                          pool_raw_id: str, vstore_id: str, kv_cache_stores: list,
                          data_cleanup_switch: str = None,
                          max_survival_time: int = None) -> dict:
    url = "/rest/kvcachemgmt/v1/kv-cache-stores"

    payload = {
        'storage_id': storage_id,
        'zone_id': zone_id,
        'pool_raw_id': pool_raw_id,
        'vstore_id': vstore_id,
        'kv_cache_stores': kv_cache_stores,
    }

    if data_cleanup_switch is not None:
        payload['data_cleanup_switch'] = data_cleanup_switch
    if max_survival_time is not None:
        payload['max_survival_time'] = max_survival_time

    response = client.post(url, body=payload)
    return response


def kvcache_modify(client: DMEAPIClient, kv_cache_stores_id: str, name: str = None,
                    description: str = None, data_cleanup_switch: str = None,
                    max_survival_time: int = None) -> dict:
    url = "/rest/kvcachemgmt/v1/kv-cache-stores/{kv_cache_stores_id}"

    payload = {}

    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description
    if data_cleanup_switch is not None:
        payload['data_cleanup_switch'] = data_cleanup_switch

    payload = {}

    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description
    if data_cleanup_switch is not None:
        payload['data_cleanup_switch'] = data_cleanup_switch
    if max_survival_time is not None:
        payload['max_survival_time'] = max_survival_time

    response = client.put(url, body=payload, params={"kv_cache_stores_id": kv_cache_stores_id})
    return response


def kvcache_batch_delete(client: DMEAPIClient, ids: list) -> dict:
    url = "/rest/kvcachemgmt/v1/kv-cache-stores/delete"

    payload = {
        'ids': ids,
    }

    response = client.post(url, body=payload)
    return response


def kvcache_list(client: DMEAPIClient, storage_id: str = None, id: str = None,
                  raw_id: str = None, name: str = None, zone_id: str = None,
                  pool_raw_id: str = None, vstore_id: str = None,
                  vstore_name: str = None, fs_id: str = None,
                  fs_name: str = None, data_cleanup_switch: str = None,
                  page_no: int = 1, page_size: int = 20,
                  sort_dir: str = None, sort_key: str = None) -> dict:
    url = "/rest/kvcachemgmt/v1/kv-cache-stores/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size,
    }

    if storage_id is not None:
        payload['storage_id'] = storage_id
    if id is not None:
        payload['id'] = id
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if name is not None:
        payload['name'] = name
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if pool_raw_id is not None:
        payload['pool_raw_id'] = pool_raw_id
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id
    if vstore_name is not None:
        payload['vstore_name'] = vstore_name
    if fs_id is not None:
        payload['fs_id'] = fs_id
    if fs_name is not None:
        payload['fs_name'] = fs_name
    if data_cleanup_switch is not None:
        payload['data_cleanup_switch'] = data_cleanup_switch
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if sort_key is not None:
        payload['sort_key'] = sort_key

    response = client.post(url, body=payload)
    return response


ACTIONS = {
    'account_dataturbo_admin_list': {
        'func': account_dataturbo_admin_list,
        'params': ['storage_id', 'vstore_id', 'vstore_name', 'zone_id', 'name', 'online_status', 'lock_status', 'account_state', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_unix_user_create': {
        'func': account_unix_user_create,
        'params': ['storage_id', 'name', 'vstore_raw_id', 'raw_id', 'description', 'primary_group_raw_id', 'primary_group_name', 'zone_id', 'status', 'secondary_group_name_list'],
        'subtopic': 'account'
    },
    'account_unix_user_add_group': {
        'func': account_unix_user_add_group,
        'params': ['user_id', 'secondary_group_name_list'],
        'subtopic': 'account'
    },
    'account_unix_user_list': {
        'func': account_unix_user_list,
        'params': ['storage_id', 'storage_name', 'vstore_raw_id', 'vstore_name', 'name', 'primary_group_name', 'raw_id', 'zone_id', 'user_status', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_unix_user_show': {
        'func': account_unix_user_show,
        'params': ['id'],
        'subtopic': 'account'
    },
    'account_unix_user_remove_group': {
        'func': account_unix_user_remove_group,
        'params': ['user_id', 'secondary_group_name_list'],
        'subtopic': 'account'
    },
    'account_unix_user_modify': {
        'func': account_unix_user_modify,
        'params': ['id', 'raw_id', 'description', 'primary_group_name', 'primary_group_raw_id', 'status_enable'],
        'subtopic': 'account'
    },
    'account_unix_user_batch_delete': {
        'func': account_unix_user_batch_delete,
        'params': ['ids'],
        'subtopic': 'account'
    },
    'account_unix_user_group_create': {
        'func': account_unix_user_group_create,
        'params': ['storage_id', 'name', 'vstore_raw_id', 'raw_id', 'description', 'zone_id'],
        'subtopic': 'account'
    },
    'account_unix_user_group_list': {
        'func': account_unix_user_group_list,
        'params': ['storage_id', 'storage_name', 'vstore_raw_id', 'vstore_name', 'name', 'raw_id', 'zone_id', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_unix_user_group_show': {
        'func': account_unix_user_group_show,
        'params': ['id'],
        'subtopic': 'account'
    },
    'account_unix_user_group_modify': {
        'func': account_unix_user_group_modify,
        'params': ['id', 'raw_id', 'description'],
        'subtopic': 'account'
    },
    'account_unix_user_group_batch_delete': {
        'func': account_unix_user_group_batch_delete,
        'params': ['ids'],
        'subtopic': 'account'
    },
    'dtree_list': {
        'func': dtree_list,
        'params': ['id_in_storage', 'name', 'device_name', 'storage_id', 'zone_id', 'manufacturer', 'tier_name', 'fs_name', 'fs_id', 'namespace_name', 'namespace_id', 'quota_switch', 'security_mode', 'nas_locking_policy', 'sort_key', 'sort_dir', 'page_no', 'page_size', 'dc_id', 'dc_name'],
        'subtopic': 'dtree'
    },
    'dtree_show': {
        'func': dtree_show,
        'params': ['dtree_id'],
        'subtopic': 'dtree'
    },
    'dtree_create': {
        'func': dtree_create,
        'params': ['storage_id', 'create_dtrees_param', 'fs_id', 'namespace_id', 'zone_id', 'parent_dir', 'quota_switch', 'security_mode', 'nas_locking_policy', 'create_nfs_share_param', 'create_cifs_share_param', 'dataturbo_share', 'create_worm_param', 'unix_permissions', 'task_remarks'],
        'subtopic': 'dtree'
    },
    'dtree_delete': {
        'func': dtree_delete,
        'params': ['dtree_ids', 'task_remarks'],
        'subtopic': 'dtree'
    },
    'dtree_modify': {
        'func': dtree_modify,
        'params': ['dtree_id', 'name', 'quota_switch', 'security_mode', 'nas_locking_policy', 'unix_permissions', 'task_remarks'],
        'subtopic': 'dtree'
    },
    # NFS share 子主题动作
    'nfs_share_list': {
        'func': nfs_share_list,
        'params': ['id_in_storage', 'name', 'share_path', 'exact_share_path', 'device_name', 'storage_id', 'tier_name', 'owning_dtree_name', 'fs_name', 'fs_id', 'owning_dtree_id', 'vstore_name', 'page_no', 'page_size', 'sort_key', 'sort_dir', 'support_provisioning', 'namespace_id', 'namespace_name', 'dc_id', 'dc_name', 'zone_id', 'zone_name', 'zone_ip'],
        'subtopic': 'nfs_share'
    },
    'nfs_share_show': {
        'func': nfs_share_show,
        'params': ['nfs_share_id'],
        'subtopic': 'nfs_share'
    },
    'nfs_share_create': {
        'func': nfs_share_create,
        'params': ['create_nfs_share_param', 'task_remarks'],
        'subtopic': 'nfs_share'
    },
    'nfs_share_modify': {
        'func': nfs_share_modify,
        'params': ['nfs_share_id', 'description', 'character_encoding', 'audit_items', 'show_snapshot_enable', 'nfs_share_client_addition', 'nfs_share_client_modification', 'nfs_share_client_deletion', 'file_name_ex_filters', 'task_remarks'],
        'subtopic': 'nfs_share'
    },
    'nfs_share_delete': {
        'func': nfs_share_delete,
        'params': ['nfs_share_ids', 'task_remarks'],
        'subtopic': 'nfs_share'
    },
    'nfs_share_show_clients': {
        'func': nfs_share_show_clients,
        'params': ['page_no', 'page_size', 'nfs_share_id', 'storage_id', 'vstore_id_in_storage', 'name', 'client_id_in_storage', 'sort_key', 'sort_dir'],
        'subtopic': 'nfs_share'
    },
    # CIFS 共享子主题动作
    'cifs_share_list': {
        'func': cifs_share_list,
        'params': ['raw_id', 'name', 'share_path', 'exact_share_path', 'fs_id', 'fs_name', 'dtree_id', 'dtree_name', 'storage_id', 'storage_name', 'vstore_raw_id', 'vstore_name', 'manufacturer', 'op_lock_enabled', 'notify_enabled', 'offline_file_modes', 'file_extension_filter_enabled', 'abe_enabled', 'page_no', 'page_size', 'sort_key', 'sort_dir', 'namespace_id', 'namespace_name', 'support_provisioning', 'dc_id', 'dc_name'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_show': {
        'func': cifs_share_show,
        'params': ['cifs_share_id'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_create': {
        'func': cifs_share_create,
        'params': ['create_cifs_param', 'fs_id', 'namespace_id', 'task_remarks'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_modify': {
        'func': cifs_share_modify,
        'params': ['cifs_share_id', 'description', 'op_lock_enabled', 'notify_enabled', 'ca_enabled', 'offline_file_mode', 'ip_control_enabled', 'abe_enabled', 'audititem_list', 'apply_default_acl', 'file_extension_filter_enabled', 'show_previous_versions_enabled', 'show_snapshot_enabled', 'user_and_user_group_info', 'ip_and_segments', 'file_name_ex_filters', 'task_remarks', 'smb3_encryption_enable', 'unencrypted_access', 'enable_lease'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_delete': {
        'func': cifs_share_delete,
        'params': ['cifs_share_ids', 'task_remarks'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_show_permissions': {
        'func': cifs_share_show_permissions,
        'params': ['cifs_share_id', 'type', 'user_filter', 'ip_filter', 'file_filter', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'cifs_share'
    },
    # dataturbo_share 子主题动作
    'dataturbo_share_list': {
        'func': dataturbo_share_list,
        'params': ['page_no', 'page_size', 'raw_id', 'share_path', 'fs_id', 'fs_name', 'dtree_id', 'dtree_name', 'vstore_id', 'vstore_raw_id', 'vstore_name', 'storage_id', 'storage_name', 'zone_id', 'zone_name', 'scope', 'sort_key', 'sort_dir'],
        'subtopic': 'dataturbo_share'
    },
    'dataturbo_share_show': {
        'func': dataturbo_share_show,
        'params': ['dataturbo_share_id'],
        'subtopic': 'dataturbo_share'
    },
    'dataturbo_share_create': {
        'func': dataturbo_share_create,
        'params': ['charset', 'fs_id', 'dtree_id', 'description', 'dataturbo_share_auth', 'task_remarks'],
        'subtopic': 'dataturbo_share'
    },
    'dataturbo_share_modify': {
        'func': dataturbo_share_modify,
        'params': ['dataturbo_share_id', 'description', 'dataturbo_share_auth_addition', 'dataturbo_share_auth_deletion', 'task_remarks'],
        'subtopic': 'dataturbo_share'
    },
    'dataturbo_share_delete': {
        'func': dataturbo_share_delete,
        'params': ['dataturbo_share_ids', 'task_remarks'],
        'subtopic': 'dataturbo_share'
    },
    'dataturbo_share_show_permissions': {
        'func': dataturbo_share_show_permissions,
        'params': ['dataturbo_share_id', 'page_no', 'page_size', 'user_id', 'user_name', 'permission'],
        'subtopic': 'dataturbo_share'
    },
    # quota 子主题动作
    'quota_list': {
        'func': quota_list,
        'params': ['page_no', 'page_size', 'ids', 'raw_ids', 'quota_type', 'parent_type', 'parent_raw_id', 'owner_name', 'vstore_id', 'vstore_raw_id', 'storage_id', 'sort_key', 'sort_dir', 'zone_id'],
        'subtopic': 'quota'
    },
    'quota_show': {
        'func': quota_show,
        'params': ['quota_id'],
        'subtopic': 'quota'
    },
    'quota_create': {
        'func': quota_create,
        'params': ['parent_id', 'parent_type', 'quota_type', 'space_soft_quota', 'space_hard_quota', 'space_advisory_quota', 'file_soft_quota', 'file_hard_quota', 'file_advisory_quota', 'snap_space_switch', 'soft_grace_time', 'quota_owner', 'dir_quota_target', 'task_remarks'],
        'subtopic': 'quota'
    },
    'quota_modify': {
        'func': quota_modify,
        'params': ['quota_id', 'space_soft_quota', 'space_hard_quota', 'space_advisory_quota', 'file_soft_quota', 'file_hard_quota', 'file_advisory_quota', 'snap_space_switch', 'soft_grace_time', 'task_remarks'],
        'subtopic': 'quota'
    },
    'quota_delete': {
        'func': quota_delete,
        'params': ['quota_ids', 'task_remarks'],
        'subtopic': 'quota'
    },
    # filesystem 子主题动作
    'filesystem_list': {
        'func': filesystem_list,
        'params': ['page_no', 'page_size', 'sort_dir', 'sort_key', 'name', 'fs_raw_id', 'storage_id'],
        'subtopic': 'filesystem'
    },
    'filesystem_show': {
        'func': filesystem_show,
        'params': ['filesystem_id'],
        'subtopic': 'filesystem'
    },
    'filesystem_delete': {
        'func': filesystem_delete,
        'params': ['filesystem_ids', 'task_remarks'],
        'subtopic': 'filesystem'
    },
    'filesystem_batch_modify': {
        'func': filesystem_batch_modify,
        'params': ['filesystems', 'task_remarks'],
        'subtopic': 'filesystem'
    },
    'filesystem_create': {
        'func': filesystem_create,
        'params': ['storage_id', 'pool_raw_id', 'filesystem_specs', 'vstore_id', 'zone_id', 'task_remarks', 'gfs_group_id', 'automatic_update_time', 'atime_update_mode', 'schedule_name', 'quota_switch', 'vaai_switch', 'initial_distribute_policy', 'capacity_threshold'],
        'subtopic': 'filesystem'
    },
    'filesystem_query_available': {
        'func': filesystem_query_available,
        'params': ['feature_type', 'local_storage_id', 'remote_storage_id', 'name', 'page_no', 'page_size', 'sort_key', 'sort_dir'],
        'subtopic': 'filesystem'
    },
    'filesystem_modify': {
        'func': filesystem_modify,
        'params': ['file_system_id', 'name', 'description', 'capacity', 'capacity_threshold', 'initial_distribute_policy', 'automatic_update_time', 'atime_update_mode', 'quota_switch', 'vaai_switch', 'owning_controller', 'task_remarks'],
        'subtopic': 'filesystem'
    },
    # namespace 子主题动作
    'namespace_list': {
        'func': namespace_list,
        'params': ['page_no', 'page_size', 'sort_dir', 'sort_key', 'name', 
                   'vstore_name', 'vstore_raw_id', 'vstore_id', 'raw_id',
                   'pool_name', 'storage_id', 'enable_encrypt', 
                   'support_provisioning', 'gfs_id', 'gfs_name', 'has_gfs'],
        'subtopic': 'namespace'
    },
    'namespace_show': {
        'func': namespace_show,
        'params': ['namespace_id'],
        'subtopic': 'namespace'
    },
    'namespace_create': {
        'func': namespace_create,
        'params': ['storage_id', 'pool_raw_id', 'namespace_specs', 
                   'enable_update_atime', 'trash_visible', 'trash_enable',
                   'interval_trash', 'dps_switch', 'forbidden_dpc',
                   'audit_log_switch', 'audit_log_rule', 'atime_update_mode',
                   'acl_policy_type', 'enable_encrypt', 'crypt_alg',
                   'case_sensitive', 'show_snap_dir', 'rdc', 'worm',
                   'qos_policy', 'public_network_qos_policy',
                   'private_network_qos_policy', 'create_s3_param',
                   'application_type', 'task_remarks'],
        'subtopic': 'namespace'
    },
    'namespace_modify': {
        'func': namespace_modify,
        'params': ['namespace_id', 'enable_update_atime', 'show_snap_dir',
                   'trash_visible', 'trash_enable', 'interval_trash',
                   'dps_switch', 'forbidden_dpc', 'audit_log_switch',
                   'audit_log_rule', 'atime_update_mode', 'acl_policy_type',
                   'enable_encrypt', 'qos_policy', 'public_network_qos_policy',
                   'private_network_qos_policy', 'application_type', 'task_remarks'],
        'subtopic': 'namespace'
    },
    'namespace_delete': {
        'func': namespace_delete,
        'params': ['namespace_ids', 'task_remarks'],
        'subtopic': 'namespace'
    },
    # dataturbo 子主题动作（原 dpc 子主题，重命名）
    'dpc_list': {
        'func': dpc_list,
        'params': ['ids', 'hostname', 'ip', 'mgmt_status', 'status', 'sn', 'storage_id', 'dpc_om_id', 'dpc_type', 'client_version', 'page_no', 'page_size'],
        'subtopic': 'dataturbo'
    },
    'dpc_show': {
        'func': dpc_show,
        'params': ['dpc_id'],
        'subtopic': 'dataturbo'
    },
    # dpc 子主题动作 (DPC客户端)
    'list': {
        'func': dpc_client_list,
        'params': ['storage_id', 'process_id', 'name', 'manage_ip', 'version', 'status', 'switch_status', 'upgrade_flag', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'dpc'
    },
    'show': {
        'func': dpc_client_show,
        'params': ['id'],
        'subtopic': 'dpc'
    },
    # kvcache 子主题动作
    'kvcache_list': {
        'func': kvcache_list,
        'params': ['storage_id', 'id', 'raw_id', 'name', 'zone_id', 'pool_raw_id', 'vstore_id', 'vstore_name', 'fs_id', 'fs_name', 'data_cleanup_switch', 'page_no', 'page_size', 'sort_dir', 'sort_key'],
        'subtopic': 'kvcache'
    },
    'kvcache_batch_create': {
        'func': kvcache_batch_create,
        'params': ['storage_id', 'zone_id', 'pool_raw_id', 'vstore_id', 'kv_cache_stores', 'data_cleanup_switch', 'max_survival_time'],
        'subtopic': 'kvcache'
    },
    'kvcache_modify': {
        'func': kvcache_modify,
        'params': ['kv_cache_stores_id', 'name', 'description', 'data_cleanup_switch', 'max_survival_time'],
        'subtopic': 'kvcache'
    },
    'kvcache_batch_delete': {
        'func': kvcache_batch_delete,
        'params': ['ids'],
        'subtopic': 'kvcache'
    },
}
