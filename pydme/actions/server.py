"""
服务器管理 (Server) 相关操作
"""

import sys
import os

from pydme.client import DMEAPIClient


def list(client: DMEAPIClient, start: int = 1, limit: int = 100,
         name: str = None, server_type: str = None) -> dict:
    """
    查询服务器列表
    
    Args:
        client: DME API client
        start: 分页起始位置，默认 1
        limit: 分页数量，默认 100
        name: 服务器名称过滤（Optional）
        server_type: 服务器类型过滤（Optional）
    
    Returns:
        {
            total: 服务器总数 (integer),
            servers: 服务器列表 (List<ServerInfo>)。参数格式如下：[{
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
    查询指定服务器的概览信息
    
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
        start: 分页起始位置，默认 1
        limit: 分页数量，默认 100

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
        start: 分页起始位置，默认 1
        limit: 分页数量，默认 100
    
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
        start: 分页起始位置，默认 1
        limit: 分页数量，默认 100
    
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
        page_no: 分页查询的页码，默认 1
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
        start: 分页起始位置，默认 1
        limit: 分页数量，默认 100
    
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
        start: 分页起始位置，默认 1
        limit: 分页数量，默认 100
    
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
        start: 分页起始位置，默认 1
        limit: 分页数量，默认 100
    
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
        start: 分页起始位置，默认 1
        limit: 分页数量，默认 100
    
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


# 动作列表，用于 CLI 帮助
ACTIONS = {
    # 直接动作（两级结构）
    'list': {
        'func': list,
        'description': '查询服务器列表',
        'params': ['start', 'limit', 'name', 'server_type'],
        'subtopic': None
    },
    'show': {
        'func': show,
        'description': '查询指定服务器的概览信息',
        'params': ['server_id'],
        'subtopic': None
    },
    # 子主题动作 - cpu（三级结构）
    'cpu_list': {
        'func': cpu_list,
        'description': '查询服务器上的所有 CPU 列表',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'cpu'
    },
    # 子主题动作 - memory（三级结构）
    'memory_list': {
        'func': memory_list,
        'description': '查询服务器上的内存',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'memory'
    },
    # 子主题动作 - disk（三级结构）
    'disk_list': {
        'func': disk_list,
        'description': '查询服务器上的硬盘集合',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'disk'
    },
    # 子主题动作 - nic（三级结构）
    'nic_list': {
        'func': nic_list,
        'description': '查询服务器上的网卡集合',
        'params': ['server_id', 'page_no', 'page_size'],
        'subtopic': 'nic'
    },
    # 子主题动作 - fan（三级结构）
    'fan_list': {
        'func': fan_list,
        'description': '查询服务器上的风扇',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'fan'
    },
    # 子主题动作 - power（三级结构）
    'power_list': {
        'func': power_list,
        'description': '查询服务器上的电源',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'power'
    },
    # 子主题动作 - raid_card（三级结构）
    'raid_card_list': {
        'func': raid_card_list,
        'description': '查询服务器上的 RAID 卡详情',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'raid_card'
    },
    # 子主题动作 - pcie_card（三级结构）
    'pcie_card_list': {
        'func': pcie_card_list,
        'description': '查询服务器上的 PCIe 卡信息',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'pcie_card'
    },
}
