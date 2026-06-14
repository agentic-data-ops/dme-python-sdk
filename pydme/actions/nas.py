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
            dpcs: DPC list (List<DpcInfo>)。 parameter format：[{
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
            data: DPC client data (List<DpcClient>)。 parameter format：[{
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
            dtrees: Dtree list (List<DtreeInfo>)。 parameter format：[{
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
        create_dtrees_param: Dtree name and count list (Conditionally Required)。 parameter format：[{
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
        dataturbo_share: Create DataTurbo share (Optional)。 parameter format：{
                description: DataTurbo share description (Optional, 0~255 characters),
                charset: Character set encoding (Required, fixed value UTF_8),
                dpc_share_auth: DataTurbo admin list (Optional)。 parameter format：[{
                        dpc_user_id: DataTurbo admin ID (Required, 0~64 characters),
                        permission: DataTurbo admin permission (Required, fixed value read_and_write),
                     }, ...]
             }
        create_worm_param: WORM configuration (Optional)。 parameter format：{
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
# NFS  sharesubtopic actions
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
     query NFS  share list

    Args:
        client: DME API Client
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
            nfs_shares: NFS share list。 parameter format：[{
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
        create_nfs_share_param: NFS share creation parameters。 parameter format：{
                name: NFS share alias (Optional),
                description: Description (Optional),
                share_path: Share path (Required),
                character_encoding: Character encoding (Optional),
                audit_items: Audit event list (Optional)。 parameter format：[{
                        audititem: Audit event type. Options: none, all, open, create, read, write, close, delete, rename, get_security, set_security, get_attr, set_attr,
                     }, ...],
                show_snapshot_enable: Show snapshot (Optional). Options: true, false,
                nfs_share_client_addition: NFS share client permissions (Optional)。 parameter format：[{
                        name: Client IP, hostname, or netgroup name (Required, 1~255 chars; netgroup starts with @),
                        permission: Permission (Required). Options: read, read_and_write, no_permission, read_and_write_not_del_rename,
                        accesskrb5: krb5 permission (Optional). Options: read, read_and_write, no_permission, read_and_write_not_del_rename,
                        accesskrb5i: krb5i permission (Optional). Options: read, read_and_write, no_permission, read_and_write_not_del_rename,
                        accesskrb5p: krb5p permission (Optional). Options: read, read_and_write, no_permission, read_and_write_not_del_rename,
                        write_mode: Write mode (Optional). Options: synchronization, asynchronization,
                        permission_constraint: Permission constraint (Required). Options: all_squash, no_all_squash,
                        root_permission_constraint: Root permission constraint (Required). Options: root_squash, no_root_squash,
                        source_port_verification: Source port verification (Optional). Options: secure, insecure,
                        anonymous_user_id: Anonymous userID (Optional),
                        access_protocol: Access protocol (Optional)。Options：nfsv3_and_nfsv4 (NFSv3和NFSv4), nfsv3 (仅NFSv3), nfsv4 (仅NFSv4),
                     }, ...],
                file_name_extension_filters: File extensionFilter rule list (Optional)。 parameter format：[{
                        file_name_ex_id_in_storage: rule on storageID (Optional, 1~64 character, when changing added rulesRequired),
                        file_name_extension: File extension (Required, 1~127 character, supports wildcards?和*, *must be at the last character),
                        rule_type:  rule允许/ reject (Optional, defaultreject)。Options：reject, permit,
                        fileoperations: Operation type list (Optional)。Options：close, create, create_dir, delete, delete_dir, getattr, link, lookup, open, read, write, rename, rename_dir, setattr, symlink,
                     }, ...],
                fs_id: Filesystem的id (与namespace_idmutually exclusive),
                namespace_id: Namespace的id (与fs_idmutually exclusive),
             }
        task_remarks: Async taskRemark

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Modify NFS  share

    Args:
        client: DME API Client
        nfs_share_id: NFS  share ID
        description: Description
        character_encoding:  character编码，Options：utf-8, zh, gbk 等
        audit_items: Audit event list (Optional)。 parameter format：[{
                audititem: Audit event type。Options：none (无操作), all ( all operations), open ( open), create (create ), read (读), write (写), close ( disable), delete (delete ), rename (重命名), get_security (Get security attribute), set_security (Set security attribute), get_attr (get), set_attr (设置),
             }, ...]
        show_snapshot_enable: Show snapshot
        nfs_share_client_addition:  need add的 NFS Share client list (Optional)。 parameter format：[{
                name: ClientIPor hostname or netgroup name (Required, 1~255 character),
                permission:  permission (Required)。Options：read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5: krb5 permission (Optional)。Options：read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5i: krb5i permission (Optional)。Options：read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5p: krb5p permission (Optional)。Options：read, read_and_write, no_permission, read_and_write_not_del_rename,
                write_mode: Write mode (Optional)。Options：synchronization (Sync), asynchronization (异步),
                permission_constraint: Permission constraint (Required)。Options：all_squash, no_all_squash,
                root_permission_constraint: rootPermission constraint (Required)。Options：root_squash, no_root_squash,
                source_port_verification: Source port verification (Optional)。Options：secure (安全), insecure (不安全),
                anonymous_user_id: Anonymous userID (Optional, 0~4294967294),
             }, ...]
        nfs_share_client_modification:  needmodify 的 NFS Share client list (Optional)。 parameter format：[{
                nfs_share_client_id_in_storage: Client on storageID (Required, 1~32 character),
                permission:  permission (Required)。Options：read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5: krb5 permission (Optional)。Options：read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5i: krb5i permission (Optional)。Options：read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5p: krb5p permission (Optional)。Options：read, read_and_write, no_permission, read_and_write_not_del_rename,
                write_mode: Write mode (Optional)。Options：synchronization (Sync), asynchronization (异步),
                permission_constraint: Permission constraint (Required)。Options：all_squash, no_all_squash,
                root_permission_constraint: rootPermission constraint (Required)。Options：root_squash, no_root_squash,
                source_port_verification: Source port verification (Optional)。Options：secure (安全), insecure (不安全),
                anonymous_user_id: Anonymous userID (Optional, 0~4294967294),
             }, ...]
        nfs_share_client_deletion:  needdelete 的 NFS Share client list (Optional)。 parameter format：[{
                nfs_share_client_id_in_storage: Client on storageID (Required, 1~32 character),
                name: ClientIPor hostname or netgroup name (Optional, 1~32000 character),
             }, ...]
        file_name_ex_filters: 扩展名Filter rule list (Optional)。 parameter format：[{
                update_type: Change type (Optional, defaultadd)。Options：add ( add), delete (delete ), modify (modify ),
                param: Extension filter rule。 format：{
                        file_name_ex_id_in_storage: rule on storageID (Optional, 1~64 character, modify 时Required),
                        file_name_extension: File extension (Required, 1~127 character, supports wildcards?和*, *can only be at the end),
                        rule_type:  rule允许/ reject (Optional, defaultreject)。Options：reject ( reject), permit (允许),
                        fileoperations: Operation type list (Optional)。Options：close, create, create_dir, delete, delete_dir, getattr, link, lookup, open, read, write, rename, rename_dir, setattr, symlink,
                }
             }, ...]
        task_remarks: Async taskRemark

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Batch delete NFS  share

    Args:
        client: DME API Client
        nfs_share_ids: 待delete  NFS  share ID  list
        task_remarks: Async taskRemark

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
        offline_file_modes: Offline cache mode list (Optional), List<OfflineFileMode> type, max array members 4。 parameter format：[{
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
        create_cifs_param: CIFS share creation parameters。 parameter format：{
                name: Share name (Required),
                description: Description (Optional),
                share_path: Share path (Required),
                op_lock_enabled: Oplock switch (Optional),
                notify_enabled: Notify switch (Optional),
                ca_enabled: Failover continuous availability switch (Optional),
                offline_file_mode: Offline cache mode (Optional). Options: none, manual, documents, programs,
                ip_control_enabled: IP access control switch (Optional),
                abe_enabled: ABE switch (Optional),
                audititem_list: Audit event list (Optional)。 parameter format：[{
                        audititem: Audit event type (default none). Options: none, all, open, create, read, write, close, delete, rename, get_security, set_security, get_attr, set_attr, get_xattr, set_xattr,
                     }, ...],
                apply_default_acl: Apply default ACL (Optional),
                file_extension_filter_enabled: File extension filter enabled (Optional),
                show_previous_versions_enabled: Show previous versions enabled (Optional),
                show_snapshot_enabled: Show snapshot enabled (Optional),
                user_and_user_group_info: User and user group list (Optional)。 parameter format：[{
                        user_or_user_group_id_in_storage: user or user group on storageid (Optional, 1~64 character,  when changingRequired),
                        user_or_user_group_name: Username or group name (Optional, 1~255 character; Group name with prefix@),
                        domain_type: 域 type (Optional, defaultlocal)。Options：ad_domain, ldap_domain, local, nis_domain,
                        permission:  permission (Optional, defaultread)。Options：read, full_control, forbidden, read_and_write, read_and_write_not_del_rename,
                     }, ...],
                ip_addresses_and_segments: IP address和IP address段 list (Optional)。 parameter format：[{
                        ip_or_segments_id_in_storage: IP address(段)on storageID (Optional, 1~64 character,  when changingRequired),
                        ip_addresses_or_segments: IP address(段) (Optional, 1~128 character,  max32条),
                     }, ...],
                file_name_extension_filters: File extensionFilter rule list (Optional)。 parameter format：[{
                        file_name_ex_id_in_storage: rule on storageID (Optional, 1~64 character, when changing added rulesRequired),
                        file_name_extension: File extension (Required, 1~127 character, supports wildcards?和*),
                        rule_type:  rule type (Optional, defaultreject)。Options：reject, permit,
                        fileoperations: Operation type list (Optional),
                     }, ...],
                smb3_encryption_enable: EnableSMB3Encryption feature (Optional),
                unencrypted_access: Allow unencrypted client access (Optional),
                enable_lease: Enable lease locking (Optional),
             }
        fs_id: Filesystem的 ID，与 namespace_id mutually exclusive
        namespace_id: Namespace的 ID，与 fs_id mutually exclusive
        task_remarks: Async taskRemark

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Modify CIFS  share

    Args:
        client: DME API Client
        cifs_share_id: CIFS  share ID
        description: Description， max 255  characters
        op_lock_enabled: Oplock Feature switch
        notify_enabled: Notify Feature switch
        ca_enabled: Failover Continuous availability feature switch
        offline_file_mode: offlineCache mode，none/manual/documents/programs
        ip_control_enabled: IP Access control feature switch
        abe_enabled: ABE Feature switch
        audititem_list: Supported audit event list (Optional)。 parameter format：[{
                audititem: Audit event type (defaultnone)。Options：none, all, open, create, read, write, close, delete, rename, get_security, set_security, get_attr, set_attr, get_xattr, set_xattr,
             }, ...]
        apply_default_acl: Add default ACL
        file_extension_filter_enabled: EnableFile extension filter特性
        show_previous_versions_enabled: EnableShow previous versions feature
        show_snapshot_enabled: Enable显示 Snapshot 的功能
        user_and_user_group_info: user 和User group list (Optional)。 parameter format：[{
                update_type: Change type (Optional, defaultadd)。Options：add ( add), delete (delete ), modify (modify ),
                param: user 和User group infoobject (Optional)。 format：{
                        user_or_user_group_id_in_storage: user or user group on storageid (Optional, 1~64 character,  when changingRequired),
                        user_or_user_group_name: Username or group name (Optional, 1~255 character; Group name with prefix@),
                        domain_type: 域 type (Optional, defaultlocal)。Options：ad_domain, ldap_domain, local, nis_domain,
                        permission:  permission (Optional, defaultread)。Options：read, full_control, forbidden, read_and_write, read_and_write_not_del_rename,
                }
             }, ...]
        ip_and_segments: IP address和IP address段 list (Optional)。 parameter format：[{
                update_type: Change type (Optional, defaultadd)。Options：add ( add), delete (delete ), modify (modify ),
                param: IP address和IP address段 infoobject (Optional)。 format：{
                        ip_or_segments_id_in_storage: IP address(段)on storageID (Optional, 1~64 character,  when changingRequired),
                        ip_addresses_or_segments: IP address(段) (Optional, 1~128 character,  max32条),
                }
             }, ...]
        file_name_ex_filters: 扩展名Filter rule list (Optional)。 parameter format：[{
                update_type: Change type (Optional, defaultadd)。Options：add ( add), delete (delete ), modify (modify ),
                param: Extension filter ruleobject (Optional)。 format：{
                        file_name_ex_id_in_storage: rule on storageID (Optional, 1~64 character, when changing added rulesRequired),
                        file_name_extension: File extension (Required, 1~127 character, supports wildcards?和*, *must be at the last character),
                        rule_type:  rule type (Optional, defaultreject)。Options：reject ( reject), permit (允许),
                        fileoperations: Operation type list (Optional,  max100个),
                }
             }, ...]
        task_remarks: Async taskRemark，0~1024  characters
        smb3_encryption_enable: Enable SMB3 Encryption feature
        unencrypted_access: Allow unencrypted client access
        enable_lease: Enable lease locking

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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

        user_filter: User permission filter (Optional, dict type, effective when type=user)。 parameter format：{
                user_or_user_group_name: User/group name (Optional), 1~256 characters,
                domain_type: Domain type (Optional). Options: ad_domain, ldap_domain, local, nis_domain,
                permissions: Permission filter list (Optional), List<Permission> type, max array members 4。 parameter format：[{
                        permission: Permission (Optional). Options: read, full_control, forbidden, read_and_write, read_and_write_not_del_rename. Default read,
                },...],
                user_or_user_group_raw_id: User/group ID on storage device (Optional), 1~256 characters,
        }

        ip_filter: IP permission filter (Optional, dict type, effective when type=ip)。 parameter format：{
                ip_addresses_or_segments: IP address/segment (Optional), 1~256 characters,
                ip_or_segments_raw_id: IP address/segment ID on storage device (Optional), 1~256 characters,
        }

        file_filter: File extension filter (Optional, dict type, effective when type=file)。 parameter format：{
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

    #  based on type parameter to query matching permission type
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

    # If type is specified, return only that type
    if type == 'user':
        return {'user_permissions': result['user']}
    elif type == 'ip':
        return {'ip_permissions': result['ip']}
    elif type == 'file':
        return {'file_permissions': result['file']}
    else:
        # Return all permissions
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
    Query DataTurbo share list

    Args:
        client: DME API client
        page_no: Page number (Optional), 1~10000000, default 1
        page_size: Items per page (Optional), 1~1000, default 10
        raw_id: DataTurbo share ID on device (Optional), 1~1024 characters, exact match
        share_path: Share path (Optional), 1~1024 characters, supports fuzzy search
        fs_id: Filesystem ID (Optional), 1~64 characters, exact match
        fs_name: Filesystem name (Optional), 1~256 characters, supports fuzzy search
        dtree_id: Dtree ID (Optional), 32 characters, regex ^[A-F0-9]{32}$, exact match
        dtree_name: Dtree name (Optional), 1~256 characters, supports fuzzy search
        vstore_id: Tenant ID (Optional), 1~64 characters, exact match
        vstore_raw_id: Tenant RAW ID (Optional), 1~64 characters, exact match
        vstore_name: Tenant name (Optional), 1~256 characters, supports fuzzy search
        storage_id: Storage device ID (Optional), 1~64 characters, exact match
        storage_name: Storage device name (Optional), 1~256 characters, supports fuzzy search
        zone_id: Zone ID (Optional), 1~64 characters, exact match
        zone_name: Zone name (Optional), 1~256 characters, supports fuzzy search
        scope: Resource scope (Optional). Options: local_scale, global_scale
        sort_key: Sort field (Optional). Options: raw_id
        sort_dir: Sort direction (Optional). Options: asc (ascending), desc (descending), default asc

    Returns:
        DataTurbo share list
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
    Query DataTurbo share details

    Args:
        client: DME API client
        dataturbo_share_id: DataTurbo share ID

    Returns:
        DataTurbo share details
    """
    url = "/rest/fileservice/v1/dpc-shares/{dataturbo_share_id}"

    response = client.get(url, params={"dataturbo_share_id": dataturbo_share_id})
    return response


def dataturbo_share_create(client: DMEAPIClient, charset: str, fs_id: str = None,
                     dtree_id: str = None, description: str = None,
                     dataturbo_share_auth: list = None, task_remarks: str = None) -> dict:
    """
    Create DataTurbo share

    Args:
        client: DME API client
        charset: Character set encoding, fixed value UTF_8
        fs_id: Filesystem ID to share, mutually exclusive with dtree_id, one required
        dtree_id: Dtree ID to share, mutually exclusive with fs_id, one required
        description: DataTurbo share description
        dataturbo_share_auth: DataTurbo admin list (Optional)。 parameter format：[{
                dpc_user_id: DataTurbo admin ID (Required, 1~64 characters),
                permission: DataTurbo admin permission (Required, fixed value read_and_write),
             }, ...]
        task_remarks: Async task remark

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Modify DataTurbo share

    Args:
        client: DME API client
        dataturbo_share_id: DataTurbo share ID
        description: DataTurbo share description
        dataturbo_share_auth_addition: DataTurbo admin list to add (Optional)。 parameter format：[{
                dpc_user_id: DataTurbo admin ID (Required, 0~64 characters),
                permission: DataTurbo admin permission (Required, fixed value read_and_write),
             }, ...]
        dataturbo_share_auth_deletion: DataTurbo admin ID list to delete
        task_remarks: Async taskRemark

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Batch delete DataTurbo  share

    Args:
        client: DME API Client
        dataturbo_share_ids: DataTurbo  share ID  list
        task_remarks: Async taskRemark

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
     query DataTurbo  shareAdminPermission list

    Args:
        client: DME API Client
        dataturbo_share_id: DataTurbo  share ID
        page_no: Page number(Optional），1~10000000，default 1
        page_size: Items per page(Optional），1~1000，default 10
        user_id: DataTurbo Admin ID(Optional），1~64  characters，exact match
        user_name: DataTurbo Admin name(Optional），1~256  characters， supportfuzzy search
        permission: DataTurbo Admin permission(Optional），Options：read_and_write (read/write)

    Returns:
        DataTurbo  shareAdminPermission list
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
# Quota subtopic functions
# ============================================================================

def quota_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 20,
               ids: list = None, raw_ids: list = None, quota_type: str = None,
               parent_type: str = None, parent_raw_id: str = None,
               owner_name: str = None, vstore_id: str = None,
               vstore_raw_id: str = None, storage_id: str = None,
               sort_key: str = None, sort_dir: str = None,
               zone_id: str = None) -> dict:
    """
    Query quota list

    Args:
        client: DME API client
        page_no: Page number (Optional), min 1, default 1
        page_size: Items per page (Optional), 1~1000, default 20
        ids: Quota ID list (Optional), List<string> type, max array members 100
        raw_ids: Quota ID list on storage device (Optional), List<string> type, 0~1024 characters, max array members 100
        quota_type: Quota type (Optional). Options: directory_quota, user_quota, user_group_quota
        parent_type: Parent object type (Optional), 0~32 characters. Options: filesystem, qtree
        parent_raw_id: Parent object ID on storage device (Optional), 0~256 characters, exact match
        owner_name: Quota owner name (Optional), 0~256 characters, supports fuzzy search
        vstore_id: Tenant ID (Optional), 0~64 characters
        vstore_raw_id: Tenant ID on storage device (Optional), 0~256 characters, exact match
        storage_id: Storage device ID (Optional), 0~64 characters
        sort_key: Sort field (Optional). Options: id, space_hard_used_rate, file_hard_used_rate, default id
        sort_dir: Sort direction (Optional). Options: asc (ascending), desc (descending), default asc
        zone_id: Zone id (Optional), 0~64 characters, OceanStor A800 only

    Returns:
        Quota list
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
    Query quota details

    Args:
        client: DME API client
        quota_id: Quota ID

    Returns:
        Quota details
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
    Create quota

    Args:
        client: DME API client
        space_soft_quota: Space soft quota (Optional), in Bytes, default -1 (invalid); space hard quota must be greater than soft when both valid; must be multiple of 1048576 for OceanStor V5
        space_hard_quota: Space hard quota (Optional), in Bytes, default -1 (invalid); must be greater than soft quota when both valid; must be multiple of 1048576 for OceanStor V5
        space_advisory_quota: Space advisory quota (Optional), in Bytes, default -1 (invalid); OceanStor Pacific only; must be less than hard/soft quota
        file_soft_quota: File soft quota (Optional), default -1 (invalid); file hard quota must be greater than soft when both valid
        file_hard_quota: File hard quota (Optional), default -1 (invalid); must be greater than soft quota when both valid
        file_advisory_quota: File advisory quota (Optional), default -1 (invalid); OceanStor Pacific only; must be less than hard/soft quota
        snap_space_switch: Include snapshot space (Optional), default false; OceanStor Pacific only
        soft_grace_time: Grace period (Optional), 0~4294967294, in days; OceanStor Pacific only
        parent_id: Parent resource ID (Required), 1~64 characters
        parent_type: Parent resource type (Required). Options: filesystem, dtree, namespace
        quota_type: Quota type (Required). Options: directory_quota, user_quota, user_group_quota
        quota_owner: Quota owner (Conditionally Required), QuotaOwner object。 parameter format：{
                        name: User (group) name (Required), 1~64 characters, * = all users (groups),
                        type: User (group) type (Required). Options: unix_local_user, domain_user, windows_user (for user_quota); unix_local_user_group, domain_user_group, windows_user_group (for user_group_quota),
                        domain_type: Domain user type (Conditionally Required). Options: local, ad_domain, ldap_domain, nis_domain,
        }
        dir_quota_target: Directory quota target (Optional). Options: dtree, filesystem; effective when parent is filesystem and quota_type is directory_quota
        task_remarks: Async task remark

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Update specified quota

    Args:
        client: DME API Client
        quota_id:  quota ID
        space_soft_quota: 空间软 quota(Optional），unit  Byte，-1 field is invalid；When both space hard/soft quotas arewhen both valid，Hard quota must exceed soft quota
        space_hard_quota: 空间硬 quota(Optional），unit  Byte，-1 field is invalid；When both space hard/soft quotas arewhen both valid，Hard quota must exceed soft quota
        space_advisory_quota: Space advisory quota(Optional），unit  Byte，-1 field is invalid；仅 OceanStor Pacific Device support；When advisory quota and hard/soft quotawhen both valid，Advisory quota must be less than hard or soft quota
        file_soft_quota: File soft quota(Optional），-1 field is invalid；When both file hard/soft quotas arewhen both valid，File hard quota must exceed soft quota
        file_hard_quota: File hard quota(Optional），-1 field is invalid；When both file hard/soft quotas arewhen both valid，File hard quota must exceed soft quota
        file_advisory_quota: File advisory quota(Optional），-1 field is invalid；仅 OceanStor Pacific Device support；When advisory quota and hard/soft quotawhen both valid，Advisory quota must be less than hard or soft quota
        snap_space_switch: Include snapshot space(Optional），true：Include snapshot space；false：Exclude snapshot space；仅 OceanStor Pacific Device support
        soft_grace_time: 超限时间(Optional），0~4294967294，unit （day(s)）；Grace period before soft limit becomes hard limit；not sent或 value 0 soft quota reached, warning only；仅 OceanStor Pacific  support
        task_remarks: Async taskRemark

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Batch delete quota

    Args:
        client: DME API Client
        quota_ids: Quota to delete ID  list
        task_remarks: Async taskRemark

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
# Filesystem subtopic functions
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
    Batch queryFilesystem

    Args:
        client: DME API Client
        page_no: Page number(Optional），1~10000000
        page_size: Items per page(Optional），1~1000，default 100
        sort_dir:  specifiedSort direction(Optional），Options：asc（ascending）、desc（descending）
        sort_key: Sort key(Optional），Options：capacity, available_capacity, capacity_usage_ratio,
                  nfs_count, cifs_count, dpc_count, dtree_count, name, allocate_pool_quota,
                  fs_raw_id, create_time, total_capacity_in_byte, available_capacity_in_byte,
                  alloc_capacity_in_byte, protection_capacity_in_byte, max_file_count, used_file_count
        name: Filesystem name(Optional），1~256  characters，与 fs_raw_id mutually exclusive， supportfuzzy match
        is_associated_qos: Filesystem whether已 associated QoS(Optional），true：是；false：否
        qos_id: QoS  policy ID(Optional），1~256  characters
        storage_name: FilesystemDevice name(Optional），1~256  characters，与 storage_id mutually exclusive， supportfuzzy match
        manufacturer: Storage device vendor(Optional），1~64  characters；Options：huawei（Huawei）、dell_emc（DELL EMC）、
                     fujitsu（FUJITSU）、hitachi（Hitachi）、hpe（HPE）、ibm（IBM）、netapp（NetApp）、
                     pure（PURE）、panji（Panji）、third_part（非华为Storage device）
        storage_pool_name: FilesystemStorage pool name(Optional），1~256  characters，与 storage_pool_id mutually exclusive， supportfuzzy match
        storage_pool_id: Storage pool ID(Optional），1~255  characters，与 storage_pool_name mutually exclusive
        tier_name: FilesystemService level name(Optional），1~256  characters，与 tier_id mutually exclusive， supportfuzzy match
        tier_id: Service level ID(Optional），1~256  characters，与 tier_name mutually exclusive，exact match
        vstore_name: Filesystem vStore  name(Optional），1~256  characters，与 vstore_raw_id mutually exclusive， supportfuzzy match
        vstore_raw_id: FilesystemTenanton the storage device ID(Optional），1~64  characters，与 vstore_name mutually exclusive
        project_name: FilesystemProject group name(Optional），1~256  characters，与 project_id mutually exclusive， supportfuzzy match
        project_id: Project group ID(Optional），1~256  characters，与 project_name mutually exclusive，exact match
        storage_id: Storage device ID(Optional），1~256  characters，与 storage_name mutually exclusive，exact match
        fs_raw_id: Filesystemon the device ID(Optional），1~256  characters，与 name mutually exclusive
        health_status: Health status(Optional），Options：normal (normal)、faulty (fault)、unknown (unknown)
        running_status: Running status(Optional），Options：online (online)、offline (offline)、invalid（失效）、
                       initializing（Initializing）、unknown (unknown)
        alloc_type: FilesystemAllocation type(Optional），Options：thin（ thin provisioning）、thick（Fixed allocation）
        type: Filesystem type(Optional），Options：normal（普通Filesystem）、worm（wormFilesystem）、
              migration（migrationFilesystem）、container（容器 appFilesystem）、hash（哈希Filesystem）、
              smart_mobility_internal（SmartMobility内部Filesystem）
        protection: Protection status(Optional），Options：protected (protected)、not_protected (unprotected)
        dc_id: Data center ID(Optional），1~128  characters, regex ^[_A-Fa-f0-9\\-]+$
        dc_name: Data center name(Optional），1~256  characters
        zone_id:  zone 的 ID(Optional），1~256  characters；仅 OceanStor A800 系列Filesystem support搜索，传入 clusterIDQueries global scopeFilesystem
        product_name: FilesystemDevice product name(Optional），1~256  characters， supportfuzzy search
        description: FilesystemDescription(Optional），1~255  characters
        tag_filters: Tag filter list(Optional），List<TagFilters>  type，max array members 11。 parameter format：[{
                        tag_ids:  tag ID  list(Optional），max array members 10，Tags are OR-related,
                        tag_type_id: Tag type ID(Optional）， regex ^[a-fA-F0-9]{32}$,
                        operator:  filter condition（Required），Options：contain（includes ）、not_contain（不includes ）,
        },...]

    Returns:
        Filesystem list
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
    Query filesystem details

    Args:
        client: DME API client
        filesystem_id: Filesystem ID

    Returns:
        Filesystem details
    """
    url = "/rest/fileservice/v1/filesystems/{filesystem_id}"

    response = client.get(url, params={"filesystem_id": filesystem_id})
    return response


def filesystem_delete(client: DMEAPIClient, filesystem_ids: list, task_remarks: str = None) -> dict:
    """
    Batch delete filesystems

    Args:
        client: DME API client
        filesystem_ids: Filesystem ID list
        task_remarks: Async task remark (Optional)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        } (async task)
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
    Batch modify filesystems

    Only name modification is supported.

    Args:
        client: DME API client
        filesystems: Filesystem info list to modify (Required), List<UpdateFileSystemInfo> type, max array members 1000。 parameter format：[{
                        file_system_id: Filesystem unique ID (Required), 1~64 characters,
                        name: Filesystem name (Required), 1~255 characters,
        },...]
        task_remarks: Async task remark (Optional), 0~1024 characters

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Custom create filesystem

    Args:
        client: DME API client
        storage_id: Storage device ID
        pool_raw_id: Storage pool ID on the storage device
        filesystem_specs: Filesystem spec list。 parameter format：[{
                name: Name (Required, 1~255 characters),
                count: Count (Required, 1~500),
                start_suffix: Starting suffix number (Optional, 0~9999),
                capacity: Capacity in GB (Required, 1~262144),
                description: Description (Optional, 0~255 characters),
             }, ...]
        vstore_id:  tenant ID(Optional）
        zone_id:  zone 的 ID(Optional）
        task_remarks: Async taskRemark(Optional）
        gfs_group_id: Global data space的 ID(Optional）
        automatic_update_time: Update access time(Optional）
        atime_update_mode: Atime  updateFrequency，hour/day/close(Optional）
        schedule_name: 定时 HyperCDP 计划 name(Optional）
        quota_switch: Enable quota(Optional）
        vaai_switch: VAAI  switch(Optional）
        initial_distribute_policy: Initial capacity allocation policy，auto/highest_perf/performance/capacity(Optional）
        capacity_threshold: Total space capacity alarmthreshold 50-99(Optional）
        tuning: 调优 parameter (Optional)。 parameter format：{
                deduplication_enabled: EnableDeduplication (Optional, defaultfalse)。Options：true, false,
                compression_enabled: EnableData compression (Optional, defaultfalse)。Options：true, false,
                block_size: Filesystem块 sizeKB (Optional, default64)。Options：4, 8, 16, 32, 64, 128,
                allocation_type: Allocation type (Optional, defaultthin)。Options：thin, thick,
                qos_policy_id: QoS policyID (Optional),
                application_scenario:  app场景 (Optional, defaultuser_defined)。Options：database, VM, user_defined, container,
                workload_type_id: Application typeid (Optional, 1~32 character),
                dist_alg: FilesystemDirectory dispersion policy (Optional, 仅A800Device support)。Options：capacity_balance, subdirectory_round_robin,
                qos_policy: SmartQosPolicy parameter info (Optional)。 format：{
                        max_bandwidth: Max bandwidthMB/s (Optional, 1~999999999),
                        max_iops:  maxiops (Optional, 1~999999999),
                        min_bandwidth: Min bandwidthMB/s (Optional, 1~999999999),
                        min_iops:  miniops (Optional, 1~999999999),
                        burst_band_width: Burst bandwidthMB/s (Optional),
                        burst_iops: burstIOPS (Optional),
                        burst_time: Max burst timesecond(s) (Optional),
                        latency: 时延 (Optional, 仅保护lower limit support),
                        max_read_bandwidth:  maxRead bandwidthMB/s (Optional),
                        max_write_bandwidth:  maxWrite bandwidthMB/s (Optional),
                        burst_read_band_width: burstRead bandwidthMB/s (Optional),
                        burst_write_band_width: burstWrite bandwidthMB/s (Optional),
                        max_read_iops:  max读iops (Optional),
                        max_write_iops:  max写iops (Optional),
                        burst_read_iops: burst读iops (Optional),
                        burst_write_iops: burst写iops (Optional),
                        schedule_policy: Scheduling policy (Optional)。Options：once, daily, weekly,
                        schedule_start_date: Effective start date (Optional,  formatyyyy-MM-dd),
                        start_time: effectiveStart time (Optional,  formathh:mm),
                        duration: effectivedurationsecond(s) (Optional, 1800~86400),
                        weekly_days: week(s)Scheduling policy (Optional, 1~6 correspondingweek(s)一到week(s)六),
                        alarm_switch: Upper limit alarm switch (Optional)。Options：off, on,
                        alarm_level: Alarm severity (Optional)。Options：event, alarm,
                        alarm_threshold: alarmthreshold% (Optional, 0~100),
                        resume_threshold:  resumethreshold% (Optional, 0~100),
                        storage_divice_id: Storage deviceid (Optional),
                        name: QoS name (Optional),
                        description:  description (Optional),
                        iotype: Policy type (Optional)。Options：2 (总upper limit), 3 (读写upper limit),
                        vstore_id: Tenantid (Optional),
                        vstore_name: Tenant name (Optional),
                        global_flag:  whether global (Optional),
                }
             }
        create_cifs_share_param: Auto-createCIFSShare parameters(Optional）。See action help for format：nas cifs_share create
        create_nfs_share_param: Auto-createNFSShare parameters(Optional）。See action help for format：nas nfs_share create
        create_dpc_share_param: Auto-createDataTurboShare parameters(Optional）。See action help for format：nas dataturbo_share create
        owning_controller: Controller(Optional），2~16 characters， format如0A、1B
        snapshot_expired_enabled: Delete old read-only snapshots(Optional）。true/false，default off
        checksum_enabled: Data verification switch(Optional）。true/false，Enabled by default
        ads_enabled: Enable data flow switching(Optional）。true/false，Enabled by default
        security_mode: Security mode(Optional）。 value：mixed/native/ntfs/unix
        nas_locking_policy: NAS锁 policy(Optional）。 value：mandatory/advisory/unknown
        capacity_autonegotiation: Capacity adaptive parameter (Optional)。 parameter format：{
                capacity_self_adjusting_mode: Auto capacity adjustment mode (Optional, default off)。Options：grow_off ( disable), grow (Auto-expand), grow_shrink ( auto扩缩容),
                capacity_recycle_mode: Capacity reclamation mode (Optional, Default: expand first)。Options：expand_capacity (Expand first), delete_snapshots (Prefer deleting old snapshots),
                auto_size_enable: Auto capacity adjustment switch (Optional, defaulttrue)。Options：true, false,
                auto_grow_threshold_percent: Auto-expand threshold% (Optional, 2~99, default85),
                auto_shrink_threshold_percent: Auto-shrink threshold% (Optional, 1~98, default50),
                max_auto_size: Auto-expandupper limitGB (Optional, 1~33554432, default33554432),
                min_auto_size:  auto缩容lower limitGB (Optional, 1~33554432, default33554432),
                auto_size_increment: Auto resize single change amountMB (Optional, 64~102400, default1024),
             }
        worm: FilesystemWorm parameter (Optional)。 parameter format：{
                type: WORM保护 mode (Optional)。Options：none_mode (无default policy), enterprise_mode (Enterprise compliance), compliance_mode ( legal compliance), advance_mode (高安遵从), audit_log (Audit log), non_worm (非WORM),
                min_protect_period: Min protection period (Optional, default0),
                min_protect_period_unit: Min protection period unit (Optional, defaultyear)。Options：minute, hour, day, month, year,
                max_protect_period: Max protection period (Optional, 0~4294967295, default70),
                max_protect_period_unit: Max protection period unit (Optional, defaultyear)。Options：minute, hour, day, month, year,
                def_protect_period: Default protection period (Optional, 不小于 min, 不greater than max, default70),
                def_protect_period_unit: Default protection period unit (Optional, defaultyear)。Options：minute, hour, day, month, year,
                auto_lock: WORMAuto-lock mode (Optional, Enabled by default)。Options：true, false,
                auto_lock_time: Auto-lock time (Optional, default2),
                auto_lock_time_unit: Auto-lock timeunit  (Optional, defaulthour)。Options：minute, hour, day, month, year,
                auto_del: Auto-delete mode (Optional, default off)。Options：true, false,
                is_worm_audit_log_fs: WORMAudit logFilesystem (Optional, default off)。Options：true, false,
                worm_append_unit: WORMAppend-only file protection granularity (Optional, 仅advance_mode support)。Options：256KB, 512KB, 1M,
             }
        snapshot_reserved_space_percentage: Snapshot reserved space percentage(Optional），0~90
        periodic_snapshots_limit: 定时 snapshotcount limit(Optional），1~2048
        snapshot_dir_visible: Snapshot directory visibility(Optional）。true/false
        object_service_optimization: object service optimization(Optional）。true/false
        case_sensitive: Case-sensitive mode(Optional）。true/false
        audit_log_rules: Audit log rule集合(Optional），如：set_security、get_security、set_attr、get_attr等， max100条
        unix_permissions: Filesystem目录 permission(Optional）， format如0755

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Query available的Filesystem

    Query availablefor configuring add/remove featuresFilesystem。当前only supports可 configRemote replication的Filesystem。

    Args:
        client: DME API Client
        feature_type: 特性 type，当前only supports remote_replication（Remote replication）
        local_storage_id: local Storage device ID
        remote_storage_id: remote Storage device ID（当 feature_type 为 remote_replication 时Required）
        name: local Filesystem name， supportfuzzy search
        page_no: Page number，default 1
        page_size: Items per page，default 20
        sort_key: Sort field，name（Filesystem name）或 capacity（Filesystem capacity）
        sort_dir: Sort direction，asc（ascending）或 desc（descending）

    Returns:
        可用Filesystem list
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
    ModifyFilesystem

    Args:
        client: DME API Client
        file_system_id: FilesystemUnique identifier
        name: Filesystem name，1~255 characters(Optional）
        description: Description，0~255 characters(Optional）
        capacity: Filesystem capacity，unit  GB，1~33554432(Optional）
        capacity_threshold: Total space capacity alarmthreshold 50-99(Optional）
        initial_distribute_policy: Initial capacity allocation policy，auto/highest_perf/performance/capacity(Optional）
        automatic_update_time: Update access time after file read，true enable/false disable(Optional）
        atime_update_mode: Atime  updateFrequency，hour（每hour(s)）/day（每day(s)）/close（not enabled）(Optional）
        quota_switch: Enable quota，true enable/falsedisabled(Optional）
        vaai_switch: VAAI  switch，Cannot be disabled once enabled，true enable/falsenot enabled(Optional）
        owning_controller: Controller，2~16 characters(Optional）
        snapshot_expired_enabled: Delete old read-only snapshots，true enable/false disable(Optional）
        checksum_enabled: Data verification switch，true enable/false disable(Optional）
        ads_enabled: Enable data flow switching，true enable/false disable，Cannot be disabled once enabled(Optional）
        security_mode: Security mode，mixed/native/ntfs/unix(Optional）
        nas_locking_policy: NAS锁 policy，mandatory（强制锁）/advisory（建议锁）/unknown(Optional）
        snapshot_reserved_space_percentage: Snapshot reserved space percentage，0~90(Optional）
        periodic_snapshots_limit: 定时 snapshotcount limit，1~2048(Optional）
        snapshot_dir_visible: Snapshot directory visibility，true可见/false invisible(Optional）
        tuning: 调优 parameter (Optional)。 parameter format：{
                qos_policy: SmartQosPolicy parameter info (UpdateFileSystemQosPolicyobject)。 format：{
                        max_bandwidth: Max bandwidthMB/s (Optional, 1~999999999; 与min_bandwidth/min_iopsmutually exclusive, A800 not undermutually exclusive),
                        max_iops: Max IOPS (Optional, 1~999999999; 与min_bandwidth/min_iopsmutually exclusive, A800 not undermutually exclusive),
                        min_bandwidth: Min bandwidthMB/s (Optional, 1~999999999; 与max_bandwidth/max_iopsmutually exclusive, A800 not undermutually exclusive),
                        min_iops: Min IOPS (Optional, 1~999999999; 与max_bandwidth/max_iopsmutually exclusive, A800 not undermutually exclusive),
                        burst_band_width: Burst bandwidthMB/s (Optional, 1~999999999),
                        burst_iops: burstIOPS (Optional, 1~999999999),
                        burst_time: Max burst timesecond(s) (Optional, 1~999999999),
                        latency: 时延 (Optional, 1~999999999; A800/Dorado V6可选500/1500unit us, V3/V5Customizable unitms),
                        max_read_bandwidth:  maxRead bandwidthMB/s (Optional, 1~999999999; read/write upper limit policy only),
                        max_write_bandwidth:  maxWrite bandwidthMB/s (Optional, 1~999999999; read/write upper limit policy only),
                        burst_read_band_width: burstRead bandwidthMB/s (Optional, 1~999999999; read/write upper limit policy only),
                        burst_write_band_width: burstWrite bandwidthMB/s (Optional, 1~999999999; read/write upper limit policy only),
                        max_read_iops:  maxRead IOPS (Optional, 1~999999999; read/write upper limit policy only),
                        max_write_iops:  maxWrite IOPS (Optional, 1~999999999; read/write upper limit policy only),
                        burst_read_iops: burstRead IOPS (Optional, 1~999999999; read/write upper limit policy only),
                        burst_write_iops: burstWrite IOPS (Optional, 1~999999999; read/write upper limit policy only),
                        schedule_policy: Scheduling policy (Optional)。Options：once, daily, weekly,
                        schedule_start_date: Effective start date (Optional,  formatyyyy-MM-dd, 0~64 character),
                        start_time: effectiveStart time (Optional,  formathh:mm, 0~64 character),
                        duration: effectivedurationsecond(s) (Optional, 1800~86400),
                        weekly_days: week(s)Scheduling policy (Optional, 0-6 correspondingweek(s)日到week(s)六,  max7个; schedule_policy为weekly时effective),
                        alarm_switch: Upper limit alarm switch (Optional)。Options：off, on,
                        alarm_level: 限高Alarm severity (Optional)。Options：event ( event), alarm (alarm),
                        alarm_threshold: 限高alarmthreshold% (Optional, 0~100),
                        resume_threshold: 限高Alarm recoverythreshold% (Optional, 0~100),
                        storage_divice_id: Storage device ID (Optional, 1~64 character),
                        name: QoS name (Optional, 1~255 character; A800unused under),
                        description: QoS description (Optional, 1~255 character; A800unused under),
                        iotype: Policy type (Optional)。Options：2 (总性能upper limit), 3 (读写upper limit; only supported by some devices),
                        vstore_id: Tenant ID (Optional, 1~64 character; A800unused under),
                        vstore_name: Tenant name (Optional, 1~64 character; A800unused under),
                        global_flag:  whether global (Optional; Current version only supports global; A800unused under),
                        qos_policy_id: QoS policyID (Optional, 0~64 character; 与除enabledother parameters exceptmutually exclusive),
                        enabled: EnableQoSPolicy (Optional, defaultfalse),
                },
                deduplication_enabled: Deduplication (Optional, default off),
                compression_enabled: Data compression (Optional, default off),
                allocation_type: FilesystemAllocation type (Optional, defaultthin)。Options：thin (精简), thick (厚),
             }
        capacity_autonegotiation: Capacity adaptive parameter (Optional)。 parameter format：{
                capacity_self_adjusting_mode: Auto capacity adjustment mode (Optional, default off)。Options：grow_off ( disable), grow (Auto-expand), grow_shrink ( auto扩缩容),
                capacity_recycle_mode: Capacity reclamation mode (Optional, Default: expand first)。Options：expand_capacity (Expand first), delete_snapshots (Prefer deleting old snapshots),
                auto_size_enable: Auto capacity adjustment switch (Optional, default open)。Options：true, false,
                auto_grow_threshold_percent: Auto-expand threshold% (Optional, 2~99, default85; must be greater thanShrink trigger threshold),
                auto_shrink_threshold_percent: Auto-shrink threshold% (Optional, 1~98, default50),
                max_auto_size: Auto-expandupper limitGB (Optional, 1~33554432, default33554432; must be greater than equals shrinklower limit和Filesystem capacity),
                min_auto_size:  auto缩容lower limitGB (Optional, 1~33554432, default33554432),
                auto_size_increment: Auto resize single change amountMB (Optional, 64~102400, default1024),
             }
        worm: FilesystemWorm parameter (Optional)。 parameter format：{
                type: WORMProtection compliance mode (Optional)。Options：none_mode, enterprise_mode, compliance_mode, advance_mode, audit_log, non_worm,
                min_protect_period: Min protection period (Optional, 0~4294967295, default0; 4294967295is indefinite),
                min_protect_period_unit: Min protection period unit (Optional, defaultyear)。Options：minute, hour, day, month, year,
                max_protect_period: Max protection period (Optional, 1~4294967295, default70; 4294967295is indefinite),
                max_protect_period_unit: Max protection period unit (Optional, defaultyear)。Options：minute, hour, day, month, year,
                def_protect_period: Default protection period (Optional, 0~4294967295, default70; not less than min and not greater than max),
                def_protect_period_unit: Default protection period unit (Optional, defaultyear)。Options：minute, hour, day, month, year,
                auto_lock: WORMAuto-lock mode (Optional, Enabled by default; advance_mode不 support)。Options：true, false,
                auto_lock_time: Auto-lock time (Optional, min1, default2),
                auto_lock_time_unit: Auto-lock timeunit  (Optional, defaulthour)。Options：minute, hour, day, month, year,
                auto_del: Auto-delete mode (Optional, default off; advance_mode不 support)。Options：true, false,
                is_worm_audit_log_fs: WORMAudit logFilesystem (Optional, default off; One tenant can only have one),
                worm_append_unit: WORMAppend-only file protection granularity (Optional, 仅advance_mode support)。Options：256KB, 512KB, 1M,
             }
        task_remarks: Async taskRemark，0~1024 characters(Optional）
        audit_log_rules: Audit log rule集合(Optional），如：set_security、get_security、set_attr、get_attr等， max100条
        unix_permissions: Filesystem目录 permission(Optional）， format如0755

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
# namespace (Namespace) subtopic actions
# ============================================================================

def namespace_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 100,
         sort_dir: str = None, sort_key: str = None, name: str = None,
         vstore_name: str = None, vstore_raw_id: str = None, vstore_id: str = None,
         raw_id: str = None, pool_name: str = None, storage_id: str = None,
         enable_encrypt: bool = None, support_provisioning: bool = None,
         gfs_id: str = None, gfs_name: str = None, has_gfs: bool = None) -> dict:
    """
    Batch queryNamespace
    
    Args:
        client: DME API Client
        page_no: Page number(Optional），1~10000000
        page_size: Items per page(Optional），1~1000，default 100
        sort_dir:  specifiedSort direction(Optional），Options：asc（ascending）、desc（descending）
        sort_key: Sort key(Optional），Options：namespace_used_rate、file_used_rate
        name: Namespace name(Optional），1~256  characters， supportfuzzy search
        vstore_name: NamespaceTenant name(Optional），1~256  characters， supportfuzzy search
        vstore_raw_id: Namespace vStore 在Storage deviceassigned on ID(Optional），1~128  characters
        vstore_id: Namespace vStore 的 ID(Optional），1~128  characters
        raw_id: Namespaceon the storage device ID(Optional），1~256  characters
        pool_name: Storage pool name(Optional），1~256  characters， supportfuzzy search
        storage_id: Storage device ID(Optional），1~255  characters
        enable_encrypt: Enable encryption(Optional），true：是；false：否
        support_provisioning: supportsService provisioning(Optional），true：是；false：否；send this field to filter unsupportedService provisioning device的 resource，当前不 supportService provisioning的 device有 DataTurbo 系列
        gfs_id: Global namespace ID(Optional），1~64  characters
        gfs_name:  globalNamespace name(Optional），1~256  characters
        has_gfs: IncludeGlobal namespace的Namespace(Optional），true：是；false：否；has_gfs 为 false not supported when gfs_id
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，includes ：
        - total: Namespacecount
        - namespace_list: Namespace list，includes  id, raw_id, name, storage_id, vstore_id 等 info
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
    QueryNamespace details
    
    Args:
        client: DME API Client
        namespace_id: Namespace ID（Required，1~64  characters）
    
    Returns:
        NamespaceDetails，includes ：
        - id: Namespace ID
        - raw_id: Namespaceon the storage device ID
        - name: Namespace name
        - storage_id: Storage device ID
        - vstore_id:  tenant ID
        - vstore_name: Tenant name
        - pool_id: Storage pool ID
        - pool_name: Storage pool name
        - running_status: Running status（NORMAL/UNKNOWN）
        - space_used_rate: Space usage ratio
        - file_used_rate: File usage ratio
        - space_used: 已 use空间
        - file_used: Used file count
        - trash_enable: Enable回收站
        - enable_encrypt: Enable encryption
        - rdc: Data redundancy copies
        - acl_policy_type: Security mode
        - gfs_id: Global namespace ID
        - qos_policy: QoS  policy
        - worm: WORM  parameter
        等Details
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
    Batch createNamespace
    
    Args:
        client: DME API Client
        storage_id: Storage device ID（Required）
        pool_raw_id: Storage poolon the storage device ID（Required）
        namespace_specs: Namespacebatch parameter。 parameter format：[{
                name:  name (Required, 1~255 character, supports letters, digits, underscores.-),
                count: count (Required, 1~500),
                start_suffix: Starting suffix number (Optional, 0~9999; 起始 suffix+count<=9999),
                isInGfs:  whether在Global namespace中 (Optional)。Options：true, false,
             }, ...]
        enable_update_atime:  whether update Atime
        trash_visible: Recycle bin directory visibility，default invisible
        trash_enable: Recycle bin enabled，defaultdisabled
        interval_trash: Recycle bin retention period（minute(s)），0 Indicates permanent retention， max 4294967295
        dps_switch: Metadata search switch，true  enable
        forbidden_dpc:  whether禁止 dpc 挂载
        audit_log_switch: EnableAudit log，default off
        audit_log_rule: Audit log rule list，Options：open, create, read, write, close, 
                       delete, rename, get_attr, set_attr, get_security, set_security,
                       get_xattr, set_xattr, list_dir, contact, mount_or_unmount, login_or_logoff
        atime_update_mode: atime  updateFrequency，4294967295  disable，3600 1 hour(s)，86400 1 day(s)
        acl_policy_type: Security mode，Options：mixed, unix, native, ntfs，default unix
        enable_encrypt: Enable encryption
        crypt_alg: Encryption algorithm type，Options：XTS_AES_128, XTS_AES_256, XTS_SM4, UNKNOWN
        case_sensitive: Case sensitive，default不敏感
        show_snap_dir: Snapshot directory visibility
        rdc: Data redundancy copies，Options：redundancy_2, redundancy_3, redundancy_4
        worm: WORM  config (Optional)。 parameter format：{
                worm_mode: WORM policy mode (Optional)。Options：non_worm (None type), enterprise_mode (企业级), compliance_mode (法规级),
                min_protect_period: Min protection period (Optional, 0~4294967295, default0; 4294967295is indefinite),
                min_protect_period_unit:  minretention periodunit  (Optional, defaultyear)。Options：day, year, month, hour, minute,
                max_protect_period: Max protection period (Optional, 1~4294967295, default70; 4294967295is indefinite),
                max_protect_period_unit:  maxretention periodunit  (Optional, defaultyear)。Options：day, year, month, hour, minute, infinite,
                def_protect_period: Default protection period (Optional, 0~4294967295, default70),
                def_protect_period_unit: defaultretention periodunit  (Optional, defaultyear)。Options：day, year, month, hour, minute, infinite,
                auto_lock_enabled: WORMAuto-lock (Optional, defaultfalse)。Options：true, false,
                auto_lock_time: Auto-lock time (Optional, 1~64800, default2; unit day时1~45, hour时1~1080, minute时1~64800),
                auto_lock_unit: Auto-lock timeunit  (Optional, defaulthour)。Options：day, minute, hour,
                legal_hold_modify: Legal hold file retention period modification switch (Optional, defaultfalse)。Options：true, false,
             }
        qos_policy: QoS Policy configuration。 parameter format：{
                qos_scale: upper limit control维度 (Required)。Options：namespace, client, account, user, innertask,
                name: QoS policy name (Optional, 1~63 character,  regex^[a-zA-Z0-9][a-zA-Z0-9_-]*, must start with letter or digit),
                qos_mode: QoS mode (Required)。Options：by_usage (by used amount), by_package (by fixed capacity), manual (按upper limit),
                account_raw_id: 帐户on the storage deviceid (Optional, 0~4294967293; 当qos_scale为namespace/account/user时Required),
                package_size: package capacityGB (Optional, 0~94371840; 当qos_mode为by_package时Required),
                max_iops: IOPSupper limit (Optional, 0~1073741824000; Batch createwhen namespaceRequired),
                max_mbps:  bandwidthupper limitMbps (Optional, 0~1073741824; 当qos_mode为manual时Required),
                max_band_width: Max bandwidthMbps (Optional, 1~1073741824; 当qos_mode为by_usage或by_package时Required),
                basic_band_width: base bandwidthMbps (Optional, 1~1073741824; 当qos_mode为by_usage或by_package时Required),
                bps_density: bandwidth densityMbps (Optional, 1~1024000; 当qos_mode为by_usage或by_package时Required),
                max_conn_cluster: Max connections (Optional),
                max_lock_cluster: max lockcount (Optional),
                max_open_file_cluster: Max open file count (Optional),
                read_ops: 读OPS limit (Optional, 0~1073741824000; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
                write_ops: 写OPS limit (Optional, 0~1073741824000; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
                read_mbps: Read bandwidth limitMbps (Optional, 0~1073741824; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
                write_mbps: Write bandwidth limitMbps (Optional, 0~1073741824; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
             }
        public_network_qos_policy: 公网 QoS Policy configuration。 parameter format：{
                        name: QoS Policy name(Optional），1~63  characters, regex ^[a-zA-Z0-9][a-zA-Z0-9_-]*，must start with letter or digit,
                        qos_mode: QoS  mode（ conditionRequired），Options：by_usage（by used amount）、by_package（by fixed capacity）、manual（按upper limit）；Batch createwhen namespaceRequired, non- when modifyingRequired,
                        package_size: package capacity(Optional），0~94371840（GB），当 qos_mode 为 by_package 时Required,
                        max_iops: IOPS upper limit（ conditionRequired），0~1073741824000，Batch createwhen namespaceRequired, non- when modifyingRequired,
                        max_mbps:  bandwidthupper limit(Optional），0~1073741824（Mbps），当 qos_mode 为 manual 时Required,
                        max_band_width: Max bandwidth(Optional），1~1073741824（Mbps），当 qos_mode 为 by_usage 或 by_package 时Required,
                        basic_band_width: base bandwidth(Optional），1~1073741824（Mbps），当 qos_mode 为 by_usage 或 by_package 时Required,
                bps_density: bandwidth densityMbps (Optional, 1~1024000; 当qos_mode为by_usage或by_package时Required),
                max_conn_cluster: Max connections (Optional),
                max_lock_cluster: max lockcount (Optional),
                max_open_file_cluster: Max open file count (Optional),
                read_ops: 读OPS limit (Optional, 0~1073741824000; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
                write_ops: 写OPS limit (Optional, 0~1073741824000; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
                read_mbps: Read bandwidth limitMbps (Optional, 0~1073741824; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
                write_mbps: Write bandwidth limitMbps (Optional, 0~1073741824; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
             }
        private_network_qos_policy: 私网 QoS Policy configuration。 parameter format：{
                        name: QoS Policy name(Optional），1~63  characters, regex ^[a-zA-Z0-9][a-zA-Z0-9_-]*，must start with letter or digit,
                        qos_mode: QoS  mode（ conditionRequired），Options：by_usage（by used amount）、by_package（by fixed capacity）、manual（按upper limit）；Batch createwhen namespaceRequired, non- when modifyingRequired,
                        package_size: package capacity(Optional），0~94371840（GB），当 qos_mode 为 by_package 时Required,
                        max_iops: IOPS upper limit（ conditionRequired），0~1073741824000，Batch createwhen namespaceRequired, non- when modifyingRequired,
                        max_mbps:  bandwidthupper limit(Optional），0~1073741824（Mbps），当 qos_mode 为 manual 时Required,
                        max_band_width: Max bandwidth(Optional），1~1073741824（Mbps），当 qos_mode 为 by_usage 或 by_package 时Required,
                        basic_band_width: base bandwidth(Optional），1~1073741824（Mbps），当 qos_mode 为 by_usage 或 by_package 时Required,
                bps_density: bandwidth densityMbps (Optional, 1~1024000; 当qos_mode为by_usage或by_package时Required),
                max_conn_cluster: Max connections (Optional),
                max_lock_cluster: max lockcount (Optional),
                max_open_file_cluster: Max open file count (Optional),
                read_ops: 读OPS limit (Optional, 0~1073741824000; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
                write_ops: 写OPS limit (Optional, 0~1073741824000; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
                read_mbps: Read bandwidth limitMbps (Optional, 0~1073741824; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
                write_mbps: Write bandwidth limitMbps (Optional, 0~1073741824; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
             }
        create_s3_param: create  S3  protocol parameter (Optional)。 parameter format：{
                bucket_permission: Policy type (Required)。Options：private (私有), public_read_only (公共读), public_write_only (公共写), public_read_write (Public read/write),
                version_status: object多 version status (Optional, 0~2)。Options：0 ( disable), 1 ( open), 2 ( pause),
             }
        application_type: Application type，Options：PACS（Medical imaging scenario）, GENERAL（通用场景）
        task_remarks: Async taskRemark
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }（Async task ID）
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
    ModifyNamespace
    
    Args:
        client: DME API Client
        namespace_id: Namespace ID（Required，1~64  characters）
        enable_update_atime:  whether update Atime，true： update；false：不 update
        show_snap_dir: Snapshot directory visibility，true：可见；false： invisible
        trash_visible: Recycle bin directory visibility，true：可见；false： invisible，default invisible
        trash_enable: Recycle bin enabled，true： enable；false：disabled，defaultdisabled
        interval_trash: Recycle bin retention period（minute(s)），0 Indicates permanent retention，不 autodelete ， max 4294967295
        dps_switch: Metadata search switch，true： enable；false： disable
        forbidden_dpc:  whether禁止 dpc 挂载，true：禁止；false：不禁止
        audit_log_switch: EnableAudit log，缺省 disable，true： enable；false： disable
        audit_log_rule: Audit log rule list，Options：open, create, read, write, close, delete, rename,
                       get_attr, set_attr, get_security, set_security, get_xattr, set_xattr,
                       list_dir, contact, mount_or_unmount, login_or_logoff
        atime_update_mode: atime  updateFrequency，4294967295： disable update；3600：1 hour(s) update；86400：1 day(s) update
        acl_policy_type: NamespaceSecurity mode，Options：mixed（同时 support UNIX 和 Windows  permission），
                        unix（适用于 NFS User permissions determined by Unix Mode/NFSv4 ACL  permission control），
                        native（与 Mixed Mode applicable to same scenario），
                        ntfs（适用于 CIFS User permissions determined by Windows NT ACL  permission control）
        enable_encrypt: Enable encryption，true： enable；false： disable
        qos_policy: QoS Policy configuration。 parameter format：{
                qos_switch: QoS switch (Required)。Options：on, off,
                name: QoS policy name (Optional, 1~63 character,  regex^[a-zA-Z0-9][a-zA-Z0-9_-]*),
                qos_mode: QoS mode ( conditionRequired)。Options：by_usage (by used amount), by_package (by fixed capacity), manual (按upper limit),
                package_size: package capacityGB (Optional, 0~94371840; 当qos_mode为by_package时Required),
                max_iops: IOPSupper limit ( conditionRequired, 0~1073741824000),
                max_mbps:  bandwidthupper limitMbps (Optional, 0~1073741824; 当qos_mode为manual时Required),
                max_band_width: Max bandwidthMbps (Optional, 1~1073741824; 当qos_mode为by_usage或by_package时Required),
                basic_band_width: base bandwidthMbps (Optional, 1~1073741824; 当qos_mode为by_usage或by_package时Required),
                bps_density: bandwidth densityMbps (Optional, 1~1024000; 当qos_mode为by_usage或by_package时Required),
                max_conn_cluster: Max connections (Optional),
                max_lock_cluster: max lockcount (Optional),
                max_open_file_cluster: Max open file count (Optional),
                read_ops: 读OPS limit (Optional, 0~1073741824000; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
                write_ops: 写OPS limit (Optional, 0~1073741824000; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
                read_mbps: Read bandwidth limitMbps (Optional, 0~1073741824; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
                write_mbps: Write bandwidth limitMbps (Optional, 0~1073741824; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
             }
        public_network_qos_policy: 公网 QoS Policy configuration。 parameter format：{
                        qos_switch: QoS  switch（Required），Options：on、off,
                        name: QoS Policy name(Optional），1~63  characters, regex ^[a-zA-Z0-9][a-zA-Z0-9_-]*，must start with letter or digit,
                        qos_mode: QoS  mode（ conditionRequired），Options：by_usage（by used amount）、by_package（by fixed capacity）、manual（按upper limit）；Batch createwhen namespaceRequired, non- when modifyingRequired,
                        package_size: package capacity(Optional），0~94371840（GB），当 qos_mode 为 by_package 时Required,
                        max_iops: IOPS upper limit（ conditionRequired），0~1073741824000，Batch createwhen namespaceRequired, non- when modifyingRequired,
                        max_mbps:  bandwidthupper limit(Optional），0~1073741824（Mbps），当 qos_mode 为 manual 时Required,
                        max_band_width: Max bandwidth(Optional），1~1073741824（Mbps），当 qos_mode 为 by_usage 或 by_package 时Required,
                        basic_band_width: base bandwidth(Optional），1~1073741824（Mbps），当 qos_mode 为 by_usage 或 by_package 时Required,
                bps_density: bandwidth densityMbps (Optional, 1~1024000; 当qos_mode为by_usage或by_package时Required),
                max_conn_cluster: Max connections (Optional),
                max_lock_cluster: max lockcount (Optional),
                max_open_file_cluster: Max open file count (Optional),
                read_ops: 读OPS limit (Optional, 0~1073741824000; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
                write_ops: 写OPS limit (Optional, 0~1073741824000; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
                read_mbps: Read bandwidth limitMbps (Optional, 0~1073741824; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
                write_mbps: Write bandwidth limitMbps (Optional, 0~1073741824; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
             }
        private_network_qos_policy: 私网 QoS Policy configuration。 parameter format：{
                        qos_switch: QoS  switch（Required），Options：on、off,
                        name: QoS Policy name(Optional），1~63  characters, regex ^[a-zA-Z0-9][a-zA-Z0-9_-]*，must start with letter or digit,
                        qos_mode: QoS  mode（ conditionRequired），Options：by_usage（by used amount）、by_package（by fixed capacity）、manual（按upper limit）；Batch createwhen namespaceRequired, non- when modifyingRequired,
                        package_size: package capacity(Optional），0~94371840（GB），当 qos_mode 为 by_package 时Required,
                        max_iops: IOPS upper limit（ conditionRequired），0~1073741824000，Batch createwhen namespaceRequired, non- when modifyingRequired,
                        max_mbps:  bandwidthupper limit(Optional），0~1073741824（Mbps），当 qos_mode 为 manual 时Required,
                        max_band_width: Max bandwidth(Optional），1~1073741824（Mbps），当 qos_mode 为 by_usage 或 by_package 时Required,
                        basic_band_width: base bandwidth(Optional），1~1073741824（Mbps），当 qos_mode 为 by_usage 或 by_package 时Required,
                bps_density: bandwidth densityMbps (Optional, 1~1024000; 当qos_mode为by_usage或by_package时Required),
                max_conn_cluster: Max connections (Optional),
                max_lock_cluster: max lockcount (Optional),
                max_open_file_cluster: Max open file count (Optional),
                read_ops: 读OPS limit (Optional, 0~1073741824000; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
                write_ops: 写OPS limit (Optional, 0~1073741824000; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
                read_mbps: Read bandwidth limitMbps (Optional, 0~1073741824; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
                write_mbps: Write bandwidth limitMbps (Optional, 0~1073741824; only whenqos_mode为manual且qos_scalenotaccountwhen Optional),
             }
        application_type: Application type，Options：PACS（Medical imaging scenario）, GENERAL（通用场景）
        task_remarks: Async taskRemark
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }（Async task ID）
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
    Batch deleteNamespace
    
    Args:
        client: DME API Client
        namespace_ids: Namespace ID  list（Required），数组 max 100 个， min 1 个
        task_remarks: Async taskRemark(Optional，0~1024  characters）
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }（Async task ID）
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
     query NFS share client access list

     specified device或 NFS ID， query NFS share client access list。

    Args:
        client: DME API Client
        page_no: Page queryStart page(Optional），min 1，default 1
        page_size: shown per pagecount(Optional），1~1000，default 20
        nfs_share_id: NFS  share ID(Optional），1~64  characters
        storage_id: Storage device ID(Optional），1~64  characters；如果 specified nfs_share_id，this parameter is invalid
        vstore_id_in_storage: vStore ID(Optional），1~256  characters；vStore must be sent in this scenario
        name: Client IP or hostname or netgroup name(Optional），1~256  characters； specified nfs_share_id  condition下 supportfuzzy search
        client_id_in_storage: NFS  shareClient ID(Optional），1~256  characters
        sort_key: Sort field(Optional），Options：raw_id、name
        sort_dir: Sort direction(Optional），Options：asc（ascending）、desc（descending），default asc

    Returns:
        Client访问 list
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
    Batch query DataTurbo Admin

    仅 OceanStor A800 series storage only。

    Args:
        client: DME API Client
        storage_id:  device ID (1~64 characters, Optional)
        vstore_id:  tenant的 ID (1~64 characters, Optional)
        vstore_name:  tenant name， supportfuzzy search (1~256 characters, Optional)
        zone_id:  zone 的 ID (1~64 characters, Optional)。When resource scope is global，Zone ID of the device Id；When resource scope is local，Zone ID 为 Zone 的 ID。仅 OceanStor A800 series storage only
        name: DataTurbo Admin名， supportfuzzy search (1~256 characters, Optional)
        online_status: DataTurbo AdminOnline status (Optional)。Options：offline (offline), online (online)
        lock_status: DataTurbo AdminLock status (Optional)。Options：unlocked (未 lock), locked ( lock)
        account_state: DataTurbo Admin密码 status (Optional)。Options：normal (normal), expired (Password expired), initial (User password is in initial state， needmodify ), expiring_soon (Password expiring soon), change_required (Must change password on next login), never (Password never expires)
        sort_key: sort by specified field (Optional)。Options：create_time
        sort_dir:  specifiedSort direction (Optional)。Options：asc (ascending), desc (descending)
        page_no: Page queryStart page (int32, min: 1, Default: 1, Optional)
        page_size: shown per pagecount (int32, min: 1, max: 1000, Default: 20, Optional)

    Returns:
        DataTurbo Admin list，includes  total 和 administrators
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
    modify  UNIX user 

    Args:
        client: DME API Client
        id: UNIX user  ID (1~32 characters, Required)
        raw_id: UNIX user on the storage device ID (int64, 0~4294967294, Optional)
        description: UNIX user  description (0~255 characters, Optional)
        primary_group_name: User primary group name (1~64 characters, Optional。与 primary_group_raw_id 都下发仅 primary_group_raw_id effective)
        primary_group_raw_id: user 主组 ID (int64, 0~4294967294, Optional。与 primary_group_name 都下发仅 primary_group_raw_id effective)
        status_enable: User status (boolean, Optional)。Options：true ( enable), false ( lock)。仅 OceanStor Pacific 和 OceanStor A310 series storage only

    Returns:
        Modification result
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
    create  UNIX User group

    Args:
        client: DME API Client
        storage_id: create  UNIX User groupStorage device ID (1~64 characters, Required)
        name: UNIX User group name (1~64 characters, Required)
        raw_id: UNIX User group ID (int64, 0~4294967294, Optional。OceanStor Pacific 和 OceanStor A310  storageRequired)
        description: UNIX User group description (0~255 characters, Optional)
        vstore_raw_id: user Tenanton the storage device ID (1~32 characters, Required)
        zone_id:  Zone ID (1~64 characters, Optional。仅 OceanStor A800 storage support)

    Returns:
        creation result
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
    delete  UNIX user 

    Args:
        client: DME API Client
        ids: UNIX user  ID  list (List<string>, min array members: 1, max array members: 100, Required)

    Returns:
        Operation result
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
     query UNIX  authUser group list

    Args:
        client: DME API Client
        page_no: Page queryStart position (int32, 1~2147483647, Default: 1, Optional)
        page_size: Items per page (int32, 10~100, Default: 100, Optional)
        storage_name: Device name， supportfuzzy match filter (1~256 characters, Optional)
        vstore_raw_id: Tenanton the storage device ID (1~64 characters, Optional)
        vstore_name: Tenant name， supportfuzzy search filter (1~256 characters, Optional)
        name: User group name， supportfuzzy search filter (1~256 characters, Optional)
        raw_id: User groupon the storage device ID (1~256 characters, Optional)
        zone_id: Zone ID (1~64 characters, Optional)。仅 OceanStor A800 auth under storageUser groupsupports filtering by this field
        sort_key: sort by specified field (Optional)。Options：name (User group名), raw_id (User groupon the storage device ID), create_time (Creation time)。Default：create_time
        storage_id: Storage device ID (1~36 characters, Optional)
        sort_dir:  specifiedSort direction (Optional)。Options：asc (ascending), desc (descending)。Default：desc

    Returns:
        UNIX  authUser group list
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
     query UNIX User group details

    Args:
        client: DME API Client
        id: User group ID (1~32 characters, Required)

    Returns:
        UNIX User group details
    """
    url = "/rest/fileservice/v1/unix-user-groups/{id}"

    response = client.get(url, params={"id": id})
    return response


def account_unix_user_group_modify(client: DMEAPIClient, id: str,
                                    raw_id: int = None,
                                    description: str = None) -> dict:
    """
    modify  UNIX User group

    Args:
        client: DME API Client
        id: UNIX User group ID (1~32 characters, Required)
        raw_id: UNIX User groupon the storage device ID (int64, 0~4294967294, Optional)
        description: UNIX User group description (0~255 characters, Optional)

    Returns:
        Modification result
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
    delete  UNIX User group

    Args:
        client: DME API Client
        ids: UNIX User group的 ID  list (List<string>, min array members: 1, max array members: 100, Required)

    Returns:
        Operation result
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
    移除 UNIX user secondary group

    Args:
        client: DME API Client
        user_id: UNIX user  ID (1~32 characters, Required)
        secondary_group_name_list: secondary groupName list (List<string>, min array members: 1, max array members: 100, Required)

    Returns:
        Operation result
    """
    url = "/rest/fileservice/v1/unix-users/{user_id}/remove-secondary-group"

    payload = {
        'secondary_group_name_list': secondary_group_name_list,
    }

    response = client.post(url, params={"user_id": user_id})
    return response


def account_unix_user_show(client: DMEAPIClient, id: str) -> dict:
    """
     query UNIX Auth user details

    Args:
        client: DME API Client
        id: user  ID (1~32 characters, Required)

    Returns:
        UNIX Auth user details
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
     query UNIX  authUser list

    Args:
        client: DME API Client
        page_no: Page queryStart position (int32, 1~2147483647, Default: 1, Optional)
        page_size: Items per page (int32, 10~100, Default: 100, Optional)
        storage_name: Device name， supportfuzzy search filter (1~256 characters, Optional)
        vstore_raw_id: Tenanton the storage device ID (1~64 characters, Optional)
        vstore_name: Tenant name， supportfuzzy search filter (1~256 characters, Optional)
        name: Username称， supportfuzzy search filter (1~256 characters, Optional)
        primary_group_name: 主组 name， supportfuzzy search filter (1~256 characters, Optional)
        raw_id: user on the storage device ID (1~255 characters, Optional)
        zone_id: Zone ID (1~64 characters, Optional)。仅 OceanStor A800  storage underauth usersupports filtering by this field
        user_status: User status (Optional)。Options：enable ( enable), disable (禁用)
        sort_key: sort by specified field (Optional)。Options：name (Username), raw_id (user on the storage device ID), primary_group_name (主组名), create_time (Creation time)。Default：create_time
        storage_id: Storage device ID (1~36 characters, Optional)
        sort_dir:  specifiedSort direction (Optional)。Options：asc (ascending), desc (descending)。Default：desc

    Returns:
        UNIX  authUser list
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
    add  UNIX user secondary group

    Args:
        client: DME API Client
        user_id: UNIX user  ID (1~32 characters, Required)
        secondary_group_name_list: secondary groupName list (List<string>, min array members: 1, max array members: 100, Required)

    Returns:
        Operation result
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
    create  UNIX user 

    Args:
        client: DME API Client
        storage_id: create  UNIX user Storage device ID (1~64 characters, Required)
        name: UNIX Username称 (1~64 characters, Required)
        raw_id: UNIX user  ID (int64, 0~4294967294, Optional。OceanStor Pacific 和 OceanStor A310  storageRequired)
        description: UNIX user  description (0~255 characters, Optional)
        primary_group_raw_id: user 主组 ID (int64, 0~4294967294, Optional。与 primary_group_name provide at least one， if both sent, only primary_group_name effective)
        primary_group_name: User primary group name (1~64 characters, Optional。与 primary_group_raw_id provide at least one， if both sent, only primary_group_name effective)
        vstore_raw_id: user Tenanton the storage device ID (1~32 characters, Required)
        zone_id:  Zone ID (1~64 characters, Optional。仅 OceanStor A800 storage support)
        status: User status (boolean, Optional。Default：true)。Options：true ( enable), false ( lock)。仅 OceanStor Pacific 和 OceanStor A310 series storage only
        secondary_group_name_list: user secondary groupName list (List<string>, min array members: 0, max array members: 100, Optional)

    Returns:
        creation result
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
    Batch create KV Cache 库

    Args:
        client: DME API Client
        storage_id: Storage device ID (length is36 characters, Required)
        zone_id:  Zone 的 ID (length is36 characters, Required)
        pool_raw_id: Storage pool在 Zone 上的 ID (1~64 characters, Required)
        vstore_id:  tenant ID (length is32 characters, Required)
        data_cleanup_switch: Cleanup switch (Optional)。Options：on ( open), off ( disable)。Default：off
        max_survival_time: KV Cache Max TTL/survival time (int32, 1~3650, Optional。当 data_cleanup_switch 为 on 时Required)
        kv_cache_stores: KV Cache 库 list (List<CreateKVCacheStoreBaseInfo>, min array members: 1, max array members: 100, Required)。 parameter format：[{
                name: KV Cache 库 name (1~255 characters, Required),
                capacity: KV Cache 库 capacity (int64, 20971520~70368744177664, unit : 扇区数, 1扇区=512 byte, Required),
                description: Description (1~255 characters, Optional),
                count: Batch create KV Cache 库的count (int32, 1~100, Default: 1, Optional),
                start_suffix: Starting suffix number (int32, 0~9999, Optional。Starting suffix number+KV Cache库count<=9999),
             }, ...]

    Returns:
        creation result
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
    modify  KV Cache 库

    Args:
        client: DME API Client
        kv_cache_stores_id: KV Cache 库 ID (1~64 characters, Required)
        name: KV Cache 库 name (1~255 characters, Optional)
        description: Description (0~255 characters, Optional)
        data_cleanup_switch: Cleanup switch (Optional)。Options：on ( open), off ( disable)。Default：off
        max_survival_time: KV Cache Max TTL/survival time (int32, 1~3650, Optional。当 data_cleanup_switch 为 on 时Required)

    Returns:
        Modification result
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
    Batch delete KV Cache 库

    Args:
        client: DME API Client
        ids: KV Cache 库 ID  list (List<string>, min array members: 1, max array members: 100, Required)

    Returns:
        Operation result
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
     query KV Cache 库

    Args:
        client: DME API Client
        storage_id: Storage device ID (length is36 characters, Optional)
        id: KV Cache 库 ID (length is32 characters, Optional)
        raw_id: KV Cache 库在 Zone 上的 ID (1~256 characters, Optional)
        name: KV Cache 库 name (1~256 characters, Optional)
        zone_id:  Zone 的 ID (length is36 characters, Optional)
        pool_raw_id: Storage pool在 Zone 上的 ID (1~64 characters, Optional)
        vstore_id:  tenant ID (length is32 characters, Optional)
        vstore_name: Tenant name (1~256 characters, Optional)
        fs_id: Filesystem ID (length is32 characters, Optional)
        fs_name: Filesystem name (1~256 characters, Optional)
        data_cleanup_switch: Cleanup switch (Optional)。Options：on ( open), off ( disable)
        page_no: Page number (int32, 1~10000, Default: 1, Optional)
        page_size: Items per page (int32, 1~100, Default: 20, Optional)
        sort_dir:  specifiedSort direction (Optional)。Options：asc (ascending), desc (descending)。Default：asc
        sort_key: Sort key (Optional)。Options：capacity (Total capacity), used_capacity (Used capacity), used_tokens (已 use的 token count), hit_ratio (命中率)

    Returns:
        KV Cache 库 list
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
        'description': 'Batch query DataTurbo admins',
        'params': ['storage_id', 'vstore_id', 'vstore_name', 'zone_id', 'name', 'online_status', 'lock_status', 'account_state', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_unix_user_create': {
        'func': account_unix_user_create,
        'description': 'Create UNIX user',
        'params': ['storage_id', 'name', 'vstore_raw_id', 'raw_id', 'description', 'primary_group_raw_id', 'primary_group_name', 'zone_id', 'status', 'secondary_group_name_list'],
        'subtopic': 'account'
    },
    'account_unix_user_add_group': {
        'func': account_unix_user_add_group,
        'description': 'Add UNIX user secondary group',
        'params': ['user_id', 'secondary_group_name_list'],
        'subtopic': 'account'
    },
    'account_unix_user_list': {
        'func': account_unix_user_list,
        'description': 'Query UNIX user list',
        'params': ['storage_id', 'storage_name', 'vstore_raw_id', 'vstore_name', 'name', 'primary_group_name', 'raw_id', 'zone_id', 'user_status', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_unix_user_show': {
        'func': account_unix_user_show,
        'description': 'Query UNIX user details',
        'params': ['id'],
        'subtopic': 'account'
    },
    'account_unix_user_remove_group': {
        'func': account_unix_user_remove_group,
        'description': 'Remove UNIX user secondary group',
        'params': ['user_id', 'secondary_group_name_list'],
        'subtopic': 'account'
    },
    'account_unix_user_modify': {
        'func': account_unix_user_modify,
        'description': 'Modify UNIX user',
        'params': ['id', 'raw_id', 'description', 'primary_group_name', 'primary_group_raw_id', 'status_enable'],
        'subtopic': 'account'
    },
    'account_unix_user_batch_delete': {
        'func': account_unix_user_batch_delete,
        'description': 'Delete UNIX user',
        'params': ['ids'],
        'subtopic': 'account'
    },
    'account_unix_user_group_create': {
        'func': account_unix_user_group_create,
        'description': 'Create UNIX user group',
        'params': ['storage_id', 'name', 'vstore_raw_id', 'raw_id', 'description', 'zone_id'],
        'subtopic': 'account'
    },
    'account_unix_user_group_list': {
        'func': account_unix_user_group_list,
        'description': 'Query UNIX user group list',
        'params': ['storage_id', 'storage_name', 'vstore_raw_id', 'vstore_name', 'name', 'raw_id', 'zone_id', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_unix_user_group_show': {
        'func': account_unix_user_group_show,
        'description': 'Query UNIX user group details',
        'params': ['id'],
        'subtopic': 'account'
    },
    'account_unix_user_group_modify': {
        'func': account_unix_user_group_modify,
        'description': 'Modify UNIX user group',
        'params': ['id', 'raw_id', 'description'],
        'subtopic': 'account'
    },
    'account_unix_user_group_batch_delete': {
        'func': account_unix_user_group_batch_delete,
        'description': 'Delete UNIX user group',
        'params': ['ids'],
        'subtopic': 'account'
    },
    'dtree_list': {
        'func': dtree_list,
        'description': 'Query Dtree list',
        'params': ['id_in_storage', 'name', 'device_name', 'storage_id', 'zone_id', 'manufacturer', 'tier_name', 'fs_name', 'fs_id', 'namespace_name', 'namespace_id', 'quota_switch', 'security_mode', 'nas_locking_policy', 'sort_key', 'sort_dir', 'page_no', 'page_size', 'dc_id', 'dc_name'],
        'subtopic': 'dtree'
    },
    'dtree_show': {
        'func': dtree_show,
        'description': 'Query Dtree details',
        'params': ['dtree_id'],
        'subtopic': 'dtree'
    },
    'dtree_create': {
        'func': dtree_create,
        'description': 'Create and share Dtree',
        'params': ['storage_id', 'create_dtrees_param', 'fs_id', 'namespace_id', 'zone_id', 'parent_dir', 'quota_switch', 'security_mode', 'nas_locking_policy', 'create_nfs_share_param', 'create_cifs_share_param', 'dataturbo_share', 'create_worm_param', 'unix_permissions', 'task_remarks'],
        'subtopic': 'dtree'
    },
    'dtree_delete': {
        'func': dtree_delete,
        'description': 'Batch delete Dtree',
        'params': ['dtree_ids', 'task_remarks'],
        'subtopic': 'dtree'
    },
    'dtree_modify': {
        'func': dtree_modify,
        'description': 'Modify Dtree',
        'params': ['dtree_id', 'name', 'quota_switch', 'security_mode', 'nas_locking_policy', 'unix_permissions', 'task_remarks'],
        'subtopic': 'dtree'
    },
    # NFS share subtopic actions
    'nfs_share_list': {
        'func': nfs_share_list,
        'description': 'Query NFS share list',
        'params': ['id_in_storage', 'name', 'share_path', 'exact_share_path', 'device_name', 'storage_id', 'tier_name', 'owning_dtree_name', 'fs_name', 'fs_id', 'owning_dtree_id', 'vstore_name', 'page_no', 'page_size', 'sort_key', 'sort_dir', 'support_provisioning', 'namespace_id', 'namespace_name', 'dc_id', 'dc_name', 'zone_id', 'zone_name', 'zone_ip'],
        'subtopic': 'nfs_share'
    },
    'nfs_share_show': {
        'func': nfs_share_show,
        'description': 'Query NFS share details',
        'params': ['nfs_share_id'],
        'subtopic': 'nfs_share'
    },
    'nfs_share_create': {
        'func': nfs_share_create,
        'description': 'Create NFS share',
        'params': ['create_nfs_share_param', 'task_remarks'],
        'subtopic': 'nfs_share'
    },
    'nfs_share_modify': {
        'func': nfs_share_modify,
        'description': 'Modify NFS share',
        'params': ['nfs_share_id', 'description', 'character_encoding', 'audit_items', 'show_snapshot_enable', 'nfs_share_client_addition', 'nfs_share_client_modification', 'nfs_share_client_deletion', 'file_name_ex_filters', 'task_remarks'],
        'subtopic': 'nfs_share'
    },
    'nfs_share_delete': {
        'func': nfs_share_delete,
        'description': 'Batch delete NFS shares',
        'params': ['nfs_share_ids', 'task_remarks'],
        'subtopic': 'nfs_share'
    },
    'nfs_share_show_clients': {
        'func': nfs_share_show_clients,
        'description': 'Query NFS share client list',
        'params': ['page_no', 'page_size', 'nfs_share_id', 'storage_id', 'vstore_id_in_storage', 'name', 'client_id_in_storage', 'sort_key', 'sort_dir'],
        'subtopic': 'nfs_share'
    },
    # CIFS share subtopic actions
    'cifs_share_list': {
        'func': cifs_share_list,
        'description': 'Batch query CIFS shares',
        'params': ['raw_id', 'name', 'share_path', 'exact_share_path', 'fs_id', 'fs_name', 'dtree_id', 'dtree_name', 'storage_id', 'storage_name', 'vstore_raw_id', 'vstore_name', 'manufacturer', 'op_lock_enabled', 'notify_enabled', 'offline_file_modes', 'file_extension_filter_enabled', 'abe_enabled', 'page_no', 'page_size', 'sort_key', 'sort_dir', 'namespace_id', 'namespace_name', 'support_provisioning', 'dc_id', 'dc_name'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_show': {
        'func': cifs_share_show,
        'description': 'Query CIFS share details',
        'params': ['cifs_share_id'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_create': {
        'func': cifs_share_create,
        'description': 'Create CIFS share',
        'params': ['create_cifs_param', 'fs_id', 'namespace_id', 'task_remarks'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_modify': {
        'func': cifs_share_modify,
        'description': 'Modify CIFS share',
        'params': ['cifs_share_id', 'description', 'op_lock_enabled', 'notify_enabled', 'ca_enabled', 'offline_file_mode', 'ip_control_enabled', 'abe_enabled', 'audititem_list', 'apply_default_acl', 'file_extension_filter_enabled', 'show_previous_versions_enabled', 'show_snapshot_enabled', 'user_and_user_group_info', 'ip_and_segments', 'file_name_ex_filters', 'task_remarks', 'smb3_encryption_enable', 'unencrypted_access', 'enable_lease'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_delete': {
        'func': cifs_share_delete,
        'description': 'Batch delete CIFS shares',
        'params': ['cifs_share_ids', 'task_remarks'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_show_permissions': {
        'func': cifs_share_show_permissions,
        'description': 'Query CIFS share permissions (user/IP/file)',
        'params': ['cifs_share_id', 'type', 'user_filter', 'ip_filter', 'file_filter', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'cifs_share'
    },
    # DataTurbo share subtopic actions
    'dataturbo_share_list': {
        'func': dataturbo_share_list,
        'description': 'Query DataTurbo share list',
        'params': ['page_no', 'page_size', 'raw_id', 'share_path', 'fs_id', 'fs_name', 'dtree_id', 'dtree_name', 'vstore_id', 'vstore_raw_id', 'vstore_name', 'storage_id', 'storage_name', 'zone_id', 'zone_name', 'scope', 'sort_key', 'sort_dir'],
        'subtopic': 'dataturbo_share'
    },
    'dataturbo_share_show': {
        'func': dataturbo_share_show,
        'description': 'Query DataTurbo share details',
        'params': ['dataturbo_share_id'],
        'subtopic': 'dataturbo_share'
    },
    'dataturbo_share_create': {
        'func': dataturbo_share_create,
        'description': 'Create DataTurbo share',
        'params': ['charset', 'fs_id', 'dtree_id', 'description', 'dataturbo_share_auth', 'task_remarks'],
        'subtopic': 'dataturbo_share'
    },
    'dataturbo_share_modify': {
        'func': dataturbo_share_modify,
        'description': 'Modify DataTurbo share',
        'params': ['dataturbo_share_id', 'description', 'dataturbo_share_auth_addition', 'dataturbo_share_auth_deletion', 'task_remarks'],
        'subtopic': 'dataturbo_share'
    },
    'dataturbo_share_delete': {
        'func': dataturbo_share_delete,
        'description': 'Batch delete DataTurbo shares',
        'params': ['dataturbo_share_ids', 'task_remarks'],
        'subtopic': 'dataturbo_share'
    },
    'dataturbo_share_show_permissions': {
        'func': dataturbo_share_show_permissions,
        'description': 'Query DataTurbo share admin permissions',
        'params': ['dataturbo_share_id', 'page_no', 'page_size', 'user_id', 'user_name', 'permission'],
        'subtopic': 'dataturbo_share'
    },
    # Quota subtopic actions
    'quota_list': {
        'func': quota_list,
        'description': 'Query quota list',
        'params': ['page_no', 'page_size', 'ids', 'raw_ids', 'quota_type', 'parent_type', 'parent_raw_id', 'owner_name', 'vstore_id', 'vstore_raw_id', 'storage_id', 'sort_key', 'sort_dir', 'zone_id'],
        'subtopic': 'quota'
    },
    'quota_show': {
        'func': quota_show,
        'description': 'Query quota details',
        'params': ['quota_id'],
        'subtopic': 'quota'
    },
    'quota_create': {
        'func': quota_create,
        'description': 'Create quota',
        'params': ['parent_id', 'parent_type', 'quota_type', 'space_soft_quota', 'space_hard_quota', 'space_advisory_quota', 'file_soft_quota', 'file_hard_quota', 'file_advisory_quota', 'snap_space_switch', 'soft_grace_time', 'quota_owner', 'dir_quota_target', 'task_remarks'],
        'subtopic': 'quota'
    },
    'quota_modify': {
        'func': quota_modify,
        'description': 'Update quota',
        'params': ['quota_id', 'space_soft_quota', 'space_hard_quota', 'space_advisory_quota', 'file_soft_quota', 'file_hard_quota', 'file_advisory_quota', 'snap_space_switch', 'soft_grace_time', 'task_remarks'],
        'subtopic': 'quota'
    },
    'quota_delete': {
        'func': quota_delete,
        'description': 'Batch delete quotas',
        'params': ['quota_ids', 'task_remarks'],
        'subtopic': 'quota'
    },
    # Filesystem subtopic actions
    'filesystem_list': {
        'func': filesystem_list,
        'description': 'Batch query filesystems',
        'params': ['page_no', 'page_size', 'sort_dir', 'sort_key', 'name', 'fs_raw_id', 'storage_id'],
        'subtopic': 'filesystem'
    },
    'filesystem_show': {
        'func': filesystem_show,
        'description': 'Query filesystem details',
        'params': ['filesystem_id'],
        'subtopic': 'filesystem'
    },
    'filesystem_delete': {
        'func': filesystem_delete,
        'description': 'Batch delete filesystems',
        'params': ['filesystem_ids', 'task_remarks'],
        'subtopic': 'filesystem'
    },
    'filesystem_batch_modify': {
        'func': filesystem_batch_modify,
        'description': 'Batch modify filesystems (names)',
        'params': ['filesystems', 'task_remarks'],
        'subtopic': 'filesystem'
    },
    'filesystem_create': {
        'func': filesystem_create,
        'description': 'Custom create filesystem',
        'params': ['storage_id', 'pool_raw_id', 'filesystem_specs', 'vstore_id', 'zone_id', 'task_remarks', 'gfs_group_id', 'automatic_update_time', 'atime_update_mode', 'schedule_name', 'quota_switch', 'vaai_switch', 'initial_distribute_policy', 'capacity_threshold'],
        'subtopic': 'filesystem'
    },
    'filesystem_query_available': {
        'func': filesystem_query_available,
        'description': 'Query available filesystems (remote replication)',
        'params': ['feature_type', 'local_storage_id', 'remote_storage_id', 'name', 'page_no', 'page_size', 'sort_key', 'sort_dir'],
        'subtopic': 'filesystem'
    },
    'filesystem_modify': {
        'func': filesystem_modify,
        'description': 'Modify filesystem (full params)',
        'params': ['file_system_id', 'name', 'description', 'capacity', 'capacity_threshold', 'initial_distribute_policy', 'automatic_update_time', 'atime_update_mode', 'quota_switch', 'vaai_switch', 'owning_controller', 'task_remarks'],
        'subtopic': 'filesystem'
    },
    # Namespace subtopic actions
    'namespace_list': {
        'func': namespace_list,
        'description': 'Batch query namespaces',
        'params': ['page_no', 'page_size', 'sort_dir', 'sort_key', 'name', 
                   'vstore_name', 'vstore_raw_id', 'vstore_id', 'raw_id',
                   'pool_name', 'storage_id', 'enable_encrypt', 
                   'support_provisioning', 'gfs_id', 'gfs_name', 'has_gfs'],
        'subtopic': 'namespace'
    },
    'namespace_show': {
        'func': namespace_show,
        'description': 'Query namespace details',
        'params': ['namespace_id'],
        'subtopic': 'namespace'
    },
    'namespace_create': {
        'func': namespace_create,
        'description': 'Batch create namespaces',
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
        'description': 'Modify namespace',
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
        'description': 'Batch delete namespaces',
        'params': ['namespace_ids', 'task_remarks'],
        'subtopic': 'namespace'
    },
    # DataTurbo subtopic actions
    'dpc_list': {
        'func': dpc_list,
        'description': 'Batch query DPC list',
        'params': ['ids', 'hostname', 'ip', 'mgmt_status', 'status', 'sn', 'storage_id', 'dpc_om_id', 'dpc_type', 'client_version', 'page_no', 'page_size'],
        'subtopic': 'dataturbo'
    },
    'dpc_show': {
        'func': dpc_show,
        'description': 'Query DPC details',
        'params': ['dpc_id'],
        'subtopic': 'dataturbo'
    },
    # DPC client subtopic actions
    'list': {
        'func': dpc_client_list,
        'description': 'Batch query DPC clients',
        'params': ['storage_id', 'process_id', 'name', 'manage_ip', 'version', 'status', 'switch_status', 'upgrade_flag', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'dpc'
    },
    'show': {
        'func': dpc_client_show,
        'description': 'Query DPC client details',
        'params': ['id'],
        'subtopic': 'dpc'
    },
    # KVCache subtopic actions
    'kvcache_list': {
        'func': kvcache_list,
        'description': 'Query KV Cache stores',
        'params': ['storage_id', 'id', 'raw_id', 'name', 'zone_id', 'pool_raw_id', 'vstore_id', 'vstore_name', 'fs_id', 'fs_name', 'data_cleanup_switch', 'page_no', 'page_size', 'sort_dir', 'sort_key'],
        'subtopic': 'kvcache'
    },
    'kvcache_batch_create': {
        'func': kvcache_batch_create,
        'description': 'Batch create KV Cache stores',
        'params': ['storage_id', 'zone_id', 'pool_raw_id', 'vstore_id', 'kv_cache_stores', 'data_cleanup_switch', 'max_survival_time'],
        'subtopic': 'kvcache'
    },
    'kvcache_modify': {
        'func': kvcache_modify,
        'description': 'Modify KV Cache store',
        'params': ['kv_cache_stores_id', 'name', 'description', 'data_cleanup_switch', 'max_survival_time'],
        'subtopic': 'kvcache'
    },
    'kvcache_batch_delete': {
        'func': kvcache_batch_delete,
        'description': 'Batch delete KV Cache stores',
        'params': ['ids'],
        'subtopic': 'kvcache'
    },
}
