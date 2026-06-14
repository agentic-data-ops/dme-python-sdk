"""
AIOps  intelligent operationsoperations
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

     queryCurrent alarm,Optionalchoose whether to query simultaneouslyHistory alarm.

    Args:
        client: DME API client
        alarm_id: alarm ID,supports fuzzy match
        severity: Alarm severity list, value:critical, major, minor, warning, indeterminate, cleared
        mo_dn: Managed object DN, supports operator matching
        alarm_group_id: alarm group ID
        dc_id: Data center ID
        product_name:  product name
        alarm_name: Alarm name,supports fuzzy match
        occur_utc_start: Alarm start time(ms timestamp)
        occur_utc_end: Alarm end time(ms timestamp)
        fields: Specified return field list
        page_no: Page queryStart page,default 1
        page_size: Items per page,1~1000,default 100 (for current alarm query)
        cleared:  whether cleared, true/false (for history alarm query)
        size: Max results, 1~1000, default 100 (for history alarm query)
        iterator: iterator, not needed on first query,use last returned iterator for subsequent queries (history alarm)
        include_history:  switch parameter,query both if specifiedHistory alarm

    Returns:
        {
            current_alarms: Current alarm list (List<AlarmInfo>).  parameter format: [{
                alarm_id: Alarm ID (string),
                alarm_name: Alarm name (string),
                severity: Alarm severity (string),
                status:  status (string),
            }, ...],
            total: alarmTotal count (integer),
        }
    """
    result = {
        'current_alarms': None,
        'history_alarms': None
    }

    #  queryCurrent alarm(Always query by default)
    current_url = "/rest/alarmmgmt/v1/alarms/current-alarm/query"
    current_params = _build_current_alarm_params(
        alarm_id=alarm_id, severity=severity, mo_dn=mo_dn,
        alarm_group_id=alarm_group_id, dc_id=dc_id, product_name=product_name,
        alarm_name=alarm_name, occur_utc_start=occur_utc_start,
        occur_utc_end=occur_utc_end, fields=fields, page_size=page_size
    )

    current_response = client.post(current_url, body=current_params)
    result['current_alarms'] = current_response

    # if specified include_history, simultaneously queryHistory alarm
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

    Acknowledge (ACK) specified alarm.

    Args:
        client: DME API client
        csns: Alarm serial numbers (Required), max 30

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

    print(f" request URL: {url}")
    print(f"Request load:{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


def alarm_unack(client: DMEAPIClient, csns: list) -> dict:
    r"""
     cancelAcknowledge alarm

    Un-acknowledge (UNACK) specified alarm.

    Args:
        client: DME API client
        csns: Alarm serial numbers (Required), max 30

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

    print(f" request URL: {url}")
    print(f"Request load:{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


def alarm_clear(client: DMEAPIClient, csns: list) -> dict:
    r"""
    Clear alarm

    Clear (CLEAR) specified alarm.

    Args:
        client: DME API client
        csns: Alarm serial numbers (Required), max 30

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

    print(f" request URL: {url}")
    print(f"Request load:{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


def diagnose_task_create(client: DMEAPIClient, object_ids: list, object_type: str,
                         begin_time: int, end_time: int, analysis_types: list) -> dict:
    r"""
    Create intelligent analysis task

    Args:
        client: DME API client
        object_ids: entry analysisobject ID  list(Required),Array size:1~50
        object_type: entryObject type(Required),value range:
            - VM: Virtual machine
            - STORAGE_HOST: Storage host
            - STORAGE_DEVICE: Storage device
            - LUN: LUN
            - FILE_SYSTEM: Filesystem
            - VBS_CLIENT: VBS Client
            - DATATURBO: DPC
            - STORAGE_POOL: Storage pool
            - IP_CLIENT: IP Client
            - HOST_GROUP: storage host group
            - FC_PORT: FC  port
            - ETH_PORT: Ethernet port
            - LUN_GROUP: LUN group
            - LOGIC_PORT: Logic port
            - CONTROLLER: Controller
            - NAMESPACE: Namespace
        begin_time:  Analysis start time(Required),Unix timestamp (ms),must be integer minute time point, supports diagnosis within recent 7 daysn
        end_time:  analysisEnd time(Required),Unix timestamp (ms),must be integer minute time point
                  Analysis interval rangemust be greater than 30 minute(s),小于 24 hour(s)
        analysis_types: Intelligent analysis type list(Required),Array size:1~4,value range:
            - highLatency: High latency
            - healthAnalysis: Health quick check
            - IOInterrupt: IO interrupt
            - highReadLatency: 高Read latency
            - highWriteLatency: 高Write latency
            - trafficAnalysis: traffic analysis
            - cpuUsageAnalysis: CPU consumption analysis

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes :
        - total: Intelligent analysis taskTotal count
        - data: Intelligent analysis task response result list, Each item includes:
            - id: task  ID
            - analysis_type:  analysis type
            - error_msg: Error message
            - is_succeed: Created successfully
    """
    url = "/rest/diagnosis/v1/tasks"

    payload = {
        "object_ids": object_ids,
        "object_type": object_type,
        "begin_time": begin_time,
        "end_time": end_time,
        "analysis_types": analysis_types
    }

    print(f" request URL: {url}")
    print(f"Request load:{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


# ============ Performance Performance monitoringsubtopic functions ============


def performance_create_collect_task(client: DMEAPIClient, begin_time: int, end_time: int,
                        object_type_id: str, object_ids: list,
                        indicator_ids: list) -> dict:
    """
    Create performance file collection task

    Collect performance files from start to end date,only supports collecting data within 7 days,
     each passedobjectmultiplied by metric count not exceed 2000.

    Args:
        client: DME API client
        begin_time: Start time(Required,Unix Timestamp毫second(s))
        end_time: End time(Required,Unix Timestamp毫second(s))
        object_type_id: Object type ID(Required,1~32  characters)
        object_ids: object ID  list(Required, max 2000 个,ID  length 1~32 位)
        indicator_ids: Metric ID list(Required, max 20, ID length 1-16 digits)

    Returns:
        task  ID
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
        task_id: task  ID(Required)

    Returns:
        Performance file download link or content
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
    Query historyPerformance data

    Based on input parameters"range"Enum values or from start toEnd timeQuery data within range.
    With aggregated data,Returned result sequence is average,includes max, min and corresponding timestamps.

     Usage notes:
    - Object typeand metric definition:从Performance metricsobtain from model documentation (reference/dme_performance_model/index.md)
    - Object ID (CMDB instance ID) retrieval steps:
      1. running `cmdb instance list --help` View help,see class definition and query method
      2. Based on help info,从 CMDB Determine what to query from resource modelResource type (Class  name)
      3.  use `cmdb instance list --class_name <Class  name>` Query instance list
      4. obtain from response corresponding resource的 instance_id (即 obj_ids  parameter)

    Args:
        client: DME API client
        obj_type_id:  Monitor object type ID(Required), corresponding monitor object type ID
                     从Performance metricsobtain from model documentation:reference/dme_performance_model/index.md
        indicator_ids: Monitoring metric ID list(Required, max 100), corresponding metric ID
                       从Performance metricsobtain from model documentation:reference/dme_performance_model/index.md
        obj_ids:  monitorobjectIdentifier list(Required, max 512 个), corresponding CMDB instance ID
                 Retrieval method:
                 1. running `cmdb instance list --help` View help,See class definition
                 2. Determine what to query based on helpResource type (Class  name)
                 3. running `cmdb instance list --class_name <Class  name>`  queryinstance
                 4. obtain from response instance_id
        obj_type:  monitorObject type(Optional,1~512  characters)
        indicators: Monitoring metric list(Optional, max 100)
        ext_dimensions:  extended dimensioninfo list(Optional, max 100)
        interval:  interval granularity(Optional)
                  value range:ONE_MINUTE(1 minute(s)), MINUTE(5 minute(s)), HALF_HOUR(30 minute(s)),
                  HOUR(1 hour(s)), DAY(1 day(s)), WEEK(1 week(s)), MONTH(1 个month(s))
        range: Time range(Optional,default LAST_1_HOUR)
               value range:LAST_5_MINUTE( recent 5 minute(s)), LAST_1_HOUR( recent 1 hour(s)),
               LAST_1_DAY( recent 1 day(s)), LAST_1_WEEK( recent 1 week(s)), LAST_1_MONTH( recent 1 个month(s)),
               LAST_1_QUARTER( recent 3 个month(s)), HALF_1_YEAR( recent半year(s)), LAST_1_YEAR( recent 1 year(s)),
               BEGIN_END_TIME(Set start and endEnd time), INVALID(Invalid value)
        begin_time: Query start time(Optional),仅 range 为 BEGIN_END_TIME 时effective, must be end_time 小
        end_time: Query end time(Optional),仅 range 为 BEGIN_END_TIME 时effective, must be begin_time 大

    Returns:
        Historical performance data,includes  status_code, error_code, error_msg, data
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
        indicators:  Monitor object metric ID list(Required, max 1000 characters)
                    can beinteger list或string list,如 [123, 456] 或 ["123", "456"]

    Returns:
        Monitoring metric info,includes  kpi, data_type, data_unit, en_us, zh_cn 等 field
    """
    url = "/rest/metrics/v1/mgr-svc/indicators"

    # ensure indicators is an integer list
    if indicators:
        indicators = [int(i) for i in indicators]

    # API requires direct array passing, not object
    response = client.post(url, body=indicators)
    return response


def performance_list_indicators(client: DMEAPIClient, obj_type_id: int) -> dict:
    """
    List monitoringObject typeSupported monitoring metrics

    Args:
        client: DME API client
        obj_type_id:  Monitor object type ID(Required)

    Returns:
        Monitoring metric info,includes  indicator_ids  list
    """
    url = "/rest/metrics/v1/mgr-svc/obj-types/{obj_type_id}/indicators"

    response = client.get(url, params={"obj_type_id": obj_type_id})
    return response


def performance_list_object_types(client: DMEAPIClient, filter: str = None) -> dict:
    """
    Get all monitoringObject type

    Args:
        client: DME API client
        filter:  filter keyword for fuzzy matching zh_cn and en_us fields
                if provided,returns only matchesObject type

    Returns:
         monitorObject type list,includes  obj_type_id, parent_obj_type_id, resource_category,
        resource_provider, en_us, zh_cn, group_en_us, group_zh_cn 等 field
    """
    url = "/rest/metrics/v1/mgr-svc/obj-types"

    response = client.get(url)

    # if provided了 filter  parameter, filter result
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


# Health  related function
def health_query_data(client: DMEAPIClient, type: str, object_id: str, begin_time: int,
                      end_time: int, object_type: str, indicator: str = None) -> dict:
    """
    Query health-related data

     queryCapacity prediction, Performance prediction, Performance anomalyhealth-related data. 

    Args:
        client: DME API client
        type: Data type (Required) , Optional值: capacity_prediction (Capacity prediction) , performance_prediction (Performance prediction) , performance_anomaly (Performance anomaly) 
        object_id:  resource ID (Required, 1~256  characters) 
        begin_time: Start time (Required) , 自 1970 year(s) 1 month(s) 1 日 (00:00:00GMT) to current time in mssecond(s)数
        end_time: End time (Required) , 自 1970 year(s) 1 month(s) 1 日 (00:00:00GMT) to current time in mssecond(s)数
        object_type: Resource type (Required) 
        indicator: Resource typecorresponding metric (capacity_prediction 和 performance_prediction Required) 

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes Query result
    """
    if type == 'capacity_prediction':
        url = "/rest/pmmgmt/v1/prediction/query-capacity-predict"
    elif type == 'performance_prediction' or type == 'performance_predict':
        url = "/rest/pmmgmt/v1/prediction/query-performance-predict"
    elif type == 'performance_anomaly':
        url = "/rest/metrics/v1/performance/anomaly-data/query"
    else:
        raise ValueError(f"不 support的 type  parameter: {type}")

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
     queryobject health

    Query typeobjecthealth info. 

    Args:
        client: DME API client
        object_type: Object type (Required) 
                    Optional值: storage (Storage device) , storage_pool (Storage pool) , storage_host (Storage host) ,
                           storage_disk ( disk) , storage_port (Storage port) , fcswitch_port ( fiberSwitch port) ,
                           storage_file_system (Filesystem) , controller (Controller) , replication_cg (Remote replicationConsistency group) ,
                           volume (LUN) , tier (Service level) , datastore (Datastore) , virtual_machine (Virtual machine) ,
                           storage_name_space (Namespace) , storage_node ( storage node) , dpc (DPC) 
        object_name: Object name, supports fuzzy search (Optional,  max 256  characters) 
        object_ids: object resId  list, For batch exact lookup (Optional, supports up to 100 个 ID) 
        page_no: Page queryStart position (Optional, min: 1) 
        page_size: Items per page (Optional, 1~100, default 20) 
        sort_key: Sort field (Optional) , Sort by score, Optional值: health_score
        sort_dir: Sort method (Optional) , Optional值: asc, desc

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes object health list
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

    QueryobjectDeduction details under specified health dimension. 

    Args:
        client: DME API client
        object_id: object Id (Required, 1~128  characters) 
        object_type: Object type (Required) 
                    Optional值: storage, storage_pool, storage_host, storage_disk, storage_port,
                           fcswitch_port, storage_file_system, controller, replication_cg, volume,
                           tier, datastore, virtual_machine, storage_name_space, storage_node,
                           dpc, gfs, dpc_client, vbs_client
        health_dimension: Health dimension (Required) 
                        Optional值: alarm , performance_anomaly (Performance anomaly) ,
                              performance_prediction (Performance warning) , capacity_prediction (Capacity warning) 

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, Includes metric deduction list
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

    By task ID Query diagnosis task status.

    Args:
        client: DME API client
        task_id: task  ID(Required),1~128  characters

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        },includes :
        - task_id: task  ID
        - task_status: task  status,value range:
            - executing: Executing
            - failed:  failure
            - success:  success
            - waiting: Waiting
            - terminated:  terminated
        - task_result: task  result,value range:
            - un_analyzed: 未 analysis
            - warning:  warning
            - abnormal:  exception
            - event:  event
        - total_step_count:  total steps
        - finish_step_count: Completed step count
    """
    url = "/rest/dmegraphanalysis/v1/perf-tasks/query-status"

    payload = {
        "task_id": task_id
    }

    print(f" request URL: {url}")
    print(f"Request load:{json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


# ============================================================================
# Check policy subtopic functions
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
        policy_name: Policy name (supports fuzzy search, 1~256  characters) 
        exact_query:  name whetherexact match (true-exact match, false-fuzzy search) , default false
        status:  Policy status (normal, checking, failed, queued) 
        policy_type: Policy type (performance threshold, capacity threshold, availability, 
                    configuration- config, recyclable- recyclable resource, lowload- low load resource, 
                    performance_anomaly-Performance anomaly, performance_prediction-Performance warning, 
                    capacity_prediction-Capacity warning, history_performance-History performance, 
                    load imbalance, high-load resource) 
        policy_source:  source (pre-define, user-define) 
        alarm_type: Alarm type (violation- exception, alarm-alarm, event- event) 
        object_type: Object type (storage- storage, lun-Logical unit, host- host等) 
        page_no: Page number, 1~1000, default 1
        page_size: Items per page, 1~100, default 20
        sort_key: Sort field (last_check_time-Last check time, failed_count-Failed checksobjectcount) 
        sort_dir: Sort method (asc-ascending, desc-descending) 
        administrative_status: Management status (enable, disable) 
        policy_category:  check category (configuration, performance, capacity, faults, optimization) 
        object_category: Object type (Storage, IPSwitch, FCSwitch, 
                       Virtualization, Server, HCI-Hyperconverged, Client) 

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes  total (Total count) 和 policies ( policy list) 
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

    Execute specified check policy. 

    Args:
        client: DME API client
        policy_id:  policy ID (1~64  characters) 

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

    Enable specified check policy. 

    Args:
        client: DME API client
        policy_id:  policy ID (1~64  characters) 

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

    Disable specified check policy. 

    Args:
        client: DME API client
        policy_id:  policy ID (1~64  characters) 

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

    Delete check policy. 

    Args:
        client: DME API client
        policy_id:  policy ID (1~64  characters) 

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }
    """
    url = "/rest/policymgmt/v1/policies/{policy_id}"

    response = client.delete(url, params={"policy_id": policy_id})
    return response


# ============================================================================
# Check result subtopic functions
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

    Query check policy exception results, supports multiple filter criteria和Pagination. 

    Args:
        client: DME API client
        object_name: Object name (supports fuzzy search, 1~256  characters) 
        level:  Exception level (critical, major, minor, info) 
        object_ids: object ID  list ( max 100) 
        object_native_id: object nativeId (1~384  characters) 
        object_type: Object type (storage- storage, lun-Logical unit, host- host等) 
        policy_id:  policy ID (exact match, 1~64  characters) 
        policy_name: Policy name (supports fuzzy search, 1~256  characters) 
        policy_types: Policy type list ( max 30 个) 
        cause:  Exception cause (supports fuzzy search, 1~768  characters) 
        alarm_type: Alarm type (violation- exception, alarm-alarm, event- event) 
        first_occur_time: First exception time range ({beginTime, endTime}, UTC Timestamp, unit  ms) 
        last_occur_time: Last exceptionTime range ({beginTime, endTime}, UTC Timestamp, unit  ms) 
        page_no: Page number, 1~10000, default 1
        page_size: Items per page, 1~2000, default 20
        sort_key: Sort field (violation_count- Exception count) 
        sort_dir: Sort method (asc-ascending, desc-descending) 

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes  total (Total count) 和 results (Exception check result list) 
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

    Query check result details. 

    Args:
        client: DME API client
        check_result_id: Check result ID (1~64  characters) 

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, including check resultsDetails
    """
    url = "/rest/policymgmt/v1/abnormal-check-results/{check_result_id}"

    response = client.get(url, params={"check_result_id": check_result_id})
    return response


# Action list for CLI help
# ============================================================================
# Topology management subtopic functions
# ============================================================================

def topology_query_luns(client: DMEAPIClient, entry_objects: list, storage_pool_id: str,
               lun_name: str = None, san_type: str = None, page_size: int = 20, page_no: int = 1) -> dict:
    r"""
     query topology Lun  list

    via specified entryobjectQuery topology LUN  list. 

    Args:
        client: DME API client
        entry_objects: entryobject list (Required) ,  format: [{"id":"<entryObject ID>","type":"<entryObject type>"},...], Supported types: 
            - host:  host
            - storage: Storage device
            - host_group:  host组
            - lun: LUN
            - vm: Virtual machine
            - datastore: Datastore
            - application:  app
            - switch_port: Switch port
            - storage_pool: Storage pool
        storage_pool_id: Storage pool ID (Required) 
        lun_name: LUN  name, supports fuzzy match
        san_type: SAN  type, Optional值: ip_san, fc_san
        page_size: Items per page, 1~20, default 20
        page_no: Page queryStart position, default 1

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes LUN topology list
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

    print(f" request URL: {url}")
    print(f"Request load: {json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


def topology_query_san_path(client: DMEAPIClient, entry_objects: list, san_type: str = None) -> dict:
    r"""
     query SAN Path topology

    via specified entryobject query SAN Network from host toStorage pooltopology between. 
     supports IP_SAN and FC_SAN types. 

    Args:
        client: DME API client
        entry_objects: entryobject list (Required) ,  format: [{"id":"<entryObject ID>","type":"<entryObject type>"},...], Supported types: 
            - host:  host
            - storage: Storage device
            - lun: LUN
            - host_group:  host组
            - vm: Virtual machine
            - datastore: Datastore (仅 FC_SAN) 
            - application:  app (仅 FC_SAN) 
            - switch_port: Switch port (仅 FC_SAN) 
            - storage_pool: Storage pool
        san_type: SAN  type (Optional) , Optional值: ip_san, fc_san
                  - if not specified, calls both IP_SAN and FC_SAN APIs, combines results
                  -  specified为 ip_san 时,  only call IP_SAN API
                  -  specified为 fc_san 时,  only call FC_SAN API

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes  host到Storage pool topology: 
        - ip_san  data: 
          - switches: Switch list
          - hosts:  host list
          - storages:  storage list
          - switch_links: Switch connection list
          - port_links: Port connection list
        - fc_san  data: 
          - fabrics: fabric  list
          - hosts:  host list
          - storages:  storage list
    """
    result = {}

    #  if not specified san_type, call both simultaneously API
    if san_type is None:
        # Call IP_SAN API
        ip_san_url = "/rest/topomgmt/v1/topo-data/ipsan/host-storage/query"
        ip_san_payload = {"entry_objects": entry_objects}
        print(f" request URL: {ip_san_url}")
        print(f"Request load: {json.dumps(ip_san_payload, ensure_ascii=False, indent=2)}")
        ip_san_response = client.post(ip_san_url, body=ip_san_payload)
        result['ip_san'] = ip_san_response

        # Call FC_SAN API
        fc_san_url = "/rest/topomgmt/v1/topo-data/host-storage/query"
        fc_san_payload = {"entry_objects": entry_objects}
        print(f" request URL: {fc_san_url}")
        print(f"Request load: {json.dumps(fc_san_payload, ensure_ascii=False, indent=2)}")
        fc_san_response = client.post(fc_san_url, body=fc_san_payload)
        result['fc_san'] = fc_san_response

        return result

    # if specified san_type, only call the corresponding API
    elif san_type == 'ip_san':
        url = "/rest/topomgmt/v1/topo-data/ipsan/host-storage/query"
        payload = {"entry_objects": entry_objects}
        print(f" request URL: {url}")
        print(f"Request load: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        response = client.post(url, body=payload)
        return response

    elif san_type == 'fc_san':
        url = "/rest/topomgmt/v1/topo-data/host-storage/query"
        payload = {"entry_objects": entry_objects}
        print(f" request URL: {url}")
        print(f"Request load: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        response = client.post(url, body=payload)
        return response

    else:
        raise ValueError(f" invalid san_type  parameter: {san_type}, only supports: ip_san, fc_san")




def topology_query_vms(client: DMEAPIClient, entry_objects: list, host_id: str,
              vm_name: str = None, page_size: int = 20, page_no: int = 1) -> dict:
    r"""
    Query topology VM and virtual disk list, 或 query BMS Physical disk list below

    Query virtualization resources via specified entry, includes VM and virtual disk list, 
    or query BMS (bare metal server) physical disk list. 

    Args:
        client: DME API client
        entry_objects: entryobject list (Required) ,  format: [{"id":"<entryObject ID>","type":"<entryObject type>"},...], Supported types: 
            - vm: Virtual machine
            - host_group:  host组
            - host:  host
            - storage: Storage device
            - lun: LUN
            - datastore: Datastore
            - switch_port: Switch port
            - storage_pool: Storage pool
        host_id:  host ID (Required) 
        vm_name: Virtual machineName search parameter, supports fuzzy match
        page_size: Items per page, 1~20, default 20
        page_no: Page queryStart position, default 1

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes : 
        - total: Query resultTotal count
        - vms: VM list
        - disks: Physical hostAssociated physical disk list
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

    print(f" request URL: {url}")
    print(f"Request load: {json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


def topology_query_graph_path(client: DMEAPIClient, entry_res_type: str, entry_res_id: str,
                type: str = None, filter: list = None) -> dict:
    r"""
    Query topology library info

    via specified entry resourceQuery topology library info,  support NAS, K8s, DB 等Business type. 

    Args:
        client: DME API client
        entry_res_type: entryResource type (Required) , Supported types: 
            - storage_device: Storage device
            - disk:  disk
            - storage_pool: Storage pool
            - hyper_scale_pool:  large-scale pool
            - file_system: Filesystem
            - controller: Controller
            - eth_port:  ethernet port
            - ib_port: InfiniBand  port
            - logic_port: Logic port
            - ip_client: IP Client
            - dtree: Dtree
            - lun: LUN
            - k8s_application: K8s  app
            - k8s_workload: K8s  workload
            - k8s_pod: K8s Pod
            - k8s_pvc: K8s PVC
            - k8s_pv: K8s PV
            - k8s_cluster: K8s  cluster
            - k8s_node: K8s  node
            - k8s_vc_job: K8s VC task 
            - dturbo_client: DataTurbo Client
            - enclosures: Rack
            - eth_switch: Ethernet switch
            - storage_zone:  Storage zone
            - service_network: Service network
            - db_instance:  data库instance
            - db_node:  data库 node
        entry_res_id: entry resource ID (Required) 
        type: Business type, Optional值: nas, k8s, db
        filter: Filter condition list,  max 10 个

    Returns:
        {
            task_id: Task ID (string, 1~64 characters),
        }, includes : 
        - nodes:  node list, Each node contains id, type, label, sub_type
        - edges: edge list, each edge includes source, target, edge_type
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

    print(f" request URL: {url}")
    print(f"Request load: {json.dumps(payload, ensure_ascii=False, indent=2)}")

    response = client.post(url, body=payload)
    return response


# ============================================================================
# Action list for CLI help
# ============================================================================

ACTIONS = {
    'alarm_list': {
        'func': alarm_list,
        'description': 'Query alarm info(Current alarm,Optional择 whetherincludes History alarm)',
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
        'description': ' cancelAcknowledge alarm',
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
        'description': 'Query historyPerformance data',
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
        'description': 'List monitoringObject typeSupported monitoring metrics',
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
        'description': ' query SAN Path topology ( support IP_SAN 和 FC_SAN) ',
        'params': ['entry_objects', 'san_type'],
        'subtopic': 'topology'
    },
    'topology_query_luns': {
        'func': topology_query_luns,
        'description': ' query topology LUN  list',
        'params': ['entry_objects', 'storage_pool_id', 'lun_name', 'san_type', 'page_size', 'page_no'],
        'subtopic': 'topology'
    },
    'topology_query_vms': {
        'func': topology_query_vms,
        'description': 'Query topology VM and virtual disk list, 或 query BMS Physical disk list below',
        'params': ['entry_objects', 'host_id', 'vm_name', 'page_size', 'page_no'],
        'subtopic': 'topology'
    },
    'topology_query_graph_path': {
        'func': topology_query_graph_path,
        'description': 'Query topology library info ( support NAS, K8s, DB 等Business type) ',
        'params': ['entry_res_type', 'entry_res_id', 'type', 'filter'],
        'subtopic': 'topology'
    },
    # health subtopic actions
    'health_query_data': {
        'func': health_query_data,
        'description': 'Query health-related data (Capacity prediction/Performance prediction/Performance anomaly) ',
        'params': ['type', 'object_id', 'begin_time', 'end_time', 'object_type', 'indicator'],
        'subtopic': 'health'
    },
    'health_show_score': {
        'func': health_show_score,
        'description': ' queryobject health',
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
