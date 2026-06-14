"""
IP Switch (IPSwitch) management operations
"""

import sys
import os

from pydme.client import DMEAPIClient


def list(client: DMEAPIClient, name: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query Ethernet switch list info
    
    Args:
        client: DME API client
        name: Switch name (Optional, supports fuzzy search) 
        page_no: Page number, default 1
        page_size: per pagecount, 1~1000, default 20
    
    Returns:
        {
            total: Total count (integer),
            data_list: Switch list. 参数格式如下：[{
                id: SwitchID (string),
                name: Switch name (string),
                status:  status (string),
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
     query IP Switchenclosure list info
    
    Args:
        client: DME API client
        ipswitch_id: IP Switch ID (Required) 
        page_no: Page number, default 1
        page_size: per pagecount, 1~1000, default 20
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes total and frames fields
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
     query IP Switch board list info
    
    Args:
        client: DME API client
        ipswitch_id: IP Switch ID (Required) 
        page_no: Page number, default 1
        page_size: per pagecount, 1~1000, default 20
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes total and boards fields
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
     query IP Switch subcard list info
    
    Args:
        client: DME API client
        ipswitch_id: IP Switch ID (Required) 
        page_no: Page number, default 1
        page_size: per pagecount, 1~1000, default 20
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes total and subcards fields
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
     query IP Switchpower supply list info
    
    Args:
        client: DME API client
        ipswitch_id: IP Switch ID (Required) 
        page_no: Page number, default 1
        page_size: per pagecount, 1~1000, default 20
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes total and powers fields
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
     query IP switch fan list info
    
    Args:
        client: DME API client
        ipswitch_id: IP Switch ID (Required) 
        page_no: Page number, default 1
        page_size: per pagecount, 1~1000, default 20
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes total and fans fields
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
     query IP Switch port list info
    
    Args:
        client: DME API client
        ipswitch_id: IP Switch ID (Required) 
        page_no: Page number, default 1
        page_size: per pagecount, 1~1000, default 20
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes total and ports fields
    """
    url = "/rest/switchmgmt/switchmgmtservice/v1/switchs/ports/query"
    
    payload = {
        'switch_id': ipswitch_id,
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload)
    return response


# Actions, Define all available actions
ACTIONS = {
    'list': {
        'func': list,
        'description': 'Query Ethernet switch list info',
        'params': ['name', 'page_no', 'page_size'],
        'subtopic': None
    },
    'frame_list': {
        'func': frame_list,
        'description': ' query IP Switchenclosure list info',
        'params': ['ipswitch_id', 'page_no', 'page_size'],
        'subtopic': 'frame'
    },
    'board_list': {
        'func': board_list,
        'description': ' query IP Switch board list info',
        'params': ['ipswitch_id', 'page_no', 'page_size'],
        'subtopic': 'board'
    },
    'subcard_list': {
        'func': subcard_list,
        'description': ' query IP Switch subcard list info',
        'params': ['ipswitch_id', 'page_no', 'page_size'],
        'subtopic': 'subcard'
    },
    'power_list': {
        'func': power_list,
        'description': ' query IP Switchpower supply list info',
        'params': ['ipswitch_id', 'page_no', 'page_size'],
        'subtopic': 'power'
    },
    'fan_list': {
        'func': fan_list,
        'description': ' query IP switch fan list info',
        'params': ['ipswitch_id', 'page_no', 'page_size'],
        'subtopic': 'fan'
    },
    'port_list': {
        'func': port_list,
        'description': ' query IP Switch port list info',
        'params': ['ipswitch_id', 'page_no', 'page_size'],
        'subtopic': 'port'
    },
}
