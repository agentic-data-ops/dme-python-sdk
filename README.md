# DME Python SDK

## What is this
- Provide a Python client (`pydme/client.py`) to access DME RESTful APIs
- Provide a Python client to access Huawei flash storage RESTful APIs by using tokens acquired from DME for login, to avoid remember username and password of each storage

## Project Structure

```
.
├── pydme/                  # Python package
│   ├── __init__.py
│   └── client.py           # Python client library
└── README.md
```

## How to use

### Install

Install directly from GitHub:

```bash
pip install git+https://github.com/agentic-data-ops/dme-python-sdk.git
```

Or install with editable mode for development:

```bash
git clone https://github.com/agentic-data-ops/dme-python-sdk.git
cd dme-python-sdk
pip install -e .
```

### Quick start

Set up environment variables:

```
DME_API_ENDPOINT=https://dme-float-ip:26335
DME_API_USERNAME=your-username
DME_API_PASSWORD=your-password

# Or use auth token instead of username/password:
# DME_API_AUTH_TOKEN=your-token
```

#### Initialize client

```python
from pydme.client import DMEAPIClient

client = DMEAPIClient()
client.login()
```

#### Query and categorize storage devices

```python
import json

# Query storage device list
storage_list = client.get("/rest/storagemgmt/v1/storages").get("datas", [])
print(json.dumps(storage_list, indent=2))

# Categorize by type
dorado_storage_list = [
    storage for storage in storage_list if storage.get("owning_ne_type") == "dorado"
]
pacific_storage_list = [
    storage for storage in storage_list if storage.get("owning_ne_type") == "OceanStorPacific"
]
```

#### Query storage device details

```python
storage_id = dorado_storage_list[0].get("id")
storage_detail = client.get(
    "/rest/storagemgmt/v1/storages/{storage_id}/detail",
    params={"storage_id": storage_id}
)
print(json.dumps(storage_detail, indent=2))
```

#### Call storage device native APIs

```python
# Get a token-authenticated client for a specific storage device
storage_client = client.get_storage_client(storage_id)
lun_list = storage_client.get("/lun", params={"filter": "NAME:lun"}).get("data", [])
print(json.dumps(lun_list, indent=2))
```

## To do tasks
- [ ] Provide atom actions for frequently used DME APIs, like SAN and NAS provisioning, and storage device management, performance and topology data query
- [ ] Provide atom actions for frequently used storage APIs.

