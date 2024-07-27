from eth_account.signers.local import (
    LocalAccount,
)
from web3 import HTTPProvider
from anvil_web3 import AnvilInstance, AnvilWeb3

anvil_instance = AnvilInstance()
w3 = AnvilWeb3(HTTPProvider(anvil_instance.http_url))

signer: LocalAccount = w3.eth.account.from_key(w3.keccak(text="Hello world!"))

print("Signer address", signer.address)

w3.anvil.set_balance(signer.address, w3.to_wei(1, "ether"))

future_timestamp = 4242424242
w3.anvil.set_next_block_timestamp(future_timestamp)

w3.anvil.mine(1, None)
block = w3.eth.get_block("latest")
assert block.get("timestamp", None) is not None
assert block.get("timestamp") == future_timestamp
print("Hardcoded Block timestamp", block.get("timestamp"))
raise Exception("End of snippet")
