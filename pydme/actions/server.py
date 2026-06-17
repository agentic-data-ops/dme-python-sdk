"""
服务器管理 (Server) 相关操作
"""

import sys
import os

from pydme.client import DMEAPIClient


def list(client: DMEAPIClient, start: int = 1, limit: int = 100,
         name: str = None, server_type: str = None) -> dict:
    """
    query服务器list
    
    Args:
        client: DME API client
        start: 分页起始location, default 1
        limit: 分页count, default 100
        name: 服务器name过滤(Optional)
        server_type: 服务器type过滤(Optional)
    
    Returns:
        {
            total: 服务器total (integer),
            servers: 服务器list (List<ServerInfo>). parameter format: [{
                id: 服务器ID (string),
                name: 服务器name (string),
                type: 服务器type (string),
                status: status (string),
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
    query指定服务器的概览info
    
    Args:
        client: DME API client
        server_id: 服务器 ID (注意: 需要使用 device_id 字段, 即带连字符的 UUID 格式, 如 507cb27f-3eda-44c8-a491-5a81ca035da5)
    
    Returns:
        {
            id: 服务器ID (string),
            name: 服务器name (string),
            status: status (string),
            type: 服务器type (string),
        }
    """
    url = "/rest/servermgmt/v1/servers/{server_id}/summary"
    
    response = client.get(url, params={"server_id": server_id})
    return response


def cpu_list(client: DMEAPIClient, server_id: str,
                   start: int = 1, limit: int = 100) -> dict:
    """
    query服务器上的所有 CPU list

    Args:
        client: DME API client
        server_id: 服务器 ID
        start: 分页起始location, default 1
        limit: 分页count, default 100

    Returns:
        {
            total: CPUcount (int32),
            cpus: CPUlist (List<CpuInfo>). parameter format: [{
                id: CPU ID (string),
                name: name (string),
                cores: 核数 (int32),
                frequency: 频率 (string),
            }, ...],
        }
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
    query服务器上的内存
    
    Args:
        client: DME API client
        server_id: 服务器 ID
        start: 分页起始location, default 1
        limit: 分页count, default 100
    
    Returns:
        {
            total: 内存条count (int32),
            memories: 内存list (List<MemoryInfo>). parameter format: [{
                id: 内存ID (string),
                name: name (string),
                capacity: capacity (string),
            }, ...],
        }
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
    query服务器上的硬盘集合
    
    Args:
        client: DME API client
        server_id: 服务器 ID
        start: 分页起始location, default 1
        limit: 分页count, default 100
    
    Returns:
        {
            total: 硬盘count (int32),
            disks: 硬盘list (List<DiskInfo>). parameter format: [{
                id: 硬盘ID (string),
                name: name (string),
                capacity: capacity (string),
                health_status: health status (string),
            }, ...],
        }
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
    query服务器上的网卡集合

    Args:
        client: DME API client
        server_id: 服务器 ID(Optional)
        page_no: 分页query的页码, default 1
        page_size: items per page, 5~1000, default 20

    Returns:
        {
            total: 网卡count (int32),
            nics: 网卡list (List<NicInfo>). parameter format: [{
                id: 网卡ID (string),
                name: name (string),
                mac: MAC地址 (string),
                speed: 速率 (string),
            }, ...],
        }
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
    query服务器上的风扇
    
    Args:
        client: DME API client
        server_id: 服务器 ID
        start: 分页起始location, default 1
        limit: 分页count, default 100
    
    Returns:
        {
            total: 风扇count (int32),
            fans: 风扇list (List<FanInfo>). parameter format: [{
                id: 风扇ID (string),
                name: name (string),
                speed: 转速 (string),
                health_status: health status (string),
            }, ...],
        }
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
    query服务器上的电源
    
    Args:
        client: DME API client
        server_id: 服务器 ID
        start: 分页起始location, default 1
        limit: 分页count, default 100
    
    Returns:
        {
            total: 电源count (int32),
            powers: 电源list (List<PowerInfo>). parameter format: [{
                id: 电源ID (string),
                name: name (string),
                status: status (string),
                health_status: health status (string),
            }, ...],
        }
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
    query服务器上的 RAID 卡details
    
    Args:
        client: DME API client
        server_id: 服务器 ID
        start: 分页起始location, default 1
        limit: 分页count, default 100
    
    Returns:
        {
            total: RAID卡count (int32),
            raid_cards: RAID卡list (List<RaidCardInfo>). parameter format: [{
                id: RAID卡ID (string),
                name: name (string),
                model: model (string),
            }, ...],
        }
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
    query服务器上的 PCIe 卡info
    
    Args:
        client: DME API client
        server_id: 服务器 ID
        start: 分页起始location, default 1
        limit: 分页count, default 100
    
    Returns:
        {
            total: PCIe卡count (int32),
            pcie_cards: PCIe卡list (List<PcieCardInfo>). parameter format: [{
                id: PCIe卡ID (string),
                name: name (string),
                type: type (string),
            }, ...],
        }
    """
    url = "/rest/servermgmt/v1/pcies/query"
    
    payload = {
        'server_id': server_id,
        'start': start,
        'limit': limit
    }
    
    response = client.post(url, body=payload)
    return response


# action list, for CLI help
ACTIONS = {
    # 直接动作 (两级结构)
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
    # subtopic action - cpu (three-level structure)
    'cpu_list': {
        'func': cpu_list,
        'description': '查询服务器上的所有 CPU 列表',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'cpu'
    },
    # subtopic action - memory (three-level structure)
    'memory_list': {
        'func': memory_list,
        'description': '查询服务器上的内存',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'memory'
    },
    # subtopic action - disk (three-level structure)
    'disk_list': {
        'func': disk_list,
        'description': '查询服务器上的硬盘集合',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'disk'
    },
    # subtopic action - nic (three-level structure)
    'nic_list': {
        'func': nic_list,
        'description': '查询服务器上的网卡集合',
        'params': ['server_id', 'page_no', 'page_size'],
        'subtopic': 'nic'
    },
    # subtopic action - fan (three-level structure)
    'fan_list': {
        'func': fan_list,
        'description': '查询服务器上的风扇',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'fan'
    },
    # subtopic action - power (three-level structure)
    'power_list': {
        'func': power_list,
        'description': '查询服务器上的电源',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'power'
    },
    # subtopic action - raid_card (three-level structure)
    'raid_card_list': {
        'func': raid_card_list,
        'description': '查询服务器上的 RAID 卡详情',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'raid_card'
    },
    # subtopic action - pcie_card (three-level structure)
    'pcie_card_list': {
        'func': pcie_card_list,
        'description': '查询服务器上的 PCIe 卡信息',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'pcie_card'
    },
}
