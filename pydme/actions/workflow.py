"""
Workflow (Workflow) operations
"""

import sys
import os

from pydme.client import DMEAPIClient


# ==================== template Subtopic ====================

def template_list(client: DMEAPIClient, page_no: int, page_size: int,
                  directory_id: str = None, group: str = None,
                  name: str = None) -> dict:
    """
    PaginationTemplate list
    
    PaginationWorkflowTemplate list。
    
    Args:
        client: DME API client
        page_no: Page index（Required，min：1）
        page_size: 每页查询count（Required，1~1000）
        directory_id: 目录 id（Optional，1~64  characters）
        group: Template group name，supports fuzzy match（Optional，最多 255  characters）
        name: 模板名称，supports fuzzy match（Optional，最多 255  characters）
    
    Returns:
        {
            total: 模板count (integer, max：500),
            templates: Template list。参数格式如下：[{
                id: 模板ID (string),
                name: 模板名称 (string),
                description: 描述 (string),
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
    Query allTemplate group
    
    Query allWorkflowTemplate group。
    
    Args:
        client: DME API client
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含：
        - groups: Template group列表，包含 name（Template group名称）
    """
    url = "/rest/wfamgmt/v1/workflow/templates/groups/query"
    
    response = client.post(url, body={})
    return response


def template_show(client: DMEAPIClient, template_id: str,
                  template_version_id: str = None) -> dict:
    """
    查询模板Details
    
    Query模板的Details。
    
    Args:
        client: DME API client
        template_id: 模板 id（Required，1~64  characters）
        template_version_id: Template version id（Optional，1~64  characters）
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含：
        - template_version_id: Template version id
    """
    url = "/rest/wfamgmt/v1/workflow/templates/{template_id}"
    
    params_dict = {}
    if template_version_id is not None:
        params_dict['template_version_id'] = template_version_id
    
    response = client.get(url, params=params_dict)
    return response


# ==================== instance Subtopic ====================

def instance_stop(client: DMEAPIClient, instance_id: str) -> dict:
    """
    停止实例
    
    停止Executing的Workflow实例。
    
    Args:
        client: DME API client
        instance_id: 实例的 id（Required，1~64  characters）
    
    Returns:
        无
    """
    url = "/rest/wfamgmt/v1/workflow/instances/{instance_id}/stop"
    
    response = client.post(url, body={}, params={"instance_id": instance_id})
    return response


def instance_show(client: DMEAPIClient, instance_id: str) -> dict:
    """
    Query instance details
    
    QueryWorkflow实例的Details。
    
    Args:
        client: DME API client
        instance_id: 查询实例的 id（Required，1~64  characters）
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含：
        - instance_id: 实例 id
        - template_id: Instance template id
        - template_name: Instance template名称
        - state: 执行状态（EXECUTING/SUCCESSFUL/FAILED/MANUAL_TERMINATED/ABNORMAL_TERMINATED）
        - stage: 执行阶段（PRECHECK/MAIN/NORMAL_END/ABNORMAL_END）
        - params: Execute instance parameters
        - step_list: Instance step list
        - start_time: 实例执行的Start time（毫second(s)）
        - end_time: 实例执行的End time（毫second(s)）
        - instance_type: 实例类型（PRECHECK/EXECUTION）
        - template_version_id: Instance template版本 id
    """
    url = "/rest/wfamgmt/v1/workflow/instances/{instance_id}"
    
    response = client.get(url, params={"instance_id": instance_id})
    return response


def instance_create(client: DMEAPIClient, template_id: str = None,
                    template_version_id: str = None,
                    instance_id: str = None,
                    params: dict = None) -> dict:
    """
    Create and execute instance
    
    Create and execute workflow instance。by specifying template id 与Template version id（Template version id default if not specified为最新版本）
    to create and execute instance，or by specifying instance id 来找到对应Instance templateCreate and execute instance。
    
    Args:
        client: DME API client
        template_id: 模板 id（Optional，1~64  characters，satisfies regex）
        template_version_id: Template version id（Optional，1~64  characters，satisfies regex）
        instance_id: 实例的 id（Optional，1~64  characters，satisfies regex）
        params: Execute instance parameters（Optional），格式：{"key1": "value1", "key2": "value2"}，最多 100 个参数
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含：
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
    Query step log
    
    查询WorkflowExecution log of specified step in instance。
    
    Args:
        client: DME API client
        instance_id: 实例 id（Required，1~64  characters）
        step_id: 步骤 id（Required，1~64  characters）
    
    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含：
        - logs: Step log list（最多 6000 条）
    """
    url = "/rest/wfamgmt/v1/workflow/instances/{instance_id}/steps/{step_id}/log"
    
    response = client.get(url, params={"instance_id": instance_id, "step_id": step_id})
    return response


# ==================== Action registration info ====================

ACTIONS = {
    # template subtopic actions
    'template_list': {
        'func': template_list,
        'description': 'PaginationTemplate list',
        'params': ['page_no', 'page_size', 'directory_id', 'group', 'name'],
        'subtopic': 'template'
    },
    'template_groups': {
        'func': template_groups,
        'description': 'Query allTemplate group',
        'params': [],
        'subtopic': 'template'
    },
    'template_show': {
        'func': template_show,
        'description': '查询模板Details',
        'params': ['template_id', 'template_version_id'],
        'subtopic': 'template'
    },
    # instance subtopic actions
    'instance_stop': {
        'func': instance_stop,
        'description': '停止实例',
        'params': ['instance_id'],
        'subtopic': 'instance'
    },
    'instance_show': {
        'func': instance_show,
        'description': 'Query instance details',
        'params': ['instance_id'],
        'subtopic': 'instance'
    },
    'instance_create': {
        'func': instance_create,
        'description': 'Create and execute instance',
        'params': ['template_id', 'template_version_id', 'instance_id', 'params'],
        'subtopic': 'instance'
    },
    'instance_step_log': {
        'func': instance_step_log,
        'description': 'Query step log',
        'params': ['instance_id', 'step_id'],
        'subtopic': 'instance'
    }
}