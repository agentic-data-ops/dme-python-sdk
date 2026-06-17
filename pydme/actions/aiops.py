"""
AIOps intelligent operations
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
    """构建当前告警查询参数"""
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
    """构建历史告警查询参数"""
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

    Query current alarms. Optionally query history alarms simultaneously.

    Args:
        client: DME API client
        alarm_id: alarm ID,supports fuzzy match
        severity: severitylist,取值:critical, major, minor, warning, indeterminate, cleared
        mo_dn: 被管理object DN,支持 inc 操作符匹配
        alarm_group_id: alarm group ID
        dc_id: 数据中心 ID
        product_name: product name
        alarm_name: alarm name,supports fuzzy match
        occur_utc_start: alarm start time(毫秒时间戳)
        occur_utc_end: alarm end time(毫秒时间戳)
        fields: 指定返回的字段list
        page_no: pagination start page,default 1
        page_size: items per page,1~1000,default 100(current alarmquery用)
        cleared: 是否已清除,true/false(history alarmquery用)
        size: 返回的result集最大条数,1~1000,default 100(history alarmquery用)
        iterator: 迭代子,首次query无需传入,后续query使用上次返回的 iterator(history alarmquery用)
        include_history: 开关参数,指定则同时queryhistory alarm

    Returns:
        {
            current_alarms: current alarmlist (List<AlarmInfo>). parameter format: [{
                alarm_id: alarm ID (string),
                alarm_name: alarm name (string),
                severity: severity (string),
                status: status (string),
            }, ...],
            total: total alarms (integer),
        }
    """
    result = {
        'current_alarms': None,
        'history_alarms': None
    }

    # querycurrent alarm(default总是query)
    current_url = "/rest/alarmmgmt/v1/alarms/current-alarm/query"
    current_params = _build_current_alarm_params(
        alarm_id=alarm_id, severity=severity, mo_dn=mo_dn,
        alarm_group_id=alarm_group_id, dc_id=dc_id, product_name=product_name,
        alarm_name=alarm_name, occur_utc_start=occur_utc_start,
        occur_utc_end=occur_utc_end, fields=fields, page_size=page_size
    )

    current_response = client.post(current_url, body=current_params)
    result['current_alarms'] = current_response

    # 如果指定了 include_history,同时queryhistory alarm
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

    Acknowledge (ACK) the specified alarms.

    Args:
        client: DME API client
        csns: alarm serial numberlist(Required),最多 30 个

    Returns:
        operation result
    """
    url = "/rest/alarmmgmt/v1/alarms/operation"

    if not isinstance(csns, list) or len(csns) < 1 or len(csns) > 30:
        raise ValueError("csns 必须是包含 1-30 个元素的列表")

    payload = {
        "csns": csns,
        "operation_type": "ACK"
    }

    print(f"请求 URL: {url}")
    print(f"请求负载:{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


def alarm_unack(client: DMEAPIClient, csns: list) -> dict:
    r"""
    Un-acknowledge alarm

    Un-acknowledge (UNACK) the specified alarms.

    Args:
        client: DME API client
        csns: alarm serial numberlist(Required),最多 30 个

    Returns:
        operation result
    """
    url = "/rest/alarmmgmt/v1/alarms/operation"

    if not isinstance(csns, list) or len(csns) < 1 or len(csns) > 30:
        raise ValueError("csns 必须是包含 1-30 个元素的列表")

    payload = {
        "csns": csns,
        "operation_type": "UNACK"
    }

    print(f"请求 URL: {url}")
    print(f"请求负载:{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


def alarm_clear(client: DMEAPIClient, csns: list) -> dict:
    r"""
    Clear alarm

    Clear (CLEAR) the specified alarms.

    Args:
        client: DME API client
        csns: alarm serial numberlist(Required),最多 30 个

    Returns:
        operation result
    """
    url = "/rest/alarmmgmt/v1/alarms/operation"

    if not isinstance(csns, list) or len(csns) < 1 or len(csns) > 30:
        raise ValueError("csns 必须是包含 1-30 个元素的列表")

    payload = {
        "csns": csns,
        "operation_type": "CLEAR"
    }

    print(f"请求 URL: {url}")
    print(f"请求负载:{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


def diagnose_task_create(client: DMEAPIClient, object_ids: list, object_type: str,
                         begin_time: int, end_time: int, analysis_types: list) -> dict:
    r"""
    Create intelligent analysis task

    Args:
        client: DME API client
        object_ids: 入口分析object ID list(Required),数组大小:1~50
        object_type: 入口objecttype(Required),valid values: 
            - VM: Virtual machine
            - STORAGE_HOST: Storage host
            - STORAGE_DEVICE: Storage device
            - LUN: LUN
            - FILE_SYSTEM: Filesystem
            - VBS_CLIENT: VBS Client
            - DATATURBO: DPC
            - STORAGE_POOL: Storage pool
            - IP_CLIENT: IP Client
            - HOST_GROUP: Storage host group
            - FC_PORT: FC port
            - ETH_PORT: Ethernet port
            - LUN_GROUP: LUN group
            - LOGIC_PORT: Logic port
            - CONTROLLER: Controller
            - NAMESPACE: Namespace
        begin_time: 分析start time(Required),Unix 时间戳(毫秒),必须为整分钟时间点,支持最近七天内的诊断
        end_time: 分析end time(Required),Unix 时间戳(毫秒),必须为整分钟时间点
                  分析时间间隔范围必须大于 30 分钟,小于 24 小时
        analysis_types: 智能分析typelist(Required),数组大小:1~4,valid values: 
            - highLatency: High latency
            - healthAnalysis: Health quick check
            - IOInterrupt: IO interrupt
            - highReadLatency: High read latency
            - highWriteLatency: High write latency
            - trafficAnalysis: Traffic analysis
            - cpuUsageAnalysis: CPU consumption analysis

    Returns:
        {
            total: 智能分析任务total (int32, 0~4),
            data: 智能分析任务响应resultlist (List<ResponseTaskInfoOpenapi>). parameter format: [{
                    id: task ID (string, 1~32个字符),
                    analysis_type: 智能分析type枚举 (string). valid values: highLatency (High latency), healthAnalysis (Health quick check), IOInterrupt (IO中断), highReadLatency (High read latency), highWriteLatency (High write latency), trafficAnalysis (Traffic analysis), cpuUsageAnalysis (cpu消耗分析),
                    error_msg: 错误info (string, 1~1024个字符),
                    is_succeed: 是否create成功 (boolean). valid values: true (create成功), false (create失败),
                 }, ...],
        }
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
    print(f"请求负载:{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


# ============ Performance 性能监控子主题函数 ============


def performance_create_collect_task(client: DMEAPIClient, begin_time: int, end_time: int,
                        object_type_id: str, object_ids: list,
                        indicator_ids: list) -> dict:
    """
    create性能文件收集任务

    收集范围为开始日期到结束日期的性能文件,只支持收集 7 天内的数据,
    每次传入的object乘以指标数不超过 2000.

    Args:
        client: DME API client
        begin_time: start time(必填,Unix 时间戳毫秒)
        end_time: end time(必填,Unix 时间戳毫秒)
        object_type_id: objecttype ID(必填,1~32 个字符)
        object_ids: object ID list(必填,最多 2000 个,ID 长度 1~32 位)
        indicator_ids: 指标 ID list(必填,最多 20 个,ID 长度 1~16 位)

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
    下载性能文件

    Args:
        client: DME API client
        task_id: 任务 ID(必填)

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
    query历史performance data

    根据传入参数中的"range"字段所取的枚举值或从开始到end time范围内的query数据.
    有汇聚数据情况下,返回result序列是平均值序列,并包含最大值,最小值以及对应时间戳.

    使用说明:
    - objecttype和指标定义:从性能指标模型文档获取 (reference/dme_performance_model/index.md)
    - object ID (CMDB 实例 ID) 获取步骤:
      1. 运行 `cmdb instance list --help` 查看帮助,了解类定义和query方式
      2. 根据帮助info,从 CMDB 资源模型中确定要query的resource type (Class name)
      3. 使用 `cmdb instance list --class_name <Class name>` query实例list
      4. 从返回result中获取对应资源的 instance_id (即 obj_ids 参数)

    Args:
        client: DME API client
        obj_type_id: 监控objecttype标识(必填),对应监控objecttype ID
                     从性能指标模型文档获取:reference/dme_performance_model/index.md
        indicator_ids: 监控指标标识list(必填,最多 100 个),对应指标 ID
                       从性能指标模型文档获取:reference/dme_performance_model/index.md
        obj_ids: 监控object标识list(必填,最多 512 个),对应 CMDB 实例 ID
                 获取方式:
                 1. 运行 `cmdb instance list --help` 查看帮助,了解类定义
                 2. 根据帮助确定要query的resource type (Class name)
                 3. 运行 `cmdb instance list --class_name <Class name>` query实例
                 4. 从返回result中获取 instance_id
        obj_type: 监控objecttype(可选,1~512 个字符)
        indicators: 监控指标list(可选,最多 100 个)
        ext_dimensions: 扩展维度infolist(可选,最多 100 个)
        interval: 间隔粒度(Optional)
                  valid values: ONE_MINUTE(1 分钟), MINUTE(5 分钟), HALF_HOUR(30 分钟),
                  HOUR(1 小时), DAY(1 天), WEEK(1 周), MONTH(1 个月)
        range: 时间范围(可选,default LAST_1_HOUR)
               valid values: LAST_5_MINUTE(最近 5 分钟), LAST_1_HOUR(最近 1 小时),
               LAST_1_DAY(最近 1 天), LAST_1_WEEK(最近 1 周), LAST_1_MONTH(最近 1 个月),
               LAST_1_QUARTER(最近 3 个月), HALF_1_YEAR(最近半年), LAST_1_YEAR(最近 1 年),
               BEGIN_END_TIME(自行设置开始和end time), INVALID(无效值)
        begin_time: query开始时刻(Optional),仅 range 为 BEGIN_END_TIME 时生效,必须比 end_time 小
        end_time: query结束时刻(Optional),仅 range 为 BEGIN_END_TIME 时生效,必须比 begin_time 大

    Returns:
        {
            status_code: status code (int32),
            error_code: error code (int32),
            error_msg: error message (string),
            data: performance data (Map<object, Map<object, HistoryPerfData>>),
        }
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
    显示监控指标详细info

    Args:
        client: DME API client
        indicators: 监控object指标标识list(必填,最多 1000 个字符)
                   可以是整数list或字符串list,如 [123, 456] 或 ["123", "456"]

    Returns:
        {
            status_code: status code (int32),
            error_code: error code (int32),
            error_msg: error message (string),
            data: 监控指标映射 (Map<object, SimpleIndicator>),
        }
    """
    url = "/rest/metrics/v1/mgr-svc/indicators"

    # 确保 indicators 是整数list
    if indicators:
        indicators = [int(i) for i in indicators]

    # API 要求直接传递数组,而不是object
    response = client.post(url, body=indicators)
    return response


def performance_list_indicators(client: DMEAPIClient, obj_type_id: int) -> dict:
    """
    列出监控objecttype支持的监控指标

    Args:
        client: DME API client
        obj_type_id: 监控objecttype标识(必填)

    Returns:
        监控指标info,包含 indicator_ids list
    """
    url = "/rest/metrics/v1/mgr-svc/obj-types/{obj_type_id}/indicators"

    response = client.get(url, params={"obj_type_id": obj_type_id})
    return response


def performance_list_object_types(client: DMEAPIClient, filter: str = None) -> dict:
    """
    获取所有监控objecttype

    Args:
        client: DME API client
        filter: 过滤关键字(Optional),用于模糊匹配 zh_cn 和 en_us 字段
                如果提供,仅返回匹配的objecttype

    Returns:
        {
            status_code: status code (int32),
            error_code: error code (int32),
            error_msg: error message (string),
            data: 监控objecttypelist (List<ObjectTypeBody>). parameter format: [{
                obj_type_id: 监控objecttype编号 (int64),
                parent_obj_type_id: 父type编号 (int64),
                resource_category: 资源CI (string),
                resource_provider: 资源提供者 (string),
                en_us: 英文description (string),
                zh_cn: 中文description (string),
            }, ...],
        }
        resource_provider, en_us, zh_cn, group_en_us, group_zh_cn 等字段
    """
    url = "/rest/metrics/v1/mgr-svc/obj-types"

    response = client.get(url)

    # 如果提供了 filter 参数,过滤result
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
    query健康度相关数据

    querycapacity预测、性能预测、性能异常等健康度相关数据. 

    Args:
        client: DME API client
        type: 数据type(Required), valid values: capacity_prediction (capacity预测), performance_prediction (性能预测), performance_anomaly (性能异常)
        object_id: 资源 ID (必选, 1~256 个字符)
        begin_time: start time(Required), 自 1970 年 1 月 1 日 (00:00:00GMT)至当前时间的毫秒数
        end_time: end time(Required), 自 1970 年 1 月 1 日 (00:00:00GMT)至当前时间的毫秒数
        object_type: resource type(Required)
        indicator: resource type所对应的指标 (capacity_prediction 和 performance_prediction 必选)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含queryresult
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
    queryobject健康度

    query指定typeobject的健康度info. 

    Args:
        client: DME API client
        object_type: objecttype(Required)
                    valid values: storage (Storage device), storage_pool (Storage pool), storage_host (Storage host),
                           storage_disk (硬盘), storage_port (存储端口), fcswitch_port (光纤交换机端口),
                           storage_file_system (Filesystem), controller (Controller), replication_cg (远程复制一致性组),
                           volume (LUN), tier (服务等级), datastore (数据存储), virtual_machine (Virtual machine),
                           storage_name_space (Namespace), storage_node (存储节点), dpc (DPC)
        object_name: objectname, supports fuzzy query (可选, 最多 256 个字符)
        object_ids: object resId list, 用于批量精确查找 (可选, 最多支持 100 个 ID)
        page_no: 分页query的起始location (可选, 最小值: 1)
        page_size: 每页显示的count (可选, 1~100, default 20)
        sort_key: 排序字段(Optional), 按分数进行排序, valid values: health_score
        sort_dir: 排序方式(Optional), valid values: asc, desc

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含object健康度list
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
    query健康维度的扣分details

    query指定object在指定健康维度下的扣分details. 

    Args:
        client: DME API client
        object_id: object Id (必选, 1~128 个字符)
        object_type: objecttype(Required)
                    valid values: storage, storage_pool, storage_host, storage_disk, storage_port,
                           fcswitch_port, storage_file_system, controller, replication_cg, volume,
                           tier, datastore, virtual_machine, storage_name_space, storage_node,
                           dpc, gfs, dpc_client, vbs_client
        health_dimension: 健康维度(Required)
                        valid values: alarm (告警), performance_anomaly (性能异常),
                              performance_prediction (性能预警), capacity_prediction (capacity预警)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含指标扣分list
    """
    url = "/rest/healthmgmt/v1/health-result/dimension-score/query"

    payload = {
        'object_id': object_id,
        'object_type': object_type,
        'health_dimension': health_dimension
    }

    response = client.post(url, body=payload)
    return response



# ============ Performance 性能监控子主题函数 ============




def diagnose_task_status(client: DMEAPIClient, task_id: str) -> dict:
    r"""
    query性能诊断task status

    根据任务 ID query诊断task status.

    Args:
        client: DME API client
        task_id: 任务 ID(Required),1~128 个字符

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        },包含:
        - task_id: 任务 ID
        - task_status: task status,valid values: 
            - executing: 执行中
            - failed: 失败
            - success: 成功
            - waiting: 等待
            - terminated: 已终止
        - task_result: 任务result,valid values: 
            - un_analyzed: 未分析
            - warning: 警告
            - abnormal: 异常
            - event: 事件
        - total_step_count: 总步骤数
        - finish_step_count: 已完成步骤数
    """
    url = "/rest/dmegraphanalysis/v1/perf-tasks/query-status"

    payload = {
        "task_id": task_id
    }

    print(f"请求 URL: {url}")
    print(f"请求负载:{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


# ============================================================================
# 检查策略 (check_policy) 子主题函数
# ============================================================================

def check_policy_list(client: DMEAPIClient, policy_name: str = None, exact_query: bool = None,
                        status: str = None, policy_type: str = None, policy_source: str = None,
                        alarm_type: str = None, object_type: str = None, page_no: int = 1,
                        page_size: int = 20, sort_key: str = None, sort_dir: str = None,
                        administrative_status: str = None, policy_category: str = None,
                        object_category: str = None) -> dict:
    """
    query检查策略list

    Args:
        client: DME API client
        policy_name: 策略name (supports fuzzy query, 1~256 个字符)
        exact_query: name是否精确query (true-精确query, false-模糊query), default false
        status: 策略status (normal-正常, checking-检查中, failed-检查失败, queuing-排队中)
        policy_type: 策略type (performance-性能阈值, capacity-capacity阈值, availability-可用性, 
                    configuration-配置, recyclable-可回收资源, lowload-低负载资源, 
                    performance_anomaly-性能异常, performance_prediction-性能预警, 
                    capacity_prediction-capacity预警, history_performance-历史性能, 
                    load_imbalance-负载失衡, highload-高负载资源)
        policy_source: 来源 (pre-define-预置, user-define-自定义)
        alarm_type: 告警type (violation-异常, alarm-告警, event-事件)
        object_type: objecttype (storage-存储, lun-逻辑单元, host-主机等)
        page_no: 分页query的页码, 1~1000, default 1
        page_size: 分页query的个数, 1~100, default 20
        sort_key: 排序字段 (last_check_time-最后检查时间, failed_count-检查不通过的object个数)
        sort_dir: 排序方式 (asc-正序, desc-降序)
        administrative_status: 管理status (enable-启用, disable-禁用)
        policy_category: 检查分类 (configuration-配置, performance-性能, capacity-capacity, faults-故障, optimization-优化)
        object_category: object分类 (Storage-Storage device, IPSwitch-以太网交换机, FCSwitch-光纤交换机, 
                       Virtualization-虚拟化, Server-服务器, HCI-超融合, Client-客户端)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }, 包含 total (total)和 policies (策略list)
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
    执行检查策略

    执行指定的检查策略. 

    Args:
        client: DME API client
        policy_id: 策略 ID (1~64 个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/policymgmt/v1/policies/{policy_id}/execute"

    response = client.post(url, params={"policy_id": policy_id})
    return response


def check_policy_enable(client: DMEAPIClient, policy_id: str) -> dict:
    """
    启用检查策略

    启用指定的检查策略. 

    Args:
        client: DME API client
        policy_id: 策略 ID (1~64 个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/policymgmt/v1/policies/{policy_id}/enable"

    response = client.post(url, params={"policy_id": policy_id})
    return response


def check_policy_disable(client: DMEAPIClient, policy_id: str) -> dict:
    """
    禁用检查策略

    禁用指定的检查策略. 

    Args:
        client: DME API client
        policy_id: 策略 ID (1~64 个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/policymgmt/v1/policies/{policy_id}/disable"

    response = client.post(url, params={"policy_id": policy_id})
    return response


def check_policy_delete(client: DMEAPIClient, policy_id: str) -> dict:
    """
    delete检查策略

    delete指定的检查策略. 

    Args:
        client: DME API client
        policy_id: 策略 ID (1~64 个字符)

    Returns:
        {
            task_id: task ID (string, 1~64个字符),
        }
    """
    url = "/rest/policymgmt/v1/policies/{policy_id}"

    response = client.delete(url, params={"policy_id": policy_id})
    return response


# ============================================================================
# 检查result (check_result) 子主题函数
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
    query检查策略异常检查resultlist

    query检查策略的异常检查result, 支持多种过滤条件和分页query. 

    Args:
        client: DME API client
        object_name: objectname (supports fuzzy query, 1~256 个字符)
        level: 异常级别(Optional). valid values: critical (紧急), major (重要), minor (次要), info (提示)
        object_ids: object ID list (最多 100 个)
        object_native_id: object nativeId (1~384 个字符)
        object_type: objecttype(Optional). valid values: bond_port (绑定端口), clone_pair (克隆pair), controller (Controller), datastore (数据存储), device_pair (设备pair), dtree (Dtree), dtree_user_quota (Dtree用户quota), ethernet_port (Ethernet port), expansion_port (级联端口), fc_link (FC链路), fc_port (FC端口), fc_switch (FC交换机), fcswitch_port (FC交换机端口), filesystem_snapshot (Filesystem快照), fs_hyper_metro_pair (Filesystem双活), hci (超融合), host (主机), host_initiator (主机启动器), hyper_metro_cg (双活一致性组), hyper_metro_pair (双活), ip_link (IP链路), ip_switch (以太网交换机), ip_switch_board (以太网交换机单板), ip_switch_fan (以太网交换机风扇), ip_switch_port (以太网交换机端口), ip_switch_psu (以太网交换机电源), logic_port (Logic port), lun_group (LUN组), lun_snapshot (LUN快照), dataturbo (dataturbo协议), nfsv3 (NFS_v3协议), nfsv4 (NFS_v4协议), nfsv41 (NFS_v4.1协议), phost_nic (主机网口), physical_server (服务器), remote_device (远端设备), replication_cg (复制一致性组), replication_pair (复制Pair), roce_port (RoCE端口), sas_port (SAS端口), server_nic (服务器网卡), smb1 (SMB1协议), smb2_3 (SMB2/3协议), storage (存储), storage_disk (硬盘), storage_file_system (Filesystem), storage_host (Storage host), host_link (Storage host), storage_host_group (Storage host group), storage_host_initiator (Storage host启动器), storage_name_space (Namespace), storage_node (存储节点), storage_pool (Storage pool), storage_port (存储端口), tier (服务等级), virtual_cluster (虚拟化cluster), virtual_disk (虚拟硬盘), virtual_host (宿主机), virtual_machine (Virtual machine), virtual_machine_snapshot (Virtual machine快照), virtual_nic (虚拟网卡), virtual_gpu (GPU), volume (LUN), vstore (vStore), zone (zone), filesystem_replication_pair (Filesystem复制Pair), dpc, gfs (GFS), vbs_client (vbs客户端), dpc_client (dpc客户端), nfs_plus_client_link (NFS+客户端链路), knowledge_base_node (KnowledgeBase节点), object_data_flow (object数据流动)
        policy_id: 策略 ID (精确query, 1~64 个字符)
        policy_name: 策略name (supports fuzzy query, 1~256 个字符)
        policy_types: 策略typelist (最多 30 个). valid values: performance (性能阈值), capacity (capacity阈值), availability (可用性), configuration (配置), recyclable (可回收资源), lowload (低负载资源), performance_anomaly (性能异常), performance_prediction (性能预警), capacity_prediction (capacity预警), history_performance (历史性能), load_imbalance (负载失衡), highload (高负载资源)
        cause: 异常原因 (supports fuzzy query, 1~768 个字符)
        alarm_type: 告警type(Optional). valid values: violation (异常), alarm (告警), event (事件)
        first_occur_time: 第一次异常时间范围 ({beginTime, endTime}, UTC 时间戳, 单位 ms)
        last_occur_time: 最后一次异常时间范围 ({beginTime, endTime}, UTC 时间戳, 单位 ms)
        page_no: 分页query的页码, 1~10000, default 1
        page_size: 分页query的个数, 1~2000, default 20
        sort_key: 排序字段(Optional). valid values: violation_count (异常次数)
        sort_dir: 排序方式(Optional). valid values: asc (正序), desc (降序)

    Returns:
        {
            total: 异常检查resulttotal (int32, 0~2147483647),
            results: 异常检查resultlist (List<PolicyCheckResult>, max array members: 2000). parameter format: [{
                    check_result_id: 检查resultID (string, 1~64个字符),
                    policy_id: 策略ID (string, 1~64个字符),
                    policy_name: 策略name (string, 1~256个字符),
                    policy_type: 检查策略type (string). valid values: performance (性能阈值), capacity (capacity阈值), availability (可用性), configuration (配置), recyclable (可回收资源), lowload (低负载资源), performance_anomaly (性能异常), performance_prediction (性能预警), capacity_prediction (capacity预警), history_performance (历史性能), load_imbalance (负载失衡), highload (高负载资源),
                    object_name: objectname (string, 0~1000个字符),
                    object_id: objectID (string, 1~64个字符),
                    object_native_id: objectnativeId (string, 0~500个字符),
                    object_type: objecttype (string),
                    level: 异常级别 (string). valid values: critical (紧急), major (重要), minor (次要), info (提示),
                    cause: 异常条件 (string, 0~1000个字符),
                    alarm_type: 告警type (string). valid values: violation (异常), alarm (告警), event (事件),
                    violation_count: 异常次数 (int32, 0~2147483647),
                    first_occur_time: 第一次异常时间 (int64, UTC时间戳ms),
                    last_occur_time: 最后一次异常时间 (int64, UTC时间戳ms),
                    location_info: 定位info (string, 0~3000个字符),
                    abnormal_reasons: 异常原因list (List<string>, max array members: 100),
                 }, ...],
        }
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
    query检查策略异常检查resultdetails

    query指定检查result的详细info. 

    Args:
        client: DME API client
        check_result_id: 检查result ID (1~64 个字符)

    Returns:
        {
            check_result_id: 检查resultID (string, 1~64个字符),
            policy_id: 策略ID (string, 1~64个字符),
            policy_name: 策略name (string, 1~256个字符),
            policy_type: 检查策略type (string). valid values: performance (性能阈值), capacity (capacity阈值), availability (可用性), configuration (配置), recyclable (可回收资源), lowload (低负载资源), performance_anomaly (性能异常), performance_prediction (性能预警), capacity_prediction (capacity预警), history_performance (历史性能), load_imbalance (负载失衡), highload (高负载资源),
            object_name: objectname (string, 0~1000个字符),
            object_id: objectID (string, 1~64个字符),
            object_native_id: objectnativeId (string, 0~500个字符),
            object_type: objecttype (string),
            level: 异常级别 (string). valid values: critical (紧急), major (重要), minor (次要), info (提示),
            cause: 异常条件 (string, 0~1000个字符),
            alarm_type: 告警type (string). valid values: violation (异常), alarm (告警), event (事件),
            violation_count: 异常次数 (int32, 0~2147483647),
            first_occur_time: 第一次异常时间 (int64, UTC时间戳ms),
            last_occur_time: 最后一次异常时间 (int64, UTC时间戳ms),
            location_info: 定位info (string, 0~3000个字符),
            abnormal_reasons: 异常原因list (List<string>, max array members: 100),
        }
    """
    url = "/rest/policymgmt/v1/abnormal-check-results/{check_result_id}"

    response = client.get(url, params={"check_result_id": check_result_id})
    return response


# action list, for CLI help
# ============================================================================
# 拓扑管理 (topology) 子主题函数
# ============================================================================

def topology_query_luns(client: DMEAPIClient, entry_objects: list, storage_pool_id: str,
               lun_name: str = None, san_type: str = None, page_size: int = 20, page_no: int = 1) -> dict:
    r"""
    query拓扑图 LUN list

    根据指定入口object和Storage poolquery LUN list. 

    Args:
        client: DME API client
        entry_objects: 入口objectlist (List<LunTopoQueryEntryObject>, 必选, max array members: 5). parameter format: [{
                id: 入口object id (必选, string, 1~128 个字符),
                type: 入口objecttype (必选, string). valid values: host (物理主机), storage (闪存存储/分布式存储), host_group (主机组), lun (LUN), vm (Virtual machine), datastore (数据存储), application (应用), switch_port (光纤交换机端口), storage_pool (Storage pool). 注意: ip_san 时不支持 datastore/application/switch_port; 入口object为 vm/storage_pool 时最多支持 5 个, 其余type只支持 1 个,
            }, ...]
        storage_pool_id: storage池 ID (必选, string, 1~128 个字符). 格式为 {storageId}STORAGE_POOL{poolId}, 如 "b9326bbf-...STORAGE_POOL163BECEA...", 从 storage pool list 返回的 id 字段获取
        san_type: 存储区域网络type (可选, string). valid values: ip_san, fc_san
        lun_name: LUN name (可选, string, 1~256 个字符), supports fuzzy query
        page_size: 分页query的个数 (可选, int32, 1~20), default 20
        page_no: 分页query的起始location (可选, int32, 1~2147483647), default 1

    Returns:
        {
            total: LUN queryresulttotal (int32),
            luns: LUN queryresultlist (List<LunObject>). parameter format: [{
                id: LUN id (string, 1~128个字符),
                name: LUN name (string, 1~256个字符),
                datastore: LUN 对应数据存储list (List<LunsQueryDataStoreItem>). attribute format: [{
                    id: 数据存储 id (string, 1~128个字符),
                    name: 数据存储name (string, 1~256个字符),
                    storage_type: 存储type (string). valid values: vmfs (Virtual machineFilesystem),
                    vr_type: 虚拟化type (string). valid values: vmware, hcs,
                }, ...],
                is_replication_member: 是否是复制卷 (boolean, true/false),
                is_replication_primary: 是否是复制卷本端 (boolean, true/false),
                is_hyper_metro_member: 是否是保护卷 (boolean, true/false),
                is_hyper_metro_primary: 是否是保护卷本端 (boolean, true/false),
                storage_pool_id: Storage pool ID (string, 1~140个字符). 格式为 {storageId}STORAGE_POOL{poolId},
            }, ...],
        }
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
    print(f"请求负载：{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


def topology_query_san_path(client: DMEAPIClient, entry_objects: list, san_type: str = None) -> dict:
    r"""
    query SAN 路径拓扑结构

    根据指定入口objectquery SAN 网络中从主机到Storage pool之间的拓扑结构. 
    支持 IP_SAN 和 FC_SAN 两种type. 

    Args:
        client: DME API client
        entry_objects: 入口objectlist (必选, max array members: 1). FC_SAN parameter format: [{
                id: 入口object id (必选, string, 1~128 个字符),
                type: 入口objecttype (必选, string). valid values: host (主机), storage (闪存Storage device), lun (LUN), host_group (主机组), vm (Virtual machine), datastore (数据存储), application (应用), switch_port (光纤交换机端口), storage_pool (Storage pool),
            },...]. IP_SAN parameter format: [{
                id: 入口object id (必选, string, 1~128 个字符),
                type: 入口objecttype (必选, string). valid values: host (主机), storage (闪存存储或分布式存储), lun (LUN), host_group (主机组), vm (Virtual machine), storage_pool (Storage pool). 注: IP_SAN 不支持 datastore/application/switch_port type, 最多支持 5 个object,
            }, ...]
        san_type: SAN type (可选, string). valid values: ip_san, fc_san
                  - 不指定时, 同时调用 IP_SAN 和 FC_SAN 两个 API, 组合返回数据
                  - 指定为 ip_san 时, 仅调用 IP_SAN API
                  - 指定为 fc_san 时, 仅调用 FC_SAN API

    Returns:
        当 san_type=fc_san 或不指定时 (FC_SAN 部分): 
        {
            fabrics: Fabric list (List<HostToStoragePoolFabric>). parameter format: [{
                id: Fabric id (string, 1~64个字符),
                name: Fabric name (string, 1~128个字符),
                switches: 交换机list (List<SwitchItem>). attribute format: [{
                    id: 交换机节点 id (string, 1~64个字符),
                    name: 交换机节点name (string, 1~128个字符),
                    ports: 交换机端口list (List<SwitchPortItem>). attribute format: [{
                        id: 交换机端口节点 id (string, 1~64个字符),
                        name: 交换机端口节点name (string, 1~128个字符),
                        status: 交换机端口status (string). valid values: normal (正常), abnormal (故障), unknown (未知),
                    }, ...],
                }, ...],
                port_links: 交换机端口链路list (List<PortLinkItem>). attribute format: [{
                    left_port: 左端口 (PortNodeItem). attribute format: {
                        id: 端口 Id (string, 1~64个字符),
                        type: 端口type (string). valid values: host_port, switch_port, storage_port,
                    },
                    right_port: 右端口 (PortNodeItem),
                }, ...],
                switch_links: 交换机连接关系list (List<SwitchLinkItem>). attribute format: [{
                    host_to_switch_id: 主机连接的交换机 ID (string, 1~64个字符),
                    storage_to_switch_id: 存储连接的交换机 ID (string, 1~64个字符),
                }, ...],
            }, ...],
            hosts: 主机list (List<HostToStoragePoolHost>). attribute format: [{
                id: 主机 id (string, 1~64个字符),
                name: host name (string, 1~256个字符),
                access_mode: 接入模式 (string). valid values: vcenter, none,
                host_groups: 主机组list (List<HostToStoragePoolHostGroup>),
                ports: 主机端口list (List<HostToStoragePoolPort>),
                deployment_type: 部署type (string). valid values: BMS (裸金属服务器), ECS (ECS主机),
                direct_storage_ids: 主机直连的Storage device ID list (List<string>),
            }, ...],
            storages: 存储list (List<HostToStoragePoolStorage>). attribute format: [{
                id: 存储 id (string, 1~64个字符),
                name: 存储name (string, 1~128个字符),
                product_model: storage device type (string),
                controllers: Controllerlist (List<HostToStoragePoolController>),
                pools: Storage poollist (List<HostToStoragePoolPool>),
                disks: 存储磁盘list (List<HostToStorageDiskDisks>),
            }, ...],
        }
        当 san_type=ip_san 时 (IP_SAN): 
        {
            switches: 交换机list (List<SwitchItem>),
            hosts: 主机list (List<HostToStoragePoolHost>),
            storages: 存储list (List<HostToStoragePoolStorage>),
            switch_links: 交换机连接关系list (List<SwitchLinkItem>),
        }
        当 san_type=None 时: 
        {
            ip_san: { IP_SAN 返回数据 },
            fc_san: { FC_SAN 返回数据 },
        }
    """
    result = {}

    # 如果未指定 san_type, 同时调用两个 API
    if san_type is None:
        # 调用 IP_SAN API
        ip_san_url = "/rest/topomgmt/v1/topo-data/ipsan/host-storage/query"
        ip_san_payload = {"entry_objects": entry_objects}
        print(f"请求 URL: {ip_san_url}")
        print(f"请求负载：{json.dumps(ip_san_payload, ensure_ascii=False, indent=2)}")
        ip_san_response = client.post(ip_san_url, body=ip_san_payload)
        result['ip_san'] = ip_san_response

        # 调用 FC_SAN API
        fc_san_url = "/rest/topomgmt/v1/topo-data/host-storage/query"
        fc_san_payload = {"entry_objects": entry_objects}
        print(f"请求 URL: {fc_san_url}")
        print(f"请求负载：{json.dumps(fc_san_payload, ensure_ascii=False, indent=2)}")
        fc_san_response = client.post(fc_san_url, body=fc_san_payload)
        result['fc_san'] = fc_san_response

        return result

    # 如果指定了 san_type, 只调用对应的 API
    elif san_type == 'ip_san':
        url = "/rest/topomgmt/v1/topo-data/ipsan/host-storage/query"
        payload = {"entry_objects": entry_objects}
        print(f"请求 URL: {url}")
        print(f"请求负载：{json.dumps(payload, ensure_ascii=False, indent=2)}")
        response = client.post(url, body=payload)
        return response

    elif san_type == 'fc_san':
        url = "/rest/topomgmt/v1/topo-data/host-storage/query"
        payload = {"entry_objects": entry_objects}
        print(f"请求 URL: {url}")
        print(f"请求负载：{json.dumps(payload, ensure_ascii=False, indent=2)}")
        response = client.post(url, body=payload)
        return response

    else:
        raise ValueError(f"无效的 san_type 参数：{san_type}，仅支持：ip_san, fc_san")




def topology_query_vms(client: DMEAPIClient, entry_objects: list, host_id: str,
              vm_name: str = None, page_size: int = 20, page_no: int = 1) -> dict:
    r"""
    query拓扑图Virtual machine和虚拟磁盘list, 或query BMS 下物理磁盘list

    根据指定入口objectquery虚拟化资源. 

    Args:
        client: DME API client
        entry_objects: 入口objectlist (List<VmTopoQueryEntryObject>, 必选, max array members: 5). parameter format: [{
                id: 入口object id (必选, string, 1~128 个字符),
                type: 入口objecttype (必选, string). valid values: vm (Virtual machine), host_group (主机组), host (主机), storage (闪存存储或分布式存储), lun (LUN), datastore (数据存储), switch_port (光纤交换机端口), storage_pool (Storage pool),
            }, ...]
        host_id: 主机 ID (必选, string, 0~128 个字符)
        vm_name: Virtual machinename搜索参数 (可选, string, 0~256 个字符), supports fuzzy match
        page_size: 分页query的个数 (可选, int32, 1~20), default 20
        page_no: 分页query的起始location (可选, int32, 1~2147483647), default 1

    Returns:
        {
            total: vms queryresulttotal (int32),
            vms: vm queryresultlist (List<VirtualMachine>). parameter format: [{
                id: id (string, 1~64个字符),
                name: vm name (string, 1~128个字符),
                ip: vm ip (string, 1~3072个字符),
                host_id: 物理主机 ID (string, 1~64个字符),
                vr_type: 虚拟化type (string). valid values: vmware, hcs,
                vdisks: 虚拟盘list (List<VirtualDisk>). attribute format: [{
                    id: vdisk id (string, 1~64个字符),
                    name: vdisk name (string, 1~128个字符),
                }, ...],
            }, ...],
            disks: 物理主机关联的物理磁盘list (List<PhysicalDisk>). parameter format: [{
                id: disk id (string, 1~64个字符),
                native_id: disk native id (string, 1~768个字符),
                name: disk name (string, 1~768个字符),
            }, ...],
        }
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
    print(f"请求负载：{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


def topology_query_graph_path(client: DMEAPIClient, entry_res_type: str, entry_res_id: str,
                type: str = None, filter: list = None) -> dict:
    r"""
    query拓扑图库info

    query拓扑图库info, 支持 NAS、K8s、DB 等业务type. 

    Args:
        client: DME API client
        entry_res_type: 入口resource type (必选, string). valid values: storage_device (Storage device), disk (硬盘), storage_pool (Storage pool), hyper_scale_pool (全局池), file_system (Filesystem), controller (Controller), eth_port (以太/RoCE端口), ib_port (IB端口), logic_port (Logic port), ip_client (IP客户端), dtree (Dtree), lun (LUN), k8s_application (容器应用), k8s_workload (工作负载), k8s_pod (容器组), k8s_pvc (持久卷申领), k8s_pv (持久卷), k8s_cluster (容器cluster), k8s_node (容器节点), k8s_vc_job (Volcano Job), data_turbo_client (DataTurbo客户端), enclosures (机框), eth_switch (交换机), storage_zone (存储zone), service_network (业务网络), db_instance (高斯数据库实例), db_node (高斯数据库节点)
        entry_res_id: 入口资源 ID (必选, string, 1~256 个字符)
        type: 业务type (可选, string). valid values: nas, k8s, db
        filter: 条件过滤list (可选, List<TopoFilter>, max array members: 10). parameter format: [{
                type: 拓扑query返回resource type (可选, string). 可选值与 entry_res_type 相同,
                key: 字段name (可选, string, 1~256个字符). 如 id, name, ip,
                value: 字段值 (可选, string, 0~256个字符),
                operator: 比较方式 (可选, string). valid values: lt (小于), le (小于等于), eq (等于), gt (大于), ge (大于等于), ne (不等于), contains (包含),
            }, ...]

    Returns:
        {
            nodes: 节点list (List<NodeItem>). parameter format: [{
                id: 节点object ID (string, 1~256个字符),
                type: 拓扑query返回resource type (string). valid values: storage_device, disk, storage_pool, hyper_scale_pool, file_system, controller, eth_port, ib_port, logic_port, ip_client, dtree, lun, k8s_application, k8s_workload, k8s_pod, k8s_pvc, k8s_pv, k8s_cluster, k8s_node, k8s_vc_job, k8s_pod_group, data_turbo_client, enclosures, eth_switch, storage_zone, service_network, db_instance, db_node, host, host_port, storage_port,
                label: 节点objectname (string, 1~256个字符),
                sub_type: 工作负载type (string, 仅 k8s_workload 时). valid values: deployment, replica_set, stateful_set, daemon_set, job, cron_job,
            }, ...],
            edges: 边list (List<EdgeItem>). parameter format: [{
                source: 起始节点 ID (string, 1~256个字符),
                target: 目标节点 ID (string, 1~256个字符),
                edge_type: 边type (string). valid values: edge_k8s_node_to_k8s_pod, edge_storage_pool_to_storage_disk, edge_filesystem_to_storage_pool, edge_storage_disk_to_storage_device, edge_k8s_pvc_to_k8s_pv, edge_k8s_pod_to_k8s_pvc, edge_dtree_to_filesystem, edge_lun_storage_pool, edge_k8s_cluster_to_k8s_node, edge_k8s_pv_to_lun, edge_k8s_pv_to_dtree, edge_nas_client_to_logic_port, edge_logic_port_to_ethernet_port, edge_ethernet_port_to_controller, edge_controller_to_filesystem, edge_data_turbo_client_to_logic_port, edge_controller_to_ethernet_port, edge_data_turbo_client_to_service_network, edge_ethernet_port_to_eth_switch_port, edge_service_network_to_logic_port, edge_a800_enclosures_to_storage_zone, edge_controller_to_enclosures, edge_storage_zone_to_filesystem, edge_eth_switch_port_to_eth_switch_port, edge_enclosures_to_controller, edge_controller_to_storage_port, edge_eth_switch_to_eth_switch_port, edge_storage_port_to_eth_switch_port, edge_filesystem_to_hyper_scale_pool, edge_hyper_scale_pool_to_storage_pool, edge_eth_switch_port_to_eth_switch, edge_k8s_pod_to_k8s_node, edge_k8s_podgroup_to_k8s_pod, edge_k8s_vcjob_to_k8s_podgroup, edge_lun_to_controller, edge_host_to_service_network, edge_host_to_host_port, edge_host_port_to_service_network, edge_service_network_to_lun, edge_service_network_to_storage_port, edge_db_instance_to_db_node, edge_db_node_to_host,
            }, ...],
        }
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
    print(f"请求负载：{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


# ============================================================================
# action list, for CLI help
# ============================================================================

ACTIONS = {
    'alarm_list': {
        'func': alarm_list,
        'description': '查询告警信息(当前告警,可选择是否包含历史告警)',
        'params': ['alarm_id', 'severity', 'mo_dn', 'alarm_group_id', 'dc_id',
                   'product_name', 'alarm_name', 'occur_utc_start', 'occur_utc_end',
                   'fields', 'page_no', 'page_size', 'cleared', 'size', 'iterator', 'include_history'],
        'subtopic': 'alarm'
    },
    'alarm_ack': {
        'func': alarm_ack,
        'description': '确认告警',
        'params': ['csns'],
        'subtopic': 'alarm'
    },
    'alarm_unack': {
        'func': alarm_unack,
        'description': '取消确认告警',
        'params': ['csns'],
        'subtopic': 'alarm'
    },
    'alarm_clear': {
        'func': alarm_clear,
        'description': '清除告警',
        'params': ['csns'],
        'subtopic': 'alarm'
    },
    'diagnose_task_create': {
        'func': diagnose_task_create,
        'description': '创建智能分析任务',
        'params': ['object_ids', 'object_type', 'begin_time', 'end_time', 'analysis_types'],
        'subtopic': 'diagnose_task'
    },
    'diagnose_task_status': {
        'func': diagnose_task_status,
        'description': '查询性能诊断任务状态',
        'params': ['task_id'],
        'subtopic': 'diagnose_task'
    },
    # performance subtopic action
    'performance_create_collect_task': {
        'func': performance_create_collect_task,
        'description': '创建性能文件收集任务',
        'params': ['begin_time', 'end_time', 'object_type_id', 'object_ids', 'indicator_ids'],
        'subtopic': 'performance'
    },
    'performance_download_collect_result': {
        'func': performance_download_collect_result,
        'description': '下载性能文件',
        'params': ['task_id'],
        'subtopic': 'performance'
    },
    'performance_query': {
        'func': performance_query,
        'description': '查询历史性能数据',
        'params': ['obj_type_id', 'indicator_ids', 'obj_ids', 'obj_type', 'indicators', 'ext_dimensions', 'interval', 'range', 'begin_time', 'end_time'],
        'subtopic': 'performance'
    },
    'performance_show_indicators': {
        'func': performance_show_indicators,
        'description': '显示监控指标详细信息',
        'params': ['indicators'],
        'subtopic': 'performance'
    },
    'performance_list_indicators': {
        'func': performance_list_indicators,
        'description': '列出监控对象类型支持的监控指标',
        'params': ['obj_type_id'],
        'subtopic': 'performance'
    },
    'performance_list_object_types': {
        'func': performance_list_object_types,
        'description': '获取所有监控对象类型',
        'params': ['filter'],
        'subtopic': 'performance'
    },
    # check_result subtopic action
    'check_result_list': {
        'func': check_result_list,
        'description': '查询检查策略异常检查结果列表',
        'params': ['object_name', 'level', 'object_ids', 'object_native_id', 'object_type', 'policy_id', 'policy_name', 'policy_types', 'cause', 'alarm_type', 'first_occur_time', 'last_occur_time', 'page_no', 'page_size', 'sort_key', 'sort_dir'],
        'subtopic': 'check_result'
    },
    'check_result_show': {
        'func': check_result_show,
        'description': '查询检查策略异常检查结果详情',
        'params': ['check_result_id'],
        'subtopic': 'check_result'
    },
    # check_policy subtopic action
    'check_policy_list': {
        'func': check_policy_list,
        'description': '查询检查策略列表',
        'params': ['policy_name', 'exact_query', 'status', 'policy_type', 'policy_source', 'alarm_type', 'object_type', 'page_no', 'page_size', 'sort_key', 'sort_dir', 'administrative_status', 'policy_category', 'object_category'],
        'subtopic': 'check_policy'
    },
    'check_policy_execute': {
        'func': check_policy_execute,
        'description': '执行检查策略',
        'params': ['policy_id'],
        'subtopic': 'check_policy'
    },
    'check_policy_enable': {
        'func': check_policy_enable,
        'description': '启用检查策略',
        'params': ['policy_id'],
        'subtopic': 'check_policy'
    },
    'check_policy_disable': {
        'func': check_policy_disable,
        'description': '禁用检查策略',
        'params': ['policy_id'],
        'subtopic': 'check_policy'
    },
    'check_policy_delete': {
        'func': check_policy_delete,
        'description': '删除检查策略',
        'params': ['policy_id'],
        'subtopic': 'check_policy'
    },
    # topology subtopic action
    'topology_query_san_path': {
        'func': topology_query_san_path,
        'description': '查询 SAN 路径拓扑结构（支持 IP_SAN 和 FC_SAN）',
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
        'description': '查询拓扑图虚拟机和虚拟磁盘列表，或查询 BMS 下物理磁盘列表',
        'params': ['entry_objects', 'host_id', 'vm_name', 'page_size', 'page_no'],
        'subtopic': 'topology'
    },
    'topology_query_graph_path': {
        'func': topology_query_graph_path,
        'description': '查询拓扑图库信息（支持 NAS、K8s、DB 等业务类型）',
        'params': ['entry_res_type', 'entry_res_id', 'type', 'filter'],
        'subtopic': 'topology'
    },
    # health subtopic action
    'health_query_data': {
        'func': health_query_data,
        'description': '查询健康度相关数据（容量预测/性能预测/性能异常）',
        'params': ['type', 'object_id', 'begin_time', 'end_time', 'object_type', 'indicator'],
        'subtopic': 'health'
    },
    'health_show_score': {
        'func': health_show_score,
        'description': '查询对象健康度',
        'params': ['object_type', 'object_name', 'object_ids', 'page_no', 'page_size', 'sort_key', 'sort_dir'],
        'subtopic': 'health'
    },
    'health_show_detail': {
        'func': health_show_detail,
        'description': '查询健康维度的扣分详情',
        'params': ['object_id', 'object_type', 'health_dimension'],
        'subtopic': 'health'
    }
}
