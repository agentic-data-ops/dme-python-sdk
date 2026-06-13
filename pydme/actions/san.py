"""
SAN (Storage Area Network) 相关操作
包含LUN、LUN组、映射视图、存储主机、存储主机组、端口组等子主题
"""

import sys
import os

from pydme.client import DMEAPIClient

# ============================================================================
# LUN 子主题函数
# ============================================================================

"""
LUN (Volume) 相关操作
"""

import sys
import os

from pydme.client import DMEAPIClient


def lun_list(client: DMEAPIClient, limit: int = 1000, offset: int = 0,
                 sort_dir: str = None, sort_key: str = None, name: str = None,
                 vstore_raw_id: str = None, vstore_name: str = None,
                 status: str = None, health_status: str = None,
                 service_level_id: str = None, volume_wwn: str = None,
                 storage_id: str = None, pool_raw_id: str = None,
                 host_id: str = None, hostgroup_id: str = None,
                 unmapped_host_id: str = None, unmapped_hostgroup_id: str = None,
                 project_id: str = None, allocate_type: str = None,
                 attached: bool = None, query_mode: str = None,
                 protected: bool = None, pg_id: str = None,
                 usage_type: str = None,
                 support_provisioning: bool = None) -> dict:
    """
    批量查询 LUN
    
    Args:
        client: DME API 客户端
        limit: 分页查询的个数 (可选, 0~1000, 默认1000)
        offset: 分页查询的起始位置 (可选, 最小值0, 默认0)
        sort_dir: 排序方向 (可选)。可选值：asc (升序), desc (降序)
        sort_key: 排序字段 (可选)。可选值：name, size, alloc_capacity, capacity_usage, protection_capacity
        name: LUN名称 (可选, 1~256个字符, 支持模糊查询)
        vstore_raw_id: 存储设备上分配的租户ID (可选, 1~64个字符)
        vstore_name: 租户名称 (可选, 1~256个字符, 支持模糊查询)
        status: 状态 (可选, 已废弃, 建议使用health_status)。可选值：creating (创建中), normal (正常), mapping (映射中), unmapping (解除映射中), deleting (删除中), error (错误), expanding (扩容中), faulty (故障), write_protected (写保护)
        health_status: 健康状态 (可选)。可选值：normal (正常), faulty (故障), write_protected (写保护)
        service_level_id: 服务等级ID (可选, 1~64个字符)
        volume_wwn: LUN WWN (可选, 1~128个字符)
        storage_id: 存储设备ID (可选, 1~36个字符, UUID格式或32位十六进制)
        pool_raw_id: 存储池在存储设备上的ID (可选, 1~64个字符; 需同时指定storage_id)
        host_id: 主机ID (可选, 1~64个字符, UUID格式或32位十六进制)
        hostgroup_id: 主机组ID (可选, 1~64个字符, UUID格式或32位十六进制)
        unmapped_host_id: 未映射主机ID (可选, 1~64个字符)
        unmapped_hostgroup_id: 未映射主机组ID (可选, 1~64个字符)
        project_id: 业务群组ID (可选, 1~64个字符)
        allocate_type: 分配类型 (可选)。可选值：thin, thick
        attached: 映射状态 (可选)。可选值：true (已映射), false (未映射)
        query_mode: LUN发放模式 (可选)。可选值：service (服务化LUN), non-service (非服务LUN), all (所有LUN)
        protected: LUN保护状态 (可选)。可选值：true (已被保护), false (未被保护)
        pg_id: 保护组ID (可选, 1~64个字符, UUID格式或32位十六进制)
        usage_type: LUN使用类型 (可选)。可选值：traditional (传统LUN), edev (eDevLUN)
        support_provisioning: 过滤查询可发放变更的LUN (可选)。可选值：true (仅查询可发放变更), false (查询全量)
    
    Returns:
        {
            total: 总数 (integer),
            volumes: LUN 列表 (List<VolumeInfo>)。参数格式如下：[{
                id: LUN ID (string),
                name: LUN名称 (string),
                size: 容量 (integer),
                status: 状态 (string),
                health_status: 健康状态 (string),
            }, ...],
        }
    """
    url = "/rest/blockservice/v1/volumes"
    
    query_params = {
        'limit': limit,
        'offset': offset
    }
    
    if sort_dir is not None:
        query_params['sort_dir'] = sort_dir
    if sort_key is not None:
        query_params['sort_key'] = sort_key
    if name is not None:
        query_params['name'] = name
    if vstore_raw_id is not None:
        query_params['vstore_raw_id'] = vstore_raw_id
    if vstore_name is not None:
        query_params['vstore_name'] = vstore_name
    if status is not None:
        query_params['status'] = status
    if health_status is not None:
        query_params['health_status'] = health_status
    if service_level_id is not None:
        query_params['service_level_id'] = service_level_id
    if volume_wwn is not None:
        query_params['volume_wwn'] = volume_wwn
    if storage_id is not None:
        query_params['storage_id'] = storage_id
    if pool_raw_id is not None:
        query_params['pool_raw_id'] = pool_raw_id
    if host_id is not None:
        query_params['host_id'] = host_id
    if hostgroup_id is not None:
        query_params['hostgroup_id'] = hostgroup_id
    if unmapped_host_id is not None:
        query_params['unmapped_host_id'] = unmapped_host_id
    if unmapped_hostgroup_id is not None:
        query_params['unmapped_hostgroup_id'] = unmapped_hostgroup_id
    if project_id is not None:
        query_params['project_id'] = project_id
    if allocate_type is not None:
        query_params['allocate_type'] = allocate_type
    if attached is not None:
        query_params['attached'] = attached
    if query_mode is not None:
        query_params['query_mode'] = query_mode
    if protected is not None:
        query_params['protected'] = protected
    if pg_id is not None:
        query_params['pg_id'] = pg_id
    if usage_type is not None:
        query_params['usage_type'] = usage_type
    if support_provisioning is not None:
        query_params['support_provisioning'] = support_provisioning
    
    response = client.get(url, params=query_params)
    return response


def lun_show(client: DMEAPIClient, volume_id: str) -> dict:
    """
    查询指定 LUN。

    Args:
        client: DME API 客户端
        volume_id: LUN id (必选, string, 1~64个字符)

    Returns:
        {
            volume: LUN详细信息 (VolumeDetails对象)。属性格式如下：{
                id: LUN的唯一标识 (string, 1~64个字符),
                name: 名称 (string, 1~255个字符),
                description: 描述信息 (string, 0~255个字符),
                status: 状态 (string)。可选值：creating (创建中), normal (正常), mapping (映射中), unmapping (解除映射中), deleting (删除中), error (错误), expanding (扩容中), faulty (故障), write_protected (写保护),
                attached: 映射状态 (boolean, true,false),
                alloctype: 分配类型 (string)。可选值：thin (按需分配), thick (固定分配),
                total_capacity: 总容量，单位GB (double),
                storage_id: 存储设备id (string, 1~64个字符),
                storage_name: 存储设备名称 (string, 1~64个字符),
                pool_id: LUN所属存储池的id (string, 1~64个字符),
                volume_wwn: LUN在存储设备上的wwn (string, 1~64个字符),
            },
        }
    """
    url = "/rest/blockservice/v1/volumes/{volume_id}"

    if not volume_id:
        raise ValueError("volume_id 是必选参数")

    response = client.get(url, params={"volume_id": volume_id})
    return response


def lun_create(client: DMEAPIClient, storage_id: str, lun_specs: list = None,
                  lun_specs_pass_through: list = None, pool_id: str = None,
                  vstore_id: str = None, owner_controller: str = None,
                  initial_distribute_policy: str = None, prefetch_policy: str = None,
                  prefetch_value: int = None, tuning: dict = None,
                  mapping: dict = None, task_remarks: str = None) -> dict:
    """
    自定义创建 LUN

    Args:
        client: DME API 客户端
        storage_id: 存储设备 ID（必填），1~64 个字符，通过存储设备查询接口获取
        lun_specs: 待创建 LUN 基本参数 (条件必传), List<LunSpecs> 类型, 数组最大成员个数 1000, 单次最多可创建 10 组; 与 lun_specs_pass_through 互斥; 当存储设备模式不为直通模式时必传。参数格式如下：[{
                name: LUN名称 (1~255个字符, 支持字母数字._-和中文字符; 当count>1时名称为1~27个字符),
                count: 该规格LUN数量 (1~500),
                capacity: 单个LUN容量 (1~262144, 单位GB),
                suffix_length: 命名后缀规则 (1~4; 名称长度+后缀长度<=255),
                start_suffix: 起始后缀编号 (1~9999; 数量+起始后缀<=9999),
                start_lun_id: 起始LUN ID (1~65535),
                usage_type: LUN使用类型。可选值：traditional (传统LUN), edev (eDevLUN),
                write_policy: 回写策略。可选值：back (回写), through (透写),
                remote_lun_raw_id: 外部LUN ID (0~255个字符; 当usage_type为edev时生效),
                disguise_status: LUN伪装 (当usage_type为edev时生效)。可选值：nodisguise (不伪装), basic (基本伪装), expansion (扩展伪装), inheritance (继承伪装),
             }, ...]
        lun_specs_pass_through: 直通模式存储设备待创建 LUN 基本参数 (条件必传), List<lunSpecsPassThrough> 类型, 数组最大成员个数 24, 单次最多可创建 24 组; 与 lun_specs 互斥; 当存储设备模式为直通模式时必传。参数格式如下：[{
                name: LUN名称 (1~247个字符, 支持字母数字-._和中文字符; 最终名称由LUN名称+后缀编码+'-'+硬盘位置组成),
                description: LUN描述 (0~255个字符),
                disk_location: 创建LUN的硬盘位置 (1~255个字符),
                count: 每个硬盘创建的LUN数量 (1~8),
                suffix_length: 后缀编码位数 (1~4, 默认4; 当count大于1时有效),
                start_suffix: 后缀起始编码 (0~9999, 默认0; 当count大于1时有效),
             }, ...]
        pool_id: 存储池 ID（条件必传），1~64 个字符；当存储设备模式不为直通模式时必传；通过查询指定资源类型的所有实例接口获取，存储池的资源类型名称为 SYS_StoragePool
        vstore_id: 租户 ID（可选），1~64 个字符；当设备为 OceanStor V300R006C00、OceanStor V500R007C00、OceanStor Dorado 6.1.3、OceanStor 6.1.3 及其以上版本时有效
        owner_controller: 归属控制器（可选），1~64 个字符，通过查询指定存储上的控制器获取
        initial_distribute_policy: 容量初始分配策略（可选），仅支持华为 V3/V5 设备，Dorado 系列不支持；
                                  可选值：automatic（自动）、highest_performance（高性能层）、performance（性能层）、capacity（容量层）；默认 automatic
        prefetch_policy: 预取策略（可选），影响磁盘读取；
                        可选值：no_prefetch（不预取）、constant_prefetch（固定预取）、variable_prefetch（可变预取）、intelligent_prefetch（智能预取）；默认 intelligent_prefetch
        prefetch_value: 预取策略值（可选），0~1024；下发了 prefetch_policy 且其值为固定或可变预取时需要下发；固定预取取值范围 0~1024KB，可变预取取值范围 0~1024 倍
        tuning: 调优属性 (可选), CustomizeLunTuning 对象。参数格式如下：{
                smart_tier: 数据迁移策略。可选值：no_migration (不迁移), automatic_migration (自动迁移), migration_to_higher (向高性能层迁移), migration_to_lower (向低性能层迁移)。默认no_migration,
                deduplication_enabled: 重复数据删除 (仅Thin LUN支持)。可选值：true (开启), false (关闭),
                compression_enabled: 数据压缩 (仅Thin LUN支持)。可选值：true (开启), false (关闭),
                alloction_type: LUN分配类型。可选值：thin, thick,
                smart_qos: Smart QoS对象。属性格式如下：{
                        max_bandwidth: 最大带宽 (1~999999999Mbit/s; 与min_bandwidth/min_iops互斥),
                        max_iops: 最大IOPS (1~999999999; 与min_bandwidth/min_iops互斥),
                        min_bandwidth: 最小带宽 (1~999999999Mbit/s; 与max_bandwidth/max_iops互斥),
                        min_iops: 最小IOPS (1~999999999; 与max_bandwidth/max_iops互斥),
                        latency: 时延 (1~999999999ms; Dorado V6系列单位为us, 可选值为500/1500; 与max_bandwidth/max_iops互斥),
                },
                workload_type_raw_id: 应用类型ID (0~4294967295; 通过查询指定存储设备上应用类型接口获取),
             }
        mapping: 映射信息 (可选), LunMapping 对象, 存在即表示为主机或主机组创建 LUN。参数格式如下：{
                host_id: 主机ID (1~64个字符; 与hostgroup_id二选其一, 不可同时存在),
                hostgroup_id: 主机组ID (1~64个字符; 与host_id二选其一, 不可同时存在),
                host_type: 映射主机类型。可选值：storage_host (存储主机), host (主机)。默认host,
                start_host_lun_id: 起始主机LUN ID (1~4096),
                mapping_view: 映射视图请求信息 (LunMappingRequest对象)。属性格式如下：{
                        mapping_view_raw_id: 映射视图在存储设备上的ID (1~31个字符),
                        mapping_view_name: 映射视图在存储设备上的名称 (1~31个字符),
                        lun_group_raw_id: LUN组在存储设备上的ID (1~31个字符),
                        lun_group_name: LUN组在存储设备上的名称 (1~255个字符),
                        port_group_raw_id: 端口组在存储设备上的ID (1~31个字符; 主机或主机组不存在映射关系时可指定, 存在映射关系时不可指定),
                },
             }
        task_remarks: 异步任务备注信息（可选），最多 1024 个字符

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
    url = "/rest/blockservice/v1/volumes/customize"

    if not storage_id:
        raise ValueError("storage_id 是必选参数")

    payload = {
        'storage_id': storage_id
    }

    if lun_specs is not None:
        payload['lun_specs'] = lun_specs
    if lun_specs_pass_through is not None:
        payload['lun_specs_pass_through'] = lun_specs_pass_through
    if pool_id is not None:
        payload['pool_id'] = pool_id
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id
    if owner_controller is not None:
        payload['owner_controller'] = owner_controller
    if initial_distribute_policy is not None:
        payload['initial_distribute_policy'] = initial_distribute_policy
    if prefetch_policy is not None:
        payload['prefetch_policy'] = prefetch_policy
    if prefetch_value is not None:
        payload['prefetch_value'] = prefetch_value
    if tuning is not None:
        payload['tuning'] = tuning
    if mapping is not None:
        payload['mapping'] = mapping
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def lun_delete(client: DMEAPIClient, volume_ids: list, task_remarks: str = None) -> dict:
    """
    批量删除 LUN。

    Args:
        client: DME API 客户端
        volume_ids: LUN ID 列表 (必选, List[string], 数组最大成员个数：1000)
        task_remarks: 异步任务备注信息 (可选, string, 最多1024个字符)

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
    url = "/rest/blockservice/v1/volumes/delete"

    if not volume_ids or len(volume_ids) == 0:
        raise ValueError("volume_ids 是必选参数")

    payload = {
        'volume_ids': volume_ids
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def lun_modify(client: DMEAPIClient, volume_id: str, name: str = None,
                  description: str = None, owner_controller: str = None,
                  prefetch_policy: str = None, prefetch_value: int = None,
                  tuning: dict = None, task_remarks: str = None) -> dict:
    """
    修改指定 LUN

    Args:
        client: DME API 客户端
        volume_id: LUN ID
        name: 新名称（可选，1~255 个字符）
        description: 修改 LUN 描述信息（可选，0~255 个字符）
        owner_controller: 归属控制器（可选，仅非服务化 LUN 支持修改）
        prefetch_policy: 预取策略（可选，仅非服务化 LUN 支持修改）
                        可选值：0（不预取），1（固定预取），2（可变预取），3（智能预取）
        prefetch_value: 预取策略值（可选，仅非服务化 LUN 支持修改）
        tuning: LUN 调优属性 (可选, 仅非服务化LUN支持修改)。参数格式如下：{
                smarttier: 数据迁移策略 (可选, 默认0)。可选值：0 (不迁移), 1 (自动迁移), 2 (向高性能层迁移), 3 (向低性能层迁移),
                smartqos: SmartQos4Update对象 (可选)。属性格式如下：{
                        maxbandwidth: 最大带宽 (可选, 0~2147483647; 支持所有设备; 用于V3/V5系列时与minbandwidth/miniops互斥),
                        maxiops: 最大iops (可选, 0~2147483647; 支持所有设备; 用于V3/V5系列时与minbandwidth/miniops互斥),
                        minbandwidth: 最小带宽 (可选, 0~2147483647; 支持Dorado V6/V3/V5; 用于V3/V5系列时与maxbandwidth/maxiops互斥),
                        miniops: 最小iops (可选, 0~2147483647; 支持Dorado V6/V3/V5; 用于V3/V5系列时与maxbandwidth/maxiops互斥),
                        control_policy: 控制策略 (可选)。可选值：0 (保护IO下限), 1 (控制IO上限),
                        latency: 时延ms或us (可选, 0~2147483647; 需根据不同存储设备指定; 仅保护下限支持),
                        enabled: 是否启用smartqos (可选)。可选值：true, false,
                }
             }
        task_remarks: 异步任务备注信息（可选，最多 1024 个字符）

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
    url = "/rest/blockservice/v1/volumes/{volume_id}"

    if not volume_id:
        raise ValueError("volume_id 是必选参数")

    volume = {}
    if name is not None:
        volume['name'] = name
    if description is not None:
        volume['description'] = description
    if owner_controller is not None:
        volume['owner_controller'] = owner_controller
    if prefetch_policy is not None:
        volume['prefetch_policy'] = prefetch_policy
    if prefetch_value is not None:
        volume['prefetch_value'] = prefetch_value
    if tuning is not None:
        volume['tuning'] = tuning

    payload = {
        'volume': volume
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.put(url, body=payload, params={"volume_id": volume_id})
    return response


def lun_modify_name(client: DMEAPIClient, volumes: list) -> dict:
    """
    批量修改 LUN 名称

    Args:
        client: DME API 客户端
        volumes: 待修改的 LUN 信息列表 (数组最大成员个数: 1000)。参数格式如下：[{
                volume_id: LUN唯一标识 (1~64个字符),
                name: LUN新名称 (1~255个字符, 支持字母数字._-和中文字符),
             }, ...]

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
    url = "/rest/blockservice/v1/volumes"

    if not volumes or len(volumes) == 0:
        raise ValueError("volumes 是必选参数")

    payload = {
        'volumes': volumes
    }

    response = client.put(url, body=payload)
    return response


def lun_expand(client: DMEAPIClient, volumes: list, task_remarks: str = None) -> dict:
    """
    批量扩容 LUN

    Args:
        client: DME API 客户端
        volumes: 需要扩容的 LUN 信息列表 (数组最大成员个数: 1000)。参数格式如下：[{
                volume_id: LUN唯一标识 (必选, 1~64个字符),
                added_capacity: 扩容容量GB (必选, 1~262144),
             }, ...]
        task_remarks: 异步任务备注信息（可选，最多 1024 个字符）

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
    url = "/rest/blockservice/v1/volumes/expand"

    if not volumes or len(volumes) == 0:
        raise ValueError("volumes 是必选参数")

    payload = {
        'volumes': volumes
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response



def lun_connection(client: DMEAPIClient, volume_ids: list) -> dict:
    """
    查询指定 LUN ID 的连接信息。

    Args:
        client: DME API 客户端
        volume_ids: LUN ID 列表 (必选, List[string], 数组最大成员个数: 1000)

    Returns:
        {
            lun_id: LUN ID (string),
            lun_wwn: LUN WWN (string),
            iscsi_targets: iSCSI 目标列表 (List),
            fc_targets: FC 目标列表 (List),
        }
    """
    url = "/rest/blockservice/v1/volumes/connection-infos-query"

    if not volume_ids or len(volume_ids) == 0:
        raise ValueError("volume_ids 是必选参数")

    payload = {
        'lun_ids': volume_ids
    }

    response = client.post(url, body=payload)
    return response


def lun_group_list(client: DMEAPIClient, page_size: int = 20, page_no: int = 1,
                    sort_dir: str = None, sort_key: str = None,
                    name: str = None, vstore_raw_id: str = None,
                    vstore_name: str = None, storage_id: str = None,
                    storage_name: str = None, raw_id: str = None,
                    attached: bool = None,
                    protection_group_raw_id: str = None,
                    avaiable_mapping_for_host_id: str = None,
                    avaiable_mapping_for_host_group_id: str = None,
                    support_provisioning: bool = None) -> dict:
    """
    批量查询 LUN 组

    查询 LUN 组列表，支持分页和多种过滤条件。

    Args:
        client: DME API 客户端
        page_size: 分页查询的个数 (可选, 0~1000, 默认20)
        page_no: 分页查询的起始页码 (可选, 1~10000000, 默认1)
        sort_dir: 排序方向 (可选)。可选值：asc (升序), desc (降序)
        sort_key: 排序字段 (可选)。可选值：lun_count (LUN数量), total_capcity (总容量), capacity_usage (已用容量), name, raw_id (设备侧ID)
        name: LUN组名称 (可选, 1~256个字符, 支持模糊查询)
        vstore_raw_id: 存储设备上分配的租户ID (可选, 1~64个字符)
        vstore_name: 租户名称 (可选, 1~256个字符, 支持模糊查询)
        storage_id: 存储设备ID (可选, 1~64个字符)
        storage_name: 存储名称 (可选, 1~256个字符, 支持模糊查询)
        raw_id: LUN组在存储设备上的ID (可选, 1~256个字符)
        attached: 映射状态 (可选)。可选值：true (已映射), false (未映射)
        protection_group_raw_id: 保护组在存储设备上的ID (可选, 0~64个字符; 非空则查询保护组下的LUN组, 空串则查询未加入保护组的LUN组)
        avaiable_mapping_for_host_id: 可映射的主机ID (可选, 1~64个字符; 与avaiable_mapping_for_host_group_id互斥)
        avaiable_mapping_for_host_group_id: 可映射的主机组ID (可选, 1~64个字符; 与avaiable_mapping_for_host_id互斥)
        support_provisioning: 是否支持发放 (可选)。可选值：true (支持), false (不支持)

    Returns:
        {
            total: LUN组总数 (integer),
            lun_groups: LUN组列表 (List<LunGroupInfo>)。参数格式如下：[{
                id: LUN组ID (string),
                name: LUN组名称 (string),
                storage_id: 存储设备ID (string),
                lun_count: LUN数量 (integer),
                attached: 映射状态 (boolean),
            }, ...],
        }
    """
    url = "/rest/blockservice/v1/lun-groups/query"

    body_params = {
        'page_no': page_no,
        'page_size': page_size
    }

    if sort_dir is not None:
        body_params['sort_dir'] = sort_dir
    if sort_key is not None:
        body_params['sort_key'] = sort_key
    if name is not None:
        body_params['name'] = name
    if vstore_raw_id is not None:
        body_params['vstore_raw_id'] = vstore_raw_id
    if vstore_name is not None:
        body_params['vstore_name'] = vstore_name
    if storage_id is not None:
        body_params['storage_id'] = storage_id
    if storage_name is not None:
        body_params['storage_name'] = storage_name
    if raw_id is not None:
        body_params['raw_id'] = raw_id
    if attached is not None:
        body_params['attached'] = attached
    if protection_group_raw_id is not None:
        body_params['protection_group_raw_id'] = protection_group_raw_id
    if avaiable_mapping_for_host_id is not None:
        body_params['avaiable_mapping_for_host_id'] = avaiable_mapping_for_host_id
    if avaiable_mapping_for_host_group_id is not None:
        body_params['avaiable_mapping_for_host_group_id'] = avaiable_mapping_for_host_group_id
    if support_provisioning is not None:
        body_params['support_provisioning'] = support_provisioning

    response = client.post(url, body=body_params)
    return response


def lun_group_show(client: DMEAPIClient, group_id: str, storage_id: str = None) -> dict:
    """
    查询指定 LUN 组详情。

    Args:
        client: DME API 客户端
        group_id: LUN 组 ID (必选, string)
        storage_id: 存储设备 ID (可选, string)

    Returns:
        {
            id: LUN组ID (string),
            name: LUN组名称 (string),
            storage_id: 存储设备ID (string),
            lun_count: LUN数量 (integer),
            description: 描述 (string),
        }
    """
    url = "/rest/blockservice/v1/lun-groups/{group_id}"

    response = client.get(url, params={"group_id": group_id})
    return response


def lun_group_create(client: DMEAPIClient, storage_id: str, name: str,
                     description: str = None, existing_lun_ids: list = None,
                     customize_volumes: dict = None, task_remarks: str = None,
                     vstore_id: str = None, zoning_info: dict = None,
                     mapping_view: dict = None) -> dict:
    """
    创建 LUN 组

    创建新的 LUN 组。

    Args:
        client: DME API 客户端
        storage_id: 存储设备 ID (必选, 1~64个字符)
        name: LUN 组名称 (必选, 1~255个字符, 支持字母数字._-和中文字符)
        description: LUN 组描述 (可选, 0~255个字符)
        existing_lun_ids: LUN ID 列表 (可选, 与customize_volumes互斥, 数组最大成员个数: 1000)
        customize_volumes: CustomizeVolumesParam对象 (可选, 与existing_lun_ids互斥)。参数格式如下：{
                volume_specs: VolumeSpecsParam列表 (可选, 与lun_specs_pass_through互斥, 数组最大成员个数: 1000)。参数格式如下：[{
                        name: LUN名称 (必选, 1~255个字符, 支持字母数字._-和中文字符; count>1时名称长度1~27字符),
                        description: LUN描述 (可选, 0~255个字符),
                        count: 该规格LUN数量 (必选, 1~500),
                        capacity: 该规格LUN容量GB (必选, 1~262144),
                        suffix_length: LUN命名后缀规则 (可选, 0~4; 名称长度+后缀长度<=255),
                        start_suffix: 该规格LUN起始后缀编号 (可选, 0~9999),
                        start_lun_id: 该规格起始LUN ID (可选, 0~65535),
                     }, ...],
                lun_specs_pass_through: lunSpecsPassThrough列表 (可选, 与volume_specs互斥, 数组最大成员个数: 24; 当存储设备模式为直通模式时必传)。参数格式如下：[{
                        name: LUN名称 (必选, 1~247个字符, 支持字母数字-._和中文字符; 最终名称由LUN名称+后缀编码+硬盘位置组成),
                        description: LUN描述 (可选, 0~255个字符),
                        disk_location: 创建LUN的硬盘位置 (必选, 1~255个字符),
                        count: 每个硬盘创建的LUN数量 (必选, 1~8),
                        suffix_length: 后缀编码位数 (可选, 1~4, 默认4; count>1时有效),
                        start_suffix: 后缀起始编码 (可选, 0~9999, 默认0; count>1时有效),
                     }, ...],
                pool_raw_id: 存储池在存储设备上的id (可选, 1~64个字符; 设备模式不为直通模式时必传),
                availability_zone: 可用分区id (可选, 0~64个字符),
                owner_controller: 归属控制器 (可选, 0~64个字符),
                initial_distribute_policy: 容量初始分配策略 (可选, 仅V3/V5设备, 全闪存不支持)。可选值：0 (自动), 1 (高性能层), 2 (性能层), 3 (容量层)。默认0,
                prefetch_policy: 预取策略 (可选)。可选值：0 (不预取), 1 (固定预取), 2 (可变预取), 3 (智能预取)。默认3,
                prefetch_value: 预取策略值 (可选, 0~1024; 固定预取0~1024KB, 可变预取0~1024倍),
                tuning: CustomizeVolumeTuning对象 (可选)。属性格式如下：{
                        smartqos: SmartQos对象 (可选)。属性格式如下：{
                                name: Smart QoS名称 (可选, 1~255个字符),
                        },
                        alloctype: LUN分配类型 (可选)。可选值：thin, thick,
                        workload_type_id: 应用类型id (可选, 从存储设备上获取),
                }
             }
        task_remarks: 异步任务备注信息 (可选, 最多1024个字符)
        vstore_id: 租户ID (可选, 1~64个字符; 当设备为OceanStor V300R006C30/V500R007C20/Dorado 6.1.3/6.1.3及以上版本时有效)
        zoning_info: ZoningParam对象 (可选)。参数格式如下：{
                zone_policy_id: zone策略id (可选, 0~64个字符; 指定则自动划zone),
                target_fcports: 端口wwn列表 (可选, 与target_fcportgroups二选其一, 数组最大成员个数: 1000; 当mapping_view中port_group_id为空时生效),
                target_fcportgroups: 端口组id列表 (可选, 与target_fcports二选其一, 数组最大成员个数: 1000; 当mapping_view中port_group_id为空时生效),
             }
        mapping_view: MappingViewRequestParam对象 (可选)。参数格式如下：{
                mapping_view_name: 映射视图在设备上的名字 (可选, 最多31个字符),
                mapping_host_info: MappingHostInfo对象 (可选, 与mapping_host_group_info二选其一)。属性格式如下：{
                        todo_host_name: todo任务中的主机名称 (可选, 1~255个字符, 支持字母数字._-和中文字符),
                        id: 主机ID (可选, 1~64个字符),
                },
                mapping_host_group_info: MappingHostGroupInfo对象 (可选, 与mapping_host_info二选其一)。属性格式如下：{
                        todo_host_group_name: todo任务中的主机组名称 (可选, 1~255个字符, 支持字母数字._-和中文字符),
                        id: 主机组ID (可选, 1~64个字符),
                },
                port_group_id: 端口组在设备上的ID (可选, 1~31个字符),
                start_host_lun_id: 起始HostLunID (可选, 0~2147483647),
             }

    Returns:
        {
            id: LUN组ID (string, 1~64个字符),
        }
    """
    url = "/rest/blockservice/v1/lun-groups"

    if not storage_id or not name:
        raise ValueError("storage_id 和 name 是必选参数")

    body_params = {
        'storage_id': storage_id,
        'name': name
    }

    if description is not None:
        body_params['description'] = description
    if existing_lun_ids is not None:
        body_params['existing_lun_ids'] = existing_lun_ids
    if customize_volumes is not None:
        body_params['customize_volumes'] = customize_volumes
    if task_remarks is not None:
        body_params['task_remarks'] = task_remarks
    if vstore_id is not None:
        body_params['vstore_id'] = vstore_id
    if zoning_info is not None:
        body_params['zoning_info'] = zoning_info
    if mapping_view is not None:
        body_params['mapping_view'] = mapping_view

    response = client.post(url, body=body_params)
    return response


def lun_group_delete(client: DMEAPIClient, lun_group_ids: list,
                     task_remarks: str = None) -> dict:
    """
    批量删除 LUN 组

    Args:
        client: DME API 客户端
        lun_group_ids: LUN组ID列表 (必选, 数组最大成员个数: 500)
        task_remarks: 异步任务备注信息 (可选, 最多1024个字符)

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
    url = "/rest/blockservice/v1/lun-groups/delete"

    if not lun_group_ids or len(lun_group_ids) == 0:
        raise ValueError("lun_group_ids 是必选参数")

    body_params = {
        'lun_group_ids': lun_group_ids
    }

    if task_remarks is not None:
        body_params['task_remarks'] = task_remarks

    response = client.post(url, body=body_params)
    return response


def lun_group_add_luns(client: DMEAPIClient, group_id: str,
                       existing_lun_ids: list = None,
                       customize_volumes: dict = None,
                       host_lun_id_infos: list = None,
                       host_lun_id_verify: bool = False,
                       task_remarks: str = None) -> dict:
    """
    向 LUN 组添加 LUN

    Args:
        client: DME API 客户端
        group_id: LUN 组 ID
        existing_lun_ids: 已有LUN集合 (可选, 与customize_volumes互斥, 数组最大成员个数: 1000)。参数格式如下：[{
                lun_id: 已有LUN ID (必选, 1~64个字符),
             }, ...]
        customize_volumes: CustomizeVolumesParam对象 (可选, 与existing_lun_ids互斥)。参数格式如下：{
                volume_specs: VolumeSpecsParam列表 (可选, 与lun_specs_pass_through互斥, 数组最大成员个数: 1000)。参数格式如下：[{
                        name: LUN名称 (必选, 1~255个字符, 支持字母数字._-和中文字符; count>1时名称长度1~27字符),
                        description: LUN描述 (可选, 0~255个字符),
                        count: 该规格LUN数量 (必选, 1~500),
                        capacity: 该规格LUN容量GB (必选, 1~262144),
                        suffix_length: LUN命名后缀规则 (可选, 0~4; 名称长度+后缀长度<=255),
                        start_suffix: 该规格LUN起始后缀编号 (可选, 0~9999),
                        start_lun_id: 该规格起始LUN ID (可选, 0~65535),
                     }, ...],
                lun_specs_pass_through: lunSpecsPassThrough列表 (可选, 与volume_specs互斥, 数组最大成员个数: 24; 直通模式时必传)。参数格式如下：[{
                        name: LUN名称 (必选, 1~247个字符, 支持字母数字-._和中文字符; 最终名称由LUN名称+后缀编码+硬盘位置组成),
                        description: LUN描述 (可选, 0~255个字符),
                        disk_location: 创建LUN的硬盘位置 (必选, 1~255个字符),
                        count: 每个硬盘创建的LUN数量 (必选, 1~8),
                        suffix_length: 后缀编码位数 (可选, 1~4, 默认4; count>1时有效),
                        start_suffix: 后缀起始编码 (可选, 0~9999, 默认0; count>1时有效),
                     }, ...],
                pool_raw_id: 存储池在存储设备上的id (可选, 1~64个字符; 设备模式不为直通模式时必传),
                availability_zone: 可用分区id (可选, 0~64个字符),
                owner_controller: 归属控制器 (可选, 0~64个字符),
                initial_distribute_policy: 容量初始分配策略 (可选, 仅V3/V5, 全闪存不支持)。可选值：0 (自动), 1 (高性能层), 2 (性能层), 3 (容量层)。默认0,
                prefetch_policy: 预取策略 (可选)。可选值：0 (不预取), 1 (固定预取), 2 (可变预取), 3 (智能预取)。默认3,
                prefetch_value: 预取策略值 (可选, 0~1024; 固定预取0~1024KB, 可变预取0~1024倍),
                tuning: CustomizeVolumeTuning对象 (可选)。属性格式如下：{
                        smartqos: SmartQos对象 (可选)。属性格式如下：{
                                name: Smart QoS名称 (可选, 1~255个字符),
                        },
                        alloctype: LUN分配类型 (可选)。可选值：thin, thick,
                        workload_type_id: 应用类型id (可选),
                }
             }
        host_lun_id_infos: HostLunIdInfo列表 (可选, 数组最大成员个数: 1000; 仅Dorado V6/V7和OceanStor V6/V7设备支持)。参数格式如下：[{
                host_lun_id: LUN指定的主机LUN ID (必选, 0~4095),
                lun_id: 加入LUN组的LUN ID (必选, 1~64个字符),
             }, ...]
        host_lun_id_verify: 是否进行双活主机LUN ID一致性校验 (可选, 默认false)。可选值：true (不校验), false (校验)
        task_remarks: 异步任务备注信息 (可选, 最多1024个字符)

    Returns:
        响应数据
    """
    url = "/rest/blockservice/v1/lun-groups/{group_id}/add-luns"

    body_params = {}

    if existing_lun_ids is not None:
        body_params['existing_lun_ids'] = existing_lun_ids
    if customize_volumes is not None:
        body_params['customize_volumes'] = customize_volumes
    if host_lun_id_infos is not None:
        body_params['host_lun_id_infos'] = host_lun_id_infos

    body_params = {}

    if existing_lun_ids is not None:
        body_params['existing_lun_ids'] = existing_lun_ids
    if customize_volumes is not None:
        body_params['customize_volumes'] = customize_volumes
    if host_lun_id_infos is not None:
        body_params['host_lun_id_infos'] = host_lun_id_infos
    if host_lun_id_verify is not False:
        body_params['host_lun_id_verify'] = host_lun_id_verify
    if task_remarks is not None:
        body_params['task_remarks'] = task_remarks

    response = client.post(url, body=body_params)
    return response


def lun_group_remove_luns(client: DMEAPIClient, group_id: str,
                           lun_ids: list, task_remarks: str = None) -> dict:
    """
    从 LUN 组移除 LUN

    Args:
        client: DME API 客户端
        group_id: LUN 组 ID
        lun_ids: LUN ID 列表 (必选, 数组最小成员个数: 1, 数组最大成员个数: 10000)
        task_remarks: 异步任务备注信息 (可选, 最多1024个字符)

    Returns:
        响应数据
    """
    url = "/rest/blockservice/v1/lun-groups/{group_id}/remove-luns"

    body_params = {
        'lun_ids': lun_ids
    }

    if task_remarks is not None:
        body_params['task_remarks'] = task_remarks

    response = client.post(url, params={"group_id": group_id})
    return response


def lun_group_show_luns(client: DMEAPIClient, group_id: str,
                         page_size: int = 100, page_no: int = 1,
                         health_status: str = None) -> dict:
    """
    查询 LUN 组中的 LUN

    Args:
        client: DME API 客户端
        group_id: LUN 组 ID
        page_size: 分页查询的个数 (可选, 1~1000, 默认100)
        page_no: 分页查询的页码 (可选, 1~10000000, 默认1)
        health_status: 健康状态 (可选)。可选值：normal (正常), faulty (故障), write_protected (写保护)

    Returns:
        响应数据，包含 LUN 列表
    """
    url = "/rest/blockservice/v1/lun-groups/{group_id}/luns/query"

    body_params = {
        'page_size': page_size,
        'page_no': page_no
    }

    if health_status is not None:
        body_params['health_status'] = health_status


    body_params = {
        'page_size': page_size,
        'page_no': page_no
    }

    if health_status is not None:
        body_params['health_status'] = health_status

    response = client.post(url, body=body_params)
    return response


# 动作列表，用于 CLI 帮助

# ============================================================================
# 映射视图 (mapping_view) 子主题函数
# ============================================================================



import sys
import os

from pydme.client import DMEAPIClient


def mapping_view_create(
    client: DMEAPIClient,
    storage_id: str, name: str = None,
    port_group_id: str = None,
    start_host_lun_id: int = None,
    host: dict = None, vbs: dict = None,
    host_group: dict = None,
    lun_group: dict = None,
    luns: dict = None,
    task_remarks: str = None
) -> dict:
    """
    创建映射视图

    Args:
        client: DME API 客户端
        storage_id: 存储设备 ID (必选, 1~64个字符)
        name: 映射视图名称 (可选, 1~31个字符; 设备类型为OceanStor V3/V5时有效)
        port_group_id: 端口组 ID (可选, 1~64个字符)
        start_host_lun_id: 主机LUN SCSI ID起始值 (可选, 0~2147483647)
        host: 存储主机 (可选, 与vbs/host_group互斥)。属性格式如下：{
                todo_host_name: todo任务中的主机名称 (可选, 1~255个字符, 支持字母数字._-和中文字符),
                id: 主机ID (可选, 1~64个字符),
             }
        vbs: VBS客户端 (可选, 与host/host_group互斥; 仅OceanStor Pacific和FusionStorage支持)。属性格式如下：{
                id: VBS ID (可选, 1~64个字符),
             }
        host_group: 存储主机组 (可选, 与host/vbs互斥)。属性格式如下：{
                todo_host_group_name: todo任务中的主机组名称 (可选, 1~255个字符, 支持字母数字._-和中文字符),
                id: 主机组ID (可选, 1~64个字符),
             }
        lun_group: 待映射的LUN组 (可选, 与luns互斥)。属性格式如下：{
                id: LUN组ID (可选, 1~64个字符),
             }
        luns: 待映射的LUN信息 (可选, 与lun_group互斥)。属性格式如下：{
                ids: 待映射的LUN ID列表 (可选, 数组最大成员个数: 1000),
                lungroup_name: LUN组名称 (可选, 1~255个字符; lun映射时需创建指定名称lun组时下发),
             }
        task_remarks: 异步任务备注信息 (可选, 最多1024个字符)

    Returns:
        响应数据，包含 task_id
    """
    url = "/rest/blockservice/v1/mapping-views"

    body_params = {
        'storage_id': storage_id
    }

    if name is not None:
        body_params['name'] = name
    if port_group_id is not None:
        body_params['port_group_id'] = port_group_id
    if start_host_lun_id is not None:
        body_params['start_host_lun_id'] = start_host_lun_id
    if host is not None:
        body_params['host'] = host
    if vbs is not None:
        body_params['vbs'] = vbs
    if host_group is not None:
        body_params['host_group'] = host_group
    if lun_group is not None:
        body_params['lun_group'] = lun_group
    if luns is not None:
        body_params['luns'] = luns
    if task_remarks is not None:
        body_params['task_remarks'] = task_remarks

    response = client.post(url, body=body_params)
    return response


def mapping_view_delete(client: DMEAPIClient, ids: list) -> dict:
    """
    批量删除映射视图。

    Args:
        client: DME API 客户端
        ids: 映射视图 ID 列表 (必选, List[string])

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
    url = "/rest/blockservice/v1/mapping-views/batch-delete"

    if not ids or len(ids) == 0:
        raise ValueError("ids 是必选参数")

    body_params = {
        'ids': ids
    }

    response = client.post(url, body=body_params)
    return response


def mapping_view_list(
    client: DMEAPIClient,
    page_size: int = 100,
    page_no: int = 1,
    name: str = None,
    raw_id: str = None,
    storage_id: str = None,
    lun_id: str = None,
    lun_name: str = None,
    lun_group_id: str = None,
    lun_group_raw_id: str = None,
    lun_group_name: str = None,
    storage_host_id: str = None,
    storage_host_name: str = None,
    storage_host_group_id: str = None,
    storage_host_group_name: str = None,
    storage_host_group_raw_id: str = None,
    port_group_id: str = None,
    port_group_raw_id: str = None,
    port_group_name: str = None,
    sort_key: str = None,
    sort_dir: str = None
) -> dict:
    """
    批量查询映射视图列表

    批量查询存储设备上的映射视图信息，支持多种过滤条件。

    Args:
        client: DME API 客户端
        page_size: 分页查询的个数 (可选, 0~1000, 默认100)
        page_no: 分页查询的起始位置 (可选, 1~10000000, 默认1)
        name: 映射视图名称 (可选, 0~256个字符, 支持模糊搜索)
        raw_id: 映射视图在存储设备上的ID (可选, 1~256个字符)
        storage_id: 存储设备的唯一标识 (可选, 0~64个字符)
        lun_id: LUN的唯一标识 (可选, 0~64个字符; 与lun_name参数不支持同时下发)
        lun_name: LUN名称 (可选, 1~256个字符, 支持模糊搜索; 与lun_id参数不支持同时下发)
        lun_group_id: LUN组的唯一标识 (可选, 0~64个字符; 与lun_group_raw_id/lun_group_name不支持同时下发)
        lun_group_raw_id: 设备侧分配的LUN组ID (可选, 1~64个字符; 与lun_group_id/lun_group_name不支持同时下发)
        lun_group_name: LUN组名称 (可选, 1~256个字符, 支持模糊查询; 与lun_group_id/lun_group_raw_id不支持同时下发)
        storage_host_id: 存储主机的唯一标识 (可选, 0~64个字符; 与storage_host_name不支持同时下发)
        storage_host_name: 存储主机名称 (可选, 0~256个字符, 支持模糊搜索; 仅OceanStor Dorado v6和OceanProtect X支持; 与storage_host_id不支持同时下发)
        storage_host_group_id: 存储主机组的唯一标识 (可选, 0~64个字符; 与storage_host_group_name/storage_host_group_raw_id不支持同时下发)
        storage_host_group_name: 存储主机组名称 (可选, 0~256个字符, 支持模糊搜索; 与storage_host_group_id/storage_host_group_raw_id不支持同时下发)
        storage_host_group_raw_id: 设备侧分配的存储主机组ID (可选, 1~64个字符; 与storage_host_group_id/storage_host_group_name不支持同时下发)
        port_group_id: 端口组的唯一标识 (可选, 0~64个字符; 与port_group_raw_id/port_group_name不支持同时下发)
        port_group_raw_id: 设备侧分配的端口组ID (可选, 1~64个字符; 与port_group_id/port_group_name不支持同时下发)
        port_group_name: 端口组名称 (可选, 0~256个字符, 支持模糊搜索; 与port_group_id/port_group_raw_id不支持同时下发)
        sort_key: 排序字段 (可选)。可选值：raw_id, storage_host_group_raw_id, lun_group_raw_id, port_group_raw_id
        sort_dir: 排序方向 (可选)。可选值：asc (升序), desc (降序)

    Returns:
        响应数据，包含映射视图列表
    """
    url = "/rest/blockservice/v1/mapping-views/query"

    body_params = {
        'page_size': page_size,
        'page_no': page_no
    }

    if name is not None:
        body_params['name'] = name

    if raw_id is not None:
        body_params['raw_id'] = raw_id

    if storage_id is not None:
        body_params['storage_id'] = storage_id

    if lun_id is not None:
        body_params['lun_id'] = lun_id

    if lun_name is not None:
        body_params['lun_name'] = lun_name

    if lun_group_id is not None:
        body_params['lun_group_id'] = lun_group_id

    if lun_group_raw_id is not None:
        body_params['lun_group_raw_id'] = lun_group_raw_id

    if lun_group_name is not None:
        body_params['lun_group_name'] = lun_group_name

    if storage_host_id is not None:
        body_params['storage_host_id'] = storage_host_id

    if storage_host_name is not None:
        body_params['storage_host_name'] = storage_host_name

    if storage_host_group_id is not None:
        body_params['storage_host_group_id'] = storage_host_group_id

    if storage_host_group_name is not None:
        body_params['storage_host_group_name'] = storage_host_group_name

    if storage_host_group_raw_id is not None:
        body_params['storage_host_group_raw_id'] = storage_host_group_raw_id

    if port_group_id is not None:
        body_params['port_group_id'] = port_group_id

    if port_group_raw_id is not None:
        body_params['port_group_raw_id'] = port_group_raw_id

    if port_group_name is not None:
        body_params['port_group_name'] = port_group_name

    if sort_key is not None:
        body_params['sort_key'] = sort_key

    if sort_dir is not None:
        body_params['sort_dir'] = sort_dir

    response = client.post(url, body=body_params)
    return response


def query_host_lun_mapping(
    client: DMEAPIClient,
    storage_host_id: str = None,
    storage_host_name: str = None,
    lun_id: str = None,
    lun_name: str = None,
    storage_id: str = None
) -> dict:
    """
    查询存储主机和 LUN 映射关系

    根据存储主机/存储主机名称或 LUN 过滤查询映射关系。

    Args:
        client: DME API 客户端
        storage_host_id: 存储主机 ID，和 storage_host_name 参数不支持同时下发
        storage_host_name: 存储主机名称，支持模糊搜索，和 storage_host_id 参数不支持同时下发
        lun_id: LUN ID，和 lun_name 参数不支持同时下发
        lun_name: LUN 名称，支持模糊搜索，和 lun_id 参数不支持同时下发
        storage_id: 存储设备 ID

    Returns:
        响应数据，包含映射关系列表
    """
    url = "/rest/blockservice/v1/storage-host-lun-mappings/query"

    body_params = {}

    if storage_id is not None:
        body_params['storage_id'] = storage_id

    if storage_host_id is not None:
        body_params['storage_host_id'] = storage_host_id

    if storage_host_name is not None:
        body_params['storage_host_name'] = storage_host_name

    if lun_id is not None:
        body_params['lun_id'] = lun_id

    if lun_name is not None:
        body_params['lun_name'] = lun_name

    response = client.post(url, body=body_params)
    return response


def mapping_view_query(
    client: DMEAPIClient,
    type: str,
    request_id: str,
    storage_id: str
) -> dict:
    """
    查询物理主机（组）关联的映射关系

    根据物理主机/主机组 ID 过滤查询指定存储设备上的映射视图。

    Args:
        client: DME API 客户端
        type: 查询类别 (必选)。可选值：host (物理主机), host_group (主机组)
        request_id: 物理主机/主机组 ID (必选, 1~64个字符)
        storage_id: 存储设备 ID (必选, 1~64个字符)

    Returns:
        响应数据，包含映射视图列表
    """
    url = "/rest/blockservice/v1/volumes/mapping-view/query"

    body_params = {
        'type': type,
        'request_id': request_id,
        'storage_id': storage_id
    }

    response = client.post(url, body=body_params)
    return response


def physical_host_show_mapping_views(client: DMEAPIClient, host_id: str,
                                      storage_id: str) -> dict:
    """
    查询物理主机关联的映射关系

    Args:
        client: DME API 客户端
        host_id: 物理主机 ID (必选, 1~64个字符)
        storage_id: 存储设备 ID (必选, 1~64个字符)

    Returns:
        响应数据，包含映射视图列表
    """
    return mapping_view_query(
        client=client, type="host",
        request_id=host_id, storage_id=storage_id
    )


def physical_host_group_show_mapping_views(client: DMEAPIClient, host_group_id: str,
                                            storage_id: str) -> dict:
    """
    查询物理主机组关联的映射关系

    Args:
        client: DME API 客户端
        host_group_id: 物理主机组 ID (必选, 1~64个字符)
        storage_id: 存储设备 ID (必选, 1~64个字符)

    Returns:
        响应数据，包含映射视图列表
    """
    return mapping_view_query(
        client=client, type="host_group",
        request_id=host_group_id, storage_id=storage_id
    )


# ============================================================================
# 存储主机 (storage_host) 子主题函数
# ============================================================================

def storage_host_create(client: DMEAPIClient, storage_id: str,
                host_info: dict, task_remarks: str = None,
                vstore_id: str = None) -> dict:
    """
    创建存储主机

    在指定存储设备上创建存储主机。

    Args:
        client: DME API 客户端
        storage_id: 存储设备ID (必选, 1~64个字符)
        host_info: CreateStorageHostInfo对象 (必选)。属性格式如下：{
                name: 主机名称 (必选, 1~255个字符, 支持字母数字._-和中文字符),
                os_type: 主机类型 (必选)。可选值：LINUX, WINDOWS, WINDOWSSERVER2012, SOLARIS, HPUX, AIX, XENSERVER, LINUX_VIS, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC,
                ip: 主机ip地址 (可选, 最多127个字符),
                description: 主机描述 (可选, 最多63个字符),
                initiators: StorageInitiatorParam列表 (可选, 数组最大成员个数: 1000)。参数格式如下：[{
                        protocol: 启动器类型 (必选)。可选值：fc, iscsi, nvme_over_roce,
                        raw_id: 主机启动器wwpn或iqn或nqn (必选, 1~223个字符),
                        alias: 启动器别名 (可选, 最多31个字符),
                     }, ...],
                multipath: MultiPathForCreateRequestParam对象 (可选)。属性格式如下：{
                        multipath_type: 第三方多路径策略 (必选)。可选值：default (默认), third_party (第三方多路径),
                        path_type: 启动器路径类型 (可选, 开启第三方多路径时有效)。可选值：optimal_path (优选路径), non_optimal_path (非优选路径),
                        failover_mode: 启动器切换模式 (可选, 开启第三方多路径时有效)。可选值：early_version_alua, common_alua, alua_not_used, special_alua,
                        special_mode_type: 特殊模式类型 (可选, 切换模式为特殊模式时有效)。可选值：mode_zero, mode_one, mode_two, mode_three,
                }
             }
        task_remarks: 异步任务备注信息 (可选, 最多1024个字符)
        vstore_id: 租户ID (可选, 1~64个字符; 设备为OceanStor V300R006C30/V500R007C20/Dorado 6.1.3及以上时有效)

    Returns:
        任务 ID
    """
    url = "/rest/hostmgmt/v1/storage-hosts"

    payload = {
        'storage_id': storage_id,
        'host_info': host_info
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id

    response = client.post(url, body=payload)
    return response


def storage_host_batch_query(client: DMEAPIClient, ids: list) -> dict:
    """
    根据存储主机 ID 列表批量查询存储主机

    Args:
        client: DME API 客户端
        ids: ID 列表（必选，1~1000 个）

    Returns:
        存储主机信息列表
    """
    url = "/rest/hostmgmt/v1/storage-hosts/query-by-ids"

    payload = {
        'ids': ids
    }

    response = client.post(url, body=payload)
    return response


def storage_host_list(client: DMEAPIClient, page_size: int = None, page_no: int = None,
              sort_key: str = None, sort_dir: str = None, name: str = None,
              raw_id: str = None, host_group_id: str = None,
              avaliable_add_to_host_group_id: str = None, host_group_name: str = None,
              ip: str = None, health_status: str = None, os_type: str = None,
              storage_id: str = None, avaiable_mapping_for_lun_group_id: str = None,
              avaiable_mapping_for_lun_id: str = None, support_provisioning: bool = None,
              manufacturer: str = None, vstore_raw_id: str = None,
              vstore_name: str = None) -> dict:
    """
    批量查询存储主机

    Args:
        client: DME API 客户端
        page_size: 分页查询的个数 (可选, 1~1000, 默认20)
        page_no: 分页查询的起始位置 (可选, 最小值1, 默认1)
        sort_key: 排序关键字 (可选, sort_key不填时sort_dir不生效)。可选值：ip, name, initiator_count, lun_count, lun_group_count, capacity, allocated_capacity, raw_id
        sort_dir: 排序方向 (可选)。可选值：desc (降序), asc (升序)
        name: 主机名称 (可选, 1~256个字符, 支持模糊匹配)
        raw_id: 主机在设备侧的ID (可选, 0~256个字符)
        host_group_id: 归属主机组ID (可选, 最多64个字符)
        avaliable_add_to_host_group_id: 待添加主机组ID (可选, 与host_group_id互斥, 最多64个字符)
        host_group_name: 归属主机组名称 (可选, 最多256个字符, 支持模糊匹配; 空串查询未归属主机组的主机)
        ip: 主机IP (可选, 最多256个字符, 支持模糊匹配; 空串查询未配置IP的主机)
        health_status: 健康状态 (可选)。可选值：normal (正常), no_redundant_link (无冗余路径), offline (离线), fault (故障), degraded (已降级)
        os_type: 存储主机类型 (可选)。可选值：LINUX, WINDOWS, WINDOWSSERVER2012, SOLARIS, HPUX, AIX, XENSERVER, LINUX_VIS, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC, UNKNOWN
        storage_id: 存储设备ID (可选, 1~64个字符)
        avaiable_mapping_for_lun_group_id: 可映射的LUN组ID (可选, 1~64个字符; 与avaiable_mapping_for_lun_id互斥)
        avaiable_mapping_for_lun_id: 可映射的LUN ID (可选, 1~64个字符; 与avaiable_mapping_for_lun_group_id互斥)
        support_provisioning: 是否支持发放 (可选)。可选值：true, false
        manufacturer: 存储设备厂商 (可选, 1~64个字符)。可选值：huawei, dell_emc, fujitsu, hitachi, hpe, ibm, netapp, pure, third_part
        vstore_raw_id: 租户ID (可选)
        vstore_name: 租户名称 (可选)

    Returns:
        响应数据，包含存储主机列表和总数
    """
    url = "/rest/hostmgmt/v1/storage-hosts/query"

    payload = {}

    if page_size is not None:
        payload['page_size'] = page_size
    if page_no is not None:
        payload['page_no'] = page_no
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if name is not None:
        payload['name'] = name
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if host_group_id is not None:
        payload['host_group_id'] = host_group_id
    if avaliable_add_to_host_group_id is not None:
        payload['avaliable_add_to_host_group_id'] = avaliable_add_to_host_group_id
    if host_group_name is not None:
        payload['host_group_name'] = host_group_name
    if ip is not None:
        payload['ip'] = ip
    if health_status is not None:
        payload['health_status'] = health_status
    if os_type is not None:
        payload['os_type'] = os_type
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if avaiable_mapping_for_lun_group_id is not None:
        payload['avaiable_mapping_for_lun_group_id'] = avaiable_mapping_for_lun_group_id
    if avaiable_mapping_for_lun_id is not None:
        payload['avaiable_mapping_for_lun_id'] = avaiable_mapping_for_lun_id
    if support_provisioning is not None:
        payload['support_provisioning'] = support_provisioning
    if manufacturer is not None:
        payload['manufacturer'] = manufacturer
    if vstore_raw_id is not None:
        payload['vstore_raw_id'] = vstore_raw_id
    if vstore_name is not None:
        payload['vstore_name'] = vstore_name

    response = client.post(url, body=payload)
    return response


def storage_host_modify(client: DMEAPIClient, storage_host_id: str,
                storage_host_name: str = None, storage_host_description: str = None,
                storage_host_ip: str = None, storage_host_os_type: str = None,
                add_initiators: list = None, remove_initiators: list = None,
                multipath: dict = None, access_mode: str = None,
                hyper_metro_path_optimized: bool = None, task_remarks: str = None) -> dict:
    """
    修改存储主机

    Args:
        client: DME API 客户端
        storage_host_id: 存储主机 ID (必选)
        storage_host_name: 存储主机名称 (可选, 1~255个字符, 支持字母数字._-和中文字符)
        storage_host_description: 存储主机描述信息 (可选, 0~63个字符)
        storage_host_ip: 主机IP (可选, 最多127个字符)
        storage_host_os_type: 主机类型 (可选)。可选值：UNKNOWN, LINUX, WINDOWS, SUSE, EULER, REDHAT, CENTOS, WINDOWSSERVER2012, SOLARIS, LINUX_VIS, HPUX, AIX, XENSERVER, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC
        add_initiators: StorageInitiatorParam列表 (可选, 数组最大成员个数: 1000)。参数格式如下：[{
                protocol: 启动器类型 (必选)。可选值：fc, iscsi, nvme_over_roce,
                raw_id: 主机启动器wwpn或iqn或nqn (必选, 1~223个字符),
                alias: 启动器别名 (可选, 最多31个字符),
             }, ...]
        remove_initiators: 移除的启动器id列表 (可选, 数组最大成员个数: 1000)
        multipath: MultiPathForCreateRequestParam对象 (可选)。属性格式如下：{
                multipath_type: 第三方多路径策略 (必选)。可选值：default (默认), third_party (第三方多路径),
                path_type: 启动器路径类型 (可选, 开启第三方多路径时有效)。可选值：optimal_path (优选路径), non_optimal_path (非优选路径),
                failover_mode: 启动器切换模式 (可选, 开启第三方多路径时有效)。可选值：early_version_alua, common_alua, alua_not_used, special_alua,
                special_mode_type: 特殊模式类型 (可选, 切换模式为特殊模式时有效)。可选值：mode_zero, mode_one, mode_two, mode_three,
             }
        access_mode: 主机访问模式 (可选, 仅Dorado V6及以后产品)。可选值：balanced (均衡模式), asymmetric (非对称模式)
        hyper_metro_path_optimized: 双活优选路径 (可选, 仅Dorado V6及以后产品)。可选值：true, false
        task_remarks: 异步任务备注信息 (可选, 最多1024个字符)

    Returns:
        修改结果
    """
    url = "/rest/hostmgmt/v1/storage-hosts/{storage_host_id}"

    payload = {}

    if storage_host_name is not None:
        payload['storage_host_name'] = storage_host_name
    if storage_host_description is not None:
        payload['storage_host_description'] = storage_host_description
    if storage_host_ip is not None:
        payload['storage_host_ip'] = storage_host_ip

    payload = {}

    if storage_host_name is not None:
        payload['storage_host_name'] = storage_host_name
    if storage_host_description is not None:
        payload['storage_host_description'] = storage_host_description
    if storage_host_ip is not None:
        payload['storage_host_ip'] = storage_host_ip
    if storage_host_os_type is not None:
        payload['storage_host_os_type'] = storage_host_os_type
    if add_initiators is not None:
        payload['add_initiators'] = add_initiators
    if remove_initiators is not None:
        payload['remove_initiators'] = remove_initiators
    if multipath is not None:
        payload['multipath'] = multipath
    if access_mode is not None:
        payload['access_mode'] = access_mode
    if hyper_metro_path_optimized is not None:
        payload['hyper_metro_path_optimized'] = hyper_metro_path_optimized
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.put(url, body=payload, params={"storage_host_id": storage_host_id})
    return response


def storage_host_delete(client: DMEAPIClient, host_ids: list) -> dict:
    """
    批量删除存储主机

    批量删除指定的存储主机。

    Args:
        client: DME API 客户端
        host_ids: 存储主机 ID 列表（必选，最多 1000 个）

    Returns:
        删除结果
    """
    url = "/rest/hostmgmt/v1/storage-hosts/delete"

    payload = {
        'host_ids': host_ids
    }

    response = client.post(url, body=payload)
    return response


def storage_host_show_paths(client: DMEAPIClient, page_no: int = None, page_size: int = None,
                    storage_id: str = None, storage_host_ids: list = None,
                    storage_host_raw_ids: list = None, health_status: str = None,
                    running_status: str = None, initiator_type: str = None) -> dict:
    """
    批量查询存储主机的路径信息

    Args:
        client: DME API 客户端
        page_no: 分页查询的页码 (可选, 1~2147483647, 默认1)
        page_size: 分页查询的每页大小 (可选, 1~1000, 默认20)
        storage_id: 所属存储设备ID (可选, 1~64个字符)
        storage_host_ids: 所属存储主机的ID列表 (可选, 与storage_host_raw_ids二选一, 数组最大成员个数: 20; 单个ID长度1~64个字符)
        storage_host_raw_ids: 所属存储主机在设备上的ID列表 (可选, 与storage_host_ids二选一, 数组最大成员个数: 20; 单个ID长度1~64个字符)
        health_status: 健康状态 (可选)。可选值：normal (正常), fault (故障), no_redundant_link (无冗余路径), offline (离线)
        running_status: 链路状态 (可选)。可选值：link_up (已连接), link_down (未连接), online (在线), disabled (已禁用), connecting (正在连接)
        initiator_type: 启动器类型 (可选)。可选值：iSCSI, FC, NVMe_over_RoCE, IB, vHBA

    Returns:
        路径信息列表
    """
    url = "/rest/hostmgmt/v1/host-links/query"

    payload = {}

    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size
    if storage_id is not None:
        payload['storage_id'] = storage_id
    if storage_host_ids is not None:
        payload['storage_host_ids'] = storage_host_ids
    if storage_host_raw_ids is not None:
        payload['storage_host_raw_ids'] = storage_host_raw_ids
    if health_status is not None:
        payload['health_status'] = health_status
    if running_status is not None:
        payload['running_status'] = running_status
    if initiator_type is not None:
        payload['initiator_type'] = initiator_type

    response = client.post(url, body=payload)
    return response
# ============================================================================
# 存储主机组 (storage_host_group) 子主题函数
# ============================================================================

def storage_host_group_create(client: DMEAPIClient, storage_id: str, name: str,
                      description: str = None, exist_host_ids: list = None,
                      create_storage_host_params: dict = None,
                      task_remarks: str = None, vstore_id: str = None) -> dict:
    """
    创建存储主机组

    Args:
        client: DME API 客户端
        storage_id: 存储设备ID (必选, 1~64个字符)
        name: 主机组名称 (必选, 1~255个字符, 支持字母数字._-和中文字符; V3/V5设备最长31字节, V6设备最长255字节)
        description: 描述信息 (可选, 0~63个字符)
        exist_host_ids: 待添加至主机组的主机ID列表 (可选, 与create_storage_host_params互斥, 数组最大成员个数: 1000)
        create_storage_host_params: 创建新的存储主机列表 (可选, 与exist_host_ids互斥, 数组最大成员个数: 1000)。参数格式如下：[{
                name: 主机名称 (必选, 1~255个字符, 支持字母数字._-和中文字符),
                os_type: 主机类型 (必选)。可选值：LINUX, WINDOWS, WINDOWSSERVER2012, SOLARIS, HPUX, AIX, XENSERVER, LINUX_VIS, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC,
                ip: 主机ip地址 (可选, 最多127个字符),
                description: 主机描述 (可选, 最多63个字符),
                initiators: 启动器列表 (可选, 数组最大成员个数: 1000)。参数格式如下：[{
                        protocol: 启动器类型 (必选)。可选值：fc, iscsi, nvme_over_roce,
                        raw_id: 主机启动器wwpn或iqn或nqn (必选, 1~223个字符),
                        alias: 启动器别名 (可选, 最多31个字符),
                     }, ...],
                multipath: 多路径配置 (可选)。属性格式如下：{
                        multipath_type: 第三方多路径策略 (必选)。可选值：default (默认), third_party (第三方多路径),
                        path_type: 启动器路径类型 (可选, 开启第三方多路径时有效)。可选值：optimal_path (优选路径), non_optimal_path (非优选路径),
                        failover_mode: 启动器切换模式 (可选, 开启第三方多路径时有效)。可选值：early_version_alua, common_alua, alua_not_used, special_alua,
                        special_mode_type: 特殊模式类型 (可选, 切换模式为特殊模式时有效)。可选值：mode_zero, mode_one, mode_two, mode_three,
                }
             }, ...]
        task_remarks: 异步任务备注信息 (可选, 最多1024个字符)
        vstore_id: 租户ID (可选, 1~64个字符; 设备为OceanStor V300R006C30/V500R007C20/Dorado 6.1.3及以上时有效)

    Returns:
        任务 ID
    """
    url = "/rest/hostmgmt/v1/storage-hostgroups"

    payload = {
        'storage_id': storage_id,
        'name': name
    }

    if description is not None:
        payload['description'] = description
    if exist_host_ids is not None:
        payload['exist_host_ids'] = exist_host_ids
    if create_storage_host_params is not None:
        payload['create_storage_host_params'] = create_storage_host_params
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id

    response = client.post(url, body=payload)
    return response


def storage_host_group_list(client: DMEAPIClient, storage_id: str = None, name: str = None,
                    raw_id: str = None, vstore_id: str = None,
                    vstore_name: str = None, page_no: int = None,
                    page_size: int = None, sort_key: str = None,
                    sort_dir: str = None, avaiable_mapping_for_lun_group_id: str = None,
                    avaiable_mapping_for_lun_id: str = None,
                    support_provisioning: bool = None) -> dict:
    """
    批量查询存储主机组

    Args:
        client: DME API 客户端
        raw_id: 主机组在设备侧的ID (可选, 0~256个字符)
        storage_id: 设备ID (可选, 0~64个字符)
        page_size: 分页查询的个数 (可选, 1~1000, 默认100)
        page_no: 分页查询的页码 (可选, 1~10000000, 默认1)
        sort_dir: 排序方向 (可选, sort_key不填时不生效)。可选值：desc (降序), asc (升序)
        sort_key: 排序关键字 (可选)。可选值：name, host_count, lun_group_count, lun_count, raw_id
        name: 主机组名称 (可选, 0~256个字符, 支持模糊匹配)
        vstore_id: 租户ID (可选)
        vstore_name: 租户名称 (可选)
        avaiable_mapping_for_lun_group_id: 待映射的LUN组ID (可选, 0~64个字符; 查询可映射给指定LUN组的主机组时必传)
        avaiable_mapping_for_lun_id: 待映射的LUN ID (可选, 0~64个字符; 查询可映射给指定LUN的主机组时必传)
        support_provisioning: 是否支持发放 (可选)。可选值：true, false

    Returns:
        响应数据，包含存储主机组列表和总数
    """
    url = "/rest/hostmgmt/v1/storage-hostgroups/query"

    payload = {}

    if storage_id is not None:
        payload['storage_id'] = storage_id
    if name is not None:
        payload['name'] = name
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if vstore_id is not None:
        payload['vstore_id'] = vstore_id
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
    if avaiable_mapping_for_lun_group_id is not None:
        payload['avaiable_mapping_for_lun_group_id'] = avaiable_mapping_for_lun_group_id
    if avaiable_mapping_for_lun_id is not None:
        payload['avaiable_mapping_for_lun_id'] = avaiable_mapping_for_lun_id
    if support_provisioning is not None:
        payload['support_provisioning'] = support_provisioning

    response = client.post(url, body=payload)
    return response


def storage_host_group_add_hosts(client: DMEAPIClient, storage_host_group_id: str,
                         storage_host_id_ids: list = None,
                         create_storage_host_params: dict = None,
                         task_remarks: str = None) -> dict:
    """
    添加存储主机到存储主机组

    将现有主机添加到存储主机组，或在主机组中创建新主机。

    Args:
        client: DME API 客户端
        storage_host_group_id: 存储主机组 ID (必选)
        storage_host_id_ids: 存储主机ID列表 (可选, 与create_storage_host_params互斥, 数组最大成员个数: 1000)
        create_storage_host_params: 创建新的存储主机列表 (可选, 与storage_host_id_ids互斥, 数组最大成员个数: 1000)。参数格式如下：[{
                name: 主机名称 (必选, 1~255个字符, 支持字母数字._-和中文字符),
                os_type: 主机类型 (必选)。可选值：LINUX, WINDOWS, WINDOWSSERVER2012, SOLARIS, HPUX, AIX, XENSERVER, LINUX_VIS, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC,
                ip: 主机ip地址 (可选, 最多127个字符),
                description: 主机描述 (可选, 最多63个字符),
                initiators: 启动器列表 (可选, 数组最大成员个数: 1000)。参数格式如下：[{
                        protocol: 启动器类型 (必选)。可选值：fc, iscsi, nvme_over_roce,
                        raw_id: 主机启动器wwpn或iqn或nqn (必选, 1~223个字符),
                        alias: 启动器别名 (可选, 最多31个字符),
                     }, ...],
                multipath: 多路径配置 (可选)。属性格式如下：{
                        multipath_type: 第三方多路径策略 (必选)。可选值：default (默认), third_party (第三方多路径),
                        path_type: 启动器路径类型 (可选, 开启第三方多路径时有效)。可选值：optimal_path (优选路径), non_optimal_path (非优选路径),
                        failover_mode: 启动器切换模式 (可选, 开启第三方多路径时有效)。可选值：early_version_alua, common_alua, alua_not_used, special_alua,
                        special_mode_type: 特殊模式类型 (可选, 切换模式为特殊模式时有效)。可选值：mode_zero, mode_one, mode_two, mode_three,
                }
             }, ...]
        task_remarks: 异步任务备注信息 (可选, 最多1024个字符)

    Returns:
        任务 ID
    """
    url = "/rest/hostmgmt/v1/storage-hostgroups/{storage_host_group_id}/hosts/add"

    payload = {}

    if storage_host_id_ids is not None:
        payload['storage_host_id_ids'] = storage_host_id_ids
    if create_storage_host_params is not None:
        payload['create_storage_host_params'] = create_storage_host_params
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    payload = {}

    if storage_host_id_ids is not None:
        payload['storage_host_id_ids'] = storage_host_id_ids
    if create_storage_host_params is not None:
        payload['create_storage_host_params'] = create_storage_host_params
    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.put(url, body=payload, params={"storage_host_group_id": storage_host_group_id})
    return response


def storage_host_group_remove_hosts(client: DMEAPIClient, storage_host_group_id: str,
                            storage_host_ids: list,
                            task_remarks: str = None) -> dict:
    """
    从存储主机组中移除主机

    从指定的存储主机组中移除一个或多个主机。

    Args:
        client: DME API 客户端
        storage_host_group_id: 存储主机组 ID（必选，1~64 字符）
        storage_host_ids: 要移除的主机 ID 列表（必选，最多 1000 个）
        task_remarks: 任务备注（可选，最多 1024 字符）

    Returns:
        任务 ID
    """
    url = "/rest/hostmgmt/v1/storage-hostgroups/{storage_host_group_id}/hosts/remove"

    payload = {
        'storage_host_ids': storage_host_ids
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.put(url, params={"storage_host_group_id": storage_host_group_id})
    return response


def storage_host_group_delete(client: DMEAPIClient, host_group_ids: list,
                      task_remarks: str = None) -> dict:
    """
    批量删除存储主机组

    批量删除指定的存储主机组。

    Args:
        client: DME API 客户端
        host_group_ids: 存储主机组 ID 列表（必选，1~100 个）
        task_remarks: 任务备注（可选，最多 1024 字符）

    Returns:
        删除结果
    """
    url = "/rest/hostmgmt/v1/storage-hostgroups/delete"

    payload = {
        'host_group_ids': host_group_ids
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def storage_host_show_luns(client: DMEAPIClient, storage_host_id: str,
                   name: str = None, page_size: int = 20,
                   page_no: int = 1, sort_key: str = None,
                   sort_dir: str = None) -> dict:
    """
    查询存储主机映射的 LUN 信息列表

    指定存储主机查询映射 LUN 信息列表，包含 LUN 信息和主机 LUN ID 信息。

    Args:
        client: DME API 客户端
        storage_host_id: 存储主机 ID（必选，1~64 字符）
        name: LUN 名称（可选，1~256 字符，支持模糊搜索）
        page_size: 分页查询的个数（可选，1~1000，默认 20）
        page_no: 分页查询的起始位置（可选，1~10000000，默认 1）
        sort_key: 排序字段（可选，host_lun_id/mapping_view_raw_id/lun_raw_id）
        sort_dir: 排序方向（可选，asc/desc，默认 desc）

    Returns:
        响应数据，包含 total 和 lun_mapping_list
    """
    url = "/rest/blockservice/v1/lun-mapping/query"

    payload = {
        'storage_host_id': storage_host_id,
        'page_size': page_size,
        'page_no': page_no
    }

    if name is not None:
        payload['name'] = name
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


def storage_host_group_show_luns(client: DMEAPIClient, storage_host_group_id: str,
                         name: str = None, page_size: int = 20,
                         page_no: int = 1, sort_key: str = None,
                         sort_dir: str = None) -> dict:
    """
    查询存储主机组映射的 LUN 信息列表

    指定存储主机组查询映射 LUN 信息列表，包含 LUN 信息和主机 LUN ID 信息。

    Args:
        client: DME API 客户端
        storage_host_group_id: 存储主机组 ID（必选，1~64 字符）
        name: LUN 名称（可选，1~256 字符，支持模糊搜索）
        page_size: 分页查询的个数（可选，1~1000，默认 20）
        page_no: 分页查询的起始位置（可选，1~10000000，默认 1）
        sort_key: 排序字段（可选，host_lun_id/mapping_view_raw_id/lun_raw_id）
        sort_dir: 排序方向（可选，asc/desc，默认 desc）

    Returns:
        响应数据，包含 total 和 lun_mapping_list
    """
    url = "/rest/blockservice/v1/lun-mapping/query"

    payload = {
        'storage_host_group_id': storage_host_group_id,
        'page_size': page_size,
        'page_no': page_no
    }

    if name is not None:
        payload['name'] = name
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response
# ============================================================================
# 端口组 (port_group) 子主题函数
# ============================================================================

def port_group_list(client: DMEAPIClient, storage_id: str = None,
                    page_no: int = 1, page_size: int = 20) -> dict:
    """
    批量查询端口组

    Args:
        client: DME API 客户端
        storage_id: 存储设备ID (可选, 1~64个字符, 支持过滤)
        page_no: 分页查询的页码 (可选, 1~10000, 默认1)
        page_size: 分页查询的每页大小 (可选, 1~1000, 默认20)

    Returns:
        响应数据，包含端口组列表
    """
    url = "/rest/storagemgmt/v1/port-groups/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    if storage_id is not None:
        payload['storage_id'] = storage_id

    response = client.post(url, body=payload)
    return response


def port_group_create(client: DMEAPIClient, storage_id: str, name: str,
                      description: str = None, port_ids: list = None) -> dict:
    """
    创建端口组

    注意：仅支持 OceanStor 1800 系列存储。

    Args:
        client: DME API 客户端
        storage_id: 存储设备ID (必选, 1~64个字符)
        name: 端口组名称 (必选, 1~255个字符, 支持字母数字._-和中文字符)
        description: 端口组描述 (可选, 0~63个字符)
        port_ids: 关联到端口组的端口ID列表 (可选, 数组最大成员个数: 10; 只支持关联ROCE端口和逻辑端口, 只能关联其中一种)

    Returns:
        响应数据，包含新创建的端口组 ID
    """
    url = "/rest/storagemgmt/v1/port-groups"

    body_params = {
        'storage_id': storage_id,
        'name': name
    }

    if description is not None:
        body_params['description'] = description
    if port_ids is not None:
        body_params['port_ids'] = port_ids

    response = client.post(url, body=body_params)
    return response


def port_group_show_ports(client: DMEAPIClient, port_group_id: str,
                          type: str = None, page_no: int = 1,
                          page_size: int = 20) -> dict:
    """
    批量查询指定端口组的端口

    Args:
        client: DME API 客户端
        port_group_id: 端口组 ID (必选)
        type: 端口类型 (可选)。可选值：fc (FC端口), fcoe (FCoE端口), eth (以太网口), roce (RoCE端口)
        page_no: 分页查询的页码 (可选, 1~10000, 默认1)
        page_size: 分页查询的每页大小 (可选, 1~1000, 默认20)

    Returns:
        响应数据，包含端口列表
    """
    url = "/rest/storagemgmt/v1/port-groups/{port_group_id}/ports/query"

    payload = {}

    if type is not None:
        payload['type'] = type
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size

    payload = {}

    if type is not None:
        payload['type'] = type
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size

    response = client.post(url, body=payload)
    return response


def port_group_show_relations(client: DMEAPIClient, page_no: int = 1,
                              page_size: int = 20) -> dict:
    """
    批量查询端口组与端口关联关系

    Args:
        client: DME API 客户端
        page_no: 分页查询的页码 (可选, 1~10000, 默认1)
        page_size: 分页查询的每页大小 (可选, 1~1000, 默认20)

    Returns:
        响应数据，包含关联关系列表
    """
    url = "/rest/storagemgmt/v1/port-groups/ports/relations/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    response = client.post(url, body=payload)
    return response




# ============================================================================
# 动作列表，用于 CLI 帮助
# ============================================================================


# ============================================================================
# 物理主机 (physical_host) 子主题函数
# ============================================================================

def physical_host_list(client: DMEAPIClient, limit: int = None, start: int = None,
               sort_key: str = None, sort_dir: str = None, name: str = None,
               host_group_name: str = None, ip: str = None,
               display_status: str = None, managed_status: list = None,
               os_type: str = None, access_mode: str = None,
               az_id: str = None, az_ids: list = None,
               project_id: str = None) -> dict:
    """
    批量查询物理主机

    Args:
        client: DME API 客户端
        limit: 分页查询的个数 (可选, 1~1000)
        start: 分页查询的起始位置 (可选, 0~10000000)
        sort_key: 排序关键字 (可选)。可选值：initiator_count, ip, name
        sort_dir: 排序方向 (可选, sort_key不填时不生效)。可选值：desc (降序), asc (升序)
        name: 物理主机名称 (可选, 1~256个字符, 支持模糊匹配)
        host_group_name: 物理主机组名称 (可选, 1~256个字符, 支持模糊匹配)
        ip: 物理主机IP (可选, 1~256个字符, 支持模糊匹配)
        display_status: 展示状态 (可选, 1~32个字符)。可选值：OFFLINE (断开), NOT_RESPONDING (未响应), GRAY (未知), NORMAL (正常), RED (存在问题), YELLOW (可能存在问题), REBOOTING (重启中), INITIAL (初始化), BOOTING (重启), SHUTDOWNING (下电中)
        managed_status: 物理主机纳管状态列表 (可选, 数组最大成员个数: 1000)。可选值：UNKNOWN (未知), NORMAL (正常), TAKE_OVERING (纳管中), TAKE_ERROR (错误), TAKE_OVER_ALARM (纳管告警)
        os_type: 主机类型 (可选)。可选值：UNKNOWN, LINUX, WINDOWS, SUSE, EULER, REDHAT, CENTOS, WINDOWSSERVER2012, SOLARIS, LINUX_VIS, HPUX, AIX, XENSERVER, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC
        access_mode: 物理主机接入方式 (可选)。可选值：ACCOUNT (账号密码), NONE (手动接入), VCENTER (vCenter纳管), FUSIONSPHERE (FusionSphere纳管), HCS (HCS纳管), TPOPS (TPOPS纳管)
        az_id: 可用分区ID (可选, 1~64个字符; 当提供az_ids时此参数无效)
        az_ids: 可用分区ID列表 (可选, 数组最大成员个数: 40)
        project_id: 业务群组ID (可选, 1~64个字符)

    Returns:
        响应数据，包含物理主机列表和总数
    """
    url = "/rest/hostmgmt/v1/hosts/summary"

    payload = {}

    if limit is not None:
        payload['limit'] = limit
    if start is not None:
        payload['start'] = start
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if name is not None:
        payload['name'] = name
    if host_group_name is not None:
        payload['host_group_name'] = host_group_name
    if ip is not None:
        payload['ip'] = ip
    if display_status is not None:
        payload['display_status'] = display_status
    if managed_status is not None:
        payload['managed_status'] = managed_status
    if os_type is not None:
        payload['os_type'] = os_type
    if access_mode is not None:
        payload['access_mode'] = access_mode
    if az_id is not None:
        payload['az_id'] = az_id
    if az_ids is not None:
        payload['az_ids'] = az_ids
    if project_id is not None:
        payload['project_id'] = project_id

    response = client.post(url, body=payload)
    return response


def physical_host_show(client: DMEAPIClient, host_id: str) -> dict:
    """
    查询指定物理主机

    Args:
        client: DME API 客户端
        host_id: 物理主机 ID（必选）

    Returns:
        物理主机详细信息
    """
    url = "/rest/hostmgmt/v1/hosts/{host_id}/summary"

    response = client.get(url, params={"host_id": host_id})
    return response


def physical_host_create(client: DMEAPIClient, access_mode: str, type: str,
                host_name: str = None, ip: str = None, port: int = None,
                username: str = None, password: str = None,
                description: str = None, initiator: list = None,
                azs: list = None, project_id: str = None,
                sync_to_storage: bool = False, multipath_type: str = None,
                path_type: str = None, failover_mode: str = None,
                special_mode_type: str = None, save_public_key: bool = False) -> dict:
    """
    接入物理主机

    Args:
        client: DME API 客户端
        access_mode: 物理主机接入方式 (必选)。可选值：ACCOUNT (指定账号密码), NONE (手动录入)
        type: 主机类型 (必选)。可选值：UNKNOWN, LINUX, WINDOWS, SUSE, EULER, REDHAT, CENTOS, WINDOWSSERVER2012, SOLARIS, LINUX_VIS, HPUX, AIX, XENSERVER, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC。ACCOUNT模式仅支持LINUX
        host_name: 物理主机名称 (NONE模式必填, 1~255个字符, 支持字母数字._-和中文字符)
        ip: 物理主机IP地址 (ACCOUNT模式有效, 支持IPv4和IPv6, 最多127个字符)
        port: 物理主机接入端口 (ACCOUNT模式必填, 1~65535)
        username: 物理主机接入用户名 (ACCOUNT模式必填, 1~255个字符)
        password: 物理主机接入密码 (ACCOUNT模式必填, 1~1024个字符)
        description: 物理主机描述信息 (可选, 0~63个字符)
        initiator: 物理主机启动器列表 (NONE模式必填)。参数格式如下：[{
                protocol: 启动器类型 (必选)。可选值：FC, ISCSI, NVME_OVER_ROCE,
                port_name: 主机启动器wwn或iqn (必选, 1~223个字符),
             }, ...]
        azs: 可用分区ID列表 (可选, 数组最大成员个数: 40)
        project_id: 业务群组ID (可选, 1~64个字符)
        sync_to_storage: 自动同步已接入主机信息到存储 (可选, 默认false)。可选值：true, false
        multipath_type: 多路径类型 (可选)。可选值：default, third_party
        path_type: 启动器路径类型 (可选, 开启第三方多路径时有效)。可选值：optimal_path (优选路径), non_optimal_path (非优选路径)
        failover_mode: 启动器切换模式 (可选, 开启第三方多路径时有效)。可选值：early_version_alua, common_alua, alua_not_used, special_alua
        special_mode_type: 特殊模式类型 (可选, 切换模式为特殊模式时有效)。可选值：mode_zero, mode_one, mode_two, mode_three
        save_public_key: 是否自动保存物理主机公钥 (可选, 默认false)。可选值：true, false

    Returns:
        创建的物理主机信息
    """
    url = "/rest/hostmgmt/v1/hosts"

    payload = {
        'access_mode': access_mode,
        'type': type
    }

    if host_name is not None:
        payload['host_name'] = host_name
    if ip is not None:
        payload['ip'] = ip
    if port is not None:
        payload['port'] = port
    if username is not None:
        payload['username'] = username
    if password is not None:
        payload['password'] = password
    if description is not None:
        payload['description'] = description
    if initiator is not None:
        payload['initiator'] = initiator
    if azs is not None:
        payload['azs'] = azs
    if project_id is not None:
        payload['project_id'] = project_id
    if sync_to_storage is not None:
        payload['sync_to_storage'] = sync_to_storage
    if multipath_type is not None:
        payload['multipath_type'] = multipath_type
    if path_type is not None:
        payload['path_type'] = path_type
    if failover_mode is not None:
        payload['failover_mode'] = failover_mode
    if special_mode_type is not None:
        payload['special_mode_type'] = special_mode_type
    if save_public_key is not None:
        payload['save_public_key'] = save_public_key

    response = client.post(url, body=payload)
    return response


def physical_host_modify(client: DMEAPIClient, host_id: str,
                ip: str = None, host_name: str = None,
                os_type: str = None, azs: list = None,
                project_id: str = None) -> dict:
    """
    修改物理主机基本信息

    Args:
        client: DME API 客户端
        host_id: 物理主机 ID (必选)
        ip: 物理主机IP地址 (可选, 最多127个字符, 支持IPv4和IPv6; 不填表示不变)
        host_name: 物理主机名称 (可选, 1~255个字符, 支持字母数字._-; 为空表示保持不变)
        os_type: 主机类型 (可选)。可选值：LINUX, WINDOWS, WINDOWSSERVER2012, SOLARIS, HPUX, AIX, XENSERVER, LINUX_VIS, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC
        azs: 可用分区ID列表 (可选, 数组最大成员个数: 40; 空值或空列表表示解除az关联)
        project_id: 业务群组ID (可选, 0~64个字符; 不填表示不做修改; 空字符串表示解除project关联; 非空且与原值不一致表示关联至新project)

    Returns:
        修改结果
    """
    url = "/rest/hostmgmt/v1/hosts/{host_id}/general"

    payload = {}

    if ip is not None:
        payload['ip'] = ip
    if host_name is not None:
        payload['host_name'] = host_name
    if os_type is not None:
        payload['os_type'] = os_type

    payload = {}

    if ip is not None:
        payload['ip'] = ip
    if host_name is not None:
        payload['host_name'] = host_name
    if os_type is not None:
        payload['os_type'] = os_type
    if azs is not None:
        payload['azs'] = azs
    if project_id is not None:
        payload['project_id'] = project_id

    response = client.put(url, body=payload, params={"host_id": host_id})
    return response


def physical_host_modify_access_info(client: DMEAPIClient, host_id: str,
                ip: str = None, port: int = None, username: str = None,
                password: str = None, project_id: str = None,
                azs: list = None, sync_to_storage: bool = False,
                description: str = None, multipath_type: str = None,
                path_type: str = None, failover_mode: str = None,
                special_mode_type: str = None) -> dict:
    """
    修改物理主机接入信息

    Args:
        client: DME API 客户端
        host_id: 物理主机ID (必选, 1~64个字符)
        ip: 物理主机接入IP地址 (可选, 最多127个字符, 支持IPv4和IPv6; NONE转ACCOUNT场景必填)
        port: 物理主机接入端口 (可选, 1~65535; NONE转ACCOUNT场景必填)
        username: 物理主机接入用户名 (可选, 1~255个字符; NONE转ACCOUNT场景必填)
        password: 物理主机接入用户密码 (可选, 1~1024个字符; NONE转ACCOUNT场景必填)
        project_id: 业务群组ID (可选, 0~64个字符; 不填表示不做修改; 空字符串表示解除关联; 非空且与原值不一致表示关联至新project)
        azs: 可用分区ID列表 (可选, 数组最大成员个数: 40; 空值或空列表表示解除az关联)
        sync_to_storage: 是否同步修改存储主机信息 (可选, 默认false)。可选值：true (同步修改), false (不同步)
        description: 物理主机描述信息 (可选, 0~63个字符)
        multipath_type: 多路径类型 (可选)。可选值：default, third_party
        path_type: 启动器路径类型 (可选, 开启第三方多路径时有效)。可选值：optimal_path (优选路径), non_optimal_path (非优选路径)
        failover_mode: 启动器切换模式 (可选, 开启第三方多路径时有效)。可选值：early_version_alua, common_alua, alua_not_used, special_alua
        special_mode_type: 特殊模式类型 (可选, 切换模式为特殊模式时有效)。可选值：mode_zero, mode_one, mode_two, mode_three

    Returns:
        修改结果
    """
    url = "/rest/hostmgmt/v1/hosts/{host_id}/accessinfo"

    payload = {}

    if ip is not None:
        payload['ip'] = ip
    if port is not None:
        payload['port'] = port
    if username is not None:
        payload['username'] = username

    payload = {}

    if ip is not None:
        payload['ip'] = ip
    if port is not None:
        payload['port'] = port
    if username is not None:
        payload['username'] = username
    if password is not None:
        payload['password'] = password
    if project_id is not None:
        payload['project_id'] = project_id
    if azs is not None:
        payload['azs'] = azs
    if sync_to_storage is not None:
        payload['sync_to_storage'] = sync_to_storage
    if description is not None:
        payload['description'] = description
    if multipath_type is not None:
        payload['multipath_type'] = multipath_type
    if path_type is not None:
        payload['path_type'] = path_type
    if failover_mode is not None:
        payload['failover_mode'] = failover_mode
    if special_mode_type is not None:
        payload['special_mode_type'] = special_mode_type

    response = client.put(url, body=payload, params={"host_id": host_id})
    return response


def physical_host_delete(client: DMEAPIClient, host_id: str,
                sync_to_storage: bool = False) -> dict:
    """
    移除物理主机

    移除指定的物理主机。

    Args:
        client: DME API 客户端
        host_id: 物理主机 ID（必选）
        sync_to_storage: 是否同步从存储删除（可选，默认 false）

    Returns:
        删除结果
    """
    url = "/rest/hostmgmt/v1/hosts/{host_id}"

    response = client.delete(url, params={"host_id": host_id, "sync_to_storage": str(sync_to_storage).lower()})
    return response


def physical_host_add_initiators(client: DMEAPIClient, host_id: str,
                  initiators: list) -> dict:
    """
    为物理主机添加启动器

    Args:
        client: DME API 客户端
        host_id: 物理主机 ID (必选)
        initiators: 启动器列表 (必选, 数组最大成员个数: 100)。参数格式如下：[{
                protocol: 启动器类型 (必选)。可选值：FC (WWPN格式, 16字符十六进制), ISCSI, NVME_OVER_ROCE,
                port_name: 主机启动器wwn或iqn (必选, 1~223个字符),
             }, ...]

    Returns:
        添加结果
    """
    url = "/rest/hostmgmt/v1/hosts/{host_id}/initiators/add"

    payload = {
        'initiators': initiators
    }

    response = client.put(url, params={"host_id": host_id})
    return response


def physical_host_remove_initiators(client: DMEAPIClient, host_id: str,
                     initiators: list) -> dict:
    """
    从物理主机移除启动器

    Args:
        client: DME API 客户端
        host_id: 物理主机 ID（必选）
        initiators: 启动器 ID 列表（必选，最多 1000 个）

    Returns:
        移除结果
    """
    url = "/rest/hostmgmt/v1/hosts/{host_id}/initiators/remove"

    payload = {
        'initiators': initiators
    }

    response = client.put(url, params={"host_id": host_id})
    return response


def physical_host_show_initiators(client: DMEAPIClient, host_id: str,
                   port_name: str = None, protocol: str = None,
                   status: str = None) -> dict:
    """
    查询指定物理主机的启动器

    Args:
        client: DME API 客户端
        host_id: 物理主机 ID (必选)
        port_name: 物理主机启动器wwn或iqn (可选, 1~223个字符)
        protocol: 启动器类型 (可选, 1~64个字符)。可选值：UNKNOWN, FC, ISCSI, NVME_OVER_ROCE, SAS, NVME_OVER_FABRIC
        status: 启动器状态 (可选, 1~32个字符)。可选值：UNKNOWN, ONLINE, OFFLINE, UNBOUND

    Returns:
        启动器列表
    """
    url = "/rest/hostmgmt/v1/hosts/{host_id}/initiators"

    params = {}
    if port_name is not None:
        params['port_name'] = port_name
    if protocol is not None:
        params['protocol'] = protocol
    if status is not None:
        params['status'] = status


    params = {}
    if port_name is not None:
        params['port_name'] = port_name
    if protocol is not None:
        params['protocol'] = protocol
    if status is not None:
        params['status'] = status

    response = client.get(url, params=params)
    return response


def physical_host_test(client: DMEAPIClient, storage_id: str,
         host_ids: list = None, hostgroup_id: str = None,
         auto_zoning: bool = False,
         target_fcports: list = None,
         target_fcportgroups: list = None) -> dict:
    """
    检测存储设备和物理主机连通性

    Args:
        client: DME API 客户端
        storage_id: 存储设备 ID（必选）
        host_ids: 物理主机 ID 列表（可选，与 hostgroup_id 二选一）
        hostgroup_id: 物理主机组 ID（可选，与 host_ids 二选一）
        auto_zoning: 自动划 zone 策略（可选，默认 false）
        target_fcports: 端口 wwn 列表（可选，auto_zoning 为 true 时生效）
        target_fcportgroups: 端口组 id 列表（可选，auto_zoning 为 true 时生效）

    Returns:
        连通性检测结果
    """
    url = "/rest/hostmgmt/v1/connectivity/host-and-storage"

    payload = {
        'storage_id': storage_id
    }

    if host_ids is not None:
        payload['host_ids'] = host_ids
    if hostgroup_id is not None:
        payload['hostgroup_id'] = hostgroup_id
    if auto_zoning is not None:
        payload['auto_zoning'] = auto_zoning
    if target_fcports is not None:
        payload['target_fcports'] = target_fcports
    if target_fcportgroups is not None:
        payload['target_fcportgroups'] = target_fcportgroups

    response = client.post(url, body=payload)
    return response


def physical_host_save_sshkey(client: DMEAPIClient, ip: str, key: str,
                port: int = None) -> dict:
    """
    保存指定物理主机 SSH 公钥

    保存物理主机的 SSH 公钥，用于后续通信中检测通信物理主机的身份是否合法。

    Args:
        client: DME API 客户端
        ip: 物理主机 IP 地址（必选）
        key: 物理主机 SSH 公钥（必选）
        port: SSH 端口（可选，默认 22）

    Returns:
        保存结果
    """
    url = "/rest/hostmgmt/v1/host-keys"

    payload = {
        'ip': ip,
        'key': key
    }

    if port is not None:
        payload['port'] = port

    response = client.put(url, body=payload)
    return response


def physical_host_query_sshkey(client: DMEAPIClient, ip: str,
                 port: int = None) -> dict:
    """
    查询指定物理主机 SSH 公钥

    Args:
        client: DME API 客户端
        ip: 物理主机 IP 地址（必选）
        port: SSH 端口（可选，默认 22）

    Returns:
        SSH 公钥信息
    """
    url = "/rest/hostmgmt/v1/host-keys"

    params = {
        'ip': ip
    }

    if port is not None:
        params['port'] = port

    response = client.get(url, params=params)
    return response


def physical_host_query_by_initiator(client: DMEAPIClient, initiator_id: str = None,
                         raw_id: str = None, protocol: str = None) -> dict:
    """
    根据启动器查询关联的物理主机

    根据启动器 ID 或启动器 WWPN/IQN/NQN 查询关联的物理主机。

    Args:
        client: DME API 客户端
        initiator_id: 启动器 ID（可选，与 raw_id 互斥）
        raw_id: 启动器 WWPN/IQN/NQN（可选，与 initiator_id 互斥）
        protocol: 启动器类型（可选，FC/ISCSI/NVME_OVER_ROCE）

    Returns:
        关联的物理主机信息
    """
    url = "/rest/hostmgmt/v1/hosts/query-by-initiator"

    payload = {}

    if initiator_id is not None:
        payload['initiator_id'] = initiator_id
    if raw_id is not None:
        payload['raw_id'] = raw_id
    if protocol is not None:
        payload['protocol'] = protocol

    response = client.post(url, body=payload)
    return response


def physical_host_map_luns(client: DMEAPIClient, volume_ids: list, host_id: str,
            mapping_policy: list = None, task_remarks: str = None) -> dict:
    """
    LUN 映射给物理主机

    将 LUN 映射给指定的物理主机。

    Args:
        client: DME API 客户端
        volume_ids: LUN ID 列表 (必选, 数组最大成员个数: 1000)
        host_id: 物理主机 ID (必选, 1~64个字符)
        mapping_policy: MappingPolicy列表 (可选, 数组最大成员个数: 64; 服务化LUN不需要配置)。参数格式如下：[{
                storage_id: 存储设备ID (可选, 0~64个字符),
                start_host_lun_id: 起始主机LUN ID (可选, 0~4095),
                auto_zoning: 自动划zone (可选)。可选值：true (划zone), false (不划zone),
                zone_policy_id: zone策略ID (可选, 0~64个字符; auto_zoning为true时生效),
                target_fcports: 端口wwn列表 (可选, 与target_fcportgroups互斥, 数组最大成员个数: 1000; auto_zoning为true时生效),
                target_fcportgroups: 端口组ID列表 (可选, 与target_fcports互斥, 数组最大成员个数: 1000; auto_zoning为true时生效),
                mapping_view: MappingRequest对象 (可选)。属性格式如下：{
                        mapping_view_id: 映射视图在设备上的ID (可选, 最多31个字符),
                        mapping_view_name: 映射视图在设备上的名字 (可选, 最多31个字符),
                        lun_group_id: LUN组在设备上的ID (可选, 最多31个字符),
                        lun_group_name: LUN组在设备上的名称 (可选, 最多255个字符),
                        port_group_id: 端口组在设备上的ID (可选, 最多31个字符),
                }
             }, ...]
        task_remarks: 异步任务备注信息 (可选, 最多1024个字符)

    Returns:
        响应数据，包含 task_id
    """
    url = "/rest/blockservice/v1/volumes/host-mapping"

    payload = {
        'volume_ids': volume_ids,
        'host_id': host_id
    }

    if mapping_policy is not None:
        payload['mapping_policy'] = mapping_policy

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def physical_host_unmap_luns(client: DMEAPIClient, volume_ids: list, host_id: str,
              task_remarks: str = None) -> dict:
    """
    解除主机映射

    LUN 解除主机映射。

    Args:
        client: DME API 客户端
        volume_ids: LUN ID 列表 (必选, 数组最大成员个数: 1000)
        host_id: 主机 ID (必选, 1~64个字符)
        task_remarks: 异步任务备注信息 (可选, 最多1024个字符)

    Returns:
        响应数据，包含 task_id
    """
    url = "/rest/blockservice/v1/volumes/host-unmapping"

    payload = {
        'volume_ids': volume_ids,
        'host_id': host_id,
        'host_type': "host"
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def storage_host_unmap_luns(client: DMEAPIClient, volume_ids: list, host_id: str,
              task_remarks: str = None) -> dict:
    """
    解除存储主机映射

    解除 LUN 与存储主机的映射关系。

    Args:
        client: DME API 客户端
        volume_ids: LUN ID 列表 (必选, 数组最大成员个数: 1000)
        host_id: 主机 ID (必选, 1~64个字符)
        task_remarks: 异步任务备注信息 (可选, 最多1024个字符)

    Returns:
        响应数据，包含 task_id
    """
    url = "/rest/blockservice/v1/volumes/host-unmapping"

    payload = {
        'volume_ids': volume_ids,
        'host_id': host_id,
        'host_type': "storage_host"
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


# ============================================================================
# 物理主机组 (physical_host_group) 子主题函数
# ============================================================================

def physical_host_group_list(client: DMEAPIClient, limit: int = None, start: int = None,
         sort_dir: str = None, sort_key: str = None, name: str = None,
         project_id: str = None, az_ids: list = None,
         managed_status: list = None) -> dict:
    """
    批量查询物理主机组

    Args:
        client: DME API 客户端
        limit: 分页查询的个数 (可选, 1~1000)
        start: 分页查询的起始位置 (可选, 0~10000000)
        sort_dir: 排序方向 (可选, sort_key不填时不生效)。可选值：desc (降序), asc (升序)
        sort_key: 排序关键字 (可选, 1~255个字符)。可选值：host_count (主机组主机个数)
        name: 物理主机组名称 (可选, 1~256个字符, 支持模糊匹配)
        project_id: 所属业务群组ID (可选, 1~64个字符)
        az_ids: 所属可用分区ID列表 (可选, 数组最大成员个数: 1000; 单个ID长度1~64个字符)
        managed_status: 纳管状态列表 (可选, 数组最大成员个数: 1000)。可选值：UNKNOWN, NORMAL, TAKE_OVERING, TAKE_ERROR, TAKE_OVER_ALARM

    Returns:
        响应数据，包含物理主机组列表和总数
    """
    url = "/rest/hostmgmt/v1/hostgroups/summary"

    payload = {}

    if limit is not None:
        payload['limit'] = limit
    if start is not None:
        payload['start'] = start
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if name is not None:
        payload['name'] = name
    if project_id is not None:
        payload['project_id'] = project_id
    if az_ids is not None:
        payload['az_ids'] = az_ids
    if managed_status is not None:
        payload['managed_status'] = managed_status

    response = client.post(url, body=payload)
    return response


def physical_host_group_show_hosts(client: DMEAPIClient, hostgroup_id: str,
                name: str = None, ip: str = None,
                display_status: list = None, managed_status: list = None,
                os_type: list = None, sort_key: str = None,
                sort_dir: str = None, page_size: int = 1024,
                page_no: int = 1) -> dict:
    """
    查询物理主机组中的物理主机

    查询指定物理主机组的物理主机列表。

    Args:
        client: DME API 客户端
        hostgroup_id: 物理主机组ID (必选, 1~64个字符)
        name: 物理主机名称 (可选, 1~256个字符, 支持模糊匹配)
        ip: 物理主机IP (可选, 1~256个字符, 支持模糊匹配)
        display_status: 展示状态列表 (可选, 数组最大成员个数: 1000)。可选值：OFFLINE (断开), NOT_RESPONDING (未响应), GRAY (未知), NORMAL (正常), RED (存在问题), YELLOW (可能存在问题), REBOOTING (重启中), INITIAL (初始化), BOOTING (重启), SHUTDOWNING (下电中)
        managed_status: 纳管状态列表 (可选, 数组最大成员个数: 1000)。可选值：UNKNOWN, NORMAL, TAKE_OVERING, TAKE_ERROR, TAKE_OVER_ALARM
        os_type: 操作系统类型列表 (可选, 数组最大成员个数: 1000)。可选值：UNKNOWN, LINUX, WINDOWS, SUSE, EULER, REDHAT, CENTOS, WINDOWSSERVER2012, SOLARIS, HPUX, AIX, XENSERVER, MACOS, VMWAREESX, ORACLE, OPENVMS
        sort_key: 排序关键字 (可选)。可选值：ip, name
        sort_dir: 排序方向 (可选, sort_key不填时不生效)。可选值：desc (降序), asc (升序)
        page_size: 分页查询的个数 (可选, 1~1024, 默认1024)
        page_no: 分页查询的页码 (可选, 1~10000000, 默认1)

    Returns:
        物理主机列表
    """
    url = "/rest/hostmgmt/v1/hostgroups/{hostgroup_id}/hosts/list"

    payload = {}

    if name is not None:
        payload['name'] = name
    if ip is not None:
        payload['ip'] = ip
    if display_status is not None:
        payload['display_status'] = display_status

    payload = {}

    if name is not None:
        payload['name'] = name
    if ip is not None:
        payload['ip'] = ip
    if display_status is not None:
        payload['display_status'] = display_status
    if managed_status is not None:
        payload['managed_status'] = managed_status
    if os_type is not None:
        payload['os_type'] = os_type
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if page_size is not None:
        payload['page_size'] = page_size
    if page_no is not None:
        payload['page_no'] = page_no

    response = client.post(url, body=payload)
    return response


def physical_host_group_show(client: DMEAPIClient, hostgroup_id: str) -> dict:
    """
    查询指定物理主机组

    Args:
        client: DME API 客户端
        hostgroup_id: 物理主机组 ID（必选）

    Returns:
        物理主机组详细信息
    """
    url = "/rest/hostmgmt/v1/hostgroups/{hostgroup_id}/summary"

    response = client.get(url, params={"hostgroup_id": hostgroup_id})
    return response


def physical_host_group_create(client: DMEAPIClient, name: str, host_ids: list,
           azs: list = None, project_id: str = None,
           description: str = None) -> dict:
    """
    创建物理主机组

    指定物理主机创建物理主机组。

    Args:
        client: DME API 客户端
        name: 物理主机组名称 (必选, 1~255个字符, 支持字母数字._-和中文字符)
        host_ids: 物理主机ID列表 (必选, 数组最大成员个数: 100)
        azs: 可用分区ID列表 (可选, 数组最大成员个数: 40)
        project_id: 业务群组ID (可选, 1~64个字符)
        description: 物理主机组描述信息 (可选, 0~63个字符)

    Returns:
        创建的物理主机组信息
    """
    url = "/rest/hostmgmt/v1/hostgroups"

    payload = {
        'name': name,
        'host_ids': host_ids
    }

    if azs is not None:
        payload['azs'] = azs
    if project_id is not None:
        payload['project_id'] = project_id
    if description is not None:
        payload['description'] = description

    response = client.post(url, body=payload)
    return response


def physical_host_group_modify(client: DMEAPIClient, hostgroup_id: str,
           name: str = None, description: str = None,
           azs: list = None, project_id: str = None) -> dict:
    """
    修改物理主机组基本信息

    Args:
        client: DME API 客户端
        hostgroup_id: 物理主机组 ID (必选)
        name: 物理主机组名称 (可选, 1~255个字符, 支持字母数字._-和中文字符; 不填或空串表示不修改)
        description: 物理主机组描述信息 (可选, 0~63个字符)
        azs: 可用分区ID列表 (可选, 数组最大成员个数: 40; 空值或空列表表示解除az关联)
        project_id: 业务群组ID (可选, 0~64个字符; 不填表示不做修改; 空字符串表示解除关联; 非空且与原值不一致表示关联至新project)

    Returns:
        修改结果
    """
    url = "/rest/hostmgmt/v1/hostgroups/{hostgroup_id}/general"

    payload = {}

    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description
    if azs is not None:
        payload['azs'] = azs

    payload = {}

    if name is not None:
        payload['name'] = name
    if description is not None:
        payload['description'] = description
    if azs is not None:
        payload['azs'] = azs
    if project_id is not None:
        payload['project_id'] = project_id

    response = client.put(url, body=payload, params={"hostgroup_id": hostgroup_id})
    return response


def physical_host_group_delete(client: DMEAPIClient, hostgroup_id: str,
           sync_to_storage: bool = False) -> dict:
    """
    删除指定物理主机组

    Args:
        client: DME API 客户端
        hostgroup_id: 物理主机组 ID（必选）
        sync_to_storage: 是否同步从存储删除（可选，默认 false）

    Returns:
        删除结果
    """
    url = "/rest/hostmgmt/v1/hostgroups/{hostgroup_id}"

    response = client.delete(url, params={"hostgroup_id": hostgroup_id, "sync_to_storage": str(sync_to_storage).lower()})
    return response


def physical_host_group_add_hosts(client: DMEAPIClient, hostgroup_id: str,
             host_ids: list, sync_to_storage: bool = False) -> dict:
    """
    向物理主机组中增加物理主机

    Args:
        client: DME API 客户端
        hostgroup_id: 物理主机组 ID（必选）
        host_ids: 物理主机 ID 列表（必选，最多 100 个）
        sync_to_storage: 是否同步添加到存储（可选，默认 false）

    Returns:
        添加结果
    """
    url = "/rest/hostmgmt/v1/hostgroups/{hostgroup_id}/hosts/add"

    payload = {
        'host_ids': host_ids
    }

    response = client.put(url, body=payload, params={"hostgroup_id": hostgroup_id, "sync_to_storage": str(sync_to_storage).lower()})
    return response


def physical_host_group_remove_hosts(client: DMEAPIClient, hostgroup_id: str,
                host_ids: list, sync_to_storage: bool = False) -> dict:
    """
    物理主机组移除物理主机

    从物理主机组中移除物理主机。

    Args:
        client: DME API 客户端
        hostgroup_id: 物理主机组 ID（必选）
        host_ids: 物理主机 ID 列表（必选，最多 1000 个）
        sync_to_storage: 是否同步从存储移除（可选，默认 false）

    Returns:
        移除结果
    """
    url = "/rest/hostmgmt/v1/hostgroups/{hostgroup_id}/hosts/remove"

    payload = {
        'host_ids': host_ids
    }

    response = client.put(url, body=payload, params={"hostgroup_id": hostgroup_id, "sync_to_storage": str(sync_to_storage).lower()})
    return response


def physical_host_group_map_luns(client: DMEAPIClient, volume_ids: list, hostgroup_id: str,
            mapping_policy: list = None, task_remarks: str = None) -> dict:
    """
    LUN 映射给物理主机组

    将 LUN 映射给指定的物理主机组。

    Args:
        client: DME API 客户端
        volume_ids: LUN ID 列表 (必选, 数组最大成员个数: 1000)
        hostgroup_id: 物理主机组 ID (必选, 0~64个字符)
        mapping_policy: MappingPolicy列表 (可选)。参数格式如下：[{
                storage_id: 存储设备ID (可选, 0~64个字符),
                start_host_lun_id: 起始主机LUN ID (可选, 0~4095),
                auto_zoning: 自动划zone (可选)。可选值：true (划zone), false (不划zone),
                zone_policy_id: zone策略ID (可选, 0~64个字符; auto_zoning为true时生效),
                target_fcports: 端口wwn列表 (可选, 与target_fcportgroups互斥, 数组最大成员个数: 1000; auto_zoning为true时生效),
                target_fcportgroups: 端口组ID列表 (可选, 与target_fcports互斥, 数组最大成员个数: 1000; auto_zoning为true时生效),
                mapping_view: MappingRequest对象 (可选)。属性格式如下：{
                        mapping_view_id: 映射视图在设备上的ID (可选, 最多31个字符),
                        mapping_view_name: 映射视图在设备上的名字 (可选, 最多31个字符),
                        lun_group_id: LUN组在设备上的ID (可选, 最多31个字符),
                        lun_group_name: LUN组在设备上的名称 (可选, 最多255个字符),
                        port_group_id: 端口组在设备上的ID (可选, 最多31个字符),
                }
             }, ...]
        task_remarks: 异步任务备注信息 (可选, 最多1024个字符)

    Returns:
        响应数据，包含 task_id
    """
    url = "/rest/blockservice/v1/volumes/hostgroup-mapping"

    payload = {
        'volume_ids': volume_ids,
        'hostgroup_id': hostgroup_id
    }

    if mapping_policy is not None:
        payload['mapping_policy'] = mapping_policy

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def physical_host_group_unmap_luns(client: DMEAPIClient, volume_ids: list, hostgroup_id: str,
              task_remarks: str = None) -> dict:
    """
    解除主机组映射

    解除 LUN 与主机组的映射关系。

    Args:
        client: DME API 客户端
        volume_ids: LUN ID 列表 (必选, 数组最大成员个数: 1000)
        hostgroup_id: 主机组 ID (必选, 1~64个字符)
        task_remarks: 异步任务备注信息 (可选, 最多1024个字符)

    Returns:
        响应数据，包含 task_id
    """
    url = "/rest/blockservice/v1/volumes/hostgroup-unmapping"

    payload = {
        'volume_ids': volume_ids,
        'hostgroup_id': hostgroup_id,
        'host_group_type': "host_group"
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


def storage_host_group_unmap_luns(client: DMEAPIClient, volume_ids: list, hostgroup_id: str,
              task_remarks: str = None) -> dict:
    """
    解除存储主机组映射

    解除 LUN 与存储主机组的映射关系。

    Args:
        client: DME API 客户端
        volume_ids: LUN ID 列表 (必选, 数组最大成员个数: 1000)
        hostgroup_id: 主机组 ID (必选, 1~64个字符)
        task_remarks: 异步任务备注信息 (可选, 最多1024个字符)

    Returns:
        响应数据，包含 task_id
    """
    url = "/rest/blockservice/v1/volumes/hostgroup-unmapping"

    payload = {
        'volume_ids': volume_ids,
        'hostgroup_id': hostgroup_id,
        'host_group_type': "storage_host_group"
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response


# ============================================================================
# 动作列表，用于 CLI 帮助
# ============================================================================

ACTIONS = {
    # LUN 子主题动作（san lun xxx）
    'lun_list': {
        'func': lun_list,
        'description': '批量查询 LUN',
        'params': ['limit', 'offset', 'sort_dir', 'sort_key', 'name', 'vstore_raw_id', 'vstore_name', 'status', 'health_status', 'service_level_id', 'volume_wwn', 'storage_id', 'pool_raw_id', 'host_id', 'hostgroup_id', 'unmapped_host_id', 'unmapped_hostgroup_id', 'project_id', 'allocate_type', 'attached', 'query_mode', 'protected', 'pg_id', 'usage_type', 'support_provisioning'],
        'subtopic': 'lun'
    },
    'lun_show': {
        'func': lun_show,
        'description': '查询指定 LUN',
        'params': ['volume_id'],
        'subtopic': 'lun'
    },
    'lun_create': {
        'func': lun_create,
        'description': '自定义创建 LUN',
        'params': ['storage_id', 'lun_specs', 'lun_specs_pass_through', 'pool_id', 'vstore_id', 'owner_controller', 'initial_distribute_policy', 'prefetch_policy', 'prefetch_value', 'tuning', 'mapping', 'task_remarks'],
        'subtopic': 'lun'
    },
    'lun_delete': {
        'func': lun_delete,
        'description': '批量删除 LUN',
        'params': ['volume_ids', 'task_remarks'],
        'subtopic': 'lun'
    },
    'lun_modify': {
        'func': lun_modify,
        'description': '修改指定 LUN',
        'params': ['volume_id', 'name', 'description', 'owner_controller', 'prefetch_policy', 'prefetch_value', 'tuning', 'task_remarks'],
        'subtopic': 'lun'
    },
    'lun_modify_name': {
        'func': lun_modify_name,
        'description': '批量修改 LUN 名称',
        'params': ['volumes'],
        'subtopic': 'lun'
    },
    'lun_expand': {
        'func': lun_expand,
        'description': '批量扩容 LUN',
        'params': ['volumes', 'task_remarks'],
        'subtopic': 'lun'
    },
    'lun_connection': {
        'func': lun_connection,
        'description': '查询指定 LUN ID 的连接信息',
        'params': ['volume_ids'],
        'subtopic': 'lun'
    },

    # LUN 组子主题动作（san lun_group xxx）
    'lun_group_list': {
        'func': lun_group_list,
        'description': '批量查询 LUN 组',
        'params': ['page_size', 'page_no', 'sort_dir', 'sort_key', 'name', 'vstore_raw_id', 'vstore_name', 'storage_id', 'storage_name', 'raw_id', 'attached', 'protection_group_raw_id', 'avaiable_mapping_for_host_id', 'avaiable_mapping_for_host_group_id', 'support_provisioning'],
        'subtopic': 'lun_group'
    },
    'lun_group_show': {
        'func': lun_group_show,
        'description': '查询指定 LUN 组详情',
        'params': ['group_id', 'storage_id'],
        'subtopic': 'lun_group'
    },
    'lun_group_create': {
        'func': lun_group_create,
        'description': '创建 LUN 组',
        'params': ['storage_id', 'name', 'description', 'existing_lun_ids', 'customize_volumes', 'task_remarks', 'vstore_id', 'zoning_info', 'mapping_view'],
        'subtopic': 'lun_group'
    },
    'lun_group_delete': {
        'func': lun_group_delete,
        'description': '批量删除 LUN 组',
        'params': ['lun_group_ids', 'task_remarks'],
        'subtopic': 'lun_group'
    },
    'lun_group_add_luns': {
        'func': lun_group_add_luns,
        'description': '向 LUN 组添加 LUN',
        'params': ['group_id', 'existing_lun_ids', 'customize_volumes', 'host_lun_id_infos', 'host_lun_id_verify', 'task_remarks'],
        'subtopic': 'lun_group'
    },
    'lun_group_remove_luns': {
        'func': lun_group_remove_luns,
        'description': '从 LUN 组移除 LUN',
        'params': ['group_id', 'lun_ids', 'task_remarks'],
        'subtopic': 'lun_group'
    },
    'lun_group_show_luns': {
        'func': lun_group_show_luns,
        'description': '查询 LUN 组中的 LUN',
        'params': ['group_id', 'page_size', 'page_no', 'health_status'],
        'subtopic': 'lun_group'
    },
    # 映射视图子主题动作（san mapping_view xxx）
    'mapping_view_create': {
        'func': mapping_view_create,
        'description': '创建映射视图',
        'params': ['storage_id', 'name', 'port_group_id', 'start_host_lun_id',
                   'host', 'vbs', 'host_group', 'lun_group', 'luns',
                   'task_remarks'],
        'subtopic': 'mapping_view'
    },
    'mapping_view_delete': {
        'func': mapping_view_delete,
        'description': '批量删除映射视图',
        'params': ['mapping_view_ids'],
        'subtopic': 'mapping_view'
    },
    'mapping_view_list': {
        'func': mapping_view_list,
        'description': '批量查询映射视图列表',
        'params': ['page_size', 'page_no', 'name', 'raw_id', 'storage_id',
                   'lun_id', 'lun_name', 'lun_group_id', 'lun_group_raw_id',
                   'lun_group_name', 'storage_host_id', 'storage_host_name',
                   'storage_host_group_id', 'storage_host_group_name',
                   'storage_host_group_raw_id', 'port_group_id', 'port_group_raw_id',
                   'port_group_name', 'sort_key', 'sort_dir'],
        'subtopic': 'mapping_view'
    },

    # 存储主机子主题动作（san storage_host xxx）
    'storage_host_create': {
        'func': storage_host_create,
        'description': '创建存储主机',
        'params': ['storage_id', 'host_info', 'task_remarks', 'vstore_id'],
        'subtopic': 'storage_host'
    },
    'storage_host_batch_query': {
        'func': storage_host_batch_query,
        'description': '根据存储主机 ID 列表批量查询存储主机',
        'params': ['ids'],
        'subtopic': 'storage_host'
    },
    'storage_host_list': {
        'func': storage_host_list,
        'description': '批量查询存储主机',
        'params': ['page_size', 'page_no', 'sort_key', 'sort_dir', 'name', 'raw_id', 'host_group_id',
                   'avaliable_add_to_host_group_id', 'host_group_name', 'ip', 'health_status', 'os_type',
                   'storage_id', 'avaiable_mapping_for_lun_group_id', 'avaiable_mapping_for_lun_id',
                   'support_provisioning', 'manufacturer', 'vstore_raw_id', 'vstore_name'],
        'subtopic': 'storage_host'
    },
    'storage_host_modify': {
        'func': storage_host_modify,
        'description': '修改存储主机',
        'params': ['storage_host_id', 'storage_host_name', 'storage_host_description', 'storage_host_ip',
                   'storage_host_os_type', 'add_initiators', 'remove_initiators', 'multipath', 'access_mode',
                   'hyper_metro_path_optimized', 'task_remarks'],
        'subtopic': 'storage_host'
    },
    'storage_host_delete': {
        'func': storage_host_delete,
        'description': '批量删除存储主机',
        'params': ['host_ids'],
        'subtopic': 'storage_host'
    },
    'storage_host_show_paths': {
        'func': storage_host_show_paths,
        'description': '批量查询存储主机的路径信息',
        'params': ['page_no', 'page_size', 'storage_id', 'storage_host_ids', 'storage_host_raw_ids',
                   'health_status', 'running_status', 'initiator_type'],
        'subtopic': 'storage_host'
    },
    'storage_host_show_luns': {
        'func': storage_host_show_luns,
        'description': '查询存储主机映射的 LUN 信息列表',
        'params': ['storage_host_id', 'name', 'page_size', 'page_no', 'sort_key', 'sort_dir'],
        'subtopic': 'storage_host'
    },
    'storage_host_unmap_luns': {
        'func': storage_host_unmap_luns,
        'description': '解除存储主机映射',
        'params': ['volume_ids', 'host_id', 'task_remarks'],
        'subtopic': 'storage_host'
    },
    # 存储主机组子主题动作（san storage_host_group xxx）
    'storage_host_group_create': {
        'func': storage_host_group_create,
        'description': '创建存储主机组',
        'params': ['storage_id', 'name', 'description', 'exist_host_ids', 'create_storage_host_params', 'task_remarks', 'vstore_id'],
        'subtopic': 'storage_host_group'
    },
    'storage_host_group_list': {
        'func': storage_host_group_list,
        'description': '批量查询存储主机组',
        'params': ['storage_id', 'name', 'raw_id', 'vstore_id', 'vstore_name', 'page_no', 'page_size',
                   'sort_key', 'sort_dir', 'avaiable_mapping_for_lun_group_id', 'avaiable_mapping_for_lun_id',
                   'support_provisioning'],
        'subtopic': 'storage_host_group'
    },
    'storage_host_group_add_hosts': {
        'func': storage_host_group_add_hosts,
        'description': '添加存储主机到存储主机组',
        'params': ['storage_host_group_id', 'storage_host_id_ids', 'create_storage_host_params', 'task_remarks'],
        'subtopic': 'storage_host_group'
    },
    'storage_host_group_remove_hosts': {
        'func': storage_host_group_remove_hosts,
        'description': '从存储主机组中移除主机',
        'params': ['storage_host_group_id', 'storage_host_ids', 'task_remarks'],
        'subtopic': 'storage_host_group'
    },
    'storage_host_group_delete': {
        'func': storage_host_group_delete,
        'description': '批量删除存储主机组',
        'params': ['host_group_ids', 'task_remarks'],
        'subtopic': 'storage_host_group'
    },
    'storage_host_group_show_luns': {
        'func': storage_host_group_show_luns,
        'description': '查询存储主机组映射的 LUN 信息列表',
        'params': ['storage_host_group_id', 'name', 'page_size', 'page_no', 'sort_key', 'sort_dir'],
        'subtopic': 'storage_host_group'
    },
    'storage_host_group_unmap_luns': {
        'func': storage_host_group_unmap_luns,
        'description': '解除存储主机组映射',
        'params': ['volume_ids', 'hostgroup_id', 'task_remarks'],
        'subtopic': 'storage_host_group'
    },
    # 端口组子主题动作（san port_group xxx）
    'port_group_list': {
        'func': port_group_list,
        'description': '批量查询端口组',
        'params': ['storage_id', 'page_no', 'page_size'],
        'subtopic': 'port_group'
    },
    'port_group_create': {
        'func': port_group_create,
        'description': '创建端口组',
        'params': ['storage_id', 'name', 'description', 'port_ids'],
        'subtopic': 'port_group'
    },
    'port_group_show_ports': {
        'func': port_group_show_ports,
        'description': '批量查询指定端口组的端口',
        'params': ['port_group_id', 'type', 'page_no', 'page_size'],
        'subtopic': 'port_group'
    },
    'port_group_show_relations': {
        'func': port_group_show_relations,
        'description': '批量查询端口组与端口关联关系',
        'params': ['page_no', 'page_size'],
        'subtopic': 'port_group'
    },
    # 物理主机子主题动作（san physical_host xxx）
    'physical_host_list': {
        'func': physical_host_list,
        'description': '批量查询物理主机',
        'params': ['limit', 'start', 'sort_key', 'sort_dir', 'name',
                   'host_group_name', 'ip', 'display_status', 'managed_status',
                   'os_type', 'access_mode', 'az_id', 'az_ids', 'project_id'],
        'subtopic': 'physical_host'
    },
    'physical_host_show': {
        'func': physical_host_show,
        'description': '查询指定物理主机',
        'params': ['host_id'],
        'subtopic': 'physical_host'
    },
    'physical_host_create': {
        'func': physical_host_create,
        'description': '接入物理主机',
        'params': ['access_mode', 'type', 'host_name', 'ip', 'port',
                   'username', 'password', 'description', 'initiator',
                   'azs', 'project_id', 'sync_to_storage', 'multipath_type',
                   'path_type', 'failover_mode', 'special_mode_type', 'save_public_key'],
        'subtopic': 'physical_host'
    },
    'physical_host_modify': {
        'func': physical_host_modify,
        'description': '修改物理主机基本信息',
        'params': ['host_id', 'ip', 'host_name', 'os_type', 'azs', 'project_id'],
        'subtopic': 'physical_host'
    },
    'physical_host_modify_access_info': {
        'func': physical_host_modify_access_info,
        'description': '修改物理主机接入信息',
        'params': ['host_id', 'ip', 'port', 'username', 'password', 'project_id', 'azs', 'sync_to_storage', 'description', 'multipath_type', 'path_type', 'failover_mode', 'special_mode_type'],
        'subtopic': 'physical_host'
    },
    'physical_host_delete': {
        'func': physical_host_delete,
        'description': '移除物理主机',
        'params': ['host_id', 'sync_to_storage'],
        'subtopic': 'physical_host'
    },
    'physical_host_add_initiators': {
        'func': physical_host_add_initiators,
        'description': '为物理主机添加启动器',
        'params': ['host_id', 'initiators'],
        'subtopic': 'physical_host'
    },
    'physical_host_remove_initiators': {
        'func': physical_host_remove_initiators,
        'description': '从物理主机移除启动器',
        'params': ['host_id', 'initiators'],
        'subtopic': 'physical_host'
    },
    'physical_host_show_initiators': {
        'func': physical_host_show_initiators,
        'description': '查询指定物理主机的启动器',
        'params': ['host_id', 'port_name', 'protocol', 'status'],
        'subtopic': 'physical_host'
    },
    'physical_host_test': {
        'func': physical_host_test,
        'description': '检测存储设备和物理主机连通性',
        'params': ['storage_id', 'host_ids', 'hostgroup_id', 'auto_zoning', 'target_fcports', 'target_fcportgroups'],
        'subtopic': 'physical_host'
    },
    'physical_host_query_sshkey': {
        'func': physical_host_query_sshkey,
        'description': '查询指定物理主机SSH公钥',
        'params': ['ip', 'port'],
        'subtopic': 'physical_host'
    },
    'physical_host_save_sshkey': {
        'func': physical_host_save_sshkey,
        'description': '保存指定物理主机SSH公钥',
        'params': ['ip', 'key', 'port'],
        'subtopic': 'physical_host'
    },
    'physical_host_query_by_initiator': {
        'func': physical_host_query_by_initiator,
        'description': '根据启动器查询关联的物理主机',
        'params': ['initiator_id', 'raw_id', 'protocol'],
        'subtopic': 'physical_host'
    },
    'physical_host_map_luns': {
        'func': physical_host_map_luns,
        'description': 'LUN映射给物理主机',
        'params': ['volume_ids', 'host_id', 'mapping_policy', 'task_remarks'],
        'subtopic': 'physical_host'
    },
    'physical_host_unmap_luns': {
        'func': physical_host_unmap_luns,
        'description': '解除主机映射',
        'params': ['volume_ids', 'host_id', 'task_remarks'],
        'subtopic': 'physical_host'
    },
    'physical_host_show_mapping_views': {
        'func': physical_host_show_mapping_views,
        'description': '查询物理主机关联的映射关系',
        'params': ['host_id', 'storage_id'],
        'subtopic': 'physical_host'
    },
    # 物理主机组子主题动作（san physical_host_group xxx）
    'physical_host_group_list': {
        'func': physical_host_group_list,
        'description': '批量查询物理主机组',
        'params': ['limit', 'start', 'sort_dir', 'sort_key', 'name', 'project_id', 'az_ids', 'managed_status'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_show_hosts': {
        'func': physical_host_group_show_hosts,
        'description': '查询物理主机组中的物理主机',
        'params': ['hostgroup_id', 'name', 'ip', 'display_status', 'managed_status', 'os_type', 'sort_key', 'sort_dir', 'page_size', 'page_no'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_show': {
        'func': physical_host_group_show,
        'description': '查询指定物理主机组',
        'params': ['hostgroup_id'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_create': {
        'func': physical_host_group_create,
        'description': '创建物理主机组',
        'params': ['name', 'host_ids', 'azs', 'project_id', 'description'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_modify': {
        'func': physical_host_group_modify,
        'description': '修改物理主机组基本信息',
        'params': ['hostgroup_id', 'name', 'description', 'azs', 'project_id'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_delete': {
        'func': physical_host_group_delete,
        'description': '删除指定物理主机组',
        'params': ['hostgroup_id', 'sync_to_storage'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_add_hosts': {
        'func': physical_host_group_add_hosts,
        'description': '向物理主机组中增加物理主机',
        'params': ['hostgroup_id', 'host_ids', 'sync_to_storage'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_remove_hosts': {
        'func': physical_host_group_remove_hosts,
        'description': '物理主机组移除物理主机',
        'params': ['hostgroup_id', 'host_ids', 'sync_to_storage'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_map_luns': {
        'func': physical_host_group_map_luns,
        'description': 'LUN映射给物理主机组',
        'params': ['volume_ids', 'hostgroup_id', 'mapping_policy', 'task_remarks'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_unmap_luns': {
        'func': physical_host_group_unmap_luns,
        'description': '解除物理主机组映射',
        'params': ['volume_ids', 'hostgroup_id', 'task_remarks'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_show_mapping_views': {
        'func': physical_host_group_show_mapping_views,
        'description': '查询物理主机组关联的映射关系',
        'params': ['host_group_id', 'storage_id'],
        'subtopic': 'physical_host_group'
    }
}
