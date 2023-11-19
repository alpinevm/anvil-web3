from typing import (
    Dict,
    Callable,
    Any,
    Union,
    Optional,
    Sequence,
    Generic,
    TYPE_CHECKING,
    Type,
)
from ens import ENS
from hexbytes import HexBytes
from toolz import compose, curry
from web3 import Web3
from web3.providers.base import BaseProvider
from web3.types import RPCEndpoint, Nonce, TxParams, Wei, TReturn
from eth_typing import (
    Address,
    BlockNumber,
    ChecksumAddress,
    Hash32,
    HexStr,
    BlockIdentifier,
)
from web3.module import Module
from web3.method import Method, Munger, TFunc
from web3._utils.module import attach_modules
from web3._utils.method_formatters import (
    PYTHONIC_REQUEST_FORMATTERS,
    combine_formatters,
    get_result_formatters,
)

from anvil_web3.types import Forking, ValidAddress, ValidBytes

from .rpc import (
    AnvilRPC,
    get_anvil_result_formatter,
    get_anvil_request_formatter,
)


from web3._utils.empty import (
    empty,
)

if TYPE_CHECKING:
    from web3._utils.empty import Empty


# Same as Method but override the request/response formatters to use
# ours by default (avoid code duping in the Anvil Module)
class AnvilMethod(Method, Generic[TFunc]):
    def __init__(
        self,
        json_rpc_method: Optional[RPCEndpoint] = None,
        mungers: Optional[Sequence[Munger]] = None,
        request_formatters: Optional[Callable[..., TReturn]] = None,
        result_formatters: Optional[Callable[..., TReturn]] = None,
        null_result_formatters: Optional[Callable[..., TReturn]] = None,
        method_choice_depends_on_args: Optional[Callable[..., RPCEndpoint]] = None,
        is_property: bool = False,
    ):
        super().__init__(
            json_rpc_method,
            mungers,
            request_formatters,
            result_formatters,
            null_result_formatters,
            method_choice_depends_on_args,
            is_property,
        )
        self.request_formatters = request_formatters or get_anvil_request_formatter
        self.result_formatters = result_formatters or get_result_formatters


class Anvil(Module):
    # anvil_impersonateAccount

    _impersonate_account: AnvilMethod[Callable[[ValidAddress], None]] = AnvilMethod(
        AnvilRPC.anvil_impersonateAccount
    )

    def impersonate_account(
        self,
        account: ValidAddress,
    ) -> None:
        return self._impersonate_account(account)

    # anvil_stopImpersonatingAccount

    _stop_impersonating_account: AnvilMethod[
        Callable[[ValidAddress], None]
    ] = AnvilMethod(AnvilRPC.anvil_stopImpersonatingAccount)

    def stop_impersonating_account(
        self,
        account: ValidAddress,
    ) -> None:
        return self._stop_impersonating_account(account)

    # anvil_autoImpersonateAccount

    _auto_impersonate_account: AnvilMethod[Callable[[bool], None]] = AnvilMethod(
        AnvilRPC.anvil_autoImpersonateAccount
    )

    def auto_impersonate_account(self, enabled: bool) -> None:
        return self._auto_impersonate_account(enabled)

    # anvil_getAutomine

    _get_auto_mine: AnvilMethod[Callable[[], bool]] = AnvilMethod(
        AnvilRPC.anvil_getAutomine
    )

    def get_auto_mine(self) -> bool:
        return self._get_auto_mine()

    # evm_setAutomine

    _set_auto_mine: AnvilMethod[Callable[[bool], None]] = AnvilMethod(
        AnvilRPC.evm_setAutomine
    )

    def set_auto_mine(self, enable_automine: bool) -> None:
        return self._set_auto_mine(enable_automine)

    # anvil_mine

    _mine: AnvilMethod[Callable[[Optional[int], Optional[int]], None]] = AnvilMethod(
        AnvilRPC.anvil_mine
    )

    def mine(self, num_blocks: Optional[int], interval: Optional[int]) -> None:
        return self._mine(num_blocks, interval)

    # evm_setIntervalMining
    _set_interval_mining: AnvilMethod[Callable[[int], None]] = AnvilMethod(
        AnvilRPC.evm_setIntervalMining
    )

    def set_interval_mining(self, secs: int) -> None:
        return self._set_interval_mining(secs)

    # anvil_dropTransaction

    _drop_transaction: AnvilMethod[
        Callable[[ValidBytes], Optional[ValidBytes]]
    ] = AnvilMethod(AnvilRPC.anvil_dropTransaction)

    def drop_transaction(self, tx_hash: ValidBytes) -> Optional[ValidBytes]:
        return self._drop_transaction(tx_hash)

    # anvil_reset

    _reset: AnvilMethod[Callable[[Optional[Forking]], None]] = AnvilMethod(
        AnvilRPC.anvil_reset
    )

    def reset(self, forking: Optional[Forking]) -> None:
        return self._reset(forking)

    # anvil_setChainId

    _set_chain_id: AnvilMethod[Callable[[int], None]] = AnvilMethod(
        AnvilRPC.anvil_setChainId
    )

    def set_chain_id(self, chain_id: int) -> None:
        return self._set_chain_id(chain_id)

    # anvil_setBalance

    _set_balance: AnvilMethod[
        Callable[[ValidAddress, Union[int, Wei]], None]
    ] = AnvilMethod(AnvilRPC.anvil_setBalance)

    def set_balance(
        self,
        account: ValidAddress,
        balance: Union[int, Wei],
    ) -> None:
        return self._set_balance(account, balance)

    # anvil_setCode

    _set_code: AnvilMethod[Callable[[ValidAddress, ValidBytes], None]] = AnvilMethod(
        AnvilRPC.anvil_setCode
    )

    def set_code(
        self,
        address: ValidAddress,
        code: ValidBytes,
    ) -> None:
        return self._set_code(address, code)

    # anvil_setNonce

    _set_nonce: AnvilMethod[Callable[[ValidAddress, int], None]] = AnvilMethod(
        AnvilRPC.anvil_setNonce
    )

    def set_nonce(
        self,
        address: ValidAddress,
        nonce: int,
    ) -> None:
        return self._set_nonce(address, nonce)

    # anvil_setStorageAt

    _set_storage_at: AnvilMethod[
        Callable[[ValidAddress, int, ValidBytes], bool]
    ] = AnvilMethod(AnvilRPC.anvil_setStorageAt)

    def set_storage_at(self, address: ValidAddress, slot: int, val: ValidBytes) -> bool:
        return self._set_storage_at(address, slot, val)


class AnvilWeb3(Web3):
    anvil: Anvil

    def __init__(
        self,
        provider: Optional[BaseProvider] = None,
        middlewares: Optional[Sequence[Any]] = None,
        modules: Optional[Dict[str, Union[Type[Module], Sequence[Any]]]] = None,
        external_modules: Optional[
            Dict[str, Union[Type[Module], Sequence[Any]]]
        ] = None,
        ens: Union[ENS, "Empty"] = empty,
    ) -> None:
        if not isinstance(external_modules, dict):
            external_modules = {}
        external_modules["anvil"] = (Anvil,)
        super().__init__(provider, middlewares, modules, external_modules, ens)


def anvil(
    w3: Web3,
):
    attach_modules(w3, {"anvil": (Anvil,)})
