"""
System management related operations
"""

import sys
import os

from pydme.client import DMEAPIClient


def login(client: DMEAPIClient) -> dict:
    """
    Authenticate user login

    Force call client.login() to complete authentication, then get accessSession
    from header, prompt user to configure environment variables to reuse the
    authentication key and avoid repeated logins.

    Args:
        client: DME API client

    Returns:
        {
            accessSession: session token (string), used as X-Auth-Token header in subsequent requests,
        }
    """
    client.login()

    accessSession = client.headers.get("X-Auth-Token", "")
    if accessSession:
        print(f"\nLogin successful!")
        print(f"\nTip: configure environment variable to reuse the authentication key and avoid repeated logins:")
        print("  export DME_API_AUTH_TOKEN='<accessSession>'")

    return {
        'accessSession': accessSession
    }


def logout(client: DMEAPIClient) -> dict:
    """
    Log out the currently logged-in third-party session or normal session.

    Args:
        client: DME API client

    Returns:
        None
    """
    url = "/rest/plat/smapp/v1/sessions"

    response = client.delete(url)
    return response


def reset_password(client: DMEAPIClient, user_name: str, new_value: str,
                   is_initial_password: bool = True) -> dict:
    """
    Reset the password of the specified user by username. Resetting does not
    require the original password. Therefore, the third-party user role calling
    this API must be the security administrator role.

    Args:
        client: DME API client
        user_name: Username whose password needs to be reset (Required, string, 1~128 characters)
        new_value: New password (Required, string, 8~32 characters). Requirements: 1. Password length cannot be less than 8 characters or more than 32 characters. 2. Password must contain at least 2 letters, must contain at least 1 uppercase letter, must contain at least 1 lowercase letter, must contain at least 1 digit, must contain at least 1 special character (!"#$%&'()*+,-./:;<=>?@[]^`{|}~). 3. The same character cannot appear consecutively more than 2 times, and cannot contain repeated character sequences (repeat count 4, repeat sequence character count 1). 4. Password cannot contain the username or its reverse, the user's phone number or email account, or words from the password dictionary.
        is_initial_password: Indicates whether the password must be changed on next login after reset (Required, boolean, true/false). true: must change password on next login; false: can log in directly on next login without changing. Default: true

    Returns:
        None
    """
    url = "/rest/usm/v1/users/{user_name}/reset-credentials"

    # Parameter validation
    if not user_name or len(user_name) > 128:
        raise ValueError("user_name is a required parameter, 1~128 characters")
    if not new_value or len(new_value) < 8 or len(new_value) > 32:
        raise ValueError("new_value is a required parameter, 8~32 characters")

    payload = {
        'newValue': new_value,
        'isInitialPassword': is_initial_password
    }

    response = client.put(url, body=payload, params={"user_name": user_name})
    return response


def user_delete(client: DMEAPIClient, user_id: int) -> dict:
    """
    Delete user. This API may directly or indirectly affect live network
    operations, causing service interruptions or critical data loss.
    Exercise caution.

    Args:
        client: DME API client
        user_id: User ID (Required, integer, 11~2147483647)

    Returns:
        None
    """
    url = "/rest/usermgmt/v1/users/{user_id}"

    # Parameter validation
    if user_id is None:
        raise ValueError("user_id is a required parameter")

    response = client.delete(url, params={"user_id": user_id})
    return response


def user_create(client: DMEAPIClient, name: str, type: int,
                value: str = None, description: str = None,
                roles: list = None) -> dict:
    """
    Create user.

    Args:
        client: DME API client
        name: Username (Required, string, max 32 characters). Local username cannot be less than 6 or more than 32 characters, cannot contain spaces, escape characters, invisible characters or special characters. Remote username cannot be less than 1 or more than 32 characters, cannot contain invisible characters or ; special characters.
        type: User type (Required, integer). 0: local user; 2: remote user.
        value: Password (Optional, string, 8~32 characters). Password length cannot be less than 8 or more than 32 characters. Password must contain at least 2 letters, must contain at least 1 uppercase letter, must contain at least 1 lowercase letter, must contain at least 1 digit, must contain at least 1 special character. Not applicable for remote users.
        description: Description (Optional, string, max 127 characters)
        roles: User roles (Optional, List[integer], max array members: 10). Such as Administrators, Northbound user group, Security administrator group, Filesystem group or user-defined roles.

    Returns:
        None
    """
    url = "/rest/usermgmt/v1/users"

    # Parameter validation
    if not name:
        raise ValueError("name is a required parameter")

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
    """
    Batch query user information.

    Args:
        client: DME API client
        page_no: Page number (Required, integer, min: 1). Default: 1
        page_size: Page size (Required, integer, 5~200). Default: 10
        name: Username search keyword (Optional, string, max 32 characters)

    Returns:
        {
            total: total (integer, max: 5000),
            datas: user data (List<UserData>, max array members: 5000). parameter format: [{
                id: user ID (integer, 1~2147483647),
                name: username (string, 6~32 characters),
                description: description (string, max 127 characters),
                type: user type (integer). valid values: 0 (local user), 1 (third-party system access user), 2 (remote user),
                roles: role ID list (List<integer>, max array members: 50),
            }, ...]
        }
    """
    url = "/rest/usermgmt/v1/users"

    response = client.get(url, params={
        'page_no': page_no,
        'page_size': page_size,
        'name': name
    })
    return response


def role_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 10,
              name: str = None) -> dict:
    """
    Batch query role information.

    Args:
        client: DME API client
        page_no: Page number (Required, integer, min: 1). Default: 1
        page_size: Page size (Required, integer, 5~100). Default: 10
        name: Role name search keyword (Optional, string, max 64 characters)

    Returns:
        {
            total: total (integer, max: 10),
            datas: role data (List<RoleData>, max array members: 5000). parameter format: [{
                id: role ID (integer, 1~2147483647),
                name: role name (string, max 64 characters),
                description: description (string, max 127 characters),
            }, ...]
        }
    """
    url = "/rest/usermgmt/v1/roles"

    response = client.get(url, params={
        'page_no': page_no,
        'page_size': page_size,
        'name': name
    })
    return response


def user_show(client: DMEAPIClient, user_id: int) -> dict:
    """
    Query the specified user information.

    Args:
        client: DME API client
        user_id: User ID (Required, integer, 1~2147483647)

    Returns:
        {
            id: user ID (integer, 1~2147483647),
            name: username (string, max 32 characters),
            type: user type (integer). valid values: 0 (local user), 1 (third-party system access user), 2 (remote user),
            description: description (string, max 127 characters),
            roles: user roles (List<integer>, max array members: 50),
        }
    """
    url = "/rest/usermgmt/v1/users/{user_id}"

    # Parameter validation
    if user_id is None:
        raise ValueError("user_id is a required parameter")

    response = client.get(url, params={"user_id": user_id})
    return response


def show(client: DMEAPIClient) -> dict:
    """
    Query product system information.

    Args:
        client: DME API client

    Returns:
        {
            version: DME product version info (string, max 128 characters),
            sn: DME product SN number (string, max 64 characters),
        }
    """
    url = "/rest/productmgmt/v1/system-info"

    response = client.get(url)
    return response


def certificate(client: DMEAPIClient, service_type: str = "APIGWService") -> dict:
    """
    Get DME certificate.

    Args:
        client: DME API client
        service_type: Service type (Required, string). valid values: APIGWService (DME northbound gateway)

    Returns:
        {
            cert: Base64 encoded certificate file string (string),
        }
    """
    url = "/rest/certmgmt/v1/certs"

    # Parameter validation
    if service_type not in ["APIGWService"]:
        raise ValueError(f"service_type valid values: APIGWService")

    response = client.get(url, params={'service_type': service_type})
    return response


def backup_server_list(client: DMEAPIClient, address: str = None,
                         name: str = None,
                         page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch query backup servers.

    Args:
        client: DME API client
        address: Backup server address, supports IPv4 address, supports fuzzy match (Optional, string, 1~256 characters)
        name: Backup server name (Optional, string)
        page_no: Pagination start page (Optional, int32). Default: 1
        page_size: Items per page (Optional, int32, 1~1000). Default: 20

    Returns:
        {
            total: total backup servers (int32),
            backup_servers: backup server list (List<BackupServerInfo>). parameter format: [{
                id: backup server id (string, 1~64 characters),
            }, ...]
        }
    """
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
    """
    Query todo task group list

    Args:
        client: DME API client
        group_id: Todo task group ID(Optional)
        name: Todo task group name(Optional)
        creator_name: Creator name(Optional)
        is_finished: Whether completed(Optional)
        is_group: Whether group task(Optional)
        start: Pagination start position (Optional, 0~10000000)
        limit: Pagination count (Optional, 1~1000)
        status: Todo task group status list (Optional, 1-pending/2-in progress/3-completed/4-failed)
        todo_item_status: Todo item status list (Optional, 0-to be confirmed/1-incomplete/2-in progress/3-completed)
        start_time_from: Start time lower bound (Optional, format: yyyy-MM-dd HH:mm:ss)
        start_time_to: Start time upper bound (Optional, format: yyyy-MM-dd HH:mm:ss)
        end_time_from: End time lower bound (Optional, format: yyyy-MM-dd HH:mm:ss)
        end_time_to: End time upper bound (Optional, format: yyyy-MM-dd HH:mm:ss)
        sort_key: Sort field(Optional)
        sort_dir: Sort order (Optional, asc/desc)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, including todo task group list and total
    """
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
    """
    Execute todo task group

    Execute the specified todo task group.

    Args:
        client: DME API client
        group_id: Todo task group ID(Required)

    Returns:
        Execution result, including task_id
    """
    url = "/rest/taskmgmt/v1/todo-groups/{group_id}/execute"

    response = client.put(url, body={}, params={"group_id": group_id})
    return response


def todo_task_group_confirm(client: DMEAPIClient, group_id: str) -> dict:
    """
    Confirm execution of scheduled todo task group

    Args:
        client: DME API client
        group_id: Todo task group ID(Required)

    Returns:
        Confirmation result
    """
    url = "/rest/taskmgmt/v1/todo-groups/{group_id}/confirm"

    response = client.put(url, body={}, params={"group_id": group_id})
    return response


# ==================== Todo task management (todo_task subtopic) ====================

def todo_task_list(client: DMEAPIClient, service_type: str,
               status: list = None, page_no: int = None,
               page_size: int = None) -> dict:
    """
    Batch query todo task details

    Batch query the todo item list, supports filtering and pagination.

    Args:
        client: DME API client
        service_type: Service type (Required, wfa_execute_activity-automation orchestration)
        status: Todo item status list (Optional, 1-not executed/2-executing/3-success/4-partial success/5-failure/6-timeout/7-warning/8-failed/9-pending review/10-review rejected/21-pre-checking/22-pre-check failed)
        page_no: Page index (Optional, default 1)
        page_size: Items per page (Optional, 1~10, default 10)

    Returns:
        {
            total: total todo tasks count (integer),
            todo_items: todo task list (List<ItemDetail>). parameter format: [{
                id: todo item ID (string, 1~64 characters),
                name: todo task name (string, 1~128 characters),
                context: todo task context body (string, 1~2097152 characters),
            }, ...],
        }
    """
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
    """
    Query todo item details info

    Query the detailed info of the specified todo item.

    Args:
        client: DME API client
        item_id: Todo item ID(Required)

    Returns:
        {
            item_id: todo item ID (string),
            name: name (string),
            description: description (string),
            group_id: group ID (string),
            service_type: service type (string),
            status: status (string),
            creator_name: creator (string),
            create_time: creation time (string),
            task_id: task ID (string),
            start_time: start time (string),
            end_time: end time (string),
            close_reason: close reason (string),
            suggestion: review comment (string),
        }
    """
    url = "/rest/taskmgmt/v1/todo-items/{item_id}"

    response = client.get(url, params={"item_id": item_id})
    return response


def todo_task_execute(client: DMEAPIClient, item_id: str) -> dict:
    """
    Execute todo task

    Execute the specified todo item.

    Args:
        client: DME API client
        item_id: Todo item ID(Required)

    Returns:
        Execution result, including task_id
    """
    url = "/rest/taskmgmt/v1/todo-items/{item_id}/execute"

    response = client.put(url, body={}, params={"item_id": item_id})
    return response


def todo_task_audit(client: DMEAPIClient, item_id: str, is_approval: bool,
          suggestion: str = None) -> dict:
    """
    Audit todo task

    Audit the todo item (approve or reject).

    Args:
        client: DME API client
        item_id: Todo item ID(Required)
        is_approval: Whether to approve (Required, true-approve/false-reject)
        suggestion: Review suggestion (Optional, 0-63 characters)

    Returns:
        Audit result
    """
    url = "/rest/taskmgmt/v1/todo-items/{item_id}/audit"

    payload = {
        'is_approval': is_approval
    }
    if suggestion is not None:
        payload['suggestion'] = suggestion

    response = client.post(url, body=payload, params={"item_id": item_id})
    return response


def todo_task_revoke(client: DMEAPIClient, item_id: str) -> dict:
    """
    Revoke audit for todo item

    Revoke the audit of the specified todo item.

    Args:
        client: DME API client
        item_id: Todo item ID(Required)

    Returns:
        Revocation result
    """
    url = "/rest/taskmgmt/v1/todo-items/{item_id}/revoke-audit"

    response = client.put(url, body={}, params={"item_id": item_id})
    return response


def todo_task_close(client: DMEAPIClient, item_id: str, reason: str) -> dict:
    """
    Close todo task

    Close the specified todo item, requires a reason.

    Args:
        client: DME API client
        item_id: Todo item ID(Required)
        reason: Close reason (Required, 0-63 characters)

    Returns:
        Close result
    """
    url = "/rest/taskmgmt/v1/todo-items/{item_id}/close"

    payload = {
        'reason': reason
    }

    response = client.put(url, body=payload, params={"item_id": item_id})
    return response


# ==================== Task management (task subtopic) ====================

import time

def task_show(client: DMEAPIClient, task_id: str) -> list:
    """
    Query specified task details

    Query by the unique task identifier TaskId.

    Args:
        client: DME API client
        task_id: Task ID (Required, 1~36 characters)

    Returns:
        {
            id: task ID (string),
            name_en: task English name (string),
            name_cn: task Chinese name (string),
            description: task description (string),
            parent_id: parent task ID (string),
            seq_no: task sequence number (string),
            status: status. valid values: 1 (initial status), 2 (executing), 3 (success), 4 (partial success), 5 (failure), 6 (timeout),
            progress: task progress (string),
            owner_name: task creator username (string),
            owner_id: task creator user ID (string),
            create_time: task creation time (string, UTC milliseconds),
            start_time: task start time (string, UTC milliseconds),
            end_time: task end time (string, UTC milliseconds),
            detail_en: task English details (string),
            detail_cn: task Chinese details (string),
            is_support_retry: whether retry is supported (boolean),
            is_support_rollback: whether rollback is supported (boolean),
            remarks: remarks info (string),
            resources: list of resources associated with the task (List<AffectedResource>). parameter format: [{
                operate: operation type (string),
                type: resource type (string),
                id: resource ID (string),
                name: resource name (string),
            }, ...],
        }
    """
    url = "/rest/taskmgmt/v1/tasks/{task_id}"

    response = client.get(url, params={"task_id": task_id})
    return response


def task_list(client: DMEAPIClient, start: int = 1, limit: int = 100,
               task_name: str = None, status: int = None,
               owner_id: str = None, create_time_from: int = None,
               create_time_to: int = None) -> dict:
    """
    Batch query tasks

    Args:
        client: DME API client
        start: Pagination start position, default 1
        limit: Pagination count, default 100
        task_name: Task name filter(Optional)
        status: Status filter (Optional, 1-initial status;2-executing;3-success;4-partial success;5-failure;6-timeout)
        owner_id: Task creator user ID filter(Optional)
        create_time_from: Creation time lower bound (Optional, UTC milliseconds)
        create_time_to: Creation time upper bound (Optional, UTC milliseconds)

    Returns:
        {
            total: total tasks (int32),
            tasks: task list (List<TaskDetail>). parameter format: [{
                id: task ID (string),
                name_en: task English name (string),
                status: status (string),
                progress: task progress (string),
                owner_name: task creator username (string),
                create_time: creation time (string),
                start_time: start time (string),
                end_time: end time (string),
            }, ...],
        }
    """
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
    """
    Retry task

    Retry the specified task, used when the task was not fully successful.

    Args:
        client: DME API client
        task_id: Task ID (Required, 1~36 characters)

    Returns:
        Retry result
    """
    url = "/rest/taskmgmt/v1/tasks/{task_id}/retry"

    response = client.post(url, body={}, params={"task_id": task_id})
    return response


def task_wait(client: DMEAPIClient, task_id: str, timeout: int = 300,
              poll_interval: int = 2) -> dict:
    """
    Wait for task completion

    Call DMEAPIClient.get_task_result to poll task status until completion or timeout.
    Warning(7) status is also considered as task completed.

    Args:
        client: DME API client
        task_id: Task ID (Required, 1~36 characters)
        timeout: Timeout in seconds, default 300 seconds. Poll count = timeout / poll_interval
        poll_interval: Poll interval in seconds, default 2 seconds

    Returns:
        {
            id: task ID (string),
            status: task status (integer). valid values: 3 (success), 4 (partial success), 5 (failure), 6 (timeout), 7 (warning),
            progress: task progress (integer, 0~100),
            name_en: task English name (string),
            name_cn: task Chinese name (string),
            resources: list of resources associated with the task (List<AffectedResource>). parameter format: [{
                operate: operation type (string). valid values: CREATE, MODIFY, DELETE,
                type: affected resource type (string),
                id: affected resource ID (string),
                name: affected resource name (string),
            }, ...],
        }

    Raises:
        Exception: Task query timeout (exceeded poll count without completion)
    """
    retry_times = max(1, timeout // poll_interval)
    return client.get_task_result(
        task_id,
        retry_times=retry_times,
        retry_interval=poll_interval,
    )


# ==================== Tag type management (tag_type subtopic) ====================

def tag_type_create(client: DMEAPIClient, name: str, description: str = None) -> dict:
    """
    Create tag type

    Args:
        client: DME API client
        name: tag type name(Required)
        description: tag type description(Optional)

    Returns:
        {
            id: tag type ID (string),
            name: tag type name (string),
        }
    """
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
    """
    Batch query tag types

    Args:
        client: DME API client
        start: Pagination start position, default 1
        limit: Pagination count, default 100
        name: tag type name filter(Optional)

    Returns:
        {
            total: total tag types (int32),
            datas: tag type list (List<TagType>). parameter format: [{
                id: tag type ID (string),
                name: tag type name (string),
            }, ...],
        }
    """
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
    """
    Modify tag type

    Args:
        client: DME API client
        tag_type_id: tag type ID(Required)
        name: tag type name(Optional)
        description: tag type description(Optional)

    Returns:
        {
            id: tag type ID (string),
            name: tag type name (string),
        }
    """
    url = "/rest/tagmgmt/v1/tag-types/{tag_type_id}"

    payload = {}

    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description

    response = client.put(url, body=payload, params={"tag_type_id": tag_type_id})
    return response


def tag_type_delete(client: DMEAPIClient, tag_type_ids: list) -> dict:
    """
    Batch delete tag types

    Args:
        client: DME API client
        tag_type_ids: tag type ID list(Required)

    Returns:
        Batch delete result
    """
    url = "/rest/tagmgmt/v1/tag-types/delete"

    payload = {
        'ids': tag_type_ids
    }

    response = client.post(url, body=payload)
    return response


# ==================== Tag management (tag subtopic) ====================

def tag_create(client: DMEAPIClient, name: str, tag_type_id: str,
                tag_type_name: str = None, description: str = None, color: str = None) -> dict:
    """
    Create tag

    Args:
        client: DME API client
        name: tag name(Required)
        tag_type_id: tag type ID(Required)
        tag_type_name: tag type name (API requires)
        description: tag description(Optional)
        color: tag color(Optional)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
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
    """
    Batch query tags

    Args:
        client: DME API client
        start: Pagination start position, default 1
        limit: Pagination count, default 100
        name: tag name filter(Optional)
        tag_type_id: tag type ID filter(Optional)

    Returns:
        {
            total: total tags (int32),
            datas: tag list (List<Tag>). parameter format: [{
                id: tag ID (string),
                name: tag name (string),
                tag_type_name: tag type name (string),
            }, ...],
        }
    """
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
    """
    Modify tag

    Args:
        client: DME API client
        tag_id: tag ID(Required)
        name: tag name(Optional)
        description: tag description(Optional)
        color: tag color(Optional)

    Returns:
        {
            id: tag ID (string),
            name: tag name (string),
        }
    """
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
    """
    Batch delete tags

    Args:
        client: DME API client
        tag_ids: tag ID list(Required)

    Returns:
        Batch delete result
    """
    url = "/rest/tagmgmt/v1/tags/delete"

    payload = {
        'ids': tag_ids
    }

    response = client.post(url, body=payload)
    return response


def tag_bind(client: DMEAPIClient, tag_id: str, resources: list) -> dict:
    """
    Associate resources with tag

    Args:
        client: DME API client
        tag_id: Tag ID (Required, 32-bit hex string, pattern ^[a-fA-F0-9]{32}$)
        resources: Resource list (List<TagResource>, Required, min array items: 1, max array members: 100). parameter format: [{
            resource_type: resource type (Required, string, 1~128 characters). valid values: storage_device (Storage device), backup_medium (Backup storage), fc_switch (Fiber Channel switch), protect_appliance (A8000 backup appliance), security_appliance (Data security appliance), ethernet_switch (Ethernet switch), physical_server (Server), virtual_machine (Virtual machine), logic_port (Logic port), file_system (Filesystem),
            resource_id: resource ID (Required, string, UUID format or 32-bit hex string, pattern ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$),
        }, ...]

    Returns:
        Asynchronous task created successfully, returns task ID.
    """
    url = "/rest/tagmgmt/v1/tags/{tag_id}/associate-resources"

    payload = {
        'resources': resources
    }

    response = client.post(url, body=payload, params={"tag_id": tag_id})
    return response


def tag_unbind(client: DMEAPIClient, tag_id: str, resources: list) -> dict:
    """
    Disassociate resources from tag

    Args:
        client: DME API client
        tag_id: Tag ID (Required, 32-bit hex string, pattern ^[a-fA-F0-9]{32}$)
        resources: Resource list (List<TagResource>, Required, min array items: 1, max array members: 100). parameter format: [{
            resource_type: resource type (Required, string, 1~128 characters). valid values: storage_device (Storage device), backup_medium (Backup storage), fc_switch (Fiber Channel switch), protect_appliance (A8000 backup appliance), security_appliance (Data security appliance), ethernet_switch (Ethernet switch), physical_server (Server), virtual_machine (Virtual machine), logic_port (Logic port), file_system (Filesystem),
            resource_id: resource ID (Required, string, UUID format or 32-bit hex string, pattern ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$),
        }, ...]

    Returns:
        Asynchronous task created successfully, returns task ID.
    """
    url = "/rest/tagmgmt/v1/tags/{tag_id}/disassociate-resources"

    payload = {
        'resources': resources
    }

    response = client.post(url, body=payload, params={"tag_id": tag_id})
    return response


# ==================== Availability zone management (az subtopic) ====================

def az_list(client: DMEAPIClient, az_name: str = None, operate_status: str = None,
         start: int = 1, limit: int = 512, is_sc: bool = False) -> dict:
    """
    Batch query availability zones.

    Args:
        client: DME API client
        az_name: Availability zone name, supports fuzzy match (Optional, string, 1~64 characters)
        operate_status: Availability zone operation status. For an AZ that is not online, its operate_status is null, so currently only filtering online AZs is supported (Optional, string, 1~16 characters)
        start: Page number, starting from 1 (Optional, int32, 1~10000000). Default: 1
        limit: Page size (Optional, int32, 1~512). Default: 512
        is_sc: Whether querying from the operations side (Optional, boolean, true/false). Default: false

    Returns:
        {
            total: total availability zones (integer),
            az_list: availability zone list (List<GetAzResponse>). parameter format: [{
                id: availability zone id (string),
                name: availability zone name (string),
                description: availability zone description (string),
                operate_status: availability zone operation status (string). default value: offline,
                site_urn: site urn (string, 1~64 characters),
            }, ...]
        }
    """
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
    """
    Get data center list

    Query data center list, supports filtering by name and pagination.

    Args:
        client: DME API client
        name: Data center name (Optional, supports fuzzy query)
        page_no: Pagination start page, default 1
        page_size: Items per page, 1~1000, default 20

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, includes total and datacenters fields
    """
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
    """
    Get data center details

    Query the detailed info of the specified data center.

    Args:
        client: DME API client
        dc_id: Data center ID(Required)

    Returns:
        {
            id: data center ID (string),
            name: name (string),
            description: description (string),
            longitude: longitude (number),
            latitude: latitude (number),
            device_num: device count (int32),
            critical_num: critical alarm count (int32),
            major_num: major alarm count (int32),
            minor_num: minor alarm count (int32),
            info_num: info alarm count (int32),
            total_cpu: total CPU (int32),
            allocated_cpu: allocated CPU (int32),
            total_memory: total memory (int32),
            allocated_memory: allocated memory (int32),
            storage_total_usable_capacity: total usable storage capacity (int64),
            storage_total_used_capacity: used storage capacity (int64),
        }
    """
    url = "/rest/dcmgmt/dcmgmtservice/v1/datacenters/{dc_id}"

    response = client.get(url, params={"dc_id": dc_id})
    return response


def dc_show_devices(client: DMEAPIClient, dc_id: str,
                 device_type: list = None, page_no: int = 1,
                 page_size: int = 20) -> dict:
    """
    Query device list info of the specified data center

    Args:
        client: DME API client
        dc_id: Data center ID(Required)
        device_type: Device type list(Optional)
                     values: server, storage, network, switch, router, firewall,
                         loadbalancer, firewall_cluster, ipswitch, other
        page_no: Pagination start page, default 1
        page_size: Items per page, 1~1000, default 20

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, includes device list
    """
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
    """
    Batch query Regions.

    Args:
        client: DME API client
        ids: Region ID list, supports exact match (Optional, List[string], max array members: 100)
        name: Region name, supports fuzzy search (Optional, string, max 256 characters)
        active_ip_address: Region active IP address, supports fuzzy search (Optional, string, max 256 characters)
        standby_ip_address: Region standby IP address, supports fuzzy search (Optional, string, max 256 characters)
        sync_status: Region sync status, exact filter (Optional, List[string], max array members: 3). valid values: normal (normal), sync (syncing), failed (sync failed)
        role: Region role, exact filter (Optional, string). valid values: parent (parent Region), child (child Region)
        sort_key: Sort field (Optional, string). valid values: last_sync_time (last sync time)
        sort_dir: Sort direction (Optional, string). valid values: asc (ascending), desc (descending). default value: desc
        page_no: Start page for pagination query (Optional, int32, 1~100). default value: 1
        page_size: Items per page (Optional, int32, 1~100). default value: 20

    Returns:
        {
            total: total (integer),
            regions: Region list. parameter format: [{
                id: Region ID (string),
                name: Region name (string),
                role: Region role (string),
                sync_status: sync status (string),
            }, ...],
        }
    """
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
    """
    Query child Region resource info.

    Args:
        client: DME API client
        region_id: Child Region ID (Required, string, 1~64 characters)
        request_url: URL for querying child region northbound API (Required, string, 1~8192 characters)
        request_method: Request method (Required, string). valid values: get (Get request), post (Post request)
        request_body: Request body for calling child northbound API (Optional, string, 1~20480 characters)

    Returns:
        None
    """
    url = "/rest/regionmgmt/v1/regions/{region_id}/resources/query"

    if not region_id:
        raise ValueError("region_id is a required parameter")
    if not request_url:
        raise ValueError("request_url is a required parameter")

    payload = {
        'request_url': request_url,
        'request_method': request_method
    }
    if request_body is not None:
        payload['request_body'] = request_body

    response = client.post(url, body=payload, params={"region_id": region_id})
    return response


# action list, for CLI help
ACTIONS = {
    # Direct actions (two-level structure)
    'login': {
        'func': login,
        'description': 'Authenticate user login',
        'params': ['username', 'password', 'grant_type'],
        'subtopic': None
    },
    'logout': {
        'func': logout,
        'description': 'Log out session',
        'params': [],
        'subtopic': None
    },
    'show': {
        'func': show,
        'description': 'Query product system info',
        'params': [],
        'subtopic': None
    },
    'certificate': {
        'func': certificate,
        'description': 'Get DME certificate',
        'params': [],
        'subtopic': None
    },
    'reset_password': {
        'func': reset_password,
        'description': 'Reset password',
        'params': ['user_name', 'new_value', 'is_initial_password'],
        'subtopic': None
    },
    # subtopic action - user (three-level structure)
    'user_list': {
        'func': user_list,
        'description': 'Batch query user info',
        'params': ['page_no', 'page_size', 'name'],
        'subtopic': 'user'
    },
    'user_show': {
        'func': user_show,
        'description': 'Query specified user info',
        'params': ['user_id'],
        'subtopic': 'user'
    },
    'user_create': {
        'func': user_create,
        'description': 'Create user',
        'params': ['name', 'type', 'value', 'description', 'roles'],
        'subtopic': 'user'
    },
    'user_delete': {
        'func': user_delete,
        'description': 'Delete user',
        'params': ['user_id'],
        'subtopic': 'user'
    },
    # subtopic action - role (three-level structure)
    'role_list': {
        'func': role_list,
        'description': 'Batch query role info',
        'params': ['page_no', 'page_size', 'name'],
        'subtopic': 'role'
    },
    # subtopic action - backup_server (three-level structure)
    'backup_server_list': {
        'func': backup_server_list,
        'description': 'Batch query backup servers',
        'params': ['address', 'name', 'page_no', 'page_size'],
        'subtopic': 'backup_server'
    },
    # subtopic action - todo_task_group (three-level structure)
    'todo_task_group_list': {
        'func': todo_task_group_list,
        'description': 'Query todo task group list',
        'params': ['group_id', 'name', 'creator_name', 'is_finished', 'is_group',
                   'start', 'limit', 'status', 'todo_item_status',
                   'start_time_from', 'start_time_to', 'end_time_from',
                   'end_time_to', 'sort_key', 'sort_dir'],
        'subtopic': 'todo_task_group'
    },
    'todo_task_group_execute': {
        'func': todo_task_group_execute,
        'description': 'Execute todo task group',
        'params': ['group_id'],
        'subtopic': 'todo_task_group'
    },
    'todo_task_group_confirm': {
        'func': todo_task_group_confirm,
        'description': 'Confirm scheduled todo task group execution',
        'params': ['group_id'],
        'subtopic': 'todo_task_group'
    },
    # subtopic action - todo_task (three-level structure)
    'todo_task_list': {
        'func': todo_task_list,
        'description': 'Query todo task list',
        'params': ['service_type', 'status', 'page_no', 'page_size'],
        'subtopic': 'todo_task'
    },
    'todo_task_show': {
        'func': todo_task_show,
        'description': 'Query todo task details',
        'params': ['item_id'],
        'subtopic': 'todo_task'
    },
    'todo_task_execute': {
        'func': todo_task_execute,
        'description': 'Execute todo task',
        'params': ['item_id'],
        'subtopic': 'todo_task'
    },
    'todo_task_audit': {
        'func': todo_task_audit,
        'description': 'Audit todo task',
        'params': ['item_id', 'is_approval', 'suggestion'],
        'subtopic': 'todo_task'
    },
    'todo_task_revoke': {
        'func': todo_task_revoke,
        'description': 'Revoke audit for todo item',
        'params': ['item_id'],
        'subtopic': 'todo_task'
    },
    'todo_task_close': {
        'func': todo_task_close,
        'description': 'Close todo task',
        'params': ['item_id', 'reason'],
        'subtopic': 'todo_task'
    },
    # subtopic action - task (three-level structure)
    'task_show': {
        'func': task_show,
        'description': 'Query specified task details',
        'params': ['task_id'],
        'subtopic': 'task'
    },
    'task_list': {
        'func': task_list,
        'description': 'Batch query tasks',
        'params': ['start', 'limit', 'task_name', 'status', 'owner_id', 'create_time_from', 'create_time_to'],
        'subtopic': 'task'
    },
    'task_retry': {
        'func': task_retry,
        'description': 'Retry task',
        'params': ['task_id'],
        'subtopic': 'task'
    },
    'task_wait': {
        'func': task_wait,
        'description': 'Wait for task completion',
        'params': ['task_id', 'timeout', 'poll_interval'],
        'subtopic': 'task'
    },
    # subtopic action - tag_type (three-level structure)
    'tag_type_create': {
        'func': tag_type_create,
        'description': 'Create tag type',
        'params': ['name', 'description'],
        'subtopic': 'tag_type'
    },
    'tag_type_list': {
        'func': tag_type_list,
        'description': 'Batch query tag types',
        'params': ['start', 'limit', 'name'],
        'subtopic': 'tag_type'
    },
    'tag_type_modify': {
        'func': tag_type_modify,
        'description': 'Modify tag type',
        'params': ['tag_type_id', 'name', 'description'],
        'subtopic': 'tag_type'
    },
    'tag_type_delete': {
        'func': tag_type_delete,
        'description': 'Batch delete tag types',
        'params': ['tag_type_ids'],
        'subtopic': 'tag_type'
    },
    # subtopic action - tag (three-level structure)
    'tag_create': {
        'func': tag_create,
        'description': 'Create tag',
        'params': ['name', 'tag_type_id', 'tag_type_name', 'description', 'color'],
        'subtopic': 'tag'
    },
    'tag_list': {
        'func': tag_list,
        'description': 'Batch query tags',
        'params': ['start', 'limit', 'name', 'tag_type_id'],
        'subtopic': 'tag'
    },
    'tag_modify': {
        'func': tag_modify,
        'description': 'Modify tag',
        'params': ['tag_id', 'name', 'description', 'color'],
        'subtopic': 'tag'
    },
    'tag_delete': {
        'func': tag_delete,
        'description': 'Batch delete tags',
        'params': ['tag_ids'],
        'subtopic': 'tag'
    },
    'tag_bind': {
        'func': tag_bind,
        'description': 'Associate resources with tag',
        'params': ['tag_id', 'resources'],
        'subtopic': 'tag'
    },
    'tag_unbind': {
        'func': tag_unbind,
        'description': 'Disassociate resources from tag',
        'params': ['tag_id', 'resources'],
        'subtopic': 'tag'
    },
    # subtopic action - az (three-level structure)
    'az_list': {
        'func': az_list,
        'description': 'Batch query availability zones',
        'params': ['az_name', 'operate_status', 'start', 'limit', 'is_sc'],
        'subtopic': 'az'
    },
    # subtopic action - dc (three-level structure)
    'dc_list': {
        'func': dc_list,
        'description': 'Get data center list',
        'params': ['name', 'page_no', 'page_size'],
        'subtopic': 'dc'
    },
    'dc_show': {
        'func': dc_show,
        'description': 'Get data center details',
        'params': ['dc_id'],
        'subtopic': 'dc'
    },
    'dc_show_devices': {
        'func': dc_show_devices,
        'description': 'Query device list info of specified data center',
        'params': ['dc_id', 'device_type', 'page_no', 'page_size'],
        'subtopic': 'dc'
    },
    # region subtopic action
    'region_list': {
        'func': region_list,
        'description': 'Batch query Regions',
        'params': ['ids', 'name', 'active_ip_address', 'standby_ip_address', 'sync_status', 'role', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'region'
    },
    'region_query': {
        'func': region_query,
        'description': 'Query child Region resource info',
        'params': ['region_id', 'request_url', 'request_method', 'request_body'],
        'subtopic': 'region'
    },
}
