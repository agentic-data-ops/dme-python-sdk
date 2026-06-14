"""
租户自助服务 (Self Service) operations

租户自助服务用于管理Service level和Project group。
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
        volumes: 待创建 LUN 基本参数列表 (List<ServiceVolumeBasicParams>, max array members: 1000)。参数格式如下：[{
                name: LUN名称 (1~255个字符, supports alphanumeric._-and Chinese characters),
                capacity: 容量GB (1~262144),
                count: 创建count (1~500),
                description: 描述 (0~255个字符),
                start_suffix: Starting suffix number (0~9999),
                suffix_length: 后缀长度规则 (1~4, 名称长度+后缀长度<=255),
             }, ...]
        service_level_id: Service level ID（Required，0~64 个字符）
        task_remarks: Async task remark（Optional，最多 1024 个字符）
        project_id: Project group ID（Optional，0~64 个字符）
        availability_zone: Availability zone ID（Optional，0~64 个字符）
        scheduler_hints: Scheduling policy (Optional, SchedulerHints object)。参数格式如下：{
                affinity: 是否开启亲和性。Optional值：true (开启), false (disabled)。默认disabled,
                affinity_volume: 待亲和的 LUN ID (Optional, 0~64个字符),
             }
        mapping: Mapping info (Optional, ServiceVolumeMapping object, 存在即表示为主机或主机组创建 LUN)。参数格式如下：{
                host_id: Host ID (Optional, 0~64个字符, 与hostgroup_idone of),
                hostgroup_id: Host group ID (Optional, 0~64个字符, 与host_idone of),
             }

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
    批量更新 LUN 的Service level

    Args:
        client: DME API client
        volume_ids: LUN ID 列表
        tier_id: Service level ID
        attributes_auto_change: 是否根据Service level参数刷新 LUN 属性（Optional，true/false）

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
        attributes_auto_change: 是否根据Service level参数刷新 LUN 属性（Optional，true/false）

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
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
            task_id: Task ID (string, 1~64个字符),
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
            task_id: Task ID (string, 1~64个字符),
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
            task_id: Task ID (string, 1~64个字符),
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

    查询Service level列表，支持按名称、项目 ID、可用区、存储 ID 等过滤和分页。

    Args:
        client: DME API client
        name: Service level name（Optional，supports fuzzy search）
        project_id: Project group ID（Optional）
        available_zone_id: 可用区 ID（Optional）
        storage_array_id: Storage device ID（Optional）
        start: 查询的Start position，默认 0
        limit: 每页count，10~1000，默认 200
        sort_key: Sort field，name/total_capacity/created_at，默认 name
        sort_dir: Sort direction，asc/desc，默认 asc
        type: Storage class型，FILE/BLOCK/VIRTUAL_DATASTORE（Optional）

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }，包含Service level列表
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

    查询Project group与Service level的Association列表，支持按Service level ID 过滤。

    Args:
        client: DME API client
        tier_id: Service level ID（Optional）
        page_no: Page queryStart page，默认 1
        page_size: 每页count，10~1000，默认 200

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }，包含Association列表
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

    查询Project group列表，supports name filtering and pagination。

    Args:
        client: DME API client
        name: Project group名称（Optional，supports fuzzy search）
        start: 分页的页号，从 1 开始，默认 1
        limit: 分页的大小，1~512，默认 20

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }，包含Project group列表
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

    QueryProject group的关联Service level列表。

    Args:
        client: DME API client
        project_id: Project group ID（Optional）
        page_no: Page queryStart page，默认 1
        page_size: 每页count，10~1000，默认 200

    Returns:
        {
            task_id: Task ID (string, 1~64个字符),
        }，包含Association列表
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
# 本主题无直接动作，所有动作均在子主题下
ACTIONS = {
    # tier 子主题
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
    # project 子主题
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
    # lun 子主题
    'lun_create': {
        'func': lun_create,
        'description': 'ServiceBatch create LUN',
        'params': ['volumes', 'service_level_id', 'task_remarks', 'project_id', 'availability_zone', 'scheduler_hints', 'mapping'],
        'subtopic': 'lun'
    },
    'lun_change_tier': {
        'func': lun_change_tier,
        'description': '批量更新 LUN 的Service level',
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
