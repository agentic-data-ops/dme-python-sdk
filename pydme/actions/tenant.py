"""
Tenant Self Service related operations

Tenant self service is used to manage service levels and business groups.
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
    Service-oriented batch create LUN

    Args:
        client: DME API client
        volumes: List of basic parameters for LUNs to create (List<ServiceVolumeBasicParams>, max array members: 1000). parameter format: [{
                name: LUN name (1~255 characters, supports letters, digits, ._- and Chinese characters),
                capacity: capacityGB (1~262144),
                count: createcount (1~500),
                description: description (0~255 characters),
                start_suffix: start suffix number (0~9999),
                suffix_length: suffix length rule (1~4, name length+suffix length<=255),
             }, ...]
        service_level_id: Service level ID (required, 0~64 characters)
        task_remarks: Async task remark info (optional, at most 1024 characters)
        project_id: Business group ID (optional, 0~64 characters)
        availability_zone: Availability zone ID (optional, 0~64 characters)
        scheduler_hints: Scheduler hints (optional, SchedulerHints object). parameter format: {
                affinity: whether to enable affinity. valid values: true (true), false (not true). default not true,
                affinity_volume: LUN ID to affinity with (optional, 0~64 characters),
             }
        mapping: Mapping info (optional, ServiceVolumeMapping object, presence indicates creating LUN for host or host group). parameter format: {
                host_id: host ID (optional, 0~64 characters, mutually exclusive with hostgroup_id),
                hostgroup_id: host group ID (optional, 0~64 characters, mutually exclusive with host_id),
             }

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
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
                                tier_id: str, attributes_auto_change: bool = None,
                                task_remarks: str = None) -> dict:
    """
    Batch update LUN service level

    This operation updates LUN capabilities and attributes based on service level attributes. Supported updates include: QoS policy, I/O priority, SmartTier policy.

    Args:
        client: DME API client
        volume_ids: LUN list (List<string>, max array members: 1000)
        tier_id: service level ID (string, 1~64 characters)
        attributes_auto_change: whether to refresh LUN attributes based on service level parameters (boolean). valid values: true (auto update), false (no auto update)
        task_remarks: async task remarks (string, max 1024 characters)

    Returns:
        Request submitted successfully, async operation started:
        {
            task_id: task ID (string, 0~64 characters),
        }
    """
    url = "/rest/blockservice/v1/volumes/update-service-level"

    payload = {
        'volume_ids': volume_ids,
        'service_level_id': tier_id
    }

    if attributes_auto_change is not None:
        payload['attributes_auto_change'] = attributes_auto_change

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def lun_bind_tier(client: DMEAPIClient, volume_id: str,
                       tier_id: str, attributes_auto_change: bool = None) -> dict:
    """
    LUN associate service level

    Args:
        client: DME API client
        volume_id: LUN ID
        tier_id: Service level ID
        attributes_auto_change: Whether to refresh LUN attributes based on service level parameters (optional, true/false)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        } (async task)
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
    Remove LUN from service level association

    Args:
        client: DME API client
        volume_id: LUN ID

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        } (async task)
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
    LUN associate business group

    Associate a LUN to a specified business group.

    Args:
        client: DME API client
        volume_id: LUN ID (string, 1~64 characters)
        business_group_id: business group ID (string, 1~64 characters)

    Returns:
        No return data. HTTP 200 indicates association succeeded.
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
    Remove LUN from business group association

    Remove the association between a LUN and a business group.

    Args:
        client: DME API client
        volume_id: LUN ID (string, 1~64 characters)
        business_group_id: business group ID (string, 1~64 characters)

    Returns:
        No return data. HTTP 200 indicates unbind succeeded.
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
    Batch query service levels

    Query service level list, supports filtering by name, project ID, availability zone, storage ID, etc. and pagination.

    Args:
        client: DME API client
        name: Service level name (optional, supports fuzzy query)
        project_id: Business group ID (Optional)
        available_zone_id: Availability zone ID (Optional)
        storage_array_id: Storage device ID (Optional)
        start: Query start position, default 0
        limit: items per page, 10~1000, default 200
        sort_key: Sort field, name/total_capacity/created_at, default name
        sort_dir: Sort direction, asc/desc, default asc
        type: Storage type, FILE/BLOCK/VIRTUAL_DATASTORE (Optional)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, including service level list
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
    Batch query business group and service level associations

    Query the list of associations between business groups and service levels, supports filtering by service level ID.

    Args:
        client: DME API client
        tier_id: Service level ID (Optional)
        page_no: Pagination start page, default 1
        page_size: items per page, 10~1000, default 200

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, including association list
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
    Batch query business groups

    Query business group list, supports filtering by name and pagination.

    Args:
        client: DME API client
        name: Business group name (optional, supports fuzzy query)
        start: Page number, starting from 1, default 1
        limit: Page size, 1~512, default 20

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, including business group list
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
    Batch query business group and service level associations

    Query the list of associated service levels for a specified business group.

    Args:
        client: DME API client
        project_id: Business group ID (Optional)
        page_no: Pagination start page, default 1
        page_size: items per page, 10~1000, default 200

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, including association list
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


# action list, for CLI help
# This topic has no direct actions; all actions are under subtopics
ACTIONS = {
    # tier subtopic
    'tier_list': {
        'func': tier_list,
        'description': 'Batch query service levels',
        'params': ['name', 'project_id', 'available_zone_id', 'storage_array_id', 'start', 'limit', 'sort_key', 'sort_dir', 'type'],
        'subtopic': 'tier'
    },
    'tier_show_projects': {
        'func': tier_show_projects,
        'description': 'Batch query business group and service level associations',
        'params': ['tier_id', 'page_no', 'page_size'],
        'subtopic': 'tier'
    },
    # project subtopic
    'project_list': {
        'func': project_list,
        'description': 'Batch query business groups',
        'params': ['name', 'start', 'limit'],
        'subtopic': 'project'
    },
    'project_show_tiers': {
        'func': project_show_tiers,
        'description': 'Batch query business group and service level associations',
        'params': ['project_id', 'page_no', 'page_size'],
        'subtopic': 'project'
    },
    # lun subtopic
    'lun_create': {
        'func': lun_create,
        'description': 'Service-oriented batch create LUN',
        'params': ['volumes', 'service_level_id', 'task_remarks', 'project_id', 'availability_zone', 'scheduler_hints', 'mapping'],
        'subtopic': 'lun'
    },
    'lun_change_tier': {
        'func': lun_change_tier,
        'description': 'Batch update LUN service level',
        'params': ['volume_ids', 'tier_id'],
        'subtopic': 'lun'
    },
    'lun_bind_tier': {
        'func': lun_bind_tier,
        'description': 'LUN associate service level',
        'params': ['volume_id', 'tier_id'],
        'subtopic': 'lun'
    },
    'lun_unbind_tier': {
        'func': lun_unbind_tier,
        'description': 'Remove LUN from service level association',
        'params': ['volume_id'],
        'subtopic': 'lun'
    },
    'lun_bind_project': {
        'func': lun_bind_project,
        'description': 'LUN associate business group',
        'params': ['volume_id', 'business_group_id'],
        'subtopic': 'lun'
    },
    'lun_unbind_project': {
        'func': lun_unbind_project,
        'description': 'Remove LUN from business group association',
        'params': ['volume_id', 'business_group_id'],
        'subtopic': 'lun'
    },
}
