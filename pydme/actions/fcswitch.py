"""
FC Switch (Fibre Channel switch) operations
"""

import sys
import os

from pydme.client import DMEAPIClient


def list(client: DMEAPIClient, name: str = None, 
                  page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch querySwitch
    
    Args:
        client: DME API client
        name: Switch name（Optional，supports fuzzy search）
        page_no: Page number，默认 1
        page_size: 每页count，1~1000，默认 20
    
    Returns:
        {
            total: Total count (integer),
            fcswitches: Switch list (List<FcSwitchInfo>)。参数格式如下：[{
                id: SwitchID (string),
                name: Switch name (string),
                status: Running status (string),
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
    Sync指定Switch
    
    Args:
        client: DME API client
        switch_id: Switch ID（Required）
    
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
    Batch querySwitch port
    
    Args:
        client: DME API client
        switch_id: Switch ID（Optional）
        port_name: Port name（Optional）
        page_no: Page number，默认 1
        page_size: 每页count，1~1000，默认 20
    
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
    Batch querySwitch control processor
    
    Args:
        client: DME API client
        switch_id: Switch ID（Optional）
        page_no: Page number，默认 1
        page_size: 每页count，1~1000，默认 20
    
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
    Batch queryFibre Channel network
    
    Args:
        client: DME API client
        name: FC network name（Optional，supports fuzzy search）
        page_no: Page number，默认 1
        page_size: 每页count，1~1000，默认 20
    
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
    QueryFC network port list

    Args:
        client: DME API client
        fabric_id: Fibre Channel network ID（Required）
        page_no: Page number，默认 1
        page_size: 每页count，1~1000，默认 20

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
    执行Fibre Channel network配置文件备份
    
    Args:
        client: DME API client
        fabric_id: Fibre Channel network ID（Required）
        backup_server_id: Backup server ID（Required）
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
        page_no: Page number，默认 1
        page_size: 每页count，1~1000，默认 20
    
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
        fabric_wwn: Fibre Channel network WWN（Optional），1~1024 个字符
        name: Zone 名称（Optional），supports fuzzy search，1~1024 个字符
        cfg_name: 所属 CFG 名称（Optional），supports fuzzy search，0~1024 个字符
        zone_set: 所属 Zone 集合（Optional），supports fuzzy search，0~1024 个字符
        active_status: Zone 状态列表（Optional），max array members：2
        member_count: 成员count（Optional），0~2147483647
        sort_key: Sort field（Optional），支持 member_count
        sort_dir: Sort direction（Optional），asc：升序；desc：降序
        page_no: Page number（Optional），1~65535
        page_size: 每页count（Optional），1~1000

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

    注：根据 DME API 文档，需要提供 fabric_wwn 或 vsan_wwn，and at least one member type。

    Args:
        client: DME API client
        name: Zone 名称（Required）
        fabric_wwn: Fibre Channel network WWN（条件Required，fabric 创建 zone 时需要）
        vsan_wwn: VSAN WWN（条件Required，vsan 创建 zone 时需要）
        wwn_members: WWN Member list（Optional），格式：["<wwn>",...]
        port_members: Port member list（Optional），格式：[{"domain_id":"<domainId>","port_index":"<portIndex>","port_name":"portName"},...]，Brocade switch: specifyport_index，Cisco switch: specifyport_name
        fwwn_members: FWWN Member list（Optional），格式：["<fwwn>",...]
        fcid_members: FCID Member list（Optional），格式：["<fcid>",...]
        alias_members: Alias member list（Optional），格式：["<alias>",...]
        device_alias_members: Device alias member list（Optional），格式：["<deviceAlias>",...]

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }，includes newly created Zone ID
    """
    url = "/rest/fcswitchmgmt/v1/zones"

    payload = {
        'name': name
    }

    # fabric_wwn 或 vsan_wwn provide at least one
    if fabric_wwn is not None:
        payload['fabric_wwn'] = fabric_wwn
    if vsan_wwn is not None:
        payload['vsan_wwn'] = vsan_wwn

    # Member list
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
        alias_members: Alias member modification（Optional），格式：{"added_members": ["<alias>",...], "removed_members": ["<alias>",...]}
        fwwn_members: FWWN 成员修改（Optional），格式：{"added_members": ["<fwwn>",...], "removed_members": ["<fwwn>",...]}
        port_members: Port member modification（Optional），格式：{"added_members": [{"domain_id":"<domainId>","port_index":"<portIndex>","port_name":"portName"},...], "removed_members": [{"domain_id":"<domainId>","port_index":"<portIndex>","port_name":"portName"},...]}，Brocade switch: specifyport_index，Cisco switch: specifyport_name
        fcid_members: FCID 成员修改（Optional），格式：{"added_members": ["<fcid>",...], "removed_members": ["<fcid>",...]}
        device_alias_members: Device alias member modification（Optional），格式：{"added_members": ["<deviceAlias>",...], "removed_members": ["<deviceAlias>",...]}

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
        is_active_zone: 是否激活 Zone（Required，string "true" 或 "false"）
        zones: Zone 配置列表，每个元素应包含:
            - fabric_wwn: Fibre Channel network WWN（Required）
            - name: Zone 名称（Required）
            - wwn_members: WWN Member list（Optional），格式：["<wwn>",...]
            - port_members: Port member list（Optional），格式：[{"domain_id":"<domainId>","port_index":"<portIndex>","port_name":"portName"},...]，Brocade switch: specifyport_index，Cisco switch: specifyport_name
            - fwwn_members: FWWN Member list（Optional），格式：["<fwwn>",...]
            - fcid_members: FCID Member list（Optional），格式：["<fcid>",...]
            - alias_members: Alias member list（Optional），格式：["<alias>",...]
            - device_alias_members: Device alias member list（Optional），格式：["<deviceAlias>",...]

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

    查询 Zone members contained in，支持端口成员、WWN members and alias members。

    Args:
        client: DME API client
        zone_id: Zone ID（Required）
        type: 成员类型，Optional值：port（端口成员）,wwn（WWN 成员）,alias（别名成员）。
             returns all member types if not specified

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }，Includes member list
    """
    result = {'port_members': [], 'wwn_members': [], 'alias_members': []}

    # 根据 type parameter to query matching member type
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

    # if specified type，returns only matching member type
    if type == 'port':
        return {'port_members': result['port_members']}
    elif type == 'wwn':
        return {'wwn_members': result['wwn_members']}
    elif type == 'alias':
        return {'alias_members': result['alias_members']}
    else:
        # returns all members
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
        fabric_wwn: Fibre Channel network WWN（Required）
        page_no: Page number，默认 1
        page_size: 每页count，1~1000，默认 20
    
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

    注：根据 DME API 文档，需要提供 fabric_wwn 或 vsan_wwn，and at least one member type。

    Args:
        client: DME API client
        name: Alias 名称（Required）
        fabric_wwn: Fibre Channel network WWN（条件Required，fabric Alias creation requires）
        vsan_wwn: VSAN WWN（条件Required，vsan Alias creation requires）
        wwn_members: WWN Member list（Optional，思科Switch PWWN 成员）
        port_members: Port member list（Optional）
        fwwn_members: FWWN Member list（Optional）
        fcid_members: FCID Member list（Optional）
        device_alias_members: Device alias member list（Optional）
    
    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }，includes newly created Alias ID
    """
    url = "/rest/fcswitchmgmt/v1/aliases"
    
    payload = {
        'name': name
    }
    
    # fabric_wwn 或 vsan_wwn provide at least one
    if fabric_wwn is not None:
        payload['fabric_wwn'] = fabric_wwn
    if vsan_wwn is not None:
        payload['vsan_wwn'] = vsan_wwn
    
    # Member list
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

    注：根据 DME API 文档，member modification requires {type}.added_members 和 {type}.removed_members 格式。

    Args:
        client: DME API client
        alias_id: Alias ID（Required）
        name: Alias 名称（Optional）
        wwn_members: WWN 成员修改（Optional，格式：{'added_members': [...], 'removed_members': [...]}）
        fwwn_members: FWWN 成员修改（Optional）
        port_members: Port member modification（Optional）
        fcid_members: FCID 成员修改（Optional）
        device_alias_members: Device alias member modification（Optional）
    
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
    Query alias members

    查询 Alias members contained in，支持查询端口成员和 WWN 成员。

    Args:
        client: DME API client
        alias_id: Alias ID（Required）
        type: 成员类型，Optional值：port（端口成员）,wwn（WWN 成员）。
             returns all member types if not specified

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }，Includes member list
    """
    result = {'port_members': [], 'wwn_members': []}

    # if specified type 或默认为 None 时，查询对应类型的成员
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

    # if specified type，returns only matching member type
    if type == 'port':
        return {'port_members': result['port_members']}
    elif type == 'wwn':
        return {'wwn_members': result['wwn_members']}
    else:
        # returns all members
        all_members = result['port_members'] + result['wwn_members']
        return {'members': all_members}


# ACTIONS 字典，Define all available actions
ACTIONS = {
    'list': {
        'func': list,
        'description': 'Batch queryFibre Channel switch',
        'params': ['name', 'page_no', 'page_size'],
        'subtopic': None
    },
    'sync': {
        'func': sync,
        'description': 'SyncSwitch配置',
        'params': ['switch_id'],
        'subtopic': None
    },
    'port_list': {
        'func': port_list,
        'description': '查询Switch port列表',
        'params': ['switch_id', 'port_name', 'page_no', 'page_size'],
        'subtopic': 'port'
    },
    'controller_list': {
        'func': controller_list,
        'description': '查询Switch控制器列表',
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
        'description': 'Query alias members',
        'params': ['alias_id', 'type'],
        'subtopic': 'alias'
    },
}


