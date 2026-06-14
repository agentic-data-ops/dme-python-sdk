"""
Tenant self-service (Self Service) operations

Tenant self-service用于management Service level和Project group。
"""

import sys
import os

from pydme.client import DMEAPIClient

# ============ lun subtopic functions ============


def lun_create(client: DMEAPIClient, volumes: list,
               service_level_id: str, task_remarks: str = None,
               project_id: str = None, availability_zone: str = None,
               scheduler_hints: dict = None, mapping: dict = None) -> dict:
    """
    ServiceBatch create LUN

    Args:
        client: DME API client
        volumes: 待create  LUN Basic parameter list (List<ServiceVolumeBasicParams>, max array members: 1000)。 parameter format：[{
                name: LUN name (1~255 characters, supports alphanumeric._-and Chinese characters),
                capacity:  capacityGB (1~262144),
                count: create count (1~500),
                description:  description (0~255 characters),
                start_suffix: Starting suffix number (0~9999),
                suffix_length: Suffix length rule (1~4,  name length+后缀 length<=255),
             }, ...]
        service_level_id: Service level ID（Required，0~64  characters）
        task_remarks: Async task remark（Optional， max 1024  characters）
        project_id: Project group ID（Optional，0~64  characters）
        availability_zone: Availability zone ID（Optional，0~64  characters）
        scheduler_hints: Scheduling policy (Optional, SchedulerHints object)。 parameter format：{
                affinity: Enable affinity。Optional值：true ( enable), false (disabled)。defaultdisabled,
                affinity_volume: 待亲和的 LUN ID (Optional, 0~64 characters),
             }
        mapping: Mapping info (Optional, ServiceVolumeMapping object, If present, creates for host or host group LUN)。 parameter format：{
                host_id: Host ID (Optional, 0~64 characters, 与hostgroup_idone of),
                hostgroup_id: Host group ID (Optional, 0~64 characters, 与host_idone of),
             }

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/blockservice/v1/volumes"

    payload = {
        'volumes': volumes,
        'service_level_id': service_level_id
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks
    if project_id is not None:
        payload['project_id'] = project_id
    if availability_zone is not None:
        payload['availability_zone'] = availability_zone
    if scheduler_hints is not None:
        payload['scheduler_hints'] = scheduler_hints
    if mapping is not None:
        payload['mapping'] = mapping

    response = client.post(url, body=payload)
    return response


def lun_change_tier(client: DMEAPIClient, volume_ids: list,
                                tier_id: str, attributes_auto_change: bool = None) -> dict:
    """
    batch更新 LUN 的Service level

    Args:
        client: DME API client
        volume_ids: LUN ID  list
        tier_id: Service level ID
        attributes_auto_change: 是否 based onService level parameter刷新 LUN （Optional，true/false）

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }（Async task）
    """
    url = "/rest/blockservice/v1/volumes/update-service-level"

    payload = {
        'volume_ids': volume_ids,
        'service_level_id': tier_id
    }

    if attributes_auto_change is not None:
        payload['attributes_auto_change'] = attributes_auto_change

    response = client.post(url, body=payload)
    return response


def lun_bind_tier(client: DMEAPIClient, volume_id: str,
                       tier_id: str, attributes_auto_change: bool = None) -> dict:
    """
    LUN 关联Service level

    Args:
        client: DME API client
        volume_id: LUN ID
        tier_id: Service level ID
        attributes_auto_change: 是否 based onService level parameter刷新 LUN （Optional，true/false）

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }（Async task）
    """
    url = "/rest/blockservice/v1/volumes/add-to-service-level"

    payload = {
        'volume_ids': [volume_id],
        'service_level_id': tier_id
    }

    if attributes_auto_change is not None:
        payload['attributes_auto_change'] = attributes_auto_change

    response = client.post(url, body=payload)
    return response


def lun_unbind_tier(client: DMEAPIClient, volume_id: str) -> dict:
    """
    解除 LUN 与Service level关联

    Args:
        client: DME API client
        volume_id: LUN ID

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }（Async task）
    """
    url = "/rest/blockservice/v1/volumes/remove-service-level"

    payload = {
        'volume_ids': [volume_id]
    }

    response = client.post(url, body=payload)
    return response


def lun_bind_project(client: DMEAPIClient, volume_id: str,
                        business_group_id: str) -> dict:
    """
    LUN 关联Project group

    Args:
        client: DME API client
        volume_id: LUN ID
        business_group_id: Project group ID

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/blockservice/v1/projects/{business_group_id}/volumes/bound"

    payload = {
        'volume_ids': [volume_id]
    }

    response = client.put(url, body=payload, params={"business_group_id": business_group_id})
    return response


def lun_unbind_project(client: DMEAPIClient, volume_id: str,
                          business_group_id: str) -> dict:
    """
    解除 LUN 与Project group间关联

    Args:
        client: DME API client
        volume_id: LUN ID
        business_group_id: Project group ID

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/blockservice/v1/projects/{business_group_id}/volumes/unbound"

    payload = {
        'volume_ids': [volume_id]
    }

    response = client.put(url, body=payload, params={"business_group_id": business_group_id})
    return response


# ============ tier subtopic functions ============


def tier_list(client: DMEAPIClient, name: str = None,
                        project_id: str = None, available_zone_id: str = None,
                        storage_array_id: str = None, start: int = 0,
                        limit: int = 200, sort_key: str = 'name',
                        sort_dir: str = 'asc', type: str = None) -> dict:
    """
    Batch queryService level

     queryService level list， support按 name、项目 ID、可用区、 storage ID filtering and pagination。

    Args:
        client: DME API client
        name: Service level name（Optional，supports fuzzy search）
        project_id: Project group ID（Optional）
        available_zone_id: 可用区 ID（Optional）
        storage_array_id: Storage device ID（Optional）
        start:  query的Start position，default 0
        limit: per pagecount，10~1000，default 200
        sort_key: Sort field，name/total_capacity/created_at，default name
        sort_dir: Sort direction，asc/desc，default asc
        type: Storage class型，FILE/BLOCK/VIRTUAL_DATASTORE（Optional）

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，includes Service level list
    """
    url = "/rest/service-policy/v1/service-levels"

    query_params = {
        'start': start,
        'limit': limit
    }

    if name is not None:
        query_params['name'] = name

    if project_id is not None:
        query_params['project_id'] = project_id

    if available_zone_id is not None:
        query_params['available_zone_id'] = available_zone_id

    if storage_array_id is not None:
        query_params['storage_array_id'] = storage_array_id

    query_params['sort_key'] = sort_key
    query_params['sort_dir'] = sort_dir

    if type is not None:
        query_params['type'] = type

    response = client.get(url, params=query_params)
    return response


def tier_show_projects(client: DMEAPIClient, tier_id: str = None,
                                page_no: int = 1, page_size: int = 200) -> dict:
    """
    Batch queryProject group与Service levelAssociation

     queryProject group与Service level的Association list， support按Service level ID  filter。

    Args:
        client: DME API client
        tier_id: Service level ID（Optional）
        page_no: Page queryStart page，default 1
        page_size: per pagecount，10~1000，default 200

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，includes Association list
    """
    url = "/rest/service-policy/v1/service-levels/projects/relations"

    query_params = {
        'pageNo': page_no,
        'pageSize': page_size
    }

    if tier_id is not None:
        query_params['serviceLevelId'] = tier_id

    response = client.get(url, params=query_params)
    return response


# ============ project subtopic functions ============


def project_list(client: DMEAPIClient, name: str = None,
                  start: int = 1, limit: int = 20) -> dict:
    """
    Batch queryProject group

     queryProject group list，supports name filtering and pagination。

    Args:
        client: DME API client
        name: Project group name（Optional，supports fuzzy search）
        start: Page number，从 1  start，default 1
        limit: Page size，1~512，default 20

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，includes Project group list
    """
    url = "/rest/projectmgmt/v1/projects"

    query_params = {
        'start': start,
        'limit': limit
    }

    if name is not None:
        query_params['name'] = name

    response = client.get(url, params=query_params)
    return response


def project_show_tiers(client: DMEAPIClient, project_id: str = None,
                                page_no: int = 1, page_size: int = 200) -> dict:
    """
    Batch queryProject group与Service levelAssociation

    QueryProject group的关联Service level list。

    Args:
        client: DME API client
        project_id: Project group ID（Optional）
        page_no: Page queryStart page，default 1
        page_size: per pagecount，10~1000，default 200

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，includes Association list
    """
    url = "/rest/service-policy/v1/service-levels/projects/relations"

    query_params = {
        'pageNo': page_no,
        'pageSize': page_size
    }

    if project_id is not None:
        query_params['projectId'] = project_id

    response = client.get(url, params=query_params)
    return response


# Action list for CLI help
# No direct actions for this topic，All actions are under subtopics
ACTIONS = {
    # tier Subtopic
    'tier_list': {
        'func': tier_list,
        'description': 'Batch queryService level',
        'params': ['name', 'project_id', 'available_zone_id', 'storage_array_id', 'start', 'limit', 'sort_key', 'sort_dir', 'type'],
        'subtopic': 'tier'
    },
    'tier_show_projects': {
        'func': tier_show_projects,
        'description': 'Batch queryProject group与Service levelAssociation',
        'params': ['tier_id', 'page_no', 'page_size'],
        'subtopic': 'tier'
    },
    # project Subtopic
    'project_list': {
        'func': project_list,
        'description': 'Batch queryProject group',
        'params': ['name', 'start', 'limit'],
        'subtopic': 'project'
    },
    'project_show_tiers': {
        'func': project_show_tiers,
        'description': 'Batch queryProject group与Service levelAssociation',
        'params': ['project_id', 'page_no', 'page_size'],
        'subtopic': 'project'
    },
    # lun Subtopic
    'lun_create': {
        'func': lun_create,
        'description': 'ServiceBatch create LUN',
        'params': ['volumes', 'service_level_id', 'task_remarks', 'project_id', 'availability_zone', 'scheduler_hints', 'mapping'],
        'subtopic': 'lun'
    },
    'lun_change_tier': {
        'func': lun_change_tier,
        'description': 'batch更新 LUN 的Service level',
        'params': ['volume_ids', 'tier_id'],
        'subtopic': 'lun'
    },
    'lun_bind_tier': {
        'func': lun_bind_tier,
        'description': 'LUN 关联Service level',
        'params': ['volume_id', 'tier_id'],
        'subtopic': 'lun'
    },
    'lun_unbind_tier': {
        'func': lun_unbind_tier,
        'description': '解除 LUN 与Service level关联',
        'params': ['volume_id'],
        'subtopic': 'lun'
    },
    'lun_bind_project': {
        'func': lun_bind_project,
        'description': 'LUN 关联Project group',
        'params': ['volume_id', 'business_group_id'],
        'subtopic': 'lun'
    },
    'lun_unbind_project': {
        'func': lun_unbind_project,
        'description': '解除 LUN 与Project group间关联',
        'params': ['volume_id', 'business_group_id'],
        'subtopic': 'lun'
    },
}
