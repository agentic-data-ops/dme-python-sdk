"""
Hyper-converged infrastructure (HCI) related operations
"""

from pydme.client import DMEAPIClient


def list(client: DMEAPIClient, hci_id_list: list = None, name: str = None,
         ip_address: str = None, sync_status: list = None, model: list = None,
         version: list = None, sort_dir: str = "desc",
         sort_key: str = "last_modified", page_no: int = 1, page_size: int = 1000,
         dc_id: str = None, is_support_market_place: bool = None) -> dict:
    url = "/rest/hcimgmt/v1/hcis/query"

    body_params = {
        'page_no': page_no,
        'page_size': page_size,
        'sort_dir': sort_dir,
        'sort_key': sort_key
    }

    if hci_id_list is not None:
        body_params['hci_id_list'] = hci_id_list
    if name is not None:
        body_params['name'] = name
    if ip_address is not None:
        body_params['ip_address'] = ip_address
    if sync_status is not None:
        body_params['sync_status'] = sync_status
    if model is not None:
        body_params['model'] = model
    if version is not None:
        body_params['version'] = version
    if dc_id is not None:
        body_params['dc_id'] = dc_id
    if is_support_market_place is not None:
        body_params['is_support_market_place'] = is_support_market_place

    response = client.post(url, body=body_params)
    return response


def show(client: DMEAPIClient, hci_id: str) -> dict:
    url = "/rest/hcimgmt/v1/hcis/{hci_id}"

    response = client.get(url, params={"hci_id": hci_id})
    return response


def cluster_list(client: DMEAPIClient, hci_id: str, sort_dir: str = "asc",
                 sort_key: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    url = "/rest/vmmgmt/v1/hci-vm-clusters/query"

    body_params = {
        'hci_id': hci_id,
        'page_no': page_no,
        'page_size': page_size,
        'sort_dir': sort_dir
    }

    if sort_key is not None:
        body_params['sort_key'] = sort_key

    response = client.post(url, body=body_params)
    return response


def vswitch_list(client: DMEAPIClient, hci_id: str, sort_dir: str = "asc",
                 sort_key: str = None, page_no: int = 1, page_size: int = 20) -> dict:
    url = "/rest/vmmgmt/v1/hci-dvswitchs/query"

    body_params = {
        'hci_id': hci_id,
        'page_no': page_no,
        'page_size': page_size,
        'sort_dir': sort_dir
    }

    if sort_key is not None:
        body_params['sort_key'] = sort_key

    response = client.post(url, body=body_params)
    return response


def storage_list(client: DMEAPIClient, hci_id: str) -> dict:
    url = "/rest/storagemgmt/v2/hci-storages/query"

    body_params = {
        'hci_id': hci_id
    }

    response = client.post(url, body=body_params)
    return response
