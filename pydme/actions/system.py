"""
系统管理 (System) 相关操作
"""

import sys
import os

from pydme.client import DMEAPIClient


def login(client: DMEAPIClient) -> dict:
    """
    认证用户登录

    强制调用 client.login() 完成认证，然后从 header 获取 accessSession，
    提示用户可配置环境变量复用认证密钥，避免重复登录。

    Args:
        client: DME API 客户端

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }，包含 accessSession
        - accessSession: 会话 token，用于后续请求的 X-Auth-Token header
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
    注销当前已经登录的三方会话或普通会话。

    Args:
        client: DME API 客户端

    Returns:
        无
    """
    url = "/rest/plat/smapp/v1/sessions"
    
    response = client.delete(url)
    return response


def reset_password(client: DMEAPIClient, user_name: str, new_value: str,
                   is_initial_password: bool = True) -> dict:
    """
    根据指定用户名重置指定用户的密码，重置不需要原始密码，因此，执行该接口的三方用户角色权限必须是安全管理员角色。

    Args:
        client: DME API 客户端
        user_name: 需要重置密码的用户名 (必选, string, 1~128个字符)
        new_value: 新密码 (必选, string, 8~32个字符)。要求：1. 密码长度不能小于8个字符、大于32个字符。2. 密码中至少包含2个字母，至少包含1个大写字母，至少包含1个小写字母，至少包含1个数字，至少包含1个特殊字符（!"#$%&'()*+,-./:;<=>?@[]^`{|}~）。3. 密码中同一字符连续出现次数不能超过2，不能包含重复字符序列（重复次数为4，重复序列字符数为1）。4. 密码不能包含用户名和用户名的倒序，不能包含用户手机号码和电子邮箱帐号，不能包含密码字典中的词汇。
        is_initial_password: 标识密码重置后当下次登录时是否必须修改密码 (必选, boolean, true,false)。true：下次登录系统时必须执行初始化修改；false：下次直接登录系统，不需初始化修改。默认值：true

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
    删除用户。该API可能会直接或间接影响现网业务运行，导致业务中断、关键数据丢失等，请谨慎操作。

    Args:
        client: DME API 客户端
        user_id: 用户ID (必选, integer, 11~2147483647)

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
    创建用户。

    Args:
        client: DME API 客户端
        name: 用户名 (必选, string, 最多32个字符)。本地用户名不能小于6个字符，大于32个字符，不能包含空格、转义字符、不可见字符和特殊字符。远端用户名不能小于1个字符，大于32个字符，不能包含不可见字符和;特殊字符。
        type: 用户类型 (必选, integer, 无)。0：本地用户；2：远端用户。
        value: 密码 (可选, string, 8~32个字符)。密码长度不能小于8个字符、大于32个字符。密码中至少包含2个字母，至少包含1个大写字母，至少包含1个小写字母，至少包含1个数字，至少包含1个特殊字符。远端用户不涉及。
        description: 描述 (可选, string, 最多127个字符)
        roles: 用户所属角色 (可选, List[integer], 数组最大成员个数：10)。如Administrators，北向用户组，安全管理员组，文件系统组或用户自定义角色。

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
    批量查询用户信息。

    Args:
        client: DME API 客户端
        page_no: 页数 (必选, integer, 最小值：1)。默认值：1
        page_size: 页面大小 (必选, integer, 5~200)。默认值：10
        name: 用户名搜索关键字 (可选, string, 最多32个字符)

    Returns:
        {
            total: 总数 (integer, 最大值：5000),
            datas: 用户数据 (List<UserData>, 数组最大成员个数：5000)。参数格式如下：[{
                id: 用户ID (integer, 1~2147483647),
                name: 用户名 (string, 6~32个字符),
                description: 描述 (string, 最多127个字符),
                type: 用户类型 (integer)。可选值：0 (本地用户), 1 (三方系统接入用户), 2 (远端用户),
                roles: 角色ID列表 (List<integer>, 数组最大成员个数：50),
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
    批量查询角色信息。

    Args:
        client: DME API 客户端
        page_no: 页数 (必选, integer, 最小值：1)。默认值：1
        page_size: 页面大小 (必选, integer, 5~100)。默认值：10
        name: 角色名搜索关键字 (可选, string, 最多64个字符)

    Returns:
        {
            total: 总数 (integer, 最大值：10),
            datas: 角色数据 (List<RoleData>, 数组最大成员个数：5000)。参数格式如下：[{
                id: 角色ID (integer, 1~2147483647),
                name: 角色名称 (string, 最多64个字符),
                description: 描述 (string, 最多127个字符),
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
    查询指定用户信息。

    Args:
        client: DME API 客户端
        user_id: 用户ID (必选, integer, 1~2147483647)

    Returns:
        {
            id: 用户ID (integer, 1~2147483647),
            name: 用户名 (string, 最多32个字符),
            type: 用户类型 (integer)。可选值：0 (本地用户), 1 (三方系统接入用户), 2 (远端用户),
            description: 描述 (string, 最多127个字符),
            roles: 用户所属角色 (List<integer>, 数组最大成员个数：50),
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
    查询产品系统信息。

    Args:
        client: DME API 客户端

    Returns:
        {
            version: DME产品版本信息 (string, 最多128个字符),
            sn: DME产品SN号 (string, 最多64个字符),
        }
    """
    url = "/rest/productmgmt/v1/system-info"
    
    response = client.get(url)
    return response


def certificate(client: DMEAPIClient, service_type: str = "APIGWService") -> dict:
    """
    获取DME证书。

    Args:
        client: DME API 客户端
        service_type: 服务类型 (必选, string)。可选值：APIGWService (DME北向网关)

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
    批量查询备份服务器。

    Args:
        client: DME API 客户端
        address: 备份服务器地址，支持IPv4地址，支持模糊匹配 (可选, string, 1~256个字符)
        name: 备份服务器名称 (可选, string)
        page_no: 分页查询的起始页码 (可选, int32)。默认值：1
        page_size: 每页数量 (可选, int32, 1~1000)。默认值：20

    Returns:
        {
            total: 备份服务器总数 (int32),
            backup_servers: 备份服务器列表 (List<BackupServerInfo>)。参数格式如下：[{
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


# ==================== 待办任务组管理（todo_task_group 子主题） ====================

def todo_task_group_list(client: DMEAPIClient, group_id: str = None, name: str = None,
               creator_name: str = None, is_finished: bool = None,
               is_group: bool = None, start: int = None, limit: int = None,
               status: list = None, todo_item_status: list = None,
               start_time_from: str = None, start_time_to: str = None,
               end_time_from: str = None, end_time_to: str = None,
               sort_key: str = None, sort_dir: str = None) -> dict:
    """
    查询待办任务组列表

    Args:
        client: DME API 客户端
        group_id: 待办任务组 ID（可选）
        name: 待办任务组名称（可选）
        creator_name: 创建人名称（可选）
        is_finished: 是否已完成（可选）
        is_group: 是否群组任务（可选）
        start: 分页起始位置（可选，0~10000000）
        limit: 分页个数（可选，1~1000）
        status: 待办任务组状态列表（可选，1-待处理/2-执行中/3-已完成/4-已关闭）
        todo_item_status: 待办项状态列表（可选，0-待确认/1-未完成/2-执行中/3-已完成）
        start_time_from: 开始时间起始值（可选，格式：yyyy-MM-dd HH:mm:ss）
        start_time_to: 开始时间结束值（可选，格式：yyyy-MM-dd HH:mm:ss）
        end_time_from: 结束时间起始值（可选，格式：yyyy-MM-dd HH:mm:ss）
        end_time_to: 结束时间结束值（可选，格式：yyyy-MM-dd HH:mm:ss）
        sort_key: 排序字段（可选）
        sort_dir: 排序方式（可选，asc/desc）

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }，包含待办任务组列表和总数
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

    执行指定的待办任务组。

    Args:
        client: DME API 客户端
        group_id: 待办任务组 ID（必选）

    Returns:
        执行结果，包含 task_id
    """
    url = "/rest/taskmgmt/v1/todo-groups/{group_id}/execute"

    response = client.put(url, body={}, params={"group_id": group_id})
    return response


def todo_task_group_confirm(client: DMEAPIClient, group_id: str) -> dict:
    """
    确认执行定时待办任务组

    Args:
        client: DME API 客户端
        group_id: 待办任务组 ID（必选）

    Returns:
        确认结果
    """
    url = "/rest/taskmgmt/v1/todo-groups/{group_id}/confirm"

    response = client.put(url, body={}, params={"group_id": group_id})
    return response


# ==================== 待办任务管理（todo_task 子主题） ====================

def todo_task_list(client: DMEAPIClient, service_type: str,
               status: list = None, page_no: int = None,
               page_size: int = None) -> dict:
    """
    批量查询待办任务详情

    批量查询待办项列表，支持过滤和分页。

    Args:
        client: DME API 客户端
        service_type: 业务类型（必选，wfa_execute_activity-自动化编排）
        status: 待办项状态列表（可选，1-未执行/2-执行中/3-成功/4-部分成功/5-失败/6-超时/7-警告/8-已关闭/9-待审核/10-审核不通过/21-预检查中/22-预检查失败）
        page_no: 页索引号（可选，默认 1）
        page_size: 每页数量（可选，1~10，默认 10）

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }，包含待办项列表和总数
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
    查询待办项详情信息

    查询指定待办项的详细信息。

    Args:
        client: DME API 客户端
        item_id: 待办项 ID（必选）

    Returns:
        待办项详细信息
    """
    url = "/rest/taskmgmt/v1/todo-items/{item_id}"

    response = client.get(url, params={"item_id": item_id})
    return response


def todo_task_execute(client: DMEAPIClient, item_id: str) -> dict:
    """
    执行待办任务

    执行指定的待办项。

    Args:
        client: DME API 客户端
        item_id: 待办项 ID（必选）

    Returns:
        执行结果，包含 task_id
    """
    url = "/rest/taskmgmt/v1/todo-items/{item_id}/execute"

    response = client.put(url, body={}, params={"item_id": item_id})
    return response


def todo_task_audit(client: DMEAPIClient, item_id: str, is_approval: bool,
          suggestion: str = None) -> dict:
    """
    审核待办任务

    对待办项进行审核（批准或拒绝）。

    Args:
        client: DME API 客户端
        item_id: 待办项 ID（必选）
        is_approval: 是否批准（必选，true-批准/false-拒绝）
        suggestion: 审核建议（可选，0-63 字符）

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
    撤销审核待办项

    撤销对指定待办项的审核。

    Args:
        client: DME API 客户端
        item_id: 待办项 ID（必选）

    Returns:
        撤销结果
    """
    url = "/rest/taskmgmt/v1/todo-items/{item_id}/revoke-audit"

    response = client.put(url, body={}, params={"item_id": item_id})
    return response


def todo_task_close(client: DMEAPIClient, item_id: str, reason: str) -> dict:
    """
    关闭待办任务

    关闭指定的待办项，需要提供关闭原因。

    Args:
        client: DME API 客户端
        item_id: 待办项 ID（必选）
        reason: 关闭原因（必选，0-63 字符）

    Returns:
        关闭结果
    """
    url = "/rest/taskmgmt/v1/todo-items/{item_id}/close"

    payload = {
        'reason': reason
    }

    response = client.put(url, body=payload, params={"item_id": item_id})
    return response


# ==================== 任务管理（task 子主题） ====================

import time

def task_show(client: DMEAPIClient, task_id: str) -> list:
    """
    查询指定任务详情
    
    根据任务唯一标识 TaskId 进行查询。
    
    Args:
        client: DME API 客户端
        task_id: 任务 ID（必选，1~36 个字符）
    
    Returns:
        任务详情列表，包含：
        - id: 任务 ID
        - name_en: 任务英文名称
        - name_cn: 任务中文名称
        - description: 任务描述
        - parent_id: 父任务 ID
        - seq_no: 任务序号
        - status: 状态（1-初始状态;2-执行中;3-成功;4-部分成功;5-失败;6-超时）
        - progress: 任务进度
        - owner_name: 创建任务用户名称
        - owner_id: 创建任务用户 ID
        - create_time: 任务创建时间（UTC 毫秒数）
        - start_time: 任务开始时间（UTC 毫秒数）
        - end_time: 任务结束时间（UTC 毫秒数）
        - detail_en: 任务英文详情
        - detail_cn: 任务中文详情
        - is_support_retry: 是否支持重试
        - is_support_rollback: 是否支持回滚
        - remarks: 备注信息
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
    批量查询任务
    
    Args:
        client: DME API 客户端
        start: 分页起始位置，默认 1
        limit: 分页数量，默认 100
        task_name: 任务名称过滤（可选）
        status: 状态过滤（可选，1-初始状态;2-执行中;3-成功;4-部分成功;5-失败;6-超时）
        owner_id: 创建任务用户 ID 过滤（可选）
        create_time_from: 创建时间起始（可选，UTC 毫秒数）
        create_time_to: 创建时间结束（可选，UTC 毫秒数）
    
    Returns:
        任务列表
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
        client: DME API 客户端
        task_id: 任务 ID（必选，1~36 个字符）

    Returns:
        重试结果
    """
    url = "/rest/taskmgmt/v1/tasks/{task_id}/retry"

    response = client.post(url, body={}, params={"task_id": task_id})
    return response


def task_wait(client: DMEAPIClient, task_id: str, timeout: int = 300,
              poll_interval: int = 2) -> dict:
    """
    等待任务完成

    轮询查询任务状态，直到任务完成或超时。

    Args:
        client: DME API 客户端
        task_id: 任务 ID
        timeout: 超时时间（秒），默认 300 秒
        poll_interval: 轮询间隔（秒），默认 2 秒

    Returns:
        任务最终状态详情
        status 说明：
        - 3: 成功
        - 4: 部分成功
        - 5: 失败
        - 6: 超时
    """
    start_time = time.time()

    while True:
        task_info = task_show(client, task_id)

        # API 返回的是列表，获取根任务详情
        for task in task_info:
            if task["id"] == task_id:
                root_task = task
                break

        status = root_task.get('status')

        # 检查任务是否完成
        if status in [3, 4, 5, 6]:  # 成功、部分成功、失败、超时
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


# ==================== 标签类型管理（tag_type 子主题） ====================

def tag_type_create(client: DMEAPIClient, name: str, description: str = None) -> dict:
    """
    创建标签类型
    
    Args:
        client: DME API 客户端
        name: 标签类型名称（必选）
        description: 标签类型描述（可选）
    
    Returns:
        创建的标签类型信息
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
    批量查询标签类型
    
    Args:
        client: DME API 客户端
        start: 分页起始位置，默认 1
        limit: 分页数量，默认 100
        name: 标签类型名称过滤（可选）
    
    Returns:
        标签类型列表
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
    修改标签类型
    
    Args:
        client: DME API 客户端
        tag_type_id: 标签类型 ID（必选）
        name: 标签类型名称（可选）
        description: 标签类型描述（可选）
    
    Returns:
        修改后的标签类型信息
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
    批量删除标签类型
    
    Args:
        client: DME API 客户端
        tag_type_ids: 标签类型 ID 列表（必选）
    
    Returns:
        批量删除结果
    """
    url = "/rest/tagmgmt/v1/tag-types/delete"
    
    payload = {
        'ids': tag_type_ids
    }
    
    response = client.post(url, body=payload)
    return response


# ==================== 标签管理（tag 子主题） ====================

def tag_create(client: DMEAPIClient, name: str, tag_type_id: str,
                tag_type_name: str = None, description: str = None, color: str = None) -> dict:
    """
    创建标签
    
    Args:
        client: DME API 客户端
        name: 标签名称（必选）
        tag_type_id: 标签类型 ID（必选）
        tag_type_name: 标签类型名称（API 需要）
        description: 标签描述（可选）
        color: 标签颜色（可选）
    
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
    批量查询标签
    
    Args:
        client: DME API 客户端
        start: 分页起始位置，默认 1
        limit: 分页数量，默认 100
        name: 标签名称过滤（可选）
        tag_type_id: 标签类型 ID 过滤（可选）
    
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
    修改标签
    
    Args:
        client: DME API 客户端
        tag_id: 标签 ID（必选）
        name: 标签名称（可选）
        description: 标签描述（可选）
        color: 标签颜色（可选）
    
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
    批量删除标签
    
    Args:
        client: DME API 客户端
        tag_ids: 标签 ID 列表（必选）
    
    Returns:
        批量删除结果
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
        client: DME API 客户端
        tag_id: 标签 ID（必选）
        resources: 资源列表，格式为 [{"resource_id": "xxx", "resource_type": "xxx"}]（必选）
    
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
    标签取消关联资源
    
    Args:
        client: DME API 客户端
        tag_id: 标签 ID（必选）
        resources: 资源列表，格式为 [{"resource_id": "xxx", "resource_type": "xxx"}]（必选）
    
    Returns:
        取消关联结果
    """
    url = "/rest/tagmgmt/v1/tags/{tag_id}/disassociate-resources"
    
    payload = {
        'resources': resources
    }
    
    response = client.post(url, body=payload, params={"tag_id": tag_id})
    return response


# ==================== 可用分区管理（az 子主题） ====================

def az_list(client: DMEAPIClient, az_name: str = None, operate_status: str = None,
         start: int = 1, limit: int = 512, is_sc: bool = False) -> dict:
    """
    批量查询可用分区。

    Args:
        client: DME API 客户端
        az_name: 可用分区名称，支持模糊匹配 (可选, string, 1~64个字符)
        operate_status: 可用分区运营状态。对于未上线的az，其operate_status是null，因此暂时只支持过滤上线online的az (可选, string, 1~16个字符)
        start: 分页的页号，从1开始 (可选, int32, 1~10000000)。默认值：1
        limit: 分页的大小 (可选, int32, 1~512)。默认值：512
        is_sc: 是否运营侧查询 (可选, boolean, true,false)。默认值：false

    Returns:
        {
            total: 可用分区总数 (integer),
            az_list: 可用分区列表 (List<GetAzResponse>)。参数格式如下：[{
                id: 可用分区id (string),
                name: 可用分区名称 (string),
                description: 可用分区描述 (string),
                operate_status: 可用分区的运营状态 (string)。默认值：offline,
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


# ==================== 数据中心管理（dc 子主题） ====================

def dc_list(client: DMEAPIClient, name: str = None,
                     page_no: int = 1, page_size: int = 20) -> dict:
    """
    获取数据中心列表
    
    查询数据中心列表，支持按名称过滤和分页。
    
    Args:
        client: DME API 客户端
        name: 数据中心名称（可选，支持模糊查询）
        page_no: 分页查询的起始页码，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
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
    获取数据中心详情
    
    查询指定数据中心的详细信息。
    
    Args:
        client: DME API 客户端
        dc_id: 数据中心 ID（必选）
    
    Returns:
        数据中心详细信息
    """
    url = "/rest/dcmgmt/dcmgmtservice/v1/datacenters/{dc_id}"
    
    response = client.get(url, params={"dc_id": dc_id})
    return response


def dc_show_devices(client: DMEAPIClient, dc_id: str,
                 device_type: list = None, page_no: int = 1,
                 page_size: int = 20) -> dict:
    """
    查询指定数据中心的设备列表信息
    
    Args:
        client: DME API 客户端
        dc_id: 数据中心 ID（必选）
        device_type: 设备类型列表（可选）
                     取值：server, storage, network, switch, router, firewall,
                          loadbalancer, firewall_cluster, ipswitch, other
        page_no: 分页查询的起始页码，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
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


# 动作列表，用于 CLI 帮助
ACTIONS = {
    # 直接动作（两级结构）
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
    # 子主题动作 - user（三级结构）
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
    # 子主题动作 - role（三级结构）
    'role_list': {
        'func': role_list,
        'description': '批量查询角色信息',
        'params': ['page_no', 'page_size', 'name'],
        'subtopic': 'role'
    },
    # 子主题动作 - backup_server（三级结构）
    'backup_server_list': {
        'func': backup_server_list,
        'description': '批量查询备份服务器',
        'params': ['address', 'name', 'page_no', 'page_size'],
        'subtopic': 'backup_server'
    },
    # 子主题动作 - todo_task_group（三级结构）
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
    # 子主题动作 - todo_task（三级结构）
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
    # 子主题动作 - task（三级结构）
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
    # 子主题动作 - tag_type（三级结构）
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
    # 子主题动作 - tag（三级结构）
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
    # 子主题动作 - az（三级结构）
    'az_list': {
        'func': az_list,
        'description': '批量查询可用分区',
        'params': ['az_name', 'operate_status', 'start', 'limit', 'is_sc'],
        'subtopic': 'az'
    },
    # 子主题动作 - dc（三级结构）
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
}
