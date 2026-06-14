"""
Protection (snapshot/active-active/replication) operations
"""

import sys
import os

from pydme.client import DMEAPIClient


# ============================================================================
# group Subtopic - Protection groupoperations
# ============================================================================

def group_list(client: DMEAPIClient, name: str = None, project_id: str = None,
               storage_name: str = None, storage_id: str = None,
               raw_id: str = None, lun_group_raw_id: str = None,
               vstore_id: str = None, vstore_raw_id: str = None,
               sort_key: str = None, sort_dir: str = None,
               page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch query protection group

    Args:
        client: DME API client
        name: Protection group name, supports fuzzy search
        project_id: Project group ID, supports conditional filtering
        storage_name: Storage device name, supports fuzzy search
        storage_id: Storage device ID, supports conditional filtering
        raw_id: Protection group ID on device, supports exact search,  supports sorting
        lun_group_raw_id: LUN group ID on device, supports conditional filtering
        vstore_id: Tenant ID, mutually exclusive with vstore_raw_id
        vstore_raw_id: Tenanton the device ID, this parameter and vstore_id mutually exclusive
        sort_key: Sort field, Options: sort_id
        sort_dir: Sort direction. Options: asc, desc (default desc)
        page_no: Page number, default 1
        page_size: Items per page, default 20

    Returns:
        {
            total: Protection groupTotal count (integer),
            protection_groups: Protection group list (List<ProtectionGroupInfor>). 参数格式如下：[{
                id: Protection group ID (string),
                name: Protection group name (string),
                status:  status (string),
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
    create Protection group

    Args:
        client: DME API client
        name: Protection group name
        storage_id: Storage device ID
        lun_ids: LUN ID list,  conditionally required,  required when creating protection group based on LUN
        lun_group_id: LUN group ID,  conditionally required,  required when creating protection group based on LUN group
        description: Protection group description

    Returns:
        {
            id: Protection group ID (string),
            task_id: Task ID (string, 1~64 characters),
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
    modify Protection group

    Args:
        client: DME API client
        pg_id: Protection group ID
        name: Protection group name
        description: Protection group description

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Batch delete protection group

    >![](public_sys-resources/icon-notice.gif) **: **
    This API may directly or indirectly affect production services, causing service interruption or data loss. Proceed with caution.

    Args:
        client: DME API client
        pg_ids: Protection group ID list

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Add member LUN to protection group

    Add member LUN to the specified protection group. 

    Args:
        client: DME API client
        pg_id: Protection group ID
        lun_ids: to add to protection group LUN ID list (Optional) , max array members 100, mutually exclusive with hyper_metro and rem_reps lun_pairs parameter; Protection group does not existactive-active, replication, ring 3DC parameter effective when feature exists
        hyper_metro: request parameter for adding LUN to active-active protection group (Optional) , mutually exclusive with lun_ids parameter; Protection group has active-active feature exists.  format: {
                        is_delay: Deferred execution (Required) , true/false. When deferred execution is true, if consistency group or new pair is syncing,  will wait for sync to complete before, new pair joins consistency group; when deferred execution is false: if consistency group or new pair is syncing,  directly pause consistency groupand new pair, join new pair to consistency group, then sync consistency group
                        create_mode: Active-active pair creation mode (Required) , Options: auto, manual
                        remote_storage_pool_id: Remote storage pool ID (Optional) , 1~32  characters, regex ^[a-fA-F0-9]+$; Effective when active-active pair creation mode is auto
                        remote_lun_name_rule: LUN naming policy (Optional) , Options: same_as_local, prefix_and_suffix, prefix_and_num, prefix_and_suffix ( prefix+local Resource name+ suffix) , prefix_and_num ( prefix + auto number) ; effective in auto-create mode
                        name_prefix: Remote LUN name prefix (Optional) , 0~251  characters; auto-create mode and naming rule is prefix_and_suffix or prefix_and_numefix_and_num effective when; prefix_and_suffix max prefix length: 32 bytes, prefix_and_num max prefix length 251  byte
                        name_suffix: Remote LUN name suffix (Optional) , 0~16  characters; auto-create mode and naming rule is prefix_and_suffix effective when
                        lun_pairs:  manually configured active-active pair infor list (Optional) , max array members 100; effective when create_mode is manual.  format: [{
                                local_lun_id: Local LUN ID (Required) , 1~32  characters, regex ^[a-fA-F0-9]+$; Local device, peer device is remote
                                remote_lun_id: Remote LUN ID (Required) , 1~32  characters, regex ^[a-fA-F0-9]+$
                        },...]
        }
        rem_reps: request parameter for adding LUN to replication-capable protection group (Optional) , max array members 2, mutually exclusive with lun_ids parameter; Protection group has replication feature exists.  format: [{
                        is_delay: Deferred execution (Optional) , default true. When deferred execution is true, if new pair is syncing,  will wait for sync to complete before, new pair joins consistency group; when deferred execution is false:  directlySplitConsistency groupand new pair, join new pair to consistency group, then sync consistency group
                        create_mode: Remote replication pair creation mode (Required) , Options: auto, manual
                        remote_storage_id: Remote storage device ID (Required) , 1~64  characters, regex ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$
                        remote_storage_pool_id: Remote storage pool ID (Optional) , 1~32  characters, regex ^[a-fA-F0-9]+$; Replication pair creation mode is auto. Effective when
                        remote_lun_name_rule: LUN naming policy (Optional) , Options: same_as_local, prefix_and_suffix, prefix_and_num, prefix_and_suffix ( prefix+local Resource name+ suffix) , prefix_and_num ( prefix + auto number) ; effective in auto-create mode
                        name_prefix: Remote LUN name prefix (Optional) , 0~251  characters; auto-create mode and naming rule is prefix_and_suffix or prefix_and_numefix_and_num effective when; prefix_and_suffix max prefix length: 32 bytes, prefix_and_num max prefix length 251  byte
                        name_suffix: Remote LUN name suffix (Optional) , 0~16  characters; auto-create mode and naming rule is prefix_and_suffix effective when
                        lun_pairs:  manually configured remote replication pair infor list (Optional) , max array members 100; effective when create_mode is manual.  format: [{
                                local_lun_id: Local LUN ID (Required) , 1~32  characters, regex ^[a-fA-F0-9]+$; Local device, peer device is remote
                                remote_lun_id: Remote LUN ID (Required) , 1~32  characters, regex ^[a-fA-F0-9]+$
                        },...]
        },...]

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Remove LUN members from protection group

    RemoveProtection groupmembers in LUN. 

    Args:
        client: DME API client
        pg_id: Protection group ID
        lun_ids: to be removedProtection group member LUN ID list
        is_delay: Deferred execution. In remote replication, sync + async ring 3DC case, this parameter is N/A

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
# hypermetro_group Subtopic - Active-active consistency groupoperations
# ============================================================================

def hypermetro_group_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 20,
                          name: str = None, raw_id: str = None,
                          protect_group_id: str = None, storage_id: str = None,
                          storage_name: str = None, local_vstore_id: str = None,
                          local_vstore_raw_id: str = None, remote_vstore_id: str = None,
                          remote_vstore_raw_id: str = None) -> dict:
    """
    Batch query active-active consistency group

    Args:
        client: DME API client
        page_no: Page number, default 1
        page_size: Items per page, default 20
        name: Active-active consistency group name, supports fuzzy match
        raw_id: Active-active consistency groupon the device ID
        protect_group_id: Protection group ID
        storage_id: Storage device ID, Supports local storage ID  filter
        storage_name: Storage device name, Supports local storage namefuzzy match
        local_vstore_id: local tenant ID, this parameter and local_vstore_raw_id mutually exclusive
        local_vstore_raw_id: local tenanton the device ID, this parameter and local_vstore_id mutually exclusive
        remote_vstore_id: remote tenant ID, this parameter and remote_vstore_raw_id mutually exclusive
        remote_vstore_raw_id: remote tenanton the device ID, this parameter and remote_vstore_id mutually exclusive

    Returns:
        Active-active consistency group list
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
    create Active-active consistency group

    Args:
        client: DME API client
        domain_id: Active-active domain ID
        name: Active-active consistency group name
        local_storage_id: local  device ID
        local_pg_id: Local protection group ID,  conditionally required for OceanStor Dorado V6+, required for OceanStor V6
        description: Description
        create_mode: Active-active pair creation mode, Options: auto , manual 
        remote_vstore_id: Remote device tenant ID,  conditionally required when create_mode is auto for OceanStor Dorado 6.1.3 version and above
        remote_storage_pool_id: Remote storage pool ID,  conditionally required when create_mode is auto
        lun_ids: LUN ID list,  conditionally optional: when create_mode is auto
        remote_resource_name_rule: Remote resource naming policy, Options: same_as_local, prefix_and_suffix, prefix_and_num

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    modify Active-active consistency group

    Args:
        client: DME API client
        group_id: Active-active consistency group ID
        name: Active-active consistency group name
        description: Description
        recovery_policy: Active-active pair recovery policy, Options: automatic , manual 
        service_assurance_policy: Service assurance policy, Options: data_reliability_preferred (data reliability first)t) , service_continuity_preferred (Business continuity priority) 
        speed: Sync rate. Options: low, medium, high, highest, custom
        bandwidth: Custom sync rate (MB/s) , required when speed is custom
        isolation_threshold_time:  Isolation threshold (ms) , required when service_assurance_policy is service_continuity_preferred

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Batch delete active-active consistency group

    Args:
        client: DME API client
        ids: Active-active consistency group ID  list
        delete_mode: Delete mode, Options: preferred_only , non_preferred_only , dual_endse both sites) 
        is_self_adapt: supportsAdaptive member deletion Pair, default false

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Active-active consistency group - add member pair

    Args:
        client: DME API client
        group_id: Active-active consistency group ID
        pair_ids: Active-active Pair ID  list
        is_self_adapt: Adaptive modificationActive-active Pair Running status

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Active-active consistency group - remove member pair

    Args:
        client: DME API client
        group_id: Active-active consistency group ID
        pair_ids: Active-active Pair ID  list

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
     pause active-active consistency group

    Args:
        client: DME API client
        ids: Active-active consistency group ID  list
        priority_station_type: Site type, Options: preferred , non_preferred 

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    force start active-active consistency group

    Args:
        client: DME API client
        ids: Active-active consistency group ID  list
        priority_station_type: Site type, Options: preferred , non_preferred 

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Active-active consistency grouppreferred site switch

    Args:
        client: DME API client
        ids: Active-active consistency group ID  list

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/groups/switch-priority-site"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


# ============================================================================
# hypermetro_pair Subtopic - Active-active Pair operations
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
    Batch query LUN Active-active Pair

    Args:
        client: DME API client
        page_no: Page number, default 1
        page_size: Items per page, default 20
        group_id: Active-active consistency group ID
        group_name: Active-active consistency group name, supports fuzzy match
        group_raw_id: Active-active consistency groupon the storage device ID
        pair_raw_id: Active-active Pair on the storage device ID
        local_storage_id: local Storage device ID
        local_storage_name: local Storage device name, supports fuzzy match
        local_vstore_id: local tenant ID, this parameter and local_vstore_raw_id mutually exclusive
        local_vstore_raw_id: local tenanton the device ID, this parameter and local_vstore_id mutually exclusive
        local_volume_name: local  LUN  name, supports fuzzy match
        local_host_access_state: Local resource host access status. Options: access_forbidden, read_only, read_write
        remote_vstore_id: remote tenant ID, this parameter and remote_vstore_raw_id mutually exclusive
        remote_vstore_raw_id: remote tenanton the device ID, this parameter and remote_vstore_id mutually exclusive
        remote_volume_name: remote  LUN  name, supports fuzzy match

    Returns:
        Active-active Pair  list
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


def hypermetro_pair_create(client: DMEAPIClient, create_mode: str, local_storage_id: str,
                           domain_id: str, lun_ids: list = None, lun_pairs: list = None,
                           remote_storage_pool_id: str = None, remote_vstore_id: str = None,
                           remote_resource_name_rule: str = None, name_prefix: str = None,
                           name_suffix: str = None, speed: str = None, bandwidth: int = None,
                           service_assurance_policy: str = None, isolation_threshold_time: int = None,
                           recovery_policy: str = None) -> dict:
    """
    create Active-active Pair

    Args:
        client: DME API client
        create_mode: Active-active pair creation mode, Options: auto , manual 
        local_storage_id: Create active-active pair storage device ID
        domain_id: Active-active domain ID
        lun_ids: In auto-create mode, Source LUN ID list
        lun_pairs: In manual create mode, Active-active pair source and target LUN ID list
        remote_storage_pool_id: Remote storage pool ID, effective in auto-create mode
        remote_vstore_id: Remote device tenant ID, effective in auto-create mode
        remote_resource_name_rule: LUN naming policy, Options: same_as_local, prefix_and_suffix, prefix_and_num
        name_prefix: Remote LUN name prefix
        name_suffix: Remote LUN name suffix
        speed: Sync rate. Options: low, medium, high, highest, custom
        bandwidth: Custom sync rate (MB/s) , required when speed is custom
        service_assurance_policy: Service assurance policy, Options: data_reliability_preferred, service_continuity_preferred
        isolation_threshold_time:  Isolation threshold (ms) , required when service_assurance_policy is service_continuity_preferred
        recovery_policy: Recovery policy, Options: automatic, manual

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    modify Active-active Pair

    Args:
        client: DME API client
        pair_id: Active-active Pair instance ID
        speed: Active-active Pair Sync rate. Options: low, medium, high, highest, custom
        bandwidth:  custom rate (MB/s) , required when speed is custom
        recovery_policy: Recovery policy, Options: automatic, manual
        service_assurance_policy: Service assurance policy, Options: data_reliability_preferred, service_continuity_preferred
        isolation_threshold_time:  Isolation threshold (ms) , required when service_assurance_policy is service_continuity_preferred

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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


def hypermetro_pair_delete(client: DMEAPIClient, ids: list, delete_mode: str = None,
                            is_lun_service_interrupt: bool = None) -> dict:
    """
    Batch delete active-active Pair

    >![](public_sys-resources/icon-notice.gif) **: **
    This API may directly or indirectly affect production services, causing service interruption or data loss. Proceed with caution.

    Args:
        client: DME API client
        ids: Active-active Pair instance ID  list
        delete_mode: Delete mode, Options: preferred_only, non_preferred_only, dual_ends
        is_lun_service_interrupt:  Whether to interrupt LUN service, effective when delete_mode is preferred_only or non_preferred_only

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/lun-pairs/delete"

    payload = {
        'ids': ids
    }

    if delete_mode is not None:
        payload['delete_mode'] = delete_mode
    if is_lun_service_interrupt is not None:
        payload['is_lun_service_interrupt'] = is_lun_service_interrupt

    response = client.post(url, body=payload)
    return response


def hypermetro_pair_sync(client: DMEAPIClient, ids: list) -> dict:
    """
    Sync active-active pair

    Args:
        client: DME API client
        ids: Active-active Pair ID  list

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
     pause active-active pair

    Args:
        client: DME API client
        ids: Active-active Pair ID  list
        priority_station_type: Site type, Options: preferred, non_preferred

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    force start active-active pair

    Args:
        client: DME API client
        ids: Active-active Pair ID  list
        priority_station_type: Site type, Options: preferred, non_preferred

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Active-active Pair preferred site switch

    Args:
        client: DME API client
        ids: Active-active Pair ID  list

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/lun-pairs/switch-priority-site"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


# ============================================================================
# hypermetro_domain Subtopic - Active-active domainoperations
# ============================================================================

def hypermetro_domain_list(client: DMEAPIClient, storage_id: str = None,
                            types: list = None) -> dict:
    """
    Batch query active-active domain

    Args:
        client: DME API client
        storage_id:  device ID
        types: Active-active domain type list

    Returns:
        Active-active domain list
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
# replication_pair Subtopic -  replication Pair operations
# ============================================================================

def replication_pair_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 20,
                          group_id: str = None, group_name: str = None,
                          pair_raw_id: str = None, local_storage_id: str = None,
                          local_storage_name: str = None, local_vstore_id: str = None,
                          local_vstore_raw_id: str = None, local_volume_name: str = None,
                          remote_vstore_id: str = None, remote_vstore_raw_id: str = None,
                          remote_volume_name: str = None) -> dict:
    """
    Batch query replication Pair

    Args:
        client: DME API client
        page_no: Page number, default 1
        page_size: Items per page, default 20
        group_id:  replicationConsistency group ID
        group_name:  replicationConsistency group name, supports fuzzy match
        pair_raw_id:  replication Pair on the storage device ID
        local_storage_id: local Storage device ID
        local_storage_name: local Storage device name, supports fuzzy match
        local_vstore_id: local tenant ID, this parameter and local_vstore_raw_id mutually exclusive
        local_vstore_raw_id: local tenanton the device ID, this parameter and local_vstore_id mutually exclusive
        local_volume_name: local  LUN  name, supports fuzzy match
        remote_vstore_id: remote tenant ID, this parameter and remote_vstore_raw_id mutually exclusive
        remote_vstore_raw_id: remote tenanton the device ID, this parameter and remote_vstore_id mutually exclusive
        remote_volume_name: remote  LUN  name, supports fuzzy match

    Returns:
         replication Pair  list
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
    Create remote replication Pair

    Args:
        client: DME API client
        local_storage_id: local Storage device ID
        local_lun_id: local  LUN ID
        remote_storage_id: Remote storage device ID
        remote_storage_pool_id: Remote storage pool ID
        remote_vstore_id: Remote device tenant ID
        remote_resource_name_rule: Remote resource naming policy, Options: same_as_local, prefix_and_suffix, prefix_and_num
        name_prefix: remote Resource name prefix
        name_suffix: remote Resource name suffix
        speed: Sync rate. Options: low, medium, high, highest, custom
        bandwidth: Custom sync rate (MB/s) , required when speed is custom
        recovery_policy: Recovery policy, Options: automatic, manual
        sync_type: Sync type, Options: manual, wait_after_sync_begins, wait_after_sync_ends, specified_time_policy
        timing_value_in_sec: Timer duration (second(s)) , required when sync_type is wait_after_sync_begins or wait_after_sync_ends
        sync_schedule: Timer rule, required when sync_type is specified_time_policy
        rep_io_timeout: remote  IO timeout (second(s)) , when replication mode isSync modeeffective when
        sync_snap_policy: User snapshotSync policy, Options: not_sync_snap, same_as_source, user_snap_retention_num, snap_tag_based
        user_snap_retention_num: Slave user snapshot retentioncount
        switch_to_async: Auto-convert sync to async remote replication switch
        enable_compress: Link compression, when replication mode isin async modeRequired

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    modify  replication Pair

    Args:
        client: DME API client
        pair_id:  replication Pair instance ID
        speed: Sync rate. Options: low, medium, high, highest, custom
        bandwidth: Custom sync rate (MB/s) , required when speed is custom
        recovery_policy: Recovery policy, Options: automatic, manual
        enable_compress: Link compression, when replication mode isin async modeRequired
        sync_type: Sync type, Options: manual, wait_after_sync_begins, wait_after_sync_ends, specified_time_policy
        timing_value_in_sec: Timer duration (second(s)) , required when sync_type is wait_after_sync_begins or wait_after_sync_ends
        sync_schedule: Timer rule, required when sync_type is specified_time_policy
        rep_io_timeout: remote  IO timeout (second(s)) , when replication mode isSync modeeffective when
        sync_snap_policy: User snapshotSync policy, Options: not_sync_snap, same_as_source, user_snap_retention_num, snap_tag_based
        user_snap_retention_num: Slave user snapshot retentioncount
        switch_to_async: Auto-convert sync to async remote replication switch

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Batch delete remote replication pair

    Args:
        client: DME API client
        ids:  replication Pair instance ID  list
        delete_mode: Delete mode, Options: primary_only, secondary_only, dual_ends (default)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Batch sync remote replication Pair

    Args:
        client: DME API client
        ids:  replication Pair ID  list

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Batch split remote replication Pair

    Args:
        client: DME API client
        ids:  replication Pair ID  list

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Remote replication Pair Batch primary/standby switch

    Args:
        client: DME API client
        ids:  replication Pair ID  list

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Remote replication Pair Switch from resource protection state

    Args:
        client: DME API client
        id:  replication Pair ID
        operation_type: Operation type, Options: enable, disable 

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/replication/pairs/{id}/switch-write-protection"

    payload = {
        'operation_type': operation_type
    }

    response = client.post(url, body=payload, params={"id": id})
    return response


# ============================================================================
# Device pair and replication link operations
# ============================================================================

def device_pair_list(client: DMEAPIClient, storage_id: str = None) -> dict:
    """
     query device Pairs

    Args:
        client: DME API client
        storage_id: Storage device ID

    Returns:
         device Pairs  list
    """
    url = "/rest/protection/v1/device-pairs/query"

    payload = {}

    if storage_id is not None:
        payload['storage_id'] = storage_id

    response = client.post(url, body=payload)
    return response


def replication_link_list(client: DMEAPIClient, storage_id: str = None) -> dict:
    """
    Query replication link

    Args:
        client: DME API client
        storage_id: Storage device ID

    Returns:
        Replication pair creation link list
    """
    url = "/rest/protection/v1/replication-links/query"

    payload = {}

    if storage_id is not None:
        payload['storage_id'] = storage_id

    response = client.post(url, body=payload)
    return response


# ============================================================================
# snapshot Subtopic - LUN  snapshotoperations
# ============================================================================

def snapshot_list(client: DMEAPIClient, snapshot_ids: list = None, storage_id: str = None,
                  raw_id: str = None, name: str = None, health_status: str = None,
                  running_status: str = None, source_lun_name: str = None,
                  parent_name: str = None, activated_time_from: int = None,
                  activated_time_to: int = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch query LUN  snapshot

    Args:
        client: DME API client
        snapshot_ids:  snapshot ID  list
        storage_id: Storage device ID
        raw_id:  snapshoton the storage device ID
        name: Snapshot name, supports fuzzy search
        health_status: Health status, Options: normal, fault, write_protected
        running_status: Running status, Options: activated, rolling_back, unactivated, initializing, deleting, unknown
        source_lun_name: Source LUN name, supports fuzzy search
        parent_name: Parent object name, supports fuzzy search
        activated_time_from: Query activation start time (Unix Timestamp, unit second(s)) 
        activated_time_to: Query activation end time (Unix Timestamp, unit second(s)) 
        page_no: Page start, min: 1, default: 1
        page_size: per pagecount, 1~1000, default 20

    Returns:
        LUN  snapshot list
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


def snapshot_create(client: DMEAPIClient, snapshots_infor: list, is_consist_activate: bool = None) -> dict:
    """
    Batch create LUN  snapshot

    Args:
        client: DME API client
        snapshots_infor: LUN  snapshotcreate infor list, Each item includes name, source_type, source_id
        is_consist_activate: Consistency activation, default false

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/lun-snapshots"

    payload = {
        'snapshots_infor': snapshots_infor
    }

    if is_consist_activate is not None:
        payload['is_consist_activate'] = is_consist_activate

    response = client.post(url, body=payload)
    return response


def snapshot_rollback(client: DMEAPIClient, rollback_speed: str, rollback_snapshots: list) -> dict:
    """
    batch rollback LUN  snapshot

    Args:
        client: DME API client
        rollback_speed:  Rollback rate, Options: low, medium, high, highest
        rollback_snapshots: Snapshot rollback resourceinfor list, Each item includes snapshot_id, target_type, target_id

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Batch delete LUN  snapshot

    Args:
        client: DME API client
        snapshot_ids:  snapshot ID  list
        is_delete_target_lun: Delete target LUN, default true
        is_auto_deactivate: Auto before deleteDeactivate snapshot, default false

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
# snapshot_group Subtopic - Snapshot consistency groupoperations
# ============================================================================

def snapshot_group_create(client: DMEAPIClient, name: str, protect_group_id: str,
                          description: str = None, creation_mode: str = None) -> dict:
    """
    create Snapshot consistency group

    Args:
        client: DME API client
        name: Snapshot consistency group name
        protect_group_id: Protection group ID
        description: Description
        creation_mode: creation mode, Options: new_snapshot

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Batch delete snapshot consistency group

    Args:
        client: DME API client
        snapshot_cg_ids: Snapshot consistency group ID  list
        is_delete_target_lun: Delete target LUN, Dorado 6.1.2+ only, default true

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
     activateSnapshot consistency group

    Args:
        client: DME API client
        snapshot_cg_id: Snapshot consistency group ID
        object_type: Object type, Options: parent_object
        snapshot_create_mode: Snapshot creation method, Options: auto, manual
        name_rule: Snapshot naming rule, Options: prefix_and_suffix, prefix_and_num
        name_prefix: Snapshot name prefix
        name_suffix: Snapshot name suffix
        target_snapshot_objects:  target snapshotobject list

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Batch deactivateSnapshot consistency group

    Args:
        client: DME API client
        snapshot_cg_ids: Snapshot consistency group ID  list

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
     rollbackSnapshot consistency group

    Args:
        client: DME API client
        snapshot_cg_id: Snapshot consistency group ID
        rollback_speed:  Rollback rate, Options: low, medium, high, highest
        snapshot_create_mode: Snapshot creation method, Options: auto, manual
        name_rule: Snapshot naming rule, Options: prefix_and_suffix, prefix_and_num
        name_prefix: Snapshot name prefix
        name_suffix: Snapshot name suffix
        target_snapshot_objects:  target snapshotobject list

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
# clone_group Subtopic - cloneConsistency groupoperations
# ============================================================================

def clone_group_create(client: DMEAPIClient, name: str, protect_group_id: str,
                       create_mode: str, description: str = None, name_rule: str = None,
                       name_prefix: str = None, name_suffix: str = None,
                       copy_rate: str = None, is_sync: bool = None,
                       clone_pairs: list = None) -> dict:
    """
    create cloneConsistency group

    Args:
        client: DME API client
        name: cloneConsistency group name
        protect_group_id: Protection group ID
        create_mode: creation mode, Options: auto, manual
        description: Description
        name_rule:  target LUN Naming rule, Options: prefix_and_suffix, prefix_and_num
        name_prefix:  target LUN name prefix
        name_suffix:  target LUN name suffix
        copy_rate:  copy rate, Options: low, medium, high, highest, default medium
        is_sync:  Whether to sync immediately, default true
        clone_pairs: Clone pair list, required when create_mode is manual

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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


def clone_group_sync(client: DMEAPIClient, clone_group_id: str, create_mode: str = None,
                            name_rule: str = None, name_prefix: str = None,
                            name_suffix: str = None, clone_pairs: list = None) -> dict:
    """
    SynccloneConsistency group

    Args:
        client: DME API client
        clone_group_id: cloneConsistency group ID
        create_mode: clone Pair creation mode, Options: auto, manual
        name_rule:  target LUN Naming rule, Options: prefix_and_suffix, prefix_and_num
        name_prefix:  target LUN name prefix
        name_suffix:  target LUN name suffix
        clone_pairs: Clone pair list, required when create_mode is manual

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/clone-consistency-groups/{clone_group_id}/synchronize"

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

    response = client.post(url, body=payload, params={"clone_group_id": clone_group_id})
    return response


def clone_group_delete(client: DMEAPIClient, ids: list, is_delete_dst_lun: bool = None,
                       is_recycle_dst_lun_data: bool = None) -> dict:
    """
    Batch deletecloneConsistency group

    Args:
        client: DME API client
        ids: cloneConsistency group ID  list
        is_delete_dst_lun: Delete target LUN
        is_recycle_dst_lun_data: Reclaim target LUN  data

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
# replication_group Subtopic -  replicationConsistency groupoperations
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
    Create remote replication consistency group

    Args:
        client: DME API client
        cg_name: Remote replicationConsistency group name
        remote_storage_id: Remote storage device ID
        local_pg_id: Local protection group ID, Required for OceanStor V6/Dorado V6
        description: Description
        remote_lun_group_id: Remote LUN group ID. Required for OceanStor V6/Dorado V6 when local PG is based on LUN groupred when
        local_storage_id: local Storage device ID, Required for non-V6/non-Dorado V6
        create_mode: Replication pair creation mode, Options: auto , manual 
        existed_pair_ids: Existing replication Pair  ID  list
        lun_pairs: In manual create mode,  Replication pair creation pair source and target LUN ID list
        lun_ids: In auto-create mode, Source LUN ID list
        remote_storage_pool_id: Remote storage pool ID, effective in auto-create mode
        remote_vstore_id: Remote device tenant ID, effective in auto-create mode
        remote_resource_name_rule: Remote resource naming policy, Options: same_as_local, prefix_and_suffix, prefix_and_num
        name_prefix: remote Resource name prefix
        name_suffix: remote Resource name suffix

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
        replication_group_id: Remote replicationConsistency group ID
        name: Remote replicationConsistency group name
        description: Description
        speed: Sync rate. Options: low, medium, high, highest, custom
        bandwidth: Custom sync rate (MB/s) , required when speed is custom
        recovery_policy: Recovery policy, Options: automatic, manual
        enable_compress: Link compression, when replication mode isin async modeRequired
        sync_type: Sync type, Options: manual, wait_after_sync_begins, wait_after_sync_ends, specified_time_policy
        timing_value_in_sec: Timer duration (second(s)) , required when sync_type is wait_after_sync_begins or wait_after_sync_ends
        sync_schedule: Timer rule, required when sync_type is specified_time_policy
        rep_io_timeout: remote  IO timeout (second(s)) , when replication mode isSync modeeffective when
        sync_snap_policy: User snapshotSync policy, Options: not_sync_snap, same_as_source, user_snap_retention_num, snap_tag_based
        user_snap_retention_num: Slave user snapshot retentioncount
        switch_to_async: Auto-convert sync to async remote replication switch

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Batch delete remote replication consistency group

    Args:
        client: DME API client
        ids: Remote replicationConsistency group ID  list
        is_self_adapt: supports adaptiveRemove member Pair, default false
        delete_mode: Delete mode, Options: primary_only, secondary_only, dual_ends (default)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Remote replication consistency group - add member pair

    Args:
        client: DME API client
        group_id: Remote replicationConsistency group ID
        pair_ids: Remote replication Pair  ID  list

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Remote replication consistency group - remove member pair

    Args:
        client: DME API client
        group_id: Remote replicationConsistency group ID
        pair_ids: Remote replication Pair  ID  list

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Batch sync remote replication consistency group

    >![](public_sys-resources/icon-notice.gif) **: **
    This API may directly or indirectly affect production services, causing service interruption or data loss. Proceed with caution.

    Args:
        client: DME API client
        ids: Consistency group ID  list

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Batch split remote replication consistency group

    >![](public_sys-resources/icon-notice.gif) **: **
    This API may directly or indirectly affect production services, causing service interruption or data loss. Proceed with caution.

    Args:
        client: DME API client
        ids: Consistency group ID  list

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Remote replication consistency group - batch primary/standby switch

    >![](public_sys-resources/icon-notice.gif) **: **
    This API may directly or indirectly affect production services, causing service interruption or data loss. Proceed with caution.

    Args:
        client: DME API client
        ids: Consistency group ID  list

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Remote replication consistency group - switch from write-protection state

    Args:
        client: DME API client
        id: Consistency group ID
        operation_type: Operation type, Options: enable, disable 

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/replication/groups/{id}/switch-write-protection"

    payload = {
        'operation_type': operation_type
    }

    response = client.post(url, body=payload, params={"id": id})
    return response


# ============================================================================
# FilesystemActive-active pair (fs_hypermetro_pair) subtopic functions
# ============================================================================


def filesystem_pair_create(client: DMEAPIClient, vstore_pair_id: str,
                            create_mode: str = "manual", fs_pairs: list = None,
                            speed: str = None, bandwidth: int = None,
                            service_assurance_policy: str = None,
                            isolation_threshold_time: int = None) -> dict:
    """
    Create filesystem active-active pair. This API potentially affects production services, Proceed with caution.

    Args:
        client: DME API client
        vstore_pair_id: Active-active tenantPair ID (Required, string, 1~32 characters)
        create_mode: creation mode (Optional, string). Options: manual. Default: manual
        fs_pairs: FilesystemPair list (Optional, List[FsPairInstance], max array members: 100)
        speed: Sync rate (Optional, string). Options: low, medium, high, highest, custom
        bandwidth:  bandwidth (Optional, integer, 1~1024). required when speed is custom
        service_assurance_policy: Service assurance policy (Optional, string). Options: data_reliability_preferred, service_continuity_preferred
        isolation_threshold_time:  isolationthreshold (Optional, int32, 10~30000)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/hypermetro/filesystem-pairs"

    if not vstore_pair_id:
        raise ValueError("vstore_pair_id is required")

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
     queryFilesystem active-active pair list. 

    Args:
        client: DME API client
        ids: Active-active pairinstanceID list (Optional, List[string])
        name: Active-active pair name (Optional, string)
        status: Running status (Optional, string)
        storage_id: Storage device ID (Optional, string)
        vstore_pair_id: Active-active tenantPair ID (Optional, string)
        local_fs_name: local Filesystem name (Optional, string)
        local_fs_id: local Filesystem ID (Optional, string)
        health_status: Health status (Optional, string)
        running_status: Running status (Optional, string)
        sort_key: Sort field (Optional, string)
        sort_dir: Sort direction (Optional, string)
        page_no: Page number (Optional, int32)
        page_size: per pagecount (Optional, int32)

    Returns:
        {
            total: Total count (integer),
            filesystem_pairs: Filesystem active-active pair list. 参数格式如下：[{
                id: Pair ID (string),
                name:  name (string),
                status:  status (string),
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
    Batch pause filesystem active-active pair. This API potentially affects production services, Proceed with caution.

    Args:
        client: DME API client
        fs_pair_ids: FilesystemActive-active pairID list (Required, List[string], max array members: 100, min array members: 1)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/hypermetro/filesystem-pairs/pause"

    if not fs_pair_ids or len(fs_pair_ids) == 0:
        raise ValueError("fs_pair_ids is required")

    payload = {
        'fs_pair_ids': fs_pair_ids
    }

    response = client.post(url, body=payload)
    return response


def filesystem_pair_sync(client: DMEAPIClient, fs_pair_ids: list) -> dict:
    """
    Batch sync filesystem active-active pair. This API potentially affects production services, Proceed with caution.

    Args:
        client: DME API client
        fs_pair_ids: FilesystemActive-active pairID list (Required, List[string])

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/hypermetro/filesystem-pairs/sync"

    if not fs_pair_ids or len(fs_pair_ids) == 0:
        raise ValueError("fs_pair_ids is required")

    payload = {
        'fs_pair_ids': fs_pair_ids
    }

    response = client.post(url, body=payload)
    return response


def filesystem_pair_delete(client: DMEAPIClient, ids: list,
                            is_local_delete: bool = None,
                            is_online_delete: bool = None) -> dict:
    """
    Batch delete filesystem active-active pair. This API potentially affects production services, Proceed with caution.

    Args:
        client: DME API client
        ids: Active-active pairinstanceID list (Required, List[string])
        is_local_delete: Delete localConfiguration infor (Optional, boolean, true,false)
        is_online_delete: Online deletion (Optional, boolean, true,false)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/hypermetro/filesystem-pairs/delete"

    if not ids or len(ids) == 0:
        raise ValueError("ids is required")

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
        vstore_pair_id: File systemActive-active tenantPair ID (Required, string)
        fs_pairs: Snapshot parameter list (Required, List)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/filesystem-snapshots"

    if not vstore_pair_id:
        raise ValueError("vstore_pair_id is required")

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
    Batch queryFilesystem snapshot. 

    Args:
        client: DME API client
        fs_pair_id: Active-active pair ID (Optional, string)
        name: Snapshot name (Optional, string, supports fuzzy search)
        status:  snapshot status (Optional, string)
        local_fs_name: local Filesystem name (Optional, string)
        local_fs_id: local Filesystem ID (Optional, string)
        page_no: Page number (Optional, int32)
        page_size: per pagecount (Optional, int32)

    Returns:
        {
            total: Total count (integer),
            snapshots: Filesystem snapshot list. 参数格式如下：[{
                id:  snapshotID (string),
                name: Snapshot name (string),
                status:  status (string),
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
    Batch deleteFilesystem snapshot. 

    Args:
        client: DME API client
        ids:  snapshotID list (Required, List[string])

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/filesystem-snapshots/delete"

    if not ids or len(ids) == 0:
        raise ValueError("ids is required")

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


# ============================================================================
# Active-active tenantPair (vstore_hypermetro_pair) subtopic functions
# ============================================================================


def vstore_pair_force_start(client: DMEAPIClient, ids: list) -> dict:
    """
    Batch force startActive-active tenantPair. 

    Args:
        client: DME API client
        ids: Active-active tenantPairID list (Required, List[string])

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/vstore-pairs/force-start"

    if not ids or len(ids) == 0:
        raise ValueError("ids is required")

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
    create Active-active tenantPair. 

    Args:
        client: DME API client
        local_storage_id: local Storage device ID (Required, string)
        remote_storage_id: Remote storage device ID (Required, string)
        name:  tenantPair name (Optional, string)
        description:  description (Optional, string)
        remote_vstore_id: remote Tenant ID (Optional, string)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/vstore-pairs"

    if not local_storage_id or not remote_storage_id:
        raise ValueError("local_storage_id and remote_storage_id are required")

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
     query active-active tenant pair list. 

    Args:
        client: DME API client
        ids: Active-active tenantPair ID list (Optional, List[string])
        name:  name (Optional, string)
        status:  status (Optional, string)
        local_storage_id: local Storage device ID (Optional, string)
        remote_storage_id: Remote storage device ID (Optional, string)
        health_status: Health status (Optional, string)
        running_status: Running status (Optional, string)
        page_no: Page number (Optional, int32)
        page_size: per pagecount (Optional, int32)

    Returns:
        {
            total: Total count (integer),
            vstore_pairs: Active-active tenant pair list. 参数格式如下：[{
                id: Pair ID (string),
                name:  name (string),
                status:  status (string),
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
    Batch primary/standby switchActive-active tenantPair. 

    Args:
        client: DME API client
        ids: Active-active tenantPairID list (Required, List[string])

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/vstore-pairs/switch"

    if not ids or len(ids) == 0:
        raise ValueError("ids is required")

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def vstore_pair_delete(client: DMEAPIClient, ids: list) -> dict:
    """
    Batch delete active-active tenantPair. 

    Args:
        client: DME API client
        ids: Active-active tenantPairID list (Required, List[string])

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/vstore-pairs/delete"

    if not ids or len(ids) == 0:
        raise ValueError("ids is required")

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def vstore_pair_modify(client: DMEAPIClient, id: str, name: str = None) -> dict:
    """
    ModifyActive-active tenantpair. 

    Args:
        client: DME API client
        id: Active-active tenantPair ID (Required, string)
        name:  name (Optional, string)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/metro/vstore-pairs/{id}"

    if not id:
        raise ValueError("id is required")

    payload = {}
    if name is not None:
        payload['name'] = name

    response = client.put(url, body=payload, params={"id": id})
    return response


# ============================================================================
# Active-active domain (hypermetro_domain) subtopic functions
# ============================================================================


def hypermetro_domain_force_start(client: DMEAPIClient, id: str) -> dict:
    """
    force startFilesystemActive-active domain. 

    Args:
        client: DME API client
        id: Active-active domainID (Required, string)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/hyper-metro-domains/{id}/force-start"

    if not id:
        raise ValueError("id is required")

    response = client.post(url, body={}, params={"id": id})
    return response


def hypermetro_domain_switch_site(client: DMEAPIClient, id: str) -> dict:
    """
    preferred site switchFilesystemActive-active domain. 

    Args:
        client: DME API client
        id: Active-active domainID (Required, string)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/hyper-metro-domains/{id}/switch-priority-site"

    if not id:
        raise ValueError("id is required")

    response = client.post(url, body={}, params={"id": id})
    return response


def hypermetro_domain_recover(client: DMEAPIClient, id: str) -> dict:
    """
     resumeFilesystemActive-active domain. 

    Args:
        client: DME API client
        id: Active-active domainID (Required, string)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/hyper-metro-domains/{id}/recover"

    if not id:
        raise ValueError("id is required")

    response = client.post(url, body={}, params={"id": id})
    return response


def hypermetro_domain_split(client: DMEAPIClient, id: str) -> dict:
    """
    SplitFilesystemActive-active domain. 

    Args:
        client: DME API client
        id: Active-active domainID (Required, string)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/hyper-metro-domains/{id}/split"

    if not id:
        raise ValueError("id is required")

    response = client.post(url, body={}, params={"id": id})
    return response


def hypermetro_domain_swap_role(client: DMEAPIClient, id: str) -> dict:
    """
    Primary/standby switchFilesystemActive-active domain. 

    Args:
        client: DME API client
        id: Active-active domainID (Required, string)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/protection/v1/hyper-metro-domains/{id}/swap-role"

    if not id:
        raise ValueError("id is required")

    response = client.post(url, body={}, params={"id": id})
    return response


# ============================================================================
# Active-active pair (hypermetro_pair) subtopic functions
# ============================================================================


def hypermetro_pair_query_available_luns(client: DMEAPIClient,
                                          source_lun_id: str) -> dict:
    """
     Query available target LUNs for active-active pair. 

    Args:
        client: DME API client
        source_lun_id: Source LUN ID (Required, string)

    Returns:
        {
            optional_target_luns: Optional targetLUN list. 参数格式如下：[{
                lun_id: LUN ID (string),
                lun_name: LUN name (string),
                capacity:  capacity (integer),
            }, ...],
        }
    """
    url = "/rest/protection/v1/metro/lun-pairs/{source_lun_id}/optional-target-luns"

    if not source_lun_id:
        raise ValueError("source_lun_id is required")

    response = client.get(url, params={"source_lun_id": source_lun_id})
    return response


# Action list for CLI help
ACTIONS = {
    # group subtopic actions
    'group_list': {
        'func': group_list,
        'description': 'Batch query protection group',
        'params': ['name', 'project_id', 'storage_name', 'storage_id', 'raw_id', 'lun_group_raw_id', 'vstore_id', 'vstore_raw_id', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'group'
    },
    'group_create': {
        'func': group_create,
        'description': 'create Protection group',
        'params': ['name', 'storage_id', 'lun_ids', 'lun_group_id', 'description'],
        'subtopic': 'group'
    },
    'group_modify': {
        'func': group_modify,
        'description': 'modify Protection group',
        'params': ['pg_id', 'name', 'description'],
        'subtopic': 'group'
    },
    'group_delete': {
        'func': group_delete,
        'description': 'Batch delete protection group',
        'params': ['pg_ids'],
        'subtopic': 'group'
    },
    'group_add_luns': {
        'func': group_add_luns,
        'description': 'Add member LUN to protection group',
        'params': ['pg_id', 'lun_ids', 'hyper_metro', 'rem_reps'],
        'subtopic': 'group'
    },
    'group_remove_luns': {
        'func': group_remove_luns,
        'description': 'Remove LUN members from protection group',
        'params': ['pg_id', 'lun_ids', 'is_delay'],
        'subtopic': 'group'
    },
    # hypermetro_group subtopic actions
    'hypermetro_group_list': {
        'func': hypermetro_group_list,
        'description': 'Batch query active-active consistency group',
        'params': ['page_no', 'page_size', 'name', 'raw_id', 'protect_group_id', 'storage_id', 'storage_name', 'local_vstore_id', 'local_vstore_raw_id', 'remote_vstore_id', 'remote_vstore_raw_id'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_create': {
        'func': hypermetro_group_create,
        'description': 'create Active-active consistency group',
        'params': ['domain_id', 'name', 'local_storage_id', 'local_pg_id', 'description', 'create_mode', 'remote_vstore_id', 'remote_storage_pool_id', 'lun_ids', 'remote_resource_name_rule'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_modify': {
        'func': hypermetro_group_modify,
        'description': 'modify Active-active consistency group',
        'params': ['group_id', 'name', 'description', 'recovery_policy', 'service_assurance_policy', 'speed', 'bandwidth', 'isolation_threshold_time'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_delete': {
        'func': hypermetro_group_delete,
        'description': 'Batch delete active-active consistency group',
        'params': ['ids', 'is_self_adapt', 'delete_mode'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_add_pairs': {
        'func': hypermetro_group_add_pairs,
        'description': 'Active-active consistency group - add member pair',
        'params': ['group_id', 'pair_ids', 'is_self_adapt'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_remove_pairs': {
        'func': hypermetro_group_remove_pairs,
        'description': 'Active-active consistency group - remove member pair',
        'params': ['group_id', 'pair_ids'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_pause': {
        'func': hypermetro_group_pause,
        'description': ' pause active-active consistency group',
        'params': ['ids', 'priority_station_type'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_force_startup': {
        'func': hypermetro_group_force_startup,
        'description': 'force start active-active consistency group',
        'params': ['ids', 'priority_station_type'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_switch_priority': {
        'func': hypermetro_group_switch_priority,
        'description': 'Active-active consistency grouppreferred site switch',
        'params': ['ids'],
        'subtopic': 'hypermetro_group'
    },
    # hypermetro_pair subtopic actions
    'hypermetro_pair_list': {
        'func': hypermetro_pair_list,
        'description': 'Batch query LUN Active-active Pair',
        'params': ['page_no', 'page_size', 'group_id', 'group_name', 'group_raw_id', 'pair_raw_id', 'local_storage_id', 'local_storage_name', 'local_vstore_id', 'local_vstore_raw_id', 'local_volume_name', 'local_host_access_state', 'remote_vstore_id', 'remote_vstore_raw_id', 'remote_volume_name'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_create': {
        'func': hypermetro_pair_create,
        'description': 'create Active-active Pair',
        'params': ['create_mode', 'lun_pairs', 'lun_ids', 'remote_storage_pool_id', 'remote_vstore_id', 'remote_resource_name_rule', 'name_prefix', 'name_suffix', 'local_storage_id', 'domain_id', 'speed', 'bandwidth', 'service_assurance_policy', 'isolation_threshold_time', 'recovery_policy'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_modify': {
        'func': hypermetro_pair_modify,
        'description': 'modify Active-active Pair',
        'params': ['pair_id', 'speed', 'bandwidth', 'recovery_policy', 'service_assurance_policy', 'isolation_threshold_time'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_delete': {
        'func': hypermetro_pair_delete,
        'description': 'Batch delete active-active Pair',
        'params': ['ids', 'delete_mode', 'is_lun_service_interrupt'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_sync': {
        'func': hypermetro_pair_sync,
        'description': 'Sync active-active pair',
        'params': ['ids'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_pause': {
        'func': hypermetro_pair_pause,
        'description': ' pause active-active pair',
        'params': ['ids', 'priority_station_type'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_force_startup': {
        'func': hypermetro_pair_force_startup,
        'description': 'force start active-active pair',
        'params': ['ids', 'priority_station_type'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_switch_priority': {
        'func': hypermetro_pair_switch_priority,
        'description': 'Active-active Pair preferred site switch',
        'params': ['ids'],
        'subtopic': 'hypermetro_pair'
    },
    # hypermetro_domain subtopic actions
    'hypermetro_domain_list': {
        'func': hypermetro_domain_list,
        'description': 'Batch query active-active domain',
        'params': ['storage_id', 'types'],
        'subtopic': 'hypermetro_domain'
    },
    # replication_group subtopic actions
    'replication_group_create': {
        'func': replication_group_create,
        'description': 'Create remote replication consistency group',
        'params': ['cg_name', 'remote_storage_id', 'local_pg_id', 'description', 'remote_lun_group_id', 'local_storage_id', 'create_mode', 'existed_pair_ids', 'lun_pairs', 'lun_ids', 'remote_storage_pool_id', 'remote_vstore_id', 'remote_resource_name_rule', 'name_prefix', 'name_suffix'],
        'subtopic': 'replication_group'
    },
    'replication_group_modify': {
        'func': replication_group_modify,
        'description': 'modify remote replication consistency group',
        'params': ['replication_group_id', 'name', 'description', 'speed', 'bandwidth', 'recovery_policy', 'enable_compress', 'sync_type', 'timing_value_in_sec', 'sync_schedule', 'rep_io_timeout', 'sync_snap_policy', 'user_snap_retention_num', 'switch_to_async'],
        'subtopic': 'replication_group'
    },
    'replication_group_delete': {
        'func': replication_group_delete,
        'description': 'Batch delete remote replication consistency group',
        'params': ['ids', 'is_self_adapt', 'delete_mode'],
        'subtopic': 'replication_group'
    },
    'replication_group_add_pairs': {
        'func': replication_group_add_pairs,
        'description': 'Remote replication consistency group - add member pair',
        'params': ['group_id', 'pair_ids'],
        'subtopic': 'replication_group'
    },
    'replication_group_remove_pairs': {
        'func': replication_group_remove_pairs,
        'description': 'Remote replication consistency group - remove member pair',
        'params': ['group_id', 'pair_ids'],
        'subtopic': 'replication_group'
    },
    'replication_group_sync': {
        'func': replication_group_sync,
        'description': 'Batch sync remote replication consistency group',
        'params': ['ids'],
        'subtopic': 'replication_group'
    },
    'replication_group_split': {
        'func': replication_group_split,
        'description': 'Batch split remote replication consistency group',
        'params': ['ids'],
        'subtopic': 'replication_group'
    },
    'replication_group_switch': {
        'func': replication_group_switch,
        'description': 'Remote replication consistency group - batch primary/standby switch',
        'params': ['ids'],
        'subtopic': 'replication_group'
    },
    'replication_group_switch_write_protection': {
        'func': replication_group_switch_write_protection,
        'description': 'Remote replication consistency group - switch from write-protection state',
        'params': ['id', 'operation_type'],
        'subtopic': 'replication_group'
    },
    # replication_pair subtopic actions
    'replication_pair_list': {
        'func': replication_pair_list,
        'description': 'Batch query replication Pair',
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
        'description': 'modify  replication Pair',
        'params': ['pair_id', 'speed', 'bandwidth', 'recovery_policy', 'enable_compress', 'sync_type', 'timing_value_in_sec', 'sync_schedule', 'rep_io_timeout', 'sync_snap_policy', 'user_snap_retention_num', 'switch_to_async'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_delete': {
        'func': replication_pair_delete,
        'description': 'Batch delete remote replication pair',
        'params': ['ids', 'delete_mode'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_sync': {
        'func': replication_pair_sync,
        'description': 'Batch sync remote replication Pair',
        'params': ['ids'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_split': {
        'func': replication_pair_split,
        'description': 'Batch split remote replication Pair',
        'params': ['ids'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_switch': {
        'func': replication_pair_switch,
        'description': 'Remote replication Pair Batch primary/standby switch',
        'params': ['ids'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_switch_write_protection': {
        'func': replication_pair_switch_write_protection,
        'description': 'Remote replication Pair Switch from resource protection state',
        'params': ['id', 'operation_type'],
        'subtopic': 'replication_pair'
    },
    # device subtopic actions
    'device_pair_list': {
        'func': device_pair_list,
        'description': ' query device Pairs',
        'params': ['storage_id'],
        'subtopic': 'device_pair'
    },
    'replication_link_list': {
        'func': replication_link_list,
        'description': 'Query replication link',
        'params': ['storage_id'],
        'subtopic': 'replication_link'
    },
    # snapshot subtopic actions
    'snapshot_list': {
        'func': snapshot_list,
        'description': 'Batch query LUN  snapshot',
        'params': ['snapshot_ids', 'storage_id', 'raw_id', 'name', 'health_status', 'running_status', 'source_lun_name', 'parent_name', 'activated_time_from', 'activated_time_to', 'page_no', 'page_size'],
        'subtopic': 'snapshot'
    },
    'snapshot_create': {
        'func': snapshot_create,
        'description': 'Batch create LUN  snapshot',
        'params': ['snapshots_infor', 'is_consist_activate'],
        'subtopic': 'snapshot'
    },
    'snapshot_rollback': {
        'func': snapshot_rollback,
        'description': 'batch rollback LUN  snapshot',
        'params': ['rollback_speed', 'rollback_snapshots'],
        'subtopic': 'snapshot'
    },
    'snapshot_delete': {
        'func': snapshot_delete,
        'description': 'Batch delete LUN  snapshot',
        'params': ['snapshot_ids', 'is_delete_target_lun', 'is_auto_deactivate'],
        'subtopic': 'snapshot'
    },
    # snapshot_group subtopic actions
    'snapshot_group_create': {
        'func': snapshot_group_create,
        'description': 'create Snapshot consistency group',
        'params': ['name', 'protect_group_id', 'description', 'creation_mode'],
        'subtopic': 'snapshot_group'
    },
    'snapshot_group_delete': {
        'func': snapshot_group_delete,
        'description': 'Batch delete snapshot consistency group',
        'params': ['snapshot_cg_ids', 'is_delete_target_lun'],
        'subtopic': 'snapshot_group'
    },
    'snapshot_group_activate': {
        'func': snapshot_group_activate,
        'description': ' activateSnapshot consistency group',
        'params': ['snapshot_cg_id', 'object_type', 'snapshot_create_mode', 'name_rule', 'name_prefix', 'name_suffix', 'target_snapshot_objects'],
        'subtopic': 'snapshot_group'
    },
    'snapshot_group_deactivate': {
        'func': snapshot_group_deactivate,
        'description': 'Batch deactivateSnapshot consistency group',
        'params': ['snapshot_cg_ids'],
        'subtopic': 'snapshot_group'
    },
    'snapshot_group_rollback': {
        'func': snapshot_group_rollback,
        'description': ' rollbackSnapshot consistency group',
        'params': ['snapshot_cg_id', 'rollback_speed', 'snapshot_create_mode', 'name_rule', 'name_prefix', 'name_suffix', 'target_snapshot_objects'],
        'subtopic': 'snapshot_group'
    },
    # clone_group subtopic actions
    'clone_group_create': {
        'func': clone_group_create,
        'description': 'create cloneConsistency group',
        'params': ['name', 'protect_group_id', 'create_mode', 'description', 'name_rule', 'name_prefix', 'name_suffix', 'copy_rate', 'is_sync', 'clone_pairs'],
        'subtopic': 'clone_group'
    },
    'clone_group_sync': {
        'func': clone_group_sync,
        'description': 'SynccloneConsistency group',
        'params': ['clone_cg_id', 'create_mode', 'name_rule', 'name_prefix', 'name_suffix', 'clone_pairs'],
        'subtopic': 'clone_group'
    },
    'clone_group_delete': {
        'func': clone_group_delete,
        'description': 'Batch deletecloneConsistency group',
        'params': ['ids', 'is_delete_dst_lun', 'is_recycle_dst_lun_data'],
        'subtopic': 'clone_group'
    },
    # fs_hypermetro_pair subtopic actions
    'filesystem_pair_create': {
        'func': filesystem_pair_create,
        'description': 'Create filesystem active-active pair',
        'params': ['vstore_pair_id', 'create_mode', 'fs_pairs', 'speed', 'bandwidth', 'service_assurance_policy', 'isolation_threshold_time'],
        'subtopic': 'fs_hypermetro_pair'
    },
    'filesystem_pair_list': {
        'func': filesystem_pair_list,
        'description': ' queryFilesystem active-active pair list',
        'params': ['ids', 'name', 'status', 'storage_id', 'vstore_pair_id', 'local_fs_name', 'local_fs_id', 'health_status', 'running_status', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'fs_hypermetro_pair'
    },
    'filesystem_pair_pause': {
        'func': filesystem_pair_pause,
        'description': 'Batch pause filesystem active-active pair',
        'params': ['fs_pair_ids'],
        'subtopic': 'fs_hypermetro_pair'
    },
    'filesystem_pair_sync': {
        'func': filesystem_pair_sync,
        'description': 'Batch sync filesystem active-active pair',
        'params': ['fs_pair_ids'],
        'subtopic': 'fs_hypermetro_pair'
    },
    'filesystem_pair_delete': {
        'func': filesystem_pair_delete,
        'description': 'Batch delete filesystem active-active pair',
        'params': ['ids', 'is_local_delete', 'is_online_delete'],
        'subtopic': 'fs_hypermetro_pair'
    },
    # fs_snapshot subtopic actions
    'fs_snapshot_create': {
        'func': fs_snapshot_create,
        'description': 'create Filesystem snapshot',
        'params': ['vstore_pair_id', 'fs_pairs'],
        'subtopic': 'fs_snapshot'
    },
    'fs_snapshot_list': {
        'func': fs_snapshot_list,
        'description': 'Batch queryFilesystem snapshot',
        'params': ['fs_pair_id', 'name', 'status', 'local_fs_name', 'local_fs_id', 'page_no', 'page_size'],
        'subtopic': 'fs_snapshot'
    },
    'fs_snapshot_delete': {
        'func': fs_snapshot_delete,
        'description': 'Batch deleteFilesystem snapshot',
        'params': ['ids'],
        'subtopic': 'fs_snapshot'
    },
    # vstore_hypermetro_pair subtopic actions
    'vstore_pair_force_start': {
        'func': vstore_pair_force_start,
        'description': 'Batch force startActive-active tenantPair',
        'params': ['ids'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    'vstore_pair_create': {
        'func': vstore_pair_create,
        'description': 'create Active-active tenantPair',
        'params': ['local_storage_id', 'remote_storage_id', 'name', 'description', 'remote_vstore_id'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    'vstore_pair_list': {
        'func': vstore_pair_list,
        'description': ' query active-active tenant pair list',
        'params': ['ids', 'name', 'status', 'local_storage_id', 'remote_storage_id', 'health_status', 'running_status', 'page_no', 'page_size'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    'vstore_pair_switch': {
        'func': vstore_pair_switch,
        'description': 'Batch primary/standby switchActive-active tenantPair',
        'params': ['ids'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    'vstore_pair_delete': {
        'func': vstore_pair_delete,
        'description': 'Batch delete active-active tenantPair',
        'params': ['ids'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    'vstore_pair_modify': {
        'func': vstore_pair_modify,
        'description': 'ModifyActive-active tenantpair',
        'params': ['id', 'name'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    # hypermetro_domain subtopic actions
    'hypermetro_domain_force_start': {
        'func': hypermetro_domain_force_start,
        'description': 'force startFilesystemActive-active domain',
        'params': ['id'],
        'subtopic': 'hypermetro_domain'
    },
    'hypermetro_domain_switch_site': {
        'func': hypermetro_domain_switch_site,
        'description': 'preferred site switchFilesystemActive-active domain',
        'params': ['id'],
        'subtopic': 'hypermetro_domain'
    },
    'hypermetro_domain_recover': {
        'func': hypermetro_domain_recover,
        'description': ' resumeFilesystemActive-active domain',
        'params': ['id'],
        'subtopic': 'hypermetro_domain'
    },
    'hypermetro_domain_split': {
        'func': hypermetro_domain_split,
        'description': 'SplitFilesystemActive-active domain',
        'params': ['id'],
        'subtopic': 'hypermetro_domain'
    },
    'hypermetro_domain_swap_role': {
        'func': hypermetro_domain_swap_role,
        'description': 'Primary/standby switchFilesystemActive-active domain',
        'params': ['id'],
        'subtopic': 'hypermetro_domain'
    },
    # hypermetro_pair subtopic actions
    'query_available_luns': {
        'func': hypermetro_pair_query_available_luns,
        'description': ' Query available target LUNs for active-active pair',
        'params': ['source_lun_id'],
        'subtopic': 'hypermetro_pair'
    },
}
