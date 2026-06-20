"""
NAS related operations
"""

import sys
import os

from pydme.client import DMEAPIClient


# ============================================================================
# DPC (DPC) sub-topic functions
# ============================================================================


def dpc_list(client: DMEAPIClient, ids: list = None, hostname: str = None, ip: str = None,
             mgmt_status: list = None, status: list = None, sn: str = None,
             storage_id: str = None, dpc_om_id: str = None, dpc_type: list = None,
             client_version: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch query DPC list

    Args:
        client: DME API client
        ids: DPC ID list(Optional), List<string> type, max array members 100, exact query
        hostname: Host name of the compute node(Optional), 1~256 characters, fuzzy query
        ip: Management IP of the DPC's compute node(Optional), 1~256 characters, fuzzy query
        mgmt_status: Management status list(Optional), List<string> type, exact query; valid values: normal (normal), abnormal (abnormal), unready (unready, client configuration status abnormal), subhealth (sub-health), pre_registered (pre-registered), unknown (unknown)
        status: Service status list(Optional), List<string> type, exact query; valid values: normal (normal), abnormal (abnormal), subhealth (sub-health), unknown (unknown)
        sn: Hardware SN of the DPC's compute node(Optional), 1~256 characters, fuzzy query
        storage_id: Storage device ID(Optional), 1~256 characters, exact query
        dpc_om_id: DPC O&M ID(Optional), 1~256 characters, exact query
        dpc_type: DPC type list(Optional), List<string> type
        client_version: DPC version number(Optional), up to 256 characters, exact query
        page_no: Page number(Optional), 1~10000000, default 1
        page_size: Records per page(Optional), 1~1000, default 20

    Returns:
        {
            total: DPC total (integer),
            dpcs: DPC list (List<DpcInfo>). parameter format: [{
                id: DPC ID (string),
                hostname: host name (string),
                ip: management IP (string),
                status: service status (string),
                mgmt_status: management status (string),
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
    Query DPC details

    Args:
        client: DME API client
        dpc_id: DPC ID (Required, string)

    Returns:
        {
            id: DPC ID (string),
            hostname: host name (string),
            ip: management IP (string),
            status: service status (string),
            mgmt_status: management status (string),
        }
    """
    url = "/rest/dpc-mgmt/v1/dpcs/{dpc_id}"

    if not dpc_id:
        raise ValueError("dpc_id is a required parameter")

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
    Batch query DPC clients

    Args:
        client: DME API client
        storage_id: Storage ID (Optional, string, 1~64 characters)
        process_id: DPC client process ID (Optional, string, 1~64 characters)
        name: DPC client name, supports fuzzy search (Optional, string, 1~256 characters)
        manage_ip: DPC client node management IP, supports fuzzy search (Optional, string, 1~256 characters)
        version: DPC client version, supports fuzzy search (Optional, string, 1~256 characters)
        status: DPC client status (Optional, string). valid values: normal (normal), abnormal (abnormal), disabled (disabled)
        switch_status: Node FSA switch status (Optional, string). valid values: on (true), off (false)
        upgrade_flag: Upgrade flag (Optional, string). valid values: required (upgrade required), not_required (no upgrade required)
        sort_key: Sort field (Optional, string). valid values: manage_ip (node management IP), dpc_mem (DPC client node memory)
        sort_dir: Sort direction (Optional, string). valid values: asc (ascending), desc (descending)
        page_no: Page number (Optional, int32, 1~10000000). default value: 1
        page_size: Records per page (Optional, int32, 1~1000). default value: 10

    Returns:
        {
            total: total (integer),
            data: DPC client data (List<DpcClient>). parameter format: [{
                id: ID (string),
                storage_id: storage ID (string),
                process_id: DPC client process ID (string),
                name: DPC client name (string),
                manage_ip: DPC client node management IP (string),
                version: DPC client version (string),
                status: DPC client status (string),
                switch_status: node FSA switch status (string),
                upgrade_flag: upgrade flag (string),
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
    Query DPC client details

    Args:
        client: DME API client
        id: Query DPC client ID (Required, string, 1~64 characters)

    Returns:
        {
            id: ID (string),
            storage_id: storage ID (string),
            process_id: DPC client process ID (string),
            name: DPC client name (string),
            manage_ip: DPC client node management IP (string),
            version: DPC client version (string),
            status: DPC client status (string),
        }
    """
    url = "/rest/fileservice/v1/dpc-clients/{id}"

    if not id:
        raise ValueError("id is a required parameter")

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
        id_in_storage: Dtree ID on the storage side(Optional), 1~256 characters
        name: Dtree name(Optional), 1~256 characters, supports fuzzy search
        device_name: Name of the storage device the dtree belongs to(Optional), 1~256 characters, supports fuzzy search
        storage_id: Dtree storage device ID(Optional), 1~64 characters, supports filtering
        zone_id: ID of the zone the dtree belongs to(Optional), 36 characters; only supported by OceanStor A800/A600 series storage
        manufacturer: Dtree storage device manufacturer(Optional), valid values: huawei (Huawei), third_part (third-party)
        tier_name: Service tier name (Optional, reserved field), 1~256 characters, supports fuzzy search
        fs_name: Name of the filesystem the dtree belongs to(Optional), 1~256 characters, supports fuzzy search
        fs_id: ID of the filesystem the dtree belongs to(Optional), 1~64 characters, mutually exclusive with namespace_id
        namespace_name: Name of the namespace the dtree belongs to(Optional), 1~64 characters
        namespace_id: ID of the namespace the dtree belongs to(Optional), 1~64 characters, mutually exclusive with fs_id
        quota_switch: Whether quota is enabled(Optional), true: enabled; false: disabled
        security_mode: Security mode(Optional), 1~32 characters; valid values: mixed (mixed security mode), native (native security mode), ntfs (ntfs security mode), unix (unix security mode)
        nas_locking_policy: NAS locking policy(Optional), valid values: mandatory (mandatory lock), advisory (advisory lock), unknown (Native security mode not enabled)
        sort_key: Sort field(Optional), valid values: nfs_count, cifs_count, dataturbo_count, name
        sort_dir: Sort direction(Optional), valid values: asc (ascending), desc (descending), default asc
        page_no: Page number for query(Optional), minimum 1, default 1
        page_size: Records per page(Optional), 1~1000, default 20
        dc_id: Data center ID(Optional), 1~128 characters, regex ^[_A-Fa-f0-9\\-]+$
        dc_name: Data center name(Optional), 1~256 characters

    Returns:
        {
            total: Dtree total (integer),
            dtrees: Dtree list (List<DtreeInfo>). parameter format: [{
                id: Dtree ID (string),
                name: Dtree name (string),
                path: path (string),
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
    Query specified Dtree details

    Args:
        client: DME API client
        dtree_id: Dtree ID (Required, string)

    Returns:
        {
            id: Dtree ID (string),
            name: Dtree name (string),
            path: path (string),
            fs_id: Filesystem ID (string),
        }
    """
    url = "/rest/fileservice/v1/dtrees/{dtree_id}"

    if not dtree_id:
        raise ValueError("dtree_id is a required parameter")

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

    Create Dtree, and share the Dtree via NFS, CIFS or DataTurbo.

    Args:
        client: DME API client
        storage_id: Dtree storage device ID, 1~64 characters
        create_dtrees_param: Dtree name and count info list (conditionally required). parameter format: [{
                dtree_name: Dtree name (1~255 characters, regex: ^[^,//:]+$, supports alphanumeric, spaces and some special characters; if creating multiple Dtrees in a single request, names start from 0000 and increment),
                count: Number of Dtrees to create in a single batch (int, max 500 per group, total sum of all groups up to 500),
             }, ...]
        fs_id: ID of the filesystem the dtree belongs to, mutually exclusive with namespace_id, required for centralized storage
        namespace_id: ID of the namespace the dtree belongs to, mutually exclusive with fs_id, required for distributed storage
        zone_id: ID of the zone the dtree belongs to, only supported by OceanStor A800/A600 series storage, length 36 characters
        parent_dir: Parent directory, valid for distributed storage, 1~4008 characters
        quota_switch: Quota switch, true/false, default false
        security_mode: Security mode, mixed/native/ntfs/unix. Required if model supports it. Supported by v3 series V300R006C60+, v5 series V500R007C50+, v6 series 6.1.2+
        nas_locking_policy: NAS locking policy, mandatory/advisory/unknown
        create_nfs_share_param: Associated creation of NFS share. Not supported when creating multiple Dtrees. Refer to action help: nas nfs_share create
        create_cifs_share_param: Associated creation of CIFS share. Not supported when creating multiple Dtrees. Refer to action help: nas cifs_share create
        dataturbo_share: Associated creation of DataTurbo share (Optional). parameter format: {
                description: DataTurbo share description (Optional, 0~255 characters),
                charset: Character set encoding (Required, fixed value UTF_8),
                dpc_share_auth: DataTurbo administrator list (Optional). parameter format: [{
                        dpc_user_id: DataTurbo administrator ID (Required, 0~64 characters),
                        permission: DataTurbo administrator permission (Required, fixed value read_and_write),
                     }, ...]
             }
        create_worm_param: WORM configuration (Optional). parameter format: {
                worm_mode: Policy mode (Required). valid values: enterprise_mode (enterprise), compliance_mode (compliance),
                min_protected_period: Minimum retention period (Required, 0~36817920, 0 means indefinite),
                min_protected_period_unit: Minimum retention period unit (Required). valid values: day, year, month, hour, minute. A310 or OceanStor Pacific 8.2.1+ support month/hour/minute,
                max_protected_period: Maximum retention period (Required, 0~36817920, 0 means indefinite),
                max_protected_period_unit: Maximum retention period unit (Required). valid values: day, year, month, hour, minute, infinite. A310 or OceanStor Pacific 8.2.1+ support month/hour/minute,
                def_protected_period: Default retention period (Required, 0~36817920, 0 means indefinite),
                def_protected_period_unit: Default retention period unit (Required). valid values: day, year, month, hour, minute, infinite. A310 or OceanStor Pacific 8.2.1+ support month/hour/minute,
                auto_lock_enabled: Auto-lock switch (Optional, default false; if true, files not modified within the specified time will be auto-locked),
                auto_lock_time: Auto-lock time (Optional, 1~64800; in days: 1~45, hours: 1~1080, minutes: 1~64800),
                auto_lock_unit: Auto-lock time unit (Optional). valid values: day, minute, hour,
                legal_hold_modify: Legal hold file modification permission (Optional, default false),
             }
        unix_permissions: Dtree directory permissions, regex [0-7]{3}, e.g., 755.
        task_remarks: Async task remark info, 0~1024 characters

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/fileservice/v1/dtrees"

    if not storage_id or not create_dtrees_param:
        raise ValueError("storage_id and create_dtrees_param are required parameters")

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
    Batch delete Dtree

    Args:
        client: DME API client
        dtree_ids: List of Dtree IDs to delete (Required, List[string])
        task_remarks: Async task remark info (Optional, string, up to 1024 characters)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/fileservice/v1/dtrees/delete"

    if not dtree_ids or len(dtree_ids) == 0:
        raise ValueError("dtree_ids is a required parameter")

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
    Modify specified Dtree

    Args:
        client: DME API client
        dtree_id: Dtree ID
        name: Dtree name
        quota_switch: Quota switch, true/false
        security_mode: Security mode, mixed/native/ntfs/unix
        nas_locking_policy: NAS locking policy, mandatory/advisory/unknown
        unix_permissions: Dtree directory permissions, e.g., 755
        task_remarks: Async task remark info

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
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
# NFS share sub-topic related actions
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
    Query NFS share list

    Args:
        client: DME API client
        id_in_storage: NFS ID on the storage side(Optional), 1~256 characters
        name: Share name(Optional), 1~256 characters, supports fuzzy search
        share_path: Share path(Optional), 1~256 characters, supports fuzzy search
        exact_share_path: Exact search for NFS share path(Optional), 1~1024 characters; when both share_path and exact_share_path have values, exact_share_path takes precedence
        device_name: Name of the storage device it belongs to(Optional), 1~256 characters, supports fuzzy search
        manufacturer: Storage device manufacturer(Optional), valid values: huawei (Huawei), third_part (third-party)
        storage_id: Storage device ID(Optional), 1~64 characters, supports filtering
        tier_name: Service tier name(Optional), 1~256 characters, supports fuzzy search
        owning_dtree_name: Name of the owning Dtree(Optional), 1~256 characters, supports fuzzy search
        fs_name: Filesystem name(Optional), 1~256 characters, supports fuzzy search
        fs_id: Filesystem ID(Optional), 1~64 characters
        owning_dtree_id: ID of the owning Dtree(Optional), 1~256 characters, supports filtering
        vstore_name: vStore name of the NFS share(Optional), 1~256 characters, supports fuzzy query
        page_no: Page number for query(Optional), minimum 1, default 1
        page_size: Records per page(Optional), 1~1000, default 20
        sort_key: Sort field(Optional), valid values: name, id_in_storage; when sorting by id_in_storage, only objects with numeric IDs are supported
        sort_dir: Sort direction(Optional), valid values: asc (ascending), desc (descending), default asc
        support_provisioning: Whether service provisioning is supported(Optional), true: yes; false: no; sending this field filters out resources from devices that do not support service provisioning, currently OceanStor Pacific series
        namespace_id: Namespace ID(Optional), 1~64 characters, only supported by OceanStor Pacific series storage devices
        namespace_name: Namespace name(Optional), 1~256 characters, supports fuzzy query, only supported by OceanStor Pacific series storage devices
        dc_id: Data center ID(Optional), 1~128 characters, regex ^[_A-Fa-f0-9\\-]+$
        dc_name: Data center name(Optional), 1~256 characters
        zone_id: Zone ID of the NFS share(Optional), 1~64 characters
        zone_name: Zone name of the NFS share(Optional), 1~256 characters, supports fuzzy search
        zone_ip: Zone management IP of the NFS share(Optional), 0~255 characters
        scope: Resource scope(Optional), valid values: local_scale (local), global_scale (global)

    Returns:
        {
            total: NFS share total (integer),
            nfs_shares: NFS share list. parameter format: [{
                id: share ID (string),
                name: share name (string),
                path: path (string),
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
    Query specified NFS share details

    Args:
        client: DME API client
        nfs_share_id: NFS share ID

    Returns:
        {
            id: share ID (string),
            name: share name (string),
            path: path (string),
            fs_id: Filesystem ID (string),
            export_ip: export IP (string),
        }
    """
    url = "/rest/fileservice/v1/nfs-shares/{nfs_share_id}"

    if not nfs_share_id:
        raise ValueError("nfs_share_id is a required parameter")

    response = client.get(url, params={"nfs_share_id": nfs_share_id})
    return response


def nfs_share_create(client: DMEAPIClient, create_nfs_share_param: dict,
                     task_remarks: str = None) -> dict:
    """
    Create NFS share

    Args:
        client: DME API client
        create_nfs_share_param: Create NFS share parameters. parameter format: {
                name: NFS share alias (Optional),
                description: description info (Optional),
                share_path: Share path (Required),
                character_encoding: Character encoding (Optional),
                audit_items: List of audit event types (Optional). parameter format: [{
                        audititem: Audit event type. valid values: none (no operation), all (all operations), open (open), create (create), read (read), write (write), close (close), delete (delete), rename (rename), get_security (get security attributes), set_security (set security attributes), get_attr (get attributes), set_attr (set attributes),
                     }, ...],
                show_snapshot_enable: Whether to show snapshots (Optional). valid values: true, false,
                nfs_share_client_addition: NFS share client permission list (Optional). parameter format: [{
                        name: Client IP or hostname or network group name (Required, 1~255 characters; network group name starts with @),
                        permission: Permission (Required). valid values: read (read), read_and_write (read and write), no_permission (no permission), read_and_write_not_del_rename (read and write, cannot delete or rename),
                        accesskrb5: krb5 permission (Optional). valid values: read, read_and_write, no_permission, read_and_write_not_del_rename,
                        accesskrb5i: krb5i permission (Optional). valid values: read, read_and_write, no_permission, read_and_write_not_del_rename,
                        accesskrb5p: krb5p permission (Optional). valid values: read, read_and_write, no_permission, read_and_write_not_del_rename,
                        write_mode: Write mode (Optional). valid values: synchronization (synchronous), asynchronization (asynchronous),
                        permission_constraint: Permission constraint (Required). valid values: all_squash, no_all_squash,
                        root_permission_constraint: Root permission constraint (Required). valid values: root_squash, no_root_squash,
                        source_port_verification: Source port verification restriction (Optional). valid values: secure (secure), insecure (insecure),
                        anonymous_user_id: Anonymous user ID (Optional),
                        access_protocol: Access protocol (Optional). valid values: nfsv3_and_nfsv4 (NFSv3 and NFSv4), nfsv3 (NFSv3 only), nfsv4 (NFSv4 only),
                     }, ...],
                file_name_extension_filters: File name extension filter rule list (Optional). parameter format: [{
                        file_name_ex_id_in_storage: Rule ID on storage (Optional, 1~64 characters, required when modifying an already added rule),
                        file_name_extension: File extension (Required, 1~127 characters, supports wildcards ? and *, * can only be the last character),
                        rule_type: Rule allow/reject (Optional, default reject). valid values: reject, permit,
                        fileoperations: Operation type list (Optional). valid values: close, create, create_dir, delete, delete_dir, getattr, link, lookup, open, read, write, rename, rename_dir, setattr, symlink,
                     }, ...],
                fs_id: Filesystem ID (mutually exclusive with namespace_id),
                namespace_id: Namespace ID (mutually exclusive with fs_id),
             }
        task_remarks: Async task remark info

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
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
    Modify specified NFS share

    Args:
        client: DME API client
        nfs_share_id: NFS share ID
        description: description info
        character_encoding: Character encoding, valid values: utf-8, zh, gbk, etc.
        audit_items: List of audit events (Optional). parameter format: [{
                audititem: Audit event type. valid values: none (no operation), all (all operations), open (open), create (create), read (read), write (write), close (close), delete (delete), rename (rename), get_security (get security attributes), set_security (set security attributes), get_attr (get attributes), set_attr (set attributes),
             }, ...]
        show_snapshot_enable: Whether to show snapshots
        nfs_share_client_addition: List of NFS share clients to add (Optional). parameter format: [{
                name: Client IP or hostname or network group name (Required, 1~255 characters),
                permission: Permission (Required). valid values: read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5: krb5 permission (Optional). valid values: read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5i: krb5i permission (Optional). valid values: read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5p: krb5p permission (Optional). valid values: read, read_and_write, no_permission, read_and_write_not_del_rename,
                write_mode: Write mode (Optional). valid values: synchronization (synchronous), asynchronization (asynchronous),
                permission_constraint: Permission constraint (Required). valid values: all_squash, no_all_squash,
                root_permission_constraint: Root permission constraint (Required). valid values: root_squash, no_root_squash,
                source_port_verification: Source port verification restriction (Optional). valid values: secure (secure), insecure (insecure),
                anonymous_user_id: Anonymous user ID (Optional, 0~4294967294),
             }, ...]
        nfs_share_client_modification: List of NFS share clients to modify (Optional). parameter format: [{
                nfs_share_client_id_in_storage: Client ID on storage (Required, 1~32 characters),
                permission: Permission (Required). valid values: read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5: krb5 permission (Optional). valid values: read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5i: krb5i permission (Optional). valid values: read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5p: krb5p permission (Optional). valid values: read, read_and_write, no_permission, read_and_write_not_del_rename,
                write_mode: Write mode (Optional). valid values: synchronization (synchronous), asynchronization (asynchronous),
                permission_constraint: Permission constraint (Required). valid values: all_squash, no_all_squash,
                root_permission_constraint: Root permission constraint (Required). valid values: root_squash, no_root_squash,
                source_port_verification: Source port verification restriction (Optional). valid values: secure (secure), insecure (insecure),
                anonymous_user_id: Anonymous user ID (Optional, 0~4294967294),
             }, ...]
        nfs_share_client_deletion: List of NFS share clients to delete (Optional). parameter format: [{
                nfs_share_client_id_in_storage: Client ID on storage (Required, 1~32 characters),
                name: Client IP or hostname or network group name (Optional, 1~32000 characters),
             }, ...]
        file_name_ex_filters: Extension name filter rule list (Optional). parameter format: [{
                update_type: Change type (Optional, default add). valid values: add (add), delete (delete), modify (modify),
                param: Extension name filter rule. attribute format: {
                        file_name_ex_id_in_storage: Rule ID on storage (Optional, 1~64 characters, required for modify),
                        file_name_extension: File extension (Required, 1~127 characters, supports wildcards ? and *, * can only be at the end),
                        rule_type: Rule allow/reject (Optional, default reject). valid values: reject (reject), permit (allow),
                        fileoperations: Operation type list (Optional). valid values: close, create, create_dir, delete, delete_dir, getattr, link, lookup, open, read, write, rename, rename_dir, setattr, symlink,
                }
             }, ...]
        task_remarks: Async task remark info

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
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
    Batch delete NFS shares

    Args:
        client: DME API client
        nfs_share_ids: List of NFS share IDs to delete
        task_remarks: Async task remark info

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
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
# CIFS share sub-topic related actions
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
        raw_id: CIFS share ID on the storage device(Optional), 1~256 characters
        name: CIFS share name(Optional), 1~256 characters, supports fuzzy query
        share_path: CIFS share path(Optional), 1~512 characters, supports fuzzy query
        exact_share_path: Exact search for CIFS share path(Optional), 1~1024 characters; when both share_path and exact_share_path have values, exact_share_path takes precedence
        fs_id: ID of the filesystem the CIFS share belongs to(Optional), 1~64 characters
        fs_name: Name of the filesystem the CIFS share belongs to(Optional), 1~256 characters, supports fuzzy query
        dtree_id: ID of the Dtree the CIFS share belongs to(Optional), 1~64 characters
        dtree_name: Name of the Dtree the CIFS share belongs to(Optional), 1~256 characters, supports fuzzy query
        storage_id: ID of the storage device the CIFS share belongs to(Optional), 1~64 characters
        storage_name: Name of the storage device the CIFS share belongs to(Optional), 1~256 characters, supports fuzzy query
        vstore_raw_id: ID of the vStore the CIFS share belongs to, assigned by the storage device(Optional), 1~256 characters
        vstore_name: Name of the vStore the CIFS share belongs to(Optional), 1~256 characters, supports fuzzy query
        manufacturer: Storage device manufacturer(Optional), valid values: huawei (Huawei), third_party (third-party)
        op_lock_enabled: Whether Oplock is enabled for the CIFS share(Optional), true: yes; false: no
        notify_enabled: Whether Notify is enabled for the CIFS share(Optional), true: yes; false: no
        offline_file_modes: Offline cache mode list for the CIFS share(Optional), List<OfflineFileMode> type, max array members 4. parameter format: [{
                        mode: Offline cache mode(Optional), valid values: none (disabled), manual (manual), documents (documents), programs (programs), default manual,
        },...]
        file_extension_filter_enabled: Whether file extension filtering is enabled for the CIFS share(Optional), true: yes; false: no
        abe_enabled: Whether ABE is enabled for the CIFS share(Optional), true: yes; false: no
        page_no: Page number(Optional), 1~10000000, default 1
        page_size: Records per page(Optional), 1~1000, default 10
        sort_key: Sort field(Optional), valid values: name, raw_id; when sorting by raw_id, only objects with numeric IDs are supported
        sort_dir: Sort direction(Optional), valid values: asc (ascending), desc (descending), default asc
        namespace_id: Namespace ID(Optional), 1~64 characters, only supported by OceanStor Pacific series storage devices
        namespace_name: Namespace name(Optional), 1~256 characters, supports fuzzy query, only supported by OceanStor Pacific series storage devices
        support_provisioning: Whether service provisioning is supported(Optional), true: yes; false: no; sending this field filters out resources from devices that do not support service provisioning, currently OceanStor Pacific series
        dc_id: Data center ID(Optional), 1~128 characters, regex ^[_A-Fa-f0-9\\-]+$
        dc_name: Data center name(Optional), 1~256 characters

    Returns:
        {
            total: CIFS share count (int32),
            cifs_shares: CIFS share list (List<CifsShare>). parameter format: [{
                id: share ID (string),
                raw_id: device-side ID (string),
                name: share name (string),
                share_path: share path (string),
                description: description (string),
                vstore_raw_id: tenant ID (string),
                vstore_name: tenant name (string),
                fs_id: Filesystem ID (string),
                fs_name: Filesystem name (string),
                storage_id: storage device ID (string),
                storage_name: storage device name (string),
                storage_ip: Storage device IP (string),
                op_lock_enabled: Whether OPLock is enabled. valid values: true, false,
                notify_enabled: Whether notification is enabled. valid values: true, false,
                offline_file_mode: Offline file mode (string),
                ca_enabled: Whether CA is enabled. valid values: true, false,
            }, ...],
        }
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
    Query specified CIFS share details

    Args:
        client: DME API client
        cifs_share_id: CIFS share ID

    Returns:
        {
            id: share ID (string),
            raw_id: device-side ID (string),
            name: share name (string),
            share_path: share path (string),
            description: description (string),
            vstore_raw_id: tenant ID (string),
            vstore_name: tenant name (string),
            fs_id: Filesystem ID (string),
            fs_name: Filesystem name (string),
            storage_id: storage device ID (string),
            storage_name: storage device name (string),
            storage_ip: Storage device IP (string),
            op_lock_enabled: Whether OPLock is enabled. valid values: true, false,
            notify_enabled: Whether notification is enabled. valid values: true, false,
            offline_file_mode: Offline file mode (string),
            ca_enabled: Whether CA is enabled. valid values: true, false,
            abe_enabled: Whether ABE is enabled. valid values: true, false,
            show_snapshot_enabled: Whether to show snapshot directory. valid values: true, false,
        }
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
        create_cifs_param: Create CIFS share parameters. parameter format: {
                name: Share name (Required),
                description: description info (Optional),
                share_path: Share path (Required),
                op_lock_enabled: Oplock feature switch (Optional),
                notify_enabled: Notify feature switch (Optional),
                ca_enabled: Failover continuous availability feature switch (Optional),
                offline_file_mode: Offline cache mode (Optional). valid values: none (disabled), manual (manual), documents (documents), programs (programs),
                ip_control_enabled: IP access control feature switch (Optional),
                abe_enabled: ABE feature switch (Optional),
                audititem_list: List of supported audit events (Optional). parameter format: [{
                        audititem: Audit event type (default none). valid values: none, all, open, create, read, write, close, delete, rename, get_security, set_security, get_attr, set_attr, get_xattr, set_xattr,
                     }, ...],
                apply_default_acl: Whether to add default ACL (Optional),
                file_extension_filter_enabled: Whether to enable file extension filtering (Optional),
                show_previous_versions_enabled: Whether to enable showing previous versions (Optional),
                show_snapshot_enabled: Whether to enable showing snapshots (Optional),
                user_and_user_group_info: List of users and user groups (Optional). parameter format: [{
                        user_or_user_group_id_in_storage: User or user group ID on storage (Optional, 1~64 characters, required for modification),
                        user_or_user_group_name: User name or user group name (Optional, 1~255 characters; user group name prefixed with @),
                        domain_type: Domain type (Optional, default local). valid values: ad_domain, ldap_domain, local, nis_domain,
                        permission: Permission (Optional, default read). valid values: read, full_control, forbidden, read_and_write, read_and_write_not_del_rename,
                     }, ...],
                ip_addresses_and_segments: IP address and IP address segment list (Optional). parameter format: [{
                        ip_or_segments_id_in_storage: IP address (segment) ID on storage (Optional, 1~64 characters, required for modification),
                        ip_addresses_or_segments: IP address (segment) (Optional, 1~128 characters, up to 32 entries),
                     }, ...],
                file_name_extension_filters: File extension filter rule list (Optional). parameter format: [{
                        file_name_ex_id_in_storage: Rule ID on storage (Optional, 1~64 characters, required when modifying an already added rule),
                        file_name_extension: File extension (Required, 1~127 characters, supports wildcards ? and *),
                        rule_type: Rule type (Optional, default reject). valid values: reject, permit,
                        fileoperations: Operation type list (Optional),
                     }, ...],
                smb3_encryption_enable: Whether to enable SMB3 encryption (Optional),
                unencrypted_access: Whether to allow unencrypted client access (Optional),
                enable_lease: Whether to enable lease lock (Optional),
             }
        fs_id: Filesystem ID, mutually exclusive with namespace_id
        namespace_id: Namespace ID, mutually exclusive with fs_id
        task_remarks: Async task remark info

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
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
    Modify specified CIFS share

    Args:
        client: DME API client
        cifs_share_id: CIFS share ID
        description: description info, up to 255 characters
        op_lock_enabled: Oplock feature switch
        notify_enabled: Notify feature switch
        ca_enabled: Failover continuous availability feature switch
        offline_file_mode: Offline cache mode, none/manual/documents/programs
        ip_control_enabled: IP access control feature switch
        abe_enabled: ABE feature switch
        audititem_list: List of supported audit events (Optional). parameter format: [{
                audititem: Audit event type (default none). valid values: none, all, open, create, read, write, close, delete, rename, get_security, set_security, get_attr, set_attr, get_xattr, set_xattr,
             }, ...]
        apply_default_acl: Whether to add default ACL
        file_extension_filter_enabled: Whether to enable file extension filtering
        show_previous_versions_enabled: Whether to enable showing previous versions
        show_snapshot_enabled: Whether to enable showing snapshots
        user_and_user_group_info: List of users and user groups (Optional). parameter format: [{
                update_type: Change type (Optional, default add). valid values: add (add), delete (delete), modify (modify),
                param: User and user group info object (Optional). attribute format: {
                        user_or_user_group_id_in_storage: User or user group ID on storage (Optional, 1~64 characters, required for modification),
                        user_or_user_group_name: User name or user group name (Optional, 1~255 characters; user group name prefixed with @),
                        domain_type: Domain type (Optional, default local). valid values: ad_domain, ldap_domain, local, nis_domain,
                        permission: Permission (Optional, default read). valid values: read, full_control, forbidden, read_and_write, read_and_write_not_del_rename,
                }
             }, ...]
        ip_and_segments: IP address and IP address segment list (Optional). parameter format: [{
                update_type: Change type (Optional, default add). valid values: add (add), delete (delete), modify (modify),
                param: IP address and IP address segment info object (Optional). attribute format: {
                        ip_or_segments_id_in_storage: IP address (segment) ID on storage (Optional, 1~64 characters, required for modification),
                        ip_addresses_or_segments: IP address (segment) (Optional, 1~128 characters, up to 32 entries),
                }
             }, ...]
        file_name_ex_filters: Extension name filter rule list (Optional). parameter format: [{
                update_type: Change type (Optional, default add). valid values: add (add), delete (delete), modify (modify),
                param: Extension name filter rule object (Optional). attribute format: {
                        file_name_ex_id_in_storage: Rule ID on storage (Optional, 1~64 characters, required when modifying an already added rule),
                        file_name_extension: File extension (Required, 1~127 characters, supports wildcards ? and *, * can only be the last character),
                        rule_type: Rule type (Optional, default reject). valid values: reject (reject), permit (allow),
                        fileoperations: Operation type list (Optional, up to 100),
                }
             }, ...]
        task_remarks: Async task remark info, 0~1024 characters
        smb3_encryption_enable: Whether to enable SMB3 encryption
        unencrypted_access: Whether to allow unencrypted client access
        enable_lease: Whether to enable lease lock

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
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
        task_remarks: Async task remark info

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
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
    Query permissions list of a single CIFS share

    Query the permissions info of a CIFS share, including users/user groups, IP addresses/IP address segments, file extension filter rules, etc.

    Args:
        client: DME API client
        cifs_share_id: CIFS share ID
        type: Permission type(Optional), valid values: user (user/user group), ip (IP address/IP address segment), file (file extension filter rule);
              when not specified, all permission types are returned

        user_filter: User permission filter parameters (Optional, dict type, valid when type=user). parameter format: {
                user_or_user_group_name: User/user group name(Optional), 1~256 characters, used to filter the user/user group list,
                domain_type: Domain type(Optional). valid values: ad_domain (AD domain user/group), ldap_domain (LDAP domain user/group), local (local user/group), nis_domain (NIS domain user/group),
                permissions: Permission filter list(Optional), List<Permission> type, max array members 4. parameter format: [{
                        permission: Permission(Optional). valid values: read (read), full_control (full control), forbidden (forbidden), read_and_write (read and write), read_and_write_not_del_rename (read and write, cannot delete or rename). default read,
                },...],
                user_or_user_group_raw_id: User/user group ID on the storage device(Optional), 1~256 characters,
        }

        ip_filter: IP permission filter parameters (Optional, dict type, valid when type=ip). parameter format: {
                ip_addresses_or_segments: IP address/IP address segment(Optional), 1~256 characters,
                ip_or_segments_raw_id: IP address/IP address segment ID on the storage device(Optional), 1~256 characters,
        }

        file_filter: File extension filter parameters (Optional, dict type, valid when type=file). parameter format: {
                rule_type: File extension type filter(Optional). valid values: reject (reject only), permit (allow only),
                file_name_extension: File extension name filter(Optional), 1~256 characters,
                file_extension_name_raw_id: File extension filter rule ID on storage(Optional), 1~256 characters,
        }

        # Common pagination and sorting parameters
        sort_key: Sort field(Optional), valid values: raw_id, name
        sort_dir: Sort direction(Optional), valid values: asc (ascending), desc (descending), default asc
        page_no: Page number(Optional), 1~10000000, default 1
        page_size: Records per page(Optional), 1~1000, default 10

    Returns:
        {
            permission_list: Permission list. parameter format: [{
                type: Permission type (string),
                rules: Rule list (List),
            }, ...],
        }
    """
    result = {'user': [], 'ip': [], 'file': []}

    # Query corresponding type of permissions based on the type parameter
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

    # If a specific type is specified, return only that type of permissions
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
# dataturbo_share (DataTurbo share) sub-topic related actions
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
        page_no: Page number(Optional), 1~10000000, default 1
        page_size: Records per page(Optional), 1~1000, default 10
        raw_id: DataTurbo share device-side ID(Optional), 1~1024 characters, exact query
        share_path: Share path(Optional), 1~1024 characters, supports fuzzy search
        fs_id: Filesystem ID of the DataTurbo share(Optional), 1~64 characters, exact query
        fs_name: Filesystem name of the DataTurbo share(Optional), 1~256 characters, supports fuzzy search
        dtree_id: Dtree ID of the DataTurbo share(Optional), 32 characters, regex ^[A-F0-9]{32}$, exact query
        dtree_name: Dtree name of the DataTurbo share(Optional), 1~256 characters, supports fuzzy query
        vstore_id: Tenant ID of the DataTurbo share(Optional), 1~64 characters, exact query
        vstore_raw_id: Tenant RAW ID of the DataTurbo share(Optional), 1~64 characters, exact query
        vstore_name: Tenant name of the DataTurbo share(Optional), 1~256 characters, supports fuzzy search
        storage_id: Storage device ID of the DataTurbo share(Optional), 1~64 characters, exact query
        storage_name: Storage device name of the DataTurbo share(Optional), 1~256 characters, supports fuzzy search
        zone_id: Zone ID of the DataTurbo share(Optional), 1~64 characters, exact query
        zone_name: Zone name of the DataTurbo share(Optional), 1~256 characters, supports fuzzy search
        scope: Resource scope(Optional), valid values: local_scale (local), global_scale (global)
        sort_key: Sort field(Optional), valid values: raw_id (device-side ID)
        sort_dir: Sort direction(Optional), valid values: asc (ascending), desc (descending), default asc

    Returns:
        {
            total: DataTurbo share count (int32),
            data: DataTurbo share list (List<DpcShare>). parameter format: [{
                id: share ID (string),
                raw_id: device-side ID (string),
                share_path: share path (string),
                fs_id: Filesystem ID (string),
                fs_name: Filesystem name (string),
                storage_id: storage device ID (string),
                storage_name: storage device name (string),
                vstore_id: tenant ID (string),
                vstore_raw_id: tenant device-side ID (string),
                vstore_name: tenant name (string),
                charset: character set (string),
            }, ...],
        }
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
    Query specified DataTurbo share details

    Args:
        client: DME API client
        dataturbo_share_id: DataTurbo share ID

    Returns:
        {
            id: share ID (string),
            raw_id: device-side ID (string),
            description: description (string),
            share_path: share path (string),
            fs_id: Filesystem ID (string),
            fs_name: Filesystem name (string),
            storage_id: storage device ID (string),
            storage_name: storage device name (string),
            storage_ip: Storage device IP (string),
            vstore_id: tenant ID (string),
            vstore_raw_id: tenant device-side ID (string),
            vstore_name: tenant name (string),
            charset: character set (string),
            zone_id: zone ID (string),
            zone_name: zone name (string),
            zone_ip: zone IP (string),
            scope: scope (string),
        }
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
        fs_id: ID of the filesystem to share, mutually exclusive with dtree_id, one must be provided
        dtree_id: ID of the Dtree to share, mutually exclusive with fs_id, one must be provided
        description: DataTurbo share description
        dataturbo_share_auth: DataTurbo administrator list (Optional). parameter format: [{
                dpc_user_id: DataTurbo administrator ID (Required, 1~64 characters),
                permission: DataTurbo administrator permission (Required, fixed value read_and_write),
             }, ...]
        task_remarks: Async task remark info

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
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
    Modify specified DataTurbo share

    Args:
        client: DME API client
        dataturbo_share_id: DataTurbo share ID
        description: DataTurbo share description
        dataturbo_share_auth_addition: List of DataTurbo administrators to add (Optional). parameter format: [{
                dpc_user_id: DataTurbo administrator ID (Required, 0~64 characters),
                permission: DataTurbo administrator permission (Required, fixed value read_and_write),
             }, ...]
        dataturbo_share_auth_deletion: List of DataTurbo administrator IDs to delete
        task_remarks: Async task remark info

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
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
    Batch delete DataTurbo shares

    Args:
        client: DME API client
        dataturbo_share_ids: DataTurbo share ID list
        task_remarks: Async task remark info

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
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
    Query DataTurbo share administrator permission list

    Args:
        client: DME API client
        dataturbo_share_id: DataTurbo share ID
        page_no: Page number(Optional), 1~10000000, default 1
        page_size: Records per page(Optional), 1~1000, default 10
        user_id: DataTurbo administrator ID(Optional), 1~64 characters, exact query
        user_name: DataTurbo administrator name(Optional), 1~256 characters, supports fuzzy search
        permission: DataTurbo administrator permission(Optional), valid values: read_and_write (read and write)

    Returns:
        {
            total: Permission count (int32),
            data: Permission list (List<DpcShareAuth>). parameter format: [{
                user_id: user ID (string),
                user_name: user name (string),
                permission: permission (string),
            }, ...],
        }
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
# Quota (quota) sub-topic related actions
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
        page_no: Page number for query(Optional), minimum 1, default 1
        page_size: Records per page(Optional), 1~1000, default 20
        ids: Quota ID list(Optional), List<string> type, max array members 100
        raw_ids: Quota device-side ID list(Optional), List<string> type, 0~1024 characters, max array members 100
        quota_type: Quota type(Optional), valid values: directory_quota (directory quota), user_quota (user quota), user_group_quota (user group quota)
        parent_type: Quota parent object type(Optional), 0~32 characters; valid values: filesystem (Filesystem or Namespace, OceanStor Pacific devices call it Namespace, other devices call it Filesystem), qtree (Quota Tree or Dtree, OceanStor V3/V5 devices call it Quota Tree, other devices call it Dtree)
        parent_raw_id: Quota parent object ID on the storage device(Optional), 0~256 characters, supports exact match; when parent_type is filesystem, it's the Filesystem or Namespace ID on the storage device; when parent_type is qtree, it's the Quota Tree or Dtree ID on the storage device
        owner_name: Quota-associated user or user group name(Optional), 0~256 characters, supports fuzzy query
        vstore_id: Tenant ID of the quota(Optional), 0~64 characters
        vstore_raw_id: Tenant storage device ID of the quota(Optional), 0~256 characters, supports exact match
        storage_id: Quota storage device ID(Optional), 0~64 characters
        sort_key: Query sort field(Optional), valid values: id, space_hard_used_rate (space usage rate), file_hard_used_rate (file usage rate), default id
        sort_dir: Sort direction(Optional), valid values: asc (ascending), desc (descending), default asc
        zone_id: Zone id(Optional), 0~64 characters, only supported by OceanStor A800 storage

    Returns:
        {
            total: Quota count (int32),
            datas: Quota list (List<QuotaListItem>). parameter format: [{
                id: quota ID (string),
                raw_id: device-side ID (string),
                quota_type: quota type (string),
                parent_type: parent object type (string),
                owner_name: owner name (string),
                space_soft_quota: space soft quota (string),
                space_hard_quota: space hard quota (string),
                space_hard_used_rate: space hard quota usage rate (string),
                file_hard_quota: file hard quota (string),
                file_hard_used: files used (string),
            }, ...],
        }
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
    Query specified quota details

    Args:
        client: DME API client
        quota_id: Quota ID

    Returns:
        {
            id: quota ID (string),
            raw_id: device-side ID (string),
            quota_type: quota type (string),
            parent_type: parent object type (string),
            owner_name: owner name (string),
            space_soft_quota: space soft quota (string),
            space_hard_quota: space hard quota (string),
            file_hard_quota: file hard quota (string),
            file_hard_used: files used (string),
        }
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
        space_soft_quota: Space soft quota(Optional), unit Byte, default -1 (field invalid); when both hard and soft space quotas are valid, hard must be greater than soft; for OceanStor V5 devices, this field must be a multiple of 1048576
        space_hard_quota: Space hard quota(Optional), unit Byte, default -1 (field invalid); when both hard and soft space quotas are valid, hard must be greater than soft; for OceanStor V5 devices, this field must be a multiple of 1048576
        space_advisory_quota: Space advisory quota(Optional), unit Byte, default -1 (field invalid); only supported by OceanStor Pacific devices; when advisory and hard/soft space quotas are both valid, advisory must be less than hard or soft
        file_soft_quota: File soft quota(Optional), default -1 (field invalid); when both hard and soft file quotas are valid, hard must be greater than soft
        file_hard_quota: File hard quota(Optional), default -1 (field invalid); when both hard and soft file quotas are valid, hard must be greater than soft
        file_advisory_quota: File advisory quota(Optional), default -1 (field invalid); only supported by OceanStor Pacific devices; when advisory and hard/soft file quotas are both valid, advisory must be less than hard or soft
        snap_space_switch: Whether to count snapshot space(Optional), default false; true: count snapshot space; false: do not count snapshot space; only supported by OceanStor Pacific devices
        soft_grace_time: Grace period(Optional), 0~4294967294, unit (day); indicates how long after soft quota is exceeded before automatically transitioning to hard limit; not passing or value 0 means only warning when soft quota is reached; only supported by OceanStor Pacific
        parent_id: Parent resource ID (Required), 1~64 characters
        parent_type: Parent resource type (Required), valid values: filesystem (Filesystem), dtree (dtree, storage cluster not supported), namespace (Namespace)
        quota_type: Quota type (Required), valid values: directory_quota (directory quota), user_quota (user quota), user_group_quota (user group quota)
        quota_owner: Quota user (conditionally required), QuotaOwner object. parameter format: {
                        name: User (group) name (Required), 1~64 characters, * means all users (groups),
                        type: User (group) type (Required), when quota_type is user_quota, valid values: unix_local_user (unix local user), domain_user (domain user), windows_user (windows user); when quota_type is user_group_quota, valid values: unix_local_user_group (unix local user group), domain_user_group (domain user group), windows_user_group (windows user group),
                        domain_type: Domain user type (conditionally required), required when type is domain_user or domain_user_group; valid values: local (local), ad_domain (AD domain), ldap_domain (LDAP domain), nis_domain (NIS domain); OceanStor Pacific, OceanStor Dorado V6, OceanProtect support this field,
        }
        dir_quota_target: Directory quota target(Optional), valid values: dtree (template directory quota, applies to all Dtrees under the current Filesystem), filesystem (root directory quota, applies to the current Filesystem); valid when parent resource type is filesystem and quota type is directory_quota
        task_remarks: Async task remark info

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
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
        client: DME API client
        quota_id: Quota ID
        space_soft_quota: Space soft quota(Optional), unit Byte, -1 means field invalid; when both hard and soft space quotas are valid, hard must be greater than soft
        space_hard_quota: Space hard quota(Optional), unit Byte, -1 means field invalid; when both hard and soft space quotas are valid, hard must be greater than soft
        space_advisory_quota: Space advisory quota(Optional), unit Byte, -1 means field invalid; only supported by OceanStor Pacific devices; when advisory and hard/soft space quotas are both valid, advisory must be less than hard or soft
        file_soft_quota: File soft quota(Optional), -1 means field invalid; when both hard and soft file quotas are valid, hard must be greater than soft
        file_hard_quota: File hard quota(Optional), -1 means field invalid; when both hard and soft file quotas are valid, hard must be greater than soft
        file_advisory_quota: File advisory quota(Optional), -1 means field invalid; only supported by OceanStor Pacific devices; when advisory and hard/soft file quotas are both valid, advisory must be less than hard or soft
        snap_space_switch: Whether to count snapshot space(Optional), true: count snapshot space; false: do not count snapshot space; only supported by OceanStor Pacific devices
        soft_grace_time: Grace period(Optional), 0~4294967294, unit (day); indicates how long after soft quota is exceeded before automatically transitioning to hard limit; not sending or value 0 means only warning when soft quota is reached; only supported by OceanStor Pacific
        task_remarks: Async task remark info

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
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
    Batch delete quotas

    Args:
        client: DME API client
        quota_ids: List of quota IDs to delete
        task_remarks: Async task remark info

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
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
# filesystem (Filesystem) sub-topic related actions
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
    Batch query Filesystem

    Args:
        client: DME API client
        page_no: Page number for query(Optional), 1~10000000
        page_size: Records per page(Optional), 1~1000, default 100
        sort_dir: Sort direction(Optional), valid values: asc (ascending), desc (descending)
        sort_key: Sort parameter(Optional), valid values: capacity, available_capacity, capacity_usage_ratio,
                  nfs_count, cifs_count, dpc_count, dtree_count, name, allocate_pool_quota,
                  fs_raw_id, create_time, total_capacity_in_byte, available_capacity_in_byte,
                  alloc_capacity_in_byte, protection_capacity_in_byte, max_file_count, used_file_count
        name: Filesystem name(Optional), 1~256 characters, mutually exclusive with fs_raw_id, supports fuzzy match
        is_associated_qos: Whether Filesystem is associated with QoS(Optional), true: yes; false: no
        qos_id: QoS policy ID(Optional), 1~256 characters
        storage_name: Filesystem device name(Optional), 1~256 characters, mutually exclusive with storage_id, supports fuzzy match
        manufacturer: Storage device manufacturer(Optional), 1~64 characters; valid values: huawei (Huawei), dell_emc (DELL EMC),
                     fujitsu (FUJITSU), hitachi (Hitachi), hpe (HPE), ibm (IBM), netapp (NetApp),
                     pure (PURE), panji (Panji), third_part (non-Huawei storage device)
        storage_pool_name: Filesystem storage pool name(Optional), 1~256 characters, mutually exclusive with storage_pool_id, supports fuzzy match
        storage_pool_id: Storage pool ID(Optional), 1~255 characters, mutually exclusive with storage_pool_name
        tier_name: Filesystem service tier name(Optional), 1~256 characters, mutually exclusive with tier_id, supports fuzzy match
        tier_id: Service tier ID(Optional), 1~256 characters, mutually exclusive with tier_name, exact match
        vstore_name: Filesystem vStore name(Optional), 1~256 characters, mutually exclusive with vstore_raw_id, supports fuzzy match
        vstore_raw_id: Filesystem tenant ID on the storage device(Optional), 1~64 characters, mutually exclusive with vstore_name
        project_name: Filesystem business group name(Optional), 1~256 characters, mutually exclusive with project_id, supports fuzzy match
        project_id: Business group ID(Optional), 1~256 characters, mutually exclusive with project_name, exact match
        storage_id: Owning storage device ID(Optional), 1~256 characters, mutually exclusive with storage_name, exact match
        fs_raw_id: Filesystem ID on the device(Optional), 1~256 characters, mutually exclusive with name
        health_status: Health status(Optional), valid values: normal (normal), faulty (faulty), unknown (unknown)
        running_status: Running status(Optional), valid values: online (online), offline (offline), invalid (invalid),
                       initializing (initializing), unknown (unknown)
        alloc_type: Filesystem allocation type(Optional), valid values: thin (on-demand), thick (fixed)
        type: Filesystem type(Optional), valid values: normal (normal filesystem), worm (worm filesystem),
              migration (migration filesystem), container (container application filesystem), hash (hash filesystem),
              smart_mobility_internal (SmartMobility internal filesystem)
        protection: Protection status(Optional), valid values: protected (protected), not_protected (not protected)
        dc_id: Data center ID(Optional), 1~128 characters, regex ^[_A-Fa-f0-9\\-]+$
        dc_name: Data center name(Optional), 1~256 characters
        zone_id: Zone ID(Optional), 1~256 characters; only OceanStor A800 series filesystems support search, passing clusterID queries global filesystems
        product_name: Filesystem device product name(Optional), 1~256 characters, supports fuzzy search
        description: Filesystem description info(Optional), 1~255 characters
        tag_filters: Tag filter list(Optional), List<TagFilters> type, max array members 11. parameter format: [{
                        tag_ids: Tag ID list(Optional), max array members 10, multiple tags use OR relation,
                        tag_type_id: Tag type ID(Optional), regex ^[a-fA-F0-9]{32}$,
                        operator: Filter condition (Required), valid values: contain (contains), not_contain (does not contain),
        },...]

    Returns:
        {
            total: Filesystem count (int32),
            data: Filesystem list (List<FileSystemSummary>). parameter format: [{
                id: Filesystem ID (string),
                fs_raw_id: device-side ID (string),
                name: name (string),
                description: description (string),
                health_status: health status (string),
                running_status: running status (string),
                alloc_type: allocation type. valid values: thin, thick,
                type: type (string),
                protection: protection status (string),
                capacity: capacity (string),
                available_capacity: available capacity (string),
                total_capacity_in_byte: total capacity (int64, bytes),
                available_capacity_in_byte: available capacity (int64, bytes),
                nfs_count: NFS share count (int32),
                cifs_count: CIFS share count (int32),
                dpc_count: DPC client count (int32),
                dtree_count: dtree count (int32),
                storage_id: storage device ID (string),
                storage_name: storage device name (string),
                storage_ip: Storage device IP (string),
            }, ...],
        }
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
    Query specified Filesystem details

    Args:
        client: DME API client
        filesystem_id: Filesystem ID

    Returns:
        {
            id: Filesystem ID (string),
            fs_raw_id: device-side ID (string),
            name: name (string),
            description: description (string),
            health_status: health status (string),
            running_status: running status (string),
            alloc_type: allocation type. valid values: thin, thick,
            type: type (string),
            protection: protection status (string),
            capacity: capacity (string),
            available_capacity: available capacity (string),
            total_capacity_in_byte: total capacity (int64, bytes),
            available_capacity_in_byte: available capacity (int64, bytes),
            nfs_count: NFS share count (int32),
            cifs_count: CIFS share count (int32),
            dpc_count: DPC client count (int32),
            dtree_count: dtree count (int32),
            storage_id: storage device ID (string),
            storage_name: storage device name (string),
            storage_ip: Storage device IP (string),
            storage_type: storage device type (string),
        }
    """
    url = "/rest/fileservice/v1/filesystems/{filesystem_id}"

    response = client.get(url, params={"filesystem_id": filesystem_id})
    return response


def filesystem_delete(client: DMEAPIClient, filesystem_ids: list, task_remarks: str = None) -> dict:
    """
    Batch delete Filesystem

    Args:
        client: DME API client
        filesystem_ids: Filesystem ID list
        task_remarks: Async task remark info(Optional)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
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
    Batch modify Filesystem

    Only supports modifying names.

    Args:
        client: DME API client
        filesystems: List of Filesystem info to modify (Required), List<UpdateFileSystemInfo> type, max array members 1000. parameter format: [{
                        file_system_id: Unique identifier of the Filesystem (Required), 1~64 characters,
                        name: Filesystem name (Required), 1~255 characters; OceanStor Dorado V6, OceanStor, OceanProtect series can only contain letters, digits, "-", "." and national language characters; OceanStor V3/V5 series can only contain letters, digits and Chinese characters,
        },...]
        task_remarks: Async task remark info(Optional), 0~1024 characters

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
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
    Custom create Filesystem

    Args:
        client: DME API client
        storage_id: Storage device ID
        pool_raw_id: Storage pool ID on the specified storage device
        filesystem_specs: Filesystem spec list. parameter format: [{
                name: name (Required, 1~255 characters),
                count: count (Required, 1~500),
                start_suffix: Starting suffix number (Optional, 0~9999),
                capacity: capacity GB (Required, 1~262144),
                description: description (Optional, 0~255 characters),
             }, ...]
        vstore_id: Tenant ID(Optional)
        zone_id: Zone ID(Optional)
        task_remarks: Async task remark info(Optional)
        gfs_group_id: Global data space ID(Optional)
        automatic_update_time: Whether to update access time(Optional)
        atime_update_mode: Atime update frequency, hour/day/close(Optional)
        schedule_name: Scheduled HyperCDP plan name(Optional)
        quota_switch: Whether to enable quota(Optional)
        vaai_switch: VAAI switch(Optional)
        initial_distribute_policy: Initial capacity distribution policy, auto/highest_perf/performance/capacity(Optional)
        capacity_threshold: Total space capacity alarm threshold 50-99(Optional)
        tuning: Tuning parameters (Optional). parameter format: {
                deduplication_enabled: Whether to enable deduplication (Optional, default false). valid values: true, false,
                compression_enabled: Whether to enable compression (Optional, default false). valid values: true, false,
                block_size: Filesystem block size KB (Optional, default 64). valid values: 4, 8, 16, 32, 64, 128,
                allocation_type: Allocation type (Optional, default thin). valid values: thin, thick,
                qos_policy_id: QoS policy ID (Optional),
                application_scenario: Application scenario (Optional, default user_defined). valid values: database, VM, user_defined, container,
                workload_type_id: Workload type id (Optional, 1~32 characters),
                dist_alg: Filesystem directory distribution strategy (Optional, only supported by A800 devices). valid values: capacity_balance, subdirectory_round_robin,
                qos_policy: SmartQos policy parameter info (Optional). attribute format: {
                        max_bandwidth: max bandwidth MB/s (Optional, 1~999999999),
                        max_iops: max iops (Optional, 1~999999999),
                        min_bandwidth: min bandwidth MB/s (Optional, 1~999999999),
                        min_iops: min iops (Optional, 1~999999999),
                        burst_band_width: Burst bandwidth MB/s (Optional),
                        burst_iops: Burst IOPS (Optional),
                        burst_time: Max burst time seconds (Optional),
                        latency: latency (Optional, only supports lower limit protection),
                        max_read_bandwidth: Max read bandwidth MB/s (Optional),
                        max_write_bandwidth: Max write bandwidth MB/s (Optional),
                        burst_read_band_width: Burst read bandwidth MB/s (Optional),
                        burst_write_band_width: Burst write bandwidth MB/s (Optional),
                        max_read_iops: Max read iops (Optional),
                        max_write_iops: Max write iops (Optional),
                        burst_read_iops: Burst read iops (Optional),
                        burst_write_iops: Burst write iops (Optional),
                        schedule_policy: Schedule policy (Optional). valid values: once, daily, weekly,
                        schedule_start_date: Effective start date (Optional, format yyyy-MM-dd),
                        start_time: Effective start time (Optional, format hh:mm),
                        duration: Effective duration seconds (Optional, 1800~86400),
                        weekly_days: Weekly schedule days (Optional, 1~6 for Monday to Saturday),
                        alarm_switch: Upper limit alarm switch (Optional). valid values: off, on,
                        alarm_level: Severity (Optional). valid values: event, alarm,
                        alarm_threshold: Alarm threshold % (Optional, 0~100),
                        resume_threshold: Recovery threshold % (Optional, 0~100),
                        storage_divice_id: Storage device id (Optional),
                        name: QoS name (Optional),
                        description: description (Optional),
                        iotype: Policy type (Optional). valid values: 2 (total upper limit), 3 (read/write upper limit),
                        vstore_id: Owning tenant id (Optional),
                        vstore_name: Owning tenant name (Optional),
                        global_flag: Whether global (Optional),
                }
             }
        create_cifs_share_param: Auto-create CIFS share parameters(Optional). Refer to action help: nas cifs_share create
        create_nfs_share_param: Auto-create NFS share parameters(Optional). Refer to action help: nas nfs_share create
        create_dpc_share_param: Auto-create DataTurbo share parameters(Optional). Refer to action help: nas dataturbo_share create
        owning_controller: Owning controller(Optional), 2~16 characters, format like 0A, 1B
        snapshot_expired_enabled: Whether to delete old read-only snapshots(Optional). true/false, default false
        checksum_enabled: Data checksum switch(Optional). true/false, default true
        ads_enabled: Whether to enable alternate data streams(Optional). true/false, default true
        security_mode: Security mode(Optional). values: mixed/native/ntfs/unix
        nas_locking_policy: NAS locking policy(Optional). values: mandatory/advisory/unknown
        capacity_autonegotiation: Capacity auto-negotiation parameters (Optional). parameter format: {
                capacity_self_adjusting_mode: Capacity auto-adjustment mode (Optional, default false). valid values: grow_off (false), grow (auto expand), grow_shrink (auto expand and shrink),
                capacity_recycle_mode: Capacity recycle mode (Optional, default prioritize expansion). valid values: expand_capacity (prioritize expansion), delete_snapshots (prioritize deleting old snapshots),
                auto_size_enable: Auto-size switch (Optional, default true). valid values: true, false,
                auto_grow_threshold_percent: Auto-grow trigger threshold % (Optional, 2~99, default 85),
                auto_shrink_threshold_percent: Auto-shrink trigger threshold % (Optional, 1~98, default 50),
                max_auto_size: Auto-grow upper limit GB (Optional, 1~33554432, default 33554432),
                min_auto_size: Auto-shrink lower limit GB (Optional, 1~33554432, default 33554432),
                auto_size_increment: Single change amount for auto expand/shrink MB (Optional, 64~102400, default 1024),
             }
        worm: Filesystem WORM parameters (Optional). parameter format: {
                type: WORM protection mode (Optional). valid values: none_mode (no default policy), enterprise_mode (enterprise compliance), compliance_mode (regulatory compliance), advance_mode (advanced compliance), audit_log (audit log), non_worm (non-WORM),
                min_protect_period: Minimum protection period (Optional, default 0),
                min_protect_period_unit: Minimum protection period unit (Optional, default year). valid values: minute, hour, day, month, year,
                max_protect_period: Maximum protection period (Optional, 0~4294967295, default 70),
                max_protect_period_unit: Maximum protection period unit (Optional, default year). valid values: minute, hour, day, month, year,
                def_protect_period: Default protection period (Optional, not less than min, not greater than max, default 70),
                def_protect_period_unit: Default protection period unit (Optional, default year). valid values: minute, hour, day, month, year,
                auto_lock: WORM auto-lock mode (Optional, default true). valid values: true, false,
                auto_lock_time: Auto-lock time (Optional, default 2),
                auto_lock_time_unit: Auto-lock time unit (Optional, default hour). valid values: minute, hour, day, month, year,
                auto_del: Auto-delete mode (Optional, default false). valid values: true, false,
                is_worm_audit_log_fs: WORM audit log Filesystem (Optional, default false). valid values: true, false,
                worm_append_unit: WORM append file protection granularity (Optional, only supported by advance_mode). valid values: 256KB, 512KB, 1M,
             }
        snapshot_reserved_space_percentage: Snapshot reserved space percentage(Optional), 0~90
        periodic_snapshots_limit: Periodic snapshot count limit(Optional), 1~2048
        snapshot_dir_visible: Whether the snapshot directory is visible(Optional). true/false
        object_service_optimization: Object service optimization(Optional). true/false
        case_sensitive: Case sensitive mode(Optional). true/false
        audit_log_rules: Audit log rule set(Optional), e.g.: set_security, get_security, set_attr, get_attr, etc., up to 100
        unix_permissions: Filesystem directory permissions(Optional), format like 0755

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
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
    Query available Filesystems

    Query Filesystems that can be used for adding or removing features. Currently only supports Filesystems that can be configured for remote replication.

    Args:
        client: DME API client
        feature_type: Feature type, currently only supports remote_replication (remote replication)
        local_storage_id: Local storage device ID
        remote_storage_id: Remote storage device ID (required when feature_type is remote_replication)
        name: Local Filesystem name, supports fuzzy search
        page_no: Page number for query, default 1
        page_size: Records per page, default 20
        sort_key: Sort field, name (Filesystem name) or capacity (Filesystem capacity)
        sort_dir: Sort direction, asc (ascending) or desc (descending)

    Returns:
        {
            total: Available Filesystem count (int32),
            available_filesystems: Available Filesystem list (List<AvailableFilesystemResponse>). parameter format: [{
                id: Filesystem ID (string),
                name: Filesystem name (string),
                capacity: capacity (string),
            }, ...],
        }
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
    Modify specified Filesystem

    Args:
        client: DME API client
        file_system_id: Filesystem unique identifier
        name: Filesystem name, 1~255 characters(Optional)
        description: description info, 0~255 characters(Optional)
        capacity: Filesystem capacity, unit GB, 1~33554432(Optional)
        capacity_threshold: Total space capacity alarm threshold 50-99(Optional)
        initial_distribute_policy: Initial capacity distribution policy, auto/highest_perf/performance/capacity(Optional)
        automatic_update_time: Whether to update access time after file read, true/false(Optional)
        atime_update_mode: Atime update frequency, hour (hourly)/day (daily)/close (disabled)(Optional)
        quota_switch: Whether to enable quota, true enable/false disable(Optional)
        vaai_switch: VAAI switch, cannot be disabled after enabled, true enabled/false not enabled(Optional)
        owning_controller: Owning controller, 2~16 characters(Optional)
        snapshot_expired_enabled: Whether to delete old read-only snapshots, true/false(Optional)
        checksum_enabled: Data checksum switch, true/false(Optional)
        ads_enabled: Whether to enable alternate data streams, true/false, cannot be disabled after enabled(Optional)
        security_mode: Security mode, mixed/native/ntfs/unix(Optional)
        nas_locking_policy: NAS locking policy, mandatory (mandatory lock)/advisory (advisory lock)/unknown(Optional)
        snapshot_reserved_space_percentage: Snapshot reserved space percentage, 0~90(Optional)
        periodic_snapshots_limit: Periodic snapshot count limit, 1~2048(Optional)
        snapshot_dir_visible: Whether the snapshot directory is visible, true visible/false invisible(Optional)
        tuning: Tuning parameters (Optional). parameter format: {
                qos_policy: SmartQos policy parameter info (UpdateFileSystemQosPolicy object). attribute format: {
                        max_bandwidth: max bandwidth MB/s (Optional, 1~999999999; mutually exclusive with min_bandwidth/min_iops, not mutually exclusive on A800),
                        max_iops: max IOPS (Optional, 1~999999999; mutually exclusive with min_bandwidth/min_iops, not mutually exclusive on A800),
                        min_bandwidth: min bandwidth MB/s (Optional, 1~999999999; mutually exclusive with max_bandwidth/max_iops, not mutually exclusive on A800),
                        min_iops: min IOPS (Optional, 1~999999999; mutually exclusive with max_bandwidth/max_iops, not mutually exclusive on A800),
                        burst_band_width: Burst bandwidth MB/s (Optional, 1~999999999),
                        burst_iops: Burst IOPS (Optional, 1~999999999),
                        burst_time: Max burst time seconds (Optional, 1~999999999),
                        latency: latency (Optional, 1~999999999; A800/Dorado V6 optional 500/1500 unit us, V3/V5 customizable unit ms),
                        max_read_bandwidth: Max read bandwidth MB/s (Optional, 1~999999999; only valid for read/write upper limit policy),
                        max_write_bandwidth: Max write bandwidth MB/s (Optional, 1~999999999; only valid for read/write upper limit policy),
                        burst_read_band_width: Burst read bandwidth MB/s (Optional, 1~999999999; only valid for read/write upper limit policy),
                        burst_write_band_width: Burst write bandwidth MB/s (Optional, 1~999999999; only valid for read/write upper limit policy),
                        max_read_iops: Max read IOPS (Optional, 1~999999999; only valid for read/write upper limit policy),
                        max_write_iops: Max write IOPS (Optional, 1~999999999; only valid for read/write upper limit policy),
                        burst_read_iops: Burst read IOPS (Optional, 1~999999999; only valid for read/write upper limit policy),
                        burst_write_iops: Burst write IOPS (Optional, 1~999999999; only valid for read/write upper limit policy),
                        schedule_policy: Schedule policy (Optional). valid values: once, daily, weekly,
                        schedule_start_date: Effective start date (Optional, format yyyy-MM-dd, 0~64 characters),
                        start_time: Effective start time (Optional, format hh:mm, 0~64 characters),
                        duration: Effective duration seconds (Optional, 1800~86400),
                        weekly_days: Weekly schedule days (Optional, 0-6 for Sunday to Saturday, max 7; effective when schedule_policy is weekly),
                        alarm_switch: Upper limit alarm switch (Optional). valid values: off, on,
                        alarm_level: Upper limit severity (Optional). valid values: event (event), alarm (alarm),
                        alarm_threshold: Upper limit alarm threshold % (Optional, 0~100),
                        resume_threshold: Upper limit alarm recovery threshold % (Optional, 0~100),
                        storage_divice_id: Owning storage device ID (Optional, 1~64 characters),
                        name: QoS name (Optional, 1~255 characters; unused on A800),
                        description: QoS description (Optional, 1~255 characters; unused on A800),
                        iotype: Policy type (Optional). valid values: 2 (total performance upper limit), 3 (read/write upper limit; only supported by some devices),
                        vstore_id: Owning tenant ID (Optional, 1~64 characters; unused on A800),
                        vstore_name: Owning tenant name (Optional, 1~64 characters; unused on A800),
                        global_flag: Whether global (Optional; current version only supports global; unused on A800),
                        qos_policy_id: QoS policy ID (Optional, 0~64 characters; mutually exclusive with other parameters except enabled),
                        enabled: Whether to enable QoS Policy (Optional, default false),
                },
                deduplication_enabled: Deduplication (Optional, default false),
                compression_enabled: Compression (Optional, default false),
                allocation_type: Filesystem allocation type (Optional, default thin). valid values: thin (thin), thick (thick),
             }
        capacity_autonegotiation: Capacity auto-negotiation parameters (Optional). parameter format: {
                capacity_self_adjusting_mode: Capacity auto-adjustment mode (Optional, default false). valid values: grow_off (false), grow (auto expand), grow_shrink (auto expand and shrink),
                capacity_recycle_mode: Capacity recycle mode (Optional, default prioritize expansion). valid values: expand_capacity (prioritize expansion), delete_snapshots (prioritize deleting old snapshots),
                auto_size_enable: Auto-size switch (Optional, default on). valid values: true, false,
                auto_grow_threshold_percent: Auto-grow trigger threshold % (Optional, 2~99, default 85; must be greater than shrink trigger threshold),
                auto_shrink_threshold_percent: Auto-shrink trigger threshold % (Optional, 1~98, default 50),
                max_auto_size: Auto-grow upper limit GB (Optional, 1~33554432, default 33554432; must be greater than or equal to shrink lower limit and Filesystem capacity),
                min_auto_size: Auto-shrink lower limit GB (Optional, 1~33554432, default 33554432),
                auto_size_increment: Single change amount for auto expand/shrink MB (Optional, 64~102400, default 1024),
             }
        worm: Filesystem WORM parameters (Optional). parameter format: {
                type: WORM protection compliance mode (Optional). valid values: none_mode, enterprise_mode, compliance_mode, advance_mode, audit_log, non_worm,
                min_protect_period: Minimum protection period (Optional, 0~4294967295, default 0; 4294967295 is indefinite),
                min_protect_period_unit: Minimum protection period unit (Optional, default year). valid values: minute, hour, day, month, year,
                max_protect_period: Maximum protection period (Optional, 1~4294967295, default 70; 4294967295 is indefinite),
                max_protect_period_unit: Maximum protection period unit (Optional, default year). valid values: minute, hour, day, month, year,
                def_protect_period: Default protection period (Optional, 0~4294967295, default 70; not less than min and not greater than max),
                def_protect_period_unit: Default protection period unit (Optional, default year). valid values: minute, hour, day, month, year,
                auto_lock: WORM auto-lock mode (Optional, default true; not supported by advance_mode). valid values: true, false,
                auto_lock_time: Auto-lock time (Optional, minimum 1, default 2),
                auto_lock_time_unit: Auto-lock time unit (Optional, default hour). valid values: minute, hour, day, month, year,
                auto_del: Auto-delete mode (Optional, default false; not supported by advance_mode). valid values: true, false,
                is_worm_audit_log_fs: WORM audit log Filesystem (Optional, default false; only one per tenant),
                worm_append_unit: WORM append file protection granularity (Optional, only supported by advance_mode). valid values: 256KB, 512KB, 1M,
             }
        task_remarks: Async task remark info, 0~1024 characters(Optional)
        audit_log_rules: Audit log rule set(Optional), e.g.: set_security, get_security, set_attr, get_attr, etc., up to 100
        unix_permissions: Filesystem directory permissions(Optional), format like 0755

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
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
# namespace (Namespace) sub-topic related actions
# ============================================================================

def namespace_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 100,
         sort_dir: str = None, sort_key: str = None, name: str = None,
         vstore_name: str = None, vstore_raw_id: str = None, vstore_id: str = None,
         raw_id: str = None, pool_name: str = None, storage_id: str = None,
         enable_encrypt: bool = None, support_provisioning: bool = None,
         gfs_id: str = None, gfs_name: str = None, has_gfs: bool = None) -> dict:
    """
    Batch query Namespace

    Args:
        client: DME API client
        page_no: Page number for query(Optional), 1~10000000
        page_size: Records per page(Optional), 1~1000, default 100
        sort_dir: Sort direction(Optional), valid values: asc (ascending), desc (descending)
        sort_key: Sort parameter(Optional), valid values: namespace_used_rate, file_used_rate
        name: Namespace name(Optional), 1~256 characters, supports fuzzy query
        vstore_name: Namespace tenant name(Optional), 1~256 characters, supports fuzzy query
        vstore_raw_id: Namespace vStore ID assigned by the storage device(Optional), 1~128 characters
        vstore_id: Namespace vStore ID(Optional), 1~128 characters
        raw_id: Namespace ID on the storage device(Optional), 1~256 characters
        pool_name: Storage pool name(Optional), 1~256 characters, supports fuzzy query
        storage_id: Owning storage device ID(Optional), 1~255 characters
        enable_encrypt: Whether encryption is enabled(Optional), true: yes; false: no
        support_provisioning: Whether service provisioning is supported(Optional), true: yes; false: no; sending this field filters out resources from devices that do not support service provisioning, currently DataTurbo series
        gfs_id: Global namespace ID(Optional), 1~64 characters
        gfs_name: Global namespace name(Optional), 1~256 characters
        has_gfs: Whether it includes namespaces belonging to a global namespace(Optional), true: yes; false: no; when has_gfs is false, gfs_id cannot be sent

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, includes:
        - total: Namespace count
        - namespace_list: Namespace list, contains id, raw_id, name, storage_id, vstore_id and other info
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
    Query specified Namespace details

    Args:
        client: DME API client
        namespace_id: Namespace ID (Required, 1~64 characters)

    Returns:
        {
            id: namespace ID (string),
            raw_id: device-side ID (string),
            name: namespace name (string),
            storage_id: storage device ID (string),
            vstore_id: tenant ID (string),
            vstore_name: tenant name (string),
            pool_id: storage pool ID (string),
            pool_name: storage pool name (string),
            running_status: running status. valid values: NORMAL, UNKNOWN,
            space_used_rate: space usage rate (string),
            file_used_rate: file usage rate (string),
            space_used: used space (string),
            file_used: used file count (string),
            trash_enable: Whether recycle bin is enabled (string),
            enable_encrypt: Whether encryption is enabled (string),
        }
        - rdc: Data redundancy copies
        - acl_policy_type: Security mode
        - gfs_id: Global namespace ID
        - qos_policy: QoS policy
        - worm: WORM parameters
        and other detailed info
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
    Batch create Namespace

    Args:
        client: DME API client
        storage_id: Storage device ID (Required)
        pool_raw_id: Storage pool ID on the storage device (Required)
        namespace_specs: Namespace batch parameters. parameter format: [{
                name: name (Required, 1~255 characters, supports digits, letters, underscores, dots, hyphens),
                count: count (Required, 1~500),
                start_suffix: Starting suffix number (Optional, 0~9999; start_suffix + count <= 9999),
                isInGfs: Whether in global namespace (Optional). valid values: true, false,
             }, ...]
        enable_update_atime: Whether to update Atime
        trash_visible: Whether the recycle bin directory is visible, default invisible
        trash_enable: Whether the recycle bin feature is enabled, default disabled
        interval_trash: Recycle bin protection duration (minutes), 0 means permanent retention, max 4294967295
        dps_switch: Metadata search switch, true to enable
        forbidden_dpc: Whether to forbid dpc mounting
        audit_log_switch: Whether to enable audit log, default false
        audit_log_rule: Audit log rule list, valid values: open, create, read, write, close,
                       delete, rename, get_attr, set_attr, get_security, set_security,
                       get_xattr, set_xattr, list_dir, contact, mount_or_unmount, login_or_logoff
        atime_update_mode: Atime update frequency, 4294967295 disable, 3600 1 hour, 86400 1 day
        acl_policy_type: Security mode, valid values: mixed, unix, native, ntfs, default unix
        enable_encrypt: Whether to enable encryption
        crypt_alg: Encryption algorithm type, valid values: XTS_AES_128, XTS_AES_256, XTS_SM4, UNKNOWN
        case_sensitive: Whether case sensitive, default insensitive
        show_snap_dir: Whether the snapshot directory is visible
        rdc: Data redundancy copies, valid values: redundancy_2, redundancy_3, redundancy_4
        worm: WORM configuration (Optional). parameter format: {
                worm_mode: WORM policy mode (Optional). valid values: non_worm (None type), enterprise_mode (enterprise), compliance_mode (compliance),
                min_protect_period: Minimum protection period (Optional, 0~4294967295, default 0; 4294967295 is indefinite),
                min_protect_period_unit: Minimum retention time unit (Optional, default year). valid values: day, year, month, hour, minute,
                max_protect_period: Maximum protection period (Optional, 1~4294967295, default 70; 4294967295 is indefinite),
                max_protect_period_unit: Maximum retention time unit (Optional, default year). valid values: day, year, month, hour, minute, infinite,
                def_protect_period: Default protection period (Optional, 0~4294967295, default 70),
                def_protect_period_unit: Default retention time unit (Optional, default year). valid values: day, year, month, hour, minute, infinite,
                auto_lock_enabled: Whether WORM auto-lock is enabled (Optional, default false). valid values: true, false,
                auto_lock_time: Auto-lock time (Optional, 1~64800, default 2; in days: 1~45, hours: 1~1080, minutes: 1~64800),
                auto_lock_unit: Auto-lock time unit (Optional, default hour). valid values: day, minute, hour,
                legal_hold_modify: Legal hold file modification retention period switch (Optional, default false). valid values: true, false,
             }
        qos_policy: QoS policy configuration. parameter format: {
                qos_scale: Upper limit control dimension (Required). valid values: namespace, client, account, user, innertask,
                name: QoS policy name (Optional, 1~63 characters, regex ^[a-zA-Z0-9][a-zA-Z0-9_-]*, must start with digit or letter),
                qos_mode: QoS mode (Required). valid values: by_usage (by used amount), by_package (by fixed capacity), manual (by upper limit),
                account_raw_id: Account ID on the storage device (Optional, 0~4294967293; required when qos_scale is namespace/account/user),
                package_size: Package capacity GB (Optional, 0~94371840; required when qos_mode is by_package),
                max_iops: IOPS upper limit (Optional, 0~1073741824000; required for batch create Namespace),
                max_mbps: Bandwidth upper limit Mbps (Optional, 0~1073741824; required when qos_mode is manual),
                max_band_width: Max bandwidth Mbps (Optional, 1~1073741824; required when qos_mode is by_usage or by_package),
                basic_band_width: Basic bandwidth Mbps (Optional, 1~1073741824; required when qos_mode is by_usage or by_package),
                bps_density: Bandwidth density Mbps (Optional, 1~1024000; required when qos_mode is by_usage or by_package),
                max_conn_cluster: Max connections (Optional),
                max_lock_cluster: Max lock count (Optional),
                max_open_file_cluster: Max open file count (Optional),
                read_ops: Read OPS limit (Optional, 0~1073741824000; only available when qos_mode is manual and qos_scale is not account),
                write_ops: Write OPS limit (Optional, 0~1073741824000; only available when qos_mode is manual and qos_scale is not account),
                read_mbps: Read bandwidth limit Mbps (Optional, 0~1073741824; only available when qos_mode is manual and qos_scale is not account),
                write_mbps: Write bandwidth limit Mbps (Optional, 0~1073741824; only available when qos_mode is manual and qos_scale is not account),
             }
        public_network_qos_policy: Public network QoS policy configuration. parameter format: {
                        name: QoS policy name(Optional), 1~63 characters, regex ^[a-zA-Z0-9][a-zA-Z0-9_-]*, must start with digit or letter,
                        qos_mode: QoS mode (conditionally required), valid values: by_usage (by used amount), by_package (by fixed capacity), manual (by upper limit); required for batch create Namespace, optional for modify,
                        package_size: Package capacity(Optional), 0~94371840 (GB), required when qos_mode is by_package,
                        max_iops: IOPS upper limit (conditionally required), 0~1073741824000, required for batch create Namespace, optional for modify,
                        max_mbps: Bandwidth upper limit(Optional), 0~1073741824 (Mbps), required when qos_mode is manual,
                        max_band_width: Max bandwidth(Optional), 1~1073741824 (Mbps), required when qos_mode is by_usage or by_package,
                        basic_band_width: Basic bandwidth(Optional), 1~1073741824 (Mbps), required when qos_mode is by_usage or by_package,
                bps_density: Bandwidth density Mbps (Optional, 1~1024000; required when qos_mode is by_usage or by_package),
                max_conn_cluster: Max connections (Optional),
                max_lock_cluster: Max lock count (Optional),
                max_open_file_cluster: Max open file count (Optional),
                read_ops: Read OPS limit (Optional, 0~1073741824000; only available when qos_mode is manual and qos_scale is not account),
                write_ops: Write OPS limit (Optional, 0~1073741824000; only available when qos_mode is manual and qos_scale is not account),
                read_mbps: Read bandwidth limit Mbps (Optional, 0~1073741824; only available when qos_mode is manual and qos_scale is not account),
                write_mbps: Write bandwidth limit Mbps (Optional, 0~1073741824; only available when qos_mode is manual and qos_scale is not account),
             }
        private_network_qos_policy: Private network QoS policy configuration. parameter format: {
                        name: QoS policy name(Optional), 1~63 characters, regex ^[a-zA-Z0-9][a-zA-Z0-9_-]*, must start with digit or letter,
                        qos_mode: QoS mode (conditionally required), valid values: by_usage (by used amount), by_package (by fixed capacity), manual (by upper limit); required for batch create Namespace, optional for modify,
                        package_size: Package capacity(Optional), 0~94371840 (GB), required when qos_mode is by_package,
                        max_iops: IOPS upper limit (conditionally required), 0~1073741824000, required for batch create Namespace, optional for modify,
                        max_mbps: Bandwidth upper limit(Optional), 0~1073741824 (Mbps), required when qos_mode is manual,
                        max_band_width: Max bandwidth(Optional), 1~1073741824 (Mbps), required when qos_mode is by_usage or by_package,
                        basic_band_width: Basic bandwidth(Optional), 1~1073741824 (Mbps), required when qos_mode is by_usage or by_package,
                bps_density: Bandwidth density Mbps (Optional, 1~1024000; required when qos_mode is by_usage or by_package),
                max_conn_cluster: Max connections (Optional),
                max_lock_cluster: Max lock count (Optional),
                max_open_file_cluster: Max open file count (Optional),
                read_ops: Read OPS limit (Optional, 0~1073741824000; only available when qos_mode is manual and qos_scale is not account),
                write_ops: Write OPS limit (Optional, 0~1073741824000; only available when qos_mode is manual and qos_scale is not account),
                read_mbps: Read bandwidth limit Mbps (Optional, 0~1073741824; only available when qos_mode is manual and qos_scale is not account),
                write_mbps: Write bandwidth limit Mbps (Optional, 0~1073741824; only available when qos_mode is manual and qos_scale is not account),
             }
        create_s3_param: Create S3 protocol parameters (Optional). parameter format: {
                bucket_permission: Policy type (Required). valid values: private (private), public_read_only (public read only), public_write_only (public write only), public_read_write (public read and write),
                version_status: Object multi-version status (Optional, 0~2). valid values: 0 (disabled), 1 (enabled), 2 (suspended),
             }
        application_type: Application type, valid values: PACS (medical imaging scenario), GENERAL (general scenario)
        task_remarks: Async task remark info

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        } (async task ID)
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
    Modify specified Namespace

    Args:
        client: DME API client
        namespace_id: Namespace ID (Required, 1~64 characters)
        enable_update_atime: Whether to update Atime, true: update; false: do not update
        show_snap_dir: Whether the snapshot directory is visible, true: visible; false: invisible
        trash_visible: Whether the recycle bin directory is visible, true: visible; false: invisible, default invisible
        trash_enable: Whether the recycle bin feature is enabled, true: enabled; false: disabled, default disabled
        interval_trash: Recycle bin protection duration (minutes), 0 means permanent retention, not auto-deleted, max 4294967295
        dps_switch: Metadata search switch, true: enabled; false: disabled
        forbidden_dpc: Whether to forbid dpc mounting, true: forbid; false: allow
        audit_log_switch: Whether to enable audit log, default false, true: enabled; false: disabled
        audit_log_rule: Audit log rule list, valid values: open, create, read, write, close, delete, rename,
                       get_attr, set_attr, get_security, set_security, get_xattr, set_xattr,
                       list_dir, contact, mount_or_unmount, login_or_logoff
        atime_update_mode: Atime update frequency, 4294967295: disabled; 3600: update every 1 hour; 86400: update every 1 day
        acl_policy_type: Namespace security mode, valid values: mixed (supports both UNIX and Windows permissions),
                        unix (NFS user permissions controlled by Unix Mode/NFSv4 ACL),
                        native (applies to the same scenarios as Mixed mode),
                        ntfs (CIFS user permissions controlled by Windows NT ACL)
        enable_encrypt: Whether to enable encryption, true: enabled; false: disabled
        qos_policy: QoS policy configuration. parameter format: {
                qos_switch: QoS switch (Required). valid values: on, off,
                name: QoS policy name (Optional, 1~63 characters, regex ^[a-zA-Z0-9][a-zA-Z0-9_-]*),
                qos_mode: QoS mode (conditionally required). valid values: by_usage (by used amount), by_package (by fixed capacity), manual (by upper limit),
                package_size: Package capacity GB (Optional, 0~94371840; required when qos_mode is by_package),
                max_iops: IOPS upper limit (conditionally required, 0~1073741824000),
                max_mbps: Bandwidth upper limit Mbps (Optional, 0~1073741824; required when qos_mode is manual),
                max_band_width: Max bandwidth Mbps (Optional, 1~1073741824; required when qos_mode is by_usage or by_package),
                basic_band_width: Basic bandwidth Mbps (Optional, 1~1073741824; required when qos_mode is by_usage or by_package),
                bps_density: Bandwidth density Mbps (Optional, 1~1024000; required when qos_mode is by_usage or by_package),
                max_conn_cluster: Max connections (Optional),
                max_lock_cluster: Max lock count (Optional),
                max_open_file_cluster: Max open file count (Optional),
                read_ops: Read OPS limit (Optional, 0~1073741824000; only available when qos_mode is manual and qos_scale is not account),
                write_ops: Write OPS limit (Optional, 0~1073741824000; only available when qos_mode is manual and qos_scale is not account),
                read_mbps: Read bandwidth limit Mbps (Optional, 0~1073741824; only available when qos_mode is manual and qos_scale is not account),
                write_mbps: Write bandwidth limit Mbps (Optional, 0~1073741824; only available when qos_mode is manual and qos_scale is not account),
             }
        public_network_qos_policy: Public network QoS policy configuration. parameter format: {
                        qos_switch: QoS switch (Required), valid values: on, off,
                        name: QoS policy name(Optional), 1~63 characters, regex ^[a-zA-Z0-9][a-zA-Z0-9_-]*, must start with digit or letter,
                        qos_mode: QoS mode (conditionally required), valid values: by_usage (by used amount), by_package (by fixed capacity), manual (by upper limit); required for batch create Namespace, optional for modify,
                        package_size: Package capacity(Optional), 0~94371840 (GB), required when qos_mode is by_package,
                        max_iops: IOPS upper limit (conditionally required), 0~1073741824000, required for batch create Namespace, optional for modify,
                        max_mbps: Bandwidth upper limit(Optional), 0~1073741824 (Mbps), required when qos_mode is manual,
                        max_band_width: Max bandwidth(Optional), 1~1073741824 (Mbps), required when qos_mode is by_usage or by_package,
                        basic_band_width: Basic bandwidth(Optional), 1~1073741824 (Mbps), required when qos_mode is by_usage or by_package,
                bps_density: Bandwidth density Mbps (Optional, 1~1024000; required when qos_mode is by_usage or by_package),
                max_conn_cluster: Max connections (Optional),
                max_lock_cluster: Max lock count (Optional),
                max_open_file_cluster: Max open file count (Optional),
                read_ops: Read OPS limit (Optional, 0~1073741824000; only available when qos_mode is manual and qos_scale is not account),
                write_ops: Write OPS limit (Optional, 0~1073741824000; only available when qos_mode is manual and qos_scale is not account),
                read_mbps: Read bandwidth limit Mbps (Optional, 0~1073741824; only available when qos_mode is manual and qos_scale is not account),
                write_mbps: Write bandwidth limit Mbps (Optional, 0~1073741824; only available when qos_mode is manual and qos_scale is not account),
             }
        private_network_qos_policy: Private network QoS policy configuration. parameter format: {
                        qos_switch: QoS switch (Required), valid values: on, off,
                        name: QoS policy name(Optional), 1~63 characters, regex ^[a-zA-Z0-9][a-zA-Z0-9_-]*, must start with digit or letter,
                        qos_mode: QoS mode (conditionally required), valid values: by_usage (by used amount), by_package (by fixed capacity), manual (by upper limit); required for batch create Namespace, optional for modify,
                        package_size: Package capacity(Optional), 0~94371840 (GB), required when qos_mode is by_package,
                        max_iops: IOPS upper limit (conditionally required), 0~1073741824000, required for batch create Namespace, optional for modify,
                        max_mbps: Bandwidth upper limit(Optional), 0~1073741824 (Mbps), required when qos_mode is manual,
                        max_band_width: Max bandwidth(Optional), 1~1073741824 (Mbps), required when qos_mode is by_usage or by_package,
                        basic_band_width: Basic bandwidth(Optional), 1~1073741824 (Mbps), required when qos_mode is by_usage or by_package,
                bps_density: Bandwidth density Mbps (Optional, 1~1024000; required when qos_mode is by_usage or by_package),
                max_conn_cluster: Max connections (Optional),
                max_lock_cluster: Max lock count (Optional),
                max_open_file_cluster: Max open file count (Optional),
                read_ops: Read OPS limit (Optional, 0~1073741824000; only available when qos_mode is manual and qos_scale is not account),
                write_ops: Write OPS limit (Optional, 0~1073741824000; only available when qos_mode is manual and qos_scale is not account),
                read_mbps: Read bandwidth limit Mbps (Optional, 0~1073741824; only available when qos_mode is manual and qos_scale is not account),
                write_mbps: Write bandwidth limit Mbps (Optional, 0~1073741824; only available when qos_mode is manual and qos_scale is not account),
             }
        application_type: Application type, valid values: PACS (medical imaging scenario), GENERAL (general scenario)
        task_remarks: Async task remark info

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        } (async task ID)
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
    Batch delete Namespace

    Args:
        client: DME API client
        namespace_ids: Namespace ID list (Required), array max 100, min 1
        task_remarks: Async task remark info (Optional, 0~1024 characters)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        } (async task ID)
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
    Query client access list under NFS share

    Specify a device or NFS ID to query the client access list under the NFS share.

    Args:
        client: DME API client
        page_no: pagination start page(Optional), minimum 1, default 1
        page_size: Records per page(Optional), 1~1000, default 20
        nfs_share_id: NFS share ID(Optional), 1~64 characters
        storage_id: Storage device ID(Optional), 1~64 characters; if nfs_share_id is specified, this parameter is invalid
        vstore_id_in_storage: vStore ID(Optional), 1~256 characters; must be sent in vStore scenarios
        name: Client IP or hostname or network group name(Optional), 1~256 characters; supports fuzzy search when nfs_share_id is specified
        client_id_in_storage: NFS share client ID(Optional), 1~256 characters
        sort_key: Sort field(Optional), valid values: raw_id, name
        sort_dir: Sort direction(Optional), valid values: asc (ascending), desc (descending), default asc

    Returns:
        {
            total: Client count (int32),
            auth_client_list: Client access list (List<AuthClientV2>). parameter format: [{
                client_id_in_storage: Client ID on the device (string),
                nfs_share_id_in_storage: NFS share ID on the device (string),
                name: Client name (string),
                permission: Permission (string),
                accesskrb5: Kerberos authentication (string),
            }, ...],
        }
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
    Batch query DataTurbo administrators

    Only supported by OceanStor A800 series storage.

    Args:
        client: DME API client
        storage_id: Device ID (1~64 characters, Optional)
        vstore_id: Tenant ID (1~64 characters, Optional)
        vstore_name: Tenant name, supports fuzzy query (1~256 characters, Optional)
        zone_id: Zone ID (1~64 characters, Optional). When the resource scope is global, zone ID is the device ID; when local, zone ID is the zone ID. Only supported by OceanStor A800 series storage
        name: DataTurbo administrator name, supports fuzzy query (1~256 characters, Optional)
        online_status: DataTurbo administrator online status (Optional). valid values: offline (offline), online (online)
        lock_status: DataTurbo administrator lock status (Optional). valid values: unlocked (unlocked), locked (locked)
        account_state: DataTurbo administrator password status (Optional). valid values: normal (normal), expired (password expired), initial (user password in initial state, needs modification), expiring_soon (password expiring soon), change_required (password must be changed on next login), never (password never expires)
        sort_key: Sort by specified field (Optional). valid values: create_time
        sort_dir: Sort direction (Optional). valid values: asc (ascending), desc (descending)
        page_no: pagination start page (int32, min: 1, default: 1, Optional)
        page_size: Records per page (int32, min: 1, max: 1000, default: 20, Optional)

    Returns:
        {
            total: Administrator count (integer),
            administrators: Administrator list (List<AdministratorQueryResp>). parameter format: [{
                id: Administrator ID (string),
                name: Administrator name (string),
                type: Administrator type (string),
            }, ...],
        }
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
    Modify UNIX user

    Args:
        client: DME API client
        id: UNIX user ID (1~32 characters, Required)
        raw_id: UNIX user ID on the storage device (int64, 0~4294967294, Optional)
        description: UNIX user description (0~255 characters, Optional)
        primary_group_name: User primary group name (1~64 characters, Optional. If both primary_group_name and primary_group_raw_id are sent, only primary_group_raw_id takes effect)
        primary_group_raw_id: User primary group ID (int64, 0~4294967294, Optional. If both primary_group_name and primary_group_raw_id are sent, only primary_group_raw_id takes effect)
        status_enable: User status (boolean, Optional). valid values: true (enabled), false (locked). Only supported by OceanStor Pacific and OceanStor A310 series storage

    Returns:
        Modify result
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
    Create UNIX user group

    Args:
        client: DME API client
        storage_id: Create UNIX user group storage device ID (1~64 characters, Required)
        name: UNIX user group name (1~64 characters, Required)
        raw_id: UNIX user group ID (int64, 0~4294967294, Optional. Required for OceanStor Pacific and OceanStor A310 storage)
        description: UNIX user group description (0~255 characters, Optional)
        vstore_raw_id: User tenant ID on the storage device (1~32 characters, Required)
        zone_id: Zone ID (1~64 characters, Optional. Only supported by OceanStor A800 storage)

    Returns:
        Create result
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
    Delete UNIX user

    Args:
        client: DME API client
        ids: UNIX user ID list (List<string>, array min members: 1, max array members: 100, Required)

    Returns:
        operation result
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
    Query UNIX authentication user group list

    Args:
        client: DME API client
        page_no: Start page for paginated query (int32, 1~2147483647, default: 1, Optional)
        page_size: Records per page (int32, 10~100, default: 100, Optional)
        storage_name: Device name, supports fuzzy match filtering (1~256 characters, Optional)
        vstore_raw_id: Tenant ID on the storage device (1~64 characters, Optional)
        vstore_name: Tenant name, supports fuzzy search filtering (1~256 characters, Optional)
        name: User group name, supports fuzzy search filtering (1~256 characters, Optional)
        raw_id: User group ID on the storage device (1~256 characters, Optional)
        zone_id: Zone ID (1~64 characters, Optional). Only authentication user groups under OceanStor A800 storage support filtering by this field
        sort_key: Sort by specified field (Optional). valid values: name (user group name), raw_id (user group ID on storage device), create_time (creation time). default: create_time
        storage_id: Storage device ID (1~36 characters, Optional)
        sort_dir: Sort direction (Optional). valid values: asc (ascending), desc (descending). default: desc

    Returns:
        {
            total: User group count (int32),
            groups: UNIX authentication user group list (List<UnixUserGroup>). parameter format: [{
                id: User group ID (string),
                name: User group name (string),
                gid: Group GID (int32),
            }, ...],
        }
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
    Query UNIX user group details

    Args:
        client: DME API client
        id: User group ID (1~32 characters, Required)

    Returns:
        {
            id: User group ID (string),
            name: User group name (string),
            gid: Group GID (int32),
            description: description (string),
        }
    """
    url = "/rest/fileservice/v1/unix-user-groups/{id}"

    response = client.get(url, params={"id": id})
    return response


def account_unix_user_group_modify(client: DMEAPIClient, id: str,
                                    raw_id: int = None,
                                    description: str = None) -> dict:
    """
    Modify UNIX user group

    Args:
        client: DME API client
        id: UNIX user group ID (1~32 characters, Required)
        raw_id: UNIX user group ID on the storage device (int64, 0~4294967294, Optional)
        description: UNIX user group description (0~255 characters, Optional)

    Returns:
        Modify result
    """
    url = "/rest/fileservice/v1/unix-user-groups/{id}"

    payload = {}

    if raw_id is not None:
        payload['raw_id'] = raw_id
    if description is not None:
        payload['description'] = description

    response = client.put(url, body=payload, params={"id": id})
    return response


def account_unix_user_group_batch_delete(client: DMEAPIClient, ids: list) -> dict:
    """
    Delete UNIX user group

    Args:
        client: DME API client
        ids: UNIX user group ID list (List<string>, array min members: 1, max array members: 100, Required)

    Returns:
        operation result
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
    Remove UNIX user secondary group

    Args:
        client: DME API client
        user_id: UNIX user ID (1~32 characters, Required)
        secondary_group_name_list: Secondary group name list (List<string>, array min members: 1, max array members: 100, Required)

    Returns:
        operation result
    """
    url = "/rest/fileservice/v1/unix-users/{user_id}/remove-secondary-group"

    payload = {
        'secondary_group_name_list': secondary_group_name_list,
    }

    response = client.post(url, body=payload, params={"user_id": user_id})
    return response


def account_unix_user_show(client: DMEAPIClient, id: str) -> dict:
    """
    Query UNIX authentication user details

    Args:
        client: DME API client
        id: User ID (1~32 characters, Required)

    Returns:
        {
            id: user ID (string),
            name: user name (string),
            uid: user UID (int32),
            primary_group_name: primary group name (string),
            description: description (string),
        }
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
    Query UNIX authentication user list

    Args:
        client: DME API client
        page_no: Start page for paginated query (int32, 1~2147483647, default: 1, Optional)
        page_size: Records per page (int32, 10~100, default: 100, Optional)
        storage_name: Device name, supports fuzzy search filtering (1~256 characters, Optional)
        vstore_raw_id: Tenant ID on the storage device (1~64 characters, Optional)
        vstore_name: Tenant name, supports fuzzy search filtering (1~256 characters, Optional)
        name: User name, supports fuzzy search filtering (1~256 characters, Optional)
        primary_group_name: Primary group name, supports fuzzy search filtering (1~256 characters, Optional)
        raw_id: User ID on the storage device (1~255 characters, Optional)
        zone_id: Zone ID (1~64 characters, Optional). Only authentication users under OceanStor A800 storage support filtering by this field
        user_status: User status (Optional). valid values: enable (enabled), disable (disabled)
        sort_key: Sort by specified field (Optional). valid values: name (user name), raw_id (user ID on storage device), primary_group_name (primary group name), create_time (creation time). default: create_time
        storage_id: Storage device ID (1~36 characters, Optional)
        sort_dir: Sort direction (Optional). valid values: asc (ascending), desc (descending). default: desc

    Returns:
        {
            total: User count (int32),
            users: UNIX authentication user list (List<UnixUser>). parameter format: [{
                id: user ID (string),
                name: user name (string),
                uid: user UID (int32),
                primary_group_name: primary group name (string),
            }, ...],
        }
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
    Add UNIX user secondary group

    Args:
        client: DME API client
        user_id: UNIX user ID (1~32 characters, Required)
        secondary_group_name_list: Secondary group name list (List<string>, array min members: 1, max array members: 100, Required)

    Returns:
        operation result
    """
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
    """
    Create UNIX user

    Args:
        client: DME API client
        storage_id: Create UNIX user storage device ID (1~64 characters, Required)
        name: UNIX user name (1~64 characters, Required)
        raw_id: UNIX user ID (int64, 0~4294967294, Optional. Required for OceanStor Pacific and OceanStor A310 storage)
        description: UNIX user description (0~255 characters, Optional)
        primary_group_raw_id: User primary group ID (int64, 0~4294967294, Optional. At least one of primary_group_raw_id and primary_group_name must be provided; if both are sent, only primary_group_name takes effect)
        primary_group_name: User primary group name (1~64 characters, Optional. At least one of primary_group_raw_id and primary_group_name must be provided; if both are sent, only primary_group_name takes effect)
        vstore_raw_id: User tenant ID on the storage device (1~32 characters, Required)
        zone_id: Zone ID (1~64 characters, Optional. Only supported by OceanStor A800 storage)
        status: User status (boolean, Optional. default: true). valid values: true (enabled), false (locked). Only supported by OceanStor Pacific and OceanStor A310 series storage
        secondary_group_name_list: User secondary group name list (List<string>, array min members: 0, max array members: 100, Optional)

    Returns:
        Create result
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
    Batch create KV Cache store

    Args:
        client: DME API client
        storage_id: Storage device ID (36 characters, Required)
        zone_id: Zone ID (36 characters, Required)
        pool_raw_id: Storage pool ID on the zone (1~64 characters, Required)
        vstore_id: Tenant ID (32 characters, Required)
        data_cleanup_switch: Cleanup switch (Optional). valid values: on (enabled), off (disabled). default: off
        max_survival_time: KV Cache max survival time (int32, 1~3650, Optional. Required when data_cleanup_switch is on)
        kv_cache_stores: KV Cache store list (List<CreateKVCacheStoreBaseInfo>, array min members: 1, max array members: 100, Required). parameter format: [{
                name: KV Cache store name (1~255 characters, Required),
                capacity: KV Cache store capacity (int64, 20971520~70368744177664, unit: sectors, 1 sector = 512 bytes, Required),
                description: description info (1~255 characters, Optional),
                count: Batch create KV Cache store count (int32, 1~100, default: 1, Optional),
                start_suffix: Starting suffix number (int32, 0~9999, Optional. start_suffix + KV Cache store count <= 9999),
             }, ...]

    Returns:
        Create result
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
    Modify KV Cache store

    Args:
        client: DME API client
        kv_cache_stores_id: KV Cache store ID (1~64 characters, Required)
        name: KV Cache store name (1~255 characters, Optional)
        description: description info (0~255 characters, Optional)
        data_cleanup_switch: Cleanup switch (Optional). valid values: on (enabled), off (disabled). default: off
        max_survival_time: KV Cache max survival time (int32, 1~3650, Optional. Required when data_cleanup_switch is on)

    Returns:
        Modify result
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
    Batch delete KV Cache store

    Args:
        client: DME API client
        ids: KV Cache store ID list (List<string>, array min members: 1, max array members: 100, Required)

    Returns:
        operation result
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
    Query KV Cache store

    Args:
        client: DME API client
        storage_id: Storage device ID (36 characters, Optional)
        id: KV Cache store ID (32 characters, Optional)
        raw_id: KV Cache store ID on the zone (1~256 characters, Optional)
        name: KV Cache store name (1~256 characters, Optional)
        zone_id: Zone ID (36 characters, Optional)
        pool_raw_id: Storage pool ID on the zone (1~64 characters, Optional)
        vstore_id: Tenant ID (32 characters, Optional)
        vstore_name: Tenant name (1~256 characters, Optional)
        fs_id: Filesystem ID (32 characters, Optional)
        fs_name: Filesystem name (1~256 characters, Optional)
        data_cleanup_switch: Cleanup switch (Optional). valid values: on (enabled), off (disabled)
        page_no: Page number (int32, 1~10000, default: 1, Optional)
        page_size: Records per page (int32, 1~100, default: 20, Optional)
        sort_dir: Sort direction (Optional). valid values: asc (ascending), desc (descending). default: asc
        sort_key: Sort parameter (Optional). valid values: capacity (total capacity), used_capacity (used capacity), used_tokens (used token count), hit_ratio (hit ratio)

    Returns:
        {
            total: KV Cache store count (int32),
            kv_cache_stores: KV Cache store list (List<KVCacheStore>). parameter format: [{
                id: Store ID (string),
                name: Store name (string),
                status: status (string),
                capacity: capacity (string),
            }, ...],
        }
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
        'description': 'Batch query DataTurbo administrators',
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
        'description': 'Query UNIX authentication user list',
        'params': ['storage_id', 'storage_name', 'vstore_raw_id', 'vstore_name', 'name', 'primary_group_name', 'raw_id', 'zone_id', 'user_status', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_unix_user_show': {
        'func': account_unix_user_show,
        'description': 'Query UNIX authentication user details',
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
        'description': 'Query UNIX authentication user group list',
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
        'description': 'Query specified Dtree details',
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
        'description': 'Modify specified Dtree',
        'params': ['dtree_id', 'name', 'quota_switch', 'security_mode', 'nas_locking_policy', 'unix_permissions', 'task_remarks'],
        'subtopic': 'dtree'
    },
    # NFS share subtopic action
    'nfs_share_list': {
        'func': nfs_share_list,
        'description': 'Query NFS share list',
        'params': ['id_in_storage', 'name', 'share_path', 'exact_share_path', 'device_name', 'storage_id', 'tier_name', 'owning_dtree_name', 'fs_name', 'fs_id', 'owning_dtree_id', 'vstore_name', 'page_no', 'page_size', 'sort_key', 'sort_dir', 'support_provisioning', 'namespace_id', 'namespace_name', 'dc_id', 'dc_name', 'zone_id', 'zone_name', 'zone_ip'],
        'subtopic': 'nfs_share'
    },
    'nfs_share_show': {
        'func': nfs_share_show,
        'description': 'Query specified NFS share details',
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
        'description': 'Modify specified NFS share',
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
        'description': 'Query client access list under NFS share',
        'params': ['page_no', 'page_size', 'nfs_share_id', 'storage_id', 'vstore_id_in_storage', 'name', 'client_id_in_storage', 'sort_key', 'sort_dir'],
        'subtopic': 'nfs_share'
    },
    # CIFS share subtopic action
    'cifs_share_list': {
        'func': cifs_share_list,
        'description': 'Batch query CIFS shares',
        'params': ['raw_id', 'name', 'share_path', 'exact_share_path', 'fs_id', 'fs_name', 'dtree_id', 'dtree_name', 'storage_id', 'storage_name', 'vstore_raw_id', 'vstore_name', 'manufacturer', 'op_lock_enabled', 'notify_enabled', 'offline_file_modes', 'file_extension_filter_enabled', 'abe_enabled', 'page_no', 'page_size', 'sort_key', 'sort_dir', 'namespace_id', 'namespace_name', 'support_provisioning', 'dc_id', 'dc_name'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_show': {
        'func': cifs_share_show,
        'description': 'Query specified CIFS share details',
        'params': ['cifs_share_id'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_create': {
        'func': cifs_share_create,
        'description': 'Create a single CIFS share',
        'params': ['create_cifs_param', 'fs_id', 'namespace_id', 'task_remarks'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_modify': {
        'func': cifs_share_modify,
        'description': 'Modify specified CIFS share',
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
        'description': 'Query permissions list of a single CIFS share (user/IP/file filter)',
        'params': ['cifs_share_id', 'type', 'user_filter', 'ip_filter', 'file_filter', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'cifs_share'
    },
    # dataturbo_share subtopic action
    'dataturbo_share_list': {
        'func': dataturbo_share_list,
        'description': 'Query DataTurbo share list',
        'params': ['page_no', 'page_size', 'raw_id', 'share_path', 'fs_id', 'fs_name', 'dtree_id', 'dtree_name', 'vstore_id', 'vstore_raw_id', 'vstore_name', 'storage_id', 'storage_name', 'zone_id', 'zone_name', 'scope', 'sort_key', 'sort_dir'],
        'subtopic': 'dataturbo_share'
    },
    'dataturbo_share_show': {
        'func': dataturbo_share_show,
        'description': 'Query specified DataTurbo share details',
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
        'description': 'Modify specified DataTurbo share',
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
        'description': 'Query DataTurbo share administrator permission list',
        'params': ['dataturbo_share_id', 'page_no', 'page_size', 'user_id', 'user_name', 'permission'],
        'subtopic': 'dataturbo_share'
    },
    # quota subtopic action
    'quota_list': {
        'func': quota_list,
        'description': 'Query quota list',
        'params': ['page_no', 'page_size', 'ids', 'raw_ids', 'quota_type', 'parent_type', 'parent_raw_id', 'owner_name', 'vstore_id', 'vstore_raw_id', 'storage_id', 'sort_key', 'sort_dir', 'zone_id'],
        'subtopic': 'quota'
    },
    'quota_show': {
        'func': quota_show,
        'description': 'Query specified quota details',
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
        'description': 'Update specified quota',
        'params': ['quota_id', 'space_soft_quota', 'space_hard_quota', 'space_advisory_quota', 'file_soft_quota', 'file_hard_quota', 'file_advisory_quota', 'snap_space_switch', 'soft_grace_time', 'task_remarks'],
        'subtopic': 'quota'
    },
    'quota_delete': {
        'func': quota_delete,
        'description': 'Batch delete quotas',
        'params': ['quota_ids', 'task_remarks'],
        'subtopic': 'quota'
    },
    # filesystem subtopic action
    'filesystem_list': {
        'func': filesystem_list,
        'description': 'Batch query filesystems',
        'params': ['page_no', 'page_size', 'sort_dir', 'sort_key', 'name', 'fs_raw_id', 'storage_id'],
        'subtopic': 'filesystem'
    },
    'filesystem_show': {
        'func': filesystem_show,
        'description': 'Query specified filesystem details',
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
        'description': 'Batch modify filesystems (supports batch renaming)',
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
        'description': 'Query available filesystems (supports remote replication)',
        'params': ['feature_type', 'local_storage_id', 'remote_storage_id', 'name', 'page_no', 'page_size', 'sort_key', 'sort_dir'],
        'subtopic': 'filesystem'
    },
    'filesystem_modify': {
        'func': filesystem_modify,
        'description': 'Modify specified filesystem (full parameters)',
        'params': ['file_system_id', 'name', 'description', 'capacity', 'capacity_threshold', 'initial_distribute_policy', 'automatic_update_time', 'atime_update_mode', 'quota_switch', 'vaai_switch', 'owning_controller', 'task_remarks'],
        'subtopic': 'filesystem'
    },
    # namespace subtopic action
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
        'description': 'Query specified namespace details',
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
        'description': 'Modify specified namespace',
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
    # dataturbo subtopic action (formerly dpc sub-topic, renamed)
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
    # dpc subtopic action (DPC client)
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
    # kvcache subtopic action
    'kvcache_list': {
        'func': kvcache_list,
        'description': 'Query KV Cache store',
        'params': ['storage_id', 'id', 'raw_id', 'name', 'zone_id', 'pool_raw_id', 'vstore_id', 'vstore_name', 'fs_id', 'fs_name', 'data_cleanup_switch', 'page_no', 'page_size', 'sort_dir', 'sort_key'],
        'subtopic': 'kvcache'
    },
    'kvcache_batch_create': {
        'func': kvcache_batch_create,
        'description': 'Batch create KV Cache store',
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
        'description': 'Batch delete KV Cache store',
        'params': ['ids'],
        'subtopic': 'kvcache'
    },
}
