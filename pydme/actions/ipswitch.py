"""
IP 交换机 (IPSwitch) 管理相关操作
"""

import sys
import os

from pydme.client import DMEAPIClient


def list(client: DMEAPIClient, name: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    query以太网交换机listinfo
    
    Args:
        client: DME API client
        name: switch name (可选, supports fuzzy query)
        page_no: 分页query的页码, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            total: 总count (integer),
            data_list: 交换机list. parameter format: [{
                id: 交换机ID (string),
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
    query IP 交换机机框listinfo
    
    Args:
        client: DME API client
        ipswitch_id: IP 交换机 ID(Required)
        page_no: 分页query的页码, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含 total 和 frames 字段
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
    query IP 交换机单板listinfo
    
    Args:
        client: DME API client
        ipswitch_id: IP 交换机 ID(Required)
        page_no: 分页query的页码, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含 total 和 boards 字段
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
    query IP 交换机子卡listinfo
    
    Args:
        client: DME API client
        ipswitch_id: IP 交换机 ID(Required)
        page_no: 分页query的页码, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含 total 和 subcards 字段
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
    query IP 交换机电源listinfo
    
    Args:
        client: DME API client
        ipswitch_id: IP 交换机 ID(Required)
        page_no: 分页query的页码, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含 total 和 powers 字段
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
    query IP 交换机风扇listinfo
    
    Args:
        client: DME API client
        ipswitch_id: IP 交换机 ID(Required)
        page_no: 分页query的页码, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含 total 和 fans 字段
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
    query IP 交换机端口listinfo
    
    Args:
        client: DME API client
        ipswitch_id: IP 交换机 ID(Required)
        page_no: 分页query的页码, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含 total 和 ports 字段
    """
    url = "/rest/switchmgmt/switchmgmtservice/v1/switchs/ports/query"
    
    payload = {
        'switch_id': ipswitch_id,
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload)
    return response


# ACTIONS 字典, 定义所有可用动作
ACTIONS = {
    'list': {
        'func': list,
        'description': '查询以太网交换机列表信息',
        'params': ['name', 'page_no', 'page_size'],
        'subtopic': None
    },
    'frame_list': {
        'func': frame_list,
        'description': '查询 IP 交换机机框列表信息',
        'params': ['ipswitch_id', 'page_no', 'page_size'],
        'subtopic': 'frame'
    },
    'board_list': {
        'func': board_list,
        'description': '查询 IP 交换机单板列表信息',
        'params': ['ipswitch_id', 'page_no', 'page_size'],
        'subtopic': 'board'
    },
    'subcard_list': {
        'func': subcard_list,
        'description': '查询 IP 交换机子卡列表信息',
        'params': ['ipswitch_id', 'page_no', 'page_size'],
        'subtopic': 'subcard'
    },
    'power_list': {
        'func': power_list,
        'description': '查询 IP 交换机电源列表信息',
        'params': ['ipswitch_id', 'page_no', 'page_size'],
        'subtopic': 'power'
    },
    'fan_list': {
        'func': fan_list,
        'description': '查询 IP 交换机风扇列表信息',
        'params': ['ipswitch_id', 'page_no', 'page_size'],
        'subtopic': 'fan'
    },
    'port_list': {
        'func': port_list,
        'description': '查询 IP 交换机端口列表信息',
        'params': ['ipswitch_id', 'page_no', 'page_size'],
        'subtopic': 'port'
    },
}
