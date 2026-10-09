"""
Protection related operations
"""

import sys
import os

from pydme.client import DMEAPIClient


# ============================================================================
# group subtopic - protection group operations
# ============================================================================

def group_list(client: DMEAPIClient, name: str = None, project_id: str = None,
               storage_name: str = None, storage_id: str = None,
               raw_id: str = None, lun_group_raw_id: str = None,
               vstore_id: str = None, vstore_raw_id: str = None,
               sort_key: str = None, sort_dir: str = None,
               page_no: int = 1, page_size: int = 20) -> dict:
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
    url = "/rest/protection/v1/protection-groups/{pg_id}"

    payload = {}

    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description

    response = client.put(url, body=payload, params={"pg_id": pg_id})
    return response


def group_delete(client: DMEAPIClient, pg_ids: list) -> dict:
    url = "/rest/protection/v1/protection-groups/delete"

    payload = {
        'pg_ids': pg_ids
    }

    response = client.post(url, body=payload)
    return response


def group_add_luns(client: DMEAPIClient, pg_id: str, lun_ids: list = None,
                   hyper_metro: dict = None, rem_reps: list = None) -> dict:
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
    url = "/rest/protection/v1/protection-groups/{pg_id}/remove-luns"

    payload = {
        'lun_ids': lun_ids
    }

    if is_delay is not None:
        payload['is_delay'] = is_delay

    response = client.post(url, body=payload, params={"pg_id": pg_id})
    return response


# ============================================================================
# hypermetro_group subtopic - hypermetro consistency group operations
# ============================================================================

def hypermetro_group_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 20,
                          name: str = None, raw_id: str = None,
                          protect_group_id: str = None, storage_id: str = None,
                          storage_name: str = None, local_vstore_id: str = None,
                          local_vstore_raw_id: str = None, remote_vstore_id: str = None,
                          remote_vstore_raw_id: str = None, domain_name: str = None,
                          health_status: str = None, running_status: str = None,
                          priority_station_type: str = None) -> dict:
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
    if domain_name is not None:
        payload['domain_name'] = domain_name
    if health_status is not None:
        payload['health_status'] = health_status
    if running_status is not None:
        payload['running_status'] = running_status
    if priority_station_type is not None:
        payload['priority_station_type'] = priority_station_type

    response = client.post(url, body=payload)
    return response


def hypermetro_group_create(client: DMEAPIClient, domain_id: str, name: str,
                            local_storage_id: str = None, local_pg_id: str = None,
                            description: str = None, create_mode: str = None,
                            remote_vstore_id: str = None, remote_storage_pool_id: str = None,
                            lun_ids: list = None, remote_resource_name_rule: str = None,
                            name_prefix: str = None, name_suffix: str = None,
                            service_assurance_policy: str = None,
                            recovery_policy: str = None, speed: str = None,
                            bandwidth: int = None, first_sync_policy: str = None,
                            remote_lun_group_id: str = None,
                            lun_pairs: list = None,
                            existed_pair_ids: list = None,
                            is_auto_pause: bool = None,
                            is_auto_sync: bool = None,
                            isolation_threshold_time: int = None) -> dict:
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
    if name_prefix is not None:
        payload['name_prefix'] = name_prefix
    if name_suffix is not None:
        payload['name_suffix'] = name_suffix
    if service_assurance_policy is not None:
        payload['service_assurance_policy'] = service_assurance_policy
    if recovery_policy is not None:
        payload['recovery_policy'] = recovery_policy
    if speed is not None:
        payload['speed'] = speed
    if bandwidth is not None:
        payload['bandwidth'] = bandwidth
    if first_sync_policy is not None:
        payload['first_sync_policy'] = first_sync_policy
    if remote_lun_group_id is not None:
        payload['remote_lun_group_id'] = remote_lun_group_id
    if lun_pairs is not None:
        payload['lun_pairs'] = lun_pairs
    if existed_pair_ids is not None:
        payload['existed_pair_ids'] = existed_pair_ids
    if is_auto_pause is not None:
        payload['is_auto_pause'] = is_auto_pause
    if is_auto_sync is not None:
        payload['is_auto_sync'] = is_auto_sync
    if isolation_threshold_time is not None:
        payload['isolation_threshold_time'] = isolation_threshold_time

    response = client.post(url, body=payload)
    return response


def hypermetro_group_modify(client: DMEAPIClient, group_id: str, name: str = None,
                             description: str = None, recovery_policy: str = None,
                             service_assurance_policy: str = None, speed: str = None,
                             bandwidth: int = None, isolation_threshold_time: int = None) -> dict:
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
    url = "/rest/protection/v1/metro/groups/{group_id}/add-pairs"

    payload = {
        'pair_ids': pair_ids
    }

    if is_self_adapt is not None:
        payload['is_self_adapt'] = is_self_adapt

    response = client.post(url, body=payload, params={"group_id": group_id})
    return response


def hypermetro_group_remove_pairs(client: DMEAPIClient, group_id: str, pair_ids: list) -> dict:
    url = "/rest/protection/v1/metro/groups/{group_id}/remove-pairs"

    payload = {
        'pair_ids': pair_ids
    }

    response = client.post(url, body=payload, params={"group_id": group_id})
    return response


def hypermetro_group_pause(client: DMEAPIClient, ids: list, priority_station_type: str) -> dict:
    url = "/rest/protection/v1/metro/groups/pause"

    payload = {
        'ids': ids,
        'priority_station_type': priority_station_type
    }

    response = client.post(url, body=payload)
    return response


def hypermetro_group_force_startup(client: DMEAPIClient, ids: list, priority_station_type: str) -> dict:
    url = "/rest/protection/v1/metro/groups/force-startup"

    payload = {
        'ids': ids,
        'priority_station_type': priority_station_type
    }

    response = client.post(url, body=payload)
    return response


def hypermetro_group_switch_priority(client: DMEAPIClient, ids: list) -> dict:
    url = "/rest/protection/v1/metro/groups/switch-priority-site"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def hypermetro_group_sync(client: DMEAPIClient, ids: list) -> dict:
    url = "/rest/protection/v1/metro/groups/sync"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


# ============================================================================
# hypermetro_pair subtopic - hypermetro pair operations
# ============================================================================

def hypermetro_pair_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 20,
                         group_id: str = None, group_name: str = None,
                         group_raw_id: str = None, pair_raw_id: str = None,
                         local_storage_id: str = None, local_storage_name: str = None,
                         local_vstore_id: str = None, local_vstore_raw_id: str = None,
                         local_volume_name: str = None, local_host_access_state: str = None,
                         remote_vstore_id: str = None, remote_vstore_raw_id: str = None,
                         remote_volume_name: str = None) -> dict:
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
    url = "/rest/protection/v1/metro/lun-pairs/sync"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def hypermetro_pair_pause(client: DMEAPIClient, ids: list, priority_station_type: str) -> dict:
    url = "/rest/protection/v1/metro/lun-pairs/pause"

    payload = {
        'ids': ids,
        'priority_station_type': priority_station_type
    }

    response = client.post(url, body=payload)
    return response


def hypermetro_pair_force_startup(client: DMEAPIClient, ids: list, priority_station_type: str) -> dict:
    url = "/rest/protection/v1/metro/lun-pairs/force-startup"

    payload = {
        'ids': ids,
        'priority_station_type': priority_station_type
    }

    response = client.post(url, body=payload)
    return response


def hypermetro_pair_switch_priority(client: DMEAPIClient, ids: list) -> dict:
    url = "/rest/protection/v1/metro/lun-pairs/switch-priority-site"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


# ============================================================================
# hypermetro_domain subtopic - hypermetro domain operations
# ============================================================================

def hypermetro_domain_list(client: DMEAPIClient, storage_id: str = None,
                            types: list = None) -> dict:
    url = "/rest/protection/v1/hyper-metro-domains/query"

    payload = {}

    if storage_id is not None:
        payload['storage_id'] = storage_id
    if types is not None:
        payload['types'] = types

    response = client.post(url, body=payload)
    return response


# ============================================================================
# replication_pair subtopic - replication pair operations
# ============================================================================

def replication_pair_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 20,
                          raw_id: str = None,
                          local_resource_types: list = None,
                          local_vstore_raw_id: str = None,
                          group_id: str = None, group_name: str = None,
                          group_raw_id: str = None,
                          local_resource_raw_id: str = None,
                          local_resource_raw_ids: list = None,
                          local_resource_name: str = None,
                          remote_resource_name: str = None,
                          local_storage_id: str = None,
                          local_storage_name: str = None,
                          health_status: str = None,
                          running_status: str = None,
                          recovery_policy: str = None,
                          sort_key: str = None, sort_dir: str = None) -> dict:
    url = "/rest/protection/v1/replication/pairs/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if raw_id is not None:
        payload['raw_id'] = raw_id
    if local_resource_types is not None:
        payload['local_resource_types'] = local_resource_types
    if local_vstore_raw_id is not None:
        payload['local_vstore_raw_id'] = local_vstore_raw_id
    if group_id is not None:
        payload['group_id'] = group_id
    if group_name is not None:
        payload['group_name'] = group_name
    if group_raw_id is not None:
        payload['group_raw_id'] = group_raw_id
    if local_resource_raw_id is not None:
        payload['local_resource_raw_id'] = local_resource_raw_id
    if local_resource_raw_ids is not None:
        payload['local_resource_raw_ids'] = local_resource_raw_ids
    if local_resource_name is not None:
        payload['local_resource_name'] = local_resource_name
    if remote_resource_name is not None:
        payload['remote_resource_name'] = remote_resource_name
    if local_storage_id is not None:
        payload['local_storage_id'] = local_storage_id
    if local_storage_name is not None:
        payload['local_storage_name'] = local_storage_name
    if health_status is not None:
        payload['health_status'] = health_status
    if running_status is not None:
        payload['running_status'] = running_status
    if recovery_policy is not None:
        payload['recovery_policy'] = recovery_policy
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def replication_pair_create(client: DMEAPIClient, local_storage_id: str,
                            remote_storage_id: str,
                            create_mode: str = None,
                            replication_mode: str = None,
                            resource_pairs: list = None,
                            remote_storage_pool_id: str = None,
                            remote_vstore_id: str = None,
                            remote_resource_name_rule: str = None,
                            name_prefix: str = None, name_suffix: str = None,
                            speed: str = None, bandwidth: int = None,
                            recovery_policy: str = None,
                            first_sync_policy: str = None,
                            sync_type: str = None,
                            timing_val: int = None,
                            sync_schedule: dict = None,
                            rep_io_timeout: int = None,
                            sync_snap_policy: str = None,
                            user_snap_retention_num: int = None,
                            snap_tag_list: list = None,
                            enable_compress: bool = None,
                            is_backup: bool = None,
                            switch_to_async: bool = None,
                            consistency_group_info: dict = None) -> dict:
    url = "/rest/protection/v1/replication/pairs"

    payload = {
        'local_storage_id': local_storage_id,
        'remote_storage_id': remote_storage_id
    }

    if create_mode is not None:
        payload['create_mode'] = create_mode
    if replication_mode is not None:
        payload['replication_mode'] = replication_mode
    if resource_pairs is not None:
        payload['resource_pairs'] = resource_pairs
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
    if first_sync_policy is not None:
        payload['first_sync_policy'] = first_sync_policy
    if sync_type is not None:
        payload['sync_type'] = sync_type
    if timing_val is not None:
        payload['timing_val'] = timing_val
    if sync_schedule is not None:
        payload['sync_schedule'] = sync_schedule
    if rep_io_timeout is not None:
        payload['rep_io_timeout'] = rep_io_timeout
    if sync_snap_policy is not None:
        payload['sync_snap_policy'] = sync_snap_policy
    if user_snap_retention_num is not None:
        payload['user_snap_retention_num'] = user_snap_retention_num
    if snap_tag_list is not None:
        payload['snap_tag_list'] = snap_tag_list
    if enable_compress is not None:
        payload['enable_compress'] = enable_compress
    if is_backup is not None:
        payload['is_backup'] = is_backup
    if switch_to_async is not None:
        payload['switch_to_async'] = switch_to_async
    if consistency_group_info is not None:
        payload['consistency_group_info'] = consistency_group_info

    response = client.post(url, body=payload)
    return response


def replication_pair_modify(client: DMEAPIClient, pair_id: str, speed: str = None,
                            bandwidth: int = None, recovery_policy: str = None,
                            enable_compress: bool = None,
                            secondary_res_protection: str = None,
                            sync_type: str = None,
                            timing_val: int = None,
                            sync_schedule: dict = None,
                            rep_io_timeout: int = None,
                            sync_snap_policy: str = None,
                            user_snap_retention_num: int = None,
                            snap_tag_list: list = None,
                            switch_to_async: bool = None,
                            switch_to_sync: bool = None,
                            sync_to_async_bandwidth: int = None,
                            sync_to_async_latency: int = None,
                            async_to_sync_bandwidth: int = None,
                            async_to_sync_latency: int = None,
                            transfer_cycle: int = None) -> dict:
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
    if secondary_res_protection is not None:
        payload['secondary_res_protection'] = secondary_res_protection
    if timing_val is not None:
        payload['timing_val'] = timing_val
    if snap_tag_list is not None:
        payload['snap_tag_list'] = snap_tag_list
    if switch_to_async is not None:
        payload['switch_to_async'] = switch_to_async
    if switch_to_sync is not None:
        payload['switch_to_sync'] = switch_to_sync
    if sync_to_async_bandwidth is not None:
        payload['sync_to_async_bandwidth'] = sync_to_async_bandwidth
    if sync_to_async_latency is not None:
        payload['sync_to_async_latency'] = sync_to_async_latency
    if async_to_sync_bandwidth is not None:
        payload['async_to_sync_bandwidth'] = async_to_sync_bandwidth
    if async_to_sync_latency is not None:
        payload['async_to_sync_latency'] = async_to_sync_latency
    if transfer_cycle is not None:
        payload['transfer_cycle'] = transfer_cycle

    response = client.put(url, body=payload, params={"pair_id": pair_id})
    return response


def replication_pair_delete(client: DMEAPIClient, ids: list, delete_mode: str = None,
                             is_enforce_secondary_data: bool = None) -> dict:
    url = "/rest/protection/v1/replication/pairs/delete"

    payload = {
        'ids': ids
    }

    if delete_mode is not None:
        payload['delete_mode'] = delete_mode
    if is_enforce_secondary_data is not None:
        payload['is_enforce_secondary_data'] = is_enforce_secondary_data

    response = client.post(url, body=payload)
    return response


def replication_pair_sync(client: DMEAPIClient, ids: list) -> dict:
    url = "/rest/protection/v1/replication/pairs/sync"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def replication_pair_split(client: DMEAPIClient, ids: list) -> dict:
    url = "/rest/protection/v1/replication/pairs/split"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def replication_pair_switch(client: DMEAPIClient, ids: list) -> dict:
    url = "/rest/protection/v1/replication/pairs/switch"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def replication_pair_switch_write_protection(client: DMEAPIClient, id: str, operation_type: str) -> dict:
    url = "/rest/protection/v1/replication/pairs/{id}/switch-write-protection"

    payload = {
        'operation_type': operation_type
    }

    response = client.post(url, body=payload, params={"id": id})
    return response


# ============================================================================
# device subtopic - device pair and replication link operations
# ============================================================================

def device_pair_list(client: DMEAPIClient, storage_id: str = None,
                     local_storage_name: str = None,
                     remote_storage_name: str = None,
                     health_status: str = None,
                     running_status: str = None,
                     page_no: int = None, page_size: int = None) -> dict:
    url = "/rest/protection/v1/device-pairs/query"

    payload = {}

    if storage_id is not None:
        payload['storage_id'] = storage_id
    if local_storage_name is not None:
        payload['local_storage_name'] = local_storage_name
    if remote_storage_name is not None:
        payload['remote_storage_name'] = remote_storage_name
    if health_status is not None:
        payload['health_status'] = health_status
    if running_status is not None:
        payload['running_status'] = running_status
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size

    response = client.post(url, body=payload)
    return response


def replication_link_list(client: DMEAPIClient, local_storage_id: str = None,
                          page_no: int = None, page_size: int = None,
                          health_status: str = None,
                          running_status: str = None,
                          link_type: str = None) -> dict:
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
# snapshot subtopic - LUN snapshot operations
# ============================================================================

def snapshot_list(client: DMEAPIClient, snapshot_ids: list = None, storage_id: str = None,
                  raw_id: str = None, name: str = None, health_status: str = None,
                  running_status: str = None, source_lun_name: str = None,
                  parent_name: str = None, activated_time_from: int = None,
                  activated_time_to: int = None, page_no: int = 1, page_size: int = 20) -> dict:
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
    url = "/rest/protection/v1/lun-snapshots"

    payload = {
        'snapshots_info': snapshots_info
    }

    if is_consist_activate is not None:
        payload['is_consist_activate'] = is_consist_activate

    response = client.post(url, body=payload)
    return response


def snapshot_rollback(client: DMEAPIClient, rollback_speed: str, rollback_snapshots: list) -> dict:
    url = "/rest/protection/v1/lun-snapshots/batch-rollback"

    payload = {
        'rollback_speed': rollback_speed,
        'rollback_snapshots': rollback_snapshots
    }

    response = client.post(url, body=payload)
    return response


def snapshot_delete(client: DMEAPIClient, snapshot_ids: list, is_delete_target_lun: bool = None,
                    is_auto_deactivate: bool = None) -> dict:
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
# snapshot_group subtopic - snapshot consistency group operations
# ============================================================================

def snapshot_group_create(client: DMEAPIClient, name: str, protect_group_id: str,
                          description: str = None, creation_mode: str = None) -> dict:
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
# clone_group subtopic - clone consistency group operations
# ============================================================================

def clone_group_create(client: DMEAPIClient, name: str, protect_group_id: str,
                       create_mode: str, description: str = None, name_rule: str = None,
                       name_prefix: str = None, name_suffix: str = None,
                       copy_rate: str = None, is_sync: bool = None,
                       clone_pairs: list = None) -> dict:
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
# replication_group subtopic - replication consistency group operations
# ============================================================================

def replication_group_create(client: DMEAPIClient, cg_name: str, remote_storage_id: str,
                              local_pg_id: str = None, description: str = None,
                              remote_lun_group_id: str = None, local_storage_id: str = None,
                              create_mode: str = None, existed_pair_ids: list = None,
                              lun_pairs: list = None, lun_ids: list = None,
                              remote_storage_pool_id: str = None, remote_vstore_id: str = None,
                              remote_resource_name_rule: str = None, name_prefix: str = None,
                              name_suffix: str = None, replication_mode: str = None,
                              sync_type: str = None, timing_val: int = None,
                              sync_schedule: dict = None, is_backup: bool = None,
                              speed: str = None, bandwidth: int = None,
                              recovery_policy: str = None, first_sync_policy: str = None,
                              enable_compress: bool = None, rep_io_timeout: int = None,
                              sync_snap_policy: str = None, user_snap_retention_num: int = None,
                              is_auto_sync: bool = None) -> dict:
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
    if replication_mode is not None:
        payload['replication_mode'] = replication_mode
    if sync_type is not None:
        payload['sync_type'] = sync_type
    if timing_val is not None:
        payload['timing_val'] = timing_val
    if sync_schedule is not None:
        payload['sync_schedule'] = sync_schedule
    if is_backup is not None:
        payload['is_backup'] = is_backup
    if speed is not None:
        payload['speed'] = speed
    if bandwidth is not None:
        payload['bandwidth'] = bandwidth
    if recovery_policy is not None:
        payload['recovery_policy'] = recovery_policy
    if first_sync_policy is not None:
        payload['first_sync_policy'] = first_sync_policy
    if enable_compress is not None:
        payload['enable_compress'] = enable_compress
    if rep_io_timeout is not None:
        payload['rep_io_timeout'] = rep_io_timeout
    if sync_snap_policy is not None:
        payload['sync_snap_policy'] = sync_snap_policy
    if user_snap_retention_num is not None:
        payload['user_snap_retention_num'] = user_snap_retention_num
    if is_auto_sync is not None:
        payload['is_auto_sync'] = is_auto_sync

    response = client.post(url, body=payload)
    return response


def replication_group_modify(client: DMEAPIClient, replication_group_id: str, name: str = None,
                              description: str = None, speed: str = None, bandwidth: int = None,
                              recovery_policy: str = None, enable_compress: bool = None,
                              sync_type: str = None, timing_value_in_sec: int = None,
                              sync_schedule: dict = None, rep_io_timeout: int = None,
                              sync_snap_policy: str = None, user_snap_retention_num: int = None,
                              switch_to_async: bool = None,
                              switch_to_sync: bool = None,
                              async_to_sync_bandwidth: int = None,
                              async_to_sync_latency: int = None,
                              sync_to_async_bandwidth: int = None,
                              sync_to_async_latency: int = None,
                              transfer_cycle: int = None) -> dict:
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
    if switch_to_sync is not None:
        payload['switch_to_sync'] = switch_to_sync
    if async_to_sync_bandwidth is not None:
        payload['async_to_sync_bandwidth'] = async_to_sync_bandwidth
    if async_to_sync_latency is not None:
        payload['async_to_sync_latency'] = async_to_sync_latency
    if sync_to_async_bandwidth is not None:
        payload['sync_to_async_bandwidth'] = sync_to_async_bandwidth
    if sync_to_async_latency is not None:
        payload['sync_to_async_latency'] = sync_to_async_latency
    if transfer_cycle is not None:
        payload['transfer_cycle'] = transfer_cycle

    response = client.put(url, body=payload, params={"replication_group_id": replication_group_id})
    return response


def replication_group_delete(client: DMEAPIClient, ids: list, is_self_adapt: bool = None,
                              delete_mode: str = None) -> dict:
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
    url = "/rest/protection/v1/replication/groups/{group_id}/add-pairs"

    payload = {
        'pair_ids': pair_ids
    }

    response = client.post(url, body=payload, params={"group_id": group_id})
    return response


def replication_group_remove_pairs(client: DMEAPIClient, group_id: str, pair_ids: list) -> dict:
    url = "/rest/protection/v1/replication/groups/{group_id}/remove-pairs"

    payload = {
        'pair_ids': pair_ids
    }

    response = client.post(url, body=payload, params={"group_id": group_id})
    return response


def replication_group_sync(client: DMEAPIClient, ids: list) -> dict:
    url = "/rest/protection/v1/replication/groups/sync"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def replication_group_split(client: DMEAPIClient, ids: list) -> dict:
    url = "/rest/protection/v1/replication/groups/split"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def replication_group_switch(client: DMEAPIClient, ids: list) -> dict:
    url = "/rest/protection/v1/replication/groups/switch"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def replication_group_switch_write_protection(client: DMEAPIClient, id: str, operation_type: str) -> dict:
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
# Filesystem hypermetro pair (fs_hypermetro_pair) subtopic functions
# ============================================================================


def fs_hypermetro_pair_create(client: DMEAPIClient, vstore_pair_id: str,
                            create_mode: str = "manual", fs_pairs: list = None,
                            speed: str = None, bandwidth: int = None,
                            service_assurance_policy: str = None,
                            isolation_threshold_time: int = None,
                            recovery_policy: str = None,
                            first_sync_policy: str = None) -> dict:
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
    if recovery_policy is not None:
        payload['recovery_policy'] = recovery_policy
    if first_sync_policy is not None:
        payload['first_sync_policy'] = first_sync_policy

    response = client.post(url, body=payload)
    return response


def fs_hypermetro_pair_list(client: DMEAPIClient, ids: list = None, name: str = None,
                          status: str = None, storage_id: str = None,
                          vstore_pair_id: str = None, local_fs_name: str = None,
                          local_fs_id: str = None, health_status: str = None,
                          running_status: str = None, sort_key: str = None,
                          sort_dir: str = None, page_no: int = 1,
                          page_size: int = 10,
                          pair_raw_id: str = None,
                          local_filesystem_raw_id: str = None,
                          remote_filesystem_raw_id: str = None,
                          remote_filesystem_name: str = None,
                          is_primary: bool = None,
                          local_host_access_state: str = None,
                          remote_host_access_state: str = None,
                          recovery_policy: str = None,
                          link_status: str = None,
                          sync_direction: str = None) -> dict:
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
    if pair_raw_id is not None:
        payload['pair_raw_id'] = pair_raw_id
    if local_filesystem_raw_id is not None:
        payload['local_filesystem_raw_id'] = local_filesystem_raw_id
    if remote_filesystem_raw_id is not None:
        payload['remote_filesystem_raw_id'] = remote_filesystem_raw_id
    if remote_filesystem_name is not None:
        payload['remote_filesystem_name'] = remote_filesystem_name
    if is_primary is not None:
        payload['is_primary'] = is_primary
    if local_host_access_state is not None:
        payload['local_host_access_state'] = local_host_access_state
    if remote_host_access_state is not None:
        payload['remote_host_access_state'] = remote_host_access_state
    if recovery_policy is not None:
        payload['recovery_policy'] = recovery_policy
    if link_status is not None:
        payload['link_status'] = link_status
    if sync_direction is not None:
        payload['sync_direction'] = sync_direction

    response = client.post(url, body=payload)
    return response


def fs_hypermetro_pair_pause(client: DMEAPIClient, fs_pair_ids: list) -> dict:
    url = "/rest/protection/v1/hypermetro/filesystem-pairs/pause"

    if not fs_pair_ids or len(fs_pair_ids) == 0:
        raise ValueError("fs_pair_ids is required")

    payload = {
        'fs_pair_ids': fs_pair_ids
    }

    response = client.post(url, body=payload)
    return response


def fs_hypermetro_pair_sync(client: DMEAPIClient, fs_pair_ids: list) -> dict:
    url = "/rest/protection/v1/hypermetro/filesystem-pairs/sync"

    if not fs_pair_ids or len(fs_pair_ids) == 0:
        raise ValueError("fs_pair_ids is required")

    payload = {
        'fs_pair_ids': fs_pair_ids
    }

    response = client.post(url, body=payload)
    return response


def fs_hypermetro_pair_delete(client: DMEAPIClient, ids: list,
                            is_local_delete: bool = None,
                            is_online_delete: bool = None) -> dict:
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
    url = "/rest/protection/v1/filesystem-snapshots/delete"

    if not ids or len(ids) == 0:
        raise ValueError("ids is required")

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


# ============================================================================
# Hypermetro tenant pair (vstore_hypermetro_pair) subtopic functions
# ============================================================================


def vstore_pair_force_start(client: DMEAPIClient, ids: list) -> dict:
    url = "/rest/protection/v1/metro/vstore-pairs/force-start"

    if not ids or len(ids) == 0:
        raise ValueError("ids is required")

    payload = {
        'vstore_pair_ids': ids
    }

    response = client.post(url, body=payload)
    return response


def vstore_pair_create(client: DMEAPIClient, domain_id: str,
                        local_vstore_id: str,
                        remote_vstore_id: str,
                        preferred_mode: str,
                        preferred_site: str = None) -> dict:
    url = "/rest/protection/v1/metro/vstore-pairs"

    if not domain_id or not local_vstore_id or not remote_vstore_id or not preferred_mode:
        raise ValueError("domain_id, local_vstore_id, remote_vstore_id, preferred_mode are required")

    payload = {
        'domain_id': domain_id,
        'local_vstore_id': local_vstore_id,
        'remote_vstore_id': remote_vstore_id,
        'preferred_mode': preferred_mode
    }
    if preferred_site is not None:
        payload['preferred_site'] = preferred_site

    response = client.post(url, body=payload)
    return response


def vstore_pair_list(client: DMEAPIClient, ids: list = None, name: str = None,
                      status: str = None, local_storage_id: str = None,
                      remote_storage_id: str = None,
                      health_status: str = None, running_status: str = None,
                      page_no: int = 1, page_size: int = 10,
                      raw_id: str = None,
                      local_vstore_name: str = None,
                      local_vstore_raw_id: str = None,
                      remote_vstore_name: str = None,
                      remote_vstore_raw_id: str = None,
                      domain_id: str = None,
                      domain_name: str = None,
                      config_status: str = None,
                      link_status: str = None,
                      role: str = None,
                      active_status: str = None,
                      sort_key: str = None,
                      sort_dir: str = None) -> dict:
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
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if local_vstore_name is not None:
        payload['local_vstore_name'] = local_vstore_name
    if local_vstore_raw_id is not None:
        payload['local_vstore_raw_id'] = local_vstore_raw_id
    if remote_vstore_name is not None:
        payload['remote_vstore_name'] = remote_vstore_name
    if remote_vstore_raw_id is not None:
        payload['remote_vstore_raw_id'] = remote_vstore_raw_id
    if domain_id is not None:
        payload['domain_id'] = domain_id
    if domain_name is not None:
        payload['domain_name'] = domain_name
    if config_status is not None:
        payload['config_status'] = config_status
    if link_status is not None:
        payload['link_status'] = link_status
    if role is not None:
        payload['role'] = role
    if active_status is not None:
        payload['active_status'] = active_status
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def vstore_pair_switch(client: DMEAPIClient, ids: list, is_force: bool = None) -> dict:
    url = "/rest/protection/v1/metro/vstore-pairs/switch"

    if not ids or len(ids) == 0:
        raise ValueError("ids is required")

    payload = {
        'vstore_pair_ids': ids
    }
    if is_force is not None:
        payload['is_force'] = is_force

    response = client.post(url, body=payload)
    return response


def vstore_pair_delete(client: DMEAPIClient, ids: list) -> dict:
    url = "/rest/protection/v1/metro/vstore-pairs/delete"

    if not ids or len(ids) == 0:
        raise ValueError("ids is required")

    payload = {
        'vstore_pair_ids': ids
    }

    response = client.post(url, body=payload)
    return response


def vstore_pair_modify(client: DMEAPIClient, id: str,
                         preferred_mode: str,
                         preferred_site: str = None) -> dict:
    url = "/rest/protection/v1/metro/vstore-pairs/{id}"

    if not id:
        raise ValueError("id is required")

    payload = {
        'preferred_mode': preferred_mode
    }
    if preferred_site is not None:
        payload['preferred_site'] = preferred_site

    response = client.put(url, body=payload, params={"id": id})
    return response


# ============================================================================
# Hypermetro domain (hypermetro_domain) subtopic functions
# ============================================================================


def fs_domain_force_start(client: DMEAPIClient, id: str) -> dict:
    url = "/rest/protection/v1/hyper-metro-domains/{id}/force-start"

    if not id:
        raise ValueError("id is required")

    response = client.post(url, body={}, params={"id": id})
    return response


def fs_domain_switch_site(client: DMEAPIClient, id: str) -> dict:
    url = "/rest/protection/v1/hyper-metro-domains/{id}/switch-priority-site"

    if not id:
        raise ValueError("id is required")

    response = client.post(url, body={}, params={"id": id})
    return response


def fs_domain_recover(client: DMEAPIClient, id: str) -> dict:
    url = "/rest/protection/v1/hyper-metro-domains/{id}/recover"

    if not id:
        raise ValueError("id is required")

    response = client.post(url, body={}, params={"id": id})
    return response


def fs_domain_split(client: DMEAPIClient, id: str, stop_role: str = None) -> dict:
    url = "/rest/protection/v1/hyper-metro-domains/{id}/split"

    if not id:
        raise ValueError("id is required")

    payload = {}
    if stop_role is not None:
        payload['stop_role'] = stop_role

    response = client.post(url, body=payload, params={"id": id})
    return response


def fs_domain_swap_role(client: DMEAPIClient, id: str) -> dict:
    url = "/rest/protection/v1/hyper-metro-domains/{id}/swap-role"

    if not id:
        raise ValueError("id is required")

    response = client.post(url, body={}, params={"id": id})
    return response


# ============================================================================
# Hypermetro pair (hypermetro_pair) subtopic functions
# ============================================================================


def hypermetro_pair_query_available_luns(client: DMEAPIClient,
                                          source_lun_id: str,
                                          remote_storage_id: str = None,
                                          name: str = None,
                                          vstore_id: str = None,
                                          vstore_raw_id: str = None,
                                          remote_lun_group_id: str = None,
                                          page_no: int = None,
                                          page_size: int = None) -> dict:
    url = "/rest/protection/v1/metro/lun-pairs/{source_lun_id}/optional-target-luns"

    if not source_lun_id:
        raise ValueError("source_lun_id is required")

    payload = {}
    if remote_storage_id is not None:
        payload['remote_storage_id'] = remote_storage_id
    if name is not None:
        payload['name'] = name
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if remote_lun_group_id is not None:
        payload['remote_lun_group_id'] = remote_lun_group_id
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size

    response = client.post(url, body=payload, params={"source_lun_id": source_lun_id})
    return response


# Action list for CLI help
ACTIONS = {
    # group subtopic actions
    'group_list': {
        'func': group_list,
        'params': ['name', 'project_id', 'storage_name', 'storage_id', 'raw_id', 'lun_group_raw_id', 'vstore_id', 'vstore_raw_id', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'group'
    },
    'group_create': {
        'func': group_create,
        'params': ['name', 'storage_id', 'lun_ids', 'lun_group_id', 'description'],
        'subtopic': 'group'
    },
    'group_modify': {
        'func': group_modify,
        'params': ['pg_id', 'name', 'description'],
        'subtopic': 'group'
    },
    'group_delete': {
        'func': group_delete,
        'params': ['pg_ids'],
        'subtopic': 'group'
    },
    'group_add_luns': {
        'func': group_add_luns,
        'params': ['pg_id', 'lun_ids', 'hyper_metro', 'rem_reps'],
        'subtopic': 'group'
    },
    'group_remove_luns': {
        'func': group_remove_luns,
        'params': ['pg_id', 'lun_ids', 'is_delay'],
        'subtopic': 'group'
    },
    # hypermetro_group subtopic actions
    'hypermetro_group_list': {
        'func': hypermetro_group_list,
        'params': ['page_no', 'page_size', 'name', 'raw_id', 'protect_group_id', 'storage_id', 'storage_name', 'local_vstore_id', 'local_vstore_raw_id', 'remote_vstore_id', 'remote_vstore_raw_id', 'domain_name', 'health_status', 'running_status', 'priority_station_type'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_create': {
        'func': hypermetro_group_create,
        'params': ['domain_id', 'name', 'local_storage_id', 'local_pg_id', 'description', 'create_mode', 'remote_vstore_id', 'remote_storage_pool_id', 'lun_ids', 'remote_resource_name_rule', 'name_prefix', 'name_suffix', 'service_assurance_policy', 'recovery_policy', 'speed', 'bandwidth', 'first_sync_policy', 'remote_lun_group_id', 'lun_pairs', 'existed_pair_ids', 'is_auto_pause', 'is_auto_sync', 'isolation_threshold_time'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_modify': {
        'func': hypermetro_group_modify,
        'params': ['group_id', 'name', 'description', 'recovery_policy', 'service_assurance_policy', 'speed', 'bandwidth', 'isolation_threshold_time'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_delete': {
        'func': hypermetro_group_delete,
        'params': ['ids', 'is_self_adapt', 'delete_mode'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_add_pairs': {
        'func': hypermetro_group_add_pairs,
        'params': ['group_id', 'pair_ids', 'is_self_adapt'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_remove_pairs': {
        'func': hypermetro_group_remove_pairs,
        'params': ['group_id', 'pair_ids'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_pause': {
        'func': hypermetro_group_pause,
        'params': ['ids', 'priority_station_type'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_force_startup': {
        'func': hypermetro_group_force_startup,
        'params': ['ids', 'priority_station_type'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_switch_priority': {
        'func': hypermetro_group_switch_priority,
        'params': ['ids'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_sync': {
        'func': hypermetro_group_sync,
        'params': ['ids'],
        'subtopic': 'hypermetro_group'
    },
    # hypermetro_pair subtopic actions
    'hypermetro_pair_list': {
        'func': hypermetro_pair_list,
        'params': ['page_no', 'page_size', 'group_id', 'group_name', 'group_raw_id', 'pair_raw_id', 'local_storage_id', 'local_storage_name', 'local_vstore_id', 'local_vstore_raw_id', 'local_volume_name', 'local_host_access_state', 'remote_vstore_id', 'remote_vstore_raw_id', 'remote_volume_name'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_create': {
        'func': hypermetro_pair_create,
        'params': ['create_mode', 'lun_pairs', 'lun_ids', 'remote_storage_pool_id', 'remote_vstore_id', 'remote_resource_name_rule', 'name_prefix', 'name_suffix', 'local_storage_id', 'domain_id', 'speed', 'bandwidth', 'service_assurance_policy', 'isolation_threshold_time', 'recovery_policy'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_modify': {
        'func': hypermetro_pair_modify,
        'params': ['pair_id', 'speed', 'bandwidth', 'recovery_policy', 'service_assurance_policy', 'isolation_threshold_time'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_delete': {
        'func': hypermetro_pair_delete,
        'params': ['ids', 'delete_mode', 'is_lun_service_interrupt'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_sync': {
        'func': hypermetro_pair_sync,
        'params': ['ids'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_pause': {
        'func': hypermetro_pair_pause,
        'params': ['ids', 'priority_station_type'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_force_startup': {
        'func': hypermetro_pair_force_startup,
        'params': ['ids', 'priority_station_type'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_switch_priority': {
        'func': hypermetro_pair_switch_priority,
        'params': ['ids'],
        'subtopic': 'hypermetro_pair'
    },
    # hypermetro_domain subtopic actions
    'hypermetro_domain_list': {
        'func': hypermetro_domain_list,
        'params': ['storage_id', 'types'],
        'subtopic': 'hypermetro_domain'
    },
    # replication_group subtopic actions
    'replication_group_create': {
        'func': replication_group_create,
        'params': ['cg_name', 'remote_storage_id', 'local_pg_id', 'description', 'remote_lun_group_id', 'local_storage_id', 'create_mode', 'existed_pair_ids', 'lun_pairs', 'lun_ids', 'remote_storage_pool_id', 'remote_vstore_id', 'remote_resource_name_rule', 'name_prefix', 'name_suffix', 'replication_mode', 'sync_type', 'timing_val', 'sync_schedule', 'is_backup', 'speed', 'bandwidth', 'recovery_policy', 'first_sync_policy', 'enable_compress', 'rep_io_timeout', 'sync_snap_policy', 'user_snap_retention_num', 'is_auto_sync'],
        'subtopic': 'replication_group'
    },
    'replication_group_list': {
        'func': replication_group_list,
        'params': ['page_no', 'page_size', 'protect_group_id', 'name', 'raw_id', 'running_status', 'health_status', 'storage_name', 'storage_id', 'replication_mode'],
        'subtopic': 'replication_group'
    },
    'replication_group_modify': {
        'func': replication_group_modify,
        'params': ['replication_group_id', 'name', 'description', 'speed', 'bandwidth', 'recovery_policy', 'enable_compress', 'sync_type', 'timing_value_in_sec', 'sync_schedule', 'rep_io_timeout', 'sync_snap_policy', 'user_snap_retention_num', 'switch_to_async', 'switch_to_sync', 'async_to_sync_bandwidth', 'async_to_sync_latency', 'sync_to_async_bandwidth', 'sync_to_async_latency', 'transfer_cycle'],
        'subtopic': 'replication_group'
    },
    'replication_group_delete': {
        'func': replication_group_delete,
        'params': ['ids', 'is_self_adapt', 'delete_mode'],
        'subtopic': 'replication_group'
    },
    'replication_group_add_pairs': {
        'func': replication_group_add_pairs,
        'params': ['group_id', 'pair_ids'],
        'subtopic': 'replication_group'
    },
    'replication_group_remove_pairs': {
        'func': replication_group_remove_pairs,
        'params': ['group_id', 'pair_ids'],
        'subtopic': 'replication_group'
    },
    'replication_group_sync': {
        'func': replication_group_sync,
        'params': ['ids'],
        'subtopic': 'replication_group'
    },
    'replication_group_split': {
        'func': replication_group_split,
        'params': ['ids'],
        'subtopic': 'replication_group'
    },
    'replication_group_switch': {
        'func': replication_group_switch,
        'params': ['ids'],
        'subtopic': 'replication_group'
    },
    'replication_group_switch_write_protection': {
        'func': replication_group_switch_write_protection,
        'params': ['id', 'operation_type'],
        'subtopic': 'replication_group'
    },
    # replication_pair subtopic actions
    'replication_pair_list': {
        'func': replication_pair_list,
        'params': ['page_no', 'page_size', 'raw_id', 'local_resource_types', 'local_vstore_raw_id', 'group_id', 'group_name', 'group_raw_id', 'local_resource_raw_id', 'local_resource_raw_ids', 'local_resource_name', 'remote_resource_name', 'local_storage_id', 'local_storage_name', 'health_status', 'running_status', 'recovery_policy', 'sort_key', 'sort_dir'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_create': {
        'func': replication_pair_create,
        'params': ['local_storage_id', 'remote_storage_id', 'create_mode', 'replication_mode', 'resource_pairs', 'remote_storage_pool_id', 'remote_vstore_id', 'remote_resource_name_rule', 'name_prefix', 'name_suffix', 'speed', 'bandwidth', 'recovery_policy', 'first_sync_policy', 'sync_type', 'timing_val', 'sync_schedule', 'rep_io_timeout', 'sync_snap_policy', 'user_snap_retention_num', 'snap_tag_list', 'enable_compress', 'is_backup', 'switch_to_async', 'consistency_group_info'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_modify': {
        'func': replication_pair_modify,
        'params': ['pair_id', 'speed', 'bandwidth', 'recovery_policy', 'enable_compress', 'secondary_res_protection', 'sync_type', 'timing_val', 'sync_schedule', 'rep_io_timeout', 'sync_snap_policy', 'user_snap_retention_num', 'snap_tag_list', 'switch_to_async', 'switch_to_sync', 'sync_to_async_bandwidth', 'sync_to_async_latency', 'async_to_sync_bandwidth', 'async_to_sync_latency', 'transfer_cycle'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_delete': {
        'func': replication_pair_delete,
        'params': ['ids', 'delete_mode', 'is_enforce_secondary_data'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_sync': {
        'func': replication_pair_sync,
        'params': ['ids'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_split': {
        'func': replication_pair_split,
        'params': ['ids'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_switch': {
        'func': replication_pair_switch,
        'params': ['ids'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_switch_write_protection': {
        'func': replication_pair_switch_write_protection,
        'params': ['id', 'operation_type'],
        'subtopic': 'replication_pair'
    },
    # device subtopic actions
    'device_pair_list': {
        'func': device_pair_list,
        'params': ['storage_id', 'local_storage_name', 'remote_storage_name', 'health_status', 'running_status', 'page_no', 'page_size'],
        'subtopic': 'device_pair'
    },
    'replication_link_list': {
        'func': replication_link_list,
        'params': ['local_storage_id', 'page_no', 'page_size', 'health_status', 'running_status', 'link_type'],
        'subtopic': 'replication_link'
    },
    # snapshot subtopic actions
    'snapshot_list': {
        'func': snapshot_list,
        'params': ['snapshot_ids', 'storage_id', 'raw_id', 'name', 'health_status', 'running_status', 'source_lun_name', 'parent_name', 'activated_time_from', 'activated_time_to', 'page_no', 'page_size'],
        'subtopic': 'snapshot'
    },
    'snapshot_create': {
        'func': snapshot_create,
        'params': ['snapshots_info', 'is_consist_activate'],
        'subtopic': 'snapshot'
    },
    'snapshot_rollback': {
        'func': snapshot_rollback,
        'params': ['rollback_speed', 'rollback_snapshots'],
        'subtopic': 'snapshot'
    },
    'snapshot_delete': {
        'func': snapshot_delete,
        'params': ['snapshot_ids', 'is_delete_target_lun', 'is_auto_deactivate'],
        'subtopic': 'snapshot'
    },
    # snapshot_group subtopic actions
    'snapshot_group_create': {
        'func': snapshot_group_create,
        'params': ['name', 'protect_group_id', 'description', 'creation_mode'],
        'subtopic': 'snapshot_group'
    },
    'snapshot_group_delete': {
        'func': snapshot_group_delete,
        'params': ['snapshot_cg_ids', 'is_delete_target_lun'],
        'subtopic': 'snapshot_group'
    },
    'snapshot_group_activate': {
        'func': snapshot_group_activate,
        'params': ['snapshot_cg_id', 'object_type', 'snapshot_create_mode', 'name_rule', 'name_prefix', 'name_suffix', 'target_snapshot_objects'],
        'subtopic': 'snapshot_group'
    },
    'snapshot_group_deactivate': {
        'func': snapshot_group_deactivate,
        'params': ['snapshot_cg_ids'],
        'subtopic': 'snapshot_group'
    },
    'snapshot_group_rollback': {
        'func': snapshot_group_rollback,
        'params': ['snapshot_cg_id', 'rollback_speed', 'snapshot_create_mode', 'name_rule', 'name_prefix', 'name_suffix', 'target_snapshot_objects'],
        'subtopic': 'snapshot_group'
    },
    # clone_group subtopic actions
    'clone_group_create': {
        'func': clone_group_create,
        'params': ['name', 'protect_group_id', 'create_mode', 'description', 'name_rule', 'name_prefix', 'name_suffix', 'copy_rate', 'is_sync', 'clone_pairs'],
        'subtopic': 'clone_group'
    },
    'clone_group_sync': {
        'func': clone_group_sync,
        'params': ['clone_cg_id', 'create_mode', 'name_rule', 'name_prefix', 'name_suffix', 'clone_pairs'],
        'subtopic': 'clone_group'
    },
    'clone_group_delete': {
        'func': clone_group_delete,
        'params': ['ids', 'is_delete_dst_lun', 'is_recycle_dst_lun_data'],
        'subtopic': 'clone_group'
    },
    # fs_hypermetro_pair subtopic actions
    'fs_hypermetro_pair_create': {
        'func': fs_hypermetro_pair_create,
        'params': ['vstore_pair_id', 'create_mode', 'fs_pairs', 'speed', 'bandwidth', 'service_assurance_policy', 'isolation_threshold_time', 'recovery_policy', 'first_sync_policy'],
        'subtopic': 'fs_hypermetro_pair'
    },
    'fs_hypermetro_pair_list': {
        'func': fs_hypermetro_pair_list,
        'params': ['ids', 'name', 'status', 'storage_id', 'vstore_pair_id', 'local_fs_name', 'local_fs_id', 'health_status', 'running_status', 'sort_key', 'sort_dir', 'page_no', 'page_size', 'pair_raw_id', 'local_filesystem_raw_id', 'remote_filesystem_raw_id', 'remote_filesystem_name', 'is_primary', 'local_host_access_state', 'remote_host_access_state', 'recovery_policy', 'link_status', 'sync_direction'],
        'subtopic': 'fs_hypermetro_pair'
    },
    'fs_hypermetro_pair_pause': {
        'func': fs_hypermetro_pair_pause,
        'params': ['fs_pair_ids'],
        'subtopic': 'fs_hypermetro_pair'
    },
    'fs_hypermetro_pair_sync': {
        'func': fs_hypermetro_pair_sync,
        'params': ['fs_pair_ids'],
        'subtopic': 'fs_hypermetro_pair'
    },
    'fs_hypermetro_pair_delete': {
        'func': fs_hypermetro_pair_delete,
        'params': ['ids', 'is_local_delete', 'is_online_delete'],
        'subtopic': 'fs_hypermetro_pair'
    },
    # fs_snapshot subtopic actions
    'fs_snapshot_create': {
        'func': fs_snapshot_create,
        'params': ['vstore_pair_id', 'fs_pairs'],
        'subtopic': 'fs_snapshot'
    },
    'fs_snapshot_list': {
        'func': fs_snapshot_list,
        'params': ['fs_pair_id', 'name', 'status', 'local_fs_name', 'local_fs_id', 'page_no', 'page_size'],
        'subtopic': 'fs_snapshot'
    },
    'fs_snapshot_delete': {
        'func': fs_snapshot_delete,
        'params': ['ids'],
        'subtopic': 'fs_snapshot'
    },
    # vstore_hypermetro_pair subtopic actions
    'vstore_hypermetro_pair_force_start': {
        'func': vstore_pair_force_start,
        'params': ['ids'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    'vstore_hypermetro_pair_create': {
        'func': vstore_pair_create,
        'params': ['domain_id', 'local_vstore_id', 'remote_vstore_id', 'preferred_mode', 'preferred_site'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    'vstore_hypermetro_pair_list': {
        'func': vstore_pair_list,
        'params': ['ids', 'name', 'status', 'local_storage_id', 'remote_storage_id', 'health_status', 'running_status', 'page_no', 'page_size', 'raw_id', 'local_vstore_name', 'local_vstore_raw_id', 'remote_vstore_name', 'remote_vstore_raw_id', 'domain_id', 'domain_name', 'config_status', 'link_status', 'role', 'active_status', 'sort_key', 'sort_dir'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    'vstore_hypermetro_pair_switch': {
        'func': vstore_pair_switch,
        'params': ['ids', 'is_force'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    'vstore_hypermetro_pair_delete': {
        'func': vstore_pair_delete,
        'params': ['ids'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    'vstore_hypermetro_pair_modify': {
        'func': vstore_pair_modify,
        'params': ['id', 'preferred_mode', 'preferred_site'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    # hypermetro_domain subtopic actions
    # fs_hypermetro_domain subtopic (filesystem hypermetro domain specific operations)
    'fs_hypermetro_domain_force_start': {
        'func': fs_domain_force_start,
        'params': ['id'],
        'subtopic': 'fs_hypermetro_domain'
    },
    'fs_hypermetro_domain_switch_site': {
        'func': fs_domain_switch_site,
        'params': ['id'],
        'subtopic': 'fs_hypermetro_domain'
    },
    'fs_hypermetro_domain_recover': {
        'func': fs_domain_recover,
        'params': ['id'],
        'subtopic': 'fs_hypermetro_domain'
    },
    'fs_hypermetro_domain_split': {
        'func': fs_domain_split,
        'params': ['id', 'stop_role'],
        'subtopic': 'fs_hypermetro_domain'
    },
    'fs_hypermetro_domain_swap_role': {
        'func': fs_domain_swap_role,
        'params': ['id'],
        'subtopic': 'fs_hypermetro_domain'
    },
    # hypermetro_pair subtopic actions
    'hypermetro_pair_query_available_luns': {
        'func': hypermetro_pair_query_available_luns,
        'params': ['source_lun_id', 'remote_storage_id', 'name', 'vstore_id', 'vstore_raw_id', 'remote_lun_group_id', 'page_no', 'page_size'],
        'subtopic': 'hypermetro_pair'
    },
}
