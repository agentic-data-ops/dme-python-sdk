"""
Backup management operations
"""

from pydme.client import DMEAPIClient


# ==================== Backup cluster management ====================

def cluster_list(client: DMEAPIClient,
                  page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query backup cluster list
    
    Args:
        client: DME API client
        page_no: pagination start page, 1~10000, default 1
        page_size: items per page, 1~200, default 20
    
    Returns:
        {
            total: total clusters (integer),
            datas: backup cluster list. parameter format: [{
                cluster_id: backup cluster ID (string),
                cluster_name: backup cluster name (string),
                cluster_ip: IP address (string),
            }, ...],
        }
    """
    url = "/rest/dmebackupsoftmgmtservice/v1/clusters/query"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload)
    return response


def cluster_capacity(client: DMEAPIClient, cluster_id: str) -> dict:
    """
    Query backup cluster capacity
    
    Query specified backup cluster capacity info.
    
    Args:
        client: DME API client
        cluster_id: backup cluster ID (Required, 1~64 characters)
    
    Returns:
        {
            cluster_ip: cluster IP (string),
            total_capacity: total capacity (double, GB),
            used_capacity: used capacity (double, GB),
        }
    """
    url = "/rest/dmebackupsoftmgmtservice/v1/clusters/{cluster_id}/capacity"
    
    response = client.get(url, params={"cluster_id": cluster_id})
    return response


def cluster_quota(client: DMEAPIClient, cluster_id: str,
                        page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query backup cluster tenant quota list
    
    Query the tenant quota list under a specified backup cluster.
    
    Args:
        client: DME API client
        cluster_id: backup cluster ID (Required, 1~64 characters)
        page_no: pagination start page, 1~10000, default 1
        page_size: items per page, 1~200, default 20
    
    Returns:
        {
            total: total tenants (integer),
            quotas: tenant quota detail list. parameter format: [{
                tenant_raw_id: tenant ID on device (string),
                tenant_name: tenant name (string),
                tenant_total_capacity: total backup quota capacity (double, GB),
                tenant_used_capacity: used backup quota capacity (double, GB),
            }, ...],
        }
    """
    url = "/rest/dmebackupsoftmgmtservice/v1/clusters/{cluster_id}/tenant-quotas/query"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload, params={"cluster_id": cluster_id})
    return response


# action list, for CLI help
ACTIONS = {
    # subtopic action - cluster (three-level structure: backup cluster list/capacity/quota)
    'cluster_list': {
        'func': cluster_list,
        'description': 'Query backup cluster list',
        'params': ['page_no', 'page_size'],
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
        'description': 'Query backup cluster tenant quota list',
        'params': ['cluster_id', 'page_no', 'page_size'],
        'subtopic': 'cluster'
    },
}
