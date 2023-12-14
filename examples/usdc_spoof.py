# Use storage manipulation to fake being USDC rich
from eth_account.signers.local import (
    LocalAccount,
)
from eth_typing import ChecksumAddress, HexAddress, HexStr
from web3 import HTTPProvider, Web3
from web3.types import Gwei, Wei
from anvil_web3 import anvil, AnvilInstance, AnvilWeb3
from eth_abi.abi import encode

anvil_instance = AnvilInstance(fork_url="https://eth.llamarpc.com")
w3 = AnvilWeb3(HTTPProvider(anvil_instance.http_url))

signer: LocalAccount = w3.eth.account.from_key(w3.keccak(text="Hello world!"))

print("Signer address", signer.address)

USDC = w3.to_checksum_address("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
USDC_ABI_FRAGMENT = [
    {
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    }
]

usdc_contract = w3.eth.contract(USDC, abi=USDC_ABI_FRAGMENT)

print("USDC Balance before", usdc_contract.functions.balanceOf(signer.address).call())

# Initial slot index of balances mapping in the USDC contract is 0x9:
# contract FiatTokenV1 is AbstractFiatTokenV1, Ownable, Pausable, Blacklistable {
#     using SafeMath for uint256;
#     // first 4 slots used by Ownable + Pausable + Blacklistable
#     string public name; // 0x4
#     string public symbol; // 0x5
#     uint8 public decimals; // 0x6
#     string public currency; // 0x7
#     address public masterMinter; // 0x8
#     bool internal initialized; // 0x8 (shared slot)
#
#     mapping(address => uint256) internal balances; // 0x9


# the keccak hash of this initial slot and the actual key (signer.address here) is the
# slot where the balance is actually stored:
# keccak256(abi.encode(user_address, 9))
slot = w3.keccak(encode(["address", "uint256"], [signer.address, 9]))

w3.anvil.set_storage_at(USDC, int.from_bytes(slot), encode(["uint256"], [10000]))

# we're rich!
print("USDC Balance after", usdc_contract.functions.balanceOf(signer.address).call())
