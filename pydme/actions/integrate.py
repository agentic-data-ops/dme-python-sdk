"""
Third-party system integration (Integrate) operations
包含CMDB系统、主机、Application resource query
"""

import sys
import os

from pydme.client import DMEAPIClient


def cmdb_system_list(client: DMEAPIClient, name: str = None,
                     page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询CMDB system list。

    Args:
        client: DME API client
        name: CMDB系统名称（Optional，supports fuzzy search）
        page_no: Page queryStart page，默认 1
        page_size: 每页count，1~1000，默认 20

    Returns:
        {
            total: Total count (integer),
            systems: CMDB system list。参数格式如下：[{
                id: 系统ID (string),
                name: 系统名称 (string),
                ip: IP地址 (string),
            }, ...],
        }
    """
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
    """
    查询CMDBHost list in system。

    Args:
        client: DME API client
        system_id: CMDB系统ID（Optional）
        name: Host name（Optional，supports fuzzy search）
        ip: Host IP（Optional）
        page_no: Page queryStart page，默认 1
        page_size: 每页count，1~1000，默认 20

    Returns:
        {
            total: Total count (integer),
            hosts: CMDB host list。参数格式如下：[{
                id: Host ID (string),
                name: Host name (string),
                ip: IP地址 (string),
            }, ...],
        }
    """
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
    """
    QueryCMDB主机详情。

    Args:
        client: DME API client
        cmdb_host_id: CMDBHost ID（Required）

    Returns:
        {
            id: Host ID (string),
            name: Host name (string),
            ip: IP地址 (string),
        }
    """
    url = "/rest/appmgmt/v1/cmdb-hosts/{cmdb_host_id}"

    if not cmdb_host_id:
        raise ValueError("cmdb_host_id 是required parameter")

    response = client.get(url, params={"cmdb_host_id": cmdb_host_id})
    return response


def cmdb_app_list(client: DMEAPIClient, system_id: str = None, name: str = None,
                  page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询CMDB系统中的Application list。

    Args:
        client: DME API client
        system_id: CMDB系统ID（Optional）
        name: 应用名称（Optional，supports fuzzy search）
        page_no: Page queryStart page，默认 1
        page_size: 每页count，1~1000，默认 20

    Returns:
        {
            total: Total count (integer),
            applications: Application list。参数格式如下：[{
                id: 应用ID (string),
                name: 应用名称 (string),
            }, ...],
        }
    """
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
    """
    根据Initiator list查询CMDB host list。

    Args:
        client: DME API client
        initiators: Initiator list（Required）

    Returns:
        {
            hosts: CMDB host list。参数格式如下：[{
                id: Host ID (string),
                name: Host name (string),
            }, ...],
        }
    """
    url = "/rest/appmgmt/v1/cmdb-hosts/query-by-initiators"

    if not initiators or len(initiators) == 0:
        raise ValueError("initiators 是required parameter")

    payload = {
        'initiators': initiators
    }

    response = client.post(url, body=payload)
    return response


ACTIONS = {
    # cmdb subtopic actions
    'cmdb_system_list': {
        'func': cmdb_system_list,
        'description': '查询CMDB system list',
        'params': ['name', 'page_no', 'page_size'],
        'subtopic': 'cmdb'
    },
    'cmdb_host_list': {
        'func': cmdb_host_list,
        'description': '查询CMDBHost list in system',
        'params': ['system_id', 'name', 'ip', 'page_no', 'page_size'],
        'subtopic': 'cmdb'
    },
    'cmdb_host_show': {
        'func': cmdb_host_show,
        'description': 'QueryCMDB主机详情',
        'params': ['cmdb_host_id'],
        'subtopic': 'cmdb'
    },
    'cmdb_app_list': {
        'func': cmdb_app_list,
        'description': '查询CMDB系统中的Application list',
        'params': ['system_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'cmdb'
    },
    'cmdb_host_query_by_initiators': {
        'func': cmdb_host_query_by_initiators,
        'description': '根据Initiator list查询CMDB host list',
        'params': ['initiators'],
        'subtopic': 'cmdb'
    },
}
