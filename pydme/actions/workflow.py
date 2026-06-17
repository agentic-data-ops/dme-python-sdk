"""
Workflow related operations
"""

import sys
import os

from pydme.client import DMEAPIClient


# ==================== template subtopic ====================

def template_list(client: DMEAPIClient, page_no: int, page_size: int,
                  directory_id: str = None, group: str = None,
                  name: str = None) -> dict:
    """
    Paginated query template list
    
    Paginated query of workflow template list.
    
    Args:
        client: DME API client
        page_no: Page index (required, minimum: 1)
        page_size: Number of items per page (required, 1~1000)
        directory_id: Directory id (optional, 1~64 characters)
        group: Template group name, supports fuzzy match (optional, at most 255 characters)
        name: Template name, supports fuzzy match (optional, at most 255 characters)
    
    Returns:
        {
            total: Template count (integer, max: 500),
            templates: Template list. parameter format: [{
                id: Template ID (string),
                name: Template name (string),
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
    Query all template groups
    
    Query all workflow template groups.
    
    Args:
        client: DME API client
    
    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, including:
        - groups: Template group list, containing name (template group name)
    """
    url = "/rest/wfamgmt/v1/workflow/templates/groups/query"
    
    response = client.post(url, body={})
    return response


def template_show(client: DMEAPIClient, template_id: str,
                  template_version_id: str = None) -> dict:
    """
    Query template detailed info
    
    Query detailed info of a specified template.
    
    Args:
        client: DME API client
        template_id: Template id (required, 1~64 characters)
        template_version_id: Template version id (optional, 1~64 characters)
    
    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, including:
        - template_version_id: Template version id
    """
    url = "/rest/wfamgmt/v1/workflow/templates/{template_id}"
    
    params_dict = {"template_id": template_id}
    if template_version_id is not None:
        params_dict['template_version_id'] = template_version_id
    
    response = client.get(url, params=params_dict)
    return response


# ==================== instance subtopic ====================

def instance_stop(client: DMEAPIClient, instance_id: str) -> dict:
    """
    Stop instance
    
    Stop a running workflow instance.
    
    Args:
        client: DME API client
        instance_id: Instance id (required, 1~64 characters)
    
    Returns:
        operation result
    """
    url = "/rest/wfamgmt/v1/workflow/instances/{instance_id}/stop"
    
    response = client.post(url, body={}, params={"instance_id": instance_id})
    return response


def instance_show(client: DMEAPIClient, instance_id: str) -> dict:
    """
    Query instance details
    
    Query detailed info of a specified workflow instance.
    
    Args:
        client: DME API client
        instance_id: Instance id to query (required, 1~64 characters)
    
    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, including:
        - instance_id: Instance id
        - template_id: Template id of the instance
        - template_name: Template name of the instance
        - state: Execution status (EXECUTING/SUCCESSFUL/FAILED/MANUAL_TERMINATED/ABNORMAL_TERMINATED)
        - stage: Execution stage (PRECHECK/MAIN/NORMAL_END/ABNORMAL_END)
        - params: Execution instance parameters
        - step_list: Step list of the instance
        - start_time: Instance start time (milliseconds)
        - end_time: Instance end time (milliseconds)
        - instance_type: Instance type (PRECHECK/EXECUTION)
        - template_version_id: Template version id of the instance
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
    
    Create and execute a workflow instance. It can create and execute an instance by specifying
    template id and template version id (when template version id is not specified, the latest version
    is used by default), or it can create and execute an instance by finding the template
    corresponding to an existing instance id.
    
    Args:
        client: DME API client
        template_id: Template id (optional, 1~64 characters, matching regex)
        template_version_id: Template version id (optional, 1~64 characters, matching regex)
        instance_id: Instance id (optional, 1~64 characters, matching regex)
        params: Execution instance parameters (Optional), format: {"key1": "value1", "key2": "value2"}, at most 100 parameters
    
    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, including:
        - instance_id: Instance id
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
    
    Query the execution log of a specified step in a workflow instance.
    
    Args:
        client: DME API client
        instance_id: Instance id (required, 1~64 characters)
        step_id: Step id (required, 1~64 characters)
    
    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, including:
        - logs: Step log list (at most 6000 entries)
    """
    url = "/rest/wfamgmt/v1/workflow/instances/{instance_id}/steps/{step_id}/log"
    
    response = client.get(url, params={"instance_id": instance_id, "step_id": step_id})
    return response


# ==================== action registration info ====================

ACTIONS = {
    # template subtopic action
    'template_list': {
        'func': template_list,
        'description': 'Paginated query template list',
        'params': ['page_no', 'page_size', 'directory_id', 'group', 'name'],
        'subtopic': 'template'
    },
    'template_groups': {
        'func': template_groups,
        'description': 'Query all template groups',
        'params': [],
        'subtopic': 'template'
    },
    'template_show': {
        'func': template_show,
        'description': 'Query template detailed info',
        'params': ['template_id', 'template_version_id'],
        'subtopic': 'template'
    },
    # instance subtopic action
    'instance_stop': {
        'func': instance_stop,
        'description': 'Stop instance',
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
