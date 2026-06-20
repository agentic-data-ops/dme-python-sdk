"""
GFS (Global File System) related operations
"""

import sys
import os

from pydme.client import DMEAPIClient


# ============================================================================
# Dataspace subtopic related actions
# ============================================================================

def dataspace_list(client: DMEAPIClient, name: str = None, id: str = None,
                   raw_id: str = None, max_site_num: int = None,
                   page_no: int = 1, page_size: int = 100) -> dict:
    """
    Batch query Omni-Dataverse

    Args:
        client: DME API client
        name: Omni-Dataverse name, supports fuzzy query
        id: Omni-Dataverse id
        raw_id: Omni-Dataverse id on the device side
        max_site_num: Maximum count of data service sites under Omni-Dataverse
        page_no: Page number for paginated query, default 1, range 1~10000
        page_size: Number of items per page for paginated query, default 100, range 1~1000

    Returns:
        {
            total: total (integer),
            gfs_groups: Omni-Dataverse list. parameter format: [{
                id: ID (string),
                name: name (string),
                status: status (string),
            }, ...],
        }
    """
    url = "/rest/fileservice/v1/gfs-groups/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if name is not None:
        payload['name'] = name
    if id is not None:
        payload['id'] = id
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if max_site_num is not None:
        payload['max_site_num'] = max_site_num

    response = client.post(url, body=payload)
    return response


def dataspace_show(client: DMEAPIClient, id: str = None, name: str = None) -> dict:
    """
    Query capacity statistics info of the specified Omni-Dataverse

    Args:
        client: DME API client
        id: Omni-Dataverse ID, cannot be empty simultaneously with name, ID is used first when both have values
        name: Omni-Dataverse name, cannot be empty simultaneously with id, ID is used first when both have values

    Returns:
        {
            total_capacity: total capacity (string),
            used_capacity: used capacity (string),
            available_capacity: available capacity (string),
            file_count: file count (int64),
        }
    """
    url = "/rest/fileservice/v1/gfs-groups/query-summary"

    payload = {}

    if id is not None:
        payload['id'] = id
    if name is not None:
        payload['name'] = name

    response = client.post(url, body=payload)
    return response


def dataspace_site_list(client: DMEAPIClient, raw_id: str = None,
                        site_role: dict = None, gfs_group_id: str = None,
                        storage_name: str = None, storage_pool_name: str = None,
                        account_name: str = None, page_no: int = 1,
                        page_size: int = 100) -> dict:
    """
    Query Omni-Dataverse data service sites

    Args:
        client: DME API client
        raw_id: Data service site id on the device side
        site_role: Data service site role, contains site_role field. valid values: ORDINARY, METASTORE
        gfs_group_id: Omni-Dataverse id
        storage_name: Query data service sites by storage name, supports fuzzy query
        storage_pool_name: Query data service sites by storage pool name, supports fuzzy query
        account_name: Query data service sites by account name, supports fuzzy query
        page_no: Page number for paginated query, default 1, range 1~10000
        page_size: Number of items per page for paginated query, default 100, range 1~1000

    Returns:
        {
            total: site count (int32),
            sites: Data service site list (List<SiteInfo>). parameter format: [{
                id: site ID (string),
                name: site name (string),
                status: status (string),
            }, ...],
        }
    """
    url = "/rest/fileservice/v1/data-service-sites/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if raw_id is not None:
        payload['raw_id'] = raw_id
    if site_role is not None:
        payload['site_role'] = site_role
    if gfs_group_id is not None:
        payload['gfs_group_id'] = gfs_group_id
    if storage_name is not None:
        payload['storage_name'] = storage_name
    if storage_pool_name is not None:
        payload['storage_pool_name'] = storage_pool_name
    if account_name is not None:
        payload['account_name'] = account_name

    response = client.post(url, body=payload)
    return response


# ============================================================================
# Namespace subtopic related actions
# ============================================================================

def namespace_list(client: DMEAPIClient, name: str = None, gfs_group_name: str = None,
                   gfs_group_id: str = None, gfs_type: str = None,
                   sort_key: str = None, sort_dir: str = None,
                   page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch query global Namespace

    Args:
        client: DME API client
        name: Global Namespace name, supports fuzzy search (0~256 characters, Optional)
        gfs_group_name: Global dataspaces name, supports fuzzy search (0~256 characters, Optional)
        gfs_group_id: ID of the owning global dataspaces (1~32 characters, Optional)
        gfs_type: Global Namespace type (Optional). valid values: enable_object_multi_version, disable_object_multi_version
        sort_key: Sort by the specified field (Optional). valid values: child_name_space_num
        sort_dir: Specify sort direction (Optional). valid values: asc, desc. default: asc
        page_no: Pagination start page (int32, 1~1000, default: 1, Optional)
        page_size: Number of items per page (int32, 1~1000, default: 20, Optional)

    Returns:
        {
            total: Namespace count (int32),
            namespaces: Global Namespace list (List<NamespaceInfo>). parameter format: [{
                id: namespace ID (string),
                name: name (string),
                status: status (string),
            }, ...],
        }
    """
    url = "/rest/fileservice/v1/gfs/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if name is not None:
        payload['name'] = name
    if gfs_group_name is not None:
        payload['gfs_group_name'] = gfs_group_name
    if gfs_group_id is not None:
        payload['gfs_group_id'] = gfs_group_id
    if gfs_type is not None:
        payload['gfs_type'] = gfs_type
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def namespace_show(client: DMEAPIClient, id: str = None, name_locator: str = None) -> dict:
    """
    Query global Namespace details

    Args:
        client: DME API client
        id: Global Namespace ID, cannot be empty simultaneously with name_locator, ID is used first when both have values
        name_locator: Name locator, format: global Namespace name@global dataspaces name

    Returns:
        {
            id: namespace ID (string),
            name: name (string),
            description: description (string),
            status: status (string),
            storage_id: storage device ID (string),
        }
    """
    url = "/rest/fileservice/v1/gfs/detail/query"

    payload = {}

    if id is not None:
        payload['id'] = id
    if name_locator is not None:
        payload['name_locator'] = name_locator

    response = client.post(url, body=payload)
    return response


def namespace_create(client: DMEAPIClient, name: str, gfs_group_id: str = None,
                     gfs_group_name: str = None, gfs_mode: str = 'smart_share',
                     single_write_switch: str = None,
                     smart_share_members: list = None) -> dict:
    """
    Create global Namespace

    Args:
        client: DME API client
        name: Global namespace name (1~255 characters, Required)
        gfs_group_id: Global dataspaces ID (1~32 characters, Optional. Cannot be empty simultaneously with gfs_group_name, gfs_group_id is used first when both have values)
        gfs_group_name: Global dataspaces name (1~255 characters, Optional. Cannot be empty simultaneously with gfs_group_id, gfs_group_id is used first when both have values)
        gfs_mode: Global Namespace mode (Optional). valid values: smart_share. default: smart_share
        single_write_switch: Single write mode switch (Optional). valid values: close (any member can write), open (only one member can write)
        smart_share_members: SmartShare member list (List<SmartShareMember>, max array members: 32, Optional. Required when gfs_mode is smart_share). parameter format: [{
                id: Namespace ID (1~64 characters, Required),
                pull_mode: Data read mode (Optional). valid values: no_cache (forward read), on_demand (on-demand read). default: on_demand,
                cache_time: Cache duration (int32, Optional, default: 8). When cache_time_unit is hour: 1~4320, when day: 1~180,
                cache_time_unit: Cache duration unit (Optional). valid values: hour, day. Required when cache_time is set. default: hour,
                single_write_mode: Single write mode policy (Optional). valid values: read_only, read_write. When single_write_switch is open, exactly one member must have read_write,
             }, ...]

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/fileservice/v1/gfs"

    payload = {
        'name': name,
        'gfs_mode': gfs_mode
    }

    if gfs_group_id is not None:
        payload['gfs_group_id'] = gfs_group_id
    if gfs_group_name is not None:
        payload['gfs_group_name'] = gfs_group_name
    if single_write_switch is not None:
        payload['single_write_switch'] = single_write_switch
    if smart_share_members is not None:
        payload['smart_share_members'] = smart_share_members

    response = client.post(url, body=payload)
    return response


def namespace_modify(client: DMEAPIClient, id: str = None, name_locator: str = None,
                     smart_share_members: list = None) -> dict:
    """
    Modify the specified global Namespace

    Args:
        client: DME API client
        id: Global Namespace ID (1~32 characters, Optional. Cannot be empty simultaneously with name_locator, id is used first when both have values)
        name_locator: Name locator, format: global Namespace name@global dataspaces name (3~507 characters, Optional. Cannot be empty simultaneously with id, id is used first when both have values)
        smart_share_members: SmartShare member list (List<ModifySmartShareMember>, min array members: 0, max array members: 256, Optional. Valid when global Namespace mode is smart_share). parameter format: [{
                id: Namespace ID or Filesystem ID (1~64 characters, Required),
                pull_mode: Data read mode (Optional). valid values: no_cache (forward read), on_demand (on-demand read),
                cache_time: Cache duration (int32, Optional, default: 8). When cache_time_unit is hour: 1~4320, when day: 1~180,
                cache_time_unit: Cache duration unit (Optional). valid values: hour, day. Required when cache_time is set,
             }, ...]

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/fileservice/v1/gfs/modify"

    payload = {}

    if id is not None:
        payload['id'] = id
    if name_locator is not None:
        payload['name_locator'] = name_locator
    if smart_share_members is not None:
        payload['smart_share_members'] = smart_share_members

    response = client.post(url, body=payload)
    return response


def namespace_delete(client: DMEAPIClient, id: str = None, name_locator: str = None,
                     is_delete_child: bool = True) -> dict:
    """
    Delete the specified global Namespace

    Args:
        client: DME API client
        id: Global Namespace ID, cannot be empty simultaneously with name_locator
        name_locator: Name locator, format: global Namespace name@global dataspaces name
        is_delete_child: Whether to delete child Namespace, default true

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/fileservice/v1/gfs/delete"

    payload = {
        'is_delete_child': is_delete_child
    }

    if id is not None:
        payload['id'] = id
    if name_locator is not None:
        payload['name_locator'] = name_locator

    response = client.post(url, body=payload)
    return response


# ============================================================================
# Migration Task subtopic related actions
# ============================================================================

def migration_task_list(client: DMEAPIClient, gfs_id: str = None,
                        task_name: str = None, task_id: str = None,
                        target_storage_name: str = None, namespace_name: str = None,
                        namespace_id: str = None, namespace_raw_id: str = None,
                        local_path: str = None, status: list = None,
                        task_mode: list = None, execute_mode: list = None,
                        page_no: int = 1, page_size: int = 20,
                        sort_dir: str = 'desc', sort_key: str = None) -> dict:
    """
    Batch query Omni-Dataverse data migration tasks

    Args:
        client: DME API client
        gfs_id: Global Namespace ID (1~32 characters, Optional)
        task_name: task name, supports fuzzy query (1~256 characters, Optional)
        task_id: Data migration task ID on the device side (1~256 characters, Optional)
        target_storage_name: Target site name (1~256 characters, Optional)
        namespace_name: namespace name, supports fuzzy query (1~256 characters, Optional)
        namespace_id: Namespace ID (1~32 characters, Optional)
        namespace_raw_id: Namespace ID on the device side (1~256 characters, Optional)
        local_path: Path under Namespace, supports fuzzy query (1~256 characters, Optional, default: "/")
        status: task status list (List<string>, max array members: 9, Optional). valid values: not_run, synchronizing, completed, suspended, faulty, to_be_scheduled, partially_success, failed, unknown
        task_mode: Task mode list (List<string>, max array members: 2, Optional)
        execute_mode: Execute mode list (List<string>, max array members: 2, Optional)
        page_no: Pagination query page number (int32, 1~1000, default: 1, Optional)
        page_size: Items per page (int32, 1~1000, default: 20, Optional)
        sort_dir: Specify sort direction (Optional). valid values: asc, desc. default: desc
        sort_key: Sort parameter (Optional). valid values: progress (task execution progress), real_start_time (task actual start time), real_finish_time (task actual end time)

    Returns:
        {
            total: task count (int32),
            tasks: Data migration task list (List<MigrationTaskInfo>). parameter format: [{
                id: task ID (string),
                name: task name (string),
                status: status (string),
            }, ...],
        }
    """
    url = "/rest/fileservice/v1/gfs/migration-tasks/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size,
        'sort_dir': sort_dir
    }

    if gfs_id is not None:
        payload['gfs_id'] = gfs_id
    if task_name is not None:
        payload['task_name'] = task_name
    if task_id is not None:
        payload['task_id'] = task_id
    if target_storage_name is not None:
        payload['target_storage_name'] = target_storage_name
    if namespace_name is not None:
        payload['namespace_name'] = namespace_name
    if namespace_id is not None:
        payload['namespace_id'] = namespace_id
    if namespace_raw_id is not None:
        payload['namespace_raw_id'] = namespace_raw_id
    if local_path is not None:
        payload['local_path'] = local_path
    if status is not None:
        payload['status'] = status
    if task_mode is not None:
        payload['task_mode'] = task_mode
    if execute_mode is not None:
        payload['execute_mode'] = execute_mode
    if sort_key is not None:
        payload['sort_key'] = sort_key

    response = client.post(url, body=payload)
    return response


def migration_task_show(client: DMEAPIClient, id: str) -> dict:
    """
    Query Omni-Dataverse data migration task details

    Args:
        client: DME API client
        id: Data migration task ID

    Returns:
        {
            id: task ID (string),
            name: task name (string),
            status: status (string),
            progress: progress (string),
            source: source info (string),
            target: target info (string),
        }
    """
    url = "/rest/fileservice/v1/gfs/migration-tasks/{id}"

    response = client.get(url, params={"id": id})
    return response


def migration_task_create(client: DMEAPIClient, gfs_id: str, task_mode: str,
                          start_mode: str, max_bandwidth: int,
                          target_namespace_id: str, task_name: str = None,
                          execute_mode: str = None, execute_time: int = None,
                          execute_time_unit: str = None, start_time: int = None,
                          period_start_day: str = None, period_end_day: str = None,
                          period_time: str = None, period_max_bandwidth: str = None,
                          local_path: str = None, src_namespace_ids: list = None,
                          atime_operator: str = None, atime: int = None,
                          atime_unit: str = None, mtime_operator: str = None,
                          mtime: int = None, mtime_unit: str = None,
                          ctime_operator: str = None, ctime: int = None,
                          ctime_unit: str = None, crtime_operator: str = None,
                          crtime: int = None, crtime_unit: str = None,
                          name_operator: str = None, name_filter: str = None,
                          size_operator: str = None, file_size: int = None,
                          tag: str = None, file_paths: list = None,
                          authentication_type: str = None, user_operator: str = None,
                          user_name: str = None, group_operator: str = None,
                          group_name: str = None, files_filter: dict = None) -> dict:
    """
    Create Omni-Dataverse data migration task

    Args:
        client: DME API client
        gfs_id: Global Namespace ID (1~64 characters, Required)
        task_name: task name (1~255 characters, Optional)
        task_mode: Task mode (Required). valid values: pre_fetch (prefetch cache), tier (data pull)
        execute_mode: Execute mode (Optional). valid values: interval (periodic), one_time (execute once). Invalid when task_mode is pre_fetch
        execute_time: Periodic task execution interval (int32, 1~365, Optional). Required when execute_mode is interval. Invalid when task_mode is pre_fetch
        execute_time_unit: Periodic task execution interval unit (Optional). valid values: minute, hour, day, month. Required when execute_mode is interval. Invalid when task_mode is pre_fetch
        start_mode: Task execution mode (Required). valid values: manual, auto
        start_time: Task start UTC timestamp (int64, min: 0, unit: seconds, Optional). Configurable when start_mode is auto, value 0 means start immediately
        max_bandwidth: Maximum sync rate (int32, 1~10240, unit: MB/s, Required)
        period_start_day: Start date of the specified time period (Optional, format: YYYY-MM-DD). Must be provided together with period_end_day, period_time, period_max_bandwidth
        period_end_day: End date of the specified time period (Optional, format: YYYY-MM-DD). Must be provided together with period_start_day, period_time, period_max_bandwidth
        period_time: Start and end time of the specified time period (Optional, format: "time1,duration1;time2,duration2"). Must be provided together with period_start_day, period_end_day, period_max_bandwidth
        period_max_bandwidth: Bandwidth cap for the specified time period (Optional, format: "bandwidth1;bandwidth2"). Must be provided together with period_start_day, period_end_day, period_time
        target_namespace_id: Target Namespace ID under the global Namespace (1~32 characters, Required)
        local_path: Path under Namespace (Optional, default: "/")
        src_namespace_ids: Source site Namespace ID list under the global Namespace (List<string>, max array members: 32, Optional)
        atime_operator: File access time match rule (Optional). valid values: less_or_equal, greater. Must be provided together with atime, atime_unit
        atime: File access time interval (int32, 0~26304, Optional). Must be provided together with atime_operator, atime_unit
        atime_unit: File access time interval unit (Optional). valid values: hour, day. Must be provided together with atime_operator, atime
        mtime_operator: File modify time match rule (Optional). valid values: less_or_equal, greater. Must be provided together with mtime, mtime_unit
        mtime: File modify time interval (int32, 0~26304, Optional). Must be provided together with mtime_operator, mtime_unit
        mtime_unit: File modify time interval unit (Optional). valid values: hour, day. Must be provided together with mtime_operator, mtime
        ctime_operator: File status change time match rule (Optional). valid values: less_or_equal, greater. Must be provided together with ctime, ctime_unit
        ctime: File status change time interval (int32, 0~26304, Optional). Must be provided together with ctime_operator, ctime_unit
        ctime_unit: File status change time interval unit (Optional). valid values: hour, day. Must be provided together with ctime_operator, ctime
        crtime_operator: File creation time match rule (Optional). valid values: less_or_equal, greater. Must be provided together with crtime, crtime_unit
        crtime: File creation time interval (int32, 0~26304, Optional). Must be provided together with crtime_operator, crtime_unit
        crtime_unit: File creation time interval unit (Optional). valid values: hour, day. Must be provided together with crtime_operator, crtime
        name_operator: File name match rule (Optional). valid values: equal, not_equal. Must be provided together with name_filter
        name_filter: File name match expression list (1~1023 characters, Optional). Must be provided together with name_operator
        size_operator: File size match rule (Optional). valid values: less_or_equal, greater. Must be provided together with file_size
        file_size: File size (int64, 0~4398046511104, unit: KB, Optional). Must be provided together with size_operator
        tag: Object tag match rule (Optional, format: "key1:value1;key2:value2")
        file_paths: File identifier list uploaded by file list filter policy (List<string>, max array members: 200, Optional). Configurable only when execute_mode is one_time
        authentication_type: Authentication type (Optional). valid values: ldap_or_ldaps_domain, unix_local, nis_domain
        user_operator: Username match rule (Optional). valid values: equal, not_equal. Must be provided together with authentication_type, user_name
        user_name: Username (1~255 characters, Optional). Must be provided together with authentication_type, user_operator
        group_operator: User group name match rule (Optional). valid values: equal, not_equal. Must be provided together with authentication_type, group_name
        group_name: User group name (1~255 characters, Optional). Must be provided together with authentication_type, group_operator
        files_filter: File list filter request parameters (FilesFilter object, Optional). Configurable only when execute_mode is one_time. parameter format: {
                file_id: File ID uploaded by file list filter policy (1~63 characters, Required),
                file_name: File name uploaded by file list filter policy (1~1023 characters, Required),
             }

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/fileservice/v1/gfs/migration-tasks"

    payload = {
        'gfs_id': gfs_id,
        'task_mode': task_mode,
        'start_mode': start_mode,
        'max_bandwidth': max_bandwidth,
        'target_namespace_id': target_namespace_id
    }

    if task_name is not None:
        payload['task_name'] = task_name
    if execute_mode is not None:
        payload['execute_mode'] = execute_mode
    if execute_time is not None:
        payload['execute_time'] = execute_time
    if execute_time_unit is not None:
        payload['execute_time_unit'] = execute_time_unit
    if start_time is not None:
        payload['start_time'] = start_time
    if period_start_day is not None:
        payload['period_start_day'] = period_start_day
    if period_end_day is not None:
        payload['period_end_day'] = period_end_day
    if period_time is not None:
        payload['period_time'] = period_time
    if period_max_bandwidth is not None:
        payload['period_max_bandwidth'] = period_max_bandwidth
    if local_path is not None:
        payload['local_path'] = local_path
    if src_namespace_ids is not None:
        payload['src_namespace_ids'] = src_namespace_ids
    if atime_operator is not None:
        payload['atime_operator'] = atime_operator
    if atime is not None:
        payload['atime'] = atime
    if atime_unit is not None:
        payload['atime_unit'] = atime_unit
    if mtime_operator is not None:
        payload['mtime_operator'] = mtime_operator
    if mtime is not None:
        payload['mtime'] = mtime
    if mtime_unit is not None:
        payload['mtime_unit'] = mtime_unit
    if ctime_operator is not None:
        payload['ctime_operator'] = ctime_operator
    if ctime is not None:
        payload['ctime'] = ctime
    if ctime_unit is not None:
        payload['ctime_unit'] = ctime_unit
    if crtime_operator is not None:
        payload['crtime_operator'] = crtime_operator
    if crtime is not None:
        payload['crtime'] = crtime
    if crtime_unit is not None:
        payload['crtime_unit'] = crtime_unit
    if name_operator is not None:
        payload['name_operator'] = name_operator
    if name_filter is not None:
        payload['name_filter'] = name_filter
    if size_operator is not None:
        payload['size_operator'] = size_operator
    if file_size is not None:
        payload['file_size'] = file_size
    if tag is not None:
        payload['tag'] = tag
    if file_paths is not None:
        payload['file_paths'] = file_paths
    if authentication_type is not None:
        payload['authentication_type'] = authentication_type
    if user_operator is not None:
        payload['user_operator'] = user_operator
    if user_name is not None:
        payload['user_name'] = user_name
    if group_operator is not None:
        payload['group_operator'] = group_operator
    if group_name is not None:
        payload['group_name'] = group_name
    if files_filter is not None:
        payload['files_filter'] = files_filter

    response = client.post(url, body=payload)
    return response


def migration_task_modify(client: DMEAPIClient, id: str, task_name: str = None,
                          start_mode: str = None, start_time: int = None,
                          execute_time: int = None, execute_time_unit: str = None,
                          max_bandwidth: int = None, period_start_day: str = None,
                          period_end_day: str = None, period_time: str = None,
                          period_max_bandwidth: str = None) -> dict:
    """
    Modify Omni-Dataverse data migration task

    Args:
        client: DME API client
        id: Data migration task ID (1~32 characters, Required)
        task_name: task name (1~255 characters, Optional)
        start_mode: Task execution mode (Optional). valid values: manual, auto
        start_time: Task start UTC timestamp (int64, min: 0, unit: seconds, Optional). Configurable when start_mode is auto, value 0 means start immediately
        execute_time: Periodic task execution interval (int32, 1~365, Optional). Required when execute_mode is interval
        execute_time_unit: Periodic task execution interval unit (Optional). valid values: minute, hour, day, month. Required when execute_mode is interval
        max_bandwidth: Maximum sync rate (int32, 1~10240, unit: MB/s, Optional)
        period_start_day: Start date of the specified time period (Optional, format: YYYY-MM-DD). Must be provided together with period_end_day, period_time, period_max_bandwidth
        period_end_day: End date of the specified time period (Optional, format: YYYY-MM-DD). Must be provided together with period_start_day, period_time, period_max_bandwidth
        period_time: Start and end time of the specified time period (Optional, format: "time1,duration1;time2,duration2"). Must be provided together with period_start_day, period_end_day, period_max_bandwidth
        period_max_bandwidth: Bandwidth cap for the specified time period (Optional, format: "bandwidth1;bandwidth2"). Must be provided together with period_start_day, period_end_day, period_time

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/fileservice/v1/gfs/migration-tasks/{id}"

    payload = {}

    if task_name is not None:
        payload['task_name'] = task_name
    if start_mode is not None:
        payload['start_mode'] = start_mode
    if start_time is not None:
        payload['start_time'] = start_time
    if execute_time is not None:
        payload['execute_time'] = execute_time
    if execute_time_unit is not None:
        payload['execute_time_unit'] = execute_time_unit
    if max_bandwidth is not None:
        payload['max_bandwidth'] = max_bandwidth
    if period_start_day is not None:
        payload['period_start_day'] = period_start_day
    if period_end_day is not None:
        payload['period_end_day'] = period_end_day
    if period_time is not None:
        payload['period_time'] = period_time
    if period_max_bandwidth is not None:
        payload['period_max_bandwidth'] = period_max_bandwidth

    response = client.put(url, body=payload, params={"id": id})
    return response


def migration_task_delete(client: DMEAPIClient, ids: list) -> dict:
    """
    Batch delete Omni-Dataverse data migration tasks

    Args:
        client: DME API client
        ids: Data migration task ID list

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/fileservice/v1/gfs/migration-tasks/delete"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def migration_task_operate(client: DMEAPIClient, ids: list, operate_type: str) -> dict:
    """
    Batch pause or start Omni-Dataverse data migration tasks

    Args:
        client: DME API client
        ids: Data migration task ID list
        operate_type: Operation type (Required), valid values: start, stop

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/fileservice/v1/gfs/migration-tasks/operate"

    payload = {
        'ids': ids,
        'operate_type': operate_type
    }

    response = client.post(url, body=payload)
    return response


# action list, for CLI help
ACTIONS = {
    # Dataspace subtopic action
    'dataspace_list': {
        'func': dataspace_list,
        'description': 'Batch query Omni-Dataverse',
        'params': ['name', 'id', 'raw_id', 'max_site_num', 'page_no', 'page_size'],
        'subtopic': 'dataspace'
    },
    'dataspace_show': {
        'func': dataspace_show,
        'description': 'Query capacity statistics info of the specified Omni-Dataverse',
        'params': ['id', 'name'],
        'subtopic': 'dataspace'
    },
    'dataspace_site_list': {
        'func': dataspace_site_list,
        'description': 'Query Omni-Dataverse data service sites',
        'params': ['raw_id', 'site_role', 'gfs_group_id', 'storage_name', 'storage_pool_name', 'account_name', 'page_no', 'page_size'],
        'subtopic': 'dataspace'
    },
    # Namespace subtopic action
    'namespace_list': {
        'func': namespace_list,
        'description': 'Batch query global namespace',
        'params': ['name', 'gfs_group_name', 'gfs_group_id', 'gfs_type', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'namespace'
    },
    'namespace_show': {
        'func': namespace_show,
        'description': 'Query global namespace details',
        'params': ['id', 'name_locator'],
        'subtopic': 'namespace'
    },
    'namespace_create': {
        'func': namespace_create,
        'description': 'Create global namespace',
        'params': ['name', 'gfs_group_id', 'gfs_group_name', 'gfs_mode', 'single_write_switch', 'smart_share_members'],
        'subtopic': 'namespace'
    },
    'namespace_modify': {
        'func': namespace_modify,
        'description': 'Modify the specified global namespace',
        'params': ['id', 'name_locator', 'smart_share_members'],
        'subtopic': 'namespace'
    },
    'namespace_delete': {
        'func': namespace_delete,
        'description': 'Delete the specified global namespace',
        'params': ['id', 'name_locator', 'is_delete_child'],
        'subtopic': 'namespace'
    },
    # Migration Task subtopic action
    'migration_task_list': {
        'func': migration_task_list,
        'description': 'Batch query Omni-Dataverse data migration tasks',
        'params': ['gfs_id', 'task_name', 'task_id', 'target_storage_name', 'namespace_name', 'namespace_id', 'namespace_raw_id', 'local_path', 'status', 'task_mode', 'execute_mode', 'page_no', 'page_size', 'sort_dir', 'sort_key'],
        'subtopic': 'migration_task'
    },
    'migration_task_show': {
        'func': migration_task_show,
        'description': 'Query Omni-Dataverse data migration task details',
        'params': ['id'],
        'subtopic': 'migration_task'
    },
    'migration_task_create': {
        'func': migration_task_create,
        'description': 'Create Omni-Dataverse data migration task',
        'params': ['gfs_id', 'task_mode', 'start_mode', 'max_bandwidth', 'target_namespace_id', 'task_name', 'execute_mode', 'execute_time', 'execute_time_unit', 'start_time', 'period_start_day', 'period_end_day', 'period_time', 'period_max_bandwidth', 'local_path', 'src_namespace_ids', 'atime_operator', 'atime', 'atime_unit', 'mtime_operator', 'mtime', 'mtime_unit', 'ctime_operator', 'ctime', 'ctime_unit', 'crtime_operator', 'crtime', 'crtime_unit', 'name_operator', 'name_filter', 'size_operator', 'file_size', 'tag', 'file_paths', 'authentication_type', 'user_operator', 'user_name', 'group_operator', 'group_name', 'files_filter'],
        'subtopic': 'migration_task'
    },
    'migration_task_modify': {
        'func': migration_task_modify,
        'description': 'Modify Omni-Dataverse data migration task',
        'params': ['id', 'task_name', 'start_mode', 'start_time', 'execute_time', 'execute_time_unit', 'max_bandwidth', 'period_start_day', 'period_end_day', 'period_time', 'period_max_bandwidth'],
        'subtopic': 'migration_task'
    },
    'migration_task_delete': {
        'func': migration_task_delete,
        'description': 'Batch delete Omni-Dataverse data migration tasks',
        'params': ['ids'],
        'subtopic': 'migration_task'
    },
    'migration_task_operate': {
        'func': migration_task_operate,
        'description': 'Batch pause or start Omni-Dataverse data migration tasks',
        'params': ['ids', 'operate_type'],
        'subtopic': 'migration_task'
    },
}
