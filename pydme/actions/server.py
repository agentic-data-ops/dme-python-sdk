"""
服务器管理 (Server) operations
"""

import sys
import os

from pydme.client import DMEAPIClient


def list(client: DMEAPIClient, start: int = 1, limit: int = 100,
         name: str = None, server_type: str = None) -> dict:
    """
    查询Server list
    
    Args:
        client: DME API client
        start: 分页Start position，默认 1
        limit: Page size, default 100
        name: 服务器名称过滤（Optional）
        server_type: 服务器类型过滤（Optional）
    
    Returns:
        {
            total: 服务器Total count (integer),
            servers: Server list (List<ServerInfo>)。参数格式如下：[{
                id: 服务器ID (string),
                name: 服务器名称 (string),
                type: 服务器类型 (string),
                status: 状态 (string),
            }, ...],
        }
    """
    url = "/rest/servermgmt/v1/servers/query"
    
    payload = {
        'start': start,
        'limit': limit
    }
    
    if name is not None:
        payload['name'] = name
    if server_type is not None:
        payload['server_type'] = server_type
    
    response = client.post(url, body=payload)
    return response


def show(client: DMEAPIClient, server_id: str) -> dict:
    """
    Query服务器的概览信息
    
    Args:
        client: DME API client
        server_id: 服务器 ID（注意：需要使用 device_id 字段，即带连字符的 UUID 格式，如 507cb27f-3eda-44c8-a491-5a81ca035da5）
    
    Returns:
        {
            id: 服务器ID (string),
            name: 服务器名称 (string),
            status: 状态 (string),
            type: 服务器类型 (string),
        }
    """
    url = "/rest/servermgmt/v1/servers/{server_id}/summary"
    
    response = client.get(url, params={"server_id": server_id})
    return response


def cpu_list(client: DMEAPIClient, server_id: str,
                   start: int = 1, limit: int = 100) -> dict:
    """
    查询服务器上的所有 CPU 列表

    Args:
        client: DME API client
        server_id: 服务器 ID
        start: 分页Start position，默认 1
        limit: Page size, default 100

    Returns:
        CPU 列表
    """
    url = "/rest/servermgmt/v1/processors/query"

    payload = {
        'server_id': server_id,
        'start': start,
        'limit': limit
    }

    response = client.post(url, body=payload)
    return response


def memory_list(client: DMEAPIClient, server_id: str,
                 start: int = 1, limit: int = 100) -> dict:
    """
    查询服务器上的内存
    
    Args:
        client: DME API client
        server_id: 服务器 ID
        start: 分页Start position，默认 1
        limit: Page size, default 100
    
    Returns:
        内存列表
    """
    url = "/rest/servermgmt/v1/memories/query"
    
    payload = {
        'server_id': server_id,
        'start': start,
        'limit': limit
    }
    
    response = client.post(url, body=payload)
    return response


def disk_list(client: DMEAPIClient, server_id: str,
                    start: int = 1, limit: int = 100) -> dict:
    """
    查询服务器上的硬盘集合
    
    Args:
        client: DME API client
        server_id: 服务器 ID
        start: 分页Start position，默认 1
        limit: Page size, default 100
    
    Returns:
        硬盘列表
    """
    url = "/rest/servermgmt/v1/disks/query"
    
    payload = {
        'server_id': server_id,
        'start': start,
        'limit': limit
    }
    
    response = client.post(url, body=payload)
    return response


def nic_list(client: DMEAPIClient, server_id: str = None,
                   page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询服务器上的网卡集合

    Args:
        client: DME API client
        server_id: 服务器 ID（Optional）
        page_no: Page number，默认 1
        page_size: 每页数量，5~1000，默认 20

    Returns:
        网卡列表
    """
    url = "/rest/servermgmt/v1/network-adapters/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if server_id is not None:
        payload['server_id'] = server_id

    response = client.post(url, body=payload)
    return response


def fan_list(client: DMEAPIClient, server_id: str,
                   start: int = 1, limit: int = 100) -> dict:
    """
    查询服务器上的风扇
    
    Args:
        client: DME API client
        server_id: 服务器 ID
        start: 分页Start position，默认 1
        limit: Page size, default 100
    
    Returns:
        风扇列表
    """
    url = "/rest/servermgmt/v1/fans/query"
    
    payload = {
        'server_id': server_id,
        'start': start,
        'limit': limit
    }
    
    response = client.post(url, body=payload)
    return response


def power_list(client: DMEAPIClient, server_id: str,
                     start: int = 1, limit: int = 100) -> dict:
    """
    查询服务器上的电源
    
    Args:
        client: DME API client
        server_id: 服务器 ID
        start: 分页Start position，默认 1
        limit: Page size, default 100
    
    Returns:
        电源列表
    """
    url = "/rest/servermgmt/v1/powers/query"
    
    payload = {
        'server_id': server_id,
        'start': start,
        'limit': limit
    }
    
    response = client.post(url, body=payload)
    return response


def raid_card_list(client: DMEAPIClient, server_id: str,
                    start: int = 1, limit: int = 100) -> dict:
    """
    查询服务器上的 RAID 卡详情
    
    Args:
        client: DME API client
        server_id: 服务器 ID
        start: 分页Start position，默认 1
        limit: Page size, default 100
    
    Returns:
        RAID 卡列表
    """
    url = "/rest/servermgmt/v1/raid-cards/query"
    
    payload = {
        'server_id': server_id,
        'start': start,
        'limit': limit
    }
    
    response = client.post(url, body=payload)
    return response


def pcie_card_list(client: DMEAPIClient, server_id: str,
                    start: int = 1, limit: int = 100) -> dict:
    """
    查询服务器上的 PCIe 卡信息
    
    Args:
        client: DME API client
        server_id: 服务器 ID
        start: 分页Start position，默认 1
        limit: Page size, default 100
    
    Returns:
        PCIe 卡列表
    """
    url = "/rest/servermgmt/v1/pcies/query"
    
    payload = {
        'server_id': server_id,
        'start': start,
        'limit': limit
    }
    
    response = client.post(url, body=payload)
    return response


# Action list for CLI help
ACTIONS = {
    # 直接动作（两级结构）
    'list': {
        'func': list,
        'description': '查询Server list',
        'params': ['start', 'limit', 'name', 'server_type'],
        'subtopic': None
    },
    'show': {
        'func': show,
        'description': 'Query服务器的概览信息',
        'params': ['server_id'],
        'subtopic': None
    },
    # 子主题动作 - cpu (three-level structure)
    'cpu_list': {
        'func': cpu_list,
        'description': '查询服务器上的所有 CPU 列表',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'cpu'
    },
    # 子主题动作 - memory (three-level structure)
    'memory_list': {
        'func': memory_list,
        'description': '查询服务器上的内存',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'memory'
    },
    # 子主题动作 - disk (three-level structure)
    'disk_list': {
        'func': disk_list,
        'description': '查询服务器上的硬盘集合',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'disk'
    },
    # 子主题动作 - nic (three-level structure)
    'nic_list': {
        'func': nic_list,
        'description': '查询服务器上的网卡集合',
        'params': ['server_id', 'page_no', 'page_size'],
        'subtopic': 'nic'
    },
    # 子主题动作 - fan (three-level structure)
    'fan_list': {
        'func': fan_list,
        'description': '查询服务器上的风扇',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'fan'
    },
    # 子主题动作 - power (three-level structure)
    'power_list': {
        'func': power_list,
        'description': '查询服务器上的电源',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'power'
    },
    # 子主题动作 - raid_card (three-level structure)
    'raid_card_list': {
        'func': raid_card_list,
        'description': '查询服务器上的 RAID 卡详情',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'raid_card'
    },
    # 子主题动作 - pcie_card (three-level structure)
    'pcie_card_list': {
        'func': pcie_card_list,
        'description': '查询服务器上的 PCIe 卡信息',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'pcie_card'
    },
}
