"""
System management (System) related operations
"""

import sys
import os

from pydme.client import DMEAPIClient


def login(client: DMEAPIClient) -> dict:
    client.login()

    accessSession = client.headers.get("X-Auth-Token", "")
    if accessSession:
        print(f"\nLogin successful!")
        print(f"\nTip: configure environment variables to reuse the auth token and avoid repeated login:")
        print("  export DME_API_AUTH_TOKEN='<accessSession>'")

    return {
        'accessSession': accessSession
    }


def logout(client: DMEAPIClient) -> dict:
    url = "/rest/plat/smapp/v1/sessions"
    
    response = client.delete(url)
    return response


def reset_password(client: DMEAPIClient, user_name: str, new_value: str,
                   is_initial_password: bool = True) -> dict:
    url = "/rest/usm/v1/users/{user_name}/reset-credentials"

    # Parameter validation
    if not user_name or len(user_name) > 128:
        raise ValueError("user_name is required, 1~128 characters")
    if not new_value or len(new_value) < 8 or len(new_value) > 32:
        raise ValueError("new_value is required, 8~32 characters")

    payload = {
        'newValue': new_value,
        'isInitialPassword': is_initial_password
    }

    response = client.put(url, body=payload, params={"user_name": user_name})
    return response


def user_delete(client: DMEAPIClient, user_id: int) -> dict:
    url = "/rest/usermgmt/v1/users/{user_id}"

    # Parameter validation
    if user_id is None:
        raise ValueError("user_id is required")

    response = client.delete(url, params={"user_id": user_id})
    return response


def user_create(client: DMEAPIClient, name: str, type: int,
                value: str = None, description: str = None,
                roles: list = None) -> dict:
    url = "/rest/usermgmt/v1/users"

    # Parameter validation
    if not name:
        raise ValueError("name is required")

    payload = {
        'name': name,
        'type': type,
    }

    if value is not None:
        payload['value'] = value
    if description is not None:
        payload['description'] = description
    if roles is not None:
        payload['roles'] = roles

    response = client.post(url, body=payload)
    return response


def user_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 10,
              name: str = None) -> dict:
    url = "/rest/usermgmt/v1/users"
    
    response = client.get(url, params={
        'page_no': page_no,
        'page_size': page_size,
        'name': name
    })
    return response


def role_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 10,
              name: str = None) -> dict:
    url = "/rest/usermgmt/v1/roles"
    
    response = client.get(url, params={
        'page_no': page_no,
        'page_size': page_size,
        'name': name
    })
    return response


def user_show(client: DMEAPIClient, user_id: int) -> dict:
    url = "/rest/usermgmt/v1/users/{user_id}"
    
    # Parameter validation
    if user_id is None:
        raise ValueError("user_id is required")

    response = client.get(url, params={"user_id": user_id})
    return response


def show(client: DMEAPIClient) -> dict:
    url = "/rest/productmgmt/v1/system-info"
    
    response = client.get(url)
    return response


def certificate(client: DMEAPIClient, service_type: str = "APIGWService") -> dict:
    url = "/rest/certmgmt/v1/certs"

    # Parameter validation
    if service_type not in ["APIGWService"]:
        raise ValueError(f"service_type valid values: APIGWService")

    response = client.get(url, params={'service_type': service_type})
    return response


def backup_server_list(client: DMEAPIClient, address: str = None,
                         name: str = None,
                         page_no: int = 1, page_size: int = 20) -> dict:
    url = "/rest/configmgmt/v1/backup-servers"
    
    query_params = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if address is not None:
        query_params['address'] = address
    if name is not None:
        query_params['name'] = name
    
    response = client.get(url, params=query_params)
    return response


# ==================== Todo task group management (todo_task_group subtopic) ====================

def todo_task_group_list(client: DMEAPIClient, group_id: str = None, name: str = None,
               creator_name: str = None, is_finished: bool = None,
               is_group: bool = None, start: int = None, limit: int = None,
               status: list = None, todo_item_status: list = None,
               start_time_from: str = None, start_time_to: str = None,
               end_time_from: str = None, end_time_to: str = None,
               sort_key: str = None, sort_dir: str = None) -> dict:
    url = "/rest/taskmgmt/v1/todo-groups"

    params = {}
    if group_id is not None:
        params['group_id'] = group_id
    if name is not None:
        params['name'] = name
    if creator_name is not None:
        params['creator_name'] = creator_name
    if is_finished is not None:
        params['is_finished'] = str(is_finished).lower()
    if is_group is not None:
        params['is_group'] = str(is_group).lower()
    if start is not None:
        params['start'] = start
    if limit is not None:
        params['limit'] = limit
    if status is not None:
        params['status'] = status
    if todo_item_status is not None:
        params['todo_item_status'] = todo_item_status
    if start_time_from is not None:
        params['start_time_from'] = start_time_from
    if start_time_to is not None:
        params['start_time_to'] = start_time_to
    if end_time_from is not None:
        params['end_time_from'] = end_time_from
    if end_time_to is not None:
        params['end_time_to'] = end_time_to
    if sort_key is not None:
        params['sort_key'] = sort_key
    if sort_dir is not None:
        params['sort_dir'] = sort_dir

    response = client.get(url, params=params)
    return response


def todo_task_group_execute(client: DMEAPIClient, group_id: str) -> dict:
    url = "/rest/taskmgmt/v1/todo-groups/{group_id}/execute"

    response = client.put(url, body={}, params={"group_id": group_id})
    return response


def todo_task_group_confirm(client: DMEAPIClient, group_id: str) -> dict:
    url = "/rest/taskmgmt/v1/todo-groups/{group_id}/confirm"

    response = client.put(url, body={}, params={"group_id": group_id})
    return response


# ==================== Todo task management (todo_task subtopic) ====================

def todo_task_list(client: DMEAPIClient, service_type: str,
               status: list = None, page_no: int = None,
               page_size: int = None) -> dict:
    url = "/rest/taskmgmt/v1/todo-items/query"

    payload = {
        'service_type': service_type
    }
    if status is not None:
        payload['status'] = status
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size

    response = client.post(url, body=payload)
    return response


def todo_task_show(client: DMEAPIClient, item_id: str) -> dict:
    url = "/rest/taskmgmt/v1/todo-items/{item_id}"

    response = client.get(url, params={"item_id": item_id})
    return response


def todo_task_execute(client: DMEAPIClient, item_id: str) -> dict:
    url = "/rest/taskmgmt/v1/todo-items/{item_id}/execute"

    response = client.put(url, body={}, params={"item_id": item_id})
    return response


def todo_task_audit(client: DMEAPIClient, item_id: str, is_approval: bool,
          suggestion: str = None) -> dict:
    url = "/rest/taskmgmt/v1/todo-items/{item_id}/audit"

    payload = {
        'is_approval': is_approval
    }
    if suggestion is not None:
        payload['suggestion'] = suggestion

    response = client.post(url, body=payload, params={"item_id": item_id})
    return response


def todo_task_revoke(client: DMEAPIClient, item_id: str) -> dict:
    url = "/rest/taskmgmt/v1/todo-items/{item_id}/revoke-audit"

    response = client.put(url, body={}, params={"item_id": item_id})
    return response


def todo_task_close(client: DMEAPIClient, item_id: str, reason: str) -> dict:
    url = "/rest/taskmgmt/v1/todo-items/{item_id}/close"

    payload = {
        'reason': reason
    }

    response = client.put(url, body=payload, params={"item_id": item_id})
    return response


# ==================== Task management (task subtopic) ====================

import time

def task_show(client: DMEAPIClient, task_id: str) -> list:
    url = "/rest/taskmgmt/v1/tasks/{task_id}"
    
    response = client.get(url, params={"task_id": task_id})
    return response


def task_list(client: DMEAPIClient, start: int = 1, limit: int = 100,
               task_name: str = None, status: int = None,
               owner_id: str = None, create_time_from: int = None,
               create_time_to: int = None) -> dict:
    url = "/rest/taskmgmt/v1/tasks"
    
    params = {
        'start': start,
        'limit': limit
    }
    
    if task_name is not None:
        params['taskName'] = task_name
    if status is not None:
        params['status'] = status
    if owner_id is not None:
        params['ownerId'] = owner_id
    if create_time_from is not None:
        params['createTimeFrom'] = create_time_from
    if create_time_to is not None:
        params['createTimeTo'] = create_time_to
    
    response = client.get(url, params=params)
    return response


def task_retry(client: DMEAPIClient, task_id: str) -> dict:
    url = "/rest/taskmgmt/v1/tasks/{task_id}/retry"

    response = client.post(url, body={}, params={"task_id": task_id})
    return response


def task_wait(client: DMEAPIClient, task_id: str, timeout: int = 300,
              poll_interval: int = 2) -> dict:
    retry_times = max(1, timeout // poll_interval)
    return client.get_task_result(
        task_id,
        retry_times=retry_times,
        retry_interval=poll_interval,
    )


# ==================== Tag type management (tag_type subtopic) ====================

def tag_type_create(client: DMEAPIClient, name: str, description: str = None) -> dict:
    url = "/rest/tagmgmt/v1/tag-types"
    
    payload = {
        'name': name
    }
    
    if description is not None:
        payload['description'] = description
    
    response = client.post(url, body=payload)
    return response


def tag_type_list(client: DMEAPIClient, start: int = 1, limit: int = 100,
                         name: str = None) -> dict:
    url = "/rest/tagmgmt/v1/tag-types/query"
    
    payload = {
        'start': start,
        'limit': limit
    }
    
    if name is not None:
        payload['name'] = name
    
    response = client.post(url, body=payload)
    return response


def tag_type_modify(client: DMEAPIClient, tag_type_id: str, name: str = None,
                     description: str = None) -> dict:
    url = "/rest/tagmgmt/v1/tag-types/{tag_type_id}"
    
    payload = {}
    
    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description
    
    response = client.put(url, body=payload, params={"tag_type_id": tag_type_id})
    return response


def tag_type_delete(client: DMEAPIClient, tag_type_ids: list) -> dict:
    url = "/rest/tagmgmt/v1/tag-types/delete"
    
    payload = {
        'ids': tag_type_ids
    }
    
    response = client.post(url, body=payload)
    return response


# ==================== Tag management (tag subtopic) ====================

def tag_create(client: DMEAPIClient, name: str, tag_type_id: str,
                tag_type_name: str = None, description: str = None, color: str = None) -> dict:
    url = "/rest/tagmgmt/v1/tags"
    
    payload = {
        'name': name,
        'tag_type_id': tag_type_id
    }
    
    if tag_type_name is not None:
        payload['tag_type_name'] = tag_type_name
    if description is not None:
        payload['description'] = description
    if color is not None:
        payload['color'] = color
    
    response = client.post(url, body=payload)
    return response


def tag_list(client: DMEAPIClient, start: int = 1, limit: int = 100,
                    name: str = None, tag_type_id: str = None) -> dict:
    url = "/rest/tagmgmt/v1/tags/query"
    
    payload = {
        'start': start,
        'limit': limit
    }
    
    if name is not None:
        payload['name'] = name
    if tag_type_id is not None:
        payload['tag_type_id'] = tag_type_id
    
    response = client.post(url, body=payload)
    return response


def tag_modify(client: DMEAPIClient, tag_id: str, name: str = None,
                description: str = None, color: str = None) -> dict:
    url = "/rest/tagmgmt/v1/tags/{tag_id}"
    
    payload = {}
    
    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description
    if color is not None:
        payload['color'] = color
    
    response = client.put(url, body=payload, params={"tag_id": tag_id})
    return response


def tag_delete(client: DMEAPIClient, tag_ids: list) -> dict:
    url = "/rest/tagmgmt/v1/tags/delete"
    
    payload = {
        'ids': tag_ids
    }
    
    response = client.post(url, body=payload)
    return response


def tag_bind(client: DMEAPIClient, tag_id: str, resources: list) -> dict:
    url = "/rest/tagmgmt/v1/tags/{tag_id}/associate-resources"
    
    payload = {
        'resources': resources
    }
    
    response = client.post(url, body=payload, params={"tag_id": tag_id})
    return response


def tag_unbind(client: DMEAPIClient, tag_id: str, resources: list) -> dict:
    url = "/rest/tagmgmt/v1/tags/{tag_id}/disassociate-resources"
    
    payload = {
        'resources': resources
    }
    
    response = client.post(url, body=payload, params={"tag_id": tag_id})
    return response


# ==================== Available zone management (az subtopic) ====================

def az_list(client: DMEAPIClient, az_name: str = None, operate_status: str = None,
         start: int = 1, limit: int = 512, is_sc: bool = False) -> dict:
    url = "/rest/azmgmt/v1/availability-zones"

    query_params = {}
    if az_name is not None:
        query_params['az_name'] = az_name
    if operate_status is not None:
        query_params['operate_status'] = operate_status
    if start is not None:
        query_params['start'] = start
    if limit is not None:
        query_params['limit'] = limit
    if is_sc is not None:
        query_params['is_sc'] = str(is_sc).lower()

    response = client.get(url, params=query_params)
    return response


# ==================== Data center management (dc subtopic) ====================

def dc_list(client: DMEAPIClient, name: str = None,
                     page_no: int = 1, page_size: int = 20) -> dict:
    url = "/rest/dcmgmt/dcmgmtservice/v1/datacenters/query"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if name is not None:
        payload['name'] = name
    
    response = client.post(url, body=payload)
    return response


def dc_show(client: DMEAPIClient, dc_id: str) -> dict:
    url = "/rest/dcmgmt/dcmgmtservice/v1/datacenters/{dc_id}"
    
    response = client.get(url, params={"dc_id": dc_id})
    return response


def dc_show_devices(client: DMEAPIClient, dc_id: str,
                 device_type: list = None, page_no: int = 1,
                 page_size: int = 20) -> dict:
    url = "/rest/dcmgmt/dcmgmtservice/v1/datacenters/devices/query"
    
    payload = {
        'dc_id': dc_id,
        'page_no': page_no,
        'page_size': page_size
    }
    
    if device_type is not None:
        payload['device_type'] = device_type
    
    response = client.post(url, body=payload)
    return response


def region_list(client: DMEAPIClient, ids: list = None, name: str = None,
                active_ip_address: str = None, standby_ip_address: str = None,
                sync_status: list = None, role: str = None,
                sort_key: str = None, sort_dir: str = None,
                page_no: int = 1, page_size: int = 20) -> dict:
    url = "/rest/regionmgmt/v1/regions/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    if ids is not None:
        payload['ids'] = ids
    if name is not None:
        payload['name'] = name
    if active_ip_address is not None:
        payload['active_ip_address'] = active_ip_address
    if standby_ip_address is not None:
        payload['standby_ip_address'] = standby_ip_address
    if sync_status is not None:
        payload['sync_status'] = sync_status
    if role is not None:
        payload['role'] = role
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def region_query(client: DMEAPIClient, region_id: str, request_url: str,
                 request_method: str, request_body: str = None) -> dict:
    url = "/rest/regionmgmt/v1/regions/{region_id}/resources/query"

    if not region_id:
        raise ValueError("region_id is required")
    if not request_url:
        raise ValueError("request_url is required")

    payload = {
        'request_url': request_url,
        'request_method': request_method
    }
    if request_body is not None:
        payload['request_body'] = request_body

    response = client.post(url, body=payload, params={"region_id": region_id})
    return response


# Action list for CLI help
ACTIONS = {
    # Direct actions (two-level structure)
    'login': {
        'func': login,
        'params': ['username', 'password', 'grant_type'],
        'subtopic': None
    },
    'logout': {
        'func': logout,
        'params': [],
        'subtopic': None
    },
    'show': {
        'func': show,
        'params': [],
        'subtopic': None
    },
    'certificate': {
        'func': certificate,
        'params': [],
        'subtopic': None
    },
    'reset_password': {
        'func': reset_password,
        'params': ['user_name', 'new_value', 'is_initial_password'],
        'subtopic': None
    },
    # Subtopic actions - user (three-level structure)
    'user_list': {
        'func': user_list,
        'params': ['page_no', 'page_size', 'name'],
        'subtopic': 'user'
    },
    'user_show': {
        'func': user_show,
        'params': ['user_id'],
        'subtopic': 'user'
    },
    'user_create': {
        'func': user_create,
        'params': ['name', 'type', 'value', 'description', 'roles'],
        'subtopic': 'user'
    },
    'user_delete': {
        'func': user_delete,
        'params': ['user_id'],
        'subtopic': 'user'
    },
    # Subtopic actions - role (three-level structure)
    'role_list': {
        'func': role_list,
        'params': ['page_no', 'page_size', 'name'],
        'subtopic': 'role'
    },
    # Subtopic actions - backup_server (three-level structure)
    'backup_server_list': {
        'func': backup_server_list,
        'params': ['address', 'name', 'page_no', 'page_size'],
        'subtopic': 'backup_server'
    },
    # Subtopic actions - todo_task_group (three-level structure)
    'todo_task_group_list': {
        'func': todo_task_group_list,
        'params': ['group_id', 'name', 'creator_name', 'is_finished', 'is_group',
                   'start', 'limit', 'status', 'todo_item_status',
                   'start_time_from', 'start_time_to', 'end_time_from',
                   'end_time_to', 'sort_key', 'sort_dir'],
        'subtopic': 'todo_task_group'
    },
    'todo_task_group_execute': {
        'func': todo_task_group_execute,
        'params': ['group_id'],
        'subtopic': 'todo_task_group'
    },
    'todo_task_group_confirm': {
        'func': todo_task_group_confirm,
        'params': ['group_id'],
        'subtopic': 'todo_task_group'
    },
    # Subtopic actions - todo_task (three-level structure)
    'todo_task_list': {
        'func': todo_task_list,
        'params': ['service_type', 'status', 'page_no', 'page_size'],
        'subtopic': 'todo_task'
    },
    'todo_task_show': {
        'func': todo_task_show,
        'params': ['item_id'],
        'subtopic': 'todo_task'
    },
    'todo_task_execute': {
        'func': todo_task_execute,
        'params': ['item_id'],
        'subtopic': 'todo_task'
    },
    'todo_task_audit': {
        'func': todo_task_audit,
        'params': ['item_id', 'is_approval', 'suggestion'],
        'subtopic': 'todo_task'
    },
    'todo_task_revoke': {
        'func': todo_task_revoke,
        'params': ['item_id'],
        'subtopic': 'todo_task'
    },
    'todo_task_close': {
        'func': todo_task_close,
        'params': ['item_id', 'reason'],
        'subtopic': 'todo_task'
    },
    # Subtopic actions - task (three-level structure)
    'task_show': {
        'func': task_show,
        'params': ['task_id'],
        'subtopic': 'task'
    },
    'task_list': {
        'func': task_list,
        'params': ['start', 'limit', 'task_name', 'status', 'owner_id', 'create_time_from', 'create_time_to'],
        'subtopic': 'task'
    },
    'task_retry': {
        'func': task_retry,
        'params': ['task_id'],
        'subtopic': 'task'
    },
    'task_wait': {
        'func': task_wait,
        'params': ['task_id', 'timeout', 'poll_interval'],
        'subtopic': 'task'
    },
    # Subtopic actions - tag_type (three-level structure)
    'tag_type_create': {
        'func': tag_type_create,
        'params': ['name', 'description'],
        'subtopic': 'tag_type'
    },
    'tag_type_list': {
        'func': tag_type_list,
        'params': ['start', 'limit', 'name'],
        'subtopic': 'tag_type'
    },
    'tag_type_modify': {
        'func': tag_type_modify,
        'params': ['tag_type_id', 'name', 'description'],
        'subtopic': 'tag_type'
    },
    'tag_type_delete': {
        'func': tag_type_delete,
        'params': ['tag_type_ids'],
        'subtopic': 'tag_type'
    },
    # Subtopic actions - tag (three-level structure)
    'tag_create': {
        'func': tag_create,
        'params': ['name', 'tag_type_id', 'tag_type_name', 'description', 'color'],
        'subtopic': 'tag'
    },
    'tag_list': {
        'func': tag_list,
        'params': ['start', 'limit', 'name', 'tag_type_id'],
        'subtopic': 'tag'
    },
    'tag_modify': {
        'func': tag_modify,
        'params': ['tag_id', 'name', 'description', 'color'],
        'subtopic': 'tag'
    },
    'tag_delete': {
        'func': tag_delete,
        'params': ['tag_ids'],
        'subtopic': 'tag'
    },
    'tag_bind': {
        'func': tag_bind,
        'params': ['tag_id', 'resources'],
        'subtopic': 'tag'
    },
    'tag_unbind': {
        'func': tag_unbind,
        'params': ['tag_id', 'resources'],
        'subtopic': 'tag'
    },
    # Subtopic actions - az (three-level structure)
    'az_list': {
        'func': az_list,
        'params': ['az_name', 'operate_status', 'start', 'limit', 'is_sc'],
        'subtopic': 'az'
    },
    # Subtopic actions - dc (three-level structure)
    'dc_list': {
        'func': dc_list,
        'params': ['name', 'page_no', 'page_size'],
        'subtopic': 'dc'
    },
    'dc_show': {
        'func': dc_show,
        'params': ['dc_id'],
        'subtopic': 'dc'
    },
    'dc_show_devices': {
        'func': dc_show_devices,
        'params': ['dc_id', 'device_type', 'page_no', 'page_size'],
        'subtopic': 'dc'
    },
    # region subtopic actions
    'region_list': {
        'func': region_list,
        'params': ['ids', 'name', 'active_ip_address', 'standby_ip_address', 'sync_status', 'role', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'region'
    },
    'region_query': {
        'func': region_query,
        'params': ['region_id', 'request_url', 'request_method', 'request_body'],
        'subtopic': 'region'
    },
}
