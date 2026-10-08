"""
三方系统集成 (Integrate) 相关操作
包含CMDB系统、主机、应用等资源查询
"""

import sys
import os

from pydme.client import DMEAPIClient


def cmdb_system_list(client: DMEAPIClient, name: str = None,
                     page_no: int = 1, page_size: int = 20) -> dict:
    url = "/rest/appmgmt/v1/cmdb-systems/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    if name is not None:
        payload['name'] = name

    response = client.post(url, body=payload)
    return response


def cmdb_host_list(client: DMEAPIClient, system_id: str = None, name: str = None,
                   ip: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    url = "/rest/appmgmt/v1/cmdb-hosts/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    if system_id is not None:
        payload['system_id'] = system_id
    if name is not None:
        payload['name'] = name
    if ip is not None:
        payload['ip'] = ip

    response = client.post(url, body=payload)
    return response


def cmdb_host_show(client: DMEAPIClient, cmdb_host_id: str) -> dict:
    url = "/rest/appmgmt/v1/cmdb-hosts/{cmdb_host_id}"

    if not cmdb_host_id:
        raise ValueError("cmdb_host_id 是必选参数")

    response = client.get(url, params={"cmdb_host_id": cmdb_host_id})
    return response


def cmdb_app_list(client: DMEAPIClient, system_id: str = None, name: str = None,
                  page_no: int = 1, page_size: int = 20) -> dict:
    url = "/rest/appmgmt/v1/applications/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    if system_id is not None:
        payload['system_id'] = system_id
    if name is not None:
        payload['name'] = name

    response = client.post(url, body=payload)
    return response


def cmdb_host_query_by_initiators(client: DMEAPIClient, initiators: list) -> dict:
    url = "/rest/appmgmt/v1/cmdb-hosts/query-by-initiators"

    if not initiators or len(initiators) == 0:
        raise ValueError("initiators 是必选参数")

    payload = {
        'initiators': initiators
    }

    response = client.post(url, body=payload)
    return response


ACTIONS = {
    # cmdb 子主题动作
    'cmdb_system_list': {
        'func': cmdb_system_list,
        'description': '查询CMDB系统列表',
        'params': ['name', 'page_no', 'page_size'],
        'subtopic': 'cmdb'
    },
    'cmdb_host_list': {
        'func': cmdb_host_list,
        'description': '查询CMDB系统中的主机列表',
        'params': ['system_id', 'name', 'ip', 'page_no', 'page_size'],
        'subtopic': 'cmdb'
    },
    'cmdb_host_show': {
        'func': cmdb_host_show,
        'description': '查询指定CMDB主机详情',
        'params': ['cmdb_host_id'],
        'subtopic': 'cmdb'
    },
    'cmdb_app_list': {
        'func': cmdb_app_list,
        'description': '查询CMDB系统中的应用列表',
        'params': ['system_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'cmdb'
    },
    'cmdb_host_query_by_initiators': {
        'func': cmdb_host_query_by_initiators,
        'description': '根据启动器列表查询CMDB主机列表',
        'params': ['initiators'],
        'subtopic': 'cmdb'
    },
}
