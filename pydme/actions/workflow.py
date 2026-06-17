"""
工作流 (Workflow) 相关操作
"""

import sys
import os

from pydme.client import DMEAPIClient


# ==================== template 子主题 ====================

def template_list(client: DMEAPIClient, page_no: int, page_size: int,
                  directory_id: str = None, group: str = None,
                  name: str = None) -> dict:
    """
    分页query模板list
    
    分页query工作流模板list. 
    
    Args:
        client: DME API client
        page_no: 页索引号 (必选, 最小值: 1)
        page_size: 每页querycount (必选, 1~1000)
        directory_id: 目录 id (可选, 1~64 个字符)
        group: 模板所属分组name, supports fuzzy match (可选, 最多 255 个字符)
        name: 模板name, supports fuzzy match (可选, 最多 255 个字符)
    
    Returns:
        {
            total: 模板count (integer, 最大值: 500),
            templates: 模板list. parameter format: [{
                id: 模板ID (string),
                name: 模板name (string),
                description: description (string),
            }, ...],
        }
    """
    url = "/rest/wfamgmt/v1/workflow/templates/query"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if directory_id is not None:
        payload['directory_id'] = directory_id
    if group is not None:
        payload['group'] = group
    if name is not None:
        payload['name'] = name
    
    response = client.post(url, body=payload)
    return response


def template_groups(client: DMEAPIClient) -> dict:
    """
    query所有模板分组
    
    query所有工作流模板分组. 
    
    Args:
        client: DME API client
    
    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含: 
        - groups: 模板分组list, 包含 name (模板分组name)
    """
    url = "/rest/wfamgmt/v1/workflow/templates/groups/query"
    
    response = client.post(url, body={})
    return response


def template_show(client: DMEAPIClient, template_id: str,
                  template_version_id: str = None) -> dict:
    """
    query模板详细info
    
    query指定模板的详细info. 
    
    Args:
        client: DME API client
        template_id: 模板 id (必选, 1~64 个字符)
        template_version_id: 模板version id (可选, 1~64 个字符)
    
    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含: 
        - template_version_id: 模板version id
    """
    url = "/rest/wfamgmt/v1/workflow/templates/{template_id}"
    
    params_dict = {"template_id": template_id}
    if template_version_id is not None:
        params_dict['template_version_id'] = template_version_id
    
    response = client.get(url, params=params_dict)
    return response


# ==================== instance 子主题 ====================

def instance_stop(client: DMEAPIClient, instance_id: str) -> dict:
    """
    停止实例
    
    停止正在执行的工作流实例. 
    
    Args:
        client: DME API client
        instance_id: 实例的 id (必选, 1~64 个字符)
    
    Returns:
        operation result
    """
    url = "/rest/wfamgmt/v1/workflow/instances/{instance_id}/stop"
    
    response = client.post(url, body={}, params={"instance_id": instance_id})
    return response


def instance_show(client: DMEAPIClient, instance_id: str) -> dict:
    """
    query实例details
    
    query指定工作流实例的详细info. 
    
    Args:
        client: DME API client
        instance_id: query实例的 id (必选, 1~64 个字符)
    
    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含: 
        - instance_id: 实例 id
        - template_id: 实例对应的模板 id
        - template_name: 实例对应的模板name
        - state: 执行status (EXECUTING/SUCCESSFUL/FAILED/MANUAL_TERMINATED/ABNORMAL_TERMINATED)
        - stage: 执行阶段 (PRECHECK/MAIN/NORMAL_END/ABNORMAL_END)
        - params: 执行实例参数
        - step_list: 实例的步骤list
        - start_time: 实例执行的start time (毫秒)
        - end_time: 实例执行的end time (毫秒)
        - instance_type: 实例type (PRECHECK/EXECUTION)
        - template_version_id: 实例对应的模板version id
    """
    url = "/rest/wfamgmt/v1/workflow/instances/{instance_id}"
    
    response = client.get(url, params={"instance_id": instance_id})
    return response


def instance_create(client: DMEAPIClient, template_id: str = None,
                    template_version_id: str = None,
                    instance_id: str = None,
                    params: dict = None) -> dict:
    """
    create并执行实例
    
    create并执行工作流实例. 可以通过指定模板 id 与模板version id (模板version id 未指定时default为最新version)
    来create实例并执行, 也可以通过指定实例 id 来找到对应实例对应的模板create实例并执行. 
    
    Args:
        client: DME API client
        template_id: 模板 id (可选, 1~64 个字符, 满足正则)
        template_version_id: 模板version id (可选, 1~64 个字符, 满足正则)
        instance_id: 实例的 id (可选, 1~64 个字符, 满足正则)
        params: 执行实例参数(Optional), 格式: {"key1": "value1", "key2": "value2"}, 最多 100 个参数
    
    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含: 
        - instance_id: 实例 id
    """
    url = "/rest/wfamgmt/v1/workflow/instances"
    
    payload = {}
    
    if template_id is not None:
        payload['template_id'] = template_id
    if template_version_id is not None:
        payload['template_version_id'] = template_version_id
    if instance_id is not None:
        payload['instance_id'] = instance_id
    if params is not None:
        payload['params'] = params
    
    response = client.post(url, body=payload)
    return response


def instance_step_log(client: DMEAPIClient, instance_id: str, step_id: str) -> dict:
    """
    query步骤日志
    
    query工作流实例中指定步骤的执行日志. 
    
    Args:
        client: DME API client
        instance_id: 实例 id (必选, 1~64 个字符)
        step_id: 步骤 id (必选, 1~64 个字符)
    
    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含: 
        - logs: 步骤日志list (最多 6000 条)
    """
    url = "/rest/wfamgmt/v1/workflow/instances/{instance_id}/steps/{step_id}/log"
    
    response = client.get(url, params={"instance_id": instance_id, "step_id": step_id})
    return response


# ==================== 动作注册info ====================

ACTIONS = {
    # template subtopic action
    'template_list': {
        'func': template_list,
        'description': '分页查询模板列表',
        'params': ['page_no', 'page_size', 'directory_id', 'group', 'name'],
        'subtopic': 'template'
    },
    'template_groups': {
        'func': template_groups,
        'description': '查询所有模板分组',
        'params': [],
        'subtopic': 'template'
    },
    'template_show': {
        'func': template_show,
        'description': '查询模板详细信息',
        'params': ['template_id', 'template_version_id'],
        'subtopic': 'template'
    },
    # instance subtopic action
    'instance_stop': {
        'func': instance_stop,
        'description': '停止实例',
        'params': ['instance_id'],
        'subtopic': 'instance'
    },
    'instance_show': {
        'func': instance_show,
        'description': '查询实例详情',
        'params': ['instance_id'],
        'subtopic': 'instance'
    },
    'instance_create': {
        'func': instance_create,
        'description': '创建并执行实例',
        'params': ['template_id', 'template_version_id', 'instance_id', 'params'],
        'subtopic': 'instance'
    },
    'instance_step_log': {
        'func': instance_step_log,
        'description': '查询步骤日志',
        'params': ['instance_id', 'step_id'],
        'subtopic': 'instance'
    }
}