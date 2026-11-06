"""
Local mock data store for pydme topics without a real DME API (memstore).

Data file: ~/.config/pydme/mock/memstore.json (JSON array of memstore objects).

Structure (see .reasonix/plans/600-memstore-impl.md):

  [
    {
      "id": "<uuid>",
      "name": "<memstore_name>",              # 1~128 chars
      "disks": [
        {"id": "<uuid>",
         "location": "FRAME<0~47>.SLOT<0~11>",
         "capacity": 16384 | 32768 | 65536,   # GB
         "pools": [{"pool": "<pool_id>", "capacity": "<GB, 1~disk capacity>"}]}
      ],
      "pools": [
        {"id": "<uuid>",
         "name": "<pool_name>",               # 1~128 chars
         "disks": [{"disk": "<disk_id>", "capacity": "<GB, 1~disk capacity>"}],
         "namespaces": [
           {"id": "<uuid>",
            "name": "<namespace_name>",       # 1~128 chars
            "capacity": "<GB, 1~pool capacity>",
            "used_capacity": "<GB, >=0>",
            "eviction": "<1~99>",             # %
            "retention": "<hours, >1>",
            "clients": [{"ip": "<client_ip>", "type": "ip|ip_segment"}]}
         ]}
      ]
    }
  ]

Derived values are computed on read and never stored:
  disk.allocated_capacity     = sum(disk.pools[].capacity)
  pool.capacity               = sum(pool.disks[].capacity)
  pool.used_capacity          = sum(namespaces[].capacity)
  memstore.raw_capacity       = sum(disks[].capacity)
  memstore.pool_capacity      = sum(pools[].capacity)
  memstore.pool_used_capacity = sum(pools[].used_capacity)

Each memstore numbers its FRAMEs independently starting from FRAME0 (each
FRAME holds SLOT_COUNT=12 disks), so disk locations may repeat across
memstores; within one memstore they are unique.

The file is created with a self-consistent sample dataset on first access.
"""

import json
import os
import sys
import uuid
from pathlib import Path

MEMSTORE_MOCK_DIR = Path.home() / '.config' / 'pydme' / 'mock'
MEMSTORE_MOCK_FILE = MEMSTORE_MOCK_DIR / 'memstore.json'

#: allowed single-disk capacities, GB
DISK_CAPACITIES = (16384, 32768, 65536)
#: legal disk location grid (48 frames x 12 slots = 576 slots)
FRAME_COUNT = 48
SLOT_COUNT = 12


def new_uuid() -> str:
    """A random uuid4 string."""
    return str(uuid.uuid4())


def sample_memstores() -> list:
    """A self-consistent seed dataset used when the mock file does not exist."""
    memstore_id = new_uuid()
    disk1_id = new_uuid()
    disk2_id = new_uuid()
    pool_id = new_uuid()
    ns_id = new_uuid()
    return [
        {
            'id': memstore_id,
            'name': 'demo-memstore',
            'disks': [
                {'id': disk1_id, 'location': 'FRAME0.SLOT0', 'capacity': 32768,
                 'pools': [{'pool': pool_id, 'capacity': 1024}]},
                {'id': disk2_id, 'location': 'FRAME0.SLOT1', 'capacity': 32768,
                 'pools': [{'pool': pool_id, 'capacity': 1024}]},
            ],
            'pools': [
                {
                    'id': pool_id,
                    'name': 'demo-pool',
                    'disks': [
                        {'disk': disk1_id, 'capacity': 1024},
                        {'disk': disk2_id, 'capacity': 1024},
                    ],
                    'namespaces': [
                        {
                            'id': ns_id,
                            'name': 'demo-ns',
                            'capacity': 512,
                            'used_capacity': 256,
                            'eviction': 80,
                            'retention': 24,
                            'clients': [{'ip': '192.168.1.10', 'type': 'ip'}],
                        }
                    ],
                }
            ],
        }
    ]


def ensure_memstore_mock() -> list:
    """Load the mock store, creating it with the sample dataset when missing."""
    if not MEMSTORE_MOCK_FILE.exists():
        data = sample_memstores()
        try:
            MEMSTORE_MOCK_DIR.mkdir(parents=True, exist_ok=True)
            _write(data)
        except OSError as e:
            print(f'Warning: cannot create {MEMSTORE_MOCK_FILE} ({e}), '
                  f'using in-memory sample data', file=sys.stderr)
        return data
    return load_memstores()


def load_memstores() -> list:
    """Read the memstore list from the mock file.

    Falls back to the sample dataset (without overwriting the file) when the
    file is missing, unreadable or malformed.
    """
    try:
        text = MEMSTORE_MOCK_FILE.read_text(encoding='utf-8')
    except FileNotFoundError:
        return ensure_memstore_mock()
    except OSError as e:
        print(f'Warning: cannot read {MEMSTORE_MOCK_FILE} ({e}), '
              f'using sample data', file=sys.stderr)
        return sample_memstores()
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        print(f'Warning: invalid JSON in {MEMSTORE_MOCK_FILE} ({e}), '
              f'using sample data', file=sys.stderr)
        return sample_memstores()
    if not isinstance(data, list):
        print(f'Warning: {MEMSTORE_MOCK_FILE} must contain a JSON array, '
              f'using sample data', file=sys.stderr)
        return sample_memstores()
    return data


def save_memstores(data: list) -> None:
    """Atomically write the memstore list back to the mock file."""
    try:
        MEMSTORE_MOCK_DIR.mkdir(parents=True, exist_ok=True)
        _write(data)
    except OSError as e:
        raise RuntimeError(f'cannot write {MEMSTORE_MOCK_FILE}: {e}')


def _write(data: list) -> None:
    tmp = MEMSTORE_MOCK_DIR / (MEMSTORE_MOCK_FILE.name + '.tmp')
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n',
                   encoding='utf-8')
    os.replace(tmp, MEMSTORE_MOCK_FILE)


# ---------------------------------------------------------------------------
# validation helpers
# ---------------------------------------------------------------------------

def validate_name(value, field='name') -> str:
    """Validate a name field: required, 1~128 characters."""
    if value is None or str(value).strip() == '':
        raise ValueError(f'{field} is required')
    if len(str(value)) > 128:
        raise ValueError(f'{field} must be 1~128 characters')
    return str(value)


def validate_disk_capacity(value) -> int:
    """Validate disk capacity: one of 16384 / 32768 / 65536 (GB)."""
    try:
        value = int(value)
    except (TypeError, ValueError):
        raise ValueError(f'disk_size must be an integer, '
                         f'one of {list(DISK_CAPACITIES)} (GB)')
    if value not in DISK_CAPACITIES:
        raise ValueError(f'disk_size must be one of {list(DISK_CAPACITIES)} (GB), '
                         f'got {value}')
    return value


def validate_int_range(value, field, minimum, maximum=None) -> int:
    """Validate an integer field within [minimum, maximum] (or >= minimum)."""
    try:
        value = int(value)
    except (TypeError, ValueError):
        raise ValueError(f'{field} must be an integer')
    if value < minimum or (maximum is not None and value > maximum):
        rng = f'{minimum}~{maximum}' if maximum is not None else f'>={minimum}'
        raise ValueError(f'{field} must be {rng}, got {value}')
    return value


def require_id(value, field='id') -> str:
    """Validate a required id field."""
    if value is None or str(value).strip() == '':
        raise ValueError(f'{field} is required')
    return str(value)


# ---------------------------------------------------------------------------
# disk location allocation (per-memstore independent FRAME numbering)
# ---------------------------------------------------------------------------

def all_locations():
    """Yield every legal disk location: FRAME0.SLOT0 .. FRAME47.SLOT11."""
    for frame in range(FRAME_COUNT):
        for slot in range(SLOT_COUNT):
            yield f'FRAME{frame}.SLOT{slot}'


def alloc_locations(used: set, count: int) -> list:
    """Allocate `count` unused disk locations within one memstore.

    Each memstore numbers its FRAMEs independently starting from FRAME0, so
    `used` is the set of locations already taken by THIS memstore only.

    Raises:
        ValueError: when fewer than `count` free slots remain.
    """
    free = [loc for loc in all_locations() if loc not in used]
    if count > len(free):
        raise ValueError(f'not enough free disk locations: requested {count}, '
                         f'available {len(free)}')
    return free[:count]


# ---------------------------------------------------------------------------
# lookups (return references so callers can mutate in place)
# ---------------------------------------------------------------------------

def find_memstore(memstores, memstore_id):
    """Return the memstore dict by id, or None."""
    for ms in memstores:
        if ms.get('id') == memstore_id:
            return ms
    return None


def find_disk(memstores, disk_id):
    """Return (memstore, disk) by disk id, or (None, None)."""
    for ms in memstores:
        for disk in ms.get('disks', []):
            if disk.get('id') == disk_id:
                return ms, disk
    return None, None


def find_pool(memstores, pool_id):
    """Return (memstore, pool) by pool id, or (None, None)."""
    for ms in memstores:
        for pool in ms.get('pools', []):
            if pool.get('id') == pool_id:
                return ms, pool
    return None, None


def find_namespace(memstores, namespace_id):
    """Return (memstore, pool, namespace) by namespace id, or (None, None, None)."""
    for ms in memstores:
        for pool in ms.get('pools', []):
            for ns in pool.get('namespaces', []):
                if ns.get('id') == namespace_id:
                    return ms, pool, ns
    return None, None, None


# ---------------------------------------------------------------------------
# derived values (capacities, GB)
# ---------------------------------------------------------------------------

def disk_allocated_capacity(disk) -> int:
    """GB allocated from the disk by pools: sum(disk.pools[].capacity)."""
    return sum(int(p.get('capacity', 0)) for p in disk.get('pools', []))


def disk_free_capacity(disk) -> int:
    """GB still free on the disk."""
    return int(disk.get('capacity', 0)) - disk_allocated_capacity(disk)


def pool_capacity(pool) -> int:
    """Total pool capacity: sum(pool.disks[].capacity)."""
    return sum(int(d.get('capacity', 0)) for d in pool.get('disks', []))


def pool_used_capacity(pool) -> int:
    """GB allocated from the pool by namespaces: sum(namespaces[].capacity)."""
    return sum(int(n.get('capacity', 0)) for n in pool.get('namespaces', []))


def pool_free_capacity(pool) -> int:
    """GB still free in the pool."""
    return pool_capacity(pool) - pool_used_capacity(pool)


def memstore_raw_capacity(memstore) -> int:
    """Bare capacity: sum of all disk capacities."""
    return sum(int(d.get('capacity', 0)) for d in memstore.get('disks', []))


def memstore_pool_capacity(memstore) -> int:
    """Pool capacity: sum of all pool capacities."""
    return sum(pool_capacity(p) for p in memstore.get('pools', []))


def memstore_pool_used_capacity(memstore) -> int:
    """Pool used capacity: sum of all pools' used capacities."""
    return sum(pool_used_capacity(p) for p in memstore.get('pools', []))
