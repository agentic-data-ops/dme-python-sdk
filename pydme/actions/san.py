"""
SAN (Storage Area Network) 相关操作
包含LUN、LUN组、mapping view、Storage host、Storage host group、端口组等子主题
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
    批量query LUN
    
    Args:
        client: DME API client
        limit: 分页query的个数 (可选, 0~1000, default1000)
        offset: 分页query的起始location (可选, 最小值0, default0)
        sort_dir: 排序方向 (Optional). valid values: asc (升序), desc (降序)
        sort_key: 排序字段 (Optional). valid values: name, size, alloc_capacity, capacity_usage, protection_capacity
        name: LUN name (可选, 1~256个字符, supports fuzzy query)
        vstore_raw_id: Storage device上分配的tenant ID (可选, 1~64个字符)
        vstore_name: 租户name (可选, 1~256个字符, supports fuzzy query)
        status: status (可选, 已废弃, 建议使用health_status). valid values: creating (create中), normal (正常), mapping (映射中), unmapping (解除映射中), deleting (delete中), error (错误), expanding (扩容中), faulty (故障), write_protected (写保护)
        health_status: health status (Optional). valid values: normal (正常), faulty (故障), write_protected (写保护)
        service_level_id: 服务等级ID (可选, 1~64个字符)
        volume_wwn: LUN WWN (可选, 1~128个字符)
        storage_id: storage device ID (可选, 1~36个字符, UUID格式或32位十六进制)
        pool_raw_id: Storage pool在Storage device上的ID (可选, 1~64个字符; 需同时指定storage_id)
        host_id: host ID (可选, 1~64个字符, UUID格式或32位十六进制)
        hostgroup_id: host group ID (可选, 1~64个字符, UUID格式或32位十六进制)
        unmapped_host_id: 未映射host ID (可选, 1~64个字符)
        unmapped_hostgroup_id: 未映射host group ID (可选, 1~64个字符)
        project_id: 业务群组ID (可选, 1~64个字符)
        allocate_type: allocation type (Optional). valid values: thin, thick
        attached: 映射status (Optional). valid values: true (已映射), false (未映射)
        query_mode: LUN发放模式 (Optional). valid values: service (服务化LUN), non-service (非服务LUN), all (所有LUN)
        protected: LUN保护status (Optional). valid values: true (已被保护), false (未被保护)
        pg_id: 保护组ID (可选, 1~64个字符, UUID格式或32位十六进制)
        usage_type: LUN使用type (Optional). valid values: traditional (传统LUN), edev (eDevLUN)
        support_provisioning: 过滤query可发放变更的LUN (Optional). valid values: true (仅query可发放变更), false (query全量)
    
    Returns:
        {
            count: LUNcount (int32),
            volumes: LUNlist (List<Volume>). parameter format: [{
                id: LUN的唯一标识 (string, 1~64个字符),
                pid: 保护发放业务ID (string, 1~64个字符),
                name: name (string, 1~255个字符),
                nguid: Namespace全局唯一标识符 (string, 1~256个字符),
                vstore_raw_id: tenant ID (string, 1~64个字符),
                vstore_name: 租户name (string, 1~256个字符),
                description: descriptioninfo (string, 0~255个字符),
                status: status (string). valid values: creating, normal, mapping, unmapping, deleting, error, expanding, faulty, write_protected,
                health_status: health status (string). valid values: normal (正常), faulty (故障), write_protected (写保护),
                attached: 映射status. valid values: true (已映射), false (未映射),
                project_id: 业务群组id (string, 1~64个字符),
                alloctype: allocation type. valid values: thin (按需分配), thick (固定分配),
                usage_type: 使用type. valid values: traditional (传统LUN), edev (eDevLUN),
                capacity: capacity (int32, GB). 注: 建议使用total_capacity,
                total_capacity: total capacity (int64, 字节),
                alloc_capacity: 已分配capacity (int64, 字节),
                service_level_name: 服务等级name (string, 1~64个字符),
                attachments: 映射info (List<Attachment>). parameter format: [{
                    id: 映射关系ID (string),
                    volume_id: LUN唯一标识 (string),
                    host_id: 主机id (string),
                    host_name: 主机name (string),
                    attached_at: 映射时间 (string),
                    attached_host_group: 主机组id (string),
                    host_group_name: 主机组name (string),
                }, ...],
                volume_raw_id: LUN在Storage device上的id (string, 1~64个字符),
                volume_wwn: LUN在Storage device上的wwn (string, 1~64个字符),
                pool_raw_id: storage池在设备上的id (string, 1~64个字符),
                capacity_usage: capacity利用率 (string),
                protected: 保护status. valid values: true (已保护), false (未保护),
                updated_at: update time (string),
                created_at: creation time (string),
                function_type: LUNtype. valid values: lun (普通LUN), snapshot (快照), clone (克隆),
                remote_lun_wwn: 外部LUN的WWN (string),
                take_over_lun_wwn: 接管LUN的WWN (string),
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
    query指定 LUN. 

    Args:
        client: DME API client
        volume_id: LUN id (必选, string, 1~64个字符)

    Returns:
        {
            volume: LUN详细info (VolumeDetailsobject). attribute format: {
                id: LUN的唯一标识 (string, 1~64个字符),
                name: name (string, 1~255个字符),
                description: descriptioninfo (string, 0~255个字符),
                status: status (string). valid values: creating (create中), normal (正常), mapping (映射中), unmapping (解除映射中), deleting (delete中), error (错误), expanding (扩容中), faulty (故障), write_protected (写保护),
                attached: 映射status (boolean, true,false),
                alloctype: allocation type (string). valid values: thin (按需分配), thick (固定分配),
                total_capacity: total capacity, 单位GB (double),
                storage_id: Storage deviceid (string, 1~64个字符),
                storage_name: storage device name (string, 1~64个字符),
                pool_id: LUNstorage池的id (string, 1~64个字符),
                volume_wwn: LUN在Storage device上的wwn (string, 1~64个字符),
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
    自定义create LUN

    Args:
        client: DME API client
        storage_id: Storage device ID (必填), 1~64 个字符, 通过Storage devicequery接口获取
        lun_specs: 待create LUN 基本参数 (条件必传), List<LunSpecs> type, max array members 1000, 单次最多可create 10 组; 与 lun_specs_pass_through 互斥; 当Storage device模式不为直通模式时必传. parameter format: [{
                name: LUN name (1~255个字符, 支持字母数字._-和中文字符; 当count>1时name为1~27个字符),
                count: 该规格LUNcount (1~500),
                capacity: 单个LUN capacity (1~262144, 单位GB),
                suffix_length: 命名后缀规则 (1~4; name长度+后缀长度<=255),
                start_suffix: 起始后缀编号 (1~9999; count+起始后缀<=9999),
                start_lun_id: 起始LUN ID (1~65535),
                usage_type: LUN使用type. valid values: traditional (传统LUN), edev (eDevLUN),
                write_policy: 回写策略. valid values: back (回写), through (透写),
                remote_lun_raw_id: 外部LUN ID (0~255个字符; 当usage_type为edev时生效),
                disguise_status: LUN伪装 (当usage_type为edev时生效). valid values: nodisguise (不伪装), basic (基本伪装), expansion (扩展伪装), inheritance (继承伪装),
             }, ...]
        lun_specs_pass_through: 直通模式Storage device待create LUN 基本参数 (条件必传), List<lunSpecsPassThrough> type, max array members 24, 单次最多可create 24 组; 与 lun_specs 互斥; 当Storage device模式为直通模式时必传. parameter format: [{
                name: LUN name (1~247个字符, 支持字母数字-._和中文字符; 最终name由LUN name+后缀编码+'-'+硬盘location组成),
                description: LUNdescription (0~255个字符),
                disk_location: createLUN的硬盘location (1~255个字符),
                count: 每个硬盘create的LUNcount (1~8),
                suffix_length: 后缀编码位数 (1~4, default4; 当count大于1时有效),
                start_suffix: 后缀起始编码 (0~9999, default0; 当count大于1时有效),
             }, ...]
        pool_id: Storage pool ID (条件必传), 1~64 个字符; 当Storage device模式不为直通模式时必传; 通过query指定resource type的所有实例接口获取, Storage pool的resource typename为 SYS_StoragePool
        vstore_id: 租户 ID(Optional), 1~64 个字符; 当设备为 OceanStor V300R006C00、OceanStor V500R007C00、OceanStor Dorado 6.1.3、OceanStor 6.1.3 及其以上version时有效
        owner_controller: 归属Controller(Optional), 1~64 个字符, 通过query指定存储上的Controller获取
        initial_distribute_policy: capacity初始分配策略(Optional), 仅支持华为 V3/V5 设备, Dorado 系列不支持; 
                                  valid values: automatic (自动)、highest_performance (高性能层)、performance (性能层)、capacity (capacity层); default automatic
        prefetch_policy: 预取策略(Optional), 影响磁盘读取; 
                        valid values: no_prefetch (不预取)、constant_prefetch (固定预取)、variable_prefetch (可变预取)、intelligent_prefetch (智能预取); default intelligent_prefetch
        prefetch_value: 预取策略值(Optional), 0~1024; 下发了 prefetch_policy 且其值为固定或可变预取时需要下发; 固定预取取值范围 0~1024KB, 可变预取取值范围 0~1024 倍
        tuning: 调优属性 (Optional), CustomizeLunTuning object. parameter format: {
                smart_tier: data migration policy. valid values: no_migration (不迁移), automatic_migration (automatic migration), migration_to_higher (migration to higher tier), migration_to_lower (migration to lower tier). defaultno_migration,
                deduplication_enabled: deduplication (仅Thin LUN支持). valid values: true (true), false (false),
                compression_enabled: compression (仅Thin LUN支持). valid values: true (true), false (false),
                alloction_type: LUNallocation type. valid values: thin, thick,
                smart_qos: Smart QoSobject. attribute format: {
                        max_bandwidth: max bandwidth (1~999999999Mbit/s; 与min_bandwidth/min_iops互斥),
                        max_iops: max IOPS (1~999999999; 与min_bandwidth/min_iops互斥),
                        min_bandwidth: min bandwidth (1~999999999Mbit/s; 与max_bandwidth/max_iops互斥),
                        min_iops: min IOPS (1~999999999; 与max_bandwidth/max_iops互斥),
                        latency: latency (1~999999999ms; Dorado V6系列单位为us, 可选值为500/1500; 与max_bandwidth/max_iops互斥),
                },
                workload_type_raw_id: workload type ID (0~4294967295; 通过query指定Storage device上应用type接口获取),
             }
        mapping: 映射info (Optional), LunMapping object, 存在即表示为主机或主机组create LUN. parameter format: {
                host_id: host ID (1~64个字符; 与hostgroup_id二选其一, 不可同时存在),
                hostgroup_id: host group ID (1~64个字符; 与host_id二选其一, 不可同时存在),
                host_type: 映射主机type. valid values: storage_host (Storage host), host (主机). defaulthost,
                start_host_lun_id: 起始主机LUN ID (1~4096),
                mapping_view: mapping view请求info (LunMappingRequestobject). attribute format: {
                        mapping_view_raw_id: mapping view在Storage device上的ID (1~31个字符),
                        mapping_view_name: mapping view在Storage device上的name (1~31个字符),
                        lun_group_raw_id: LUN组在Storage device上的ID (1~31个字符),
                        lun_group_name: LUN组在Storage device上的name (1~255个字符),
                        port_group_raw_id: 端口组在Storage device上的ID (1~31个字符; 主机或主机组不存在映射关系时可指定, 存在映射关系时不可指定),
                },
             }
        task_remarks: 异步任务备注info(Optional), 最多 1024 个字符

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    批量delete LUN. 

    Args:
        client: DME API client
        volume_ids: LUN ID list (必选, List[string], max array members: 1000)
        task_remarks: 异步任务备注info (可选, string, 最多1024个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    modify指定 LUN

    Args:
        client: DME API client
        volume_id: LUN ID
        name: 新name (可选, 1~255 个字符)
        description: modify LUN descriptioninfo (可选, 0~255 个字符)
        owner_controller: 归属Controller (可选, 仅非服务化 LUN 支持modify)
        prefetch_policy: 预取策略 (可选, 仅非服务化 LUN 支持modify)
                        valid values: 0 (不预取), 1 (固定预取), 2 (可变预取), 3 (智能预取)
        prefetch_value: 预取策略值 (可选, 仅非服务化 LUN 支持modify)
        tuning: LUN 调优属性 (可选, 仅非服务化LUN支持modify). parameter format: {
                smarttier: data migration policy (可选, default0). valid values: 0 (不迁移), 1 (automatic migration), 2 (migration to higher tier), 3 (migration to lower tier),
                smartqos: SmartQos4Updateobject (Optional). attribute format: {
                        maxbandwidth: max bandwidth (可选, 0~2147483647; 支持所有设备; 用于V3/V5系列时与minbandwidth/miniops互斥),
                        maxiops: 最大iops (可选, 0~2147483647; 支持所有设备; 用于V3/V5系列时与minbandwidth/miniops互斥),
                        minbandwidth: min bandwidth (可选, 0~2147483647; 支持Dorado V6/V3/V5; 用于V3/V5系列时与maxbandwidth/maxiops互斥),
                        miniops: 最小iops (可选, 0~2147483647; 支持Dorado V6/V3/V5; 用于V3/V5系列时与maxbandwidth/maxiops互斥),
                        control_policy: 控制策略 (Optional). valid values: 0 (保护IO下限), 1 (控制IO上限),
                        latency: latencyms或us (可选, 0~2147483647; 需根据不同Storage device指定; 仅保护下限支持),
                        enabled: 是否启用smartqos (Optional). valid values: true, false,
                }
             }
        task_remarks: 异步任务备注info (可选, 最多 1024 个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    批量modify LUN name

    Args:
        client: DME API client
        volumes: 待modify的 LUN infolist (max array members: 1000). parameter format: [{
                volume_id: LUN唯一标识 (1~64个字符),
                name: LUN新name (1~255个字符, 支持字母数字._-和中文字符),
             }, ...]

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
        client: DME API client
        volumes: 需要扩容的 LUN infolist (max array members: 1000). parameter format: [{
                volume_id: LUN唯一标识 (必选, 1~64个字符),
                added_capacity: 扩容capacityGB (必选, 1~262144),
             }, ...]
        task_remarks: 异步任务备注info (可选, 最多 1024 个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    query指定 LUN ID 的连接info. 

    Args:
        client: DME API client
        volume_ids: LUN ID list (必选, List[string], max array members: 1000)

    Returns:
        {
            lun_id: LUN ID (string),
            lun_wwn: LUN WWN (string),
            iscsi_targets: iSCSI 目标list (List),
            fc_targets: FC 目标list (List),
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
    批量query LUN group

    query LUN grouplist, 支持分页和多种过滤条件. 

    Args:
        client: DME API client
        page_size: 分页query的个数 (可选, 0~1000, default20)
        page_no: pagination start page (可选, 1~10000000, default1)
        sort_dir: 排序方向 (Optional). valid values: asc (升序), desc (降序)
        sort_key: 排序字段 (Optional). valid values: lun_count (LUNcount), total_capcity (total capacity), capacity_usage (used capacity), name, raw_id (设备侧ID)
        name: LUN组name (可选, 1~256个字符, supports fuzzy query)
        vstore_raw_id: Storage device上分配的tenant ID (可选, 1~64个字符)
        vstore_name: 租户name (可选, 1~256个字符, supports fuzzy query)
        storage_id: storage device ID (可选, 1~64个字符)
        storage_name: 存储name (可选, 1~256个字符, supports fuzzy query)
        raw_id: LUN组在Storage device上的ID (可选, 1~256个字符)
        attached: 映射status (Optional). valid values: true (已映射), false (未映射)
        protection_group_raw_id: 保护组在Storage device上的ID (可选, 0~64个字符; 非空则query保护组下的LUN组, 空串则query未加入保护组的LUN组)
        avaiable_mapping_for_host_id: 可映射的host ID (可选, 1~64个字符; 与avaiable_mapping_for_host_group_id互斥)
        avaiable_mapping_for_host_group_id: 可映射的host group ID (可选, 1~64个字符; 与avaiable_mapping_for_host_id互斥)
        support_provisioning: 是否支持发放 (Optional). valid values: true (支持), false (不支持)

    Returns:
        {
            total: LUN组total (integer),
            lun_groups: LUN组list (List<LunGroupInfo>). parameter format: [{
                id: LUN组ID (string),
                name: LUN组name (string),
                storage_id: storage device ID (string),
                lun_count: LUNcount (integer),
                attached: 映射status (boolean),
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
    query指定 LUN groupdetails. 

    Args:
        client: DME API client
        group_id: LUN group ID (必选, string)
        storage_id: Storage device ID (可选, string)

    Returns:
        {
            id: LUN组ID (string),
            name: LUN组name (string),
            storage_id: storage device ID (string),
            lun_count: LUNcount (integer),
            description: description (string),
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
    create LUN group

    create新的 LUN group. 

    Args:
        client: DME API client
        storage_id: Storage device ID (必选, 1~64个字符)
        name: LUN groupname (必选, 1~255个字符, 支持字母数字._-和中文字符)
        description: LUN groupdescription (可选, 0~255个字符)
        existing_lun_ids: LUN ID list (可选, 与customize_volumes互斥, max array members: 1000)
        customize_volumes: CustomizeVolumesParamobject (可选, 与existing_lun_ids互斥). parameter format: {
                volume_specs: VolumeSpecsParamlist (可选, 与lun_specs_pass_through互斥, max array members: 1000). parameter format: [{
                        name: LUN name (必选, 1~255个字符, 支持字母数字._-和中文字符; count>1时name长度1~27字符),
                        description: LUNdescription (可选, 0~255个字符),
                        count: 该规格LUNcount (必选, 1~500),
                        capacity: 该规格LUN capacityGB (必选, 1~262144),
                        suffix_length: LUN命名后缀规则 (可选, 0~4; name长度+后缀长度<=255),
                        start_suffix: 该规格LUN起始后缀编号 (可选, 0~9999),
                        start_lun_id: 该规格起始LUN ID (可选, 0~65535),
                     }, ...],
                lun_specs_pass_through: lunSpecsPassThroughlist (可选, 与volume_specs互斥, max array members: 24; 当Storage device模式为直通模式时必传). parameter format: [{
                        name: LUN name (必选, 1~247个字符, 支持字母数字-._和中文字符; 最终name由LUN name+后缀编码+硬盘location组成),
                        description: LUNdescription (可选, 0~255个字符),
                        disk_location: createLUN的硬盘location (必选, 1~255个字符),
                        count: 每个硬盘create的LUNcount (必选, 1~8),
                        suffix_length: 后缀编码位数 (可选, 1~4, default4; count>1时有效),
                        start_suffix: 后缀起始编码 (可选, 0~9999, default0; count>1时有效),
                     }, ...],
                pool_raw_id: Storage pool在Storage device上的id (可选, 1~64个字符; 设备模式不为直通模式时必传),
                availability_zone: 可用分区id (可选, 0~64个字符),
                owner_controller: 归属Controller (可选, 0~64个字符),
                initial_distribute_policy: capacity初始分配策略 (可选, 仅V3/V5设备, 全闪存不支持). valid values: 0 (自动), 1 (高性能层), 2 (性能层), 3 (capacity层). default0,
                prefetch_policy: 预取策略 (Optional). valid values: 0 (不预取), 1 (固定预取), 2 (可变预取), 3 (智能预取). default3,
                prefetch_value: 预取策略值 (可选, 0~1024; 固定预取0~1024KB, 可变预取0~1024倍),
                tuning: CustomizeVolumeTuningobject (Optional). attribute format: {
                        smartqos: SmartQosobject (Optional). attribute format: {
                                name: Smart QoSname (可选, 1~255个字符),
                        },
                        alloctype: LUNallocation type (Optional). valid values: thin, thick,
                        workload_type_id: 应用typeid (可选, 从Storage device上获取),
                }
             }
        task_remarks: 异步任务备注info (可选, 最多1024个字符)
        vstore_id: tenant ID (可选, 1~64个字符; 当设备为OceanStor V300R006C30/V500R007C20/Dorado 6.1.3/6.1.3及以上version时有效)
        zoning_info: ZoningParamobject (Optional). parameter format: {
                zone_policy_id: zone策略id (可选, 0~64个字符; 指定则自动划zone),
                target_fcports: 端口wwnlist (可选, 与target_fcportgroups二选其一, max array members: 1000; 当mapping_view中port_group_id为空时生效),
                target_fcportgroups: 端口组idlist (可选, 与target_fcports二选其一, max array members: 1000; 当mapping_view中port_group_id为空时生效),
             }
        mapping_view: MappingViewRequestParamobject (Optional). parameter format: {
                mapping_view_name: mapping view在设备上的名字 (可选, 最多31个字符),
                mapping_host_info: MappingHostInfoobject (可选, 与mapping_host_group_info二选其一). attribute format: {
                        todo_host_name: todo任务中的host name (可选, 1~255个字符, 支持字母数字._-和中文字符),
                        id: host ID (可选, 1~64个字符),
                },
                mapping_host_group_info: MappingHostGroupInfoobject (可选, 与mapping_host_info二选其一). attribute format: {
                        todo_host_group_name: todo任务中的host group name (可选, 1~255个字符, 支持字母数字._-和中文字符),
                        id: host group ID (可选, 1~64个字符),
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
    批量delete LUN group

    Args:
        client: DME API client
        lun_group_ids: LUN组IDlist (必选, max array members: 500)
        task_remarks: 异步任务备注info (可选, 最多1024个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    向 LUN group添加 LUN

    Args:
        client: DME API client
        group_id: LUN group ID
        existing_lun_ids: 已有LUN集合 (可选, 与customize_volumes互斥, max array members: 1000). parameter format: [{
                lun_id: 已有LUN ID (必选, 1~64个字符),
             }, ...]
        customize_volumes: CustomizeVolumesParamobject (可选, 与existing_lun_ids互斥). parameter format: {
                volume_specs: VolumeSpecsParamlist (可选, 与lun_specs_pass_through互斥, max array members: 1000). parameter format: [{
                        name: LUN name (必选, 1~255个字符, 支持字母数字._-和中文字符; count>1时name长度1~27字符),
                        description: LUNdescription (可选, 0~255个字符),
                        count: 该规格LUNcount (必选, 1~500),
                        capacity: 该规格LUN capacityGB (必选, 1~262144),
                        suffix_length: LUN命名后缀规则 (可选, 0~4; name长度+后缀长度<=255),
                        start_suffix: 该规格LUN起始后缀编号 (可选, 0~9999),
                        start_lun_id: 该规格起始LUN ID (可选, 0~65535),
                     }, ...],
                lun_specs_pass_through: lunSpecsPassThroughlist (可选, 与volume_specs互斥, max array members: 24; 直通模式时必传). parameter format: [{
                        name: LUN name (必选, 1~247个字符, 支持字母数字-._和中文字符; 最终name由LUN name+后缀编码+硬盘location组成),
                        description: LUNdescription (可选, 0~255个字符),
                        disk_location: createLUN的硬盘location (必选, 1~255个字符),
                        count: 每个硬盘create的LUNcount (必选, 1~8),
                        suffix_length: 后缀编码位数 (可选, 1~4, default4; count>1时有效),
                        start_suffix: 后缀起始编码 (可选, 0~9999, default0; count>1时有效),
                     }, ...],
                pool_raw_id: Storage pool在Storage device上的id (可选, 1~64个字符; 设备模式不为直通模式时必传),
                availability_zone: 可用分区id (可选, 0~64个字符),
                owner_controller: 归属Controller (可选, 0~64个字符),
                initial_distribute_policy: capacity初始分配策略 (可选, 仅V3/V5, 全闪存不支持). valid values: 0 (自动), 1 (高性能层), 2 (性能层), 3 (capacity层). default0,
                prefetch_policy: 预取策略 (Optional). valid values: 0 (不预取), 1 (固定预取), 2 (可变预取), 3 (智能预取). default3,
                prefetch_value: 预取策略值 (可选, 0~1024; 固定预取0~1024KB, 可变预取0~1024倍),
                tuning: CustomizeVolumeTuningobject (Optional). attribute format: {
                        smartqos: SmartQosobject (Optional). attribute format: {
                                name: Smart QoSname (可选, 1~255个字符),
                        },
                        alloctype: LUNallocation type (Optional). valid values: thin, thick,
                        workload_type_id: 应用typeid (Optional),
                }
             }
        host_lun_id_infos: HostLunIdInfolist (可选, max array members: 1000; 仅Dorado V6/V7和OceanStor V6/V7设备支持). parameter format: [{
                host_lun_id: LUN指定的主机LUN ID (必选, 0~4095),
                lun_id: 加入LUN组的LUN ID (必选, 1~64个字符),
             }, ...]
        host_lun_id_verify: 是否进行双活主机LUN ID一致性校验 (可选, defaultfalse). valid values: true (不校验), false (校验)
        task_remarks: 异步任务备注info (可选, 最多1024个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
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
    从 LUN group移除 LUN

    Args:
        client: DME API client
        group_id: LUN group ID
        lun_ids: LUN ID list (必选, 数组最小成员个数: 1, max array members: 10000)
        task_remarks: 异步任务备注info (可选, 最多1024个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/blockservice/v1/lun-groups/{group_id}/remove-luns"

    body_params = {
        'lun_ids': lun_ids
    }

    if task_remarks is not None:
        body_params['task_remarks'] = task_remarks

    response = client.post(url, body=body_params, params={"group_id": group_id})
    return response


def lun_group_show_luns(client: DMEAPIClient, group_id: str,
                         page_size: int = 100, page_no: int = 1,
                         health_status: str = None) -> dict:
    """
    query LUN group中的 LUN

    Args:
        client: DME API client
        group_id: LUN group ID
        page_size: 分页query的个数 (可选, 1~1000, default100)
        page_no: 分页query的页码 (可选, 1~10000000, default1)
        health_status: health status (Optional). valid values: normal (正常), faulty (故障), write_protected (写保护)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含 LUN list
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


# action list, for CLI help

# ============================================================================
# mapping view (mapping_view) 子主题函数
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
    createmapping view

    Args:
        client: DME API client
        storage_id: Storage device ID (必选, 1~64个字符)
        name: mapping viewname (可选, 1~31个字符; 设备type为OceanStor V3/V5时有效)
        port_group_id: 端口组 ID (可选, 1~64个字符)
        start_host_lun_id: 主机LUN SCSI ID起始值 (可选, 0~2147483647)
        host: Storage host (可选, 与vbs/host_group互斥). attribute format: {
                todo_host_name: todo任务中的host name (可选, 1~255个字符, 支持字母数字._-和中文字符),
                id: host ID (可选, 1~64个字符),
             }
        vbs: VBS客户端 (可选, 与host/host_group互斥; 仅OceanStor Pacific和FusionStorage支持). attribute format: {
                id: VBS ID (可选, 1~64个字符),
             }
        host_group: Storage host group (可选, 与host/vbs互斥). attribute format: {
                todo_host_group_name: todo任务中的host group name (可选, 1~255个字符, 支持字母数字._-和中文字符),
                id: host group ID (可选, 1~64个字符),
             }
        lun_group: 待映射的LUN组 (可选, 与luns互斥). attribute format: {
                id: LUN组ID (可选, 1~64个字符),
             }
        luns: 待映射的LUNinfo (可选, 与lun_group互斥). attribute format: {
                ids: 待映射的LUN IDlist (可选, max array members: 1000),
                lungroup_name: LUN组name (可选, 1~255个字符; lun映射时需create指定namelun组时下发),
             }
        task_remarks: 异步任务备注info (可选, 最多1024个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
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
    批量deletemapping view. 

    Args:
        client: DME API client
        ids: mapping view ID list (必选, List[string])

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
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
    批量querymapping viewlist

    批量queryStorage device上的mapping viewinfo, 支持多种过滤条件. 

    Args:
        client: DME API client
        page_size: 分页query的个数 (可选, 0~1000, default100)
        page_no: 分页query的起始location (可选, 1~10000000, default1)
        name: mapping viewname (可选, 0~256个字符, 支持模糊搜索)
        raw_id: mapping view在Storage device上的ID (可选, 1~256个字符)
        storage_id: Storage device的唯一标识 (可选, 0~64个字符)
        lun_id: LUN的唯一标识 (可选, 0~64个字符; 与lun_name参数不支持同时下发)
        lun_name: LUN name (可选, 1~256个字符, 支持模糊搜索; 与lun_id参数不支持同时下发)
        lun_group_id: LUN组的唯一标识 (可选, 0~64个字符; 与lun_group_raw_id/lun_group_name不支持同时下发)
        lun_group_raw_id: 设备侧分配的LUN组ID (可选, 1~64个字符; 与lun_group_id/lun_group_name不支持同时下发)
        lun_group_name: LUN组name (可选, 1~256个字符, supports fuzzy query; 与lun_group_id/lun_group_raw_id不支持同时下发)
        storage_host_id: Storage host的唯一标识 (可选, 0~64个字符; 与storage_host_name不支持同时下发)
        storage_host_name: 存储host name (可选, 0~256个字符, 支持模糊搜索; 仅OceanStor Dorado v6和OceanProtect X支持; 与storage_host_id不支持同时下发)
        storage_host_group_id: Storage host group的唯一标识 (可选, 0~64个字符; 与storage_host_group_name/storage_host_group_raw_id不支持同时下发)
        storage_host_group_name: 存储host group name (可选, 0~256个字符, 支持模糊搜索; 与storage_host_group_id/storage_host_group_raw_id不支持同时下发)
        storage_host_group_raw_id: 设备侧分配的存储host group ID (可选, 1~64个字符; 与storage_host_group_id/storage_host_group_name不支持同时下发)
        port_group_id: 端口组的唯一标识 (可选, 0~64个字符; 与port_group_raw_id/port_group_name不支持同时下发)
        port_group_raw_id: 设备侧分配的port group ID (可选, 1~64个字符; 与port_group_id/port_group_name不支持同时下发)
        port_group_name: port group name (可选, 0~256个字符, 支持模糊搜索; 与port_group_id/port_group_raw_id不支持同时下发)
        sort_key: 排序字段 (Optional). valid values: raw_id, storage_host_group_raw_id, lun_group_raw_id, port_group_raw_id
        sort_dir: 排序方向 (Optional). valid values: asc (升序), desc (降序)

    Returns:
        {
            total: mapping viewtotal (integer),
            mapping_views: mapping viewlist (List<MappingViewInfo>). parameter format: [{
                id: mapping viewID (string),
                name: mapping viewname (string),
                storage_id: storage device ID (string),
            }, ...],
        }
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




def mapping_view_query(
    client: DMEAPIClient,
    type: str,
    request_id: str,
    storage_id: str
) -> dict:
    """
    query物理主机 (组)关联的映射关系

    根据物理主机/主机组 ID 过滤query指定Storage device上的mapping view. 

    Args:
        client: DME API client
        type: query类别 (Required). valid values: host (物理主机), host_group (主机组)
        request_id: 物理主机/主机组 ID (必选, 1~64个字符)
        storage_id: Storage device ID (必选, 1~64个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含mapping viewlist
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
    query物理主机关联的映射关系

    Args:
        client: DME API client
        host_id: 物理主机 ID (必选, 1~64个字符)
        storage_id: Storage device ID (必选, 1~64个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含mapping viewlist
    """
    return mapping_view_query(
        client=client, type="host",
        request_id=host_id, storage_id=storage_id
    )


def physical_host_group_show_mapping_views(client: DMEAPIClient, host_group_id: str,
                                            storage_id: str) -> dict:
    """
    query物理主机组关联的映射关系

    Args:
        client: DME API client
        host_group_id: 物理主机组 ID (必选, 1~64个字符)
        storage_id: Storage device ID (必选, 1~64个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含mapping viewlist
    """
    return mapping_view_query(
        client=client, type="host_group",
        request_id=host_group_id, storage_id=storage_id
    )


# ============================================================================
# Storage host (storage_host) 子主题函数
# ============================================================================

def storage_host_create(client: DMEAPIClient, storage_id: str,
                host_info: dict, task_remarks: str = None,
                vstore_id: str = None) -> dict:
    """
    createStorage host

    在指定Storage device上createStorage host. 

    Args:
        client: DME API client
        storage_id: storage device ID (必选, 1~64个字符)
        host_info: CreateStorageHostInfoobject (Required). attribute format: {
                name: host name (必选, 1~255个字符, 支持字母数字._-和中文字符),
                os_type: 主机type (Required). valid values: LINUX, WINDOWS, WINDOWSSERVER2012, SOLARIS, HPUX, AIX, XENSERVER, LINUX_VIS, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC,
                ip: 主机ip地址 (可选, 最多127个字符),
                description: 主机description (可选, 最多63个字符),
                initiators: StorageInitiatorParamlist (可选, max array members: 1000). parameter format: [{
                        protocol: 启动器type (Required). valid values: fc, iscsi, nvme_over_roce,
                        raw_id: 主机启动器wwpn或iqn或nqn (必选, 1~223个字符),
                        alias: 启动器别名 (可选, 最多31个字符),
                     }, ...],
                multipath: MultiPathForCreateRequestParamobject (Optional). attribute format: {
                        multipath_type: 第三方多路径策略 (Required). valid values: default (default), third_party (第三方多路径),
                        path_type: 启动器路径type (可选, true第三方多路径时有效). valid values: optimal_path (优选路径), non_optimal_path (非优选路径),
                        failover_mode: 启动器切换模式 (可选, true第三方多路径时有效). valid values: early_version_alua, common_alua, alua_not_used, special_alua,
                        special_mode_type: 特殊模式type (可选, 切换模式为特殊模式时有效). valid values: mode_zero, mode_one, mode_two, mode_three,
                }
             }
        task_remarks: 异步任务备注info (可选, 最多1024个字符)
        vstore_id: tenant ID (可选, 1~64个字符; 设备为OceanStor V300R006C30/V500R007C20/Dorado 6.1.3及以上时有效)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
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
    根据Storage host ID list批量queryStorage host

    Args:
        client: DME API client
        ids: ID list (必选, 1~1000 个)

    Returns:
        {
            total: Storage hostcount (int32),
            hosts: Storage hostinfolist (List<QueryStorageHostResponse>). parameter format: [{
                id: 存储host ID (string, 1~64个字符),
                raw_id: 在Storage device上的ID (string, 1~64个字符),
                name: 存储host name (string, 1~255个字符),
                ip: Storage host的IP (string, 1~255个字符),
                health_status: health status. valid values: normal, no_redundant_link, offline, fault, degraded,
                os_type: Storage hosttype. valid values: LINUX, WINDOWS, SOLARIS, HPUX, AIX, VMWAREESX 等,
                initiator_count: 启动器个数 (int32),
                lun_count: 映射LUN个数 (int32),
                lun_group_count: 映射LUN组个数 (int32),
                description: descriptioninfo (string, 1~255个字符),
                capacity_in_byte: 已映射LUN capacity (int64, 字节),
                allocated_capacity_in_byte: 已映射LUN已分配capacity (int64, 字节),
                access_mode: 访问模式. valid values: unknown, balanced, asymmetric,
                vstore_raw_id: tenant ID (string, 1~64个字符),
                vstore_name: 租户name (string, 1~256个字符),
                storage: Storage deviceinfo (SimpleStorage). attribute format: {
                    storage_id: storage device ID (string, 1~64个字符),
                    storage_name: storage device name (string, 1~255个字符),
                    storage_ip: Storage deviceIP (string, 1~255个字符),
                },
                host_group: 所属Storage host groupinfo (List<HostGroupName>). parameter format: [{
                    id: host group ID (string),
                    name: host group name (string),
                }, ...],
                physical_host_info: 物理主机info (PhysicalHostInfo). attribute format: {
                    id: 物理host ID (string, 1~64个字符),
                    name: 物理host name (string, 1~255个字符),
                    ip: 物理主机的IP (string, 1~255个字符),
                },
            }, ...],
        }
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
    批量queryStorage host

    Args:
        client: DME API client
        page_size: 分页query的个数 (可选, 1~1000, default20)
        page_no: 分页query的起始location (可选, 最小值1, default1)
        sort_key: 排序关键字 (可选, sort_key不填时sort_dir不生效). valid values: ip, name, initiator_count, lun_count, lun_group_count, capacity, allocated_capacity, raw_id
        sort_dir: 排序方向 (Optional). valid values: desc (降序), asc (升序)
        name: host name (可选, 1~256个字符, supports fuzzy match)
        raw_id: 主机在设备侧的ID (可选, 0~256个字符)
        host_group_id: 归属host group ID (可选, 最多64个字符)
        avaliable_add_to_host_group_id: 待添加host group ID (可选, 与host_group_id互斥, 最多64个字符)
        host_group_name: 归属host group name (可选, 最多256个字符, supports fuzzy match; 空串query未归属主机组的主机)
        ip: 主机IP (可选, 最多256个字符, supports fuzzy match; 空串query未配置IP的主机)
        health_status: health status (Optional). valid values: normal (正常), no_redundant_link (无冗余路径), offline (离线), fault (故障), degraded (已降级)
        os_type: Storage hosttype (Optional). valid values: LINUX, WINDOWS, WINDOWSSERVER2012, SOLARIS, HPUX, AIX, XENSERVER, LINUX_VIS, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC, UNKNOWN
        storage_id: storage device ID (可选, 1~64个字符)
        avaiable_mapping_for_lun_group_id: 可映射的LUN组ID (可选, 1~64个字符; 与avaiable_mapping_for_lun_id互斥)
        avaiable_mapping_for_lun_id: 可映射的LUN ID (可选, 1~64个字符; 与avaiable_mapping_for_lun_group_id互斥)
        support_provisioning: 是否支持发放 (Optional). valid values: true, false
        manufacturer: Storage device厂商 (可选, 1~64个字符). valid values: huawei, dell_emc, fujitsu, hitachi, hpe, ibm, netapp, pure, third_part
        vstore_raw_id: tenant ID (Optional)
        vstore_name: 租户name (Optional)

    Returns:
        {
            total: Storage hostcount (int32),
            hosts: Storage hostinfolist (List<QueryStorageHostResponse>). parameter format: [{
                id: 存储host ID (string, 1~64个字符),
                raw_id: 在Storage device上的ID (string, 1~64个字符),
                name: 存储host name (string, 1~255个字符),
                ip: Storage host的IP (string, 1~255个字符),
                health_status: health status. valid values: normal, no_redundant_link, offline, fault, degraded,
                os_type: Storage hosttype. valid values: LINUX, WINDOWS, SOLARIS 等,
                initiator_count: 启动器个数 (int32),
                lun_count: 映射LUN个数 (int32),
                lun_group_count: 映射LUN组个数 (int32),
                description: descriptioninfo (string, 1~255个字符),
                capacity_in_byte: 已映射LUN capacity (int64, 字节),
                allocated_capacity_in_byte: 已映射LUN已分配capacity (int64, 字节),
                access_mode: 访问模式. valid values: unknown, balanced, asymmetric,
                vstore_raw_id: tenant ID (string, 1~64个字符),
                vstore_name: 租户name (string, 1~256个字符),
                storage: Storage deviceinfo (SimpleStorage). attribute format: {
                    storage_id: storage device ID (string),
                    storage_name: storage device name (string),
                    storage_ip: Storage deviceIP (string),
                },
                host_group: 所属Storage host groupinfo (List<HostGroupName>). parameter format: [{
                    id: host group ID (string),
                    name: host group name (string),
                }, ...],
                physical_host_info: 物理主机info (PhysicalHostInfo). attribute format: {
                    id: 物理host ID (string),
                    name: 物理host name (string),
                    ip: 物理主机的IP (string),
                },
            }, ...],
        }
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
    modifyStorage host

    Args:
        client: DME API client
        storage_host_id: Storage host ID (Required)
        storage_host_name: 存储host name (可选, 1~255个字符, 支持字母数字._-和中文字符)
        storage_host_description: Storage hostdescriptioninfo (可选, 0~63个字符)
        storage_host_ip: 主机IP (可选, 最多127个字符)
        storage_host_os_type: 主机type (Optional). valid values: UNKNOWN, LINUX, WINDOWS, SUSE, EULER, REDHAT, CENTOS, WINDOWSSERVER2012, SOLARIS, LINUX_VIS, HPUX, AIX, XENSERVER, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC
        add_initiators: StorageInitiatorParamlist (可选, max array members: 1000). parameter format: [{
                protocol: 启动器type (Required). valid values: fc, iscsi, nvme_over_roce,
                raw_id: 主机启动器wwpn或iqn或nqn (必选, 1~223个字符),
                alias: 启动器别名 (可选, 最多31个字符),
             }, ...]
        remove_initiators: 移除的启动器idlist (可选, max array members: 1000)
        multipath: MultiPathForCreateRequestParamobject (Optional). attribute format: {
                multipath_type: 第三方多路径策略 (Required). valid values: default (default), third_party (第三方多路径),
                path_type: 启动器路径type (可选, true第三方多路径时有效). valid values: optimal_path (优选路径), non_optimal_path (非优选路径),
                failover_mode: 启动器切换模式 (可选, true第三方多路径时有效). valid values: early_version_alua, common_alua, alua_not_used, special_alua,
                special_mode_type: 特殊模式type (可选, 切换模式为特殊模式时有效). valid values: mode_zero, mode_one, mode_two, mode_three,
             }
        access_mode: 主机访问模式 (可选, 仅Dorado V6及以后产品). valid values: balanced (均衡模式), asymmetric (非对称模式)
        hyper_metro_path_optimized: 双活优选路径 (可选, 仅Dorado V6及以后产品). valid values: true, false
        task_remarks: 异步任务备注info (可选, 最多1024个字符)

    Returns:
        modifyresult
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
    批量deleteStorage host

    批量delete指定的Storage host. 

    Args:
        client: DME API client
        host_ids: Storage host ID list (必选, 最多 1000 个)

    Returns:
        deleteresult
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
    批量queryStorage host的路径info

    Args:
        client: DME API client
        page_no: 分页query的页码 (可选, 1~2147483647, default1)
        page_size: 分页query的每页大小 (可选, 1~1000, default20)
        storage_id: 所属storage device ID (可选, 1~64个字符)
        storage_host_ids: storage主机的IDlist (可选, 与storage_host_raw_ids二选一, max array members: 20; 单个ID长度1~64个字符)
        storage_host_raw_ids: storage主机在设备上的IDlist (可选, 与storage_host_ids二选一, max array members: 20; 单个ID长度1~64个字符)
        health_status: health status (Optional). valid values: normal (正常), fault (故障), no_redundant_link (无冗余路径), offline (离线)
        running_status: 链路status (Optional). valid values: link_up (已连接), link_down (未连接), online (在线), disabled (已禁用), connecting (正在连接)
        initiator_type: 启动器type (Optional). valid values: iSCSI, FC, NVMe_over_RoCE, IB, vHBA

    Returns:
        {
            total: 主机链路count (integer),
            host_links: 主机链路list (List<HostLinkInfo>). parameter format: [{
                id: 链路ID (string),
                host_id: 存储host ID (string),
                initiator_type: 启动器type. valid values: iSCSI, FC, NVMe,
                initiator_id: 启动器ID (string),
                initiator_port_name: 启动器端口name (string),
                storage_id: storage device ID (string),
                target_id: 目标器ID (string),
                target_port_name: 目标器端口name (string),
                status: status (string),
                link_mode: 链路模式. valid values: single, multipath,
                vstore_raw_id: 租户在设备上的ID (string),
            }, ...],
        }
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
# Storage host group (storage_host_group) 子主题函数
# ============================================================================

def storage_host_group_create(client: DMEAPIClient, storage_id: str, name: str,
                      description: str = None, exist_host_ids: list = None,
                      create_storage_host_params: dict = None,
                      task_remarks: str = None, vstore_id: str = None) -> dict:
    """
    createStorage host group

    Args:
        client: DME API client
        storage_id: storage device ID (必选, 1~64个字符)
        name: host group name (必选, 1~255个字符, 支持字母数字._-和中文字符; V3/V5设备最长31字节, V6设备最长255字节)
        description: descriptioninfo (可选, 0~63个字符)
        exist_host_ids: 待添加至主机组的host IDlist (可选, 与create_storage_host_params互斥, max array members: 1000)
        create_storage_host_params: create新的Storage hostlist (可选, 与exist_host_ids互斥, max array members: 1000). parameter format: [{
                name: host name (必选, 1~255个字符, 支持字母数字._-和中文字符),
                os_type: 主机type (Required). valid values: LINUX, WINDOWS, WINDOWSSERVER2012, SOLARIS, HPUX, AIX, XENSERVER, LINUX_VIS, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC,
                ip: 主机ip地址 (可选, 最多127个字符),
                description: 主机description (可选, 最多63个字符),
                initiators: 启动器list (可选, max array members: 1000). parameter format: [{
                        protocol: 启动器type (Required). valid values: fc, iscsi, nvme_over_roce,
                        raw_id: 主机启动器wwpn或iqn或nqn (必选, 1~223个字符),
                        alias: 启动器别名 (可选, 最多31个字符),
                     }, ...],
                multipath: 多路径配置 (Optional). attribute format: {
                        multipath_type: 第三方多路径策略 (Required). valid values: default (default), third_party (第三方多路径),
                        path_type: 启动器路径type (可选, true第三方多路径时有效). valid values: optimal_path (优选路径), non_optimal_path (非优选路径),
                        failover_mode: 启动器切换模式 (可选, true第三方多路径时有效). valid values: early_version_alua, common_alua, alua_not_used, special_alua,
                        special_mode_type: 特殊模式type (可选, 切换模式为特殊模式时有效). valid values: mode_zero, mode_one, mode_two, mode_three,
                }
             }, ...]
        task_remarks: 异步任务备注info (可选, 最多1024个字符)
        vstore_id: tenant ID (可选, 1~64个字符; 设备为OceanStor V300R006C30/V500R007C20/Dorado 6.1.3及以上时有效)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
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
    批量queryStorage host group

    Args:
        client: DME API client
        raw_id: 主机组在设备侧的ID (可选, 0~256个字符)
        storage_id: 设备ID (可选, 0~64个字符)
        page_size: 分页query的个数 (可选, 1~1000, default100)
        page_no: 分页query的页码 (可选, 1~10000000, default1)
        sort_dir: 排序方向 (可选, sort_key不填时不生效). valid values: desc (降序), asc (升序)
        sort_key: 排序关键字 (Optional). valid values: name, host_count, lun_group_count, lun_count, raw_id
        name: host group name (可选, 0~256个字符, supports fuzzy match)
        vstore_id: tenant ID (Optional)
        vstore_name: 租户name (Optional)
        avaiable_mapping_for_lun_group_id: 待映射的LUN组ID (可选, 0~64个字符; query可映射给指定LUN组的主机组时必传)
        avaiable_mapping_for_lun_id: 待映射的LUN ID (可选, 0~64个字符; query可映射给指定LUN的主机组时必传)
        support_provisioning: 是否支持发放 (Optional). valid values: true, false

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含Storage host grouplist和total
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
    添加Storage host到Storage host group

    将现有主机添加到Storage host group, 或在主机组中create新主机. 

    Args:
        client: DME API client
        storage_host_group_id: Storage host group ID (Required)
        storage_host_id_ids: 存储host IDlist (可选, 与create_storage_host_params互斥, max array members: 1000)
        create_storage_host_params: create新的Storage hostlist (可选, 与storage_host_id_ids互斥, max array members: 1000). parameter format: [{
                name: host name (必选, 1~255个字符, 支持字母数字._-和中文字符),
                os_type: 主机type (Required). valid values: LINUX, WINDOWS, WINDOWSSERVER2012, SOLARIS, HPUX, AIX, XENSERVER, LINUX_VIS, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC,
                ip: 主机ip地址 (可选, 最多127个字符),
                description: 主机description (可选, 最多63个字符),
                initiators: 启动器list (可选, max array members: 1000). parameter format: [{
                        protocol: 启动器type (Required). valid values: fc, iscsi, nvme_over_roce,
                        raw_id: 主机启动器wwpn或iqn或nqn (必选, 1~223个字符),
                        alias: 启动器别名 (可选, 最多31个字符),
                     }, ...],
                multipath: 多路径配置 (Optional). attribute format: {
                        multipath_type: 第三方多路径策略 (Required). valid values: default (default), third_party (第三方多路径),
                        path_type: 启动器路径type (可选, true第三方多路径时有效). valid values: optimal_path (优选路径), non_optimal_path (非优选路径),
                        failover_mode: 启动器切换模式 (可选, true第三方多路径时有效). valid values: early_version_alua, common_alua, alua_not_used, special_alua,
                        special_mode_type: 特殊模式type (可选, 切换模式为特殊模式时有效). valid values: mode_zero, mode_one, mode_two, mode_three,
                }
             }, ...]
        task_remarks: 异步任务备注info (可选, 最多1024个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
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
    从Storage host group中移除主机

    从指定的Storage host group中移除一个或多个主机. 

    Args:
        client: DME API client
        storage_host_group_id: Storage host group ID (必选, 1~64 字符)
        storage_host_ids: 要移除的主机 ID list (必选, 最多 1000 个)
        task_remarks: 任务备注 (可选, 最多 1024 字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/hostmgmt/v1/storage-hostgroups/{storage_host_group_id}/hosts/remove"

    payload = {
        'storage_host_ids': storage_host_ids
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.put(url, body=payload, params={"storage_host_group_id": storage_host_group_id})
    return response


def storage_host_group_delete(client: DMEAPIClient, host_group_ids: list,
                      task_remarks: str = None) -> dict:
    """
    批量deleteStorage host group

    批量delete指定的Storage host group. 

    Args:
        client: DME API client
        host_group_ids: Storage host group ID list (必选, 1~100 个)
        task_remarks: 任务备注 (可选, 最多 1024 字符)

    Returns:
        deleteresult
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
    queryStorage host映射的 LUN infolist

    指定Storage hostquery映射 LUN infolist, 包含 LUN info和主机 LUN ID info. 

    Args:
        client: DME API client
        storage_host_id: Storage host ID (必选, 1~64 字符)
        name: LUN name (可选, 1~256 字符, 支持模糊搜索)
        page_size: 分页query的个数 (可选, 1~1000, default 20)
        page_no: 分页query的起始location (可选, 1~10000000, default 1)
        sort_key: 排序字段 (可选, host_lun_id/mapping_view_raw_id/lun_raw_id)
        sort_dir: 排序方向 (可选, asc/desc, default desc)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含 total 和 lun_mapping_list
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
    queryStorage host group映射的 LUN infolist

    指定Storage host groupquery映射 LUN infolist, 包含 LUN info和主机 LUN ID info. 

    Args:
        client: DME API client
        storage_host_group_id: Storage host group ID (必选, 1~64 字符)
        name: LUN name (可选, 1~256 字符, 支持模糊搜索)
        page_size: 分页query的个数 (可选, 1~1000, default 20)
        page_no: 分页query的起始location (可选, 1~10000000, default 1)
        sort_key: 排序字段 (可选, host_lun_id/mapping_view_raw_id/lun_raw_id)
        sort_dir: 排序方向 (可选, asc/desc, default desc)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含 total 和 lun_mapping_list
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
    批量query端口组

    Args:
        client: DME API client
        storage_id: storage device ID (可选, 1~64个字符, 支持过滤)
        page_no: 分页query的页码 (可选, 1~10000, default1)
        page_size: 分页query的每页大小 (可选, 1~1000, default20)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含端口组list
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
    create端口组

    注意: 仅支持 OceanStor 1800 系列存储. 

    Args:
        client: DME API client
        storage_id: storage device ID (必选, 1~64个字符)
        name: port group name (必选, 1~255个字符, 支持字母数字._-和中文字符)
        description: 端口组description (可选, 0~63个字符)
        port_ids: 关联到端口组的端口IDlist (可选, max array members: 10; 只支持关联ROCE端口和Logic port, 只能关联其中一种)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
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
    批量query指定端口组的端口

    Args:
        client: DME API client
        port_group_id: 端口组 ID (Required)
        type: 端口type (Optional). valid values: fc (FC端口), fcoe (FCoE端口), eth (以太网口), roce (RoCE端口)
        page_no: 分页query的页码 (可选, 1~10000, default1)
        page_size: 分页query的每页大小 (可选, 1~1000, default20)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含端口list
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

    response = client.post(url, body=payload, params={"port_group_id": port_group_id})
    return response


def port_group_show_relations(client: DMEAPIClient, page_no: int = 1,
                              page_size: int = 20) -> dict:
    """
    批量query端口组与端口关联关系

    Args:
        client: DME API client
        page_no: 分页query的页码 (可选, 1~10000, default1)
        page_size: 分页query的每页大小 (可选, 1~1000, default20)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含关联关系list
    """
    url = "/rest/storagemgmt/v1/port-groups/ports/relations/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    response = client.post(url, body=payload)
    return response




# ============================================================================
# action list, for CLI help
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
    批量query物理主机

    Args:
        client: DME API client
        limit: 分页query的个数 (可选, 1~1000)
        start: 分页query的起始location (可选, 0~10000000)
        sort_key: 排序关键字 (Optional). valid values: initiator_count, ip, name
        sort_dir: 排序方向 (可选, sort_key不填时不生效). valid values: desc (降序), asc (升序)
        name: 物理host name (可选, 1~256个字符, supports fuzzy match)
        host_group_name: 物理host group name (可选, 1~256个字符, supports fuzzy match)
        ip: 物理主机IP (可选, 1~256个字符, supports fuzzy match)
        display_status: 展示status (可选, 1~32个字符). valid values: OFFLINE (断开), NOT_RESPONDING (未响应), GRAY (未知), NORMAL (正常), RED (存在问题), YELLOW (可能存在问题), REBOOTING (重启中), INITIAL (初始化), BOOTING (重启), SHUTDOWNING (下电中)
        managed_status: 物理主机纳管statuslist (可选, max array members: 1000). valid values: UNKNOWN (未知), NORMAL (正常), TAKE_OVERING (纳管中), TAKE_ERROR (错误), TAKE_OVER_ALARM (纳管告警)
        os_type: 主机type (Optional). valid values: UNKNOWN, LINUX, WINDOWS, SUSE, EULER, REDHAT, CENTOS, WINDOWSSERVER2012, SOLARIS, LINUX_VIS, HPUX, AIX, XENSERVER, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC
        access_mode: 物理主机接入方式 (Optional). valid values: ACCOUNT (账号密码), NONE (手动接入), VCENTER (vCenter纳管), FUSIONSPHERE (FusionSphere纳管), HCS (HCS纳管), TPOPS (TPOPS纳管)
        az_id: 可用分区ID (可选, 1~64个字符; 当提供az_ids时此参数无效)
        az_ids: 可用分区IDlist (可选, max array members: 40)
        project_id: 业务群组ID (可选, 1~64个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含物理主机list和total
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
    query指定物理主机

    Args:
        client: DME API client
        host_id: 物理主机 ID(Required)

    Returns:
        {
            id: 物理host ID (string),
            name: 物理host name (string),
            description: descriptioninfo (string),
            ip: 物理主机IP (string),
            port: 端口 (int32),
            username: 用户名 (string),
            display_status: 显示status (string),
            managed_status: 管理status (string),
            os_status: 操作系统status (string),
            os_type: 操作系统type (string),
            os_version: 操作系统version (string),
            initiator_count: 启动器count (int32),
            access_mode: 访问模式 (string),
            multipathing_software: 多路径软件 (string),
            project_id: 项目ID (string),
            sync_to_storage: 同步到存储 (string),
            multipath_type: 多路径type (string),
            path_type: 路径type (string),
            failover_mode: 故障切换模式 (string),
            special_mode_type: 特殊模式type (string),
            capacity_in_byte: capacity (int64, 字节),
            allocated_capacity_in_byte: 已分配capacity (int64, 字节),
            hostGroups: 主机组info (List<HostGroupName>). parameter format: [{
                id: host group ID (string),
                name: host group name (string),
            }, ...],
            azs: 可用区list (List<string>),
        }
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
        client: DME API client
        access_mode: 物理主机接入方式 (Required). valid values: ACCOUNT (指定账号密码), NONE (手动录入)
        type: 主机type (Required). valid values: UNKNOWN, LINUX, WINDOWS, SUSE, EULER, REDHAT, CENTOS, WINDOWSSERVER2012, SOLARIS, LINUX_VIS, HPUX, AIX, XENSERVER, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC. ACCOUNT模式仅支持LINUX
        host_name: 物理host name (NONE模式必填, 1~255个字符, 支持字母数字._-和中文字符)
        ip: 物理主机IP address (ACCOUNT模式有效, 支持IPv4和IPv6, 最多127个字符)
        port: 物理主机接入端口 (ACCOUNT模式必填, 1~65535)
        username: 物理主机接入用户名 (ACCOUNT模式必填, 1~255个字符)
        password: 物理主机接入密码 (ACCOUNT模式必填, 1~1024个字符)
        description: 物理主机descriptioninfo (可选, 0~63个字符)
        initiator: 物理主机启动器list (NONE模式必填). parameter format: [{
                protocol: 启动器type (Required). valid values: FC, ISCSI, NVME_OVER_ROCE,
                port_name: 主机启动器wwn或iqn (必选, 1~223个字符),
             }, ...]
        azs: 可用分区IDlist (可选, max array members: 40)
        project_id: 业务群组ID (可选, 1~64个字符)
        sync_to_storage: 自动同步已接入主机info到存储 (可选, defaultfalse). valid values: true, false
        multipath_type: 多路径type (Optional). valid values: default, third_party
        path_type: 启动器路径type (可选, true第三方多路径时有效). valid values: optimal_path (优选路径), non_optimal_path (非优选路径)
        failover_mode: 启动器切换模式 (可选, true第三方多路径时有效). valid values: early_version_alua, common_alua, alua_not_used, special_alua
        special_mode_type: 特殊模式type (可选, 切换模式为特殊模式时有效). valid values: mode_zero, mode_one, mode_two, mode_three
        save_public_key: 是否自动保存物理主机公钥 (可选, defaultfalse). valid values: true, false

    Returns:
        {
            id: 物理host ID (string, 1~64个字符),
        }
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
    modify物理主机基本info

    Args:
        client: DME API client
        host_id: 物理主机 ID (Required)
        ip: 物理主机IP address (可选, 最多127个字符, 支持IPv4和IPv6; 不填表示不变)
        host_name: 物理host name (可选, 1~255个字符, 支持字母数字._-; 为空表示保持不变)
        os_type: 主机type (Optional). valid values: LINUX, WINDOWS, WINDOWSSERVER2012, SOLARIS, HPUX, AIX, XENSERVER, LINUX_VIS, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC
        azs: 可用分区IDlist (可选, max array members: 40; 空值或空list表示解除az关联)
        project_id: 业务群组ID (可选, 0~64个字符; 不填表示不做modify; 空字符串表示解除project关联; 非空且与原值不一致表示关联至新project)

    Returns:
        modifyresult
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
    modify物理主机接入info

    Args:
        client: DME API client
        host_id: 物理host ID (必选, 1~64个字符)
        ip: 物理主机接入IP address (可选, 最多127个字符, 支持IPv4和IPv6; NONE转ACCOUNT场景必填)
        port: 物理主机接入端口 (可选, 1~65535; NONE转ACCOUNT场景必填)
        username: 物理主机接入用户名 (可选, 1~255个字符; NONE转ACCOUNT场景必填)
        password: 物理主机接入用户密码 (可选, 1~1024个字符; NONE转ACCOUNT场景必填)
        project_id: 业务群组ID (可选, 0~64个字符; 不填表示不做modify; 空字符串表示解除关联; 非空且与原值不一致表示关联至新project)
        azs: 可用分区IDlist (可选, max array members: 40; 空值或空list表示解除az关联)
        sync_to_storage: 是否同步modifyStorage hostinfo (可选, defaultfalse). valid values: true (同步modify), false (不同步)
        description: 物理主机descriptioninfo (可选, 0~63个字符)
        multipath_type: 多路径type (Optional). valid values: default, third_party
        path_type: 启动器路径type (可选, true第三方多路径时有效). valid values: optimal_path (优选路径), non_optimal_path (非优选路径)
        failover_mode: 启动器切换模式 (可选, true第三方多路径时有效). valid values: early_version_alua, common_alua, alua_not_used, special_alua
        special_mode_type: 特殊模式type (可选, 切换模式为特殊模式时有效). valid values: mode_zero, mode_one, mode_two, mode_three

    Returns:
        modifyresult
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

    移除指定的物理主机. 

    Args:
        client: DME API client
        host_id: 物理主机 ID(Required)
        sync_to_storage: 是否同步从存储delete (可选, default false)

    Returns:
        deleteresult
    """
    url = "/rest/hostmgmt/v1/hosts/{host_id}"

    response = client.delete(url, params={"host_id": host_id, "sync_to_storage": str(sync_to_storage).lower()})
    return response


def physical_host_add_initiators(client: DMEAPIClient, host_id: str,
                  initiators: list) -> dict:
    """
    为物理主机添加启动器

    Args:
        client: DME API client
        host_id: 物理主机 ID (Required)
        initiators: 启动器list (必选, max array members: 100). parameter format: [{
                protocol: 启动器type (Required). valid values: FC (WWPN格式, 16字符十六进制), ISCSI, NVME_OVER_ROCE,
                port_name: 主机启动器wwn或iqn (必选, 1~223个字符),
             }, ...]

    Returns:
        添加result
    """
    url = "/rest/hostmgmt/v1/hosts/{host_id}/initiators/add"

    payload = {
        'initiators': initiators
    }

    response = client.put(url, body=payload, params={"host_id": host_id})
    return response


def physical_host_remove_initiators(client: DMEAPIClient, host_id: str,
                     initiators: list) -> dict:
    """
    从物理主机移除启动器

    Args:
        client: DME API client
        host_id: 物理主机 ID(Required)
        initiators: 启动器 ID list (必选, 最多 1000 个)

    Returns:
        移除result
    """
    url = "/rest/hostmgmt/v1/hosts/{host_id}/initiators/remove"

    payload = {
        'initiators': initiators
    }

    response = client.put(url, body=payload, params={"host_id": host_id})
    return response


def physical_host_show_initiators(client: DMEAPIClient, host_id: str,
                   port_name: str = None, protocol: str = None,
                   status: str = None) -> dict:
    """
    query指定物理主机的启动器

    Args:
        client: DME API client
        host_id: 物理主机 ID (Required)
        port_name: 物理主机启动器wwn或iqn (可选, 1~223个字符)
        protocol: 启动器type (可选, 1~64个字符). valid values: UNKNOWN, FC, ISCSI, NVME_OVER_ROCE, SAS, NVME_OVER_FABRIC
        status: 启动器status (可选, 1~32个字符). valid values: UNKNOWN, ONLINE, OFFLINE, UNBOUND

    Returns:
        {
            total: 启动器count (int32),
            initiators: 启动器list (List<InitiatorInHostResponse>). parameter format: [{
                id: 启动器ID (string),
                port_name: 端口name (string),
                status: status (string),
                protocol: 协议. valid values: iSCSI, FC, NVMe,
                switch: 交换机info. attribute format: {
                    switch_id: 交换机ID (string),
                    switch_name: switch name (string),
                },
            }, ...],
        }
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
    检测Storage device和物理主机连通性

    Args:
        client: DME API client
        storage_id: Storage device ID(Required)
        host_ids: 物理主机 ID list (可选, 与 hostgroup_id 二选一)
        hostgroup_id: 物理主机组 ID (可选, 与 host_ids 二选一)
        auto_zoning: 自动划 zone 策略 (可选, default false)
        target_fcports: 端口 wwn list (可选, auto_zoning 为 true 时生效)
        target_fcportgroups: 端口组 id list (可选, auto_zoning 为 true 时生效)

    Returns:
        连通性检测result
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

    保存物理主机的 SSH 公钥, 用于后续通信中检测通信物理主机的身份是否合法. 

    Args:
        client: DME API client
        ip: 物理主机 IP 地址(Required)
        key: 物理主机 SSH 公钥(Required)
        port: SSH 端口 (可选, default 22)

    Returns:
        保存result
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
    query指定物理主机 SSH 公钥

    Args:
        client: DME API client
        ip: 物理主机 IP 地址(Required)
        port: SSH 端口 (可选, default 22)

    Returns:
        SSH 公钥info
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
    根据启动器query关联的物理主机

    根据启动器 ID 或启动器 WWPN/IQN/NQN query关联的物理主机. 

    Args:
        client: DME API client
        initiator_id: 启动器 ID (可选, 与 raw_id 互斥)
        raw_id: 启动器 WWPN/IQN/NQN (可选, 与 initiator_id 互斥)
        protocol: 启动器type (可选, FC/ISCSI/NVME_OVER_ROCE)

    Returns:
        {
            id: 物理host ID (string),
            name: 物理host name (string),
            ip: 物理主机IP (string),
            description: descriptioninfo (string),
            display_status: 显示status (string),
            managed_status: 管理status (string),
            os_type: 操作系统type (string),
            initiator_info: 启动器infolist (List<InitiatorInfo>). parameter format: [{
                id: 启动器ID (string),
                port_name: 端口name (string),
                status: status (string),
                protocol: 协议 (string),
            }, ...],
            lun_count: LUNcount (int32),
            storage_info: 存储infolist (List<StorageInfo>). parameter format: [{
                storage_id: storage device ID (string),
                storage_name: storage device name (string),
            }, ...],
            multipath_type: 多路径type (string),
            path_type: 路径type (string),
            failover_mode: 故障切换模式 (string),
            special_mode_type: 特殊模式type (string),
        }
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

    将 LUN 映射给指定的物理主机. 

    Args:
        client: DME API client
        volume_ids: LUN ID list (必选, max array members: 1000)
        host_id: 物理主机 ID (必选, 1~64个字符)
        mapping_policy: MappingPolicylist (可选, max array members: 64; 服务化LUN不需要配置). parameter format: [{
                storage_id: storage device ID (可选, 0~64个字符),
                start_host_lun_id: 起始主机LUN ID (可选, 0~4095),
                auto_zoning: 自动划zone (Optional). valid values: true (划zone), false (不划zone),
                zone_policy_id: zone策略ID (可选, 0~64个字符; auto_zoning为true时生效),
                target_fcports: 端口wwnlist (可选, 与target_fcportgroups互斥, max array members: 1000; auto_zoning为true时生效),
                target_fcportgroups: port group IDlist (可选, 与target_fcports互斥, max array members: 1000; auto_zoning为true时生效),
                mapping_view: MappingRequestobject (Optional). attribute format: {
                        mapping_view_id: mapping view在设备上的ID (可选, 最多31个字符),
                        mapping_view_name: mapping view在设备上的名字 (可选, 最多31个字符),
                        lun_group_id: LUN组在设备上的ID (可选, 最多31个字符),
                        lun_group_name: LUN组在设备上的name (可选, 最多255个字符),
                        port_group_id: 端口组在设备上的ID (可选, 最多31个字符),
                }
             }, ...]
        task_remarks: 异步任务备注info (可选, 最多1024个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
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

    LUN 解除主机映射. 

    Args:
        client: DME API client
        volume_ids: LUN ID list (必选, max array members: 1000)
        host_id: 主机 ID (必选, 1~64个字符)
        task_remarks: 异步任务备注info (可选, 最多1024个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
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
    解除Storage host映射

    解除 LUN 与Storage host的映射关系. 

    Args:
        client: DME API client
        volume_ids: LUN ID list (必选, max array members: 1000)
        host_id: 主机 ID (必选, 1~64个字符)
        task_remarks: 异步任务备注info (可选, 最多1024个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
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
    批量query物理主机组

    Args:
        client: DME API client
        limit: 分页query的个数 (可选, 1~1000)
        start: 分页query的起始location (可选, 0~10000000)
        sort_dir: 排序方向 (可选, sort_key不填时不生效). valid values: desc (降序), asc (升序)
        sort_key: 排序关键字 (可选, 1~255个字符). valid values: host_count (主机组主机个数)
        name: 物理host group name (可选, 1~256个字符, supports fuzzy match)
        project_id: 所属业务群组ID (可选, 1~64个字符)
        az_ids: 所属可用分区IDlist (可选, max array members: 1000; 单个ID长度1~64个字符)
        managed_status: 纳管statuslist (可选, max array members: 1000). valid values: UNKNOWN, NORMAL, TAKE_OVERING, TAKE_ERROR, TAKE_OVER_ALARM

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含物理主机组list和total
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
    query物理主机组中的物理主机

    query指定物理主机组的物理主机list. 

    Args:
        client: DME API client
        hostgroup_id: 物理host group ID (必选, 1~64个字符)
        name: 物理host name (可选, 1~256个字符, supports fuzzy match)
        ip: 物理主机IP (可选, 1~256个字符, supports fuzzy match)
        display_status: 展示statuslist (可选, max array members: 1000). valid values: OFFLINE (断开), NOT_RESPONDING (未响应), GRAY (未知), NORMAL (正常), RED (存在问题), YELLOW (可能存在问题), REBOOTING (重启中), INITIAL (初始化), BOOTING (重启), SHUTDOWNING (下电中)
        managed_status: 纳管statuslist (可选, max array members: 1000). valid values: UNKNOWN, NORMAL, TAKE_OVERING, TAKE_ERROR, TAKE_OVER_ALARM
        os_type: 操作系统typelist (可选, max array members: 1000). valid values: UNKNOWN, LINUX, WINDOWS, SUSE, EULER, REDHAT, CENTOS, WINDOWSSERVER2012, SOLARIS, HPUX, AIX, XENSERVER, MACOS, VMWAREESX, ORACLE, OPENVMS
        sort_key: 排序关键字 (Optional). valid values: ip, name
        sort_dir: 排序方向 (可选, sort_key不填时不生效). valid values: desc (降序), asc (升序)
        page_size: 分页query的个数 (可选, 1~1024, default1024)
        page_no: 分页query的页码 (可选, 1~10000000, default1)

    Returns:
        {
            total: 主机count (int32),
            hosts: 主机list (List<HostInHostGroupResponse>). parameter format: [{
                id: 物理host ID (string),
                name: 物理host name (string),
                ip: 物理主机IP (string),
                port: 端口 (int32),
                display_status: 显示status (string),
                managed_status: 管理status (string),
                os_status: 操作系统status (string),
                os_type: 操作系统type (string),
                os_version: 操作系统version (string),
                manufacturer: 厂商 (string),
                model: model (string),
            }, ...],
        }
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

    response = client.post(url, body=payload, params={"hostgroup_id": hostgroup_id})
    return response


def physical_host_group_show(client: DMEAPIClient, hostgroup_id: str) -> dict:
    """
    query指定物理主机组

    Args:
        client: DME API client
        hostgroup_id: 物理主机组 ID(Required)

    Returns:
        物理主机组详细info
    """
    url = "/rest/hostmgmt/v1/hostgroups/{hostgroup_id}/summary"

    response = client.get(url, params={"hostgroup_id": hostgroup_id})
    return response


def physical_host_group_create(client: DMEAPIClient, name: str, host_ids: list,
           azs: list = None, project_id: str = None,
           description: str = None) -> dict:
    """
    create物理主机组

    指定物理主机create物理主机组. 

    Args:
        client: DME API client
        name: 物理host group name (必选, 1~255个字符, 支持字母数字._-和中文字符)
        host_ids: 物理host IDlist (必选, max array members: 100)
        azs: 可用分区IDlist (可选, max array members: 40)
        project_id: 业务群组ID (可选, 1~64个字符)
        description: 物理主机组descriptioninfo (可选, 0~63个字符)

    Returns:
        create的物理主机组info
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
    modify物理主机组基本info

    Args:
        client: DME API client
        hostgroup_id: 物理主机组 ID (Required)
        name: 物理host group name (可选, 1~255个字符, 支持字母数字._-和中文字符; 不填或空串表示不modify)
        description: 物理主机组descriptioninfo (可选, 0~63个字符)
        azs: 可用分区IDlist (可选, max array members: 40; 空值或空list表示解除az关联)
        project_id: 业务群组ID (可选, 0~64个字符; 不填表示不做modify; 空字符串表示解除关联; 非空且与原值不一致表示关联至新project)

    Returns:
        modifyresult
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
    delete指定物理主机组

    Args:
        client: DME API client
        hostgroup_id: 物理主机组 ID(Required)
        sync_to_storage: 是否同步从存储delete (可选, default false)

    Returns:
        deleteresult
    """
    url = "/rest/hostmgmt/v1/hostgroups/{hostgroup_id}"

    response = client.delete(url, params={"hostgroup_id": hostgroup_id, "sync_to_storage": str(sync_to_storage).lower()})
    return response


def physical_host_group_add_hosts(client: DMEAPIClient, hostgroup_id: str,
             host_ids: list, sync_to_storage: bool = False) -> dict:
    """
    向物理主机组中增加物理主机

    Args:
        client: DME API client
        hostgroup_id: 物理主机组 ID(Required)
        host_ids: 物理主机 ID list (必选, 最多 100 个)
        sync_to_storage: 是否同步添加到存储 (可选, default false)

    Returns:
        添加result
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

    从物理主机组中移除物理主机. 

    Args:
        client: DME API client
        hostgroup_id: 物理主机组 ID(Required)
        host_ids: 物理主机 ID list (必选, 最多 1000 个)
        sync_to_storage: 是否同步从存储移除 (可选, default false)

    Returns:
        移除result
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

    将 LUN 映射给指定的物理主机组. 

    Args:
        client: DME API client
        volume_ids: LUN ID list (必选, max array members: 1000)
        hostgroup_id: 物理主机组 ID (必选, 0~64个字符)
        mapping_policy: MappingPolicylist (Optional). parameter format: [{
                storage_id: storage device ID (可选, 0~64个字符),
                start_host_lun_id: 起始主机LUN ID (可选, 0~4095),
                auto_zoning: 自动划zone (Optional). valid values: true (划zone), false (不划zone),
                zone_policy_id: zone策略ID (可选, 0~64个字符; auto_zoning为true时生效),
                target_fcports: 端口wwnlist (可选, 与target_fcportgroups互斥, max array members: 1000; auto_zoning为true时生效),
                target_fcportgroups: port group IDlist (可选, 与target_fcports互斥, max array members: 1000; auto_zoning为true时生效),
                mapping_view: MappingRequestobject (Optional). attribute format: {
                        mapping_view_id: mapping view在设备上的ID (可选, 最多31个字符),
                        mapping_view_name: mapping view在设备上的名字 (可选, 最多31个字符),
                        lun_group_id: LUN组在设备上的ID (可选, 最多31个字符),
                        lun_group_name: LUN组在设备上的name (可选, 最多255个字符),
                        port_group_id: 端口组在设备上的ID (可选, 最多31个字符),
                }
             }, ...]
        task_remarks: 异步任务备注info (可选, 最多1024个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
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

    解除 LUN 与主机组的映射关系. 

    Args:
        client: DME API client
        volume_ids: LUN ID list (必选, max array members: 1000)
        hostgroup_id: 主机组 ID (必选, 1~64个字符)
        task_remarks: 异步任务备注info (可选, 最多1024个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
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
    解除Storage host group映射

    解除 LUN 与Storage host group的映射关系. 

    Args:
        client: DME API client
        volume_ids: LUN ID list (必选, max array members: 1000)
        hostgroup_id: 主机组 ID (必选, 1~64个字符)
        task_remarks: 异步任务备注info (可选, 最多1024个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
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


def physical_host_group_show_related(client: DMEAPIClient, hostgroup_id: str,
                                       storage_ip: str = None,
                                       storage_name: str = None) -> dict:
    """
    query物理主机组关联的Storage host grouplist. 

    Args:
        client: DME API client
        hostgroup_id: 物理host group ID (必选, string, 1~64个字符)
        storage_ip: Storage deviceIP (可选, string, 1~127个字符)
        storage_name: storage device name, 支持模糊搜索 (可选, string, 1~256个字符)

    Returns:
        {
            total: query的Storage host数 (integer),
            strorage_host_group_list: Storage host grouplist (List<StorageHostGroupResponse>). parameter format: [{
                host_group_id: 存储host group ID (string),
            }, ...],
        }
    """
    url = "/rest/hostmgmt/v1/hostgroups/{hostgroup_id}/related-storage-hostgroups"

    if not hostgroup_id:
        raise ValueError("hostgroup_id 是必选参数")

    params = {
        'hostgroup_id': hostgroup_id
    }
    if storage_ip is not None:
        params['storage_ip'] = storage_ip
    if storage_name is not None:
        params['storage_name'] = storage_name

    response = client.get(url, params=params)
    return response


def mapping_view_query_host_to_lun(client: DMEAPIClient, storage_id: str,
                                     name: str = None, mapping_type: str = None,
                                     host_info: dict = None, lun_info: dict = None,
                                     sort_key: str = None, sort_dir: str = None,
                                     page_size: int = 100, page_no: int = 1) -> dict:
    """
    queryStorage host和LUN映射关系. 

    Args:
        client: DME API client
        storage_id: storage device ID (必选, string, 1~64个字符)
        name: mapping viewname, 支持模糊搜索 (可选, string, 0~256个字符)
        mapping_type: query主机映射type (可选, string). valid values: all (和LUN存在映射关系的Storage host, 包括直接映射和间接映射), match_mapping_view (与LUN直接映射的Storage host)
        host_info: Storage hostinfo (可选, LunToHostQueryParamobject)
        lun_info: LUNinfo (可选, HostToLunQueryParamobject)
        sort_key: 排序字段 (可选, string). valid values: host_name (存储host name), lun_name (LUN name), capacity_usage (capacity使用率), lun_raw_id, host_raw_id
        sort_dir: 排序方向 (可选, string). valid values: asc (升序), desc (降序)
        page_size: 分页querymapping view的个数 (可选, int32, 0~1000). default值: 100
        page_no: 分页querymapping view的起始location (可选, int32). default值: 1

    Returns:
        {
            total: mapping viewcount (int32),
            mapping_views: mapping viewlist (List<HostToLunMappingView>). parameter format: [{
                id: mapping viewID (string),
                name: mapping viewname (string),
                host_info: Storage hostinfo (HostInfoRespParamobject),
                lun_info: LUNinfo (LunInfoRespParamobject),
            }, ...],
        }
    """
    url = "/rest/blockservice/v1/mapping-views/query_for_host_to_lun"

    if not storage_id:
        raise ValueError("storage_id 是必选参数")

    payload = {
        'storage_id': storage_id,
        'page_size': page_size,
        'page_no': page_no
    }
    if name is not None:
        payload['name'] = name
    if mapping_type is not None:
        payload['mapping_type'] = mapping_type
    if host_info is not None:
        payload['host_info'] = host_info
    if lun_info is not None:
        payload['lun_info'] = lun_info
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir

    response = client.post(url, body=payload)
    return response


# ============================================================================
# action list, for CLI help
# ============================================================================

ACTIONS = {
    # LUN subtopic action (san lun xxx)
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

    # LUN groupsubtopic action (san lun_group xxx)
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
    # mapping viewsubtopic action (san mapping_view xxx)
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

    # Storage hostsubtopic action (san storage_host xxx)
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
    # Storage host groupsubtopic action (san storage_host_group xxx)
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
    # 端口组subtopic action (san port_group xxx)
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
    # 物理主机subtopic action (san physical_host xxx)
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
    # 物理主机组subtopic action (san physical_host_group xxx)
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
    },
    'show_related': {
        'func': physical_host_group_show_related,
        'description': '查询物理主机组关联的存储主机组列表',
        'params': ['hostgroup_id', 'storage_ip', 'storage_name'],
        'subtopic': 'physical_host_group'
    },
    'query_host_to_lun': {
        'func': mapping_view_query_host_to_lun,
        'description': '查询存储主机和LUN映射关系',
        'params': ['storage_id', 'name', 'mapping_type', 'host_info', 'lun_info', 'sort_key', 'sort_dir', 'page_size', 'page_no'],
        'subtopic': 'mapping_view'
    }
}
