"""
NAS operations
"""

import sys
import os

from pydme.client import DMEAPIClient


# ============================================================================
# DPC (Distributed Parallel Client) subtopic functions
# ============================================================================


def dpc_list(client: DMEAPIClient, ids: list = None, hostname: str = None, ip: str = None,
             mgmt_status: list = None, status: list = None, sn: str = None,
             storage_id: str = None, dpc_om_id: str = None, dpc_type: list = None,
             client_version: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch query DPC list

    Args:
        client: DME API client
        ids: DPC ID list (Optional), List<string> type, max array members 100, exact match
        hostname: Compute node hostname (Optional), 1~256 characters, fuzzy search
        ip: Management IP of DPC compute node (Optional), 1~256 characters, fuzzy search
        mgmt_status: Management status list (Optional), List<string> type, exact match. Options: normal, abnormal, unready, subhealth, pre_registered, unknown
        status: Service status list (Optional), List<string> type, exact match. Options: normal, abnormal, subhealth, unknown
        sn: Hardware SN of compute node (Optional), 1~256 characters, fuzzy search
        storage_id: Storage device ID (Optional), 1~256 characters, exact match
        dpc_om_id: DPC O&M ID (Optional), 1~256 characters, exact match
        dpc_type: DPC type list (Optional), List<string> type
        client_version: DPC client version (Optional), max 256 characters, exact match
        page_no: Page number (Optional), 1~10000000, default 1
        page_size: Items per page (Optional), 1~1000, default 20

    Returns:
        {
            total: Total DPC count (integer),
            dpcs: DPC list (List<DpcInfo>)。参数格式如下：[{
                id: DPC ID (string),
                hostname: Hostname (string),
                ip: Management IP (string),
                status: Service status (string),
                mgmt_status: Management status (string),
            }, ...],
        }
    """
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
    """
    Query DPC details.

    Args:
        client: DME API client
        dpc_id: DPC ID (Required, string)

    Returns:
        {
            id: DPC ID (string),
            hostname: Hostname (string),
            ip: Management IP (string),
            status: Service status (string),
            mgmt_status: Management status (string),
        }
    """
    url = "/rest/dpc-mgmt/v1/dpcs/{dpc_id}"

    if not dpc_id:
        raise ValueError("dpc_id is required")

    response = client.get(url, params={"dpc_id": dpc_id})
    return response


def dpc_client_list(client: DMEAPIClient, storage_id: str = None,
                     process_id: str = None, name: str = None,
                     manage_ip: str = None, version: str = None,
                     status: str = None, switch_status: str = None,
                     upgrade_flag: str = None, sort_key: str = None,
                     sort_dir: str = None,
                     page_no: int = 1, page_size: int = 10) -> dict:
    """
    Batch query DPC clients.

    Args:
        client: DME API client
        storage_id: Storage ID (Optional, string, 1~64 characters)
        process_id: DPC client process ID (Optional, string, 1~64 characters)
        name: DPC client name, supports fuzzy search (Optional, string, 1~256 characters)
        manage_ip: DPC client node management IP, supports fuzzy search (Optional, string, 1~256 characters)
        version: DPC client version, supports fuzzy search (Optional, string, 1~256 characters)
        status: DPC client status (Optional, string). Options: normal, abnormal, disabled
        switch_status: Node FSA switch status (Optional, string). Options: on, off
        upgrade_flag: Upgrade flag (Optional, string). Options: required, not_required
        sort_key: Sort field (Optional, string). Options: manage_ip, dpc_mem
        sort_dir: Sort direction (Optional, string). Options: asc (ascending), desc (descending)
        page_no: Page number (Optional, int32, 1~10000000). Default: 1
        page_size: Items per page (Optional, int32, 1~1000). Default: 10

    Returns:
        {
            total: Total count (integer),
            data: DPC client data (List<DpcClient>)。参数格式如下：[{
                id: ID (string),
                storage_id: Storage ID (string),
                process_id: DPC client process ID (string),
                name: DPC client name (string),
                manage_ip: DPC client node management IP (string),
                version: DPC client version (string),
                status: DPC client status (string),
                switch_status: Node FSA switch status (string),
                upgrade_flag: Upgrade flag (string),
                dpc_mem: DPC client node memory (int64),
            }, ...],
        }
    """
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
    """
    Query DPC client details.

    Args:
        client: DME API client
        id: DPC client ID (Required, string, 1~64 characters)

    Returns:
        {
            id: ID (string),
            storage_id: Storage ID (string),
            process_id: DPC client process ID (string),
            name: DPC client name (string),
            manage_ip: DPC client node management IP (string),
            version: DPC client version (string),
            status: DPC client status (string),
        }
    """
    url = "/rest/fileservice/v1/dpc-clients/{id}"

    if not id:
        raise ValueError("id is required")

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
    """
    Query Dtree list

    Args:
        client: DME API client
        id_in_storage: Dtree ID on storage (Optional), 1~256 characters
        name: Dtree name (Optional), 1~256 characters, supports fuzzy search
        device_name: Storage device name for the dtree (Optional), 1~256 characters, supports fuzzy search
        storage_id: Storage device ID for the dtree (Optional), 1~64 characters
        zone_id: Zone ID for the dtree (Optional), 36 characters; OceanStor A800/A600 series only
        manufacturer: Storage device vendor (Optional). Options: huawei, third_part
        tier_name: Service level name (Optional, reserved), 1~256 characters, supports fuzzy search
        fs_name: Filesystem name for the dtree (Optional), 1~256 characters, supports fuzzy search
        fs_id: Filesystem ID for the dtree (Optional), 1~64 characters, mutually exclusive with namespace_id
        namespace_name: Namespace name for the dtree (Optional), 1~64 characters
        namespace_id: Namespace ID for the dtree (Optional), 1~64 characters, mutually exclusive with fs_id
        quota_switch: Quota enabled (Optional), true: enabled; false: disabled
        security_mode: Security mode (Optional), 1~32 characters. Options: mixed, native, ntfs, unix
        nas_locking_policy: NAS locking policy (Optional). Options: mandatory, advisory, unknown
        sort_key: Sort field (Optional). Options: nfs_count, cifs_count, dataturbo_count, name
        sort_dir: Sort direction (Optional). Options: asc (ascending), desc (descending), default asc
        page_no: Page number (Optional), min 1, default 1
        page_size: Items per page (Optional), 1~1000, default 20
        dc_id: Data center ID (Optional), 1~128 characters
        dc_name: Data center name (Optional), 1~256 characters

    Returns:
        {
            total: Total Dtree count (integer),
            dtrees: Dtree list (List<DtreeInfo>)。参数格式如下：[{
                id: Dtree ID (string),
                name: Dtree name (string),
                path: Path (string),
                fs_id: Filesystem ID (string),
            }, ...],
        }
    """
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
    """
    Query Dtree details.

    Args:
        client: DME API client
        dtree_id: Dtree ID (Required, string)

    Returns:
        {
            id: Dtree ID (string),
            name: Dtree name (string),
            path: Path (string),
            fs_id: Filesystem ID (string),
        }
    """
    url = "/rest/fileservice/v1/dtrees/{dtree_id}"

    if not dtree_id:
        raise ValueError("dtree_id is required")

    response = client.get(url, params={"dtree_id": dtree_id})
    return response


def dtree_create(client: DMEAPIClient, storage_id: str, create_dtrees_param: list,
                 fs_id: str = None, namespace_id: str = None, zone_id: str = None,
                 parent_dir: str = None, quota_switch: bool = None,
                 security_mode: str = None, nas_locking_policy: str = None,
                 create_nfs_share_param: dict = None, create_cifs_share_param: dict = None,
                 dataturbo_share: dict = None, create_worm_param: dict = None,
                 unix_permissions: str = None, task_remarks: str = None) -> dict:
    """
    Create and share Dtree

    Create a Dtree and share it via NFS, CIFS, or DataTurbo.

    Args:
        client: DME API client
        storage_id: Storage device ID for the dtree, 1~64 characters
        create_dtrees_param: Dtree name and count list (Conditionally Required)。参数格式如下：[{
                dtree_name: Dtree name (1~255 characters, regex: ^[^,//:]+$, supports letters, digits, spaces and special chars; when creating multiple dtrees, names start from 0000),
                count: Number of dtrees to create (int, max 500 per group, total 500 across groups),
             }, ...]
        fs_id: Filesystem ID for the dtree, mutually exclusive with namespace_id, required for centralized storage
        namespace_id: Namespace ID for the dtree, mutually exclusive with fs_id, required for distributed storage
        zone_id: Zone ID for the dtree, OceanStor A800/A600 series only, 36 characters
        parent_dir: Parent directory, effective for distributed storage, 1~4008 characters
        quota_switch: Quota switch, true/false, default false
        security_mode: Security mode, mixed/native/ntfs/unix. Required if supported by model
        nas_locking_policy: NAS locking policy, mandatory/advisory/unknown
        create_nfs_share_param: Create NFS share. Not supported when creating multiple dtrees.
        create_cifs_share_param: Create CIFS share. Not supported when creating multiple dtrees.
        dataturbo_share: Create DataTurbo share (Optional)。参数格式如下：{
                description: DataTurbo share description (Optional, 0~255 characters),
                charset: Character set encoding (Required, fixed value UTF_8),
                dpc_share_auth: DataTurbo admin list (Optional)。参数格式如下：[{
                        dpc_user_id: DataTurbo admin ID (Required, 0~64 characters),
                        permission: DataTurbo admin permission (Required, fixed value read_and_write),
                     }, ...]
             }
        create_worm_param: WORM configuration (Optional)。参数格式如下：{
                worm_mode: Policy mode (Required). Options: enterprise_mode, compliance_mode,
                min_protected_period: Minimum retention period (Required, 0~36817920, 0 = indefinite),
                min_protected_period_unit: Minimum retention unit (Required). Options: day, year, month, hour, minute,
                max_protected_period: Maximum retention period (Required, 0~36817920, 0 = indefinite),
                max_protected_period_unit: Maximum retention unit (Required). Options: day, year, month, hour, minute, infinite,
                def_protected_period: Default retention period (Required, 0~36817920, 0 = indefinite),
                def_protected_period_unit: Default retention unit (Required). Options: day, year, month, hour, minute, infinite,
                auto_lock_enabled: Auto-lock switch (Optional, default false; auto-locks files unchanged within specified time),
                auto_lock_time: Auto-lock time (Optional, 1~64800; day:1~45, hour:1~1080, minute:1~64800),
                auto_lock_unit: Auto-lock time unit (Optional). Options: day, minute, hour,
                legal_hold_modify: Legal hold file modification permission (Optional, default false),
             }
        unix_permissions: Dtree directory permissions, regex [0-7]{3}, e.g. 755.
        task_remarks: Async task remark, 0~1024 characters

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/fileservice/v1/dtrees"

    if not storage_id or not create_dtrees_param:
        raise ValueError("storage_id and create_dtrees_param are required")

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
    """
    Batch delete Dtree.

    Args:
        client: DME API client
        dtree_ids: Dtree ID list to delete (Required, List[string])
        task_remarks: Async task remark (Optional, string, max 1024 characters)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/fileservice/v1/dtrees/delete"

    if not dtree_ids or len(dtree_ids) == 0:
        raise ValueError("dtree_ids is required")

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
    """
    Modify Dtree

    Args:
        client: DME API client
        dtree_id: Dtree ID
        name: Dtree name
        quota_switch: Quota switch, true/false
        security_mode: Security mode, mixed/native/ntfs/unix
        nas_locking_policy: NAS locking policy, mandatory/advisory/unknown
        unix_permissions: Dtree directory permissions, e.g. 755
        task_remarks: Async task remark

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
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
    """
    查询 NFS 共享列表

    Args:
        client: DME API 客户端
        id_in_storage: NFS ID on storage (Optional), 1~256 characters
        name: Share name (Optional), 1~256 characters, supports fuzzy search
        share_path: Share path (Optional), 1~256 characters, supports fuzzy search
        exact_share_path: Exact NFS share path (Optional), 1~1024 characters; takes precedence over share_path when both are specified
        device_name: Storage device name (Optional), 1~256 characters, supports fuzzy search
        manufacturer: Storage device vendor (Optional). Options: huawei, third_part
        storage_id: Storage device ID (Optional), 1~64 characters
        tier_name: Service level name (Optional), 1~256 characters, supports fuzzy search
        owning_dtree_name: Dtree name (Optional), 1~256 characters, supports fuzzy search
        fs_name: Filesystem name (Optional), 1~256 characters, supports fuzzy search
        fs_id: Filesystem ID (Optional), 1~64 characters
        owning_dtree_id: Dtree ID (Optional), 1~256 characters
        vstore_name: NFS share vStore name (Optional), 1~256 characters, supports fuzzy search
        page_no: Page number (Optional), min 1, default 1
        page_size: Items per page (Optional), 1~1000, default 20
        sort_key: Sort field (Optional). Options: name, id_in_storage
        sort_dir: Sort direction (Optional). Options: asc (ascending), desc (descending), default asc
        support_provisioning: Supports provisioning (Optional), true/false
        namespace_id: Namespace ID (Optional), 1~64 characters, OceanStor Pacific series only
        namespace_name: Namespace name (Optional), 1~256 characters, supports fuzzy search, OceanStor Pacific series only
        dc_id: Data center ID (Optional), 1~128 characters
        dc_name: Data center name (Optional), 1~256 characters
        zone_id: Zone ID (Optional), 1~64 characters
        zone_name: Zone name (Optional), 1~256 characters, supports fuzzy search
        zone_ip: Zone management IP (Optional), 0~255 characters
        scope: Resource scope (Optional). Options: local_scale, global_scale

    Returns:
        {
            total: Total NFS shares (integer),
            nfs_shares: NFS share list。参数格式如下：[{
                id: Share ID (string),
                name: Share name (string),
                path: Path (string),
                fs_id: Filesystem ID (string),
            }, ...],
        }
    """
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
    """
    Query NFS share details

    Args:
        client: DME API client
        nfs_share_id: NFS share ID

    Returns:
        {
            id: Share ID (string),
            name: Share name (string),
            path: Path (string),
            fs_id: Filesystem ID (string),
            export_ip: Export IP (string),
        }
    """
    url = "/rest/fileservice/v1/nfs-shares/{nfs_share_id}"

    if not nfs_share_id:
        raise ValueError("nfs_share_id is required")

    response = client.get(url, params={"nfs_share_id": nfs_share_id})
    return response


def nfs_share_create(client: DMEAPIClient, create_nfs_share_param: dict,
                     task_remarks: str = None) -> dict:
    """
    Create NFS share

    Args:
        client: DME API client
        create_nfs_share_param: NFS share creation parameters。参数格式如下：{
                name: NFS share alias (Optional),
                description: Description (Optional),
                share_path: Share path (Required),
                character_encoding: Character encoding (Optional),
                audit_items: Audit event list (Optional)。参数格式如下：[{
                        audititem: Audit event type. Options: none, all, open, create, read, write, close, delete, rename, get_security, set_security, get_attr, set_attr,
                     }, ...],
                show_snapshot_enable: Show snapshot (Optional). Options: true, false,
                nfs_share_client_addition: NFS share client permissions (Optional)。参数格式如下：[{
                        name: Client IP, hostname, or netgroup name (Required, 1~255 chars; netgroup starts with @),
                        permission: Permission (Required). Options: read, read_and_write, no_permission, read_and_write_not_del_rename,
                        accesskrb5: krb5 permission (Optional). Options: read, read_and_write, no_permission, read_and_write_not_del_rename,
                        accesskrb5i: krb5i permission (Optional). Options: read, read_and_write, no_permission, read_and_write_not_del_rename,
                        accesskrb5p: krb5p permission (Optional). Options: read, read_and_write, no_permission, read_and_write_not_del_rename,
                        write_mode: Write mode (Optional). Options: synchronization, asynchronization,
                        permission_constraint: Permission constraint (Required). Options: all_squash, no_all_squash,
                        root_permission_constraint: Root permission constraint (Required). Options: root_squash, no_root_squash,
                        source_port_verification: Source port verification (Optional). Options: secure, insecure,
                        anonymous_user_id: 匿名用户ID (可选),
                        access_protocol: 访问协议 (可选)。可选值：nfsv3_and_nfsv4 (NFSv3和NFSv4), nfsv3 (仅NFSv3), nfsv4 (仅NFSv4),
                     }, ...],
                file_name_extension_filters: 文件扩展名过滤规则列表 (可选)。参数格式如下：[{
                        file_name_ex_id_in_storage: 规则在存储上的ID (可选, 1~64字符, 变更已添加规则时必填),
                        file_name_extension: 文件扩展名 (必选, 1~127字符, 支持通配符?和*, *只能位于最后一个字符),
                        rule_type: 规则允许/拒绝 (可选, 默认reject)。可选值：reject, permit,
                        fileoperations: 操作类型列表 (可选)。可选值：close, create, create_dir, delete, delete_dir, getattr, link, lookup, open, read, write, rename, rename_dir, setattr, symlink,
                     }, ...],
                fs_id: 文件系统的id (与namespace_id互斥),
                namespace_id: 命名空间的id (与fs_id互斥),
             }
        task_remarks: 异步任务备注信息

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
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
    """
    修改指定 NFS 共享

    Args:
        client: DME API 客户端
        nfs_share_id: NFS 共享 ID
        description: 描述信息
        character_encoding: 字符编码，可选值：utf-8, zh, gbk 等
        audit_items: 审计事件列表 (可选)。参数格式如下：[{
                audititem: 审计事件类型。可选值：none (无操作), all (所有操作), open (打开), create (创建), read (读), write (写), close (关闭), delete (删除), rename (重命名), get_security (获取安全属性), set_security (设置安全属性), get_attr (获取属性), set_attr (设置属性),
             }, ...]
        show_snapshot_enable: 是否显示快照
        nfs_share_client_addition: 需要新增的 NFS 共享客户端列表 (可选)。参数格式如下：[{
                name: 客户端IP或主机名或网络组名 (必选, 1~255字符),
                permission: 权限 (必选)。可选值：read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5: krb5权限 (可选)。可选值：read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5i: krb5i权限 (可选)。可选值：read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5p: krb5p权限 (可选)。可选值：read, read_and_write, no_permission, read_and_write_not_del_rename,
                write_mode: 写入模式 (可选)。可选值：synchronization (同步), asynchronization (异步),
                permission_constraint: 权限限制 (必选)。可选值：all_squash, no_all_squash,
                root_permission_constraint: root权限限制 (必选)。可选值：root_squash, no_root_squash,
                source_port_verification: 源端口校验限制 (可选)。可选值：secure (安全), insecure (不安全),
                anonymous_user_id: 匿名用户ID (可选, 0~4294967294),
             }, ...]
        nfs_share_client_modification: 需要修改的 NFS 共享客户端列表 (可选)。参数格式如下：[{
                nfs_share_client_id_in_storage: 客户端在存储上的ID (必选, 1~32字符),
                permission: 权限 (必选)。可选值：read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5: krb5权限 (可选)。可选值：read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5i: krb5i权限 (可选)。可选值：read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5p: krb5p权限 (可选)。可选值：read, read_and_write, no_permission, read_and_write_not_del_rename,
                write_mode: 写入模式 (可选)。可选值：synchronization (同步), asynchronization (异步),
                permission_constraint: 权限限制 (必选)。可选值：all_squash, no_all_squash,
                root_permission_constraint: root权限限制 (必选)。可选值：root_squash, no_root_squash,
                source_port_verification: 源端口校验限制 (可选)。可选值：secure (安全), insecure (不安全),
                anonymous_user_id: 匿名用户ID (可选, 0~4294967294),
             }, ...]
        nfs_share_client_deletion: 需要删除的 NFS 共享客户端列表 (可选)。参数格式如下：[{
                nfs_share_client_id_in_storage: 客户端在存储上的ID (必选, 1~32字符),
                name: 客户端IP或主机名或网络组名 (可选, 1~32000字符),
             }, ...]
        file_name_ex_filters: 扩展名过滤规则列表 (可选)。参数格式如下：[{
                update_type: 变更类型 (可选, 默认add)。可选值：add (新增), delete (删除), modify (修改),
                param: 扩展名过滤规则。属性格式如下：{
                        file_name_ex_id_in_storage: 规则在存储上的ID (可选, 1~64字符, 修改时必填),
                        file_name_extension: 文件扩展名 (必选, 1~127字符, 支持通配符?和*, *只能位于最后),
                        rule_type: 规则允许/拒绝 (可选, 默认reject)。可选值：reject (拒绝), permit (允许),
                        fileoperations: 操作类型列表 (可选)。可选值：close, create, create_dir, delete, delete_dir, getattr, link, lookup, open, read, write, rename, rename_dir, setattr, symlink,
                }
             }, ...]
        task_remarks: 异步任务备注信息

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
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
    """
    批量删除 NFS 共享

    Args:
        client: DME API 客户端
        nfs_share_ids: 待删除 NFS 共享 ID 列表
        task_remarks: 异步任务备注信息

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
    url = "/rest/fileservice/v1/nfs-shares/delete"

    payload = {
        'nfs_share_ids': nfs_share_ids
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


# ============================================================================
# CIFS share subtopic functions
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
    """
    Batch query CIFS shares

    Args:
        client: DME API client
        raw_id: CIFS share ID on storage device (Optional), 1~256 characters
        name: CIFS share name (Optional), 1~256 characters, supports fuzzy search
        share_path: CIFS share path (Optional), 1~512 characters, supports fuzzy search
        exact_share_path: Exact CIFS share path (Optional), 1~1024 characters; takes precedence over share_path
        fs_id: Filesystem ID (Optional), 1~64 characters
        fs_name: Filesystem name (Optional), 1~256 characters, supports fuzzy search
        dtree_id: Dtree ID (Optional), 1~64 characters
        dtree_name: Dtree name (Optional), 1~256 characters, supports fuzzy search
        storage_id: Storage device ID (Optional), 1~64 characters
        storage_name: Storage device name (Optional), 1~256 characters, supports fuzzy search
        vstore_raw_id: vStore ID on storage device (Optional), 1~256 characters
        vstore_name: vStore name (Optional), 1~256 characters, supports fuzzy search
        manufacturer: Storage device vendor (Optional). Options: huawei, third_party
        op_lock_enabled: Oplock enabled (Optional), true/false
        notify_enabled: Notify enabled (Optional), true/false
        offline_file_modes: Offline cache mode list (Optional), List<OfflineFileMode> type, max array members 4。参数格式如下：[{
                        mode: Offline cache mode (Optional). Options: none, manual, documents, programs, default manual,
        },...]
        file_extension_filter_enabled: File extension filter enabled (Optional), true/false
        abe_enabled: ABE enabled (Optional), true/false
        page_no: Page number (Optional), 1~10000000, default 1
        page_size: Items per page (Optional), 1~1000, default 10
        sort_key: Sort field (Optional). Options: name, raw_id
        sort_dir: Sort direction (Optional). Options: asc (ascending), desc (descending), default asc
        namespace_id: Namespace ID (Optional), 1~64 characters, OceanStor Pacific series only
        namespace_name: Namespace name (Optional), 1~256 characters, supports fuzzy search, OceanStor Pacific series only
        support_provisioning: Supports provisioning (Optional), true/false
        dc_id: Data center ID (Optional), 1~128 characters
        dc_name: Data center name (Optional), 1~256 characters

    Returns:
        CIFS share list
    """
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
    """
    Query CIFS share details

    Args:
        client: DME API client
        cifs_share_id: CIFS share ID

    Returns:
        CIFS share details
    """
    url = "/rest/fileservice/v1/cifs-shares/{cifs_share_id}"

    response = client.get(url, params={"cifs_share_id": cifs_share_id})
    return response


def cifs_share_create(client: DMEAPIClient, create_cifs_param: dict, fs_id: str = None,
                namespace_id: str = None, task_remarks: str = None) -> dict:
    """
    Create a single CIFS share

    Args:
        client: DME API client
        create_cifs_param: CIFS share creation parameters。参数格式如下：{
                name: Share name (Required),
                description: Description (Optional),
                share_path: Share path (Required),
                op_lock_enabled: Oplock switch (Optional),
                notify_enabled: Notify switch (Optional),
                ca_enabled: Failover continuous availability switch (Optional),
                offline_file_mode: Offline cache mode (Optional). Options: none, manual, documents, programs,
                ip_control_enabled: IP access control switch (Optional),
                abe_enabled: ABE switch (Optional),
                audititem_list: Audit event list (Optional)。参数格式如下：[{
                        audititem: Audit event type (default none). Options: none, all, open, create, read, write, close, delete, rename, get_security, set_security, get_attr, set_attr, get_xattr, set_xattr,
                     }, ...],
                apply_default_acl: Apply default ACL (Optional),
                file_extension_filter_enabled: File extension filter enabled (Optional),
                show_previous_versions_enabled: Show previous versions enabled (Optional),
                show_snapshot_enabled: Show snapshot enabled (Optional),
                user_and_user_group_info: User and user group list (Optional)。参数格式如下：[{
                        user_or_user_group_id_in_storage: 用户或用户组在存储上的id (可选, 1~64字符, 变更时必填),
                        user_or_user_group_name: 用户名或用户组名 (可选, 1~255字符; 用户组名称加前缀@),
                        domain_type: 域类型 (可选, 默认local)。可选值：ad_domain, ldap_domain, local, nis_domain,
                        permission: 权限 (可选, 默认read)。可选值：read, full_control, forbidden, read_and_write, read_and_write_not_del_rename,
                     }, ...],
                ip_addresses_and_segments: IP地址和IP地址段列表 (可选)。参数格式如下：[{
                        ip_or_segments_id_in_storage: IP地址(段)在存储上的ID (可选, 1~64字符, 变更时必填),
                        ip_addresses_or_segments: IP地址(段) (可选, 1~128字符, 最多32条),
                     }, ...],
                file_name_extension_filters: 文件扩展名过滤规则列表 (可选)。参数格式如下：[{
                        file_name_ex_id_in_storage: 规则在存储上的ID (可选, 1~64字符, 变更已添加规则时必填),
                        file_name_extension: 文件扩展名 (必选, 1~127字符, 支持通配符?和*),
                        rule_type: 规则类型 (可选, 默认reject)。可选值：reject, permit,
                        fileoperations: 操作类型列表 (可选),
                     }, ...],
                smb3_encryption_enable: 是否开启SMB3加密功能 (可选),
                unencrypted_access: 是否允许未加密客户端访问 (可选),
                enable_lease: 是否开启租约锁定开关 (可选),
             }
        fs_id: 文件系统的 ID，与 namespace_id 互斥
        namespace_id: 命名空间的 ID，与 fs_id 互斥
        task_remarks: 异步任务备注信息

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
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
    """
    修改指定 CIFS 共享

    Args:
        client: DME API 客户端
        cifs_share_id: CIFS 共享 ID
        description: 描述信息，最多 255 个字符
        op_lock_enabled: Oplock 功能开关
        notify_enabled: Notify 功能开关
        ca_enabled: Failover 连续可用特性开关
        offline_file_mode: 离线缓存模式，none/manual/documents/programs
        ip_control_enabled: IP 访问控制特性开关
        abe_enabled: ABE 功能开关
        audititem_list: 支持审计的事件列表 (可选)。参数格式如下：[{
                audititem: 审计事件类型 (默认none)。可选值：none, all, open, create, read, write, close, delete, rename, get_security, set_security, get_attr, set_attr, get_xattr, set_xattr,
             }, ...]
        apply_default_acl: 是否添加默认 ACL
        file_extension_filter_enabled: 是否开启文件扩展名过滤特性
        show_previous_versions_enabled: 是否开启显示以前的版本的功能
        show_snapshot_enabled: 是否开启显示 Snapshot 的功能
        user_and_user_group_info: 用户和用户组列表 (可选)。参数格式如下：[{
                update_type: 变更类型 (可选, 默认add)。可选值：add (新增), delete (删除), modify (修改),
                param: 用户和用户组信息对象 (可选)。属性格式如下：{
                        user_or_user_group_id_in_storage: 用户或用户组在存储上的id (可选, 1~64字符, 变更时必填),
                        user_or_user_group_name: 用户名或用户组名 (可选, 1~255字符; 用户组名称加前缀@),
                        domain_type: 域类型 (可选, 默认local)。可选值：ad_domain, ldap_domain, local, nis_domain,
                        permission: 权限 (可选, 默认read)。可选值：read, full_control, forbidden, read_and_write, read_and_write_not_del_rename,
                }
             }, ...]
        ip_and_segments: IP地址和IP地址段列表 (可选)。参数格式如下：[{
                update_type: 变更类型 (可选, 默认add)。可选值：add (新增), delete (删除), modify (修改),
                param: IP地址和IP地址段信息对象 (可选)。属性格式如下：{
                        ip_or_segments_id_in_storage: IP地址(段)在存储上的ID (可选, 1~64字符, 变更时必填),
                        ip_addresses_or_segments: IP地址(段) (可选, 1~128字符, 最多32条),
                }
             }, ...]
        file_name_ex_filters: 扩展名过滤规则列表 (可选)。参数格式如下：[{
                update_type: 变更类型 (可选, 默认add)。可选值：add (新增), delete (删除), modify (修改),
                param: 扩展名过滤规则对象 (可选)。属性格式如下：{
                        file_name_ex_id_in_storage: 规则在存储上的ID (可选, 1~64字符, 变更已添加规则时必填),
                        file_name_extension: 文件扩展名 (必选, 1~127字符, 支持通配符?和*, *只能位于最后一个字符),
                        rule_type: 规则类型 (可选, 默认reject)。可选值：reject (拒绝), permit (允许),
                        fileoperations: 操作类型列表 (可选, 最多100个),
                }
             }, ...]
        task_remarks: 异步任务备注信息，0~1024 个字符
        smb3_encryption_enable: 是否开启 SMB3 加密功能
        unencrypted_access: 是否允许未加密客户端访问
        enable_lease: 是否开启租约锁定开关

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
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
    """
    Batch delete CIFS shares

    Args:
        client: DME API client
        cifs_share_ids: List of CIFS share IDs to delete
        task_remarks: Async task remark

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
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
    """
    Query CIFS share permission list

    Query user/group, IP address/segment, and file extension filter rules for a CIFS share.

    Args:
        client: DME API client
        cifs_share_id: CIFS share ID
        type: Permission type (Optional). Options: user (user/group), ip (IP address/segment), file (file extension filter);
              returns all types when not specified

        user_filter: User permission filter (Optional, dict type, effective when type=user)。参数格式如下：{
                user_or_user_group_name: User/group name (Optional), 1~256 characters,
                domain_type: Domain type (Optional). Options: ad_domain, ldap_domain, local, nis_domain,
                permissions: Permission filter list (Optional), List<Permission> type, max array members 4。参数格式如下：[{
                        permission: Permission (Optional). Options: read, full_control, forbidden, read_and_write, read_and_write_not_del_rename. Default read,
                },...],
                user_or_user_group_raw_id: User/group ID on storage device (Optional), 1~256 characters,
        }

        ip_filter: IP permission filter (Optional, dict type, effective when type=ip)。参数格式如下：{
                ip_addresses_or_segments: IP address/segment (Optional), 1~256 characters,
                ip_or_segments_raw_id: IP address/segment ID on storage device (Optional), 1~256 characters,
        }

        file_filter: File extension filter (Optional, dict type, effective when type=file)。参数格式如下：{
                rule_type: File extension type filter (Optional). Options: reject, permit,
                file_name_extension: File extension name filter (Optional), 1~256 characters,
                file_extension_name_raw_id: File extension filter rule ID on storage (Optional), 1~256 characters,
        }

        # Common pagination and sort parameters
        sort_key: Sort field (Optional). Options: raw_id, name
        sort_dir: Sort direction (Optional). Options: asc (ascending), desc (descending), default asc
        page_no: Page number (Optional), 1~10000000, default 1
        page_size: Items per page (Optional), 1~1000, default 10

    Returns:
        Permission list
    """
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
        response = client.post(url, body=payload)
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
        response = client.post(url, body=payload)
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
        response = client.post(url, body=payload)
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
# DataTurbo share subtopic functions
# ============================================================================

def dataturbo_share_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 10,
                   raw_id: str = None, share_path: str = None, fs_id: str = None,
                   fs_name: str = None, dtree_id: str = None, dtree_name: str = None,
                   vstore_id: str = None, vstore_raw_id: str = None, vstore_name: str = None,
                   storage_id: str = None, storage_name: str = None, zone_id: str = None,
                   zone_name: str = None, scope: str = None, sort_key: str = None,
                   sort_dir: str = None) -> dict:
    """
    查询 DataTurbo 共享列表

    Args:
        client: DME API 客户端
        page_no: 分页页码（可选），1~10000000，默认 1
        page_size: 每页数据条数（可选），1~1000，默认 10
        raw_id: DataTurbo 共享在设备上 ID（可选），1~1024 个字符，精确查询
        share_path: 共享路径（可选），1~1024 个字符，支持模糊搜索
        fs_id: DataTurbo 共享所属文件系统 ID（可选），1~64 个字符，精确查询
        fs_name: DataTurbo 共享所属文件系统名称（可选），1~256 个字符，支持模糊搜索
        dtree_id: DataTurbo 共享所属 Dtree 的 ID（可选），32 个字符，正则 ^[A-F0-9]{32}$，精确查询
        dtree_name: DataTurbo 共享所属 Dtree 名称（可选），1~256 个字符，支持模糊查询
        vstore_id: DataTurbo 共享所属租户 ID（可选），1~64 个字符，精确查询
        vstore_raw_id: DataTurbo 共享所属租户 RAW ID（可选），1~64 个字符，精确查询
        vstore_name: DataTurbo 共享所属租户名称（可选），1~256 个字符，支持模糊搜索
        storage_id: DataTurbo 共享所属存储设备 ID（可选），1~64 个字符，精确查询
        storage_name: DataTurbo 共享所属存储设备名称（可选），1~256 个字符，支持模糊搜索
        zone_id: DataTurbo 共享所属 zone ID（可选），1~64 个字符，精确查询
        zone_name: DataTurbo 共享所属 zone 名称（可选），1~256 个字符，支持模糊搜索
        scope: 资源所属范围（可选），可选值：local_scale（本地）、global_scale（全局）
        sort_key: 排序字段（可选），可选值：raw_id（在设备上 ID）
        sort_dir: 排序方向（可选），可选值：asc（升序）、desc（降序），默认 asc

    Returns:
        DataTurbo 共享列表
    """
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
    """
    查询指定 DataTurbo 共享详情

    Args:
        client: DME API 客户端
        dataturbo_share_id: DataTurbo 共享 ID

    Returns:
        DataTurbo 共享详细信息
    """
    url = "/rest/fileservice/v1/dpc-shares/{dataturbo_share_id}"

    response = client.get(url, params={"dataturbo_share_id": dataturbo_share_id})
    return response


def dataturbo_share_create(client: DMEAPIClient, charset: str, fs_id: str = None,
                     dtree_id: str = None, description: str = None,
                     dataturbo_share_auth: list = None, task_remarks: str = None) -> dict:
    """
    创建 DataTurbo 共享

    Args:
        client: DME API 客户端
        charset: 字符集编码，固定值 UTF_8
        fs_id: 需共享的文件系统的 ID，与 dtree_id 互斥，必传其中一个
        dtree_id: 需共享的 Dtree 的 ID，与 fs_id 互斥，必传其中一个
        description: DataTurbo 共享描述
        dataturbo_share_auth: DataTurbo 管理员列表 (可选)。参数格式如下：[{
                dpc_user_id: DataTurbo管理员ID (必选, 1~64个字符),
                permission: DataTurbo管理员权限 (必选, 固定值read_and_write),
             }, ...]
        task_remarks: 异步任务备注信息

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
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
    """
    修改指定 DataTurbo 共享

    Args:
        client: DME API 客户端
        dataturbo_share_id: DataTurbo 共享 ID
        description: DataTurbo 共享描述
        dataturbo_share_auth_addition: 要增加的 DataTurbo 管理员列表 (可选)。参数格式如下：[{
                dpc_user_id: DataTurbo管理员ID (必选, 0~64个字符),
                permission: DataTurbo管理员权限 (必选, 固定值read_and_write),
             }, ...]
        dataturbo_share_auth_deletion: 要删除的 DataTurbo 管理员 ID 列表
        task_remarks: 异步任务备注信息

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
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
    """
    批量删除 DataTurbo 共享

    Args:
        client: DME API 客户端
        dataturbo_share_ids: DataTurbo 共享 ID 列表
        task_remarks: 异步任务备注信息

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
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
    """
    查询 DataTurbo 共享管理员权限列表

    Args:
        client: DME API 客户端
        dataturbo_share_id: DataTurbo 共享 ID
        page_no: 分页页码（可选），1~10000000，默认 1
        page_size: 每页数据条数（可选），1~1000，默认 10
        user_id: DataTurbo 管理员 ID（可选），1~64 个字符，精确查询
        user_name: DataTurbo 管理员名称（可选），1~256 个字符，支持模糊搜索
        permission: DataTurbo 管理员权限（可选），可选值：read_and_write（读写）

    Returns:
        DataTurbo 共享管理员权限列表
    """
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
    """
    查询配额列表

    Args:
        client: DME API 客户端
        page_no: 分页查询页码（可选），最小值 1，默认 1
        page_size: 每页数据条数（可选），1~1000，默认 20
        ids: 配额的 ID 列表（可选），List<string> 类型，数组最大成员个数 100
        raw_ids: 配额在存储设备上的 ID 列表（可选），List<string> 类型，0~1024 个字符，数组最大成员个数 100
        quota_type: 配额类型（可选），可选值：directory_quota（目录配额）、user_quota（用户配额）、user_group_quota（用户组配额）
        parent_type: 配额所属父对象类型（可选），0~32 个字符；可选值：filesystem（文件系统或者命名空间，OceanStor Pacific 设备称为命名空间，其余设备称为文件系统）、qtree（Quota Tree 或者 Dtree，OceanStor V3/V5 设备称为 Quota Tree，其余设备称为 Dtree）
        parent_raw_id: 配额所属父对象在存储设备上的 ID（可选），0~256 个字符，支持精确匹配；当 parent_type 为 filesystem 时是文件系统或命名空间在存储设备上的 ID，当 parent_type 为 qtree 时是 Quota Tree 或 Dtree 在存储设备上的 ID
        owner_name: 配额关联的用户或者用户组名称（可选），0~256 个字符，支持模糊查询
        vstore_id: 配额所属租户的 ID（可选），0~64 个字符
        vstore_raw_id: 配额所属租户存储设备上的 ID（可选），0~256 个字符，支持精确匹配
        storage_id: 配额所属存储设备的 ID（可选），0~64 个字符
        sort_key: 查询的排序字段（可选），可选值：id、space_hard_used_rate（空间使用率）、file_hard_used_rate（文件使用率），默认 id
        sort_dir: 排序方向（可选），可选值：asc（升序）、desc（降序），默认 asc
        zone_id: Zone id（可选），0~64 个字符，仅 OceanStor A800 存储支持

    Returns:
        配额列表
    """
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
    """
    查询指定配额详情

    Args:
        client: DME API 客户端
        quota_id: 配额 ID

    Returns:
        配额详细信息
    """
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
    """
    创建配额

    Args:
        client: DME API 客户端
        space_soft_quota: 空间软配额（可选），单位 Byte，默认 -1（字段无效）；当空间硬配额和空间软配额均有效时，空间硬配额需大于空间软配额；OceanStor V5 设备时此字段必须为 1048576 的整数倍
        space_hard_quota: 空间硬配额（可选），单位 Byte，默认 -1（字段无效）；当空间硬配额和空间软配额均有效时，空间硬配额需大于空间软配额；OceanStor V5 设备时此字段必须为 1048576 的整数倍
        space_advisory_quota: 空间建议配额（可选），单位 Byte，默认 -1（字段无效）；仅 OceanStor Pacific 设备支持；当空间建议配额和空间硬配额或空间软配额均有效时，空间建议配额需小于空间硬配额或空间软配额
        file_soft_quota: 文件数软配额（可选），默认 -1（字段无效）；当文件数硬配额和文件数软配额均有效时，文件数硬配额需大于文件数软配额
        file_hard_quota: 文件数硬配额（可选），默认 -1（字段无效）；当文件数硬配额和文件数软配额均有效时，文件数硬配额需大于文件数软配额
        file_advisory_quota: 文件数建议配额（可选），默认 -1（字段无效）；仅 OceanStor Pacific 设备支持；当文件数建议配额和文件数硬配额或文件数软配额均有效时，文件数建议配额需小于文件数硬配额或文件数软配额
        snap_space_switch: 是否统计快照空间（可选），默认 false；true：统计快照空间；false：不统计快照空间；仅 OceanStor Pacific 设备支持
        soft_grace_time: 超限时间（可选），0~4294967294，单位（天）；表示软配超限多长时间后自动转硬超限；不传或取值 0 时达到软配额只告警；仅 OceanStor Pacific 支持
        parent_id: 父资源 ID（必填），1~64 个字符
        parent_type: 父资源类型（必填），可选值：filesystem（文件系统）、dtree（dtree，存储集群不支持）、namespace（命名空间）
        quota_type: 配额类型（必填），可选值：directory_quota（目录配额）、user_quota（用户配额）、user_group_quota（用户组配额）
        quota_owner: 配额用户（条件必传），QuotaOwner 对象。参数格式如下：{
                        name: 用户（组）名称（必填），1~64 个字符，* 表示所有用户（组）,
                        type: 用户（组）类型（必填），当 quota_type 为 user_quota 时可选值：unix_local_user（unix 本地用户）、domain_user（域用户）、windows_user（windows 用户）；当 quota_type 为 user_group_quota 时可选值：unix_local_user_group（unix 本地用户组）、domain_user_group（域用户组）、windows_user_group（windows 用户组）,
                        domain_type: 域用户类型（条件必传），当 type 为 domain_user 或 domain_user_group 时必传；可选值：local（本地）、ad_domain（AD 域）、ldap_domain（LDAP 域）、nis_domain（NIS 域）；OceanStor Pacific、OceanStor Dorado V6、OceanProtect 支持该字段,
        }
        dir_quota_target: 目录配额作用目标（可选），可选值：dtree（模板目录配额，作用于当前文件系统下的所有 Dtree）、filesystem（根目录配额，作用于当前文件系统）；当父资源类型为 filesystem 且配额类型为 directory_quota 时有效
        task_remarks: 异步任务备注信息

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
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
    """
    更新指定配额

    Args:
        client: DME API 客户端
        quota_id: 配额 ID
        space_soft_quota: 空间软配额（可选），单位 Byte，-1 表示字段无效；当空间硬配额和空间软配额均有效时，空间硬配额需大于空间软配额
        space_hard_quota: 空间硬配额（可选），单位 Byte，-1 表示字段无效；当空间硬配额和空间软配额均有效时，空间硬配额需大于空间软配额
        space_advisory_quota: 空间建议配额（可选），单位 Byte，-1 表示字段无效；仅 OceanStor Pacific 设备支持；当空间建议配额和空间硬配额或空间软配额均有效时，空间建议配额需小于空间硬配额或空间软配额
        file_soft_quota: 文件数软配额（可选），-1 表示字段无效；当文件数硬配额和文件数软配额均有效时，文件数硬配额需大于文件数软配额
        file_hard_quota: 文件数硬配额（可选），-1 表示字段无效；当文件数硬配额和文件数软配额均有效时，文件数硬配额需大于文件数软配额
        file_advisory_quota: 文件数建议配额（可选），-1 表示字段无效；仅 OceanStor Pacific 设备支持；当文件数建议配额和文件数硬配额或文件数软配额均有效时，文件数建议配额需小于文件数硬配额或文件数软配额
        snap_space_switch: 是否统计快照空间（可选），true：统计快照空间；false：不统计快照空间；仅 OceanStor Pacific 设备支持
        soft_grace_time: 超限时间（可选），0~4294967294，单位（天）；表示软配超限多长时间后自动转硬超限；不下发或取值 0 时达到软配额只告警；仅 OceanStor Pacific 支持
        task_remarks: 异步任务备注信息

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
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
    """
    批量删除配额

    Args:
        client: DME API 客户端
        quota_ids: 待删除的配额 ID 列表
        task_remarks: 异步任务备注信息

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
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
    """
    批量查询文件系统

    Args:
        client: DME API 客户端
        page_no: 分页查询页码（可选），1~10000000
        page_size: 每页显示的数量（可选），1~1000，默认 100
        sort_dir: 指定排序方向（可选），可选值：asc（升序）、desc（降序）
        sort_key: 排序参数（可选），可选值：capacity, available_capacity, capacity_usage_ratio,
                  nfs_count, cifs_count, dpc_count, dtree_count, name, allocate_pool_quota,
                  fs_raw_id, create_time, total_capacity_in_byte, available_capacity_in_byte,
                  alloc_capacity_in_byte, protection_capacity_in_byte, max_file_count, used_file_count
        name: 文件系统名称（可选），1~256 个字符，与 fs_raw_id 互斥，支持模糊匹配
        is_associated_qos: 文件系统是否已关联 QoS（可选），true：是；false：否
        qos_id: QoS 策略 ID（可选），1~256 个字符
        storage_name: 文件系统所属设备名称（可选），1~256 个字符，与 storage_id 互斥，支持模糊匹配
        manufacturer: 存储设备厂商（可选），1~64 个字符；可选值：huawei（Huawei）、dell_emc（DELL EMC）、
                     fujitsu（FUJITSU）、hitachi（Hitachi）、hpe（HPE）、ibm（IBM）、netapp（NetApp）、
                     pure（PURE）、panji（Panji）、third_part（非华为存储设备）
        storage_pool_name: 文件系统所属存储池名称（可选），1~256 个字符，与 storage_pool_id 互斥，支持模糊匹配
        storage_pool_id: 存储池 ID（可选），1~255 个字符，与 storage_pool_name 互斥
        tier_name: 文件系统所属服务等级名称（可选），1~256 个字符，与 tier_id 互斥，支持模糊匹配
        tier_id: 服务等级 ID（可选），1~256 个字符，与 tier_name 互斥，精确匹配
        vstore_name: 文件系统所属 vStore 名称（可选），1~256 个字符，与 vstore_raw_id 互斥，支持模糊匹配
        vstore_raw_id: 文件系统所属租户在存储设备上的 ID（可选），1~64 个字符，与 vstore_name 互斥
        project_name: 文件系统所属业务群组名称（可选），1~256 个字符，与 project_id 互斥，支持模糊匹配
        project_id: 业务群组 ID（可选），1~256 个字符，与 project_name 互斥，精确匹配
        storage_id: 归属存储设备 ID（可选），1~256 个字符，与 storage_name 互斥，精确匹配
        fs_raw_id: 文件系统在设备上的 ID（可选），1~256 个字符，与 name 互斥
        health_status: 健康状态（可选），可选值：normal（正常）、faulty（故障）、unknown（未知）
        running_status: 运行状态（可选），可选值：online（在线）、offline（离线）、invalid（失效）、
                       initializing（初始化中）、unknown（未知）
        alloc_type: 文件系统分配类型（可选），可选值：thin（按需分配）、thick（固定分配）
        type: 文件系统类型（可选），可选值：normal（普通文件系统）、worm（worm文件系统）、
              migration（migration文件系统）、container（容器应用文件系统）、hash（哈希文件系统）、
              smart_mobility_internal（SmartMobility内部文件系统）
        protection: 保护状态（可选），可选值：protected（已保护）、not_protected（未保护）
        dc_id: 数据中心 ID（可选），1~128 个字符，正则 ^[_A-Fa-f0-9\\-]+$
        dc_name: 数据中心名称（可选），1~256 个字符
        zone_id: 所属 zone 的 ID（可选），1~256 个字符；仅 OceanStor A800 系列文件系统支持搜索，传入集群ID代表查询全局文件系统
        product_name: 文件系统所属设备产品名称（可选），1~256 个字符，支持模糊搜索
        description: 文件系统描述信息（可选），1~255 个字符
        tag_filters: 标签过滤列表（可选），List<TagFilters> 类型，数组最大成员个数 11。参数格式如下：[{
                        tag_ids: 标签 ID 列表（可选），数组最大成员个数 10，多个标签之间为或关系,
                        tag_type_id: 标签类型 ID（可选），正则 ^[a-fA-F0-9]{32}$,
                        operator: 过滤条件（必填），可选值：contain（包含）、not_contain（不包含）,
        },...]

    Returns:
        文件系统列表
    """
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
    """
    查询指定文件系统详情

    Args:
        client: DME API 客户端
        filesystem_id: 文件系统 ID

    Returns:
        文件系统详细信息
    """
    url = "/rest/fileservice/v1/filesystems/{filesystem_id}"

    response = client.get(url, params={"filesystem_id": filesystem_id})
    return response


def filesystem_delete(client: DMEAPIClient, filesystem_ids: list, task_remarks: str = None) -> dict:
    """
    批量删除文件系统

    Args:
        client: DME API 客户端
        filesystem_ids: 文件系统 ID 列表
        task_remarks: 异步任务备注信息（可选）

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }（异步任务）
    """
    url = "/rest/fileservice/v1/filesystems/delete"

    payload = {
        'file_system_ids': filesystem_ids
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def filesystem_batch_modify(client: DMEAPIClient, filesystems: list, task_remarks: str = None) -> dict:
    """
    批量修改文件系统

    仅支持修改名称。

    Args:
        client: DME API 客户端
        filesystems: 待修改的文件系统信息列表（必填），List<UpdateFileSystemInfo> 类型，数组最大成员个数 1000。参数格式如下：[{
                        file_system_id: 文件系统的唯一标识（必填），1~64 个字符,
                        name: 文件系统名称（必填），1~255 个字符；OceanStor Dorado V6、OceanStor、OceanProtect 系列只能包含字母、数字、"-"、"."和各国语言字符；OceanStor V3/V5 系列只能包含字母、数字和中文字符,
        },...]
        task_remarks: 异步任务备注信息（可选），0~1024 个字符

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
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
    """
    自定义创建文件系统

    Args:
        client: DME API 客户端
        storage_id: 存储设备 ID
        pool_raw_id: 存储池在指定存储设备上的 ID
        filesystem_specs: 文件系统规格列表。参数格式如下：[{
                name: 名称 (必选, 1~255字符),
                count: 数量 (必选, 1~500),
                start_suffix: 起始后缀编号 (可选, 0~9999),
                capacity: 容量GB (必选, 1~262144),
                description: 描述 (可选, 0~255字符),
             }, ...]
        vstore_id: 租户 ID（可选）
        zone_id: 所属 zone 的 ID（可选）
        task_remarks: 异步任务备注信息（可选）
        gfs_group_id: 全局数据空间的 ID（可选）
        automatic_update_time: 是否更新访问时间（可选）
        atime_update_mode: Atime 更新频率，hour/day/close（可选）
        schedule_name: 定时 HyperCDP 计划名称（可选）
        quota_switch: 是否启用配额（可选）
        vaai_switch: VAAI 开关（可选）
        initial_distribute_policy: 容量初始分配策略，auto/highest_perf/performance/capacity（可选）
        capacity_threshold: 总空间容量告警阈值 50-99（可选）
        tuning: 调优参数 (可选)。参数格式如下：{
                deduplication_enabled: 是否开启重复数据删除 (可选, 默认false)。可选值：true, false,
                compression_enabled: 是否开启数据压缩 (可选, 默认false)。可选值：true, false,
                block_size: 文件系统块大小KB (可选, 默认64)。可选值：4, 8, 16, 32, 64, 128,
                allocation_type: 分配类型 (可选, 默认thin)。可选值：thin, thick,
                qos_policy_id: QoS策略ID (可选),
                application_scenario: 应用场景 (可选, 默认user_defined)。可选值：database, VM, user_defined, container,
                workload_type_id: 应用类型id (可选, 1~32字符),
                dist_alg: 文件系统目录打散策略 (可选, 仅A800设备支持)。可选值：capacity_balance, subdirectory_round_robin,
                qos_policy: SmartQos策略参数信息 (可选)。属性格式如下：{
                        max_bandwidth: 最大带宽MB/s (可选, 1~999999999),
                        max_iops: 最大iops (可选, 1~999999999),
                        min_bandwidth: 最小带宽MB/s (可选, 1~999999999),
                        min_iops: 最小iops (可选, 1~999999999),
                        burst_band_width: 突发带宽MB/s (可选),
                        burst_iops: 突发IOPS (可选),
                        burst_time: 最大突发时间秒 (可选),
                        latency: 时延 (可选, 仅保护下限支持),
                        max_read_bandwidth: 最大读带宽MB/s (可选),
                        max_write_bandwidth: 最大写带宽MB/s (可选),
                        burst_read_band_width: 突发读带宽MB/s (可选),
                        burst_write_band_width: 突发写带宽MB/s (可选),
                        max_read_iops: 最大读iops (可选),
                        max_write_iops: 最大写iops (可选),
                        burst_read_iops: 突发读iops (可选),
                        burst_write_iops: 突发写iops (可选),
                        schedule_policy: 调度策略 (可选)。可选值：once, daily, weekly,
                        schedule_start_date: 生效开始日期 (可选, 格式yyyy-MM-dd),
                        start_time: 生效开始时间 (可选, 格式hh:mm),
                        duration: 生效持续时间秒 (可选, 1800~86400),
                        weekly_days: 周调度策略 (可选, 1~6对应周一到周六),
                        alarm_switch: 限高告警开关 (可选)。可选值：off, on,
                        alarm_level: 告警级别 (可选)。可选值：event, alarm,
                        alarm_threshold: 告警阈值% (可选, 0~100),
                        resume_threshold: 恢复阈值% (可选, 0~100),
                        storage_divice_id: 所属存储设备id (可选),
                        name: QoS名称 (可选),
                        description: 描述 (可选),
                        iotype: 策略类型 (可选)。可选值：2 (总上限), 3 (读写上限),
                        vstore_id: 所属租户id (可选),
                        vstore_name: 所属租户名称 (可选),
                        global_flag: 是否全局 (可选),
                }
             }
        create_cifs_share_param: 自动创建CIFS共享参数（可选）。格式参见动作帮助：nas cifs_share create
        create_nfs_share_param: 自动创建NFS共享参数（可选）。格式参见动作帮助：nas nfs_share create
        create_dpc_share_param: 自动创建DataTurbo共享参数（可选）。格式参见动作帮助：nas dataturbo_share create
        owning_controller: 归属控制器（可选），2~16个字符，格式如0A、1B
        snapshot_expired_enabled: 是否开启删除旧的只读快照（可选）。true/false，默认关闭
        checksum_enabled: 数据校验开关（可选）。true/false，默认开启
        ads_enabled: 是否开启交换数据流功能（可选）。true/false，默认开启
        security_mode: 安全模式（可选）。取值：mixed/native/ntfs/unix
        nas_locking_policy: NAS锁策略（可选）。取值：mandatory/advisory/unknown
        capacity_autonegotiation: 容量自适应参数 (可选)。参数格式如下：{
                capacity_self_adjusting_mode: 容量自动调整模式 (可选, 默认关闭)。可选值：grow_off (关闭), grow (自动扩容), grow_shrink (自动扩缩容),
                capacity_recycle_mode: 容量回收模式 (可选, 默认优先扩容)。可选值：expand_capacity (优先扩容), delete_snapshots (优先删除旧快照),
                auto_size_enable: 自动调整容量开关 (可选, 默认true)。可选值：true, false,
                auto_grow_threshold_percent: 自动扩容触发门限% (可选, 2~99, 默认85),
                auto_shrink_threshold_percent: 自动缩容触发门限% (可选, 1~98, 默认50),
                max_auto_size: 自动扩容上限GB (可选, 1~33554432, 默认33554432),
                min_auto_size: 自动缩容下限GB (可选, 1~33554432, 默认33554432),
                auto_size_increment: 自动扩缩容单次变化量MB (可选, 64~102400, 默认1024),
             }
        worm: 文件系统Worm参数 (可选)。参数格式如下：{
                type: WORM保护模式 (可选)。可选值：none_mode (无默认策略), enterprise_mode (企业遵从), compliance_mode (法规遵从), advance_mode (高安遵从), audit_log (审计日志), non_worm (非WORM),
                min_protect_period: 最小保护期 (可选, 默认0),
                min_protect_period_unit: 最小保护期单位 (可选, 默认year)。可选值：minute, hour, day, month, year,
                max_protect_period: 最大保护期 (可选, 0~4294967295, 默认70),
                max_protect_period_unit: 最大保护期单位 (可选, 默认year)。可选值：minute, hour, day, month, year,
                def_protect_period: 默认保护期 (可选, 不小于最小, 不大于最大, 默认70),
                def_protect_period_unit: 默认保护期单位 (可选, 默认year)。可选值：minute, hour, day, month, year,
                auto_lock: WORM自动锁定模式 (可选, 默认开启)。可选值：true, false,
                auto_lock_time: 自动锁定时间 (可选, 默认2),
                auto_lock_time_unit: 自动锁定时间单位 (可选, 默认hour)。可选值：minute, hour, day, month, year,
                auto_del: 自动删除模式 (可选, 默认关闭)。可选值：true, false,
                is_worm_audit_log_fs: WORM审计日志文件系统 (可选, 默认关闭)。可选值：true, false,
                worm_append_unit: WORM追加态文件保护粒度 (可选, 仅advance_mode支持)。可选值：256KB, 512KB, 1M,
             }
        snapshot_reserved_space_percentage: 快照预留空间百分比（可选），0~90
        periodic_snapshots_limit: 定时快照数量限制（可选），1~2048
        snapshot_dir_visible: 快照目录是否可见（可选）。true/false
        object_service_optimization: 对象服务优化（可选）。true/false
        case_sensitive: 大小写敏感模式（可选）。true/false
        audit_log_rules: 审计日志规则集合（可选），如：set_security、get_security、set_attr、get_attr等，最多100条
        unix_permissions: 文件系统目录权限（可选），格式如0755

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
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
    """
    查询可用的文件系统

    查询可用于配置增删特性的文件系统。当前仅支持可配置远程复制的文件系统。

    Args:
        client: DME API 客户端
        feature_type: 特性类型，当前仅支持 remote_replication（远程复制）
        local_storage_id: 本端存储设备 ID
        remote_storage_id: 远端存储设备 ID（当 feature_type 为 remote_replication 时必选）
        name: 本端文件系统名称，支持模糊搜索
        page_no: 分页查询页码，默认 1
        page_size: 每页显示的数量，默认 20
        sort_key: 排序字段，name（文件系统名称）或 capacity（文件系统容量）
        sort_dir: 排序方向，asc（升序）或 desc（降序）

    Returns:
        可用文件系统列表
    """
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
    """
    修改指定文件系统

    Args:
        client: DME API 客户端
        file_system_id: 文件系统唯一标识
        name: 文件系统名称，1~255个字符（可选）
        description: 描述信息，0~255个字符（可选）
        capacity: 文件系统容量，单位 GB，1~33554432（可选）
        capacity_threshold: 总空间容量告警阈值 50-99（可选）
        initial_distribute_policy: 容量初始分配策略，auto/highest_perf/performance/capacity（可选）
        automatic_update_time: 文件被读取后是否更新访问时间，true开启/false关闭（可选）
        atime_update_mode: Atime 更新频率，hour（每小时）/day（每天）/close（未启用）（可选）
        quota_switch: 是否启用配额，true启用/false不启用（可选）
        vaai_switch: VAAI 开关，启用后不能关闭，true启用/false未启用（可选）
        owning_controller: 归属控制器，2~16个字符（可选）
        snapshot_expired_enabled: 是否开启删除旧的只读快照，true开启/false关闭（可选）
        checksum_enabled: 数据校验开关，true开启/false关闭（可选）
        ads_enabled: 是否开启交换数据流功能，true开启/false关闭，开启后不允许关闭（可选）
        security_mode: 安全模式，mixed/native/ntfs/unix（可选）
        nas_locking_policy: NAS锁策略，mandatory（强制锁）/advisory（建议锁）/unknown（可选）
        snapshot_reserved_space_percentage: 快照预留空间百分比，0~90（可选）
        periodic_snapshots_limit: 定时快照数量限制，1~2048（可选）
        snapshot_dir_visible: 快照目录是否可见，true可见/false不可见（可选）
        tuning: 调优参数 (可选)。参数格式如下：{
                qos_policy: SmartQos策略参数信息 (UpdateFileSystemQosPolicy对象)。属性格式如下：{
                        max_bandwidth: 最大带宽MB/s (可选, 1~999999999; 与min_bandwidth/min_iops互斥, A800下不互斥),
                        max_iops: 最大IOPS (可选, 1~999999999; 与min_bandwidth/min_iops互斥, A800下不互斥),
                        min_bandwidth: 最小带宽MB/s (可选, 1~999999999; 与max_bandwidth/max_iops互斥, A800下不互斥),
                        min_iops: 最小IOPS (可选, 1~999999999; 与max_bandwidth/max_iops互斥, A800下不互斥),
                        burst_band_width: 突发带宽MB/s (可选, 1~999999999),
                        burst_iops: 突发IOPS (可选, 1~999999999),
                        burst_time: 最大突发时间秒 (可选, 1~999999999),
                        latency: 时延 (可选, 1~999999999; A800/Dorado V6可选500/1500单位us, V3/V5可自定义单位ms),
                        max_read_bandwidth: 最大读带宽MB/s (可选, 1~999999999; 仅读写上限策略有效),
                        max_write_bandwidth: 最大写带宽MB/s (可选, 1~999999999; 仅读写上限策略有效),
                        burst_read_band_width: 突发读带宽MB/s (可选, 1~999999999; 仅读写上限策略有效),
                        burst_write_band_width: 突发写带宽MB/s (可选, 1~999999999; 仅读写上限策略有效),
                        max_read_iops: 最大读IOPS (可选, 1~999999999; 仅读写上限策略有效),
                        max_write_iops: 最大写IOPS (可选, 1~999999999; 仅读写上限策略有效),
                        burst_read_iops: 突发读IOPS (可选, 1~999999999; 仅读写上限策略有效),
                        burst_write_iops: 突发写IOPS (可选, 1~999999999; 仅读写上限策略有效),
                        schedule_policy: 调度策略 (可选)。可选值：once, daily, weekly,
                        schedule_start_date: 生效开始日期 (可选, 格式yyyy-MM-dd, 0~64字符),
                        start_time: 生效开始时间 (可选, 格式hh:mm, 0~64字符),
                        duration: 生效持续时间秒 (可选, 1800~86400),
                        weekly_days: 周调度策略 (可选, 0-6对应周日到周六, 最多7个; schedule_policy为weekly时生效),
                        alarm_switch: 限高告警开关 (可选)。可选值：off, on,
                        alarm_level: 限高告警级别 (可选)。可选值：event (事件), alarm (告警),
                        alarm_threshold: 限高告警阈值% (可选, 0~100),
                        resume_threshold: 限高告警恢复阈值% (可选, 0~100),
                        storage_divice_id: 所属存储设备ID (可选, 1~64字符),
                        name: QoS名称 (可选, 1~255字符; A800下未使用),
                        description: QoS描述 (可选, 1~255字符; A800下未使用),
                        iotype: 策略类型 (可选)。可选值：2 (总性能上限), 3 (读写上限; 仅部分设备支持),
                        vstore_id: 所属租户ID (可选, 1~64字符; A800下未使用),
                        vstore_name: 所属租户名称 (可选, 1~64字符; A800下未使用),
                        global_flag: 是否全局 (可选; 当前版本只支持全局; A800下未使用),
                        qos_policy_id: QoS策略ID (可选, 0~64字符; 与除enabled外的其他参数互斥),
                        enabled: 是否启用QoSPolicy (可选, 默认false),
                },
                deduplication_enabled: 重复数据删除 (可选, 默认关闭),
                compression_enabled: 数据压缩 (可选, 默认关闭),
                allocation_type: 文件系统分配类型 (可选, 默认thin)。可选值：thin (精简), thick (厚),
             }
        capacity_autonegotiation: 容量自适应参数 (可选)。参数格式如下：{
                capacity_self_adjusting_mode: 容量自动调整模式 (可选, 默认关闭)。可选值：grow_off (关闭), grow (自动扩容), grow_shrink (自动扩缩容),
                capacity_recycle_mode: 容量回收模式 (可选, 默认优先扩容)。可选值：expand_capacity (优先扩容), delete_snapshots (优先删除旧快照),
                auto_size_enable: 自动调整容量开关 (可选, 默认打开)。可选值：true, false,
                auto_grow_threshold_percent: 自动扩容触发门限% (可选, 2~99, 默认85; 必须大于缩容触发门限),
                auto_shrink_threshold_percent: 自动缩容触发门限% (可选, 1~98, 默认50),
                max_auto_size: 自动扩容上限GB (可选, 1~33554432, 默认33554432; 必须大于等于缩容下限和文件系统容量),
                min_auto_size: 自动缩容下限GB (可选, 1~33554432, 默认33554432),
                auto_size_increment: 自动扩缩容单次变化量MB (可选, 64~102400, 默认1024),
             }
        worm: 文件系统Worm参数 (可选)。参数格式如下：{
                type: WORM保护遵从模式 (可选)。可选值：none_mode, enterprise_mode, compliance_mode, advance_mode, audit_log, non_worm,
                min_protect_period: 最小保护期 (可选, 0~4294967295, 默认0; 4294967295为无限期),
                min_protect_period_unit: 最小保护期单位 (可选, 默认year)。可选值：minute, hour, day, month, year,
                max_protect_period: 最大保护期 (可选, 1~4294967295, 默认70; 4294967295为无限期),
                max_protect_period_unit: 最大保护期单位 (可选, 默认year)。可选值：minute, hour, day, month, year,
                def_protect_period: 默认保护期 (可选, 0~4294967295, 默认70; 不小于最小且不大于最大),
                def_protect_period_unit: 默认保护期单位 (可选, 默认year)。可选值：minute, hour, day, month, year,
                auto_lock: WORM自动锁定模式 (可选, 默认开启; advance_mode不支持)。可选值：true, false,
                auto_lock_time: 自动锁定时间 (可选, 最小值1, 默认2),
                auto_lock_time_unit: 自动锁定时间单位 (可选, 默认hour)。可选值：minute, hour, day, month, year,
                auto_del: 自动删除模式 (可选, 默认关闭; advance_mode不支持)。可选值：true, false,
                is_worm_audit_log_fs: WORM审计日志文件系统 (可选, 默认关闭; 一个租户只能有一个),
                worm_append_unit: WORM追加态文件保护粒度 (可选, 仅advance_mode支持)。可选值：256KB, 512KB, 1M,
             }
        task_remarks: 异步任务备注信息，0~1024个字符（可选）
        audit_log_rules: 审计日志规则集合（可选），如：set_security、get_security、set_attr、get_attr等，最多100条
        unix_permissions: 文件系统目录权限（可选），格式如0755

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
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
    """
    批量查询命名空间
    
    Args:
        client: DME API 客户端
        page_no: 分页查询页码（可选），1~10000000
        page_size: 每页显示的数量（可选），1~1000，默认 100
        sort_dir: 指定排序方向（可选），可选值：asc（升序）、desc（降序）
        sort_key: 排序参数（可选），可选值：namespace_used_rate、file_used_rate
        name: 命名空间名称（可选），1~256 个字符，支持模糊查询
        vstore_name: 命名空间所属租户名称（可选），1~256 个字符，支持模糊查询
        vstore_raw_id: 命名空间所属 vStore 在存储设备上分配的 ID（可选），1~128 个字符
        vstore_id: 命名空间所属 vStore 的 ID（可选），1~128 个字符
        raw_id: 命名空间在存储设备上的 ID（可选），1~256 个字符
        pool_name: 存储池名称（可选），1~256 个字符，支持模糊查询
        storage_id: 归属存储设备 ID（可选），1~255 个字符
        enable_encrypt: 是否开启加密（可选），true：是；false：否
        support_provisioning: 是否支持业务发放（可选），true：是；false：否；下发此字段可过滤不支持业务发放设备的资源，当前不支持业务发放的设备有 DataTurbo 系列
        gfs_id: 全局命名空间 ID（可选），1~64 个字符
        gfs_name: 全局命名空间名称（可选），1~256 个字符
        has_gfs: 是否包含所属全局命名空间的命名空间（可选），true：是；false：否；has_gfs 为 false 时不支持下发 gfs_id
    
    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }，包含：
        - total: 命名空间数量
        - namespace_list: 命名空间列表，包含 id, raw_id, name, storage_id, vstore_id 等信息
    """
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
    """
    查询指定命名空间详情
    
    Args:
        client: DME API 客户端
        namespace_id: 命名空间 ID（必选，1~64 个字符）
    
    Returns:
        命名空间详细信息，包含：
        - id: 命名空间 ID
        - raw_id: 命名空间在存储设备上的 ID
        - name: 命名空间名称
        - storage_id: 存储设备 ID
        - vstore_id: 租户 ID
        - vstore_name: 租户名称
        - pool_id: 存储池 ID
        - pool_name: 存储池名称
        - running_status: 运行状态（NORMAL/UNKNOWN）
        - space_used_rate: 空间使用率
        - file_used_rate: 文件使用率
        - space_used: 已使用空间
        - file_used: 已使用文件数
        - trash_enable: 是否开启回收站
        - enable_encrypt: 是否开启加密
        - rdc: 数据冗余份数
        - acl_policy_type: 安全模式
        - gfs_id: 全局命名空间 ID
        - qos_policy: QoS 策略
        - worm: WORM 参数
        等详细信息
    """
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
    """
    批量创建命名空间
    
    Args:
        client: DME API 客户端
        storage_id: 存储设备 ID（必填）
        pool_raw_id: 存储池在存储设备上的 ID（必填）
        namespace_specs: 命名空间批量参数。参数格式如下：[{
                name: 名称 (必填, 1~255字符, 支持数字字母下划线.-),
                count: 数量 (必填, 1~500),
                start_suffix: 起始后缀编号 (可选, 0~9999; 起始后缀+数量<=9999),
                isInGfs: 是否在全局命名空间中 (可选)。可选值：true, false,
             }, ...]
        enable_update_atime: 是否更新 Atime
        trash_visible: 回收站目录是否可见，默认不可见
        trash_enable: 回收站功能是否开启，默认不开启
        interval_trash: 回收站保护时长（分钟），0 表示永久保留，最大 4294967295
        dps_switch: 元数据检索开关，true 开启
        forbidden_dpc: 是否禁止 dpc 挂载
        audit_log_switch: 是否开启审计日志，默认关闭
        audit_log_rule: 审计日志规则列表，可选值：open, create, read, write, close, 
                       delete, rename, get_attr, set_attr, get_security, set_security,
                       get_xattr, set_xattr, list_dir, contact, mount_or_unmount, login_or_logoff
        atime_update_mode: atime 更新频率，4294967295 关闭，3600 1 小时，86400 1 天
        acl_policy_type: 安全模式，可选值：mixed, unix, native, ntfs，默认 unix
        enable_encrypt: 是否开启加密
        crypt_alg: 加密算法类型，可选值：XTS_AES_128, XTS_AES_256, XTS_SM4, UNKNOWN
        case_sensitive: 大小写是否敏感，默认不敏感
        show_snap_dir: 快照目录是否可见
        rdc: 数据冗余份数，可选值：redundancy_2, redundancy_3, redundancy_4
        worm: WORM 配置 (可选)。参数格式如下：{
                worm_mode: WORM策略模式 (可选)。可选值：non_worm (None类型), enterprise_mode (企业级), compliance_mode (法规级),
                min_protect_period: 最小保护期 (可选, 0~4294967295, 默认0; 4294967295为无限期),
                min_protect_period_unit: 最小保留时间单位 (可选, 默认year)。可选值：day, year, month, hour, minute,
                max_protect_period: 最大保护期 (可选, 1~4294967295, 默认70; 4294967295为无限期),
                max_protect_period_unit: 最大保留时间单位 (可选, 默认year)。可选值：day, year, month, hour, minute, infinite,
                def_protect_period: 默认保护期 (可选, 0~4294967295, 默认70),
                def_protect_period_unit: 默认保留时间单位 (可选, 默认year)。可选值：day, year, month, hour, minute, infinite,
                auto_lock_enabled: WORM是否自动锁定 (可选, 默认false)。可选值：true, false,
                auto_lock_time: 自动锁定时间 (可选, 1~64800, 默认2; 单位day时1~45, hour时1~1080, minute时1~64800),
                auto_lock_unit: 自动锁定时间单位 (可选, 默认hour)。可选值：day, minute, hour,
                legal_hold_modify: 诉讼保留文件修改保留期开关 (可选, 默认false)。可选值：true, false,
             }
        qos_policy: QoS 策略配置。参数格式如下：{
                qos_scale: 上限控制维度 (必选)。可选值：namespace, client, account, user, innertask,
                name: QoS策略名称 (可选, 1~63字符, 正则^[a-zA-Z0-9][a-zA-Z0-9_-]*, 只能以数字或字母开头),
                qos_mode: QoS模式 (必选)。可选值：by_usage (按已使用量), by_package (按固定容量), manual (按上限),
                account_raw_id: 帐户在存储设备上的id (可选, 0~4294967293; 当qos_scale为namespace/account/user时必选),
                package_size: 包容量GB (可选, 0~94371840; 当qos_mode为by_package时必选),
                max_iops: IOPS上限 (可选, 0~1073741824000; 批量创建命名空间时为必选),
                max_mbps: 带宽上限Mbps (可选, 0~1073741824; 当qos_mode为manual时必选),
                max_band_width: 最大带宽Mbps (可选, 1~1073741824; 当qos_mode为by_usage或by_package时必选),
                basic_band_width: 基础带宽Mbps (可选, 1~1073741824; 当qos_mode为by_usage或by_package时必选),
                bps_density: 带宽密度Mbps (可选, 1~1024000; 当qos_mode为by_usage或by_package时必选),
                max_conn_cluster: 最大连接数 (可选),
                max_lock_cluster: 最大锁数量 (可选),
                max_open_file_cluster: 最大打开文件数量 (可选),
                read_ops: 读OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_ops: 写OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                read_mbps: 读带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_mbps: 写带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
             }
        public_network_qos_policy: 公网 QoS 策略配置。参数格式如下：{
                        name: QoS 策略名称（可选），1~63 个字符，正则 ^[a-zA-Z0-9][a-zA-Z0-9_-]*，只能以数字或字母开头,
                        qos_mode: QoS 模式（条件必选），可选值：by_usage（按已使用量）、by_package（按固定容量）、manual（按上限）；批量创建命名空间时为必选，修改时为非必选,
                        package_size: 包容量（可选），0~94371840（GB），当 qos_mode 为 by_package 时必选,
                        max_iops: IOPS 上限（条件必选），0~1073741824000，批量创建命名空间时为必选，修改时为非必选,
                        max_mbps: 带宽上限（可选），0~1073741824（Mbps），当 qos_mode 为 manual 时必选,
                        max_band_width: 最大带宽（可选），1~1073741824（Mbps），当 qos_mode 为 by_usage 或 by_package 时必选,
                        basic_band_width: 基础带宽（可选），1~1073741824（Mbps），当 qos_mode 为 by_usage 或 by_package 时必选,
                bps_density: 带宽密度Mbps (可选, 1~1024000; 当qos_mode为by_usage或by_package时必选),
                max_conn_cluster: 最大连接数 (可选),
                max_lock_cluster: 最大锁数量 (可选),
                max_open_file_cluster: 最大打开文件数量 (可选),
                read_ops: 读OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_ops: 写OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                read_mbps: 读带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_mbps: 写带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
             }
        private_network_qos_policy: 私网 QoS 策略配置。参数格式如下：{
                        name: QoS 策略名称（可选），1~63 个字符，正则 ^[a-zA-Z0-9][a-zA-Z0-9_-]*，只能以数字或字母开头,
                        qos_mode: QoS 模式（条件必选），可选值：by_usage（按已使用量）、by_package（按固定容量）、manual（按上限）；批量创建命名空间时为必选，修改时为非必选,
                        package_size: 包容量（可选），0~94371840（GB），当 qos_mode 为 by_package 时必选,
                        max_iops: IOPS 上限（条件必选），0~1073741824000，批量创建命名空间时为必选，修改时为非必选,
                        max_mbps: 带宽上限（可选），0~1073741824（Mbps），当 qos_mode 为 manual 时必选,
                        max_band_width: 最大带宽（可选），1~1073741824（Mbps），当 qos_mode 为 by_usage 或 by_package 时必选,
                        basic_band_width: 基础带宽（可选），1~1073741824（Mbps），当 qos_mode 为 by_usage 或 by_package 时必选,
                bps_density: 带宽密度Mbps (可选, 1~1024000; 当qos_mode为by_usage或by_package时必选),
                max_conn_cluster: 最大连接数 (可选),
                max_lock_cluster: 最大锁数量 (可选),
                max_open_file_cluster: 最大打开文件数量 (可选),
                read_ops: 读OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_ops: 写OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                read_mbps: 读带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_mbps: 写带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
             }
        create_s3_param: 创建 S3 协议参数 (可选)。参数格式如下：{
                bucket_permission: 策略类型 (必选)。可选值：private (私有), public_read_only (公共读), public_write_only (公共写), public_read_write (公共读写),
                version_status: 对象多版本状态 (可选, 0~2)。可选值：0 (关闭), 1 (打开), 2 (暂停),
             }
        application_type: 应用类型，可选值：PACS（医疗影像场景）, GENERAL（通用场景）
        task_remarks: 异步任务备注信息
    
    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }（异步任务 ID）
    """
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
    """
    修改指定命名空间
    
    Args:
        client: DME API 客户端
        namespace_id: 命名空间 ID（必选，1~64 个字符）
        enable_update_atime: 是否更新 Atime，true：更新；false：不更新
        show_snap_dir: 快照目录是否可见，true：可见；false：不可见
        trash_visible: 回收站目录是否可见，true：可见；false：不可见，默认不可见
        trash_enable: 回收站功能是否开启，true：开启；false：不开启，默认不开启
        interval_trash: 回收站保护时长（分钟），0 表示永久保留，不自动删除，最大 4294967295
        dps_switch: 元数据检索开关，true：开启；false：关闭
        forbidden_dpc: 是否禁止 dpc 挂载，true：禁止；false：不禁止
        audit_log_switch: 是否开启审计日志，缺省关闭，true：开启；false：关闭
        audit_log_rule: 审计日志规则列表，可选值：open, create, read, write, close, delete, rename,
                       get_attr, set_attr, get_security, set_security, get_xattr, set_xattr,
                       list_dir, contact, mount_or_unmount, login_or_logoff
        atime_update_mode: atime 更新频率，4294967295：关闭更新；3600：1 小时更新；86400：1 天更新
        acl_policy_type: 命名空间安全模式，可选值：mixed（同时支持 UNIX 和 Windows 权限），
                        unix（适用于 NFS 用户的权限由 Unix Mode/NFSv4 ACL 权限控制），
                        native（与 Mixed 模式适用于相同的场景），
                        ntfs（适用于 CIFS 用户的权限由 Windows NT ACL 权限控制）
        enable_encrypt: 是否开启加密，true：开启；false：关闭
        qos_policy: QoS 策略配置。参数格式如下：{
                qos_switch: QoS开关 (必选)。可选值：on, off,
                name: QoS策略名称 (可选, 1~63字符, 正则^[a-zA-Z0-9][a-zA-Z0-9_-]*),
                qos_mode: QoS模式 (条件必选)。可选值：by_usage (按已使用量), by_package (按固定容量), manual (按上限),
                package_size: 包容量GB (可选, 0~94371840; 当qos_mode为by_package时必选),
                max_iops: IOPS上限 (条件必选, 0~1073741824000),
                max_mbps: 带宽上限Mbps (可选, 0~1073741824; 当qos_mode为manual时必选),
                max_band_width: 最大带宽Mbps (可选, 1~1073741824; 当qos_mode为by_usage或by_package时必选),
                basic_band_width: 基础带宽Mbps (可选, 1~1073741824; 当qos_mode为by_usage或by_package时必选),
                bps_density: 带宽密度Mbps (可选, 1~1024000; 当qos_mode为by_usage或by_package时必选),
                max_conn_cluster: 最大连接数 (可选),
                max_lock_cluster: 最大锁数量 (可选),
                max_open_file_cluster: 最大打开文件数量 (可选),
                read_ops: 读OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_ops: 写OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                read_mbps: 读带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_mbps: 写带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
             }
        public_network_qos_policy: 公网 QoS 策略配置。参数格式如下：{
                        qos_switch: QoS 开关（必填），可选值：on、off,
                        name: QoS 策略名称（可选），1~63 个字符，正则 ^[a-zA-Z0-9][a-zA-Z0-9_-]*，只能以数字或字母开头,
                        qos_mode: QoS 模式（条件必选），可选值：by_usage（按已使用量）、by_package（按固定容量）、manual（按上限）；批量创建命名空间时为必选，修改时为非必选,
                        package_size: 包容量（可选），0~94371840（GB），当 qos_mode 为 by_package 时必选,
                        max_iops: IOPS 上限（条件必选），0~1073741824000，批量创建命名空间时为必选，修改时为非必选,
                        max_mbps: 带宽上限（可选），0~1073741824（Mbps），当 qos_mode 为 manual 时必选,
                        max_band_width: 最大带宽（可选），1~1073741824（Mbps），当 qos_mode 为 by_usage 或 by_package 时必选,
                        basic_band_width: 基础带宽（可选），1~1073741824（Mbps），当 qos_mode 为 by_usage 或 by_package 时必选,
                bps_density: 带宽密度Mbps (可选, 1~1024000; 当qos_mode为by_usage或by_package时必选),
                max_conn_cluster: 最大连接数 (可选),
                max_lock_cluster: 最大锁数量 (可选),
                max_open_file_cluster: 最大打开文件数量 (可选),
                read_ops: 读OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_ops: 写OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                read_mbps: 读带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_mbps: 写带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
             }
        private_network_qos_policy: 私网 QoS 策略配置。参数格式如下：{
                        qos_switch: QoS 开关（必填），可选值：on、off,
                        name: QoS 策略名称（可选），1~63 个字符，正则 ^[a-zA-Z0-9][a-zA-Z0-9_-]*，只能以数字或字母开头,
                        qos_mode: QoS 模式（条件必选），可选值：by_usage（按已使用量）、by_package（按固定容量）、manual（按上限）；批量创建命名空间时为必选，修改时为非必选,
                        package_size: 包容量（可选），0~94371840（GB），当 qos_mode 为 by_package 时必选,
                        max_iops: IOPS 上限（条件必选），0~1073741824000，批量创建命名空间时为必选，修改时为非必选,
                        max_mbps: 带宽上限（可选），0~1073741824（Mbps），当 qos_mode 为 manual 时必选,
                        max_band_width: 最大带宽（可选），1~1073741824（Mbps），当 qos_mode 为 by_usage 或 by_package 时必选,
                        basic_band_width: 基础带宽（可选），1~1073741824（Mbps），当 qos_mode 为 by_usage 或 by_package 时必选,
                bps_density: 带宽密度Mbps (可选, 1~1024000; 当qos_mode为by_usage或by_package时必选),
                max_conn_cluster: 最大连接数 (可选),
                max_lock_cluster: 最大锁数量 (可选),
                max_open_file_cluster: 最大打开文件数量 (可选),
                read_ops: 读OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_ops: 写OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                read_mbps: 读带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_mbps: 写带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
             }
        application_type: 应用类型，可选值：PACS（医疗影像场景）, GENERAL（通用场景）
        task_remarks: 异步任务备注信息
    
    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }（异步任务 ID）
    """
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
    """
    批量删除命名空间
    
    Args:
        client: DME API 客户端
        namespace_ids: 命名空间 ID 列表（必选），数组最大 100 个，最小 1 个
        task_remarks: 异步任务备注信息（可选，0~1024 个字符）
    
    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }（异步任务 ID）
    """
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
    """
    查询 NFS 共享下的客户端访问列表

    指定设备或 NFS ID，查询 NFS 共享下的客户端访问列表。

    Args:
        client: DME API 客户端
        page_no: 分页查询的起始页码（可选），最小值 1，默认 1
        page_size: 单页显示的数量（可选），1~1000，默认 20
        nfs_share_id: NFS 共享 ID（可选），1~64 个字符
        storage_id: 存储设备 ID（可选），1~64 个字符；如果指定 nfs_share_id，则此参数无效
        vstore_id_in_storage: vStore ID（可选），1~256 个字符；vStore 场景下必须下发
        name: 客户端 IP 或主机名或网络组名（可选），1~256 个字符；指定 nfs_share_id 条件下支持模糊搜索
        client_id_in_storage: NFS 共享客户端 ID（可选），1~256 个字符
        sort_key: 排序字段（可选），可选值：raw_id、name
        sort_dir: 排序方向（可选），可选值：asc（升序）、desc（降序），默认 asc

    Returns:
        客户端访问列表
    """
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
    """
    批量查询 DataTurbo 管理员

    仅 OceanStor A800 系列存储支持。

    Args:
        client: DME API 客户端
        storage_id: 设备 ID (1~64个字符, 可选)
        vstore_id: 租户的 ID (1~64个字符, 可选)
        vstore_name: 租户的名称，支持模糊查询 (1~256个字符, 可选)
        zone_id: 所属 zone 的 ID (1~64个字符, 可选)。当资源所属范围为全局时，Zone ID 为所属设备的 Id；当资源所属范围为本地时，Zone ID 为所属 Zone 的 ID。仅 OceanStor A800 系列存储支持
        name: DataTurbo 管理员名，支持模糊查询 (1~256个字符, 可选)
        online_status: DataTurbo 管理员在线状态 (可选)。可选值：offline (离线), online (在线)
        lock_status: DataTurbo 管理员锁定状态 (可选)。可选值：unlocked (未锁定), locked (锁定)
        account_state: DataTurbo 管理员密码状态 (可选)。可选值：normal (正常), expired (密码过期), initial (用户密码处于初始化状态，需要修改), expiring_soon (密码即将到期), change_required (下一次登录必须修改密码), never (密码永不过期)
        sort_key: 按照指定字段排序 (可选)。可选值：create_time
        sort_dir: 指定排序方向 (可选)。可选值：asc (升序), desc (降序)
        page_no: 分页查询的起始页码 (int32, 最小值: 1, 默认值: 1, 可选)
        page_size: 单页显示的数量 (int32, 最小值: 1, 最大值: 1000, 默认值: 20, 可选)

    Returns:
        DataTurbo 管理员列表，包含 total 和 administrators
    """
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
    """
    修改 UNIX 用户

    Args:
        client: DME API 客户端
        id: UNIX 用户 ID (1~32个字符, 必填)
        raw_id: UNIX 用户在存储设备上的 ID (int64, 0~4294967294, 可选)
        description: UNIX 用户描述 (0~255个字符, 可选)
        primary_group_name: 用户主组名称 (1~64个字符, 可选。与 primary_group_raw_id 都下发仅 primary_group_raw_id 生效)
        primary_group_raw_id: 用户主组 ID (int64, 0~4294967294, 可选。与 primary_group_name 都下发仅 primary_group_raw_id 生效)
        status_enable: 用户状态 (boolean, 可选)。可选值：true (启用), false (锁定)。仅 OceanStor Pacific 和 OceanStor A310 系列存储支持

    Returns:
        修改结果
    """
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
    """
    创建 UNIX 用户组

    Args:
        client: DME API 客户端
        storage_id: 创建 UNIX 用户组所属存储设备 ID (1~64个字符, 必填)
        name: UNIX 用户组名称 (1~64个字符, 必填)
        raw_id: UNIX 用户组 ID (int64, 0~4294967294, 可选。OceanStor Pacific 和 OceanStor A310 存储必填)
        description: UNIX 用户组描述 (0~255个字符, 可选)
        vstore_raw_id: 用户所属租户在存储设备上的 ID (1~32个字符, 必填)
        zone_id: 所属 Zone ID (1~64个字符, 可选。仅 OceanStor A800 存储支持)

    Returns:
        创建结果
    """
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
    """
    删除 UNIX 用户

    Args:
        client: DME API 客户端
        ids: UNIX 用户 ID 列表 (List<string>, 数组最小成员个数: 1, 数组最大成员个数: 100, 必填)

    Returns:
        操作结果
    """
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
    """
    查询 UNIX 认证用户组列表

    Args:
        client: DME API 客户端
        page_no: 分页查询的起始位置 (int32, 1~2147483647, 默认值: 1, 可选)
        page_size: 每页显示的数量 (int32, 10~100, 默认值: 100, 可选)
        storage_name: 设备名称，支持模糊匹配过滤 (1~256个字符, 可选)
        vstore_raw_id: 所属租户在存储设备上的 ID (1~64个字符, 可选)
        vstore_name: 所属租户名称，支持模糊搜索过滤 (1~256个字符, 可选)
        name: 用户组名称，支持模糊搜索过滤 (1~256个字符, 可选)
        raw_id: 用户组在存储设备上的 ID (1~256个字符, 可选)
        zone_id: Zone ID (1~64个字符, 可选)。仅 OceanStor A800 存储下的认证用户组支持通过该字段过滤
        sort_key: 按照指定字段排序 (可选)。可选值：name (用户组名), raw_id (用户组在存储设备上的 ID), create_time (创建时间)。默认值：create_time
        storage_id: 存储设备 ID (1~36个字符, 可选)
        sort_dir: 指定排序方向 (可选)。可选值：asc (升序), desc (降序)。默认值：desc

    Returns:
        UNIX 认证用户组列表
    """
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
    """
    查询 UNIX 用户组详情

    Args:
        client: DME API 客户端
        id: 用户组 ID (1~32个字符, 必填)

    Returns:
        UNIX 用户组详情
    """
    url = "/rest/fileservice/v1/unix-user-groups/{id}"

    response = client.get(url, params={"id": id})
    return response


def account_unix_user_group_modify(client: DMEAPIClient, id: str,
                                    raw_id: int = None,
                                    description: str = None) -> dict:
    """
    修改 UNIX 用户组

    Args:
        client: DME API 客户端
        id: UNIX 用户组 ID (1~32个字符, 必填)
        raw_id: UNIX 用户组在存储设备上的 ID (int64, 0~4294967294, 可选)
        description: UNIX 用户组描述 (0~255个字符, 可选)

    Returns:
        修改结果
    """
    url = "/rest/fileservice/v1/unix-user-groups/{id}"

    payload = {}

    if raw_id is not None:
        payload['raw_id'] = raw_id
    if description is not None:
        payload['description'] = description

    response = client.put(url, params={"id": id})
    return response


def account_unix_user_group_batch_delete(client: DMEAPIClient, ids: list) -> dict:
    """
    删除 UNIX 用户组

    Args:
        client: DME API 客户端
        ids: UNIX 用户组的 ID 列表 (List<string>, 数组最小成员个数: 1, 数组最大成员个数: 100, 必填)

    Returns:
        操作结果
    """
    url = "/rest/fileservice/v1/unix-user-groups/delete"

    payload = {
        'ids': ids,
    }

    response = client.post(url, body=payload)
    return response


def account_unix_user_remove_group(client: DMEAPIClient, user_id: str,
                                    secondary_group_name_list: list) -> dict:
    """
    移除 UNIX 用户附属组

    Args:
        client: DME API 客户端
        user_id: UNIX 用户 ID (1~32个字符, 必填)
        secondary_group_name_list: 附属组名称列表 (List<string>, 数组最小成员个数: 1, 数组最大成员个数: 100, 必填)

    Returns:
        操作结果
    """
    url = "/rest/fileservice/v1/unix-users/{user_id}/remove-secondary-group"

    payload = {
        'secondary_group_name_list': secondary_group_name_list,
    }

    response = client.post(url, params={"user_id": user_id})
    return response


def account_unix_user_show(client: DMEAPIClient, id: str) -> dict:
    """
    查询 UNIX 认证用户详情

    Args:
        client: DME API 客户端
        id: 用户 ID (1~32个字符, 必填)

    Returns:
        UNIX 认证用户详情
    """
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
    """
    查询 UNIX 认证用户列表

    Args:
        client: DME API 客户端
        page_no: 分页查询的起始位置 (int32, 1~2147483647, 默认值: 1, 可选)
        page_size: 每页显示的数量 (int32, 10~100, 默认值: 100, 可选)
        storage_name: 设备名称，支持模糊搜索过滤 (1~256个字符, 可选)
        vstore_raw_id: 所属租户在存储设备上的 ID (1~64个字符, 可选)
        vstore_name: 所属租户名称，支持模糊搜索过滤 (1~256个字符, 可选)
        name: 用户名称，支持模糊搜索过滤 (1~256个字符, 可选)
        primary_group_name: 主组名称，支持模糊搜索过滤 (1~256个字符, 可选)
        raw_id: 用户在存储设备上的 ID (1~255个字符, 可选)
        zone_id: Zone ID (1~64个字符, 可选)。仅 OceanStor A800 存储下的认证用户支持通过该字段过滤
        user_status: 用户状态 (可选)。可选值：enable (启用), disable (禁用)
        sort_key: 按照指定字段排序 (可选)。可选值：name (用户名), raw_id (用户在存储设备上的 ID), primary_group_name (主组名), create_time (创建时间)。默认值：create_time
        storage_id: 存储设备 ID (1~36个字符, 可选)
        sort_dir: 指定排序方向 (可选)。可选值：asc (升序), desc (降序)。默认值：desc

    Returns:
        UNIX 认证用户列表
    """
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
    """
    添加 UNIX 用户附属组

    Args:
        client: DME API 客户端
        user_id: UNIX 用户 ID (1~32个字符, 必填)
        secondary_group_name_list: 附属组名称列表 (List<string>, 数组最小成员个数: 1, 数组最大成员个数: 100, 必填)

    Returns:
        操作结果
    """
    url = "/rest/fileservice/v1/unix-users/{user_id}/add-secondary-group"

    payload = {
        'secondary_group_name_list': secondary_group_name_list,
    }

    response = client.post(url, params={"user_id": user_id})
    return response


def account_unix_user_create(client: DMEAPIClient, storage_id: str, name: str, vstore_raw_id: str,
                              raw_id: int = None, description: str = None,
                              primary_group_raw_id: int = None,
                              primary_group_name: str = None, zone_id: str = None,
                              status: bool = None,
                              secondary_group_name_list: list = None) -> dict:
    """
    创建 UNIX 用户

    Args:
        client: DME API 客户端
        storage_id: 创建 UNIX 用户所属存储设备 ID (1~64个字符, 必填)
        name: UNIX 用户名称 (1~64个字符, 必填)
        raw_id: UNIX 用户 ID (int64, 0~4294967294, 可选。OceanStor Pacific 和 OceanStor A310 存储必填)
        description: UNIX 用户描述 (0~255个字符, 可选)
        primary_group_raw_id: 用户主组 ID (int64, 0~4294967294, 可选。与 primary_group_name 至少下发一个，若都下发仅 primary_group_name 生效)
        primary_group_name: 用户所归属的主组名称 (1~64个字符, 可选。与 primary_group_raw_id 至少下发一个，若都下发仅 primary_group_name 生效)
        vstore_raw_id: 用户所属租户在存储设备上的 ID (1~32个字符, 必填)
        zone_id: 所属 Zone ID (1~64个字符, 可选。仅 OceanStor A800 存储支持)
        status: 用户状态 (boolean, 可选。默认值：true)。可选值：true (启用), false (锁定)。仅 OceanStor Pacific 和 OceanStor A310 系列存储支持
        secondary_group_name_list: 用户附属组名称列表 (List<string>, 数组最小成员个数: 0, 数组最大成员个数: 100, 可选)

    Returns:
        创建结果
    """
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
    """
    批量创建 KV Cache 库

    Args:
        client: DME API 客户端
        storage_id: 存储设备 ID (长度为36个字符, 必填)
        zone_id: 所属 Zone 的 ID (长度为36个字符, 必填)
        pool_raw_id: 存储池在所属 Zone 上的 ID (1~64个字符, 必填)
        vstore_id: 租户 ID (长度为32个字符, 必填)
        data_cleanup_switch: 清理开关 (可选)。可选值：on (打开), off (关闭)。默认值：off
        max_survival_time: KV Cache 最长存活时间 (int32, 1~3650, 可选。当 data_cleanup_switch 为 on 时必填)
        kv_cache_stores: KV Cache 库列表 (List<CreateKVCacheStoreBaseInfo>, 数组最小成员个数: 1, 数组最大成员个数: 100, 必填)。参数格式如下：[{
                name: KV Cache 库名称 (1~255个字符, 必填),
                capacity: KV Cache 库容量 (int64, 20971520~70368744177664, 单位: 扇区数, 1扇区=512字节, 必填),
                description: 描述信息 (1~255个字符, 可选),
                count: 批量创建 KV Cache 库的数量 (int32, 1~100, 默认值: 1, 可选),
                start_suffix: 起始后缀编号 (int32, 0~9999, 可选。起始后缀编号+KV Cache库数量<=9999),
             }, ...]

    Returns:
        创建结果
    """
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
    """
    修改 KV Cache 库

    Args:
        client: DME API 客户端
        kv_cache_stores_id: KV Cache 库 ID (1~64个字符, 必填)
        name: KV Cache 库名称 (1~255个字符, 可选)
        description: 描述信息 (0~255个字符, 可选)
        data_cleanup_switch: 清理开关 (可选)。可选值：on (打开), off (关闭)。默认值：off
        max_survival_time: KV Cache 最长存活时间 (int32, 1~3650, 可选。当 data_cleanup_switch 为 on 时必填)

    Returns:
        修改结果
    """
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
    """
    批量删除 KV Cache 库

    Args:
        client: DME API 客户端
        ids: KV Cache 库 ID 列表 (List<string>, 数组最小成员个数: 1, 数组最大成员个数: 100, 必填)

    Returns:
        操作结果
    """
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
    """
    查询 KV Cache 库

    Args:
        client: DME API 客户端
        storage_id: 存储设备 ID (长度为36个字符, 可选)
        id: KV Cache 库 ID (长度为32个字符, 可选)
        raw_id: KV Cache 库在 Zone 上的 ID (1~256个字符, 可选)
        name: KV Cache 库名称 (1~256个字符, 可选)
        zone_id: 所属 Zone 的 ID (长度为36个字符, 可选)
        pool_raw_id: 存储池在所属 Zone 上的 ID (1~64个字符, 可选)
        vstore_id: 租户 ID (长度为32个字符, 可选)
        vstore_name: 租户名称 (1~256个字符, 可选)
        fs_id: 文件系统 ID (长度为32个字符, 可选)
        fs_name: 文件系统名称 (1~256个字符, 可选)
        data_cleanup_switch: 清理开关 (可选)。可选值：on (打开), off (关闭)
        page_no: 分页页码 (int32, 1~10000, 默认值: 1, 可选)
        page_size: 每页数据条数 (int32, 1~100, 默认值: 20, 可选)
        sort_dir: 指定排序方向 (可选)。可选值：asc (升序), desc (降序)。默认值：asc
        sort_key: 排序参数 (可选)。可选值：capacity (总容量), used_capacity (已用容量), used_tokens (已使用的 token 数量), hit_ratio (命中率)

    Returns:
        KV Cache 库列表
    """
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
        'description': '批量查询 DataTurbo 管理员',
        'params': ['storage_id', 'vstore_id', 'vstore_name', 'zone_id', 'name', 'online_status', 'lock_status', 'account_state', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_unix_user_create': {
        'func': account_unix_user_create,
        'description': '创建 UNIX 用户',
        'params': ['storage_id', 'name', 'vstore_raw_id', 'raw_id', 'description', 'primary_group_raw_id', 'primary_group_name', 'zone_id', 'status', 'secondary_group_name_list'],
        'subtopic': 'account'
    },
    'account_unix_user_add_group': {
        'func': account_unix_user_add_group,
        'description': '添加 UNIX 用户附属组',
        'params': ['user_id', 'secondary_group_name_list'],
        'subtopic': 'account'
    },
    'account_unix_user_list': {
        'func': account_unix_user_list,
        'description': '查询 UNIX 认证用户列表',
        'params': ['storage_id', 'storage_name', 'vstore_raw_id', 'vstore_name', 'name', 'primary_group_name', 'raw_id', 'zone_id', 'user_status', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_unix_user_show': {
        'func': account_unix_user_show,
        'description': '查询 UNIX 认证用户详情',
        'params': ['id'],
        'subtopic': 'account'
    },
    'account_unix_user_remove_group': {
        'func': account_unix_user_remove_group,
        'description': '移除 UNIX 用户附属组',
        'params': ['user_id', 'secondary_group_name_list'],
        'subtopic': 'account'
    },
    'account_unix_user_modify': {
        'func': account_unix_user_modify,
        'description': '修改 UNIX 用户',
        'params': ['id', 'raw_id', 'description', 'primary_group_name', 'primary_group_raw_id', 'status_enable'],
        'subtopic': 'account'
    },
    'account_unix_user_batch_delete': {
        'func': account_unix_user_batch_delete,
        'description': '删除 UNIX 用户',
        'params': ['ids'],
        'subtopic': 'account'
    },
    'account_unix_user_group_create': {
        'func': account_unix_user_group_create,
        'description': '创建 UNIX 用户组',
        'params': ['storage_id', 'name', 'vstore_raw_id', 'raw_id', 'description', 'zone_id'],
        'subtopic': 'account'
    },
    'account_unix_user_group_list': {
        'func': account_unix_user_group_list,
        'description': '查询 UNIX 认证用户组列表',
        'params': ['storage_id', 'storage_name', 'vstore_raw_id', 'vstore_name', 'name', 'raw_id', 'zone_id', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_unix_user_group_show': {
        'func': account_unix_user_group_show,
        'description': '查询 UNIX 用户组详情',
        'params': ['id'],
        'subtopic': 'account'
    },
    'account_unix_user_group_modify': {
        'func': account_unix_user_group_modify,
        'description': '修改 UNIX 用户组',
        'params': ['id', 'raw_id', 'description'],
        'subtopic': 'account'
    },
    'account_unix_user_group_batch_delete': {
        'func': account_unix_user_group_batch_delete,
        'description': '删除 UNIX 用户组',
        'params': ['ids'],
        'subtopic': 'account'
    },
    'dtree_list': {
        'func': dtree_list,
        'description': '查询 Dtree 列表',
        'params': ['id_in_storage', 'name', 'device_name', 'storage_id', 'zone_id', 'manufacturer', 'tier_name', 'fs_name', 'fs_id', 'namespace_name', 'namespace_id', 'quota_switch', 'security_mode', 'nas_locking_policy', 'sort_key', 'sort_dir', 'page_no', 'page_size', 'dc_id', 'dc_name'],
        'subtopic': 'dtree'
    },
    'dtree_show': {
        'func': dtree_show,
        'description': '查询指定 Dtree 详情',
        'params': ['dtree_id'],
        'subtopic': 'dtree'
    },
    'dtree_create': {
        'func': dtree_create,
        'description': '创建并共享 Dtree',
        'params': ['storage_id', 'create_dtrees_param', 'fs_id', 'namespace_id', 'zone_id', 'parent_dir', 'quota_switch', 'security_mode', 'nas_locking_policy', 'create_nfs_share_param', 'create_cifs_share_param', 'dataturbo_share', 'create_worm_param', 'unix_permissions', 'task_remarks'],
        'subtopic': 'dtree'
    },
    'dtree_delete': {
        'func': dtree_delete,
        'description': '批量删除 Dtree',
        'params': ['dtree_ids', 'task_remarks'],
        'subtopic': 'dtree'
    },
    'dtree_modify': {
        'func': dtree_modify,
        'description': '修改指定 Dtree',
        'params': ['dtree_id', 'name', 'quota_switch', 'security_mode', 'nas_locking_policy', 'unix_permissions', 'task_remarks'],
        'subtopic': 'dtree'
    },
    # NFS share 子主题动作
    'nfs_share_list': {
        'func': nfs_share_list,
        'description': '查询 NFS 共享列表',
        'params': ['id_in_storage', 'name', 'share_path', 'exact_share_path', 'device_name', 'storage_id', 'tier_name', 'owning_dtree_name', 'fs_name', 'fs_id', 'owning_dtree_id', 'vstore_name', 'page_no', 'page_size', 'sort_key', 'sort_dir', 'support_provisioning', 'namespace_id', 'namespace_name', 'dc_id', 'dc_name', 'zone_id', 'zone_name', 'zone_ip'],
        'subtopic': 'nfs_share'
    },
    'nfs_share_show': {
        'func': nfs_share_show,
        'description': '查询指定 NFS 共享详情',
        'params': ['nfs_share_id'],
        'subtopic': 'nfs_share'
    },
    'nfs_share_create': {
        'func': nfs_share_create,
        'description': '创建 NFS 共享',
        'params': ['create_nfs_share_param', 'task_remarks'],
        'subtopic': 'nfs_share'
    },
    'nfs_share_modify': {
        'func': nfs_share_modify,
        'description': '修改指定 NFS 共享',
        'params': ['nfs_share_id', 'description', 'character_encoding', 'audit_items', 'show_snapshot_enable', 'nfs_share_client_addition', 'nfs_share_client_modification', 'nfs_share_client_deletion', 'file_name_ex_filters', 'task_remarks'],
        'subtopic': 'nfs_share'
    },
    'nfs_share_delete': {
        'func': nfs_share_delete,
        'description': '批量删除 NFS 共享',
        'params': ['nfs_share_ids', 'task_remarks'],
        'subtopic': 'nfs_share'
    },
    'nfs_share_show_clients': {
        'func': nfs_share_show_clients,
        'description': '查询 NFS 共享下的客户端访问列表',
        'params': ['page_no', 'page_size', 'nfs_share_id', 'storage_id', 'vstore_id_in_storage', 'name', 'client_id_in_storage', 'sort_key', 'sort_dir'],
        'subtopic': 'nfs_share'
    },
    # CIFS 共享子主题动作
    'cifs_share_list': {
        'func': cifs_share_list,
        'description': '批量查询 CIFS 共享',
        'params': ['raw_id', 'name', 'share_path', 'exact_share_path', 'fs_id', 'fs_name', 'dtree_id', 'dtree_name', 'storage_id', 'storage_name', 'vstore_raw_id', 'vstore_name', 'manufacturer', 'op_lock_enabled', 'notify_enabled', 'offline_file_modes', 'file_extension_filter_enabled', 'abe_enabled', 'page_no', 'page_size', 'sort_key', 'sort_dir', 'namespace_id', 'namespace_name', 'support_provisioning', 'dc_id', 'dc_name'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_show': {
        'func': cifs_share_show,
        'description': '查询指定 CIFS 共享详情',
        'params': ['cifs_share_id'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_create': {
        'func': cifs_share_create,
        'description': '创建单个 CIFS 共享',
        'params': ['create_cifs_param', 'fs_id', 'namespace_id', 'task_remarks'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_modify': {
        'func': cifs_share_modify,
        'description': '修改指定 CIFS 共享',
        'params': ['cifs_share_id', 'description', 'op_lock_enabled', 'notify_enabled', 'ca_enabled', 'offline_file_mode', 'ip_control_enabled', 'abe_enabled', 'audititem_list', 'apply_default_acl', 'file_extension_filter_enabled', 'show_previous_versions_enabled', 'show_snapshot_enabled', 'user_and_user_group_info', 'ip_and_segments', 'file_name_ex_filters', 'task_remarks', 'smb3_encryption_enable', 'unencrypted_access', 'enable_lease'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_delete': {
        'func': cifs_share_delete,
        'description': '批量删除 CIFS 共享',
        'params': ['cifs_share_ids', 'task_remarks'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_show_permissions': {
        'func': cifs_share_show_permissions,
        'description': '查询单个 CIFS 共享的权限列表（用户/IP/文件过滤）',
        'params': ['cifs_share_id', 'type', 'user_filter', 'ip_filter', 'file_filter', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'cifs_share'
    },
    # dataturbo_share 子主题动作
    'dataturbo_share_list': {
        'func': dataturbo_share_list,
        'description': '查询 DataTurbo 共享列表',
        'params': ['page_no', 'page_size', 'raw_id', 'share_path', 'fs_id', 'fs_name', 'dtree_id', 'dtree_name', 'vstore_id', 'vstore_raw_id', 'vstore_name', 'storage_id', 'storage_name', 'zone_id', 'zone_name', 'scope', 'sort_key', 'sort_dir'],
        'subtopic': 'dataturbo_share'
    },
    'dataturbo_share_show': {
        'func': dataturbo_share_show,
        'description': '查询指定 DataTurbo 共享详情',
        'params': ['dataturbo_share_id'],
        'subtopic': 'dataturbo_share'
    },
    'dataturbo_share_create': {
        'func': dataturbo_share_create,
        'description': '创建 DataTurbo 共享',
        'params': ['charset', 'fs_id', 'dtree_id', 'description', 'dataturbo_share_auth', 'task_remarks'],
        'subtopic': 'dataturbo_share'
    },
    'dataturbo_share_modify': {
        'func': dataturbo_share_modify,
        'description': '修改指定 DataTurbo 共享',
        'params': ['dataturbo_share_id', 'description', 'dataturbo_share_auth_addition', 'dataturbo_share_auth_deletion', 'task_remarks'],
        'subtopic': 'dataturbo_share'
    },
    'dataturbo_share_delete': {
        'func': dataturbo_share_delete,
        'description': '批量删除 DataTurbo 共享',
        'params': ['dataturbo_share_ids', 'task_remarks'],
        'subtopic': 'dataturbo_share'
    },
    'dataturbo_share_show_permissions': {
        'func': dataturbo_share_show_permissions,
        'description': '查询 DataTurbo 共享管理员权限列表',
        'params': ['dataturbo_share_id', 'page_no', 'page_size', 'user_id', 'user_name', 'permission'],
        'subtopic': 'dataturbo_share'
    },
    # quota 子主题动作
    'quota_list': {
        'func': quota_list,
        'description': '查询配额列表',
        'params': ['page_no', 'page_size', 'ids', 'raw_ids', 'quota_type', 'parent_type', 'parent_raw_id', 'owner_name', 'vstore_id', 'vstore_raw_id', 'storage_id', 'sort_key', 'sort_dir', 'zone_id'],
        'subtopic': 'quota'
    },
    'quota_show': {
        'func': quota_show,
        'description': '查询指定配额详情',
        'params': ['quota_id'],
        'subtopic': 'quota'
    },
    'quota_create': {
        'func': quota_create,
        'description': '创建配额',
        'params': ['parent_id', 'parent_type', 'quota_type', 'space_soft_quota', 'space_hard_quota', 'space_advisory_quota', 'file_soft_quota', 'file_hard_quota', 'file_advisory_quota', 'snap_space_switch', 'soft_grace_time', 'quota_owner', 'dir_quota_target', 'task_remarks'],
        'subtopic': 'quota'
    },
    'quota_modify': {
        'func': quota_modify,
        'description': '更新指定配额',
        'params': ['quota_id', 'space_soft_quota', 'space_hard_quota', 'space_advisory_quota', 'file_soft_quota', 'file_hard_quota', 'file_advisory_quota', 'snap_space_switch', 'soft_grace_time', 'task_remarks'],
        'subtopic': 'quota'
    },
    'quota_delete': {
        'func': quota_delete,
        'description': '批量删除配额',
        'params': ['quota_ids', 'task_remarks'],
        'subtopic': 'quota'
    },
    # filesystem 子主题动作
    'filesystem_list': {
        'func': filesystem_list,
        'description': '批量查询文件系统',
        'params': ['page_no', 'page_size', 'sort_dir', 'sort_key', 'name', 'fs_raw_id', 'storage_id'],
        'subtopic': 'filesystem'
    },
    'filesystem_show': {
        'func': filesystem_show,
        'description': '查询指定文件系统详情',
        'params': ['filesystem_id'],
        'subtopic': 'filesystem'
    },
    'filesystem_delete': {
        'func': filesystem_delete,
        'description': '批量删除文件系统',
        'params': ['filesystem_ids', 'task_remarks'],
        'subtopic': 'filesystem'
    },
    'filesystem_batch_modify': {
        'func': filesystem_batch_modify,
        'description': '批量修改文件系统（支持批量修改名称）',
        'params': ['filesystems', 'task_remarks'],
        'subtopic': 'filesystem'
    },
    'filesystem_create': {
        'func': filesystem_create,
        'description': '自定义创建文件系统',
        'params': ['storage_id', 'pool_raw_id', 'filesystem_specs', 'vstore_id', 'zone_id', 'task_remarks', 'gfs_group_id', 'automatic_update_time', 'atime_update_mode', 'schedule_name', 'quota_switch', 'vaai_switch', 'initial_distribute_policy', 'capacity_threshold'],
        'subtopic': 'filesystem'
    },
    'filesystem_query_available': {
        'func': filesystem_query_available,
        'description': '查询可用的文件系统（支持远程复制）',
        'params': ['feature_type', 'local_storage_id', 'remote_storage_id', 'name', 'page_no', 'page_size', 'sort_key', 'sort_dir'],
        'subtopic': 'filesystem'
    },
    'filesystem_modify': {
        'func': filesystem_modify,
        'description': '修改指定文件系统（完整参数）',
        'params': ['file_system_id', 'name', 'description', 'capacity', 'capacity_threshold', 'initial_distribute_policy', 'automatic_update_time', 'atime_update_mode', 'quota_switch', 'vaai_switch', 'owning_controller', 'task_remarks'],
        'subtopic': 'filesystem'
    },
    # namespace 子主题动作
    'namespace_list': {
        'func': namespace_list,
        'description': '批量查询命名空间',
        'params': ['page_no', 'page_size', 'sort_dir', 'sort_key', 'name', 
                   'vstore_name', 'vstore_raw_id', 'vstore_id', 'raw_id',
                   'pool_name', 'storage_id', 'enable_encrypt', 
                   'support_provisioning', 'gfs_id', 'gfs_name', 'has_gfs'],
        'subtopic': 'namespace'
    },
    'namespace_show': {
        'func': namespace_show,
        'description': '查询指定命名空间详情',
        'params': ['namespace_id'],
        'subtopic': 'namespace'
    },
    'namespace_create': {
        'func': namespace_create,
        'description': '批量创建命名空间',
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
        'description': '修改指定命名空间',
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
        'description': '批量删除命名空间',
        'params': ['namespace_ids', 'task_remarks'],
        'subtopic': 'namespace'
    },
    # dataturbo 子主题动作（原 dpc 子主题，重命名）
    'dpc_list': {
        'func': dpc_list,
        'description': '批量查询并行客户端列表',
        'params': ['ids', 'hostname', 'ip', 'mgmt_status', 'status', 'sn', 'storage_id', 'dpc_om_id', 'dpc_type', 'client_version', 'page_no', 'page_size'],
        'subtopic': 'dataturbo'
    },
    'dpc_show': {
        'func': dpc_show,
        'description': '查询并行客户端详情',
        'params': ['dpc_id'],
        'subtopic': 'dataturbo'
    },
    # dpc 子主题动作 (DPC客户端)
    'list': {
        'func': dpc_client_list,
        'description': '批量查询DPC客户端',
        'params': ['storage_id', 'process_id', 'name', 'manage_ip', 'version', 'status', 'switch_status', 'upgrade_flag', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'dpc'
    },
    'show': {
        'func': dpc_client_show,
        'description': '查询DPC客户端详情',
        'params': ['id'],
        'subtopic': 'dpc'
    },
    # kvcache 子主题动作
    'kvcache_list': {
        'func': kvcache_list,
        'description': '查询 KV Cache 库',
        'params': ['storage_id', 'id', 'raw_id', 'name', 'zone_id', 'pool_raw_id', 'vstore_id', 'vstore_name', 'fs_id', 'fs_name', 'data_cleanup_switch', 'page_no', 'page_size', 'sort_dir', 'sort_key'],
        'subtopic': 'kvcache'
    },
    'kvcache_batch_create': {
        'func': kvcache_batch_create,
        'description': '批量创建 KV Cache 库',
        'params': ['storage_id', 'zone_id', 'pool_raw_id', 'vstore_id', 'kv_cache_stores', 'data_cleanup_switch', 'max_survival_time'],
        'subtopic': 'kvcache'
    },
    'kvcache_modify': {
        'func': kvcache_modify,
        'description': '修改 KV Cache 库',
        'params': ['kv_cache_stores_id', 'name', 'description', 'data_cleanup_switch', 'max_survival_time'],
        'subtopic': 'kvcache'
    },
    'kvcache_batch_delete': {
        'func': kvcache_batch_delete,
        'description': '批量删除 KV Cache 库',
        'params': ['ids'],
        'subtopic': 'kvcache'
    },
}
