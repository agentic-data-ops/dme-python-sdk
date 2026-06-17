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
    """Build current alarm query parameters"""
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
    """Build history alarm query parameters"""
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
        alarm_id: alarm ID, supports fuzzy match
        severity: severity list, valid values: critical, major, minor, warning, indeterminate, cleared
        mo_dn: managed object DN, supports inc operator match
        alarm_group_id: alarm group ID
        dc_id: data center ID
        product_name: product name
        alarm_name: alarm name, supports fuzzy match
        occur_utc_start: alarm start time (millisecond timestamp)
        occur_utc_end: alarm end time (millisecond timestamp)
        fields: specified return field list
        page_no: pagination start page, default 1
        page_size: items per page, 1~1000, default 100 (for current alarm query)
        cleared: whether cleared, true/false (for history alarm query)
        size: max result set size, 1~1000, default 100 (for history alarm query)
        iterator: iterator, not needed for first query, use the returned iterator from previous query (for history alarm query)
        include_history: toggle parameter, if set, also query history alarms

    Returns:
        {
            current_alarms: current alarm list (List<AlarmInfo>). parameter format: [{
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

    # Query current alarm (always queried by default)
    current_url = "/rest/alarmmgmt/v1/alarms/current-alarm/query"
    current_params = _build_current_alarm_params(
        alarm_id=alarm_id, severity=severity, mo_dn=mo_dn,
        alarm_group_id=alarm_group_id, dc_id=dc_id, product_name=product_name,
        alarm_name=alarm_name, occur_utc_start=occur_utc_start,
        occur_utc_end=occur_utc_end, fields=fields, page_size=page_size
    )

    current_response = client.post(current_url, body=current_params)
    result['current_alarms'] = current_response

    # If include_history is specified, also query history alarms
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
        csns: alarm serial number list (Required), up to 30

    Returns:
        operation result
    """
    url = "/rest/alarmmgmt/v1/alarms/operation"

    if not isinstance(csns, list) or len(csns) < 1 or len(csns) > 30:
        raise ValueError("csns must be a list of 1-30 elements")

    payload = {
        "csns": csns,
        "operation_type": "ACK"
    }

    print(f"Request URL: {url}")
    print(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


def alarm_unack(client: DMEAPIClient, csns: list) -> dict:
    r"""
    Un-acknowledge alarm

    Un-acknowledge (UNACK) the specified alarms.

    Args:
        client: DME API client
        csns: alarm serial number list (Required), up to 30

    Returns:
        operation result
    """
    url = "/rest/alarmmgmt/v1/alarms/operation"

    if not isinstance(csns, list) or len(csns) < 1 or len(csns) > 30:
        raise ValueError("csns must be a list of 1-30 elements")

    payload = {
        "csns": csns,
        "operation_type": "UNACK"
    }

    print(f"Request URL: {url}")
    print(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


def alarm_clear(client: DMEAPIClient, csns: list) -> dict:
    r"""
    Clear alarm

    Clear (CLEAR) the specified alarms.

    Args:
        client: DME API client
        csns: alarm serial number list (Required), up to 30

    Returns:
        operation result
    """
    url = "/rest/alarmmgmt/v1/alarms/operation"

    if not isinstance(csns, list) or len(csns) < 1 or len(csns) > 30:
        raise ValueError("csns must be a list of 1-30 elements")

    payload = {
        "csns": csns,
        "operation_type": "CLEAR"
    }

    print(f"Request URL: {url}")
    print(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


def diagnose_task_create(client: DMEAPIClient, object_ids: list, object_type: str,
                         begin_time: int, end_time: int, analysis_types: list) -> dict:
    r"""
    Create intelligent analysis task

    Args:
        client: DME API client
        object_ids: entry analysis object ID list (Required), array size: 1~50
        object_type: entry object type (Required), valid values: 
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
        begin_time: analysis start time (Required), Unix timestamp (milliseconds), must be a whole minute time point, supports diagnosis within the last 7 days
        end_time: analysis end time (Required), Unix timestamp (milliseconds), must be a whole minute time point
                  analysis time interval must be greater than 30 minutes and less than 24 hours
        analysis_types: intelligent analysis type list (Required), array size: 1~4, valid values: 
            - highLatency: High latency
            - healthAnalysis: Health quick check
            - IOInterrupt: IO interrupt
            - highReadLatency: High read latency
            - highWriteLatency: High write latency
            - trafficAnalysis: Traffic analysis
            - cpuUsageAnalysis: CPU consumption analysis

    Returns:
        {
            total: total intelligent analysis tasks (int32, 0~4),
            data: intelligent analysis task response result list (List<ResponseTaskInfoOpenapi>). parameter format: [{
                    id: task ID (string, 1~32 characters),
                    analysis_type: intelligent analysis type enum (string). valid values: highLatency (High latency), healthAnalysis (Health quick check), IOInterrupt (IO interrupt), highReadLatency (High read latency), highWriteLatency (High write latency), trafficAnalysis (Traffic analysis), cpuUsageAnalysis (CPU consumption analysis),
                    error_msg: error info (string, 1~1024 characters),
                    is_succeed: whether created successfully (boolean). valid values: true (created successfully), false (creation failed),
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

    print(f"Request URL: {url}")
    print(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


# ============ Performance monitoring subtopic functions ============


def performance_create_collect_task(client: DMEAPIClient, begin_time: int, end_time: int,
                        object_type_id: str, object_ids: list,
                        indicator_ids: list) -> dict:
    """
    Create performance file collection task

    Collection scope is from start date to end date, only supports collecting data within 7 days,
    the number of objects multiplied by indicators per call must not exceed 2000.

    Args:
        client: DME API client
        begin_time: start time (Required, Unix timestamp milliseconds)
        end_time: end time (Required, Unix timestamp milliseconds)
        object_type_id: object type ID (Required, 1~32 characters)
        object_ids: object ID list (Required, up to 2000, ID length 1~32 characters)
        indicator_ids: indicator ID list (Required, up to 20, ID length 1~16 characters)

    Returns:
        task ID
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
        task_id: task ID (Required)

    Returns:
        performance file download link or file content
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
    Query historical performance data

    Query data based on the enum value of the "range" field or from the start to end time.
    When aggregated data exists, the returned result sequence is the average sequence, containing
    the maximum, minimum values and their corresponding timestamps.

    Usage notes:
    - Object type and indicator definitions: obtain from the performance indicator model documentation (reference/dme_performance_model/index.md)
    - Object ID (CMDB instance ID) acquisition steps:
      1. Run `cmdb instance list --help` to view help, understand class definitions and query methods
      2. Based on help info, determine the resource type (Class name) to query from the CMDB resource model
      3. Use `cmdb instance list --class_name <Class name>` to query instance list
      4. Obtain the instance_id of the corresponding resource from the returned result (i.e., the obj_ids parameter)

    Args:
        client: DME API client
        obj_type_id: monitoring object type ID (Required), corresponds to monitoring object type ID
                     obtain from the performance indicator model documentation: reference/dme_performance_model/index.md
        indicator_ids: monitoring indicator ID list (Required, up to 100), corresponds to indicator ID
                       obtain from the performance indicator model documentation: reference/dme_performance_model/index.md
        obj_ids: monitoring object ID list (Required, up to 512), corresponds to CMDB instance ID
                 acquisition method:
                 1. Run `cmdb instance list --help` to view help, understand class definitions
                 2. Determine the resource type (Class name) to query based on help
                 3. Run `cmdb instance list --class_name <Class name>` to query instances
                 4. Obtain instance_id from the returned result
        obj_type: monitoring object type (Optional, 1~512 characters)
        indicators: monitoring indicator list (Optional, up to 100)
        ext_dimensions: extended dimension info list (Optional, up to 100)
        interval: interval granularity (Optional)
                  valid values: ONE_MINUTE(1 minute), MINUTE(5 minutes), HALF_HOUR(30 minutes),
                  HOUR(1 hour), DAY(1 day), WEEK(1 week), MONTH(1 month)
        range: time range (Optional, default LAST_1_HOUR)
               valid values: LAST_5_MINUTE(last 5 minutes), LAST_1_HOUR(last 1 hour),
               LAST_1_DAY(last 1 day), LAST_1_WEEK(last 1 week), LAST_1_MONTH(last 1 month),
               LAST_1_QUARTER(last 3 months), HALF_1_YEAR(last half year), LAST_1_YEAR(last 1 year),
               BEGIN_END_TIME(custom start and end time), INVALID(invalid value)
        begin_time: query start time (Optional), only effective when range is BEGIN_END_TIME, must be earlier than end_time
        end_time: query end time (Optional), only effective when range is BEGIN_END_TIME, must be later than begin_time

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
    Show monitoring indicator details

    Args:
        client: DME API client
        indicators: monitoring object indicator ID list (Required, up to 1000 characters)
                    can be integer list or string list, e.g. [123, 456] or ["123", "456"]

    Returns:
        {
            status_code: status code (int32),
            error_code: error code (int32),
            error_msg: error message (string),
            data: monitoring indicator mapping (Map<object, SimpleIndicator>),
        }
    """
    url = "/rest/metrics/v1/mgr-svc/indicators"

    # Ensure indicators is an integer list
    if indicators:
        indicators = [int(i) for i in indicators]

    # API requires passing array directly, not object
    response = client.post(url, body=indicators)
    return response


def performance_list_indicators(client: DMEAPIClient, obj_type_id: int) -> dict:
    """
    List monitoring indicators supported by the monitoring object type

    Args:
        client: DME API client
        obj_type_id: monitoring object type ID (Required)

    Returns:
        monitoring indicator info, containing indicator_ids list
    """
    url = "/rest/metrics/v1/mgr-svc/obj-types/{obj_type_id}/indicators"

    response = client.get(url, params={"obj_type_id": obj_type_id})
    return response


def performance_list_object_types(client: DMEAPIClient, filter: str = None) -> dict:
    """
    Get all monitoring object types

    Args:
        client: DME API client
        filter: filter keyword (Optional), used for fuzzy matching zh_cn and en_us fields
                If provided, only return matching object types

    Returns:
        {
            status_code: status code (int32),
            error_code: error code (int32),
            error_msg: error message (string),
            data: monitoring object type list (List<ObjectTypeBody>). parameter format: [{
                obj_type_id: monitoring object type number (int64),
                parent_obj_type_id: parent type number (int64),
                resource_category: resource CI (string),
                resource_provider: resource provider (string),
                en_us: English description (string),
                zh_cn: Chinese description (string),
            }, ...],
        }
        resource_provider, en_us, zh_cn, group_en_us, group_zh_cn and other fields
    """
    url = "/rest/metrics/v1/mgr-svc/obj-types"

    response = client.get(url)

    # If filter parameter is provided, filter results
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


# Health related functions
def health_query_data(client: DMEAPIClient, type: str, object_id: str, begin_time: int,
                      end_time: int, object_type: str, indicator: str = None) -> dict:
    """
    Query health related data

    Query capacity prediction, performance prediction, performance anomaly and other health related data.

    Args:
        client: DME API client
        type: data type (Required), valid values: capacity_prediction, performance_prediction, performance_anomaly
        object_id: resource ID (Required, 1~256 characters)
        begin_time: start time (Required), milliseconds since January 1, 1970 (00:00:00 GMT)
        end_time: end time (Required), milliseconds since January 1, 1970 (00:00:00 GMT)
        object_type: resource type (Required)
        indicator: indicator corresponding to the resource type (Required for capacity_prediction and performance_prediction)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, containing query results
    """
    if type == 'capacity_prediction':
        url = "/rest/pmmgmt/v1/prediction/query-capacity-predict"
    elif type == 'performance_prediction' or type == 'performance_predict':
        url = "/rest/pmmgmt/v1/prediction/query-performance-predict"
    elif type == 'performance_anomaly':
        url = "/rest/metrics/v1/performance/anomaly-data/query"
    else:
        raise ValueError(f"Unsupported type parameter: {type}")

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
    Query object health score

    Query health score info of specified type of objects.

    Args:
        client: DME API client
        object_type: object type (Required)
                    valid values: storage (Storage device), storage_pool (Storage pool), storage_host (Storage host),
                           storage_disk (Hard disk), storage_port (Storage port), fcswitch_port (FC switch port),
                           storage_file_system (Filesystem), controller (Controller), replication_cg (Remote replication consistency group),
                           volume (LUN), tier (Service level), datastore (Data store), virtual_machine (Virtual machine),
                           storage_name_space (Namespace), storage_node (Storage node), dpc (DPC)
        object_name: object name, supports fuzzy query (Optional, up to 256 characters)
        object_ids: object resId list, for batch exact lookup (Optional, up to 100 IDs)
        page_no: pagination query start position (Optional, min: 1)
        page_size: items per page (Optional, 1~100, default 20)
        sort_key: sort field (Optional), sort by score, valid values: health_score
        sort_dir: sort direction (Optional), valid values: asc, desc

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, containing object health score list
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
    Query deduction details of health dimensions

    Query the deduction details of a specified object under a specified health dimension.

    Args:
        client: DME API client
        object_id: object Id (Required, 1~128 characters)
        object_type: object type (Required)
                    valid values: storage, storage_pool, storage_host, storage_disk, storage_port,
                           fcswitch_port, storage_file_system, controller, replication_cg, volume,
                           tier, datastore, virtual_machine, storage_name_space, storage_node,
                           dpc, gfs, dpc_client, vbs_client
        health_dimension: health dimension (Required)
                        valid values: alarm, performance_anomaly,
                              performance_prediction, capacity_prediction

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, containing indicator deduction list
    """
    url = "/rest/healthmgmt/v1/health-result/dimension-score/query"

    payload = {
        'object_id': object_id,
        'object_type': object_type,
        'health_dimension': health_dimension
    }

    response = client.post(url, body=payload)
    return response



# ============ Performance monitoring subtopic functions ============




def diagnose_task_status(client: DMEAPIClient, task_id: str) -> dict:
    r"""
    Query performance diagnosis task status

    Query diagnosis task status by task ID.

    Args:
        client: DME API client
        task_id: task ID (Required), 1~128 characters

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, containing:
        - task_id: task ID
        - task_status: task status, valid values: 
            - executing: executing
            - failed: failed
            - success: success
            - waiting: waiting
            - terminated: terminated
        - task_result: task result, valid values: 
            - un_analyzed: unanalyzed
            - warning: warning
            - abnormal: abnormal
            - event: event
        - total_step_count: total steps
        - finish_step_count: completed steps
    """
    url = "/rest/dmegraphanalysis/v1/perf-tasks/query-status"

    payload = {
        "task_id": task_id
    }

    print(f"Request URL: {url}")
    print(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


# ============================================================================
# Check policy (check_policy) subtopic functions
# ============================================================================

def check_policy_list(client: DMEAPIClient, policy_name: str = None, exact_query: bool = None,
                        status: str = None, policy_type: str = None, policy_source: str = None,
                        alarm_type: str = None, object_type: str = None, page_no: int = 1,
                        page_size: int = 20, sort_key: str = None, sort_dir: str = None,
                        administrative_status: str = None, policy_category: str = None,
                        object_category: str = None) -> dict:
    """
    Query check policy list

    Query the check policy list, supports filtering by policy name, status, type, etc.

    Args:
        client: DME API client
        policy_name: policy name (supports fuzzy query, up to 256 characters)
        exact_query: whether to use exact query (Optional, boolean). When True, exact matching; when False, fuzzy matching
        status: policy status (Optional). valid values: enabled (enabled), disabled (disabled)
        policy_type: policy type (Optional). valid values: performance (performance), capacity (capacity), availability (availability)
        policy_source: policy source (Optional). valid values: system (system), custom (custom)
        alarm_type: alarm type (Optional). valid values: violation (violation), alarm (alarm), event (event)
        object_type: object type (Optional). valid values: storage (storage), volume (volume), host (host)
        page_no: pagination start page, default 1
        page_size: items per page, 1~1000, default 20
        sort_key: sort field (Optional). valid values: name (policy name), status (status)
        sort_dir: sort direction (Optional). valid values: asc (ascending), desc (descending)
        administrative_status: administrative status (Optional)
        policy_category: policy category (Optional)
        object_category: object category (Optional)

    Returns:
        {
            total: total policies (int32),
            policies: policy list (List<CheckPolicy>). parameter format: [{
                id: policy ID (string, 1~64 characters),
                name: policy name (string, 1~256 characters),
                policy_type: policy type (string),
                status: policy status (string). valid values: enabled, disabled,
                policy_source: policy source (string). valid values: system, custom,
                object_type: object type (string),
                alarm_type: alarm type (string). valid values: violation, alarm, event,
            }, ...],
        }
    """
    url = "/rest/policymgmt/v1/policies/query"

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

    Execute the specified check policy.

    Args:
        client: DME API client
        policy_id: policy ID (1~64 characters)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/policymgmt/v1/policies/{policy_id}/execute"

    response = client.post(url, params={"policy_id": policy_id})
    return response


def check_policy_enable(client: DMEAPIClient, policy_id: str) -> dict:
    """
    Enable check policy

    Enable the specified check policy.

    Args:
        client: DME API client
        policy_id: policy ID (1~64 characters)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/policymgmt/v1/policies/{policy_id}/enable"

    response = client.post(url, params={"policy_id": policy_id})
    return response


def check_policy_disable(client: DMEAPIClient, policy_id: str) -> dict:
    """
    Disable check policy

    Disable the specified check policy.

    Args:
        client: DME API client
        policy_id: policy ID (1~64 characters)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/policymgmt/v1/policies/{policy_id}/disable"

    response = client.post(url, params={"policy_id": policy_id})
    return response


def check_policy_delete(client: DMEAPIClient, policy_id: str) -> dict:
    """
    Delete check policy

    Delete the specified check policy.

    Args:
        client: DME API client
        policy_id: policy ID (1~64 characters)

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/policymgmt/v1/policies/{policy_id}"

    response = client.delete(url, params={"policy_id": policy_id})
    return response


# ============================================================================
# Check result (check_result) subtopic functions
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
    Query check policy abnormal check result list

    Query abnormal check results of check policies, supports multiple filter conditions and pagination.

    Args:
        client: DME API client
        object_name: object name (supports fuzzy query, 1~256 characters)
        level: abnormal level (Optional). valid values: critical (critical), major (major), minor (minor), info (info)
        object_ids: object ID list (up to 100)
        object_native_id: object nativeId (1~384 characters)
        object_type: object type (Optional). valid values: bond_port (bond port), clone_pair (clone pair), controller (Controller), datastore (data store), device_pair (device pair), dtree (Dtree), dtree_user_quota (Dtree user quota), ethernet_port (Ethernet port), expansion_port (cascade port), fc_link (FC link), fc_port (FC port), fc_switch (FC switch), fcswitch_port (FC switch port), filesystem_snapshot (Filesystem snapshot), fs_hyper_metro_pair (Filesystem hypermetro), hci (hyper-converged), host (host), host_initiator (host initiator), hyper_metro_cg (hypermetro consistency group), hyper_metro_pair (hypermetro), ip_link (IP link), ip_switch (Ethernet switch), ip_switch_board (Ethernet switch board), ip_switch_fan (Ethernet switch fan), ip_switch_port (Ethernet switch port), ip_switch_psu (Ethernet switch PSU), logic_port (Logic port), lun_group (LUN group), lun_snapshot (LUN snapshot), dataturbo (dataturbo protocol), nfsv3 (NFS_v3 protocol), nfsv4 (NFS_v4 protocol), nfsv41 (NFS_v4.1 protocol), phost_nic (host NIC), physical_server (physical server), remote_device (remote device), replication_cg (replication consistency group), replication_pair (replication Pair), roce_port (RoCE port), sas_port (SAS port), server_nic (server NIC), smb1 (SMB1 protocol), smb2_3 (SMB2/3 protocol), storage (storage), storage_disk (hard disk), storage_file_system (Filesystem), storage_host (Storage host), host_link (Storage host), storage_host_group (Storage host group), storage_host_initiator (Storage host initiator), storage_name_space (Namespace), storage_node (storage node), storage_pool (Storage pool), storage_port (storage port), tier (service level), virtual_cluster (virtualization cluster), virtual_disk (virtual disk), virtual_host (hypervisor), virtual_machine (Virtual machine), virtual_machine_snapshot (Virtual machine snapshot), virtual_nic (virtual NIC), virtual_gpu (GPU), volume (LUN), vstore (vStore), zone (zone), filesystem_replication_pair (Filesystem replication pair), dpc, gfs (GFS), vbs_client (vbs client), dpc_client (dpc client), nfs_plus_client_link (NFS+ client link), knowledge_base_node (KnowledgeBase node), object_data_flow (object data flow)
        policy_id: policy ID (exact query, 1~64 characters)
        policy_name: policy name (supports fuzzy query, 1~256 characters)
        policy_types: policy type list (up to 30). valid values: performance (performance threshold), capacity (capacity threshold), availability (availability), configuration (configuration), recyclable (recyclable resources), lowload (low load resources), performance_anomaly (performance anomaly), performance_prediction (performance prediction), capacity_prediction (capacity prediction), history_performance (historical performance), load_imbalance (load imbalance), highload (high load resources)
        cause: abnormal cause (supports fuzzy query, 1~768 characters)
        alarm_type: alarm type (Optional). valid values: violation (violation), alarm (alarm), event (event)
        first_occur_time: first occurrence time range ({beginTime, endTime}, UTC timestamp, ms)
        last_occur_time: last occurrence time range ({beginTime, endTime}, UTC timestamp, ms)
        page_no: pagination query page number, 1~10000, default 1
        page_size: pagination query item count, 1~2000, default 20
        sort_key: sort field (Optional). valid values: violation_count (violation count)
        sort_dir: sort direction (Optional). valid values: asc (ascending), desc (descending)

    Returns:
        {
            total: total abnormal check results (int32, 0~2147483647),
            results: abnormal check result list (List<PolicyCheckResult>, max array members: 2000). parameter format: [{
                    check_result_id: check result ID (string, 1~64 characters),
                    policy_id: policy ID (string, 1~64 characters),
                    policy_name: policy name (string, 1~256 characters),
                    policy_type: check policy type (string). valid values: performance (performance threshold), capacity (capacity threshold), availability (availability), configuration (configuration), recyclable (recyclable resources), lowload (low load resources), performance_anomaly (performance anomaly), performance_prediction (performance prediction), capacity_prediction (capacity prediction), history_performance (historical performance), load_imbalance (load imbalance), highload (high load resources),
                    object_name: object name (string, 0~1000 characters),
                    object_id: object ID (string, 1~64 characters),
                    object_native_id: object nativeId (string, 0~500 characters),
                    object_type: object type (string),
                    level: abnormal level (string). valid values: critical, major, minor, info,
                    cause: abnormal condition (string, 0~1000 characters),
                    alarm_type: alarm type (string). valid values: violation, alarm, event,
                    violation_count: violation count (int32, 0~2147483647),
                    first_occur_time: first occurrence time (int64, UTC timestamp ms),
                    last_occur_time: last occurrence time (int64, UTC timestamp ms),
                    location_info: location info (string, 0~3000 characters),
                    abnormal_reasons: abnormal reason list (List<string>, max array members: 100),
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
    Query check policy abnormal check result details

    Query details of a specified check result.

    Args:
        client: DME API client
        check_result_id: check result ID (1~64 characters)

    Returns:
        {
            check_result_id: check result ID (string, 1~64 characters),
            policy_id: policy ID (string, 1~64 characters),
            policy_name: policy name (string, 1~256 characters),
            policy_type: check policy type (string). valid values: performance (performance threshold), capacity (capacity threshold), availability (availability), configuration (configuration), recyclable (recyclable resources), lowload (low load resources), performance_anomaly (performance anomaly), performance_prediction (performance prediction), capacity_prediction (capacity prediction), history_performance (historical performance), load_imbalance (load imbalance), highload (high load resources),
            object_name: object name (string, 0~1000 characters),
            object_id: object ID (string, 1~64 characters),
            object_native_id: object nativeId (string, 0~500 characters),
            object_type: object type (string),
            level: abnormal level (string). valid values: critical, major, minor, info,
            cause: abnormal condition (string, 0~1000 characters),
            alarm_type: alarm type (string). valid values: violation, alarm, event,
            violation_count: violation count (int32, 0~2147483647),
            first_occur_time: first occurrence time (int64, UTC timestamp ms),
            last_occur_time: last occurrence time (int64, UTC timestamp ms),
            location_info: location info (string, 0~3000 characters),
            abnormal_reasons: abnormal reason list (List<string>, max array members: 100),
        }
    """
    url = "/rest/policymgmt/v1/abnormal-check-results/{check_result_id}"

    response = client.get(url, params={"check_result_id": check_result_id})
    return response


# action list, for CLI help
# ============================================================================
# Topology (topology) subtopic functions
# ============================================================================

def topology_query_luns(client: DMEAPIClient, entry_objects: list, storage_pool_id: str,
               lun_name: str = None, san_type: str = None, page_size: int = 20, page_no: int = 1) -> dict:
    r"""
    Query topology LUN list

    Query LUN list based on the specified entry object and storage pool.

    Args:
        client: DME API client
        entry_objects: entry object list (List<LunTopoQueryEntryObject>, Required, max array members: 5). parameter format: [{
                id: entry object id (Required, string, 1~128 characters),
                type: entry object type (Required, string). valid values: host (physical host), storage (flash storage/distributed storage), host_group (host group), lun (LUN), vm (Virtual machine), datastore (data store), application (application), switch_port (FC switch port), storage_pool (Storage pool). Note: datastore/application/switch_port not supported for ip_san; up to 5 for entry object type vm/storage_pool, only 1 for other types,
            }, ...]
        storage_pool_id: storage pool ID (Required, string, 1~128 characters). Format is {storageId}STORAGE_POOL{poolId}, e.g. "b9326bbf-...STORAGE_POOL163BECEA...", obtained from the id field of storage pool list
        san_type: storage area network type (Optional, string). valid values: ip_san, fc_san
        lun_name: LUN name (Optional, string, 1~256 characters), supports fuzzy query
        page_size: pagination query item count (Optional, int32, 1~20), default 20
        page_no: pagination query start position (Optional, int32, 1~2147483647), default 1

    Returns:
        {
            total: total LUN query results (int32),
            luns: LUN query result list (List<LunObject>). parameter format: [{
                id: LUN id (string, 1~128 characters),
                name: LUN name (string, 1~256 characters),
                datastore: data store list for the LUN (List<LunsQueryDataStoreItem>). attribute format: [{
                    id: data store id (string, 1~128 characters),
                    name: data store name (string, 1~256 characters),
                    storage_type: storage type (string). valid values: vmfs (Virtual machine Filesystem),
                    vr_type: virtualization type (string). valid values: vmware, hcs,
                }, ...],
                is_replication_member: whether it is a replication volume (boolean, true/false),
                is_replication_primary: whether it is the replication volume primary side (boolean, true/false),
                is_hyper_metro_member: whether it is a protection volume (boolean, true/false),
                is_hyper_metro_primary: whether it is the protection volume primary side (boolean, true/false),
                storage_pool_id: Storage pool ID (string, 1~140 characters). Format is {storageId}STORAGE_POOL{poolId},
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

    print(f"Request URL: {url}")
    print(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


def topology_query_san_path(client: DMEAPIClient, entry_objects: list, san_type: str = None) -> dict:
    r"""
    Query SAN path topology structure

    Query the topology structure from host to storage pool in the SAN network based on the specified entry object.
    Supports both IP_SAN and FC_SAN types.

    Args:
        client: DME API client
        entry_objects: entry object list (Required, max array members: 1). FC_SAN parameter format: [{
                id: entry object id (Required, string, 1~128 characters),
                type: entry object type (Required, string). valid values: host (host), storage (flash Storage device), lun (LUN), host_group (host group), vm (Virtual machine), datastore (data store), application (application), switch_port (FC switch port), storage_pool (Storage pool),
            },...]. IP_SAN parameter format: [{
                id: entry object id (Required, string, 1~128 characters),
                type: entry object type (Required, string). valid values: host (host), storage (flash storage or distributed storage), lun (LUN), host_group (host group), vm (Virtual machine), storage_pool (Storage pool). Note: IP_SAN does not support datastore/application/switch_port types, up to 5 objects,
            }, ...]
        san_type: SAN type (Optional, string). valid values: ip_san, fc_san
                  - If not specified, both IP_SAN and FC_SAN APIs are called, data is combined
                  - If ip_san, only IP_SAN API is called
                  - If fc_san, only FC_SAN API is called

    Returns:
        When san_type=fc_san or not specified (FC_SAN part): 
        {
            fabrics: Fabric list (List<HostToStoragePoolFabric>). parameter format: [{
                id: Fabric id (string, 1~64 characters),
                name: Fabric name (string, 1~128 characters),
                switches: switch list (List<SwitchItem>). attribute format: [{
                    id: switch node id (string, 1~64 characters),
                    name: switch node name (string, 1~128 characters),
                    ports: switch port list (List<SwitchPortItem>). attribute format: [{
                        id: switch port node id (string, 1~64 characters),
                        name: switch port node name (string, 1~128 characters),
                        status: switch port status (string). valid values: normal, abnormal, unknown,
                    }, ...],
                }, ...],
                port_links: switch port link list (List<PortLinkItem>). attribute format: [{
                    left_port: left port (PortNodeItem). attribute format: {
                        id: port Id (string, 1~64 characters),
                        type: port type (string). valid values: host_port, switch_port, storage_port,
                    },
                    right_port: right port (PortNodeItem),
                }, ...],
                switch_links: switch connection list (List<SwitchLinkItem>). attribute format: [{
                    host_to_switch_id: host-connected switch ID (string, 1~64 characters),
                    storage_to_switch_id: storage-connected switch ID (string, 1~64 characters),
                }, ...],
            }, ...],
            hosts: host list (List<HostToStoragePoolHost>). attribute format: [{
                id: host id (string, 1~64 characters),
                name: host name (string, 1~256 characters),
                access_mode: access mode (string). valid values: vcenter, none,
                host_groups: host group list (List<HostToStoragePoolHostGroup>),
                ports: host port list (List<HostToStoragePoolPort>),
                deployment_type: deployment type (string). valid values: BMS (bare metal server), ECS (ECS host),
                direct_storage_ids: storage device ID list directly connected to host (List<string>),
            }, ...],
            storages: storage list (List<HostToStoragePoolStorage>). attribute format: [{
                id: storage id (string, 1~64 characters),
                name: storage name (string, 1~128 characters),
                product_model: storage device type (string),
                controllers: Controller list (List<HostToStoragePoolController>),
                pools: Storage pool list (List<HostToStoragePoolPool>),
                disks: storage disk list (List<HostToStorageDiskDisks>),
            }, ...],
        }
        When san_type=ip_san (IP_SAN): 
        {
            switches: switch list (List<SwitchItem>),
            hosts: host list (List<HostToStoragePoolHost>),
            storages: storage list (List<HostToStoragePoolStorage>),
            switch_links: switch connection list (List<SwitchLinkItem>),
        }
        When san_type=None: 
        {
            ip_san: { IP_SAN return data },
            fc_san: { FC_SAN return data },
        }
    """
    result = {}

    # If san_type is not specified, call both APIs
    if san_type is None:
        # Call IP_SAN API
        ip_san_url = "/rest/topomgmt/v1/topo-data/ipsan/host-storage/query"
        ip_san_payload = {"entry_objects": entry_objects}
        print(f"Request URL: {ip_san_url}")
        print(f"Request payload: {json.dumps(ip_san_payload, ensure_ascii=False, indent=2)}")
        ip_san_response = client.post(ip_san_url, body=ip_san_payload)
        result['ip_san'] = ip_san_response

        # Call FC_SAN API
        fc_san_url = "/rest/topomgmt/v1/topo-data/host-storage/query"
        fc_san_payload = {"entry_objects": entry_objects}
        print(f"Request URL: {fc_san_url}")
        print(f"Request payload: {json.dumps(fc_san_payload, ensure_ascii=False, indent=2)}")
        fc_san_response = client.post(fc_san_url, body=fc_san_payload)
        result['fc_san'] = fc_san_response

        return result

    # If san_type is specified, call only the corresponding API
    elif san_type == 'ip_san':
        url = "/rest/topomgmt/v1/topo-data/ipsan/host-storage/query"
        payload = {"entry_objects": entry_objects}
        print(f"Request URL: {url}")
        print(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        response = client.post(url, body=payload)
        return response

    elif san_type == 'fc_san':
        url = "/rest/topomgmt/v1/topo-data/host-storage/query"
        payload = {"entry_objects": entry_objects}
        print(f"Request URL: {url}")
        print(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        response = client.post(url, body=payload)
        return response

    else:
        raise ValueError(f"Invalid san_type parameter: {san_type}, only supports: ip_san, fc_san")




def topology_query_vms(client: DMEAPIClient, entry_objects: list, host_id: str,
              vm_name: str = None, page_size: int = 20, page_no: int = 1) -> dict:
    r"""
    Query topology virtual machines and virtual disk list, or query BMS physical disk list

    Query virtualization resources based on the specified entry object.

    Args:
        client: DME API client
        entry_objects: entry object list (List<VmTopoQueryEntryObject>, Required, max array members: 5). parameter format: [{
                id: entry object id (Required, string, 1~128 characters),
                type: entry object type (Required, string). valid values: vm (Virtual machine), host_group (host group), host (host), storage (flash storage or distributed storage), lun (LUN), datastore (data store), switch_port (FC switch port), storage_pool (Storage pool),
            }, ...]
        host_id: host ID (Required, string, 0~128 characters)
        vm_name: Virtual machine name search parameter (Optional, string, 0~256 characters), supports fuzzy match
        page_size: pagination query item count (Optional, int32, 1~20), default 20
        page_no: pagination query start position (Optional, int32, 1~2147483647), default 1

    Returns:
        {
            total: total vm query results (int32),
            vms: vm query result list (List<VirtualMachine>). parameter format: [{
                id: id (string, 1~64 characters),
                name: vm name (string, 1~128 characters),
                ip: vm ip (string, 1~3072 characters),
                host_id: physical host ID (string, 1~64 characters),
                vr_type: virtualization type (string). valid values: vmware, hcs,
                vdisks: virtual disk list (List<VirtualDisk>). attribute format: [{
                    id: vdisk id (string, 1~64 characters),
                    name: vdisk name (string, 1~128 characters),
                }, ...],
            }, ...],
            disks: physical disks associated with the physical host list (List<PhysicalDisk>). parameter format: [{
                id: disk id (string, 1~64 characters),
                native_id: disk native id (string, 1~768 characters),
                name: disk name (string, 1~768 characters),
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

    print(f"Request URL: {url}")
    print(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


def topology_query_graph_path(client: DMEAPIClient, entry_res_type: str, entry_res_id: str,
                type: str = None, filter: list = None) -> dict:
    r"""
    Query topology graph info

    Query topology graph info, supports NAS, K8s, DB and other service types.

    Args:
        client: DME API client
        entry_res_type: entry resource type (Required, string). valid values: storage_device (Storage device), disk (hard disk), storage_pool (Storage pool), hyper_scale_pool (global pool), file_system (Filesystem), controller (Controller), eth_port (Ethernet/RoCE port), ib_port (IB port), logic_port (Logic port), ip_client (IP client), dtree (Dtree), lun (LUN), k8s_application (container application), k8s_workload (workload), k8s_pod (pod group), k8s_pvc (persistent volume claim), k8s_pv (persistent volume), k8s_cluster (container cluster), k8s_node (container node), k8s_vc_job (Volcano Job), data_turbo_client (DataTurbo client), enclosures (chassis), eth_switch (switch), storage_zone (storage zone), service_network (service network), db_instance (GaussDB instance), db_node (GaussDB node)
        entry_res_id: entry resource ID (Required, string, 1~256 characters)
        type: service type (Optional, string). valid values: nas, k8s, db
        filter: condition filter list (Optional, List<TopoFilter>, max array members: 10). parameter format: [{
                type: topology query return resource type (Optional, string). valid values same as entry_res_type,
                key: field name (Optional, string, 1~256 characters). e.g. id, name, ip,
                value: field value (Optional, string, 0~256 characters),
                operator: comparison method (Optional, string). valid values: lt (less than), le (less than or equal), eq (equal), gt (greater than), ge (greater than or equal), ne (not equal), contains,
            }, ...]

    Returns:
        {
            nodes: node list (List<NodeItem>). parameter format: [{
                id: node object ID (string, 1~256 characters),
                type: topology query return resource type (string). valid values: storage_device, disk, storage_pool, hyper_scale_pool, file_system, controller, eth_port, ib_port, logic_port, ip_client, dtree, lun, k8s_application, k8s_workload, k8s_pod, k8s_pvc, k8s_pv, k8s_cluster, k8s_node, k8s_vc_job, k8s_pod_group, data_turbo_client, enclosures, eth_switch, storage_zone, service_network, db_instance, db_node, host, host_port, storage_port,
                label: node object name (string, 1~256 characters),
                sub_type: workload type (string, only for k8s_workload). valid values: deployment, replica_set, stateful_set, daemon_set, job, cron_job,
            }, ...],
            edges: edge list (List<EdgeItem>). parameter format: [{
                source: source node ID (string, 1~256 characters),
                target: target node ID (string, 1~256 characters),
                edge_type: edge type (string). valid values: edge_k8s_node_to_k8s_pod, edge_storage_pool_to_storage_disk, edge_filesystem_to_storage_pool, edge_storage_disk_to_storage_device, edge_k8s_pvc_to_k8s_pv, edge_k8s_pod_to_k8s_pvc, edge_dtree_to_filesystem, edge_lun_storage_pool, edge_k8s_cluster_to_k8s_node, edge_k8s_pv_to_lun, edge_k8s_pv_to_dtree, edge_nas_client_to_logic_port, edge_logic_port_to_ethernet_port, edge_ethernet_port_to_controller, edge_controller_to_filesystem, edge_data_turbo_client_to_logic_port, edge_controller_to_ethernet_port, edge_data_turbo_client_to_service_network, edge_ethernet_port_to_eth_switch_port, edge_service_network_to_logic_port, edge_a800_enclosures_to_storage_zone, edge_controller_to_enclosures, edge_storage_zone_to_filesystem, edge_eth_switch_port_to_eth_switch_port, edge_enclosures_to_controller, edge_controller_to_storage_port, edge_eth_switch_to_eth_switch_port, edge_storage_port_to_eth_switch_port, edge_filesystem_to_hyper_scale_pool, edge_hyper_scale_pool_to_storage_pool, edge_eth_switch_port_to_eth_switch, edge_k8s_pod_to_k8s_node, edge_k8s_podgroup_to_k8s_pod, edge_k8s_vcjob_to_k8s_podgroup, edge_lun_to_controller, edge_host_to_service_network, edge_host_to_host_port, edge_host_port_to_service_network, edge_service_network_to_lun, edge_service_network_to_storage_port, edge_db_instance_to_db_node, edge_db_node_to_host,
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

    print(f"Request URL: {url}")
    print(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


# ============================================================================
# action list, for CLI help
# ============================================================================

ACTIONS = {
    'alarm_list': {
        'func': alarm_list,
        'description': 'Query alarm info (current alarms, optionally including history alarms)',
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
        'description': 'Un-acknowledge alarm',
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
    # performance subtopic action
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
        'description': 'Query historical performance data',
        'params': ['obj_type_id', 'indicator_ids', 'obj_ids', 'obj_type', 'indicators', 'ext_dimensions', 'interval', 'range', 'begin_time', 'end_time'],
        'subtopic': 'performance'
    },
    'performance_show_indicators': {
        'func': performance_show_indicators,
        'description': 'Show monitoring indicator details',
        'params': ['indicators'],
        'subtopic': 'performance'
    },
    'performance_list_indicators': {
        'func': performance_list_indicators,
        'description': 'List monitoring indicators for a monitoring object type',
        'params': ['obj_type_id'],
        'subtopic': 'performance'
    },
    'performance_list_object_types': {
        'func': performance_list_object_types,
        'description': 'Get all monitoring object types',
        'params': ['filter'],
        'subtopic': 'performance'
    },
    # check_result subtopic action
    'check_result_list': {
        'func': check_result_list,
        'description': 'Query check policy abnormal check result list',
        'params': ['object_name', 'level', 'object_ids', 'object_native_id', 'object_type', 'policy_id', 'policy_name', 'policy_types', 'cause', 'alarm_type', 'first_occur_time', 'last_occur_time', 'page_no', 'page_size', 'sort_key', 'sort_dir'],
        'subtopic': 'check_result'
    },
    'check_result_show': {
        'func': check_result_show,
        'description': 'Query check policy abnormal check result details',
        'params': ['check_result_id'],
        'subtopic': 'check_result'
    },
    # check_policy subtopic action
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
    # topology subtopic action
    'topology_query_san_path': {
        'func': topology_query_san_path,
        'description': 'Query SAN path topology (supports IP_SAN and FC_SAN)',
        'params': ['entry_objects', 'san_type'],
        'subtopic': 'topology'
    },
    'topology_query_luns': {
        'func': topology_query_luns,
        'description': 'Query topology LUN list',
        'params': ['entry_objects', 'storage_pool_id', 'lun_name', 'san_type', 'page_size', 'page_no'],
        'subtopic': 'topology'
    },
    'topology_query_vms': {
        'func': topology_query_vms,
        'description': 'Query topology virtual machines and virtual disk list, or BMS physical disk list',
        'params': ['entry_objects', 'host_id', 'vm_name', 'page_size', 'page_no'],
        'subtopic': 'topology'
    },
    'topology_query_graph_path': {
        'func': topology_query_graph_path,
        'description': 'Query topology graph info (supports NAS, K8s, DB and other service types)',
        'params': ['entry_res_type', 'entry_res_id', 'type', 'filter'],
        'subtopic': 'topology'
    },
    # health subtopic action
    'health_query_data': {
        'func': health_query_data,
        'description': 'Query health related data (capacity prediction/performance prediction/performance anomaly)',
        'params': ['type', 'object_id', 'begin_time', 'end_time', 'object_type', 'indicator'],
        'subtopic': 'health'
    },
    'health_show_score': {
        'func': health_show_score,
        'description': 'Query object health score',
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
