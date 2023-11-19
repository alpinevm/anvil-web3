from typing import Dict, Callable, Any, TypeVar, Union
from hexbytes import HexBytes

try:
    from cytoolz import compose, curry  # type:ignore
except ImportError:
    from toolz import compose, curry
from eth_utils.curried import (
    apply_formatter_at_index,  # type: ignore
    apply_formatters_to_dict,
)
from eth_utils.address import to_normalized_address
from web3._utils.type_conversion import to_hex_if_bytes
from web3.types import RPCEndpoint
from web3._utils.method_formatters import to_hex_if_integer, combine_formatters

"""Accessible formatters

apply_formatter_at_index = curry(apply_formatter_at_index)
apply_formatter_if = curry(non_curried_apply_formatter_if)
apply_formatter_to_array = curry(apply_formatter_to_array)
apply_formatters_to_dict = curry(non_curried_apply_formatters_to_dict)
apply_formatters_to_sequence = curry(apply_formatters_to_sequence)
apply_key_map = curry(apply_key_map)
apply_one_of_formatters = curry(non_curried_apply_one_of_formatters)
from_wei = curry(from_wei)
get_logger = curry(get_logger)
hexstr_if_str = curry(non_curried_hexstr_if_str)
is_same_address = curry(is_same_address)
text_if_str = curry(non_curried_text_if_str)
to_wei = curry(to_wei)
clamp = curry(clamp)

"""

T = TypeVar("T")


def buffer(arg: T) -> T:
    return arg


def no_args() -> list:
    return []


def no_expected_return(*args, **kwargs) -> None:
    return None


def _optional_value(formatter: Callable[[T], Any], value: T):
    if value is not None:
        return formatter(value)


optional_value = curry(_optional_value)


class AnvilRPC:
    # Standard Methods
    anvil_impersonateAccount = RPCEndpoint("anvil_impersonateAccount")
    anvil_stopImpersonatingAccount = RPCEndpoint("anvil_stopImpersonatingAccount")
    anvil_autoImpersonateAccount = RPCEndpoint("anvil_autoImpersonateAccount")
    anvil_getAutomine = RPCEndpoint("anvil_getAutomine")
    anvil_mine = RPCEndpoint("anvil_mine")
    anvil_dropTransaction = RPCEndpoint("anvil_dropTransaction")
    anvil_reset = RPCEndpoint("anvil_reset")
    anvil_setRpcUrl = RPCEndpoint("anvil_setRpcUrl")
    anvil_setBalance = RPCEndpoint("anvil_setBalance")
    anvil_setCode = RPCEndpoint("anvil_setCode")
    anvil_setNonce = RPCEndpoint("anvil_setNonce")
    anvil_setStorageAt = RPCEndpoint("anvil_setStorageAt")
    anvil_setCoinbase = RPCEndpoint("anvil_setCoinbase")
    anvil_setLoggingEnabled = RPCEndpoint("anvil_setLoggingEnabled")
    anvil_setMinGasPrice = RPCEndpoint("anvil_setMinGasPrice")
    anvil_setNextBlockBaseFeePerGas = RPCEndpoint("anvil_setNextBlockBaseFeePerGas")
    anvil_setChainId = RPCEndpoint("anvil_setChainId")
    anvil_dumpState = RPCEndpoint("anvil_dumpState")
    anvil_loadState = RPCEndpoint("anvil_loadState")
    anvil_nodeInfo = RPCEndpoint("anvil_nodeInfo")

    # Special Methods
    evm_setAutomine = RPCEndpoint("evm_setAutomine")
    evm_setIntervalMining = RPCEndpoint("evm_setIntervalMining")
    evm_snapshot = RPCEndpoint("evm_snapshot")
    evm_revert = RPCEndpoint("evm_revert")
    evm_increaseTime = RPCEndpoint("evm_increaseTime")
    evm_setNextBlockTimestamp = RPCEndpoint("evm_setNextBlockTimestamp")
    anvil_setBlockTimestampInterval = RPCEndpoint("anvil_setBlockTimestampInterval")
    evm_setBlockGasLimit = RPCEndpoint("evm_setBlockGasLimit")
    anvil_removeBlockTimestampInterval = RPCEndpoint(
        "anvil_removeBlockTimestampInterval"
    )
    evm_mine = RPCEndpoint("evm_mine")
    anvil_enableTraces = RPCEndpoint("anvil_enableTraces")
    eth_sendUnsignedTransaction = RPCEndpoint("eth_sendUnsignedTransaction")

    # Methods based on Geth's documentation
    txpool_status = RPCEndpoint("txpool_status")
    txpool_inspect = RPCEndpoint("txpool_inspect")
    txpool_content = RPCEndpoint("txpool_content")


ANVIL_REQUEST_FORMATTER: Dict[RPCEndpoint, Callable[..., Any]] = {
    AnvilRPC.anvil_impersonateAccount: compose(
        apply_formatter_at_index(to_normalized_address, 0),
    ),
    AnvilRPC.anvil_stopImpersonatingAccount: compose(
        apply_formatter_at_index(to_normalized_address, 0),
    ),
    AnvilRPC.anvil_autoImpersonateAccount: compose(
        apply_formatter_at_index(buffer, 0),
    ),
    AnvilRPC.anvil_getAutomine: no_args,
    AnvilRPC.evm_setAutomine: compose(
        apply_formatter_at_index(buffer, 0),
    ),
    AnvilRPC.anvil_mine: compose(
        apply_formatter_at_index(to_hex_if_integer, 0),
        apply_formatter_at_index(to_hex_if_integer, 1),
    ),
    AnvilRPC.evm_setIntervalMining: compose(
        apply_formatter_at_index(to_hex_if_integer, 0)
    ),
    AnvilRPC.anvil_dropTransaction: compose(
        apply_formatter_at_index(to_hex_if_bytes, 0)
    ),
    AnvilRPC.anvil_reset: compose(
        apply_formatter_at_index(
            apply_formatters_to_dict(
                {"json_rpc_url": str, "block_number": to_hex_if_integer}
            ),
            0,
        )
    ),
    AnvilRPC.anvil_setBalance: compose(
        apply_formatter_at_index(to_normalized_address, 0),
        apply_formatter_at_index(to_hex_if_integer, 1),
    ),
    AnvilRPC.anvil_setChainId: compose(apply_formatter_at_index(to_hex_if_integer, 0)),
    AnvilRPC.anvil_setCode: compose(
        apply_formatter_at_index(to_normalized_address, 0),
        apply_formatter_at_index(to_hex_if_bytes, 1),
    ),
    AnvilRPC.anvil_setNonce: compose(
        apply_formatter_at_index(to_normalized_address, 0),
        apply_formatter_at_index(to_hex_if_integer, 1),
    ),
    AnvilRPC.anvil_setStorageAt: compose(
        apply_formatter_at_index(to_normalized_address, 0),
        apply_formatter_at_index(to_hex_if_integer, 1),
        apply_formatter_at_index(to_hex_if_bytes, 2),
    ),
}

ANVIL_RESULT_FORMATTER: Dict[RPCEndpoint, Callable[..., Any]] = {
    AnvilRPC.anvil_impersonateAccount: no_expected_return,
    AnvilRPC.anvil_stopImpersonatingAccount: no_expected_return,
    AnvilRPC.anvil_autoImpersonateAccount: no_expected_return,
    AnvilRPC.anvil_getAutomine: bool,
    AnvilRPC.evm_setAutomine: no_expected_return,
    AnvilRPC.anvil_mine: no_expected_return,
    AnvilRPC.evm_setIntervalMining: no_expected_return,
    AnvilRPC.anvil_dropTransaction: optional_value(HexBytes),
    AnvilRPC.anvil_reset: no_expected_return,
    AnvilRPC.anvil_setBalance: no_expected_return,
    AnvilRPC.anvil_setChainId: no_expected_return,
    AnvilRPC.anvil_setCode: no_expected_return,
    AnvilRPC.anvil_setNonce: no_expected_return,
    AnvilRPC.anvil_setStorageAt: bool,
}


def get_anvil_request_formatter(
    method_name: Union[RPCEndpoint, Callable[..., RPCEndpoint]]
):
    return compose(*combine_formatters([ANVIL_REQUEST_FORMATTER], method_name))


def get_anvil_result_formatter(
    method_name: Union[RPCEndpoint, Callable[..., RPCEndpoint]]
):
    return compose(*combine_formatters([ANVIL_RESULT_FORMATTER], method_name))
