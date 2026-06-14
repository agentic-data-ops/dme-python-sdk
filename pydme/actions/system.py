"""
System management (System) operations
"""

import sys
import os

from pydme.client import DMEAPIClient


def login(client: DMEAPIClient) -> dict:
    """
    Auth user login

    强制调用 client.login() 完成认证，然后从 header 获取 accessSession，
    提示用户可配置环境变量复用认证密钥，Avoid duplicate login。

    Args:
        client: DME API client

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含 accessSession
        - accessSession: 会话 token，用于后续请求的 X-Auth-Token header
    """
    client.login()

    accessSession = client.headers.get("X-Auth-Token", "")
    if accessSession:
        print(f"\n登录成功！")
        print(f"\n提示：配置环境变量复用认证密钥，Avoid duplicate login：")
        print("  export DME_API_AUTH_TOKEN='<accessSession>'")

    return {
        'accessSession': accessSession
    }


def logout(client: DMEAPIClient) -> dict:
    """
    注销当前已经登录的三方会话或普通会话。

    Args:
        client: DME API client

    Returns:
        无
    """
    url = "/rest/plat/smapp/v1/sessions"
    
    response = client.delete(url)
    return response


def reset_password(client: DMEAPIClient, user_name: str, new_value: str,
                   is_initial_password: bool = True) -> dict:
    """
    根据指定Username重置指定用户的密码，重置不需要原始密码，因此，执行该接口的三方用户角色权限必须是安全管理员角色。

    Args:
        client: DME API client
        user_name: 需要重置密码的Username (Required, string, 1~128 characters)
        new_value: 新密码 (Required, string, 8~32 characters)。要求：1. 密码长度cannot be less than8 characters、大于32 characters。2. Password must contain at least2个字母，must contain at least1个大写字母，must contain at least1个小写字母，must contain at least1count字，must contain at least1个特殊字符（!"#$%&'()*+,-./:;<=>?@[]^`{|}~）。3. 密码中同一字符连续出现次数cannot exceed2，Cannot contain repeated character sequences（重复次数为4，重复序列字符数为1）。4. 密码不能包含Username和Username的倒序，Cannot contain phone number or email，Cannot contain dictionary words。
        is_initial_password: 标识密码重置后当下次登录时是否必须修改密码 (Required, boolean, true,false)。true：Must perform initial password change on next login；false：Direct login next time，不需初始化修改。Default：true

    Returns:
        无
    """
    url = "/rest/usm/v1/users/{user_name}/reset-credentials"

    # Parameter validation
    if not user_name or len(user_name) > 128:
        raise ValueError("user_name 是required parameter，1~128 characters")
    if not new_value or len(new_value) < 8 or len(new_value) > 32:
        raise ValueError("new_value 是required parameter，8~32 characters")

    payload = {
        'newValue': new_value,
        'isInitialPassword': is_initial_password
    }

    response = client.put(url, body=payload, params={"user_name": user_name})
    return response


def user_delete(client: DMEAPIClient, user_id: int) -> dict:
    """
    删除用户。该APIMay directly or indirectly affect production services, causing service interruption or data loss. Proceed with caution.。

    Args:
        client: DME API client
        user_id: 用户ID (Required, integer, 11~2147483647)

    Returns:
        无
    """
    url = "/rest/usermgmt/v1/users/{user_id}"

    # Parameter validation
    if user_id is None:
        raise ValueError("user_id 是required parameter")

    response = client.delete(url, params={"user_id": user_id})
    return response


def user_create(client: DMEAPIClient, name: str, type: int,
                value: str = None, description: str = None,
                roles: list = None) -> dict:
    """
    创建用户。

    Args:
        client: DME API client
        name: Username (Required, string, 最多32 characters)。本地Usernamecannot be less than6 characters，大于32 characters，Cannot contain spaces、转义字符、Invisible and special characters。远端Usernamecannot be less than1 characters，大于32 characters，Cannot contain invisible characters;特殊字符。
        type: User type (Required, integer, 无)。0：Local user；2：Remote user。
        value: 密码 (Optional, string, 8~32 characters)。密码长度cannot be less than8 characters、大于32 characters。Password must contain at least2个字母，must contain at least1个大写字母，must contain at least1个小写字母，must contain at least1count字，must contain at least1个特殊字符。Remote user不涉及。
        description: 描述 (Optional, string, 最多127 characters)
        roles: User role (Optional, List[integer], max array members：10)。如Administrators，北向User group，安全管理员组，Filesystem组或用户自定义角色。

    Returns:
        无
    """
    url = "/rest/usermgmt/v1/users"

    # Parameter validation
    if not name:
        raise ValueError("name 是required parameter")

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
    Batch queryUser info。

    Args:
        client: DME API client
        page_no: 页数 (Required, integer, min：1)。Default：1
        page_size: 页面大小 (Required, integer, 5~200)。Default：10
        name: Username搜索关键字 (Optional, string, 最多32 characters)

    Returns:
        {
            total: Total count (integer, max：5000),
            datas: User data (List<UserData>, max array members：5000)。参数格式如下：[{
                id: 用户ID (integer, 1~2147483647),
                name: Username (string, 6~32 characters),
                description: 描述 (string, 最多127 characters),
                type: User type (integer)。Optional值：0 (Local user), 1 (Third-party system access user), 2 (Remote user),
                roles: 角色ID列表 (List<integer>, max array members：50),
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
    Batch query角色信息。

    Args:
        client: DME API client
        page_no: 页数 (Required, integer, min：1)。Default：1
        page_size: 页面大小 (Required, integer, 5~100)。Default：10
        name: 角色名搜索关键字 (Optional, string, 最多64 characters)

    Returns:
        {
            total: Total count (integer, max：10),
            datas: Role data (List<RoleData>, max array members：5000)。参数格式如下：[{
                id: 角色ID (integer, 1~2147483647),
                name: 角色名称 (string, 最多64 characters),
                description: 描述 (string, 最多127 characters),
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
    QueryUser info。

    Args:
        client: DME API client
        user_id: 用户ID (Required, integer, 1~2147483647)

    Returns:
        {
            id: 用户ID (integer, 1~2147483647),
            name: Username (string, 最多32 characters),
            type: User type (integer)。Optional值：0 (Local user), 1 (Third-party system access user), 2 (Remote user),
            description: 描述 (string, 最多127 characters),
            roles: User role (List<integer>, max array members：50),
        }
    """
    url = "/rest/usermgmt/v1/users/{user_id}"
    
    # Parameter validation
    if user_id is None:
        raise ValueError("user_id 是required parameter")

    response = client.get(url, params={"user_id": user_id})
    return response


def show(client: DMEAPIClient) -> dict:
    """
    Query product system info。

    Args:
        client: DME API client

    Returns:
        {
            version: DME产品Version info (string, 最多128 characters),
            sn: DME产品SN号 (string, 最多64 characters),
        }
    """
    url = "/rest/productmgmt/v1/system-info"
    
    response = client.get(url)
    return response


def certificate(client: DMEAPIClient, service_type: str = "APIGWService") -> dict:
    """
    获取DME证书。

    Args:
        client: DME API client
        service_type: Service type (Required, string)。Optional值：APIGWService (DME北向网关)

    Returns:
        {
            cert: 证书文件Base64编码string (string),
        }
    """
    url = "/rest/certmgmt/v1/certs"

    # Parameter validation
    if service_type not in ["APIGWService"]:
        raise ValueError(f"service_type Optional值：APIGWService")

    response = client.get(url, params={'service_type': service_type})
    return response


def backup_server_list(client: DMEAPIClient, address: str = None,
                         name: str = None,
                         page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch query backup servers。

    Args:
        client: DME API client
        address: Backup server地址，支持IPv4地址，supports fuzzy match (Optional, string, 1~256 characters)
        name: Backup server名称 (Optional, string)
        page_no: Page queryStart page (Optional, int32)。Default：1
        page_size: 每页count (Optional, int32, 1~1000)。Default：20

    Returns:
        {
            total: Backup serverTotal count (int32),
            backup_servers: 备份Server list (List<BackupServerInfo>)。参数格式如下：[{
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


# ==================== Pending task group管理（todo_task_group Subtopic） ====================

def todo_task_group_list(client: DMEAPIClient, group_id: str = None, name: str = None,
               creator_name: str = None, is_finished: bool = None,
               is_group: bool = None, start: int = None, limit: int = None,
               status: list = None, todo_item_status: list = None,
               start_time_from: str = None, start_time_to: str = None,
               end_time_from: str = None, end_time_to: str = None,
               sort_key: str = None, sort_dir: str = None) -> dict:
    """
    查询Pending task group列表

    Args:
        client: DME API client
        group_id: Pending task group ID（Optional）
        name: Pending task group名称（Optional）
        creator_name: 创建人名称（Optional）
        is_finished: 是否Completed（Optional）
        is_group: 是否群组任务（Optional）
        start: 分页Start position（Optional，0~10000000）
        limit: 分页count（Optional，1~1000）
        status: Pending task groupstatus list（Optional，1-Pending/2-Executing/3-Completed/4-已关闭）
        todo_item_status: Pending item status list（Optional，0-待确认/1-未完成/2-Executing/3-Completed）
        start_time_from: Start time起始值（Optional，格式：yyyy-MM-dd HH:mm:ss）
        start_time_to: Start time结束值（Optional，格式：yyyy-MM-dd HH:mm:ss）
        end_time_from: End time起始值（Optional，格式：yyyy-MM-dd HH:mm:ss）
        end_time_to: End time结束值（Optional，格式：yyyy-MM-dd HH:mm:ss）
        sort_key: Sort field（Optional）
        sort_dir: Sort method（Optional，asc/desc）

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含Pending task group列表和Total count
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
    执行Pending task group

    执行指定的Pending task group。

    Args:
        client: DME API client
        group_id: Pending task group ID（Required）

    Returns:
        执行结果，包含 task_id
    """
    url = "/rest/taskmgmt/v1/todo-groups/{group_id}/execute"

    response = client.put(url, body={}, params={"group_id": group_id})
    return response


def todo_task_group_confirm(client: DMEAPIClient, group_id: str) -> dict:
    """
    Confirm scheduled executionPending task group

    Args:
        client: DME API client
        group_id: Pending task group ID（Required）

    Returns:
        确认结果
    """
    url = "/rest/taskmgmt/v1/todo-groups/{group_id}/confirm"

    response = client.put(url, body={}, params={"group_id": group_id})
    return response


# ==================== 待办任务管理（todo_task Subtopic） ====================

def todo_task_list(client: DMEAPIClient, service_type: str,
               status: list = None, page_no: int = None,
               page_size: int = None) -> dict:
    """
    Batch query待办Task details

    Batch queryPending item列表，supports filtering和分页。

    Args:
        client: DME API client
        service_type: Business type（Required，wfa_execute_activity-自动化编排）
        status: Pending item status list（Optional，1-未执行/2-Executing/3-成功/4-partial success/5-失败/6-超时/7-警告/8-已关闭/9-待审核/10-审核不通过/21-预检查中/22-预检查失败）
        page_no: 页索引号（Optional，默认 1）
        page_size: 每页count（Optional，1~10，默认 10）

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含Pending item列表和Total count
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
    查询Pending item详情信息

    QueryPending item的Details。

    Args:
        client: DME API client
        item_id: Pending item ID（Required）

    Returns:
        Pending itemDetails
    """
    url = "/rest/taskmgmt/v1/todo-items/{item_id}"

    response = client.get(url, params={"item_id": item_id})
    return response


def todo_task_execute(client: DMEAPIClient, item_id: str) -> dict:
    """
    Execute pending task

    执行指定的Pending item。

    Args:
        client: DME API client
        item_id: Pending item ID（Required）

    Returns:
        执行结果，包含 task_id
    """
    url = "/rest/taskmgmt/v1/todo-items/{item_id}/execute"

    response = client.put(url, body={}, params={"item_id": item_id})
    return response


def todo_task_audit(client: DMEAPIClient, item_id: str, is_approval: bool,
          suggestion: str = None) -> dict:
    """
    Review pending task

    对Pending item进行审核（批准或拒绝）。

    Args:
        client: DME API client
        item_id: Pending item ID（Required）
        is_approval: 是否批准（Required，true-批准/false-拒绝）
        suggestion: 审核建议（Optional，0-63 字符）

    Returns:
        审核结果
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

    撤销对指定Pending item的审核。

    Args:
        client: DME API client
        item_id: Pending item ID（Required）

    Returns:
        撤销结果
    """
    url = "/rest/taskmgmt/v1/todo-items/{item_id}/revoke-audit"

    response = client.put(url, body={}, params={"item_id": item_id})
    return response


def todo_task_close(client: DMEAPIClient, item_id: str, reason: str) -> dict:
    """
    Close pending task

    关闭指定的Pending item，需要提供关闭原因。

    Args:
        client: DME API client
        item_id: Pending item ID（Required）
        reason: 关闭原因（Required，0-63 字符）

    Returns:
        关闭结果
    """
    url = "/rest/taskmgmt/v1/todo-items/{item_id}/close"

    payload = {
        'reason': reason
    }

    response = client.put(url, body=payload, params={"item_id": item_id})
    return response


# ==================== 任务管理（task Subtopic） ====================

import time

def task_show(client: DMEAPIClient, task_id: str) -> list:
    """
    QueryTask details
    
    根据任务Unique identifier TaskId 进行查询。
    
    Args:
        client: DME API client
        task_id: 任务 ID（Required，1~36  characters）
    
    Returns:
        Task details列表，包含：
        - id: 任务 ID
        - name_en: 任务英文名称
        - name_cn: 任务中文名称
        - description: 任务描述
        - parent_id: 父任务 ID
        - seq_no: 任务序号
        - status: 状态（1-初始状态;2-Executing;3-成功;4-partial success;5-失败;6-超时）
        - progress: 任务进度
        - owner_name: Create task user名称
        - owner_id: Create task user ID
        - create_time: Task creation时间（UTC 毫second(s)数）
        - start_time: 任务Start time（UTC 毫second(s)数）
        - end_time: 任务End time（UTC 毫second(s)数）
        - detail_en: 任务英文详情
        - detail_cn: 任务中文详情
        - is_support_retry: supports重试
        - is_support_rollback: supports回滚
        - remarks: Remark
        - resources: 任务关联的资源列表
    """
    url = "/rest/taskmgmt/v1/tasks/{task_id}"
    
    response = client.get(url, params={"task_id": task_id})
    return response


def task_list(client: DMEAPIClient, start: int = 1, limit: int = 100,
               task_name: str = None, status: int = None,
               owner_id: str = None, create_time_from: int = None,
               create_time_to: int = None) -> dict:
    """
    Batch query任务
    
    Args:
        client: DME API client
        start: 分页Start position，默认 1
        limit: Page size, default 100
        task_name: Task name过滤（Optional）
        status: 状态过滤（Optional，1-初始状态;2-Executing;3-成功;4-partial success;5-失败;6-超时）
        owner_id: Create task user ID 过滤（Optional）
        create_time_from: Creation time起始（Optional，UTC 毫second(s)数）
        create_time_to: Creation time结束（Optional，UTC 毫second(s)数）
    
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
    重试任务

    重试指定的任务，用于任务未完全成功的重试。

    Args:
        client: DME API client
        task_id: 任务 ID（Required，1~36  characters）

    Returns:
        重试结果
    """
    url = "/rest/taskmgmt/v1/tasks/{task_id}/retry"

    response = client.post(url, body={}, params={"task_id": task_id})
    return response


def task_wait(client: DMEAPIClient, task_id: str, timeout: int = 300,
              poll_interval: int = 2) -> dict:
    """
    Wait for task completion

    轮询查询任务状态，直到任务完成或超时。

    Args:
        client: DME API client
        task_id: 任务 ID
        timeout: timeout（second(s)），默认 300 second(s)
        poll_interval: 轮询间隔（second(s)），默认 2 second(s)

    Returns:
        任务最终状态详情
        status 说明：
        - 3: 成功
        - 4: partial success
        - 5: 失败
        - 6: 超时
    """
    start_time = time.time()

    while True:
        task_info = task_show(client, task_id)

        # API 返回的是列表，获取根Task details
        for task in task_info:
            if task["id"] == task_id:
                root_task = task
                break

        status = root_task.get('status')

        # 检查任务是否完成
        if status in [3, 4, 5, 6]:  # 成功、partial success、失败、超时
            return root_task

        # 检查是否超时
        elapsed = time.time() - start_time
        if elapsed >= timeout:
            return {
                'error': 'Task timeout',
                'task_id': task_id,
                'elapsed': elapsed,
                'current_status': status
            }

        # 等待后继续轮询
        time.sleep(poll_interval)


# ==================== Tag type管理（tag_type Subtopic） ====================

def tag_type_create(client: DMEAPIClient, name: str, description: str = None) -> dict:
    """
    Create tag type
    
    Args:
        client: DME API client
        name: Tag type name（Required）
        description: Tag type description（Optional）
    
    Returns:
        创建的Tag type信息
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
        start: 分页Start position，默认 1
        limit: Page size, default 100
        name: Tag type name过滤（Optional）
    
    Returns:
        Tag type列表
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
        tag_type_id: Tag type ID（Required）
        name: Tag type name（Optional）
        description: Tag type description（Optional）
    
    Returns:
        修改后的Tag type信息
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
        tag_type_ids: Tag type ID 列表（Required）
    
    Returns:
        批量Deletion result
    """
    url = "/rest/tagmgmt/v1/tag-types/delete"
    
    payload = {
        'ids': tag_type_ids
    }
    
    response = client.post(url, body=payload)
    return response


# ==================== 标签管理（tag Subtopic） ====================

def tag_create(client: DMEAPIClient, name: str, tag_type_id: str,
                tag_type_name: str = None, description: str = None, color: str = None) -> dict:
    """
    Create tag
    
    Args:
        client: DME API client
        name: Tag name（Required）
        tag_type_id: Tag type ID（Required）
        tag_type_name: Tag type name（API 需要）
        description: 标签描述（Optional）
        color: 标签颜色（Optional）
    
    Returns:
        创建的标签信息
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
    Batch query标签
    
    Args:
        client: DME API client
        start: 分页Start position，默认 1
        limit: Page size, default 100
        name: Tag name过滤（Optional）
        tag_type_id: Tag type ID 过滤（Optional）
    
    Returns:
        标签列表
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
        tag_id: 标签 ID（Required）
        name: Tag name（Optional）
        description: 标签描述（Optional）
        color: 标签颜色（Optional）
    
    Returns:
        修改后的标签信息
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
    Batch delete标签
    
    Args:
        client: DME API client
        tag_ids: 标签 ID 列表（Required）
    
    Returns:
        批量Deletion result
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
        tag_id: 标签 ID（Required）
        resources: 资源列表，format is [{"resource_id": "xxx", "resource_type": "xxx"}]（Required）
    
    Returns:
        关联结果
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
        tag_id: 标签 ID（Required）
        resources: 资源列表，format is [{"resource_id": "xxx", "resource_type": "xxx"}]（Required）
    
    Returns:
        取消关联结果
    """
    url = "/rest/tagmgmt/v1/tags/{tag_id}/disassociate-resources"
    
    payload = {
        'resources': resources
    }
    
    response = client.post(url, body=payload, params={"tag_id": tag_id})
    return response


# ==================== AZ management（az Subtopic） ====================

def az_list(client: DMEAPIClient, az_name: str = None, operate_status: str = None,
         start: int = 1, limit: int = 512, is_sc: bool = False) -> dict:
    """
    Batch queryAvailability zone。

    Args:
        client: DME API client
        az_name: Availability zone名称，supports fuzzy match (Optional, string, 1~64 characters)
        operate_status: Availability zone运营状态。对于未上线的az，其operate_status是null，因此暂时只supports filtering上线online的az (Optional, string, 1~16 characters)
        start: 分页的页号，从1开始 (Optional, int32, 1~10000000)。Default：1
        limit: 分页的大小 (Optional, int32, 1~512)。Default：512
        is_sc: 是否运营侧查询 (Optional, boolean, true,false)。Default：false

    Returns:
        {
            total: Availability zoneTotal count (integer),
            az_list: Availability zone list (List<GetAzResponse>)。参数格式如下：[{
                id: Availability zoneid (string),
                name: Availability zone名称 (string),
                description: Availability zone描述 (string),
                operate_status: Availability zone的运营状态 (string)。Default：offline,
                site_urn: 站点urn (string, 1~64 characters),
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


# ==================== Data center管理（dc Subtopic） ====================

def dc_list(client: DMEAPIClient, name: str = None,
                     page_no: int = 1, page_size: int = 20) -> dict:
    """
    获取Data center列表
    
    查询Data center列表，supports name filtering and pagination。
    
    Args:
        client: DME API client
        name: Data center name（Optional，supports fuzzy search）
        page_no: Page queryStart page，默认 1
        page_size: 每页count，1~1000，默认 20
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含 total 和 datacenters 字段
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
    获取Data center详情
    
    QueryData center的Details。
    
    Args:
        client: DME API client
        dc_id: Data center ID（Required）
    
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
        dc_id: Data center ID（Required）
        device_type: Device type列表（Optional）
                     取值：server, storage, network, switch, router, firewall,
                          loadbalancer, firewall_cluster, ipswitch, other
        page_no: Page queryStart page，默认 1
        page_size: 每页count，1~1000，默认 20
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含设备列表
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
    Batch queryRegion。

    Args:
        client: DME API client
        ids: RegionID list，支持exact match (Optional, List[string], max array members：100)
        name: Region的名称，supports fuzzy search (Optional, string, 最多256 characters)
        active_ip_address: Region主IP地址，supports fuzzy search (Optional, string, 最多256 characters)
        standby_ip_address: Region备IP地址，supports fuzzy search (Optional, string, 最多256 characters)
        sync_status: RegionSync状态，精确过滤 (Optional, List[string], max array members：3)。Optional值：normal (正常), sync (Syncing), failed (Sync失败)
        role: Region角色，精确过滤 (Optional, string)。Optional值：parent (上级Region), child (下级Region)
        sort_key: Sort field (Optional, string)。Optional值：last_sync_time (最近Sync time)
        sort_dir: Sort direction (Optional, string)。Optional值：asc (升序), desc (降序)。Default：desc
        page_no: Page query开始页 (Optional, int32, 1~100)。Default：1
        page_size: 每页count (Optional, int32, 1~100)。Default：20

    Returns:
        {
            total: Total count (integer),
            regions: Region list。参数格式如下：[{
                id: Region ID (string),
                name: Region名称 (string),
                role: Region角色 (string),
                sync_status: Sync状态 (string),
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
    查询下级Region资源信息。

    Args:
        client: DME API client
        region_id: 下级Region的ID (Required, string, 1~64 characters)
        request_url: 查询下级相应资源北向接口URL (Required, string, 1~8192 characters)
        request_method: 请求方式 (Required, string)。Optional值：get (Get请求), post (Post请求)
        request_body: 调用下级北向接口请求Body体 (Optional, string, 1~20480 characters)

    Returns:
        无
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
    # Direct action（Two-level structure）
    'login': {
        'func': login,
        'description': 'Auth user login',
        'params': ['username', 'password', 'grant_type'],
        'subtopic': None
    },
    'logout': {
        'func': logout,
        'description': '注销会话',
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
        'description': '获取 DME 证书',
        'params': [],
        'subtopic': None
    },
    'reset_password': {
        'func': reset_password,
        'description': '重置密码',
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
        'description': '创建用户',
        'params': ['name', 'type', 'value', 'description', 'roles'],
        'subtopic': 'user'
    },
    'user_delete': {
        'func': user_delete,
        'description': '删除用户',
        'params': ['user_id'],
        'subtopic': 'user'
    },
    # subtopic actions - role (three-level structure)
    'role_list': {
        'func': role_list,
        'description': 'Batch query角色信息',
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
        'description': '查询Pending task group列表',
        'params': ['group_id', 'name', 'creator_name', 'is_finished', 'is_group',
                   'start', 'limit', 'status', 'todo_item_status',
                   'start_time_from', 'start_time_to', 'end_time_from',
                   'end_time_to', 'sort_key', 'sort_dir'],
        'subtopic': 'todo_task_group'
    },
    'todo_task_group_execute': {
        'func': todo_task_group_execute,
        'description': '执行Pending task group',
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
        'description': '查询待办Task list',
        'params': ['service_type', 'status', 'page_no', 'page_size'],
        'subtopic': 'todo_task'
    },
    'todo_task_show': {
        'func': todo_task_show,
        'description': '查询待办Task details',
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
        'description': 'Batch query任务',
        'params': ['start', 'limit', 'task_name', 'status', 'owner_id', 'create_time_from', 'create_time_to'],
        'subtopic': 'task'
    },
    'task_retry': {
        'func': task_retry,
        'description': '重试任务',
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
        'description': 'Batch query标签',
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
        'description': 'Batch delete标签',
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
        'description': '获取Data center列表',
        'params': ['name', 'page_no', 'page_size'],
        'subtopic': 'dc'
    },
    'dc_show': {
        'func': dc_show,
        'description': '获取Data center详情',
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
        'description': '查询下级Region资源信息',
        'params': ['region_id', 'request_url', 'request_method', 'request_body'],
        'subtopic': 'region'
    },
}
