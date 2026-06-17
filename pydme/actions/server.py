"""
Server management related operations
"""

import sys
import os

from pydme.client import DMEAPIClient


def list(client: DMEAPIClient, start: int = 1, limit: int = 100,
         name: str = None, server_type: str = None) -> dict:
    """
    Query server list
    
    Args:
        client: DME API client
        start: Pagination start position, default 1
        limit: Page size, default 100
        name: Server name filter (Optional)
        server_type: Server type filter (Optional)
    
    Returns:
        {
            total: Total servers (integer),
            servers: Server list (List<ServerInfo>). parameter format: [{
                id: Server ID (string),
                name: Server name (string),
                type: Server type (string),
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
    Query overview info of a specified server
    
    Args:
        client: DME API client
        server_id: Server ID (Note: must use the device_id field, which is a UUID with hyphens, e.g. 507cb27f-3eda-44c8-a491-5a81ca035da5)
    
    Returns:
        {
            id: Server ID (string),
            name: Server name (string),
            status: status (string),
            type: Server type (string),
        }
    """
    url = "/rest/servermgmt/v1/servers/{server_id}/summary"
    
    response = client.get(url, params={"server_id": server_id})
    return response


def cpu_list(client: DMEAPIClient, server_id: str,
                   start: int = 1, limit: int = 100) -> dict:
    """
    Query all CPU list on a server

    Args:
        client: DME API client
        server_id: Server ID
        start: Pagination start position, default 1
        limit: Page size, default 100

    Returns:
        {
            total: CPU count (int32),
            cpus: CPU list (List<CpuInfo>). parameter format: [{
                id: CPU ID (string),
                name: name (string),
                cores: Core count (int32),
                frequency: Frequency (string),
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
    Query memory on a server
    
    Args:
        client: DME API client
        server_id: Server ID
        start: Pagination start position, default 1
        limit: Page size, default 100
    
    Returns:
        {
            total: Memory module count (int32),
            memories: Memory list (List<MemoryInfo>). parameter format: [{
                id: Memory ID (string),
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
    Query disk collection on a server
    
    Args:
        client: DME API client
        server_id: Server ID
        start: Pagination start position, default 1
        limit: Page size, default 100
    
    Returns:
        {
            total: Disk count (int32),
            disks: Disk list (List<DiskInfo>). parameter format: [{
                id: Disk ID (string),
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
    Query NIC collection on a server

    Args:
        client: DME API client
        server_id: Server ID (Optional)
        page_no: Pagination query page number, default 1
        page_size: items per page, 5~1000, default 20

    Returns:
        {
            total: NIC count (int32),
            nics: NIC list (List<NicInfo>). parameter format: [{
                id: NIC ID (string),
                name: name (string),
                mac: MAC address (string),
                speed: Speed (string),
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
    Query fans on a server
    
    Args:
        client: DME API client
        server_id: Server ID
        start: Pagination start position, default 1
        limit: Page size, default 100
    
    Returns:
        {
            total: Fan count (int32),
            fans: Fan list (List<FanInfo>). parameter format: [{
                id: Fan ID (string),
                name: name (string),
                speed: Rotation speed (string),
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
    Query power supplies on a server
    
    Args:
        client: DME API client
        server_id: Server ID
        start: Pagination start position, default 1
        limit: Page size, default 100
    
    Returns:
        {
            total: Power supply count (int32),
            powers: Power supply list (List<PowerInfo>). parameter format: [{
                id: Power supply ID (string),
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
    Query RAID card details on a server
    
    Args:
        client: DME API client
        server_id: Server ID
        start: Pagination start position, default 1
        limit: Page size, default 100
    
    Returns:
        {
            total: RAID card count (int32),
            raid_cards: RAID card list (List<RaidCardInfo>). parameter format: [{
                id: RAID card ID (string),
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
    Query PCIe card info on a server
    
    Args:
        client: DME API client
        server_id: Server ID
        start: Pagination start position, default 1
        limit: Page size, default 100
    
    Returns:
        {
            total: PCIe card count (int32),
            pcie_cards: PCIe card list (List<PcieCardInfo>). parameter format: [{
                id: PCIe card ID (string),
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
    # Direct actions (two-level structure)
    'list': {
        'func': list,
        'description': 'Query server list',
        'params': ['start', 'limit', 'name', 'server_type'],
        'subtopic': None
    },
    'show': {
        'func': show,
        'description': 'Query overview info of specified server',
        'params': ['server_id'],
        'subtopic': None
    },
    # subtopic action - cpu (three-level structure)
    'cpu_list': {
        'func': cpu_list,
        'description': 'Query all CPU list on server',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'cpu'
    },
    # subtopic action - memory (three-level structure)
    'memory_list': {
        'func': memory_list,
        'description': 'Query memory on server',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'memory'
    },
    # subtopic action - disk (three-level structure)
    'disk_list': {
        'func': disk_list,
        'description': 'Query disk collection on server',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'disk'
    },
    # subtopic action - nic (three-level structure)
    'nic_list': {
        'func': nic_list,
        'description': 'Query NIC collection on server',
        'params': ['server_id', 'page_no', 'page_size'],
        'subtopic': 'nic'
    },
    # subtopic action - fan (three-level structure)
    'fan_list': {
        'func': fan_list,
        'description': 'Query fans on server',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'fan'
    },
    # subtopic action - power (three-level structure)
    'power_list': {
        'func': power_list,
        'description': 'Query power supplies on server',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'power'
    },
    # subtopic action - raid_card (three-level structure)
    'raid_card_list': {
        'func': raid_card_list,
        'description': 'Query RAID card details on server',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'raid_card'
    },
    # subtopic action - pcie_card (three-level structure)
    'pcie_card_list': {
        'func': pcie_card_list,
        'description': 'Query PCIe card info on server',
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'pcie_card'
    },
}
