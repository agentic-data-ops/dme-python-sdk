"""
FC Switch (光纤交换机) operations
"""

import sys
import os

from pydme.client import DMEAPIClient


def list(client: DMEAPIClient, name: str = None, 
                  page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch query交换机
    
    Args:
        client: DME API client
        name: 交换机名称（Optional，supports fuzzy search）
        page_no: 分页查询的页码，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        {
            total: 总数量 (integer),
            fcswitches: Switch list (List<FcSwitchInfo>)。参数格式如下：[{
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
        client: DME API client
        switch_id: 交换机 ID（Required）
    
    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fcswitchmgmt/v1/fcswitches/{switch_id}/sync"
    
    response = client.post(url, params={"switch_id": switch_id})
    return response


def port_list(client: DMEAPIClient, switch_id: str = None,
                       port_name: str = None, page_no: int = 1, 
                       page_size: int = 20) -> dict:
    """
    Batch query交换机端口
    
    Args:
        client: DME API client
        switch_id: 交换机 ID（Optional）
        port_name: 端口名称（Optional）
        page_no: 分页查询的页码，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }，包含 total 和 ports 字段
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
    Batch query交换机控制处理器
    
    Args:
        client: DME API client
        switch_id: 交换机 ID（Optional）
        page_no: 分页查询的页码，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }，包含 total 和 controllers 字段
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
    Batch query光纤网络
    
    Args:
        client: DME API client
        name: 光纤网络名称（Optional，supports fuzzy search）
        page_no: 分页查询的页码，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }，包含 total 和 fabrics 字段
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
    Query光纤网络的端口列表

    Args:
        client: DME API client
        fabric_id: 光纤网络 ID（Required）
        page_no: 分页查询的页码，默认 1
        page_size: 每页数量，1~1000，默认 20

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }，包含 total 和 ports 字段
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
        client: DME API client
        fabric_id: 光纤网络 ID（Required）
        backup_server_id: 备份服务器 ID（Required）
        backup_type: 备份类型，默认 full（full/incremental）
    
    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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


# ==================== VSAN operations ====================

def vsan_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询 VSAN 列表
    
    Args:
        client: DME API client
        page_no: 分页查询的页码，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }，包含 total 和 vsans 字段
    """
    url = "/rest/fcswitchmgmt/v1/vsans/query"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload)
    return response


# ==================== Zone operations ====================

def zone_list(client: DMEAPIClient, fabric_wwn: str = None, name: str = None,
              cfg_name: str = None, zone_set: str = None, active_status: list = None,
              member_count: int = None, sort_key: str = None, sort_dir: str = None,
              page_no: int = None, page_size: int = None) -> dict:
    """
    Batch query zone

    查询光纤 Zone 列表。

    Args:
        client: DME API client
        fabric_wwn: 光纤网络 WWN（Optional），1~1024 个字符
        name: Zone 名称（Optional），supports fuzzy search，1~1024 个字符
        cfg_name: 所属 CFG 名称（Optional），supports fuzzy search，0~1024 个字符
        zone_set: 所属 Zone 集合（Optional），supports fuzzy search，0~1024 个字符
        active_status: Zone 状态列表（Optional），数组最大成员个数：2
        member_count: 成员数量（Optional），0~2147483647
        sort_key: 排序字段（Optional），支持 member_count
        sort_dir: 排序方向（Optional），asc：升序；desc：降序
        page_no: 分页查询的页码（Optional），1~65535
        page_size: 每页数量（Optional），1~1000

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }，包含 total 和 zones 字段
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

    注：根据 DME API 文档，需要提供 fabric_wwn 或 vsan_wwn，以及至少一种成员类型。

    Args:
        client: DME API client
        name: Zone 名称（Required）
        fabric_wwn: 光纤网络 WWN（条件Required，fabric 创建 zone 时需要）
        vsan_wwn: VSAN WWN（条件Required，vsan 创建 zone 时需要）
        wwn_members: WWN 成员列表（Optional），格式：["<wwn>",...]
        port_members: 端口成员列表（Optional），格式：[{"domain_id":"<domainId>","port_index":"<portIndex>","port_name":"portName"},...]，其中博科交换机指定port_index，思科交换机指定port_name
        fwwn_members: FWWN 成员列表（Optional），格式：["<fwwn>",...]
        fcid_members: FCID 成员列表（Optional），格式：["<fcid>",...]
        alias_members: 别名成员列表（Optional），格式：["<alias>",...]
        device_alias_members: 设备别名成员列表（Optional），格式：["<deviceAlias>",...]

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }，包含新创建的 Zone ID
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

    修改光纤 Zone 的Configuration info。

    Args:
        client: DME API client
        zone_id: Zone ID（Required）
        zone_name: Zone 名称（Optional）
        wwn_members: WWN 成员修改（Optional），格式：{"added_members": ["<wwn>",...], "removed_members": ["<wwn>",...]}
        alias_members: 别名成员修改（Optional），格式：{"added_members": ["<alias>",...], "removed_members": ["<alias>",...]}
        fwwn_members: FWWN 成员修改（Optional），格式：{"added_members": ["<fwwn>",...], "removed_members": ["<fwwn>",...]}
        port_members: 端口成员修改（Optional），格式：{"added_members": [{"domain_id":"<domainId>","port_index":"<portIndex>","port_name":"portName"},...], "removed_members": [{"domain_id":"<domainId>","port_index":"<portIndex>","port_name":"portName"},...]}，其中博科交换机指定port_index，思科交换机指定port_name
        fcid_members: FCID 成员修改（Optional），格式：{"added_members": ["<fcid>",...], "removed_members": ["<fcid>",...]}
        device_alias_members: 设备别名成员修改（Optional），格式：{"added_members": ["<deviceAlias>",...], "removed_members": ["<deviceAlias>",...]}

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
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
    注：根据 DME API 文档，使用 DELETE 方法到 /zones/{zone_id}
    
    Args:
        client: DME API client
        zone_id: Zone ID（Required）
    
    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fcswitchmgmt/v1/zones/{zone_id}"
    
    response = client.delete(url, params={"zone_id": zone_id})
    return response


def zone_batch_create(client: DMEAPIClient, is_active_zone: str, zones: list) -> dict:
    """
    Batch create zone

    注：根据 DME API 文档，需要 is_active_zone 和 zone_list 参数。

    Args:
        client: DME API client
        is_active_zone: 是否激活 Zone（Required，字符串 "true" 或 "false"）
        zones: Zone 配置列表，每个元素应包含:
            - fabric_wwn: 光纤网络 WWN（Required）
            - name: Zone 名称（Required）
            - wwn_members: WWN 成员列表（Optional），格式：["<wwn>",...]
            - port_members: 端口成员列表（Optional），格式：[{"domain_id":"<domainId>","port_index":"<portIndex>","port_name":"portName"},...]，其中博科交换机指定port_index，思科交换机指定port_name
            - fwwn_members: FWWN 成员列表（Optional），格式：["<fwwn>",...]
            - fcid_members: FCID 成员列表（Optional），格式：["<fcid>",...]
            - alias_members: 别名成员列表（Optional），格式：["<alias>",...]
            - device_alias_members: 设备别名成员列表（Optional），格式：["<deviceAlias>",...]

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
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

    Args:
        client: DME API client
        zone_id: Zone ID（Required）
        type: 成员类型，Optional值：port（端口成员）,wwn（WWN 成员）,alias（别名成员）。
             不指定时返回所有类型的成员

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }，包含成员列表
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


# ==================== Alias operations ====================

def alias_list(client: DMEAPIClient, fabric_wwn: str,
               page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch query别名
    
    查询光纤 Alias 列表。
    
    Args:
        client: DME API client
        fabric_wwn: 光纤网络 WWN（Required）
        page_no: 分页查询的页码，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }，包含 total 和 aliases 字段
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

    注：根据 DME API 文档，需要提供 fabric_wwn 或 vsan_wwn，以及至少一种成员类型。

    Args:
        client: DME API client
        name: Alias 名称（Required）
        fabric_wwn: 光纤网络 WWN（条件Required，fabric 创建别名时需要）
        vsan_wwn: VSAN WWN（条件Required，vsan 创建别名时需要）
        wwn_members: WWN 成员列表（Optional，思科交换机 PWWN 成员）
        port_members: 端口成员列表（Optional）
        fwwn_members: FWWN 成员列表（Optional）
        fcid_members: FCID 成员列表（Optional）
        device_alias_members: 设备别名成员列表（Optional）
    
    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }，包含新创建的 Alias ID
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

    注：根据 DME API 文档，成员修改需要使用 {type}.added_members 和 {type}.removed_members 格式。

    Args:
        client: DME API client
        alias_id: Alias ID（Required）
        name: Alias 名称（Optional）
        wwn_members: WWN 成员修改（Optional，格式：{'added_members': [...], 'removed_members': [...]}）
        fwwn_members: FWWN 成员修改（Optional）
        port_members: 端口成员修改（Optional）
        fcid_members: FCID 成员修改（Optional）
        device_alias_members: 设备别名成员修改（Optional）
    
    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
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

    注：根据 DME API 文档，使用 DELETE 方法到 /aliases/{alias_id}

    Args:
        client: DME API client
        alias_id: Alias ID（Required）
    
    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fcswitchmgmt/v1/aliases/{alias_id}"
    
    response = client.delete(url, params={"alias_id": alias_id})
    return response


def alias_show_members(client: DMEAPIClient, alias_id: str, type: str = None) -> dict:
    """
    查询别名的成员

    查询 Alias 中包含的成员，支持查询端口成员和 WWN 成员。

    Args:
        client: DME API client
        alias_id: Alias ID（Required）
        type: 成员类型，Optional值：port（端口成员）,wwn（WWN 成员）。
             不指定时返回所有类型的成员

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }，包含成员列表
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
        'description': 'Batch query光纤交换机',
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
        'description': 'Batch query fabric',
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
        'description': 'Batch query vsan',
        'params': ['page_no', 'page_size'],
        'subtopic': 'vsan'
    },
    'zone_list': {
        'func': zone_list,
        'description': 'Batch query zone',
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
        'description': 'Batch create zone',
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
        'description': 'Batch query别名',
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


