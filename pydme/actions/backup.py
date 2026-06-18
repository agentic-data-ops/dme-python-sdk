"""
数据备份管理 (Backup) 相关操作
"""

from pydme.client import DMEAPIClient


# ==================== 备份集群管理 ====================

def cluster_list(client: DMEAPIClient,
                  page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询备份集群列表
    
    Args:
        client: DME API 客户端
        page_no: 分页查询的起始页码，1~10000，默认 1
        page_size: 每页数量，1~200，默认 20
    
    Returns:
        {
            total: 集群总数 (integer),
            datas: 备份集群列表。参数格式如下：[{
                cluster_id: 备份集群ID (string),
                cluster_name: 备份集群名称 (string),
                cluster_ip: IP地址 (string),
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
    查询备份集群容量
    
    查询指定备份集群的容量信息。
    
    Args:
        client: DME API 客户端
        cluster_id: 备份集群 ID（必选，1~64个字符）
    
    Returns:
        {
            cluster_ip: 集群IP (string),
            total_capacity: 总容量 (double, GB),
            used_capacity: 已用容量 (double, GB),
        }
    """
    url = "/rest/dmebackupsoftmgmtservice/v1/clusters/{cluster_id}/capacity"
    
    response = client.get(url, params={"cluster_id": cluster_id})
    return response


def cluster_quota(client: DMEAPIClient, cluster_id: str,
                        page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询备份集群租户配额列表
    
    查询指定备份集群下的租户配额列表。
    
    Args:
        client: DME API 客户端
        cluster_id: 备份集群 ID（必选，1~64个字符）
        page_no: 分页查询的起始页码，1~10000，默认 1
        page_size: 每页数量，1~200，默认 20
    
    Returns:
        {
            total: 租户总数 (integer),
            quotas: 租户配额详情列表。参数格式如下：[{
                tenant_raw_id: 租户在设备上的ID (string),
                tenant_name: 租户名称 (string),
                tenant_total_capacity: 租户总备份配额容量 (double, GB),
                tenant_used_capacity: 租户已使用备份配额容量 (double, GB),
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
