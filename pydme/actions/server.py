"""
Server management (Server) related operations
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


# Action list for CLI help
ACTIONS = {
    # Direct actions (two-level structure)
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
    # Subtopic actions - cpu (three-level structure)
    'cpu_list': {
        'func': cpu_list,
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'cpu'
    },
    # Subtopic actions - memory (three-level structure)
    'memory_list': {
        'func': memory_list,
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'memory'
    },
    # Subtopic actions - disk (three-level structure)
    'disk_list': {
        'func': disk_list,
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'disk'
    },
    # Subtopic actions - nic (three-level structure)
    'nic_list': {
        'func': nic_list,
        'params': ['server_id', 'page_no', 'page_size'],
        'subtopic': 'nic'
    },
    # Subtopic actions - fan (three-level structure)
    'fan_list': {
        'func': fan_list,
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'fan'
    },
    # Subtopic actions - power (three-level structure)
    'power_list': {
        'func': power_list,
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'power'
    },
    # Subtopic actions - raid_card (three-level structure)
    'raid_card_list': {
        'func': raid_card_list,
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'raid_card'
    },
    # Subtopic actions - pcie_card (three-level structure)
    'pcie_card_list': {
        'func': pcie_card_list,
        'params': ['server_id', 'start', 'limit'],
        'subtopic': 'pcie_card'
    },
}
