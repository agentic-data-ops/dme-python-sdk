"""
服务器管理 (Server) 相关操作
"""

import sys
import os

from pydme.client import DMEAPIClient


def list(client: DMEAPIClient, start: int = 1, limit: int = 100,
         name: str = None, server_type: str = None) -> dict:
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
    url = "/rest/servermgmt/v1/servers/{server_id}/summary"
    
    response = client.get(url, params={"server_id": server_id})
    return response


def cpu_list(client: DMEAPIClient, server_id: str,
                   start: int = 1, limit: int = 100) -> dict:
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
        'params': ['start', 'limit', 'name', 'server_type'],
        'subtopic': None
    },
    'show': {
        'func': show,
        'params': ['server_id'],
        'subtopic': None
    },
    # 子主题动作 - cpu（三级结构）
    'cpu_list': {
        'func': cpu_list,
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'cpu'
    },
    # 子主题动作 - memory（三级结构）
    'memory_list': {
        'func': memory_list,
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'memory'
    },
    # 子主题动作 - disk（三级结构）
    'disk_list': {
        'func': disk_list,
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'disk'
    },
    # 子主题动作 - nic（三级结构）
    'nic_list': {
        'func': nic_list,
        'params': ['server_id', 'page_no', 'page_size'],
        'subtopic': 'nic'
    },
    # 子主题动作 - fan（三级结构）
    'fan_list': {
        'func': fan_list,
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'fan'
    },
    # 子主题动作 - power（三级结构）
    'power_list': {
        'func': power_list,
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'power'
    },
    # 子主题动作 - raid_card（三级结构）
    'raid_card_list': {
        'func': raid_card_list,
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'raid_card'
    },
    # 子主题动作 - pcie_card（三级结构）
    'pcie_card_list': {
        'func': pcie_card_list,
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'pcie_card'
    },
}
