"""
Data backup management (Backup) related operations
"""

from pydme.client import DMEAPIClient


# ==================== Backup cluster management ====================

def cluster_list(client: DMEAPIClient,
                  page_no: int = 1, page_size: int = 20) -> dict:
    url = "/rest/dmebackupsoftmgmtservice/v1/clusters/query"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload)
    return response


def cluster_capacity(client: DMEAPIClient, cluster_id: str) -> dict:
    url = "/rest/dmebackupsoftmgmtservice/v1/clusters/{cluster_id}/capacity"
    
    response = client.get(url, params={"cluster_id": cluster_id})
    return response


def cluster_quota(client: DMEAPIClient, cluster_id: str,
                        page_no: int = 1, page_size: int = 20) -> dict:
    url = "/rest/dmebackupsoftmgmtservice/v1/clusters/{cluster_id}/tenant-quotas/query"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload, params={"cluster_id": cluster_id})
    return response


# Action list for CLI help
ACTIONS = {
    # Subtopic actions - cluster (three-level structure: backup cluster list/capacity/quota)
    'cluster_list': {
        'func': cluster_list,
        'params': ['page_no', 'page_size'],
        'subtopic': 'cluster'
    },
    'cluster_capacity': {
        'func': cluster_capacity,
        'params': ['cluster_id'],
        'subtopic': 'cluster'
    },
    'cluster_quota': {
        'func': cluster_quota,
        'params': ['cluster_id', 'page_no', 'page_size'],
        'subtopic': 'cluster'
    },
}
