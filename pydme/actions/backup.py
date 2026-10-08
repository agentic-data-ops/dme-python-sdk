"""
数据备份管理 (Backup) 相关操作
"""

from pydme.client import DMEAPIClient


# ==================== 备份集群管理 ====================

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


# 动作列表，用于 CLI 帮助
ACTIONS = {
    # 子主题动作 - cluster（三级结构：backup cluster list/capacity/quota）
    'cluster_list': {
        'func': cluster_list,
        'description': '查询备份集群列表',
        'params': ['page_no', 'page_size'],
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
        'params': ['cluster_id', 'page_no', 'page_size'],
        'subtopic': 'cluster'
    },
}
