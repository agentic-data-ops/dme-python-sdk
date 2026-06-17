"""
AIOps 智能运维相关操作
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
    查询告警信息

    查询当前告警,可选择是否同时查询历史告警.

    Args:
        client: DME API 客户端
        alarm_id: 告警 ID,支持模糊匹配
        severity: 告警级别列表,取值:critical, major, minor, warning, indeterminate, cleared
        mo_dn: 被管理对象 DN,支持 inc 操作符匹配
        alarm_group_id: 告警组 ID
        dc_id: 数据中心 ID
        product_name: 产品名称
        alarm_name: 告警名称,支持模糊匹配
        occur_utc_start: 告警发生开始时间(毫秒时间戳)
        occur_utc_end: 告警发生结束时间(毫秒时间戳)
        fields: 指定返回的字段列表
        page_no: 分页查询的起始页码,默认 1
        page_size: 每页数量,1~1000,默认 100(当前告警查询用)
        cleared: 是否已清除,true/false(历史告警查询用)
        size: 返回的结果集最大条数,1~1000,默认 100(历史告警查询用)
        iterator: 迭代子,首次查询无需传入,后续查询使用上次返回的 iterator(历史告警查询用)
        include_history: 开关参数,指定则同时查询历史告警

    Returns:
        {
            current_alarms: 当前告警列表 (List<AlarmInfo>)。参数格式如下：[{
                alarm_id: 告警ID (string),
                alarm_name: 告警名称 (string),
                severity: 告警级别 (string),
                status: 状态 (string),
            }, ...],
            total: 告警总数 (integer),
        }
    """
    result = {
        'current_alarms': None,
        'history_alarms': None
    }

    # 查询当前告警(默认总是查询)
    current_url = "/rest/alarmmgmt/v1/alarms/current-alarm/query"
    current_params = _build_current_alarm_params(
        alarm_id=alarm_id, severity=severity, mo_dn=mo_dn,
        alarm_group_id=alarm_group_id, dc_id=dc_id, product_name=product_name,
        alarm_name=alarm_name, occur_utc_start=occur_utc_start,
        occur_utc_end=occur_utc_end, fields=fields, page_size=page_size
    )

    current_response = client.post(current_url, body=current_params)
    result['current_alarms'] = current_response

    # 如果指定了 include_history,同时查询历史告警
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
    确认告警

    对指定告警执行确认 (ACK) 操作.

    Args:
        client: DME API 客户端
        csns: 告警流水号列表(必选),最多 30 个

    Returns:
        操作结果
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
    取消确认告警

    对指定告警执行取消确认 (UNACK) 操作.

    Args:
        client: DME API 客户端
        csns: 告警流水号列表(必选),最多 30 个

    Returns:
        操作结果
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
    清除告警

    对指定告警执行清除 (CLEAR) 操作.

    Args:
        client: DME API 客户端
        csns: 告警流水号列表(必选),最多 30 个

    Returns:
        操作结果
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
    创建智能分析任务

    Args:
        client: DME API 客户端
        object_ids: 入口分析对象 ID 列表(必选),数组大小:1~50
        object_type: 入口对象类型(必选),取值范围:
            - VM: 虚拟机
            - STORAGE_HOST: 存储主机
            - STORAGE_DEVICE: 存储设备
            - LUN: LUN
            - FILE_SYSTEM: 文件系统
            - VBS_CLIENT: VBS 客户端
            - DATATURBO: 并行客户端
            - STORAGE_POOL: 存储池
            - IP_CLIENT: IP 客户端
            - HOST_GROUP: 存储主机组
            - FC_PORT: FC 端口
            - ETH_PORT: 以太端口
            - LUN_GROUP: LUN 组
            - LOGIC_PORT: 逻辑端口
            - CONTROLLER: 控制器
            - NAMESPACE: 命名空间
        begin_time: 分析开始时间(必选),Unix 时间戳(毫秒),必须为整分钟时间点,支持最近七天内的诊断
        end_time: 分析结束时间(必选),Unix 时间戳(毫秒),必须为整分钟时间点
                  分析时间间隔范围必须大于 30 分钟,小于 24 小时
        analysis_types: 智能分析类型列表(必选),数组大小:1~4,取值范围:
            - highLatency: 高时延
            - healthAnalysis: 健康快检
            - IOInterrupt: IO 中断
            - highReadLatency: 高读时延
            - highWriteLatency: 高写时延
            - trafficAnalysis: 流量分析
            - cpuUsageAnalysis: cpu 消耗分析

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }，包含:
        - total: 智能分析任务总数
        - data: 智能分析任务响应结果列表，每项包含:
            - id: 任务 ID
            - analysis_type: 分析类型
            - error_msg: 错误信息
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
    print(f"请求负载:{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


# ============ Performance 性能监控子主题函数 ============


def performance_create_collect_task(client: DMEAPIClient, begin_time: int, end_time: int,
                        object_type_id: str, object_ids: list,
                        indicator_ids: list) -> dict:
    """
    创建性能文件收集任务

    收集范围为开始日期到结束日期的性能文件,只支持收集 7 天内的数据,
    每次传入的对象乘以指标数不超过 2000.

    Args:
        client: DME API 客户端
        begin_time: 开始时间(必填,Unix 时间戳毫秒)
        end_time: 结束时间(必填,Unix 时间戳毫秒)
        object_type_id: 对象类型 ID(必填,1~32 个字符)
        object_ids: 对象 ID 列表(必填,最多 2000 个,ID 长度 1~32 位)
        indicator_ids: 指标 ID 列表(必填,最多 20 个,ID 长度 1~16 位)

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
        client: DME API 客户端
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
    查询历史性能数据

    根据传入参数中的"range"字段所取的枚举值或从开始到结束时间范围内的查询数据.
    有汇聚数据情况下,返回结果序列是平均值序列,并包含最大值,最小值以及对应时间戳.

    使用说明:
    - 对象类型和指标定义:从性能指标模型文档获取 (reference/dme_performance_model/index.md)
    - 对象 ID (CMDB 实例 ID) 获取步骤:
      1. 运行 `cmdb instance list --help` 查看帮助,了解类定义和查询方式
      2. 根据帮助信息,从 CMDB 资源模型中确定要查询的资源类型 (Class 名称)
      3. 使用 `cmdb instance list --class_name <Class 名称>` 查询实例列表
      4. 从返回结果中获取对应资源的 instance_id (即 obj_ids 参数)

    Args:
        client: DME API 客户端
        obj_type_id: 监控对象类型标识(必填),对应监控对象类型 ID
                     从性能指标模型文档获取:reference/dme_performance_model/index.md
        indicator_ids: 监控指标标识列表(必填,最多 100 个),对应指标 ID
                       从性能指标模型文档获取:reference/dme_performance_model/index.md
        obj_ids: 监控对象标识列表(必填,最多 512 个),对应 CMDB 实例 ID
                 获取方式:
                 1. 运行 `cmdb instance list --help` 查看帮助,了解类定义
                 2. 根据帮助确定要查询的资源类型 (Class 名称)
                 3. 运行 `cmdb instance list --class_name <Class 名称>` 查询实例
                 4. 从返回结果中获取 instance_id
        obj_type: 监控对象类型(可选,1~512 个字符)
        indicators: 监控指标列表(可选,最多 100 个)
        ext_dimensions: 扩展维度信息列表(可选,最多 100 个)
        interval: 间隔粒度(可选)
                  取值范围:ONE_MINUTE(1 分钟), MINUTE(5 分钟), HALF_HOUR(30 分钟),
                  HOUR(1 小时), DAY(1 天), WEEK(1 周), MONTH(1 个月)
        range: 时间范围(可选,默认 LAST_1_HOUR)
               取值范围:LAST_5_MINUTE(最近 5 分钟), LAST_1_HOUR(最近 1 小时),
               LAST_1_DAY(最近 1 天), LAST_1_WEEK(最近 1 周), LAST_1_MONTH(最近 1 个月),
               LAST_1_QUARTER(最近 3 个月), HALF_1_YEAR(最近半年), LAST_1_YEAR(最近 1 年),
               BEGIN_END_TIME(自行设置开始和结束时间), INVALID(无效值)
        begin_time: 查询开始时刻(可选),仅 range 为 BEGIN_END_TIME 时生效,必须比 end_time 小
        end_time: 查询结束时刻(可选),仅 range 为 BEGIN_END_TIME 时生效,必须比 begin_time 大

    Returns:
        {
            status_code: 状态码 (int32),
            error_code: 错误码 (int32),
            error_msg: 错误消息 (string),
            data: 性能数据 (Map<object, Map<object, HistoryPerfData>>),
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
    显示监控指标详细信息

    Args:
        client: DME API 客户端
        indicators: 监控对象指标标识列表(必填,最多 1000 个字符)
                   可以是整数列表或字符串列表,如 [123, 456] 或 ["123", "456"]

    Returns:
        {
            status_code: 状态码 (int32),
            error_code: 错误码 (int32),
            error_msg: 错误消息 (string),
            data: 监控指标映射 (Map<object, SimpleIndicator>),
        }
    """
    url = "/rest/metrics/v1/mgr-svc/indicators"

    # 确保 indicators 是整数列表
    if indicators:
        indicators = [int(i) for i in indicators]

    # API 要求直接传递数组,而不是对象
    response = client.post(url, body=indicators)
    return response


def performance_list_indicators(client: DMEAPIClient, obj_type_id: int) -> dict:
    """
    列出监控对象类型支持的监控指标

    Args:
        client: DME API 客户端
        obj_type_id: 监控对象类型标识(必填)

    Returns:
        监控指标信息,包含 indicator_ids 列表
    """
    url = "/rest/metrics/v1/mgr-svc/obj-types/{obj_type_id}/indicators"

    response = client.get(url, params={"obj_type_id": obj_type_id})
    return response


def performance_list_object_types(client: DMEAPIClient, filter: str = None) -> dict:
    """
    获取所有监控对象类型

    Args:
        client: DME API 客户端
        filter: 过滤关键字(可选),用于模糊匹配 zh_cn 和 en_us 字段
                如果提供,仅返回匹配的对象类型

    Returns:
        {
            status_code: 状态码 (int32),
            error_code: 错误码 (int32),
            error_msg: 错误消息 (string),
            data: 监控对象类型列表 (List<ObjectTypeBody>)。参数格式如下：[{
                obj_type_id: 监控对象类型编号 (int64),
                parent_obj_type_id: 父类型编号 (int64),
                resource_category: 资源CI (string),
                resource_provider: 资源提供者 (string),
                en_us: 英文描述 (string),
                zh_cn: 中文描述 (string),
            }, ...],
        }
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
    查询健康度相关数据

    查询容量预测、性能预测、性能异常等健康度相关数据。

    Args:
        client: DME API 客户端
        type: 数据类型（必选），可选值：capacity_prediction（容量预测）, performance_prediction（性能预测）, performance_anomaly（性能异常）
        object_id: 资源 ID（必选，1~256 个字符）
        begin_time: 开始时间（必选），自 1970 年 1 月 1 日（00:00:00GMT）至当前时间的毫秒数
        end_time: 结束时间（必选），自 1970 年 1 月 1 日（00:00:00GMT）至当前时间的毫秒数
        object_type: 资源类型（必选）
        indicator: 资源类型所对应的指标（capacity_prediction 和 performance_prediction 必选）

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }，包含查询结果
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
    查询对象健康度

    查询指定类型对象的健康度信息。

    Args:
        client: DME API 客户端
        object_type: 对象类型（必选）
                    可选值：storage（存储设备）, storage_pool（存储池）, storage_host（存储主机）,
                           storage_disk（硬盘）, storage_port（存储端口）, fcswitch_port（光纤交换机端口）,
                           storage_file_system（文件系统）, controller（控制器）, replication_cg（远程复制一致性组）,
                           volume（LUN）, tier（服务等级）, datastore（数据存储）, virtual_machine（虚拟机）,
                           storage_name_space（命名空间）, storage_node（存储节点）, dpc（并行客户端）
        object_name: 对象名称，支持模糊查询（可选，最多 256 个字符）
        object_ids: 对象 resId 列表，用于批量精确查找（可选，最多支持 100 个 ID）
        page_no: 分页查询的起始位置（可选，最小值：1）
        page_size: 每页显示的数量（可选，1~100，默认 20）
        sort_key: 排序字段（可选），按分数进行排序，可选值：health_score
        sort_dir: 排序方式（可选），可选值：asc, desc

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }，包含对象健康度列表
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
    查询健康维度的扣分详情

    查询指定对象在指定健康维度下的扣分详情。

    Args:
        client: DME API 客户端
        object_id: 对象 Id（必选，1~128 个字符）
        object_type: 对象类型（必选）
                    可选值：storage, storage_pool, storage_host, storage_disk, storage_port,
                           fcswitch_port, storage_file_system, controller, replication_cg, volume,
                           tier, datastore, virtual_machine, storage_name_space, storage_node,
                           dpc, gfs, dpc_client, vbs_client
        health_dimension: 健康维度（必选）
                        可选值：alarm（告警）, performance_anomaly（性能异常）,
                              performance_prediction（性能预警）, capacity_prediction（容量预警）

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
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



# ============ Performance 性能监控子主题函数 ============




def diagnose_task_status(client: DMEAPIClient, task_id: str) -> dict:
    r"""
    查询性能诊断任务状态

    根据任务 ID 查询诊断任务状态.

    Args:
        client: DME API 客户端
        task_id: 任务 ID(必选),1~128 个字符

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        },包含:
        - task_id: 任务 ID
        - task_status: 任务状态,取值范围:
            - executing: 执行中
            - failed: 失败
            - success: 成功
            - waiting: 等待
            - terminated: 已终止
        - task_result: 任务结果,取值范围:
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
    查询检查策略列表

    Args:
        client: DME API 客户端
        policy_name: 策略名称（支持模糊查询，1~256 个字符）
        exact_query: 名称是否精确查询（true-精确查询，false-模糊查询），默认 false
        status: 策略状态（normal-正常，checking-检查中，failed-检查失败，queuing-排队中）
        policy_type: 策略类型（performance-性能阈值，capacity-容量阈值，availability-可用性，
                    configuration-配置，recyclable-可回收资源，lowload-低负载资源，
                    performance_anomaly-性能异常，performance_prediction-性能预警，
                    capacity_prediction-容量预警，history_performance-历史性能，
                    load_imbalance-负载失衡，highload-高负载资源）
        policy_source: 来源（pre-define-预置，user-define-自定义）
        alarm_type: 告警类型（violation-异常，alarm-告警，event-事件）
        object_type: 对象类型（storage-存储，lun-逻辑单元，host-主机等）
        page_no: 分页查询的页码，1~1000，默认 1
        page_size: 分页查询的个数，1~100，默认 20
        sort_key: 排序字段（last_check_time-最后检查时间，failed_count-检查不通过的对象个数）
        sort_dir: 排序方式（asc-正序，desc-降序）
        administrative_status: 管理状态（enable-启用，disable-禁用）
        policy_category: 检查分类（configuration-配置，performance-性能，capacity-容量，faults-故障，optimization-优化）
        object_category: 对象分类（Storage-存储设备，IPSwitch-以太网交换机，FCSwitch-光纤交换机，
                       Virtualization-虚拟化，Server-服务器，HCI-超融合，Client-客户端）

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }，包含 total（总数）和 policies（策略列表）
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

    执行指定的检查策略。

    Args:
        client: DME API 客户端
        policy_id: 策略 ID（1~64 个字符）

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
    url = "/rest/policymgmt/v1/policies/{policy_id}/execute"

    response = client.post(url, params={"policy_id": policy_id})
    return response


def check_policy_enable(client: DMEAPIClient, policy_id: str) -> dict:
    """
    启用检查策略

    启用指定的检查策略。

    Args:
        client: DME API 客户端
        policy_id: 策略 ID（1~64 个字符）

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
    url = "/rest/policymgmt/v1/policies/{policy_id}/enable"

    response = client.post(url, params={"policy_id": policy_id})
    return response


def check_policy_disable(client: DMEAPIClient, policy_id: str) -> dict:
    """
    禁用检查策略

    禁用指定的检查策略。

    Args:
        client: DME API 客户端
        policy_id: 策略 ID（1~64 个字符）

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
    url = "/rest/policymgmt/v1/policies/{policy_id}/disable"

    response = client.post(url, params={"policy_id": policy_id})
    return response


def check_policy_delete(client: DMEAPIClient, policy_id: str) -> dict:
    """
    删除检查策略

    删除指定的检查策略。

    Args:
        client: DME API 客户端
        policy_id: 策略 ID（1~64 个字符）

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }
    """
    url = "/rest/policymgmt/v1/policies/{policy_id}"

    response = client.delete(url, params={"policy_id": policy_id})
    return response


# ============================================================================
# 检查结果 (check_result) 子主题函数
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
    查询检查策略异常检查结果列表

    查询检查策略的异常检查结果，支持多种过滤条件和分页查询。

    Args:
        client: DME API 客户端
        object_name: 对象名称（支持模糊查询，1~256 个字符）
        level: 异常级别（critical-紧急，major-重要，minor-次要，info-提示）
        object_ids: 对象 ID 列表（最多 100 个）
        object_native_id: 对象 nativeId（1~384 个字符）
        object_type: 对象类型（storage-存储，lun-逻辑单元，host-主机等）
        policy_id: 策略 ID（精确查询，1~64 个字符）
        policy_name: 策略名称（支持模糊查询，1~256 个字符）
        policy_types: 策略类型列表（最多 30 个）
        cause: 异常原因（支持模糊查询，1~768 个字符）
        alarm_type: 告警类型（violation-异常，alarm-告警，event-事件）
        first_occur_time: 第一次异常时间范围（{beginTime, endTime}，UTC 时间戳，单位 ms）
        last_occur_time: 最后一次异常时间范围（{beginTime, endTime}，UTC 时间戳，单位 ms）
        page_no: 分页查询的页码，1~10000，默认 1
        page_size: 分页查询的个数，1~2000，默认 20
        sort_key: 排序字段（violation_count-异常次数）
        sort_dir: 排序方式（asc-正序，desc-降序）

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }，包含 total（总数）和 results（异常检查结果列表）
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
    查询检查策略异常检查结果详情

    查询指定检查结果的详细信息。

    Args:
        client: DME API 客户端
        check_result_id: 检查结果 ID（1~64 个字符）

    Returns:
        {
            task_id: 任务ID (string, 1~64个字符),
        }，包含检查结果的详细信息
    """
    url = "/rest/policymgmt/v1/abnormal-check-results/{check_result_id}"

    response = client.get(url, params={"check_result_id": check_result_id})
    return response


# 动作列表，用于 CLI 帮助
# ============================================================================
# 拓扑管理 (topology) 子主题函数
# ============================================================================

def topology_query_luns(client: DMEAPIClient, entry_objects: list, storage_pool_id: str,
               lun_name: str = None, san_type: str = None, page_size: int = 20, page_no: int = 1) -> dict:
    r"""
    查询拓扑图 LUN 列表

    根据指定入口对象和存储池查询 LUN 列表。

    Args:
        client: DME API 客户端
        entry_objects: 入口对象列表（List<LunTopoQueryEntryObject>，必选，数组最大成员个数: 5）。参数格式如下：[{
                id: 入口对象 id（必选，string，1~128 个字符）,
                type: 入口对象类型（必选，string）。可选值：host（物理主机），storage（闪存存储/分布式存储），host_group（主机组），lun（LUN），vm（虚拟机），datastore（数据存储），application（应用），switch_port（光纤交换机端口），storage_pool（存储池）。注意：ip_san 时不支持 datastore/application/switch_port；入口对象为 vm/storage_pool 时最多支持 5 个，其余类型只支持 1 个,
            }, ...]
        storage_pool_id: 所属存储池 ID（必选，string，1~128 个字符）。格式为 {storageId}STORAGE_POOL{poolId}，如 "b9326bbf-...STORAGE_POOL163BECEA..."，从 storage pool list 返回的 id 字段获取
        san_type: 存储区域网络类型（可选，string）。可选值：ip_san，fc_san
        lun_name: LUN 名称（可选，string，1~256 个字符），支持模糊查询
        page_size: 分页查询的个数（可选，int32，1~20），默认 20
        page_no: 分页查询的起始位置（可选，int32，1~2147483647），默认 1

    Returns:
        {
            total: LUN 查询结果总数 (int32),
            luns: LUN 查询结果列表 (List<LunObject>)。参数格式如下：[{
                id: LUN id (string, 1~128个字符),
                name: LUN 名称 (string, 1~256个字符),
                datastore: LUN 对应数据存储列表 (List<LunsQueryDataStoreItem>)。属性格式如下：[{
                    id: 数据存储 id (string, 1~128个字符),
                    name: 数据存储名称 (string, 1~256个字符),
                    storage_type: 存储类型 (string)。可选值：vmfs（虚拟机文件系统）,
                    vr_type: 虚拟化类型 (string)。可选值：vmware, hcs,
                }, ...],
                is_replication_member: 是否是复制卷 (boolean, true/false),
                is_replication_primary: 是否是复制卷本端 (boolean, true/false),
                is_hyper_metro_member: 是否是保护卷 (boolean, true/false),
                is_hyper_metro_primary: 是否是保护卷本端 (boolean, true/false),
                storage_pool_id: 存储池 ID (string, 1~140个字符)。格式为 {storageId}STORAGE_POOL{poolId},
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
    查询 SAN 路径拓扑结构

    根据指定入口对象查询 SAN 网络中从主机到存储池之间的拓扑结构。
    支持 IP_SAN 和 FC_SAN 两种类型。

    Args:
        client: DME API 客户端
        entry_objects: 入口对象列表（必选，数组最大成员个数: 1）。FC_SAN 参数格式如下：[{
                id: 入口对象 id（必选，string，1~128 个字符）,
                type: 入口对象类型（必选，string）。可选值：host（主机），storage（闪存存储设备），lun（LUN），host_group（主机组），vm（虚拟机），datastore（数据存储），application（应用），switch_port（光纤交换机端口），storage_pool（存储池）,
            }, ...]。IP_SAN 参数格式如下：[{
                id: 入口对象 id（必选，string，1~128 个字符）,
                type: 入口对象类型（必选，string）。可选值：host（主机），storage（闪存存储或分布式存储），lun（LUN），host_group（主机组），vm（虚拟机），storage_pool（存储池）。注：IP_SAN 不支持 datastore/application/switch_port 类型，最多支持 5 个对象,
            }, ...]
        san_type: SAN 类型（可选，string）。可选值：ip_san, fc_san
                  - 不指定时，同时调用 IP_SAN 和 FC_SAN 两个 API，组合返回数据
                  - 指定为 ip_san 时，仅调用 IP_SAN API
                  - 指定为 fc_san 时，仅调用 FC_SAN API

    Returns:
        当 san_type=fc_san 或不指定时（FC_SAN 部分）：
        {
            fabrics: Fabric 列表 (List<HostToStoragePoolFabric>)。参数格式如下：[{
                id: Fabric id (string, 1~64个字符),
                name: Fabric 名称 (string, 1~128个字符),
                switches: 交换机列表 (List<SwitchItem>)。属性格式如下：[{
                    id: 交换机节点 id (string, 1~64个字符),
                    name: 交换机节点名称 (string, 1~128个字符),
                    ports: 交换机端口列表 (List<SwitchPortItem>)。属性格式如下：[{
                        id: 交换机端口节点 id (string, 1~64个字符),
                        name: 交换机端口节点名称 (string, 1~128个字符),
                        status: 交换机端口状态 (string)。可选值：normal（正常），abnormal（故障），unknown（未知）,
                    }, ...],
                }, ...],
                port_links: 交换机端口链路列表 (List<PortLinkItem>)。属性格式如下：[{
                    left_port: 左端口 (PortNodeItem)。属性格式如下：{
                        id: 端口 Id (string, 1~64个字符),
                        type: 端口类型 (string)。可选值：host_port, switch_port, storage_port,
                    },
                    right_port: 右端口 (PortNodeItem),
                }, ...],
                switch_links: 交换机连接关系列表 (List<SwitchLinkItem>)。属性格式如下：[{
                    host_to_switch_id: 主机连接的交换机 ID (string, 1~64个字符),
                    storage_to_switch_id: 存储连接的交换机 ID (string, 1~64个字符),
                }, ...],
            }, ...],
            hosts: 主机列表 (List<HostToStoragePoolHost>)。属性格式如下：[{
                id: 主机 id (string, 1~64个字符),
                name: 主机名称 (string, 1~256个字符),
                access_mode: 接入模式 (string)。可选值：vcenter, none,
                host_groups: 主机组列表 (List<HostToStoragePoolHostGroup>),
                ports: 主机端口列表 (List<HostToStoragePoolPort>),
                deployment_type: 部署类型 (string)。可选值：BMS（裸金属服务器），ECS（ECS主机）,
                direct_storage_ids: 主机直连的存储设备 ID 列表 (List<string>),
            }, ...],
            storages: 存储列表 (List<HostToStoragePoolStorage>)。属性格式如下：[{
                id: 存储 id (string, 1~64个字符),
                name: 存储名称 (string, 1~128个字符),
                product_model: 存储设备类型 (string),
                controllers: 控制器列表 (List<HostToStoragePoolController>),
                pools: 存储池列表 (List<HostToStoragePoolPool>),
                disks: 存储磁盘列表 (List<HostToStorageDiskDisks>),
            }, ...],
        }
        当 san_type=ip_san 时（IP_SAN）：
        {
            switches: 交换机列表 (List<SwitchItem>),
            hosts: 主机列表 (List<HostToStoragePoolHost>),
            storages: 存储列表 (List<HostToStoragePoolStorage>),
            switch_links: 交换机连接关系列表 (List<SwitchLinkItem>),
        }
        当 san_type=None 时：
        {
            ip_san: { IP_SAN 返回数据 },
            fc_san: { FC_SAN 返回数据 },
        }
    """
    result = {}

    # 如果未指定 san_type，同时调用两个 API
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

    # 如果指定了 san_type，只调用对应的 API
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
    查询拓扑图虚拟机和虚拟磁盘列表，或查询 BMS 下物理磁盘列表

    根据指定入口对象查询虚拟化资源。

    Args:
        client: DME API 客户端
        entry_objects: 入口对象列表（List<VmTopoQueryEntryObject>，必选，数组最大成员个数: 5）。参数格式如下：[{
                id: 入口对象 id（必选，string，1~128 个字符）,
                type: 入口对象类型（必选，string）。可选值：vm（虚拟机），host_group（主机组），host（主机），storage（闪存存储或分布式存储），lun（LUN），datastore（数据存储），switch_port（光纤交换机端口），storage_pool（存储池）,
            }, ...]
        host_id: 主机 ID（必选，string，0~128 个字符）
        vm_name: 虚拟机名称搜索参数（可选，string，0~256 个字符），支持模糊匹配
        page_size: 分页查询的个数（可选，int32，1~20），默认 20
        page_no: 分页查询的起始位置（可选，int32，1~2147483647），默认 1

    Returns:
        {
            total: vms 查询结果总数 (int32),
            vms: vm 查询结果列表 (List<VirtualMachine>)。参数格式如下：[{
                id: id (string, 1~64个字符),
                name: vm 名称 (string, 1~128个字符),
                ip: vm ip (string, 1~3072个字符),
                host_id: 物理主机 ID (string, 1~64个字符),
                vr_type: 虚拟化类型 (string)。可选值：vmware, hcs,
                vdisks: 虚拟盘列表 (List<VirtualDisk>)。属性格式如下：[{
                    id: vdisk id (string, 1~64个字符),
                    name: vdisk 名称 (string, 1~128个字符),
                }, ...],
            }, ...],
            disks: 物理主机关联的物理磁盘列表 (List<PhysicalDisk>)。参数格式如下：[{
                id: disk id (string, 1~64个字符),
                native_id: disk native id (string, 1~768个字符),
                name: disk 名称 (string, 1~768个字符),
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
    查询拓扑图库信息

    查询拓扑图库信息，支持 NAS、K8s、DB 等业务类型。

    Args:
        client: DME API 客户端
        entry_res_type: 入口资源类型（必选，string）。可选值：storage_device（存储设备），disk（硬盘），storage_pool（存储池），hyper_scale_pool（全局池），file_system（文件系统），controller（控制器），eth_port（以太/RoCE端口），ib_port（IB端口），logic_port（逻辑端口），ip_client（IP客户端），dtree（Dtree），lun（LUN），k8s_application（容器应用），k8s_workload（工作负载），k8s_pod（容器组），k8s_pvc（持久卷申领），k8s_pv（持久卷），k8s_cluster（容器集群），k8s_node（容器节点），k8s_vc_job（Volcano Job），data_turbo_client（DataTurbo客户端），enclosures（机框），eth_switch（交换机），storage_zone（存储zone），service_network（业务网络），db_instance（高斯数据库实例），db_node（高斯数据库节点）
        entry_res_id: 入口资源 ID（必选，string，1~256 个字符）
        type: 业务类型（可选，string）。可选值：nas, k8s, db
        filter: 条件过滤列表（可选，List<TopoFilter>，数组最大成员个数: 10）。参数格式如下：[{
                type: 拓扑查询返回资源类型 (可选, string)。可选值与 entry_res_type 相同,
                key: 字段名称 (可选, string, 1~256个字符)。如 id, name, ip,
                value: 字段值 (可选, string, 0~256个字符),
                operator: 比较方式 (可选, string)。可选值：lt（小于），le（小于等于），eq（等于），gt（大于），ge（大于等于），ne（不等于），contains（包含）,
            }, ...]

    Returns:
        {
            nodes: 节点列表 (List<NodeItem>)。参数格式如下：[{
                id: 节点对象 ID (string, 1~256个字符),
                type: 拓扑查询返回资源类型 (string)。可选值：storage_device, disk, storage_pool, hyper_scale_pool, file_system, controller, eth_port, ib_port, logic_port, ip_client, dtree, lun, k8s_application, k8s_workload, k8s_pod, k8s_pvc, k8s_pv, k8s_cluster, k8s_node, k8s_vc_job, k8s_pod_group, data_turbo_client, enclosures, eth_switch, storage_zone, service_network, db_instance, db_node, host, host_port, storage_port,
                label: 节点对象名称 (string, 1~256个字符),
                sub_type: 工作负载类型 (string, 仅 k8s_workload 时)。可选值：deployment, replica_set, stateful_set, daemon_set, job, cron_job,
            }, ...],
            edges: 边列表 (List<EdgeItem>)。参数格式如下：[{
                source: 起始节点 ID (string, 1~256个字符),
                target: 目标节点 ID (string, 1~256个字符),
                edge_type: 边类型 (string)。可选值：edge_k8s_node_to_k8s_pod, edge_storage_pool_to_storage_disk, edge_filesystem_to_storage_pool, edge_storage_disk_to_storage_device, edge_k8s_pvc_to_k8s_pv, edge_k8s_pod_to_k8s_pvc, edge_dtree_to_filesystem, edge_lun_storage_pool, edge_k8s_cluster_to_k8s_node, edge_k8s_pv_to_lun, edge_k8s_pv_to_dtree, edge_nas_client_to_logic_port, edge_logic_port_to_ethernet_port, edge_ethernet_port_to_controller, edge_controller_to_filesystem, edge_data_turbo_client_to_logic_port, edge_controller_to_ethernet_port, edge_data_turbo_client_to_service_network, edge_ethernet_port_to_eth_switch_port, edge_service_network_to_logic_port, edge_a800_enclosures_to_storage_zone, edge_controller_to_enclosures, edge_storage_zone_to_filesystem, edge_eth_switch_port_to_eth_switch_port, edge_enclosures_to_controller, edge_controller_to_storage_port, edge_eth_switch_to_eth_switch_port, edge_storage_port_to_eth_switch_port, edge_filesystem_to_hyper_scale_pool, edge_hyper_scale_pool_to_storage_pool, edge_eth_switch_port_to_eth_switch, edge_k8s_pod_to_k8s_node, edge_k8s_podgroup_to_k8s_pod, edge_k8s_vcjob_to_k8s_podgroup, edge_lun_to_controller, edge_host_to_service_network, edge_host_to_host_port, edge_host_port_to_service_network, edge_service_network_to_lun, edge_service_network_to_storage_port, edge_db_instance_to_db_node, edge_db_node_to_host,
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
# 动作列表，用于 CLI 帮助
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
    # performance 子主题动作
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
    # check_result 子主题动作
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
    # check_policy 子主题动作
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
    # topology 子主题动作
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
    # health 子主题动作
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
