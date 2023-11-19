from typing import cast
from eth_account.signers.local import (
    LocalAccount,
)
from eth_typing import HexStr
from web3 import HTTPProvider, Web3
from web3.types import Gwei, Wei
from anvil_web3 import anvil, AnvilInstance, AnvilWeb3

anvil_instance = AnvilInstance()
w3 = AnvilWeb3(HTTPProvider(anvil_instance.http_url))

signer: LocalAccount = w3.eth.account.from_key(w3.keccak(text="Hello world!"))

print("Signer address", signer.address)

w3.anvil.set_balance(signer.address, w3.to_wei(1, "ether"))

# burn some fake money
txn = {
    "chainId": w3.eth.chain_id,
    "data": HexStr("0x"),
    "from": signer.address,
    "gas": 21000,
    "maxFeePerGas": 1 * 10**9,
    "maxPriorityFeePerGas": 1 * 10**9,
    "nonce": w3.eth.get_transaction_count(signer.address),
    "to": "0x0000000000000000000000000000000000000000",
    "value": Wei(50),
}

hash = w3.eth.send_raw_transaction(signer.sign_transaction(txn)["rawTransaction"])
receipt = w3.eth.wait_for_transaction_receipt(hash)
print(receipt)
