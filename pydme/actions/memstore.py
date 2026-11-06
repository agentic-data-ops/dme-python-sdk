"""
Memory storage (memstore) management operations (mock-backed)

All memstore actions work on the local mock store at
~/.config/pydme/mock/memstore.json — no DME API exists for them yet, and the
CLI skips the DME connection/login for this topic (client is unused).
"""

import builtins
import json

from pydme import mockdata
from pydme.client import DMEAPIClient


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _normalize_clients(clients) -> list:
    """Validate clients: a list of {ip, type} objects (type: ip | ip_segment)."""
    if clients is None:
        return []
    if isinstance(clients, str):
        try:
            clients = json.loads(clients)
        except json.JSONDecodeError:
            raise ValueError(f'invalid clients JSON: {clients}')
    if not isinstance(clients, builtins.list):
        raise ValueError('clients must be a list of {ip, type} objects')
    normalized = []
    for client in clients:
        if not isinstance(client, dict) or 'ip' not in client:
            raise ValueError('each client must be an object with "ip" and "type"')
        client_type = client.get('type', 'ip')
        if client_type not in ('ip', 'ip_segment'):
            raise ValueError(f'invalid client type {client_type!r}, '
                             f'must be "ip" or "ip_segment"')
        normalized.append({'ip': str(client['ip']), 'type': client_type})
    return normalized


def _memstore_summary(ms) -> dict:
    """Summary response of one memstore (no disk/pool lists)."""
    return {
        'id': ms.get('id'),
        'name': ms.get('name'),
        'raw_capacity': mockdata.memstore_raw_capacity(ms),
        'pool_capacity': mockdata.memstore_pool_capacity(ms),
        'pool_used_capacity': mockdata.memstore_pool_used_capacity(ms),
    }


# ---------------------------------------------------------------------------
# memstore (direct actions)
# ---------------------------------------------------------------------------

def add(client: DMEAPIClient = None, name: str = None,
        num_of_disks: int = None, disk_size: int = None) -> dict:
    name = mockdata.validate_name(name)
    num_of_disks = mockdata.validate_int_range(num_of_disks, 'num_of_disks', 1)
    disk_size = mockdata.validate_disk_capacity(disk_size)

    memstores = mockdata.ensure_memstore_mock()
    # each memstore numbers its FRAMEs independently from FRAME0
    locations = mockdata.alloc_locations(set(), num_of_disks)

    memstore = {
        'id': mockdata.new_uuid(),
        'name': name,
        'disks': [
            {'id': mockdata.new_uuid(), 'location': location,
             'capacity': disk_size, 'pools': []}
            for location in locations
        ],
        'pools': [],
    }
    memstores.append(memstore)
    mockdata.save_memstores(memstores)
    return _memstore_summary(memstore)


def list(client: DMEAPIClient = None, name: str = None) -> dict:
    memstores = mockdata.ensure_memstore_mock()
    if name is not None:
        keyword = str(name)
        memstores = [ms for ms in memstores
                     if keyword in str(ms.get('name', ''))]
    return {'memstores': [_memstore_summary(ms) for ms in memstores]}


def delete(client: DMEAPIClient = None, id: str = None) -> dict:
    memstore_id = mockdata.require_id(id)
    memstores = mockdata.ensure_memstore_mock()
    memstore = mockdata.find_memstore(memstores, memstore_id)
    if memstore is None:
        raise ValueError(f'memstore {memstore_id} not found')
    if memstore.get('pools'):
        raise ValueError(f'memstore {memstore_id} still has pools, '
                         f'delete them first')
    memstore_name = memstore.get('name', '')
    memstores = [ms for ms in memstores if ms.get('id') != memstore_id]
    mockdata.save_memstores(memstores)
    return {'success': True, 'id': memstore_id,
            'message': f'memstore deleted: {memstore_name}'}


# ---------------------------------------------------------------------------
# memstore disk subtopic
# ---------------------------------------------------------------------------

def disk_list(client: DMEAPIClient = None, storage_id: str = None) -> dict:
    memstores = mockdata.ensure_memstore_mock()
    disks = []
    for ms in memstores:
        if storage_id is not None and ms.get('id') != storage_id:
            continue
        for disk in ms.get('disks', []):
            disks.append({
                'id': disk.get('id'),
                'storage_id': ms.get('id'),
                'storage_name': ms.get('name'),
                'location': disk.get('location'),
                'capacity': disk.get('capacity'),
                'allocated_capacity': mockdata.disk_allocated_capacity(disk),
            })
    return {'disks': disks}


def disk_show(client: DMEAPIClient = None, id: str = None) -> dict:
    disk_id = mockdata.require_id(id)
    memstores = mockdata.ensure_memstore_mock()
    memstore, disk = mockdata.find_disk(memstores, disk_id)
    if disk is None:
        raise ValueError(f'disk {disk_id} not found')
    pools_by_id = {p.get('id'): p for p in memstore.get('pools', [])}
    pools = []
    for entry in disk.get('pools', []):
        pool = pools_by_id.get(entry.get('pool'))
        pools.append({
            'pool_id': entry.get('pool'),
            'pool_name': pool.get('name') if pool else None,
            'allocated_capacity': entry.get('capacity'),
        })
    return {
        'id': disk.get('id'),
        'storage_id': memstore.get('id'),
        'storage_name': memstore.get('name'),
        'location': disk.get('location'),
        'capacity': disk.get('capacity'),
        'allocated_capacity': mockdata.disk_allocated_capacity(disk),
        'pools': pools,
    }


# ---------------------------------------------------------------------------
# memstore pool subtopic
# ---------------------------------------------------------------------------

def _pool_detail(memstore, pool) -> dict:
    """Pool detail response (pool list fields + disk allocations + namespaces)."""
    disks_by_id = {d.get('id'): d for d in memstore.get('disks', [])}
    disks = []
    for entry in pool.get('disks', []):
        disk = disks_by_id.get(entry.get('disk'))
        disks.append({
            'disk_id': entry.get('disk'),
            'location': disk.get('location') if disk else None,
            'allocated_capacity': entry.get('capacity'),
        })
    namespaces = []
    for ns in pool.get('namespaces', []):
        namespaces.append({
            'id': ns.get('id'),
            'name': ns.get('name'),
            'capacity': ns.get('capacity'),
            'used_capacity': ns.get('used_capacity', 0),
        })
    return {
        'id': pool.get('id'),
        'name': pool.get('name'),
        'capacity': mockdata.pool_capacity(pool),
        'used_capacity': mockdata.pool_used_capacity(pool),
        'disks': disks,
        'namespaces': namespaces,
    }


def pool_create(client: DMEAPIClient = None, storage_id: str = None,
                name: str = None, capacity: int = None,
                num_of_disks: int = None) -> dict:
    storage_id = mockdata.require_id(storage_id, 'storage_id')
    name = mockdata.validate_name(name)
    capacity = mockdata.validate_int_range(capacity, 'capacity', 1)
    num_of_disks = mockdata.validate_int_range(num_of_disks, 'num_of_disks', 1)

    memstores = mockdata.ensure_memstore_mock()
    memstore = mockdata.find_memstore(memstores, storage_id)
    if memstore is None:
        raise ValueError(f'memstore {storage_id} not found')
    disks = memstore.get('disks', [])
    if num_of_disks > len(disks):
        raise ValueError(f'not enough disks in memstore {storage_id}: '
                         f'requested {num_of_disks}, available {len(disks)}')

    # pick the disks with the lowest allocated capacity, then split the pool
    # capacity evenly across them
    candidates = sorted(disks, key=lambda d: mockdata.disk_allocated_capacity(d))
    candidates = candidates[:num_of_disks]
    base, remainder = divmod(capacity, num_of_disks)
    shares = [base + 1 if i < remainder else base
              for i in range(num_of_disks)]
    for disk, share in zip(candidates, shares):
        free = mockdata.disk_free_capacity(disk)
        if share > free:
            raise ValueError(f'disk {disk.get("location")} has only {free} GB '
                             f'free, cannot allocate {share} GB for the pool')

    pool_id = mockdata.new_uuid()
    pool_disks = []
    for disk, share in zip(candidates, shares):
        pool_disks.append({'disk': disk.get('id'), 'capacity': share})
        disk.setdefault('pools', []).append({'pool': pool_id, 'capacity': share})

    pool = {
        'id': pool_id,
        'name': name,
        'disks': pool_disks,
        'namespaces': [],
    }
    memstore.setdefault('pools', []).append(pool)
    mockdata.save_memstores(memstores)
    return _pool_detail(memstore, pool)


def pool_show(client: DMEAPIClient = None, id: str = None) -> dict:
    pool_id = mockdata.require_id(id)
    memstores = mockdata.ensure_memstore_mock()
    memstore, pool = mockdata.find_pool(memstores, pool_id)
    if pool is None:
        raise ValueError(f'pool {pool_id} not found')
    return _pool_detail(memstore, pool)


def pool_list(client: DMEAPIClient = None, storage_id: str = None,
              name: str = None) -> dict:
    memstores = mockdata.ensure_memstore_mock()
    pools = []
    for ms in memstores:
        if storage_id is not None and ms.get('id') != storage_id:
            continue
        for pool in ms.get('pools', []):
            if name is not None and str(name) not in str(pool.get('name', '')):
                continue
            pools.append({
                'id': pool.get('id'),
                'name': pool.get('name'),
                'capacity': mockdata.pool_capacity(pool),
                'used_capacity': mockdata.pool_used_capacity(pool),
            })
    return {'pools': pools}


def pool_delete(client: DMEAPIClient = None, id: str = None) -> dict:
    pool_id = mockdata.require_id(id)
    memstores = mockdata.ensure_memstore_mock()
    memstore, pool = mockdata.find_pool(memstores, pool_id)
    if pool is None:
        raise ValueError(f'pool {pool_id} not found')
    if pool.get('namespaces'):
        raise ValueError(f'pool {pool_id} still has namespaces, '
                         f'delete them first')
    memstore['pools'] = [p for p in memstore.get('pools', [])
                         if p.get('id') != pool_id]
    # release the disk-side allocations (keep disk.pools <-> pool.disks in sync)
    for entry in pool.get('disks', []):
        disk_id = entry.get('disk')
        for disk in memstore.get('disks', []):
            if disk.get('id') == disk_id:
                disk['pools'] = [p for p in disk.get('pools', [])
                                 if p.get('pool') != pool_id]
    mockdata.save_memstores(memstores)
    return {'success': True, 'id': pool_id, 'message': 'pool deleted'}


# ---------------------------------------------------------------------------
# memstore namespace subtopic
# ---------------------------------------------------------------------------

def namespace_create(client: DMEAPIClient = None, pool_id: str = None,
                     name: str = None, capacity: int = None,
                     eviction: int = None, retention: int = None,
                     clients: list = None) -> dict:
    pool_id = mockdata.require_id(pool_id, 'pool_id')
    name = mockdata.validate_name(name)
    capacity = mockdata.validate_int_range(capacity, 'capacity', 1)
    eviction = mockdata.validate_int_range(eviction, 'eviction', 1, 99)
    retention = mockdata.validate_int_range(retention, 'retention', 2)  # >1
    clients = _normalize_clients(clients)

    memstores = mockdata.ensure_memstore_mock()
    _, pool = mockdata.find_pool(memstores, pool_id)
    if pool is None:
        raise ValueError(f'pool {pool_id} not found')
    free = mockdata.pool_free_capacity(pool)
    if capacity > free:
        raise ValueError(f'not enough free capacity in pool {pool_id}: '
                         f'requested {capacity} GB, available {free} GB')

    namespace = {
        'id': mockdata.new_uuid(),
        'name': name,
        'capacity': capacity,
        'used_capacity': 0,
        'eviction': eviction,
        'retention': retention,
        'clients': clients,
    }
    pool.setdefault('namespaces', []).append(namespace)
    mockdata.save_memstores(memstores)
    return namespace


def namespace_list(client: DMEAPIClient = None, storage_id: str = None,
                   name: str = None, pool_id: str = None) -> dict:
    memstores = mockdata.ensure_memstore_mock()
    namespaces = []
    for ms in memstores:
        if storage_id is not None and ms.get('id') != storage_id:
            continue
        for pool in ms.get('pools', []):
            if pool_id is not None and pool.get('id') != pool_id:
                continue
            for ns in pool.get('namespaces', []):
                if name is not None and str(name) not in str(ns.get('name', '')):
                    continue
                namespaces.append({
                    'id': ns.get('id'),
                    'pool_id': pool.get('id'),
                    'pool_name': pool.get('name'),
                    'name': ns.get('name'),
                    'capacity': ns.get('capacity'),
                    'used_capacity': ns.get('used_capacity', 0),
                    'eviction': ns.get('eviction'),
                    'retention': ns.get('retention'),
                    'clients': ns.get('clients', []),
                })
    return {'namespaces': namespaces}


def namespace_delete(client: DMEAPIClient = None, id: str = None) -> dict:
    namespace_id = mockdata.require_id(id)
    memstores = mockdata.ensure_memstore_mock()
    _, pool, ns = mockdata.find_namespace(memstores, namespace_id)
    if ns is None:
        raise ValueError(f'namespace {namespace_id} not found')
    namespace_name = ns.get('name', '')
    pool['namespaces'] = [n for n in pool.get('namespaces', [])
                          if n.get('id') != namespace_id]
    mockdata.save_memstores(memstores)
    return {'success': True, 'id': namespace_id,
            'message': f'namespace deleted: {namespace_name}'}
