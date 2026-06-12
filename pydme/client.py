import json
import requests
import time
import logging
import sys
from abc import abstractmethod
import os

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

LOG = logging.getLogger(__name__)


class BaseClient:

    def __init__(
        self,
        endpoint: str,
        headers: dict = {
            "Content-Type": "application/json;charset=utf8",
            "Accept": "application/json",
        },
        verify: bool = False,
        timeout: int = 30,
        session_timeout: int = 900,
        enable_log=True,
    ):
        self.endpoint = endpoint
        self.headers = headers
        self.verify = verify
        self.timeout = timeout
        self.session_timeout = session_timeout
        self.last_accessed = 0
        self.enable_log = enable_log

    @abstractmethod
    def login(self):
        """Set base_url and headers after login"""
        pass

    def get(self, path: str, params: dict = None) -> dict | str:
        return self.request("GET", path, params)

    def post(self, path: str, params: dict = None, body: dict = None) -> dict | str:
        return self.request("POST", path, params, body)

    def put(self, path: str, params: dict = None, body: dict = None) -> dict | str:
        return self.request("PUT", path, params, body)

    def delete(self, path: str, params: dict = None) -> dict | str:
        return self.request("DELETE", path, params)

    def request(
        self,
        method: str,
        path: str,
        params: dict = None,
        body: dict = None,
    ) -> dict | str:
        if time.time() - self.last_accessed > self.session_timeout:
            if self.enable_log:
                LOG.info(f"Session timed out, re-logging in: {self.endpoint}")
            self.login()

        self.last_accessed = time.time()

        path_params = {}
        query_params = {}
        if params:
            for k, v in params.items():
                if f"{{{k}}}" in path:
                    path_params[k] = v
                else:
                    query_params[k] = v

        resp = requests.request(
            method=method,
            url=f"{self.base_url}{path.format(**path_params)}",
            headers=self.headers,
            params=query_params,
            json=body,
            verify=self.verify,
            timeout=self.timeout,
        )

        code = resp.status_code
        try:
            data = json.loads(resp.text)
        except:
            data = resp.text

        if self.enable_log:
            LOG.info(f"{method} {self.base_url}{path}, code: {code}")

        return data


class StorageAPIClient(BaseClient):
    """Huawei Storage API Client"""

    def __init__(
        self,
        endpoint: str,
        passphrase: str,
        verify=False,
        timeout: int = 30,
        session_timeout: int = 900,
        enable_log=True,
    ):
        headers = {
            "Content-Type": "application/json;charset=utf8",
            "Accept": "application/json",
        }
        super().__init__(
            endpoint,
            headers,
            verify,
            timeout=timeout,
            session_timeout=session_timeout,
            enable_log=enable_log,
        )
        self.passphrase = passphrase

    def login(self):
        url = f"{self.endpoint}/deviceManager/rest/xxxxx/sessions"
        body = {"passphrase": self.passphrase}
        response = requests.post(
            url,
            headers=self.headers,
            json=body,
            verify=self.verify,
            timeout=self.timeout,
        )
        if response.status_code != 200:
            raise Exception(f"Login to storage failed: {self.host}:{self.port}")

        resp_body = response.json()
        if resp_body["error"]["code"] != 0:
            error_msg = resp_body["error"]["description"]
            raise Exception(
                f"Login to storage failed: {self.host}:{self.port}, reason: {error_msg}"
            )

        self.headers["iBaseToken"] = resp_body["data"]["iBaseToken"]
        self.headers["Cookie"] = response.headers.get("Set-Cookie")

        deviceid = resp_body["data"]["deviceid"]
        self.base_url = f"{self.endpoint}/deviceManager/rest/{deviceid}"

        self.last_accessed = time.time()


class TASK_STATUS:
    INITIALIZING: int = 1
    EXECUTING: int = 2
    SUCCESS: int = 3
    PARTIAL_SUCCESS: int = 4
    FAILED: int = 5
    TIMEOUT: int = 6
    WARNING: int = 7


class CONST:
    # Task query retry count
    TASK_QUERY_RETRY_TIMES = 60

    # Task query retry interval (seconds)
    TASK_QUERY_RETRY_INTERVAL = 5


class DMEAPIClient(BaseClient):
    """DME API Client"""

    def __init__(
        self,
        endpoint: str = os.getenv("DME_API_ENDPOINT"),
        username: str = os.getenv("DME_API_USERNAME"),
        password: str = os.getenv("DME_API_PASSWORD"),
        auth_token: str = os.getenv("DME_API_AUTH_TOKEN"),
        verify=False,
        timeout: int = 30,
        session_timeout: int = 900,
        enable_log=True,
    ):
        headers = {
            "Content-Type": "application/json;charset=utf8",
            "Accept": "application/json",
            "X-Auth-Token": auth_token or "",
        }
        super().__init__(endpoint, headers, verify, timeout=timeout, session_timeout=session_timeout, enable_log=enable_log)
        self.base_url = self.endpoint
        self.username = username
        self.password = password
        self.storage_clients = {}

        if auth_token:
            self.last_accessed = time.time()

    def login(self):
        path = "/rest/plat/smapp/v1/sessions"
        url = f"{self.base_url}{path}"
        body = {
            "grantType": "password",
            "userName": self.username,
            "value": self.password,
        }
        response = requests.put(
            url,
            headers=self.headers,
            json=body,
            verify=self.verify,
            timeout=self.timeout,
        )
        if response.status_code == 200:
            self.headers["X-Auth-Token"] = response.json()["accessSession"]
            self.last_accessed = time.time()
        else:
            raise Exception(response.text)

    def get_storage_client(self, storage_id: str) -> StorageAPIClient:
        """Get storage client"""
        if storage_id in self.storage_clients:
            return self.storage_clients[storage_id]

        storage_info = self.get(
            "/rest/storagemgmt/v1/storages/{storage_id}/passphrase",
            params={"storage_id": storage_id},
        )
        storage_client = StorageAPIClient(
            endpoint=f"https://{storage_info["ip"]}:{storage_info["port"]}",
            passphrase=storage_info["passphrase"],
        )
        self.storage_clients[storage_id] = storage_client
        return storage_client

    def get_task_result(
        self,
        task_id: str,
        retry_times: int = CONST.TASK_QUERY_RETRY_TIMES,
        retry_interval: int = CONST.TASK_QUERY_RETRY_INTERVAL,
        affected_resource_filters: list[dict] = None,
    ) -> dict:
        """Get task result"""
        task_detail = self.get(
            "/rest/taskmgmt/v1/tasks/{task_id}", params={"task_id": task_id}
        )
        root_task = None
        for task in task_detail:
            if task["id"] == task_id:
                root_task = task
                break

        if (
            root_task["status"] != TASK_STATUS.INITIALIZING
            and root_task["status"] != TASK_STATUS.EXECUTING
        ):
            affected_resources = []
            for task in task_detail:
                if affected_resource_filters:
                    for resource in task["resources"]:
                        for filter in affected_resource_filters:
                            if (
                                resource["type"] == filter["type"]
                                and resource["operate"] == filter["operate"]
                            ):
                                affected_resources.append(resource)
                else:
                    affected_resources.extend(task["resources"])

            root_task["resources"] = affected_resources

            return root_task

        if retry_times > 0:
            time.sleep(retry_interval)
            return self.get_task_result(
                task_id, retry_times - 1, retry_interval, affected_resource_filters
            )
        else:
            raise Exception("Task query timeout")

