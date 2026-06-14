"""
System management (System) operations
"""

import sys
import os

from pydme.client import DMEAPIClient


def login(client: DMEAPIClient) -> dict:
    """
    Auth user login

    Force call client.login()  completed auth,  then from header get accessSession, 
    Prompt user to configure env vars to reuse auth token, Avoid duplicate login. 

    Args:
        client: DME API client

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes  accessSession
        - accessSession: session token, for subsequent requests X-Auth-Token header
    """
    client.login()

    accessSession = client.headers.get("X-Auth-Token", "")
    if accessSession:
        print('\nLogin successful!')
        print('\nTip: Configure env vars to reuse auth token to avoid duplicate login:')
        print("  export DME_API_AUTH_TOKEN='<accessSession>'")

    return {
        'accessSession': accessSession
    }


def logout(client: DMEAPIClient) -> dict:
    """
    Logout current third-party or normal session. 

    Args:
        client: DME API client

    Returns:
        N/A
    """
    url = "/rest/plat/smapp/v1/sessions"
    
    response = client.delete(url)
    return response


def reset_password(client: DMEAPIClient, user_name: str, new_value: str,
                   is_initial_password: bool = True) -> dict:
    """
     Reset specified user password by username, Reset without original password. Third-party user executing this API must have security admin role.ng this API must have security roleAdmin role. 

    Args:
        client: DME API client
        user_name: Password reset requiredUsername (Required, string, 1~128 characters)
        new_value:  New password (Required, string, 8~32 characters). Requirements: 1. Password length must not be less than8 characters, and not greater than 32 characters. 2. Password must contain at least2 letters, must contain at least1uppercase letters, must contain at least1lowercase letters, must contain at least1count字, must contain at least1special characters (!"#$%&'()*+,-./:;<=>?@[]^`{|}~) . 3. Consecutive identical character count in passwordcannot exceed2, Cannot contain repeated character sequences ( repeat count is4, Consecutive character count1) . 4. Password cannot containUsername和Username reverse order, Cannot contain phone number or email, Cannot contain dictionary words. 
        is_initial_password: Flag whether password must be changed on next login after reset (Required, boolean, true,false). true: Must perform initial password change on next login; false: Direct login next time, No initial modification required. Default: true

    Returns:
        N/A
    """
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
    """
    Delete user. This API may directly or indirectly affect production services, causing service interruption or data loss. Proceed with caution.. 

    Args:
        client: DME API client
        user_id: user ID (Required, integer, 11~2147483647)

    Returns:
        N/A
    """
    url = "/rest/usermgmt/v1/users/{user_id}"

    # Parameter validation
    if user_id is None:
        raise ValueError("user_id is required")

    response = client.delete(url, params={"user_id": user_id})
    return response


def user_create(client: DMEAPIClient, name: str, type: int,
                value: str = None, description: str = None,
                roles: list = None) -> dict:
    """
    Create user. 

    Args:
        client: DME API client
        name: Username (Required, string,  max 32 characters). Local username cannot be less than6 characters, and not greater than 32 characters, Cannot contain spaces, 转义 character, Invisible and special characters. remote Usernamecannot be less than1 characters, and not greater than 32 characters, Cannot contain invisible characters;特殊 character. 
        type: User type (Required, integer, N/A). 0: Local user; 2: Remote user. 
        value: Password (Optional, string, 8~32 characters). Password length cannot be less than8 characters, and not greater than 32 characters. Password must contain at least2 letters, must contain at least1uppercase letters, must contain at least1lowercase letters, must contain at least1count字, must contain at least1special characters. Remote user not involve. 
        description:  description (Optional, string,  max127 characters)
        roles: User role (Optional, List[integer], max array members: 10). E.g., Administrators, northbound user group, security admin group, filesystemGroup or custom user role. 

    Returns:
        N/A
    """
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
    """
    Batch queryUser info. 

    Args:
        client: DME API client
        page_no: Page number (Required, integer, min: 1). Default: 1
        page_size: Page size (Required, integer, 5~200). Default: 10
        name: UsernameSearch keyword (Optional, string,  max 32 characters)

    Returns:
        {
            total: Total count (integer, max: 5000),
            datas: User data (List<UserData>, max array members: 5000). 参数格式如下：[{
                id: user ID (integer, 1~2147483647),
                name: Username (string, 6~32 characters),
                description:  description (string,  max127 characters),
                type: User type (integer). Options: 0 (Local user), 1 (Third-party system access user), 2 (Remote user),
                roles:  roleID list (List<integer>, max array members: 50),
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
    Batch queryRole info. 

    Args:
        client: DME API client
        page_no: Page number (Required, integer, min: 1). Default: 1
        page_size: Page size (Required, integer, 5~100). Default: 10
        name: Role name search keyword (Optional, string,  max64 characters)

    Returns:
        {
            total: Total count (integer, max: 10),
            datas: Role data (List<RoleData>, max array members: 5000). 参数格式如下：[{
                id:  roleID (integer, 1~2147483647),
                name:  role name (string,  max64 characters),
                description:  description (string,  max127 characters),
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
    QueryUser info. 

    Args:
        client: DME API client
        user_id: user ID (Required, integer, 1~2147483647)

    Returns:
        {
            id: user ID (integer, 1~2147483647),
            name: Username (string,  max 32 characters),
            type: User type (integer). Options: 0 (Local user), 1 (Third-party system access user), 2 (Remote user),
            description:  description (string,  max127 characters),
            roles: User role (List<integer>, max array members: 50),
        }
    """
    url = "/rest/usermgmt/v1/users/{user_id}"
    
    # Parameter validation
    if user_id is None:
        raise ValueError("user_id is required")

    response = client.get(url, params={"user_id": user_id})
    return response


def show(client: DMEAPIClient) -> dict:
    """
    Query product system info. 

    Args:
        client: DME API client

    Returns:
        {
            version: DME productVersion info (string,  max128 characters),
            sn: DME product serial number (string,  max64 characters),
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
        service_type: Service type (Required, string). Options: APIGWService (DME northbound gateway)

    Returns:
        {
            cert: Certificate file Base64-encoded string (string),
        }
    """
    url = "/rest/certmgmt/v1/certs"

    # Parameter validation
    if service_type not in ["APIGWService"]:
        raise ValueError("service_type options: APIGWService")

    response = client.get(url, params={'service_type': service_type})
    return response


def backup_server_list(client: DMEAPIClient, address: str = None,
                         name: str = None,
                         page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch query backup servers. 

    Args:
        client: DME API client
        address: Backup server address,  supportIPv4 address, supports fuzzy match (Optional, string, 1~256 characters)
        name: Backup server name (Optional, string)
        page_no: Page queryStart page (Optional, int32). Default: 1
        page_size: per pagecount (Optional, int32, 1~1000). Default: 20

    Returns:
        {
            total: Backup serverTotal count (int32),
            backup_servers:  backupServer list (List<BackupServerInfo>). 参数格式如下：[{
                id: Backup serverid (string, 1~64 characters),
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


# ==================== Pending task groupmanagement  (todo_task_group Subtopic)  ====================

def todo_task_group_list(client: DMEAPIClient, group_id: str = None, name: str = None,
               creator_name: str = None, is_finished: bool = None,
               is_group: bool = None, start: int = None, limit: int = None,
               status: list = None, todo_item_status: list = None,
               start_time_from: str = None, start_time_to: str = None,
               end_time_from: str = None, end_time_to: str = None,
               sort_key: str = None, sort_dir: str = None) -> dict:
    """
     queryPending task group list

    Args:
        client: DME API client
        group_id: Pending task group ID (Optional) 
        name: Pending task group name (Optional) 
        creator_name: Creator name (Optional) 
        is_finished:  whetherCompleted (Optional) 
        is_group: Group task (Optional) 
        start: paginationStart position (Optional, 0~10000000) 
        limit: paginationcount (Optional, 1~1000) 
        status: Pending task group status list (Optional, 1-Pending, 2-Executing, 3-Completed, 4-Disabled) 
        todo_item_status: Pending item status list (Optional, 0-Pending confirm, 1-Incomplete, 2-Executing, 3-Completed) 
        start_time_from: Start time start value (Optional,  format: yyyy-MM-dd HH:mm:ss) 
        start_time_to: Start time end value (Optional,  format: yyyy-MM-dd HH:mm:ss) 
        end_time_from: End time start value (Optional,  format: yyyy-MM-dd HH:mm:ss) 
        end_time_to: End time end value (Optional,  format: yyyy-MM-dd HH:mm:ss) 
        sort_key: Sort field (Optional) 
        sort_dir: Sort method (Optional, asc/desc) 

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes pending task group list and total count
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
     executePending task group

    Execute specifiedPending task group. 

    Args:
        client: DME API client
        group_id: Pending task group ID (Required) 

    Returns:
        Execution result, includes  task_id
    """
    url = "/rest/taskmgmt/v1/todo-groups/{group_id}/execute"

    response = client.put(url, body={}, params={"group_id": group_id})
    return response


def todo_task_group_confirm(client: DMEAPIClient, group_id: str) -> dict:
    """
    Confirm scheduled executionPending task group

    Args:
        client: DME API client
        group_id: Pending task group ID (Required) 

    Returns:
        确认 result
    """
    url = "/rest/taskmgmt/v1/todo-groups/{group_id}/confirm"

    response = client.put(url, body={}, params={"group_id": group_id})
    return response


# ==================== Pending task management (todo_task Subtopic)  ====================

def todo_task_list(client: DMEAPIClient, service_type: str,
               status: list = None, page_no: int = None,
               page_size: int = None) -> dict:
    """
    Batch query待办Task details

    Batch queryPending item list, supports filtering和pagination. 

    Args:
        client: DME API client
        service_type: Business type (Required, wfa_execute_activity- auto orchestration) 
        status: Pending item status list (Optional, 1-未 execute/2-Executing/3- success/4-partial success/5- failure/6- timeout/7- warning/8-已 disable/9- pending review/10-Review rejected/21- pre-checking/22- pre-check failure) 
        page_no: Page index (Optional, default 1) 
        page_size: per pagecount (Optional, 1~10, default 10) 

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes Pending item list和Total count
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
     queryPending itemDetails info

    QueryPending item的Details. 

    Args:
        client: DME API client
        item_id: Pending item ID (Required) 

    Returns:
        Pending itemDetails
    """
    url = "/rest/taskmgmt/v1/todo-items/{item_id}"

    response = client.get(url, params={"item_id": item_id})
    return response


def todo_task_execute(client: DMEAPIClient, item_id: str) -> dict:
    """
    Execute pending task

    Execute specifiedPending item. 

    Args:
        client: DME API client
        item_id: Pending item ID (Required) 

    Returns:
        Execution result, includes  task_id
    """
    url = "/rest/taskmgmt/v1/todo-items/{item_id}/execute"

    response = client.put(url, body={}, params={"item_id": item_id})
    return response


def todo_task_audit(client: DMEAPIClient, item_id: str, is_approval: bool,
          suggestion: str = None) -> dict:
    """
    Review pending task

    对Pending itemReview ( approve or reject) . 

    Args:
        client: DME API client
        item_id: Pending item ID (Required) 
        is_approval:  whether批准 (Required, true-批准/false- reject) 
        suggestion: Review suggestion (Optional, 0-63  character) 

    Returns:
        审核 result
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
    Cancel review pending item

     revoke specifiedPending item review. 

    Args:
        client: DME API client
        item_id: Pending item ID (Required) 

    Returns:
        撤销 result
    """
    url = "/rest/taskmgmt/v1/todo-items/{item_id}/revoke-audit"

    response = client.put(url, body={}, params={"item_id": item_id})
    return response


def todo_task_close(client: DMEAPIClient, item_id: str, reason: str) -> dict:
    """
    Close pending task

     disable specified的Pending item, must provideShutdown reason. 

    Args:
        client: DME API client
        item_id: Pending item ID (Required) 
        reason: Shutdown reason (Required, 0-63  character) 

    Returns:
         disable result
    """
    url = "/rest/taskmgmt/v1/todo-items/{item_id}/close"

    payload = {
        'reason': reason
    }

    response = client.put(url, body=payload, params={"item_id": item_id})
    return response


# ==================== task management  (task Subtopic)  ====================

import time

def task_show(client: DMEAPIClient, task_id: str) -> list:
    """
    QueryTask details
    
    By taskUnique identifier TaskId 进行 query. 
    
    Args:
        client: DME API client
        task_id: task  ID (Required, 1~36  characters) 
    
    Returns:
        Task details list, includes : 
        - id: task  ID
        - name_en: Task name in English
        - name_cn: Task name in Chinese
        - description: task  description
        - parent_id: 父task  ID
        - seq_no: task 序号
        - status:  status (1-Initial status;2-Executing;3- success;4-partial success;5- failure;6- timeout) 
        - progress: task 进度
        - owner_name: Create task user name
        - owner_id: Create task user ID
        - create_time: Task creation时间 (UTC 毫second(s)数) 
        - start_time: task Start time (UTC 毫second(s)数) 
        - end_time: task End time (UTC 毫second(s)数) 
        - detail_en: Task details in English
        - detail_cn: Task details in Chinese
        - is_support_retry: supports retry
        - is_support_rollback: supports rollback
        - remarks: Remark
        - resources: task  associated的Resource list
    """
    url = "/rest/taskmgmt/v1/tasks/{task_id}"
    
    response = client.get(url, params={"task_id": task_id})
    return response


def task_list(client: DMEAPIClient, start: int = 1, limit: int = 100,
               task_name: str = None, status: int = None,
               owner_id: str = None, create_time_from: int = None,
               create_time_to: int = None) -> dict:
    """
    Batch querytask 
    
    Args:
        client: DME API client
        start: paginationStart position, default 1
        limit: Page size, default 100
        task_name: Task name filter (Optional) 
        status:  status filter (Optional, 1-Initial status;2-Executing;3- success;4-partial success;5- failure;6- timeout) 
        owner_id: Create task user ID  filter (Optional) 
        create_time_from: Creation time起始 (Optional, UTC 毫second(s)数) 
        create_time_to: Creation time end (Optional, UTC 毫second(s)数) 
    
    Returns:
        Task list
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

    Retry specified task, For retrying partially successful tasks. 

    Args:
        client: DME API client
        task_id: task  ID (Required, 1~36  characters) 

    Returns:
         retry result
    """
    url = "/rest/taskmgmt/v1/tasks/{task_id}/retry"

    response = client.post(url, body={}, params={"task_id": task_id})
    return response


def task_wait(client: DMEAPIClient, task_id: str, timeout: int = 300,
              poll_interval: int = 2) -> dict:
    """
    Wait for task completion

    Poll task status, Until task completes or times out. 

    Args:
        client: DME API client
        task_id: task  ID
        timeout: timeout (second(s)) , default 300 second(s)
        poll_interval:  poll间隔 (second(s)) , default 2 second(s)

    Returns:
        Task final status details
        status 说明: 
        - 3:  success
        - 4: partial success
        - 5:  failure
        - 6:  timeout
    """
    start_time = time.time()

    while True:
        task_info = task_show(client, task_id)

        # API Returns a list, get根Task details
        for task in task_info:
            if task["id"] == task_id:
                root_task = task
                break

        status = root_task.get('status')

        # Check if task is complete
        if status in [3, 4, 5, 6]:  #  success, partial success,  failure,  timeout
            return root_task

        # Check timeout
        elapsed = time.time() - start_time
        if elapsed >= timeout:
            return {
                'error': 'Task timeout',
                'task_id': task_id,
                'elapsed': elapsed,
                'current_status': status
            }

        # Wait then continue polling
        time.sleep(poll_interval)


# ==================== Tag typemanagement  (tag_type Subtopic)  ====================

def tag_type_create(client: DMEAPIClient, name: str, description: str = None) -> dict:
    """
    Create tag type
    
    Args:
        client: DME API client
        name: Tag type name (Required) 
        description: Tag type description (Optional) 
    
    Returns:
        create 的Tag type info
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
    Batch queryTag type
    
    Args:
        client: DME API client
        start: paginationStart position, default 1
        limit: Page size, default 100
        name: Tag type name filter (Optional) 
    
    Returns:
        Tag type list
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
        tag_type_id: Tag type ID (Required) 
        name: Tag type name (Optional) 
        description: Tag type description (Optional) 
    
    Returns:
        modify 后的Tag type info
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
    Batch deleteTag type
    
    Args:
        client: DME API client
        tag_type_ids: Tag type ID  list (Required) 
    
    Returns:
        batchDeletion result
    """
    url = "/rest/tagmgmt/v1/tag-types/delete"
    
    payload = {
        'ids': tag_type_ids
    }
    
    response = client.post(url, body=payload)
    return response


# ====================  tagmanagement  (tag Subtopic)  ====================

def tag_create(client: DMEAPIClient, name: str, tag_type_id: str,
                tag_type_name: str = None, description: str = None, color: str = None) -> dict:
    """
    Create tag
    
    Args:
        client: DME API client
        name: Tag name (Required) 
        tag_type_id: Tag type ID (Required) 
        tag_type_name: Tag type name (API  need) 
        description: Tag description (Optional) 
        color: Tag color (Optional) 
    
    Returns:
        Created tag info
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
    Batch query tag
    
    Args:
        client: DME API client
        start: paginationStart position, default 1
        limit: Page size, default 100
        name: Tag name filter (Optional) 
        tag_type_id: Tag type ID  filter (Optional) 
    
    Returns:
         tag list
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
        tag_id:  tag ID (Required) 
        name: Tag name (Optional) 
        description: Tag description (Optional) 
        color: Tag color (Optional) 
    
    Returns:
        Modified tag info
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
    Batch delete tag
    
    Args:
        client: DME API client
        tag_ids:  tag ID  list (Required) 
    
    Returns:
        batchDeletion result
    """
    url = "/rest/tagmgmt/v1/tags/delete"
    
    payload = {
        'ids': tag_ids
    }
    
    response = client.post(url, body=payload)
    return response


def tag_bind(client: DMEAPIClient, tag_id: str, resources: list) -> dict:
    """
    Associate tag with resource
    
    Args:
        client: DME API client
        tag_id:  tag ID (Required) 
        resources: Resource list, format is [{"resource_id": "xxx", "resource_type": "xxx"}] (Required) 
    
    Returns:
         associated result
    """
    url = "/rest/tagmgmt/v1/tags/{tag_id}/associate-resources"
    
    payload = {
        'resources': resources
    }
    
    response = client.post(url, body=payload, params={"tag_id": tag_id})
    return response


def tag_unbind(client: DMEAPIClient, tag_id: str, resources: list) -> dict:
    """
    Disassociate tag from resource
    
    Args:
        client: DME API client
        tag_id:  tag ID (Required) 
        resources: Resource list, format is [{"resource_id": "xxx", "resource_type": "xxx"}] (Required) 
    
    Returns:
        Disassociation result
    """
    url = "/rest/tagmgmt/v1/tags/{tag_id}/disassociate-resources"
    
    payload = {
        'resources': resources
    }
    
    response = client.post(url, body=payload, params={"tag_id": tag_id})
    return response


# ==================== AZ management (az Subtopic)  ====================

def az_list(client: DMEAPIClient, az_name: str = None, operate_status: str = None,
         start: int = 1, limit: int = 512, is_sc: bool = False) -> dict:
    """
    Batch queryAvailability zone. 

    Args:
        client: DME API client
        az_name: Availability zone name, supports fuzzy match (Optional, string, 1~64 characters)
        operate_status: Availability zone运营 status. For offlineaz, 其operate_status是null, currently onlysupports filtering上线online的az (Optional, string, 1~16 characters)
        start: Page number, 从1 start (Optional, int32, 1~10000000). Default: 1
        limit: Page size (Optional, int32, 1~512). Default: 512
        is_sc: Operation-side query (Optional, boolean, true,false). Default: false

    Returns:
        {
            total: Availability zoneTotal count (integer),
            az_list: Availability zone list (List<GetAzResponse>). 参数格式如下：[{
                id: Availability zoneid (string),
                name: Availability zone name (string),
                description: Availability zone description (string),
                operate_status: Availability zone operations status (string). Default: offline,
                site_urn:  siteurn (string, 1~64 characters),
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


# ==================== Data centermanagement  (dc Subtopic)  ====================

def dc_list(client: DMEAPIClient, name: str = None,
                     page_no: int = 1, page_size: int = 20) -> dict:
    """
    getData center list
    
     queryData center list, supports name filtering and pagination. 
    
    Args:
        client: DME API client
        name: Data center name (Optional, supports fuzzy search) 
        page_no: Page queryStart page, default 1
        page_size: per pagecount, 1~1000, default 20
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes  total 和 datacenters  field
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
    getData center details
    
    QueryData center的Details. 
    
    Args:
        client: DME API client
        dc_id: Data center ID (Required) 
    
    Returns:
        Data centerDetails
    """
    url = "/rest/dcmgmt/dcmgmtservice/v1/datacenters/{dc_id}"
    
    response = client.get(url, params={"dc_id": dc_id})
    return response


def dc_show_devices(client: DMEAPIClient, dc_id: str,
                 device_type: list = None, page_no: int = 1,
                 page_size: int = 20) -> dict:
    """
    QueryData centerdevice list info
    
    Args:
        client: DME API client
        dc_id: Data center ID (Required) 
        device_type: Device type list (Optional) 
                      value: server, storage, network, switch, router, firewall,
                          loadbalancer, firewall_cluster, ipswitch, other
        page_no: Page queryStart page, default 1
        page_size: per pagecount, 1~1000, default 20
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, Includes device list
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
    Batch queryRegion. 

    Args:
        client: DME API client
        ids: RegionID list,  supportexact match (Optional, List[string], max array members: 100)
        name: Region name, supports fuzzy search (Optional, string,  max256 characters)
        active_ip_address: Region主IP address, supports fuzzy search (Optional, string,  max256 characters)
        standby_ip_address: Region备IP address, supports fuzzy search (Optional, string,  max256 characters)
        sync_status: RegionSync status, Exact filter (Optional, List[string], max array members: 3). Optional值: normal (normal), sync (Syncing), failed (Sync failure)
        role: Region role, Exact filter (Optional, string). Optional值: parent (上级Region), child (下级Region)
        sort_key: Sort field (Optional, string). Optional值: last_sync_time ( recentSync time)
        sort_dir: Sort direction (Optional, string). Optional值: asc (ascending), desc (descending). Default: desc
        page_no: Page query start页 (Optional, int32, 1~100). Default: 1
        page_size: per pagecount (Optional, int32, 1~100). Default: 20

    Returns:
        {
            total: Total count (integer),
            regions: Region list. 参数格式如下：[{
                id: Region ID (string),
                name: Region name (string),
                role: Region role (string),
                sync_status: Sync status (string),
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
    Query sub-levelRegionResource info. 

    Args:
        client: DME API client
        region_id: 下级Region的ID (Required, string, 1~64 characters)
        request_url: Query sub-levelCorresponding resource northbound APIURL (Required, string, 1~8192 characters)
        request_method:  request方式 (Required, string). Optional值: get (Get request), post (Post request)
        request_body: Call lower-level northbound API requestBody体 (Optional, string, 1~20480 characters)

    Returns:
        N/A
    """
    url = "/rest/regionmgmt/v1/regions/{region_id}/resources/query"

    if not region_id:
        raise ValueError("region_id 是required parameter")
    if not request_url:
        raise ValueError("request_url 是required parameter")

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
    # Direct action (Two-level structure) 
    'login': {
        'func': login,
        'description': 'Auth user login',
        'params': ['username', 'password', 'grant_type'],
        'subtopic': None
    },
    'logout': {
        'func': logout,
        'description': 'Logout session',
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
        'description': 'get DME 证书',
        'params': [],
        'subtopic': None
    },
    'reset_password': {
        'func': reset_password,
        'description': ' reset password',
        'params': ['user_name', 'new_value', 'is_initial_password'],
        'subtopic': None
    },
    # subtopic actions - user (three-level structure)
    'user_list': {
        'func': user_list,
        'description': 'Batch queryUser info',
        'params': ['page_no', 'page_size', 'name'],
        'subtopic': 'user'
    },
    'user_show': {
        'func': user_show,
        'description': 'QueryUser info',
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
    # subtopic actions - role (three-level structure)
    'role_list': {
        'func': role_list,
        'description': 'Batch queryRole info',
        'params': ['page_no', 'page_size', 'name'],
        'subtopic': 'role'
    },
    # subtopic actions - backup_server (three-level structure)
    'backup_server_list': {
        'func': backup_server_list,
        'description': 'Batch query backup servers',
        'params': ['address', 'name', 'page_no', 'page_size'],
        'subtopic': 'backup_server'
    },
    # subtopic actions - todo_task_group (three-level structure)
    'todo_task_group_list': {
        'func': todo_task_group_list,
        'description': ' queryPending task group list',
        'params': ['group_id', 'name', 'creator_name', 'is_finished', 'is_group',
                   'start', 'limit', 'status', 'todo_item_status',
                   'start_time_from', 'start_time_to', 'end_time_from',
                   'end_time_to', 'sort_key', 'sort_dir'],
        'subtopic': 'todo_task_group'
    },
    'todo_task_group_execute': {
        'func': todo_task_group_execute,
        'description': ' executePending task group',
        'params': ['group_id'],
        'subtopic': 'todo_task_group'
    },
    'todo_task_group_confirm': {
        'func': todo_task_group_confirm,
        'description': 'Confirm scheduled executionPending task group',
        'params': ['group_id'],
        'subtopic': 'todo_task_group'
    },
    # subtopic actions - todo_task (three-level structure)
    'todo_task_list': {
        'func': todo_task_list,
        'description': 'Query pendingTask list',
        'params': ['service_type', 'status', 'page_no', 'page_size'],
        'subtopic': 'todo_task'
    },
    'todo_task_show': {
        'func': todo_task_show,
        'description': 'Query pendingTask details',
        'params': ['item_id'],
        'subtopic': 'todo_task'
    },
    'todo_task_execute': {
        'func': todo_task_execute,
        'description': 'Execute pending task',
        'params': ['item_id'],
        'subtopic': 'todo_task'
    },
    'todo_task_audit': {
        'func': todo_task_audit,
        'description': 'Review pending task',
        'params': ['item_id', 'is_approval', 'suggestion'],
        'subtopic': 'todo_task'
    },
    'todo_task_revoke': {
        'func': todo_task_revoke,
        'description': 'Cancel review pending item',
        'params': ['item_id'],
        'subtopic': 'todo_task'
    },
    'todo_task_close': {
        'func': todo_task_close,
        'description': 'Close pending task',
        'params': ['item_id', 'reason'],
        'subtopic': 'todo_task'
    },
    # subtopic actions - task (three-level structure)
    'task_show': {
        'func': task_show,
        'description': 'QueryTask details',
        'params': ['task_id'],
        'subtopic': 'task'
    },
    'task_list': {
        'func': task_list,
        'description': 'Batch querytask ',
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
    # subtopic actions - tag_type (three-level structure)
    'tag_type_create': {
        'func': tag_type_create,
        'description': 'Create tag type',
        'params': ['name', 'description'],
        'subtopic': 'tag_type'
    },
    'tag_type_list': {
        'func': tag_type_list,
        'description': 'Batch queryTag type',
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
        'description': 'Batch deleteTag type',
        'params': ['tag_type_ids'],
        'subtopic': 'tag_type'
    },
    # subtopic actions - tag (three-level structure)
    'tag_create': {
        'func': tag_create,
        'description': 'Create tag',
        'params': ['name', 'tag_type_id', 'tag_type_name', 'description', 'color'],
        'subtopic': 'tag'
    },
    'tag_list': {
        'func': tag_list,
        'description': 'Batch query tag',
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
        'description': 'Batch delete tag',
        'params': ['tag_ids'],
        'subtopic': 'tag'
    },
    'tag_bind': {
        'func': tag_bind,
        'description': 'Associate tag with resource',
        'params': ['tag_id', 'resources'],
        'subtopic': 'tag'
    },
    'tag_unbind': {
        'func': tag_unbind,
        'description': 'Disassociate tag from resource',
        'params': ['tag_id', 'resources'],
        'subtopic': 'tag'
    },
    # subtopic actions - az (three-level structure)
    'az_list': {
        'func': az_list,
        'description': 'Batch queryAvailability zone',
        'params': ['az_name', 'operate_status', 'start', 'limit', 'is_sc'],
        'subtopic': 'az'
    },
    # subtopic actions - dc (three-level structure)
    'dc_list': {
        'func': dc_list,
        'description': 'getData center list',
        'params': ['name', 'page_no', 'page_size'],
        'subtopic': 'dc'
    },
    'dc_show': {
        'func': dc_show,
        'description': 'getData center details',
        'params': ['dc_id'],
        'subtopic': 'dc'
    },
    'dc_show_devices': {
        'func': dc_show_devices,
        'description': 'QueryData centerdevice list info',
        'params': ['dc_id', 'device_type', 'page_no', 'page_size'],
        'subtopic': 'dc'
    },
    # region subtopic actions
    'region_list': {
        'func': region_list,
        'description': 'Batch queryRegion',
        'params': ['ids', 'name', 'active_ip_address', 'standby_ip_address', 'sync_status', 'role', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'region'
    },
    'region_query': {
        'func': region_query,
        'description': 'Query sub-levelRegionResource info',
        'params': ['region_id', 'request_url', 'request_method', 'request_body'],
        'subtopic': 'region'
    },
}
