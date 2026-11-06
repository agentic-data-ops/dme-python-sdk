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

def _normalize_locations(disks) -> list:
    """Accept a list of locations, a JSON array string or a comma-separated string."""
    if disks is None:
        raise ValueError('disks is required: a list of disk locations')
    if isinstance(disks, str):
        text = disks.strip()
        if text.startswith('['):
            try:
                disks = json.loads(text)
            except json.JSONDecodeError:
                raise ValueError(f'invalid disks JSON: {text}')
        else:
            disks = [part.strip() for part in text.split(',') if part.strip()]
    if not isinstance(disks, builtins.list) or not disks:
        raise ValueError('disks must be a non-empty list of disk locations')
    return [str(location) for location in disks]


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


def _split_space(size: int, free: list, locations: list) -> dict:
    """Split `size` GB over disks proportional to their free space.

    The returned mapping sums to `size` and never exceeds a disk's free space.
    """
    total = sum(free)
    if total < size:
        raise ValueError(f'not enough free space on the selected disks: '
                         f'requested {size} GB, available {total} GB')
    alloc = [int(size * f // total) for f in free]  # proportional, floor
    remainder = size - sum(alloc)
    while remainder > 0:
        candidates = [i for i in range(len(free)) if free[i] - alloc[i] >= 1]
        if not candidates:
            raise ValueError(f'cannot distribute {size} GB over the selected disks')
        idx = max(candidates, key=lambda i: free[i] - alloc[i])
        alloc[idx] += 1
        remainder -= 1
    return {loc: a for loc, a in zip(locations, alloc) if a > 0}


# ---------------------------------------------------------------------------
# memstore (direct actions)
# ---------------------------------------------------------------------------

def add(client: DMEAPIClient = None, name: str = None,
        num_of_disks: int = None, disk_size: int = None) -> dict:
    name = mockdata.validate_name(name)
    num_of_disks = mockdata.validate_int_range(num_of_disks, 'num_of_disks', 1)
    disk_size = mockdata.validate_disk_size(disk_size)

    memstores = mockdata.ensure_memstore_mock()
    locations = mockdata.alloc_locations(memstores, num_of_disks)

    memstore = {
        'id': mockdata.new_uuid(),
        'name': name,
        'disks': [
            {'id': mockdata.new_uuid(), 'location': location,
             'size': disk_size, 'pools': []}
            for location in locations
        ],
        'pools': [],
    }
    memstores.append(memstore)
    mockdata.save_memstores(memstores)
    return memstore


def list(client: DMEAPIClient = None, name: str = None) -> dict:
    memstores = mockdata.ensure_memstore_mock()
    if name is not None:
        keyword = str(name)
        memstores = [ms for ms in memstores
                     if keyword in str(ms.get('name', ''))]
    return {'memstores': memstores}


def delete(client: DMEAPIClient = None, id: str = None) -> dict:
    memstore_id = mockdata.require_id(id)
    memstores = mockdata.ensure_memstore_mock()
    memstore = mockdata.find_memstore(memstores, memstore_id)
    if memstore is None:
        raise ValueError(f'memstore {memstore_id} not found')
    if memstore.get('pools'):
        raise ValueError(f'memstore {memstore_id} still has pools, '
                         f'delete them first')
    memstores = [ms for ms in memstores if ms.get('id') != memstore_id]
    mockdata.save_memstores(memstores)
    return {'success': True, 'id': memstore_id, 'message': 'memstore deleted'}


# ---------------------------------------------------------------------------
# memstore disk subtopic
# ---------------------------------------------------------------------------

def disk_list(client: DMEAPIClient = None) -> dict:
    memstores = mockdata.ensure_memstore_mock()
    disks = []
    for ms in memstores:
        for disk in ms.get('disks', []):
            disks.append({
                'id': disk.get('id'),
                'location': disk.get('location'),
                'size': disk.get('size'),
                'allocated_size': mockdata.disk_allocated_size(disk),
            })
    return {'disks': disks}


# ---------------------------------------------------------------------------
# memstore pool subtopic
# ---------------------------------------------------------------------------

def pool_create(client: DMEAPIClient = None, name: str = None,
                size: int = None, disks: list = None) -> dict:
    name = mockdata.validate_name(name)
    size = mockdata.validate_int_range(size, 'size', 1)
    locations = _normalize_locations(disks)

    memstores = mockdata.ensure_memstore_mock()
    targets = []  # [(memstore, disk)] aligned with locations
    for location in locations:
        ms, disk = mockdata.find_disk_by_location(memstores, location)
        if disk is None:
            raise ValueError(f'disk location {location} not found')
        targets.append((ms, disk))

    owners = {ms.get('id') for ms, _ in targets}
    if len(owners) > 1:
        raise ValueError('all disks of a pool must belong to the same memstore')
    memstore = targets[0][0]

    free = [mockdata.disk_free_size(disk) for _, disk in targets]
    allocations = _split_space(size, free, locations)

    pool_id = mockdata.new_uuid()
    pool_disks = []
    for location, (_, disk) in zip(locations, targets):
        space = allocations.get(location, 0)
        if space <= 0:
            continue
        pool_disks.append({'disk': disk.get('id'), 'space': space})
        disk.setdefault('pools', []).append({'pool': pool_id, 'space': space})

    pool = {
        'id': pool_id,
        'name': name,
        'disks': pool_disks,
        'namespaces': [],
    }
    memstore.setdefault('pools', []).append(pool)
    mockdata.save_memstores(memstores)
    return pool


def pool_list(client: DMEAPIClient = None, name: str = None) -> dict:
    memstores = mockdata.ensure_memstore_mock()
    pools = []
    for ms in memstores:
        for pool in ms.get('pools', []):
            if name is not None and str(name) not in str(pool.get('name', '')):
                continue
            pools.append({
                'id': pool.get('id'),
                'name': pool.get('name'),
                'size': mockdata.pool_size(pool),
                'allocated_size': mockdata.pool_allocated_size(pool),
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
                     name: str = None, space: int = None,
                     eviction: int = None, retention: int = None,
                     clients: list = None) -> dict:
    pool_id = mockdata.require_id(pool_id, 'pool_id')
    name = mockdata.validate_name(name)
    space = mockdata.validate_int_range(space, 'space', 1)
    eviction = mockdata.validate_int_range(eviction, 'eviction', 1, 99)
    retention = mockdata.validate_int_range(retention, 'retention', 2)  # >1
    clients = _normalize_clients(clients)

    memstores = mockdata.ensure_memstore_mock()
    _, pool = mockdata.find_pool(memstores, pool_id)
    if pool is None:
        raise ValueError(f'pool {pool_id} not found')
    free = mockdata.pool_free_size(pool)
    if space > free:
        raise ValueError(f'not enough free space in pool {pool_id}: '
                         f'requested {space} GB, available {free} GB')

    namespace = {
        'id': mockdata.new_uuid(),
        'name': name,
        'space': space,
        'eviction': eviction,
        'retention': retention,
        'clients': clients,
    }
    pool.setdefault('namespaces', []).append(namespace)
    mockdata.save_memstores(memstores)
    return namespace


def namespace_list(client: DMEAPIClient = None, name: str = None,
                   pool_id: str = None) -> dict:
    memstores = mockdata.ensure_memstore_mock()
    namespaces = []
    for ms in memstores:
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
                    'space': ns.get('space'),
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
    pool['namespaces'] = [n for n in pool.get('namespaces', [])
                          if n.get('id') != namespace_id]
    mockdata.save_memstores(memstores)
    return {'success': True, 'id': namespace_id, 'message': 'namespace deleted'}
