"""
Protection related operations
"""

import sys
import os

from pydme.client import DMEAPIClient


# ============================================================================
# group subtopic - Protection group related operations
# ============================================================================

def group_list(client: DMEAPIClient, name: str = None, project_id: str = None,
               storage_name: str = None, storage_id: str = None,
               raw_id: str = None, lun_group_raw_id: str = None,
               vstore_id: str = None, vstore_raw_id: str = None,
               sort_key: str = None, sort_dir: str = None,
               page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch query protection groups

    Args:
        client: DME API client
        name: protection group name, supports fuzzy search
        project_id: business group ID, supports conditional filtering
        storage_name: storage device name, supports fuzzy search
        storage_id: Storage device ID, supports conditional filtering
        raw_id: protection group ID on the device, supports exact search, supports sorting
        lun_group_raw_id: LUN group ID on the device, supports conditional filtering
        vstore_id: tenant ID, mutually exclusive with vstore_raw_id
        vstore_raw_id: tenant ID on the device, mutually exclusive with vstore_id
        sort_key: sort field, valid values: sort_id
        sort_dir: sort direction, valid values: asc, desc (default desc)
        page_no: pagination page number, default 1
        page_size: items per page, default 20

    Returns:
        {
            total: total protection groups (int32),
            groups: protection group list (List<ProtectionGroupResponse>). parameter format: [{
                id: unique protection group ID (string, 1~64 characters),
                name: protection group name (string, 1~256 characters),
                description: protection group description (string, 0~255 characters),
                raw_id: protection group ID on the device (string, 1~64 characters),
                storage_id: storage device ID (string, 1~64 characters),
                storage_sn: storage device SN (string, 1~64 characters),
                storage_name: storage device name (string, 1~255 characters),
                storage_ip: storage device IP (string, 1~64 characters),
                local_copy_count: local copy count (int32),
                remote_copy_count: remote copy count (int32),
                cloud_copy_count: cloud backup copy count (int32),
                snapshot_consistency_group_count: snapshot consistency group count (int32),
                clone_consistency_group_count: clone consistency group count (int32),
                cdp_consistency_group_count: HyperCDP consistency group count (int32),
                dring_consistency_group_count: ring 3DC consistency group count (int32),
                metro_consistency_group_count: hypermetro consistency group count (int32),
                rep_consistency_group_count: remote replication consistency group count (int32),
                project_id: business group ID (string),
                lun_group_raw_id: LUN group ID on the device (int32, -1~16383),
                lun_group_name: LUN group name (string, 1~255 characters),
                vstore_id: tenant ID (string),
                vstore_raw_id: tenant ID on the device (string),
                vstore_name: tenant name (string),
            }, ...],
        }
    """
    url = "/rest/protection/v1/protection-groups/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if name is not None:
        payload['name'] = name
    if project_id is not None:
        payload['project_id'] = project_id
    if storage_name is not None:
        payload['storage_name'] = storage_name
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if lun_group_raw_id is not None:
        payload['lun_group_raw_id'] = lun_group_raw_id
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def group_create(client: DMEAPIClient, name: str, storage_id: str,
                 lun_ids: list = None, lun_group_id: str = None,
                 description: str = None) -> dict:
    """
    create protection group, supports creation based on LUN or LUN group

    Args:
        client: DME API client
        name: protection group name
        storage_id: Storage device ID
        lun_ids: LUN ID list, conditionally required, required when creating protection group based on LUN
        lun_group_id: LUN group ID, conditionally required, required when creating protection group based on LUN group
        description: protection group description

    Returns:
        {
            id: protection group ID (string),
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/protection-groups"

    payload = {
        'name': name,
        'storage_id': storage_id
    }

    if description is not None:
        payload['description'] = description
    if lun_ids is not None:
        payload['lun_ids'] = lun_ids
    if lun_group_id is not None:
        payload['lun_group_id'] = lun_group_id

    response = client.post(url, body=payload)
    return response


def group_modify(client: DMEAPIClient, pg_id: str, name: str = None,
                 description: str = None) -> dict:
    """
    modify protection group

    Args:
        client: DME API client
        pg_id: protection group ID
        name: protection group name
        description: protection group description

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/protection-groups/{pg_id}"

    payload = {}

    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description

    response = client.put(url, body=payload, params={"pg_id": pg_id})
    return response


def group_delete(client: DMEAPIClient, pg_ids: list) -> dict:
    """
    Batch delete protection groups

    >![](public_sys-resources/icon-notice.gif) **Notice: **
    >This API may directly or indirectly affect running services, cause service interruption, key data loss, etc., please operate with caution. 

    Args:
        client: DME API client
        pg_ids: protection group ID list

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/protection-groups/delete"

    payload = {
        'pg_ids': pg_ids
    }

    response = client.post(url, body=payload)
    return response


def group_add_luns(client: DMEAPIClient, pg_id: str, lun_ids: list = None,
                   hyper_metro: dict = None, rem_reps: list = None) -> dict:
    """
    Add member LUNs to protection group

    Add member LUNs to the specified protection group. 

    Args:
        client: DME API client
        pg_id: protection group ID
        lun_ids: ID list of LUNs to be added to the protection group (Optional), max array members 100, mutually exclusive with lun_pairs in hyper_metro and rem_reps; valid when the protection group does not have hypermetro, replication, or ring 3DC features
        hyper_metro: request parameters for adding LUNs to a protection group with hypermetro feature (Optional), mutually exclusive with lun_ids; valid when the protection group has hypermetro feature. parameter format: {
                        is_delay: whether to delay execution (Required), true: yes; false: no; when delayed execution is true: if the consistency group or new Pair is in "synchronizing" status, wait for synchronization to complete before adding the new Pair to the consistency group; when delayed execution is false: if the consistency group or new Pair is in "synchronizing" status, directly pause the consistency group and new Pair, add the new Pair to the consistency group, then synchronize the consistency group
                        create_mode: hypermetro Pair creation mode (Required), valid values: auto (automatic), manual (manual)
                        remote_storage_pool_id: remote storage pool ID (Optional), 1~32 characters, regex ^[a-fA-F0-9]+$; valid when hypermetro Pair creation mode is auto
                        remote_lun_name_rule: LUN naming strategy (Optional), valid values: same_as_local (same as local resource name), prefix_and_suffix (prefix + local resource name + suffix), prefix_and_num (prefix + auto sequence); valid in auto creation mode
                        name_prefix: remote LUN name prefix (Optional), 0~251 characters; valid in auto creation mode with name rule prefix_and_suffix or prefix_and_num; prefix_and_suffix prefix max 32 bytes, prefix_and_num prefix max 251 bytes
                        name_suffix: remote LUN name suffix (Optional), 0~16 characters; valid in auto creation mode with name rule prefix_and_suffix
                        lun_pairs: manually configured hypermetro Pair info list (Optional), max array members 100; valid when create_mode is manual. parameter format: [{
                                local_lun_id: local LUN ID (Required), 1~32 characters, regex ^[a-fA-F0-9]+$; the device side where the operation is issued is defined as local, and its peer device is defined as remote
                                remote_lun_id: remote LUN ID (Required), 1~32 characters, regex ^[a-fA-F0-9]+$
                        },...]
        }
        rem_reps: request parameters for adding LUNs to a protection group with replication feature (Optional), max array members 2, mutually exclusive with lun_ids; valid when the protection group has replication feature. parameter format: [{
                        is_delay: whether to delay execution (Optional), default true; true: yes; false: no; when delayed execution is true: if the new Pair is in "synchronizing" status, wait for synchronization to complete before adding the new Pair to the consistency group; when delayed execution is false: directly split the consistency group and new Pair, add the new Pair to the consistency group, then synchronize the consistency group
                        create_mode: remote replication Pair creation mode (Required), valid values: auto (automatic), manual (manual)
                        remote_storage_id: remote storage device ID (Required), 1~64 characters, regex ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$
                        remote_storage_pool_id: remote storage pool ID (Optional), 1~32 characters, regex ^[a-fA-F0-9]+$; valid when replication Pair creation mode is auto
                        remote_lun_name_rule: LUN naming strategy (Optional), valid values: same_as_local (same as local resource name), prefix_and_suffix (prefix + local resource name + suffix), prefix_and_num (prefix + auto sequence); valid in auto creation mode
                        name_prefix: remote LUN name prefix (Optional), 0~251 characters; valid in auto creation mode with name rule prefix_and_suffix or prefix_and_num; prefix_and_suffix prefix max 32 bytes, prefix_and_num prefix max 251 bytes
                        name_suffix: remote LUN name suffix (Optional), 0~16 characters; valid in auto creation mode with name rule prefix_and_suffix
                        lun_pairs: manually configured remote replication Pair info list (Optional), max array members 100; valid when create_mode is manual. parameter format: [{
                                local_lun_id: local LUN ID (Required), 1~32 characters, regex ^[a-fA-F0-9]+$; the device side where the operation is issued is defined as local, and its peer device is defined as remote
                                remote_lun_id: remote LUN ID (Required), 1~32 characters, regex ^[a-fA-F0-9]+$
                        },...]
        },...]

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/protection-groups/{pg_id}/add-luns"

    payload = {}

    if lun_ids is not None:
        payload['lun_ids'] = lun_ids
    if hyper_metro is not None:
        payload['hyper_metro'] = hyper_metro
    if rem_reps is not None:
        payload['rem_reps'] = rem_reps

    response = client.post(url, body=payload, params={"pg_id": pg_id})
    return response


def group_remove_luns(client: DMEAPIClient, pg_id: str, lun_ids: list,
                      is_delay: bool = None) -> dict:
    """
    Remove member LUNs from protection group

    Remove member LUNs from the specified protection group. 

    Args:
        client: DME API client
        pg_id: protection group ID
        lun_ids: ID list of protection group member LUNs to be removed
        is_delay: whether to delay execution. This parameter is invalid in remote replication, synchronous + asynchronous ring 3DC scenarios

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/protection-groups/{pg_id}/remove-luns"

    payload = {
        'lun_ids': lun_ids
    }

    if is_delay is not None:
        payload['is_delay'] = is_delay

    response = client.post(url, body=payload, params={"pg_id": pg_id})
    return response


# ============================================================================
# hypermetro_group subtopic - HyperMetro consistency group related operations
# ============================================================================

def hypermetro_group_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 20,
                          name: str = None, raw_id: str = None,
                          protect_group_id: str = None, storage_id: str = None,
                          storage_name: str = None, local_vstore_id: str = None,
                          local_vstore_raw_id: str = None, remote_vstore_id: str = None,
                          remote_vstore_raw_id: str = None) -> dict:
    """
    Batch query hypermetro consistency groups

    Args:
        client: DME API client
        page_no: pagination page number, default 1
        page_size: items per page, default 20
        name: hypermetro consistency group name, supports fuzzy match
        raw_id: hypermetro consistency group ID on the device
        protect_group_id: protection group ID
        storage_id: Storage device ID, supports local storage ID filtering
        storage_name: storage device name, supports local storage name fuzzy match
        local_vstore_id: local tenant ID, mutually exclusive with local_vstore_raw_id
        local_vstore_raw_id: local tenant ID on the device, mutually exclusive with local_vstore_id
        remote_vstore_id: remote tenant ID, mutually exclusive with remote_vstore_raw_id
        remote_vstore_raw_id: remote tenant ID on the device, mutually exclusive with remote_vstore_id

    Returns:
        {
            total: total hypermetro consistency groups (int32),
            groups: hypermetro consistency group list (List<HyperMetroGroupResponse>). parameter format: [{
                id: unique hypermetro consistency group ID (string, 1~64 characters),
                raw_id: ID on the device (string, 1~64 characters),
                name: name (string, 1~255 characters),
                local_storage_id: local storage device ID (string, 1~64 characters),
                local_storage_name: local storage device name (string, 1~256 characters),
                local_vstore_id: local tenant ID (string),
                local_vstore_raw_id: local tenant ID on the device (string),
                local_vstore_name: local tenant name (string),
                remote_storage_id: remote storage device ID (string, 0~64 characters),
                remote_storage_name: remote storage device name (string, 0~256 characters),
                remote_vstore_id: remote tenant ID (string),
                remote_vstore_raw_id: remote tenant ID on the device (string),
                remote_vstore_name: remote tenant name (string),
                domain_name: hypermetro domain name (string, 0~64 characters),
                domain_raw_id: hypermetro domain ID on the device (string, 0~64 characters),
                health_status: health status. valid values: unknown, normal, fault,
                running_status: running status. valid values: normal, synchronizing, invalid, paused, forcibly_started, to_be_synchronized, error, unknown,
                recovery_policy: recovery policy. valid values: automatic, manual,
                priority_station_type: priority station type. valid values: preferred, non_preferred,
                speed: sync speed. valid values: low, medium, high, highest, custom,
                bandwidth: custom sync speed (int32, 1~1024 MB/s),
                sync_direction: data sync direction. valid values: no_data_synchronization, local_to_remote, remote_to_local,
                activation_state: activation state. valid values: active, passive,
                local_protect_group_name: local protection group name (string, 0~255 characters),
                remote_protect_group_name: remote protection group name (string, 0~255 characters),
                isolation_enabled: isolation switch. valid values: true (on), false,
                isolation_threshold_time: isolation threshold (int32, 10~30000ms),
            }, ...],
        }
    """
    url = "/rest/protection/v1/metro/groups/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if name is not None:
        payload['name'] = name
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if protect_group_id is not None:
        payload['protect_group_id'] = protect_group_id
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if storage_name is not None:
        payload['storage_name'] = storage_name
    if local_vstore_id is not None:
        payload['local_vstore_id'] = local_vstore_id
    if local_vstore_raw_id is not None:
        payload['local_vstore_raw_id'] = local_vstore_raw_id
    if remote_vstore_id is not None:
        payload['remote_vstore_id'] = remote_vstore_id
    if remote_vstore_raw_id is not None:
        payload['remote_vstore_raw_id'] = remote_vstore_raw_id

    response = client.post(url, body=payload)
    return response


def hypermetro_group_create(client: DMEAPIClient, domain_id: str, name: str,
                            local_storage_id: str = None, local_pg_id: str = None,
                            description: str = None, create_mode: str = None,
                            remote_vstore_id: str = None, remote_storage_pool_id: str = None,
                            lun_ids: list = None, remote_resource_name_rule: str = None) -> dict:
    """
    create hypermetro consistency group

    Args:
        client: DME API client
        domain_id: hypermetro domain ID
        name: hypermetro consistency group name
        local_storage_id: local device ID
        local_pg_id: local protection group ID, conditionally required: required when device type is OceanStor Dorado V6, OceanStor V6
        description: description info
        create_mode: hypermetro Pair creation mode, valid values: auto, manual
        remote_vstore_id: remote device tenant ID, conditionally required: when create_mode is auto and device is OceanStor Dorado 6.1.3 or above
        remote_storage_pool_id: remote storage pool ID, conditionally required: when create_mode is auto
        lun_ids: LUN ID list, conditionally optional: when create_mode is auto
        remote_resource_name_rule: remote resource naming strategy, valid values: same_as_local, prefix_and_suffix, prefix_and_num

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/groups"

    payload = {
        'domain_id': domain_id,
        'name': name
    }

    if local_storage_id is not None:
        payload['local_storage_id'] = local_storage_id
    if local_pg_id is not None:
        payload['local_pg_id'] = local_pg_id
    if description is not None:
        payload['description'] = description
    if create_mode is not None:
        payload['create_mode'] = create_mode
    if remote_vstore_id is not None:
        payload['remote_vstore_id'] = remote_vstore_id
    if remote_storage_pool_id is not None:
        payload['remote_storage_pool_id'] = remote_storage_pool_id
    if lun_ids is not None:
        payload['lun_ids'] = lun_ids
    if remote_resource_name_rule is not None:
        payload['remote_resource_name_rule'] = remote_resource_name_rule

    response = client.post(url, body=payload)
    return response


def hypermetro_group_modify(client: DMEAPIClient, group_id: str, name: str = None,
                             description: str = None, recovery_policy: str = None,
                             service_assurance_policy: str = None, speed: str = None,
                             bandwidth: int = None, isolation_threshold_time: int = None) -> dict:
    """
    modify hypermetro consistency group

    Args:
        client: DME API client
        group_id: hypermetro consistency group ID
        name: hypermetro consistency group name
        description: description info
        recovery_policy: hypermetro Pair recovery policy, valid values: automatic, manual
        service_assurance_policy: service assurance policy, valid values: data_reliability_preferred, service_continuity_preferred
        speed: sync speed, valid values: low, medium, high, highest, custom
        bandwidth: custom sync speed (MB/s), required when speed is custom
        isolation_threshold_time: isolation threshold (milliseconds), required when service_assurance_policy is service_continuity_preferred

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/groups/{group_id}"

    payload = {}

    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description
    if recovery_policy is not None:
        payload['recovery_policy'] = recovery_policy
    if service_assurance_policy is not None:
        payload['service_assurance_policy'] = service_assurance_policy
    if speed is not None:
        payload['speed'] = speed
    if bandwidth is not None:
        payload['bandwidth'] = bandwidth
    if isolation_threshold_time is not None:
        payload['isolation_threshold_time'] = isolation_threshold_time

    response = client.put(url, body=payload, params={"group_id": group_id})
    return response


def hypermetro_group_delete(client: DMEAPIClient, ids: list, delete_mode: str,
                             is_self_adapt: bool = None) -> dict:
    """
    Batch delete hypermetro consistency groups

    Args:
        client: DME API client
        ids: hypermetro consistency group ID list
        delete_mode: delete mode, valid values: preferred_only, non_preferred_only, dual_ends
        is_self_adapt: whether to support adaptive deletion of member Pairs, default false

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/groups/delete"

    payload = {
        'ids': ids,
        'delete_mode': delete_mode
    }

    if is_self_adapt is not None:
        payload['is_self_adapt'] = is_self_adapt

    response = client.post(url, body=payload)
    return response


def hypermetro_group_add_pairs(client: DMEAPIClient, group_id: str, pair_ids: list,
                                is_self_adapt: bool = None) -> dict:
    """
    Add member Pairs to hypermetro consistency group

    Args:
        client: DME API client
        group_id: hypermetro consistency group ID
        pair_ids: hypermetro Pair ID list
        is_self_adapt: whether to adaptively modify hypermetro Pair running status

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/groups/{group_id}/add-pairs"

    payload = {
        'pair_ids': pair_ids
    }

    if is_self_adapt is not None:
        payload['is_self_adapt'] = is_self_adapt

    response = client.post(url, body=payload, params={"group_id": group_id})
    return response


def hypermetro_group_remove_pairs(client: DMEAPIClient, group_id: str, pair_ids: list) -> dict:
    """
    Remove member Pairs from hypermetro consistency group (async task interface)

    Args:
        client: DME API client
        group_id: hypermetro consistency group ID
        pair_ids: hypermetro Pair ID list

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/groups/{group_id}/remove-pairs"

    payload = {
        'pair_ids': pair_ids
    }

    response = client.post(url, body=payload, params={"group_id": group_id})
    return response


def hypermetro_group_pause(client: DMEAPIClient, ids: list, priority_station_type: str) -> dict:
    """
    Pause hypermetro consistency group

    Args:
        client: DME API client
        ids: hypermetro consistency group ID list
        priority_station_type: station type, valid values: preferred, non_preferred

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/groups/pause"

    payload = {
        'ids': ids,
        'priority_station_type': priority_station_type
    }

    response = client.post(url, body=payload)
    return response


def hypermetro_group_force_startup(client: DMEAPIClient, ids: list, priority_station_type: str) -> dict:
    """
    Force start hypermetro consistency group

    Args:
        client: DME API client
        ids: hypermetro consistency group ID list
        priority_station_type: station type, valid values: preferred, non_preferred

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/groups/force-startup"

    payload = {
        'ids': ids,
        'priority_station_type': priority_station_type
    }

    response = client.post(url, body=payload)
    return response


def hypermetro_group_switch_priority(client: DMEAPIClient, ids: list) -> dict:
    """
    Switch priority site for hypermetro consistency group

    Args:
        client: DME API client
        ids: hypermetro consistency group ID list

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/groups/switch-priority-site"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def hypermetro_group_sync(client: DMEAPIClient, ids: list) -> dict:
    """
    Sync hypermetro consistency group

    Args:
        client: DME API client
        ids: hypermetro consistency group ID list (Required, List<string>, min array members: 1, max array members: 100)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/groups/sync"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


# ============================================================================
# hypermetro_pair subtopic - HyperMetro Pair related operations
# ============================================================================

def hypermetro_pair_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 20,
                         group_id: str = None, group_name: str = None,
                         group_raw_id: str = None, pair_raw_id: str = None,
                         local_storage_id: str = None, local_storage_name: str = None,
                         local_vstore_id: str = None, local_vstore_raw_id: str = None,
                         local_volume_name: str = None, local_host_access_state: str = None,
                         remote_vstore_id: str = None, remote_vstore_raw_id: str = None,
                         remote_volume_name: str = None) -> dict:
    """
    Batch query LUN hypermetro Pairs

    Args:
        client: DME API client
        page_no: pagination page number, default 1
        page_size: items per page, default 20
        group_id: hypermetro consistency group ID
        group_name: hypermetro consistency group name, supports fuzzy match
        group_raw_id: hypermetro consistency group ID on the storage device
        pair_raw_id: hypermetro Pair ID on the storage device
        local_storage_id: local storage device ID
        local_storage_name: local storage device name, supports fuzzy match
        local_vstore_id: local tenant ID, mutually exclusive with local_vstore_raw_id
        local_vstore_raw_id: local tenant ID on the device, mutually exclusive with local_vstore_id
        local_volume_name: local LUN name, supports fuzzy match
        local_host_access_state: local resource host access state, valid values: access_forbidden, read_only, read_write
        remote_vstore_id: remote tenant ID, mutually exclusive with remote_vstore_raw_id
        remote_vstore_raw_id: remote tenant ID on the device, mutually exclusive with remote_vstore_id
        remote_volume_name: remote LUN name, supports fuzzy match

    Returns:
        {
            total: total hypermetro Pairs (int32),
            pairs: hypermetro Pair list (List<HyperMetroPairResponse>). parameter format: [{
                id: hypermetro Pair unique ID (string, 1~64 characters),
                raw_id: ID on the storage device (string, 1~64 characters),
                local_storage_id: local storage device ID (string, 1~64 characters),
                local_storage_name: local device name (string, 1~255 characters),
                local_volume_raw_id: local volume ID on the device (string, 1~64 characters),
                local_volume_name: local volume name (string, 1~255 characters),
                local_vstore_raw_id: local tenant ID on the device (string),
                local_vstore_name: local tenant name (string),
                remote_storage_id: remote storage device ID (string, 1~64 characters),
                remote_storage_name: remote storage device name (string, 1~255 characters),
                remote_volume_raw_id: remote volume ID on the device (string, 1~64 characters),
                remote_volume_name: remote volume name (string, 1~255 characters),
                remote_vstore_raw_id: remote tenant ID on the device (string),
                remote_vstore_name: remote tenant name (string),
                domain_name: hypermetro domain name (string, 0~64 characters),
                domain_raw_id: hypermetro domain ID on the device (string, 0~64 characters),
                health_status: health status. valid values: unknown, normal, fault,
                running_status: running status. valid values: normal, synchronizing, invalid, paused, forcibly_started, to_be_synchronized, error, unknown,
                local_host_access_state: local host access state. valid values: access_forbidden, read_only, read_write,
                remote_host_access_state: remote host access state. valid values: access_forbidden, read_only, read_write,
                recovery_policy: recovery policy. valid values: automatic, manual,
                priority_station_type: priority station type. valid values: preferred, non_preferred,
                speed: sync speed. valid values: low, medium, high, highest, custom,
                bandwidth: custom sync speed (int32, MB/s),
                sync_direction: data sync direction. valid values: no_data_synchronization, local_to_remote, remote_to_local,
                activation_state: activation state. valid values: active, passive,
                group_id: hypermetro consistency group ID (string, 0~64 characters),
                group_raw_id: hypermetro consistency group ID on the device (string, 0~64 characters),
                group_name: hypermetro consistency group name (string, 0~255 characters),
                local_protect_group_name: local protection group name (string, 0~255 characters),
                remote_protect_group_name: remote protection group name (string, 0~255 characters),
                sync_progress: sync progress (string),
                sync_left_time: remaining sync time (string),
            }, ...],
        }
    """
    url = "/rest/protection/v1/metro/lun-pairs/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if group_id is not None:
        payload['group_id'] = group_id
    if group_name is not None:
        payload['group_name'] = group_name
    if group_raw_id is not None:
        payload['group_raw_id'] = group_raw_id
    if pair_raw_id is not None:
        payload['pair_raw_id'] = pair_raw_id
    if local_storage_id is not None:
        payload['local_storage_id'] = local_storage_id
    if local_storage_name is not None:
        payload['local_storage_name'] = local_storage_name
    if local_vstore_id is not None:
        payload['local_vstore_id'] = local_vstore_id
    if local_vstore_raw_id is not None:
        payload['local_vstore_raw_id'] = local_vstore_raw_id
    if local_volume_name is not None:
        payload['local_volume_name'] = local_volume_name
    if local_host_access_state is not None:
        payload['local_host_access_state'] = local_host_access_state
    if remote_vstore_id is not None:
        payload['remote_vstore_id'] = remote_vstore_id
    if remote_vstore_raw_id is not None:
        payload['remote_vstore_raw_id'] = remote_vstore_raw_id
    if remote_volume_name is not None:
        payload['remote_volume_name'] = remote_volume_name

    response = client.post(url, body=payload)
    return response


def hypermetro_pair_create(client: DMEAPIClient, create_mode: str,
                           local_storage_id: str, domain_id: str,
                           lun_ids: list = None, lun_pairs: list = None,
                           remote_storage_pool_id: str = None,
                           remote_vstore_id: str = None,
                           remote_resource_name_rule: str = None,
                           name_prefix: str = None, name_suffix: str = None,
                           speed: str = None, bandwidth: int = None,
                           service_assurance_policy: str = None,
                           isolation_threshold_time: int = None,
                           recovery_policy: str = None) -> dict:
    """
    create hypermetro Pair

    Args:
        client: DME API client
        create_mode: hypermetro Pair creation mode (Required). valid values: auto, manual
        lun_pairs: manually configured hypermetro Pair info list (Optional, List<LunPairInstance>, max array members: 100). parameter format: [{
                local_lun_id: local LUN ID (Required, 1~32 characters, regex ^[a-fA-F0-9]+$),
                remote_lun_id: remote LUN ID (Required, 1~32 characters, regex ^[a-fA-F0-9]+$),
            }, ...]
        lun_ids: LUN ID list (Optional, List<string>, max array members: 100). valid when create_mode is auto
        remote_storage_pool_id: remote storage pool ID (Optional, 1~32 characters, regex ^[a-fA-F0-9]+$). valid when create_mode is auto
        remote_vstore_id: remote device tenant ID (Optional, 1~64 characters). conditionally required: when create_mode is auto and device is OceanStor Dorado 6.1.3 or above
        remote_resource_name_rule: remote resource naming strategy (Optional). valid values: same_as_local, prefix_and_suffix, prefix_and_num. valid in auto creation mode
        name_prefix: remote resource name prefix (Optional, 0~251 characters). valid in auto creation mode with name rule prefix_and_suffix or prefix_and_num
        name_suffix: remote resource name suffix (Optional, 0~16 characters). valid in auto creation mode with name rule prefix_and_suffix
        local_storage_id: local storage device ID (Optional, 1~64 characters). conditionally required: when create_mode is manual
        domain_id: hypermetro domain ID (Optional, 1~64 characters). conditionally required: when create_mode is manual
        speed: sync speed (Optional). valid values: low, medium, high, highest, custom
        bandwidth: custom sync speed (Optional, int32, MB/s). required when speed is custom
        service_assurance_policy: service assurance policy (Optional). valid values: data_reliability_preferred, service_continuity_preferred
        isolation_threshold_time: isolation threshold (Optional, int32, 10~30000ms). required when service_assurance_policy is service_continuity_preferred
        recovery_policy: recovery policy (Optional). valid values: automatic, manual

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/lun-pairs"

    payload = {
        'create_mode': create_mode,
        'local_storage_id': local_storage_id,
        'domain_id': domain_id
    }

    if lun_ids is not None:
        payload['lun_ids'] = lun_ids
    if lun_pairs is not None:
        payload['lun_pairs'] = lun_pairs
    if remote_storage_pool_id is not None:
        payload['remote_storage_pool_id'] = remote_storage_pool_id
    if remote_vstore_id is not None:
        payload['remote_vstore_id'] = remote_vstore_id
    if remote_resource_name_rule is not None:
        payload['remote_resource_name_rule'] = remote_resource_name_rule
    if name_prefix is not None:
        payload['name_prefix'] = name_prefix
    if name_suffix is not None:
        payload['name_suffix'] = name_suffix
    if speed is not None:
        payload['speed'] = speed
    if bandwidth is not None:
        payload['bandwidth'] = bandwidth
    if service_assurance_policy is not None:
        payload['service_assurance_policy'] = service_assurance_policy
    if isolation_threshold_time is not None:
        payload['isolation_threshold_time'] = isolation_threshold_time
    if recovery_policy is not None:
        payload['recovery_policy'] = recovery_policy

    response = client.post(url, body=payload)
    return response


def hypermetro_pair_modify(client: DMEAPIClient, pair_id: str, speed: str = None,
                            bandwidth: int = None, recovery_policy: str = None,
                            service_assurance_policy: str = None,
                            isolation_threshold_time: int = None) -> dict:
    """
    modify hypermetro Pair

    Args:
        client: DME API client
        pair_id: hypermetro Pair ID
        speed: sync speed, valid values: low, medium, high, highest, custom
        bandwidth: custom sync speed (MB/s), required when speed is custom
        recovery_policy: recovery policy, valid values: automatic, manual
        service_assurance_policy: service assurance policy, valid values: data_reliability_preferred, service_continuity_preferred
        isolation_threshold_time: isolation threshold (milliseconds), required when service_assurance_policy is service_continuity_preferred

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/lun-pairs/{pair_id}"

    payload = {}

    if speed is not None:
        payload['speed'] = speed
    if bandwidth is not None:
        payload['bandwidth'] = bandwidth
    if recovery_policy is not None:
        payload['recovery_policy'] = recovery_policy
    if service_assurance_policy is not None:
        payload['service_assurance_policy'] = service_assurance_policy
    if isolation_threshold_time is not None:
        payload['isolation_threshold_time'] = isolation_threshold_time

    response = client.put(url, body=payload, params={"pair_id": pair_id})
    return response


def hypermetro_pair_delete(client: DMEAPIClient, ids: list, delete_mode: str,
                            is_lun_service_interrupt: bool = None) -> dict:
    """
    Batch delete hypermetro Pairs

    Args:
        client: DME API client
        ids: hypermetro Pair ID list
        delete_mode: delete mode. valid values: preferred_only, non_preferred_only, dual_ends
        is_lun_service_interrupt: whether to allow LUN service interruption (Optional, boolean). valid values: true (allow), false (not allow)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/lun-pairs/delete"

    payload = {
        'ids': ids,
        'delete_mode': delete_mode
    }

    if is_lun_service_interrupt is not None:
        payload['is_lun_service_interrupt'] = is_lun_service_interrupt

    response = client.post(url, body=payload)
    return response


def hypermetro_pair_sync(client: DMEAPIClient, ids: list) -> dict:
    """
    Batch sync hypermetro Pairs

    Args:
        client: DME API client
        ids: hypermetro Pair ID list

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/lun-pairs/sync"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def hypermetro_pair_pause(client: DMEAPIClient, ids: list, priority_station_type: str) -> dict:
    """
    Pause hypermetro Pair

    Args:
        client: DME API client
        ids: hypermetro Pair ID list
        priority_station_type: station type. valid values: preferred, non_preferred

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/lun-pairs/pause"

    payload = {
        'ids': ids,
        'priority_station_type': priority_station_type
    }

    response = client.post(url, body=payload)
    return response


def hypermetro_pair_force_startup(client: DMEAPIClient, ids: list, priority_station_type: str) -> dict:
    """
    Force start hypermetro Pair

    Args:
        client: DME API client
        ids: hypermetro Pair ID list
        priority_station_type: station type. valid values: preferred, non_preferred

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/lun-pairs/force-startup"

    payload = {
        'ids': ids,
        'priority_station_type': priority_station_type
    }

    response = client.post(url, body=payload)
    return response


def hypermetro_pair_switch_priority(client: DMEAPIClient, ids: list) -> dict:
    """
    Switch priority site for hypermetro Pair

    Args:
        client: DME API client
        ids: hypermetro Pair ID list

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/lun-pairs/switch-priority-site"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


# ============================================================================
# hypermetro_domain subtopic - HyperMetro domain related operations
# ============================================================================

def hypermetro_domain_list(client: DMEAPIClient, storage_id: str = None,
                            types: list = None) -> dict:
    """
    Batch query hypermetro domains

    Args:
        client: DME API client
        storage_id: device ID
        types: hypermetro domain type list

    Returns:
        {
            metro_domain_list: hypermetro domain list (List<MetroDomain>). parameter format: [{
                id: hypermetro domain ID (string),
                storage_id: device ID (string),
                storage_name: device name (string, 1~64 characters),
                ip_address: device IP address (string),
                domain_id: hypermetro domain ID on the device (string, 1~32 characters),
                domain_name: hypermetro domain name (string, 1~64 characters),
                running_status: running status. valid values: normal, to_be_recovered, invalid, recovering, faulty, split, force_started,
                domain_type: hypermetro domain mode. valid values: AA_mode, AP_mode,
                type: hypermetro domain usage type. valid values: block, file_system, block_file_system,
                cp_type: arbitration type. valid values: quorum_server, quorum_disk, none,
                cps_name: arbitration server name (string, 1~64 characters),
                cps_running_status: arbitration server running status. valid values: online, offline,
                standby_cps_name: standby arbitration server name (string, 1~64 characters),
                server_ip_master: arbitration server IP address (string),
                server_ip_slave: alternate arbitration server IP address (string),
                iscsi_link_num: ISCSI link count (integer),
                fc_link_num: FC link count (integer),
                ip_link_num: IP link count (integer),
                remote_storage_id: remote device ID (string),
                remote_storage_name: remote device name (string, 1~64 characters),
                remote_storage_ip: remote device IP address (string),
                remote_dev_running_status: remote device running status. valid values: link_up, link_down, disabled, connecting, air_gap_link_down,
                config_role: configuration role. valid values: active_site, standby_site,
            }, ...],
        }
    """
    url = "/rest/protection/v1/hyper-metro-domains/query"

    payload = {}

    if storage_id is not None:
        payload['storage_id'] = storage_id
    if types is not None:
        payload['types'] = types

    response = client.post(url, body=payload)
    return response


# ============================================================================
# replication_pair subtopic - Replication Pair related operations
# ============================================================================

def replication_pair_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 20,
                          group_id: str = None, group_name: str = None,
                          pair_raw_id: str = None, local_storage_id: str = None,
                          local_storage_name: str = None, local_vstore_id: str = None,
                          local_vstore_raw_id: str = None, local_volume_name: str = None,
                          remote_vstore_id: str = None, remote_vstore_raw_id: str = None,
                          remote_volume_name: str = None) -> dict:
    """
    Batch query replication Pairs

    Args:
        client: DME API client
        page_no: pagination page number, default 1
        page_size: items per page, default 20
        group_id: replication consistency group ID
        group_name: replication consistency group name, supports fuzzy match
        pair_raw_id: replication Pair ID on the storage device
        local_storage_id: local storage device ID
        local_storage_name: local storage device name, supports fuzzy match
        local_vstore_id: local tenant ID, mutually exclusive with local_vstore_raw_id
        local_vstore_raw_id: local tenant ID on the device, mutually exclusive with local_vstore_id
        local_volume_name: local LUN name, supports fuzzy match
        remote_vstore_id: remote tenant ID, mutually exclusive with remote_vstore_raw_id
        remote_vstore_raw_id: remote tenant ID on the device, mutually exclusive with remote_vstore_id
        remote_volume_name: remote LUN name, supports fuzzy match

    Returns:
        {
            total: total replication Pairs (int32),
            replication_pairs: replication Pair list (List<ReplicationPairResponse>). parameter format: [{
                id: unique replication Pair ID (string, 1~64 characters),
                raw_id: ID on the storage device (string, 1~64 characters),
                local_storage_id: local storage device ID (string, 1~64 characters),
                local_storage_name: local device name (string, 1~255 characters),
                local_resource_raw_id: local resource ID on the device (string, 1~64 characters),
                local_resource_name: local resource name (string, 1~255 characters),
                remote_storage_id: remote storage device ID (string, 1~64 characters),
                remote_storage_name: remote storage device name (string, 1~255 characters),
                remote_resource_raw_id: remote resource ID on the device (string, 1~64 characters),
                remote_resource_name: remote resource name (string, 1~255 characters),
                local_resource_type: local resource type. valid values: lun (volume), file_system,
                local_vstore_raw_id: local resource tenant ID on the device (string, 1~64 characters),
                remote_vstore_raw_id: remote resource tenant ID on the device (string, 1~64 characters),
                health_status: health status. valid values: unknown, normal, fault,
                running_status: running status. valid values: normal, synchronizing, to_be_recoverd, interrupted, splited, invalid, standby, air_gap_link_down,
                replication_mode: replication mode. valid values: synchronous, asynchronous,
                speed: speed. valid values: low, medium, high, highest, custom,
                bandwidth: custom sync speed (int32, MB/s),
                synchronize_type: sync type. valid values: manual, wait_after_sync_begins, wait_after_sync_ends, specified_time_policy,
                interval: data sync period (integer, 0~86400 seconds),
                sync_left_time: remaining sync time (string),
                recovery_policy: recovery policy. valid values: automatic, manual,
                is_primary: whether local is primary. valid values: true, false,
                rep_io_timeout: remote IO timeout (integer, 10~255 seconds),
                enable_compress: link compression. valid values: true (compressed), false (not compressed),
                compress_valid: whether compression is effective. valid values: true, false,
                sync_start_time: last sync start time (string),
                sync_end_time: last sync end time (string),
                is_in_group: whether it belongs to a consistency group. valid values: true, false,
                group_id: remote replication consistency group ID (string, 1~64 characters),
                group_raw_id: consistency group ID on the device (string, 1~64 characters),
                group_name: consistency group name (string, 1~255 characters),
                data_consistent_status: whether primary and secondary data are consistent. valid values: true, false,
                primary_resource_data_status: primary resource data status. valid values: synchronized, complete, incomplete, unknown,
                secondary_resource_data_status: secondary resource data status. valid values: synchronized, complete, incomplete, unknown,
                secondary_resource_protection: secondary resource read/write setting. valid values: access_denied, read_only, read_write,
                dr_ring_id: ring 3DC object ID on the device (string, 1~64 characters),
                progress: sync progress (int32, -1~100),
            }, ...],
        }
    """
    url = "/rest/protection/v1/replication/pairs/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if group_id is not None:
        payload['group_id'] = group_id
    if group_name is not None:
        payload['group_name'] = group_name
    if pair_raw_id is not None:
        payload['pair_raw_id'] = pair_raw_id
    if local_storage_id is not None:
        payload['local_storage_id'] = local_storage_id
    if local_storage_name is not None:
        payload['local_storage_name'] = local_storage_name
    if local_vstore_id is not None:
        payload['local_vstore_id'] = local_vstore_id
    if local_vstore_raw_id is not None:
        payload['local_vstore_raw_id'] = local_vstore_raw_id
    if local_volume_name is not None:
        payload['local_volume_name'] = local_volume_name
    if remote_vstore_id is not None:
        payload['remote_vstore_id'] = remote_vstore_id
    if remote_vstore_raw_id is not None:
        payload['remote_vstore_raw_id'] = remote_vstore_raw_id
    if remote_volume_name is not None:
        payload['remote_volume_name'] = remote_volume_name

    response = client.post(url, body=payload)
    return response


def replication_pair_create(client: DMEAPIClient, local_storage_id: str,
                            local_lun_id: str, remote_storage_id: str,
                            remote_storage_pool_id: str = None, remote_vstore_id: str = None,
                            remote_resource_name_rule: str = None, name_prefix: str = None,
                            name_suffix: str = None, speed: str = None, bandwidth: int = None,
                            recovery_policy: str = None, sync_type: str = None,
                            timing_value_in_sec: int = None, sync_schedule: dict = None,
                            rep_io_timeout: int = None, sync_snap_policy: str = None,
                            user_snap_retention_num: int = None, switch_to_async: bool = None,
                            enable_compress: bool = None) -> dict:
    """
    create remote replication Pair

    Args:
        client: DME API client
        local_storage_id: local storage device ID
        local_lun_id: local LUN ID
        remote_storage_id: remote storage device ID
        remote_storage_pool_id: remote storage pool ID
        remote_vstore_id: remote device tenant ID
        remote_resource_name_rule: remote resource naming strategy, valid values: same_as_local, prefix_and_suffix, prefix_and_num
        name_prefix: remote resource name prefix
        name_suffix: remote resource name suffix
        speed: sync speed, valid values: low, medium, high, highest, custom
        bandwidth: custom sync speed (MB/s), required when speed is custom
        recovery_policy: recovery policy, valid values: automatic, manual
        sync_type: sync type, valid values: manual, wait_after_sync_begins, wait_after_sync_ends, specified_time_policy
        timing_value_in_sec: timing duration (seconds), required when sync_type is wait_after_sync_begins or wait_after_sync_ends
        sync_schedule: timing schedule, required when sync_type is specified_time_policy
        rep_io_timeout: remote IO timeout (seconds), valid when replication mode is synchronous
        sync_snap_policy: user snapshot sync policy, valid values: not_sync_snap, same_as_source, user_snap_retention_num, snap_tag_based
        user_snap_retention_num: secondary user snapshot retention count
        switch_to_async: switch for automatic conversion from sync to async remote replication
        enable_compress: link compression, required when replication mode is async

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/replication/pairs"

    payload = {
        'local_storage_id': local_storage_id,
        'local_lun_id': local_lun_id,
        'remote_storage_id': remote_storage_id
    }

    if remote_storage_pool_id is not None:
        payload['remote_storage_pool_id'] = remote_storage_pool_id
    if remote_vstore_id is not None:
        payload['remote_vstore_id'] = remote_vstore_id
    if remote_resource_name_rule is not None:
        payload['remote_resource_name_rule'] = remote_resource_name_rule
    if name_prefix is not None:
        payload['name_prefix'] = name_prefix
    if name_suffix is not None:
        payload['name_suffix'] = name_suffix
    if speed is not None:
        payload['speed'] = speed
    if bandwidth is not None:
        payload['bandwidth'] = bandwidth
    if recovery_policy is not None:
        payload['recovery_policy'] = recovery_policy
    if sync_type is not None:
        payload['sync_type'] = sync_type
    if timing_value_in_sec is not None:
        payload['timing_value_in_sec'] = timing_value_in_sec
    if sync_schedule is not None:
        payload['sync_schedule'] = sync_schedule
    if rep_io_timeout is not None:
        payload['rep_io_timeout'] = rep_io_timeout
    if sync_snap_policy is not None:
        payload['sync_snap_policy'] = sync_snap_policy
    if user_snap_retention_num is not None:
        payload['user_snap_retention_num'] = user_snap_retention_num
    if switch_to_async is not None:
        payload['switch_to_async'] = switch_to_async
    if enable_compress is not None:
        payload['enable_compress'] = enable_compress

    response = client.post(url, body=payload)
    return response


def replication_pair_modify(client: DMEAPIClient, pair_id: str, speed: str = None,
                            bandwidth: int = None, recovery_policy: str = None,
                            enable_compress: bool = None, sync_type: str = None,
                            timing_value_in_sec: int = None, sync_schedule: dict = None,
                            rep_io_timeout: int = None, sync_snap_policy: str = None,
                            user_snap_retention_num: int = None, switch_to_async: bool = None) -> dict:
    """
    modify replication Pair

    Args:
        client: DME API client
        pair_id: replication Pair instance ID
        speed: sync speed, valid values: low, medium, high, highest, custom
        bandwidth: custom sync speed (MB/s), required when speed is custom
        recovery_policy: recovery policy, valid values: automatic, manual
        enable_compress: link compression, required when replication mode is async
        sync_type: sync type, valid values: manual, wait_after_sync_begins, wait_after_sync_ends, specified_time_policy
        timing_value_in_sec: timing duration (seconds), required when sync_type is wait_after_sync_begins or wait_after_sync_ends
        sync_schedule: timing schedule, required when sync_type is specified_time_policy
        rep_io_timeout: remote IO timeout (seconds), valid when replication mode is synchronous
        sync_snap_policy: user snapshot sync policy, valid values: not_sync_snap, same_as_source, user_snap_retention_num, snap_tag_based
        user_snap_retention_num: secondary user snapshot retention count
        switch_to_async: switch for automatic conversion from sync to async remote replication

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/replication/pairs/{pair_id}"

    payload = {}

    if speed is not None:
        payload['speed'] = speed
    if bandwidth is not None:
        payload['bandwidth'] = bandwidth
    if recovery_policy is not None:
        payload['recovery_policy'] = recovery_policy
    if enable_compress is not None:
        payload['enable_compress'] = enable_compress
    if sync_type is not None:
        payload['sync_type'] = sync_type
    if timing_value_in_sec is not None:
        payload['timing_value_in_sec'] = timing_value_in_sec
    if sync_schedule is not None:
        payload['sync_schedule'] = sync_schedule
    if rep_io_timeout is not None:
        payload['rep_io_timeout'] = rep_io_timeout
    if sync_snap_policy is not None:
        payload['sync_snap_policy'] = sync_snap_policy
    if user_snap_retention_num is not None:
        payload['user_snap_retention_num'] = user_snap_retention_num
    if switch_to_async is not None:
        payload['switch_to_async'] = switch_to_async

    response = client.put(url, body=payload, params={"pair_id": pair_id})
    return response


def replication_pair_delete(client: DMEAPIClient, ids: list, delete_mode: str = None) -> dict:
    """
    Batch delete remote replication Pairs

    Args:
        client: DME API client
        ids: replication Pair instance ID list
        delete_mode: delete mode, valid values: primary_only, secondary_only, dual_ends, default dual_ends

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/replication/pairs/delete"

    payload = {
        'ids': ids
    }

    if delete_mode is not None:
        payload['delete_mode'] = delete_mode

    response = client.post(url, body=payload)
    return response


def replication_pair_sync(client: DMEAPIClient, ids: list) -> dict:
    """
    Batch sync remote replication Pairs

    Args:
        client: DME API client
        ids: replication Pair ID list

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/replication/pairs/sync"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def replication_pair_split(client: DMEAPIClient, ids: list) -> dict:
    """
    Batch split remote replication Pairs

    Args:
        client: DME API client
        ids: replication Pair ID list

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/replication/pairs/split"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def replication_pair_switch(client: DMEAPIClient, ids: list) -> dict:
    """
    Batch primary-secondary switch for remote replication Pairs

    Args:
        client: DME API client
        ids: replication Pair ID list

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/replication/pairs/switch"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def replication_pair_switch_write_protection(client: DMEAPIClient, id: str, operation_type: str) -> dict:
    """
    Switch write protection state for remote replication Pair secondary resource

    Args:
        client: DME API client
        id: replication Pair ID
        operation_type: operation type, valid values: enable, disable

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/replication/pairs/{id}/switch-write-protection"

    payload = {
        'operation_type': operation_type
    }

    response = client.post(url, body=payload, params={"id": id})
    return response


# ============================================================================
# device subtopic - Device Pair and replication link related operations
# ============================================================================

def device_pair_list(client: DMEAPIClient, storage_id: str = None) -> dict:
    """
    Query device Pairs

    Args:
        client: DME API client
        storage_id: Storage device ID

    Returns:
        {
            total: total device Pairs (int32),
            device_pairs: device Pair list (List<DevicePairInfo>). parameter format: [{
                id: device Pair ID (string, 1~64 characters),
                local_storage_sn: local device SN (string, 0~32 characters),
                remote_storage_sn: remote device SN (string, 0~32 characters),
                local_storage_ip: local device IP (string, 1~64 characters),
                local_storage_name: local device name (string, 0~255 characters),
                local_storage_model: local device model (string, 0~32 characters),
                local_storage_version: local device version (string, 0~32 characters),
                remote_storage_identifier: remote device identifier ID on local device (string, 0~32 characters),
                remote_storage_name: remote device name (string, 0~255 characters),
                remote_storage_wwn: remote device WWN (string, 0~64 characters),
                remote_storage_vendor: remote device vendor (string, 0~32 characters),
                remote_storage_ip: remote device IP (string, 1~64 characters),
                remote_storage_model: remote device model (string, 0~32 characters),
                remote_storage_type: remote device type. valid values: replication_device, heterogeneous_device, unknown_device, cloud_replication_device,
                remote_storage_version: remote device version (string, 0~32 characters),
                running_status: running status. valid values: link_up, link_down, disabled, connecting, air_gap_link_down,
                health_status: health status. valid values: normal, fault, invalid,
                compress_alg_valid: whether compression status is valid. valid values: true, false,
                compress_algorithm: compression strategy. valid values: depth_compression, fast_compression, invalid, fault,
            }, ...],
        }
    """
    url = "/rest/protection/v1/device-pairs/query"

    payload = {}

    if storage_id is not None:
        payload['storage_id'] = storage_id

    response = client.post(url, body=payload)
    return response


def replication_link_list(client: DMEAPIClient, local_storage_id: str = None,
                          page_no: int = None, page_size: int = None,
                          health_status: str = None,
                          running_status: str = None,
                          link_type: str = None) -> dict:
    """
    Query replication links

    Args:
        client: DME API client
        local_storage_id: local storage device ID (Optional, string, 1~64 characters), query as source storage device
        page_no: pagination page number (Optional, int32, default 1)
        page_size: items per page (Optional, int32, 1~1000, default 20)
        health_status: health status (Optional, string). valid values: normal, fault
        running_status: running status (Optional, string). valid values: link_up, link_down, disabled, connecting, air_gap_link_down
        link_type: replication link type (Optional, string). valid values: fc_link, ip_link

    Returns:
        {
            total: total replication links (int32),
            replication_links: replication link list (List<ReplicationLinkInfo>). parameter format: [{
                id: replication link ID (string, 1~64 characters),
                link_type: link type. valid values: fc_link, ip_link,
                local_storage_id: local storage device ID (string, 1~64 characters),
                health_status: health status. valid values: normal, fault,
                running_status: running status. valid values: link_up, link_down, disabled, connecting, air_gap_link_down,
            }, ...],
        }
    """
    url = "/rest/protection/v1/device-pairs/replication-links/query"

    payload = {}

    if local_storage_id is not None:
        payload['local_storage_id'] = local_storage_id
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size
    if health_status is not None:
        payload['health_status'] = health_status
    if running_status is not None:
        payload['running_status'] = running_status
    if link_type is not None:
        payload['link_type'] = link_type

    response = client.post(url, body=payload)
    return response


# ============================================================================
# snapshot subtopic - LUN snapshot related operations
# ============================================================================

def snapshot_list(client: DMEAPIClient, snapshot_ids: list = None, storage_id: str = None,
                  raw_id: str = None, name: str = None, health_status: str = None,
                  running_status: str = None, source_lun_name: str = None,
                  parent_name: str = None, activated_time_from: int = None,
                  activated_time_to: int = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch query LUN snapshots

    Args:
        client: DME API client
        snapshot_ids: snapshot ID list
        storage_id: Storage device ID
        raw_id: snapshot ID on the storage device
        name: snapshot name, supports fuzzy query
        health_status: health status, valid values: normal, fault, write_protected
        running_status: running status, valid values: activated, rolling_back, unactivated, initializing, deleting, unknown
        source_lun_name: source LUN name, supports fuzzy query
        parent_name: parent object name, supports fuzzy query
        activated_time_from: query activation time start point (Unix timestamp, seconds)
        activated_time_to: query activation time end point (Unix timestamp, seconds)
        page_no: pagination start page, min 1, default 1
        page_size: items per page, 1~1000, default 20

    Returns:
        {
            total: total LUN snapshots (int32),
            snapshots: LUN snapshot list (List<LunSnapshotInfo>). parameter format: [{
                id: snapshot ID (string, 1~64 characters),
                raw_id: snapshot ID on the storage device (string, 1~64 characters),
                name: snapshot name (string, 1~255 characters),
                parent_type: parent object type. valid values: lun (LUN), snapshot,
                parent_id: parent object ID (string, 1~64 characters),
                parent_raw_id: parent object ID on the storage device (string, 1~64 characters),
                parent_name: parent object name (string, 1~255 characters),
                health_status: health status. valid values: normal, fault, write_protected,
                running_status: running status. valid values: activated, rolling_back, unactivated, initializing, deleting, unknown,
                description: snapshot description info (string, 0~255 characters),
                activated_time: snapshot activation time (int64),
                rollback_start_time: rollback start time (int64),
                rollback_end_time: rollback end time (int64),
                rollback_speed: rollback speed. valid values: low, medium, high, highest, unknown,
                rollback_rate: rollback progress (int32, -1~100),
                is_mapped: mapping status. valid values: true (mapped), false (not mapped),
                wwn: WWN (string, 1~64 characters),
                user_capacity: snapshot user capacity (int64, bytes),
                consumed_capacity: snapshot actual consumed capacity (int64, bytes),
                snapshot_cg_id: snapshot consistency group ID (string, 1~64 characters),
                snapshot_cg_name: snapshot consistency group name (string, 1~255 characters),
                source_lun_id: source LUN ID (string, 1~64 characters),
                source_lun_name: source LUN name (string, 1~255 characters),
                storage_id: storage device ID (string, 1~64 characters),
            }, ...],
        }
    """
    url = "/rest/protection/v1/lun-snapshots/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if snapshot_ids is not None:
        payload['snapshot_ids'] = snapshot_ids
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if name is not None:
        payload['name'] = name
    if health_status is not None:
        payload['health_status'] = health_status
    if running_status is not None:
        payload['running_status'] = running_status
    if source_lun_name is not None:
        payload['source_lun_name'] = source_lun_name
    if parent_name is not None:
        payload['parent_name'] = parent_name
    if activated_time_from is not None:
        payload['activated_time_from'] = activated_time_from
    if activated_time_to is not None:
        payload['activated_time_to'] = activated_time_to

    response = client.post(url, body=payload)
    return response


def snapshot_create(client: DMEAPIClient, snapshots_info: list, is_consist_activate: bool = None) -> dict:
    """
    Batch create LUN snapshots

    Args:
        client: DME API client
        snapshots_info: LUN snapshot creation info list (List<LunSnapshotCreateInfo>, max array members: 2048). parameter format: [{
                name: snapshot name (1~255 characters),
                source_type: source object type. valid values: lun (LUN), snapshot,
                source_id: source object ID (1~64 characters),
             }, ...]
        is_consist_activate: whether to consistently activate, default false

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/lun-snapshots"

    payload = {
        'snapshots_info': snapshots_info
    }

    if is_consist_activate is not None:
        payload['is_consist_activate'] = is_consist_activate

    response = client.post(url, body=payload)
    return response


def snapshot_rollback(client: DMEAPIClient, rollback_speed: str, rollback_snapshots: list) -> dict:
    """
    Batch rollback LUN snapshots

    Args:
        client: DME API client
        rollback_speed: rollback speed, valid values: low, medium, high, highest
        rollback_snapshots: snapshot rollback resource info list, each item contains snapshot_id, target_type, target_id

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/lun-snapshots/batch-rollback"

    payload = {
        'rollback_speed': rollback_speed,
        'rollback_snapshots': rollback_snapshots
    }

    response = client.post(url, body=payload)
    return response


def snapshot_delete(client: DMEAPIClient, snapshot_ids: list, is_delete_target_lun: bool = None,
                    is_auto_deactivate: bool = None) -> dict:
    """
    Batch delete LUN snapshots

    Args:
        client: DME API client
        snapshot_ids: snapshot ID list
        is_delete_target_lun: whether to delete target LUN, default true
        is_auto_deactivate: whether to automatically deactivate snapshot before deletion, default false

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/lun-snapshots/batch-delete"

    payload = {
        'snapshot_ids': snapshot_ids
    }

    if is_delete_target_lun is not None:
        payload['is_delete_target_lun'] = is_delete_target_lun
    if is_auto_deactivate is not None:
        payload['is_auto_deactivate'] = is_auto_deactivate

    response = client.post(url, body=payload)
    return response


# ============================================================================
# snapshot_group subtopic - Snapshot consistency group related operations
# ============================================================================

def snapshot_group_create(client: DMEAPIClient, name: str, protect_group_id: str,
                          description: str = None, creation_mode: str = None) -> dict:
    """
    create snapshot consistency group

    Args:
        client: DME API client
        name: snapshot consistency group name
        protect_group_id: protection group ID
        description: description info
        creation_mode: creation mode, valid values: new_snapshot

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/snapshot-consistency-groups"

    payload = {
        'name': name,
        'protect_group_id': protect_group_id
    }

    if description is not None:
        payload['description'] = description
    if creation_mode is not None:
        payload['creation_mode'] = creation_mode

    response = client.post(url, body=payload)
    return response


def snapshot_group_delete(client: DMEAPIClient, snapshot_cg_ids: list, is_delete_target_lun: bool = None) -> dict:
    """
    Batch delete snapshot consistency groups

    Args:
        client: DME API client
        snapshot_cg_ids: snapshot consistency group ID list
        is_delete_target_lun: whether to delete target LUN, only supported in Dorado 6.1.2 and above, default true

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/snapshot-consistency-groups/batch-delete"

    payload = {
        'snapshot_cg_ids': snapshot_cg_ids
    }

    if is_delete_target_lun is not None:
        payload['is_delete_target_lun'] = is_delete_target_lun

    response = client.post(url, body=payload)
    return response


def snapshot_group_activate(client: DMEAPIClient, snapshot_cg_id: str, object_type: str = None,
                            snapshot_create_mode: str = None, name_rule: str = None,
                            name_prefix: str = None, name_suffix: str = None,
                            target_snapshot_objects: list = None) -> dict:
    """
    Activate snapshot consistency group

    Args:
        client: DME API client
        snapshot_cg_id: snapshot consistency group ID
        object_type: object type, valid values: parent_object
        snapshot_create_mode: snapshot creation mode, valid values: auto, manual
        name_rule: snapshot naming rule, valid values: prefix_and_suffix, prefix_and_num
        name_prefix: snapshot name prefix
        name_suffix: snapshot name suffix
        target_snapshot_objects: target snapshot object list

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/snapshot-consistency-groups/{snapshot_cg_id}/activate"

    payload = {}

    if object_type is not None:
        payload['object_type'] = object_type
    if snapshot_create_mode is not None:
        payload['snapshot_create_mode'] = snapshot_create_mode
    if name_rule is not None:
        payload['name_rule'] = name_rule
    if name_prefix is not None:
        payload['name_prefix'] = name_prefix
    if name_suffix is not None:
        payload['name_suffix'] = name_suffix
    if target_snapshot_objects is not None:
        payload['target_snapshot_objects'] = target_snapshot_objects

    response = client.post(url, body=payload, params={"snapshot_cg_id": snapshot_cg_id})
    return response


def snapshot_group_deactivate(client: DMEAPIClient, snapshot_cg_ids: list) -> dict:
    """
    Batch deactivate snapshot consistency groups

    Args:
        client: DME API client
        snapshot_cg_ids: snapshot consistency group ID list

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/snapshot-consistency-groups/batch-deactivate"

    payload = {
        'snapshot_cg_ids': snapshot_cg_ids
    }

    response = client.post(url, body=payload)
    return response


def snapshot_group_rollback(client: DMEAPIClient, snapshot_cg_id: str, rollback_speed: str = None,
                            snapshot_create_mode: str = None, name_rule: str = None,
                            name_prefix: str = None, name_suffix: str = None,
                            target_snapshot_objects: list = None) -> dict:
    """
    Rollback snapshot consistency group

    Args:
        client: DME API client
        snapshot_cg_id: snapshot consistency group ID
        rollback_speed: rollback speed, valid values: low, medium, high, highest
        snapshot_create_mode: snapshot creation mode, valid values: auto, manual
        name_rule: snapshot naming rule, valid values: prefix_and_suffix, prefix_and_num
        name_prefix: snapshot name prefix
        name_suffix: snapshot name suffix
        target_snapshot_objects: target snapshot object list

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/snapshot-consistency-groups/{snapshot_cg_id}/rollback"

    payload = {}

    if rollback_speed is not None:
        payload['rollback_speed'] = rollback_speed
    if snapshot_create_mode is not None:
        payload['snapshot_create_mode'] = snapshot_create_mode
    if name_rule is not None:
        payload['name_rule'] = name_rule
    if name_prefix is not None:
        payload['name_prefix'] = name_prefix
    if name_suffix is not None:
        payload['name_suffix'] = name_suffix
    if target_snapshot_objects is not None:
        payload['target_snapshot_objects'] = target_snapshot_objects

    response = client.post(url, body=payload, params={"snapshot_cg_id": snapshot_cg_id})
    return response


# ============================================================================
# clone_group subtopic - Clone consistency group related operations
# ============================================================================

def clone_group_create(client: DMEAPIClient, name: str, protect_group_id: str,
                       create_mode: str, description: str = None, name_rule: str = None,
                       name_prefix: str = None, name_suffix: str = None,
                       copy_rate: str = None, is_sync: bool = None,
                       clone_pairs: list = None) -> dict:
    """
    create clone consistency group

    Args:
        client: DME API client
        name: clone consistency group name
        protect_group_id: protection group ID
        create_mode: creation mode, valid values: auto, manual
        description: description info
        name_rule: target LUN naming rule, valid values: prefix_and_suffix, prefix_and_num
        name_prefix: target LUN name prefix
        name_suffix: target LUN name suffix
        copy_rate: copy rate, valid values: low, medium, high, highest, default medium
        is_sync: whether to sync immediately, default true
        clone_pairs: clone Pair list (List<TargetClonePairObject>, max array members: 4096), required when create_mode is manual. parameter format: [{
                source_lun_id: source LUN ID (1~32 characters),
                target_lun_id: target LUN ID (1~32 characters),
             }, ...]

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/clone-consistency-groups"

    payload = {
        'name': name,
        'protect_group_id': protect_group_id,
        'create_mode': create_mode
    }

    if description is not None:
        payload['description'] = description
    if name_rule is not None:
        payload['name_rule'] = name_rule
    if name_prefix is not None:
        payload['name_prefix'] = name_prefix
    if name_suffix is not None:
        payload['name_suffix'] = name_suffix
    if copy_rate is not None:
        payload['copy_rate'] = copy_rate
    if is_sync is not None:
        payload['is_sync'] = is_sync
    if clone_pairs is not None:
        payload['clone_pairs'] = clone_pairs

    response = client.post(url, body=payload)
    return response


def clone_group_sync(client: DMEAPIClient, clone_cg_id: str, create_mode: str = None,
                            name_rule: str = None, name_prefix: str = None,
                            name_suffix: str = None, clone_pairs: list = None) -> dict:
    """
    Sync clone consistency group

    Args:
        client: DME API client
        clone_cg_id: clone consistency group ID
        create_mode: clone Pair creation mode, valid values: auto, manual
        name_rule: target LUN naming rule, valid values: prefix_and_suffix, prefix_and_num
        name_prefix: target LUN name prefix
        name_suffix: target LUN name suffix
        clone_pairs: clone Pair list (List<TargetClonePairObject>, max array members: 4096), required when create_mode is manual. parameter format: [{
                source_lun_id: source LUN ID (1~32 characters),
                target_lun_id: target LUN ID (1~32 characters),
             }, ...]

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/clone-consistency-groups/{clone_cg_id}/synchronize"

    payload = {}

    if create_mode is not None:
        payload['create_mode'] = create_mode
    if name_rule is not None:
        payload['name_rule'] = name_rule
    if name_prefix is not None:
        payload['name_prefix'] = name_prefix
    if name_suffix is not None:
        payload['name_suffix'] = name_suffix
    if clone_pairs is not None:
        payload['clone_pairs'] = clone_pairs

    response = client.post(url, body=payload, params={"clone_cg_id": clone_cg_id})
    return response


def clone_group_delete(client: DMEAPIClient, ids: list, is_delete_dst_lun: bool = None,
                       is_recycle_dst_lun_data: bool = None) -> dict:
    """
    Batch delete clone consistency groups

    Args:
        client: DME API client
        ids: clone consistency group ID list
        is_delete_dst_lun: whether to delete target LUN
        is_recycle_dst_lun_data: whether to recycle target LUN data

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/clone-consistency-groups/batch-delete"

    payload = {
        'ids': ids
    }

    if is_delete_dst_lun is not None:
        payload['is_delete_dst_lun'] = is_delete_dst_lun
    if is_recycle_dst_lun_data is not None:
        payload['is_recycle_dst_lun_data'] = is_recycle_dst_lun_data

    response = client.post(url, body=payload)
    return response


# ============================================================================
# replication_group subtopic - Replication consistency group related operations
# ============================================================================

def replication_group_create(client: DMEAPIClient, cg_name: str, remote_storage_id: str,
                              local_pg_id: str = None, description: str = None,
                              remote_lun_group_id: str = None, local_storage_id: str = None,
                              create_mode: str = None, existed_pair_ids: list = None,
                              lun_pairs: list = None, lun_ids: list = None,
                              remote_storage_pool_id: str = None, remote_vstore_id: str = None,
                              remote_resource_name_rule: str = None, name_prefix: str = None,
                              name_suffix: str = None) -> dict:
    """
    create remote replication consistency group

    Args:
        client: DME API client
        cg_name: remote replication consistency group name
        remote_storage_id: remote storage device ID
        local_pg_id: local protection group ID, required when storage device version is OceanStor V6, OceanStor Dorado V6
        description: description info
        remote_lun_group_id: remote LUN group ID, required when storage device version is OceanStor V6, OceanStor Dorado V6 and local protection group is based on LUN group
        local_storage_id: local storage device ID, required when storage device version is not OceanStor V6, OceanStor Dorado V6
        create_mode: replication Pair creation mode, valid values: auto, manual
        existed_pair_ids: existing replication Pair ID list
        lun_pairs: in manual creation mode, source LUN and target LUN ID list for replication Pairs (List<PairInstance>, max array members: 100). parameter format: [{
                local_lun_id: local LUN ID (Required, 1~32 characters),
                remote_lun_id: remote LUN ID (Required, 1~32 characters),
             }, ...]
        lun_ids: in auto creation mode, source LUN ID list
        remote_storage_pool_id: remote storage pool ID, valid in auto creation mode
        remote_vstore_id: remote device tenant ID, valid in auto creation mode
        remote_resource_name_rule: remote resource naming strategy, valid values: same_as_local, prefix_and_suffix, prefix_and_num
        name_prefix: remote resource name prefix
        name_suffix: remote resource name suffix

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/replication/groups"

    payload = {
        'cg_name': cg_name,
        'remote_storage_id': remote_storage_id
    }

    if local_pg_id is not None:
        payload['local_pg_id'] = local_pg_id
    if description is not None:
        payload['description'] = description
    if remote_lun_group_id is not None:
        payload['remote_lun_group_id'] = remote_lun_group_id
    if local_storage_id is not None:
        payload['local_storage_id'] = local_storage_id
    if create_mode is not None:
        payload['create_mode'] = create_mode
    if existed_pair_ids is not None:
        payload['existed_pair_ids'] = existed_pair_ids
    if lun_pairs is not None:
        payload['lun_pairs'] = lun_pairs
    if lun_ids is not None:
        payload['lun_ids'] = lun_ids
    if remote_storage_pool_id is not None:
        payload['remote_storage_pool_id'] = remote_storage_pool_id
    if remote_vstore_id is not None:
        payload['remote_vstore_id'] = remote_vstore_id
    if remote_resource_name_rule is not None:
        payload['remote_resource_name_rule'] = remote_resource_name_rule
    if name_prefix is not None:
        payload['name_prefix'] = name_prefix
    if name_suffix is not None:
        payload['name_suffix'] = name_suffix

    response = client.post(url, body=payload)
    return response


def replication_group_modify(client: DMEAPIClient, replication_group_id: str, name: str = None,
                              description: str = None, speed: str = None, bandwidth: int = None,
                              recovery_policy: str = None, enable_compress: bool = None,
                              sync_type: str = None, timing_value_in_sec: int = None,
                              sync_schedule: dict = None, rep_io_timeout: int = None,
                              sync_snap_policy: str = None, user_snap_retention_num: int = None,
                              switch_to_async: bool = None) -> dict:
    """
    modify remote replication consistency group

    Args:
        client: DME API client
        replication_group_id: remote replication consistency group ID
        name: remote replication consistency group name
        description: description info
        speed: sync speed, valid values: low, medium, high, highest, custom
        bandwidth: custom sync speed (MB/s), required when speed is custom
        recovery_policy: recovery policy, valid values: automatic, manual
        enable_compress: link compression, required when replication mode is async
        sync_type: sync type, valid values: manual, wait_after_sync_begins, wait_after_sync_ends, specified_time_policy
        timing_value_in_sec: timing duration (seconds), required when sync_type is wait_after_sync_begins or wait_after_sync_ends
        sync_schedule: timing schedule, required when sync_type is specified_time_policy
        rep_io_timeout: remote IO timeout (seconds), valid when replication mode is synchronous
        sync_snap_policy: user snapshot sync policy, valid values: not_sync_snap, same_as_source, user_snap_retention_num, snap_tag_based
        user_snap_retention_num: secondary user snapshot retention count
        switch_to_async: switch for automatic conversion from sync to async remote replication

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/replication/groups/{replication_group_id}"

    payload = {}

    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description
    if speed is not None:
        payload['speed'] = speed
    if bandwidth is not None:
        payload['bandwidth'] = bandwidth
    if recovery_policy is not None:
        payload['recovery_policy'] = recovery_policy
    if enable_compress is not None:
        payload['enable_compress'] = enable_compress
    if sync_type is not None:
        payload['sync_type'] = sync_type
    if timing_value_in_sec is not None:
        payload['timing_value_in_sec'] = timing_value_in_sec
    if sync_schedule is not None:
        payload['sync_schedule'] = sync_schedule
    if rep_io_timeout is not None:
        payload['rep_io_timeout'] = rep_io_timeout
    if sync_snap_policy is not None:
        payload['sync_snap_policy'] = sync_snap_policy
    if user_snap_retention_num is not None:
        payload['user_snap_retention_num'] = user_snap_retention_num
    if switch_to_async is not None:
        payload['switch_to_async'] = switch_to_async

    response = client.put(url, body=payload, params={"replication_group_id": replication_group_id})
    return response


def replication_group_delete(client: DMEAPIClient, ids: list, is_self_adapt: bool = None,
                              delete_mode: str = None) -> dict:
    """
    Batch delete remote replication consistency groups

    Args:
        client: DME API client
        ids: remote replication consistency group ID list
        is_self_adapt: whether to support adaptive removal of member Pairs, default false
        delete_mode: delete mode, valid values: primary_only, secondary_only, dual_ends, default dual_ends

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/replication/groups/delete"

    payload = {
        'ids': ids
    }

    if is_self_adapt is not None:
        payload['is_self_adapt'] = is_self_adapt
    if delete_mode is not None:
        payload['delete_mode'] = delete_mode

    response = client.post(url, body=payload)
    return response


def replication_group_add_pairs(client: DMEAPIClient, group_id: str, pair_ids: list) -> dict:
    """
    Add member Pairs to remote replication consistency group (Not supported below OceanStor Dorado V6 6.1.3, requires group health status normal and running status normal or split)

    Args:
        client: DME API client
        group_id: remote replication consistency group ID
        pair_ids: remote replication Pair ID list

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/replication/groups/{group_id}/add-pairs"

    payload = {
        'pair_ids': pair_ids
    }

    response = client.post(url, body=payload, params={"group_id": group_id})
    return response


def replication_group_remove_pairs(client: DMEAPIClient, group_id: str, pair_ids: list) -> dict:
    """
    Remove member Pairs from remote replication consistency group

    Args:
        client: DME API client
        group_id: remote replication consistency group ID
        pair_ids: remote replication Pair ID list

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/replication/groups/{group_id}/remove-pairs"

    payload = {
        'pair_ids': pair_ids
    }

    response = client.post(url, body=payload, params={"group_id": group_id})
    return response


def replication_group_sync(client: DMEAPIClient, ids: list) -> dict:
    """
    Batch sync remote replication consistency groups

    >![](public_sys-resources/icon-notice.gif) **Notice: **
    >This API may directly or indirectly affect running services, cause service interruption, key data loss, etc., please operate with caution. 

    Args:
        client: DME API client
        ids: consistency group ID list

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/replication/groups/sync"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def replication_group_split(client: DMEAPIClient, ids: list) -> dict:
    """
    Batch split remote replication consistency groups

    >![](public_sys-resources/icon-notice.gif) **Notice: **
    >This API may directly or indirectly affect running services, cause service interruption, key data loss, etc., please operate with caution. 

    Args:
        client: DME API client
        ids: consistency group ID list

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/replication/groups/split"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def replication_group_switch(client: DMEAPIClient, ids: list) -> dict:
    """
    Batch primary-secondary switch for remote replication consistency groups

    >![](public_sys-resources/icon-notice.gif) **Notice: **
    >This API may directly or indirectly affect running services, cause service interruption, key data loss, etc., please operate with caution. 

    Args:
        client: DME API client
        ids: consistency group ID list

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/replication/groups/switch"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def replication_group_switch_write_protection(client: DMEAPIClient, id: str, operation_type: str) -> dict:
    """
    Switch write protection state for remote replication consistency group secondary resource

    Args:
        client: DME API client
        id: consistency group ID
        operation_type: operation type, valid values: enable, disable

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/replication/groups/{id}/switch-write-protection"

    payload = {
        'operation_type': operation_type
    }

    response = client.post(url, body=payload, params={"id": id})
    return response


def replication_group_list(client: DMEAPIClient, page_no: int = None, page_size: int = None,
                           protect_group_id: str = None, name: str = None, raw_id: str = None,
                           running_status: str = None, health_status: str = None,
                           storage_name: str = None, storage_id: str = None,
                           replication_mode: str = None) -> dict:
    """
    Batch query replication consistency groups

    Args:
        client: DME API client
        page_no: pagination start position (Optional, int32, default 1)
        page_size: items per page (Optional, int32, 1~1000, default 20)
        protect_group_id: protection group ID (Optional, string, 1~64 characters)
        name: replication consistency group name (Optional, string, 1~255 characters), supports fuzzy match
        raw_id: replication consistency group ID on the device (Optional, string, 1~64 characters)
        running_status: running status (Optional, string). valid values: normal, synchronizing, splited, to_be_recoverd, interrupted, invalid, standby, air_gap_link_down
        health_status: health status (Optional, string). valid values: normal, fault, invalid
        storage_name: storage device name (Optional, string, 1~255 characters), supports fuzzy match
        storage_id: Storage device ID (Optional, string, 1~64 characters)
        replication_mode: replication mode (Optional, string). valid values: synchronous, asynchronous

    Returns:
        {
            total: total replication consistency groups (int32),
            groups: replication consistency group list (List<ReplicationGroupDetail>). parameter format: [{
                id: replication consistency group ID (string, 1~64 characters),
                raw_id: replication consistency group ID on the device (string, 1~64 characters),
                name: replication consistency group name (string, 1~255 characters),
                replication_model: replication mode (string). valid values: synchronous, asynchronous,
                storage_name: storage device name (string, 0~255 characters),
                storage_id: Storage device id (string, 1~64 characters),
                health_status: health status (string). valid values: normal, fault, invalid,
                running_status: running status (string). valid values: normal, synchronizing, splited, to_be_recoverd, interrupted, invalid, standby, air_gap_link_down,
                protect_group_id: protection group ID (string, 0~64 characters),
                protect_group_name: protection group name (string, 0~255 characters),
            }, ...],
        }
    """
    url = "/rest/protection/v1/replication/groups/query"

    payload = {}
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size
    if protect_group_id is not None:
        payload['protect_group_id'] = protect_group_id
    if name is not None:
        payload['name'] = name
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if running_status is not None:
        payload['running_status'] = running_status
    if health_status is not None:
        payload['health_status'] = health_status
    if storage_name is not None:
        payload['storage_name'] = storage_name
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if replication_mode is not None:
        payload['replication_mode'] = replication_mode

    response = client.post(url, body=payload)
    return response


# ============================================================================
# Filesystem hypermetro Pair (fs_hypermetro_pair) subtopic functions
# ============================================================================


def filesystem_pair_create(client: DMEAPIClient, vstore_pair_id: str,
                            create_mode: str = "manual", fs_pairs: list = None,
                            speed: str = None, bandwidth: int = None,
                            service_assurance_policy: str = None,
                            isolation_threshold_time: int = None) -> dict:
    """
    create Filesystem hypermetro Pair. This API may directly or indirectly affect running services, please operate with caution. 

    Args:
        client: DME API client
        vstore_pair_id: hypermetro tenant Pair ID (Required, string, 1~32 characters)
        create_mode: creation mode (Optional, string). valid values: manual. default value: manual
        fs_pairs: Filesystem Pair list (Optional, List[FsPairInstance], max array members: 100)
        speed: sync speed (Optional, string). valid values: low, medium, high, highest, custom
        bandwidth: bandwidth (Optional, integer, 1~1024). required when speed is custom
        service_assurance_policy: service assurance policy (Optional, string). valid values: data_reliability_preferred, service_continuity_preferred
        isolation_threshold_time: isolation threshold (Optional, int32, 10~30000)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/hypermetro/filesystem-pairs"

    if not vstore_pair_id:
        raise ValueError("vstore_pair_id is a required parameter")

    payload = {
        'vstore_pair_id': vstore_pair_id,
        'create_mode': create_mode
    }
    if fs_pairs is not None:
        payload['fs_pairs'] = fs_pairs
    if speed is not None:
        payload['speed'] = speed
    if bandwidth is not None:
        payload['bandwidth'] = bandwidth
    if service_assurance_policy is not None:
        payload['service_assurance_policy'] = service_assurance_policy
    if isolation_threshold_time is not None:
        payload['isolation_threshold_time'] = isolation_threshold_time

    response = client.post(url, body=payload)
    return response


def filesystem_pair_list(client: DMEAPIClient, ids: list = None, name: str = None,
                          status: str = None, storage_id: str = None,
                          vstore_pair_id: str = None, local_fs_name: str = None,
                          local_fs_id: str = None, health_status: str = None,
                          running_status: str = None, sort_key: str = None,
                          sort_dir: str = None, page_no: int = 1,
                          page_size: int = 20) -> dict:
    """
    Query Filesystem hypermetro Pair list. 

    Args:
        client: DME API client
        ids: hypermetro Pair instance ID list (Optional, List[string])
        name: hypermetro Pair name (Optional, string)
        status: running status (Optional, string)
        storage_id: storage device ID (Optional, string)
        vstore_pair_id: hypermetro tenant Pair ID (Optional, string)
        local_fs_name: local Filesystem name (Optional, string)
        local_fs_id: local Filesystem ID (Optional, string)
        health_status: health status (Optional, string)
        running_status: running status (Optional, string)
        sort_key: sort field (Optional, string)
        sort_dir: sort direction (Optional, string)
        page_no: pagination page number (Optional, int32)
        page_size: items per page (Optional, int32)

    Returns:
        {
            total: total Filesystem hypermetro Pairs (int32),
            file_system_pairs: Filesystem hypermetro Pair list (List<FileSystemHyperMetroPair>). parameter format: [{
                id: Filesystem hypermetro Pair ID (string),
                pair_raw_id: ID on the storage device (string),
                local_filesystem_raw_id: local Filesystem ID on the device (string),
                local_filesystem_name: local Filesystem name (string),
                remote_filesystem_raw_id: remote Filesystem ID on the device (string),
                remote_filesystem_name: remote Filesystem name (string),
                domain_raw_id: hypermetro domain ID on the storage device (string),
                domain_name: hypermetro domain name (string),
                health_status: health status. valid values: unknown, normal, fault,
                running_status: running status. valid values: normal, synchronizing, invalid, pause, forced_start, to_be_synchronized, unknown, error, creating, deleting,
                recovery_policy: recovery policy. valid values: automatic, manual, unknown,
                link_status: link status. valid values: connected, disconnected, unknown,
                is_primary: whether it is the priority site. valid values: true, false,
                local_storage_id: local storage device ID (string),
                remote_storage_id: remote storage device ID (string),
                speed: sync speed. valid values: low, medium, high, highest, custom,
                bandwidth: custom sync speed (int32, MB/s),
                start_time: last sync start time (string),
                end_time: last sync end time (string),
                local_data_state: local data state. valid values: consistent, inconsistent,
                remote_data_state: remote data state. valid values: consistent, inconsistent,
                local_host_access_state: local host access state. valid values: access_forbidden, read_only, read_write, invalid, blocked, unknown,
                remote_host_access_state: remote host access state. valid values: access_forbidden, read_only, read_write, invalid, blocked, unknown,
                sync_lefttime: remaining sync time (string),
                sync_direction: sync direction. valid values: no_data_synchronization, local_to_remote, remote_to_local,
                sync_progress: sync progress (string),
                activation_state: activation state. valid values: active, passive,
                vstore_pair_id: tenant Pair ID (string),
            }, ...],
        }
    """
    url = "/rest/protection/v1/hypermetro/filesystem-pairs/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    if ids is not None:
        payload['ids'] = ids
    if name is not None:
        payload['name'] = name
    if status is not None:
        payload['status'] = status
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if vstore_pair_id is not None:
        payload['vstore_pair_id'] = vstore_pair_id
    if local_fs_name is not None:
        payload['local_fs_name'] = local_fs_name
    if local_fs_id is not None:
        payload['local_fs_id'] = local_fs_id
    if health_status is not None:
        payload['health_status'] = health_status
    if running_status is not None:
        payload['running_status'] = running_status
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def filesystem_pair_pause(client: DMEAPIClient, fs_pair_ids: list) -> dict:
    """
    Batch pause Filesystem hypermetro Pairs. This API may directly or indirectly affect running services, please operate with caution. 

    Args:
        client: DME API client
        fs_pair_ids: Filesystem hypermetro Pair ID list (Required, List[string], max array members: 100, min array members: 1)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/hypermetro/filesystem-pairs/pause"

    if not fs_pair_ids or len(fs_pair_ids) == 0:
        raise ValueError("fs_pair_ids is a required parameter")

    payload = {
        'fs_pair_ids': fs_pair_ids
    }

    response = client.post(url, body=payload)
    return response


def filesystem_pair_sync(client: DMEAPIClient, fs_pair_ids: list) -> dict:
    """
    Batch sync Filesystem hypermetro Pairs. This API may directly or indirectly affect running services, please operate with caution. 

    Args:
        client: DME API client
        fs_pair_ids: Filesystem hypermetro Pair ID list (Required, List[string])

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/hypermetro/filesystem-pairs/sync"

    if not fs_pair_ids or len(fs_pair_ids) == 0:
        raise ValueError("fs_pair_ids is a required parameter")

    payload = {
        'fs_pair_ids': fs_pair_ids
    }

    response = client.post(url, body=payload)
    return response


def filesystem_pair_delete(client: DMEAPIClient, ids: list,
                            is_local_delete: bool = None,
                            is_online_delete: bool = None) -> dict:
    """
    Batch delete Filesystem hypermetro Pairs. This API may directly or indirectly affect running services, please operate with caution. 

    Args:
        client: DME API client
        ids: hypermetro Pair instance ID list (Required, List[string])
        is_local_delete: whether to delete local configuration info (Optional, boolean, true, false)
        is_online_delete: whether to delete online (Optional, boolean, true, false)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/hypermetro/filesystem-pairs/delete"

    if not ids or len(ids) == 0:
        raise ValueError("ids is a required parameter")

    payload = {
        'ids': ids
    }
    if is_local_delete is not None:
        payload['is_local_delete'] = is_local_delete
    if is_online_delete is not None:
        payload['is_online_delete'] = is_online_delete

    response = client.post(url, body=payload)
    return response


# ============================================================================
# Filesystem snapshot (fs_snapshot) subtopic functions
# ============================================================================


def fs_snapshot_create(client: DMEAPIClient, vstore_pair_id: str,
                        fs_pairs: list) -> dict:
    """
    create Filesystem snapshot. 

    Args:
        client: DME API client
        vstore_pair_id: Filesystem hypermetro tenant Pair ID (Required, string)
        fs_pairs: snapshot parameter list (Required, List)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/filesystem-snapshots"

    if not vstore_pair_id:
        raise ValueError("vstore_pair_id is a required parameter")

    payload = {
        'vstore_pair_id': vstore_pair_id,
        'fs_pairs': fs_pairs
    }

    response = client.post(url, body=payload)
    return response


def fs_snapshot_list(client: DMEAPIClient, fs_pair_id: str = None,
                      name: str = None, status: str = None,
                      local_fs_name: str = None, local_fs_id: str = None,
                      page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch query Filesystem snapshots. 

    Args:
        client: DME API client
        fs_pair_id: hypermetro Pair ID (Optional, string)
        name: snapshot name (Optional, string, supports fuzzy search)
        status: snapshot status (Optional, string)
        local_fs_name: local Filesystem name (Optional, string)
        local_fs_id: local Filesystem ID (Optional, string)
        page_no: pagination page number (Optional, int32)
        page_size: items per page (Optional, int32)

    Returns:
        {
            total: total Filesystem snapshots (int32),
            snapshots: Filesystem snapshot list (List<FsSnapshotInfo>). parameter format: [{
                id: snapshot ID (string),
                name: snapshot name (string),
                status: status (string),
            }, ...],
        }
    """
    url = "/rest/protection/v1/filesystem-snapshots/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    if fs_pair_id is not None:
        payload['fs_pair_id'] = fs_pair_id
    if name is not None:
        payload['name'] = name
    if status is not None:
        payload['status'] = status
    if local_fs_name is not None:
        payload['local_fs_name'] = local_fs_name
    if local_fs_id is not None:
        payload['local_fs_id'] = local_fs_id

    response = client.post(url, body=payload)
    return response


def fs_snapshot_delete(client: DMEAPIClient, ids: list) -> dict:
    """
    Batch delete Filesystem snapshots. 

    Args:
        client: DME API client
        ids: snapshot ID list (Required, List[string])

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/filesystem-snapshots/delete"

    if not ids or len(ids) == 0:
        raise ValueError("ids is a required parameter")

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


# ============================================================================
# Hypermetro tenant Pair (vstore_hypermetro_pair) subtopic functions
# ============================================================================


def vstore_pair_force_start(client: DMEAPIClient, ids: list) -> dict:
    """
    Batch force start hypermetro tenant Pairs. 

    Args:
        client: DME API client
        ids: hypermetro tenant Pair ID list (Required, List[string])

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/vstore-pairs/force-start"

    if not ids or len(ids) == 0:
        raise ValueError("ids is a required parameter")

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def vstore_pair_create(client: DMEAPIClient, local_storage_id: str,
                        remote_storage_id: str, name: str = None,
                        description: str = None,
                        remote_vstore_id: str = None) -> dict:
    """
    create hypermetro tenant Pair. 

    Args:
        client: DME API client
        local_storage_id: local storage device ID (Required, string)
        remote_storage_id: remote storage device ID (Required, string)
        name: tenant Pair name (Optional, string)
        description: description (Optional, string)
        remote_vstore_id: remote tenant ID (Optional, string)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/vstore-pairs"

    if not local_storage_id or not remote_storage_id:
        raise ValueError("local_storage_id and remote_storage_id are required parameters")

    payload = {
        'local_storage_id': local_storage_id,
        'remote_storage_id': remote_storage_id
    }
    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description
    if remote_vstore_id is not None:
        payload['remote_vstore_id'] = remote_vstore_id

    response = client.post(url, body=payload)
    return response


def vstore_pair_list(client: DMEAPIClient, ids: list = None, name: str = None,
                      status: str = None, local_storage_id: str = None,
                      remote_storage_id: str = None,
                      health_status: str = None, running_status: str = None,
                      page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query hypermetro tenant Pair list. 

    Args:
        client: DME API client
        ids: hypermetro tenant Pair ID list (Optional, List[string])
        name: name (Optional, string)
        status: status (Optional, string)
        local_storage_id: local storage device ID (Optional, string)
        remote_storage_id: remote storage device ID (Optional, string)
        health_status: health status (Optional, string)
        running_status: running status (Optional, string)
        page_no: pagination page number (Optional, int32)
        page_size: items per page (Optional, int32)

    Returns:
        {
            total: total hypermetro tenant Pairs (int32),
            vstore_pairs: hypermetro tenant Pair list info (List<VstorePairListItem>). parameter format: [{
                id: hypermetro tenant Pair ID (string),
                raw_id: ID on the storage device (string),
                local_vstore_name: local tenant name (string),
                local_vstore_raw_id: local tenant ID on the storage device (string),
                local_storage_id: local storage device ID (string),
                remote_vstore_name: remote tenant name (string),
                remote_vstore_raw_id: remote tenant ID on the storage device (string),
                remote_storage_id: remote storage device ID (string),
                domain_id: hypermetro domain ID (string),
                domain_name: hypermetro domain name (string),
                running_status: running status. valid values: normal, unsynchronized, invalid, force_start, split,
                config_status: configuration status. valid values: normal, synchronizing, to_be_synchronized,
                health_status: health status. valid values: unknown, normal, fault,
                link_status: link status. valid values: connected, disconnected,
                role: role. valid values: preferred, non_preferred,
                active_status: activation state. valid values: active, passive,
            }, ...],
        }
    """
    url = "/rest/protection/v1/metro/vstore-pairs/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    if ids is not None:
        payload['ids'] = ids
    if name is not None:
        payload['name'] = name
    if status is not None:
        payload['status'] = status
    if local_storage_id is not None:
        payload['local_storage_id'] = local_storage_id
    if remote_storage_id is not None:
        payload['remote_storage_id'] = remote_storage_id
    if health_status is not None:
        payload['health_status'] = health_status
    if running_status is not None:
        payload['running_status'] = running_status

    response = client.post(url, body=payload)
    return response


def vstore_pair_switch(client: DMEAPIClient, ids: list) -> dict:
    """
    Batch primary-secondary switch for hypermetro tenant Pairs. 

    Args:
        client: DME API client
        ids: hypermetro tenant Pair ID list (Required, List[string])

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/vstore-pairs/switch"

    if not ids or len(ids) == 0:
        raise ValueError("ids is a required parameter")

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def vstore_pair_delete(client: DMEAPIClient, ids: list) -> dict:
    """
    Batch delete hypermetro tenant Pairs. 

    Args:
        client: DME API client
        ids: hypermetro tenant Pair ID list (Required, List[string])

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/vstore-pairs/delete"

    if not ids or len(ids) == 0:
        raise ValueError("ids is a required parameter")

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def vstore_pair_modify(client: DMEAPIClient, id: str, name: str = None) -> dict:
    """
    modify specified hypermetro tenant pair. 

    Args:
        client: DME API client
        id: hypermetro tenant Pair ID (Required, string)
        name: name (Optional, string)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/vstore-pairs/{id}"

    if not id:
        raise ValueError("id is a required parameter")

    payload = {}
    if name is not None:
        payload['name'] = name

    response = client.put(url, body=payload, params={"id": id})
    return response


# ============================================================================
# HyperMetro domain (hypermetro_domain) subtopic functions
# ============================================================================


def hypermetro_domain_force_start(client: DMEAPIClient, id: str) -> dict:
    """
    Force start Filesystem hypermetro domain. 

    Args:
        client: DME API client
        id: hypermetro domain ID (Required, string)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/hyper-metro-domains/{id}/force-start"

    if not id:
        raise ValueError("id is a required parameter")

    response = client.post(url, body={}, params={"id": id})
    return response


def hypermetro_domain_switch_site(client: DMEAPIClient, id: str) -> dict:
    """
    Switch priority site for Filesystem hypermetro domain. 

    Args:
        client: DME API client
        id: hypermetro domain ID (Required, string)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/hyper-metro-domains/{id}/switch-priority-site"

    if not id:
        raise ValueError("id is a required parameter")

    response = client.post(url, body={}, params={"id": id})
    return response


def hypermetro_domain_recover(client: DMEAPIClient, id: str) -> dict:
    """
    Recover Filesystem hypermetro domain. 

    Args:
        client: DME API client
        id: hypermetro domain ID (Required, string)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/hyper-metro-domains/{id}/recover"

    if not id:
        raise ValueError("id is a required parameter")

    response = client.post(url, body={}, params={"id": id})
    return response


def hypermetro_domain_split(client: DMEAPIClient, id: str) -> dict:
    """
    Split Filesystem hypermetro domain. 

    Args:
        client: DME API client
        id: hypermetro domain ID (Required, string)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/hyper-metro-domains/{id}/split"

    if not id:
        raise ValueError("id is a required parameter")

    response = client.post(url, body={}, params={"id": id})
    return response


def hypermetro_domain_swap_role(client: DMEAPIClient, id: str) -> dict:
    """
    Swap primary-secondary role for Filesystem hypermetro domain. 

    Args:
        client: DME API client
        id: hypermetro domain ID (Required, string)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/hyper-metro-domains/{id}/swap-role"

    if not id:
        raise ValueError("id is a required parameter")

    response = client.post(url, body={}, params={"id": id})
    return response


# ============================================================================
# HyperMetro Pair (hypermetro_pair) subtopic functions
# ============================================================================


def hypermetro_pair_query_available_luns(client: DMEAPIClient,
                                          source_lun_id: str) -> dict:
    """
    Query target LUNs available for creating hypermetro Pair. 

    Args:
        client: DME API client
        source_lun_id: source LUN ID (Required, string)

    Returns:
        {
            optional_target_luns: optional target LUN list. parameter format: [{
                lun_id: LUN ID (string),
                lun_name: LUN name (string),
                capacity: capacity (integer),
            }, ...],
        }
    """
    url = "/rest/protection/v1/metro/lun-pairs/{source_lun_id}/optional-target-luns"

    if not source_lun_id:
        raise ValueError("source_lun_id is a required parameter")

    response = client.get(url, params={"source_lun_id": source_lun_id})
    return response


# action list, for CLI help
ACTIONS = {
    # group subtopic action
    'group_list': {
        'func': group_list,
        'description': 'Batch query protection groups',
        'params': ['name', 'project_id', 'storage_name', 'storage_id', 'raw_id', 'lun_group_raw_id', 'vstore_id', 'vstore_raw_id', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'group'
    },
    'group_create': {
        'func': group_create,
        'description': 'Create protection group',
        'params': ['name', 'storage_id', 'lun_ids', 'lun_group_id', 'description'],
        'subtopic': 'group'
    },
    'group_modify': {
        'func': group_modify,
        'description': 'Modify protection group',
        'params': ['pg_id', 'name', 'description'],
        'subtopic': 'group'
    },
    'group_delete': {
        'func': group_delete,
        'description': 'Batch delete protection groups',
        'params': ['pg_ids'],
        'subtopic': 'group'
    },
    'group_add_luns': {
        'func': group_add_luns,
        'description': 'Add member LUNs to protection group',
        'params': ['pg_id', 'lun_ids', 'hyper_metro', 'rem_reps'],
        'subtopic': 'group'
    },
    'group_remove_luns': {
        'func': group_remove_luns,
        'description': 'Remove member LUNs from protection group',
        'params': ['pg_id', 'lun_ids', 'is_delay'],
        'subtopic': 'group'
    },
    # hypermetro_group subtopic action
    'hypermetro_group_list': {
        'func': hypermetro_group_list,
        'description': 'Batch query hypermetro consistency groups',
        'params': ['page_no', 'page_size', 'name', 'raw_id', 'protect_group_id', 'storage_id', 'storage_name', 'local_vstore_id', 'local_vstore_raw_id', 'remote_vstore_id', 'remote_vstore_raw_id'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_create': {
        'func': hypermetro_group_create,
        'description': 'Create hypermetro consistency group',
        'params': ['domain_id', 'name', 'local_storage_id', 'local_pg_id', 'description', 'create_mode', 'remote_vstore_id', 'remote_storage_pool_id', 'lun_ids', 'remote_resource_name_rule'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_modify': {
        'func': hypermetro_group_modify,
        'description': 'Modify hypermetro consistency group',
        'params': ['group_id', 'name', 'description', 'recovery_policy', 'service_assurance_policy', 'speed', 'bandwidth', 'isolation_threshold_time'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_delete': {
        'func': hypermetro_group_delete,
        'description': 'Batch delete hypermetro consistency groups',
        'params': ['ids', 'is_self_adapt', 'delete_mode'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_add_pairs': {
        'func': hypermetro_group_add_pairs,
        'description': 'Add member Pairs to hypermetro consistency group',
        'params': ['group_id', 'pair_ids', 'is_self_adapt'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_remove_pairs': {
        'func': hypermetro_group_remove_pairs,
        'description': 'Remove member Pairs from hypermetro consistency group',
        'params': ['group_id', 'pair_ids'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_pause': {
        'func': hypermetro_group_pause,
        'description': 'Pause hypermetro consistency group',
        'params': ['ids', 'priority_station_type'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_force_startup': {
        'func': hypermetro_group_force_startup,
        'description': 'Force start hypermetro consistency group',
        'params': ['ids', 'priority_station_type'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_switch_priority': {
        'func': hypermetro_group_switch_priority,
        'description': 'Switch priority site for hypermetro consistency group',
        'params': ['ids'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_sync': {
        'func': hypermetro_group_sync,
        'description': 'Sync hypermetro consistency group',
        'params': ['ids'],
        'subtopic': 'hypermetro_group'
    },
    # hypermetro_pair subtopic action
    'hypermetro_pair_list': {
        'func': hypermetro_pair_list,
        'description': 'Batch query LUN hypermetro Pairs',
        'params': ['page_no', 'page_size', 'group_id', 'group_name', 'group_raw_id', 'pair_raw_id', 'local_storage_id', 'local_storage_name', 'local_vstore_id', 'local_vstore_raw_id', 'local_volume_name', 'local_host_access_state', 'remote_vstore_id', 'remote_vstore_raw_id', 'remote_volume_name'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_create': {
        'func': hypermetro_pair_create,
        'description': 'Create hypermetro Pair',
        'params': ['create_mode', 'lun_pairs', 'lun_ids', 'remote_storage_pool_id', 'remote_vstore_id', 'remote_resource_name_rule', 'name_prefix', 'name_suffix', 'local_storage_id', 'domain_id', 'speed', 'bandwidth', 'service_assurance_policy', 'isolation_threshold_time', 'recovery_policy'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_modify': {
        'func': hypermetro_pair_modify,
        'description': 'Modify hypermetro Pair',
        'params': ['pair_id', 'speed', 'bandwidth', 'recovery_policy', 'service_assurance_policy', 'isolation_threshold_time'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_delete': {
        'func': hypermetro_pair_delete,
        'description': 'Batch delete hypermetro Pairs',
        'params': ['ids', 'delete_mode', 'is_lun_service_interrupt'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_sync': {
        'func': hypermetro_pair_sync,
        'description': 'Sync hypermetro Pairs',
        'params': ['ids'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_pause': {
        'func': hypermetro_pair_pause,
        'description': 'Pause hypermetro Pair',
        'params': ['ids', 'priority_station_type'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_force_startup': {
        'func': hypermetro_pair_force_startup,
        'description': 'Force start hypermetro Pair',
        'params': ['ids', 'priority_station_type'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_switch_priority': {
        'func': hypermetro_pair_switch_priority,
        'description': 'Switch priority site for hypermetro Pair',
        'params': ['ids'],
        'subtopic': 'hypermetro_pair'
    },
    # hypermetro_domain subtopic action
    'hypermetro_domain_list': {
        'func': hypermetro_domain_list,
        'description': 'Batch query hypermetro domains',
        'params': ['storage_id', 'types'],
        'subtopic': 'hypermetro_domain'
    },
    # replication_group subtopic action
    'replication_group_create': {
        'func': replication_group_create,
        'description': 'Create remote replication consistency group',
        'params': ['cg_name', 'remote_storage_id', 'local_pg_id', 'description', 'remote_lun_group_id', 'local_storage_id', 'create_mode', 'existed_pair_ids', 'lun_pairs', 'lun_ids', 'remote_storage_pool_id', 'remote_vstore_id', 'remote_resource_name_rule', 'name_prefix', 'name_suffix'],
        'subtopic': 'replication_group'
    },
    'replication_group_list': {
        'func': replication_group_list,
        'description': 'Batch query replication consistency groups',
        'params': ['page_no', 'page_size', 'protect_group_id', 'name', 'raw_id', 'running_status', 'health_status', 'storage_name', 'storage_id', 'replication_mode'],
        'subtopic': 'replication_group'
    },
    'replication_group_modify': {
        'func': replication_group_modify,
        'description': 'Modify remote replication consistency group',
        'params': ['replication_group_id', 'name', 'description', 'speed', 'bandwidth', 'recovery_policy', 'enable_compress', 'sync_type', 'timing_value_in_sec', 'sync_schedule', 'rep_io_timeout', 'sync_snap_policy', 'user_snap_retention_num', 'switch_to_async'],
        'subtopic': 'replication_group'
    },
    'replication_group_delete': {
        'func': replication_group_delete,
        'description': 'Batch delete remote replication consistency groups',
        'params': ['ids', 'is_self_adapt', 'delete_mode'],
        'subtopic': 'replication_group'
    },
    'replication_group_add_pairs': {
        'func': replication_group_add_pairs,
        'description': 'Add member Pairs to remote replication consistency group',
        'params': ['group_id', 'pair_ids'],
        'subtopic': 'replication_group'
    },
    'replication_group_remove_pairs': {
        'func': replication_group_remove_pairs,
        'description': 'Remove member Pairs from remote replication consistency group',
        'params': ['group_id', 'pair_ids'],
        'subtopic': 'replication_group'
    },
    'replication_group_sync': {
        'func': replication_group_sync,
        'description': 'Batch sync remote replication consistency groups',
        'params': ['ids'],
        'subtopic': 'replication_group'
    },
    'replication_group_split': {
        'func': replication_group_split,
        'description': 'Batch split remote replication consistency groups',
        'params': ['ids'],
        'subtopic': 'replication_group'
    },
    'replication_group_switch': {
        'func': replication_group_switch,
        'description': 'Batch primary-secondary switch for remote replication consistency groups',
        'params': ['ids'],
        'subtopic': 'replication_group'
    },
    'replication_group_switch_write_protection': {
        'func': replication_group_switch_write_protection,
        'description': 'Switch write protection state for remote replication consistency group secondary resource',
        'params': ['id', 'operation_type'],
        'subtopic': 'replication_group'
    },
    # replication_pair subtopic action
    'replication_pair_list': {
        'func': replication_pair_list,
        'description': 'Batch query replication Pairs',
        'params': ['page_no', 'page_size', 'group_id', 'group_name', 'pair_raw_id', 'local_storage_id', 'local_storage_name', 'local_vstore_id', 'local_vstore_raw_id', 'local_volume_name', 'remote_vstore_id', 'remote_vstore_raw_id', 'remote_volume_name'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_create': {
        'func': replication_pair_create,
        'description': 'Create remote replication Pair',
        'params': ['local_storage_id', 'local_lun_id', 'remote_storage_id', 'remote_storage_pool_id', 'remote_vstore_id', 'remote_resource_name_rule', 'name_prefix', 'name_suffix', 'speed', 'bandwidth', 'recovery_policy', 'sync_type', 'timing_value_in_sec', 'sync_schedule', 'rep_io_timeout', 'sync_snap_policy', 'user_snap_retention_num', 'switch_to_async', 'enable_compress'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_modify': {
        'func': replication_pair_modify,
        'description': 'Modify replication Pair',
        'params': ['pair_id', 'speed', 'bandwidth', 'recovery_policy', 'enable_compress', 'sync_type', 'timing_value_in_sec', 'sync_schedule', 'rep_io_timeout', 'sync_snap_policy', 'user_snap_retention_num', 'switch_to_async'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_delete': {
        'func': replication_pair_delete,
        'description': 'Batch delete remote replication Pairs',
        'params': ['ids', 'delete_mode'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_sync': {
        'func': replication_pair_sync,
        'description': 'Batch sync remote replication Pairs',
        'params': ['ids'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_split': {
        'func': replication_pair_split,
        'description': 'Batch split remote replication Pairs',
        'params': ['ids'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_switch': {
        'func': replication_pair_switch,
        'description': 'Batch primary-secondary switch for remote replication Pairs',
        'params': ['ids'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_switch_write_protection': {
        'func': replication_pair_switch_write_protection,
        'description': 'Switch protection state for remote replication Pair secondary resource',
        'params': ['id', 'operation_type'],
        'subtopic': 'replication_pair'
    },
    # device subtopic action
    'device_pair_list': {
        'func': device_pair_list,
        'description': 'Query device Pairs',
        'params': ['storage_id'],
        'subtopic': 'device_pair'
    },
    'replication_link_list': {
        'func': replication_link_list,
        'description': 'Query replication links',
        'params': ['local_storage_id', 'page_no', 'page_size', 'health_status', 'running_status', 'link_type'],
        'subtopic': 'replication_link'
    },
    # snapshot subtopic action
    'snapshot_list': {
        'func': snapshot_list,
        'description': 'Batch query LUN snapshots',
        'params': ['snapshot_ids', 'storage_id', 'raw_id', 'name', 'health_status', 'running_status', 'source_lun_name', 'parent_name', 'activated_time_from', 'activated_time_to', 'page_no', 'page_size'],
        'subtopic': 'snapshot'
    },
    'snapshot_create': {
        'func': snapshot_create,
        'description': 'Batch create LUN snapshots',
        'params': ['snapshots_info', 'is_consist_activate'],
        'subtopic': 'snapshot'
    },
    'snapshot_rollback': {
        'func': snapshot_rollback,
        'description': 'Batch rollback LUN snapshots',
        'params': ['rollback_speed', 'rollback_snapshots'],
        'subtopic': 'snapshot'
    },
    'snapshot_delete': {
        'func': snapshot_delete,
        'description': 'Batch delete LUN snapshots',
        'params': ['snapshot_ids', 'is_delete_target_lun', 'is_auto_deactivate'],
        'subtopic': 'snapshot'
    },
    # snapshot_group subtopic action
    'snapshot_group_create': {
        'func': snapshot_group_create,
        'description': 'Create snapshot consistency group',
        'params': ['name', 'protect_group_id', 'description', 'creation_mode'],
        'subtopic': 'snapshot_group'
    },
    'snapshot_group_delete': {
        'func': snapshot_group_delete,
        'description': 'Batch delete snapshot consistency groups',
        'params': ['snapshot_cg_ids', 'is_delete_target_lun'],
        'subtopic': 'snapshot_group'
    },
    'snapshot_group_activate': {
        'func': snapshot_group_activate,
        'description': 'Activate snapshot consistency group',
        'params': ['snapshot_cg_id', 'object_type', 'snapshot_create_mode', 'name_rule', 'name_prefix', 'name_suffix', 'target_snapshot_objects'],
        'subtopic': 'snapshot_group'
    },
    'snapshot_group_deactivate': {
        'func': snapshot_group_deactivate,
        'description': 'Batch deactivate snapshot consistency groups',
        'params': ['snapshot_cg_ids'],
        'subtopic': 'snapshot_group'
    },
    'snapshot_group_rollback': {
        'func': snapshot_group_rollback,
        'description': 'Rollback snapshot consistency group',
        'params': ['snapshot_cg_id', 'rollback_speed', 'snapshot_create_mode', 'name_rule', 'name_prefix', 'name_suffix', 'target_snapshot_objects'],
        'subtopic': 'snapshot_group'
    },
    # clone_group subtopic action
    'clone_group_create': {
        'func': clone_group_create,
        'description': 'Create clone consistency group',
        'params': ['name', 'protect_group_id', 'create_mode', 'description', 'name_rule', 'name_prefix', 'name_suffix', 'copy_rate', 'is_sync', 'clone_pairs'],
        'subtopic': 'clone_group'
    },
    'clone_group_sync': {
        'func': clone_group_sync,
        'description': 'Sync clone consistency group',
        'params': ['clone_cg_id', 'create_mode', 'name_rule', 'name_prefix', 'name_suffix', 'clone_pairs'],
        'subtopic': 'clone_group'
    },
    'clone_group_delete': {
        'func': clone_group_delete,
        'description': 'Batch delete clone consistency groups',
        'params': ['ids', 'is_delete_dst_lun', 'is_recycle_dst_lun_data'],
        'subtopic': 'clone_group'
    },
    # fs_hypermetro_pair subtopic action
    'filesystem_pair_create': {
        'func': filesystem_pair_create,
        'description': 'Create Filesystem hypermetro Pair',
        'params': ['vstore_pair_id', 'create_mode', 'fs_pairs', 'speed', 'bandwidth', 'service_assurance_policy', 'isolation_threshold_time'],
        'subtopic': 'fs_hypermetro_pair'
    },
    'filesystem_pair_list': {
        'func': filesystem_pair_list,
        'description': 'Query Filesystem hypermetro Pair list',
        'params': ['ids', 'name', 'status', 'storage_id', 'vstore_pair_id', 'local_fs_name', 'local_fs_id', 'health_status', 'running_status', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'fs_hypermetro_pair'
    },
    'filesystem_pair_pause': {
        'func': filesystem_pair_pause,
        'description': 'Batch pause Filesystem hypermetro Pairs',
        'params': ['fs_pair_ids'],
        'subtopic': 'fs_hypermetro_pair'
    },
    'filesystem_pair_sync': {
        'func': filesystem_pair_sync,
        'description': 'Batch sync Filesystem hypermetro Pairs',
        'params': ['fs_pair_ids'],
        'subtopic': 'fs_hypermetro_pair'
    },
    'filesystem_pair_delete': {
        'func': filesystem_pair_delete,
        'description': 'Batch delete Filesystem hypermetro Pairs',
        'params': ['ids', 'is_local_delete', 'is_online_delete'],
        'subtopic': 'fs_hypermetro_pair'
    },
    # fs_snapshot subtopic action
    'fs_snapshot_create': {
        'func': fs_snapshot_create,
        'description': 'Create Filesystem snapshot',
        'params': ['vstore_pair_id', 'fs_pairs'],
        'subtopic': 'fs_snapshot'
    },
    'fs_snapshot_list': {
        'func': fs_snapshot_list,
        'description': 'Batch query Filesystem snapshots',
        'params': ['fs_pair_id', 'name', 'status', 'local_fs_name', 'local_fs_id', 'page_no', 'page_size'],
        'subtopic': 'fs_snapshot'
    },
    'fs_snapshot_delete': {
        'func': fs_snapshot_delete,
        'description': 'Batch delete Filesystem snapshots',
        'params': ['ids'],
        'subtopic': 'fs_snapshot'
    },
    # vstore_hypermetro_pair subtopic action
    'vstore_pair_force_start': {
        'func': vstore_pair_force_start,
        'description': 'Batch force start hypermetro tenant Pairs',
        'params': ['ids'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    'vstore_pair_create': {
        'func': vstore_pair_create,
        'description': 'Create hypermetro tenant Pair',
        'params': ['local_storage_id', 'remote_storage_id', 'name', 'description', 'remote_vstore_id'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    'vstore_pair_list': {
        'func': vstore_pair_list,
        'description': 'Query hypermetro tenant Pair list',
        'params': ['ids', 'name', 'status', 'local_storage_id', 'remote_storage_id', 'health_status', 'running_status', 'page_no', 'page_size'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    'vstore_pair_switch': {
        'func': vstore_pair_switch,
        'description': 'Batch primary-secondary switch hypermetro tenant Pairs',
        'params': ['ids'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    'vstore_pair_delete': {
        'func': vstore_pair_delete,
        'description': 'Batch delete hypermetro tenant Pairs',
        'params': ['ids'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    'vstore_pair_modify': {
        'func': vstore_pair_modify,
        'description': 'Modify specified hypermetro tenant pair',
        'params': ['id', 'name'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    # hypermetro_domain subtopic action
    'hypermetro_domain_force_start': {
        'func': hypermetro_domain_force_start,
        'description': 'Force start Filesystem hypermetro domain',
        'params': ['id'],
        'subtopic': 'hypermetro_domain'
    },
    'hypermetro_domain_switch_site': {
        'func': hypermetro_domain_switch_site,
        'description': 'Switch priority site for Filesystem hypermetro domain',
        'params': ['id'],
        'subtopic': 'hypermetro_domain'
    },
    'hypermetro_domain_recover': {
        'func': hypermetro_domain_recover,
        'description': 'Recover Filesystem hypermetro domain',
        'params': ['id'],
        'subtopic': 'hypermetro_domain'
    },
    'hypermetro_domain_split': {
        'func': hypermetro_domain_split,
        'description': 'Split Filesystem hypermetro domain',
        'params': ['id'],
        'subtopic': 'hypermetro_domain'
    },
    'hypermetro_domain_swap_role': {
        'func': hypermetro_domain_swap_role,
        'description': 'Swap primary-secondary role for Filesystem hypermetro domain',
        'params': ['id'],
        'subtopic': 'hypermetro_domain'
    },
    # hypermetro_pair subtopic action
    'query_available_luns': {
        'func': hypermetro_pair_query_available_luns,
        'description': 'Query available target LUNs for creating hypermetro Pair',
        'params': ['source_lun_id'],
        'subtopic': 'hypermetro_pair'
    },
}
