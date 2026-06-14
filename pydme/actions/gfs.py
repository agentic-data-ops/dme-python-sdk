"""
GFS (Global File System) operations
"""

import sys
import os

from pydme.client import DMEAPIClient


# ============================================================================
# Dataspace subtopic actions
# ============================================================================

def dataspace_list(client: DMEAPIClient, name: str = None, id: str = None,
                   raw_id: str = None, max_site_num: int = None,
                   page_no: int = 1, page_size: int = 100) -> dict:
    """
    Batch query Omni-Dataverse

    Args:
        client: DME API client
        name: Omni-Dataverse 名称，supports fuzzy search
        id: Omni-Dataverse id
        raw_id: Omni-Dataverse 在device side的 id
        max_site_num: Omni-Dataverse 下Data service site最大count
        page_no: Page number，默认 1，范围 1~10000
        page_size: Items per page，默认 100，范围 1~1000

    Returns:
        {
            total: Total count (integer),
            gfs_groups: Omni-Dataverse 列表。参数格式如下：[{
                id: ID (string),
                name: 名称 (string),
                status: 状态 (string),
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
    Query Omni-Dataverse 的Capacity statistics信息

    Args:
        client: DME API client
        id: Omni-Dataverse 的 ID，与 name cannot both be empty; takes precedence when both have values ID
        name: Omni-Dataverse 名称，与 id cannot both be empty; takes precedence when both have values ID

    Returns:
        Omni-Dataverse Capacity statistics信息
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
    查询 Omni-Dataverse Data service site

    Args:
        client: DME API client
        raw_id: Data service site在device side的 id
        site_role: Data service site角色，包含 site_role 字段，value range：ORDINARY(普通站点)，METASTORE(元Data service site)
        gfs_group_id: Omni-Dataverse id
        storage_name: 根据存储名称查询Data service site，supports fuzzy search
        storage_pool_name: 根据Storage pool name查询Data service site，supports fuzzy search
        account_name: 根据账户名称查询Data service site，supports fuzzy search
        page_no: Page number，默认 1，范围 1~10000
        page_size: Items per page，默认 100，范围 1~1000

    Returns:
        Data service site列表
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
# Namespace subtopic actions
# ============================================================================

def namespace_list(client: DMEAPIClient, name: str = None, gfs_group_name: str = None,
                   gfs_group_id: str = None, gfs_type: str = None,
                   sort_key: str = None, sort_dir: str = None,
                   page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch queryGlobal namespace

    Args:
        client: DME API client
        name: Global namespace的名称，supports fuzzy search (0~256个字符, Optional)
        gfs_group_name: Global data space name，supports fuzzy search (0~256个字符, Optional)
        gfs_group_id: 所属Global data space的 ID (1~32个字符, Optional)
        gfs_type: Global namespace类型 (Optional)。Optional值：enable_object_multi_version (支持object多版本), disable_object_multi_version (不支持object多版本)
        sort_key: sort by specified field (Optional)。Optional值：child_name_space_num
        sort_dir: 指定Sort direction (Optional)。Optional值：asc (升序), desc (降序)。Default：asc
        page_no: 分页起始页 (int32, 1~1000, Default: 1, Optional)
        page_size: 每页查询的count (int32, 1~1000, Default: 20, Optional)

    Returns:
        Global namespace列表
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
    查询Global namespace详情

    Args:
        client: DME API client
        id: Global namespace的 ID，与 name_locator cannot both be empty; takes precedence when both have values ID
        name_locator: 名称定位器，格式为：Global namespace的名称@Global data space name

    Returns:
        Global namespaceDetails
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
    创建Global namespace

    Args:
        client: DME API client
        name: 全局Namespace name (1~255个字符, Required)
        gfs_group_id: Global data space ID (1~32个字符, Optional。与 gfs_group_name cannot both be empty; takes precedence when both have values gfs_group_id)
        gfs_group_name: Global data space名称 (1~255个字符, Optional。与 gfs_group_id cannot both be empty; takes precedence when both have values gfs_group_id)
        gfs_mode: Global namespace模式 (Optional)。Optional值：smart_share。Default：smart_share
        single_write_switch: Single write mode switch (Optional)。Optional值：close (Any member can write), open (只有一个成员可写入)
        smart_share_members: SmartShare Member list (List<SmartShareMember>, max array members: 32, Optional。当 gfs_mode 取值为 smart_share 时Required)。参数格式如下：[{
                id: Namespace ID (1~64个字符, Required),
                pull_mode: 读数据模式 (Optional)。Optional值：no_cache (转发读), on_demand (按需读)。Default：on_demand,
                cache_time: 缓存时长 (int32, Optional, Default: 8)。当 cache_time_unit 为 hour 时 1~4320, 为 day 时 1~180,
                cache_time_unit: Cache duration unit (Optional)。Optional值：hour (hour(s)), day (day(s))。cache_time 取值时Required。Default：hour,
                single_write_mode: 单写模式策略 (Optional)。Optional值：read_only (只读), read_write (读写)。当 single_write_switch 为 open 时，必须且只能有一个成员取值为 read_write,
             }, ...]

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    ModifyGlobal namespace

    Args:
        client: DME API client
        id: Global namespace的 ID (1~32个字符, Optional。与 name_locator cannot both be empty; takes precedence when both have values id)
        name_locator: 名称定位器，格式为：Global namespace的名称@Global data space name (3~507个字符, Optional。与 id cannot both be empty; takes precedence when both have values id)
        smart_share_members: SmartShare Member list (List<ModifySmartShareMember>, min array members: 0, max array members: 256, Optional。当Global namespace的模式为 smart_share 时该参数有效)。参数格式如下：[{
                id: Namespace ID 或Filesystem ID (1~64个字符, Required),
                pull_mode: 读数据模式 (Optional)。Optional值：no_cache (转发读), on_demand (按需读),
                cache_time: 缓存时长 (int32, Optional, Default: 8)。当 cache_time_unit 为 hour 时 1~4320, 为 day 时 1~180,
                cache_time_unit: Cache duration unit (Optional)。Optional值：hour (hour(s)), day (day(s))。cache_time 取值时Required,
             }, ...]

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    Delete的Global namespace

    Args:
        client: DME API client
        id: Global namespace的 ID，与 name_locator cannot both be empty
        name_locator: 名称定位器，格式为：Global namespace的名称@Global data space name
        is_delete_child: 是否删除子Namespace，默认 true

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
# Migration Task subtopic actions
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
    Batch query Omni-Dataverse Data migration task

    Args:
        client: DME API client
        gfs_id: Global namespace ID (1~32个字符, Optional)
        task_name: 任务名称，supports fuzzy search (1~256个字符, Optional)
        task_id: Data migration task在device side的 ID (1~256个字符, Optional)
        target_storage_name: 目标站点名称 (1~256个字符, Optional)
        namespace_name: Namespace name，supports fuzzy search (1~256个字符, Optional)
        namespace_id: Namespace ID (1~32个字符, Optional)
        namespace_raw_id: Namespace在device side ID (1~256个字符, Optional)
        local_path: Namespace下的路径，supports fuzzy search (1~256个字符, Optional, Default: "/")
        status: Task status list (List<string>, max array members: 9, Optional)。Optional值：not_run (未运行), synchronizing (数据Syncing), completed (完成), suspended (Paused), faulty (故障), to_be_scheduled (待调度), partially_success (部分成功), failed (失败), unknown (未知)
        task_mode: Task mode list (List<string>, max array members: 2, Optional)
        execute_mode: 执行模式列表 (List<string>, max array members: 2, Optional)
        page_no: Page number (int32, 1~1000, Default: 1, Optional)
        page_size: Items per page (int32, 1~1000, Default: 20, Optional)
        sort_dir: 指定Sort direction (Optional)。Optional值：asc (升序), desc (降序)。Default：desc
        sort_key: Sort key (Optional)。Optional值：progress (Task execution进度), real_start_time (Task actual start time), real_finish_time (任务实际End time)

    Returns:
        Data migrationTask list
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
    查询 Omni-Dataverse Data migrationTask details

    Args:
        client: DME API client
        id: Data migration task ID

    Returns:
        Data migration taskDetails
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
    创建 Omni-Dataverse Data migration task

    Args:
        client: DME API client
        gfs_id: Global namespace ID (1~64个字符, Required)
        task_name: 任务名称 (1~255个字符, Optional)
        task_mode: 任务模式 (Required)。Optional值：pre_fetch (预取缓存), tier (数据拉取)
        execute_mode: 执行模式 (Optional)。Optional值：interval (week(s)期性), one_time (只执行一次)。当 task_mode 为 pre_fetch this parameter is ineffective
        execute_time: week(s)期性Task execution时间间隔 (int32, 1~365, Optional)。当 execute_mode 为 interval 时必须下发。当 task_mode 为 pre_fetch this parameter is ineffective
        execute_time_unit: week(s)期性Task executionTime interval unit (Optional)。Optional值：minute (分), hour (hour(s)), day (day(s)), month (month(s))。当 execute_mode 为 interval 时必须下发。当 task_mode 为 pre_fetch this parameter is ineffective
        start_mode: Task execution模式 (Required)。Optional值：manual (手动), auto (自动)
        start_time: 任务启动的 UTC Timestamp (int64, min: 0, 单位: second(s), Optional)。当 start_mode 为 auto 时允许配置, 取值为 0 Immediate start
        max_bandwidth: 最大Sync速率 (int32, 1~10240, 单位: MB/s, Required)
        period_start_day: Start date of specified period (Optional, 格式: YYYY-MM-DD)。与 period_end_day、period_time、period_max_bandwidth must be sent together
        period_end_day: End date of specified period (Optional, 格式: YYYY-MM-DD)。与 period_start_day、period_time、period_max_bandwidth must be sent together
        period_time: Start/end time of specified period (Optional, 格式: "time1,duration1;time2,duration2")。与 period_start_day、period_end_day、period_max_bandwidth must be sent together
        period_max_bandwidth: Bandwidth for specified periodupper limit (Optional, 格式: "bandwidth1;bandwidth2")。与 period_start_day、period_end_day、period_time must be sent together
        target_namespace_id: Global namespace下目标Namespace ID (1~32个字符, Required)
        local_path: Namespace下的路径 (Optional, Default: "/")
        src_namespace_ids: Global namespace下源站点Namespace ID 列表 (List<string>, max array members: 32, Optional)
        atime_operator: 文件的访问时间匹配规则 (Optional)。Optional值：less_or_equal (小于等于), greater (大于)。与 atime、atime_unit must be sent together
        atime: 文件的访问时间间隔 (int32, 0~26304, Optional)。与 atime_operator、atime_unit must be sent together
        atime_unit: 文件的访问Time interval unit (Optional)。Optional值：hour (hour(s)), day (day(s))。与 atime_operator、atime must be sent together
        mtime_operator: 文件的修改时间匹配规则 (Optional)。Optional值：less_or_equal (小于等于), greater (大于)。与 mtime、mtime_unit must be sent together
        mtime: 文件的修改时间间隔 (int32, 0~26304, Optional)。与 mtime_operator、mtime_unit must be sent together
        mtime_unit: 文件的修改Time interval unit (Optional)。Optional值：hour (hour(s)), day (day(s))。与 mtime_operator、mtime must be sent together
        ctime_operator: 文件的状态修改时间匹配规则 (Optional)。Optional值：less_or_equal (小于等于), greater (大于)。与 ctime、ctime_unit must be sent together
        ctime: 文件的状态修改时间间隔 (int32, 0~26304, Optional)。与 ctime_operator、ctime_unit must be sent together
        ctime_unit: 文件的状态修改Time interval unit (Optional)。Optional值：hour (hour(s)), day (day(s))。与 ctime_operator、ctime must be sent together
        crtime_operator: 文件的Creation time匹配规则 (Optional)。Optional值：less_or_equal (小于等于), greater (大于)。与 crtime、crtime_unit must be sent together
        crtime: 文件的Creation time间隔 (int32, 0~26304, Optional)。与 crtime_operator、crtime_unit must be sent together
        crtime_unit: 文件的Creation time间隔单位 (Optional)。Optional值：hour (hour(s)), day (day(s))。与 crtime_operator、crtime must be sent together
        name_operator: 文件名匹配规则 (Optional)。Optional值：equal (相等), not_equal (不相等)。与 name_filter must be sent together
        name_filter: 文件名匹配表达式列表 (1~1023个字符, Optional)。与 name_operator must be sent together
        size_operator: File size的匹配规则 (Optional)。Optional值：less_or_equal (小于等于), greater (大于)。与 file_size must be sent together
        file_size: 文件的大小 (int64, 0~4398046511104, 单位: KB, Optional)。与 size_operator must be sent together
        tag: object标签匹配规则 (Optional, 格式: "key1:value1;key2:value2")
        file_paths: 按文件列表过滤策略上传的文件标识列表 (List<string>, max array members: 200, Optional)。仅 execute_mode 为 one_time 时可配置
        authentication_type: Auth type (Optional)。Optional值：ldap_or_ldaps_domain (LDAP/LDAPS域), unix_local (UNIX本地认证), nis_domain (NIS域)
        user_operator: 用户名匹配规则 (Optional)。Optional值：equal (相等), not_equal (不相等)。与 authentication_type、user_name must be sent together
        user_name: 用户名 (1~255个字符, Optional)。与 authentication_type、user_operator must be sent together
        group_operator: User group名匹配规则 (Optional)。Optional值：equal (相等), not_equal (不相等)。与 authentication_type、group_name must be sent together
        group_name: User group名 (1~255个字符, Optional)。与 authentication_type、group_operator must be sent together
        files_filter: 按文件列表过滤请求参数 (FilesFilterobject, Optional)。仅 execute_mode 为 one_time 时可配置。参数格式如下：{
                file_id: 按文件列表过滤策略上传的文件 ID (1~63个字符, Required),
                file_name: 按文件列表过滤策略上传的文件名称 (1~1023个字符, Required),
             }

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    修改 Omni-Dataverse Data migration task

    Args:
        client: DME API client
        id: Data migration task ID (1~32个字符, Required)
        task_name: 任务名称 (1~255个字符, Optional)
        start_mode: Task execution模式 (Optional)。Optional值：manual (手动), auto (自动)
        start_time: 任务启动的 UTC Timestamp (int64, min: 0, 单位: second(s), Optional)。当 start_mode 为 auto 时允许配置, 取值为 0 Immediate start
        execute_time: week(s)期性Task execution时间间隔 (int32, 1~365, Optional)。当 execute_mode 为 interval 时必须下发
        execute_time_unit: week(s)期性Task executionTime interval unit (Optional)。Optional值：minute (分), hour (hour(s)), day (day(s)), month (month(s))。当 execute_mode 为 interval 时必须下发
        max_bandwidth: 最大Sync速率 (int32, 1~10240, 单位: MB/s, Optional)
        period_start_day: Start date of specified period (Optional, 格式: YYYY-MM-DD)。与 period_end_day、period_time、period_max_bandwidth must be sent together
        period_end_day: End date of specified period (Optional, 格式: YYYY-MM-DD)。与 period_start_day、period_time、period_max_bandwidth must be sent together
        period_time: Start/end time of specified period (Optional, 格式: "time1,duration1;time2,duration2")。与 period_start_day、period_end_day、period_max_bandwidth must be sent together
        period_max_bandwidth: Bandwidth for specified periodupper limit (Optional, 格式: "bandwidth1;bandwidth2")。与 period_start_day、period_end_day、period_time must be sent together

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    Batch delete Omni-Dataverse Data migration task

    Args:
        client: DME API client
        ids: Data migration task ID 列表

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fileservice/v1/gfs/migration-tasks/delete"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def migration_task_operate(client: DMEAPIClient, ids: list, operate_type: dict) -> dict:
    """
    Batch pause or start Omni-Dataverse Data migration task

    Args:
        client: DME API client
        ids: Data migration task ID 列表
        operate_type: 操作类型，包含 operate_type 字段，取值 start(启动), stop(停止)

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fileservice/v1/gfs/migration-tasks/operate"

    payload = {
        'ids': ids,
        'operate_type': operate_type
    }

    response = client.post(url, body=payload)
    return response


# Action list for CLI help
ACTIONS = {
    # Dataspace subtopic actions
    'dataspace_list': {
        'func': dataspace_list,
        'description': 'Batch query Omni-Dataverse',
        'params': ['name', 'id', 'raw_id', 'max_site_num', 'page_no', 'page_size'],
        'subtopic': 'dataspace'
    },
    'dataspace_show': {
        'func': dataspace_show,
        'description': 'Query Omni-Dataverse 的Capacity statistics信息',
        'params': ['id', 'name'],
        'subtopic': 'dataspace'
    },
    'dataspace_site_list': {
        'func': dataspace_site_list,
        'description': '查询 Omni-Dataverse Data service site',
        'params': ['raw_id', 'site_role', 'gfs_group_id', 'storage_name', 'storage_pool_name', 'account_name', 'page_no', 'page_size'],
        'subtopic': 'dataspace'
    },
    # Namespace subtopic actions
    'namespace_list': {
        'func': namespace_list,
        'description': 'Batch queryGlobal namespace',
        'params': ['name', 'gfs_group_name', 'gfs_group_id', 'gfs_type', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'namespace'
    },
    'namespace_show': {
        'func': namespace_show,
        'description': '查询Global namespace详情',
        'params': ['id', 'name_locator'],
        'subtopic': 'namespace'
    },
    'namespace_create': {
        'func': namespace_create,
        'description': '创建Global namespace',
        'params': ['name', 'gfs_group_id', 'gfs_group_name', 'gfs_mode', 'single_write_switch', 'smart_share_members'],
        'subtopic': 'namespace'
    },
    'namespace_modify': {
        'func': namespace_modify,
        'description': 'ModifyGlobal namespace',
        'params': ['id', 'name_locator', 'smart_share_members'],
        'subtopic': 'namespace'
    },
    'namespace_delete': {
        'func': namespace_delete,
        'description': 'Delete的Global namespace',
        'params': ['id', 'name_locator', 'is_delete_child'],
        'subtopic': 'namespace'
    },
    # Migration Task subtopic actions
    'migration_task_list': {
        'func': migration_task_list,
        'description': 'Batch query Omni-Dataverse Data migration task',
        'params': ['gfs_id', 'task_name', 'task_id', 'target_storage_name', 'namespace_name', 'namespace_id', 'namespace_raw_id', 'local_path', 'status', 'task_mode', 'execute_mode', 'page_no', 'page_size', 'sort_dir', 'sort_key'],
        'subtopic': 'migration_task'
    },
    'migration_task_show': {
        'func': migration_task_show,
        'description': '查询 Omni-Dataverse Data migrationTask details',
        'params': ['id'],
        'subtopic': 'migration_task'
    },
    'migration_task_create': {
        'func': migration_task_create,
        'description': '创建 Omni-Dataverse Data migration task',
        'params': ['gfs_id', 'task_mode', 'start_mode', 'max_bandwidth', 'target_namespace_id', 'task_name', 'execute_mode', 'execute_time', 'execute_time_unit', 'start_time', 'period_start_day', 'period_end_day', 'period_time', 'period_max_bandwidth', 'local_path', 'src_namespace_ids', 'atime_operator', 'atime', 'atime_unit', 'mtime_operator', 'mtime', 'mtime_unit', 'ctime_operator', 'ctime', 'ctime_unit', 'crtime_operator', 'crtime', 'crtime_unit', 'name_operator', 'name_filter', 'size_operator', 'file_size', 'tag', 'file_paths', 'authentication_type', 'user_operator', 'user_name', 'group_operator', 'group_name', 'files_filter'],
        'subtopic': 'migration_task'
    },
    'migration_task_modify': {
        'func': migration_task_modify,
        'description': '修改 Omni-Dataverse Data migration task',
        'params': ['id', 'task_name', 'start_mode', 'start_time', 'execute_time', 'execute_time_unit', 'max_bandwidth', 'period_start_day', 'period_end_day', 'period_time', 'period_max_bandwidth'],
        'subtopic': 'migration_task'
    },
    'migration_task_delete': {
        'func': migration_task_delete,
        'description': 'Batch delete Omni-Dataverse Data migration task',
        'params': ['ids'],
        'subtopic': 'migration_task'
    },
    'migration_task_operate': {
        'func': migration_task_operate,
        'description': 'Batch pause or start Omni-Dataverse Data migration task',
        'params': ['ids', 'operate_type'],
        'subtopic': 'migration_task'
    },
}
