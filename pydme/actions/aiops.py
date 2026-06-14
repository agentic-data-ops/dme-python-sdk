"""
AIOps 智能运维operations
"""

import sys
import os
import json
from datetime import datetime, timedelta

from pydme.client import DMEAPIClient


def _build_current_alarm_params(alarm_id: str = None, severity: list = None,
                                 mo_dn: str = None, alarm_group_id: str = None,
                                 dc_id: str = None, product_name: str = None,
                                 alarm_name: str = None, occur_utc_start: str = None,
                                 occur_utc_end: str = None, fields: list = None,
                                 page_size: int = 100) -> dict:
    """构建Current alarm查询参数"""
    body_params = {'size': page_size}

    if alarm_id is not None or severity is not None or mo_dn is not None or \
       alarm_group_id is not None or dc_id is not None or product_name is not None or \
       alarm_name is not None or occur_utc_start is not None or occur_utc_end is not None:

        query_filters = []

        if alarm_id is not None:
            query_filters.append({
                'name': 'ALARMID',
                'field': 'alarm_id',
                'operator': 'like',
                'values': [alarm_id]
            })

        if severity is not None:
            query_filters.append({
                'name': 'SEVERITY',
                'field': 'severity',
                'operator': 'in',
                'values': severity
            })

        if mo_dn is not None:
            query_filters.append({
                'name': 'MO_DN',
                'field': 'mo_dn',
                'operator': 'inc',
                'values': [mo_dn]
            })

        if alarm_group_id is not None:
            query_filters.append({
                'name': 'ALARM_GROUP_ID',
                'field': 'alarm_group_id',
                'operator': '=',
                'values': [alarm_group_id]
            })

        if dc_id is not None:
            query_filters.append({
                'name': 'DC_ID',
                'field': 'dc_id',
                'operator': '=',
                'values': [dc_id]
            })

        if product_name is not None:
            query_filters.append({
                'name': 'PRODUCT_NAME',
                'field': 'product_name',
                'operator': 'like',
                'values': [product_name]
            })

        if alarm_name is not None:
            query_filters.append({
                'name': 'ALARM_NAME',
                'field': 'alarm_name',
                'operator': 'like',
                'values': [alarm_name]
            })

        if occur_utc_start is not None or occur_utc_end is not None:
            values = []
            if occur_utc_start is not None:
                values.append(occur_utc_start)
            if occur_utc_end is not None:
                values.append(occur_utc_end)
            if len(values) == 2:
                query_filters.append({
                    'name': 'OCCURUTC',
                    'field': 'occur_utc',
                    'operator': 'between',
                    'values': values
                })

        body_params['query'] = {'filters': query_filters}

    if fields is not None:
        body_params['fields'] = fields

    return body_params


def _build_history_alarm_params(alarm_id: str = None, severity: list = None,
                                 mo_dn: str = None, cleared: bool = None,
                                 occur_utc_start: str = None, occur_utc_end: str = None,
                                 fields: list = None, size: int = 100,
                                 iterator: str = None) -> dict:
    """构建History alarm查询参数"""
    body_params = {'size': size}

    query_filters = []

    if alarm_id is not None:
        query_filters.append({
            'name': 'ALARMID',
            'field': 'alarm_id',
            'operator': 'like',
            'values': [alarm_id]
        })

    if severity is not None:
        query_filters.append({
            'name': 'SEVERITY',
            'field': 'severity',
            'operator': 'in',
            'values': severity
        })

    if mo_dn is not None:
        query_filters.append({
            'name': 'MO_DN',
            'field': 'mo_dn',
            'operator': 'inc',
            'values': [mo_dn]
        })

    if cleared is not None:
        query_filters.append({
            'name': 'CLEARED',
            'field': 'cleared',
            'operator': '=',
            'values': ['true' if cleared else 'false']
        })

    if occur_utc_start is not None or occur_utc_end is not None:
        values = []
        if occur_utc_start is not None:
            values.append(occur_utc_start)
        if occur_utc_end is not None:
            values.append(occur_utc_end)
        if len(values) == 2:
            query_filters.append({
                'name': 'OCCURUTC',
                'field': 'occur_utc',
                'operator': 'between',
                'values': values
            })

    if query_filters:
        body_params['query_context'] = {'filters': query_filters}

    if fields is not None:
        body_params['fields'] = fields

    if iterator is not None:
        body_params['iterator'] = iterator

    return body_params


def alarm_list(client: DMEAPIClient, alarm_id: str = None, severity: list = None,
                mo_dn: str = None, alarm_group_id: str = None, dc_id: str = None,
                product_name: str = None, alarm_name: str = None,
                occur_utc_start: str = None, occur_utc_end: str = None,
                fields: list = None, page_no: int = 1, page_size: int = 100,
                cleared: bool = None, size: int = 100, iterator: str = None,
                include_history: bool = None) -> dict:
    """
    Query alarm info

    查询Current alarm,Optional择是否同时查询History alarm.

    Args:
        client: DME API client
        alarm_id: 告警 ID,supports fuzzy match
        severity: Alarm severity列表,取值:critical, major, minor, warning, indeterminate, cleared
        mo_dn: 被管理object DN,支持 inc 操作符匹配
        alarm_group_id: 告警组 ID
        dc_id: Data center ID
        product_name: 产品名称
        alarm_name: Alarm name,supports fuzzy match
        occur_utc_start: 告警发生Start time(毫second(s)Timestamp)
        occur_utc_end: 告警发生End time(毫second(s)Timestamp)
        fields: 指定返回的字段列表
        page_no: Page queryStart page,默认 1
        page_size: 每页count,1~1000,默认 100(Current alarm查询用)
        cleared: 是否已清除,true/false(History alarm查询用)
        size: 返回的结果集最大条数,1~1000,默认 100(History alarm查询用)
        iterator: 迭代子,首次查询无需传入,后续查询使用上次返回的 iterator(History alarm查询用)
        include_history: 开关参数,指定则同时查询History alarm

    Returns:
        {
            current_alarms: Current alarm list (List<AlarmInfo>)。参数格式如下：[{
                alarm_id: Alarm ID (string),
                alarm_name: Alarm name (string),
                severity: Alarm severity (string),
                status: 状态 (string),
            }, ...],
            total: 告警Total count (integer),
        }
    """
    result = {
        'current_alarms': None,
        'history_alarms': None
    }

    # 查询Current alarm(默认总是查询)
    current_url = "/rest/alarmmgmt/v1/alarms/current-alarm/query"
    current_params = _build_current_alarm_params(
        alarm_id=alarm_id, severity=severity, mo_dn=mo_dn,
        alarm_group_id=alarm_group_id, dc_id=dc_id, product_name=product_name,
        alarm_name=alarm_name, occur_utc_start=occur_utc_start,
        occur_utc_end=occur_utc_end, fields=fields, page_size=page_size
    )

    current_response = client.post(current_url, body=current_params)
    result['current_alarms'] = current_response

    # if specified include_history,同时查询History alarm
    if include_history:
        history_url = "/rest/alarmmgmt/v1/alarms/history-alarms/query"
        history_params = _build_history_alarm_params(
            alarm_id=alarm_id, severity=severity, mo_dn=mo_dn,
            cleared=cleared, occur_utc_start=occur_utc_start,
            occur_utc_end=occur_utc_end, fields=fields, size=size,
            iterator=iterator
        )

        history_response = client.post(history_url, body=history_params)
        result['history_alarms'] = history_response

    return result


def alarm_ack(client: DMEAPIClient, csns: list) -> dict:
    r"""
    Acknowledge alarm

    对指定告警执行确认 (ACK) 操作.

    Args:
        client: DME API client
        csns: Alarm serial number list(Required),最多 30 个

    Returns:
        Operation result
    """
    url = "/rest/alarmmgmt/v1/alarms/operation"

    if not isinstance(csns, list) or len(csns) < 1 or len(csns) > 30:
        raise ValueError("csns must be a list containing 1-30 elements")

    payload = {
        "csns": csns,
        "operation_type": "ACK"
    }

    print(f"请求 URL: {url}")
    print(f"Request load:{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


def alarm_unack(client: DMEAPIClient, csns: list) -> dict:
    r"""
    取消Acknowledge alarm

    对指定告警执行取消确认 (UNACK) 操作.

    Args:
        client: DME API client
        csns: Alarm serial number list(Required),最多 30 个

    Returns:
        Operation result
    """
    url = "/rest/alarmmgmt/v1/alarms/operation"

    if not isinstance(csns, list) or len(csns) < 1 or len(csns) > 30:
        raise ValueError("csns must be a list containing 1-30 elements")

    payload = {
        "csns": csns,
        "operation_type": "UNACK"
    }

    print(f"请求 URL: {url}")
    print(f"Request load:{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


def alarm_clear(client: DMEAPIClient, csns: list) -> dict:
    r"""
    Clear alarm

    对指定告警执行清除 (CLEAR) 操作.

    Args:
        client: DME API client
        csns: Alarm serial number list(Required),最多 30 个

    Returns:
        Operation result
    """
    url = "/rest/alarmmgmt/v1/alarms/operation"

    if not isinstance(csns, list) or len(csns) < 1 or len(csns) > 30:
        raise ValueError("csns must be a list containing 1-30 elements")

    payload = {
        "csns": csns,
        "operation_type": "CLEAR"
    }

    print(f"请求 URL: {url}")
    print(f"Request load:{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


def diagnose_task_create(client: DMEAPIClient, object_ids: list, object_type: str,
                         begin_time: int, end_time: int, analysis_types: list) -> dict:
    r"""
    Create intelligent analysis task

    Args:
        client: DME API client
        object_ids: 入口分析object ID 列表(Required),数组大小:1~50
        object_type: 入口Object type(Required),value range:
            - VM: Virtual machine
            - STORAGE_HOST: Storage host
            - STORAGE_DEVICE: Storage device
            - LUN: LUN
            - FILE_SYSTEM: Filesystem
            - VBS_CLIENT: VBS Client
            - DATATURBO: DPC
            - STORAGE_POOL: Storage pool
            - IP_CLIENT: IP Client
            - HOST_GROUP: Storage host组
            - FC_PORT: FC 端口
            - ETH_PORT: 以太端口
            - LUN_GROUP: LUN 组
            - LOGIC_PORT: Logic port
            - CONTROLLER: Controller
            - NAMESPACE: Namespace
        begin_time: 分析Start time(Required),Unix Timestamp(毫second(s)),必须为整minute(s)时间点,支持最近七day(s)内的诊断
        end_time: 分析End time(Required),Unix Timestamp(毫second(s)),必须为整minute(s)时间点
                  分析时间间隔范围must be greater than 30 minute(s),小于 24 hour(s)
        analysis_types: 智能分析类型列表(Required),数组大小:1~4,value range:
            - highLatency: 高时延
            - healthAnalysis: 健康快检
            - IOInterrupt: IO 中断
            - highReadLatency: 高Read latency
            - highWriteLatency: 高Write latency
            - trafficAnalysis: 流量分析
            - cpuUsageAnalysis: cpu 消耗分析

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含:
        - total: 智能分析任务Total count
        - data: 智能分析任务响应结果列表，每项包含:
            - id: 任务 ID
            - analysis_type: 分析类型
            - error_msg: Error message
            - is_succeed: 是否创建成功
    """
    url = "/rest/diagnosis/v1/tasks"

    payload = {
        "object_ids": object_ids,
        "object_type": object_type,
        "begin_time": begin_time,
        "end_time": end_time,
        "analysis_types": analysis_types
    }

    print(f"请求 URL: {url}")
    print(f"Request load:{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


# ============ Performance Performance monitoringsubtopic functions ============


def performance_create_collect_task(client: DMEAPIClient, begin_time: int, end_time: int,
                        object_type_id: str, object_ids: list,
                        indicator_ids: list) -> dict:
    """
    Create performance file collection task

    收集范围为开始日期到结束日期的性能文件,只支持收集 7 day(s)内的数据,
    每次传入的objectmultiplied by metric count不超过 2000.

    Args:
        client: DME API client
        begin_time: Start time(Required,Unix Timestamp毫second(s))
        end_time: End time(Required,Unix Timestamp毫second(s))
        object_type_id: Object type ID(Required,1~32  characters)
        object_ids: object ID 列表(Required,最多 2000 个,ID 长度 1~32 位)
        indicator_ids: 指标 ID 列表(Required,最多 20 个,ID 长度 1~16 位)

    Returns:
        任务 ID
    """
    url = "/rest/pmmgmt/v1/performance-data/collection-task"

    payload = {
        'begin_time': begin_time,
        'end_time': end_time,
        'object_type_id': object_type_id,
        'object_ids': object_ids,
        'indicator_ids': indicator_ids
    }

    response = client.post(url, body=payload)
    return response


def performance_download_collect_result(client: DMEAPIClient, task_id: str) -> dict:
    """
    Download performance file

    Args:
        client: DME API client
        task_id: 任务 ID(Required)

    Returns:
        性能文件下载链接或文件内容
    """
    url = "/rest/pmmgmt/v1/performance-data/download/{task_id}"

    response = client.get(url, params={"task_id": task_id})
    return response


def performance_query(client: DMEAPIClient, obj_type_id: int, indicator_ids: list,
          obj_ids: list, obj_type: str = None, indicators: list = None,
          ext_dimensions: list = None, interval: str = None,
          range: str = None, begin_time: int = None,
          end_time: int = None) -> dict:
    """
    查询历史Performance data

    根据传入参数中的"range"字段所取的枚举值或从开始到End time范围内的查询数据.
    有汇聚数据情况下,返回结果序列是平均值序列,并包含max,min以及对应Timestamp.

    使用说明:
    - Object type和指标定义:从Performance metricsobtain from model documentation (reference/dme_performance_model/index.md)
    - object ID (CMDB 实例 ID) 获取步骤:
      1. 运行 `cmdb instance list --help` 查看帮助,see class definition and query method
      2. 根据帮助信息,从 CMDB 资源模型中确定要查询的Resource type (Class 名称)
      3. 使用 `cmdb instance list --class_name <Class 名称>` 查询实例列表
      4. obtain from response对应资源的 instance_id (即 obj_ids 参数)

    Args:
        client: DME API client
        obj_type_id: 监控Object type标识(Required),对应监控Object type ID
                     从Performance metricsobtain from model documentation:reference/dme_performance_model/index.md
        indicator_ids: Monitoring metric标识列表(Required,最多 100 个),对应指标 ID
                       从Performance metricsobtain from model documentation:reference/dme_performance_model/index.md
        obj_ids: 监控object标识列表(Required,最多 512 个),对应 CMDB 实例 ID
                 获取方式:
                 1. 运行 `cmdb instance list --help` 查看帮助,了解类定义
                 2. 根据帮助确定要查询的Resource type (Class 名称)
                 3. 运行 `cmdb instance list --class_name <Class 名称>` 查询实例
                 4. obtain from response instance_id
        obj_type: 监控Object type(Optional,1~512  characters)
        indicators: Monitoring metric列表(Optional,最多 100 个)
        ext_dimensions: 扩展维度info list(Optional,最多 100 个)
        interval: 间隔粒度(Optional)
                  value range:ONE_MINUTE(1 minute(s)), MINUTE(5 minute(s)), HALF_HOUR(30 minute(s)),
                  HOUR(1 hour(s)), DAY(1 day(s)), WEEK(1 week(s)), MONTH(1 个month(s))
        range: Time range(Optional,默认 LAST_1_HOUR)
               value range:LAST_5_MINUTE(最近 5 minute(s)), LAST_1_HOUR(最近 1 hour(s)),
               LAST_1_DAY(最近 1 day(s)), LAST_1_WEEK(最近 1 week(s)), LAST_1_MONTH(最近 1 个month(s)),
               LAST_1_QUARTER(最近 3 个month(s)), HALF_1_YEAR(最近半year(s)), LAST_1_YEAR(最近 1 year(s)),
               BEGIN_END_TIME(自行设置开始和End time), INVALID(Invalid value)
        begin_time: 查询开始时刻(Optional),仅 range 为 BEGIN_END_TIME 时生效,必须比 end_time 小
        end_time: 查询结束时刻(Optional),仅 range 为 BEGIN_END_TIME 时生效,必须比 begin_time 大

    Returns:
        历史Performance data,包含 status_code, error_code, error_msg, data
    """
    url = "/rest/metrics/v1/data-svc/history-data/action/query"

    payload = {
        'obj_type_id': obj_type_id,
        'indicator_ids': indicator_ids,
        'obj_ids': obj_ids
    }

    if obj_type is not None:
        payload['obj_type'] = obj_type
    if indicators is not None:
        payload['indicators'] = indicators
    if ext_dimensions is not None:
        payload['ext_dimensions'] = ext_dimensions
    if interval is not None:
        payload['interval'] = interval
    if range is not None:
        payload['range'] = range
    if begin_time is not None:
        payload['begin_time'] = begin_time
    if end_time is not None:
        payload['end_time'] = end_time

    response = client.post(url, body=payload)
    return response


def performance_show_indicators(client: DMEAPIClient, indicators: list) -> dict:
    """
    Display monitoring metricsDetails

    Args:
        client: DME API client
        indicators: 监控object指标标识列表(Required,最多 1000  characters)
                   可以是integer列表或string列表,如 [123, 456] 或 ["123", "456"]

    Returns:
        Monitoring metric info,包含 kpi, data_type, data_unit, en_us, zh_cn 等字段
    """
    url = "/rest/metrics/v1/mgr-svc/indicators"

    # 确保 indicators 是integer列表
    if indicators:
        indicators = [int(i) for i in indicators]

    # API 要求直接传递数组,而不是object
    response = client.post(url, body=indicators)
    return response


def performance_list_indicators(client: DMEAPIClient, obj_type_id: int) -> dict:
    """
    列出监控Object typeSupported monitoring metrics

    Args:
        client: DME API client
        obj_type_id: 监控Object type标识(Required)

    Returns:
        Monitoring metric info,包含 indicator_ids 列表
    """
    url = "/rest/metrics/v1/mgr-svc/obj-types/{obj_type_id}/indicators"

    response = client.get(url, params={"obj_type_id": obj_type_id})
    return response


def performance_list_object_types(client: DMEAPIClient, filter: str = None) -> dict:
    """
    Get all monitoringObject type

    Args:
        client: DME API client
        filter: 过滤关键字(Optional),用于fuzzy match zh_cn 和 en_us 字段
                如果提供,returns only matchesObject type

    Returns:
        监控Object type列表,包含 obj_type_id, parent_obj_type_id, resource_category,
        resource_provider, en_us, zh_cn, group_en_us, group_zh_cn 等字段
    """
    url = "/rest/metrics/v1/mgr-svc/obj-types"

    response = client.get(url)

    # 如果提供了 filter 参数,过滤结果
    if filter is not None and response and 'data' in response:
        filter_lower = filter.lower()
        filtered_data = []
        for item in response.get('data', []):
            zh_cn = item.get('zh_cn', '')
            en_us = item.get('en_us', '')
            if filter_lower in zh_cn.lower() or filter_lower in en_us.lower():
                filtered_data.append(item)
        response['data'] = filtered_data

    return response


# Health 相关函数
def health_query_data(client: DMEAPIClient, type: str, object_id: str, begin_time: int,
                      end_time: int, object_type: str, indicator: str = None) -> dict:
    """
    Query health-related data

    查询Capacity prediction、性能预测、Performance anomaly等健康度相关数据。

    Args:
        client: DME API client
        type: Data type（Required），Optional值：capacity_prediction（Capacity prediction）, performance_prediction（性能预测）, performance_anomaly（Performance anomaly）
        object_id: 资源 ID（Required，1~256  characters）
        begin_time: Start time（Required），自 1970 year(s) 1 month(s) 1 日（00:00:00GMT）to current time in mssecond(s)数
        end_time: End time（Required），自 1970 year(s) 1 month(s) 1 日（00:00:00GMT）to current time in mssecond(s)数
        object_type: Resource type（Required）
        indicator: Resource type所对应的指标（capacity_prediction 和 performance_prediction Required）

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含Query result
    """
    if type == 'capacity_prediction':
        url = "/rest/pmmgmt/v1/prediction/query-capacity-predict"
    elif type == 'performance_prediction' or type == 'performance_predict':
        url = "/rest/pmmgmt/v1/prediction/query-performance-predict"
    elif type == 'performance_anomaly':
        url = "/rest/metrics/v1/performance/anomaly-data/query"
    else:
        raise ValueError(f"不支持的 type 参数：{type}")

    payload = {
        'object_id': object_id,
        'begin_time': begin_time,
        'end_time': end_time,
        'object_type': object_type
    }

    if indicator is not None:
        payload['indicator'] = indicator

    response = client.post(url, body=payload)
    return response


def health_show_score(client: DMEAPIClient, object_type: str, object_name: str = None,
                      object_ids: list = None, page_no: int = None, page_size: int = None,
                      sort_key: str = None, sort_dir: str = None) -> dict:
    """
    查询object健康度

    Query类型object的健康度信息。

    Args:
        client: DME API client
        object_type: Object type（Required）
                    Optional值：storage（Storage device）, storage_pool（Storage pool）, storage_host（Storage host）,
                           storage_disk（硬盘）, storage_port（存储端口）, fcswitch_port（光纤Switch port）,
                           storage_file_system（Filesystem）, controller（Controller）, replication_cg（Remote replicationConsistency group）,
                           volume（LUN）, tier（Service level）, datastore（Datastore）, virtual_machine（Virtual machine）,
                           storage_name_space（Namespace）, storage_node（存储节点）, dpc（DPC）
        object_name: Object name，supports fuzzy search（Optional，最多 256  characters）
        object_ids: object resId 列表，用于批量精确查找（Optional，supports up to 100 个 ID）
        page_no: Page queryStart position（Optional，min：1）
        page_size: Items per page（Optional，1~100，默认 20）
        sort_key: Sort field（Optional），按分数进行排序，Optional值：health_score
        sort_dir: Sort method（Optional），Optional值：asc, desc

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含object健康度列表
    """
    url = "/rest/healthmgmt/v1/health-result/query"

    payload = {
        'object_type': object_type
    }

    if object_name is not None:
        payload['object_name'] = object_name
    if object_ids is not None:
        payload['object_ids'] = object_ids
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


def health_show_detail(client: DMEAPIClient, object_id: str, object_type: str,
                       health_dimension: str) -> dict:
    """
    Query health dimension deduction details

    Queryobject在指定健康维度下的扣分详情。

    Args:
        client: DME API client
        object_id: object Id（Required，1~128  characters）
        object_type: Object type（Required）
                    Optional值：storage, storage_pool, storage_host, storage_disk, storage_port,
                           fcswitch_port, storage_file_system, controller, replication_cg, volume,
                           tier, datastore, virtual_machine, storage_name_space, storage_node,
                           dpc, gfs, dpc_client, vbs_client
        health_dimension: 健康维度（Required）
                        Optional值：alarm（告警）, performance_anomaly（Performance anomaly）,
                              performance_prediction（性能预警）, capacity_prediction（容量预警）

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含指标扣分列表
    """
    url = "/rest/healthmgmt/v1/health-result/dimension-score/query"

    payload = {
        'object_id': object_id,
        'object_type': object_type,
        'health_dimension': health_dimension
    }

    response = client.post(url, body=payload)
    return response



# ============ Performance Performance monitoringsubtopic functions ============




def diagnose_task_status(client: DMEAPIClient, task_id: str) -> dict:
    r"""
    Query performance diagnosis task status

    根据任务 ID 查询诊断任务状态.

    Args:
        client: DME API client
        task_id: 任务 ID(Required),1~128  characters

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        },包含:
        - task_id: 任务 ID
        - task_status: 任务状态,value range:
            - executing: Executing
            - failed: 失败
            - success: 成功
            - waiting: 等待
            - terminated: 已终止
        - task_result: 任务结果,value range:
            - un_analyzed: 未分析
            - warning: 警告
            - abnormal: 异常
            - event: 事件
        - total_step_count: 总步骤数
        - finish_step_count: Completed步骤数
    """
    url = "/rest/dmegraphanalysis/v1/perf-tasks/query-status"

    payload = {
        "task_id": task_id
    }

    print(f"请求 URL: {url}")
    print(f"Request load:{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


# ============================================================================
# 检查策略 (check_policy) subtopic functions
# ============================================================================

def check_policy_list(client: DMEAPIClient, policy_name: str = None, exact_query: bool = None,
                        status: str = None, policy_type: str = None, policy_source: str = None,
                        alarm_type: str = None, object_type: str = None, page_no: int = 1,
                        page_size: int = 20, sort_key: str = None, sort_dir: str = None,
                        administrative_status: str = None, policy_category: str = None,
                        object_category: str = None) -> dict:
    """
    Query check policy list

    Args:
        client: DME API client
        policy_name: Policy name（supports fuzzy search，1~256  characters）
        exact_query: 名称是否exact match（true-exact match，false-fuzzy search），默认 false
        status: 策略状态（normal-正常，checking-检查中，failed-检查失败，queuing-Queued）
        policy_type: Policy type（performance-性能threshold，capacity-容量threshold，availability-可用性，
                    configuration-配置，recyclable-可回收资源，lowload-低负载资源，
                    performance_anomaly-Performance anomaly，performance_prediction-性能预警，
                    capacity_prediction-容量预警，history_performance-History performance，
                    load_imbalance-负载失衡，highload-高负载资源）
        policy_source: 来源（pre-define-预置，user-define-自定义）
        alarm_type: Alarm type（violation-异常，alarm-告警，event-事件）
        object_type: Object type（storage-存储，lun-Logical unit，host-主机等）
        page_no: Page number，1~1000，默认 1
        page_size: Items per page，1~100，默认 20
        sort_key: Sort field（last_check_time-最后检查时间，failed_count-检查不通过的objectcount）
        sort_dir: Sort method（asc-正序，desc-降序）
        administrative_status: Management status（enable-启用，disable-禁用）
        policy_category: 检查分类（configuration-配置，performance-性能，capacity-容量，faults-故障，optimization-优化）
        object_category: object分类（Storage-Storage device，IPSwitch-Ethernet switch，FCSwitch-Fibre Channel switch，
                       Virtualization-虚拟化，Server-Server，HCI-超融合，Client-Client）

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含 total（Total count）和 policies（策略列表）
    """
    url = "/rest/policymgmt/v2/policies/query"

    body_params = {
        'page_no': page_no,
        'page_size': page_size
    }

    if policy_name is not None:
        body_params['policy_name'] = policy_name
    if exact_query is not None:
        body_params['exact_query'] = exact_query
    if status is not None:
        body_params['status'] = status
    if policy_type is not None:
        body_params['policy_type'] = policy_type
    if policy_source is not None:
        body_params['policy_source'] = policy_source
    if alarm_type is not None:
        body_params['alarm_type'] = alarm_type
    if object_type is not None:
        body_params['object_type'] = object_type
    if sort_key is not None:
        body_params['sort_key'] = sort_key
    if sort_dir is not None:
        body_params['sort_dir'] = sort_dir
    if administrative_status is not None:
        body_params['administrative_status'] = administrative_status
    if policy_category is not None:
        body_params['policy_category'] = policy_category
    if object_category is not None:
        body_params['object_category'] = object_category

    response = client.post(url, body=body_params)
    return response


def check_policy_execute(client: DMEAPIClient, policy_id: str) -> dict:
    """
    Execute check policy

    执行指定的检查策略。

    Args:
        client: DME API client
        policy_id: 策略 ID（1~64  characters）

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/policymgmt/v1/policies/{policy_id}/execute"

    response = client.post(url, params={"policy_id": policy_id})
    return response


def check_policy_enable(client: DMEAPIClient, policy_id: str) -> dict:
    """
    Enable check policy

    启用指定的检查策略。

    Args:
        client: DME API client
        policy_id: 策略 ID（1~64  characters）

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/policymgmt/v1/policies/{policy_id}/enable"

    response = client.post(url, params={"policy_id": policy_id})
    return response


def check_policy_disable(client: DMEAPIClient, policy_id: str) -> dict:
    """
    Disable check policy

    禁用指定的检查策略。

    Args:
        client: DME API client
        policy_id: 策略 ID（1~64  characters）

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/policymgmt/v1/policies/{policy_id}/disable"

    response = client.post(url, params={"policy_id": policy_id})
    return response


def check_policy_delete(client: DMEAPIClient, policy_id: str) -> dict:
    """
    Delete check policy

    Delete的检查策略。

    Args:
        client: DME API client
        policy_id: 策略 ID（1~64  characters）

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/policymgmt/v1/policies/{policy_id}"

    response = client.delete(url, params={"policy_id": policy_id})
    return response


# ============================================================================
# 检查结果 (check_result) subtopic functions
# ============================================================================

def check_result_list(client: DMEAPIClient, object_name: str = None, level: str = None,
                          object_ids: list = None, object_native_id: str = None,
                          object_type: str = None, policy_id: str = None,
                          policy_name: str = None, policy_types: list = None,
                          cause: str = None, alarm_type: str = None,
                          first_occur_time: dict = None, last_occur_time: dict = None,
                          page_no: int = 1, page_size: int = 20, sort_key: str = None,
                          sort_dir: str = None) -> dict:
    """
    Query check policy exception results

    查询检查策略的异常检查结果，supports multiple filter criteria和Pagination。

    Args:
        client: DME API client
        object_name: Object name（supports fuzzy search，1~256  characters）
        level: 异常级别（critical-紧急，major-重要，minor-次要，info-提示）
        object_ids: object ID 列表（最多 100 个）
        object_native_id: object nativeId（1~384  characters）
        object_type: Object type（storage-存储，lun-Logical unit，host-主机等）
        policy_id: 策略 ID（exact match，1~64  characters）
        policy_name: Policy name（supports fuzzy search，1~256  characters）
        policy_types: Policy type列表（最多 30 个）
        cause: 异常原因（supports fuzzy search，1~768  characters）
        alarm_type: Alarm type（violation-异常，alarm-告警，event-事件）
        first_occur_time: 第一次异常Time range（{beginTime, endTime}，UTC Timestamp，单位 ms）
        last_occur_time: 最后一次异常Time range（{beginTime, endTime}，UTC Timestamp，单位 ms）
        page_no: Page number，1~10000，默认 1
        page_size: Items per page，1~2000，默认 20
        sort_key: Sort field（violation_count-异常次数）
        sort_dir: Sort method（asc-正序，desc-降序）

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含 total（Total count）和 results（异常检查结果列表）
    """
    url = "/rest/policymgmt/v1/abnormal-check-results/query"

    body_params = {
        'page_no': page_no,
        'page_size': page_size
    }

    if object_name is not None:
        body_params['object_name'] = object_name
    if level is not None:
        body_params['level'] = level
    if object_ids is not None:
        body_params['object_ids'] = object_ids
    if object_native_id is not None:
        body_params['object_native_id'] = object_native_id
    if object_type is not None:
        body_params['object_type'] = object_type
    if policy_id is not None:
        body_params['policy_id'] = policy_id
    if policy_name is not None:
        body_params['policy_name'] = policy_name
    if policy_types is not None:
        body_params['policy_types'] = policy_types
    if cause is not None:
        body_params['cause'] = cause
    if alarm_type is not None:
        body_params['alarm_type'] = alarm_type
    if first_occur_time is not None:
        body_params['first_occur_time'] = first_occur_time
    if last_occur_time is not None:
        body_params['last_occur_time'] = last_occur_time
    if sort_key is not None:
        body_params['sort_key'] = sort_key
    if sort_dir is not None:
        body_params['sort_dir'] = sort_dir

    response = client.post(url, body=body_params)
    return response


def check_result_show(client: DMEAPIClient, check_result_id: str) -> dict:
    """
    Query check policy exception details

    Query检查结果的Details。

    Args:
        client: DME API client
        check_result_id: 检查结果 ID（1~64  characters）

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含检查结果的Details
    """
    url = "/rest/policymgmt/v1/abnormal-check-results/{check_result_id}"

    response = client.get(url, params={"check_result_id": check_result_id})
    return response


# Action list for CLI help
# ============================================================================
# 拓扑管理 (topology) subtopic functions
# ============================================================================

def topology_query_luns(client: DMEAPIClient, entry_objects: list, storage_pool_id: str,
               lun_name: str = None, san_type: str = None, page_size: int = 20, page_no: int = 1) -> dict:
    r"""
    查询拓扑图 Lun 列表

    via specified entryobject查询拓扑图中的 LUN 列表。

    Args:
        client: DME API client
        entry_objects: 入口object列表（Required），格式：[{"id":"<入口Object ID>","type":"<入口Object type>"},...]，Supported types：
            - host: 主机
            - storage: Storage device
            - host_group: 主机组
            - lun: LUN
            - vm: Virtual machine
            - datastore: Datastore
            - application: 应用
            - switch_port: Switch port
            - storage_pool: Storage pool
        storage_pool_id: Storage pool ID（Required）
        lun_name: LUN 名称，supports fuzzy match
        san_type: SAN 类型，Optional值：ip_san, fc_san
        page_size: Items per page，1~20，默认 20
        page_no: Page queryStart position，默认 1

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含 LUN 拓扑列表
    """
    url = "/rest/topomgmt/v1/topo-data/luns/query"

    payload = {
        "entry_objects": entry_objects,
        "storage_pool_id": storage_pool_id
    }

    if lun_name is not None:
        payload["lun_name"] = lun_name

    if san_type is not None:
        payload["san_type"] = san_type

    if page_size is not None:
        payload["page_size"] = page_size

    if page_no is not None:
        payload["page_no"] = page_no

    print(f"请求 URL: {url}")
    print(f"Request load：{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


def topology_query_san_path(client: DMEAPIClient, entry_objects: list, san_type: str = None) -> dict:
    r"""
    查询 SAN Path topology

    via specified entryobject查询 SAN 网络中从主机到Storage pooltopology between。
    支持 IP_SAN 和 FC_SAN 两种类型。

    Args:
        client: DME API client
        entry_objects: 入口object列表（Required），格式：[{"id":"<入口Object ID>","type":"<入口Object type>"},...]，Supported types：
            - host: 主机
            - storage: Storage device
            - lun: LUN
            - host_group: 主机组
            - vm: Virtual machine
            - datastore: Datastore（仅 FC_SAN）
            - application: 应用（仅 FC_SAN）
            - switch_port: Switch port（仅 FC_SAN）
            - storage_pool: Storage pool
        san_type: SAN 类型（Optional），Optional值：ip_san, fc_san
                  - 不指定时，同时调用 IP_SAN 和 FC_SAN 两个 API，组合返回数据
                  - 指定为 ip_san 时，仅调用 IP_SAN API
                  - 指定为 fc_san 时，仅调用 FC_SAN API

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含主机到Storage pool的拓扑结构：
        - ip_san 数据：
          - switches: Switch list
          - hosts: 主机列表
          - storages: 存储列表
          - switch_links: Switch connection list
          - port_links: 端口连接关系列表
        - fc_san 数据：
          - fabrics: fabric 列表
          - hosts: 主机列表
          - storages: 存储列表
    """
    result = {}

    # 如果未指定 san_type，同时调用两个 API
    if san_type is None:
        # 调用 IP_SAN API
        ip_san_url = "/rest/topomgmt/v1/topo-data/ipsan/host-storage/query"
        ip_san_payload = {"entry_objects": entry_objects}
        print(f"请求 URL: {ip_san_url}")
        print(f"Request load：{json.dumps(ip_san_payload, ensure_ascii=False, indent=2)}")
        ip_san_response = client.post(ip_san_url, body=ip_san_payload)
        result['ip_san'] = ip_san_response

        # 调用 FC_SAN API
        fc_san_url = "/rest/topomgmt/v1/topo-data/host-storage/query"
        fc_san_payload = {"entry_objects": entry_objects}
        print(f"请求 URL: {fc_san_url}")
        print(f"Request load：{json.dumps(fc_san_payload, ensure_ascii=False, indent=2)}")
        fc_san_response = client.post(fc_san_url, body=fc_san_payload)
        result['fc_san'] = fc_san_response

        return result

    # if specified san_type，只调用对应的 API
    elif san_type == 'ip_san':
        url = "/rest/topomgmt/v1/topo-data/ipsan/host-storage/query"
        payload = {"entry_objects": entry_objects}
        print(f"请求 URL: {url}")
        print(f"Request load：{json.dumps(payload, ensure_ascii=False, indent=2)}")
        response = client.post(url, body=payload)
        return response

    elif san_type == 'fc_san':
        url = "/rest/topomgmt/v1/topo-data/host-storage/query"
        payload = {"entry_objects": entry_objects}
        print(f"请求 URL: {url}")
        print(f"Request load：{json.dumps(payload, ensure_ascii=False, indent=2)}")
        response = client.post(url, body=payload)
        return response

    else:
        raise ValueError(f"无效的 san_type 参数：{san_type}，only supports：ip_san, fc_san")




def topology_query_vms(client: DMEAPIClient, entry_objects: list, host_id: str,
              vm_name: str = None, page_size: int = 20, page_no: int = 1) -> dict:
    r"""
    Query topology VM and virtual disk list，或查询 BMS Physical disk list below

    via specified entryobject查询虚拟化资源，包括Virtual machine和Virtual disk列表，
    或者查询 BMS（裸金属Server）physical disk list under。

    Args:
        client: DME API client
        entry_objects: 入口object列表（Required），格式：[{"id":"<入口Object ID>","type":"<入口Object type>"},...]，Supported types：
            - vm: Virtual machine
            - host_group: 主机组
            - host: 主机
            - storage: Storage device
            - lun: LUN
            - datastore: Datastore
            - switch_port: Switch port
            - storage_pool: Storage pool
        host_id: 主机 ID（Required）
        vm_name: Virtual machine名称搜索参数，supports fuzzy match
        page_size: Items per page，1~20，默认 20
        page_no: Page queryStart position，默认 1

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含：
        - total: Query resultTotal count
        - vms: VM list
        - disks: Physical host关联的物理磁盘列表
    """
    url = "/rest/topomgmt/v1/topo-data/vms/query"

    payload = {
        "entry_objects": entry_objects,
        "host_id": host_id
    }

    if vm_name is not None:
        payload["vm_name"] = vm_name

    if page_size is not None:
        payload["page_size"] = page_size

    if page_no is not None:
        payload["page_no"] = page_no

    print(f"请求 URL: {url}")
    print(f"Request load：{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


def topology_query_graph_path(client: DMEAPIClient, entry_res_type: str, entry_res_id: str,
                type: str = None, filter: list = None) -> dict:
    r"""
    Query topology library info

    via specified entry资源Query topology library info，支持 NAS、K8s、DB 等业务类型。

    Args:
        client: DME API client
        entry_res_type: 入口Resource type（Required），Supported types：
            - storage_device: Storage device
            - disk: 磁盘
            - storage_pool: Storage pool
            - hyper_scale_pool: 超大规模池
            - file_system: Filesystem
            - controller: Controller
            - eth_port: 以太网端口
            - ib_port: InfiniBand 端口
            - logic_port: Logic port
            - ip_client: IP Client
            - dtree: Dtree
            - lun: LUN
            - k8s_application: K8s 应用
            - k8s_workload: K8s 工作负载
            - k8s_pod: K8s Pod
            - k8s_pvc: K8s PVC
            - k8s_pv: K8s PV
            - k8s_cluster: K8s 集群
            - k8s_node: K8s 节点
            - k8s_vc_job: K8s VC 任务
            - dturbo_client: DataTurbo Client
            - enclosures: 机柜
            - eth_switch: Ethernet switch
            - storage_zone: 存储区域
            - service_network: 服务网络
            - db_instance: 数据库实例
            - db_node: 数据库节点
        entry_res_id: 入口资源 ID（Required）
        type: 业务类型，Optional值：nas, k8s, db
        filter: 过滤条件列表，最多 10 个

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }，包含：
        - nodes: 节点列表，每个节点包含 id, type, label, sub_type
        - edges: 边列表，每条边包含 source, target, edge_type
    """
    url = "/rest/dmegraphanalysis/v1/topo-data/query"

    payload = {
        "entry_res_type": entry_res_type,
        "entry_res_id": entry_res_id
    }

    if type is not None:
        payload["type"] = type

    if filter is not None:
        payload["filter"] = filter

    print(f"请求 URL: {url}")
    print(f"Request load：{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


# ============================================================================
# Action list for CLI help
# ============================================================================

ACTIONS = {
    'alarm_list': {
        'func': alarm_list,
        'description': 'Query alarm info(Current alarm,Optional择是否包含History alarm)',
        'params': ['alarm_id', 'severity', 'mo_dn', 'alarm_group_id', 'dc_id',
                   'product_name', 'alarm_name', 'occur_utc_start', 'occur_utc_end',
                   'fields', 'page_no', 'page_size', 'cleared', 'size', 'iterator', 'include_history'],
        'subtopic': 'alarm'
    },
    'alarm_ack': {
        'func': alarm_ack,
        'description': 'Acknowledge alarm',
        'params': ['csns'],
        'subtopic': 'alarm'
    },
    'alarm_unack': {
        'func': alarm_unack,
        'description': '取消Acknowledge alarm',
        'params': ['csns'],
        'subtopic': 'alarm'
    },
    'alarm_clear': {
        'func': alarm_clear,
        'description': 'Clear alarm',
        'params': ['csns'],
        'subtopic': 'alarm'
    },
    'diagnose_task_create': {
        'func': diagnose_task_create,
        'description': 'Create intelligent analysis task',
        'params': ['object_ids', 'object_type', 'begin_time', 'end_time', 'analysis_types'],
        'subtopic': 'diagnose_task'
    },
    'diagnose_task_status': {
        'func': diagnose_task_status,
        'description': 'Query performance diagnosis task status',
        'params': ['task_id'],
        'subtopic': 'diagnose_task'
    },
    # performance subtopic actions
    'performance_create_collect_task': {
        'func': performance_create_collect_task,
        'description': 'Create performance file collection task',
        'params': ['begin_time', 'end_time', 'object_type_id', 'object_ids', 'indicator_ids'],
        'subtopic': 'performance'
    },
    'performance_download_collect_result': {
        'func': performance_download_collect_result,
        'description': 'Download performance file',
        'params': ['task_id'],
        'subtopic': 'performance'
    },
    'performance_query': {
        'func': performance_query,
        'description': '查询历史Performance data',
        'params': ['obj_type_id', 'indicator_ids', 'obj_ids', 'obj_type', 'indicators', 'ext_dimensions', 'interval', 'range', 'begin_time', 'end_time'],
        'subtopic': 'performance'
    },
    'performance_show_indicators': {
        'func': performance_show_indicators,
        'description': 'Display monitoring metricsDetails',
        'params': ['indicators'],
        'subtopic': 'performance'
    },
    'performance_list_indicators': {
        'func': performance_list_indicators,
        'description': '列出监控Object typeSupported monitoring metrics',
        'params': ['obj_type_id'],
        'subtopic': 'performance'
    },
    'performance_list_object_types': {
        'func': performance_list_object_types,
        'description': 'Get all monitoringObject type',
        'params': ['filter'],
        'subtopic': 'performance'
    },
    # check_result subtopic actions
    'check_result_list': {
        'func': check_result_list,
        'description': 'Query check policy exception results',
        'params': ['object_name', 'level', 'object_ids', 'object_native_id', 'object_type', 'policy_id', 'policy_name', 'policy_types', 'cause', 'alarm_type', 'first_occur_time', 'last_occur_time', 'page_no', 'page_size', 'sort_key', 'sort_dir'],
        'subtopic': 'check_result'
    },
    'check_result_show': {
        'func': check_result_show,
        'description': 'Query check policy exception details',
        'params': ['check_result_id'],
        'subtopic': 'check_result'
    },
    # check_policy subtopic actions
    'check_policy_list': {
        'func': check_policy_list,
        'description': 'Query check policy list',
        'params': ['policy_name', 'exact_query', 'status', 'policy_type', 'policy_source', 'alarm_type', 'object_type', 'page_no', 'page_size', 'sort_key', 'sort_dir', 'administrative_status', 'policy_category', 'object_category'],
        'subtopic': 'check_policy'
    },
    'check_policy_execute': {
        'func': check_policy_execute,
        'description': 'Execute check policy',
        'params': ['policy_id'],
        'subtopic': 'check_policy'
    },
    'check_policy_enable': {
        'func': check_policy_enable,
        'description': 'Enable check policy',
        'params': ['policy_id'],
        'subtopic': 'check_policy'
    },
    'check_policy_disable': {
        'func': check_policy_disable,
        'description': 'Disable check policy',
        'params': ['policy_id'],
        'subtopic': 'check_policy'
    },
    'check_policy_delete': {
        'func': check_policy_delete,
        'description': 'Delete check policy',
        'params': ['policy_id'],
        'subtopic': 'check_policy'
    },
    # topology subtopic actions
    'topology_query_san_path': {
        'func': topology_query_san_path,
        'description': '查询 SAN Path topology（支持 IP_SAN 和 FC_SAN）',
        'params': ['entry_objects', 'san_type'],
        'subtopic': 'topology'
    },
    'topology_query_luns': {
        'func': topology_query_luns,
        'description': '查询拓扑图 LUN 列表',
        'params': ['entry_objects', 'storage_pool_id', 'lun_name', 'san_type', 'page_size', 'page_no'],
        'subtopic': 'topology'
    },
    'topology_query_vms': {
        'func': topology_query_vms,
        'description': 'Query topology VM and virtual disk list，或查询 BMS Physical disk list below',
        'params': ['entry_objects', 'host_id', 'vm_name', 'page_size', 'page_no'],
        'subtopic': 'topology'
    },
    'topology_query_graph_path': {
        'func': topology_query_graph_path,
        'description': 'Query topology library info（支持 NAS、K8s、DB 等业务类型）',
        'params': ['entry_res_type', 'entry_res_id', 'type', 'filter'],
        'subtopic': 'topology'
    },
    # health subtopic actions
    'health_query_data': {
        'func': health_query_data,
        'description': 'Query health-related data（Capacity prediction/性能预测/Performance anomaly）',
        'params': ['type', 'object_id', 'begin_time', 'end_time', 'object_type', 'indicator'],
        'subtopic': 'health'
    },
    'health_show_score': {
        'func': health_show_score,
        'description': '查询object健康度',
        'params': ['object_type', 'object_name', 'object_ids', 'page_no', 'page_size', 'sort_key', 'sort_dir'],
        'subtopic': 'health'
    },
    'health_show_detail': {
        'func': health_show_detail,
        'description': 'Query health dimension deduction details',
        'params': ['object_id', 'object_type', 'health_dimension'],
        'subtopic': 'health'
    }
}
