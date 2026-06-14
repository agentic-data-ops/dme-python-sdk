"""
SAN (Storage Area Network) operations
Includes subtopics: LUN, LUN group, mapping view, storage host, storage host group, port group
"""

import sys
import os

from pydme.client import DMEAPIClient

# ============================================================================
# LUN subtopic functions
# ============================================================================

"""
LUN (Volume) operations
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
    Batch query LUNs
    
    Args:
        client: DME API client
        limit: Number of items per page (Optional, 0~1000, default 1000)
        offset: Start position for pagination (Optional, min 0, default 0)
        sort_dir: Sort direction (Optional). Options: asc (ascending), desc (descending)
        sort_key: Sort field (Optional). Options: name, size, alloc_capacity, capacity_usage, protection_capacity
        name: LUN name (Optional, 1~256 characters, supports fuzzy search)
        vstore_raw_id: Tenant ID on storage device (Optional, 1~64 characters)
        vstore_name: Tenant name (Optional, 1~256 characters, supports fuzzy search)
        status: Status (Optional, deprecated, use health_status instead). Options: creating, normal, mapping, unmapping, deleting, error, expanding, faulty, write_protected
        health_status: Health status (Optional). Options: normal, faulty, write_protected
        service_level_id: Service level ID (Optional, 1~64 characters)
        volume_wwn: LUN WWN (Optional, 1~128 characters)
        storage_id: Storage device ID (Optional, 1~36 characters, UUID format or 32-bit hex)
        pool_raw_id: Storage pool ID on device (Optional, 1~64 characters; requires storage_id)
        host_id: Host ID (Optional, 1~64 characters, UUID format or 32-bit hex)
        hostgroup_id: Host group ID (Optional, 1~64 characters, UUID format or 32-bit hex)
        unmapped_host_id: Unmapped host ID (Optional, 1~64 characters)
        unmapped_hostgroup_id: Unmapped host group ID (Optional, 1~64 characters)
        project_id: Project group ID (Optional, 1~64 characters)
        allocate_type: Allocation type (Optional). Options: thin, thick
        attached: Mapping status (Optional). Options: true (mapped), false (unmapped)
        query_mode: LUN provisioning mode (Optional). Options: service (service LUN), non-service (non-service LUN), all (all LUNs)
        protected: LUN protection status (Optional). Options: true (protected), false (unprotected)
        pg_id: Protection group ID (Optional, 1~64 characters, UUID format or 32-bit hex)
        usage_type: LUN usage type (Optional). Options: traditional (traditional LUN), edev (eDevLUN)
        support_provisioning: Filter for provisionable LUNs (Optional). Options: true (provisionable only), false (all)
    
    Returns:
        {
            total: Total count (integer),
            volumes: LUN list (List<VolumeInfo>)。参数格式如下：[{
                id: LUN ID (string),
                name: LUN name (string),
                size: Capacity (integer),
                status: Status (string),
                health_status: Health status (string),
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
    Query a specific LUN.

    Args:
        client: DME API client
        volume_id: LUN id (Required, string, 1~64 characters)

    Returns:
        {
            volume: LUN details (VolumeDetails object)。属性格式如下：{
                id: LUN unique identifier (string, 1~64 characters),
                name: Name (string, 1~255 characters),
                description: Description (string, 0~255 characters),
                status: Status (string). Options: creating, normal, mapping, unmapping, deleting, error, expanding, faulty, write_protected,
                attached: Mapping status (boolean, true, false),
                alloctype: Allocation type (string). Options: thin (thin provisioning), thick (fixed allocation),
                total_capacity: Total capacity in GB (double),
                storage_id: Storage device id (string, 1~64 characters),
                storage_name: Storage device name (string, 1~64 characters),
                pool_id: Storage pool id for the LUN (string, 1~64 characters),
                volume_wwn: LUN WWN on storage device (string, 1~64 characters),
            },
        }
    """
    url = "/rest/blockservice/v1/volumes/{volume_id}"

    if not volume_id:
        raise ValueError("volume_id is required")

    response = client.get(url, params={"volume_id": volume_id})
    return response


def lun_create(client: DMEAPIClient, storage_id: str, lun_specs: list = None,
                  lun_specs_pass_through: list = None, pool_id: str = None,
                  vstore_id: str = None, owner_controller: str = None,
                  initial_distribute_policy: str = None, prefetch_policy: str = None,
                  prefetch_value: int = None, tuning: dict = None,
                  mapping: dict = None, task_remarks: str = None) -> dict:
    """
    Custom create LUN

    Args:
        client: DME API client
        storage_id: Storage device ID (Required), 1~64 characters, obtained via storage device query API
        lun_specs: LUN basic parameters (Conditionally Required), List<LunSpecs> type, max array members 1000, max 10 groups per request; mutually exclusive with lun_specs_pass_through; required when storage mode is not pass-through. 参数格式如下：[{
                name: LUN name (1~255 characters, supports letters, digits, ._- and Chinese characters; when count>1, name is 1~27 characters),
                count: Number of LUNs of this spec (1~500),
                capacity: Single LUN capacity (1~262144, in GB),
                suffix_length: Naming suffix rule (1~4; name length + suffix length <= 255),
                start_suffix: Starting suffix number (1~9999; count + start suffix <= 9999),
                start_lun_id: Starting LUN ID (1~65535),
                usage_type: LUN usage type. Options: traditional, edev (eDevLUN),
                write_policy: Write policy. Options: back (write-back), through (write-through),
                remote_lun_raw_id: External LUN ID (0~255 characters; effective when usage_type is edev),
                disguise_status: LUN disguise (effective when usage_type is edev). Options: nodisguise, basic, expansion, inheritance,
             }, ...]
        lun_specs_pass_through: LUN basic parameters for pass-through storage mode (Conditionally Required), List<lunSpecsPassThrough> type, max array members 24, max 24 groups per request; mutually exclusive with lun_specs; required when storage mode is pass-through. 参数格式如下：[{
                name: LUN name (1~247 characters, supports letters, digits, -._ and Chinese characters; final name is LUN name + suffix code + '-' + disk location),
                description: LUN description (0~255 characters),
                disk_location: Disk location for the LUN (1~255 characters),
                count: created per diskLUNcount (1~8),
                suffix_length: Suffix encoding digits (1~4, 默认4; 当count大于1effective when),
                start_suffix: Suffix start encoding (0~9999, 默认0; 当count大于1effective when),
             }, ...]
        pool_id: Storage pool ID (Conditionally required), 1~64 characters; required when storage mode is not pass-through; obtained via QueryResource type API, Resource type name is SYS_StoragePool
        vstore_id: 租户 ID（可选），1~64  characters；当设备为 OceanStor V300R006C00、OceanStor V500R007C00、OceanStor Dorado 6.1.3、OceanStor 6.1.3 effective on this version and above
        owner_controller: Owner controller (Optional), 1~64 characters, obtained by querying controllers on the storage device
        initial_distribute_policy: Initial capacity allocation policy（可选），only supports华为 V3/V5 设备，Dorado 系列不支持；
                                  Options：automatic（自动）、highest_performance（高性能层）、performance（性能层）、capacity（容量层）；默认 automatic
        prefetch_policy: 预取策略（可选），Affects disk read；
                        Options：no_prefetch（不预取）、constant_prefetch（固定预取）、variable_prefetch（可变预取）、intelligent_prefetch（智能预取）；默认 intelligent_prefetch
        prefetch_value: 预取策略值（可选），0~1024；下发了 prefetch_policy required when value is fixed or variable prefetch；固定预取value range 0~1024KB，Variable prefetch value range 0~1024 倍
        tuning: 调优属性 (可选), CustomizeLunTuning object。参数格式如下：{
                smart_tier: Data migration策略。Options：no_migration (不迁移), automatic_migration (自动迁移), migration_to_higher (migrate to higher tier), migration_to_lower (migrate to lower tier)。默认no_migration,
                deduplication_enabled: Deduplication (仅Thin LUN支持)。Options：true (开启), false (关闭),
                compression_enabled: Data compression (仅Thin LUN支持)。Options：true (开启), false (关闭),
                alloction_type: LUNAllocation type。Options：thin, thick,
                smart_qos: Smart QoSobject。属性格式如下：{
                        max_bandwidth: Max bandwidth (1~999999999Mbit/s; 与min_bandwidth/min_iopsmutually exclusive),
                        max_iops: Max IOPS (1~999999999; 与min_bandwidth/min_iopsmutually exclusive),
                        min_bandwidth: Min bandwidth (1~999999999Mbit/s; 与max_bandwidth/max_iopsmutually exclusive),
                        min_iops: Min IOPS (1~999999999; 与max_bandwidth/max_iopsmutually exclusive),
                        latency: 时延 (1~999999999ms; Dorado V6系列单位为us, Optional值为500/1500; 与max_bandwidth/max_iopsmutually exclusive),
                },
                workload_type_raw_id: Workload type ID (0~4294967295; obtained by querying application types on the storage device),
             }
        mapping: Mapping info (可选), LunMapping object, If present, creates for host or host group LUN。参数格式如下：{
                host_id: Host ID (1~64 characters; 与hostgroup_idone of, cannot coexist),
                hostgroup_id: Host group ID (1~64 characters; 与host_idone of, cannot coexist),
                host_type: 映射Host type。Options：storage_host (Storage host), host (主机)。默认host,
                start_host_lun_id: 起始主机LUN ID (1~4096),
                mapping_view: Mapping view请求信息 (LunMappingRequestobject)。属性格式如下：{
                        mapping_view_raw_id: Mapping viewon the storage deviceID (1~31 characters),
                        mapping_view_name: Mapping viewon the storage device名称 (1~31 characters),
                        lun_group_raw_id: LUN组on the storage deviceID (1~31 characters),
                        lun_group_name: LUN组on the storage device名称 (1~255 characters),
                        port_group_raw_id: Port groupon the storage deviceID (1~31 characters; Host or host group does not existMapping relationship时可指定, 存在Mapping relationship时不可指定),
                },
             }
        task_remarks: Async taskRemark（可选），最多 1024  characters

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/blockservice/v1/volumes/customize"

    if not storage_id:
        raise ValueError("storage_id 是Required参数")

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
    Batch delete LUNs.

    Args:
        client: DME API client
        volume_ids: LUN ID list (Required, List[string], max array members: 1000)
        task_remarks: Async task remark (Optional, string, max 1024 characters)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/blockservice/v1/volumes/delete"

    if not volume_ids or len(volume_ids) == 0:
        raise ValueError("volume_ids is required")

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
    Modify a specified LUN

    Args:
        client: DME API client
        volume_id: LUN ID
        name: New name (Optional, 1~255 characters)
        description: Modify LUN description (Optional, 0~255 characters)
        owner_controller: Owner controller (Optional, only non-service LUNs support modification)
        prefetch_policy: Prefetch policy (Optional, only non-service LUNs support modification)
                        Options: 0 (no prefetch), 1 (fixed prefetch), 2 (variable prefetch), 3 (smart prefetch)
        prefetch_value: Prefetch policy value (Optional, only non-service LUNs support modification)
        tuning: LUN tuning properties (Optional, only non-service LUNs support modification)。参数格式如下：{
                smarttier: Data migration policy (Optional, default 0). Options: 0 (no migration), 1 (auto migration), 2 (migrate to higher tier), 3 (migrate to lower tier),
                smartqos: SmartQos4Update object (Optional)。属性格式如下：{
                        maxbandwidth: Max bandwidth (Optional, 0~2147483647; supports all devices; mutually exclusive with minbandwidth/miniops for V3/V5 series),
                        maxiops: Max iops (Optional, 0~2147483647; supports all devices; mutually exclusive with minbandwidth/miniops for V3/V5 series),
                        minbandwidth: Min bandwidth (Optional, 0~2147483647; supports Dorado V6/V3/V5; mutually exclusive with maxbandwidth/maxiops for V3/V5 series),
                        miniops: Min iops (Optional, 0~2147483647; supports Dorado V6/V3/V5; mutually exclusive with maxbandwidth/maxiops for V3/V5 series),
                        control_policy: Control policy (Optional). Options: 0 (protect IO lower limit), 1 (control IO upper limit),
                        latency: Latency in ms or us (Optional, 0~2147483647; depends on storage device; only lower limit protection supports),
                        enabled: Whether to enable smartqos (Optional). Options: true, false,
                }
             }
        task_remarks: Async task remark (Optional, max 1024 characters)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/blockservice/v1/volumes/{volume_id}"

    if not volume_id:
        raise ValueError("volume_id is required")

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
    Batch modify LUN names

    Args:
        client: DME API client
        volumes: List of LUN info to modify (max array members: 1000)。参数格式如下：[{
                volume_id: LUN unique identifier (1~64 characters),
                name: New LUN name (1~255 characters, supports letters, digits, ._- and Chinese characters),
             }, ...]

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/blockservice/v1/volumes"

    if not volumes or len(volumes) == 0:
        raise ValueError("volumes is required")

    payload = {
        'volumes': volumes
    }

    response = client.put(url, body=payload)
    return response


def lun_expand(client: DMEAPIClient, volumes: list, task_remarks: str = None) -> dict:
    """
    Batch expand LUN capacity

    Args:
        client: DME API client
        volumes: List of LUN info to expand (max array members: 1000)。参数格式如下：[{
                volume_id: LUN unique identifier (Required, 1~64 characters),
                added_capacity: Capacity increase in GB (Required, 1~262144),
             }, ...]
        task_remarks: Async task remark (Optional, max 1024 characters)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/blockservice/v1/volumes/expand"

    if not volumes or len(volumes) == 0:
        raise ValueError("volumes is required")

    payload = {
        'volumes': volumes
    }

    if task_remarks is not None:
        payload['task_remarks'] = task_remarks

    response = client.post(url, body=payload)
    return response



def lun_connection(client: DMEAPIClient, volume_ids: list) -> dict:
    """
    Query connection info for specified LUN IDs.

    Args:
        client: DME API client
        volume_ids: LUN ID list (Required, List[string], max array members: 1000)

    Returns:
        {
            lun_id: LUN ID (string),
            lun_wwn: LUN WWN (string),
            iscsi_targets: iSCSI target list (List),
            fc_targets: FC target list (List),
        }
    """
    url = "/rest/blockservice/v1/volumes/connection-infos-query"

    if not volume_ids or len(volume_ids) == 0:
        raise ValueError("volume_ids is required")

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
    Batch query LUN groups

    Query the LUN group list with pagination and filtering.

    Args:
        client: DME API client
        page_size: Items per page (Optional, 0~1000, default 20)
        page_no: Page number (Optional, 1~10000000, default 1)
        sort_dir: Sort direction (Optional). Options: asc (ascending), desc (descending)
        sort_key: Sort field (Optional). Options: lun_count, total_capcity, capacity_usage, name, raw_id
        name: LUN group name (Optional, 1~256 characters, supports fuzzy search)
        vstore_raw_id: Tenant ID on storage device (Optional, 1~64 characters)
        vstore_name: Tenant name (Optional, 1~256 characters, supports fuzzy search)
        storage_id: Storage device ID (Optional, 1~64 characters)
        storage_name: Storage name (Optional, 1~256 characters, supports fuzzy search)
        raw_id: LUN group ID on storage device (Optional, 1~256 characters)
        attached: Mapping status (Optional). Options: true (mapped), false (unmapped)
        protection_group_raw_id: Protection group ID on device (Optional, 0~64 characters; non-empty = LUN groups under PG, empty = LUN groups not in any PG)
        avaiable_mapping_for_host_id: Available host ID for mapping (Optional, 1~64 characters; mutually exclusive with avaiable_mapping_for_host_group_id)
        avaiable_mapping_for_host_group_id: Available host group ID for mapping (Optional, 1~64 characters; mutually exclusive with avaiable_mapping_for_host_id)
        support_provisioning: Supports provisioning (Optional). Options: true, false

    Returns:
        {
            total: Total LUN groups (integer),
            lun_groups: LUN group list (List<LunGroupInfo>)。参数格式如下：[{
                id: LUN group ID (string),
                name: LUN group name (string),
                storage_id: Storage device ID (string),
                lun_count: LUN count (integer),
                attached: Mapping status (boolean),
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
    Query details of a specific LUN group.

    Args:
        client: DME API client
        group_id: LUN group ID (Required, string)
        storage_id: Storage device ID (Optional, string)

    Returns:
        {
            id: LUN group ID (string),
            name: LUN group name (string),
            storage_id: Storage device ID (string),
            lun_count: LUN count (integer),
            description: Description (string),
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
    Create LUN group

    Create a new LUN group.

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, 1~64 characters)
        name: LUN group name (Required, 1~255 characters, supports letters, digits, ._- and Chinese characters)
        description: LUN group description (Optional, 0~255 characters)
        existing_lun_ids: LUN ID list (Optional, mutually exclusive with customize_volumes, max array members: 1000)
        customize_volumes: CustomizeVolumesParam object (Optional, mutually exclusive with existing_lun_ids)。参数格式如下：{
                volume_specs: VolumeSpecsParam list (Optional, mutually exclusive with lun_specs_pass_through, max array members: 1000)。参数格式如下：[{
                        name: LUN name (Required, 1~255 characters, supports letters, digits, ._- and Chinese characters; when count>1, name length is 1~27),
                        description: LUN description (Optional, 0~255 characters),
                        count: Number of LUNs of this spec (Required, 1~500),
                        capacity: LUN capacity in GB (Required, 1~262144),
                        suffix_length: Naming suffix rule (Optional, 0~4; name length + suffix length <= 255),
                        start_suffix: Starting suffix number (Optional, 0~9999),
                        start_lun_id: Starting LUN ID (Optional, 0~65535),
                     }, ...],
                lun_specs_pass_through: lunSpecsPassThrough list (Optional, mutually exclusive with volume_specs, max array members: 24; required in pass-through mode)。参数格式如下：[{
                        name: LUN name (Required, 1~247 characters, supports letters, digits, -._ and Chinese characters; final name = LUN name + suffix + disk location),
                        description: LUN description (Optional, 0~255 characters),
                        disk_location: Disk location for LUN creation (Required, 1~255 characters),
                        count: LUNs per disk (Required, 1~8),
                        suffix_length: Suffix encoding length (Optional, 1~4, default 4; effective when count>1),
                        start_suffix: Suffix start encoding (Optional, 0~9999, default 0; effective when count>1),
                     }, ...],
                pool_raw_id: Storage pool ID on device (Optional, 1~64 characters; required when not in pass-through mode),
                availability_zone: Availability zone id (Optional, 0~64 characters),
                owner_controller: Owner controller (Optional, 0~64 characters),
                initial_distribute_policy: Initial capacity distribution policy (Optional, V3/V5 only, all-flash not supported). Options: 0 (auto), 1 (high-perf tier), 2 (perf tier), 3 (capacity tier). Default 0,
                prefetch_policy: Prefetch policy (Optional). Options: 0 (no prefetch), 1 (fixed prefetch), 2 (variable prefetch), 3 (smart prefetch). Default 3,
                prefetch_value: Prefetch value (Optional, 0~1024; fixed=0~1024KB, variable=0~1024x),
                tuning: CustomizeVolumeTuning object (Optional)。属性格式如下：{
                        smartqos: SmartQos object (Optional)。属性格式如下：{
                                name: Smart QoS name (Optional, 1~255 characters),
                        },
                        alloctype: LUN allocation type (Optional). Options: thin, thick,
                        workload_type_id: Workload type id (Optional, obtained from storage device),
                }
             }
        task_remarks: Async task remark (Optional, max 1024 characters)
        vstore_id: Tenant ID (Optional, 1~64 characters; effective for OceanStor V300R006C30/V500R007C20/Dorado 6.1.3+)
        zoning_info: ZoningParam object (Optional)。参数格式如下：{
                zone_policy_id: Zone policy id (Optional, 0~64 characters; auto zone if specified),
                target_fcports: Port WWN list (Optional, mutually exclusive with target_fcportgroups, max array members: 1000; effective when port_group_id is empty in mapping_view),
                target_fcportgroups: Port group id list (Optional, mutually exclusive with target_fcports, max array members: 1000; effective when port_group_id is empty in mapping_view),
             }
        mapping_view: MappingViewRequestParam object (Optional)。参数格式如下：{
                mapping_view_name: Mapping view name on device (Optional, max 31 characters),
                mapping_host_info: MappingHostInfo object (Optional, mutually exclusive with mapping_host_group_info)。属性格式如下：{
                        todo_host_name: Host name in todo task (Optional, 1~255 characters, supports letters, digits, ._- and Chinese),
                        id: Host ID (Optional, 1~64 characters),
                },
                mapping_host_group_info: MappingHostGroupInfo object (Optional, mutually exclusive with mapping_host_info)。属性格式如下：{
                        todo_host_group_name: Host group name in todo task (Optional, 1~255 characters, supports letters, digits, ._- and Chinese),
                        id: Host group ID (Optional, 1~64 characters),
                },
                port_group_id: Port group ID on device (Optional, 1~31 characters),
                start_host_lun_id: Starting HostLunID (Optional, 0~2147483647),
             }

    Returns:
        {
            id: LUN group ID (string, 1~64 characters),
        }
    """
    url = "/rest/blockservice/v1/lun-groups"

    if not storage_id or not name:
        raise ValueError("storage_id 和 name 是Required参数")

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
    Batch delete LUN groups

    Args:
        client: DME API client
        lun_group_ids: LUN group ID list (Required, max array members: 500)
        task_remarks: Async task remark (Optional, max 1024 characters)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/blockservice/v1/lun-groups/delete"

    if not lun_group_ids or len(lun_group_ids) == 0:
        raise ValueError("lun_group_ids is required")

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
    Add LUNs to a LUN group

    Args:
        client: DME API client
        group_id: LUN group ID
        existing_lun_ids: Existing LUN set (Optional, mutually exclusive with customize_volumes, max array members: 1000)。参数格式如下：[{
                lun_id: Existing LUN ID (Required, 1~64 characters),
             }, ...]
        customize_volumes: CustomizeVolumesParam object (Optional, mutually exclusive with existing_lun_ids)。参数格式如下：{
                volume_specs: VolumeSpecsParam list (Optional, mutually exclusive with lun_specs_pass_through, max array members: 1000)。参数格式如下：[{
                        name: LUN name (Required, 1~255 characters, supports letters, digits, ._- and Chinese; when count>1, name length 1~27),
                        description: LUN description (Optional, 0~255 characters),
                        count: LUN count of this spec (Required, 1~500),
                        capacity: LUN capacity in GB (Required, 1~262144),
                        suffix_length: Naming suffix rule (Optional, 0~4; name length + suffix length <= 255),
                        start_suffix: Starting suffix number (Optional, 0~9999),
                        start_lun_id: Starting LUN ID (Optional, 0~65535),
                     }, ...],
                lun_specs_pass_through: lunSpecsPassThrough list (Optional, mutually exclusive with volume_specs, max array members: 24; required in pass-through mode)。参数格式如下：[{
                        name: LUN name (Required, 1~247 characters, supports letters, digits, -._ and Chinese; final name = LUN name + suffix + disk location),
                        description: LUN description (Optional, 0~255 characters),
                        disk_location: Disk location for LUN (Required, 1~255 characters),
                        count: LUNs per disk (Required, 1~8),
                        suffix_length: Suffix encoding length (Optional, 1~4, default 4; effective when count>1),
                        start_suffix: Suffix start encoding (Optional, 0~9999, default 0; effective when count>1),
                     }, ...],
                pool_raw_id: Storage pool ID on device (Optional, 1~64 characters; required when not pass-through mode),
                availability_zone: Availability zone id (Optional, 0~64 characters),
                owner_controller: Owner controller (Optional, 0~64 characters),
                initial_distribute_policy: Initial capacity distribution policy (Optional, V3/V5 only, all-flash not supported). Options: 0 (auto), 1 (high-perf tier), 2 (perf tier), 3 (capacity tier). Default 0,
                prefetch_policy: Prefetch policy (Optional). Options: 0 (no prefetch), 1 (fixed prefetch), 2 (variable prefetch), 3 (smart prefetch). Default 3,
                prefetch_value: Prefetch value (Optional, 0~1024; fixed=0~1024KB, variable=0~1024x),
                tuning: CustomizeVolumeTuning object (Optional)。属性格式如下：{
                        smartqos: SmartQos object (Optional)。属性格式如下：{
                                name: Smart QoS name (Optional, 1~255 characters),
                        },
                        alloctype: LUN allocation type (Optional). Options: thin, thick,
                        workload_type_id: Workload type id (Optional),
                }
             }
        host_lun_id_infos: HostLunIdInfo list (Optional, max array members: 1000; Dorado V6/V7 and OceanStor V6/V7 only)。参数格式如下：[{
                host_lun_id: Host LUN ID assigned to LUN (Required, 0~4095),
                lun_id: LUN ID to add to group (Required, 1~64 characters),
             }, ...]
        host_lun_id_verify: Whether to verify active-active host LUN ID consistency (Optional, default false). Options: true (skip verify), false (verify)
        task_remarks: Async task remark (Optional, max 1024 characters)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Remove LUNs from a LUN group

    Args:
        client: DME API client
        group_id: LUN group ID
        lun_ids: LUN ID list (Required, min array members: 1, max array members: 10000)
        task_remarks: Async task remark (Optional, max 1024 characters)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
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
    Query LUNs in a LUN group

    Args:
        client: DME API client
        group_id: LUN group ID
        page_size: Items per page (Optional, 1~1000, default 100)
        page_no: Page number (Optional, 1~10000000, default 1)
        health_status: Health status (Optional). Options: normal, faulty, write_protected

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes LUN list
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


# Action list for CLI help

# ============================================================================
# Mapping view (mapping_view) subtopic functions
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
    Create mapping view

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, 1~64 characters)
        name: Mapping view name (Optional, 1~31 characters; effective for OceanStor V3/V5)
        port_group_id: Port group ID (Optional, 1~64 characters)
        start_host_lun_id: Host LUN SCSI ID start value (Optional, 0~2147483647)
        host: Storage host (Optional, mutually exclusive with vbs/host_group)。属性格式如下：{
                todo_host_name: Host name in todo task (Optional, 1~255 characters, supports letters, digits, ._- and Chinese),
                id: Host ID (Optional, 1~64 characters),
             }
        vbs: VBS client (Optional, mutually exclusive with host/host_group; OceanStor Pacific and FusionStorage only)。属性格式如下：{
                id: VBS ID (Optional, 1~64 characters),
             }
        host_group: Storage host group (Optional, mutually exclusive with host/vbs)。属性格式如下：{
                todo_host_group_name: Host group name in todo task (Optional, 1~255 characters, supports letters, digits, ._- and Chinese),
                id: Host group ID (Optional, 1~64 characters),
             }
        lun_group: LUN group to map (Optional, mutually exclusive with luns)。属性格式如下：{
                id: LUN group ID (Optional, 1~64 characters),
             }
        luns: LUN info to map (Optional, mutually exclusive with lun_group)。属性格式如下：{
                ids: LUN ID list to map (Optional, max array members: 1000),
                lungroup_name: LUN group name (Optional, 1~255 characters; sent when creating LUN group during LUN mapping),
             }
        task_remarks: Async task remark (Optional, max 1024 characters)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Batch delete mapping views.

    Args:
        client: DME API client
        ids: Mapping view ID list (Required, List[string])

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/blockservice/v1/mapping-views/batch-delete"

    if not ids or len(ids) == 0:
        raise ValueError("ids is required")

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
    Batch query mapping view list

    Query mapping view information on storage devices with filtering.

    Args:
        client: DME API client
        page_size: Items per page (Optional, 0~1000, default 100)
        page_no: Page number (Optional, 1~10000000, default 1)
        name: Mapping view name (Optional, 0~256 characters, supports fuzzy search)
        raw_id: Mapping view ID on storage device (Optional, 1~256 characters)
        storage_id: Storage device unique ID (Optional, 0~64 characters)
        lun_id: LUN unique ID (Optional, 0~64 characters; cannot be used with lun_name)
        lun_name: LUN name (Optional, 1~256 characters, supports fuzzy search; cannot be used with lun_id)
        lun_group_id: LUN group unique ID (Optional, 0~64 characters; cannot be used with lun_group_raw_id/lun_group_name)
        lun_group_raw_id: Device-assigned LUN group ID (Optional, 1~64 characters; cannot be used with lun_group_id/lun_group_name)
        lun_group_name: LUN group name (Optional, 1~256 characters, supports fuzzy search; cannot be used with lun_group_id/lun_group_raw_id)
        storage_host_id: Storage host unique ID (Optional, 0~64 characters; cannot be used with storage_host_name)
        storage_host_name: Storage host name (Optional, 0~256 characters, supports fuzzy search; OceanStor Dorado v6 and OceanProtect X only; cannot be used with storage_host_id)
        storage_host_group_id: Storage host group unique ID (Optional, 0~64 characters; cannot be used with storage_host_group_name/storage_host_group_raw_id)
        storage_host_group_name: Storage host group name (Optional, 0~256 characters, supports fuzzy search; cannot be used with storage_host_group_id/storage_host_group_raw_id)
        storage_host_group_raw_id: Device-assigned storage host group ID (Optional, 1~64 characters; cannot be used with storage_host_group_id/storage_host_group_name)
        port_group_id: Port group unique ID (Optional, 0~64 characters; cannot be used with port_group_raw_id/port_group_name)
        port_group_raw_id: Device-assigned port group ID (Optional, 1~64 characters; cannot be used with port_group_id/port_group_name)
        port_group_name: Port group name (Optional, 0~256 characters, supports fuzzy search; cannot be used with port_group_id/port_group_raw_id)
        sort_key: Sort field (Optional). Options: raw_id, storage_host_group_raw_id, lun_group_raw_id, port_group_raw_id
        sort_dir: Sort direction (Optional). Options: asc (ascending), desc (descending)

    Returns:
        {
            total: Total mapping views (integer),
            mapping_views: Mapping view list (List<MappingViewInfo>)。参数格式如下：[{
                id: Mapping view ID (string),
                name: Mapping view name (string),
                storage_id: Storage device ID (string),
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
    Query mapping relationships for physical host/group

    Query mapping views on a storage device filtered by physical host/host group ID.

    Args:
        client: DME API client
        type: Query type (Required). Options: host, host_group
        request_id: Physical host/host group ID (Required, 1~64 characters)
        storage_id: Storage device ID (Required, 1~64 characters)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes mapping view list
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
    Query mapping relationships for a physical host

    Args:
        client: DME API client
        host_id: Physical host ID (Required, 1~64 characters)
        storage_id: Storage device ID (Required, 1~64 characters)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes mapping view list
    """
    return mapping_view_query(
        client=client, type="host",
        request_id=host_id, storage_id=storage_id
    )


def physical_host_group_show_mapping_views(client: DMEAPIClient, host_group_id: str,
                                            storage_id: str) -> dict:
    """
    Query mapping relationships for a physical host group

    Args:
        client: DME API client
        host_group_id: Physical host group ID (Required, 1~64 characters)
        storage_id: Storage device ID (Required, 1~64 characters)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes mapping view list
    """
    return mapping_view_query(
        client=client, type="host_group",
        request_id=host_group_id, storage_id=storage_id
    )


# ============================================================================
# Storage host (storage_host) subtopic functions
# ============================================================================

def storage_host_create(client: DMEAPIClient, storage_id: str,
                host_info: dict, task_remarks: str = None,
                vstore_id: str = None) -> dict:
    """
    Create storage host

    Create a storage host on the specified storage device.

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, 1~64 characters)
        host_info: CreateStorageHostInfo object (Required)。属性格式如下：{
                name: Host name (Required, 1~255 characters, supports letters, digits, ._- and Chinese),
                os_type: Host type (Required). Options: LINUX, WINDOWS, WINDOWSSERVER2012, SOLARIS, HPUX, AIX, XENSERVER, LINUX_VIS, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC,
                ip: Host IP address (Optional, max 127 characters),
                description: Host description (Optional, max 63 characters),
                initiators: StorageInitiatorParam list (Optional, max array members: 1000)。参数格式如下：[{
                        protocol: Initiator type (Required). Options: fc, iscsi, nvme_over_roce,
                        raw_id: Host initiator wwpn or iqn or nqn (Required, 1~223 characters),
                        alias: Initiator alias (Optional, max 31 characters),
                     }, ...],
                multipath: MultiPathForCreateRequestParam object (Optional)。属性格式如下：{
                        multipath_type: Third-party multipath policy (Required). Options: default, third_party,
                        path_type: Initiator path type (Optional, effective with third-party multipath). Options: optimal_path, non_optimal_path,
                        failover_mode: Initiator failover mode (Optional, effective with third-party multipath). Options: early_version_alua, common_alua, alua_not_used, special_alua,
                        special_mode_type: Special mode type (Optional, effective when mode is special). Options: mode_zero, mode_one, mode_two, mode_three,
                }
             }
        task_remarks: Async task remark (Optional, max 1024 characters)
        vstore_id: Tenant ID (Optional, 1~64 characters; effective for OceanStor V300R006C30/V500R007C20/Dorado 6.1.3+)

    Returns:
        Task ID
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
    Batch query storage hosts by ID list

    Args:
        client: DME API client
        ids: ID list (Required, 1~1000)

    Returns:
        Storage host info list
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
    Batch query storage hosts

    Args:
        client: DME API client
        page_size: Items per page (Optional, 1~1000, default 20)
        page_no: Page number (Optional, min 1, default 1)
        sort_key: Sort key (Optional, sort_dir ineffective without sort_key). Options: ip, name, initiator_count, lun_count, lun_group_count, capacity, allocated_capacity, raw_id
        sort_dir: Sort direction (Optional). Options: desc (descending), asc (ascending)
        name: Host name (Optional, 1~256 characters, supports fuzzy match)
        raw_id: Host ID on device (Optional, 0~256 characters)
        host_group_id: Host group ID (Optional, max 64 characters)
        avaliable_add_to_host_group_id: Target host group ID for adding (Optional, mutually exclusive with host_group_id, max 64 characters)
        host_group_name: Host group name (Optional, max 256 characters, supports fuzzy match; empty string = hosts not in any host group)
        ip: Host IP (Optional, max 256 characters, supports fuzzy match; empty string = hosts without IP)
        health_status: Health status (Optional). Options: normal, no_redundant_link, offline, fault, degraded
        os_type: Storage host type (Optional). Options: LINUX, WINDOWS, WINDOWSSERVER2012, SOLARIS, HPUX, AIX, XENSERVER, LINUX_VIS, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC, UNKNOWN
        storage_id: Storage device ID (Optional, 1~64 characters)
        avaiable_mapping_for_lun_group_id: Available LUN group ID for mapping (Optional, 1~64 characters; mutually exclusive with avaiable_mapping_for_lun_id)
        avaiable_mapping_for_lun_id: Available LUN ID for mapping (Optional, 1~64 characters; mutually exclusive with avaiable_mapping_for_lun_group_id)
        support_provisioning: Supports provisioning (Optional). Options: true, false
        manufacturer: Storage device vendor (Optional, 1~64 characters). Options: huawei, dell_emc, fujitsu, hitachi, hpe, ibm, netapp, pure, third_part
        vstore_raw_id: Tenant ID (Optional)
        vstore_name: Tenant name (Optional)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes storage host list and total
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
    Modify storage host

    Args:
        client: DME API client
        storage_host_id: Storage host ID (Required)
        storage_host_name: Storage host name (Optional, 1~255 characters, supports letters, digits, ._- and Chinese)
        storage_host_description: Storage host description (Optional, 0~63 characters)
        storage_host_ip: Host IP (Optional, max 127 characters)
        storage_host_os_type: Host type (Optional). Options: UNKNOWN, LINUX, WINDOWS, SUSE, EULER, REDHAT, CENTOS, WINDOWSSERVER2012, SOLARIS, LINUX_VIS, HPUX, AIX, XENSERVER, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC
        add_initiators: StorageInitiatorParam list (Optional, max array members: 1000)。参数格式如下：[{
                protocol: Initiator type (Required). Options: fc, iscsi, nvme_over_roce,
                raw_id: Host initiator wwpn or iqn or nqn (Required, 1~223 characters),
                alias: Initiator alias (Optional, max 31 characters),
             }, ...]
        remove_initiators: Initiator ID list to remove (Optional, max array members: 1000)
        multipath: MultiPathForCreateRequestParam object (Optional)。属性格式如下：{
                multipath_type: Third-party multipath policy (Required). Options: default, third_party,
                path_type: Initiator path type (Optional, effective with third-party multipath). Options: optimal_path, non_optimal_path,
                failover_mode: Initiator failover mode (Optional, effective with third-party multipath). Options: early_version_alua, common_alua, alua_not_used, special_alua,
                special_mode_type: Special mode type (Optional, effective when mode is special). Options: mode_zero, mode_one, mode_two, mode_three,
             }
        access_mode: Host access mode (Optional, Dorado V6+ only). Options: balanced, asymmetric
        hyper_metro_path_optimized: HyperMetro preferred path (Optional, Dorado V6+ only). Options: true, false
        task_remarks: Async task remark (Optional, max 1024 characters)

    Returns:
        Modification result
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
    Batch delete storage hosts

    Batch delete the specified storage hosts.

    Args:
        client: DME API client
        host_ids: Storage host ID list (Required, max 1000)

    Returns:
        Deletion result
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
    Batch query storage host path information

    Args:
        client: DME API client
        page_no: Page number (Optional, 1~2147483647, default 1)
        page_size: Page size (Optional, 1~1000, default 20)
        storage_id: Storage device ID (Optional, 1~64 characters)
        storage_host_ids: Storage host ID list (Optional, mutually exclusive with storage_host_raw_ids, max array members: 20; single ID 1~64 characters)
        storage_host_raw_ids: Storage host ID list on device (Optional, mutually exclusive with storage_host_ids, max array members: 20; single ID 1~64 characters)
        health_status: Health status (Optional). Options: normal, fault, no_redundant_link, offline
        running_status: Link status (Optional). Options: link_up, link_down, online, disabled, connecting
        initiator_type: Initiator type (Optional). Options: iSCSI, FC, NVMe_over_RoCE, IB, vHBA

    Returns:
        Path information list
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
# Storage host group (storage_host_group) subtopic functions
# ============================================================================

def storage_host_group_create(client: DMEAPIClient, storage_id: str, name: str,
                      description: str = None, exist_host_ids: list = None,
                      create_storage_host_params: dict = None,
                      task_remarks: str = None, vstore_id: str = None) -> dict:
    """
    Create storage host group

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, 1~64 characters)
        name: Host group name (Required, 1~255 characters, supports letters, digits, ._- and Chinese; V3/V5 max 31 bytes, V6 max 255 bytes)
        description: Description (Optional, 0~63 characters)
        exist_host_ids: Host ID list to add to host group (Optional, mutually exclusive with create_storage_host_params, max array members: 1000)
        create_storage_host_params: Create new storage host list (Optional, mutually exclusive with exist_host_ids, max array members: 1000)。参数格式如下：[{
                name: Host name (Required, 1~255 characters, supports letters, digits, ._- and Chinese),
                os_type: Host type (Required). Options: LINUX, WINDOWS, WINDOWSSERVER2012, SOLARIS, HPUX, AIX, XENSERVER, LINUX_VIS, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC,
                ip: Host IP address (Optional, max 127 characters),
                description: Host description (Optional, max 63 characters),
                initiators: Initiator list (Optional, max array members: 1000)。参数格式如下：[{
                        protocol: Initiator type (Required). Options: fc, iscsi, nvme_over_roce,
                        raw_id: Host initiator wwpn or iqn or nqn (Required, 1~223 characters),
                        alias: Initiator alias (Optional, max 31 characters),
                     }, ...],
                multipath: Multipath configuration (Optional)。属性格式如下：{
                        multipath_type: Third-party multipath policy (Required). Options: default, third_party,
                        path_type: Initiator path type (Optional, effective with third-party multipath). Options: optimal_path, non_optimal_path,
                        failover_mode: Initiator failover mode (Optional, effective with third-party multipath). Options: early_version_alua, common_alua, alua_not_used, special_alua,
                        special_mode_type: Special mode type (Optional, effective when mode is special). Options: mode_zero, mode_one, mode_two, mode_three,
                }
             }, ...]
        task_remarks: Async task remark (Optional, max 1024 characters)
        vstore_id: Tenant ID (Optional, 1~64 characters; effective for OceanStor V300R006C30/V500R007C20/Dorado 6.1.3+)

    Returns:
        Task ID
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
    Batch query storage host groups

    Args:
        client: DME API client
        raw_id: Host group ID on device (Optional, 0~256 characters)
        storage_id: Device ID (Optional, 0~64 characters)
        page_size: Items per page (Optional, 1~1000, default 100)
        page_no: Page number (Optional, 1~10000000, default 1)
        sort_dir: Sort direction (Optional, ineffective without sort_key). Options: desc (descending), asc (ascending)
        sort_key: Sort key (Optional). Options: name, host_count, lun_group_count, lun_count, raw_id
        name: Host group name (Optional, 0~256 characters, supports fuzzy match)
        vstore_id: Tenant ID (Optional)
        vstore_name: Tenant name (Optional)
        avaiable_mapping_for_lun_group_id: Target LUN group ID for mapping (Optional, 0~64 characters; required when querying host groups mappable to LUN group)
        avaiable_mapping_for_lun_id: Target LUN ID for mapping (Optional, 0~64 characters; required when querying host groups mappable to LUN)
        support_provisioning: Supports provisioning (Optional). Options: true, false

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes host group list and total
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
    Add storage host to storage host group

    Add existing hosts toStorage host组，or create new hosts in host group。

    Args:
        client: DME API Client
        storage_host_group_id: Storage host组 ID (Required)
        storage_host_id_ids: 存储Host ID列表 (可选, 与create_storage_host_paramsmutually exclusive, max array members: 1000)
        create_storage_host_params: 创建新的Storage host列表 (可选, 与storage_host_id_idsmutually exclusive, max array members: 1000)。参数格式如下：[{
                name: Host name (Required, 1~255 characters, supports alphanumeric._-and Chinese characters),
                os_type: Host type (Required)。Options：LINUX, WINDOWS, WINDOWSSERVER2012, SOLARIS, HPUX, AIX, XENSERVER, LINUX_VIS, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC,
                ip: 主机ip地址 (可选, 最多127 characters),
                description: 主机描述 (可选, 最多63 characters),
                initiators: Initiator list (可选, max array members: 1000)。参数格式如下：[{
                        protocol: Initiator type (Required)。Options：fc, iscsi, nvme_over_roce,
                        raw_id: 主机Initiatorwwpn或iqn或nqn (Required, 1~223 characters),
                        alias: Initiator alias (可选, 最多31 characters),
                     }, ...],
                multipath: 多路径配置 (可选)。属性格式如下：{
                        multipath_type: Third-party multipath策略 (Required)。Options：default (默认), third_party (Third-party multipath),
                        path_type: Initiator路径类型 (可选, 开启Third-party multipatheffective when)。Options：optimal_path (优选路径), non_optimal_path (非优选路径),
                        failover_mode: Initiator切换模式 (可选, 开启Third-party multipatheffective when)。Options：early_version_alua, common_alua, alua_not_used, special_alua,
                        special_mode_type: Special mode type (可选, effective when failover mode is special)。Options：mode_zero, mode_one, mode_two, mode_three,
                }
             }, ...]
        task_remarks: Async taskRemark (可选, 最多1024 characters)

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
    Remove host from storage host group

    从指定的Storage hostRemove one or more hosts from group。

    Args:
        client: DME API Client
        storage_host_group_id: Storage host组 ID（Required，1~64 字符）
        storage_host_ids: hosts to remove ID 列表（Required，最多 1000 个）
        task_remarks: Task remark(Optional, max 1024 字符）

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
    Batch delete storage host groups

    Batch delete指定的Storage host组。

    Args:
        client: DME API Client
        host_group_ids: Storage host组 ID 列表（Required，1~100 个）
        task_remarks: Task remark(Optional, max 1024 字符）

    Returns:
        Deletion result
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
    Query LUN mapping list for storage host

    指定Storage host查询映射 LUN info list，包含 LUN 信息和主机 LUN ID 信息。

    Args:
        client: DME API Client
        storage_host_id: Storage host ID（Required，1~64 字符）
        name: LUN Name (Optional,1~256 字符，支持fuzzy search）
        page_size: Items per page（可选，1~1000，默认 20）
        page_no: Page queryStart position（可选，1~10000000，默认 1）
        sort_key: Sort field（可选，host_lun_id/mapping_view_raw_id/lun_raw_id）
        sort_dir: Sort direction（可选，asc/desc，默认 desc）

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含 total 和 lun_mapping_list
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
    Query LUN mapping list for storage host group

    指定Storage host组查询映射 LUN info list，包含 LUN 信息和主机 LUN ID 信息。

    Args:
        client: DME API Client
        storage_host_group_id: Storage host组 ID（Required，1~64 字符）
        name: LUN Name (Optional,1~256 字符，支持fuzzy search）
        page_size: Items per page（可选，1~1000，默认 20）
        page_no: Page queryStart position（可选，1~10000000，默认 1）
        sort_key: Sort field（可选，host_lun_id/mapping_view_raw_id/lun_raw_id）
        sort_dir: Sort direction（可选，asc/desc，默认 desc）

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含 total 和 lun_mapping_list
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
# Port group (port_group) subtopic functions
# ============================================================================

def port_group_list(client: DMEAPIClient, storage_id: str = None,
                    page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch query port groups

    Args:
        client: DME API client
        storage_id: Storage device ID (Optional, 1~64 characters, supports filtering)
        page_no: Page number (Optional, 1~10000, default 1)
        page_size: Items per page (Optional, 1~1000, default 20)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes port group list
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
    Create port group

    Note: Only supports OceanStor 1800 series storage.

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, 1~64 characters)
        name: Port group name (Required, 1~255 characters, supports letters, digits, ._- and Chinese)
        description: Port group description (Optional, 0~63 characters)
        port_ids: Port ID list to associate (Optional, max array members: 10; supports ROCE ports and logical ports, only one type)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes new port group ID
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
    Batch query ports of a specified port group

    Args:
        client: DME API client
        port_group_id: Port group ID (Required)
        type: Port type (Optional). Options: fc (FC port), fcoe (FCoE port), eth (Ethernet), roce (RoCE port)
        page_no: Page number (Optional, 1~10000, default 1)
        page_size: Items per page (Optional, 1~1000, default 20)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes port list
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
    Batch query port group to port associations

    Args:
        client: DME API client
        page_no: Page number (Optional, 1~10000, default 1)
        page_size: Items per page (Optional, 1~1000, default 20)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes association list
    """
    url = "/rest/storagemgmt/v1/port-groups/ports/relations/query"

    payload = {
        'page_no': page_no,
        'page_size': page_size
    }

    response = client.post(url, body=payload)
    return response




# ============================================================================
# Action list for CLI help
# ============================================================================


# ============================================================================
# Physical host (physical_host) subtopic functions
# ============================================================================

def physical_host_list(client: DMEAPIClient, limit: int = None, start: int = None,
               sort_key: str = None, sort_dir: str = None, name: str = None,
               host_group_name: str = None, ip: str = None,
               display_status: str = None, managed_status: list = None,
               os_type: str = None, access_mode: str = None,
               az_id: str = None, az_ids: list = None,
               project_id: str = None) -> dict:
    """
    Batch query physical hosts

    Args:
        client: DME API client
        limit: Items per page (Optional, 1~1000)
        start: Start position (Optional, 0~10000000)
        sort_key: Sort key (Optional). Options: initiator_count, ip, name
        sort_dir: Sort direction (Optional, ineffective without sort_key). Options: desc (descending), asc (ascending)
        name: Physical host name (Optional, 1~256 characters, supports fuzzy match)
        host_group_name: Physical host group name (Optional, 1~256 characters, supports fuzzy match)
        ip: Physical host IP (Optional, 1~256 characters, supports fuzzy match)
        display_status: Display status (Optional, 1~32 characters). Options: OFFLINE, NOT_RESPONDING, GRAY, NORMAL, RED, YELLOW, REBOOTING, INITIAL, BOOTING, SHUTDOWNING
        managed_status: Managed status list (Optional, max array members: 1000). Options: UNKNOWN, NORMAL, TAKE_OVERING, TAKE_ERROR, TAKE_OVER_ALARM
        os_type: Host type (Optional). Options: UNKNOWN, LINUX, WINDOWS, SUSE, EULER, REDHAT, CENTOS, WINDOWSSERVER2012, SOLARIS, LINUX_VIS, HPUX, AIX, XENSERVER, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC
        access_mode: Physical host access mode (Optional). Options: ACCOUNT, NONE, VCENTER, FUSIONSPHERE, HCS, TPOPS
        az_id: Availability zone ID (Optional, 1~64 characters; ignored when az_ids is provided)
        az_ids: Availability zone ID list (Optional, max array members: 40)
        project_id: Project group ID (Optional, 1~64 characters)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes physical host list and total
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
    Query a specified physical host

    Args:
        client: DME API client
        host_id: Physical host ID (Required)

    Returns:
        Physical host details
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
    Onboard a physical host

    Args:
        client: DME API client
        access_mode: Physical host access mode (Required). Options: ACCOUNT, NONE
        type: Host type (Required). Options: UNKNOWN, LINUX, WINDOWS, SUSE, EULER, REDHAT, CENTOS, WINDOWSSERVER2012, SOLARIS, LINUX_VIS, HPUX, AIX, XENSERVER, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC. ACCOUNT mode only supports LINUX
        host_name: Physical host name (Required in NONE mode, 1~255 characters, supports letters, digits, ._- and Chinese)
        ip: Physical host IP address (Effective in ACCOUNT mode, supports IPv4 and IPv6, max 127 characters)
        port: Physical host access port (Required in ACCOUNT mode, 1~65535)
        username: Physical host access username (Required in ACCOUNT mode, 1~255 characters)
        password: Physical host access password (Required in ACCOUNT mode, 1~1024 characters)
        description: Physical host description (Optional, 0~63 characters)
        initiator: Physical host initiator list (Required in NONE mode)。参数格式如下：[{
                protocol: Initiator type (Required). Options: FC, ISCSI, NVME_OVER_ROCE,
                port_name: Host initiator wwn or iqn (Required, 1~223 characters),
             }, ...]
        azs: Availability zone ID list (Optional, max array members: 40)
        project_id: Project group ID (Optional, 1~64 characters)
        sync_to_storage: Auto-sync host info to storage (Optional, default false). Options: true, false
        multipath_type: Multipath type (Optional). Options: default, third_party
        path_type: Initiator path type (Optional, effective with third-party multipath). Options: optimal_path, non_optimal_path
        failover_mode: Initiator failover mode (Optional, effective with third-party multipath). Options: early_version_alua, common_alua, alua_not_used, special_alua
        special_mode_type: Special mode type (Optional, effective when mode is special). Options: mode_zero, mode_one, mode_two, mode_three
        save_public_key: Auto-save physical host public key (Optional, default false). Options: true, false

    Returns:
        Created physical host info
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
    Modify physical host basic info

    Args:
        client: DME API client
        host_id: Physical host ID (Required)
        ip: Physical host IP address (Optional, max 127 characters, supports IPv4 and IPv6; empty = unchanged)
        host_name: Physical host name (Optional, 1~255 characters, supports letters, digits, ._-; empty = unchanged)
        os_type: Host type (Optional). Options: LINUX, WINDOWS, WINDOWSSERVER2012, SOLARIS, HPUX, AIX, XENSERVER, LINUX_VIS, MACOS, VMWAREESX, ORACLE, OPENVMS, ORACLE_VM_SERVER_FOR_X86, ORACLE_VM_SERVER_FOR_SPARC
        azs: Availability zone ID list (Optional, max array members: 40; null or empty = disassociate AZ)
        project_id: Project group ID (Optional, 0~64 characters; empty = unchanged; empty string = disassociate; non-empty and different = associate to new project)

    Returns:
        Modification result
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
    Modify physical host access info

    Args:
        client: DME API client
        host_id: Physical host ID (Required, 1~64 characters)
        ip: Physical host access IP (Optional, max 127 characters, supports IPv4 and IPv6; required for NONE to ACCOUNT transition)
        port: Physical host access port (Optional, 1~65535; required for NONE to ACCOUNT transition)
        username: Physical host access username (Optional, 1~255 characters; required for NONE to ACCOUNT transition)
        password: Physical host access password (Optional, 1~1024 characters; required for NONE to ACCOUNT transition)
        project_id: Project group ID (Optional, 0~64 characters; empty = unchanged; empty string = disassociate; non-empty and different = associate to new project)
        azs: Availability zone ID list (Optional, max array members: 40; null or empty = disassociate AZ)
        sync_to_storage: Sync storage host info (Optional, default false). Options: true, false
        description: Physical host description (Optional, 0~63 characters)
        multipath_type: Multipath type (Optional). Options: default, third_party
        path_type: Initiator path type (Optional, effective with third-party multipath). Options: optimal_path, non_optimal_path
        failover_mode: Initiator failover mode (Optional, effective with third-party multipath). Options: early_version_alua, common_alua, alua_not_used, special_alua
        special_mode_type: Special mode type (Optional, effective when mode is special). Options: mode_zero, mode_one, mode_two, mode_three

    Returns:
        Modification result
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
    Remove physical host

    Remove the specified physical host.

    Args:
        client: DME API client
        host_id: Physical host ID (Required)
        sync_to_storage: Sync delete from storage (Optional, default false)

    Returns:
        Deletion result
    """
    url = "/rest/hostmgmt/v1/hosts/{host_id}"

    response = client.delete(url, params={"host_id": host_id, "sync_to_storage": str(sync_to_storage).lower()})
    return response


def physical_host_add_initiators(client: DMEAPIClient, host_id: str,
                  initiators: list) -> dict:
    """
    Add initiators to a physical host

    Args:
        client: DME API client
        host_id: Physical host ID (Required)
        initiators: Initiator list (Required, max array members: 100)。参数格式如下：[{
                protocol: Initiator type (Required). Options: FC (WWPN format, 16-char hex), ISCSI, NVME_OVER_ROCE,
                port_name: Host initiator wwn or iqn (Required, 1~223 characters),
             }, ...]

    Returns:
        Addition result
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
    Remove initiators from a physical host

    Args:
        client: DME API client
        host_id: Physical host ID (Required)
        initiators: Initiator ID list (Required, max 1000)

    Returns:
        Removal result
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
    Query initiators of a specified physical host

    Args:
        client: DME API client
        host_id: Physical host ID (Required)
        port_name: Physical host initiator wwn or iqn (Optional, 1~223 characters)
        protocol: Initiator type (Optional, 1~64 characters). Options: UNKNOWN, FC, ISCSI, NVME_OVER_ROCE, SAS, NVME_OVER_FABRIC
        status: Initiator status (Optional, 1~32 characters). Options: UNKNOWN, ONLINE, OFFLINE, UNBOUND

    Returns:
        Initiator list
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
    Test connectivity between storage device and physical host

    Args:
        client: DME API client
        storage_id: Storage device ID (Required)
        host_ids: Physical host ID list (Optional, mutually exclusive with hostgroup_id)
        hostgroup_id: Physical host group ID (Optional, mutually exclusive with host_ids)
        auto_zoning: Auto zoning policy (Optional, default false)
        target_fcports: Port WWN list (Optional, effective when auto_zoning is true)
        target_fcportgroups: Port group ID list (Optional, effective when auto_zoning is true)

    Returns:
        Connectivity test result
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
    Save SSH public key for a physical host

    Save the SSH public key of a physical host for identity verification in subsequent communications.

    Args:
        client: DME API client
        ip: Physical host IP address (Required)
        key: Physical host SSH public key (Required)
        port: SSH port (Optional, default 22)

    Returns:
        Save result
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
    Query SSH public key of a physical host

    Args:
        client: DME API client
        ip: Physical host IP address (Required)
        port: SSH port (Optional, default 22)

    Returns:
        SSH public key info
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
    Query associated physical host by initiator

    Query the physical host associated with an initiator by initiator ID or WWPN/IQN/NQN.

    Args:
        client: DME API client
        initiator_id: Initiator ID (Optional, mutually exclusive with raw_id)
        raw_id: Initiator WWPN/IQN/NQN (Optional, mutually exclusive with initiator_id)
        protocol: Initiator type (Optional, FC/ISCSI/NVME_OVER_ROCE)

    Returns:
        Associated physical host info
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
    Map LUNs to a physical host

    Map LUNs to the specified physical host.

    Args:
        client: DME API client
        volume_ids: LUN ID list (Required, max array members: 1000)
        host_id: Physical host ID (Required, 1~64 characters)
        mapping_policy: MappingPolicy list (Optional, max array members: 64; not needed for service LUNs)。参数格式如下：[{
                storage_id: Storage device ID (Optional, 0~64 characters),
                start_host_lun_id: Starting host LUN ID (Optional, 0~4095),
                auto_zoning: Auto zone (Optional). Options: true, false,
                zone_policy_id: Zone policy ID (Optional, 0~64 characters; effective when auto_zoning is true),
                target_fcports: Port WWN list (Optional, mutually exclusive with target_fcportgroups, max array members: 1000; effective when auto_zoning is true),
                target_fcportgroups: Port group ID list (Optional, mutually exclusive with target_fcports, max array members: 1000; effective when auto_zoning is true),
                mapping_view: MappingRequest object (Optional)。属性格式如下：{
                        mapping_view_id: Mapping view ID on device (Optional, max 31 characters),
                        mapping_view_name: Mapping view name on device (Optional, max 31 characters),
                        lun_group_id: LUN group ID on device (Optional, max 31 characters),
                        lun_group_name: LUN group name on device (Optional, max 255 characters),
                        port_group_id: Port group ID on device (Optional, max 31 characters),
                }
             }, ...]
        task_remarks: Async task remark (Optional, max 1024 characters)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Unmap LUNs from a host

    Unmap LUNs from the specified host.

    Args:
        client: DME API client
        volume_ids: LUN ID list (Required, max array members: 1000)
        host_id: Host ID (Required, 1~64 characters)
        task_remarks: Async task remark (Optional, max 1024 characters)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Unmap LUNs from a storage host

    Unmap the LUN association with the storage host.

    Args:
        client: DME API client
        volume_ids: LUN ID list (Required, max array members: 1000)
        host_id: Host ID (Required, 1~64 characters)
        task_remarks: Async task remark (Optional, max 1024 characters)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
# Physical host group (physical_host_group) subtopic functions
# ============================================================================

def physical_host_group_list(client: DMEAPIClient, limit: int = None, start: int = None,
         sort_dir: str = None, sort_key: str = None, name: str = None,
         project_id: str = None, az_ids: list = None,
         managed_status: list = None) -> dict:
    """
    Batch query physical host groups

    Args:
        client: DME API client
        limit: Items per page (Optional, 1~1000)
        start: Start position (Optional, 0~10000000)
        sort_dir: Sort direction (Optional, ineffective without sort_key). Options: desc (descending), asc (ascending)
        sort_key: Sort key (Optional, 1~255 characters). Options: host_count
        name: Physical host group name (Optional, 1~256 characters, supports fuzzy match)
        project_id: Project group ID (Optional, 1~64 characters)
        az_ids: Availability zone ID list (Optional, max array members: 1000; single ID 1~64 characters)
        managed_status: Managed status list (Optional, max array members: 1000). Options: UNKNOWN, NORMAL, TAKE_OVERING, TAKE_ERROR, TAKE_OVER_ALARM

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes physical host group list and total
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
    Query physical hosts in a physical host group

    Query the list of physical hosts in a specified physical host group.

    Args:
        client: DME API client
        hostgroup_id: Physical host group ID (Required, 1~64 characters)
        name: Physical host name (Optional, 1~256 characters, supports fuzzy match)
        ip: Physical host IP (Optional, 1~256 characters, supports fuzzy match)
        display_status: Display status list (Optional, max array members: 1000). Options: OFFLINE, NOT_RESPONDING, GRAY, NORMAL, RED, YELLOW, REBOOTING, INITIAL, BOOTING, SHUTDOWNING
        managed_status: Managed status list (Optional, max array members: 1000). Options: UNKNOWN, NORMAL, TAKE_OVERING, TAKE_ERROR, TAKE_OVER_ALARM
        os_type: OS type list (Optional, max array members: 1000). Options: UNKNOWN, LINUX, WINDOWS, SUSE, EULER, REDHAT, CENTOS, WINDOWSSERVER2012, SOLARIS, HPUX, AIX, XENSERVER, MACOS, VMWAREESX, ORACLE, OPENVMS
        sort_key: Sort key (Optional). Options: ip, name
        sort_dir: Sort direction (Optional, ineffective without sort_key). Options: desc (descending), asc (ascending)
        page_size: Items per page (Optional, 1~1024, default 1024)
        page_no: Page number (Optional, 1~10000000, default 1)

    Returns:
        Physical host list
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
    Query a specified physical host group

    Args:
        client: DME API client
        hostgroup_id: Physical host group ID (Required)

    Returns:
        Physical host group details
    """
    url = "/rest/hostmgmt/v1/hostgroups/{hostgroup_id}/summary"

    response = client.get(url, params={"hostgroup_id": hostgroup_id})
    return response


def physical_host_group_create(client: DMEAPIClient, name: str, host_ids: list,
           azs: list = None, project_id: str = None,
           description: str = None) -> dict:
    """
    Create physical host group

    Create a physical host group with specified physical hosts.

    Args:
        client: DME API client
        name: Physical host group name (Required, 1~255 characters, supports letters, digits, ._- and Chinese)
        host_ids: Physical host ID list (Required, max array members: 100)
        azs: Availability zone ID list (Optional, max array members: 40)
        project_id: Project group ID (Optional, 1~64 characters)
        description: Physical host group description (Optional, 0~63 characters)

    Returns:
        Created physical host group info
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
    Modify physical host group basic info

    Args:
        client: DME API client
        hostgroup_id: Physical host group ID (Required)
        name: Physical host group name (Optional, 1~255 characters, supports letters, digits, ._- and Chinese; empty = unchanged)
        description: Physical host group description (Optional, 0~63 characters)
        azs: Availability zone ID list (Optional, max array members: 40; null or empty = disassociate AZ)
        project_id: Project group ID (Optional, 0~64 characters; empty = unchanged; empty string = disassociate; non-empty and different = associate to new project)

    Returns:
        Modification result
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
    Delete a specified physical host group

    Args:
        client: DME API client
        hostgroup_id: Physical host group ID (Required)
        sync_to_storage: Sync delete from storage (Optional, default false)

    Returns:
        Deletion result
    """
    url = "/rest/hostmgmt/v1/hostgroups/{hostgroup_id}"

    response = client.delete(url, params={"hostgroup_id": hostgroup_id, "sync_to_storage": str(sync_to_storage).lower()})
    return response


def physical_host_group_add_hosts(client: DMEAPIClient, hostgroup_id: str,
             host_ids: list, sync_to_storage: bool = False) -> dict:
    """
    Add physical hosts to a physical host group

    Args:
        client: DME API client
        hostgroup_id: Physical host group ID (Required)
        host_ids: Physical host ID list (Required, max 100)
        sync_to_storage: Sync add to storage (Optional, default false)

    Returns:
        Addition result
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
    Remove physical hosts from a physical host group

    Remove physical hosts from the specified physical host group.

    Args:
        client: DME API client
        hostgroup_id: Physical host group ID (Required)
        host_ids: Physical host ID list (Required, max 1000)
        sync_to_storage: Sync remove from storage (Optional, default false)

    Returns:
        Removal result
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
    Map LUNs to a physical host group

    Map LUNs to the specified physical host group.

    Args:
        client: DME API client
        volume_ids: LUN ID list (Required, max array members: 1000)
        hostgroup_id: Physical host group ID (Required, 0~64 characters)
        mapping_policy: MappingPolicy list (Optional)。参数格式如下：[{
                storage_id: Storage device ID (Optional, 0~64 characters),
                start_host_lun_id: Starting host LUN ID (Optional, 0~4095),
                auto_zoning: Auto zone (Optional). Options: true, false,
                zone_policy_id: Zone policy ID (Optional, 0~64 characters; effective when auto_zoning is true),
                target_fcports: Port WWN list (Optional, mutually exclusive with target_fcportgroups, max array members: 1000; effective when auto_zoning is true),
                target_fcportgroups: Port group ID list (Optional, mutually exclusive with target_fcports, max array members: 1000; effective when auto_zoning is true),
                mapping_view: MappingRequest object (Optional)。属性格式如下：{
                        mapping_view_id: Mapping view ID on device (Optional, max 31 characters),
                        mapping_view_name: Mapping view name on device (Optional, max 31 characters),
                        lun_group_id: LUN group ID on device (Optional, max 31 characters),
                        lun_group_name: LUN group name on device (Optional, max 255 characters),
                        port_group_id: Port group ID on device (Optional, max 31 characters),
                }
             }, ...]
        task_remarks: Async task remark (Optional, max 1024 characters)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Unmap LUNs from a host group

    Unmap the LUN association with the host group.

    Args:
        client: DME API client
        volume_ids: LUN ID list (Required, max array members: 1000)
        hostgroup_id: Host group ID (Required, 1~64 characters)
        task_remarks: Async task remark (Optional, max 1024 characters)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Unmap LUNs from a storage host group

    Unmap the LUN association with the storage host group.

    Args:
        client: DME API client
        volume_ids: LUN ID list (Required, max array members: 1000)
        hostgroup_id: Host group ID (Required, 1~64 characters)
        task_remarks: Async task remark (Optional, max 1024 characters)

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
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
    Query the list of storage host groups associated with a physical host group.

    Args:
        client: DME API client
        hostgroup_id: Physical host group ID (Required, string, 1~64 characters)
        storage_ip: Storage device IP (Optional, string, 1~127 characters)
        storage_name: Storage device name, supports fuzzy search (Optional, string, 1~256 characters)

    Returns:
        {
            total: Number of storage hosts queried (integer),
            strorage_host_group_list: Storage host group list (List<StorageHostGroupResponse>)。参数格式如下：[{
                host_group_id: Storage host group ID (string),
            }, ...],
        }
    """
    url = "/rest/hostmgmt/v1/hostgroups/{hostgroup_id}/related-storage-hostgroups"

    if not hostgroup_id:
        raise ValueError("hostgroup_id is required")

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
    Query host-to-LUN mapping relationships.

    Args:
        client: DME API client
        storage_id: Storage device ID (Required, string, 1~64 characters)
        name: Mapping view name, supports fuzzy search (Optional, string, 0~256 characters)
        mapping_type: Host mapping query type (Optional, string). Options: all (hosts with LUN mappings, direct and indirect), match_mapping_view (hosts directly mapped to LUN)
        host_info: Storage host info (Optional, LunToHostQueryParam object)
        lun_info: LUN info (Optional, HostToLunQueryParam object)
        sort_key: Sort field (Optional, string). Options: host_name, lun_name, capacity_usage, lun_raw_id, host_raw_id
        sort_dir: Sort direction (Optional, string). Options: asc (ascending), desc (descending)
        page_size: Items per page for mapping views (Optional, int32, 0~1000). Default: 100
        page_no: Page number for mapping views (Optional, int32). Default: 1

    Returns:
        {
            total: Number of mapping views (int32),
            mapping_views: Mapping view list (List<HostToLunMappingView>)。参数格式如下：[{
                id: Mapping view ID (string),
                name: Mapping view name (string),
                host_info: Storage host info (HostInfoRespParam object),
                lun_info: LUN info (LunInfoRespParam object),
            }, ...],
        }
    """
    url = "/rest/blockservice/v1/mapping-views/query_for_host_to_lun"

    if not storage_id:
        raise ValueError("storage_id is required")

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
# Action list for CLI help
# ============================================================================

ACTIONS = {
    # LUN subtopic actions (san lun xxx)
    'lun_list': {
        'func': lun_list,
        'description': 'Batch query LUNs',
        'params': ['limit', 'offset', 'sort_dir', 'sort_key', 'name', 'vstore_raw_id', 'vstore_name', 'status', 'health_status', 'service_level_id', 'volume_wwn', 'storage_id', 'pool_raw_id', 'host_id', 'hostgroup_id', 'unmapped_host_id', 'unmapped_hostgroup_id', 'project_id', 'allocate_type', 'attached', 'query_mode', 'protected', 'pg_id', 'usage_type', 'support_provisioning'],
        'subtopic': 'lun'
    },
    'lun_show': {
        'func': lun_show,
        'description': 'Query a specific LUN',
        'params': ['volume_id'],
        'subtopic': 'lun'
    },
    'lun_create': {
        'func': lun_create,
        'description': 'Custom create LUN',
        'params': ['storage_id', 'lun_specs', 'lun_specs_pass_through', 'pool_id', 'vstore_id', 'owner_controller', 'initial_distribute_policy', 'prefetch_policy', 'prefetch_value', 'tuning', 'mapping', 'task_remarks'],
        'subtopic': 'lun'
    },
    'lun_delete': {
        'func': lun_delete,
        'description': 'Batch delete LUNs',
        'params': ['volume_ids', 'task_remarks'],
        'subtopic': 'lun'
    },
    'lun_modify': {
        'func': lun_modify,
        'description': 'Modify a specified LUN',
        'params': ['volume_id', 'name', 'description', 'owner_controller', 'prefetch_policy', 'prefetch_value', 'tuning', 'task_remarks'],
        'subtopic': 'lun'
    },
    'lun_modify_name': {
        'func': lun_modify_name,
        'description': 'Batch modify LUN names',
        'params': ['volumes'],
        'subtopic': 'lun'
    },
    'lun_expand': {
        'func': lun_expand,
        'description': 'Batch expand LUN capacity',
        'params': ['volumes', 'task_remarks'],
        'subtopic': 'lun'
    },
    'lun_connection': {
        'func': lun_connection,
        'description': 'Query connection info for LUN IDs',
        'params': ['volume_ids'],
        'subtopic': 'lun'
    },

    # LUN group subtopic actions（san lun_group xxx）
    'lun_group_list': {
        'func': lun_group_list,
        'description': 'Batch query LUN groups',
        'params': ['page_size', 'page_no', 'sort_dir', 'sort_key', 'name', 'vstore_raw_id', 'vstore_name', 'storage_id', 'storage_name', 'raw_id', 'attached', 'protection_group_raw_id', 'avaiable_mapping_for_host_id', 'avaiable_mapping_for_host_group_id', 'support_provisioning'],
        'subtopic': 'lun_group'
    },
    'lun_group_show': {
        'func': lun_group_show,
        'description': 'Query LUN group details',
        'params': ['group_id', 'storage_id'],
        'subtopic': 'lun_group'
    },
    'lun_group_create': {
        'func': lun_group_create,
        'description': 'Create LUN group',
        'params': ['storage_id', 'name', 'description', 'existing_lun_ids', 'customize_volumes', 'task_remarks', 'vstore_id', 'zoning_info', 'mapping_view'],
        'subtopic': 'lun_group'
    },
    'lun_group_delete': {
        'func': lun_group_delete,
        'description': 'Batch delete LUN groups',
        'params': ['lun_group_ids', 'task_remarks'],
        'subtopic': 'lun_group'
    },
    'lun_group_add_luns': {
        'func': lun_group_add_luns,
        'description': 'Add LUNs to LUN group',
        'params': ['group_id', 'existing_lun_ids', 'customize_volumes', 'host_lun_id_infos', 'host_lun_id_verify', 'task_remarks'],
        'subtopic': 'lun_group'
    },
    'lun_group_remove_luns': {
        'func': lun_group_remove_luns,
        'description': 'Remove LUNs from LUN group',
        'params': ['group_id', 'lun_ids', 'task_remarks'],
        'subtopic': 'lun_group'
    },
    'lun_group_show_luns': {
        'func': lun_group_show_luns,
        'description': 'Query LUNs in LUN group',
        'params': ['group_id', 'page_size', 'page_no', 'health_status'],
        'subtopic': 'lun_group'
    },
    # Mapping view subtopic actions (san mapping_view xxx)
    'mapping_view_create': {
        'func': mapping_view_create,
        'description': 'Create mapping view',
        'params': ['storage_id', 'name', 'port_group_id', 'start_host_lun_id',
                   'host', 'vbs', 'host_group', 'lun_group', 'luns',
                   'task_remarks'],
        'subtopic': 'mapping_view'
    },
    'mapping_view_delete': {
        'func': mapping_view_delete,
        'description': 'Batch delete mapping views',
        'params': ['mapping_view_ids'],
        'subtopic': 'mapping_view'
    },
    'mapping_view_list': {
        'func': mapping_view_list,
        'description': 'Batch query mapping views',
        'params': ['page_size', 'page_no', 'name', 'raw_id', 'storage_id',
                   'lun_id', 'lun_name', 'lun_group_id', 'lun_group_raw_id',
                   'lun_group_name', 'storage_host_id', 'storage_host_name',
                   'storage_host_group_id', 'storage_host_group_name',
                   'storage_host_group_raw_id', 'port_group_id', 'port_group_raw_id',
                   'port_group_name', 'sort_key', 'sort_dir'],
        'subtopic': 'mapping_view'
    },

    # Storage host subtopic actions (san storage_host xxx)
    'storage_host_create': {
        'func': storage_host_create,
        'description': 'Create storage host',
        'params': ['storage_id', 'host_info', 'task_remarks', 'vstore_id'],
        'subtopic': 'storage_host'
    },
    'storage_host_batch_query': {
        'func': storage_host_batch_query,
        'description': 'Batch query storage hosts by IDs',
        'params': ['ids'],
        'subtopic': 'storage_host'
    },
    'storage_host_list': {
        'func': storage_host_list,
        'description': 'Batch query storage hosts',
        'params': ['page_size', 'page_no', 'sort_key', 'sort_dir', 'name', 'raw_id', 'host_group_id',
                   'avaliable_add_to_host_group_id', 'host_group_name', 'ip', 'health_status', 'os_type',
                   'storage_id', 'avaiable_mapping_for_lun_group_id', 'avaiable_mapping_for_lun_id',
                   'support_provisioning', 'manufacturer', 'vstore_raw_id', 'vstore_name'],
        'subtopic': 'storage_host'
    },
    'storage_host_modify': {
        'func': storage_host_modify,
        'description': 'Modify storage host',
        'params': ['storage_host_id', 'storage_host_name', 'storage_host_description', 'storage_host_ip',
                   'storage_host_os_type', 'add_initiators', 'remove_initiators', 'multipath', 'access_mode',
                   'hyper_metro_path_optimized', 'task_remarks'],
        'subtopic': 'storage_host'
    },
    'storage_host_delete': {
        'func': storage_host_delete,
        'description': 'Batch delete storage hosts',
        'params': ['host_ids'],
        'subtopic': 'storage_host'
    },
    'storage_host_show_paths': {
        'func': storage_host_show_paths,
        'description': 'Batch query storage host paths',
        'params': ['page_no', 'page_size', 'storage_id', 'storage_host_ids', 'storage_host_raw_ids',
                   'health_status', 'running_status', 'initiator_type'],
        'subtopic': 'storage_host'
    },
    'storage_host_show_luns': {
        'func': storage_host_show_luns,
        'description': 'Query LUN mapping list for storage host',
        'params': ['storage_host_id', 'name', 'page_size', 'page_no', 'sort_key', 'sort_dir'],
        'subtopic': 'storage_host'
    },
    'storage_host_unmap_luns': {
        'func': storage_host_unmap_luns,
        'description': '解除Storage host映射',
        'params': ['volume_ids', 'host_id', 'task_remarks'],
        'subtopic': 'storage_host'
    },
    # Storage host组subtopic actions（san storage_host_group xxx）
    'storage_host_group_create': {
        'func': storage_host_group_create,
        'description': 'Create storage host group',
        'params': ['storage_id', 'name', 'description', 'exist_host_ids', 'create_storage_host_params', 'task_remarks', 'vstore_id'],
        'subtopic': 'storage_host_group'
    },
    'storage_host_group_list': {
        'func': storage_host_group_list,
        'description': 'Batch query storage host groups',
        'params': ['storage_id', 'name', 'raw_id', 'vstore_id', 'vstore_name', 'page_no', 'page_size',
                   'sort_key', 'sort_dir', 'avaiable_mapping_for_lun_group_id', 'avaiable_mapping_for_lun_id',
                   'support_provisioning'],
        'subtopic': 'storage_host_group'
    },
    'storage_host_group_add_hosts': {
        'func': storage_host_group_add_hosts,
        'description': 'Add storage hosts to host group',
        'params': ['storage_host_group_id', 'storage_host_id_ids', 'create_storage_host_params', 'task_remarks'],
        'subtopic': 'storage_host_group'
    },
    'storage_host_group_remove_hosts': {
        'func': storage_host_group_remove_hosts,
        'description': 'Remove hosts from storage host group',
        'params': ['storage_host_group_id', 'storage_host_ids', 'task_remarks'],
        'subtopic': 'storage_host_group'
    },
    'storage_host_group_delete': {
        'func': storage_host_group_delete,
        'description': 'Batch delete storage host groups',
        'params': ['host_group_ids', 'task_remarks'],
        'subtopic': 'storage_host_group'
    },
    'storage_host_group_show_luns': {
        'func': storage_host_group_show_luns,
        'description': 'Query LUN mapping list for storage host group',
        'params': ['storage_host_group_id', 'name', 'page_size', 'page_no', 'sort_key', 'sort_dir'],
        'subtopic': 'storage_host_group'
    },
    'storage_host_group_unmap_luns': {
        'func': storage_host_group_unmap_luns,
        'description': '解除Storage host组映射',
        'params': ['volume_ids', 'hostgroup_id', 'task_remarks'],
        'subtopic': 'storage_host_group'
    },
    # Port groupsubtopic actions（san port_group xxx）
    'port_group_list': {
        'func': port_group_list,
        'description': 'Batch queryPort group',
        'params': ['storage_id', 'page_no', 'page_size'],
        'subtopic': 'port_group'
    },
    'port_group_create': {
        'func': port_group_create,
        'description': 'Create port group',
        'params': ['storage_id', 'name', 'description', 'port_ids'],
        'subtopic': 'port_group'
    },
    'port_group_show_ports': {
        'func': port_group_show_ports,
        'description': 'Query ports of a port group',
        'params': ['port_group_id', 'type', 'page_no', 'page_size'],
        'subtopic': 'port_group'
    },
    'port_group_show_relations': {
        'func': port_group_show_relations,
        'description': 'Query port group to port associations',
        'params': ['page_no', 'page_size'],
        'subtopic': 'port_group'
    },
    # Physical host subtopic actions (san physical_host xxx)
    'physical_host_list': {
        'func': physical_host_list,
        'description': 'Batch query physical hosts',
        'params': ['limit', 'start', 'sort_key', 'sort_dir', 'name',
                   'host_group_name', 'ip', 'display_status', 'managed_status',
                   'os_type', 'access_mode', 'az_id', 'az_ids', 'project_id'],
        'subtopic': 'physical_host'
    },
    'physical_host_show': {
        'func': physical_host_show,
        'description': 'Query a specific physical host',
        'params': ['host_id'],
        'subtopic': 'physical_host'
    },
    'physical_host_create': {
        'func': physical_host_create,
        'description': 'Onboard a physical host',
        'params': ['access_mode', 'type', 'host_name', 'ip', 'port',
                   'username', 'password', 'description', 'initiator',
                   'azs', 'project_id', 'sync_to_storage', 'multipath_type',
                   'path_type', 'failover_mode', 'special_mode_type', 'save_public_key'],
        'subtopic': 'physical_host'
    },
    'physical_host_modify': {
        'func': physical_host_modify,
        'description': 'Modify physical host basic info',
        'params': ['host_id', 'ip', 'host_name', 'os_type', 'azs', 'project_id'],
        'subtopic': 'physical_host'
    },
    'physical_host_modify_access_info': {
        'func': physical_host_modify_access_info,
        'description': 'Modify physical host access info',
        'params': ['host_id', 'ip', 'port', 'username', 'password', 'project_id', 'azs', 'sync_to_storage', 'description', 'multipath_type', 'path_type', 'failover_mode', 'special_mode_type'],
        'subtopic': 'physical_host'
    },
    'physical_host_delete': {
        'func': physical_host_delete,
        'description': 'Remove physical host',
        'params': ['host_id', 'sync_to_storage'],
        'subtopic': 'physical_host'
    },
    'physical_host_add_initiators': {
        'func': physical_host_add_initiators,
        'description': 'Add initiators to physical host',
        'params': ['host_id', 'initiators'],
        'subtopic': 'physical_host'
    },
    'physical_host_remove_initiators': {
        'func': physical_host_remove_initiators,
        'description': 'Remove initiators from physical host',
        'params': ['host_id', 'initiators'],
        'subtopic': 'physical_host'
    },
    'physical_host_show_initiators': {
        'func': physical_host_show_initiators,
        'description': 'Query physical host initiators',
        'params': ['host_id', 'port_name', 'protocol', 'status'],
        'subtopic': 'physical_host'
    },
    'physical_host_test': {
        'func': physical_host_test,
        'description': 'Test storage-host connectivity',
        'params': ['storage_id', 'host_ids', 'hostgroup_id', 'auto_zoning', 'target_fcports', 'target_fcportgroups'],
        'subtopic': 'physical_host'
    },
    'physical_host_query_sshkey': {
        'func': physical_host_query_sshkey,
        'description': 'QueryPhysical hostSSH公钥',
        'params': ['ip', 'port'],
        'subtopic': 'physical_host'
    },
    'physical_host_save_sshkey': {
        'func': physical_host_save_sshkey,
        'description': '保存指定Physical hostSSH公钥',
        'params': ['ip', 'key', 'port'],
        'subtopic': 'physical_host'
    },
    'physical_host_query_by_initiator': {
        'func': physical_host_query_by_initiator,
        'description': 'Query physical host by initiator',
        'params': ['initiator_id', 'raw_id', 'protocol'],
        'subtopic': 'physical_host'
    },
    'physical_host_map_luns': {
        'func': physical_host_map_luns,
        'description': 'Map LUNs to physical host',
        'params': ['volume_ids', 'host_id', 'mapping_policy', 'task_remarks'],
        'subtopic': 'physical_host'
    },
    'physical_host_unmap_luns': {
        'func': physical_host_unmap_luns,
        'description': 'Unmap LUNs from host',
        'params': ['volume_ids', 'host_id', 'task_remarks'],
        'subtopic': 'physical_host'
    },
    'physical_host_show_mapping_views': {
        'func': physical_host_show_mapping_views,
        'description': 'Query mapping views for physical host',
        'params': ['host_id', 'storage_id'],
        'subtopic': 'physical_host'
    },
    # Physical host group subtopic actions (san physical_host_group xxx)
    'physical_host_group_list': {
        'func': physical_host_group_list,
        'description': 'Batch query physical host groups',
        'params': ['limit', 'start', 'sort_dir', 'sort_key', 'name', 'project_id', 'az_ids', 'managed_status'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_show_hosts': {
        'func': physical_host_group_show_hosts,
        'description': 'Query hosts in physical host group',
        'params': ['hostgroup_id', 'name', 'ip', 'display_status', 'managed_status', 'os_type', 'sort_key', 'sort_dir', 'page_size', 'page_no'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_show': {
        'func': physical_host_group_show,
        'description': 'Query physical host group',
        'params': ['hostgroup_id'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_create': {
        'func': physical_host_group_create,
        'description': 'Create physical host group',
        'params': ['name', 'host_ids', 'azs', 'project_id', 'description'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_modify': {
        'func': physical_host_group_modify,
        'description': 'Modify physical host group info',
        'params': ['hostgroup_id', 'name', 'description', 'azs', 'project_id'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_delete': {
        'func': physical_host_group_delete,
        'description': 'Delete physical host group',
        'params': ['hostgroup_id', 'sync_to_storage'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_add_hosts': {
        'func': physical_host_group_add_hosts,
        'description': 'Add hosts to physical host group',
        'params': ['hostgroup_id', 'host_ids', 'sync_to_storage'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_remove_hosts': {
        'func': physical_host_group_remove_hosts,
        'description': 'Remove hosts from physical host group',
        'params': ['hostgroup_id', 'host_ids', 'sync_to_storage'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_map_luns': {
        'func': physical_host_group_map_luns,
        'description': 'Map LUNs to physical host group',
        'params': ['volume_ids', 'hostgroup_id', 'mapping_policy', 'task_remarks'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_unmap_luns': {
        'func': physical_host_group_unmap_luns,
        'description': 'Unmap LUNs from physical host group',
        'params': ['volume_ids', 'hostgroup_id', 'task_remarks'],
        'subtopic': 'physical_host_group'
    },
    'physical_host_group_show_mapping_views': {
        'func': physical_host_group_show_mapping_views,
        'description': 'Query mapping views for host group',
        'params': ['host_group_id', 'storage_id'],
        'subtopic': 'physical_host_group'
    },
    'show_related': {
        'func': physical_host_group_show_related,
        'description': 'Query related storage host groups',
        'params': ['hostgroup_id', 'storage_ip', 'storage_name'],
        'subtopic': 'physical_host_group'
    },
    'query_host_to_lun': {
        'func': mapping_view_query_host_to_lun,
        'description': 'Query host-to-LUN mapping relationship',
        'params': ['storage_id', 'name', 'mapping_type', 'host_info', 'lun_info', 'sort_key', 'sort_dir', 'page_size', 'page_no'],
        'subtopic': 'mapping_view'
    }
}
