"""
NAS 相关操作
"""

import sys
import os

from pydme.client import DMEAPIClient


# ============================================================================
# DPC (DPC) 子主题函数
# ============================================================================


def dpc_list(client: DMEAPIClient, ids: list = None, hostname: str = None, ip: str = None,
             mgmt_status: list = None, status: list = None, sn: str = None,
             storage_id: str = None, dpc_om_id: str = None, dpc_type: list = None,
             client_version: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    """
    批量queryDPClist

    Args:
        client: DME API client
        ids: DPC ID list(Optional), List<string> type, max array members 100, 精确query
        hostname: 计算节点的host name(Optional), 1~256 个字符, 模糊query
        ip: DPC所在计算节点的管理 IP(Optional), 1~256 个字符, 模糊query
        mgmt_status: 管理statuslist(Optional), List<string> type, 精确query; valid values: normal (正常)、abnormal (异常)、unready (未就绪, 客户端配置status异常)、subhealth (亚健康)、pre_registered (预注册)、unknown (未知)
        status: 业务statuslist(Optional), List<string> type, 精确query; valid values: normal (正常)、abnormal (异常)、subhealth (亚健康)、unknown (未知)
        sn: DPC所在计算节点的硬件 SN(Optional), 1~256 个字符, 模糊query
        storage_id: Storage device ID(Optional), 1~256 个字符, 精确query
        dpc_om_id: DPC O&M ID(Optional), 1~256 个字符, 精确query
        dpc_type: DPC typelist(Optional), List<string> type
        client_version: DPCversion号(Optional), 最多 256 个字符, 精确query
        page_no: 分页页码(Optional), 1~10000000, default 1
        page_size: 每页数据条数(Optional), 1~1000, default 20

    Returns:
        {
            total: DPCtotal (integer),
            dpcs: DPClist (List<DpcInfo>). parameter format: [{
                id: DPCID (string),
                hostname: host name (string),
                ip: 管理IP (string),
                status: 业务status (string),
                mgmt_status: 管理status (string),
            }, ...],
        }
    """
    url = "/rest/dpc-mgmt/v1/dpcs/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if ids is not None:
        payload['ids'] = ids
    if hostname is not None:
        payload['hostname'] = hostname
    if ip is not None:
        payload['ip'] = ip
    if mgmt_status is not None:
        payload['mgmt_status'] = mgmt_status
    if status is not None:
        payload['status'] = status
    if sn is not None:
        payload['sn'] = sn
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if dpc_om_id is not None:
        payload['dpc_om_id'] = dpc_om_id
    if dpc_type is not None:
        payload['dpc_type'] = dpc_type
    if client_version is not None:
        payload['client_version'] = client_version

    response = client.post(url, body=payload)
    return response


def dpc_show(client: DMEAPIClient, dpc_id: str) -> dict:
    """
    queryDPCdetails. 

    Args:
        client: DME API client
        dpc_id: DPC ID (必选, string)

    Returns:
        {
            id: DPCID (string),
            hostname: host name (string),
            ip: 管理IP (string),
            status: 业务status (string),
            mgmt_status: 管理status (string),
        }
    """
    url = "/rest/dpc-mgmt/v1/dpcs/{dpc_id}"

    if not dpc_id:
        raise ValueError("dpc_id 是必选参数")

    response = client.get(url, params={"dpc_id": dpc_id})
    return response


def dpc_client_list(client: DMEAPIClient, storage_id: str = None,
                     process_id: str = None, name: str = None,
                     manage_ip: str = None, version: str = None,
                     status: str = None, switch_status: str = None,
                     upgrade_flag: str = None, sort_key: str = None,
                     sort_dir: str = None,
                     page_no: int = 1, page_size: int = 10) -> dict:
    """
    批量queryDPC客户端. 

    Args:
        client: DME API client
        storage_id: 存储ID (可选, string, 1~64个字符)
        process_id: DPC客户端进程ID (可选, string, 1~64个字符)
        name: DPC客户端name, 支持模糊搜索 (可选, string, 1~256个字符)
        manage_ip: DPC客户端节点管理IP, 支持模糊搜索 (可选, string, 1~256个字符)
        version: DPC客户端version, 支持模糊搜索 (可选, string, 1~256个字符)
        status: DPC客户端status (可选, string). valid values: normal (正常), abnormal (异常), disabled (未启用)
        switch_status: 节点FSA开关status (可选, string). valid values: on (true), off (false)
        upgrade_flag: 升级标记 (可选, string). valid values: required (需要升级), not_required (无需升级)
        sort_key: 排序字段 (可选, string). valid values: manage_ip (节点管理IP), dpc_mem (DPC客户端节点内存)
        sort_dir: 排序方向 (可选, string). valid values: asc (升序), desc (降序)
        page_no: 分页页码 (可选, int32, 1~10000000). default值: 1
        page_size: 每页数据条数 (可选, int32, 1~1000). default值: 10

    Returns:
        {
            total: total (integer),
            data: DPC客户端数据 (List<DpcClient>). parameter format: [{
                id: ID (string),
                storage_id: 存储ID (string),
                process_id: DPC客户端进程ID (string),
                name: DPC客户端name (string),
                manage_ip: DPC客户端节点管理IP (string),
                version: DPC客户端version (string),
                status: DPC客户端status (string),
                switch_status: 节点FSA开关status (string),
                upgrade_flag: 升级标记 (string),
                dpc_mem: DPC客户端节点内存 (int64),
            }, ...],
        }
    """
    url = "/rest/fileservice/v1/dpc-clients/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if process_id is not None:
        payload['process_id'] = process_id
    if name is not None:
        payload['name'] = name
    if manage_ip is not None:
        payload['manage_ip'] = manage_ip
    if version is not None:
        payload['version'] = version
    if status is not None:
        payload['status'] = status
    if switch_status is not None:
        payload['switch_status'] = switch_status
    if upgrade_flag is not None:
        payload['upgrade_flag'] = upgrade_flag
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def dpc_client_show(client: DMEAPIClient, id: str) -> dict:
    """
    queryDPC客户端details. 

    Args:
        client: DME API client
        id: queryDPC客户端ID (必选, string, 1~64个字符)

    Returns:
        {
            id: ID (string),
            storage_id: 存储ID (string),
            process_id: DPC客户端进程ID (string),
            name: DPC客户端name (string),
            manage_ip: DPC客户端节点管理IP (string),
            version: DPC客户端version (string),
            status: DPC客户端status (string),
        }
    """
    url = "/rest/fileservice/v1/dpc-clients/{id}"

    if not id:
        raise ValueError("id 是必选参数")

    response = client.get(url, params={"id": id})
    return response


def dtree_list(client: DMEAPIClient, id_in_storage: str = None, name: str = None,
               device_name: str = None, storage_id: str = None, zone_id: str = None,
               manufacturer: str = None, tier_name: str = None, fs_name: str = None,
               fs_id: str = None, namespace_name: str = None, namespace_id: str = None,
               quota_switch: bool = None, security_mode: str = None,
               nas_locking_policy: str = None, sort_key: str = None,
               sort_dir: str = None, page_no: int = 1, page_size: int = 20,
               dc_id: str = None, dc_name: str = None) -> dict:
    """
    query Dtree list

    Args:
        client: DME API client
        id_in_storage: Dtree 在存储侧的 ID(Optional), 1~256 个字符
        name: Dtree name(Optional), 1~256 个字符, 支持模糊搜索
        device_name: dtree 所属storage device name(Optional), 1~256 个字符, 支持模糊搜索
        storage_id: dtree storage设备 ID(Optional), 1~64 个字符, 支持过滤
        zone_id: dtree 所属 zone 的 ID(Optional), 36 个字符; 仅 OceanStor A800/A600 系列存储支持
        manufacturer: dtree storage设备厂商(Optional), valid values: huawei (华为)、third_part (第三方)
        tier_name: 服务等级name (可选, 预留字段), 1~256 个字符, 支持模糊搜索
        fs_name: dtree 所属Filesystemname(Optional), 1~256 个字符, 支持模糊搜索
        fs_id: dtree 所属Filesystem ID(Optional), 1~64 个字符, 与 namespace_id 互斥
        namespace_name: dtree 所属namespace name(Optional), 1~64 个字符
        namespace_id: dtree 所属Namespace ID(Optional), 1~64 个字符, 与 fs_id 互斥
        quota_switch: quota是否启用(Optional), true: true; false: false
        security_mode: 安全模式(Optional), 1~32 个字符; valid values: mixed (mixed 安全模式)、native (native 安全模式)、ntfs (ntfs 安全模式)、unix (unix 安全模式)
        nas_locking_policy: NAS 锁策略(Optional), valid values: mandatory (强制锁)、advisory (建议锁)、unknown (未启用 Native 安全模式)
        sort_key: 排序字段(Optional), valid values: nfs_count、cifs_count、dataturbo_count、name
        sort_dir: 排序方向(Optional), valid values: asc (升序)、desc (降序), default asc
        page_no: 分页query页码(Optional), 最小值 1, default 1
        page_size: 每页显示的count(Optional), 1~1000, default 20
        dc_id: 数据中心 ID(Optional), 1~128 个字符, 正则 ^[_A-Fa-f0-9\\-]+$
        dc_name: 数据中心name(Optional), 1~256 个字符

    Returns:
        {
            total: Dtree total (integer),
            dtrees: Dtree list (List<DtreeInfo>). parameter format: [{
                id: Dtree ID (string),
                name: Dtree name (string),
                path: 路径 (string),
                fs_id: FilesystemID (string),
            }, ...],
        }
    """
    url = "/rest/fileservice/v1/dtrees/query"

    payload = {}

    if id_in_storage is not None:
        payload['id_in_storage'] = id_in_storage
    if name is not None:
        payload['name'] = name
    if device_name is not None:
        payload['device_name'] = device_name
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if manufacturer is not None:
        payload['manufacturer'] = manufacturer
    if tier_name is not None:
        payload['tier_name'] = tier_name
    if fs_name is not None:
        payload['fs_name'] = fs_name
    if fs_id is not None:
        payload['fs_id'] = fs_id
    if namespace_name is not None:
        payload['namespace_name'] = namespace_name
    if namespace_id is not None:
        payload['namespace_id'] = namespace_id
    if quota_switch is not None:
        payload['quota_switch'] = quota_switch
    if security_mode is not None:
        payload['security_mode'] = security_mode
    if nas_locking_policy is not None:
        payload['nas_locking_policy'] = nas_locking_policy
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size
    if dc_id is not None:
        payload['dc_id'] = dc_id
    if dc_name is not None:
        payload['dc_name'] = dc_name

    response = client.post(url, body=payload)
    return response


def dtree_show(client: DMEAPIClient, dtree_id: str) -> dict:
    """
    query指定 Dtree details. 

    Args:
        client: DME API client
        dtree_id: Dtree ID (必选, string)

    Returns:
        {
            id: Dtree ID (string),
            name: Dtree name (string),
            path: 路径 (string),
            fs_id: FilesystemID (string),
        }
    """
    url = "/rest/fileservice/v1/dtrees/{dtree_id}"

    if not dtree_id:
        raise ValueError("dtree_id 是必选参数")

    response = client.get(url, params={"dtree_id": dtree_id})
    return response


def dtree_create(client: DMEAPIClient, storage_id: str, create_dtrees_param: list,
                 fs_id: str = None, namespace_id: str = None, zone_id: str = None,
                 parent_dir: str = None, quota_switch: bool = None,
                 security_mode: str = None, nas_locking_policy: str = None,
                 create_nfs_share_param: dict = None, create_cifs_share_param: dict = None,
                 dataturbo_share: dict = None, create_worm_param: dict = None,
                 unix_permissions: str = None, task_remarks: str = None) -> dict:
    """
    create并共享 Dtree

    create Dtree, 同时将 Dtree 以 NFS、CIFS 或 DataTurbo 共享. 

    Args:
        client: DME API client
        storage_id: dtree storage设备 ID, 1~64个字符
        create_dtrees_param: Dtree name和countinfolist (条件必传). parameter format: [{
                dtree_name: Dtreename (1~255个字符, 正则: ^[^,//:]+$, 支持字母数字空格和部分特殊字符; 若单次请求create多个Dtree, name从0000起累加区分),
                count: 单次createDtreecount (int, 单组上限500个, 各组上限总和为500个),
             }, ...]
        fs_id: dtree 所属Filesystem ID, 与 namespace_id 互斥, 集中式存储时必填
        namespace_id: dtree 所属Namespace ID, 与 fs_id 互斥, 分布式存储时必填
        zone_id: dtree 所属 zone 的 ID, 仅 OceanStor A800/A600 系列存储支持, 长度36个字符
        parent_dir: 目录父级, 分布式存储时有效, 1~4008个字符
        quota_switch: quota开关, true/false, default false
        security_mode: 安全模式, mixed/native/ntfs/unix. 若model支持则必填. v3系列V300R006C60及以上、v5系列V500R007C50及以上、v6系列6.1.2及以上支持
        nas_locking_policy: NAS 锁策略, mandatory/advisory/unknown
        create_nfs_share_param: 关联createNFS共享. create多个Dtree时不支持指定该参数. 格式参见动作帮助: nas nfs_share create
        create_cifs_share_param: 关联createCIFS共享, create多个Dtree时不支持指定该参数. 格式参见动作帮助: nas cifs_share create
        dataturbo_share: 关联createDataTurbo共享 (Optional). parameter format: {
                description: DataTurbo共享description (可选, 0~255个字符),
                charset: 字符集编码 (必选, 固定值UTF_8),
                dpc_share_auth: DataTurbo管理员list (Optional). parameter format: [{
                        dpc_user_id: DataTurbo管理员ID (必选, 0~64个字符),
                        permission: DataTurbo管理员权限 (必选, 固定值read_and_write),
                     }, ...]
             }
        create_worm_param: WORM配置 (Optional). parameter format: {
                worm_mode: 策略模式 (Required). valid values: enterprise_mode (企业级), compliance_mode (法规级),
                min_protected_period: 最小保留时间 (必选, 0~36817920, 0代表无限期),
                min_protected_period_unit: 最小保留时间单位 (Required). valid values: day, year, month, hour, minute. A310或OceanStor Pacific 8.2.1及以上支持month/hour/minute,
                max_protected_period: 最大保留时间 (必选, 0~36817920, 0代表无限期),
                max_protected_period_unit: 最大保留时间单位 (Required). valid values: day, year, month, hour, minute, infinite. A310或OceanStor Pacific 8.2.1及以上支持month/hour/minute,
                def_protected_period: default保留时间 (必选, 0~36817920, 0代表无限期),
                def_protected_period_unit: default保留时间单位 (Required). valid values: day, year, month, hour, minute, infinite. A310或OceanStor Pacific 8.2.1及以上支持month/hour/minute,
                auto_lock_enabled: 自动锁定开关 (可选, defaultfalse; true后若指定时间内文件未modify则自动锁定),
                auto_lock_time: 自动锁定时间 (可选, 1~64800; 单位为day时1~45, hour时1~1080, minute时1~64800),
                auto_lock_unit: 自动锁定时间单位 (Optional). valid values: day, minute, hour,
                legal_hold_modify: legal hold文件modify权限 (可选, defaultfalse),
             }
        unix_permissions: Dtree 目录权限, 正则 [0-7]{3}, 如 755. 
        task_remarks: 异步任务备注info, 0~1024个字符

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fileservice/v1/dtrees"

    if not storage_id or not create_dtrees_param:
        raise ValueError("storage_id 和 create_dtrees_param 是必选参数")

    payload = {
        'storage_id': storage_id,
        'create_dtrees_param': create_dtrees_param
    }

    if fs_id is not None:
        payload['fs_id'] = fs_id
    if namespace_id is not None:
        payload['namespace_id'] = namespace_id
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if parent_dir is not None:
        payload['parent_dir'] = parent_dir
    if quota_switch is not None:
        payload['quota_switch'] = quota_switch
    if security_mode is not None:
        payload['security_mode'] = security_mode
    if nas_locking_policy is not None:
        payload['nas_locking_policy'] = nas_locking_policy
    if create_nfs_share_param is not None:
        payload['create_nfs_share_param'] = create_nfs_share_param
    if create_cifs_share_param is not None:
        payload['create_cifs_share_param'] = create_cifs_share_param
    if dataturbo_share is not None:
        payload['dataturbo_share'] = dataturbo_share
    if create_worm_param is not None:
        payload['create_worm_param'] = create_worm_param
    if unix_permissions is not None:
        payload['unix_permissions'] = unix_permissions
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def dtree_delete(client: DMEAPIClient, dtree_ids: list, task_remarks: str = None) -> dict:
    """
    批量delete Dtree. 

    Args:
        client: DME API client
        dtree_ids: 待delete Dtree ID list (必选, List[string])
        task_remarks: 异步任务备注info (可选, string, 最多1024个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fileservice/v1/dtrees/delete"

    if not dtree_ids or len(dtree_ids) == 0:
        raise ValueError("dtree_ids 是必选参数")

    payload = {
        'dtree_ids': dtree_ids
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def dtree_modify(client: DMEAPIClient, dtree_id: str, name: str = None,
                 quota_switch: bool = None, security_mode: str = None,
                 nas_locking_policy: str = None, unix_permissions: str = None,
                 task_remarks: str = None) -> dict:
    """
    modify指定 Dtree

    Args:
        client: DME API client
        dtree_id: Dtree ID
        name: Dtree name
        quota_switch: quota开关, true/false
        security_mode: 安全模式, mixed/native/ntfs/unix
        nas_locking_policy: NAS 锁策略, mandatory/advisory/unknown
        unix_permissions: Dtree 目录权限, 如 755
        task_remarks: 异步任务备注info

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fileservice/v1/dtrees/{dtree_id}"

    payload = {}

    if name is not None:
        payload['name'] = name
    if quota_switch is not None:
        payload['quota_switch'] = quota_switch
    if security_mode is not None:
        payload['security_mode'] = security_mode

    payload = {}

    if name is not None:
        payload['name'] = name
    if quota_switch is not None:
        payload['quota_switch'] = quota_switch
    if security_mode is not None:
        payload['security_mode'] = security_mode
    if nas_locking_policy is not None:
        payload['nas_locking_policy'] = nas_locking_policy
    if unix_permissions is not None:
        payload['unix_permissions'] = unix_permissions
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.put(url, body=payload, params={"dtree_id": dtree_id})
    return response


# ============================================================================
# NFS 共享子主题相关动作
# ============================================================================

def nfs_share_list(client: DMEAPIClient, id_in_storage: str = None, name: str = None,
                   share_path: str = None, exact_share_path: str = None,
                   device_name: str = None, manufacturer: str = None,
                   storage_id: str = None, tier_name: str = None,
                   owning_dtree_name: str = None, fs_name: str = None,
                   fs_id: str = None, owning_dtree_id: str = None,
                   vstore_name: str = None, page_no: int = 1,
                   page_size: int = 20, sort_key: str = None,
                   sort_dir: str = None, support_provisioning: bool = None,
                   namespace_id: str = None, namespace_name: str = None,
                   dc_id: str = None, dc_name: str = None,
                   zone_id: str = None, zone_name: str = None,
                   zone_ip: str = None, scope: str = None) -> dict:
    """
    query NFS 共享list

    Args:
        client: DME API client
        id_in_storage: NFS 在存储侧的 ID(Optional), 1~256 个字符
        name: 共享name(Optional), 1~256 个字符, 支持模糊搜索
        share_path: 共享路径(Optional), 1~256 个字符, 支持模糊搜索
        exact_share_path: 精确搜索 NFS 共享路径(Optional), 1~1024 个字符; 当 share_path 和 exact_share_path 都有值时优先选择 exact_share_path
        device_name: 所属storage device name(Optional), 1~256 个字符, 支持模糊搜索
        manufacturer: storage设备厂商(Optional), valid values: huawei (华为)、third_part (第三方)
        storage_id: storage设备 ID(Optional), 1~64 个字符, 支持过滤
        tier_name: 服务等级name(Optional), 1~256 个字符, 支持模糊搜索
        owning_dtree_name: 所属 Dtree name(Optional), 1~256 个字符, 支持模糊搜索
        fs_name: Filesystemname(Optional), 1~256 个字符, 支持模糊搜索
        fs_id: Filesystem ID(Optional), 1~64 个字符
        owning_dtree_id: 所属 Dtree Id(Optional), 1~256 个字符, 支持过滤
        vstore_name: NFS 共享所属 vStore name(Optional), 1~256 个字符, supports fuzzy query
        page_no: 分页query页码(Optional), 最小值 1, default 1
        page_size: 每页显示的count(Optional), 1~1000, default 20
        sort_key: 排序字段(Optional), valid values: name、id_in_storage; 指定 id_in_storage 排序时仅支持 ID 为数字的object
        sort_dir: 排序方向(Optional), valid values: asc (升序)、desc (降序), default asc
        support_provisioning: 是否支持业务发放(Optional), true: 是; false: 否; 下发此字段可过滤不支持业务发放设备的资源, 当前不支持业务发放的设备有 OceanStor Pacific 系列
        namespace_id: Namespace ID(Optional), 1~64 个字符, 仅 OceanStor Pacific 系列Storage device支持
        namespace_name: namespace name(Optional), 1~256 个字符, supports fuzzy query, 仅 OceanStor Pacific 系列Storage device支持
        dc_id: 数据中心 ID(Optional), 1~128 个字符, 正则 ^[_A-Fa-f0-9\\-]+$
        dc_name: 数据中心name(Optional), 1~256 个字符
        zone_id: NFS 共享所属 zone ID(Optional), 1~64 个字符
        zone_name: NFS 共享所属 zone name(Optional), 1~256 个字符, 支持模糊搜索
        zone_ip: NFS 共享所属 zone 管理 IP(Optional), 0~255 个字符
        scope: 资源所属范围(Optional), valid values: local_scale (本地)、global_scale (全局)

    Returns:
        {
            total: NFS 共享total (integer),
            nfs_shares: NFS 共享list. parameter format: [{
                id: 共享ID (string),
                name: 共享name (string),
                path: 路径 (string),
                fs_id: FilesystemID (string),
            }, ...],
        }
    """
    url = "/rest/fileservice/v1/nfs-shares/query"

    payload = {}

    if id_in_storage is not None:
        payload['id_in_storage'] = id_in_storage
    if name is not None:
        payload['name'] = name
    if share_path is not None:
        payload['share_path'] = share_path
    if exact_share_path is not None:
        payload['exact_share_path'] = exact_share_path
    if device_name is not None:
        payload['device_name'] = device_name
    if manufacturer is not None:
        payload['manufacturer'] = manufacturer
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if tier_name is not None:
        payload['tier_name'] = tier_name
    if owning_dtree_name is not None:
        payload['owning_dtree_name'] = owning_dtree_name
    if fs_name is not None:
        payload['fs_name'] = fs_name
    if fs_id is not None:
        payload['fs_id'] = fs_id
    if owning_dtree_id is not None:
        payload['owning_dtree_id'] = owning_dtree_id
    if vstore_name is not None:
        payload['vstore_name'] = vstore_name
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if support_provisioning is not None:
        payload['support_provisioning'] = support_provisioning
    if namespace_id is not None:
        payload['namespace_id'] = namespace_id
    if namespace_name is not None:
        payload['namespace_name'] = namespace_name
    if dc_id is not None:
        payload['dc_id'] = dc_id
    if dc_name is not None:
        payload['dc_name'] = dc_name
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if zone_name is not None:
        payload['zone_name'] = zone_name
    if zone_ip is not None:
        payload['zone_ip'] = zone_ip
    if scope is not None:
        payload['scope'] = scope

    response = client.post(url, body=payload)
    return response


def nfs_share_show(client: DMEAPIClient, nfs_share_id: str) -> dict:
    """
    query指定 NFS 共享details

    Args:
        client: DME API client
        nfs_share_id: NFS 共享 ID

    Returns:
        {
            id: 共享ID (string),
            name: 共享name (string),
            path: 路径 (string),
            fs_id: FilesystemID (string),
            export_ip: 导出IP (string),
        }
    """
    url = "/rest/fileservice/v1/nfs-shares/{nfs_share_id}"

    if not nfs_share_id:
        raise ValueError("nfs_share_id 是必选参数")

    response = client.get(url, params={"nfs_share_id": nfs_share_id})
    return response


def nfs_share_create(client: DMEAPIClient, create_nfs_share_param: dict,
                     task_remarks: str = None) -> dict:
    """
    create NFS 共享

    Args:
        client: DME API client
        create_nfs_share_param: create NFS 共享参数. parameter format: {
                name: NFS共享别名 (Optional),
                description: descriptioninfo (Optional),
                share_path: 共享路径 (Required),
                character_encoding: 字符编码 (Optional),
                audit_items: 支持审计的事件list (Optional). parameter format: [{
                        audititem: 审计事件type. valid values: none (无操作), all (所有操作), open (打开), create (create), read (读), write (写), close (false), delete (delete), rename (重命名), get_security (获取安全属性), set_security (设置安全属性), get_attr (获取属性), set_attr (设置属性),
                     }, ...],
                show_snapshot_enable: 是否true显示Snapshot (Optional). valid values: true, false,
                nfs_share_client_addition: NFS共享客户端权限list (Optional). parameter format: [{
                        name: 客户端IP或主机名或网络组名 (必选, 1~255字符; 网络组name以@开头),
                        permission: 权限 (Required). valid values: read (读), read_and_write (读写), no_permission (无权限), read_and_write_not_del_rename (读写不能delete重命名),
                        accesskrb5: krb5权限 (Optional). valid values: read, read_and_write, no_permission, read_and_write_not_del_rename,
                        accesskrb5i: krb5i权限 (Optional). valid values: read, read_and_write, no_permission, read_and_write_not_del_rename,
                        accesskrb5p: krb5p权限 (Optional). valid values: read, read_and_write, no_permission, read_and_write_not_del_rename,
                        write_mode: 写入模式 (Optional). valid values: synchronization (同步), asynchronization (异步),
                        permission_constraint: 权限限制 (Required). valid values: all_squash, no_all_squash,
                        root_permission_constraint: root权限限制 (Required). valid values: root_squash, no_root_squash,
                        source_port_verification: 源端口校验限制 (Optional). valid values: secure (安全), insecure (不安全),
                        anonymous_user_id: 匿名user ID (Optional),
                        access_protocol: 访问协议 (Optional). valid values: nfsv3_and_nfsv4 (NFSv3和NFSv4), nfsv3 (仅NFSv3), nfsv4 (仅NFSv4),
                     }, ...],
                file_name_extension_filters: 文件扩展名过滤规则list (Optional). parameter format: [{
                        file_name_ex_id_in_storage: 规则在存储上的ID (可选, 1~64字符, 变更已添加规则时必填),
                        file_name_extension: 文件扩展名 (必选, 1~127字符, 支持通配符?和*, *只能位于最后一个字符),
                        rule_type: 规则允许/拒绝 (可选, defaultreject). valid values: reject, permit,
                        fileoperations: 操作typelist (Optional). valid values: close, create, create_dir, delete, delete_dir, getattr, link, lookup, open, read, write, rename, rename_dir, setattr, symlink,
                     }, ...],
                fs_id: Filesystem的id (与namespace_id互斥),
                namespace_id: Namespace的id (与fs_id互斥),
             }
        task_remarks: 异步任务备注info

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fileservice/v2/nfs-shares"

    payload = {
        'create_nfs_share_param': create_nfs_share_param
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def nfs_share_modify(client: DMEAPIClient, nfs_share_id: str,
                     description: str = None, character_encoding: str = None,
                     audit_items: list = None, show_snapshot_enable: bool = None,
                     nfs_share_client_addition: list = None,
                     nfs_share_client_modification: list = None,
                     nfs_share_client_deletion: list = None,
                     file_name_ex_filters: list = None,
                     task_remarks: str = None) -> dict:
    """
    modify指定 NFS 共享

    Args:
        client: DME API client
        nfs_share_id: NFS 共享 ID
        description: descriptioninfo
        character_encoding: 字符编码, valid values: utf-8, zh, gbk 等
        audit_items: 审计事件list (Optional). parameter format: [{
                audititem: 审计事件type. valid values: none (无操作), all (所有操作), open (打开), create (create), read (读), write (写), close (false), delete (delete), rename (重命名), get_security (获取安全属性), set_security (设置安全属性), get_attr (获取属性), set_attr (设置属性),
             }, ...]
        show_snapshot_enable: 是否显示快照
        nfs_share_client_addition: 需要新增的 NFS 共享客户端list (Optional). parameter format: [{
                name: 客户端IP或主机名或网络组名 (必选, 1~255字符),
                permission: 权限 (Required). valid values: read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5: krb5权限 (Optional). valid values: read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5i: krb5i权限 (Optional). valid values: read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5p: krb5p权限 (Optional). valid values: read, read_and_write, no_permission, read_and_write_not_del_rename,
                write_mode: 写入模式 (Optional). valid values: synchronization (同步), asynchronization (异步),
                permission_constraint: 权限限制 (Required). valid values: all_squash, no_all_squash,
                root_permission_constraint: root权限限制 (Required). valid values: root_squash, no_root_squash,
                source_port_verification: 源端口校验限制 (Optional). valid values: secure (安全), insecure (不安全),
                anonymous_user_id: 匿名user ID (可选, 0~4294967294),
             }, ...]
        nfs_share_client_modification: 需要modify的 NFS 共享客户端list (Optional). parameter format: [{
                nfs_share_client_id_in_storage: 客户端在存储上的ID (必选, 1~32字符),
                permission: 权限 (Required). valid values: read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5: krb5权限 (Optional). valid values: read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5i: krb5i权限 (Optional). valid values: read, read_and_write, no_permission, read_and_write_not_del_rename,
                accesskrb5p: krb5p权限 (Optional). valid values: read, read_and_write, no_permission, read_and_write_not_del_rename,
                write_mode: 写入模式 (Optional). valid values: synchronization (同步), asynchronization (异步),
                permission_constraint: 权限限制 (Required). valid values: all_squash, no_all_squash,
                root_permission_constraint: root权限限制 (Required). valid values: root_squash, no_root_squash,
                source_port_verification: 源端口校验限制 (Optional). valid values: secure (安全), insecure (不安全),
                anonymous_user_id: 匿名user ID (可选, 0~4294967294),
             }, ...]
        nfs_share_client_deletion: 需要delete的 NFS 共享客户端list (Optional). parameter format: [{
                nfs_share_client_id_in_storage: 客户端在存储上的ID (必选, 1~32字符),
                name: 客户端IP或主机名或网络组名 (可选, 1~32000字符),
             }, ...]
        file_name_ex_filters: 扩展名过滤规则list (Optional). parameter format: [{
                update_type: 变更type (可选, defaultadd). valid values: add (新增), delete (delete), modify (modify),
                param: 扩展名过滤规则. attribute format: {
                        file_name_ex_id_in_storage: 规则在存储上的ID (可选, 1~64字符, modify时必填),
                        file_name_extension: 文件扩展名 (必选, 1~127字符, 支持通配符?和*, *只能位于最后),
                        rule_type: 规则允许/拒绝 (可选, defaultreject). valid values: reject (拒绝), permit (允许),
                        fileoperations: 操作typelist (Optional). valid values: close, create, create_dir, delete, delete_dir, getattr, link, lookup, open, read, write, rename, rename_dir, setattr, symlink,
                }
             }, ...]
        task_remarks: 异步任务备注info

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fileservice/v2/nfs-shares/{nfs_share_id}"

    payload = {}

    if description is not None:
        payload['description'] = description
    if character_encoding is not None:
        payload['character_encoding'] = character_encoding
    if audit_items is not None:
        payload['audit_items'] = audit_items

    payload = {}

    if description is not None:
        payload['description'] = description
    if character_encoding is not None:
        payload['character_encoding'] = character_encoding
    if audit_items is not None:
        payload['audit_items'] = audit_items
    if show_snapshot_enable is not None:
        payload['show_snapshot_enable'] = show_snapshot_enable
    if nfs_share_client_addition is not None:
        payload['nfs_share_client_addition'] = nfs_share_client_addition
    if nfs_share_client_modification is not None:
        payload['nfs_share_client_modification'] = nfs_share_client_modification
    if nfs_share_client_deletion is not None:
        payload['nfs_share_client_deletion'] = nfs_share_client_deletion
    if file_name_ex_filters is not None:
        payload['file_name_ex_filters'] = file_name_ex_filters
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.put(url, body=payload, params={"nfs_share_id": nfs_share_id})
    return response


def nfs_share_delete(client: DMEAPIClient, nfs_share_ids: list,
                     task_remarks: str = None) -> dict:
    """
    批量delete NFS 共享

    Args:
        client: DME API client
        nfs_share_ids: 待delete NFS 共享 ID list
        task_remarks: 异步任务备注info

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fileservice/v1/nfs-shares/delete"

    payload = {
        'nfs_share_ids': nfs_share_ids
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


# ============================================================================
# CIFS 共享子主题相关动作
# ============================================================================

def cifs_share_list(client: DMEAPIClient, raw_id: str = None, name: str = None,
              share_path: str = None, exact_share_path: str = None,
              fs_id: str = None, fs_name: str = None, dtree_id: str = None,
              dtree_name: str = None, storage_id: str = None,
              storage_name: str = None, vstore_raw_id: str = None,
              vstore_name: str = None, manufacturer: str = None,
              op_lock_enabled: bool = None, notify_enabled: bool = None,
              offline_file_modes: list = None, file_extension_filter_enabled: bool = None,
              abe_enabled: bool = None, page_no: int = 1, page_size: int = 10,
              sort_key: str = None, sort_dir: str = None,
              namespace_id: str = None, namespace_name: str = None,
              support_provisioning: bool = None, dc_id: str = None,
              dc_name: str = None) -> dict:
    """
    批量query CIFS 共享

    Args:
        client: DME API client
        raw_id: CIFS 共享在Storage device上的 ID(Optional), 1~256 个字符
        name: CIFS 共享name(Optional), 1~256 个字符, supports fuzzy query
        share_path: CIFS 共享路径(Optional), 1~512 个字符, supports fuzzy query
        exact_share_path: 精确搜索 CIFS 共享路径(Optional), 1~1024 个字符; 当 share_path 和 exact_share_path 都有值时, 优先选择 exact_share_path
        fs_id: CIFS 共享所属Filesystem的 ID(Optional), 1~64 个字符
        fs_name: CIFS 共享所属Filesystemname(Optional), 1~256 个字符, supports fuzzy query
        dtree_id: CIFS 共享所属 Dtree 的 ID(Optional), 1~64 个字符
        dtree_name: CIFS 共享所属 Dtree name(Optional), 1~256 个字符, supports fuzzy query
        storage_id: CIFS 共享storage设备的 ID(Optional), 1~64 个字符
        storage_name: CIFS 共享所属storage device name(Optional), 1~256 个字符, supports fuzzy query
        vstore_raw_id: CIFS 共享所属 vStore 在Storage device上分配的 ID(Optional), 1~256 个字符
        vstore_name: CIFS 共享所属 vStore name(Optional), 1~256 个字符, supports fuzzy query
        manufacturer: storage设备厂商(Optional), valid values: huawei (华为)、third_party (第三方)
        op_lock_enabled: CIFS 共享是否true Oplock(Optional), true: 是; false: 否
        notify_enabled: CIFS 共享是否true Notify(Optional), true: 是; false: 否
        offline_file_modes: CIFS 共享的离线缓存模式list(Optional), List<OfflineFileMode> type, max array members 4. parameter format: [{
                        mode: 离线缓存模式(Optional), valid values: none (false)、manual (手动)、documents (文档)、programs (程序), default manual,
        },...]
        file_extension_filter_enabled: CIFS 共享是否true文件扩展名过滤(Optional), true: 是; false: 否
        abe_enabled: CIFS 共享是否true ABE(Optional), true: 是; false: 否
        page_no: 分页页码(Optional), 1~10000000, default 1
        page_size: 每页数据条数(Optional), 1~1000, default 10
        sort_key: 排序字段(Optional), valid values: name、raw_id; 指定 raw_id 排序时仅支持 ID 为数字的object
        sort_dir: 排序方向(Optional), valid values: asc (升序)、desc (降序), default asc
        namespace_id: Namespace ID(Optional), 1~64 个字符, 仅 OceanStor Pacific 系列Storage device支持
        namespace_name: namespace name(Optional), 1~256 个字符, supports fuzzy query, 仅 OceanStor Pacific 系列Storage device支持
        support_provisioning: 是否支持业务发放(Optional), true: 是; false: 否; 下发此字段可过滤不支持业务发放设备的资源, 当前不支持业务发放的设备有 OceanStor Pacific 系列
        dc_id: 数据中心 ID(Optional), 1~128 个字符, 正则 ^[_A-Fa-f0-9\\-]+$
        dc_name: 数据中心name(Optional), 1~256 个字符

    Returns:
        {
            total: CIFS共享count (int32),
            cifs_shares: CIFS共享list (List<CifsShare>). parameter format: [{
                id: 共享ID (string),
                raw_id: 在设备上的ID (string),
                name: 共享name (string),
                share_path: 共享路径 (string),
                description: description (string),
                vstore_raw_id: tenant ID (string),
                vstore_name: 租户name (string),
                fs_id: FilesystemID (string),
                fs_name: Filesystemname (string),
                storage_id: storage device ID (string),
                storage_name: storage device name (string),
                storage_ip: Storage deviceIP (string),
                op_lock_enabled: 是否trueOPLock. valid values: true, false,
                notify_enabled: 是否true通知. valid values: true, false,
                offline_file_mode: 离线文件模式 (string),
                ca_enabled: 是否trueCA. valid values: true, false,
            }, ...],
        }
    """
    url = "/rest/fileservice/v1/cifs-shares/query"

    payload = {}

    if raw_id is not None:
        payload['raw_id'] = raw_id
    if name is not None:
        payload['name'] = name
    if share_path is not None:
        payload['share_path'] = share_path
    if exact_share_path is not None:
        payload['exact_share_path'] = exact_share_path
    if fs_id is not None:
        payload['fs_id'] = fs_id
    if fs_name is not None:
        payload['fs_name'] = fs_name
    if dtree_id is not None:
        payload['dtree_id'] = dtree_id
    if dtree_name is not None:
        payload['dtree_name'] = dtree_name
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if storage_name is not None:
        payload['storage_name'] = storage_name
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if vstore_name is not None:
        payload['vstore_name'] = vstore_name
    if manufacturer is not None:
        payload['manufacturer'] = manufacturer
    if op_lock_enabled is not None:
        payload['op_lock_enabled'] = op_lock_enabled
    if notify_enabled is not None:
        payload['notify_enabled'] = notify_enabled
    if offline_file_modes is not None:
        payload['offline_file_modes'] = offline_file_modes
    if file_extension_filter_enabled is not None:
        payload['file_extension_filter_enabled'] = file_extension_filter_enabled
    if abe_enabled is not None:
        payload['abe_enabled'] = abe_enabled
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if namespace_id is not None:
        payload['namespace_id'] = namespace_id
    if namespace_name is not None:
        payload['namespace_name'] = namespace_name
    if support_provisioning is not None:
        payload['support_provisioning'] = support_provisioning
    if dc_id is not None:
        payload['dc_id'] = dc_id
    if dc_name is not None:
        payload['dc_name'] = dc_name

    response = client.post(url, body=payload)
    return response


def cifs_share_show(client: DMEAPIClient, cifs_share_id: str) -> dict:
    """
    query指定 CIFS 共享details

    Args:
        client: DME API client
        cifs_share_id: CIFS 共享 ID

    Returns:
        {
            id: 共享ID (string),
            raw_id: 在设备上的ID (string),
            name: 共享name (string),
            share_path: 共享路径 (string),
            description: description (string),
            vstore_raw_id: tenant ID (string),
            vstore_name: 租户name (string),
            fs_id: FilesystemID (string),
            fs_name: Filesystemname (string),
            storage_id: storage device ID (string),
            storage_name: storage device name (string),
            storage_ip: Storage deviceIP (string),
            op_lock_enabled: 是否trueOPLock. valid values: true, false,
            notify_enabled: 是否true通知. valid values: true, false,
            offline_file_mode: 离线文件模式 (string),
            ca_enabled: 是否trueCA. valid values: true, false,
            abe_enabled: 是否trueABE. valid values: true, false,
            show_snapshot_enabled: 是否显示快照目录. valid values: true, false,
        }
    """
    url = "/rest/fileservice/v1/cifs-shares/{cifs_share_id}"

    response = client.get(url, params={"cifs_share_id": cifs_share_id})
    return response


def cifs_share_create(client: DMEAPIClient, create_cifs_param: dict, fs_id: str = None,
                namespace_id: str = None, task_remarks: str = None) -> dict:
    """
    create单个 CIFS 共享

    Args:
        client: DME API client
        create_cifs_param: create CIFS 共享参数. parameter format: {
                name: 共享name (Required),
                description: descriptioninfo (Optional),
                share_path: 共享路径 (Required),
                op_lock_enabled: Oplock功能开关 (Optional),
                notify_enabled: Notify功能开关 (Optional),
                ca_enabled: Failover连续可用特性开关 (Optional),
                offline_file_mode: 离线缓存模式 (Optional). valid values: none (false), manual (手动), documents (文档), programs (程序),
                ip_control_enabled: IP访问控制特性开关 (Optional),
                abe_enabled: ABE功能开关 (Optional),
                audititem_list: 支持审计的事件list (Optional). parameter format: [{
                        audititem: 审计事件type (defaultnone). valid values: none, all, open, create, read, write, close, delete, rename, get_security, set_security, get_attr, set_attr, get_xattr, set_xattr,
                     }, ...],
                apply_default_acl: 是否添加defaultACL (Optional),
                file_extension_filter_enabled: 是否true文件扩展名过滤特性 (Optional),
                show_previous_versions_enabled: 是否true显示历史version的功能 (Optional),
                show_snapshot_enabled: 是否true显示Snapshot的功能 (Optional),
                user_and_user_group_info: 用户和用户组list (Optional). parameter format: [{
                        user_or_user_group_id_in_storage: 用户或用户组在存储上的id (可选, 1~64字符, 变更时必填),
                        user_or_user_group_name: 用户名或用户组名 (可选, 1~255字符; 用户组name加前缀@),
                        domain_type: 域type (可选, defaultlocal). valid values: ad_domain, ldap_domain, local, nis_domain,
                        permission: 权限 (可选, defaultread). valid values: read, full_control, forbidden, read_and_write, read_and_write_not_del_rename,
                     }, ...],
                ip_addresses_and_segments: IP address和IP address段list (Optional). parameter format: [{
                        ip_or_segments_id_in_storage: IP address(段)在存储上的ID (可选, 1~64字符, 变更时必填),
                        ip_addresses_or_segments: IP address(段) (可选, 1~128字符, 最多32条),
                     }, ...],
                file_name_extension_filters: 文件扩展名过滤规则list (Optional). parameter format: [{
                        file_name_ex_id_in_storage: 规则在存储上的ID (可选, 1~64字符, 变更已添加规则时必填),
                        file_name_extension: 文件扩展名 (必选, 1~127字符, 支持通配符?和*),
                        rule_type: 规则type (可选, defaultreject). valid values: reject, permit,
                        fileoperations: 操作typelist (Optional),
                     }, ...],
                smb3_encryption_enable: 是否trueSMB3加密功能 (Optional),
                unencrypted_access: 是否允许未加密客户端访问 (Optional),
                enable_lease: 是否true租约锁定开关 (Optional),
             }
        fs_id: Filesystem的 ID, 与 namespace_id 互斥
        namespace_id: Namespace的 ID, 与 fs_id 互斥
        task_remarks: 异步任务备注info

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fileservice/v1/cifs-shares"

    payload = {
        'create_cifs_param': create_cifs_param
    }

    if fs_id is not None:
        payload['fs_id'] = fs_id
    if namespace_id is not None:
        payload['namespace_id'] = namespace_id
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def cifs_share_modify(client: DMEAPIClient, cifs_share_id: str, description: str = None,
                op_lock_enabled: bool = None, notify_enabled: bool = None,
                ca_enabled: bool = None, offline_file_mode: str = None,
                ip_control_enabled: bool = None, abe_enabled: bool = None,
                audititem_list: list = None, apply_default_acl: bool = None,
                file_extension_filter_enabled: bool = None,
                show_previous_versions_enabled: bool = None,
                show_snapshot_enabled: bool = None,
                user_and_user_group_info: list = None,
                ip_and_segments: list = None,
                file_name_ex_filters: list = None,
                task_remarks: str = None, smb3_encryption_enable: bool = None,
                unencrypted_access: bool = None, enable_lease: bool = None) -> dict:
    """
    modify指定 CIFS 共享

    Args:
        client: DME API client
        cifs_share_id: CIFS 共享 ID
        description: descriptioninfo, 最多 255 个字符
        op_lock_enabled: Oplock 功能开关
        notify_enabled: Notify 功能开关
        ca_enabled: Failover 连续可用特性开关
        offline_file_mode: 离线缓存模式, none/manual/documents/programs
        ip_control_enabled: IP 访问控制特性开关
        abe_enabled: ABE 功能开关
        audititem_list: 支持审计的事件list (Optional). parameter format: [{
                audititem: 审计事件type (defaultnone). valid values: none, all, open, create, read, write, close, delete, rename, get_security, set_security, get_attr, set_attr, get_xattr, set_xattr,
             }, ...]
        apply_default_acl: 是否添加default ACL
        file_extension_filter_enabled: 是否true文件扩展名过滤特性
        show_previous_versions_enabled: 是否true显示以前的version的功能
        show_snapshot_enabled: 是否true显示 Snapshot 的功能
        user_and_user_group_info: 用户和用户组list (Optional). parameter format: [{
                update_type: 变更type (可选, defaultadd). valid values: add (新增), delete (delete), modify (modify),
                param: 用户和用户组infoobject (Optional). attribute format: {
                        user_or_user_group_id_in_storage: 用户或用户组在存储上的id (可选, 1~64字符, 变更时必填),
                        user_or_user_group_name: 用户名或用户组名 (可选, 1~255字符; 用户组name加前缀@),
                        domain_type: 域type (可选, defaultlocal). valid values: ad_domain, ldap_domain, local, nis_domain,
                        permission: 权限 (可选, defaultread). valid values: read, full_control, forbidden, read_and_write, read_and_write_not_del_rename,
                }
             }, ...]
        ip_and_segments: IP address和IP address段list (Optional). parameter format: [{
                update_type: 变更type (可选, defaultadd). valid values: add (新增), delete (delete), modify (modify),
                param: IP address和IP address段infoobject (Optional). attribute format: {
                        ip_or_segments_id_in_storage: IP address(段)在存储上的ID (可选, 1~64字符, 变更时必填),
                        ip_addresses_or_segments: IP address(段) (可选, 1~128字符, 最多32条),
                }
             }, ...]
        file_name_ex_filters: 扩展名过滤规则list (Optional). parameter format: [{
                update_type: 变更type (可选, defaultadd). valid values: add (新增), delete (delete), modify (modify),
                param: 扩展名过滤规则object (Optional). attribute format: {
                        file_name_ex_id_in_storage: 规则在存储上的ID (可选, 1~64字符, 变更已添加规则时必填),
                        file_name_extension: 文件扩展名 (必选, 1~127字符, 支持通配符?和*, *只能位于最后一个字符),
                        rule_type: 规则type (可选, defaultreject). valid values: reject (拒绝), permit (允许),
                        fileoperations: 操作typelist (可选, 最多100个),
                }
             }, ...]
        task_remarks: 异步任务备注info, 0~1024 个字符
        smb3_encryption_enable: 是否true SMB3 加密功能
        unencrypted_access: 是否允许未加密客户端访问
        enable_lease: 是否true租约锁定开关

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fileservice/v1/cifs-shares/{cifs_share_id}"

    payload = {}

    if description is not None:
        payload['description'] = description
    if op_lock_enabled is not None:
        payload['op_lock_enabled'] = op_lock_enabled
    if notify_enabled is not None:
        payload['notify_enabled'] = notify_enabled

    payload = {}

    if description is not None:
        payload['description'] = description
    if op_lock_enabled is not None:
        payload['op_lock_enabled'] = op_lock_enabled
    if notify_enabled is not None:
        payload['notify_enabled'] = notify_enabled
    if ca_enabled is not None:
        payload['ca_enabled'] = ca_enabled
    if offline_file_mode is not None:
        payload['offline_file_mode'] = offline_file_mode
    if ip_control_enabled is not None:
        payload['ip_control_enabled'] = ip_control_enabled
    if abe_enabled is not None:
        payload['abe_enabled'] = abe_enabled
    if audititem_list is not None:
        payload['audititem_list'] = audititem_list
    if apply_default_acl is not None:
        payload['apply_default_acl'] = apply_default_acl
    if file_extension_filter_enabled is not None:
        payload['file_extension_filter_enabled'] = file_extension_filter_enabled
    if show_previous_versions_enabled is not None:
        payload['show_previous_versions_enabled'] = show_previous_versions_enabled
    if show_snapshot_enabled is not None:
        payload['show_snapshot_enabled'] = show_snapshot_enabled
    if user_and_user_group_info is not None:
        payload['user_and_user_group_info'] = user_and_user_group_info
    if ip_and_segments is not None:
        payload['ip_and_segments'] = ip_and_segments
    if file_name_ex_filters is not None:
        payload['file_name_ex_filters'] = file_name_ex_filters
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks
    if smb3_encryption_enable is not None:
        payload['smb3_encryption_enable'] = smb3_encryption_enable
    if unencrypted_access is not None:
        payload['unencrypted_access'] = unencrypted_access
    if enable_lease is not None:
        payload['enable_lease'] = enable_lease

    response = client.put(url, body=payload, params={"cifs_share_id": cifs_share_id})
    return response


def cifs_share_delete(client: DMEAPIClient, cifs_share_ids: list, task_remarks: str = None) -> dict:
    """
    批量delete CIFS 共享

    Args:
        client: DME API client
        cifs_share_ids: 需要delete CIFS 共享的 ID list
        task_remarks: 异步任务备注info

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fileservice/v1/cifs-shares/delete"

    payload = {
        'cifs_share_ids': cifs_share_ids
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def cifs_share_show_permissions(client: DMEAPIClient, cifs_share_id: str,
                          type: str = None, user_filter: dict = None,
                          ip_filter: dict = None,
                          file_filter: dict = None,
                          sort_key: str = None, sort_dir: str = None,
                          page_no: int = 1, page_size: int = 10) -> dict:
    """
    query单个 CIFS 共享的权限list

    query CIFS 共享的用户/用户组、IP 地址/IP 地址段、文件扩展名过滤规则等权限info. 

    Args:
        client: DME API client
        cifs_share_id: CIFS 共享 ID
        type: 权限type(Optional), valid values: user (用户/用户组)、ip (IP 地址/IP 地址段)、file (文件扩展名过滤规则); 
              不指定时返回所有type的权限

        user_filter: 用户权限过滤参数 (可选, dict type, type=user 时有效). parameter format: {
                user_or_user_group_name: 用户/用户组name(Optional), 1~256 个字符, 用于过滤用户/用户组list,
                domain_type: 域type(Optional). valid values: ad_domain (AD域用户/组)、ldap_domain (LDAP域用户/组)、local (本地用户/组)、nis_domain (NIS域用户/组),
                permissions: 权限过滤list(Optional), List<Permission> type, max array members 4. parameter format: [{
                        permission: 权限(Optional). valid values: read (读)、full_control (完全控制)、forbidden (禁止)、read_and_write (读写)、read_and_write_not_del_rename (读写, 不能delete、重命名). default read,
                },...],
                user_or_user_group_raw_id: 用户/用户组在Storage device上的 ID(Optional), 1~256 个字符,
        }

        ip_filter: IP 权限过滤参数 (可选, dict type, type=ip 时有效). parameter format: {
                ip_addresses_or_segments: IP 地址/IP 地址段(Optional), 1~256 个字符,
                ip_or_segments_raw_id: IP 地址/IP 地址段在Storage device上的 ID(Optional), 1~256 个字符,
        }

        file_filter: 文件扩展名过滤参数 (可选, dict type, type=file 时有效). parameter format: {
                rule_type: 文件扩展名type过滤(Optional). valid values: reject (只拒绝)、permit (只允许),
                file_name_extension: 文件扩展名name过滤(Optional), 1~256 个字符,
                file_extension_name_raw_id: 文件扩展名过滤规则在存储上的 ID(Optional), 1~256 个字符,
        }

        # 通用分页排序参数
        sort_key: 排序字段(Optional), valid values: raw_id、name
        sort_dir: 排序方向(Optional), valid values: asc (升序)、desc (降序), default asc
        page_no: 分页页码(Optional), 1~10000000, default 1
        page_size: 每页数据条数(Optional), 1~1000, default 10

    Returns:
        {
            permission_list: 权限list. parameter format: [{
                type: 权限type (string),
                rules: 规则list (List),
            }, ...],
        }
    """
    result = {'user': [], 'ip': [], 'file': []}

    # 根据 type 参数query对应type的权限
    if type is None or type == 'user':
        url = "/rest/fileservice/v1/cifs-shares/{cifs_share_id}/auth-users/query"
        payload = {}
        if user_filter is not None:
            for key, value in user_filter.items():
                if value is not None:
                    payload[key] = value
        if sort_key is not None:
            payload['sort_key'] = sort_key
        if sort_dir is not None:
            payload['sort_dir'] = sort_dir
        payload = {}
        if user_filter is not None:
            for key, value in user_filter.items():
                if value is not None:
                    payload[key] = value
        if sort_key is not None:
            payload['sort_key'] = sort_key
        if sort_dir is not None:
            payload['sort_dir'] = sort_dir
        if page_no is not None:
            payload['page_no'] = page_no
        if page_size is not None:
            payload['page_size'] = page_size
        response = client.post(url, body=payload)
        if response.get('auth_users'):
            result['user'] = response.get('auth_users')

    if type is None or type == 'ip':
        url = "/rest/fileservice/v1/cifs-shares/{cifs_share_id}/ip-access-rules/query"
        payload = {}
        if ip_filter is not None:
            for key, value in ip_filter.items():
                if value is not None:
                    payload[key] = value
        if sort_key is not None:
            payload['sort_key'] = sort_key
        if sort_dir is not None:
            payload['sort_dir'] = sort_dir
        payload = {}
        if ip_filter is not None:
            for key, value in ip_filter.items():
                if value is not None:
                    payload[key] = value
        if sort_key is not None:
            payload['sort_key'] = sort_key
        if sort_dir is not None:
            payload['sort_dir'] = sort_dir
        if page_no is not None:
            payload['page_no'] = page_no
        if page_size is not None:
            payload['page_size'] = page_size
        response = client.post(url, body=payload)
        if response.get('ip_access_rules'):
            result['ip'] = response.get('ip_access_rules')

    if type is None or type == 'file':
        url = "/rest/fileservice/v1/cifs-shares/{cifs_share_id}/file-filter-rules/query"
        payload = {}
        if file_filter is not None:
            for key, value in file_filter.items():
                if value is not None:
                    payload[key] = value
        if sort_key is not None:
            payload['sort_key'] = sort_key
        if sort_dir is not None:
            payload['sort_dir'] = sort_dir
        payload = {}
        if file_filter is not None:
            for key, value in file_filter.items():
                if value is not None:
                    payload[key] = value
        if sort_key is not None:
            payload['sort_key'] = sort_key
        if sort_dir is not None:
            payload['sort_dir'] = sort_dir
        if page_no is not None:
            payload['page_no'] = page_no
        if page_size is not None:
            payload['page_size'] = page_size
        response = client.post(url, body=payload)
        if response.get('file_filter_rules'):
            result['file'] = response.get('file_filter_rules')

    # 如果指定了 type, 只返回对应type的权限
    if type == 'user':
        return {'user_permissions': result['user']}
    elif type == 'ip':
        return {'ip_permissions': result['ip']}
    elif type == 'file':
        return {'file_permissions': result['file']}
    else:
        # 返回所有权限
        return {'user_permissions': result['user'], 'ip_permissions': result['ip'], 'file_permissions': result['file']}


# ============================================================================
# dataturbo_share (DataTurbo 共享) 子主题相关动作
# ============================================================================

def dataturbo_share_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 10,
                   raw_id: str = None, share_path: str = None, fs_id: str = None,
                   fs_name: str = None, dtree_id: str = None, dtree_name: str = None,
                   vstore_id: str = None, vstore_raw_id: str = None, vstore_name: str = None,
                   storage_id: str = None, storage_name: str = None, zone_id: str = None,
                   zone_name: str = None, scope: str = None, sort_key: str = None,
                   sort_dir: str = None) -> dict:
    """
    query DataTurbo 共享list

    Args:
        client: DME API client
        page_no: 分页页码(Optional), 1~10000000, default 1
        page_size: 每页数据条数(Optional), 1~1000, default 10
        raw_id: DataTurbo 共享在设备上 ID(Optional), 1~1024 个字符, 精确query
        share_path: 共享路径(Optional), 1~1024 个字符, 支持模糊搜索
        fs_id: DataTurbo 共享所属Filesystem ID(Optional), 1~64 个字符, 精确query
        fs_name: DataTurbo 共享所属Filesystemname(Optional), 1~256 个字符, 支持模糊搜索
        dtree_id: DataTurbo 共享所属 Dtree 的 ID(Optional), 32 个字符, 正则 ^[A-F0-9]{32}$, 精确query
        dtree_name: DataTurbo 共享所属 Dtree name(Optional), 1~256 个字符, supports fuzzy query
        vstore_id: DataTurbo 共享所属租户 ID(Optional), 1~64 个字符, 精确query
        vstore_raw_id: DataTurbo 共享所属租户 RAW ID(Optional), 1~64 个字符, 精确query
        vstore_name: DataTurbo 共享所属租户name(Optional), 1~256 个字符, 支持模糊搜索
        storage_id: DataTurbo 共享storage设备 ID(Optional), 1~64 个字符, 精确query
        storage_name: DataTurbo 共享所属storage device name(Optional), 1~256 个字符, 支持模糊搜索
        zone_id: DataTurbo 共享所属 zone ID(Optional), 1~64 个字符, 精确query
        zone_name: DataTurbo 共享所属 zone name(Optional), 1~256 个字符, 支持模糊搜索
        scope: 资源所属范围(Optional), valid values: local_scale (本地)、global_scale (全局)
        sort_key: 排序字段(Optional), valid values: raw_id (在设备上 ID)
        sort_dir: 排序方向(Optional), valid values: asc (升序)、desc (降序), default asc

    Returns:
        {
            total: DataTurbo共享count (int32),
            data: DataTurbo共享list (List<DpcShare>). parameter format: [{
                id: 共享ID (string),
                raw_id: 在设备上的ID (string),
                share_path: 共享路径 (string),
                fs_id: FilesystemID (string),
                fs_name: Filesystemname (string),
                storage_id: storage device ID (string),
                storage_name: storage device name (string),
                vstore_id: tenant ID (string),
                vstore_raw_id: 租户在设备上的ID (string),
                vstore_name: 租户name (string),
                charset: 字符集 (string),
            }, ...],
        }
    """
    url = "/rest/fileservice/v1/dpc-shares/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if raw_id is not None:
        payload['raw_id'] = raw_id
    if share_path is not None:
        payload['share_path'] = share_path
    if fs_id is not None:
        payload['fs_id'] = fs_id
    if fs_name is not None:
        payload['fs_name'] = fs_name
    if dtree_id is not None:
        payload['dtree_id'] = dtree_id
    if dtree_name is not None:
        payload['dtree_name'] = dtree_name
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if vstore_name is not None:
        payload['vstore_name'] = vstore_name
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if storage_name is not None:
        payload['storage_name'] = storage_name
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if zone_name is not None:
        payload['zone_name'] = zone_name
    if scope is not None:
        payload['scope'] = scope
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def dataturbo_share_show(client: DMEAPIClient, dataturbo_share_id: str) -> dict:
    """
    query指定 DataTurbo 共享details

    Args:
        client: DME API client
        dataturbo_share_id: DataTurbo 共享 ID

    Returns:
        {
            id: 共享ID (string),
            raw_id: 在设备上的ID (string),
            description: description (string),
            share_path: 共享路径 (string),
            fs_id: FilesystemID (string),
            fs_name: Filesystemname (string),
            storage_id: storage device ID (string),
            storage_name: storage device name (string),
            storage_ip: Storage deviceIP (string),
            vstore_id: tenant ID (string),
            vstore_raw_id: 租户在设备上的ID (string),
            vstore_name: 租户name (string),
            charset: 字符集 (string),
            zone_id: 区域ID (string),
            zone_name: 区domain name称 (string),
            zone_ip: 区域IP (string),
            scope: 范围 (string),
        }
    """
    url = "/rest/fileservice/v1/dpc-shares/{dataturbo_share_id}"

    response = client.get(url, params={"dataturbo_share_id": dataturbo_share_id})
    return response


def dataturbo_share_create(client: DMEAPIClient, charset: str, fs_id: str = None,
                     dtree_id: str = None, description: str = None,
                     dataturbo_share_auth: list = None, task_remarks: str = None) -> dict:
    """
    create DataTurbo 共享

    Args:
        client: DME API client
        charset: 字符集编码, 固定值 UTF_8
        fs_id: 需共享的Filesystem的 ID, 与 dtree_id 互斥, 必传其中一个
        dtree_id: 需共享的 Dtree 的 ID, 与 fs_id 互斥, 必传其中一个
        description: DataTurbo 共享description
        dataturbo_share_auth: DataTurbo 管理员list (Optional). parameter format: [{
                dpc_user_id: DataTurbo管理员ID (必选, 1~64个字符),
                permission: DataTurbo管理员权限 (必选, 固定值read_and_write),
             }, ...]
        task_remarks: 异步任务备注info

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fileservice/v1/dpc-shares"

    payload = {
        'charset': charset
    }

    if fs_id is not None:
        payload['fs_id'] = fs_id
    if dtree_id is not None:
        payload['dtree_id'] = dtree_id
    if description is not None:
        payload['description'] = description
    if dataturbo_share_auth is not None:
        payload['dpc_share_auth'] = dataturbo_share_auth
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def dataturbo_share_modify(client: DMEAPIClient, dataturbo_share_id: str, description: str = None,
                     dataturbo_share_auth_addition: list = None,
                     dataturbo_share_auth_deletion: list = None,
                     task_remarks: str = None) -> dict:
    """
    modify指定 DataTurbo 共享

    Args:
        client: DME API client
        dataturbo_share_id: DataTurbo 共享 ID
        description: DataTurbo 共享description
        dataturbo_share_auth_addition: 要增加的 DataTurbo 管理员list (Optional). parameter format: [{
                dpc_user_id: DataTurbo管理员ID (必选, 0~64个字符),
                permission: DataTurbo管理员权限 (必选, 固定值read_and_write),
             }, ...]
        dataturbo_share_auth_deletion: 要delete的 DataTurbo 管理员 ID list
        task_remarks: 异步任务备注info

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fileservice/v1/dpc-shares/{dataturbo_share_id}"

    payload = {}

    if description is not None:
        payload['description'] = description
    if dataturbo_share_auth_addition is not None:
        payload['dpc_share_auth_addition'] = dataturbo_share_auth_addition
    if dataturbo_share_auth_deletion is not None:
        payload['dpc_share_auth_deletion'] = dataturbo_share_auth_deletion

    payload = {}

    if description is not None:
        payload['description'] = description
    if dataturbo_share_auth_addition is not None:
        payload['dpc_share_auth_addition'] = dataturbo_share_auth_addition
    if dataturbo_share_auth_deletion is not None:
        payload['dpc_share_auth_deletion'] = dataturbo_share_auth_deletion
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.put(url, body=payload, params={"dataturbo_share_id": dataturbo_share_id})
    return response


def dataturbo_share_delete(client: DMEAPIClient, dataturbo_share_ids: list,
                     task_remarks: str = None) -> dict:
    """
    批量delete DataTurbo 共享

    Args:
        client: DME API client
        dataturbo_share_ids: DataTurbo 共享 ID list
        task_remarks: 异步任务备注info

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fileservice/v1/dpc-shares/delete"

    payload = {
        'dpc_share_ids': dataturbo_share_ids
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def dataturbo_share_show_permissions(client: DMEAPIClient, dataturbo_share_id: str,
                                      page_no: int = 1, page_size: int = 10,
                                      user_id: str = None, user_name: str = None,
                                      permission: str = None) -> dict:
    """
    query DataTurbo 共享管理员权限list

    Args:
        client: DME API client
        dataturbo_share_id: DataTurbo 共享 ID
        page_no: 分页页码(Optional), 1~10000000, default 1
        page_size: 每页数据条数(Optional), 1~1000, default 10
        user_id: DataTurbo 管理员 ID(Optional), 1~64 个字符, 精确query
        user_name: DataTurbo 管理员name(Optional), 1~256 个字符, 支持模糊搜索
        permission: DataTurbo 管理员权限(Optional), valid values: read_and_write (读写)

    Returns:
        {
            total: 权限count (int32),
            data: 权限list (List<DpcShareAuth>). parameter format: [{
                user_id: user ID (string),
                user_name: username (string),
                permission: 权限 (string),
            }, ...],
        }
    """
    url = "/rest/fileservice/v1/dpc-shares/{dataturbo_share_id}/dpc-share-auths/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if user_id is not None:
        payload['user_id'] = user_id
    if user_name is not None:
        payload['user_name'] = user_name
    if permission is not None:
        payload['permission'] = permission

    response = client.post(url, body=payload)
    return response


# ============================================================================
# Quota (quota) 子主题相关动作
# ============================================================================

def quota_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 20,
               ids: list = None, raw_ids: list = None, quota_type: str = None,
               parent_type: str = None, parent_raw_id: str = None,
               owner_name: str = None, vstore_id: str = None,
               vstore_raw_id: str = None, storage_id: str = None,
               sort_key: str = None, sort_dir: str = None,
               zone_id: str = None) -> dict:
    """
    queryquotalist

    Args:
        client: DME API client
        page_no: 分页query页码(Optional), 最小值 1, default 1
        page_size: 每页数据条数(Optional), 1~1000, default 20
        ids: quota的 ID list(Optional), List<string> type, max array members 100
        raw_ids: quota在Storage device上的 ID list(Optional), List<string> type, 0~1024 个字符, max array members 100
        quota_type: quota type(Optional), valid values: directory_quota (目录quota)、user_quota (用户quota)、user_group_quota (用户组quota)
        parent_type: quota所属父objecttype(Optional), 0~32 个字符; valid values: filesystem (Filesystem或者Namespace, OceanStor Pacific 设备称为Namespace, 其余设备称为Filesystem)、qtree (Quota Tree 或者 Dtree, OceanStor V3/V5 设备称为 Quota Tree, 其余设备称为 Dtree)
        parent_raw_id: quota所属父object在Storage device上的 ID(Optional), 0~256 个字符, 支持精确匹配; 当 parent_type 为 filesystem 时是Filesystem或Namespace在Storage device上的 ID, 当 parent_type 为 qtree 时是 Quota Tree 或 Dtree 在Storage device上的 ID
        owner_name: quota关联的用户或者用户组name(Optional), 0~256 个字符, supports fuzzy query
        vstore_id: quota所属租户的 ID(Optional), 0~64 个字符
        vstore_raw_id: quota所属租户Storage device上的 ID(Optional), 0~256 个字符, 支持精确匹配
        storage_id: quotastorage设备的 ID(Optional), 0~64 个字符
        sort_key: query的排序字段(Optional), valid values: id、space_hard_used_rate (空间使用率)、file_hard_used_rate (文件使用率), default id
        sort_dir: 排序方向(Optional), valid values: asc (升序)、desc (降序), default asc
        zone_id: zone id(Optional), 0~64 个字符, 仅 OceanStor A800 存储支持

    Returns:
        {
            total: quotacount (int32),
            datas: quotalist (List<QuotaListItem>). parameter format: [{
                id: quotaID (string),
                raw_id: 在设备上的ID (string),
                quota_type: quota type (string),
                parent_type: 父objecttype (string),
                owner_name: 属主name (string),
                space_soft_quota: 空间软quota (string),
                space_hard_quota: 空间硬quota (string),
                space_hard_used_rate: 空间硬quota使用率 (string),
                file_hard_quota: 文件数硬quota (string),
                file_hard_used: 文件数已使用 (string),
            }, ...],
        }
    """
    url = "/rest/fileservice/v1/quotas/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if ids is not None:
        payload['ids'] = ids
    if raw_ids is not None:
        payload['raw_ids'] = raw_ids
    if quota_type is not None:
        payload['quota_type'] = quota_type
    if parent_type is not None:
        payload['parent_type'] = parent_type
    if parent_raw_id is not None:
        payload['parent_raw_id'] = parent_raw_id
    if owner_name is not None:
        payload['owner_name'] = owner_name
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if zone_id is not None:
        payload['zone_id'] = zone_id

    response = client.post(url, body=payload)
    return response


def quota_show(client: DMEAPIClient, quota_id: str) -> dict:
    """
    query指定quotadetails

    Args:
        client: DME API client
        quota_id: quota ID

    Returns:
        {
            id: quotaID (string),
            raw_id: 在设备上的ID (string),
            quota_type: quota type (string),
            parent_type: 父objecttype (string),
            owner_name: 属主name (string),
            space_soft_quota: 空间软quota (string),
            space_hard_quota: 空间硬quota (string),
            file_hard_quota: 文件数硬quota (string),
            file_hard_used: 文件数已使用 (string),
        }
    """
    url = "/rest/fileservice/v1/quotas/query"

    payload = {
        'ids': [quota_id],
        'page_no': 1,
        'page_size': 1
    }

    response = client.post(url, body=payload)
    return response


def quota_create(client: DMEAPIClient, parent_id: str, parent_type: str,
                 quota_type: str, space_soft_quota: int = -1,
                 space_hard_quota: int = -1, space_advisory_quota: int = -1,
                 file_soft_quota: int = -1, file_hard_quota: int = -1,
                 file_advisory_quota: int = -1, snap_space_switch: bool = False,
                 soft_grace_time: int = None, quota_owner: dict = None,
                 dir_quota_target: str = None, task_remarks: str = None) -> dict:
    """
    createquota

    Args:
        client: DME API client
        space_soft_quota: 空间软quota(Optional), 单位 Byte, default -1 (字段无效); 当空间硬quota和空间软quota均有效时, 空间硬quota需大于空间软quota; OceanStor V5 设备时此字段必须为 1048576 的整数倍
        space_hard_quota: 空间硬quota(Optional), 单位 Byte, default -1 (字段无效); 当空间硬quota和空间软quota均有效时, 空间硬quota需大于空间软quota; OceanStor V5 设备时此字段必须为 1048576 的整数倍
        space_advisory_quota: 空间建议quota(Optional), 单位 Byte, default -1 (字段无效); 仅 OceanStor Pacific 设备支持; 当空间建议quota和空间硬quota或空间软quota均有效时, 空间建议quota需小于空间硬quota或空间软quota
        file_soft_quota: 文件数软quota(Optional), default -1 (字段无效); 当文件数硬quota和文件数软quota均有效时, 文件数硬quota需大于文件数软quota
        file_hard_quota: 文件数硬quota(Optional), default -1 (字段无效); 当文件数硬quota和文件数软quota均有效时, 文件数硬quota需大于文件数软quota
        file_advisory_quota: 文件数建议quota(Optional), default -1 (字段无效); 仅 OceanStor Pacific 设备支持; 当文件数建议quota和文件数硬quota或文件数软quota均有效时, 文件数建议quota需小于文件数硬quota或文件数软quota
        snap_space_switch: 是否统计快照空间(Optional), default false; true: 统计快照空间; false: 不统计快照空间; 仅 OceanStor Pacific 设备支持
        soft_grace_time: 超限时间(Optional), 0~4294967294, 单位 (天); 表示软配超限多长时间后自动转硬超限; 不传或取值 0 时达到软quota只告警; 仅 OceanStor Pacific 支持
        parent_id: 父资源 ID (必填), 1~64 个字符
        parent_type: 父resource type (必填), valid values: filesystem (Filesystem)、dtree (dtree, 存储cluster不支持)、namespace (Namespace)
        quota_type: quota type (必填), valid values: directory_quota (目录quota)、user_quota (用户quota)、user_group_quota (用户组quota)
        quota_owner: quota用户 (条件必传), QuotaOwner object. parameter format: {
                        name: 用户 (组)name (必填), 1~64 个字符, * 表示所有用户 (组),
                        type: 用户 (组)type (必填), 当 quota_type 为 user_quota 时valid values: unix_local_user (unix 本地用户)、domain_user (域用户)、windows_user (windows 用户); 当 quota_type 为 user_group_quota 时valid values: unix_local_user_group (unix 本地用户组)、domain_user_group (域用户组)、windows_user_group (windows 用户组),
                        domain_type: 域用户type (条件必传), 当 type 为 domain_user 或 domain_user_group 时必传; valid values: local (本地)、ad_domain (AD 域)、ldap_domain (LDAP 域)、nis_domain (NIS 域); OceanStor Pacific、OceanStor Dorado V6、OceanProtect 支持该字段,
        }
        dir_quota_target: 目录quota作用目标(Optional), valid values: dtree (模板目录quota, 作用于当前Filesystem下的所有 Dtree)、filesystem (根目录quota, 作用于当前Filesystem); 当父resource type为 filesystem 且quota type为 directory_quota 时有效
        task_remarks: 异步任务备注info

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fileservice/v1/quotas"

    payload = {
        'parent_id': parent_id,
        'parent_type': parent_type,
        'quota_type': quota_type,
        'space_soft_quota': space_soft_quota,
        'space_hard_quota': space_hard_quota,
        'space_advisory_quota': space_advisory_quota,
        'file_soft_quota': file_soft_quota,
        'file_hard_quota': file_hard_quota,
        'file_advisory_quota': file_advisory_quota,
        'snap_space_switch': snap_space_switch
    }

    if soft_grace_time is not None:
        payload['soft_grace_time'] = soft_grace_time
    if quota_owner is not None:
        payload['quota_owner'] = quota_owner
    if dir_quota_target is not None:
        payload['dir_quota_target'] = dir_quota_target
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def quota_modify(client: DMEAPIClient, quota_id: str,
                 space_soft_quota: int = None, space_hard_quota: int = None,
                 space_advisory_quota: int = None, file_soft_quota: int = None,
                 file_hard_quota: int = None, file_advisory_quota: int = None,
                 snap_space_switch: bool = None, soft_grace_time: int = None,
                 task_remarks: str = None) -> dict:
    """
    更新指定quota

    Args:
        client: DME API client
        quota_id: quota ID
        space_soft_quota: 空间软quota(Optional), 单位 Byte, -1 表示字段无效; 当空间硬quota和空间软quota均有效时, 空间硬quota需大于空间软quota
        space_hard_quota: 空间硬quota(Optional), 单位 Byte, -1 表示字段无效; 当空间硬quota和空间软quota均有效时, 空间硬quota需大于空间软quota
        space_advisory_quota: 空间建议quota(Optional), 单位 Byte, -1 表示字段无效; 仅 OceanStor Pacific 设备支持; 当空间建议quota和空间硬quota或空间软quota均有效时, 空间建议quota需小于空间硬quota或空间软quota
        file_soft_quota: 文件数软quota(Optional), -1 表示字段无效; 当文件数硬quota和文件数软quota均有效时, 文件数硬quota需大于文件数软quota
        file_hard_quota: 文件数硬quota(Optional), -1 表示字段无效; 当文件数硬quota和文件数软quota均有效时, 文件数硬quota需大于文件数软quota
        file_advisory_quota: 文件数建议quota(Optional), -1 表示字段无效; 仅 OceanStor Pacific 设备支持; 当文件数建议quota和文件数硬quota或文件数软quota均有效时, 文件数建议quota需小于文件数硬quota或文件数软quota
        snap_space_switch: 是否统计快照空间(Optional), true: 统计快照空间; false: 不统计快照空间; 仅 OceanStor Pacific 设备支持
        soft_grace_time: 超限时间(Optional), 0~4294967294, 单位 (天); 表示软配超限多长时间后自动转硬超限; 不下发或取值 0 时达到软quota只告警; 仅 OceanStor Pacific 支持
        task_remarks: 异步任务备注info

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fileservice/v1/quotas/{quota_id}"

    payload = {}

    if space_soft_quota is not None:
        payload['space_soft_quota'] = space_soft_quota
    if space_hard_quota is not None:
        payload['space_hard_quota'] = space_hard_quota
    if space_advisory_quota is not None:
        payload['space_advisory_quota'] = space_advisory_quota

    payload = {}

    if space_soft_quota is not None:
        payload['space_soft_quota'] = space_soft_quota
    if space_hard_quota is not None:
        payload['space_hard_quota'] = space_hard_quota
    if space_advisory_quota is not None:
        payload['space_advisory_quota'] = space_advisory_quota
    if file_soft_quota is not None:
        payload['file_soft_quota'] = file_soft_quota
    if file_hard_quota is not None:
        payload['file_hard_quota'] = file_hard_quota
    if file_advisory_quota is not None:
        payload['file_advisory_quota'] = file_advisory_quota
    if snap_space_switch is not None:
        payload['snap_space_switch'] = snap_space_switch
    if soft_grace_time is not None:
        payload['soft_grace_time'] = soft_grace_time
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.put(url, body=payload, params={"quota_id": quota_id})
    return response


def quota_delete(client: DMEAPIClient, quota_ids: list,
                 task_remarks: str = None) -> dict:
    """
    批量deletequota

    Args:
        client: DME API client
        quota_ids: 待delete的quota ID list
        task_remarks: 异步任务备注info

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fileservice/v1/quotas/delete"

    payload = {
        'ids': quota_ids
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


# ============================================================================
# filesystem (Filesystem) 子主题相关动作
# ============================================================================

def filesystem_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 100,
                     sort_dir: str = None, sort_key: str = None, name: str = None,
                     is_associated_qos: bool = None, qos_id: str = None,
                     storage_name: str = None, manufacturer: str = None,
                     storage_pool_name: str = None, storage_pool_id: str = None,
                     tier_name: str = None, tier_id: str = None,
                     vstore_name: str = None, vstore_raw_id: str = None,
                     project_name: str = None, project_id: str = None,
                     storage_id: str = None, fs_raw_id: str = None,
                     health_status: str = None, running_status: str = None,
                     alloc_type: str = None, type: str = None,
                     protection: str = None, dc_id: str = None,
                     dc_name: str = None, zone_id: str = None,
                     product_name: str = None, description: str = None,
                     tag_filters: list = None) -> dict:
    """
    批量queryFilesystem

    Args:
        client: DME API client
        page_no: 分页query页码(Optional), 1~10000000
        page_size: 每页显示的count(Optional), 1~1000, default 100
        sort_dir: 指定排序方向(Optional), valid values: asc (升序)、desc (降序)
        sort_key: 排序参数(Optional), valid values: capacity, available_capacity, capacity_usage_ratio,
                  nfs_count, cifs_count, dpc_count, dtree_count, name, allocate_pool_quota,
                  fs_raw_id, create_time, total_capacity_in_byte, available_capacity_in_byte,
                  alloc_capacity_in_byte, protection_capacity_in_byte, max_file_count, used_file_count
        name: Filesystemname(Optional), 1~256 个字符, 与 fs_raw_id 互斥, supports fuzzy match
        is_associated_qos: Filesystem是否已关联 QoS(Optional), true: 是; false: 否
        qos_id: QoS 策略 ID(Optional), 1~256 个字符
        storage_name: Filesystem所属设备name(Optional), 1~256 个字符, 与 storage_id 互斥, supports fuzzy match
        manufacturer: Storage device厂商(Optional), 1~64 个字符; valid values: huawei (Huawei)、dell_emc (DELL EMC)、
                     fujitsu（FUJITSU）、hitachi（Hitachi）、hpe（HPE）、ibm（IBM）、netapp（NetApp）、
                     pure (PURE)、panji (Panji)、third_part (非华为Storage device)
        storage_pool_name: Filesystem所属storage pool name(Optional), 1~256 个字符, 与 storage_pool_id 互斥, supports fuzzy match
        storage_pool_id: Storage pool ID(Optional), 1~255 个字符, 与 storage_pool_name 互斥
        tier_name: Filesystem所属服务等级name(Optional), 1~256 个字符, 与 tier_id 互斥, supports fuzzy match
        tier_id: 服务等级 ID(Optional), 1~256 个字符, 与 tier_name 互斥, 精确匹配
        vstore_name: Filesystem所属 vStore name(Optional), 1~256 个字符, 与 vstore_raw_id 互斥, supports fuzzy match
        vstore_raw_id: Filesystem所属租户在Storage device上的 ID(Optional), 1~64 个字符, 与 vstore_name 互斥
        project_name: Filesystem所属业务群组name(Optional), 1~256 个字符, 与 project_id 互斥, supports fuzzy match
        project_id: 业务群组 ID(Optional), 1~256 个字符, 与 project_name 互斥, 精确匹配
        storage_id: 归属Storage device ID(Optional), 1~256 个字符, 与 storage_name 互斥, 精确匹配
        fs_raw_id: Filesystem在设备上的 ID(Optional), 1~256 个字符, 与 name 互斥
        health_status: health status(Optional), valid values: normal (正常)、faulty (故障)、unknown (未知)
        running_status: running status(Optional), valid values: online (在线)、offline (离线)、invalid (失效)、
                       initializing (初始化中)、unknown (未知)
        alloc_type: Filesystemallocation type(Optional), valid values: thin (按需分配)、thick (固定分配)
        type: Filesystemtype(Optional), valid values: normal (普通Filesystem)、worm (wormFilesystem)、
              migration (migrationFilesystem)、container (容器应用Filesystem)、hash (哈希Filesystem)、
              smart_mobility_internal (SmartMobility内部Filesystem)
        protection: 保护status(Optional), valid values: protected (已保护)、not_protected (未保护)
        dc_id: 数据中心 ID(Optional), 1~128 个字符, 正则 ^[_A-Fa-f0-9\\-]+$
        dc_name: 数据中心name(Optional), 1~256 个字符
        zone_id: 所属 zone 的 ID(Optional), 1~256 个字符; 仅 OceanStor A800 系列Filesystem支持搜索, 传入clusterID代表query全局Filesystem
        product_name: Filesystem所属设备product name(Optional), 1~256 个字符, 支持模糊搜索
        description: Filesystemdescriptioninfo(Optional), 1~255 个字符
        tag_filters: 标签过滤list(Optional), List<TagFilters> type, max array members 11. parameter format: [{
                        tag_ids: 标签 ID list(Optional), max array members 10, 多个标签之间为或关系,
                        tag_type_id: tag type ID(Optional), 正则 ^[a-fA-F0-9]{32}$,
                        operator: 过滤条件 (必填), valid values: contain (包含)、not_contain (不包含),
        },...]

    Returns:
        {
            total: Filesystemcount (int32),
            data: Filesystemlist (List<FileSystemSummary>). parameter format: [{
                id: FilesystemID (string),
                fs_raw_id: 在设备上的ID (string),
                name: name (string),
                description: description (string),
                health_status: health status (string),
                running_status: running status (string),
                alloc_type: allocation type. valid values: thin, thick,
                type: type (string),
                protection: 保护status (string),
                capacity: capacity (string),
                available_capacity: available capacity (string),
                total_capacity_in_byte: total capacity (int64, 字节),
                available_capacity_in_byte: available capacity (int64, 字节),
                nfs_count: NFS共享数 (int32),
                cifs_count: CIFS共享数 (int32),
                dpc_count: DPC客户端数 (int32),
                dtree_count: dtree数 (int32),
                storage_id: storage device ID (string),
                storage_name: storage device name (string),
                storage_ip: Storage deviceIP (string),
            }, ...],
        }
    """
    url = "/rest/fileservice/v1/filesystems/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if name is not None:
        payload['name'] = name
    if is_associated_qos is not None:
        payload['is_associated_qos'] = is_associated_qos
    if qos_id is not None:
        payload['qos_id'] = qos_id
    if storage_name is not None:
        payload['storage_name'] = storage_name
    if manufacturer is not None:
        payload['manufacturer'] = manufacturer
    if storage_pool_name is not None:
        payload['storage_pool_name'] = storage_pool_name
    if storage_pool_id is not None:
        payload['storage_pool_id'] = storage_pool_id
    if tier_name is not None:
        payload['tier_name'] = tier_name
    if tier_id is not None:
        payload['tier_id'] = tier_id
    if vstore_name is not None:
        payload['vstore_name'] = vstore_name
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if project_name is not None:
        payload['project_name'] = project_name
    if project_id is not None:
        payload['project_id'] = project_id
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if fs_raw_id is not None:
        payload['fs_raw_id'] = fs_raw_id
    if health_status is not None:
        payload['health_status'] = health_status
    if running_status is not None:
        payload['running_status'] = running_status
    if alloc_type is not None:
        payload['alloc_type'] = alloc_type
    if type is not None:
        payload['type'] = type
    if protection is not None:
        payload['protection'] = protection
    if dc_id is not None:
        payload['dc_id'] = dc_id
    if dc_name is not None:
        payload['dc_name'] = dc_name
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if product_name is not None:
        payload['product_name'] = product_name
    if description is not None:
        payload['description'] = description
    if tag_filters is not None:
        payload['tag_filters'] = tag_filters

    response = client.post(url, body=payload)
    return response


def filesystem_show(client: DMEAPIClient, filesystem_id: str) -> dict:
    """
    query指定Filesystemdetails

    Args:
        client: DME API client
        filesystem_id: Filesystem ID

    Returns:
        {
            id: FilesystemID (string),
            fs_raw_id: 在设备上的ID (string),
            name: name (string),
            description: description (string),
            health_status: health status (string),
            running_status: running status (string),
            alloc_type: allocation type. valid values: thin, thick,
            type: type (string),
            protection: 保护status (string),
            capacity: capacity (string),
            available_capacity: available capacity (string),
            total_capacity_in_byte: total capacity (int64, 字节),
            available_capacity_in_byte: available capacity (int64, 字节),
            nfs_count: NFS共享数 (int32),
            cifs_count: CIFS共享数 (int32),
            dpc_count: DPC客户端数 (int32),
            dtree_count: dtree数 (int32),
            storage_id: storage device ID (string),
            storage_name: storage device name (string),
            storage_ip: Storage deviceIP (string),
            storage_type: storage device type (string),
        }
    """
    url = "/rest/fileservice/v1/filesystems/{filesystem_id}"

    response = client.get(url, params={"filesystem_id": filesystem_id})
    return response


def filesystem_delete(client: DMEAPIClient, filesystem_ids: list, task_remarks: str = None) -> dict:
    """
    批量deleteFilesystem

    Args:
        client: DME API client
        filesystem_ids: Filesystem ID list
        task_remarks: 异步任务备注info(Optional)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        } (异步任务)
    """
    url = "/rest/fileservice/v1/filesystems/delete"

    payload = {
        'file_system_ids': filesystem_ids
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def filesystem_batch_modify(client: DMEAPIClient, filesystems: list, task_remarks: str = None) -> dict:
    """
    批量modifyFilesystem

    仅支持modifyname. 

    Args:
        client: DME API client
        filesystems: 待modify的Filesysteminfolist (必填), List<UpdateFileSystemInfo> type, max array members 1000. parameter format: [{
                        file_system_id: Filesystem的唯一标识 (必填), 1~64 个字符,
                        name: Filesystemname (必填), 1~255 个字符; OceanStor Dorado V6、OceanStor、OceanProtect 系列只能包含字母、数字、"-"、"."和各国语言字符; OceanStor V3/V5 系列只能包含字母、数字和中文字符,
        },...]
        task_remarks: 异步任务备注info(Optional), 0~1024 个字符

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fileservice/v1/filesystems/modify"

    payload = {
        'filesystems': filesystems
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def filesystem_create(client: DMEAPIClient, storage_id: str, pool_raw_id: str,
                                 filesystem_specs: list, vstore_id: str = None,
                                 zone_id: str = None, task_remarks: str = None,
                                 gfs_group_id: str = None, automatic_update_time: bool = None,
                                 atime_update_mode: str = None, schedule_name: str = None,
                                 quota_switch: bool = None, vaai_switch: bool = None,
                                 initial_distribute_policy: str = None,
                                 capacity_threshold: int = None,
                                 tuning: dict = None,
                                 create_cifs_share_param: dict = None,
                                 create_nfs_share_param: dict = None,
                                 create_dpc_share_param: dict = None,
                                 owning_controller: str = None,
                                 snapshot_expired_enabled: bool = None,
                                 checksum_enabled: bool = None,
                                 ads_enabled: bool = None,
                                 security_mode: str = None,
                                 nas_locking_policy: str = None,
                                 capacity_autonegotiation: dict = None,
                                 worm: dict = None,
                                 snapshot_reserved_space_percentage: int = None,
                                 periodic_snapshots_limit: int = None,
                                 snapshot_dir_visible: bool = None,
                                 object_service_optimization: bool = None,
                                 case_sensitive: bool = None,
                                 audit_log_rules: list = None,
                                 unix_permissions: str = None) -> dict:
    """
    自定义createFilesystem

    Args:
        client: DME API client
        storage_id: Storage device ID
        pool_raw_id: Storage pool在指定Storage device上的 ID
        filesystem_specs: Filesystem规格list. parameter format: [{
                name: name (必选, 1~255字符),
                count: count (必选, 1~500),
                start_suffix: 起始后缀编号 (可选, 0~9999),
                capacity: capacityGB (必选, 1~262144),
                description: description (可选, 0~255字符),
             }, ...]
        vstore_id: 租户 ID(Optional)
        zone_id: 所属 zone 的 ID(Optional)
        task_remarks: 异步任务备注info(Optional)
        gfs_group_id: 全局数据空间的 ID(Optional)
        automatic_update_time: 是否更新访问时间(Optional)
        atime_update_mode: Atime 更新频率, hour/day/close(Optional)
        schedule_name: 定时 HyperCDP 计划name(Optional)
        quota_switch: 是否启用quota(Optional)
        vaai_switch: VAAI 开关(Optional)
        initial_distribute_policy: capacity初始分配策略, auto/highest_perf/performance/capacity(Optional)
        capacity_threshold: 总空间capacity告警阈值 50-99(Optional)
        tuning: 调优参数 (Optional). parameter format: {
                deduplication_enabled: 是否truededuplication (可选, defaultfalse). valid values: true, false,
                compression_enabled: 是否truecompression (可选, defaultfalse). valid values: true, false,
                block_size: Filesystem块大小KB (可选, default64). valid values: 4, 8, 16, 32, 64, 128,
                allocation_type: allocation type (可选, defaultthin). valid values: thin, thick,
                qos_policy_id: QoS策略ID (Optional),
                application_scenario: 应用场景 (可选, defaultuser_defined). valid values: database, VM, user_defined, container,
                workload_type_id: 应用typeid (可选, 1~32字符),
                dist_alg: Filesystem目录打散策略 (可选, 仅A800设备支持). valid values: capacity_balance, subdirectory_round_robin,
                qos_policy: SmartQos策略参数info (Optional). attribute format: {
                        max_bandwidth: max bandwidthMB/s (可选, 1~999999999),
                        max_iops: 最大iops (可选, 1~999999999),
                        min_bandwidth: min bandwidthMB/s (可选, 1~999999999),
                        min_iops: 最小iops (可选, 1~999999999),
                        burst_band_width: 突发带宽MB/s (Optional),
                        burst_iops: 突发IOPS (Optional),
                        burst_time: 最大突发时间秒 (Optional),
                        latency: latency (可选, 仅保护下限支持),
                        max_read_bandwidth: 最大读带宽MB/s (Optional),
                        max_write_bandwidth: 最大写带宽MB/s (Optional),
                        burst_read_band_width: 突发读带宽MB/s (Optional),
                        burst_write_band_width: 突发写带宽MB/s (Optional),
                        max_read_iops: 最大读iops (Optional),
                        max_write_iops: 最大写iops (Optional),
                        burst_read_iops: 突发读iops (Optional),
                        burst_write_iops: 突发写iops (Optional),
                        schedule_policy: 调度策略 (Optional). valid values: once, daily, weekly,
                        schedule_start_date: 生效开始日期 (可选, 格式yyyy-MM-dd),
                        start_time: 生效start time (可选, 格式hh:mm),
                        duration: 生效持续时间秒 (可选, 1800~86400),
                        weekly_days: 周调度策略 (可选, 1~6对应周一到周六),
                        alarm_switch: 限高告警开关 (Optional). valid values: off, on,
                        alarm_level: severity (Optional). valid values: event, alarm,
                        alarm_threshold: 告警阈值% (可选, 0~100),
                        resume_threshold: 恢复阈值% (可选, 0~100),
                        storage_divice_id: storage设备id (Optional),
                        name: QoSname (Optional),
                        description: description (Optional),
                        iotype: 策略type (Optional). valid values: 2 (总上限), 3 (读写上限),
                        vstore_id: 所属租户id (Optional),
                        vstore_name: 所属租户name (Optional),
                        global_flag: 是否全局 (Optional),
                }
             }
        create_cifs_share_param: 自动createCIFS共享参数(Optional). 格式参见动作帮助: nas cifs_share create
        create_nfs_share_param: 自动createNFS共享参数(Optional). 格式参见动作帮助: nas nfs_share create
        create_dpc_share_param: 自动createDataTurbo共享参数(Optional). 格式参见动作帮助: nas dataturbo_share create
        owning_controller: 归属Controller(Optional), 2~16个字符, 格式如0A、1B
        snapshot_expired_enabled: 是否truedelete旧的只读快照(Optional). true/false, defaultfalse
        checksum_enabled: 数据校验开关(Optional). true/false, defaulttrue
        ads_enabled: 是否true交换数据流功能(Optional). true/false, defaulttrue
        security_mode: 安全模式(Optional). 取值: mixed/native/ntfs/unix
        nas_locking_policy: NAS锁策略(Optional). 取值: mandatory/advisory/unknown
        capacity_autonegotiation: capacity自适应参数 (Optional). parameter format: {
                capacity_self_adjusting_mode: capacity自动调整模式 (可选, defaultfalse). valid values: grow_off (false), grow (自动扩容), grow_shrink (自动扩缩容),
                capacity_recycle_mode: capacity回收模式 (可选, default优先扩容). valid values: expand_capacity (优先扩容), delete_snapshots (优先delete旧快照),
                auto_size_enable: 自动调整capacity开关 (可选, defaulttrue). valid values: true, false,
                auto_grow_threshold_percent: 自动扩容触发门限% (可选, 2~99, default85),
                auto_shrink_threshold_percent: 自动缩容触发门限% (可选, 1~98, default50),
                max_auto_size: 自动扩容上限GB (可选, 1~33554432, default33554432),
                min_auto_size: 自动缩容下限GB (可选, 1~33554432, default33554432),
                auto_size_increment: 自动扩缩容单次变化量MB (可选, 64~102400, default1024),
             }
        worm: FilesystemWorm参数 (Optional). parameter format: {
                type: WORM保护模式 (Optional). valid values: none_mode (无default策略), enterprise_mode (企业遵从), compliance_mode (法规遵从), advance_mode (高安遵从), audit_log (审计日志), non_worm (非WORM),
                min_protect_period: 最小保护期 (可选, default0),
                min_protect_period_unit: 最小保护期单位 (可选, defaultyear). valid values: minute, hour, day, month, year,
                max_protect_period: 最大保护期 (可选, 0~4294967295, default70),
                max_protect_period_unit: 最大保护期单位 (可选, defaultyear). valid values: minute, hour, day, month, year,
                def_protect_period: default保护期 (可选, 不小于最小, 不大于最大, default70),
                def_protect_period_unit: default保护期单位 (可选, defaultyear). valid values: minute, hour, day, month, year,
                auto_lock: WORM自动锁定模式 (可选, defaulttrue). valid values: true, false,
                auto_lock_time: 自动锁定时间 (可选, default2),
                auto_lock_time_unit: 自动锁定时间单位 (可选, defaulthour). valid values: minute, hour, day, month, year,
                auto_del: 自动delete模式 (可选, defaultfalse). valid values: true, false,
                is_worm_audit_log_fs: WORM审计日志Filesystem (可选, defaultfalse). valid values: true, false,
                worm_append_unit: WORM追加态文件保护粒度 (可选, 仅advance_mode支持). valid values: 256KB, 512KB, 1M,
             }
        snapshot_reserved_space_percentage: 快照预留空间百分比(Optional), 0~90
        periodic_snapshots_limit: 定时快照count限制(Optional), 1~2048
        snapshot_dir_visible: 快照目录是否可见(Optional). true/false
        object_service_optimization: object服务优化(Optional). true/false
        case_sensitive: 大小写敏感模式(Optional). true/false
        audit_log_rules: 审计日志规则集合(Optional), 如: set_security、get_security、set_attr、get_attr等, 最多100条
        unix_permissions: Filesystem目录权限(Optional), 格式如0755

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fileservice/v1/filesystems/customize-filesystems"

    payload = {
        'storage_id': storage_id,
        'pool_raw_id': pool_raw_id,
        'filesystem_specs': filesystem_specs
    }

    if vstore_id is not None:
        payload['vstore_id'] = vstore_id
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks
    if gfs_group_id is not None:
        payload['gfs_group_id'] = gfs_group_id
    if automatic_update_time is not None:
        payload['automatic_update_time'] = automatic_update_time
    if atime_update_mode is not None:
        payload['atime_update_mode'] = atime_update_mode
    if schedule_name is not None:
        payload['schedule_name'] = schedule_name
    if quota_switch is not None:
        payload['quota_switch'] = quota_switch
    if vaai_switch is not None:
        payload['vaai_switch'] = vaai_switch
    if initial_distribute_policy is not None:
        payload['initial_distribute_policy'] = initial_distribute_policy
    if capacity_threshold is not None:
        payload['capacity_threshold'] = capacity_threshold
    if tuning is not None:
        payload['tuning'] = tuning
    if create_cifs_share_param is not None:
        payload['create_cifs_share_param'] = create_cifs_share_param
    if create_nfs_share_param is not None:
        payload['create_nfs_share_param'] = create_nfs_share_param
    if create_dpc_share_param is not None:
        payload['create_dpc_share_param'] = create_dpc_share_param
    if owning_controller is not None:
        payload['owning_controller'] = owning_controller
    if snapshot_expired_enabled is not None:
        payload['snapshot_expired_enabled'] = snapshot_expired_enabled
    if checksum_enabled is not None:
        payload['checksum_enabled'] = checksum_enabled
    if ads_enabled is not None:
        payload['ads_enabled'] = ads_enabled
    if security_mode is not None:
        payload['security_mode'] = security_mode
    if nas_locking_policy is not None:
        payload['nas_locking_policy'] = nas_locking_policy
    if capacity_autonegotiation is not None:
        payload['capacity_autonegotiation'] = capacity_autonegotiation
    if worm is not None:
        payload['worm'] = worm
    if snapshot_reserved_space_percentage is not None:
        payload['snapshot_reserved_space_percentage'] = snapshot_reserved_space_percentage
    if periodic_snapshots_limit is not None:
        payload['periodic_snapshots_limit'] = periodic_snapshots_limit
    if snapshot_dir_visible is not None:
        payload['snapshot_dir_visible'] = snapshot_dir_visible
    if object_service_optimization is not None:
        payload['object_service_optimization'] = object_service_optimization
    if case_sensitive is not None:
        payload['case_sensitive'] = case_sensitive
    if audit_log_rules is not None:
        payload['audit_log_rules'] = audit_log_rules
    if unix_permissions is not None:
        payload['unix_permissions'] = unix_permissions

    response = client.post(url, body=payload)
    return response


def filesystem_query_available(client: DMEAPIClient, feature_type: str,
                                local_storage_id: str, remote_storage_id: str = None,
                                name: str = None, page_no: int = 1,
                                page_size: int = 20, sort_key: str = None,
                                sort_dir: str = None) -> dict:
    """
    query可用的Filesystem

    query可用于配置增删特性的Filesystem. 当前仅支持可配置远程复制的Filesystem. 

    Args:
        client: DME API client
        feature_type: 特性type, 当前仅支持 remote_replication (远程复制)
        local_storage_id: 本端Storage device ID
        remote_storage_id: 远端Storage device ID (当 feature_type 为 remote_replication 时必选)
        name: 本端Filesystemname, 支持模糊搜索
        page_no: 分页query页码, default 1
        page_size: 每页显示的count, default 20
        sort_key: 排序字段, name (Filesystemname)或 capacity (Filesystemcapacity)
        sort_dir: 排序方向, asc (升序)或 desc (降序)

    Returns:
        {
            total: 可用Filesystemcount (int32),
            available_filesystems: 可用Filesystemlist (List<AvailableFilesystemResponse>). parameter format: [{
                id: FilesystemID (string),
                name: Filesystemname (string),
                capacity: capacity (string),
            }, ...],
        }
    """
    url = "/rest/fileservice/v1/filesystems/available-filesystems/query"

    payload = {
        'feature_type': feature_type,
        'local_storage_id': local_storage_id
    }

    if remote_storage_id is not None:
        payload['remote_storage_id'] = remote_storage_id
    if name is not None:
        payload['name'] = name
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def filesystem_modify(client: DMEAPIClient, file_system_id: str, name: str = None,
           description: str = None, capacity: int = None,
           capacity_threshold: int = None, initial_distribute_policy: str = None,
           automatic_update_time: bool = None, atime_update_mode: str = None,
           quota_switch: bool = None, vaai_switch: bool = None,
           owning_controller: str = None,
           snapshot_expired_enabled: bool = None,
           checksum_enabled: bool = None, ads_enabled: bool = None,
           security_mode: str = None, nas_locking_policy: str = None,
           snapshot_reserved_space_percentage: int = None,
           periodic_snapshots_limit: int = None,
           snapshot_dir_visible: bool = None, tuning: dict = None,
           capacity_autonegotiation: dict = None, worm: dict = None,
           task_remarks: str = None, audit_log_rules: list = None,
           unix_permissions: str = None) -> dict:
    """
    modify指定Filesystem

    Args:
        client: DME API client
        file_system_id: Filesystem唯一标识
        name: Filesystemname, 1~255个字符(Optional)
        description: descriptioninfo, 0~255个字符(Optional)
        capacity: Filesystemcapacity, 单位 GB, 1~33554432(Optional)
        capacity_threshold: 总空间capacity告警阈值 50-99(Optional)
        initial_distribute_policy: capacity初始分配策略, auto/highest_perf/performance/capacity(Optional)
        automatic_update_time: 文件被读取后是否更新访问时间, truetrue/falsefalse(Optional)
        atime_update_mode: Atime 更新频率, hour (每小时)/day (每天)/close (未启用)(Optional)
        quota_switch: 是否启用quota, true启用/false不启用(Optional)
        vaai_switch: VAAI 开关, 启用后不能false, true启用/false未启用(Optional)
        owning_controller: 归属Controller, 2~16个字符(Optional)
        snapshot_expired_enabled: 是否truedelete旧的只读快照, truetrue/falsefalse(Optional)
        checksum_enabled: 数据校验开关, truetrue/falsefalse(Optional)
        ads_enabled: 是否true交换数据流功能, truetrue/falsefalse, true后不允许false(Optional)
        security_mode: 安全模式, mixed/native/ntfs/unix(Optional)
        nas_locking_policy: NAS锁策略, mandatory (强制锁)/advisory (建议锁)/unknown(Optional)
        snapshot_reserved_space_percentage: 快照预留空间百分比, 0~90(Optional)
        periodic_snapshots_limit: 定时快照count限制, 1~2048(Optional)
        snapshot_dir_visible: 快照目录是否可见, true可见/false不可见(Optional)
        tuning: 调优参数 (Optional). parameter format: {
                qos_policy: SmartQos策略参数info (UpdateFileSystemQosPolicyobject). attribute format: {
                        max_bandwidth: max bandwidthMB/s (可选, 1~999999999; 与min_bandwidth/min_iops互斥, A800下不互斥),
                        max_iops: max IOPS (可选, 1~999999999; 与min_bandwidth/min_iops互斥, A800下不互斥),
                        min_bandwidth: min bandwidthMB/s (可选, 1~999999999; 与max_bandwidth/max_iops互斥, A800下不互斥),
                        min_iops: min IOPS (可选, 1~999999999; 与max_bandwidth/max_iops互斥, A800下不互斥),
                        burst_band_width: 突发带宽MB/s (可选, 1~999999999),
                        burst_iops: 突发IOPS (可选, 1~999999999),
                        burst_time: 最大突发时间秒 (可选, 1~999999999),
                        latency: latency (可选, 1~999999999; A800/Dorado V6可选500/1500单位us, V3/V5可自定义单位ms),
                        max_read_bandwidth: 最大读带宽MB/s (可选, 1~999999999; 仅读写上限策略有效),
                        max_write_bandwidth: 最大写带宽MB/s (可选, 1~999999999; 仅读写上限策略有效),
                        burst_read_band_width: 突发读带宽MB/s (可选, 1~999999999; 仅读写上限策略有效),
                        burst_write_band_width: 突发写带宽MB/s (可选, 1~999999999; 仅读写上限策略有效),
                        max_read_iops: 最大读IOPS (可选, 1~999999999; 仅读写上限策略有效),
                        max_write_iops: 最大写IOPS (可选, 1~999999999; 仅读写上限策略有效),
                        burst_read_iops: 突发读IOPS (可选, 1~999999999; 仅读写上限策略有效),
                        burst_write_iops: 突发写IOPS (可选, 1~999999999; 仅读写上限策略有效),
                        schedule_policy: 调度策略 (Optional). valid values: once, daily, weekly,
                        schedule_start_date: 生效开始日期 (可选, 格式yyyy-MM-dd, 0~64字符),
                        start_time: 生效start time (可选, 格式hh:mm, 0~64字符),
                        duration: 生效持续时间秒 (可选, 1800~86400),
                        weekly_days: 周调度策略 (可选, 0-6对应周日到周六, 最多7个; schedule_policy为weekly时生效),
                        alarm_switch: 限高告警开关 (Optional). valid values: off, on,
                        alarm_level: 限高severity (Optional). valid values: event (事件), alarm (告警),
                        alarm_threshold: 限高告警阈值% (可选, 0~100),
                        resume_threshold: 限高告警恢复阈值% (可选, 0~100),
                        storage_divice_id: 所属storage device ID (可选, 1~64字符),
                        name: QoSname (可选, 1~255字符; A800下未使用),
                        description: QoSdescription (可选, 1~255字符; A800下未使用),
                        iotype: 策略type (Optional). valid values: 2 (总性能上限), 3 (读写上限; 仅部分设备支持),
                        vstore_id: 所属tenant ID (可选, 1~64字符; A800下未使用),
                        vstore_name: 所属租户name (可选, 1~64字符; A800下未使用),
                        global_flag: 是否全局 (可选; 当前version只支持全局; A800下未使用),
                        qos_policy_id: QoS策略ID (可选, 0~64字符; 与除enabled外的其他参数互斥),
                        enabled: 是否启用QoSPolicy (可选, defaultfalse),
                },
                deduplication_enabled: deduplication (可选, defaultfalse),
                compression_enabled: compression (可选, defaultfalse),
                allocation_type: Filesystemallocation type (可选, defaultthin). valid values: thin (精简), thick (厚),
             }
        capacity_autonegotiation: capacity自适应参数 (Optional). parameter format: {
                capacity_self_adjusting_mode: capacity自动调整模式 (可选, defaultfalse). valid values: grow_off (false), grow (自动扩容), grow_shrink (自动扩缩容),
                capacity_recycle_mode: capacity回收模式 (可选, default优先扩容). valid values: expand_capacity (优先扩容), delete_snapshots (优先delete旧快照),
                auto_size_enable: 自动调整capacity开关 (可选, default打开). valid values: true, false,
                auto_grow_threshold_percent: 自动扩容触发门限% (可选, 2~99, default85; 必须大于缩容触发门限),
                auto_shrink_threshold_percent: 自动缩容触发门限% (可选, 1~98, default50),
                max_auto_size: 自动扩容上限GB (可选, 1~33554432, default33554432; 必须大于等于缩容下限和Filesystemcapacity),
                min_auto_size: 自动缩容下限GB (可选, 1~33554432, default33554432),
                auto_size_increment: 自动扩缩容单次变化量MB (可选, 64~102400, default1024),
             }
        worm: FilesystemWorm参数 (Optional). parameter format: {
                type: WORM保护遵从模式 (Optional). valid values: none_mode, enterprise_mode, compliance_mode, advance_mode, audit_log, non_worm,
                min_protect_period: 最小保护期 (可选, 0~4294967295, default0; 4294967295为无限期),
                min_protect_period_unit: 最小保护期单位 (可选, defaultyear). valid values: minute, hour, day, month, year,
                max_protect_period: 最大保护期 (可选, 1~4294967295, default70; 4294967295为无限期),
                max_protect_period_unit: 最大保护期单位 (可选, defaultyear). valid values: minute, hour, day, month, year,
                def_protect_period: default保护期 (可选, 0~4294967295, default70; 不小于最小且不大于最大),
                def_protect_period_unit: default保护期单位 (可选, defaultyear). valid values: minute, hour, day, month, year,
                auto_lock: WORM自动锁定模式 (可选, defaulttrue; advance_mode不支持). valid values: true, false,
                auto_lock_time: 自动锁定时间 (可选, 最小值1, default2),
                auto_lock_time_unit: 自动锁定时间单位 (可选, defaulthour). valid values: minute, hour, day, month, year,
                auto_del: 自动delete模式 (可选, defaultfalse; advance_mode不支持). valid values: true, false,
                is_worm_audit_log_fs: WORM审计日志Filesystem (可选, defaultfalse; 一个租户只能有一个),
                worm_append_unit: WORM追加态文件保护粒度 (可选, 仅advance_mode支持). valid values: 256KB, 512KB, 1M,
             }
        task_remarks: 异步任务备注info, 0~1024个字符(Optional)
        audit_log_rules: 审计日志规则集合(Optional), 如: set_security、get_security、set_attr、get_attr等, 最多100条
        unix_permissions: Filesystem目录权限(Optional), 格式如0755

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/fileservice/v1/filesystems/{file_system_id}"

    payload = {}

    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description
    if capacity is not None:
        payload['capacity'] = capacity

    payload = {}

    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description
    if capacity is not None:
        payload['capacity'] = capacity
    if capacity_threshold is not None:
        payload['capacity_threshold'] = capacity_threshold
    if initial_distribute_policy is not None:
        payload['initial_distribute_policy'] = initial_distribute_policy
    if automatic_update_time is not None:
        payload['automatic_update_time'] = automatic_update_time
    if atime_update_mode is not None:
        payload['atime_update_mode'] = atime_update_mode
    if quota_switch is not None:
        payload['quota_switch'] = quota_switch
    if vaai_switch is not None:
        payload['vaai_switch'] = vaai_switch
    if owning_controller is not None:
        payload['owning_controller'] = owning_controller
    if snapshot_expired_enabled is not None:
        payload['snapshot_expired_enabled'] = snapshot_expired_enabled
    if checksum_enabled is not None:
        payload['checksum_enabled'] = checksum_enabled
    if ads_enabled is not None:
        payload['ads_enabled'] = ads_enabled
    if security_mode is not None:
        payload['security_mode'] = security_mode
    if nas_locking_policy is not None:
        payload['nas_locking_policy'] = nas_locking_policy
    if snapshot_reserved_space_percentage is not None:
        payload['snapshot_reserved_space_percentage'] = snapshot_reserved_space_percentage
    if periodic_snapshots_limit is not None:
        payload['periodic_snapshots_limit'] = periodic_snapshots_limit
    if snapshot_dir_visible is not None:
        payload['snapshot_dir_visible'] = snapshot_dir_visible
    if tuning is not None:
        payload['tuning'] = tuning
    if capacity_autonegotiation is not None:
        payload['capacity_autonegotiation'] = capacity_autonegotiation
    if worm is not None:
        payload['worm'] = worm
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks
    if audit_log_rules is not None:
        payload['audit_log_rules'] = audit_log_rules
    if unix_permissions is not None:
        payload['unix_permissions'] = unix_permissions

    response = client.put(url, body=payload, params={"file_system_id": file_system_id})
    return response



# ============================================================================
# namespace (Namespace) 子主题相关动作
# ============================================================================

def namespace_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 100,
         sort_dir: str = None, sort_key: str = None, name: str = None,
         vstore_name: str = None, vstore_raw_id: str = None, vstore_id: str = None,
         raw_id: str = None, pool_name: str = None, storage_id: str = None,
         enable_encrypt: bool = None, support_provisioning: bool = None,
         gfs_id: str = None, gfs_name: str = None, has_gfs: bool = None) -> dict:
    """
    批量queryNamespace
    
    Args:
        client: DME API client
        page_no: 分页query页码(Optional), 1~10000000
        page_size: 每页显示的count(Optional), 1~1000, default 100
        sort_dir: 指定排序方向(Optional), valid values: asc (升序)、desc (降序)
        sort_key: 排序参数(Optional), valid values: namespace_used_rate、file_used_rate
        name: namespace name(Optional), 1~256 个字符, supports fuzzy query
        vstore_name: Namespace所属租户name(Optional), 1~256 个字符, supports fuzzy query
        vstore_raw_id: Namespace所属 vStore 在Storage device上分配的 ID(Optional), 1~128 个字符
        vstore_id: Namespace所属 vStore 的 ID(Optional), 1~128 个字符
        raw_id: Namespace在Storage device上的 ID(Optional), 1~256 个字符
        pool_name: storage pool name(Optional), 1~256 个字符, supports fuzzy query
        storage_id: 归属Storage device ID(Optional), 1~255 个字符
        enable_encrypt: 是否true加密(Optional), true: 是; false: 否
        support_provisioning: 是否支持业务发放(Optional), true: 是; false: 否; 下发此字段可过滤不支持业务发放设备的资源, 当前不支持业务发放的设备有 DataTurbo 系列
        gfs_id: 全局Namespace ID(Optional), 1~64 个字符
        gfs_name: 全局namespace name(Optional), 1~256 个字符
        has_gfs: 是否包含所属全局Namespace的Namespace(Optional), true: 是; false: 否; has_gfs 为 false 时不支持下发 gfs_id
    
    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含: 
        - total: Namespacecount
        - namespace_list: Namespacelist, 包含 id, raw_id, name, storage_id, vstore_id 等info
    """
    url = "/rest/fileservice/v1/namespaces/query"
    
    payload = {}
    
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if name is not None:
        payload['name'] = name
    if vstore_name is not None:
        payload['vstore_name'] = vstore_name
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if pool_name is not None:
        payload['pool_name'] = pool_name
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if enable_encrypt is not None:
        payload['enable_encrypt'] = enable_encrypt
    if support_provisioning is not None:
        payload['support_provisioning'] = support_provisioning
    if gfs_id is not None:
        payload['gfs_id'] = gfs_id
    if gfs_name is not None:
        payload['gfs_name'] = gfs_name
    if has_gfs is not None:
        payload['has_gfs'] = has_gfs
    
    response = client.post(url, body=payload)
    return response


def namespace_show(client: DMEAPIClient, namespace_id: str) -> dict:
    """
    query指定Namespacedetails
    
    Args:
        client: DME API client
        namespace_id: Namespace ID (必选, 1~64 个字符)
    
    Returns:
        {
            id: namespace ID (string),
            raw_id: 在Storage device上的ID (string),
            name: namespace name (string),
            storage_id: storage device ID (string),
            vstore_id: tenant ID (string),
            vstore_name: 租户name (string),
            pool_id: storage pool ID (string),
            pool_name: storage pool name (string),
            running_status: running status. valid values: NORMAL, UNKNOWN,
            space_used_rate: 空间使用率 (string),
            file_used_rate: 文件使用率 (string),
            space_used: 已使用空间 (string),
            file_used: 已使用文件数 (string),
            trash_enable: 是否true回收站 (string),
            enable_encrypt: 是否true加密 (string),
        }
        - rdc: 数据冗余份数
        - acl_policy_type: 安全模式
        - gfs_id: 全局Namespace ID
        - qos_policy: QoS 策略
        - worm: WORM 参数
        等详细info
    """
    url = "/rest/fileservice/v1/namespaces/{namespace_id}"
    
    response = client.get(url, params={"namespace_id": namespace_id})
    return response


def namespace_create(client: DMEAPIClient, storage_id: str, pool_raw_id: str,
           namespace_specs: list = None, enable_update_atime: bool = None,
           trash_visible: bool = None, trash_enable: bool = None,
           interval_trash: int = None, dps_switch: bool = None,
           forbidden_dpc: bool = None, audit_log_switch: bool = None,
           audit_log_rule: list = None, atime_update_mode: int = None,
           acl_policy_type: str = None, enable_encrypt: bool = None,
           crypt_alg: str = None, case_sensitive: bool = None,
           show_snap_dir: bool = None, rdc: str = None, worm: dict = None,
           qos_policy: dict = None, public_network_qos_policy: dict = None,
           private_network_qos_policy: dict = None,
           create_s3_param: dict = None, application_type: str = None,
           task_remarks: str = None) -> dict:
    """
    批量createNamespace
    
    Args:
        client: DME API client
        storage_id: Storage device ID (必填)
        pool_raw_id: Storage pool在Storage device上的 ID (必填)
        namespace_specs: Namespace批量参数. parameter format: [{
                name: name (必填, 1~255字符, 支持数字字母下划线.-),
                count: count (必填, 1~500),
                start_suffix: 起始后缀编号 (可选, 0~9999; 起始后缀+count<=9999),
                isInGfs: 是否在全局Namespace中 (Optional). valid values: true, false,
             }, ...]
        enable_update_atime: 是否更新 Atime
        trash_visible: 回收站目录是否可见, default不可见
        trash_enable: 回收站功能是否true, default不true
        interval_trash: 回收站保护时长 (分钟), 0 表示永久保留, 最大 4294967295
        dps_switch: 元数据检索开关, true true
        forbidden_dpc: 是否禁止 dpc 挂载
        audit_log_switch: 是否true审计日志, defaultfalse
        audit_log_rule: 审计日志规则list, valid values: open, create, read, write, close, 
                       delete, rename, get_attr, set_attr, get_security, set_security,
                       get_xattr, set_xattr, list_dir, contact, mount_or_unmount, login_or_logoff
        atime_update_mode: atime 更新频率, 4294967295 false, 3600 1 小时, 86400 1 天
        acl_policy_type: 安全模式, valid values: mixed, unix, native, ntfs, default unix
        enable_encrypt: 是否true加密
        crypt_alg: 加密算法type, valid values: XTS_AES_128, XTS_AES_256, XTS_SM4, UNKNOWN
        case_sensitive: 大小写是否敏感, default不敏感
        show_snap_dir: 快照目录是否可见
        rdc: 数据冗余份数, valid values: redundancy_2, redundancy_3, redundancy_4
        worm: WORM 配置 (Optional). parameter format: {
                worm_mode: WORM策略模式 (Optional). valid values: non_worm (Nonetype), enterprise_mode (企业级), compliance_mode (法规级),
                min_protect_period: 最小保护期 (可选, 0~4294967295, default0; 4294967295为无限期),
                min_protect_period_unit: 最小保留时间单位 (可选, defaultyear). valid values: day, year, month, hour, minute,
                max_protect_period: 最大保护期 (可选, 1~4294967295, default70; 4294967295为无限期),
                max_protect_period_unit: 最大保留时间单位 (可选, defaultyear). valid values: day, year, month, hour, minute, infinite,
                def_protect_period: default保护期 (可选, 0~4294967295, default70),
                def_protect_period_unit: default保留时间单位 (可选, defaultyear). valid values: day, year, month, hour, minute, infinite,
                auto_lock_enabled: WORM是否自动锁定 (可选, defaultfalse). valid values: true, false,
                auto_lock_time: 自动锁定时间 (可选, 1~64800, default2; 单位day时1~45, hour时1~1080, minute时1~64800),
                auto_lock_unit: 自动锁定时间单位 (可选, defaulthour). valid values: day, minute, hour,
                legal_hold_modify: 诉讼保留文件modify保留期开关 (可选, defaultfalse). valid values: true, false,
             }
        qos_policy: QoS 策略配置. parameter format: {
                qos_scale: 上限控制维度 (Required). valid values: namespace, client, account, user, innertask,
                name: QoS策略name (可选, 1~63字符, 正则^[a-zA-Z0-9][a-zA-Z0-9_-]*, 只能以数字或字母开头),
                qos_mode: QoS模式 (Required). valid values: by_usage (按已使用量), by_package (按固定capacity), manual (按上限),
                account_raw_id: 帐户在Storage device上的id (可选, 0~4294967293; 当qos_scale为namespace/account/user时必选),
                package_size: 包capacityGB (可选, 0~94371840; 当qos_mode为by_package时必选),
                max_iops: IOPS上限 (可选, 0~1073741824000; 批量createNamespace时为必选),
                max_mbps: 带宽上限Mbps (可选, 0~1073741824; 当qos_mode为manual时必选),
                max_band_width: max bandwidthMbps (可选, 1~1073741824; 当qos_mode为by_usage或by_package时必选),
                basic_band_width: 基础带宽Mbps (可选, 1~1073741824; 当qos_mode为by_usage或by_package时必选),
                bps_density: 带宽密度Mbps (可选, 1~1024000; 当qos_mode为by_usage或by_package时必选),
                max_conn_cluster: 最大连接数 (Optional),
                max_lock_cluster: 最大锁count (Optional),
                max_open_file_cluster: 最大打开文件count (Optional),
                read_ops: 读OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_ops: 写OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                read_mbps: 读带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_mbps: 写带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
             }
        public_network_qos_policy: 公网 QoS 策略配置. parameter format: {
                        name: QoS 策略name(Optional), 1~63 个字符, 正则 ^[a-zA-Z0-9][a-zA-Z0-9_-]*, 只能以数字或字母开头,
                        qos_mode: QoS 模式 (条件必选), valid values: by_usage (按已使用量)、by_package (按固定capacity)、manual (按上限); 批量createNamespace时为必选, modify时为非必选,
                        package_size: 包capacity(Optional), 0~94371840 (GB), 当 qos_mode 为 by_package 时必选,
                        max_iops: IOPS 上限 (条件必选), 0~1073741824000, 批量createNamespace时为必选, modify时为非必选,
                        max_mbps: 带宽上限(Optional), 0~1073741824 (Mbps), 当 qos_mode 为 manual 时必选,
                        max_band_width: max bandwidth(Optional), 1~1073741824 (Mbps), 当 qos_mode 为 by_usage 或 by_package 时必选,
                        basic_band_width: 基础带宽(Optional), 1~1073741824 (Mbps), 当 qos_mode 为 by_usage 或 by_package 时必选,
                bps_density: 带宽密度Mbps (可选, 1~1024000; 当qos_mode为by_usage或by_package时必选),
                max_conn_cluster: 最大连接数 (Optional),
                max_lock_cluster: 最大锁count (Optional),
                max_open_file_cluster: 最大打开文件count (Optional),
                read_ops: 读OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_ops: 写OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                read_mbps: 读带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_mbps: 写带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
             }
        private_network_qos_policy: 私网 QoS 策略配置. parameter format: {
                        name: QoS 策略name(Optional), 1~63 个字符, 正则 ^[a-zA-Z0-9][a-zA-Z0-9_-]*, 只能以数字或字母开头,
                        qos_mode: QoS 模式 (条件必选), valid values: by_usage (按已使用量)、by_package (按固定capacity)、manual (按上限); 批量createNamespace时为必选, modify时为非必选,
                        package_size: 包capacity(Optional), 0~94371840 (GB), 当 qos_mode 为 by_package 时必选,
                        max_iops: IOPS 上限 (条件必选), 0~1073741824000, 批量createNamespace时为必选, modify时为非必选,
                        max_mbps: 带宽上限(Optional), 0~1073741824 (Mbps), 当 qos_mode 为 manual 时必选,
                        max_band_width: max bandwidth(Optional), 1~1073741824 (Mbps), 当 qos_mode 为 by_usage 或 by_package 时必选,
                        basic_band_width: 基础带宽(Optional), 1~1073741824 (Mbps), 当 qos_mode 为 by_usage 或 by_package 时必选,
                bps_density: 带宽密度Mbps (可选, 1~1024000; 当qos_mode为by_usage或by_package时必选),
                max_conn_cluster: 最大连接数 (Optional),
                max_lock_cluster: 最大锁count (Optional),
                max_open_file_cluster: 最大打开文件count (Optional),
                read_ops: 读OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_ops: 写OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                read_mbps: 读带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_mbps: 写带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
             }
        create_s3_param: create S3 协议参数 (Optional). parameter format: {
                bucket_permission: 策略type (Required). valid values: private (私有), public_read_only (公共读), public_write_only (公共写), public_read_write (公共读写),
                version_status: object多versionstatus (可选, 0~2). valid values: 0 (false), 1 (打开), 2 (暂停),
             }
        application_type: 应用type, valid values: PACS (医疗影像场景), GENERAL (通用场景)
        task_remarks: 异步任务备注info
    
    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        } (异步任务 ID)
    """
    url = "/rest/fileservice/v1/namespaces"
    
    payload = {
        'storage_id': storage_id,
        'pool_raw_id': pool_raw_id
    }
    
    if namespace_specs is not None:
        payload['namespace_specs'] = namespace_specs
    if enable_update_atime is not None:
        payload['enable_update_atime'] = enable_update_atime
    if trash_visible is not None:
        payload['trash_visible'] = trash_visible
    if trash_enable is not None:
        payload['trash_enable'] = trash_enable
    if interval_trash is not None:
        payload['interval_trash'] = interval_trash
    if dps_switch is not None:
        payload['dps_switch'] = dps_switch
    if forbidden_dpc is not None:
        payload['forbidden_dpc'] = forbidden_dpc
    if audit_log_switch is not None:
        payload['audit_log_switch'] = audit_log_switch
    if audit_log_rule is not None:
        payload['audit_log_rule'] = audit_log_rule
    if atime_update_mode is not None:
        payload['atime_update_mode'] = atime_update_mode
    if acl_policy_type is not None:
        payload['acl_policy_type'] = acl_policy_type
    if enable_encrypt is not None:
        payload['enable_encrypt'] = enable_encrypt
    if crypt_alg is not None:
        payload['crypt_alg'] = crypt_alg
    if case_sensitive is not None:
        payload['case_sensitive'] = case_sensitive
    if show_snap_dir is not None:
        payload['show_snap_dir'] = show_snap_dir
    if rdc is not None:
        payload['rdc'] = rdc
    if worm is not None:
        payload['worm'] = worm
    if qos_policy is not None:
        payload['qos_policy'] = qos_policy
    if public_network_qos_policy is not None:
        payload['public_network_qos_policy'] = public_network_qos_policy
    if private_network_qos_policy is not None:
        payload['private_network_qos_policy'] = private_network_qos_policy
    if create_s3_param is not None:
        payload['create_s3_param'] = create_s3_param
    if application_type is not None:
        payload['application_type'] = application_type
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks
    
    response = client.post(url, body=payload)
    return response


def namespace_modify(client: DMEAPIClient, namespace_id: str,
           enable_update_atime: bool = None, show_snap_dir: bool = None,
           trash_visible: bool = None, trash_enable: bool = None,
           interval_trash: int = None, dps_switch: bool = None,
           forbidden_dpc: bool = None, audit_log_switch: bool = None,
           audit_log_rule: list = None, atime_update_mode: int = None,
           acl_policy_type: str = None, enable_encrypt: bool = None,
           qos_policy: dict = None, public_network_qos_policy: dict = None,
           private_network_qos_policy: dict = None,
           application_type: str = None, task_remarks: str = None) -> dict:
    """
    modify指定Namespace
    
    Args:
        client: DME API client
        namespace_id: Namespace ID (必选, 1~64 个字符)
        enable_update_atime: 是否更新 Atime, true: 更新; false: 不更新
        show_snap_dir: 快照目录是否可见, true: 可见; false: 不可见
        trash_visible: 回收站目录是否可见, true: 可见; false: 不可见, default不可见
        trash_enable: 回收站功能是否true, true: true; false: 不true, default不true
        interval_trash: 回收站保护时长 (分钟), 0 表示永久保留, 不自动delete, 最大 4294967295
        dps_switch: 元数据检索开关, true: true; false: false
        forbidden_dpc: 是否禁止 dpc 挂载, true: 禁止; false: 不禁止
        audit_log_switch: 是否true审计日志, 缺省false, true: true; false: false
        audit_log_rule: 审计日志规则list, valid values: open, create, read, write, close, delete, rename,
                       get_attr, set_attr, get_security, set_security, get_xattr, set_xattr,
                       list_dir, contact, mount_or_unmount, login_or_logoff
        atime_update_mode: atime 更新频率, 4294967295: false更新; 3600: 1 小时更新; 86400: 1 天更新
        acl_policy_type: Namespace安全模式, valid values: mixed (同时支持 UNIX 和 Windows 权限), 
                        unix (适用于 NFS 用户的权限由 Unix Mode/NFSv4 ACL 权限控制), 
                        native (与 Mixed 模式适用于相同的场景), 
                        ntfs (适用于 CIFS 用户的权限由 Windows NT ACL 权限控制)
        enable_encrypt: 是否true加密, true: true; false: false
        qos_policy: QoS 策略配置. parameter format: {
                qos_switch: QoS开关 (Required). valid values: on, off,
                name: QoS策略name (可选, 1~63字符, 正则^[a-zA-Z0-9][a-zA-Z0-9_-]*),
                qos_mode: QoS模式 (条件必选). valid values: by_usage (按已使用量), by_package (按固定capacity), manual (按上限),
                package_size: 包capacityGB (可选, 0~94371840; 当qos_mode为by_package时必选),
                max_iops: IOPS上限 (条件必选, 0~1073741824000),
                max_mbps: 带宽上限Mbps (可选, 0~1073741824; 当qos_mode为manual时必选),
                max_band_width: max bandwidthMbps (可选, 1~1073741824; 当qos_mode为by_usage或by_package时必选),
                basic_band_width: 基础带宽Mbps (可选, 1~1073741824; 当qos_mode为by_usage或by_package时必选),
                bps_density: 带宽密度Mbps (可选, 1~1024000; 当qos_mode为by_usage或by_package时必选),
                max_conn_cluster: 最大连接数 (Optional),
                max_lock_cluster: 最大锁count (Optional),
                max_open_file_cluster: 最大打开文件count (Optional),
                read_ops: 读OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_ops: 写OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                read_mbps: 读带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_mbps: 写带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
             }
        public_network_qos_policy: 公网 QoS 策略配置. parameter format: {
                        qos_switch: QoS 开关 (必填), valid values: on、off,
                        name: QoS 策略name(Optional), 1~63 个字符, 正则 ^[a-zA-Z0-9][a-zA-Z0-9_-]*, 只能以数字或字母开头,
                        qos_mode: QoS 模式 (条件必选), valid values: by_usage (按已使用量)、by_package (按固定capacity)、manual (按上限); 批量createNamespace时为必选, modify时为非必选,
                        package_size: 包capacity(Optional), 0~94371840 (GB), 当 qos_mode 为 by_package 时必选,
                        max_iops: IOPS 上限 (条件必选), 0~1073741824000, 批量createNamespace时为必选, modify时为非必选,
                        max_mbps: 带宽上限(Optional), 0~1073741824 (Mbps), 当 qos_mode 为 manual 时必选,
                        max_band_width: max bandwidth(Optional), 1~1073741824 (Mbps), 当 qos_mode 为 by_usage 或 by_package 时必选,
                        basic_band_width: 基础带宽(Optional), 1~1073741824 (Mbps), 当 qos_mode 为 by_usage 或 by_package 时必选,
                bps_density: 带宽密度Mbps (可选, 1~1024000; 当qos_mode为by_usage或by_package时必选),
                max_conn_cluster: 最大连接数 (Optional),
                max_lock_cluster: 最大锁count (Optional),
                max_open_file_cluster: 最大打开文件count (Optional),
                read_ops: 读OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_ops: 写OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                read_mbps: 读带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_mbps: 写带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
             }
        private_network_qos_policy: 私网 QoS 策略配置. parameter format: {
                        qos_switch: QoS 开关 (必填), valid values: on、off,
                        name: QoS 策略name(Optional), 1~63 个字符, 正则 ^[a-zA-Z0-9][a-zA-Z0-9_-]*, 只能以数字或字母开头,
                        qos_mode: QoS 模式 (条件必选), valid values: by_usage (按已使用量)、by_package (按固定capacity)、manual (按上限); 批量createNamespace时为必选, modify时为非必选,
                        package_size: 包capacity(Optional), 0~94371840 (GB), 当 qos_mode 为 by_package 时必选,
                        max_iops: IOPS 上限 (条件必选), 0~1073741824000, 批量createNamespace时为必选, modify时为非必选,
                        max_mbps: 带宽上限(Optional), 0~1073741824 (Mbps), 当 qos_mode 为 manual 时必选,
                        max_band_width: max bandwidth(Optional), 1~1073741824 (Mbps), 当 qos_mode 为 by_usage 或 by_package 时必选,
                        basic_band_width: 基础带宽(Optional), 1~1073741824 (Mbps), 当 qos_mode 为 by_usage 或 by_package 时必选,
                bps_density: 带宽密度Mbps (可选, 1~1024000; 当qos_mode为by_usage或by_package时必选),
                max_conn_cluster: 最大连接数 (Optional),
                max_lock_cluster: 最大锁count (Optional),
                max_open_file_cluster: 最大打开文件count (Optional),
                read_ops: 读OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_ops: 写OPS限制 (可选, 0~1073741824000; 仅当qos_mode为manual且qos_scale不为account时可选),
                read_mbps: 读带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
                write_mbps: 写带宽限制Mbps (可选, 0~1073741824; 仅当qos_mode为manual且qos_scale不为account时可选),
             }
        application_type: 应用type, valid values: PACS (医疗影像场景), GENERAL (通用场景)
        task_remarks: 异步任务备注info
    
    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        } (异步任务 ID)
    """
    url = "/rest/fileservice/v1/namespaces/{namespace_id}"
    
    payload = {}
    
    if enable_update_atime is not None:
        payload['enable_update_atime'] = enable_update_atime
    if show_snap_dir is not None:
        payload['show_snap_dir'] = show_snap_dir
    if trash_visible is not None:
        payload['trash_visible'] = trash_visible
    
    payload = {}
    
    if enable_update_atime is not None:
        payload['enable_update_atime'] = enable_update_atime
    if show_snap_dir is not None:
        payload['show_snap_dir'] = show_snap_dir
    if trash_visible is not None:
        payload['trash_visible'] = trash_visible
    if trash_enable is not None:
        payload['trash_enable'] = trash_enable
    if interval_trash is not None:
        payload['interval_trash'] = interval_trash
    if dps_switch is not None:
        payload['dps_switch'] = dps_switch
    if forbidden_dpc is not None:
        payload['forbidden_dpc'] = forbidden_dpc
    if audit_log_switch is not None:
        payload['audit_log_switch'] = audit_log_switch
    if audit_log_rule is not None:
        payload['audit_log_rule'] = audit_log_rule
    if atime_update_mode is not None:
        payload['atime_update_mode'] = atime_update_mode
    if acl_policy_type is not None:
        payload['acl_policy_type'] = acl_policy_type
    if enable_encrypt is not None:
        payload['enable_encrypt'] = enable_encrypt
    if qos_policy is not None:
        payload['qos_policy'] = qos_policy
    if public_network_qos_policy is not None:
        payload['public_network_qos_policy'] = public_network_qos_policy
    if private_network_qos_policy is not None:
        payload['private_network_qos_policy'] = private_network_qos_policy
    if application_type is not None:
        payload['application_type'] = application_type
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks
    
    response = client.put(url, body=payload, params={"namespace_id": namespace_id})
    return response


def namespace_delete(client: DMEAPIClient, namespace_ids: list, task_remarks: str = None) -> dict:
    """
    批量deleteNamespace
    
    Args:
        client: DME API client
        namespace_ids: Namespace ID list(Required), 数组最大 100 个, 最小 1 个
        task_remarks: 异步任务备注info (可选, 0~1024 个字符)
    
    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        } (异步任务 ID)
    """
    url = "/rest/fileservice/v1/namespaces/delete"
    
    payload = {
        'namespace_ids': namespace_ids
    }
    
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks
    
    response = client.post(url, body=payload)
    return response


def nfs_share_show_clients(client: DMEAPIClient, page_no: int = 1, page_size: int = 20,
                           nfs_share_id: str = None, storage_id: str = None,
                           vstore_id_in_storage: str = None, name: str = None,
                           client_id_in_storage: str = None, sort_key: str = None,
                           sort_dir: str = None) -> dict:
    """
    query NFS 共享下的客户端访问list

    指定设备或 NFS ID, query NFS 共享下的客户端访问list. 

    Args:
        client: DME API client
        page_no: pagination start page(Optional), 最小值 1, default 1
        page_size: 单页显示的count(Optional), 1~1000, default 20
        nfs_share_id: NFS 共享 ID(Optional), 1~64 个字符
        storage_id: Storage device ID(Optional), 1~64 个字符; 如果指定 nfs_share_id, 则此参数无效
        vstore_id_in_storage: vStore ID(Optional), 1~256 个字符; vStore 场景下必须下发
        name: 客户端 IP 或主机名或网络组名(Optional), 1~256 个字符; 指定 nfs_share_id 条件下支持模糊搜索
        client_id_in_storage: NFS 共享客户端 ID(Optional), 1~256 个字符
        sort_key: 排序字段(Optional), valid values: raw_id、name
        sort_dir: 排序方向(Optional), valid values: asc (升序)、desc (降序), default asc

    Returns:
        {
            total: 客户端count (int32),
            auth_client_list: 客户端访问list (List<AuthClientV2>). parameter format: [{
                client_id_in_storage: 客户端在设备的ID (string),
                nfs_share_id_in_storage: NFS共享在设备的ID (string),
                name: 客户端name (string),
                permission: 权限 (string),
                accesskrb5: Kerberos认证 (string),
            }, ...],
        }
    """
    url = "/rest/fileservice/v2/nfs-auth-clients/query"

    payload = {}

    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size
    if nfs_share_id is not None:
        payload['nfs_share_id'] = nfs_share_id
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if vstore_id_in_storage is not None:
        payload['vstore_id_in_storage'] = vstore_id_in_storage
    if name is not None:
        payload['name'] = name
    if client_id_in_storage is not None:
        payload['client_id_in_storage'] = client_id_in_storage
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def account_dataturbo_admin_list(client: DMEAPIClient, storage_id: str = None, vstore_id: str = None,
                   vstore_name: str = None, zone_id: str = None, name: str = None,
                   online_status: str = None, lock_status: str = None,
                   account_state: str = None, sort_key: str = None,
                   sort_dir: str = None, page_no: int = 1,
                   page_size: int = 20) -> dict:
    """
    批量query DataTurbo 管理员

    仅 OceanStor A800 系列存储支持. 

    Args:
        client: DME API client
        storage_id: 设备 ID (1~64个字符, 可选)
        vstore_id: 租户的 ID (1~64个字符, 可选)
        vstore_name: 租户的name, supports fuzzy query (1~256个字符, 可选)
        zone_id: 所属 zone 的 ID (1~64个字符, 可选). 当资源所属范围为全局时, zone ID 为所属设备的 Id; 当资源所属范围为本地时, zone ID 为所属 zone 的 ID. 仅 OceanStor A800 系列存储支持
        name: DataTurbo 管理员名, supports fuzzy query (1~256个字符, 可选)
        online_status: DataTurbo 管理员在线status (Optional). valid values: offline (离线), online (在线)
        lock_status: DataTurbo 管理员锁定status (Optional). valid values: unlocked (未锁定), locked (锁定)
        account_state: DataTurbo 管理员密码status (Optional). valid values: normal (正常), expired (密码过期), initial (用户密码处于初始化status, 需要modify), expiring_soon (密码即将到期), change_required (下一次登录必须modify密码), never (密码永不过期)
        sort_key: 按照指定字段排序 (Optional). valid values: create_time
        sort_dir: 指定排序方向 (Optional). valid values: asc (升序), desc (降序)
        page_no: pagination start page (int32, 最小值: 1, default值: 1, 可选)
        page_size: 单页显示的count (int32, 最小值: 1, 最大值: 1000, default值: 20, 可选)

    Returns:
        {
            total: 管理员count (integer),
            administrators: 管理员list (List<AdministratorQueryResp>). parameter format: [{
                id: 管理员ID (string),
                name: 管理员name (string),
                type: 管理员type (string),
            }, ...],
        }
    """
    url = "/rest/fileservice/v1/dpc-administrators/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if storage_id is not None:
        payload['storage_id'] = storage_id
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id
    if vstore_name is not None:
        payload['vstore_name'] = vstore_name
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if name is not None:
        payload['name'] = name
    if online_status is not None:
        payload['online_status'] = online_status
    if lock_status is not None:
        payload['lock_status'] = lock_status
    if account_state is not None:
        payload['account_state'] = account_state
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def account_unix_user_modify(client: DMEAPIClient, id: str, raw_id: int = None,
                              description: str = None, primary_group_name: str = None,
                              primary_group_raw_id: int = None,
                              status_enable: bool = None) -> dict:
    """
    modify UNIX 用户

    Args:
        client: DME API client
        id: UNIX 用户 ID (1~32个字符, 必填)
        raw_id: UNIX 用户在Storage device上的 ID (int64, 0~4294967294, 可选)
        description: UNIX 用户description (0~255个字符, 可选)
        primary_group_name: 用户主组name (1~64个字符, 可选. 与 primary_group_raw_id 都下发仅 primary_group_raw_id 生效)
        primary_group_raw_id: 用户主组 ID (int64, 0~4294967294, 可选. 与 primary_group_name 都下发仅 primary_group_raw_id 生效)
        status_enable: 用户status (boolean, 可选). valid values: true (启用), false (锁定). 仅 OceanStor Pacific 和 OceanStor A310 系列存储支持

    Returns:
        modifyresult
    """
    url = "/rest/fileservice/v1/unix-users/{id}"

    payload = {}

    if raw_id is not None:
        payload['raw_id'] = raw_id
    if description is not None:
        payload['description'] = description
    if primary_group_name is not None:
        payload['primary_group_name'] = primary_group_name

    payload = {}

    if raw_id is not None:
        payload['raw_id'] = raw_id
    if description is not None:
        payload['description'] = description
    if primary_group_name is not None:
        payload['primary_group_name'] = primary_group_name
    if primary_group_raw_id is not None:
        payload['primary_group_raw_id'] = primary_group_raw_id
    if status_enable is not None:
        payload['status_enable'] = status_enable

    response = client.put(url, body=payload, params={"id": id})
    return response


def account_unix_user_group_create(client: DMEAPIClient, storage_id: str, name: str,
                                    vstore_raw_id: str, raw_id: int = None,
                                    description: str = None,
                                    zone_id: str = None) -> dict:
    """
    create UNIX 用户组

    Args:
        client: DME API client
        storage_id: create UNIX 用户组storage设备 ID (1~64个字符, 必填)
        name: UNIX 用户组name (1~64个字符, 必填)
        raw_id: UNIX 用户组 ID (int64, 0~4294967294, 可选. OceanStor Pacific 和 OceanStor A310 存储必填)
        description: UNIX 用户组description (0~255个字符, 可选)
        vstore_raw_id: 用户所属租户在Storage device上的 ID (1~32个字符, 必填)
        zone_id: 所属 zone ID (1~64个字符, 可选. 仅 OceanStor A800 存储支持)

    Returns:
        createresult
    """
    url = "/rest/fileservice/v1/unix-user-groups"

    payload = {
        'storage_id': storage_id,
        'name': name,
        'vstore_raw_id': vstore_raw_id,
    }

    if raw_id is not None:
        payload['raw_id'] = raw_id
    if description is not None:
        payload['description'] = description
    if zone_id is not None:
        payload['zone_id'] = zone_id

    response = client.post(url, body=payload)
    return response


def account_unix_user_batch_delete(client: DMEAPIClient, ids: list) -> dict:
    """
    delete UNIX 用户

    Args:
        client: DME API client
        ids: UNIX 用户 ID list (List<string>, 数组最小成员个数: 1, max array members: 100, 必填)

    Returns:
        operation result
    """
    url = "/rest/fileservice/v1/unix-users/delete"

    payload = {
        'ids': ids,
    }

    response = client.post(url, body=payload)
    return response


def account_unix_user_group_list(client: DMEAPIClient, storage_id: str = None,
                                   storage_name: str = None,
                                   vstore_raw_id: str = None,
                                   vstore_name: str = None, name: str = None,
                                   raw_id: str = None, zone_id: str = None,
                                   sort_key: str = None, sort_dir: str = None,
                                   page_no: int = 1,
                                   page_size: int = 100) -> dict:
    """
    query UNIX 认证用户组list

    Args:
        client: DME API client
        page_no: 分页query的起始location (int32, 1~2147483647, default值: 1, 可选)
        page_size: 每页显示的count (int32, 10~100, default值: 100, 可选)
        storage_name: 设备name, supports fuzzy match过滤 (1~256个字符, 可选)
        vstore_raw_id: 所属租户在Storage device上的 ID (1~64个字符, 可选)
        vstore_name: 所属租户name, 支持模糊搜索过滤 (1~256个字符, 可选)
        name: 用户组name, 支持模糊搜索过滤 (1~256个字符, 可选)
        raw_id: 用户组在Storage device上的 ID (1~256个字符, 可选)
        zone_id: zone ID (1~64个字符, 可选). 仅 OceanStor A800 存储下的认证用户组支持通过该字段过滤
        sort_key: 按照指定字段排序 (Optional). valid values: name (用户组名), raw_id (用户组在Storage device上的 ID), create_time (creation time). default值: create_time
        storage_id: Storage device ID (1~36个字符, 可选)
        sort_dir: 指定排序方向 (Optional). valid values: asc (升序), desc (降序). default值: desc

    Returns:
        {
            total: 用户组count (int32),
            groups: UNIX认证用户组list (List<UnixUserGroup>). parameter format: [{
                id: 用户组ID (string),
                name: 用户组名 (string),
                gid: 组GID (int32),
            }, ...],
        }
    """
    url = "/rest/fileservice/v1/unix-user-groups/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size,
    }

    if storage_name is not None:
        payload['storage_name'] = storage_name
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if vstore_name is not None:
        payload['vstore_name'] = vstore_name
    if name is not None:
        payload['name'] = name
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def account_unix_user_group_show(client: DMEAPIClient, id: str) -> dict:
    """
    query UNIX 用户组details

    Args:
        client: DME API client
        id: 用户组 ID (1~32个字符, 必填)

    Returns:
        {
            id: 用户组ID (string),
            name: 用户组名 (string),
            gid: 组GID (int32),
            description: description (string),
        }
    """
    url = "/rest/fileservice/v1/unix-user-groups/{id}"

    response = client.get(url, params={"id": id})
    return response


def account_unix_user_group_modify(client: DMEAPIClient, id: str,
                                    raw_id: int = None,
                                    description: str = None) -> dict:
    """
    modify UNIX 用户组

    Args:
        client: DME API client
        id: UNIX 用户组 ID (1~32个字符, 必填)
        raw_id: UNIX 用户组在Storage device上的 ID (int64, 0~4294967294, 可选)
        description: UNIX 用户组description (0~255个字符, 可选)

    Returns:
        modifyresult
    """
    url = "/rest/fileservice/v1/unix-user-groups/{id}"

    payload = {}

    if raw_id is not None:
        payload['raw_id'] = raw_id
    if description is not None:
        payload['description'] = description

    response = client.put(url, body=payload, params={"id": id})
    return response


def account_unix_user_group_batch_delete(client: DMEAPIClient, ids: list) -> dict:
    """
    delete UNIX 用户组

    Args:
        client: DME API client
        ids: UNIX 用户组的 ID list (List<string>, 数组最小成员个数: 1, max array members: 100, 必填)

    Returns:
        operation result
    """
    url = "/rest/fileservice/v1/unix-user-groups/delete"

    payload = {
        'ids': ids,
    }

    response = client.post(url, body=payload)
    return response


def account_unix_user_remove_group(client: DMEAPIClient, user_id: str,
                                    secondary_group_name_list: list) -> dict:
    """
    移除 UNIX 用户附属组

    Args:
        client: DME API client
        user_id: UNIX 用户 ID (1~32个字符, 必填)
        secondary_group_name_list: 附属组namelist (List<string>, 数组最小成员个数: 1, max array members: 100, 必填)

    Returns:
        operation result
    """
    url = "/rest/fileservice/v1/unix-users/{user_id}/remove-secondary-group"

    payload = {
        'secondary_group_name_list': secondary_group_name_list,
    }

    response = client.post(url, body=payload, params={"user_id": user_id})
    return response


def account_unix_user_show(client: DMEAPIClient, id: str) -> dict:
    """
    query UNIX 认证用户details

    Args:
        client: DME API client
        id: 用户 ID (1~32个字符, 必填)

    Returns:
        {
            id: user ID (string),
            name: 用户名 (string),
            uid: 用户UID (int32),
            primary_group_name: 主组name (string),
            description: description (string),
        }
    """
    url = "/rest/fileservice/v1/unix-users/{id}"

    response = client.get(url, params={"id": id})
    return response


def account_unix_user_list(client: DMEAPIClient, storage_id: str = None,
                             storage_name: str = None, vstore_raw_id: str = None,
                             vstore_name: str = None, name: str = None,
                             primary_group_name: str = None, raw_id: str = None,
                             zone_id: str = None, user_status: str = None,
                             sort_key: str = None, sort_dir: str = None,
                             page_no: int = 1, page_size: int = 100) -> dict:
    """
    query UNIX 认证用户list

    Args:
        client: DME API client
        page_no: 分页query的起始location (int32, 1~2147483647, default值: 1, 可选)
        page_size: 每页显示的count (int32, 10~100, default值: 100, 可选)
        storage_name: 设备name, 支持模糊搜索过滤 (1~256个字符, 可选)
        vstore_raw_id: 所属租户在Storage device上的 ID (1~64个字符, 可选)
        vstore_name: 所属租户name, 支持模糊搜索过滤 (1~256个字符, 可选)
        name: username, 支持模糊搜索过滤 (1~256个字符, 可选)
        primary_group_name: 主组name, 支持模糊搜索过滤 (1~256个字符, 可选)
        raw_id: 用户在Storage device上的 ID (1~255个字符, 可选)
        zone_id: zone ID (1~64个字符, 可选). 仅 OceanStor A800 存储下的认证用户支持通过该字段过滤
        user_status: 用户status (Optional). valid values: enable (启用), disable (禁用)
        sort_key: 按照指定字段排序 (Optional). valid values: name (用户名), raw_id (用户在Storage device上的 ID), primary_group_name (主组名), create_time (creation time). default值: create_time
        storage_id: Storage device ID (1~36个字符, 可选)
        sort_dir: 指定排序方向 (Optional). valid values: asc (升序), desc (降序). default值: desc

    Returns:
        {
            total: 用户count (int32),
            users: UNIX认证用户list (List<UnixUser>). parameter format: [{
                id: user ID (string),
                name: 用户名 (string),
                uid: 用户UID (int32),
                primary_group_name: 主组name (string),
            }, ...],
        }
    """
    url = "/rest/fileservice/v1/unix-users/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size,
    }

    if storage_name is not None:
        payload['storage_name'] = storage_name
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if vstore_name is not None:
        payload['vstore_name'] = vstore_name
    if name is not None:
        payload['name'] = name
    if primary_group_name is not None:
        payload['primary_group_name'] = primary_group_name
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if user_status is not None:
        payload['user_status'] = user_status
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def account_unix_user_add_group(client: DMEAPIClient, user_id: str,
                                 secondary_group_name_list: list) -> dict:
    """
    添加 UNIX 用户附属组

    Args:
        client: DME API client
        user_id: UNIX 用户 ID (1~32个字符, 必填)
        secondary_group_name_list: 附属组namelist (List<string>, 数组最小成员个数: 1, max array members: 100, 必填)

    Returns:
        operation result
    """
    url = "/rest/fileservice/v1/unix-users/{user_id}/add-secondary-group"

    payload = {
        'secondary_group_name_list': secondary_group_name_list,
    }

    response = client.post(url, body=payload, params={"user_id": user_id})
    return response


def account_unix_user_create(client: DMEAPIClient, storage_id: str, name: str, vstore_raw_id: str,
                              raw_id: int = None, description: str = None,
                              primary_group_raw_id: int = None,
                              primary_group_name: str = None, zone_id: str = None,
                              status: bool = None,
                              secondary_group_name_list: list = None) -> dict:
    """
    create UNIX 用户

    Args:
        client: DME API client
        storage_id: create UNIX 用户storage设备 ID (1~64个字符, 必填)
        name: UNIX username (1~64个字符, 必填)
        raw_id: UNIX 用户 ID (int64, 0~4294967294, 可选. OceanStor Pacific 和 OceanStor A310 存储必填)
        description: UNIX 用户description (0~255个字符, 可选)
        primary_group_raw_id: 用户主组 ID (int64, 0~4294967294, 可选. 与 primary_group_name 至少下发一个, 若都下发仅 primary_group_name 生效)
        primary_group_name: 用户所归属的主组name (1~64个字符, 可选. 与 primary_group_raw_id 至少下发一个, 若都下发仅 primary_group_name 生效)
        vstore_raw_id: 用户所属租户在Storage device上的 ID (1~32个字符, 必填)
        zone_id: 所属 zone ID (1~64个字符, 可选. 仅 OceanStor A800 存储支持)
        status: 用户status (boolean, 可选. default值: true). valid values: true (启用), false (锁定). 仅 OceanStor Pacific 和 OceanStor A310 系列存储支持
        secondary_group_name_list: 用户附属组namelist (List<string>, 数组最小成员个数: 0, max array members: 100, 可选)

    Returns:
        createresult
    """
    url = "/rest/fileservice/v1/unix-users"

    payload = {
        'storage_id': storage_id,
        'name': name,
        'vstore_raw_id': vstore_raw_id,
    }

    if raw_id is not None:
        payload['raw_id'] = raw_id
    if description is not None:
        payload['description'] = description
    if primary_group_raw_id is not None:
        payload['primary_group_raw_id'] = primary_group_raw_id
    if primary_group_name is not None:
        payload['primary_group_name'] = primary_group_name
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if status is not None:
        payload['status'] = status
    if secondary_group_name_list is not None:
        payload['secondary_group_name_list'] = secondary_group_name_list

    response = client.post(url, body=payload)
    return response


def kvcache_batch_create(client: DMEAPIClient, storage_id: str, zone_id: str,
                          pool_raw_id: str, vstore_id: str, kv_cache_stores: list,
                          data_cleanup_switch: str = None,
                          max_survival_time: int = None) -> dict:
    """
    批量create KV Cache 库

    Args:
        client: DME API client
        storage_id: Storage device ID (长度为36个字符, 必填)
        zone_id: 所属 zone 的 ID (长度为36个字符, 必填)
        pool_raw_id: Storage pool在所属 zone 上的 ID (1~64个字符, 必填)
        vstore_id: 租户 ID (长度为32个字符, 必填)
        data_cleanup_switch: 清理开关 (Optional). valid values: on (打开), off (false). default值: off
        max_survival_time: KV Cache 最长存活时间 (int32, 1~3650, 可选. 当 data_cleanup_switch 为 on 时必填)
        kv_cache_stores: KV Cache 库list (List<CreateKVCacheStoreBaseInfo>, 数组最小成员个数: 1, max array members: 100, 必填). parameter format: [{
                name: KV Cache 库name (1~255个字符, 必填),
                capacity: KV Cache 库capacity (int64, 20971520~70368744177664, 单位: 扇区数, 1扇区=512字节, 必填),
                description: descriptioninfo (1~255个字符, 可选),
                count: 批量create KV Cache 库的count (int32, 1~100, default值: 1, 可选),
                start_suffix: 起始后缀编号 (int32, 0~9999, 可选. 起始后缀编号+KV Cache库count<=9999),
             }, ...]

    Returns:
        createresult
    """
    url = "/rest/kvcachemgmt/v1/kv-cache-stores"

    payload = {
        'storage_id': storage_id,
        'zone_id': zone_id,
        'pool_raw_id': pool_raw_id,
        'vstore_id': vstore_id,
        'kv_cache_stores': kv_cache_stores,
    }

    if data_cleanup_switch is not None:
        payload['data_cleanup_switch'] = data_cleanup_switch
    if max_survival_time is not None:
        payload['max_survival_time'] = max_survival_time

    response = client.post(url, body=payload)
    return response


def kvcache_modify(client: DMEAPIClient, kv_cache_stores_id: str, name: str = None,
                    description: str = None, data_cleanup_switch: str = None,
                    max_survival_time: int = None) -> dict:
    """
    modify KV Cache 库

    Args:
        client: DME API client
        kv_cache_stores_id: KV Cache 库 ID (1~64个字符, 必填)
        name: KV Cache 库name (1~255个字符, 可选)
        description: descriptioninfo (0~255个字符, 可选)
        data_cleanup_switch: 清理开关 (Optional). valid values: on (打开), off (false). default值: off
        max_survival_time: KV Cache 最长存活时间 (int32, 1~3650, 可选. 当 data_cleanup_switch 为 on 时必填)

    Returns:
        modifyresult
    """
    url = "/rest/kvcachemgmt/v1/kv-cache-stores/{kv_cache_stores_id}"

    payload = {}

    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description
    if data_cleanup_switch is not None:
        payload['data_cleanup_switch'] = data_cleanup_switch

    payload = {}

    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description
    if data_cleanup_switch is not None:
        payload['data_cleanup_switch'] = data_cleanup_switch
    if max_survival_time is not None:
        payload['max_survival_time'] = max_survival_time

    response = client.put(url, body=payload, params={"kv_cache_stores_id": kv_cache_stores_id})
    return response


def kvcache_batch_delete(client: DMEAPIClient, ids: list) -> dict:
    """
    批量delete KV Cache 库

    Args:
        client: DME API client
        ids: KV Cache 库 ID list (List<string>, 数组最小成员个数: 1, max array members: 100, 必填)

    Returns:
        operation result
    """
    url = "/rest/kvcachemgmt/v1/kv-cache-stores/delete"

    payload = {
        'ids': ids,
    }

    response = client.post(url, body=payload)
    return response


def kvcache_list(client: DMEAPIClient, storage_id: str = None, id: str = None,
                  raw_id: str = None, name: str = None, zone_id: str = None,
                  pool_raw_id: str = None, vstore_id: str = None,
                  vstore_name: str = None, fs_id: str = None,
                  fs_name: str = None, data_cleanup_switch: str = None,
                  page_no: int = 1, page_size: int = 20,
                  sort_dir: str = None, sort_key: str = None) -> dict:
    """
    query KV Cache 库

    Args:
        client: DME API client
        storage_id: Storage device ID (长度为36个字符, 可选)
        id: KV Cache 库 ID (长度为32个字符, 可选)
        raw_id: KV Cache 库在 zone 上的 ID (1~256个字符, 可选)
        name: KV Cache 库name (1~256个字符, 可选)
        zone_id: 所属 zone 的 ID (长度为36个字符, 可选)
        pool_raw_id: Storage pool在所属 zone 上的 ID (1~64个字符, 可选)
        vstore_id: 租户 ID (长度为32个字符, 可选)
        vstore_name: 租户name (1~256个字符, 可选)
        fs_id: Filesystem ID (长度为32个字符, 可选)
        fs_name: Filesystemname (1~256个字符, 可选)
        data_cleanup_switch: 清理开关 (Optional). valid values: on (打开), off (false)
        page_no: 分页页码 (int32, 1~10000, default值: 1, 可选)
        page_size: 每页数据条数 (int32, 1~100, default值: 20, 可选)
        sort_dir: 指定排序方向 (Optional). valid values: asc (升序), desc (降序). default值: asc
        sort_key: 排序参数 (Optional). valid values: capacity (total capacity), used_capacity (used capacity), used_tokens (已使用的 token count), hit_ratio (命中率)

    Returns:
        {
            total: KV Cache库count (int32),
            kv_cache_stores: KV Cache库list (List<KVCacheStore>). parameter format: [{
                id: 库ID (string),
                name: 库name (string),
                status: status (string),
                capacity: capacity (string),
            }, ...],
        }
    """
    url = "/rest/kvcachemgmt/v1/kv-cache-stores/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size,
    }

    if storage_id is not None:
        payload['storage_id'] = storage_id
    if id is not None:
        payload['id'] = id
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if name is not None:
        payload['name'] = name
    if zone_id is not None:
        payload['zone_id'] = zone_id
    if pool_raw_id is not None:
        payload['pool_raw_id'] = pool_raw_id
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id
    if vstore_name is not None:
        payload['vstore_name'] = vstore_name
    if fs_id is not None:
        payload['fs_id'] = fs_id
    if fs_name is not None:
        payload['fs_name'] = fs_name
    if data_cleanup_switch is not None:
        payload['data_cleanup_switch'] = data_cleanup_switch
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if sort_key is not None:
        payload['sort_key'] = sort_key

    response = client.post(url, body=payload)
    return response


ACTIONS = {
    'account_dataturbo_admin_list': {
        'func': account_dataturbo_admin_list,
        'description': '批量查询 DataTurbo 管理员',
        'params': ['storage_id', 'vstore_id', 'vstore_name', 'zone_id', 'name', 'online_status', 'lock_status', 'account_state', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_unix_user_create': {
        'func': account_unix_user_create,
        'description': '创建 UNIX 用户',
        'params': ['storage_id', 'name', 'vstore_raw_id', 'raw_id', 'description', 'primary_group_raw_id', 'primary_group_name', 'zone_id', 'status', 'secondary_group_name_list'],
        'subtopic': 'account'
    },
    'account_unix_user_add_group': {
        'func': account_unix_user_add_group,
        'description': '添加 UNIX 用户附属组',
        'params': ['user_id', 'secondary_group_name_list'],
        'subtopic': 'account'
    },
    'account_unix_user_list': {
        'func': account_unix_user_list,
        'description': '查询 UNIX 认证用户列表',
        'params': ['storage_id', 'storage_name', 'vstore_raw_id', 'vstore_name', 'name', 'primary_group_name', 'raw_id', 'zone_id', 'user_status', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_unix_user_show': {
        'func': account_unix_user_show,
        'description': '查询 UNIX 认证用户详情',
        'params': ['id'],
        'subtopic': 'account'
    },
    'account_unix_user_remove_group': {
        'func': account_unix_user_remove_group,
        'description': '移除 UNIX 用户附属组',
        'params': ['user_id', 'secondary_group_name_list'],
        'subtopic': 'account'
    },
    'account_unix_user_modify': {
        'func': account_unix_user_modify,
        'description': '修改 UNIX 用户',
        'params': ['id', 'raw_id', 'description', 'primary_group_name', 'primary_group_raw_id', 'status_enable'],
        'subtopic': 'account'
    },
    'account_unix_user_batch_delete': {
        'func': account_unix_user_batch_delete,
        'description': '删除 UNIX 用户',
        'params': ['ids'],
        'subtopic': 'account'
    },
    'account_unix_user_group_create': {
        'func': account_unix_user_group_create,
        'description': '创建 UNIX 用户组',
        'params': ['storage_id', 'name', 'vstore_raw_id', 'raw_id', 'description', 'zone_id'],
        'subtopic': 'account'
    },
    'account_unix_user_group_list': {
        'func': account_unix_user_group_list,
        'description': '查询 UNIX 认证用户组列表',
        'params': ['storage_id', 'storage_name', 'vstore_raw_id', 'vstore_name', 'name', 'raw_id', 'zone_id', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'account'
    },
    'account_unix_user_group_show': {
        'func': account_unix_user_group_show,
        'description': '查询 UNIX 用户组详情',
        'params': ['id'],
        'subtopic': 'account'
    },
    'account_unix_user_group_modify': {
        'func': account_unix_user_group_modify,
        'description': '修改 UNIX 用户组',
        'params': ['id', 'raw_id', 'description'],
        'subtopic': 'account'
    },
    'account_unix_user_group_batch_delete': {
        'func': account_unix_user_group_batch_delete,
        'description': '删除 UNIX 用户组',
        'params': ['ids'],
        'subtopic': 'account'
    },
    'dtree_list': {
        'func': dtree_list,
        'description': '查询 Dtree 列表',
        'params': ['id_in_storage', 'name', 'device_name', 'storage_id', 'zone_id', 'manufacturer', 'tier_name', 'fs_name', 'fs_id', 'namespace_name', 'namespace_id', 'quota_switch', 'security_mode', 'nas_locking_policy', 'sort_key', 'sort_dir', 'page_no', 'page_size', 'dc_id', 'dc_name'],
        'subtopic': 'dtree'
    },
    'dtree_show': {
        'func': dtree_show,
        'description': '查询指定 Dtree 详情',
        'params': ['dtree_id'],
        'subtopic': 'dtree'
    },
    'dtree_create': {
        'func': dtree_create,
        'description': '创建并共享 Dtree',
        'params': ['storage_id', 'create_dtrees_param', 'fs_id', 'namespace_id', 'zone_id', 'parent_dir', 'quota_switch', 'security_mode', 'nas_locking_policy', 'create_nfs_share_param', 'create_cifs_share_param', 'dataturbo_share', 'create_worm_param', 'unix_permissions', 'task_remarks'],
        'subtopic': 'dtree'
    },
    'dtree_delete': {
        'func': dtree_delete,
        'description': '批量删除 Dtree',
        'params': ['dtree_ids', 'task_remarks'],
        'subtopic': 'dtree'
    },
    'dtree_modify': {
        'func': dtree_modify,
        'description': '修改指定 Dtree',
        'params': ['dtree_id', 'name', 'quota_switch', 'security_mode', 'nas_locking_policy', 'unix_permissions', 'task_remarks'],
        'subtopic': 'dtree'
    },
    # NFS share subtopic action
    'nfs_share_list': {
        'func': nfs_share_list,
        'description': '查询 NFS 共享列表',
        'params': ['id_in_storage', 'name', 'share_path', 'exact_share_path', 'device_name', 'storage_id', 'tier_name', 'owning_dtree_name', 'fs_name', 'fs_id', 'owning_dtree_id', 'vstore_name', 'page_no', 'page_size', 'sort_key', 'sort_dir', 'support_provisioning', 'namespace_id', 'namespace_name', 'dc_id', 'dc_name', 'zone_id', 'zone_name', 'zone_ip'],
        'subtopic': 'nfs_share'
    },
    'nfs_share_show': {
        'func': nfs_share_show,
        'description': '查询指定 NFS 共享详情',
        'params': ['nfs_share_id'],
        'subtopic': 'nfs_share'
    },
    'nfs_share_create': {
        'func': nfs_share_create,
        'description': '创建 NFS 共享',
        'params': ['create_nfs_share_param', 'task_remarks'],
        'subtopic': 'nfs_share'
    },
    'nfs_share_modify': {
        'func': nfs_share_modify,
        'description': '修改指定 NFS 共享',
        'params': ['nfs_share_id', 'description', 'character_encoding', 'audit_items', 'show_snapshot_enable', 'nfs_share_client_addition', 'nfs_share_client_modification', 'nfs_share_client_deletion', 'file_name_ex_filters', 'task_remarks'],
        'subtopic': 'nfs_share'
    },
    'nfs_share_delete': {
        'func': nfs_share_delete,
        'description': '批量删除 NFS 共享',
        'params': ['nfs_share_ids', 'task_remarks'],
        'subtopic': 'nfs_share'
    },
    'nfs_share_show_clients': {
        'func': nfs_share_show_clients,
        'description': '查询 NFS 共享下的客户端访问列表',
        'params': ['page_no', 'page_size', 'nfs_share_id', 'storage_id', 'vstore_id_in_storage', 'name', 'client_id_in_storage', 'sort_key', 'sort_dir'],
        'subtopic': 'nfs_share'
    },
    # CIFS 共享subtopic action
    'cifs_share_list': {
        'func': cifs_share_list,
        'description': '批量查询 CIFS 共享',
        'params': ['raw_id', 'name', 'share_path', 'exact_share_path', 'fs_id', 'fs_name', 'dtree_id', 'dtree_name', 'storage_id', 'storage_name', 'vstore_raw_id', 'vstore_name', 'manufacturer', 'op_lock_enabled', 'notify_enabled', 'offline_file_modes', 'file_extension_filter_enabled', 'abe_enabled', 'page_no', 'page_size', 'sort_key', 'sort_dir', 'namespace_id', 'namespace_name', 'support_provisioning', 'dc_id', 'dc_name'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_show': {
        'func': cifs_share_show,
        'description': '查询指定 CIFS 共享详情',
        'params': ['cifs_share_id'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_create': {
        'func': cifs_share_create,
        'description': '创建单个 CIFS 共享',
        'params': ['create_cifs_param', 'fs_id', 'namespace_id', 'task_remarks'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_modify': {
        'func': cifs_share_modify,
        'description': '修改指定 CIFS 共享',
        'params': ['cifs_share_id', 'description', 'op_lock_enabled', 'notify_enabled', 'ca_enabled', 'offline_file_mode', 'ip_control_enabled', 'abe_enabled', 'audititem_list', 'apply_default_acl', 'file_extension_filter_enabled', 'show_previous_versions_enabled', 'show_snapshot_enabled', 'user_and_user_group_info', 'ip_and_segments', 'file_name_ex_filters', 'task_remarks', 'smb3_encryption_enable', 'unencrypted_access', 'enable_lease'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_delete': {
        'func': cifs_share_delete,
        'description': '批量删除 CIFS 共享',
        'params': ['cifs_share_ids', 'task_remarks'],
        'subtopic': 'cifs_share'
    },
    'cifs_share_show_permissions': {
        'func': cifs_share_show_permissions,
        'description': '查询单个 CIFS 共享的权限列表（用户/IP/文件过滤）',
        'params': ['cifs_share_id', 'type', 'user_filter', 'ip_filter', 'file_filter', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'cifs_share'
    },
    # dataturbo_share subtopic action
    'dataturbo_share_list': {
        'func': dataturbo_share_list,
        'description': '查询 DataTurbo 共享列表',
        'params': ['page_no', 'page_size', 'raw_id', 'share_path', 'fs_id', 'fs_name', 'dtree_id', 'dtree_name', 'vstore_id', 'vstore_raw_id', 'vstore_name', 'storage_id', 'storage_name', 'zone_id', 'zone_name', 'scope', 'sort_key', 'sort_dir'],
        'subtopic': 'dataturbo_share'
    },
    'dataturbo_share_show': {
        'func': dataturbo_share_show,
        'description': '查询指定 DataTurbo 共享详情',
        'params': ['dataturbo_share_id'],
        'subtopic': 'dataturbo_share'
    },
    'dataturbo_share_create': {
        'func': dataturbo_share_create,
        'description': '创建 DataTurbo 共享',
        'params': ['charset', 'fs_id', 'dtree_id', 'description', 'dataturbo_share_auth', 'task_remarks'],
        'subtopic': 'dataturbo_share'
    },
    'dataturbo_share_modify': {
        'func': dataturbo_share_modify,
        'description': '修改指定 DataTurbo 共享',
        'params': ['dataturbo_share_id', 'description', 'dataturbo_share_auth_addition', 'dataturbo_share_auth_deletion', 'task_remarks'],
        'subtopic': 'dataturbo_share'
    },
    'dataturbo_share_delete': {
        'func': dataturbo_share_delete,
        'description': '批量删除 DataTurbo 共享',
        'params': ['dataturbo_share_ids', 'task_remarks'],
        'subtopic': 'dataturbo_share'
    },
    'dataturbo_share_show_permissions': {
        'func': dataturbo_share_show_permissions,
        'description': '查询 DataTurbo 共享管理员权限列表',
        'params': ['dataturbo_share_id', 'page_no', 'page_size', 'user_id', 'user_name', 'permission'],
        'subtopic': 'dataturbo_share'
    },
    # quota subtopic action
    'quota_list': {
        'func': quota_list,
        'description': '查询配额列表',
        'params': ['page_no', 'page_size', 'ids', 'raw_ids', 'quota_type', 'parent_type', 'parent_raw_id', 'owner_name', 'vstore_id', 'vstore_raw_id', 'storage_id', 'sort_key', 'sort_dir', 'zone_id'],
        'subtopic': 'quota'
    },
    'quota_show': {
        'func': quota_show,
        'description': '查询指定配额详情',
        'params': ['quota_id'],
        'subtopic': 'quota'
    },
    'quota_create': {
        'func': quota_create,
        'description': '创建配额',
        'params': ['parent_id', 'parent_type', 'quota_type', 'space_soft_quota', 'space_hard_quota', 'space_advisory_quota', 'file_soft_quota', 'file_hard_quota', 'file_advisory_quota', 'snap_space_switch', 'soft_grace_time', 'quota_owner', 'dir_quota_target', 'task_remarks'],
        'subtopic': 'quota'
    },
    'quota_modify': {
        'func': quota_modify,
        'description': '更新指定配额',
        'params': ['quota_id', 'space_soft_quota', 'space_hard_quota', 'space_advisory_quota', 'file_soft_quota', 'file_hard_quota', 'file_advisory_quota', 'snap_space_switch', 'soft_grace_time', 'task_remarks'],
        'subtopic': 'quota'
    },
    'quota_delete': {
        'func': quota_delete,
        'description': '批量删除配额',
        'params': ['quota_ids', 'task_remarks'],
        'subtopic': 'quota'
    },
    # filesystem subtopic action
    'filesystem_list': {
        'func': filesystem_list,
        'description': '批量查询文件系统',
        'params': ['page_no', 'page_size', 'sort_dir', 'sort_key', 'name', 'fs_raw_id', 'storage_id'],
        'subtopic': 'filesystem'
    },
    'filesystem_show': {
        'func': filesystem_show,
        'description': '查询指定文件系统详情',
        'params': ['filesystem_id'],
        'subtopic': 'filesystem'
    },
    'filesystem_delete': {
        'func': filesystem_delete,
        'description': '批量删除文件系统',
        'params': ['filesystem_ids', 'task_remarks'],
        'subtopic': 'filesystem'
    },
    'filesystem_batch_modify': {
        'func': filesystem_batch_modify,
        'description': '批量修改文件系统（支持批量修改名称）',
        'params': ['filesystems', 'task_remarks'],
        'subtopic': 'filesystem'
    },
    'filesystem_create': {
        'func': filesystem_create,
        'description': '自定义创建文件系统',
        'params': ['storage_id', 'pool_raw_id', 'filesystem_specs', 'vstore_id', 'zone_id', 'task_remarks', 'gfs_group_id', 'automatic_update_time', 'atime_update_mode', 'schedule_name', 'quota_switch', 'vaai_switch', 'initial_distribute_policy', 'capacity_threshold'],
        'subtopic': 'filesystem'
    },
    'filesystem_query_available': {
        'func': filesystem_query_available,
        'description': '查询可用的文件系统（支持远程复制）',
        'params': ['feature_type', 'local_storage_id', 'remote_storage_id', 'name', 'page_no', 'page_size', 'sort_key', 'sort_dir'],
        'subtopic': 'filesystem'
    },
    'filesystem_modify': {
        'func': filesystem_modify,
        'description': '修改指定文件系统（完整参数）',
        'params': ['file_system_id', 'name', 'description', 'capacity', 'capacity_threshold', 'initial_distribute_policy', 'automatic_update_time', 'atime_update_mode', 'quota_switch', 'vaai_switch', 'owning_controller', 'task_remarks'],
        'subtopic': 'filesystem'
    },
    # namespace subtopic action
    'namespace_list': {
        'func': namespace_list,
        'description': '批量查询命名空间',
        'params': ['page_no', 'page_size', 'sort_dir', 'sort_key', 'name', 
                   'vstore_name', 'vstore_raw_id', 'vstore_id', 'raw_id',
                   'pool_name', 'storage_id', 'enable_encrypt', 
                   'support_provisioning', 'gfs_id', 'gfs_name', 'has_gfs'],
        'subtopic': 'namespace'
    },
    'namespace_show': {
        'func': namespace_show,
        'description': '查询指定命名空间详情',
        'params': ['namespace_id'],
        'subtopic': 'namespace'
    },
    'namespace_create': {
        'func': namespace_create,
        'description': '批量创建命名空间',
        'params': ['storage_id', 'pool_raw_id', 'namespace_specs', 
                   'enable_update_atime', 'trash_visible', 'trash_enable',
                   'interval_trash', 'dps_switch', 'forbidden_dpc',
                   'audit_log_switch', 'audit_log_rule', 'atime_update_mode',
                   'acl_policy_type', 'enable_encrypt', 'crypt_alg',
                   'case_sensitive', 'show_snap_dir', 'rdc', 'worm',
                   'qos_policy', 'public_network_qos_policy',
                   'private_network_qos_policy', 'create_s3_param',
                   'application_type', 'task_remarks'],
        'subtopic': 'namespace'
    },
    'namespace_modify': {
        'func': namespace_modify,
        'description': '修改指定命名空间',
        'params': ['namespace_id', 'enable_update_atime', 'show_snap_dir',
                   'trash_visible', 'trash_enable', 'interval_trash',
                   'dps_switch', 'forbidden_dpc', 'audit_log_switch',
                   'audit_log_rule', 'atime_update_mode', 'acl_policy_type',
                   'enable_encrypt', 'qos_policy', 'public_network_qos_policy',
                   'private_network_qos_policy', 'application_type', 'task_remarks'],
        'subtopic': 'namespace'
    },
    'namespace_delete': {
        'func': namespace_delete,
        'description': '批量删除命名空间',
        'params': ['namespace_ids', 'task_remarks'],
        'subtopic': 'namespace'
    },
    # dataturbo subtopic action (原 dpc 子主题, 重命名)
    'dpc_list': {
        'func': dpc_list,
        'description': '批量查询并行客户端列表',
        'params': ['ids', 'hostname', 'ip', 'mgmt_status', 'status', 'sn', 'storage_id', 'dpc_om_id', 'dpc_type', 'client_version', 'page_no', 'page_size'],
        'subtopic': 'dataturbo'
    },
    'dpc_show': {
        'func': dpc_show,
        'description': '查询并行客户端详情',
        'params': ['dpc_id'],
        'subtopic': 'dataturbo'
    },
    # dpc subtopic action (DPC客户端)
    'list': {
        'func': dpc_client_list,
        'description': '批量查询DPC客户端',
        'params': ['storage_id', 'process_id', 'name', 'manage_ip', 'version', 'status', 'switch_status', 'upgrade_flag', 'sort_key', 'sort_dir', 'page_no', 'page_size'],
        'subtopic': 'dpc'
    },
    'show': {
        'func': dpc_client_show,
        'description': '查询DPC客户端详情',
        'params': ['id'],
        'subtopic': 'dpc'
    },
    # kvcache subtopic action
    'kvcache_list': {
        'func': kvcache_list,
        'description': '查询 KV Cache 库',
        'params': ['storage_id', 'id', 'raw_id', 'name', 'zone_id', 'pool_raw_id', 'vstore_id', 'vstore_name', 'fs_id', 'fs_name', 'data_cleanup_switch', 'page_no', 'page_size', 'sort_dir', 'sort_key'],
        'subtopic': 'kvcache'
    },
    'kvcache_batch_create': {
        'func': kvcache_batch_create,
        'description': '批量创建 KV Cache 库',
        'params': ['storage_id', 'zone_id', 'pool_raw_id', 'vstore_id', 'kv_cache_stores', 'data_cleanup_switch', 'max_survival_time'],
        'subtopic': 'kvcache'
    },
    'kvcache_modify': {
        'func': kvcache_modify,
        'description': '修改 KV Cache 库',
        'params': ['kv_cache_stores_id', 'name', 'description', 'data_cleanup_switch', 'max_survival_time'],
        'subtopic': 'kvcache'
    },
    'kvcache_batch_delete': {
        'func': kvcache_batch_delete,
        'description': '批量删除 KV Cache 库',
        'params': ['ids'],
        'subtopic': 'kvcache'
    },
}
