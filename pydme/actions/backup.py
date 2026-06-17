"""
Backup management operations
"""

import sys
import os

from pydme.client import DMEAPIClient


# ==================== Backup cluster management ====================

def cluster_list(client: DMEAPIClient, name: str = None,
                  page_no: int = 1, page_size: int = 20) -> dict:
    """
    querybackup clusterlist
    
    Args:
        client: DME API client
        name: backup cluster name (可选, supports fuzzy query)
        page_no: pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            total: total clusters (integer),
            clusters: backup clusterlist. parameter format: [{
                id: clusterID (string),
                name: cluster name (string),
                status: status (string),
            }, ...],
        }
    """
    url = "/rest/dmebackupsoftmgmtservice/v1/clusters/query"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if name is not None:
        payload['name'] = name
    
    response = client.post(url, body=payload)
    return response


def cluster_capacity(client: DMEAPIClient, cluster_id: str) -> dict:
    """
    Query backup cluster capacity
    
    Query specified backup cluster capacity info. 
    
    Args:
        client: DME API client
        cluster_id: backup cluster ID(Required)
    
    Returns:
        {
            total_capacity: total capacity (integer),
            used_capacity: used capacity (integer),
            free_capacity: free capacity (integer),
        }
    """
    url = "/rest/dmebackupsoftmgmtservice/v1/clusters/{cluster_id}/capacity"
    
    response = client.get(url, params={"cluster_id": cluster_id})
    return response


def cluster_quota(client: DMEAPIClient, cluster_id: str,
                        quota_type: str = None,
                        page_no: int = 1, page_size: int = 20) -> dict:
    """
    querybackup clustertenant quotalist
    
    query指定backup cluster下的tenant quotalist. 
    
    Args:
        client: DME API client
        cluster_id: backup cluster ID(Required)
        quota_type: quota type(Optional)
        page_no: pagination start page, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            total: total quotas (integer),
            quotas: tenant quotalist. parameter format: [{
                tenant_id: tenant ID (string),
                quota: quota size (integer),
                used: used quota (integer),
            }, ...],
        }
    """
    url = "/rest/dmebackupsoftmgmtservice/v1/clusters/{cluster_id}/tenant-quotas/query"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if quota_type is not None:
        payload['quota_type'] = quota_type
    
    response = client.post(url, body=payload, params={"cluster_id": cluster_id})
    return response


# action list, for CLI help
ACTIONS = {
    # subtopic action - cluster (three-level structure: backup cluster list/capacity/quota)
    'cluster_list': {
        'func': cluster_list,
        'description': '查询备份集群列表',
        'params': ['name', 'page_no', 'page_size'],
        'subtopic': 'cluster'
    },
    'cluster_capacity': {
        'func': cluster_capacity,
        'description': '查询备份集群容量',
        'params': ['cluster_id'],
        'subtopic': 'cluster'
    },
    'cluster_quota': {
        'func': cluster_quota,
        'description': '查询备份集群租户配额列表',
        'params': ['cluster_id', 'quota_type', 'page_no', 'page_size'],
        'subtopic': 'cluster'
    },
}
