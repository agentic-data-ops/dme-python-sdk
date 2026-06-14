"""
Servermanagement  (Server) operations
"""

import sys
import os

from pydme.client import DMEAPIClient


def list(client: DMEAPIClient, start: int = 1, limit: int = 100,
         name: str = None, server_type: str = None) -> dict:
    """
     queryServer list
    
    Args:
        client: DME API client
        start: 分页Start position，default 1
        limit: Page size, default 100
        name: Server name filter（Optional）
        server_type: Server type filter（Optional）
    
    Returns:
        {
            total: ServerTotal count (integer),
            servers: Server list (List<ServerInfo>)。 parameter format如下：[{
                id: ServerID (string),
                name: Server name (string),
                type: Server type (string),
                status:  status (string),
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
    QueryServer overview info
    
    Args:
        client: DME API client
        server_id: Server ID（注意：需要使用 device_id  field，with hyphens UUID  format，如 507cb27f-3eda-44c8-a491-5a81ca035da5）
    
    Returns:
        {
            id: ServerID (string),
            name: Server name (string),
            status:  status (string),
            type: Server type (string),
        }
    """
    url = "/rest/servermgmt/v1/servers/{server_id}/summary"
    
    response = client.get(url, params={"server_id": server_id})
    return response


def cpu_list(client: DMEAPIClient, server_id: str,
                   start: int = 1, limit: int = 100) -> dict:
    """
    Query on server所有 CPU  list

    Args:
        client: DME API client
        server_id: Server ID
        start: 分页Start position，default 1
        limit: Page size, default 100

    Returns:
        CPU  list
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
    Query on server内存
    
    Args:
        client: DME API client
        server_id: Server ID
        start: 分页Start position，default 1
        limit: Page size, default 100
    
    Returns:
        内存 list
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
    Query on server硬盘集合
    
    Args:
        client: DME API client
        server_id: Server ID
        start: 分页Start position，default 1
        limit: Page size, default 100
    
    Returns:
        硬盘 list
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
    Query on server网卡集合

    Args:
        client: DME API client
        server_id: Server ID（Optional）
        page_no: Page number，default 1
        page_size: per pagecount，5~1000，default 20

    Returns:
        网卡 list
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
    Query on serverFan
    
    Args:
        client: DME API client
        server_id: Server ID
        start: 分页Start position，default 1
        limit: Page size, default 100
    
    Returns:
        Fan list
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
    Query on serverPower supply
    
    Args:
        client: DME API client
        server_id: Server ID
        start: 分页Start position，default 1
        limit: Page size, default 100
    
    Returns:
        Power supply list
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
    Query on server RAID 卡 details
    
    Args:
        client: DME API client
        server_id: Server ID
        start: 分页Start position，default 1
        limit: Page size, default 100
    
    Returns:
        RAID 卡 list
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
    Query on server PCIe 卡 info
    
    Args:
        client: DME API client
        server_id: Server ID
        start: 分页Start position，default 1
        limit: Page size, default 100
    
    Returns:
        PCIe 卡 list
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
    # Direct action（Two-level structure）
    'list': {
        'func': list,
        'description': ' queryServer list',
        'params': ['start', 'limit', 'name', 'server_type'],
        'subtopic': None
    },
    'show': {
        'func': show,
        'description': 'QueryServer overview info',
        'params': ['server_id'],
        'subtopic': None
    },
    # subtopic actions - cpu (three-level structure)
    'cpu_list': {
        'func': cpu_list,
        'description': 'Query on server所有 CPU  list',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'cpu'
    },
    # subtopic actions - memory (three-level structure)
    'memory_list': {
        'func': memory_list,
        'description': 'Query on server内存',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'memory'
    },
    # subtopic actions - disk (three-level structure)
    'disk_list': {
        'func': disk_list,
        'description': 'Query on server硬盘集合',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'disk'
    },
    # subtopic actions - nic (three-level structure)
    'nic_list': {
        'func': nic_list,
        'description': 'Query on server网卡集合',
        'params': ['server_id', 'page_no', 'page_size'],
        'subtopic': 'nic'
    },
    # subtopic actions - fan (three-level structure)
    'fan_list': {
        'func': fan_list,
        'description': 'Query on serverFan',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'fan'
    },
    # subtopic actions - power (three-level structure)
    'power_list': {
        'func': power_list,
        'description': 'Query on serverPower supply',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'power'
    },
    # subtopic actions - raid_card (three-level structure)
    'raid_card_list': {
        'func': raid_card_list,
        'description': 'Query on server RAID 卡 details',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'raid_card'
    },
    # subtopic actions - pcie_card (three-level structure)
    'pcie_card_list': {
        'func': pcie_card_list,
        'description': 'Query on server PCIe 卡 info',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'pcie_card'
    },
}
