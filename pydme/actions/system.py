"""
系统管理 (System) 相关操作
"""

import sys
import os

from pydme.client import DMEAPIClient


def login(client: DMEAPIClient) -> dict:
    """
    认证用户登录

    强制调用 client.login() 完成认证, 然后从 header 获取 accessSession, 
    提示用户可配置环境变量复用认证密钥, 避免重复登录. 

    Args:
        client: DME API client

    Returns:
        {
            accessSession: 会话 token (string), 用于后续请求的 X-Auth-Token header,
        }
    """
    client.login()

    accessSession = client.headers.get("X-Auth-Token", "")
    if accessSession:
        print(f"\n登录成功！")
        print(f"\n提示：配置环境变量复用认证密钥，避免重复登录：")
        print("  export DME_API_AUTH_TOKEN='<accessSession>'")

    return {
        'accessSession': accessSession
    }


def logout(client: DMEAPIClient) -> dict:
    """
    注销当前已经登录的三方会话或普通会话. 

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
    根据指定用户名重置指定用户的密码, 重置不需要原始密码, 因此, 执行该接口的三方用户role权限必须是安全管理员role. 

    Args:
        client: DME API client
        user_name: 需要重置密码的用户名 (必选, string, 1~128个字符)
        new_value: 新密码 (必选, string, 8~32个字符). 要求: 1. 密码长度不能小于8个字符、大于32个字符. 2. 密码中must contain at least2个字母, must contain at least1个大写字母, must contain at least1个小写字母, must contain at least1个数字, must contain at least1个特殊字符 (!"#$%&'()*+,-./:;<=>?@[]^`{|}~). 3. 密码中同一字符连续出现次数不能超过2, 不能包含重复字符序列 (重复次数为4, 重复序列字符数为1). 4. 密码不能包含用户名和用户名的倒序, 不能包含用户手机号码和电子邮箱帐号, 不能包含密码字典中的词汇. 
        is_initial_password: 标识密码重置后当下次登录时是否必须modify密码 (必选, boolean, true,false). true: 下次登录系统时必须执行初始化modify; false: 下次直接登录系统, 不需初始化modify. default值: true

    Returns:
        无
    """
    url = "/rest/usm/v1/users/{user_name}/reset-credentials"

    # 参数校验
    if not user_name or len(user_name) > 128:
        raise ValueError("user_name 是必选参数，1~128个字符")
    if not new_value or len(new_value) < 8 or len(new_value) > 32:
        raise ValueError("new_value 是必选参数，8~32个字符")

    payload = {
        'newValue': new_value,
        'isInitialPassword': is_initial_password
    }

    response = client.put(url, body=payload, params={"user_name": user_name})
    return response


def user_delete(client: DMEAPIClient, user_id: int) -> dict:
    """
    delete用户. 该API可能会直接或间接影响现网业务运行, 导致业务中断、关键数据丢失等, 请谨慎操作. 

    Args:
        client: DME API client
        user_id: user ID (必选, integer, 11~2147483647)

    Returns:
        无
    """
    url = "/rest/usermgmt/v1/users/{user_id}"

    # 参数校验
    if user_id is None:
        raise ValueError("user_id 是必选参数")

    response = client.delete(url, params={"user_id": user_id})
    return response


def user_create(client: DMEAPIClient, name: str, type: int,
                value: str = None, description: str = None,
                roles: list = None) -> dict:
    """
    create用户. 

    Args:
        client: DME API client
        name: 用户名 (必选, string, 最多32个字符). 本地用户名不能小于6个字符, 大于32个字符, 不能包含空格、转义字符、不可见字符和特殊字符. 远端用户名不能小于1个字符, 大于32个字符, 不能包含不可见字符和;特殊字符. 
        type: 用户type (必选, integer, 无). 0: 本地用户; 2: 远端用户. 
        value: 密码 (可选, string, 8~32个字符). 密码长度不能小于8个字符、大于32个字符. 密码中must contain at least2个字母, must contain at least1个大写字母, must contain at least1个小写字母, must contain at least1个数字, must contain at least1个特殊字符. 远端用户不涉及. 
        description: description (可选, string, 最多127个字符)
        roles: 用户所属role (可选, List[integer], max array members: 10). 如Administrators, 北向用户组, 安全管理员组, Filesystem组或用户自定义role. 

    Returns:
        无
    """
    url = "/rest/usermgmt/v1/users"

    # 参数校验
    if not name:
        raise ValueError("name 是必选参数")

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
    批量query用户info. 

    Args:
        client: DME API client
        page_no: 页数 (必选, integer, 最小值: 1). default值: 1
        page_size: 页面大小 (必选, integer, 5~200). default值: 10
        name: 用户名搜索关键字 (可选, string, 最多32个字符)

    Returns:
        {
            total: total (integer, 最大值: 5000),
            datas: 用户数据 (List<UserData>, max array members: 5000). parameter format: [{
                id: user ID (integer, 1~2147483647),
                name: 用户名 (string, 6~32个字符),
                description: description (string, 最多127个字符),
                type: 用户type (integer). valid values: 0 (本地用户), 1 (三方系统接入用户), 2 (远端用户),
                roles: roleIDlist (List<integer>, max array members: 50),
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
    批量queryroleinfo. 

    Args:
        client: DME API client
        page_no: 页数 (必选, integer, 最小值: 1). default值: 1
        page_size: 页面大小 (必选, integer, 5~100). default值: 10
        name: role名搜索关键字 (可选, string, 最多64个字符)

    Returns:
        {
            total: total (integer, 最大值: 10),
            datas: role数据 (List<RoleData>, max array members: 5000). parameter format: [{
                id: roleID (integer, 1~2147483647),
                name: rolename (string, 最多64个字符),
                description: description (string, 最多127个字符),
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
    query指定用户info. 

    Args:
        client: DME API client
        user_id: user ID (必选, integer, 1~2147483647)

    Returns:
        {
            id: user ID (integer, 1~2147483647),
            name: 用户名 (string, 最多32个字符),
            type: 用户type (integer). valid values: 0 (本地用户), 1 (三方系统接入用户), 2 (远端用户),
            description: description (string, 最多127个字符),
            roles: 用户所属role (List<integer>, max array members: 50),
        }
    """
    url = "/rest/usermgmt/v1/users/{user_id}"
    
    # 参数校验
    if user_id is None:
        raise ValueError("user_id 是必选参数")

    response = client.get(url, params={"user_id": user_id})
    return response


def show(client: DMEAPIClient) -> dict:
    """
    query产品系统info. 

    Args:
        client: DME API client

    Returns:
        {
            version: DME产品versioninfo (string, 最多128个字符),
            sn: DME产品SN号 (string, 最多64个字符),
        }
    """
    url = "/rest/productmgmt/v1/system-info"
    
    response = client.get(url)
    return response


def certificate(client: DMEAPIClient, service_type: str = "APIGWService") -> dict:
    """
    获取DME证书. 

    Args:
        client: DME API client
        service_type: 服务type (必选, string). valid values: APIGWService (DME北向网关)

    Returns:
        {
            cert: 证书文件Base64编码字符串 (string),
        }
    """
    url = "/rest/certmgmt/v1/certs"

    # 参数校验
    if service_type not in ["APIGWService"]:
        raise ValueError(f"service_type 可选值：APIGWService")

    response = client.get(url, params={'service_type': service_type})
    return response


def backup_server_list(client: DMEAPIClient, address: str = None,
                         name: str = None,
                         page_no: int = 1, page_size: int = 20) -> dict:
    """
    批量query备份服务器. 

    Args:
        client: DME API client
        address: 备份服务器地址, 支持IPv4地址, supports fuzzy match (可选, string, 1~256个字符)
        name: 备份服务器name (可选, string)
        page_no: pagination start page (可选, int32). default值: 1
        page_size: items per page (可选, int32, 1~1000). default值: 20

    Returns:
        {
            total: 备份服务器total (int32),
            backup_servers: 备份服务器list (List<BackupServerInfo>). parameter format: [{
                id: 备份服务器id (string, 1~64个字符),
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


# ==================== 待办任务组管理 (todo_task_group 子主题) ====================

def todo_task_group_list(client: DMEAPIClient, group_id: str = None, name: str = None,
               creator_name: str = None, is_finished: bool = None,
               is_group: bool = None, start: int = None, limit: int = None,
               status: list = None, todo_item_status: list = None,
               start_time_from: str = None, start_time_to: str = None,
               end_time_from: str = None, end_time_to: str = None,
               sort_key: str = None, sort_dir: str = None) -> dict:
    """
    query待办任务组list

    Args:
        client: DME API client
        group_id: 待办任务组 ID(Optional)
        name: 待办任务组name(Optional)
        creator_name: create人name(Optional)
        is_finished: 是否已完成(Optional)
        is_group: 是否群组任务(Optional)
        start: 分页起始location (可选, 0~10000000)
        limit: 分页个数 (可选, 1~1000)
        status: 待办任务组statuslist (可选, 1-待处理/2-执行中/3-已完成/4-已false)
        todo_item_status: 待办项statuslist (可选, 0-待确认/1-未完成/2-执行中/3-已完成)
        start_time_from: start time起始值 (可选, 格式: yyyy-MM-dd HH:mm:ss)
        start_time_to: start time结束值 (可选, 格式: yyyy-MM-dd HH:mm:ss)
        end_time_from: end time起始值 (可选, 格式: yyyy-MM-dd HH:mm:ss)
        end_time_to: end time结束值 (可选, 格式: yyyy-MM-dd HH:mm:ss)
        sort_key: 排序字段(Optional)
        sort_dir: 排序方式 (可选, asc/desc)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含待办任务组list和total
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
    执行待办任务组

    执行指定的待办任务组. 

    Args:
        client: DME API client
        group_id: 待办任务组 ID(Required)

    Returns:
        执行result, 包含 task_id
    """
    url = "/rest/taskmgmt/v1/todo-groups/{group_id}/execute"

    response = client.put(url, body={}, params={"group_id": group_id})
    return response


def todo_task_group_confirm(client: DMEAPIClient, group_id: str) -> dict:
    """
    确认执行定时待办任务组

    Args:
        client: DME API client
        group_id: 待办任务组 ID(Required)

    Returns:
        确认result
    """
    url = "/rest/taskmgmt/v1/todo-groups/{group_id}/confirm"

    response = client.put(url, body={}, params={"group_id": group_id})
    return response


# ==================== 待办任务管理 (todo_task 子主题) ====================

def todo_task_list(client: DMEAPIClient, service_type: str,
               status: list = None, page_no: int = None,
               page_size: int = None) -> dict:
    """
    批量query待办task details

    批量query待办项list, 支持过滤和分页. 

    Args:
        client: DME API client
        service_type: 业务type (必选, wfa_execute_activity-自动化编排)
        status: 待办项statuslist (可选, 1-未执行/2-执行中/3-成功/4-部分成功/5-失败/6-超时/7-警告/8-已false/9-待审核/10-审核不通过/21-预检查中/22-预检查失败)
        page_no: 页索引号 (可选, default 1)
        page_size: items per page (可选, 1~10, default 10)

    Returns:
        {
            total: 待办任务count (integer),
            todo_items: 待办任务list (List<ItemDetail>). parameter format: [{
                id: 待办项ID (string, 1~64个字符),
                name: 待办task name (string, 1~128个字符),
                context: 待办任务上下文体 (string, 1~2097152个字符),
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
    query待办项detailsinfo

    query指定待办项的详细info. 

    Args:
        client: DME API client
        item_id: 待办项 ID(Required)

    Returns:
        {
            item_id: 待办项ID (string),
            name: name (string),
            description: description (string),
            group_id: 组ID (string),
            service_type: 服务type (string),
            status: status (string),
            creator_name: create人 (string),
            create_time: creation time (string),
            task_id: task ID (string),
            start_time: start time (string),
            end_time: end time (string),
            close_reason: false原因 (string),
            suggestion: 审批意见 (string),
        }
    """
    url = "/rest/taskmgmt/v1/todo-items/{item_id}"

    response = client.get(url, params={"item_id": item_id})
    return response


def todo_task_execute(client: DMEAPIClient, item_id: str) -> dict:
    """
    执行待办任务

    执行指定的待办项. 

    Args:
        client: DME API client
        item_id: 待办项 ID(Required)

    Returns:
        执行result, 包含 task_id
    """
    url = "/rest/taskmgmt/v1/todo-items/{item_id}/execute"

    response = client.put(url, body={}, params={"item_id": item_id})
    return response


def todo_task_audit(client: DMEAPIClient, item_id: str, is_approval: bool,
          suggestion: str = None) -> dict:
    """
    审核待办任务

    对待办项进行审核 (批准或拒绝). 

    Args:
        client: DME API client
        item_id: 待办项 ID(Required)
        is_approval: 是否批准 (必选, true-批准/false-拒绝)
        suggestion: 审核建议 (可选, 0-63 字符)

    Returns:
        审核result
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
    撤销审核待办项

    撤销对指定待办项的审核. 

    Args:
        client: DME API client
        item_id: 待办项 ID(Required)

    Returns:
        撤销result
    """
    url = "/rest/taskmgmt/v1/todo-items/{item_id}/revoke-audit"

    response = client.put(url, body={}, params={"item_id": item_id})
    return response


def todo_task_close(client: DMEAPIClient, item_id: str, reason: str) -> dict:
    """
    false待办任务

    false指定的待办项, 需要提供false原因. 

    Args:
        client: DME API client
        item_id: 待办项 ID(Required)
        reason: false原因 (必选, 0-63 字符)

    Returns:
        falseresult
    """
    url = "/rest/taskmgmt/v1/todo-items/{item_id}/close"

    payload = {
        'reason': reason
    }

    response = client.put(url, body=payload, params={"item_id": item_id})
    return response


# ==================== 任务管理 (task 子主题) ====================

import time

def task_show(client: DMEAPIClient, task_id: str) -> list:
    """
    query指定task details
    
    根据任务唯一标识 TaskId 进行query. 
    
    Args:
        client: DME API client
        task_id: 任务 ID (必选, 1~36 个字符)
    
    Returns:
        {
            id: task ID (string),
            name_en: task English name (string),
            name_cn: task Chinese name (string),
            description: task description (string),
            parent_id: 父task ID (string),
            seq_no: 任务序号 (string),
            status: status. valid values: 1 (初始status), 2 (执行中), 3 (成功), 4 (部分成功), 5 (失败), 6 (超时),
            progress: task progress (string),
            owner_name: create任务username (string),
            owner_id: create任务user ID (string),
            create_time: 任务creation time (string, UTC毫秒数),
            start_time: 任务start time (string, UTC毫秒数),
            end_time: 任务end time (string, UTC毫秒数),
            detail_en: 任务英文details (string),
            detail_cn: 任务中文details (string),
            is_support_retry: 是否支持重试 (boolean),
            is_support_rollback: 是否支持回滚 (boolean),
            remarks: 备注info (string),
            resources: 任务关联的资源list (List<AffectedResource>). parameter format: [{
                operate: 操作type (string),
                type: resource type (string),
                id: resource ID (string),
                name: 资源name (string),
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
    批量query任务
    
    Args:
        client: DME API client
        start: 分页起始location, default 1
        limit: 分页count, default 100
        task_name: task name过滤(Optional)
        status: status过滤 (可选, 1-初始status;2-执行中;3-成功;4-部分成功;5-失败;6-超时)
        owner_id: create任务用户 ID 过滤(Optional)
        create_time_from: creation time起始 (可选, UTC 毫秒数)
        create_time_to: creation time结束 (可选, UTC 毫秒数)
    
    Returns:
        {
            total: 任务count (int32),
            tasks: 任务list (List<TaskDetail>). parameter format: [{
                id: task ID (string),
                name_en: task English name (string),
                status: status (string),
                progress: task progress (string),
                owner_name: create任务username (string),
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
    重试任务

    重试指定的任务, 用于任务未完全成功的重试. 

    Args:
        client: DME API client
        task_id: 任务 ID (必选, 1~36 个字符)

    Returns:
        重试result
    """
    url = "/rest/taskmgmt/v1/tasks/{task_id}/retry"

    response = client.post(url, body={}, params={"task_id": task_id})
    return response


def task_wait(client: DMEAPIClient, task_id: str, timeout: int = 300,
              poll_interval: int = 2) -> dict:
    """
    等待任务完成

    调用 DMEAPIClient.get_task_result 轮询task status, 直到任务完成或超时. 
    Warning(7) status也视为任务已完成. 

    Args:
        client: DME API client
        task_id: 任务 ID (必选, 1~36 个字符)
        timeout: 超时时间 (秒), default 300 秒. 轮询次数 = timeout / poll_interval
        poll_interval: 轮询间隔 (秒), default 2 秒

    Returns:
        {
            id: task ID (string),
            status: task status (integer). valid values: 3 (成功), 4 (部分成功), 5 (失败), 6 (超时), 7 (警告),
            progress: task progress (integer, 0~100),
            name_en: task English name (string),
            name_cn: task Chinese name (string),
            resources: 任务关联的资源list (List<AffectedResource>). parameter format: [{
                operate: operation type (string). valid values: CREATE, MODIFY, DELETE,
                type: affected resource type (string),
                id: affected resource ID (string),
                name: affected resource name (string),
            }, ...],
        }

    Raises:
        Exception: 任务query超时 (超过轮询次数仍未完成)
    """
    retry_times = max(1, timeout // poll_interval)
    return client.get_task_result(
        task_id,
        retry_times=retry_times,
        retry_interval=poll_interval,
    )


# ==================== tag type管理 (tag_type 子主题) ====================

def tag_type_create(client: DMEAPIClient, name: str, description: str = None) -> dict:
    """
    createtag type
    
    Args:
        client: DME API client
        name: tag type name(Required)
        description: tag typedescription(Optional)
    
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
    批量querytag type
    
    Args:
        client: DME API client
        start: 分页起始location, default 1
        limit: 分页count, default 100
        name: tag type name过滤(Optional)
    
    Returns:
        {
            total: tag typecount (int32),
            datas: tag typelist (List<TagType>). parameter format: [{
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
    modifytag type
    
    Args:
        client: DME API client
        tag_type_id: tag type ID(Required)
        name: tag type name(Optional)
        description: tag typedescription(Optional)
    
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
    批量deletetag type
    
    Args:
        client: DME API client
        tag_type_ids: tag type ID list(Required)
    
    Returns:
        批量deleteresult
    """
    url = "/rest/tagmgmt/v1/tag-types/delete"
    
    payload = {
        'ids': tag_type_ids
    }
    
    response = client.post(url, body=payload)
    return response


# ==================== 标签管理 (tag 子主题) ====================

def tag_create(client: DMEAPIClient, name: str, tag_type_id: str,
                tag_type_name: str = None, description: str = None, color: str = None) -> dict:
    """
    create标签
    
    Args:
        client: DME API client
        name: tag name(Required)
        tag_type_id: tag type ID(Required)
        tag_type_name: tag type name (API 需要)
        description: 标签description(Optional)
        color: 标签颜色(Optional)
    
    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    批量query标签
    
    Args:
        client: DME API client
        start: 分页起始location, default 1
        limit: 分页count, default 100
        name: tag name过滤(Optional)
        tag_type_id: tag type ID 过滤(Optional)
    
    Returns:
        {
            total: 标签count (int32),
            datas: 标签list (List<Tag>). parameter format: [{
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
    modify标签
    
    Args:
        client: DME API client
        tag_id: 标签 ID(Required)
        name: tag name(Optional)
        description: 标签description(Optional)
        color: 标签颜色(Optional)
    
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
    批量delete标签
    
    Args:
        client: DME API client
        tag_ids: 标签 ID list(Required)
    
    Returns:
        批量deleteresult
    """
    url = "/rest/tagmgmt/v1/tags/delete"
    
    payload = {
        'ids': tag_ids
    }
    
    response = client.post(url, body=payload)
    return response


def tag_bind(client: DMEAPIClient, tag_id: str, resources: list) -> dict:
    """
    标签关联资源
    
    Args:
        client: DME API client
        tag_id: 标签 ID (必选, 32 位十六进制字符, 正则 ^[a-fA-F0-9]{32}$)
        resources: 资源list (List<TagResource>, 必选, 数组最小成员个数: 1, max array members: 100). parameter format: [{
            resource_type: resource type (必选, string, 1~128 个字符). valid values: storage_device (Storage device), backup_medium (备份存储), fc_switch (光纤交换机), protect_appliance (A8000备份一体机), security_appliance (数据安全一体机), ethernet_switch (以太网交换机), physical_server (服务器), virtual_machine (Virtual machine), logic_port (Logic port), file_system (Filesystem),
            resource_id: 资源 ID (必选, string, UUID 格式或 32 位十六进制字符, 正则 ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$),
        }, ...]
    
    Returns:
        create异步任务成功, 返回任务 ID. 
    """
    url = "/rest/tagmgmt/v1/tags/{tag_id}/associate-resources"
    
    payload = {
        'resources': resources
    }
    
    response = client.post(url, body=payload, params={"tag_id": tag_id})
    return response


def tag_unbind(client: DMEAPIClient, tag_id: str, resources: list) -> dict:
    """
    标签取消关联资源
    
    Args:
        client: DME API client
        tag_id: 标签 ID (必选, 32 位十六进制字符, 正则 ^[a-fA-F0-9]{32}$)
        resources: 资源list (List<TagResource>, 必选, 数组最小成员个数: 1, max array members: 100). parameter format: [{
            resource_type: resource type (必选, string, 1~128 个字符). valid values: storage_device (Storage device), backup_medium (备份存储), fc_switch (光纤交换机), protect_appliance (A8000备份一体机), security_appliance (数据安全一体机), ethernet_switch (以太网交换机), physical_server (服务器), virtual_machine (Virtual machine), logic_port (Logic port), file_system (Filesystem),
            resource_id: 资源 ID (必选, string, UUID 格式或 32 位十六进制字符, 正则 ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$),
        }, ...]
    
    Returns:
        create异步任务成功, 返回任务 ID. 
    """
    url = "/rest/tagmgmt/v1/tags/{tag_id}/disassociate-resources"
    
    payload = {
        'resources': resources
    }
    
    response = client.post(url, body=payload, params={"tag_id": tag_id})
    return response


# ==================== 可用分区管理 (az 子主题) ====================

def az_list(client: DMEAPIClient, az_name: str = None, operate_status: str = None,
         start: int = 1, limit: int = 512, is_sc: bool = False) -> dict:
    """
    批量query可用分区. 

    Args:
        client: DME API client
        az_name: 可用分区name, supports fuzzy match (可选, string, 1~64个字符)
        operate_status: 可用分区运营status. 对于未上线的az, 其operate_status是null, 因此暂时只支持过滤上线online的az (可选, string, 1~16个字符)
        start: 分页的页号, 从1开始 (可选, int32, 1~10000000). default值: 1
        limit: 分页的大小 (可选, int32, 1~512). default值: 512
        is_sc: 是否运营侧query (可选, boolean, true,false). default值: false

    Returns:
        {
            total: 可用分区total (integer),
            az_list: 可用分区list (List<GetAzResponse>). parameter format: [{
                id: 可用分区id (string),
                name: 可用分区name (string),
                description: 可用分区description (string),
                operate_status: 可用分区的运营status (string). default值: offline,
                site_urn: 站点urn (string, 1~64个字符),
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


# ==================== 数据中心管理 (dc 子主题) ====================

def dc_list(client: DMEAPIClient, name: str = None,
                     page_no: int = 1, page_size: int = 20) -> dict:
    """
    获取数据中心list
    
    query数据中心list, 支持按name过滤和分页. 
    
    Args:
        client: DME API client
        name: 数据中心name (可选, supports fuzzy query)
        page_no: pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含 total 和 datacenters 字段
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
    获取数据中心details
    
    query指定数据中心的详细info. 
    
    Args:
        client: DME API client
        dc_id: 数据中心 ID(Required)
    
    Returns:
        {
            id: data center ID (string),
            name: name (string),
            description: description (string),
            longitude: 经度 (number),
            latitude: 纬度 (number),
            device_num: 设备count (int32),
            critical_num: 紧急告警数 (int32),
            major_num: 重要告警数 (int32),
            minor_num: 次要告警数 (int32),
            info_num: 提示告警数 (int32),
            total_cpu: CPU总量 (int32),
            allocated_cpu: 已分配CPU (int32),
            total_memory: 内存总量 (int32),
            allocated_memory: 已分配内存 (int32),
            storage_total_usable_capacity: 存储总available capacity (int64),
            storage_total_used_capacity: 存储used capacity (int64),
        }
    """
    url = "/rest/dcmgmt/dcmgmtservice/v1/datacenters/{dc_id}"
    
    response = client.get(url, params={"dc_id": dc_id})
    return response


def dc_show_devices(client: DMEAPIClient, dc_id: str,
                 device_type: list = None, page_no: int = 1,
                 page_size: int = 20) -> dict:
    """
    query指定数据中心的设备listinfo
    
    Args:
        client: DME API client
        dc_id: 数据中心 ID(Required)
        device_type: 设备typelist(Optional)
                     取值: server, storage, network, switch, router, firewall,
                          loadbalancer, firewall_cluster, ipswitch, other
        page_no: pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含设备list
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
    批量queryRegion. 

    Args:
        client: DME API client
        ids: Region的IDlist, 支持精确匹配 (可选, List[string], max array members: 100)
        name: Region的name, 支持模糊搜索 (可选, string, 最多256个字符)
        active_ip_address: Region主IP address, 支持模糊搜索 (可选, string, 最多256个字符)
        standby_ip_address: Region备IP address, 支持模糊搜索 (可选, string, 最多256个字符)
        sync_status: Region同步status, 精确过滤 (可选, List[string], max array members: 3). valid values: normal (正常), sync (同步中), failed (同步失败)
        role: Regionrole, 精确过滤 (可选, string). valid values: parent (上级Region), child (下级Region)
        sort_key: 排序字段 (可选, string). valid values: last_sync_time (最近同步时间)
        sort_dir: 排序方向 (可选, string). valid values: asc (升序), desc (降序). default值: desc
        page_no: 分页query的开始页 (可选, int32, 1~100). default值: 1
        page_size: items per page (可选, int32, 1~100). default值: 20

    Returns:
        {
            total: total (integer),
            regions: Regionlist. parameter format: [{
                id: Region ID (string),
                name: Regionname (string),
                role: Regionrole (string),
                sync_status: 同步status (string),
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
    query下级Region资源info. 

    Args:
        client: DME API client
        region_id: 下级Region的ID (必选, string, 1~64个字符)
        request_url: query下级相应资源北向接口URL (必选, string, 1~8192个字符)
        request_method: 请求方式 (必选, string). valid values: get (Get请求), post (Post请求)
        request_body: 调用下级北向接口请求Body体 (可选, string, 1~20480个字符)

    Returns:
        无
    """
    url = "/rest/regionmgmt/v1/regions/{region_id}/resources/query"

    if not region_id:
        raise ValueError("region_id 是必选参数")
    if not request_url:
        raise ValueError("request_url 是必选参数")

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
    # 直接动作 (两级结构)
    'login': {
        'func': login,
        'description': '认证用户登录',
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
        'description': '查询产品系统信息',
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
    # subtopic action - user (three-level structure)
    'user_list': {
        'func': user_list,
        'description': '批量查询用户信息',
        'params': ['page_no', 'page_size', 'name'],
        'subtopic': 'user'
    },
    'user_show': {
        'func': user_show,
        'description': '查询指定用户信息',
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
    # subtopic action - role (three-level structure)
    'role_list': {
        'func': role_list,
        'description': '批量查询角色信息',
        'params': ['page_no', 'page_size', 'name'],
        'subtopic': 'role'
    },
    # subtopic action - backup_server (three-level structure)
    'backup_server_list': {
        'func': backup_server_list,
        'description': '批量查询备份服务器',
        'params': ['address', 'name', 'page_no', 'page_size'],
        'subtopic': 'backup_server'
    },
    # subtopic action - todo_task_group (three-level structure)
    'todo_task_group_list': {
        'func': todo_task_group_list,
        'description': '查询待办任务组列表',
        'params': ['group_id', 'name', 'creator_name', 'is_finished', 'is_group',
                   'start', 'limit', 'status', 'todo_item_status',
                   'start_time_from', 'start_time_to', 'end_time_from',
                   'end_time_to', 'sort_key', 'sort_dir'],
        'subtopic': 'todo_task_group'
    },
    'todo_task_group_execute': {
        'func': todo_task_group_execute,
        'description': '执行待办任务组',
        'params': ['group_id'],
        'subtopic': 'todo_task_group'
    },
    'todo_task_group_confirm': {
        'func': todo_task_group_confirm,
        'description': '确认执行定时待办任务组',
        'params': ['group_id'],
        'subtopic': 'todo_task_group'
    },
    # subtopic action - todo_task (three-level structure)
    'todo_task_list': {
        'func': todo_task_list,
        'description': '查询待办任务列表',
        'params': ['service_type', 'status', 'page_no', 'page_size'],
        'subtopic': 'todo_task'
    },
    'todo_task_show': {
        'func': todo_task_show,
        'description': '查询待办任务详情',
        'params': ['item_id'],
        'subtopic': 'todo_task'
    },
    'todo_task_execute': {
        'func': todo_task_execute,
        'description': '执行待办任务',
        'params': ['item_id'],
        'subtopic': 'todo_task'
    },
    'todo_task_audit': {
        'func': todo_task_audit,
        'description': '审核待办任务',
        'params': ['item_id', 'is_approval', 'suggestion'],
        'subtopic': 'todo_task'
    },
    'todo_task_revoke': {
        'func': todo_task_revoke,
        'description': '撤销审核待办项',
        'params': ['item_id'],
        'subtopic': 'todo_task'
    },
    'todo_task_close': {
        'func': todo_task_close,
        'description': '关闭待办任务',
        'params': ['item_id', 'reason'],
        'subtopic': 'todo_task'
    },
    # subtopic action - task (three-level structure)
    'task_show': {
        'func': task_show,
        'description': '查询指定任务详情',
        'params': ['task_id'],
        'subtopic': 'task'
    },
    'task_list': {
        'func': task_list,
        'description': '批量查询任务',
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
        'description': '等待任务完成',
        'params': ['task_id', 'timeout', 'poll_interval'],
        'subtopic': 'task'
    },
    # subtopic action - tag_type (three-level structure)
    'tag_type_create': {
        'func': tag_type_create,
        'description': '创建标签类型',
        'params': ['name', 'description'],
        'subtopic': 'tag_type'
    },
    'tag_type_list': {
        'func': tag_type_list,
        'description': '批量查询标签类型',
        'params': ['start', 'limit', 'name'],
        'subtopic': 'tag_type'
    },
    'tag_type_modify': {
        'func': tag_type_modify,
        'description': '修改标签类型',
        'params': ['tag_type_id', 'name', 'description'],
        'subtopic': 'tag_type'
    },
    'tag_type_delete': {
        'func': tag_type_delete,
        'description': '批量删除标签类型',
        'params': ['tag_type_ids'],
        'subtopic': 'tag_type'
    },
    # subtopic action - tag (three-level structure)
    'tag_create': {
        'func': tag_create,
        'description': '创建标签',
        'params': ['name', 'tag_type_id', 'tag_type_name', 'description', 'color'],
        'subtopic': 'tag'
    },
    'tag_list': {
        'func': tag_list,
        'description': '批量查询标签',
        'params': ['start', 'limit', 'name', 'tag_type_id'],
        'subtopic': 'tag'
    },
    'tag_modify': {
        'func': tag_modify,
        'description': '修改标签',
        'params': ['tag_id', 'name', 'description', 'color'],
        'subtopic': 'tag'
    },
    'tag_delete': {
        'func': tag_delete,
        'description': '批量删除标签',
        'params': ['tag_ids'],
        'subtopic': 'tag'
    },
    'tag_bind': {
        'func': tag_bind,
        'description': '标签关联资源',
        'params': ['tag_id', 'resources'],
        'subtopic': 'tag'
    },
    'tag_unbind': {
        'func': tag_unbind,
        'description': '标签取消关联资源',
        'params': ['tag_id', 'resources'],
        'subtopic': 'tag'
    },
    # subtopic action - az (three-level structure)
    'az_list': {
        'func': az_list,
        'description': '批量查询可用分区',
        'params': ['az_name', 'operate_status', 'start', 'limit', 'is_sc'],
        'subtopic': 'az'
    },
    # subtopic action - dc (three-level structure)
    'dc_list': {
        'func': dc_list,
        'description': '获取数据中心列表',
        'params': ['name', 'page_no', 'page_size'],
        'subtopic': 'dc'
    },
    'dc_show': {
        'func': dc_show,
        'description': '获取数据中心详情',
        'params': ['dc_id'],
        'subtopic': 'dc'
    },
    'dc_show_devices': {
        'func': dc_show_devices,
        'description': '查询指定数据中心的设备列表信息',
        'params': ['dc_id', 'device_type', 'page_no', 'page_size'],
        'subtopic': 'dc'
    },
    # region subtopic action
    'region_list': {
        'func': region_list,
        'description': '批量查询Region',
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
