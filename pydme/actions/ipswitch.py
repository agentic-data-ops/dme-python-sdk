"""
IP Switch management related operations
"""

import sys
import os

from pydme.client import DMEAPIClient


def list(client: DMEAPIClient, name: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query Ethernet switch list info
    
    Args:
        client: DME API client
        name: Switch name (optional, supports fuzzy query)
        page_no: Pagination query page number, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            total: Total count (integer),
            data_list: Switch list. parameter format: [{
                id: Switch ID (string),
                name: switch name (string),
                status: status (string),
            }, ...],
        }
    """
    url = "/rest/switchmgmt/v1/switchs/query"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if name is not None:
        payload['name'] = name
    
    response = client.post(url, body=payload)
    return response


def frame_list(client: DMEAPIClient, ipswitch_id: str, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query IP switch chassis list info
    
    Args:
        client: DME API client
        ipswitch_id: IP switch ID (Required)
        page_no: Pagination query page number, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            total: total count (int),
            frames: frame list (List),
        }
    """
    url = "/rest/switchmgmt/switchmgmtservice/v1/switchs/frames/query"
    
    payload = {
        'switch_id': ipswitch_id,
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload)
    return response


def board_list(client: DMEAPIClient, ipswitch_id: str, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query IP switch board list info
    
    Args:
        client: DME API client
        ipswitch_id: IP switch ID (Required)
        page_no: Pagination query page number, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            total: total count (int),
            boards: board list (List),
        }
    """
    url = "/rest/switchmgmt/switchmgmtservice/v1/switchs/boards/query"
    
    payload = {
        'switch_id': ipswitch_id,
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload)
    return response


def subcard_list(client: DMEAPIClient, ipswitch_id: str, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query IP switch subcard list info
    
    Args:
        client: DME API client
        ipswitch_id: IP switch ID (Required)
        page_no: Pagination query page number, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            total: total count (int),
            subcards: subcard list (List),
        }
    """
    url = "/rest/switchmgmt/switchmgmtservice/v1/switchs/subcards/query"
    
    payload = {
        'switch_id': ipswitch_id,
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload)
    return response


def power_list(client: DMEAPIClient, ipswitch_id: str, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query IP switch power supply list info
    
    Args:
        client: DME API client
        ipswitch_id: IP switch ID (Required)
        page_no: Pagination query page number, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            total: total count (int),
            powers: power supply list (List),
        }
    """
    url = "/rest/switchmgmt/switchmgmtservice/v1/switchs/powers/query"
    
    payload = {
        'switch_id': ipswitch_id,
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload)
    return response


def fan_list(client: DMEAPIClient, ipswitch_id: str, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query IP switch fan list info
    
    Args:
        client: DME API client
        ipswitch_id: IP switch ID (Required)
        page_no: Pagination query page number, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            total: total count (int),
            fans: fan list (List),
        }
    """
    url = "/rest/switchmgmt/switchmgmtservice/v1/switchs/fans/query"
    
    payload = {
        'switch_id': ipswitch_id,
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload)
    return response


def port_list(client: DMEAPIClient, ipswitch_id: str, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query IP switch port list info
    
    Args:
        client: DME API client
        ipswitch_id: IP switch ID (Required)
        page_no: Pagination query page number, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            total: total count (int),
            ports: port list (List),
        }
    """
    url = "/rest/switchmgmt/switchmgmtservice/v1/switchs/ports/query"
    
    payload = {
        'switch_id': ipswitch_id,
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload)
    return response


# ACTIONS dictionary, defines all available actions
ACTIONS = {
    'list': {
        'func': list,
        'description': 'Query Ethernet switch list info',
        'params': ['name', 'page_no', 'page_size'],
        'subtopic': None
    },
    'frame_list': {
        'func': frame_list,
        'description': 'Query IP switch chassis list info',
        'params': ['ipswitch_id', 'page_no', 'page_size'],
        'subtopic': 'frame'
    },
    'board_list': {
        'func': board_list,
        'description': 'Query IP switch board list info',
        'params': ['ipswitch_id', 'page_no', 'page_size'],
        'subtopic': 'board'
    },
    'subcard_list': {
        'func': subcard_list,
        'description': 'Query IP switch subcard list info',
        'params': ['ipswitch_id', 'page_no', 'page_size'],
        'subtopic': 'subcard'
    },
    'power_list': {
        'func': power_list,
        'description': 'Query IP switch power supply list info',
        'params': ['ipswitch_id', 'page_no', 'page_size'],
        'subtopic': 'power'
    },
    'fan_list': {
        'func': fan_list,
        'description': 'Query IP switch fan list info',
        'params': ['ipswitch_id', 'page_no', 'page_size'],
        'subtopic': 'fan'
    },
    'port_list': {
        'func': port_list,
        'description': 'Query IP switch port list info',
        'params': ['ipswitch_id', 'page_no', 'page_size'],
        'subtopic': 'port'
    },
}
