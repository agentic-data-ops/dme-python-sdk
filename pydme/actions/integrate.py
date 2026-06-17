"""
Third-party system integration related operations
Includes CMDB system, host, application and other resource queries
"""

import sys
import os

from pydme.client import DMEAPIClient


def cmdb_system_list(client: DMEAPIClient, name: str = None,
                     page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query CMDB system list.

    Args:
        client: DME API client
        name: CMDB system name (optional, supports fuzzy query)
        page_no: Pagination start page, default 1
        page_size: items per page, 1~1000, default 20

    Returns:
        {
            total: total (integer),
            systems: CMDB system list. parameter format: [{
                id: System ID (string),
                name: System name (string),
                ip: IP address (string),
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
    Query host list in CMDB system.

    Args:
        client: DME API client
        system_id: CMDB system ID (Optional)
        name: Host name (optional, supports fuzzy query)
        ip: Host IP (Optional)
        page_no: Pagination start page, default 1
        page_size: items per page, 1~1000, default 20

    Returns:
        {
            total: total (integer),
            hosts: CMDB host list. parameter format: [{
                id: host ID (string),
                name: host name (string),
                ip: IP address (string),
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
    Query specified CMDB host details.

    Args:
        client: DME API client
        cmdb_host_id: CMDB host ID (Required)

    Returns:
        {
            id: host ID (string),
            name: host name (string),
            ip: IP address (string),
        }
    """
    url = "/rest/appmgmt/v1/cmdb-hosts/{cmdb_host_id}"

    if not cmdb_host_id:
        raise ValueError("cmdb_host_id is a required parameter")

    response = client.get(url, params={"cmdb_host_id": cmdb_host_id})
    return response


def cmdb_app_list(client: DMEAPIClient, system_id: str = None, name: str = None,
                  page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query application list in CMDB system.

    Args:
        client: DME API client
        system_id: CMDB system ID (Optional)
        name: Application name (optional, supports fuzzy query)
        page_no: Pagination start page, default 1
        page_size: items per page, 1~1000, default 20

    Returns:
        {
            total: total (integer),
            applications: Application list. parameter format: [{
                id: Application ID (string),
                name: Application name (string),
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
    Query CMDB host list by initiator list.

    Args:
        client: DME API client
        initiators: Initiator list (Required)

    Returns:
        {
            hosts: CMDB host list. parameter format: [{
                id: host ID (string),
                name: host name (string),
            }, ...],
        }
    """
    url = "/rest/appmgmt/v1/cmdb-hosts/query-by-initiators"

    if not initiators or len(initiators) == 0:
        raise ValueError("initiators is a required parameter")

    payload = {
        'initiators': initiators
    }

    response = client.post(url, body=payload)
    return response


ACTIONS = {
    # cmdb subtopic action
    'cmdb_system_list': {
        'func': cmdb_system_list,
        'description': 'Query CMDB system list',
        'params': ['name', 'page_no', 'page_size'],
        'subtopic': 'cmdb'
    },
    'cmdb_host_list': {
        'func': cmdb_host_list,
        'description': 'Query host list in CMDB system',
        'params': ['system_id', 'name', 'ip', 'page_no', 'page_size'],
        'subtopic': 'cmdb'
    },
    'cmdb_host_show': {
        'func': cmdb_host_show,
        'description': 'Query specified CMDB host details',
        'params': ['cmdb_host_id'],
        'subtopic': 'cmdb'
    },
    'cmdb_app_list': {
        'func': cmdb_app_list,
        'description': 'Query application list in CMDB system',
        'params': ['system_id', 'name', 'page_no', 'page_size'],
        'subtopic': 'cmdb'
    },
    'cmdb_host_query_by_initiators': {
        'func': cmdb_host_query_by_initiators,
        'description': 'Query CMDB host list by initiator list',
        'params': ['initiators'],
        'subtopic': 'cmdb'
    },
}
