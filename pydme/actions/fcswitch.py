"""
FC Switch (光纤交换机) 相关操作
"""

import sys
import os

from pydme.client import DMEAPIClient


def list(client: DMEAPIClient, name: str = None, 
                  page_no: int = 1, page_size: int = 20) -> dict:
    """
    批量查询交换机
    
    Args:
        client: DME API 客户端
        name: 交换机名称（可选，支持模糊查询）
        page_no: 分页查询的页码，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        {
            total: 总数量 (integer),
            fcswitches: 交换机列表 (List<FcSwitchInfo>)。参数格式如下：[{
                id: 交换机ID (string),
                name: 交换机名称 (string),
                status: 运行状态 (string),
            }, ...],
        }
    """
    url = "/rest/fcswitchmgmt/v1/fcswitches/list"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if name is not None:
        payload['name'] = name
    
    response = client.post(url, body=payload)
    return response


def sync(client: DMEAPIClient, switch_id: str) -> dict:
    """
    同步指定交换机
    
    Args:
        client: DME API 客户端
        switch_id: 交换机 ID（必选）
    
    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
    url = "/rest/fcswitchmgmt/v1/fcswitches/{switch_id}/sync"
    
    response = client.post(url, params={"switch_id": switch_id})
    return response


def port_list(client: DMEAPIClient, switch_id: str = None,
                       port_name: str = None, page_no: int = 1, 
                       page_size: int = 20) -> dict:
    """
    批量查询交换机端口
    
    Args:
        client: DME API 客户端
        switch_id: 交换机 ID（可选）
        port_name: 端口名称（可选）
        page_no: 分页查询的页码，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        {
            total: 总数量 (int),
            ports: 交换机端口列表 (List),
        }
    """
    url = "/rest/fcswitchmgmt/v1/fcswitches/ports/query"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if switch_id is not None:
        payload['switch_id'] = switch_id
    if port_name is not None:
        payload['port_name'] = port_name
    
    response = client.post(url, body=payload)
    return response



def controller_list(client: DMEAPIClient, switch_id: str = None,
                             page_no: int = 1, page_size: int = 20) -> dict:
    """
    批量查询交换机控制处理器
    
    Args:
        client: DME API 客户端
        switch_id: 交换机 ID（可选）
        page_no: 分页查询的页码，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        {
            total: 总数量 (int),
            controllers: 控制处理器列表 (List),
        }
    """
    url = "/rest/fcswitchmgmt/v1/fcswitches/controllers/query"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if switch_id is not None:
        payload['switch_id'] = switch_id
    
    response = client.post(url, body=payload)
    return response


def fabric_list(client: DMEAPIClient, name: str = None, 
                page_no: int = 1, page_size: int = 20) -> dict:
    """
    批量查询光纤网络
    
    Args:
        client: DME API 客户端
        name: 光纤网络名称（可选，支持模糊查询）
        page_no: 分页查询的页码，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        {
            total: 总数量 (int),
            fabrics: 光纤网络列表 (List),
        }
    """
    url = "/rest/fcswitchmgmt/v1/fabrics/list"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if name is not None:
        payload['name'] = name
    
    response = client.post(url, body=payload)
    return response


def fabric_show_ports(client: DMEAPIClient, fabric_id: str,
                      page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询指定光纤网络的端口列表

    Args:
        client: DME API 客户端
        fabric_id: 光纤网络 ID（必选）
        page_no: 分页查询的页码，默认 1
        page_size: 每页数量，1~1000，默认 20

    Returns:
        {
            total: 总数量 (int),
            ports: 端口列表 (List),
        }
    """
    url = "/rest/fcswitchmgmt/v1/fabrics/{fabric_id}/ports/list"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload, params={"fabric_id": fabric_id})
    return response


def fabric_backup(client: DMEAPIClient, fabric_id: str, backup_server_id: str,
                  backup_type: str = "full") -> dict:
    """
    执行光纤网络配置文件备份
    
    Args:
        client: DME API 客户端
        fabric_id: 光纤网络 ID（必选）
        backup_server_id: 备份服务器 ID（必选）
        backup_type: 备份类型，默认 full（full/incremental）
    
    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
    url = "/rest/fcswitchmgmt/v1/fabrics/{fabric_id}/backup"
    
    payload = {
        'backupRequest': {
            'backupServerId': backup_server_id,
            'backupType': backup_type
        }
    }
    
    response = client.post(url, body=payload, params={"fabric_id": fabric_id})
    return response


# ==================== VSAN 相关操作 ====================

def vsan_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询 VSAN 列表
    
    Args:
        client: DME API 客户端
        page_no: 分页查询的页码，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        {
            total: 总数量 (int),
            vsans: VSAN 列表 (List),
        }
    """
    url = "/rest/fcswitchmgmt/v1/vsans/query"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload)
    return response


# ==================== Zone 相关操作 ====================

def zone_list(client: DMEAPIClient, fabric_wwn: str = None, name: str = None,
              cfg_name: str = None, zone_set: str = None, active_status: list = None,
              member_count: int = None, sort_key: str = None, sort_dir: str = None,
              page_no: int = None, page_size: int = None) -> dict:
    """
    批量查询 zone

    ⚠️  注意：FC 交换机配置操作为同步执行，建议设置请求超时时间为 90 秒以上（--timeout 90）。

    Args:
        client: DME API 客户端
        fabric_wwn: 光纤网络 WWN（可选，string，1~1024 个字符）
        name: Zone 名称（可选，string，1~1024 个字符），支持模糊查询
        cfg_name: 所属 CFG 名称（可选，string，0~1024 个字符），支持模糊查询
        zone_set: 所属 Zone 集合（可选，string，0~1024 个字符），支持模糊查询
        active_status: Zone 状态列表（可选，List<string>，数组最大成员个数: 2）。可选值：ACTIVATED（已激活），INATIVATED（未激活）
        member_count: 成员数量（可选，int32，0~2147483647）
        sort_key: 排序字段（可选，string），可选值：member_count
        sort_dir: 排序方向（可选，string），可选值：asc（升序），desc（降序），默认升序
        page_no: 分页查询的页码（可选，int32，1~65535）
        page_size: 每页数量（可选，int32，1~1000）

    Returns:
        {
            total: Zone 数量 (int32),
            zones: Zone 列表 (List<ZoneBaseInfoResponse>)。参数格式如下：[{
                id: Zone id (string, 1~128个字符),
                fabric_id: 光纤网络 id (string, 0~128个字符),
                name: Zone 名称 (string, 1~64个字符),
                active_status: Zone 状态 (string, 1~16个字符)。可选值：ACTIVATED（已激活），INATIVATED（未激活）,
                member_count: 成员数量 (integer),
                cfg_name: 所属 CFG 名称 (string, 0~256个字符),
                zone_set: 所属 Zone 集合 (string, 0~256个字符),
                modifiable: 当前 Zone 是否可以操作 (boolean, true/false),
                zone_type: Zone 类型 (string)。可选值：regular（常规 Zone），user_specified_peer_zone（用户创建的对等 Zone），target_driven_peer_zone（目标驱动的对等 Zone）,
            }, ...],
        }
    """
    url = "/rest/fcswitchmgmt/v1/zones/list"

    payload = {}

    if fabric_wwn is not None:
        payload['fabric_wwn'] = fabric_wwn
    if name is not None:
        payload['name'] = name
    if cfg_name is not None:
        payload['cfg_name'] = cfg_name
    if zone_set is not None:
        payload['zone_set'] = zone_set
    if active_status is not None:
        payload['active_status'] = active_status
    if member_count is not None:
        payload['member_count'] = member_count
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size

    response = client.post(url, body=payload)
    return response


def zone_create(client: DMEAPIClient, name: str, fabric_wwn: str = None,
                vsan_wwn: str = None, wwn_members: list = None,
                port_members: list = None, fwwn_members: list = None,
                fcid_members: list = None, alias_members: list = None,
                device_alias_members: list = None) -> dict:
    """
    创建 zone
    在光纤网络中创建一个 zone 实例，必须包含 WWN 成员、端口成员、别名成员中的一种。

    ⚠️  注意：FC 交换机配置操作为同步执行，建议设置请求超时时间为 90 秒以上（--timeout 90）。

    Args:
        client: DME API 客户端
        name: Zone 名称（必选，string，1~64 个字符，正则 ^[A-Za-z][A-Za-z0-9_^$\\-]*$）
        fabric_wwn: 光纤网络 WWN（必选，string，1~128 个字符，正则 ^[A-Za-z0-9:]+$）
        vsan_wwn: VSAN WWN（可选，string，1~32 个字符）。条件必选：VSAN 创建 ZONE 时需要传递
        wwn_members: WWN 成员列表（可选，List<string>，数组最大成员个数: 100）
        port_members: 端口成员列表（可选，List<PortMemberRequest>，数组最大成员个数: 100）。参数格式如下：[{
                domain_id: 域 ID (可选, int32, 0~65535),
                port_index: 端口号 (条件必选, int32, 0~65535)，博科交换机时设置,
                port_name: 交换机端口 (条件必选, string, 1~32个字符，正则 ^[a-fA-F0-9/]+$)，思科交换机时设置,
                switch_wwn: 交换机 WWN (可选, string, 1~32个字符)，思科交换机需指定远端交换机时设置,
            }, ...]
        fwwn_members: FWWN 成员列表（可选，List<string>，数组最大成员个数: 100）
        fcid_members: FCID 成员列表（可选，List<string>，数组最大成员个数: 100）
        alias_members: 别名成员列表（可选，List<string>，数组最大成员个数: 100）
        device_alias_members: 设备别名成员列表（可选，List<string>，数组最大成员个数: 100）

    Returns:
        {
            id: Zone id (string, 1~64个字符),
            zone_name: Zone name (string, 1~64个字符),
        }
    """
    url = "/rest/fcswitchmgmt/v1/zones"

    payload = {
        'name': name
    }

    # fabric_wwn 或 vsan_wwn 至少提供一个
    if fabric_wwn is not None:
        payload['fabric_wwn'] = fabric_wwn
    if vsan_wwn is not None:
        payload['vsan_wwn'] = vsan_wwn

    # 成员列表
    if wwn_members is not None:
        payload['wwn_members'] = wwn_members
    if port_members is not None:
        payload['port_members'] = port_members
    if fwwn_members is not None:
        payload['fwwn_members'] = fwwn_members
    if fcid_members is not None:
        payload['fcid_members'] = fcid_members
    if alias_members is not None:
        payload['alias_members'] = alias_members
    if device_alias_members is not None:
        payload['device_alias_members'] = device_alias_members

    response = client.post(url, body=payload)
    return response


def zone_modify(client: DMEAPIClient, zone_id: str, zone_name: str = None,
                wwn_members: dict = None, alias_members: dict = None,
                fwwn_members: dict = None, port_members: dict = None,
                fcid_members: dict = None, device_alias_members: dict = None) -> dict:
    """
    修改 zone
    修改 zone 名称或变更成员。该操作会修改指定交换机上的 zone 名称或变更成员。

    ⚠️  注意：FC 交换机配置操作为同步执行，建议设置请求超时时间为 90 秒以上（--timeout 90）。

    Args:
        client: DME API 客户端
        zone_id: Zone ID（必选，string，正则 ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$）
        zone_name: Zone 名称（可选，string，1~64 个字符，正则 ^[A-Za-z][A-Za-z0-9_^$\\-]*$）
        wwn_members: WWN 成员修改（可选，ModifyWwnMembersRequest 对象）。参数格式如下：{
                added_members: 增加的 WWN 成员 (可选, List<string>, 数组最大成员个数: 100),
                removed_members: 移除的 WWN 成员 (可选, List<string>, 数组最大成员个数: 100),
            }
        port_members: 端口成员修改（可选，ModifyPortMembersRequest 对象）。参数格式如下：{
                added_members: 增加的端口成员 (可选, List<PortMemberRequest>, 数组最大成员个数: 100)。属性格式如下：{
                    domain_id: 域 ID (可选, int32, 0~65535),
                    port_index: 端口号 (条件必选, int32, 0~65535)，博科交换机时设置,
                    port_name: 交换机端口 (条件必选, string, 1~32个字符，正则 ^[a-fA-F0-9/]+$)，思科交换机时设置,
                    switch_wwn: 交换机 WWN (可选, string, 1~32个字符),
                },
                removed_members: 移除的端口成员 (可选, List<PortMemberRequest>, 数组最大成员个数: 100),
            }
        alias_members: 别名成员修改（可选，ModifyAliasMembersRequest 对象）。参数格式如下：{
                added_members: 增加的别名成员 (可选, List<string>, 数组最大成员个数: 100),
                removed_members: 移除的别名成员 (可选, List<string>, 数组最大成员个数: 100),
            }
        fwwn_members: FWWN 成员修改（可选，ModifyFwwnMembersRequest 对象）。参数格式如下：{
                added_members: 增加的 FWWN 成员 (可选, List<string>, 数组最大成员个数: 100),
                removed_members: 移除的 FWWN 成员 (可选, List<string>, 数组最大成员个数: 100),
            }
        fcid_members: FCID 成员修改（可选，ModifyFcidMembersRequest 对象）。参数格式如下：{
                added_members: 增加的 FCID 成员 (可选, List<string>, 数组最大成员个数: 100),
                removed_members: 移除的 FCID 成员 (可选, List<string>, 数组最大成员个数: 100),
            }
        device_alias_members: 设备别名成员修改（可选，ModifyDeviceAliasMembersRequest 对象）。参数格式如下：{
                added_members: 增加的设备别名成员 (可选, List<string>, 数组最大成员个数: 100),
                removed_members: 移除的设备别名成员 (可选, List<string>, 数组最大成员个数: 100),
            }

    Returns:
        无。
    """
    url = "/rest/fcswitchmgmt/v1/zones/{zone_id}"

    payload = {}
    if zone_name is not None:
        payload['zoneName'] = zone_name
    if wwn_members is not None:
        payload['wwn_members'] = wwn_members
    if alias_members is not None:
        payload['alias_members'] = alias_members
    if fwwn_members is not None:
        payload['fwwn_members'] = fwwn_members
    if port_members is not None:
        payload['port_members'] = port_members
    if fcid_members is not None:
        payload['fcid_members'] = fcid_members
    if device_alias_members is not None:
        payload['device_alias_members'] = device_alias_members

    response = client.put(url, body=payload, params={"zone_id": zone_id})
    return response


def zone_delete(client: DMEAPIClient, zone_id: str) -> dict:
    """
    删除 zone
    该操作会删除指定交换机上的 zone。

    ⚠️  注意：FC 交换机配置操作为同步执行，建议设置请求超时时间为 90 秒以上（--timeout 90）。

    Args:
        client: DME API 客户端
        zone_id: Zone ID（必选，string，正则 ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$）

    Returns:
        无。
    """
    url = "/rest/fcswitchmgmt/v1/zones/{zone_id}"
    
    response = client.delete(url, params={"zone_id": zone_id})
    return response


def zone_batch_create(client: DMEAPIClient, is_active_zone: str, zones: list) -> dict:
    """
    批量创建 zone

    ⚠️  注意：FC 交换机配置操作为同步执行，建议设置请求超时时间为 90 秒以上（--timeout 90）。

    Args:
        client: DME API 客户端
        is_active_zone: 是否激活 zones（必选，boolean），可选值：true（激活），false（不激活）
        zones: 创建 zone 的请求列表（List<ZoneCreateRequest>，必选，数组最小成员个数: 1，数组最大成员个数: 20）。参数格式如下：[{
                fabric_wwn: 光纤网络 WWN（必选，string，1~128 个字符，正则 ^[A-Za-z0-9:]+$）,
                name: Zone 名称（必选，string，1~64 个字符，正则 ^[A-Za-z][A-Za-z0-9_^$\\-]*$）,
                vsan_wwn: VSAN WWN（可选，string，1~32 个字符）。条件必选：VSAN 创建 ZONE 时需要传递,
                wwn_members: WWN 成员列表（可选，List<string>，数组最大成员个数: 100）,
                port_members: 端口成员列表（可选，List<PortMemberRequest>，数组最大成员个数: 100）。属性格式如下：[{
                    domain_id: 域 ID (可选, int32, 0~65535),
                    port_index: 端口号 (条件必选, int32, 0~65535)，博科交换机时设置,
                    port_name: 交换机端口 (条件必选, string, 1~32个字符，正则 ^[a-fA-F0-9/]+$)，思科交换机时设置,
                    switch_wwn: 交换机 WWN (可选, string, 1~32个字符),
                }, ...],
                alias_members: 别名成员列表（可选，List<string>，数组最大成员个数: 100）,
                device_alias_members: 设备别名成员列表（可选，List<string>，数组最大成员个数: 100）,
                fwwn_members: FWWN 成员列表（可选，List<string>，数组最大成员个数: 100）,
                fcid_members: FCID 成员列表（可选，List<string>，数组最大成员个数: 100）,
            }, ...]

    Returns:
        无。
    """
    url = "/rest/fcswitchmgmt/v1/zones/batch-create"

    payload = {
        'is_active_zone': is_active_zone,
        'zone_list': zones
    }

    response = client.post(url, body=payload)
    return response


def zone_show_members(client: DMEAPIClient, zone_id: str, type: str = None) -> dict:
    """
    查询 zone 的成员
    查询 Zone 中包含的成员，支持端口成员、WWN 成员和别名成员。

    ⚠️  注意：FC 交换机配置操作为同步执行，建议设置请求超时时间为 90 秒以上（--timeout 90）。

    Args:
        client: DME API 客户端
        zone_id: Zone ID（必选，string，正则 ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$）
        type: 成员类型（可选，string）。可选值：port（端口成员），wwn（WWN 成员），alias（别名成员）。不指定时返回所有类型的成员

    Returns:
        {
            total: WWN 成员数量 (int32, type=wwn 时),
            wwn_members: WWN 成员列表 (List<GetWwnMembersResponse>, type=wwn 时)。参数格式如下：[{
                member_wwn: 成员 WWN (string, 1~128个字符),
            }, ...],
            total: 端口成员数量 (int32, type=port 时),
            port_members: 端口成员列表 (List<ZonePortMemberResponse>, type=port 时)。参数格式如下：[{
                domain_id: 域 id (int32, 0~65535),
                port_index: 交换机端口索引 (int32, 0~65535),
                port_name: 端口名称 (string, 1~256个字符),
                switch_ip: 端口所属交换机 IP (string, 1~32个字符),
                switch_name: 端口所属交换机名称 (string, 1~2048个字符),
            }, ...],
            total: 别名成员数量 (int32, type=alias 时),
            alias_members: 别名成员列表 (List<AliasBaseInfo>, type=alias 时)。参数格式如下：[{
                id: 别名 id (string, 1~64个字符),
                role: 成员类型 (string)。可选值：regular（常规），principal（主要成员），non_principal（非主要成员）,
                type: 别名成员类型 (string)。可选值：wwn, port, fwwn, fcid, ip-address, device-alias, domain-id, symbolic-node-name, empty, mixed,
                fabric_id: 光纤网络 id (string, 0~64个字符),
                fabric_wwn: 光纤网络 WWN (string, 1~32个字符),
                name: 别名名称 (string, 1~128个字符),
                member_count: 别名的成员数量 (int32, 0~65535),
                modifiable: 当前别名是否可以操作 (boolean, true/false),
            }, ...],
            members: 所有成员列表 (List, 不指定 type 时),
        }
    """
    result = {'port_members': [], 'wwn_members': [], 'alias_members': []}

    # 根据 type 参数查询对应类型的成员
    if type is None or type == 'port':
        url = "/rest/fcswitchmgmt/v1/zones/{zone_id}/port-members/list"
        payload = {}
        response = client.post(url, body=payload, params={"zone_id": zone_id})
        if response.get('port_members'):
            result['port_members'] = response.get('port_members')

    if type is None or type == 'wwn':
        url = "/rest/fcswitchmgmt/v1/zones/{zone_id}/wwn-members/list"
        response = client.get(url, params={"zone_id": zone_id})
        if response.get('wwn_members'):
            result['wwn_members'] = response.get('wwn_members')

    if type is None or type == 'alias':
        url = "/rest/fcswitchmgmt/v1/zones/{zone_id}/alias-members/list"
        payload = {}
        response = client.post(url, body=payload, params={"zone_id": zone_id})
        if response.get('alias_members'):
            result['alias_members'] = response.get('alias_members')

    # 如果指定了 type，只返回对应类型的成员
    if type == 'port':
        return {'port_members': result['port_members']}
    elif type == 'wwn':
        return {'wwn_members': result['wwn_members']}
    elif type == 'alias':
        return {'alias_members': result['alias_members']}
    else:
        # 返回所有成员
        all_members = result['port_members'] + result['wwn_members'] + result['alias_members']
        return {'members': all_members}


# ==================== Alias 相关操作 ====================

def alias_list(client: DMEAPIClient, fabric_wwn: str,
               page_no: int = 1, page_size: int = 20) -> dict:
    """
    批量查询别名

    ⚠️  注意：FC 交换机配置操作为同步执行，建议设置请求超时时间为 90 秒以上（--timeout 90）。

    Args:
        client: DME API 客户端
        fabric_wwn: 光纤网络 WWN（必选，string，1~1024 个字符），从查询光纤网络接口获取
        name: 别名名称（可选，string，1~1024 个字符），支持模糊查询
        member_count: 成员数量（可选，int32，0~65535）
        page_no: 分页查询的页码（可选，int32，1~2147483647），默认 1
        page_size: 每页数量（可选，int32，1~1000），默认 20
        sort_key: 排序字段（可选，string），可选值：member_count（按成员数量排序）
        sort_dir: 排序方向（可选，string），可选值：asc（升序），desc（降序），默认升序

    Returns:
        {
            total: 别名总数 (int32),
            aliases: 别名列表 (List<AliasBaseInfoResponse>)。参数格式如下：[{
                id: 别名 id (string, 1~64个字符),
                fabric_id: 光纤网络 id (string, 1~64个字符),
                fabric_wwn: 光纤网络 WWN (string, 1~32个字符),
                name: 别名名称 (string, 1~128个字符),
                member_count: 成员数量 (int32, 0~65535),
                modifiable: 当前别名是否可以操作 (boolean, true/false),
            }, ...],
        }
    """
    url = "/rest/fcswitchmgmt/v1/aliases/list"
    
    payload = {
        'fabric_wwn': fabric_wwn,
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload)
    return response


def alias_create(client: DMEAPIClient, name: str, fabric_wwn: str = None,
                 vsan_wwn: str = None, wwn_members: list = None,
                 port_members: list = None, fwwn_members: list = None,
                 fcid_members: list = None, device_alias_members: list = None) -> dict:
    """
    创建别名
    该操作会在指定交换机上创建别名。

    ⚠️  注意：FC 交换机配置操作为同步执行，建议设置请求超时时间为 90 秒以上（--timeout 90）。

    Args:
        client: DME API 客户端
        name: 别名名称（必选，string，1~64 个字符，正则 ^[A-Za-z0-9][A-Za-z0-9_^$\\-]*$）
        fabric_wwn: 光纤网络 WWN（条件必选，string，1~32 个字符），光纤网络创建别名时需要传递
        vsan_wwn: VSAN WWN（条件必选，string，1~32 个字符），VSAN 创建别名时需要传递
        wwn_members: WWN 成员列表（可选，List<string>，数组最大成员个数: 100）。思科交换机的 PWWN 成员使用此参数传递。华为/博科交换机：WWN 成员与端口成员至少二选一；思科交换机：PWWN、FWWN、端口、FCID、设备别名至少五选一
        fwwn_members: FWWN 成员列表（可选，List<string>，数组最大成员个数: 100）。思科交换机：PWWN、FWWN、端口、FCID、设备别名至少五选一
        port_members: 端口成员列表（可选，List<PortMemberRequest>，数组最大成员个数: 100）。参数格式如下：[{
                domain_id: 域 ID (可选, int32, 0~65535),
                port_index: 端口号 (条件必选, int32, 0~65535)，博科交换机配置端口成员时设置,
                port_name: 交换机端口 (条件必选, string, 1~32个字符，正则 ^[a-fA-F0-9/]+$)，思科交换机配置端口成员时设置,
                switch_wwn: 交换机 WWN (可选, string, 1~32个字符)，思科交换机需指定远端交换机时设置,
            }, ...]
        fcid_members: FCID 成员列表（可选，List<string>，数组最大成员个数: 100）。思科交换机：PWWN、FWWN、端口、FCID、设备别名至少五选一
        device_alias_members: 设备别名成员列表（可选，List<string>，数组最大成员个数: 100）。思科交换机：PWWN、FWWN、端口、FCID、设备别名至少五选一

    Returns:
        {
            id: 别名 id (string, 1~64个字符),
        }
    """
    url = "/rest/fcswitchmgmt/v1/aliases"
    
    payload = {
        'name': name
    }
    
    # fabric_wwn 或 vsan_wwn 至少提供一个
    if fabric_wwn is not None:
        payload['fabric_wwn'] = fabric_wwn
    if vsan_wwn is not None:
        payload['vsan_wwn'] = vsan_wwn
    
    # 成员列表
    if wwn_members is not None:
        payload['wwn_members'] = wwn_members
    if port_members is not None:
        payload['port_members'] = port_members
    if fwwn_members is not None:
        payload['fwwn_members'] = fwwn_members
    if fcid_members is not None:
        payload['fcid_members'] = fcid_members
    if device_alias_members is not None:
        payload['device_alias_members'] = device_alias_members
    
    response = client.post(url, body=payload)
    return response


def alias_modify(client: DMEAPIClient, alias_id: str, name: str = None,
                 wwn_members: dict = None, fwwn_members: dict = None,
                 port_members: dict = None, fcid_members: dict = None,
                 device_alias_members: dict = None) -> dict:
    """
    修改别名
    变更别名成员。博科交换机支持 WWN 成员、端口成员修改；思科交换机支持 PWWN、FWWN、端口、FCID、设备别名成员修改。

    ⚠️  注意：FC 交换机配置操作为同步执行，建议设置请求超时时间为 90 秒以上（--timeout 90）。

    Args:
        client: DME API 客户端
        alias_id: 别名 ID（必选，string，正则 ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$）
        name: 别名名称（可选，string，1~64 个字符，正则 ^[A-Za-z0-9][A-Za-z0-9_^$\\-]*$）。条件可选：思科交换机支持修改别名名称，博科交换机不支持
        wwn_members: WWN 成员修改（可选，WwnMembersRequest 对象）。参数格式如下：{
                added_members: 增加的 WWN 成员 (可选, List<string>, 数组最大成员个数: 100),
                removed_members: 移除的 WWN 成员 (可选, List<string>, 数组最大成员个数: 100),
            }
        fwwn_members: FWWN 成员修改（可选，FwwnMembersRequest 对象）。参数格式如下：{
                added_members: 增加的 FWWN 成员 (可选, List<string>, 数组最大成员个数: 100),
                removed_members: 移除的 FWWN 成员 (可选, List<string>, 数组最大成员个数: 100),
            }
        port_members: 端口成员修改（可选，PortMembersRequest 对象）。参数格式如下：{
                added_members: 增加的端口成员 (可选, List<PortMemberRequest>, 数组最大成员个数: 100)。属性格式如下：{
                    domain_id: 域 ID (可选, int32, 0~65535),
                    port_index: 端口号 (条件必选, int32, 0~65535)，博科交换机时设置,
                    port_name: 交换机端口 (条件必选, string, 1~32个字符，正则 ^[a-fA-F0-9/]+$)，思科交换机时设置,
                    switch_wwn: 交换机 WWN (可选, string, 1~32个字符),
                },
                removed_members: 移除的端口成员 (可选, List<PortMemberRequest>, 数组最大成员个数: 100),
            }
        fcid_members: FCID 成员修改（可选，FcidMembersRequest 对象）。参数格式如下：{
                added_members: 增加的 FCID 成员 (可选, List<string>, 数组最大成员个数: 100),
                removed_members: 移除的 FCID 成员 (可选, List<string>, 数组最大成员个数: 100),
            }
        device_alias_members: 设备别名成员修改（可选，DeviceAliasMembersRequest 对象）。参数格式如下：{
                added_members: 增加的设备别名成员 (可选, List<string>, 数组最大成员个数: 100),
                removed_members: 移除的设备别名成员 (可选, List<string>, 数组最大成员个数: 100),
            }

    Returns:
        无。
    """
    url = "/rest/fcswitchmgmt/v1/aliases/{alias_id}"
    
    payload = {}
    if name is not None:
        payload['name'] = name
    if wwn_members is not None:
        payload['wwn_members'] = wwn_members
    if fwwn_members is not None:
        payload['fwwn_members'] = fwwn_members
    if port_members is not None:
        payload['port_members'] = port_members
    if fcid_members is not None:
        payload['fcid_members'] = fcid_members
    if device_alias_members is not None:
        payload['device_alias_members'] = device_alias_members
    
    response = client.put(url, body=payload, params={"alias_id": alias_id})
    return response


def alias_delete(client: DMEAPIClient, alias_id: str) -> dict:
    """
    删除别名
    该操作会删除指定交换机上的别名。

    ⚠️  注意：FC 交换机配置操作为同步执行，建议设置请求超时时间为 90 秒以上（--timeout 90）。

    Args:
        client: DME API 客户端
        alias_id: 别名 ID（必选，string，正则 ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$）

    Returns:
        无。
    """
    url = "/rest/fcswitchmgmt/v1/aliases/{alias_id}"
    
    response = client.delete(url, params={"alias_id": alias_id})
    return response


def alias_show_members(client: DMEAPIClient, alias_id: str, type: str = None) -> dict:
    """
    查询别名的成员
    查询 Alias 中包含的成员，支持查询端口成员和 WWN 成员。

    ⚠️  注意：FC 交换机配置操作为同步执行，建议设置请求超时时间为 90 秒以上（--timeout 90）。

    Args:
        client: DME API 客户端
        alias_id: 别名 ID（必选，string，正则 ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$）
        type: 成员类型（可选，string）。可选值：port（端口成员），wwn（WWN 成员）。不指定时返回所有类型的成员

    Returns:
        {
            total: WWN 成员总数 (int32, type=wwn 时),
            wwn_member: WWN 成员列表 (List<GetWwnMembersResponse>, type=wwn 时)。参数格式如下：[{
                member_wwn: 成员 WWN (string, 1~128个字符),
            }, ...],
            total: 端口成员总数 (int32, type=port 时),
            port_members: 端口成员列表 (List<PortMemberInfoResponse>, type=port 时)。参数格式如下：[{
                domain_id: 域 id (int32, 0~65535),
                port_index: 交换机端口索引 (int32, 0~65535),
                port_name: 交换机端口名称 (string, 1~128个字符),
                switch_ip: 端口所属交换机 IP (string, 1~32个字符),
                switch_name: 端口所属交换机名称 (string, 1~2048个字符),
            }, ...],
            members: 所有成员列表 (List, 不指定 type 时),
        }
    """
    result = {'port_members': [], 'wwn_members': []}

    # 如果指定了 type 或默认为 None 时，查询对应类型的成员
    if type is None or type == 'port':
        url = "/rest/fcswitchmgmt/v1/aliases/{alias_id}/port-members/list"
        payload = {}
        response = client.post(url, body=payload, params={"alias_id": alias_id})
        if response.get('port_members'):
            result['port_members'] = response.get('port_members')

    if type is None or type == 'wwn':
        url = "/rest/fcswitchmgmt/v1/aliases/{alias_id}/wwn-members/list"
        response = client.get(url, params={"alias_id": alias_id})
        # API 返回字段为 wwn_member（单数）
        if response.get('wwn_member'):
            result['wwn_members'] = response.get('wwn_member')

    # 如果指定了 type，只返回对应类型的成员
    if type == 'port':
        return {'port_members': result['port_members']}
    elif type == 'wwn':
        return {'wwn_members': result['wwn_members']}
    else:
        # 返回所有成员
        all_members = result['port_members'] + result['wwn_members']
        return {'members': all_members}


# ACTIONS 字典，定义所有可用动作
ACTIONS = {
    'list': {
        'func': list,
        'description': '批量查询光纤交换机',
        'params': ['name', 'page_no', 'page_size'],
        'subtopic': None
    },
    'sync': {
        'func': sync,
        'description': '同步交换机配置',
        'params': ['switch_id'],
        'subtopic': None
    },
    'port_list': {
        'func': port_list,
        'description': '查询交换机端口列表',
        'params': ['switch_id', 'port_name', 'page_no', 'page_size'],
        'subtopic': 'port'
    },
    'controller_list': {
        'func': controller_list,
        'description': '查询交换机控制器列表',
        'params': ['switch_id', 'page_no', 'page_size'],
        'subtopic': 'controller'
    },
    'fabric_list': {
        'func': fabric_list,
        'description': '批量查询 fabric',
        'params': ['name', 'page_no', 'page_size'],
        'subtopic': 'fabric'
    },
    'fabric_show_ports': {
        'func': fabric_show_ports,
        'description': '查询 fabric 的端口列表',
        'params': ['fabric_id', 'page_no', 'page_size'],
        'subtopic': 'fabric'
    },
    'fabric_backup': {
        'func': fabric_backup,
        'description': '备份 fabric 配置',
        'params': ['fabric_id', 'backup_server_id', 'backup_type'],
        'subtopic': 'fabric'
    },
    'vsan_list': {
        'func': vsan_list,
        'description': '批量查询 vsan',
        'params': ['page_no', 'page_size'],
        'subtopic': 'vsan'
    },
    'zone_list': {
        'func': zone_list,
        'description': '批量查询 zone',
        'params': ['zone_name', 'page_no', 'page_size'],
        'subtopic': 'zone'
    },
    'zone_create': {
        'func': zone_create,
        'description': '创建 zone',
        'params': ['name', 'fabric_wwn', 'vsan_wwn', 'wwn_members', 'port_members', 'fwwn_members', 'fcid_members', 'device_alias_members'],
        'subtopic': 'zone'
    },
    'zone_modify': {
        'func': zone_modify,
        'description': '修改 zone',
        'params': ['zone_id', 'zone_name', 'wwn_members', 'fwwn_members', 'port_members', 'fcid_members', 'device_alias_members'],
        'subtopic': 'zone'
    },
    'zone_delete': {
        'func': zone_delete,
        'description': '删除 zone',
        'params': ['zone_id'],
        'subtopic': 'zone'
    },
    'zone_batch_create': {
        'func': zone_batch_create,
        'description': '批量创建 zone',
        'params': ['is_active_zone', 'zones'],
        'subtopic': 'zone'
    },
    'zone_show_members': {
        'func': zone_show_members,
        'description': '查询 zone 的成员',
        'params': ['zone_id', 'type'],
        'subtopic': 'zone'
    },
    'alias_list': {
        'func': alias_list,
        'description': '批量查询别名',
        'params': ['fabric_wwn', 'page_no', 'page_size'],
        'subtopic': 'alias'
    },
    'alias_create': {
        'func': alias_create,
        'description': '创建别名',
        'params': ['name', 'fabric_wwn', 'vsan_wwn', 'wwn_members', 'port_members', 'fwwn_members', 'fcid_members', 'device_alias_members'],
        'subtopic': 'alias'
    },
    'alias_modify': {
        'func': alias_modify,
        'description': '修改别名',
        'params': ['alias_id', 'name', 'wwn_members', 'fwwn_members', 'port_members', 'fcid_members', 'device_alias_members'],
        'subtopic': 'alias'
    },
    'alias_delete': {
        'func': alias_delete,
        'description': '删除别名',
        'params': ['alias_id'],
        'subtopic': 'alias'
    },
    'alias_show_members': {
        'func': alias_show_members,
        'description': '查询别名的成员',
        'params': ['alias_id', 'type'],
        'subtopic': 'alias'
    },
}


