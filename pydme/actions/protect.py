"""
保护 (Protection) operations
"""

import sys
import os

from pydme.client import DMEAPIClient


# ============================================================================
# group 子主题 - 保护组operations
# ============================================================================

def group_list(client: DMEAPIClient, name: str = None, project_id: str = None,
               storage_name: str = None, storage_id: str = None,
               raw_id: str = None, lun_group_raw_id: str = None,
               vstore_id: str = None, vstore_raw_id: str = None,
               sort_key: str = None, sort_dir: str = None,
               page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch query保护组

    Args:
        client: DME API client
        name: 保护组名称，supports fuzzy search
        project_id: 业务群组 ID，支持条件过滤
        storage_name: Storage device name，supports fuzzy search
        storage_id: Storage device ID，支持条件过滤
        raw_id: 保护组在设备上的 ID，支持精确搜索，支持排序
        lun_group_raw_id: LUN 组在设备上的 ID，支持条件过滤
        vstore_id: 所属租户的 ID，该参数和 vstore_raw_id mutually exclusive
        vstore_raw_id: 所属租户在设备上的 ID，该参数和 vstore_id mutually exclusive
        sort_key: 排序字段，Optional值：sort_id
        sort_dir: 排序方向，Optional值：asc, desc（默认 desc）
        page_no: 分页查询页码，默认 1
        page_size: 每页显示的数量，默认 20

    Returns:
        {
            total: 保护组总数 (integer),
            protection_groups: Protection group list (List<ProtectionGroupInfo>)。参数格式如下：[{
                id: Protection group ID (string),
                name: 保护组名称 (string),
                status: 状态 (string),
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
    创建保护组

    Args:
        client: DME API client
        name: 保护组名称
        storage_id: Storage device ID
        lun_ids: LUN 的 ID 列表，条件Required，当基于 LUN 创建保护组时为必传字段
        lun_group_id: LUN 组 ID，条件Required，当基于 LUN 组形式创建保护组时为必传字段
        description: 保护组描述

    Returns:
        {
            id: Protection group ID (string),
            task_id: Task ID (string, 1~64个字符),
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
    修改保护组

    Args:
        client: DME API client
        pg_id: 保护组 ID
        name: 保护组的名称
        description: 保护组的描述

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    Batch delete保护组

    >![](public_sys-resources/icon-notice.gif) **须知：**
    >该 API 可能会直接或间接影响现网业务运行，导致业务中断、关键数据丢失等，请谨慎操作。

    Args:
        client: DME API client
        pg_ids: 保护组的 ID 列表

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    保护组中添加成员 LUN

    向指定保护组中添加成员 LUN。

    Args:
        client: DME API client
        pg_id: 保护组 ID
        lun_ids: 待添加到保护组的 LUN 的 ID 列表（Optional），max array members 100，与 hyper_metro 和 rem_reps 的参数 lun_pairs mutually exclusive；保护组不存在双活、复制、环形 3DC 特性时此参数有效
        hyper_metro: 添加 LUN 到有双活特性保护组的请求参数（Optional），与 lun_ids 参数mutually exclusive；保护组存在双活特性时此参数有效。格式：{
                        is_delay: 是否延迟执行（Required），true：是；false：否；当延迟执行为 true 时：若一致性组或新 Pair 处于"正在同步"状态，将等待同步完成后再将新 Pair 加入一致性组；当延迟执行为 false 时：若一致性组或新 Pair 处于"正在同步"状态，将直接暂停一致性组和新 Pair，将新 Pair 加入一致性组，再同步一致性组
                        create_mode: 双活 Pair 的创建模式（Required），Optional值：auto（自动）、manual（手动）
                        remote_storage_pool_id: 远端存储池 ID（Optional），1~32 个字符，正则 ^[a-fA-F0-9]+$；双活 Pair 创建模式为 auto 时有效
                        remote_lun_name_rule: LUN 的名称策略（Optional），Optional值：same_as_local（与本端Resource name保持一致）、prefix_and_suffix（前缀+本端Resource name+后缀）、prefix_and_num（前缀+自动序号）；自动创建模式下有效
                        name_prefix: 远端 LUN 名称前缀（Optional），0~251 个字符；自动创建模式且名称规则为 prefix_and_suffix 或 prefix_and_num 时有效；prefix_and_suffix 前缀最长 32 字节，prefix_and_num 前缀最长 251 字节
                        name_suffix: 远端 LUN 名称后缀（Optional），0~16 个字符；自动创建模式且名称规则为 prefix_and_suffix 时有效
                        lun_pairs: 手动配置的双活 Pair 信息列表（Optional），max array members 100；当 create_mode 为 manual 时有效。格式：[{
                                local_lun_id: 本端 LUN 的 ID（Required），1~32 个字符，正则 ^[a-fA-F0-9]+$；下发操作的设备端定义为本端，其对端设备定义为远端
                                remote_lun_id: 远端 LUN 的 ID（Required），1~32 个字符，正则 ^[a-fA-F0-9]+$
                        },...]
        }
        rem_reps: 添加 LUN 到有复制特性保护组的请求参数（Optional），max array members 2，与 lun_ids 参数mutually exclusive；保护组存在复制特性时此参数有效。格式：[{
                        is_delay: 是否延迟执行（Optional），默认 true；true：是；false：否；当延迟执行为 true 时：若新 Pair 处于"正在同步"状态，将等待同步完成后再将新 Pair 加入一致性组；当延迟执行为 false 时：将直接分裂一致性组和新 Pair，将新 Pair 加入一致性组，再同步一致性组
                        create_mode: 远程复制 Pair 的创建模式（Required），Optional值：auto（自动）、manual（手动）
                        remote_storage_id: 远端Storage device ID（Required），1~64 个字符，正则 ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$
                        remote_storage_pool_id: 远端存储池 ID（Optional），1~32 个字符，正则 ^[a-fA-F0-9]+$；复制 Pair 创建模式为 auto 时有效
                        remote_lun_name_rule: LUN 的名称策略（Optional），Optional值：same_as_local（与本端Resource name保持一致）、prefix_and_suffix（前缀+本端Resource name+后缀）、prefix_and_num（前缀+自动序号）；自动创建模式下有效
                        name_prefix: 远端 LUN 名称前缀（Optional），0~251 个字符；自动创建模式且名称规则为 prefix_and_suffix 或 prefix_and_num 时有效；prefix_and_suffix 前缀最长 32 字节，prefix_and_num 前缀最长 251 字节
                        name_suffix: 远端 LUN 名称后缀（Optional），0~16 个字符；自动创建模式且名称规则为 prefix_and_suffix 时有效
                        lun_pairs: 手动配置的远程复制 Pair 信息列表（Optional），max array members 100；当 create_mode 为 manual 时有效。格式：[{
                                local_lun_id: 本端 LUN 的 ID（Required），1~32 个字符，正则 ^[a-fA-F0-9]+$；下发操作的设备端定义为本端，其对端设备定义为远端
                                remote_lun_id: 远端 LUN 的 ID（Required），1~32 个字符，正则 ^[a-fA-F0-9]+$
                        },...]
        },...]

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    移除保护组中的成员 LUN

    Remove保护组中的成员 LUN。

    Args:
        client: DME API client
        pg_id: 保护组 ID
        lun_ids: 待移除的保护组成员 LUN 的 ID 列表
        is_delay: 是否延迟执行。在远程复制，同步 + 异步的环形 3DC 情况下，此参数无效

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
# hypermetro_group 子主题 - 双活一致性组operations
# ============================================================================

def hypermetro_group_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 20,
                          name: str = None, raw_id: str = None,
                          protect_group_id: str = None, storage_id: str = None,
                          storage_name: str = None, local_vstore_id: str = None,
                          local_vstore_raw_id: str = None, remote_vstore_id: str = None,
                          remote_vstore_raw_id: str = None) -> dict:
    """
    Batch query双活一致性组

    Args:
        client: DME API client
        page_no: 分页查询的页码，默认 1
        page_size: 每页显示的数量，默认 20
        name: 双活一致性组名称，supports fuzzy match
        raw_id: 双活一致性组在设备上的 ID
        protect_group_id: 保护组 ID
        storage_id: Storage device ID，支持本端存储 ID 过滤
        storage_name: Storage device name，支持本端存储名称模糊匹配
        local_vstore_id: 所属本端租户的 ID，该参数和 local_vstore_raw_id mutually exclusive
        local_vstore_raw_id: 所属本端租户在设备上的 ID，该参数和 local_vstore_id mutually exclusive
        remote_vstore_id: 所属远端租户的 ID，该参数和 remote_vstore_raw_id mutually exclusive
        remote_vstore_raw_id: 所属远端租户在设备上的 ID，该参数和 remote_vstore_id mutually exclusive

    Returns:
        双活一致性组列表
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
    创建双活一致性组

    Args:
        client: DME API client
        domain_id: 双活域 ID
        name: 双活一致性组名称
        local_storage_id: 本端设备 ID
        local_pg_id: 本端保护组的 ID，条件Required：当设备类型为 OceanStor Dorado V6、OceanStor V6 时Required
        description: Description
        create_mode: 双活 Pair 的创建模式，Optional值：auto（自动模式）, manual（手动模式）
        remote_vstore_id: 远端设备的租户 ID，条件Required：当 create_mode 为 auto 且设备为 OceanStor Dorado 6.1.3 及以上版本时
        remote_storage_pool_id: 远端存储池 ID，条件Required：当 create_mode 为 auto 时
        lun_ids: LUN 的 ID 列表，条件Optional：当 create_mode 为 auto 时
        remote_resource_name_rule: 远端资源的名称策略，Optional值：same_as_local, prefix_and_suffix, prefix_and_num

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    修改双活一致性组

    Args:
        client: DME API client
        group_id: 双活一致性组 ID
        name: 双活一致性组名称
        description: Description
        recovery_policy: 双活 Pair 恢复策略，Optional值：automatic（自动）, manual（手动）
        service_assurance_policy: 业务保障策略，Optional值：data_reliability_preferred（数据可靠优先）, service_continuity_preferred（业务连续优先）
        speed: 同步速率，Optional值：low, medium, high, highest, custom
        bandwidth: 自定义同步速率（MB/s），当 speed 为 custom 时Required
        isolation_threshold_time: 隔离阈值（毫秒），当 service_assurance_policy 为 service_continuity_preferred 时Required

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    Batch delete双活一致性组

    Args:
        client: DME API client
        ids: 双活一致性组 ID 列表
        delete_mode: 删除模型，Optional值：preferred_only（优先站点删除）, non_preferred_only（非优先站点删除）, dual_ends（两端站点删除）
        is_self_adapt: 是否支持自适应删除成员 Pair，默认 false

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    双活一致性组添加成员 Pair

    Args:
        client: DME API client
        group_id: 双活一致性组 ID
        pair_ids: 双活 Pair ID 列表
        is_self_adapt: 是否自适应修改双活 Pair 运行状态

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    双活一致性组移除成员 Pair

    Args:
        client: DME API client
        group_id: 双活一致性组 ID
        pair_ids: 双活 Pair ID 列表

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    暂停双活一致性组

    Args:
        client: DME API client
        ids: 双活一致性组 ID 列表
        priority_station_type: 站点类型，Optional值：preferred（优先站点）, non_preferred（非优先站点）

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    强制启动双活一致性组

    Args:
        client: DME API client
        ids: 双活一致性组 ID 列表
        priority_station_type: 站点类型，Optional值：preferred（优先站点）, non_preferred（非优先站点）

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    双活一致性组优先站点切换

    Args:
        client: DME API client
        ids: 双活一致性组 ID 列表

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/metro/groups/switch-priority-site"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


# ============================================================================
# hypermetro_pair 子主题 - 双活 Pair operations
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
    Batch query LUN 双活 Pair

    Args:
        client: DME API client
        page_no: 分页查询的页码，默认 1
        page_size: 每页显示的数量，默认 20
        group_id: 所属双活一致性组 ID
        group_name: 所属双活一致性组名称，supports fuzzy match
        group_raw_id: 所属双活一致性组在存储设备上的 ID
        pair_raw_id: 双活 Pair 在存储设备上的 ID
        local_storage_id: 本端Storage device ID
        local_storage_name: 本端Storage device name，supports fuzzy match
        local_vstore_id: 所属本端租户的 ID，该参数和 local_vstore_raw_id mutually exclusive
        local_vstore_raw_id: 所属本端租户在设备上的 ID，该参数和 local_vstore_id mutually exclusive
        local_volume_name: 本端 LUN 名称，supports fuzzy match
        local_host_access_state: 本地资源主机访问状态，Optional值：access_forbidden, read_only, read_write
        remote_vstore_id: 所属远端租户的 ID，该参数和 remote_vstore_raw_id mutually exclusive
        remote_vstore_raw_id: 所属远端租户在设备上的 ID，该参数和 remote_vstore_id mutually exclusive
        remote_volume_name: 远端 LUN 名称，supports fuzzy match

    Returns:
        双活 Pair 列表
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
    创建双活 Pair

    Args:
        client: DME API client
        create_mode: 双活 Pair 的创建模式，Optional值：auto（自动创建）, manual（手动创建）
        local_storage_id: 创建双活 Pair 的Storage device ID
        domain_id: 双活域 ID
        lun_ids: 自动创建模式下，源 LUN 的 ID 列表
        lun_pairs: 手动创建模式下，双活 Pair 的源 LUN、目标 LUN 的 ID 列表
        remote_storage_pool_id: 远端存储池 ID，自动创建模式下有效
        remote_vstore_id: 远端设备的租户 ID，自动创建模式下有效
        remote_resource_name_rule: LUN 的名称策略，Optional值：same_as_local, prefix_and_suffix, prefix_and_num
        name_prefix: 远端 LUN 名称前缀
        name_suffix: 远端 LUN 名称后缀
        speed: 同步速率，Optional值：low, medium, high, highest, custom
        bandwidth: 自定义同步速率（MB/s），当 speed 为 custom 时必传
        service_assurance_policy: 业务保障策略，Optional值：data_reliability_preferred, service_continuity_preferred
        isolation_threshold_time: 隔离阈值（毫秒），当 service_assurance_policy 为 service_continuity_preferred 时必传
        recovery_policy: 恢复策略，Optional值：automatic, manual

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    修改双活 Pair

    Args:
        client: DME API client
        pair_id: 双活 Pair 实例 ID
        speed: 双活 Pair 同步速率，Optional值：low, medium, high, highest, custom
        bandwidth: 自定义速率（MB/s），当 speed 为 custom 时Required
        recovery_policy: 恢复策略，Optional值：automatic, manual
        service_assurance_policy: 业务保障策略，Optional值：data_reliability_preferred, service_continuity_preferred
        isolation_threshold_time: 隔离阈值（毫秒），当 service_assurance_policy 为 service_continuity_preferred 时Required

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    Batch delete双活 Pair

    >![](public_sys-resources/icon-notice.gif) **须知：**
    >该 API 可能会直接或间接影响现网业务运行，导致业务中断、关键数据丢失等，请谨慎操作。

    Args:
        client: DME API client
        ids: 双活 Pair 实例 ID 列表
        delete_mode: 删除模式，Optional值：preferred_only, non_preferred_only, dual_ends
        is_lun_service_interrupt: 是否中断 LUN 业务，当 delete_mode 为 preferred_only 或 non_preferred_only 时有效

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    同步双活 Pair

    Args:
        client: DME API client
        ids: 双活 Pair ID 列表

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    暂停双活 Pair

    Args:
        client: DME API client
        ids: 双活 Pair ID 列表
        priority_station_type: 站点类型，Optional值：preferred, non_preferred

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    强制启动双活 Pair

    Args:
        client: DME API client
        ids: 双活 Pair ID 列表
        priority_station_type: 站点类型，Optional值：preferred, non_preferred

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    双活 Pair 优先站点切换

    Args:
        client: DME API client
        ids: 双活 Pair ID 列表

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/metro/lun-pairs/switch-priority-site"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


# ============================================================================
# hypermetro_domain 子主题 - 双活域operations
# ============================================================================

def hypermetro_domain_list(client: DMEAPIClient, storage_id: str = None,
                            types: list = None) -> dict:
    """
    Batch query双活域

    Args:
        client: DME API client
        storage_id: 设备 ID
        types: 双活域类型列表

    Returns:
        双活域列表
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
# replication_pair 子主题 - 复制 Pair operations
# ============================================================================

def replication_pair_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 20,
                          group_id: str = None, group_name: str = None,
                          pair_raw_id: str = None, local_storage_id: str = None,
                          local_storage_name: str = None, local_vstore_id: str = None,
                          local_vstore_raw_id: str = None, local_volume_name: str = None,
                          remote_vstore_id: str = None, remote_vstore_raw_id: str = None,
                          remote_volume_name: str = None) -> dict:
    """
    Batch query复制 Pair

    Args:
        client: DME API client
        page_no: 分页查询的页码，默认 1
        page_size: 每页显示的数量，默认 20
        group_id: 所属复制一致性组 ID
        group_name: 所属复制一致性组名称，supports fuzzy match
        pair_raw_id: 复制 Pair 在存储设备上的 ID
        local_storage_id: 本端Storage device ID
        local_storage_name: 本端Storage device name，supports fuzzy match
        local_vstore_id: 所属本端租户的 ID，该参数和 local_vstore_raw_id mutually exclusive
        local_vstore_raw_id: 所属本端租户在设备上的 ID，该参数和 local_vstore_id mutually exclusive
        local_volume_name: 本端 LUN 名称，supports fuzzy match
        remote_vstore_id: 所属远端租户的 ID，该参数和 remote_vstore_raw_id mutually exclusive
        remote_vstore_raw_id: 所属远端租户在设备上的 ID，该参数和 remote_vstore_id mutually exclusive
        remote_volume_name: 远端 LUN 名称，supports fuzzy match

    Returns:
        复制 Pair 列表
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
    创建远程复制 Pair

    Args:
        client: DME API client
        local_storage_id: 本端Storage device ID
        local_lun_id: 本端 LUN ID
        remote_storage_id: 远端Storage device ID
        remote_storage_pool_id: 远端存储池 ID
        remote_vstore_id: 远端设备的租户 ID
        remote_resource_name_rule: 远端资源的名称策略，Optional值：same_as_local, prefix_and_suffix, prefix_and_num
        name_prefix: 远端Resource name前缀
        name_suffix: 远端Resource name后缀
        speed: 同步速率，Optional值：low, medium, high, highest, custom
        bandwidth: 自定义同步速率（MB/s），当 speed 为 custom 时Required
        recovery_policy: 恢复策略，Optional值：automatic, manual
        sync_type: 同步类型，Optional值：manual, wait_after_sync_begins, wait_after_sync_ends, specified_time_policy
        timing_value_in_sec: 定时时长（秒），当 sync_type 为 wait_after_sync_begins 或 wait_after_sync_ends 时Required
        sync_schedule: 定时规则，当 sync_type 为 specified_time_policy 时Required
        rep_io_timeout: 远端 IO 超时时间（秒），当复制模式为同步模式时有效
        sync_snap_policy: 用户快照同步策略，Optional值：not_sync_snap, same_as_source, user_snap_retention_num, snap_tag_based
        user_snap_retention_num: 从端用户快照保留数量
        switch_to_async: 同步远程复制自动转换为异步远程复制的开关
        enable_compress: 链路压缩，当复制模式为异步模式时Required

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    修改复制 Pair

    Args:
        client: DME API client
        pair_id: 复制 Pair 实例 ID
        speed: 同步速率，Optional值：low, medium, high, highest, custom
        bandwidth: 自定义同步速率（MB/s），当 speed 为 custom 时Required
        recovery_policy: 恢复策略，Optional值：automatic, manual
        enable_compress: 链路压缩，当复制模式为异步模式时Required
        sync_type: 同步类型，Optional值：manual, wait_after_sync_begins, wait_after_sync_ends, specified_time_policy
        timing_value_in_sec: 定时时长（秒），当 sync_type 为 wait_after_sync_begins 或 wait_after_sync_ends 时Required
        sync_schedule: 定时规则，当 sync_type 为 specified_time_policy 时Required
        rep_io_timeout: 远端 IO 超时时间（秒），当复制模式为同步模式时有效
        sync_snap_policy: 用户快照同步策略，Optional值：not_sync_snap, same_as_source, user_snap_retention_num, snap_tag_based
        user_snap_retention_num: 从端用户快照保留数量
        switch_to_async: 同步远程复制自动转换为异步远程复制的开关

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    Batch delete远程复制 Pair

    Args:
        client: DME API client
        ids: 复制 Pair 实例 ID 列表
        delete_mode: 删除模式，Optional值：primary_only, secondary_only, dual_ends，默认 dual_ends

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    批量同步远程复制 Pair

    Args:
        client: DME API client
        ids: 复制 Pair ID 列表

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    批量分裂远程复制 Pair

    Args:
        client: DME API client
        ids: 复制 Pair ID 列表

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    远程复制 Pair 批量主从切换

    Args:
        client: DME API client
        ids: 复制 Pair ID 列表

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    远程复制 Pair 从资源保护状态切换

    Args:
        client: DME API client
        id: 复制 Pair ID
        operation_type: 操作类型，Optional值：enable（开启）, disable（取消）

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/replication/pairs/{id}/switch-write-protection"

    payload = {
        'operation_type': operation_type
    }

    response = client.post(url, body=payload, params={"id": id})
    return response


# ============================================================================
# device 子主题 - 设备 Pair 和复制链路operations
# ============================================================================

def device_pair_list(client: DMEAPIClient, storage_id: str = None) -> dict:
    """
    查询设备 Pairs

    Args:
        client: DME API client
        storage_id: Storage device ID

    Returns:
        设备 Pairs 列表
    """
    url = "/rest/protection/v1/device-pairs/query"

    payload = {}

    if storage_id is not None:
        payload['storage_id'] = storage_id

    response = client.post(url, body=payload)
    return response


def replication_link_list(client: DMEAPIClient, storage_id: str = None) -> dict:
    """
    查询复制链路

    Args:
        client: DME API client
        storage_id: Storage device ID

    Returns:
        复制链路列表
    """
    url = "/rest/protection/v1/replication-links/query"

    payload = {}

    if storage_id is not None:
        payload['storage_id'] = storage_id

    response = client.post(url, body=payload)
    return response


# ============================================================================
# snapshot 子主题 - LUN 快照operations
# ============================================================================

def snapshot_list(client: DMEAPIClient, snapshot_ids: list = None, storage_id: str = None,
                  raw_id: str = None, name: str = None, health_status: str = None,
                  running_status: str = None, source_lun_name: str = None,
                  parent_name: str = None, activated_time_from: int = None,
                  activated_time_to: int = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch query LUN 快照

    Args:
        client: DME API client
        snapshot_ids: 快照 ID 列表
        storage_id: Storage device ID
        raw_id: 快照在存储设备上的 ID
        name: 快照名称，supports fuzzy search
        health_status: Health status，Optional值：normal, fault, write_protected
        running_status: 运行状态，Optional值：activated, rolling_back, unactivated, initializing, deleting, unknown
        source_lun_name: 源 LUN 名称，supports fuzzy search
        parent_name: 父Object name，supports fuzzy search
        activated_time_from: 查询激活时间的起始点（Unix 时间戳，单位秒）
        activated_time_to: 查询激活时间的结束点（Unix 时间戳，单位秒）
        page_no: 分页查询的开始页，min为 1，Default为 1
        page_size: 每页数量，1~1000，默认 20

    Returns:
        LUN 快照列表
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
    Batch create LUN 快照

    Args:
        client: DME API client
        snapshots_info: LUN 快照创建信息列表，每项包含 name, source_type, source_id
        is_consist_activate: 是否一致性激活，默认 false

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    批量回滚 LUN 快照

    Args:
        client: DME API client
        rollback_speed: 回滚速率，Optional值：low, medium, high, highest
        rollback_snapshots: 快照回滚的资源信息列表，每项包含 snapshot_id, target_type, target_id

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    Batch delete LUN 快照

    Args:
        client: DME API client
        snapshot_ids: 快照 ID 列表
        is_delete_target_lun: 是否删除目标 LUN，默认 true
        is_auto_deactivate: 是否在删除前自动取消激活快照，默认 false

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
# snapshot_group 子主题 - 快照一致性组operations
# ============================================================================

def snapshot_group_create(client: DMEAPIClient, name: str, protect_group_id: str,
                          description: str = None, creation_mode: str = None) -> dict:
    """
    创建快照一致性组

    Args:
        client: DME API client
        name: 快照一致性组名称
        protect_group_id: 保护组的 ID
        description: Description
        creation_mode: 创建模式，Optional值：new_snapshot

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    Batch delete快照一致性组

    Args:
        client: DME API client
        snapshot_cg_ids: 快照一致性组 ID 列表
        is_delete_target_lun: 是否删除目标 LUN，仅 Dorado 6.1.2 及以上版本支持，默认 true

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    激活快照一致性组

    Args:
        client: DME API client
        snapshot_cg_id: 快照一致性组 ID
        object_type: Object type，Optional值：parent_object
        snapshot_create_mode: 快照创建方式，Optional值：auto, manual
        name_rule: 快照名称命名规则，Optional值：prefix_and_suffix, prefix_and_num
        name_prefix: 快照名称前缀
        name_suffix: 快照名称后缀
        target_snapshot_objects: 目标快照object列表

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    批量取消激活快照一致性组

    Args:
        client: DME API client
        snapshot_cg_ids: 快照一致性组 ID 列表

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    回滚快照一致性组

    Args:
        client: DME API client
        snapshot_cg_id: 快照一致性组 ID
        rollback_speed: 回滚速率，Optional值：low, medium, high, highest
        snapshot_create_mode: 快照创建方式，Optional值：auto, manual
        name_rule: 快照名称命名规则，Optional值：prefix_and_suffix, prefix_and_num
        name_prefix: 快照名称前缀
        name_suffix: 快照名称后缀
        target_snapshot_objects: 目标快照object列表

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
# clone_group 子主题 - 克隆一致性组operations
# ============================================================================

def clone_group_create(client: DMEAPIClient, name: str, protect_group_id: str,
                       create_mode: str, description: str = None, name_rule: str = None,
                       name_prefix: str = None, name_suffix: str = None,
                       copy_rate: str = None, is_sync: bool = None,
                       clone_pairs: list = None) -> dict:
    """
    创建克隆一致性组

    Args:
        client: DME API client
        name: 克隆一致性组名称
        protect_group_id: 保护组 ID
        create_mode: 创建模式，Optional值：auto, manual
        description: Description
        name_rule: 目标 LUN 名称命名规则，Optional值：prefix_and_suffix, prefix_and_num
        name_prefix: 目标 LUN 名称前缀
        name_suffix: 目标 LUN 名称后缀
        copy_rate: 拷贝速率，Optional值：low, medium, high, highest，默认 medium
        is_sync: 是否立即同步，默认 true
        clone_pairs: 克隆 Pair 列表，create_mode 为 manual 时Required

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    同步克隆一致性组

    Args:
        client: DME API client
        clone_group_id: 克隆一致性组 ID
        create_mode: 克隆 Pair 创建模式，Optional值：auto, manual
        name_rule: 目标 LUN 名称命名规则，Optional值：prefix_and_suffix, prefix_and_num
        name_prefix: 目标 LUN 名称前缀
        name_suffix: 目标 LUN 名称后缀
        clone_pairs: 克隆 Pair 列表，create_mode 为 manual 时Required

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    Batch delete克隆一致性组

    Args:
        client: DME API client
        ids: 克隆一致性组 ID 列表
        is_delete_dst_lun: 是否删除目标 LUN
        is_recycle_dst_lun_data: 是否回收目标 LUN 数据

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
# replication_group 子主题 - 复制一致性组operations
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
    创建远程复制一致性组

    Args:
        client: DME API client
        cg_name: 远程复制一致性组名称
        remote_storage_id: 远端Storage device ID
        local_pg_id: 本端保护组的 ID，当Storage device version是 OceanStor V6、OceanStor Dorado V6 时必传
        description: Description
        remote_lun_group_id: 远端 LUN 组的 ID，当Storage device version是 OceanStor V6、OceanStor Dorado V6 时且本端保护组是基于 LUN 组创建的时必传
        local_storage_id: 本端Storage device ID，当Storage device version不是 OceanStor V6、OceanStor Dorado V6 时必传
        create_mode: 复制 Pair 的创建模式，Optional值：auto（自动）, manual（手动）
        existed_pair_ids: 已存在的复制 Pair 的 ID 列表
        lun_pairs: 手动创建模式下，复制 Pair 的源 LUN、目标 LUN 的 ID 列表
        lun_ids: 自动创建模式下，源 LUN 的 ID 列表
        remote_storage_pool_id: 远端存储池 ID，自动创建模式下有效
        remote_vstore_id: 远端设备的租户 ID，自动创建模式下有效
        remote_resource_name_rule: 远端资源的名称策略，Optional值：same_as_local, prefix_and_suffix, prefix_and_num
        name_prefix: 远端Resource name前缀
        name_suffix: 远端Resource name后缀

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    修改远程复制一致性组

    Args:
        client: DME API client
        replication_group_id: 远程复制一致性组 ID
        name: 远程复制一致性组名称
        description: Description
        speed: 同步速率，Optional值：low, medium, high, highest, custom
        bandwidth: 自定义同步速率（MB/s），当 speed 为 custom 时Required
        recovery_policy: 恢复策略，Optional值：automatic, manual
        enable_compress: 链路压缩，当复制模式为异步模式时Required
        sync_type: 同步类型，Optional值：manual, wait_after_sync_begins, wait_after_sync_ends, specified_time_policy
        timing_value_in_sec: 定时时长（秒），当 sync_type 为 wait_after_sync_begins 或 wait_after_sync_ends 时Required
        sync_schedule: 定时规则，当 sync_type 为 specified_time_policy 时Required
        rep_io_timeout: 远端 IO 超时时间（秒），当复制模式为同步模式时有效
        sync_snap_policy: 用户快照同步策略，Optional值：not_sync_snap, same_as_source, user_snap_retention_num, snap_tag_based
        user_snap_retention_num: 从端用户快照保留数量
        switch_to_async: 同步远程复制自动转换为异步远程复制的开关

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    Batch delete远程复制一致性组

    Args:
        client: DME API client
        ids: 远程复制一致性组 ID 列表
        is_self_adapt: 是否支持自适应移除成员 Pair，默认 false
        delete_mode: 删除模式，Optional值：primary_only, secondary_only, dual_ends，默认 dual_ends

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    远程复制一致性组添加成员 Pair

    Args:
        client: DME API client
        group_id: 远程复制一致性组的 ID
        pair_ids: 远程复制 Pair 的 ID 列表

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    远程复制一致性组移除成员 Pair

    Args:
        client: DME API client
        group_id: 远程复制一致性组的 ID
        pair_ids: 远程复制 Pair 的 ID 列表

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    批量同步远程复制一致性组

    >![](public_sys-resources/icon-notice.gif) **须知：**
    >该 API 可能会直接或间接影响现网业务运行，导致业务中断、关键数据丢失等，请谨慎操作。

    Args:
        client: DME API client
        ids: 一致性组的 ID 列表

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    批量分裂远程复制一致性组

    >![](public_sys-resources/icon-notice.gif) **须知：**
    >该 API 可能会直接或间接影响现网业务运行，导致业务中断、关键数据丢失等，请谨慎操作。

    Args:
        client: DME API client
        ids: 一致性组的 ID 列表

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    远程复制一致性组批量主从切换

    >![](public_sys-resources/icon-notice.gif) **须知：**
    >该 API 可能会直接或间接影响现网业务运行，导致业务中断、关键数据丢失等，请谨慎操作。

    Args:
        client: DME API client
        ids: 一致性组的 ID 列表

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    远程复制一致性组从资源写保护状态切换

    Args:
        client: DME API client
        id: 一致性组的 ID
        operation_type: 操作类型，Optional值：enable（开启）, disable（取消）

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/replication/groups/{id}/switch-write-protection"

    payload = {
        'operation_type': operation_type
    }

    response = client.post(url, body=payload, params={"id": id})
    return response


# ============================================================================
# 文件系统双活Pair (fs_hypermetro_pair) subtopic functions
# ============================================================================


def filesystem_pair_create(client: DMEAPIClient, vstore_pair_id: str,
                            create_mode: str = "manual", fs_pairs: list = None,
                            speed: str = None, bandwidth: int = None,
                            service_assurance_policy: str = None,
                            isolation_threshold_time: int = None) -> dict:
    """
    创建文件系统双活Pair。该API可能会直接或间接影响现网业务运行，请谨慎操作。

    Args:
        client: DME API client
        vstore_pair_id: 双活租户Pair的ID (Required, string, 1~32个字符)
        create_mode: 创建模式 (Optional, string)。Optional值：manual (手动)。Default：manual
        fs_pairs: 文件系统Pair列表 (Optional, List[FsPairInstance], max array members：100)
        speed: 同步速率 (Optional, string)。Optional值：low, medium, high, highest, custom
        bandwidth: 带宽 (Optional, integer, 1~1024)。当speed为custom时Required
        service_assurance_policy: 业务保障策略 (Optional, string)。Optional值：data_reliability_preferred, service_continuity_preferred
        isolation_threshold_time: 隔离阈值 (Optional, int32, 10~30000)

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/hypermetro/filesystem-pairs"

    if not vstore_pair_id:
        raise ValueError("vstore_pair_id 是required parameter")

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
    查询Filesystem active-active pair list。

    Args:
        client: DME API client
        ids: 双活Pair实例ID列表 (Optional, List[string])
        name: 双活Pair名称 (Optional, string)
        status: 运行状态 (Optional, string)
        storage_id: Storage device ID (Optional, string)
        vstore_pair_id: 双活租户Pair的ID (Optional, string)
        local_fs_name: 本端Filesystem name (Optional, string)
        local_fs_id: 本端Filesystem ID (Optional, string)
        health_status: Health status (Optional, string)
        running_status: 运行状态 (Optional, string)
        sort_key: 排序字段 (Optional, string)
        sort_dir: 排序方向 (Optional, string)
        page_no: 分页页码 (Optional, int32)
        page_size: 每页数量 (Optional, int32)

    Returns:
        {
            total: 总数 (integer),
            filesystem_pairs: Filesystem active-active pair list。参数格式如下：[{
                id: Pair ID (string),
                name: 名称 (string),
                status: 状态 (string),
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
    批量暂停文件系统双活Pair。该API可能会直接或间接影响现网业务运行，请谨慎操作。

    Args:
        client: DME API client
        fs_pair_ids: 文件系统双活Pair的ID列表 (Required, List[string], max array members：100, min array members：1)

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/hypermetro/filesystem-pairs/pause"

    if not fs_pair_ids or len(fs_pair_ids) == 0:
        raise ValueError("fs_pair_ids 是required parameter")

    payload = {
        'fs_pair_ids': fs_pair_ids
    }

    response = client.post(url, body=payload)
    return response


def filesystem_pair_sync(client: DMEAPIClient, fs_pair_ids: list) -> dict:
    """
    批量同步文件系统双活Pair。该API可能会直接或间接影响现网业务运行，请谨慎操作。

    Args:
        client: DME API client
        fs_pair_ids: 文件系统双活Pair的ID列表 (Required, List[string])

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/hypermetro/filesystem-pairs/sync"

    if not fs_pair_ids or len(fs_pair_ids) == 0:
        raise ValueError("fs_pair_ids 是required parameter")

    payload = {
        'fs_pair_ids': fs_pair_ids
    }

    response = client.post(url, body=payload)
    return response


def filesystem_pair_delete(client: DMEAPIClient, ids: list,
                            is_local_delete: bool = None,
                            is_online_delete: bool = None) -> dict:
    """
    Batch delete文件系统双活Pair。该API可能会直接或间接影响现网业务运行，请谨慎操作。

    Args:
        client: DME API client
        ids: 双活Pair实例ID列表 (Required, List[string])
        is_local_delete: 是否删除本端Configuration info (Optional, boolean, true,false)
        is_online_delete: 是否在线删除 (Optional, boolean, true,false)

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/hypermetro/filesystem-pairs/delete"

    if not ids or len(ids) == 0:
        raise ValueError("ids 是required parameter")

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
# 文件系统快照 (fs_snapshot) subtopic functions
# ============================================================================


def fs_snapshot_create(client: DMEAPIClient, vstore_pair_id: str,
                        fs_pairs: list) -> dict:
    """
    创建文件系统快照。

    Args:
        client: DME API client
        vstore_pair_id: 文件名系统所属双活租户Pair的ID (Required, string)
        fs_pairs: 快照参数列表 (Required, List)

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/filesystem-snapshots"

    if not vstore_pair_id:
        raise ValueError("vstore_pair_id 是required parameter")

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
    Batch query文件系统快照。

    Args:
        client: DME API client
        fs_pair_id: 双活Pair ID (Optional, string)
        name: 快照名称 (Optional, string, supports fuzzy search)
        status: 快照状态 (Optional, string)
        local_fs_name: 本端Filesystem name (Optional, string)
        local_fs_id: 本端Filesystem ID (Optional, string)
        page_no: 分页页码 (Optional, int32)
        page_size: 每页数量 (Optional, int32)

    Returns:
        {
            total: 总数 (integer),
            snapshots: Filesystem snapshot list。参数格式如下：[{
                id: 快照ID (string),
                name: 快照名称 (string),
                status: 状态 (string),
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
    Batch delete文件系统快照。

    Args:
        client: DME API client
        ids: 快照ID列表 (Required, List[string])

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/filesystem-snapshots/delete"

    if not ids or len(ids) == 0:
        raise ValueError("ids 是required parameter")

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


# ============================================================================
# 双活租户Pair (vstore_hypermetro_pair) subtopic functions
# ============================================================================


def vstore_pair_force_start(client: DMEAPIClient, ids: list) -> dict:
    """
    批量强制启动双活租户Pair。

    Args:
        client: DME API client
        ids: 双活租户Pair的ID列表 (Required, List[string])

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/metro/vstore-pairs/force-start"

    if not ids or len(ids) == 0:
        raise ValueError("ids 是required parameter")

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
    创建双活租户Pair。

    Args:
        client: DME API client
        local_storage_id: 本端Storage device ID (Required, string)
        remote_storage_id: 远端Storage device ID (Required, string)
        name: 租户Pair名称 (Optional, string)
        description: 描述 (Optional, string)
        remote_vstore_id: 远端Tenant ID (Optional, string)

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/metro/vstore-pairs"

    if not local_storage_id or not remote_storage_id:
        raise ValueError("local_storage_id 和 remote_storage_id 是required parameter")

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
    查询Active-active tenant pair list。

    Args:
        client: DME API client
        ids: 双活租户Pair ID列表 (Optional, List[string])
        name: 名称 (Optional, string)
        status: 状态 (Optional, string)
        local_storage_id: 本端Storage device ID (Optional, string)
        remote_storage_id: 远端Storage device ID (Optional, string)
        health_status: Health status (Optional, string)
        running_status: 运行状态 (Optional, string)
        page_no: 分页页码 (Optional, int32)
        page_size: 每页数量 (Optional, int32)

    Returns:
        {
            total: 总数 (integer),
            vstore_pairs: Active-active tenant pair list。参数格式如下：[{
                id: Pair ID (string),
                name: 名称 (string),
                status: 状态 (string),
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
    批量主从切换双活租户Pair。

    Args:
        client: DME API client
        ids: 双活租户Pair的ID列表 (Required, List[string])

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/metro/vstore-pairs/switch"

    if not ids or len(ids) == 0:
        raise ValueError("ids 是required parameter")

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def vstore_pair_delete(client: DMEAPIClient, ids: list) -> dict:
    """
    Batch delete双活租户Pair。

    Args:
        client: DME API client
        ids: 双活租户Pair的ID列表 (Required, List[string])

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/metro/vstore-pairs/delete"

    if not ids or len(ids) == 0:
        raise ValueError("ids 是required parameter")

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def vstore_pair_modify(client: DMEAPIClient, id: str, name: str = None) -> dict:
    """
    Modify双活租户pair。

    Args:
        client: DME API client
        id: 双活租户Pair的ID (Required, string)
        name: 名称 (Optional, string)

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/metro/vstore-pairs/{id}"

    if not id:
        raise ValueError("id 是required parameter")

    payload = {}
    if name is not None:
        payload['name'] = name

    response = client.put(url, body=payload, params={"id": id})
    return response


# ============================================================================
# 双活域 (hypermetro_domain) subtopic functions
# ============================================================================


def hypermetro_domain_force_start(client: DMEAPIClient, id: str) -> dict:
    """
    强制启动文件系统双活域。

    Args:
        client: DME API client
        id: 双活域ID (Required, string)

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/hyper-metro-domains/{id}/force-start"

    if not id:
        raise ValueError("id 是required parameter")

    response = client.post(url, body={}, params={"id": id})
    return response


def hypermetro_domain_switch_site(client: DMEAPIClient, id: str) -> dict:
    """
    优先站点切换文件系统双活域。

    Args:
        client: DME API client
        id: 双活域ID (Required, string)

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/hyper-metro-domains/{id}/switch-priority-site"

    if not id:
        raise ValueError("id 是required parameter")

    response = client.post(url, body={}, params={"id": id})
    return response


def hypermetro_domain_recover(client: DMEAPIClient, id: str) -> dict:
    """
    恢复文件系统双活域。

    Args:
        client: DME API client
        id: 双活域ID (Required, string)

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/hyper-metro-domains/{id}/recover"

    if not id:
        raise ValueError("id 是required parameter")

    response = client.post(url, body={}, params={"id": id})
    return response


def hypermetro_domain_split(client: DMEAPIClient, id: str) -> dict:
    """
    分裂文件系统双活域。

    Args:
        client: DME API client
        id: 双活域ID (Required, string)

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/hyper-metro-domains/{id}/split"

    if not id:
        raise ValueError("id 是required parameter")

    response = client.post(url, body={}, params={"id": id})
    return response


def hypermetro_domain_swap_role(client: DMEAPIClient, id: str) -> dict:
    """
    主从切换文件系统双活域。

    Args:
        client: DME API client
        id: 双活域ID (Required, string)

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/hyper-metro-domains/{id}/swap-role"

    if not id:
        raise ValueError("id 是required parameter")

    response = client.post(url, body={}, params={"id": id})
    return response


# ============================================================================
# 双活Pair (hypermetro_pair) subtopic functions
# ============================================================================


def hypermetro_pair_query_available_luns(client: DMEAPIClient,
                                          source_lun_id: str) -> dict:
    """
    查询可创建双活Pair的目标LUN。

    Args:
        client: DME API client
        source_lun_id: 源LUN ID (Required, string)

    Returns:
        {
            optional_target_luns: Optional目标LUN列表。参数格式如下：[{
                lun_id: LUN ID (string),
                lun_name: LUN名称 (string),
                capacity: 容量 (integer),
            }, ...],
        }
    """
    url = "/rest/protection/v1/metro/lun-pairs/{source_lun_id}/optional-target-luns"

    if not source_lun_id:
        raise ValueError("source_lun_id 是required parameter")

    response = client.get(url, params={"source_lun_id": source_lun_id})
    return response


# Action list for CLI help
ACTIONS = {
    # group 子主题动作
    'group_list': {
        'func': group_list,
        'description': 'Batch query保护组',
        'params': ['name', 'project_id', 'storage_name', 'storage_id', 'raw_id', 'lun_group_raw_id', 'vstore_id', 'vstore_raw_id', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'group'
    },
    'group_create': {
        'func': group_create,
        'description': '创建保护组',
        'params': ['name', 'storage_id', 'lun_ids', 'lun_group_id', 'description'],
        'subtopic': 'group'
    },
    'group_modify': {
        'func': group_modify,
        'description': '修改保护组',
        'params': ['pg_id', 'name', 'description'],
        'subtopic': 'group'
    },
    'group_delete': {
        'func': group_delete,
        'description': 'Batch delete保护组',
        'params': ['pg_ids'],
        'subtopic': 'group'
    },
    'group_add_luns': {
        'func': group_add_luns,
        'description': '保护组中添加成员 LUN',
        'params': ['pg_id', 'lun_ids', 'hyper_metro', 'rem_reps'],
        'subtopic': 'group'
    },
    'group_remove_luns': {
        'func': group_remove_luns,
        'description': '移除保护组中的成员 LUN',
        'params': ['pg_id', 'lun_ids', 'is_delay'],
        'subtopic': 'group'
    },
    # hypermetro_group 子主题动作
    'hypermetro_group_list': {
        'func': hypermetro_group_list,
        'description': 'Batch query双活一致性组',
        'params': ['page_no', 'page_size', 'name', 'raw_id', 'protect_group_id', 'storage_id', 'storage_name', 'local_vstore_id', 'local_vstore_raw_id', 'remote_vstore_id', 'remote_vstore_raw_id'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_create': {
        'func': hypermetro_group_create,
        'description': '创建双活一致性组',
        'params': ['domain_id', 'name', 'local_storage_id', 'local_pg_id', 'description', 'create_mode', 'remote_vstore_id', 'remote_storage_pool_id', 'lun_ids', 'remote_resource_name_rule'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_modify': {
        'func': hypermetro_group_modify,
        'description': '修改双活一致性组',
        'params': ['group_id', 'name', 'description', 'recovery_policy', 'service_assurance_policy', 'speed', 'bandwidth', 'isolation_threshold_time'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_delete': {
        'func': hypermetro_group_delete,
        'description': 'Batch delete双活一致性组',
        'params': ['ids', 'is_self_adapt', 'delete_mode'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_add_pairs': {
        'func': hypermetro_group_add_pairs,
        'description': '双活一致性组添加成员 Pair',
        'params': ['group_id', 'pair_ids', 'is_self_adapt'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_remove_pairs': {
        'func': hypermetro_group_remove_pairs,
        'description': '双活一致性组移除成员 Pair',
        'params': ['group_id', 'pair_ids'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_pause': {
        'func': hypermetro_group_pause,
        'description': '暂停双活一致性组',
        'params': ['ids', 'priority_station_type'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_force_startup': {
        'func': hypermetro_group_force_startup,
        'description': '强制启动双活一致性组',
        'params': ['ids', 'priority_station_type'],
        'subtopic': 'hypermetro_group'
    },
    'hypermetro_group_switch_priority': {
        'func': hypermetro_group_switch_priority,
        'description': '双活一致性组优先站点切换',
        'params': ['ids'],
        'subtopic': 'hypermetro_group'
    },
    # hypermetro_pair 子主题动作
    'hypermetro_pair_list': {
        'func': hypermetro_pair_list,
        'description': 'Batch query LUN 双活 Pair',
        'params': ['page_no', 'page_size', 'group_id', 'group_name', 'group_raw_id', 'pair_raw_id', 'local_storage_id', 'local_storage_name', 'local_vstore_id', 'local_vstore_raw_id', 'local_volume_name', 'local_host_access_state', 'remote_vstore_id', 'remote_vstore_raw_id', 'remote_volume_name'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_create': {
        'func': hypermetro_pair_create,
        'description': '创建双活 Pair',
        'params': ['create_mode', 'lun_pairs', 'lun_ids', 'remote_storage_pool_id', 'remote_vstore_id', 'remote_resource_name_rule', 'name_prefix', 'name_suffix', 'local_storage_id', 'domain_id', 'speed', 'bandwidth', 'service_assurance_policy', 'isolation_threshold_time', 'recovery_policy'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_modify': {
        'func': hypermetro_pair_modify,
        'description': '修改双活 Pair',
        'params': ['pair_id', 'speed', 'bandwidth', 'recovery_policy', 'service_assurance_policy', 'isolation_threshold_time'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_delete': {
        'func': hypermetro_pair_delete,
        'description': 'Batch delete双活 Pair',
        'params': ['ids', 'delete_mode', 'is_lun_service_interrupt'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_sync': {
        'func': hypermetro_pair_sync,
        'description': '同步双活 Pair',
        'params': ['ids'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_pause': {
        'func': hypermetro_pair_pause,
        'description': '暂停双活 Pair',
        'params': ['ids', 'priority_station_type'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_force_startup': {
        'func': hypermetro_pair_force_startup,
        'description': '强制启动双活 Pair',
        'params': ['ids', 'priority_station_type'],
        'subtopic': 'hypermetro_pair'
    },
    'hypermetro_pair_switch_priority': {
        'func': hypermetro_pair_switch_priority,
        'description': '双活 Pair 优先站点切换',
        'params': ['ids'],
        'subtopic': 'hypermetro_pair'
    },
    # hypermetro_domain 子主题动作
    'hypermetro_domain_list': {
        'func': hypermetro_domain_list,
        'description': 'Batch query双活域',
        'params': ['storage_id', 'types'],
        'subtopic': 'hypermetro_domain'
    },
    # replication_group 子主题动作
    'replication_group_create': {
        'func': replication_group_create,
        'description': '创建远程复制一致性组',
        'params': ['cg_name', 'remote_storage_id', 'local_pg_id', 'description', 'remote_lun_group_id', 'local_storage_id', 'create_mode', 'existed_pair_ids', 'lun_pairs', 'lun_ids', 'remote_storage_pool_id', 'remote_vstore_id', 'remote_resource_name_rule', 'name_prefix', 'name_suffix'],
        'subtopic': 'replication_group'
    },
    'replication_group_modify': {
        'func': replication_group_modify,
        'description': '修改远程复制一致性组',
        'params': ['replication_group_id', 'name', 'description', 'speed', 'bandwidth', 'recovery_policy', 'enable_compress', 'sync_type', 'timing_value_in_sec', 'sync_schedule', 'rep_io_timeout', 'sync_snap_policy', 'user_snap_retention_num', 'switch_to_async'],
        'subtopic': 'replication_group'
    },
    'replication_group_delete': {
        'func': replication_group_delete,
        'description': 'Batch delete远程复制一致性组',
        'params': ['ids', 'is_self_adapt', 'delete_mode'],
        'subtopic': 'replication_group'
    },
    'replication_group_add_pairs': {
        'func': replication_group_add_pairs,
        'description': '远程复制一致性组添加成员 Pair',
        'params': ['group_id', 'pair_ids'],
        'subtopic': 'replication_group'
    },
    'replication_group_remove_pairs': {
        'func': replication_group_remove_pairs,
        'description': '远程复制一致性组移除成员 Pair',
        'params': ['group_id', 'pair_ids'],
        'subtopic': 'replication_group'
    },
    'replication_group_sync': {
        'func': replication_group_sync,
        'description': '批量同步远程复制一致性组',
        'params': ['ids'],
        'subtopic': 'replication_group'
    },
    'replication_group_split': {
        'func': replication_group_split,
        'description': '批量分裂远程复制一致性组',
        'params': ['ids'],
        'subtopic': 'replication_group'
    },
    'replication_group_switch': {
        'func': replication_group_switch,
        'description': '远程复制一致性组批量主从切换',
        'params': ['ids'],
        'subtopic': 'replication_group'
    },
    'replication_group_switch_write_protection': {
        'func': replication_group_switch_write_protection,
        'description': '远程复制一致性组从资源写保护状态切换',
        'params': ['id', 'operation_type'],
        'subtopic': 'replication_group'
    },
    # replication_pair 子主题动作
    'replication_pair_list': {
        'func': replication_pair_list,
        'description': 'Batch query复制 Pair',
        'params': ['page_no', 'page_size', 'group_id', 'group_name', 'pair_raw_id', 'local_storage_id', 'local_storage_name', 'local_vstore_id', 'local_vstore_raw_id', 'local_volume_name', 'remote_vstore_id', 'remote_vstore_raw_id', 'remote_volume_name'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_create': {
        'func': replication_pair_create,
        'description': '创建远程复制 Pair',
        'params': ['local_storage_id', 'local_lun_id', 'remote_storage_id', 'remote_storage_pool_id', 'remote_vstore_id', 'remote_resource_name_rule', 'name_prefix', 'name_suffix', 'speed', 'bandwidth', 'recovery_policy', 'sync_type', 'timing_value_in_sec', 'sync_schedule', 'rep_io_timeout', 'sync_snap_policy', 'user_snap_retention_num', 'switch_to_async', 'enable_compress'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_modify': {
        'func': replication_pair_modify,
        'description': '修改复制 Pair',
        'params': ['pair_id', 'speed', 'bandwidth', 'recovery_policy', 'enable_compress', 'sync_type', 'timing_value_in_sec', 'sync_schedule', 'rep_io_timeout', 'sync_snap_policy', 'user_snap_retention_num', 'switch_to_async'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_delete': {
        'func': replication_pair_delete,
        'description': 'Batch delete远程复制 Pair',
        'params': ['ids', 'delete_mode'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_sync': {
        'func': replication_pair_sync,
        'description': '批量同步远程复制 Pair',
        'params': ['ids'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_split': {
        'func': replication_pair_split,
        'description': '批量分裂远程复制 Pair',
        'params': ['ids'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_switch': {
        'func': replication_pair_switch,
        'description': '远程复制 Pair 批量主从切换',
        'params': ['ids'],
        'subtopic': 'replication_pair'
    },
    'replication_pair_switch_write_protection': {
        'func': replication_pair_switch_write_protection,
        'description': '远程复制 Pair 从资源保护状态切换',
        'params': ['id', 'operation_type'],
        'subtopic': 'replication_pair'
    },
    # device 子主题动作
    'device_pair_list': {
        'func': device_pair_list,
        'description': '查询设备 Pairs',
        'params': ['storage_id'],
        'subtopic': 'device_pair'
    },
    'replication_link_list': {
        'func': replication_link_list,
        'description': '查询复制链路',
        'params': ['storage_id'],
        'subtopic': 'replication_link'
    },
    # snapshot 子主题动作
    'snapshot_list': {
        'func': snapshot_list,
        'description': 'Batch query LUN 快照',
        'params': ['snapshot_ids', 'storage_id', 'raw_id', 'name', 'health_status', 'running_status', 'source_lun_name', 'parent_name', 'activated_time_from', 'activated_time_to', 'page_no', 'page_size'],
        'subtopic': 'snapshot'
    },
    'snapshot_create': {
        'func': snapshot_create,
        'description': 'Batch create LUN 快照',
        'params': ['snapshots_info', 'is_consist_activate'],
        'subtopic': 'snapshot'
    },
    'snapshot_rollback': {
        'func': snapshot_rollback,
        'description': '批量回滚 LUN 快照',
        'params': ['rollback_speed', 'rollback_snapshots'],
        'subtopic': 'snapshot'
    },
    'snapshot_delete': {
        'func': snapshot_delete,
        'description': 'Batch delete LUN 快照',
        'params': ['snapshot_ids', 'is_delete_target_lun', 'is_auto_deactivate'],
        'subtopic': 'snapshot'
    },
    # snapshot_group 子主题动作
    'snapshot_group_create': {
        'func': snapshot_group_create,
        'description': '创建快照一致性组',
        'params': ['name', 'protect_group_id', 'description', 'creation_mode'],
        'subtopic': 'snapshot_group'
    },
    'snapshot_group_delete': {
        'func': snapshot_group_delete,
        'description': 'Batch delete快照一致性组',
        'params': ['snapshot_cg_ids', 'is_delete_target_lun'],
        'subtopic': 'snapshot_group'
    },
    'snapshot_group_activate': {
        'func': snapshot_group_activate,
        'description': '激活快照一致性组',
        'params': ['snapshot_cg_id', 'object_type', 'snapshot_create_mode', 'name_rule', 'name_prefix', 'name_suffix', 'target_snapshot_objects'],
        'subtopic': 'snapshot_group'
    },
    'snapshot_group_deactivate': {
        'func': snapshot_group_deactivate,
        'description': '批量取消激活快照一致性组',
        'params': ['snapshot_cg_ids'],
        'subtopic': 'snapshot_group'
    },
    'snapshot_group_rollback': {
        'func': snapshot_group_rollback,
        'description': '回滚快照一致性组',
        'params': ['snapshot_cg_id', 'rollback_speed', 'snapshot_create_mode', 'name_rule', 'name_prefix', 'name_suffix', 'target_snapshot_objects'],
        'subtopic': 'snapshot_group'
    },
    # clone_group 子主题动作
    'clone_group_create': {
        'func': clone_group_create,
        'description': '创建克隆一致性组',
        'params': ['name', 'protect_group_id', 'create_mode', 'description', 'name_rule', 'name_prefix', 'name_suffix', 'copy_rate', 'is_sync', 'clone_pairs'],
        'subtopic': 'clone_group'
    },
    'clone_group_sync': {
        'func': clone_group_sync,
        'description': '同步克隆一致性组',
        'params': ['clone_cg_id', 'create_mode', 'name_rule', 'name_prefix', 'name_suffix', 'clone_pairs'],
        'subtopic': 'clone_group'
    },
    'clone_group_delete': {
        'func': clone_group_delete,
        'description': 'Batch delete克隆一致性组',
        'params': ['ids', 'is_delete_dst_lun', 'is_recycle_dst_lun_data'],
        'subtopic': 'clone_group'
    },
    # fs_hypermetro_pair 子主题动作
    'filesystem_pair_create': {
        'func': filesystem_pair_create,
        'description': '创建文件系统双活Pair',
        'params': ['vstore_pair_id', 'create_mode', 'fs_pairs', 'speed', 'bandwidth', 'service_assurance_policy', 'isolation_threshold_time'],
        'subtopic': 'fs_hypermetro_pair'
    },
    'filesystem_pair_list': {
        'func': filesystem_pair_list,
        'description': '查询Filesystem active-active pair list',
        'params': ['ids', 'name', 'status', 'storage_id', 'vstore_pair_id', 'local_fs_name', 'local_fs_id', 'health_status', 'running_status', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'fs_hypermetro_pair'
    },
    'filesystem_pair_pause': {
        'func': filesystem_pair_pause,
        'description': '批量暂停文件系统双活Pair',
        'params': ['fs_pair_ids'],
        'subtopic': 'fs_hypermetro_pair'
    },
    'filesystem_pair_sync': {
        'func': filesystem_pair_sync,
        'description': '批量同步文件系统双活Pair',
        'params': ['fs_pair_ids'],
        'subtopic': 'fs_hypermetro_pair'
    },
    'filesystem_pair_delete': {
        'func': filesystem_pair_delete,
        'description': 'Batch delete文件系统双活Pair',
        'params': ['ids', 'is_local_delete', 'is_online_delete'],
        'subtopic': 'fs_hypermetro_pair'
    },
    # fs_snapshot 子主题动作
    'fs_snapshot_create': {
        'func': fs_snapshot_create,
        'description': '创建文件系统快照',
        'params': ['vstore_pair_id', 'fs_pairs'],
        'subtopic': 'fs_snapshot'
    },
    'fs_snapshot_list': {
        'func': fs_snapshot_list,
        'description': 'Batch query文件系统快照',
        'params': ['fs_pair_id', 'name', 'status', 'local_fs_name', 'local_fs_id', 'page_no', 'page_size'],
        'subtopic': 'fs_snapshot'
    },
    'fs_snapshot_delete': {
        'func': fs_snapshot_delete,
        'description': 'Batch delete文件系统快照',
        'params': ['ids'],
        'subtopic': 'fs_snapshot'
    },
    # vstore_hypermetro_pair 子主题动作
    'vstore_pair_force_start': {
        'func': vstore_pair_force_start,
        'description': '批量强制启动双活租户Pair',
        'params': ['ids'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    'vstore_pair_create': {
        'func': vstore_pair_create,
        'description': '创建双活租户Pair',
        'params': ['local_storage_id', 'remote_storage_id', 'name', 'description', 'remote_vstore_id'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    'vstore_pair_list': {
        'func': vstore_pair_list,
        'description': '查询Active-active tenant pair list',
        'params': ['ids', 'name', 'status', 'local_storage_id', 'remote_storage_id', 'health_status', 'running_status', 'page_no', 'page_size'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    'vstore_pair_switch': {
        'func': vstore_pair_switch,
        'description': '批量主从切换双活租户Pair',
        'params': ['ids'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    'vstore_pair_delete': {
        'func': vstore_pair_delete,
        'description': 'Batch delete双活租户Pair',
        'params': ['ids'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    'vstore_pair_modify': {
        'func': vstore_pair_modify,
        'description': 'Modify双活租户pair',
        'params': ['id', 'name'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    # hypermetro_domain 子主题动作
    'hypermetro_domain_force_start': {
        'func': hypermetro_domain_force_start,
        'description': '强制启动文件系统双活域',
        'params': ['id'],
        'subtopic': 'hypermetro_domain'
    },
    'hypermetro_domain_switch_site': {
        'func': hypermetro_domain_switch_site,
        'description': '优先站点切换文件系统双活域',
        'params': ['id'],
        'subtopic': 'hypermetro_domain'
    },
    'hypermetro_domain_recover': {
        'func': hypermetro_domain_recover,
        'description': '恢复文件系统双活域',
        'params': ['id'],
        'subtopic': 'hypermetro_domain'
    },
    'hypermetro_domain_split': {
        'func': hypermetro_domain_split,
        'description': '分裂文件系统双活域',
        'params': ['id'],
        'subtopic': 'hypermetro_domain'
    },
    'hypermetro_domain_swap_role': {
        'func': hypermetro_domain_swap_role,
        'description': '主从切换文件系统双活域',
        'params': ['id'],
        'subtopic': 'hypermetro_domain'
    },
    # hypermetro_pair 子主题动作
    'query_available_luns': {
        'func': hypermetro_pair_query_available_luns,
        'description': '查询可创建双活Pair的目标LUN',
        'params': ['source_lun_id'],
        'subtopic': 'hypermetro_pair'
    },
}
