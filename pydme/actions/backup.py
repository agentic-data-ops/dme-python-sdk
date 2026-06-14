"""
数据备份管理 (Backup) 相关操作
"""

import sys
import os

from pydme.client import DMEAPIClient


# ==================== 备份集群管理 ====================

def cluster_list(client: DMEAPIClient, name: str = None,
                  page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询备份集群列表
    
    Args:
        client: DME API client
        name: 备份集群名称（Optional，supports fuzzy search）
        page_no: 分页查询的起始页码，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        {
            total: 集群总数 (integer),
            clusters: 备份集群列表。参数格式如下：[{
                id: 集群ID (string),
                name: 集群名称 (string),
                status: 状态 (string),
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
    查询备份集群容量
    
    查询指定备份集群的容量信息。
    
    Args:
        client: DME API client
        cluster_id: 备份集群 ID（Required）
    
    Returns:
        {
            total_capacity: 总容量 (integer),
            used_capacity: 已用容量 (integer),
            free_capacity: 空闲容量 (integer),
        }
    """
    url = "/rest/dmebackupsoftmgmtservice/v1/clusters/{cluster_id}/capacity"
    
    response = client.get(url, params={"cluster_id": cluster_id})
    return response


def cluster_quota(client: DMEAPIClient, cluster_id: str,
                        quota_type: str = None,
                        page_no: int = 1, page_size: int = 20) -> dict:
    """
    查询备份集群租户配额列表
    
    查询指定备份集群下的租户配额列表。
    
    Args:
        client: DME API client
        cluster_id: 备份集群 ID（Required）
        quota_type: 配额类型（Optional）
        page_no: 分页查询的起始页码，默认 1
        page_size: 每页数量，1~1000，默认 20
    
    Returns:
        {
            total: 配额总数 (integer),
            quotas: 租户配额列表。参数格式如下：[{
                tenant_id: 租户ID (string),
                quota: 配额大小 (integer),
                used: 已用配额 (integer),
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


# 动作列表，用于 CLI 帮助
ACTIONS = {
    # 子主题动作 - cluster（三级结构：backup cluster list/capacity/quota）
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
