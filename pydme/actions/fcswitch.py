"""
FC Switch related operations
"""

import sys
import os

from pydme.client import DMEAPIClient


def list(client: DMEAPIClient, name: str = None, 
                  page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch query switches
    
    Args:
        client: DME API client
        name: switch name (Optional, supports fuzzy query)
        page_no: page number for paginated query, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            total: total count (integer),
            fcswitches: switch list (List<FcSwitchInfo>). parameter format: [{
                id: switch ID (string),
                name: switch name (string),
                status: running status (string),
            }, ...],
        }
    """
    url = "/rest/fcswitchmgmt/v1/fcswitches/list"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if name is not None:
        payload['name'] = name
    
    response = client.post(url, body=payload)
    return response


def sync(client: DMEAPIClient, switch_id: str) -> dict:
    """
    Sync specified switch
    
    Args:
        client: DME API client
        switch_id: switch ID (Required)
    
    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/fcswitchmgmt/v1/fcswitches/{switch_id}/sync"
    
    response = client.post(url, params={"switch_id": switch_id})
    return response


def port_list(client: DMEAPIClient, switch_id: str = None,
                       port_name: str = None, page_no: int = 1, 
                       page_size: int = 20) -> dict:
    """
    Batch query switch ports
    
    Args:
        client: DME API client
        switch_id: switch ID (Optional)
        port_name: port name (Optional)
        page_no: page number for paginated query, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, includes total and ports fields
    """
    url = "/rest/fcswitchmgmt/v1/fcswitches/ports/query"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if switch_id is not None:
        payload['switch_id'] = switch_id
    if port_name is not None:
        payload['port_name'] = port_name
    
    response = client.post(url, body=payload)
    return response



def controller_list(client: DMEAPIClient, switch_id: str = None,
                             page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch query switch control processors
    
    Args:
        client: DME API client
        switch_id: switch ID (Optional)
        page_no: page number for paginated query, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, includes total and controllers fields
    """
    url = "/rest/fcswitchmgmt/v1/fcswitches/controllers/query"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if switch_id is not None:
        payload['switch_id'] = switch_id
    
    response = client.post(url, body=payload)
    return response


def fabric_list(client: DMEAPIClient, name: str = None, 
                page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch query fabrics
    
    Args:
        client: DME API client
        name: fabric name (Optional, supports fuzzy query)
        page_no: page number for paginated query, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, includes total and fabrics fields
    """
    url = "/rest/fcswitchmgmt/v1/fabrics/list"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    if name is not None:
        payload['name'] = name
    
    response = client.post(url, body=payload)
    return response


def fabric_show_ports(client: DMEAPIClient, fabric_id: str,
                      page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query port list of specified fabric

    Args:
        client: DME API client
        fabric_id: fabric ID (Required)
        page_no: page number for paginated query, default 1
        page_size: items per page, 1~1000, default 20

    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, includes total and ports fields
    """
    url = "/rest/fcswitchmgmt/v1/fabrics/{fabric_id}/ports/list"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload, params={"fabric_id": fabric_id})
    return response


def fabric_backup(client: DMEAPIClient, fabric_id: str, backup_server_id: str,
                  backup_type: str = "full") -> dict:
    """
    Execute fabric configuration file backup
    
    Args:
        client: DME API client
        fabric_id: fabric ID (Required)
        backup_server_id: backup server ID (Required)
        backup_type: backup type, default full (full/incremental)
    
    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }
    """
    url = "/rest/fcswitchmgmt/v1/fabrics/{fabric_id}/backup"
    
    payload = {
        'backupRequest': {
            'backupServerId': backup_server_id,
            'backupType': backup_type
        }
    }
    
    response = client.post(url, body=payload, params={"fabric_id": fabric_id})
    return response


# ==================== VSAN related operations ====================

def vsan_list(client: DMEAPIClient, page_no: int = 1, page_size: int = 20) -> dict:
    """
    Query VSAN list
    
    Args:
        client: DME API client
        page_no: page number for paginated query, default 1
        page_size: items per page, 1~1000, default 20
    
    Returns:
        {
            task_id: task ID (string, 1~64 characters),
        }, includes total and vsans fields
    """
    url = "/rest/fcswitchmgmt/v1/vsans/query"
    
    payload = {
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload)
    return response


# ==================== zone related operations ====================

def zone_list(client: DMEAPIClient, fabric_wwn: str = None, name: str = None,
              cfg_name: str = None, zone_set: str = None, active_status: list = None,
              member_count: int = None, sort_key: str = None, sort_dir: str = None,
              page_no: int = None, page_size: int = None) -> dict:
    """
    Batch query zone

    ⚠️  Note: FC switch configuration operations are synchronous. It is recommended to set the request timeout to 90 seconds or more (--timeout 90). 

    Args:
        client: DME API client
        fabric_wwn: fabric WWN (Optional, string, 1~1024 characters)
        name: zone name (Optional, string, 1~1024 characters), supports fuzzy query
        cfg_name: CFG name (Optional, string, 0~1024 characters), supports fuzzy query
        zone_set: zone set (Optional, string, 0~1024 characters), supports fuzzy query
        active_status: zone status list (Optional, List<string>, max array members: 2). valid values: ACTIVATED, INATIVATED
        member_count: member count (Optional, int32, 0~2147483647)
        sort_key: sort field (Optional, string), valid values: member_count
        sort_dir: sort direction (Optional, string), valid values: asc, desc, default asc
        page_no: page number for paginated query (Optional, int32, 1~65535)
        page_size: items per page (Optional, int32, 1~1000)

    Returns:
        {
            total: zone count (int32),
            zones: zone list (List<zoneBaseInfoResponse>). parameter format: [{
                id: zone id (string, 1~128 characters),
                fabric_id: fabric id (string, 0~128 characters),
                name: zone name (string, 1~64 characters),
                active_status: zone status (string, 1~16 characters). valid values: ACTIVATED, INATIVATED,
                member_count: member count (integer),
                cfg_name: CFG name (string, 0~256 characters),
                zone_set: zone set (string, 0~256 characters),
                modifiable: whether the zone can be modified (boolean, true/false),
                zone_type: zone type (string). valid values: regular, user_specified_peer_zone, target_driven_peer_zone,
            }, ...],
        }
    """
    url = "/rest/fcswitchmgmt/v1/zones/list"

    payload = {}

    if fabric_wwn is not None:
        payload['fabric_wwn'] = fabric_wwn
    if name is not None:
        payload['name'] = name
    if cfg_name is not None:
        payload['cfg_name'] = cfg_name
    if zone_set is not None:
        payload['zone_set'] = zone_set
    if active_status is not None:
        payload['active_status'] = active_status
    if member_count is not None:
        payload['member_count'] = member_count
    if sort_key is not None:
        payload['sort_key'] = sort_key
    if sort_dir is not None:
        payload['sort_dir'] = sort_dir
    if page_no is not None:
        payload['page_no'] = page_no
    if page_size is not None:
        payload['page_size'] = page_size

    response = client.post(url, body=payload)
    return response


def zone_create(client: DMEAPIClient, name: str, fabric_wwn: str = None,
                vsan_wwn: str = None, wwn_members: list = None,
                port_members: list = None, fwwn_members: list = None,
                fcid_members: list = None, alias_members: list = None,
                device_alias_members: list = None) -> dict:
    """
    Create zone
    Create a zone instance in the fabric, must include one of WWN members, port members, or alias members. 

    ⚠️  Note: FC switch configuration operations are synchronous. It is recommended to set the request timeout to 90 seconds or more (--timeout 90). 

    Args:
        client: DME API client
        name: zone name (Required, string, 1~64 characters, regex ^[A-Za-z][A-Za-z0-9_^$\\-]*$)
        fabric_wwn: fabric WWN (Required, string, 1~128 characters, regex ^[A-Za-z0-9:]+$)
        vsan_wwn: VSAN WWN (Optional, string, 1~32 characters). Conditionally required: must pass when creating zone in VSAN
        wwn_members: WWN member list (Optional, List<string>, max array members: 100)
        port_members: port member list (Optional, List<PortMemberRequest>, max array members: 100). parameter format: [{
                domain_id: domain ID (Optional, int32, 0~65535),
                port_index: port number (conditionally required, int32, 0~65535), set for Brocade switches,
                port_name: switch port (conditionally required, string, 1~32 characters, regex ^[a-fA-F0-9/]+$), set for Cisco switches,
                switch_wwn: switch WWN (Optional, string, 1~32 characters), set for Cisco switches when specifying remote switch,
            }, ...]
        fwwn_members: FWWN member list (Optional, List<string>, max array members: 100)
        fcid_members: FCID member list (Optional, List<string>, max array members: 100)
        alias_members: alias member list (Optional, List<string>, max array members: 100)
        device_alias_members: device alias member list (Optional, List<string>, max array members: 100)

    Returns:
        {
            id: zone id (string, 1~64 characters),
            zone_name: zone name (string, 1~64 characters),
        }
    """
    url = "/rest/fcswitchmgmt/v1/zones"

    payload = {
        'name': name
    }

    # Provide at least one of fabric_wwn or vsan_wwn
    if fabric_wwn is not None:
        payload['fabric_wwn'] = fabric_wwn
    if vsan_wwn is not None:
        payload['vsan_wwn'] = vsan_wwn

    # member list
    if wwn_members is not None:
        payload['wwn_members'] = wwn_members
    if port_members is not None:
        payload['port_members'] = port_members
    if fwwn_members is not None:
        payload['fwwn_members'] = fwwn_members
    if fcid_members is not None:
        payload['fcid_members'] = fcid_members
    if alias_members is not None:
        payload['alias_members'] = alias_members
    if device_alias_members is not None:
        payload['device_alias_members'] = device_alias_members

    response = client.post(url, body=payload)
    return response


def zone_modify(client: DMEAPIClient, zone_id: str, zone_name: str = None,
                wwn_members: dict = None, alias_members: dict = None,
                fwwn_members: dict = None, port_members: dict = None,
                fcid_members: dict = None, device_alias_members: dict = None) -> dict:
    """
    Modify zone
    Modify zone name or change members. This operation modifies the zone name or changes members on the specified switch. 

    ⚠️  Note: FC switch configuration operations are synchronous. It is recommended to set the request timeout to 90 seconds or more (--timeout 90). 

    Args:
        client: DME API client
        zone_id: zone ID (Required, string, regex ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$)
        zone_name: zone name (Optional, string, 1~64 characters, regex ^[A-Za-z][A-Za-z0-9_^$\\-]*$)
        wwn_members: WWN member modification (Optional, ModifyWwnMembersRequest object). parameter format: {
                added_members: WWN members to add (Optional, List<string>, max array members: 100),
                removed_members: WWN members to remove (Optional, List<string>, max array members: 100),
            }
        port_members: port member modification (Optional, ModifyPortMembersRequest object). parameter format: {
                added_members: port members to add (Optional, List<PortMemberRequest>, max array members: 100). attribute format: {
                    domain_id: domain ID (Optional, int32, 0~65535),
                    port_index: port number (conditionally required, int32, 0~65535), set for Brocade switches,
                    port_name: switch port (conditionally required, string, 1~32 characters, regex ^[a-fA-F0-9/]+$), set for Cisco switches,
                    switch_wwn: switch WWN (Optional, string, 1~32 characters),
                },
                removed_members: port members to remove (Optional, List<PortMemberRequest>, max array members: 100),
            }
        alias_members: alias member modification (Optional, ModifyAliasMembersRequest object). parameter format: {
                added_members: alias members to add (Optional, List<string>, max array members: 100),
                removed_members: alias members to remove (Optional, List<string>, max array members: 100),
            }
        fwwn_members: FWWN member modification (Optional, ModifyFwwnMembersRequest object). parameter format: {
                added_members: FWWN members to add (Optional, List<string>, max array members: 100),
                removed_members: FWWN members to remove (Optional, List<string>, max array members: 100),
            }
        fcid_members: FCID member modification (Optional, ModifyFcidMembersRequest object). parameter format: {
                added_members: FCID members to add (Optional, List<string>, max array members: 100),
                removed_members: FCID members to remove (Optional, List<string>, max array members: 100),
            }
        device_alias_members: device alias member modification (Optional, ModifyDeviceAliasMembersRequest object). parameter format: {
                added_members: device alias members to add (Optional, List<string>, max array members: 100),
                removed_members: device alias members to remove (Optional, List<string>, max array members: 100),
            }

    Returns:
        None. 
    """
    url = "/rest/fcswitchmgmt/v1/zones/{zone_id}"

    payload = {}
    if zone_name is not None:
        payload['zoneName'] = zone_name
    if wwn_members is not None:
        payload['wwn_members'] = wwn_members
    if alias_members is not None:
        payload['alias_members'] = alias_members
    if fwwn_members is not None:
        payload['fwwn_members'] = fwwn_members
    if port_members is not None:
        payload['port_members'] = port_members
    if fcid_members is not None:
        payload['fcid_members'] = fcid_members
    if device_alias_members is not None:
        payload['device_alias_members'] = device_alias_members

    response = client.put(url, body=payload, params={"zone_id": zone_id})
    return response


def zone_delete(client: DMEAPIClient, zone_id: str) -> dict:
    """
    Delete zone
    This operation deletes the zone on the specified switch. 

    ⚠️  Note: FC switch configuration operations are synchronous. It is recommended to set the request timeout to 90 seconds or more (--timeout 90). 

    Args:
        client: DME API client
        zone_id: zone ID (Required, string, regex ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$)

    Returns:
        None. 
    """
    url = "/rest/fcswitchmgmt/v1/zones/{zone_id}"
    
    response = client.delete(url, params={"zone_id": zone_id})
    return response


def zone_batch_create(client: DMEAPIClient, is_active_zone: str, zones: list) -> dict:
    """
    Batch create zones

    ⚠️  Note: FC switch configuration operations are synchronous. It is recommended to set the request timeout to 90 seconds or more (--timeout 90). 

    Args:
        client: DME API client
        is_active_zone: whether to activate zones (Required, boolean), valid values: true, false
        zones: zone create request list (List<zoneCreateRequest>, Required, min array items: 1, max array members: 20). parameter format: [{
                fabric_wwn: fabric WWN (Required, string, 1~128 characters, regex ^[A-Za-z0-9:]+$),
                name: zone name (Required, string, 1~64 characters, regex ^[A-Za-z][A-Za-z0-9_^$\\-]*$),
                vsan_wwn: VSAN WWN (Optional, string, 1~32 characters). Conditionally required: must pass when creating ZONE in VSAN,
                wwn_members: WWN member list (Optional, List<string>, max array members: 100),
                port_members: port member list (Optional, List<PortMemberRequest>, max array members: 100). attribute format: [{
                    domain_id: domain ID (Optional, int32, 0~65535),
                    port_index: port number (conditionally required, int32, 0~65535), set for Brocade switches,
                    port_name: switch port (conditionally required, string, 1~32 characters, regex ^[a-fA-F0-9/]+$), set for Cisco switches,
                    switch_wwn: switch WWN (Optional, string, 1~32 characters),
                }, ...],
                alias_members: alias member list (Optional, List<string>, max array members: 100),
                device_alias_members: device alias member list (Optional, List<string>, max array members: 100),
                fwwn_members: FWWN member list (Optional, List<string>, max array members: 100),
                fcid_members: FCID member list (Optional, List<string>, max array members: 100),
            }, ...]

    Returns:
        None. 
    """
    url = "/rest/fcswitchmgmt/v1/zones/batch-create"

    payload = {
        'is_active_zone': is_active_zone,
        'zone_list': zones
    }

    response = client.post(url, body=payload)
    return response


def zone_show_members(client: DMEAPIClient, zone_id: str, type: str = None) -> dict:
    """
    Query zone members
    Query members in a zone, supports port members, WWN members, and alias members. 

    ⚠️  Note: FC switch configuration operations are synchronous. It is recommended to set the request timeout to 90 seconds or more (--timeout 90). 

    Args:
        client: DME API client
        zone_id: zone ID (Required, string, regex ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$)
        type: member type (Optional, string). valid values: port, wwn, alias. Returns all types when not specified

    Returns:
        {
            total: WWN member count (int32, when type=wwn),
            wwn_members: WWN member list (List<GetWwnMembersResponse>, when type=wwn). parameter format: [{
                member_wwn: member WWN (string, 1~128 characters),
            }, ...],
            total: port member count (int32, when type=port),
            port_members: port member list (List<zonePortMemberResponse>, when type=port). parameter format: [{
                domain_id: domain id (int32, 0~65535),
                port_index: switch port index (int32, 0~65535),
                port_name: port name (string, 1~256 characters),
                switch_ip: switch IP of the port (string, 1~32 characters),
                switch_name: switch name of the port (string, 1~2048 characters),
            }, ...],
            total: alias member count (int32, when type=alias),
            alias_members: alias member list (List<AliasBaseInfo>, when type=alias). parameter format: [{
                id: alias id (string, 1~64 characters),
                role: member type (string). valid values: regular, principal, non_principal,
                type: alias member type (string). valid values: wwn, port, fwwn, fcid, ip-address, device-alias, domain-id, symbolic-node-name, empty, mixed,
                fabric_id: fabric id (string, 0~64 characters),
                fabric_wwn: fabric WWN (string, 1~32 characters),
                name: alias name (string, 1~128 characters),
                member_count: alias member count (int32, 0~65535),
                modifiable: whether the alias can be modified (boolean, true/false),
            }, ...],
            members: all members list (List, when type not specified),
        }
    """
    result = {'port_members': [], 'wwn_members': [], 'alias_members': []}

    # Query members of the corresponding type based on type parameter
    if type is None or type == 'port':
        url = "/rest/fcswitchmgmt/v1/zones/{zone_id}/port-members/list"
        payload = {}
        response = client.post(url, body=payload, params={"zone_id": zone_id})
        if response.get('port_members'):
            result['port_members'] = response.get('port_members')

    if type is None or type == 'wwn':
        url = "/rest/fcswitchmgmt/v1/zones/{zone_id}/wwn-members/list"
        response = client.get(url, params={"zone_id": zone_id})
        if response.get('wwn_members'):
            result['wwn_members'] = response.get('wwn_members')

    if type is None or type == 'alias':
        url = "/rest/fcswitchmgmt/v1/zones/{zone_id}/alias-members/list"
        payload = {}
        response = client.post(url, body=payload, params={"zone_id": zone_id})
        if response.get('alias_members'):
            result['alias_members'] = response.get('alias_members')

    # If type is specified, return only members of that type
    if type == 'port':
        return {'port_members': result['port_members']}
    elif type == 'wwn':
        return {'wwn_members': result['wwn_members']}
    elif type == 'alias':
        return {'alias_members': result['alias_members']}
    else:
        # Return all members
        all_members = result['port_members'] + result['wwn_members'] + result['alias_members']
        return {'members': all_members}


# ==================== Alias related operations ====================

def alias_list(client: DMEAPIClient, fabric_wwn: str,
               page_no: int = 1, page_size: int = 20) -> dict:
    """
    Batch query aliases

    ⚠️  Note: FC switch configuration operations are synchronous. It is recommended to set the request timeout to 90 seconds or more (--timeout 90). 

    Args:
        client: DME API client
        fabric_wwn: fabric WWN (Required, string, 1~1024 characters), obtained from query fabric interface
        name: alias name (Optional, string, 1~1024 characters), supports fuzzy query
        member_count: member count (Optional, int32, 0~65535)
        page_no: page number for paginated query (Optional, int32, 1~2147483647), default 1
        page_size: items per page (Optional, int32, 1~1000), default 20
        sort_key: sort field (Optional, string), valid values: member_count
        sort_dir: sort direction (Optional, string), valid values: asc, desc, default asc

    Returns:
        {
            total: alias total (int32),
            aliases: alias list (List<AliasBaseInfoResponse>). parameter format: [{
                id: alias id (string, 1~64 characters),
                fabric_id: fabric id (string, 1~64 characters),
                fabric_wwn: fabric WWN (string, 1~32 characters),
                name: alias name (string, 1~128 characters),
                member_count: member count (int32, 0~65535),
                modifiable: whether the alias can be modified (boolean, true/false),
            }, ...],
        }
    """
    url = "/rest/fcswitchmgmt/v1/aliases/list"
    
    payload = {
        'fabric_wwn': fabric_wwn,
        'page_no': page_no,
        'page_size': page_size
    }
    
    response = client.post(url, body=payload)
    return response


def alias_create(client: DMEAPIClient, name: str, fabric_wwn: str = None,
                 vsan_wwn: str = None, wwn_members: list = None,
                 port_members: list = None, fwwn_members: list = None,
                 fcid_members: list = None, device_alias_members: list = None) -> dict:
    """
    Create alias
    This operation creates an alias on the specified switch. 

    ⚠️  Note: FC switch configuration operations are synchronous. It is recommended to set the request timeout to 90 seconds or more (--timeout 90). 

    Args:
        client: DME API client
        name: alias name (Required, string, 1~64 characters, regex ^[A-Za-z0-9][A-Za-z0-9_^$\\-]*$)
        fabric_wwn: fabric WWN (conditionally required, string, 1~32 characters), must pass when creating alias in fabric
        vsan_wwn: VSAN WWN (conditionally required, string, 1~32 characters), must pass when creating alias in VSAN
        wwn_members: WWN member list (Optional, List<string>, max array members: 100). For Cisco switches, PWWN members use this parameter. Huawei/Brocade switches: at least one of WWN members or port members required; Cisco switches: at least one of PWWN, FWWN, port, FCID, device alias required
        fwwn_members: FWWN member list (Optional, List<string>, max array members: 100). Cisco switches: at least one of PWWN, FWWN, port, FCID, device alias required
        port_members: port member list (Optional, List<PortMemberRequest>, max array members: 100). parameter format: [{
                domain_id: domain ID (Optional, int32, 0~65535),
                port_index: port number (conditionally required, int32, 0~65535), set when configuring port members on Brocade switches,
                port_name: switch port (conditionally required, string, 1~32 characters, regex ^[a-fA-F0-9/]+$), set when configuring port members on Cisco switches,
                switch_wwn: switch WWN (Optional, string, 1~32 characters), set for Cisco switches when specifying remote switch,
            }, ...]
        fcid_members: FCID member list (Optional, List<string>, max array members: 100). Cisco switches: at least one of PWWN, FWWN, port, FCID, device alias required
        device_alias_members: device alias member list (Optional, List<string>, max array members: 100). Cisco switches: at least one of PWWN, FWWN, port, FCID, device alias required

    Returns:
        {
            id: alias id (string, 1~64 characters),
        }
    """
    url = "/rest/fcswitchmgmt/v1/aliases"
    
    payload = {
        'name': name
    }
    
    # Provide at least one of fabric_wwn or vsan_wwn
    if fabric_wwn is not None:
        payload['fabric_wwn'] = fabric_wwn
    if vsan_wwn is not None:
        payload['vsan_wwn'] = vsan_wwn
    
    # member list
    if wwn_members is not None:
        payload['wwn_members'] = wwn_members
    if port_members is not None:
        payload['port_members'] = port_members
    if fwwn_members is not None:
        payload['fwwn_members'] = fwwn_members
    if fcid_members is not None:
        payload['fcid_members'] = fcid_members
    if device_alias_members is not None:
        payload['device_alias_members'] = device_alias_members
    
    response = client.post(url, body=payload)
    return response


def alias_modify(client: DMEAPIClient, alias_id: str, name: str = None,
                 wwn_members: dict = None, fwwn_members: dict = None,
                 port_members: dict = None, fcid_members: dict = None,
                 device_alias_members: dict = None) -> dict:
    """
    Modify alias
    Modify alias members. Brocade switches support WWN member and port member modification; Cisco switches support PWWN, FWWN, port, FCID, and device alias member modification. 

    ⚠️  Note: FC switch configuration operations are synchronous. It is recommended to set the request timeout to 90 seconds or more (--timeout 90). 

    Args:
        client: DME API client
        alias_id: alias ID (Required, string, regex ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$)
        name: alias name (Optional, string, 1~64 characters, regex ^[A-Za-z0-9][A-Za-z0-9_^$\\-]*$). Conditionally optional: Cisco switches support modifying alias name, Brocade switches do not
        wwn_members: WWN member modification (Optional, WwnMembersRequest object). parameter format: {
                added_members: WWN members to add (Optional, List<string>, max array members: 100),
                removed_members: WWN members to remove (Optional, List<string>, max array members: 100),
            }
        fwwn_members: FWWN member modification (Optional, FwwnMembersRequest object). parameter format: {
                added_members: FWWN members to add (Optional, List<string>, max array members: 100),
                removed_members: FWWN members to remove (Optional, List<string>, max array members: 100),
            }
        port_members: port member modification (Optional, PortMembersRequest object). parameter format: {
                added_members: port members to add (Optional, List<PortMemberRequest>, max array members: 100). attribute format: {
                    domain_id: domain ID (Optional, int32, 0~65535),
                    port_index: port number (conditionally required, int32, 0~65535), set for Brocade switches,
                    port_name: switch port (conditionally required, string, 1~32 characters, regex ^[a-fA-F0-9/]+$), set for Cisco switches,
                    switch_wwn: switch WWN (Optional, string, 1~32 characters),
                },
                removed_members: port members to remove (Optional, List<PortMemberRequest>, max array members: 100),
            }
        fcid_members: FCID member modification (Optional, FcidMembersRequest object). parameter format: {
                added_members: FCID members to add (Optional, List<string>, max array members: 100),
                removed_members: FCID members to remove (Optional, List<string>, max array members: 100),
            }
        device_alias_members: device alias member modification (Optional, DeviceAliasMembersRequest object). parameter format: {
                added_members: device alias members to add (Optional, List<string>, max array members: 100),
                removed_members: device alias members to remove (Optional, List<string>, max array members: 100),
            }

    Returns:
        None. 
    """
    url = "/rest/fcswitchmgmt/v1/aliases/{alias_id}"
    
    payload = {}
    if name is not None:
        payload['name'] = name
    if wwn_members is not None:
        payload['wwn_members'] = wwn_members
    if fwwn_members is not None:
        payload['fwwn_members'] = fwwn_members
    if port_members is not None:
        payload['port_members'] = port_members
    if fcid_members is not None:
        payload['fcid_members'] = fcid_members
    if device_alias_members is not None:
        payload['device_alias_members'] = device_alias_members
    
    response = client.put(url, body=payload, params={"alias_id": alias_id})
    return response


def alias_delete(client: DMEAPIClient, alias_id: str) -> dict:
    """
    Delete alias
    This operation deletes the alias on the specified switch. 

    ⚠️  Note: FC switch configuration operations are synchronous. It is recommended to set the request timeout to 90 seconds or more (--timeout 90). 

    Args:
        client: DME API client
        alias_id: alias ID (Required, string, regex ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$)

    Returns:
        None. 
    """
    url = "/rest/fcswitchmgmt/v1/aliases/{alias_id}"
    
    response = client.delete(url, params={"alias_id": alias_id})
    return response


def alias_show_members(client: DMEAPIClient, alias_id: str, type: str = None) -> dict:
    """
    Query alias members
    Query members in an Alias, supports querying port members and WWN members. 

    ⚠️  Note: FC switch configuration operations are synchronous. It is recommended to set the request timeout to 90 seconds or more (--timeout 90). 

    Args:
        client: DME API client
        alias_id: alias ID (Required, string, regex ^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$|^[a-fA-F0-9]{32}$)
        type: member type (Optional, string). valid values: port, wwn. Returns all types when not specified

    Returns:
        {
            total: WWN member total (int32, when type=wwn),
            wwn_member: WWN member list (List<GetWwnMembersResponse>, when type=wwn). parameter format: [{
                member_wwn: member WWN (string, 1~128 characters),
            }, ...],
            total: port member total (int32, when type=port),
            port_members: port member list (List<PortMemberInfoResponse>, when type=port). parameter format: [{
                domain_id: domain id (int32, 0~65535),
                port_index: switch port index (int32, 0~65535),
                port_name: switch port name (string, 1~128 characters),
                switch_ip: switch IP of the port (string, 1~32 characters),
                switch_name: switch name of the port (string, 1~2048 characters),
            }, ...],
            members: all members list (List, when type not specified),
        }
    """
    result = {'port_members': [], 'wwn_members': []}

    # If type is specified or defaults to None, query members of the corresponding type
    if type is None or type == 'port':
        url = "/rest/fcswitchmgmt/v1/aliases/{alias_id}/port-members/list"
        payload = {}
        response = client.post(url, body=payload, params={"alias_id": alias_id})
        if response.get('port_members'):
            result['port_members'] = response.get('port_members')

    if type is None or type == 'wwn':
        url = "/rest/fcswitchmgmt/v1/aliases/{alias_id}/wwn-members/list"
        response = client.get(url, params={"alias_id": alias_id})
        # API returns field wwn_member (singular)
        if response.get('wwn_member'):
            result['wwn_members'] = response.get('wwn_member')

    # If type is specified, return only members of that type
    if type == 'port':
        return {'port_members': result['port_members']}
    elif type == 'wwn':
        return {'wwn_members': result['wwn_members']}
    else:
        # Return all members
        all_members = result['port_members'] + result['wwn_members']
        return {'members': all_members}


# ACTIONS dictionary, defines all available actions
ACTIONS = {
    'list': {
        'func': list,
        'description': 'Batch query FC switches',
        'params': ['name', 'page_no', 'page_size'],
        'subtopic': None
    },
    'sync': {
        'func': sync,
        'description': 'Sync switch configuration',
        'params': ['switch_id'],
        'subtopic': None
    },
    'port_list': {
        'func': port_list,
        'description': 'Query switch port list',
        'params': ['switch_id', 'port_name', 'page_no', 'page_size'],
        'subtopic': 'port'
    },
    'controller_list': {
        'func': controller_list,
        'description': 'Query switch controller list',
        'params': ['switch_id', 'page_no', 'page_size'],
        'subtopic': 'controller'
    },
    'fabric_list': {
        'func': fabric_list,
        'description': 'Batch query fabrics',
        'params': ['name', 'page_no', 'page_size'],
        'subtopic': 'fabric'
    },
    'fabric_show_ports': {
        'func': fabric_show_ports,
        'description': 'Query fabric port list',
        'params': ['fabric_id', 'page_no', 'page_size'],
        'subtopic': 'fabric'
    },
    'fabric_backup': {
        'func': fabric_backup,
        'description': 'Backup fabric configuration',
        'params': ['fabric_id', 'backup_server_id', 'backup_type'],
        'subtopic': 'fabric'
    },
    'vsan_list': {
        'func': vsan_list,
        'description': 'Batch query VSANs',
        'params': ['page_no', 'page_size'],
        'subtopic': 'vsan'
    },
    'zone_list': {
        'func': zone_list,
        'description': 'Batch query zones',
        'params': ['zone_name', 'page_no', 'page_size'],
        'subtopic': 'zone'
    },
    'zone_create': {
        'func': zone_create,
        'description': 'Create zone',
        'params': ['name', 'fabric_wwn', 'vsan_wwn', 'wwn_members', 'port_members', 'fwwn_members', 'fcid_members', 'device_alias_members'],
        'subtopic': 'zone'
    },
    'zone_modify': {
        'func': zone_modify,
        'description': 'Modify zone',
        'params': ['zone_id', 'zone_name', 'wwn_members', 'fwwn_members', 'port_members', 'fcid_members', 'device_alias_members'],
        'subtopic': 'zone'
    },
    'zone_delete': {
        'func': zone_delete,
        'description': 'Delete zone',
        'params': ['zone_id'],
        'subtopic': 'zone'
    },
    'zone_batch_create': {
        'func': zone_batch_create,
        'description': 'Batch create zones',
        'params': ['is_active_zone', 'zones'],
        'subtopic': 'zone'
    },
    'zone_show_members': {
        'func': zone_show_members,
        'description': 'Query zone members',
        'params': ['zone_id', 'type'],
        'subtopic': 'zone'
    },
    'alias_list': {
        'func': alias_list,
        'description': 'Batch query aliases',
        'params': ['fabric_wwn', 'page_no', 'page_size'],
        'subtopic': 'alias'
    },
    'alias_create': {
        'func': alias_create,
        'description': 'Create alias',
        'params': ['name', 'fabric_wwn', 'vsan_wwn', 'wwn_members', 'port_members', 'fwwn_members', 'fcid_members', 'device_alias_members'],
        'subtopic': 'alias'
    },
    'alias_modify': {
        'func': alias_modify,
        'description': 'Modify alias',
        'params': ['alias_id', 'name', 'wwn_members', 'fwwn_members', 'port_members', 'fcid_members', 'device_alias_members'],
        'subtopic': 'alias'
    },
    'alias_delete': {
        'func': alias_delete,
        'description': 'Delete alias',
        'params': ['alias_id'],
        'subtopic': 'alias'
    },
    'alias_show_members': {
        'func': alias_show_members,
        'description': 'Query alias members',
        'params': ['alias_id', 'type'],
        'subtopic': 'alias'
    },
}
