from typing import Optional, TypedDict, Union
from eth_typing import (
    Address,
    BlockNumber,
    ChecksumAddress,
    Hash32,
    HexAddress,
    HexStr,
    BlockIdentifier,
)

ValidAddress = Union[Address, ChecksumAddress, HexAddress, str]
ValidBytes = Union[HexStr, bytes]


class AnvilConfigBase(TypedDict, total=False):
    # Anvil Options
    accounts: Optional[int]
    block_time: Optional[int]
    balance: Optional[int]
    config_out: Optional[str]
    derivation_path: Optional[str]
    dump_state: Optional[str]
    hardfork: Optional[str]
    init: Optional[str]
    ipc: Optional[str]
    load_state: Optional[str]
    mnemonic: Optional[str]
    no_mining: Optional[bool]
    order: Optional[str]
    prune_history: Optional[Union[bool, int]]
    state_interval: Optional[int]
    silent: Optional[bool]
    state: Optional[str]
    timestamp: Optional[int]
    transaction_block_keeper: Optional[int]

    # Server Options
    allow_origin: Optional[str]
    no_cors: Optional[bool]
    # host: Optional[str]
    # port: Optional[str]

    # Fork Config
    compute_units_per_second: Optional[int]
    fork_url: Optional[str]
    fork_block_number: Optional[int]
    fork_chain_id: Optional[str]
    fork_retry_backoff: Optional[str]
    no_rate_limit: Optional[bool]
    no_storage_caching: Optional[bool]
    retries: Optional[int]
    timeout: Optional[int]

    # Enviroment Config
    block_base_fee_per_gas: Optional[int]
    chain_id: Optional[int]
    code_size_limit: Optional[int]
    disable_block_gas_limit: Optional[bool]
    gas_limit: Optional[int]
    gas_price: Optional[int]

    # EVM options
    auto_impersonate: Optional[bool]
    steps_tracing: Optional[bool]


class AnvilConfig(AnvilConfigBase, total=False):
    host: Optional[str]
    port: Optional[str]


class AnvilConfigInstance(AnvilConfigBase):
    host: str
    port: str


class Forking(TypedDict, total=False):
    json_rpc_url: Optional[str]
    block_number: Optional[int]
