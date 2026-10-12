"""
IP switch (IPSwitch) management related operations
"""

import sys
import os

from pydme.client import DMEAPIClient


def list(client: DMEAPIClient, name: str = None, page_no: int = 1, page_size: int = 20) -> dict:
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
    url = "/rest/switchmgmt/switchmgmtservice/v1/switchs/frames/query"
    
    payload = {
        'switch_id': ipswitch_id,
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload)
    return response


def board_list(client: DMEAPIClient, ipswitch_id: str, page_no: int = 1, page_size: int = 20) -> dict:
    url = "/rest/switchmgmt/switchmgmtservice/v1/switchs/boards/query"
    
    payload = {
        'switch_id': ipswitch_id,
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload)
    return response


def subcard_list(client: DMEAPIClient, ipswitch_id: str, page_no: int = 1, page_size: int = 20) -> dict:
    url = "/rest/switchmgmt/switchmgmtservice/v1/switchs/subcards/query"
    
    payload = {
        'switch_id': ipswitch_id,
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload)
    return response


def power_list(client: DMEAPIClient, ipswitch_id: str, page_no: int = 1, page_size: int = 20) -> dict:
    url = "/rest/switchmgmt/switchmgmtservice/v1/switchs/powers/query"
    
    payload = {
        'switch_id': ipswitch_id,
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload)
    return response


def fan_list(client: DMEAPIClient, ipswitch_id: str, page_no: int = 1, page_size: int = 20) -> dict:
    url = "/rest/switchmgmt/switchmgmtservice/v1/switchs/fans/query"
    
    payload = {
        'switch_id': ipswitch_id,
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload)
    return response


def port_list(client: DMEAPIClient, ipswitch_id: str, page_no: int = 1, page_size: int = 20) -> dict:
    url = "/rest/switchmgmt/switchmgmtservice/v1/switchs/ports/query"
    
    payload = {
        'switch_id': ipswitch_id,
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload)
    return response
