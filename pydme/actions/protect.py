"""
保护 (Protection) 相关操作
"""

import sys
import os

from pydme.client import DMEAPIClient


# ============================================================================
# group 子主题 - 保护组相关操作
# ============================================================================

def group_list(client: DMEAPIClient, name: str = None, project_id: str = None,
               storage_name: str = None, storage_id: str = None,
               raw_id: str = None, lun_group_raw_id: str = None,
               vstore_id: str = None, vstore_raw_id: str = None,
               sort_key: str = None, sort_dir: str = None,
               page_no: int = 1, page_size: int = 20) -> dict:
    """
    批量query保护组

    Args:
        client: DME API client
        name: 保护组name, 支持模糊搜索
        project_id: 业务群组 ID, 支持条件过滤
        storage_name: storage device name, 支持模糊搜索
        storage_id: Storage device ID, 支持条件过滤
        raw_id: 保护组在设备上的 ID, 支持精确搜索, 支持排序
        lun_group_raw_id: LUN group在设备上的 ID, 支持条件过滤
        vstore_id: 所属租户的 ID, 该参数和 vstore_raw_id 互斥
        vstore_raw_id: 所属租户在设备上的 ID, 该参数和 vstore_id 互斥
        sort_key: 排序字段, valid values: sort_id
        sort_dir: 排序方向, valid values: asc, desc (default desc)
        page_no: 分页query页码, default 1
        page_size: 每页显示的count, default 20

    Returns:
        {
            total: 保护组total (int32),
            groups: 保护组list (List<ProtectionGroupResponse>). parameter format: [{
                id: 保护组唯一标识ID (string, 1~64个字符),
                name: 保护组name (string, 1~256个字符),
                description: 保护组description (string, 0~255个字符),
                raw_id: 保护组在设备上的ID (string, 1~64个字符),
                storage_id: 所属storage device ID (string, 1~64个字符),
                storage_sn: storage设备SN号 (string, 1~64个字符),
                storage_name: 所属storage device name (string, 1~255个字符),
                storage_ip: storage设备IP (string, 1~64个字符),
                local_copy_count: 本地副本count (int32),
                remote_copy_count: 远端副本count (int32),
                cloud_copy_count: 云备份副本count (int32),
                snapshot_consistency_group_count: 快照一致性组count (int32),
                clone_consistency_group_count: 克隆一致性组count (int32),
                cdp_consistency_group_count: HyperCDP一致性组count (int32),
                dring_consistency_group_count: 环形3DC一致性组count (int32),
                metro_consistency_group_count: 双活一致性组count (int32),
                rep_consistency_group_count: 远程复制一致性组count (int32),
                project_id: 所属业务群组ID (string),
                lun_group_raw_id: LUN组在设备上的ID (int32, -1~16383),
                lun_group_name: LUN组name (string, 1~255个字符),
                vstore_id: 所属tenant ID (string),
                vstore_raw_id: 所属租户在设备上的ID (string),
                vstore_name: 所属租户name (string),
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
    create保护组, 支持基于LUN或者LUN组create

    Args:
        client: DME API client
        name: 保护组name
        storage_id: Storage device ID
        lun_ids: LUN 的 ID list, 条件必选, 当基于 LUN create保护组时为必传字段
        lun_group_id: LUN group ID, 条件必选, 当基于 LUN group形式create保护组时为必传字段
        description: 保护组description

    Returns:
        {
            id: 保护组ID (string),
            task_id: task ID (string, 1~64个字符),
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
    modify保护组

    Args:
        client: DME API client
        pg_id: 保护组 ID
        name: 保护组的name
        description: 保护组的description

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    批量delete保护组

    >![](public_sys-resources/icon-notice.gif) **须知: **
    >该 API 可能会直接或间接影响现网业务运行, 导致业务中断、关键数据丢失等, 请谨慎操作. 

    Args:
        client: DME API client
        pg_ids: 保护组的 ID list

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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

    向指定保护组中添加成员 LUN. 

    Args:
        client: DME API client
        pg_id: 保护组 ID
        lun_ids: 待添加到保护组的 LUN 的 ID list(Optional), max array members 100, 与 hyper_metro 和 rem_reps 的参数 lun_pairs 互斥; 保护组不存在双活、复制、环形 3DC 特性时此参数有效
        hyper_metro: 添加 LUN 到有双活特性保护组的请求参数(Optional), 与 lun_ids 参数互斥; 保护组存在双活特性时此参数有效. parameter format: {
                        is_delay: 是否延迟执行 (必填), true: 是; false: 否; 当延迟执行为 true 时: 若一致性组或新 Pair 处于"正在同步"status, 将等待同步完成后再将新 Pair 加入一致性组; 当延迟执行为 false 时: 若一致性组或新 Pair 处于"正在同步"status, 将直接暂停一致性组和新 Pair, 将新 Pair 加入一致性组, 再同步一致性组
                        create_mode: 双活 Pair 的create模式 (必填), valid values: auto (自动)、manual (手动)
                        remote_storage_pool_id: 远端Storage pool ID(Optional), 1~32 个字符, 正则 ^[a-fA-F0-9]+$; 双活 Pair create模式为 auto 时有效
                        remote_lun_name_rule: LUN 的name策略(Optional), valid values: same_as_local (与本端资源name保持一致)、prefix_and_suffix (前缀+本端资源name+后缀)、prefix_and_num (前缀+自动序号); 自动create模式下有效
                        name_prefix: 远端 LUN name前缀(Optional), 0~251 个字符; 自动create模式且name规则为 prefix_and_suffix 或 prefix_and_num 时有效; prefix_and_suffix 前缀最长 32 字节, prefix_and_num 前缀最长 251 字节
                        name_suffix: 远端 LUN name后缀(Optional), 0~16 个字符; 自动create模式且name规则为 prefix_and_suffix 时有效
                        lun_pairs: 手动配置的双活 Pair infolist(Optional), max array members 100; 当 create_mode 为 manual 时有效. parameter format: [{
                                local_lun_id: 本端 LUN 的 ID (必填), 1~32 个字符, 正则 ^[a-fA-F0-9]+$; 下发操作的设备端定义为本端, 其对端设备定义为远端
                                remote_lun_id: 远端 LUN 的 ID (必填), 1~32 个字符, 正则 ^[a-fA-F0-9]+$
                        },...]
        }
        rem_reps: 添加 LUN 到有复制特性保护组的请求参数(Optional), max array members 2, 与 lun_ids 参数互斥; 保护组存在复制特性时此参数有效. parameter format: [{
                        is_delay: 是否延迟执行(Optional), default true; true: 是; false: 否; 当延迟执行为 true 时: 若新 Pair 处于"正在同步"status, 将等待同步完成后再将新 Pair 加入一致性组; 当延迟执行为 false 时: 将直接分裂一致性组和新 Pair, 将新 Pair 加入一致性组, 再同步一致性组
                        create_mode: 远程复制 Pair 的create模式 (必填), valid values: auto (自动)、manual (手动)
                        remote_storage_id: 远端Storage device ID (必填), 1~64 个字符, 正则 ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$
                        remote_storage_pool_id: 远端Storage pool ID(Optional), 1~32 个字符, 正则 ^[a-fA-F0-9]+$; 复制 Pair create模式为 auto 时有效
                        remote_lun_name_rule: LUN 的name策略(Optional), valid values: same_as_local (与本端资源name保持一致)、prefix_and_suffix (前缀+本端资源name+后缀)、prefix_and_num (前缀+自动序号); 自动create模式下有效
                        name_prefix: 远端 LUN name前缀(Optional), 0~251 个字符; 自动create模式且name规则为 prefix_and_suffix 或 prefix_and_num 时有效; prefix_and_suffix 前缀最长 32 字节, prefix_and_num 前缀最长 251 字节
                        name_suffix: 远端 LUN name后缀(Optional), 0~16 个字符; 自动create模式且name规则为 prefix_and_suffix 时有效
                        lun_pairs: 手动配置的远程复制 Pair infolist(Optional), max array members 100; 当 create_mode 为 manual 时有效. parameter format: [{
                                local_lun_id: 本端 LUN 的 ID (必填), 1~32 个字符, 正则 ^[a-fA-F0-9]+$; 下发操作的设备端定义为本端, 其对端设备定义为远端
                                remote_lun_id: 远端 LUN 的 ID (必填), 1~32 个字符, 正则 ^[a-fA-F0-9]+$
                        },...]
        },...]

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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

    移除指定保护组中的成员 LUN. 

    Args:
        client: DME API client
        pg_id: 保护组 ID
        lun_ids: 待移除的保护组成员 LUN 的 ID list
        is_delay: 是否延迟执行. 在远程复制, 同步 + 异步的环形 3DC 情况下, 此参数无效

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
# hypermetro_group 子主题 - 双活一致性组相关操作
# ============================================================================

def hypermetro_group_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 20,
                          name: str = None, raw_id: str = None,
                          protect_group_id: str = None, storage_id: str = None,
                          storage_name: str = None, local_vstore_id: str = None,
                          local_vstore_raw_id: str = None, remote_vstore_id: str = None,
                          remote_vstore_raw_id: str = None) -> dict:
    """
    批量query双活一致性组

    Args:
        client: DME API client
        page_no: 分页query的页码, default 1
        page_size: 每页显示的count, default 20
        name: 双活一致性组name, supports fuzzy match
        raw_id: 双活一致性组在设备上的 ID
        protect_group_id: 保护组 ID
        storage_id: Storage device ID, 支持本端存储 ID 过滤
        storage_name: storage device name, 支持本端存储name模糊匹配
        local_vstore_id: 所属本端租户的 ID, 该参数和 local_vstore_raw_id 互斥
        local_vstore_raw_id: 所属本端租户在设备上的 ID, 该参数和 local_vstore_id 互斥
        remote_vstore_id: 所属远端租户的 ID, 该参数和 remote_vstore_raw_id 互斥
        remote_vstore_raw_id: 所属远端租户在设备上的 ID, 该参数和 remote_vstore_id 互斥

    Returns:
        {
            total: 双活一致性组count (int32),
            groups: 双活一致性组list (List<HyperMetroGroupResponse>). parameter format: [{
                id: 双活一致性组唯一标识 (string, 1~64个字符),
                raw_id: 在设备上的ID (string, 1~64个字符),
                name: name (string, 1~255个字符),
                local_storage_id: 本端storage device ID (string, 1~64个字符),
                local_storage_name: 本端storage device name (string, 1~256个字符),
                local_vstore_id: 所属本端tenant ID (string),
                local_vstore_raw_id: 所属本端租户在设备上的ID (string),
                local_vstore_name: 所属本端租户name (string),
                remote_storage_id: 远端storage device ID (string, 0~64个字符),
                remote_storage_name: 远端storage device name (string, 0~256个字符),
                remote_vstore_id: 所属远端tenant ID (string),
                remote_vstore_raw_id: 所属远端租户在设备上的ID (string),
                remote_vstore_name: 所属远端租户name (string),
                domain_name: 双活domain name称 (string, 0~64个字符),
                domain_raw_id: 双活域在设备上的ID (string, 0~64个字符),
                health_status: health status. valid values: unknown (未知), normal (正常), fault (故障),
                running_status: running status. valid values: normal (正常), synchronizing (同步中), invalid (失效), paused (暂停), forcibly_started (强制启动), to_be_synchronized (待同步), error (故障), unknown (未知),
                recovery_policy: 恢复策略. valid values: automatic (自动恢复), manual (手动恢复),
                priority_station_type: 优先站点type. valid values: preferred (优先站点), non_preferred (非优先站点),
                speed: 同步速率. valid values: low, medium, high, highest, custom,
                bandwidth: 自定义同步速率 (int32, 1~1024 MB/s),
                sync_direction: 数据同步方向. valid values: no_data_synchronization, local_to_remote, remote_to_local,
                activation_state: 激活status. valid values: active (激活), passive (未激活),
                local_protect_group_name: 本端保护组name (string, 0~255个字符),
                remote_protect_group_name: 远端保护组name (string, 0~255个字符),
                isolation_enabled: 隔离开关. valid values: true (打开), false (false),
                isolation_threshold_time: 隔离阈值 (int32, 10~30000ms),
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
    create双活一致性组

    Args:
        client: DME API client
        domain_id: 双活域 ID
        name: 双活一致性组name
        local_storage_id: 本端设备 ID
        local_pg_id: 本端保护组的 ID, 条件必选: 当设备type为 OceanStor Dorado V6、OceanStor V6 时必选
        description: descriptioninfo
        create_mode: 双活 Pair 的create模式, valid values: auto (自动模式), manual (手动模式)
        remote_vstore_id: 远端设备的租户 ID, 条件必选: 当 create_mode 为 auto 且设备为 OceanStor Dorado 6.1.3 及以上version时
        remote_storage_pool_id: 远端Storage pool ID, 条件必选: 当 create_mode 为 auto 时
        lun_ids: LUN 的 ID list, 条件可选: 当 create_mode 为 auto 时
        remote_resource_name_rule: 远端资源的name策略, valid values: same_as_local, prefix_and_suffix, prefix_and_num

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    modify双活一致性组

    Args:
        client: DME API client
        group_id: 双活一致性组 ID
        name: 双活一致性组name
        description: descriptioninfo
        recovery_policy: 双活 Pair 恢复策略, valid values: automatic (自动), manual (手动)
        service_assurance_policy: 业务保障策略, valid values: data_reliability_preferred (数据可靠优先), service_continuity_preferred (业务连续优先)
        speed: 同步速率, valid values: low, medium, high, highest, custom
        bandwidth: 自定义同步速率 (MB/s), 当 speed 为 custom 时必选
        isolation_threshold_time: 隔离阈值 (毫秒), 当 service_assurance_policy 为 service_continuity_preferred 时必选

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    批量delete双活一致性组

    Args:
        client: DME API client
        ids: 双活一致性组 ID list
        delete_mode: delete模型, valid values: preferred_only (优先站点delete), non_preferred_only (非优先站点delete), dual_ends (两端站点delete)
        is_self_adapt: 是否支持自适应delete成员 Pair, default false

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
        pair_ids: 双活 Pair ID list
        is_self_adapt: 是否自适应modify双活 Pair running status

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    双活一致性组移除成员 Pair (异步任务接口)

    Args:
        client: DME API client
        group_id: 双活一致性组 ID
        pair_ids: 双活 Pair ID list

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
        ids: 双活一致性组 ID list
        priority_station_type: 站点type, valid values: preferred (优先站点), non_preferred (非优先站点)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
        ids: 双活一致性组 ID list
        priority_station_type: 站点type, valid values: preferred (优先站点), non_preferred (非优先站点)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
        ids: 双活一致性组 ID list

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    同步双活一致性组

    Args:
        client: DME API client
        ids: 双活一致性组 ID list (必选, List<string>, 数组最小成员个数: 1, max array members: 100)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/metro/groups/sync"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


# ============================================================================
# hypermetro_pair 子主题 - 双活 Pair 相关操作
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
    批量query LUN 双活 Pair

    Args:
        client: DME API client
        page_no: 分页query的页码, default 1
        page_size: 每页显示的count, default 20
        group_id: 所属双活一致性组 ID
        group_name: 所属双活一致性组name, supports fuzzy match
        group_raw_id: 所属双活一致性组在Storage device上的 ID
        pair_raw_id: 双活 Pair 在Storage device上的 ID
        local_storage_id: 本端Storage device ID
        local_storage_name: 本端storage device name, supports fuzzy match
        local_vstore_id: 所属本端租户的 ID, 该参数和 local_vstore_raw_id 互斥
        local_vstore_raw_id: 所属本端租户在设备上的 ID, 该参数和 local_vstore_id 互斥
        local_volume_name: 本端 LUN name, supports fuzzy match
        local_host_access_state: 本地资源主机访问status, valid values: access_forbidden, read_only, read_write
        remote_vstore_id: 所属远端租户的 ID, 该参数和 remote_vstore_raw_id 互斥
        remote_vstore_raw_id: 所属远端租户在设备上的 ID, 该参数和 remote_vstore_id 互斥
        remote_volume_name: 远端 LUN name, supports fuzzy match

    Returns:
        {
            total: LUN双活Paircount (int32),
            hypermetro_pairs: LUN双活Pairlist (List<HyperMetroPairResponse>). parameter format: [{
                id: LUN双活Pair唯一标识 (string, 1~64个字符),
                pair_raw_id: 在Storage device上的ID (string, 1~64个字符),
                local_volume_raw_id: 本端LUN在设备上的ID (string, 1~64个字符),
                local_volume_name: 本端LUN name (string, 1~255个字符),
                remote_volume_raw_id: 远端LUN在设备上的ID (string, 1~64个字符),
                remote_volume_name: 远端LUN name (string, 1~255个字符),
                domain_raw_id: 双活域在设备上的ID (string, 0~64个字符),
                domain_name: 双活domain name称 (string, 0~64个字符),
                volume_wwn: 本端LUN的WWN (string, 1~64个字符),
                health_status: health status. valid values: unknown (未知), normal (正常), fault (故障),
                running_status: running status. valid values: normal (正常), synchronizing (同步中), invalid (失效), pause (暂停), forced_start (强制启动), to_be_synchronized (待同步), unknown (未知), error (故障),
                link_status: 链路status. valid values: connected (已连接), disconnected (未连接), unknown (未知),
                recovery_policy: 恢复策略. valid values: automatic (自动), manual (手动),
                priority_station_type: 优先站点type. valid values: preferred, non_preferred,
                local_storage_id: 本端storage device ID (string, 1~64个字符),
                local_storage_name: 本端storage device name (string, 1~255个字符),
                local_vstore_id: 所属本端tenant ID (string),
                local_vstore_raw_id: 所属本端租户在设备上的ID (string),
                local_vstore_name: 所属本端租户name (string),
                remote_storage_id: 远端storage device ID (string, 0~64个字符),
                remote_storage_name: 远端端storage device name (string, 0~255个字符),
                remote_vstore_id: 所属远端tenant ID (string),
                remote_vstore_raw_id: 所属远端租户在设备上的ID (string),
                remote_vstore_name: 所属远端租户name (string),
                is_in_group: 是否属于一致性组. valid values: true, false,
                group_id: 所属双活一致性组ID (string, 0~64个字符),
                group_raw_id: 所属一致性组在设备上的ID (string, 0~64个字符),
                group_name: 所属一致性组name (string, 0~255个字符),
                speed: 同步速率. valid values: low, medium, high, highest,
                sync_start_time: 最后一次同步启动时间 (string),
                sync_end_time: 最后一次同步end time (string),
                local_data_state: 本端资源数据status. valid values: consistent (完整), inconsistent (不完整),
                remote_data_state: 远端资源数据status. valid values: consistent (完整), inconsistent (不完整),
                local_host_access_state: 本端资源主机访问status. valid values: access_forbidden, read_only, read_write,
                remote_host_access_state: 远端资源主机访问status. valid values: access_forbidden, read_only, read_write,
                sync_left_time: 同步完成剩余时间 (string),
                sync_direction: 数据同步方向. valid values: no_data_synchronization, local_to_remote, remote_to_local,
                progress: 同步progress (int32),
                activation_state: 激活status. valid values: active (激活), passive (未激活),
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


def hypermetro_pair_create(client: DMEAPIClient, create_mode: str, local_storage_id: str,
                           domain_id: str, lun_ids: list = None, lun_pairs: list = None,
                           remote_storage_pool_id: str = None, remote_vstore_id: str = None,
                           remote_resource_name_rule: str = None, name_prefix: str = None,
                           name_suffix: str = None, speed: str = None, bandwidth: int = None,
                           service_assurance_policy: str = None, isolation_threshold_time: int = None,
                           recovery_policy: str = None) -> dict:
    """
    create双活 Pair

    Args:
        client: DME API client
        create_mode: 双活 Pair 的create模式, valid values: auto (自动create), manual (手动create)
        local_storage_id: create双活 Pair 的Storage device ID
        domain_id: 双活域 ID
        lun_ids: 自动create模式下, 源 LUN 的 ID list
        lun_pairs: 手动create模式下, 双活 Pair 的源 LUN、目标 LUN 的 ID list (List<PairInstance>, max array members: 100). parameter format: [{
                local_lun_id: 本端 LUN 的 ID (必填, 1~32个字符),
                remote_lun_id: 远端 LUN 的 ID (必填, 1~32个字符),
             }, ...]
        remote_storage_pool_id: 远端Storage pool ID, 自动create模式下有效
        remote_vstore_id: 远端设备的租户 ID, 自动create模式下有效
        remote_resource_name_rule: LUN 的name策略, valid values: same_as_local, prefix_and_suffix, prefix_and_num
        name_prefix: 远端 LUN name前缀
        name_suffix: 远端 LUN name后缀
        speed: 同步速率, valid values: low, medium, high, highest, custom
        bandwidth: 自定义同步速率 (MB/s), 当 speed 为 custom 时必传
        service_assurance_policy: 业务保障策略, valid values: data_reliability_preferred, service_continuity_preferred
        isolation_threshold_time: 隔离阈值 (毫秒), 当 service_assurance_policy 为 service_continuity_preferred 时必传
        recovery_policy: 恢复策略, valid values: automatic, manual

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    modify双活 Pair

    Args:
        client: DME API client
        pair_id: 双活 Pair 实例 ID
        speed: 双活 Pair 同步速率, valid values: low, medium, high, highest, custom
        bandwidth: 自定义速率 (MB/s), 当 speed 为 custom 时必选
        recovery_policy: 恢复策略, valid values: automatic, manual
        service_assurance_policy: 业务保障策略, valid values: data_reliability_preferred, service_continuity_preferred
        isolation_threshold_time: 隔离阈值 (毫秒), 当 service_assurance_policy 为 service_continuity_preferred 时必选

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    批量delete双活 Pair

    >![](public_sys-resources/icon-notice.gif) **须知: **
    >该 API 可能会直接或间接影响现网业务运行, 导致业务中断、关键数据丢失等, 请谨慎操作. 

    Args:
        client: DME API client
        ids: 双活 Pair 实例 ID list
        delete_mode: delete模式, valid values: preferred_only, non_preferred_only, dual_ends
        is_lun_service_interrupt: 是否中断 LUN 业务, 当 delete_mode 为 preferred_only 或 non_preferred_only 时有效

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
        ids: 双活 Pair ID list

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
        ids: 双活 Pair ID list
        priority_station_type: 站点type, valid values: preferred, non_preferred

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
        ids: 双活 Pair ID list
        priority_station_type: 站点type, valid values: preferred, non_preferred

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
        ids: 双活 Pair ID list

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/metro/lun-pairs/switch-priority-site"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


# ============================================================================
# hypermetro_domain 子主题 - 双活域相关操作
# ============================================================================

def hypermetro_domain_list(client: DMEAPIClient, storage_id: str = None,
                            types: list = None) -> dict:
    """
    批量query双活域

    Args:
        client: DME API client
        storage_id: 设备 ID
        types: 双活域typelist

    Returns:
        {
            metro_domain_list: 双活域list (List<MetroDomain>). parameter format: [{
                id: 双活域ID (string),
                storage_id: 设备ID (string),
                storage_name: 设备name (string, 1~64个字符),
                ip_address: 设备的IP address (string),
                domain_id: 双活域在设备的ID (string, 1~32个字符),
                domain_name: 双活domain name称 (string, 1~64个字符),
                running_status: running status. valid values: normal, to_be_recovered, invalid, recovering, faulty, split, force_started,
                domain_type: 双活域模式. valid values: AA_mode, AP_mode,
                type: 双活域使用type. valid values: block, file_system, block_file_system,
                cp_type: 仲裁type. valid values: quorum_server, quorum_disk, none,
                cps_name: 仲裁服务器name (string, 1~64个字符),
                cps_running_status: 仲裁服务器running status. valid values: online, offline,
                standby_cps_name: 备用仲裁服务器name (string, 1~64个字符),
                server_ip_master: 仲裁服务器IP address (string),
                server_ip_slave: 备选仲裁服务器IP address (string),
                iscsi_link_num: ISCSI链路count (integer),
                fc_link_num: FC链路count (integer),
                ip_link_num: IP链路count (integer),
                remote_storage_id: 远端设备ID (string),
                remote_storage_name: 远端设备name (string, 1~64个字符),
                remote_storage_ip: 远端设备IP address (string),
                remote_dev_running_status: 远端设备running status. valid values: link_up, link_down, disabled, connecting, air_gap_link_down,
                config_role: 配置role. valid values: active_site, standby_site,
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
# replication_pair 子主题 - 复制 Pair 相关操作
# ============================================================================

def replication_pair_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 20,
                          group_id: str = None, group_name: str = None,
                          pair_raw_id: str = None, local_storage_id: str = None,
                          local_storage_name: str = None, local_vstore_id: str = None,
                          local_vstore_raw_id: str = None, local_volume_name: str = None,
                          remote_vstore_id: str = None, remote_vstore_raw_id: str = None,
                          remote_volume_name: str = None) -> dict:
    """
    批量query复制 Pair

    Args:
        client: DME API client
        page_no: 分页query的页码, default 1
        page_size: 每页显示的count, default 20
        group_id: 所属复制一致性组 ID
        group_name: 所属复制一致性组name, supports fuzzy match
        pair_raw_id: 复制 Pair 在Storage device上的 ID
        local_storage_id: 本端Storage device ID
        local_storage_name: 本端storage device name, supports fuzzy match
        local_vstore_id: 所属本端租户的 ID, 该参数和 local_vstore_raw_id 互斥
        local_vstore_raw_id: 所属本端租户在设备上的 ID, 该参数和 local_vstore_id 互斥
        local_volume_name: 本端 LUN name, supports fuzzy match
        remote_vstore_id: 所属远端租户的 ID, 该参数和 remote_vstore_raw_id 互斥
        remote_vstore_raw_id: 所属远端租户在设备上的 ID, 该参数和 remote_vstore_id 互斥
        remote_volume_name: 远端 LUN name, supports fuzzy match

    Returns:
        {
            total: 复制Paircount (int32),
            replication_pairs: 复制Pairlist (List<ReplicationPairResponse>). parameter format: [{
                id: 复制Pair唯一标识 (string, 1~64个字符),
                raw_id: 在Storage device上的ID (string, 1~64个字符),
                local_storage_id: 本端storage device ID (string, 1~64个字符),
                local_storage_name: 本端设备name (string, 1~255个字符),
                local_resource_raw_id: 本端资源在设备上的ID (string, 1~64个字符),
                local_resource_name: 本端资源name (string, 1~255个字符),
                remote_storage_id: 远端storage device ID (string, 1~64个字符),
                remote_storage_name: 远端storage device name (string, 1~255个字符),
                remote_resource_raw_id: 远端资源在设备上的ID (string, 1~64个字符),
                remote_resource_name: 远端资源name (string, 1~255个字符),
                local_resource_type: 本端resource type. valid values: lun (卷), file_system (Filesystem),
                local_vstore_raw_id: 本端资源所属租户在设备上的ID (string, 1~64个字符),
                remote_vstore_raw_id: 远端资源所属租户在设备上的ID (string, 1~64个字符),
                health_status: health status. valid values: unknown (未知), normal (正常), fault (故障),
                running_status: running status. valid values: normal, synchronizing, to_be_recoverd, interrupted, splited, invalid, standby, air_gap_link_down,
                replication_mode: 复制模式. valid values: synchronous (同步复制), asynchronous (异步复制),
                speed: 速率. valid values: low, medium, high, highest, custom,
                bandwidth: 自定义同步速率 (int32, MB/s),
                synchronize_type: 同步type. valid values: manual, wait_after_sync_begins, wait_after_sync_ends, specified_time_policy,
                interval: 数据同步周期 (integer, 0~86400秒),
                sync_left_time: 同步完成剩余时间 (string),
                recovery_policy: 恢复策略. valid values: automatic (自动恢复), manual (手动恢复),
                is_primary: 本端是否是主端. valid values: true, false,
                rep_io_timeout: 远端IO超时时间 (integer, 10~255秒),
                enable_compress: 链路压缩. valid values: true (压缩), false (不压缩),
                compress_valid: 压缩是否有效. valid values: true, false,
                sync_start_time: 最后一次同步启动时间 (string),
                sync_end_time: 最后一次同步end time (string),
                is_in_group: 是否属于一致性组. valid values: true, false,
                group_id: 所属远程复制一致性组ID (string, 1~64个字符),
                group_raw_id: 所属一致性组在设备上的ID (string, 1~64个字符),
                group_name: 所属一致性组name (string, 1~255个字符),
                data_consistent_status: 主从数据是否一致. valid values: true, false,
                primary_resource_data_status: 主端资源数据status. valid values: synchronized, complete, incomplete, unknown,
                secondary_resource_data_status: 从端资源数据status. valid values: synchronized, complete, incomplete, unknown,
                secondary_resource_protection: 从端资源读写设置. valid values: access_denied, read_only, read_write,
                dr_ring_id: 环形3DCobject在设备上的ID (string, 1~64个字符),
                progress: 同步progress (int32, -1~100),
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
    create远程复制 Pair

    Args:
        client: DME API client
        local_storage_id: 本端Storage device ID
        local_lun_id: 本端 LUN ID
        remote_storage_id: 远端Storage device ID
        remote_storage_pool_id: 远端Storage pool ID
        remote_vstore_id: 远端设备的租户 ID
        remote_resource_name_rule: 远端资源的name策略, valid values: same_as_local, prefix_and_suffix, prefix_and_num
        name_prefix: 远端资源name前缀
        name_suffix: 远端资源name后缀
        speed: 同步速率, valid values: low, medium, high, highest, custom
        bandwidth: 自定义同步速率 (MB/s), 当 speed 为 custom 时必选
        recovery_policy: 恢复策略, valid values: automatic, manual
        sync_type: 同步type, valid values: manual, wait_after_sync_begins, wait_after_sync_ends, specified_time_policy
        timing_value_in_sec: 定时时长 (秒), 当 sync_type 为 wait_after_sync_begins 或 wait_after_sync_ends 时必选
        sync_schedule: 定时规则, 当 sync_type 为 specified_time_policy 时必选
        rep_io_timeout: 远端 IO 超时时间 (秒), 当复制模式为同步模式时有效
        sync_snap_policy: 用户快照同步策略, valid values: not_sync_snap, same_as_source, user_snap_retention_num, snap_tag_based
        user_snap_retention_num: 从端用户快照保留count
        switch_to_async: 同步远程复制自动转换为异步远程复制的开关
        enable_compress: 链路压缩, 当复制模式为异步模式时必选

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    modify复制 Pair

    Args:
        client: DME API client
        pair_id: 复制 Pair 实例 ID
        speed: 同步速率, valid values: low, medium, high, highest, custom
        bandwidth: 自定义同步速率 (MB/s), 当 speed 为 custom 时必选
        recovery_policy: 恢复策略, valid values: automatic, manual
        enable_compress: 链路压缩, 当复制模式为异步模式时必选
        sync_type: 同步type, valid values: manual, wait_after_sync_begins, wait_after_sync_ends, specified_time_policy
        timing_value_in_sec: 定时时长 (秒), 当 sync_type 为 wait_after_sync_begins 或 wait_after_sync_ends 时必选
        sync_schedule: 定时规则, 当 sync_type 为 specified_time_policy 时必选
        rep_io_timeout: 远端 IO 超时时间 (秒), 当复制模式为同步模式时有效
        sync_snap_policy: 用户快照同步策略, valid values: not_sync_snap, same_as_source, user_snap_retention_num, snap_tag_based
        user_snap_retention_num: 从端用户快照保留count
        switch_to_async: 同步远程复制自动转换为异步远程复制的开关

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    批量delete远程复制 Pair

    Args:
        client: DME API client
        ids: 复制 Pair 实例 ID list
        delete_mode: delete模式, valid values: primary_only, secondary_only, dual_ends, default dual_ends

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
        ids: 复制 Pair ID list

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
        ids: 复制 Pair ID list

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
        ids: 复制 Pair ID list

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    远程复制 Pair 从资源保护status切换

    Args:
        client: DME API client
        id: 复制 Pair ID
        operation_type: 操作type, valid values: enable (true), disable (取消)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/replication/pairs/{id}/switch-write-protection"

    payload = {
        'operation_type': operation_type
    }

    response = client.post(url, body=payload, params={"id": id})
    return response


# ============================================================================
# device 子主题 - 设备 Pair 和复制链路相关操作
# ============================================================================

def device_pair_list(client: DMEAPIClient, storage_id: str = None) -> dict:
    """
    query设备 Pairs

    Args:
        client: DME API client
        storage_id: Storage device ID

    Returns:
        {
            total: 设备Pair的count (int32),
            device_pairs: 设备Pairlist (List<DevicePairInfo>). parameter format: [{
                id: 设备Pair的ID (string, 1~64个字符),
                local_storage_sn: 本端设备SN号 (string, 0~32个字符),
                remote_storage_sn: 远端设备SN号 (string, 0~32个字符),
                local_storage_ip: 本端设备的IP (string, 1~64个字符),
                local_storage_name: 本端设备name (string, 0~255个字符),
                local_storage_model: 本端设备的model (string, 0~32个字符),
                local_storage_version: 本端设备的version号 (string, 0~32个字符),
                remote_storage_identifier: 远端设备在本端设备上的标识ID (string, 0~32个字符),
                remote_storage_name: 远端设备的name (string, 0~255个字符),
                remote_storage_wwn: 远端设备WWN号 (string, 0~64个字符),
                remote_storage_vendor: 远端设备的厂商 (string, 0~32个字符),
                remote_storage_ip: 远端设备的IP (string, 1~64个字符),
                remote_storage_model: 远端设备的model (string, 0~32个字符),
                remote_storage_type: 远端设备的type. valid values: replication_device, heterogeneous_device, unknown_device, cloud_replication_device,
                remote_storage_version: 远端设备的version号 (string, 0~32个字符),
                running_status: running status. valid values: link_up (已连接), link_down (未连接), disabled (已禁用), connecting (正在连接), air_gap_link_down (Air Gap断开),
                health_status: health status. valid values: normal (正常), fault (故障), invalid (失效),
                compress_alg_valid: compressionstatus是否有效. valid values: true, false,
                compress_algorithm: compression策略. valid values: depth_compression, fast_compression, invalid, fault,
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
    query复制链路

    Args:
        client: DME API client
        local_storage_id: 本端Storage device ID (可选, string, 1~64 个字符), 作为源端Storage device进行query
        page_no: 分页query的页码 (可选, int32, default 1)
        page_size: 每页显示的count (可选, int32, 1~1000, default 20)
        health_status: health status (可选, string). valid values: normal (正常), fault (故障)
        running_status: running status (可选, string). valid values: link_up (已连接), link_down (未连接), disabled (已禁用), connecting (正在连接), air_gap_link_down (Air Gap断开)
        link_type: 复制链路type (可选, string). valid values: fc_link (FC链路), ip_link (IP链路)

    Returns:
        {
            total: 复制链路count (int32),
            replication_links: 复制链路list (List<ReplicationLinkInfo>). parameter format: [{
                id: 复制链路的ID (string, 1~64个字符),
                link_type: 链路type. valid values: fc_link (FC链路), ip_link (IP链路),
                local_storage_id: 本端storage device ID (string, 1~64个字符),
                health_status: health status. valid values: normal (正常), fault (故障),
                running_status: running status. valid values: link_up (已连接), link_down (未连接), disabled (已禁用), connecting (正在连接), air_gap_link_down (Air Gap断开),
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
# snapshot 子主题 - LUN 快照相关操作
# ============================================================================

def snapshot_list(client: DMEAPIClient, snapshot_ids: list = None, storage_id: str = None,
                  raw_id: str = None, name: str = None, health_status: str = None,
                  running_status: str = None, source_lun_name: str = None,
                  parent_name: str = None, activated_time_from: int = None,
                  activated_time_to: int = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    批量query LUN 快照

    Args:
        client: DME API client
        snapshot_ids: 快照 ID list
        storage_id: Storage device ID
        raw_id: 快照在Storage device上的 ID
        name: 快照name, supports fuzzy query
        health_status: health status, valid values: normal, fault, write_protected
        running_status: running status, valid values: activated, rolling_back, unactivated, initializing, deleting, unknown
        source_lun_name: 源 LUN name, supports fuzzy query
        parent_name: 父objectname, supports fuzzy query
        activated_time_from: query激活时间的起始点 (Unix 时间戳, 单位秒)
        activated_time_to: query激活时间的结束点 (Unix 时间戳, 单位秒)
        page_no: 分页query的开始页, 最小值为 1, default值为 1
        page_size: items per page, 1~1000, default 20

    Returns:
        {
            total: LUN快照count (int32),
            snapshots: LUN快照list (List<LunSnapshotInfo>). parameter format: [{
                id: 快照ID (string, 1~64个字符),
                raw_id: 快照在Storage device上的ID (string, 1~64个字符),
                name: 快照name (string, 1~255个字符),
                parent_type: 父objecttype. valid values: lun (LUN), snapshot (快照),
                parent_id: 父objectID (string, 1~64个字符),
                parent_raw_id: 父object在Storage device上的ID (string, 1~64个字符),
                parent_name: 父objectname (string, 1~255个字符),
                health_status: health status. valid values: normal (正常), fault (故障), write_protected (写保护),
                running_status: running status. valid values: activated (已激活), rolling_back (正在回滚), unactivated (未激活), initializing (初始化中), deleting (delete中), unknown (未知),
                description: 快照descriptioninfo (string, 0~255个字符),
                activated_time: 快照激活时间 (int64),
                rollback_start_time: 回滚start time (int64),
                rollback_end_time: 回滚end time (int64),
                rollback_speed: 回滚速率. valid values: low, medium, high, highest, unknown,
                rollback_rate: 回滚progress (int32, -1~100),
                is_mapped: 映射status. valid values: true (映射), false (未映射),
                wwn: WWN (string, 1~64个字符),
                user_capacity: 快照的用户capacity (int64, 字节),
                consumed_capacity: 快照实际消耗的capacity (int64, 字节),
                snapshot_cg_id: 快照一致性组ID (string, 1~64个字符),
                snapshot_cg_name: 快照一致性组name (string, 1~255个字符),
                source_lun_id: 源LUN ID (string, 1~64个字符),
                source_lun_name: 源LUN name (string, 1~255个字符),
                storage_id: storage device ID (string, 1~64个字符),
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
    批量create LUN 快照

    Args:
        client: DME API client
        snapshots_info: LUN 快照createinfolist (List<LunSnapshotCreateInfo>, max array members: 2048). parameter format: [{
                name: 快照name (1~255个字符),
                source_type: 源objecttype. valid values: lun (LUN), snapshot (快照),
                source_id: 源objectID (1~64个字符),
             }, ...]
        is_consist_activate: 是否一致性激活, default false

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
        rollback_speed: 回滚速率, valid values: low, medium, high, highest
        rollback_snapshots: 快照回滚的资源infolist, 每项包含 snapshot_id, target_type, target_id

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    批量delete LUN 快照

    Args:
        client: DME API client
        snapshot_ids: 快照 ID list
        is_delete_target_lun: 是否delete目标 LUN, default true
        is_auto_deactivate: 是否在delete前自动取消激活快照, default false

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
# snapshot_group 子主题 - 快照一致性组相关操作
# ============================================================================

def snapshot_group_create(client: DMEAPIClient, name: str, protect_group_id: str,
                          description: str = None, creation_mode: str = None) -> dict:
    """
    create快照一致性组

    Args:
        client: DME API client
        name: 快照一致性组name
        protect_group_id: 保护组的 ID
        description: descriptioninfo
        creation_mode: create模式, valid values: new_snapshot

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    批量delete快照一致性组

    Args:
        client: DME API client
        snapshot_cg_ids: 快照一致性组 ID list
        is_delete_target_lun: 是否delete目标 LUN, 仅 Dorado 6.1.2 及以上version支持, default true

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
        object_type: objecttype, valid values: parent_object
        snapshot_create_mode: 快照create方式, valid values: auto, manual
        name_rule: 快照name命名规则, valid values: prefix_and_suffix, prefix_and_num
        name_prefix: 快照name前缀
        name_suffix: 快照name后缀
        target_snapshot_objects: 目标快照objectlist

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
        snapshot_cg_ids: 快照一致性组 ID list

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
        rollback_speed: 回滚速率, valid values: low, medium, high, highest
        snapshot_create_mode: 快照create方式, valid values: auto, manual
        name_rule: 快照name命名规则, valid values: prefix_and_suffix, prefix_and_num
        name_prefix: 快照name前缀
        name_suffix: 快照name后缀
        target_snapshot_objects: 目标快照objectlist

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
# clone_group 子主题 - 克隆一致性组相关操作
# ============================================================================

def clone_group_create(client: DMEAPIClient, name: str, protect_group_id: str,
                       create_mode: str, description: str = None, name_rule: str = None,
                       name_prefix: str = None, name_suffix: str = None,
                       copy_rate: str = None, is_sync: bool = None,
                       clone_pairs: list = None) -> dict:
    """
    create克隆一致性组

    Args:
        client: DME API client
        name: 克隆一致性组name
        protect_group_id: 保护组 ID
        create_mode: create模式, valid values: auto, manual
        description: descriptioninfo
        name_rule: 目标 LUN name命名规则, valid values: prefix_and_suffix, prefix_and_num
        name_prefix: 目标 LUN name前缀
        name_suffix: 目标 LUN name后缀
        copy_rate: 拷贝速率, valid values: low, medium, high, highest, default medium
        is_sync: 是否立即同步, default true
        clone_pairs: 克隆 Pair list (List<TargetClonePairObject>, max array members: 4096), create_mode 为 manual 时必选. parameter format: [{
                source_lun_id: 源LUN ID (1~32个字符),
                target_lun_id: 目标LUN ID (1~32个字符),
             }, ...]

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    同步克隆一致性组

    Args:
        client: DME API client
        clone_cg_id: 克隆一致性组 ID
        create_mode: 克隆 Pair create模式, valid values: auto, manual
        name_rule: 目标 LUN name命名规则, valid values: prefix_and_suffix, prefix_and_num
        name_prefix: 目标 LUN name前缀
        name_suffix: 目标 LUN name后缀
        clone_pairs: 克隆 Pair list (List<TargetClonePairObject>, max array members: 4096), create_mode 为 manual 时必选. parameter format: [{
                source_lun_id: 源LUN ID (1~32个字符),
                target_lun_id: 目标LUN ID (1~32个字符),
             }, ...]

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    批量delete克隆一致性组

    Args:
        client: DME API client
        ids: 克隆一致性组 ID list
        is_delete_dst_lun: 是否delete目标 LUN
        is_recycle_dst_lun_data: 是否回收目标 LUN 数据

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
# replication_group 子主题 - 复制一致性组相关操作
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
    create远程复制一致性组

    Args:
        client: DME API client
        cg_name: 远程复制一致性组name
        remote_storage_id: 远端Storage device ID
        local_pg_id: 本端保护组的 ID, 当Storage deviceversion是 OceanStor V6、OceanStor Dorado V6 时必传
        description: descriptioninfo
        remote_lun_group_id: 远端 LUN group的 ID, 当Storage deviceversion是 OceanStor V6、OceanStor Dorado V6 时且本端保护组是基于 LUN groupcreate的时必传
        local_storage_id: 本端Storage device ID, 当Storage deviceversion不是 OceanStor V6、OceanStor Dorado V6 时必传
        create_mode: 复制 Pair 的create模式, valid values: auto (自动), manual (手动)
        existed_pair_ids: 已存在的复制 Pair 的 ID list
        lun_pairs: 手动create模式下, 复制 Pair 的源 LUN、目标 LUN 的 ID list (List<PairInstance>, max array members: 100). parameter format: [{
                local_lun_id: 本端 LUN 的 ID (必填, 1~32个字符),
                remote_lun_id: 远端 LUN 的 ID (必填, 1~32个字符),
             }, ...]
        lun_ids: 自动create模式下, 源 LUN 的 ID list
        remote_storage_pool_id: 远端Storage pool ID, 自动create模式下有效
        remote_vstore_id: 远端设备的租户 ID, 自动create模式下有效
        remote_resource_name_rule: 远端资源的name策略, valid values: same_as_local, prefix_and_suffix, prefix_and_num
        name_prefix: 远端资源name前缀
        name_suffix: 远端资源name后缀

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    modify远程复制一致性组

    Args:
        client: DME API client
        replication_group_id: 远程复制一致性组 ID
        name: 远程复制一致性组name
        description: descriptioninfo
        speed: 同步速率, valid values: low, medium, high, highest, custom
        bandwidth: 自定义同步速率 (MB/s), 当 speed 为 custom 时必选
        recovery_policy: 恢复策略, valid values: automatic, manual
        enable_compress: 链路压缩, 当复制模式为异步模式时必选
        sync_type: 同步type, valid values: manual, wait_after_sync_begins, wait_after_sync_ends, specified_time_policy
        timing_value_in_sec: 定时时长 (秒), 当 sync_type 为 wait_after_sync_begins 或 wait_after_sync_ends 时必选
        sync_schedule: 定时规则, 当 sync_type 为 specified_time_policy 时必选
        rep_io_timeout: 远端 IO 超时时间 (秒), 当复制模式为同步模式时有效
        sync_snap_policy: 用户快照同步策略, valid values: not_sync_snap, same_as_source, user_snap_retention_num, snap_tag_based
        user_snap_retention_num: 从端用户快照保留count
        switch_to_async: 同步远程复制自动转换为异步远程复制的开关

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    批量delete远程复制一致性组

    Args:
        client: DME API client
        ids: 远程复制一致性组 ID list
        is_self_adapt: 是否支持自适应移除成员 Pair, default false
        delete_mode: delete模式, valid values: primary_only, secondary_only, dual_ends, default dual_ends

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    远程复制一致性组添加成员 Pair (OceanStor Dorado V6 6.1.3以下不支持, 需组health status正常且running status为正常或分裂)

    Args:
        client: DME API client
        group_id: 远程复制一致性组的 ID
        pair_ids: 远程复制 Pair 的 ID list

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
        pair_ids: 远程复制 Pair 的 ID list

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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

    >![](public_sys-resources/icon-notice.gif) **须知: **
    >该 API 可能会直接或间接影响现网业务运行, 导致业务中断、关键数据丢失等, 请谨慎操作. 

    Args:
        client: DME API client
        ids: 一致性组的 ID list

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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

    >![](public_sys-resources/icon-notice.gif) **须知: **
    >该 API 可能会直接或间接影响现网业务运行, 导致业务中断、关键数据丢失等, 请谨慎操作. 

    Args:
        client: DME API client
        ids: 一致性组的 ID list

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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

    >![](public_sys-resources/icon-notice.gif) **须知: **
    >该 API 可能会直接或间接影响现网业务运行, 导致业务中断、关键数据丢失等, 请谨慎操作. 

    Args:
        client: DME API client
        ids: 一致性组的 ID list

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    远程复制一致性组从资源写保护status切换

    Args:
        client: DME API client
        id: 一致性组的 ID
        operation_type: 操作type, valid values: enable (true), disable (取消)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    批量query复制一致性组

    Args:
        client: DME API client
        page_no: 分页query的起始location (可选, int32, default 1)
        page_size: 每页显示的count (可选, int32, 1~1000, default 20)
        protect_group_id: 保护组 ID (可选, string, 1~64 个字符)
        name: 复制一致性组name (可选, string, 1~255 个字符), supports fuzzy match
        raw_id: 复制一致性组在设备上的 ID (可选, string, 1~64 个字符)
        running_status: running status (可选, string). valid values: normal (正常), synchronizing (同步中), splited (已分裂), to_be_recoverd (待恢复), interrupted (异常断开), invalid (失效), standby (备用), air_gap_link_down (Air Gap断开)
        health_status: health status (可选, string). valid values: normal (正常), fault (故障), invalid (失效)
        storage_name: storage device name (可选, string, 1~255 个字符), supports fuzzy match
        storage_id: Storage device ID (可选, string, 1~64 个字符)
        replication_mode: 复制模式 (可选, string). valid values: synchronous (同步复制), asynchronous (异步复制)

    Returns:
        {
            total: 复制一致性组count (int32),
            groups: 复制一致性组list (List<ReplicationGroupDetail>). parameter format: [{
                id: 复制一致性组 ID (string, 1~64个字符),
                raw_id: 复制一致性组在设备上的 ID (string, 1~64个字符),
                name: 复制一致性组name (string, 1~255个字符),
                replication_model: 复制模式 (string). valid values: synchronous, asynchronous,
                storage_name: storage device name (string, 0~255个字符),
                storage_id: Storage device id (string, 1~64个字符),
                health_status: health status (string). valid values: normal, fault, invalid,
                running_status: running status (string). valid values: normal, synchronizing, splited, to_be_recoverd, interrupted, invalid, standby, air_gap_link_down,
                protect_group_id: 保护组 ID (string, 0~64个字符),
                protect_group_name: 保护组name (string, 0~255个字符),
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
# Filesystem双活Pair (fs_hypermetro_pair) 子主题函数
# ============================================================================


def filesystem_pair_create(client: DMEAPIClient, vstore_pair_id: str,
                            create_mode: str = "manual", fs_pairs: list = None,
                            speed: str = None, bandwidth: int = None,
                            service_assurance_policy: str = None,
                            isolation_threshold_time: int = None) -> dict:
    """
    createFilesystem双活Pair. 该API可能会直接或间接影响现网业务运行, 请谨慎操作. 

    Args:
        client: DME API client
        vstore_pair_id: 双活租户Pair的ID (必选, string, 1~32个字符)
        create_mode: create模式 (可选, string). valid values: manual (手动). default值: manual
        fs_pairs: FilesystemPairlist (可选, List[FsPairInstance], max array members: 100)
        speed: 同步速率 (可选, string). valid values: low, medium, high, highest, custom
        bandwidth: 带宽 (可选, integer, 1~1024). 当speed为custom时必选
        service_assurance_policy: 业务保障策略 (可选, string). valid values: data_reliability_preferred, service_continuity_preferred
        isolation_threshold_time: 隔离阈值 (可选, int32, 10~30000)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/hypermetro/filesystem-pairs"

    if not vstore_pair_id:
        raise ValueError("vstore_pair_id 是必选参数")

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
    queryFilesystem双活Pairlist. 

    Args:
        client: DME API client
        ids: 双活Pair实例IDlist (可选, List[string])
        name: 双活Pairname (可选, string)
        status: running status (可选, string)
        storage_id: storage device ID (可选, string)
        vstore_pair_id: 双活租户Pair的ID (可选, string)
        local_fs_name: 本端Filesystemname (可选, string)
        local_fs_id: 本端FilesystemID (可选, string)
        health_status: health status (可选, string)
        running_status: running status (可选, string)
        sort_key: 排序字段 (可选, string)
        sort_dir: 排序方向 (可选, string)
        page_no: 分页页码 (可选, int32)
        page_size: items per page (可选, int32)

    Returns:
        {
            total: Filesystem双活Pair的total (int32),
            file_system_pairs: Filesystem双活Pairlist (List<FileSystemHyperMetroPair>). parameter format: [{
                id: Filesystem双活Pair的ID (string),
                pair_raw_id: 在Storage device上的ID (string),
                local_filesystem_raw_id: 本端Filesystem在设备上的ID (string),
                local_filesystem_name: 本端Filesystemname (string),
                remote_filesystem_raw_id: 远端Filesystem在设备上的ID (string),
                remote_filesystem_name: 远端Filesystemname (string),
                domain_raw_id: 双活域在Storage device上的ID (string),
                domain_name: 双活domain name称 (string),
                health_status: health status. valid values: unknown (未知), normal (正常), fault (故障),
                running_status: running status. valid values: normal, synchronizing, invalid, pause, forced_start, to_be_synchronized, unknown, error, creating, deleting,
                recovery_policy: 恢复策略. valid values: automatic (自动), manual (手动), unknown (未知),
                link_status: 链路status. valid values: connected (已连接), disconnected (未连接), unknown (未知),
                is_primary: 是否为优先站点. valid values: true, false,
                local_storage_id: 本端storage device ID (string),
                remote_storage_id: 远端storage device ID (string),
                speed: 同步速率. valid values: low, medium, high, highest, custom,
                bandwidth: 自定义同步速率 (int32, MB/s),
                start_time: 最后一次同步启动时间 (string),
                end_time: 最后一次同步end time (string),
                local_data_state: 本端数据status. valid values: consistent (完整), inconsistent (不完整),
                remote_data_state: 远端数据status. valid values: consistent (完整), inconsistent (不完整),
                local_host_access_state: 本端主机访问status. valid values: access_forbidden, read_only, read_write, invalid, blocked, unknown,
                remote_host_access_state: 远端主机访问status. valid values: access_forbidden, read_only, read_write, invalid, blocked, unknown,
                sync_lefttime: 同步完成剩余时间 (string),
                sync_direction: 同步方向. valid values: no_data_synchronization, local_to_remote, remote_to_local,
                sync_progress: 同步progress (string),
                activation_state: 激活status. valid values: active (激活), passive (未激活),
                vstore_pair_id: 所属租户Pair的ID (string),
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
    批量暂停Filesystem双活Pair. 该API可能会直接或间接影响现网业务运行, 请谨慎操作. 

    Args:
        client: DME API client
        fs_pair_ids: Filesystem双活Pair的IDlist (必选, List[string], max array members: 100, 数组最小成员个数: 1)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/hypermetro/filesystem-pairs/pause"

    if not fs_pair_ids or len(fs_pair_ids) == 0:
        raise ValueError("fs_pair_ids 是必选参数")

    payload = {
        'fs_pair_ids': fs_pair_ids
    }

    response = client.post(url, body=payload)
    return response


def filesystem_pair_sync(client: DMEAPIClient, fs_pair_ids: list) -> dict:
    """
    批量同步Filesystem双活Pair. 该API可能会直接或间接影响现网业务运行, 请谨慎操作. 

    Args:
        client: DME API client
        fs_pair_ids: Filesystem双活Pair的IDlist (必选, List[string])

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/hypermetro/filesystem-pairs/sync"

    if not fs_pair_ids or len(fs_pair_ids) == 0:
        raise ValueError("fs_pair_ids 是必选参数")

    payload = {
        'fs_pair_ids': fs_pair_ids
    }

    response = client.post(url, body=payload)
    return response


def filesystem_pair_delete(client: DMEAPIClient, ids: list,
                            is_local_delete: bool = None,
                            is_online_delete: bool = None) -> dict:
    """
    批量deleteFilesystem双活Pair. 该API可能会直接或间接影响现网业务运行, 请谨慎操作. 

    Args:
        client: DME API client
        ids: 双活Pair实例IDlist (必选, List[string])
        is_local_delete: 是否delete本端配置info (可选, boolean, true,false)
        is_online_delete: 是否在线delete (可选, boolean, true,false)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/hypermetro/filesystem-pairs/delete"

    if not ids or len(ids) == 0:
        raise ValueError("ids 是必选参数")

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
# Filesystem快照 (fs_snapshot) 子主题函数
# ============================================================================


def fs_snapshot_create(client: DMEAPIClient, vstore_pair_id: str,
                        fs_pairs: list) -> dict:
    """
    createFilesystem快照. 

    Args:
        client: DME API client
        vstore_pair_id: 文件名系统所属双活租户Pair的ID (必选, string)
        fs_pairs: 快照参数list (必选, List)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/filesystem-snapshots"

    if not vstore_pair_id:
        raise ValueError("vstore_pair_id 是必选参数")

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
    批量queryFilesystem快照. 

    Args:
        client: DME API client
        fs_pair_id: 双活Pair ID (可选, string)
        name: 快照name (可选, string, 支持模糊搜索)
        status: 快照status (可选, string)
        local_fs_name: 本端Filesystemname (可选, string)
        local_fs_id: 本端FilesystemID (可选, string)
        page_no: 分页页码 (可选, int32)
        page_size: items per page (可选, int32)

    Returns:
        {
            total: Filesystem快照total (int32),
            snapshots: Filesystem快照list (List<FsSnapshotInfo>). parameter format: [{
                id: 快照ID (string),
                name: 快照name (string),
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
    批量deleteFilesystem快照. 

    Args:
        client: DME API client
        ids: 快照IDlist (必选, List[string])

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/filesystem-snapshots/delete"

    if not ids or len(ids) == 0:
        raise ValueError("ids 是必选参数")

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


# ============================================================================
# 双活租户Pair (vstore_hypermetro_pair) 子主题函数
# ============================================================================


def vstore_pair_force_start(client: DMEAPIClient, ids: list) -> dict:
    """
    批量强制启动双活租户Pair. 

    Args:
        client: DME API client
        ids: 双活租户Pair的IDlist (必选, List[string])

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/metro/vstore-pairs/force-start"

    if not ids or len(ids) == 0:
        raise ValueError("ids 是必选参数")

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
    create双活租户Pair. 

    Args:
        client: DME API client
        local_storage_id: 本端storage device ID (必选, string)
        remote_storage_id: 远端storage device ID (必选, string)
        name: 租户Pairname (可选, string)
        description: description (可选, string)
        remote_vstore_id: 远端tenant ID (可选, string)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/metro/vstore-pairs"

    if not local_storage_id or not remote_storage_id:
        raise ValueError("local_storage_id 和 remote_storage_id 是必选参数")

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
    query双活租户Pairlist. 

    Args:
        client: DME API client
        ids: 双活租户Pair IDlist (可选, List[string])
        name: name (可选, string)
        status: status (可选, string)
        local_storage_id: 本端storage device ID (可选, string)
        remote_storage_id: 远端storage device ID (可选, string)
        health_status: health status (可选, string)
        running_status: running status (可选, string)
        page_no: 分页页码 (可选, int32)
        page_size: items per page (可选, int32)

    Returns:
        {
            total: 双活租户Pair的count (int32),
            vstore_pairs: 双活租户Pair的listinfo (List<VstorePairListItem>). parameter format: [{
                id: 双活租户Pair的ID (string),
                raw_id: 在Storage device上的ID (string),
                local_vstore_name: 本端租户的name (string),
                local_vstore_raw_id: 本端租户在Storage device的ID (string),
                local_storage_id: 本端storage device ID (string),
                remote_vstore_name: 远端租户的name (string),
                remote_vstore_raw_id: 远端租户在Storage device的ID (string),
                remote_storage_id: 远端storage device ID (string),
                domain_id: 所属双活域的ID (string),
                domain_name: 所属双活域的name (string),
                running_status: running status. valid values: normal (正常), unsynchronized (未同步), invalid (失效), force_start (强制启动), split (分裂),
                config_status: 配置status. valid values: normal (正常), synchronizing (同步中), to_be_synchronized (待同步),
                health_status: health status. valid values: unknown (未知), normal (正常), fault (故障),
                link_status: 链路status. valid values: connected (已连接), disconnected (未连接),
                role: role. valid values: preferred (优先站点), non_preferred (非优先站点),
                active_status: 激活status. valid values: active (激活), passive (未激活),
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
    批量主从切换双活租户Pair. 

    Args:
        client: DME API client
        ids: 双活租户Pair的IDlist (必选, List[string])

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/metro/vstore-pairs/switch"

    if not ids or len(ids) == 0:
        raise ValueError("ids 是必选参数")

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def vstore_pair_delete(client: DMEAPIClient, ids: list) -> dict:
    """
    批量delete双活租户Pair. 

    Args:
        client: DME API client
        ids: 双活租户Pair的IDlist (必选, List[string])

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/metro/vstore-pairs/delete"

    if not ids or len(ids) == 0:
        raise ValueError("ids 是必选参数")

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def vstore_pair_modify(client: DMEAPIClient, id: str, name: str = None) -> dict:
    """
    modify指定双活租户pair. 

    Args:
        client: DME API client
        id: 双活租户Pair的ID (必选, string)
        name: name (可选, string)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/metro/vstore-pairs/{id}"

    if not id:
        raise ValueError("id 是必选参数")

    payload = {}
    if name is not None:
        payload['name'] = name

    response = client.put(url, body=payload, params={"id": id})
    return response


# ============================================================================
# 双活域 (hypermetro_domain) 子主题函数
# ============================================================================


def hypermetro_domain_force_start(client: DMEAPIClient, id: str) -> dict:
    """
    强制启动Filesystem双活域. 

    Args:
        client: DME API client
        id: 双活域ID (必选, string)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/hyper-metro-domains/{id}/force-start"

    if not id:
        raise ValueError("id 是必选参数")

    response = client.post(url, body={}, params={"id": id})
    return response


def hypermetro_domain_switch_site(client: DMEAPIClient, id: str) -> dict:
    """
    优先站点切换Filesystem双活域. 

    Args:
        client: DME API client
        id: 双活域ID (必选, string)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/hyper-metro-domains/{id}/switch-priority-site"

    if not id:
        raise ValueError("id 是必选参数")

    response = client.post(url, body={}, params={"id": id})
    return response


def hypermetro_domain_recover(client: DMEAPIClient, id: str) -> dict:
    """
    恢复Filesystem双活域. 

    Args:
        client: DME API client
        id: 双活域ID (必选, string)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/hyper-metro-domains/{id}/recover"

    if not id:
        raise ValueError("id 是必选参数")

    response = client.post(url, body={}, params={"id": id})
    return response


def hypermetro_domain_split(client: DMEAPIClient, id: str) -> dict:
    """
    分裂Filesystem双活域. 

    Args:
        client: DME API client
        id: 双活域ID (必选, string)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/hyper-metro-domains/{id}/split"

    if not id:
        raise ValueError("id 是必选参数")

    response = client.post(url, body={}, params={"id": id})
    return response


def hypermetro_domain_swap_role(client: DMEAPIClient, id: str) -> dict:
    """
    主从切换Filesystem双活域. 

    Args:
        client: DME API client
        id: 双活域ID (必选, string)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/protection/v1/hyper-metro-domains/{id}/swap-role"

    if not id:
        raise ValueError("id 是必选参数")

    response = client.post(url, body={}, params={"id": id})
    return response


# ============================================================================
# 双活Pair (hypermetro_pair) 子主题函数
# ============================================================================


def hypermetro_pair_query_available_luns(client: DMEAPIClient,
                                          source_lun_id: str) -> dict:
    """
    query可create双活Pair的目标LUN. 

    Args:
        client: DME API client
        source_lun_id: 源LUN ID (必选, string)

    Returns:
        {
            optional_target_luns: 可选目标LUNlist. parameter format: [{
                lun_id: LUN ID (string),
                lun_name: LUN name (string),
                capacity: capacity (integer),
            }, ...],
        }
    """
    url = "/rest/protection/v1/metro/lun-pairs/{source_lun_id}/optional-target-luns"

    if not source_lun_id:
        raise ValueError("source_lun_id 是必选参数")

    response = client.get(url, params={"source_lun_id": source_lun_id})
    return response


# action list, for CLI help
ACTIONS = {
    # group subtopic action
    'group_list': {
        'func': group_list,
        'description': '批量查询保护组',
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
        'description': '批量删除保护组',
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
    # hypermetro_group subtopic action
    'hypermetro_group_list': {
        'func': hypermetro_group_list,
        'description': '批量查询双活一致性组',
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
        'description': '批量删除双活一致性组',
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
    'hypermetro_group_sync': {
        'func': hypermetro_group_sync,
        'description': '同步双活一致性组',
        'params': ['ids'],
        'subtopic': 'hypermetro_group'
    },
    # hypermetro_pair subtopic action
    'hypermetro_pair_list': {
        'func': hypermetro_pair_list,
        'description': '批量查询 LUN 双活 Pair',
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
        'description': '批量删除双活 Pair',
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
    # hypermetro_domain subtopic action
    'hypermetro_domain_list': {
        'func': hypermetro_domain_list,
        'description': '批量查询双活域',
        'params': ['storage_id', 'types'],
        'subtopic': 'hypermetro_domain'
    },
    # replication_group subtopic action
    'replication_group_create': {
        'func': replication_group_create,
        'description': '创建远程复制一致性组',
        'params': ['cg_name', 'remote_storage_id', 'local_pg_id', 'description', 'remote_lun_group_id', 'local_storage_id', 'create_mode', 'existed_pair_ids', 'lun_pairs', 'lun_ids', 'remote_storage_pool_id', 'remote_vstore_id', 'remote_resource_name_rule', 'name_prefix', 'name_suffix'],
        'subtopic': 'replication_group'
    },
    'replication_group_list': {
        'func': replication_group_list,
        'description': '批量查询复制一致性组',
        'params': ['page_no', 'page_size', 'protect_group_id', 'name', 'raw_id', 'running_status', 'health_status', 'storage_name', 'storage_id', 'replication_mode'],
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
        'description': '批量删除远程复制一致性组',
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
    # replication_pair subtopic action
    'replication_pair_list': {
        'func': replication_pair_list,
        'description': '批量查询复制 Pair',
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
        'description': '批量删除远程复制 Pair',
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
    # device subtopic action
    'device_pair_list': {
        'func': device_pair_list,
        'description': '查询设备 Pairs',
        'params': ['storage_id'],
        'subtopic': 'device_pair'
    },
    'replication_link_list': {
        'func': replication_link_list,
        'description': '查询复制链路',
        'params': ['local_storage_id', 'page_no', 'page_size', 'health_status', 'running_status', 'link_type'],
        'subtopic': 'replication_link'
    },
    # snapshot subtopic action
    'snapshot_list': {
        'func': snapshot_list,
        'description': '批量查询 LUN 快照',
        'params': ['snapshot_ids', 'storage_id', 'raw_id', 'name', 'health_status', 'running_status', 'source_lun_name', 'parent_name', 'activated_time_from', 'activated_time_to', 'page_no', 'page_size'],
        'subtopic': 'snapshot'
    },
    'snapshot_create': {
        'func': snapshot_create,
        'description': '批量创建 LUN 快照',
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
        'description': '批量删除 LUN 快照',
        'params': ['snapshot_ids', 'is_delete_target_lun', 'is_auto_deactivate'],
        'subtopic': 'snapshot'
    },
    # snapshot_group subtopic action
    'snapshot_group_create': {
        'func': snapshot_group_create,
        'description': '创建快照一致性组',
        'params': ['name', 'protect_group_id', 'description', 'creation_mode'],
        'subtopic': 'snapshot_group'
    },
    'snapshot_group_delete': {
        'func': snapshot_group_delete,
        'description': '批量删除快照一致性组',
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
    # clone_group subtopic action
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
        'description': '批量删除克隆一致性组',
        'params': ['ids', 'is_delete_dst_lun', 'is_recycle_dst_lun_data'],
        'subtopic': 'clone_group'
    },
    # fs_hypermetro_pair subtopic action
    'filesystem_pair_create': {
        'func': filesystem_pair_create,
        'description': '创建文件系统双活Pair',
        'params': ['vstore_pair_id', 'create_mode', 'fs_pairs', 'speed', 'bandwidth', 'service_assurance_policy', 'isolation_threshold_time'],
        'subtopic': 'fs_hypermetro_pair'
    },
    'filesystem_pair_list': {
        'func': filesystem_pair_list,
        'description': '查询文件系统双活Pair列表',
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
        'description': '批量删除文件系统双活Pair',
        'params': ['ids', 'is_local_delete', 'is_online_delete'],
        'subtopic': 'fs_hypermetro_pair'
    },
    # fs_snapshot subtopic action
    'fs_snapshot_create': {
        'func': fs_snapshot_create,
        'description': '创建文件系统快照',
        'params': ['vstore_pair_id', 'fs_pairs'],
        'subtopic': 'fs_snapshot'
    },
    'fs_snapshot_list': {
        'func': fs_snapshot_list,
        'description': '批量查询文件系统快照',
        'params': ['fs_pair_id', 'name', 'status', 'local_fs_name', 'local_fs_id', 'page_no', 'page_size'],
        'subtopic': 'fs_snapshot'
    },
    'fs_snapshot_delete': {
        'func': fs_snapshot_delete,
        'description': '批量删除文件系统快照',
        'params': ['ids'],
        'subtopic': 'fs_snapshot'
    },
    # vstore_hypermetro_pair subtopic action
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
        'description': '查询双活租户Pair列表',
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
        'description': '批量删除双活租户Pair',
        'params': ['ids'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    'vstore_pair_modify': {
        'func': vstore_pair_modify,
        'description': '修改指定双活租户pair',
        'params': ['id', 'name'],
        'subtopic': 'vstore_hypermetro_pair'
    },
    # hypermetro_domain subtopic action
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
    # hypermetro_pair subtopic action
    'query_available_luns': {
        'func': hypermetro_pair_query_available_luns,
        'description': '查询可创建双活Pair的目标LUN',
        'params': ['source_lun_id'],
        'subtopic': 'hypermetro_pair'
    },
}
