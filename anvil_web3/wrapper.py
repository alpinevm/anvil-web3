from typing import Any, Union, Dict, Callable, cast, Optional
import json
import os
from typing_extensions import Unpack
import subprocess
import socket
from web3 import Web3, HTTPProvider
from web3.types import Wei
from .types import AnvilConfig, AnvilConfigInstance
import time
import requests
import traceback

# import psutil


class AnvilInstance:
    """
    Python wrapper over the Anvil CLI
    """

    def __init__(
        self,
        *,
        supress_anvil_output: bool = True,
        liveliness_timeout: int = 60,
        auto_exit: bool = True,
        **config: Unpack[AnvilConfig],
    ):
        self.config: Union[AnvilConfigInstance, dict] = {}
        self.cli_config: list[str] = []
        self.default_config_setters: Dict[str, Callable[[], str]] = {
            "host": lambda: "127.0.0.1",
            "port": lambda: AnvilInstance._find_free_port(),
        }
        self.liveliness_timeout: int
        # Auto-exiting state
        self.parent_pid: int

        # Populate config
        for key in AnvilConfig.__annotations__:
            value = config.get(key)
            if self.default_config_setters.get(key, None) is not None and value is None:
                value_func = self.default_config_setters.get(key)
                if value_func is not None:
                    value = value_func()
            self.config[key] = value
            if value is not None:
                fmt_key = key.replace("_", "-")
                if isinstance(value, bool):
                    self.cli_config.extend([f"--{fmt_key}"])
                else:
                    self.cli_config.extend([f"--{fmt_key}", str(value)])
        self.liveliness_timeout = liveliness_timeout

        if auto_exit:
            # TODO: Implement auto exit
            # Potentially:
            # Attach a signal listener (running in a different subprocess)
            # to the parent PID, then killing the anvil process on SIGTERM/SIGKILL
            self.parent_pid = os.getpid()

        self.anvil_process = subprocess.Popen(
            ["anvil"] + self.cli_config,
            stdout=subprocess.DEVNULL if supress_anvil_output else None,
            stderr=subprocess.DEVNULL if supress_anvil_output else None,
        )

        self._wait_until_live()

    @property
    def url(self):
        return f"{self.config['host']}:{self.config['port']}"

    @property
    def http_url(self):
        return f"http://{self.url}"

    @property
    def ws_url(self):
        return f"ws://{self.url}"

    def kill(self):
        self.anvil_process.terminate()

    @staticmethod
    def _find_free_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", 0))  # Bind to a port assigned by the kernel
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return str(s.getsockname()[1])

    @staticmethod
    def _consume_error(error):
        pass

    def _wait_until_live(self):
        end_time = time.time() + self.liveliness_timeout
        while time.time() < end_time:
            try:
                response = requests.post(
                    self.http_url,
                    json={
                        "method": "web3_clientVersion",
                        "params": [],
                        "id": "0",
                        "jsonrpc": "2.0",
                    },
                )
                response.raise_for_status()
                return response
            except requests.RequestException:
                time.sleep(0.001)

        raise TimeoutError(
            f"Unable to connect to {self.http_url} after {self.liveliness_timeout} seconds."
        )
