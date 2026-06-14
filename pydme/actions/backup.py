"""
Backup management (Backup) operations
"""

import sys
import os

from pydme.client import DMEAPIClient


# ==================== Backup cluster management ====================

def cluster_list(client: DMEAPIClient, name: str = None,
                  page_no: int = 1, page_size: int = 20) -> dict:
    """
     queryBackup cluster list
    
    Args:
        client: DME API client
        name: Backup cluster name (Optional, supports fuzzy search) 
        page_no: Page queryStart page, default 1
        page_size: per pagecount, 1~1000, default 20
    
    Returns:
        {
            total:  clusterTotal count (integer),
            clusters: Backup cluster list. 参数格式如下：[{
                id:  clusterID (string),
                name: Cluster name (string),
                status:  status (string),
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
    
    QueryBackup cluster capacity info. 
    
    Args:
        client: DME API client
        cluster_id:  backup cluster ID (Required) 
    
    Returns:
        {
            total_capacity: Total capacity (integer),
            used_capacity: Used capacity (integer),
            free_capacity: Free capacity (integer),
        }
    """
    url = "/rest/dmebackupsoftmgmtservice/v1/clusters/{cluster_id}/capacity"
    
    response = client.get(url, params={"cluster_id": cluster_id})
    return response


def cluster_quota(client: DMEAPIClient, cluster_id: str,
                        quota_type: str = None,
                        page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query backup clusterTenant quota list
    
    QueryBackup clusterTenant quota list. 
    
    Args:
        client: DME API client
        cluster_id:  backup cluster ID (Required) 
        quota_type:  quota type (Optional) 
        page_no: Page queryStart page, default 1
        page_size: per pagecount, 1~1000, default 20
    
    Returns:
        {
            total:  quotaTotal count (integer),
            quotas: Tenant quota list. 参数格式如下：[{
                tenant_id: Tenant ID (string),
                quota:  quota size (integer),
                used: Used quota (integer),
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


# Action list for CLI help
ACTIONS = {
    # subtopic actions - cluster (Three-level structure: backup cluster list/capacity/quota) 
    'cluster_list': {
        'func': cluster_list,
        'description': ' queryBackup cluster list',
        'params': ['name', 'page_no', 'page_size'],
        'subtopic': 'cluster'
    },
    'cluster_capacity': {
        'func': cluster_capacity,
        'description': 'Query backup cluster capacity',
        'params': ['cluster_id'],
        'subtopic': 'cluster'
    },
    'cluster_quota': {
        'func': cluster_quota,
        'description': 'Query backup clusterTenant quota list',
        'params': ['cluster_id', 'quota_type', 'page_no', 'page_size'],
        'subtopic': 'cluster'
    },
}
