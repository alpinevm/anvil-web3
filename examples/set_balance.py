from typing import cast
from anvil_web3 import anvil, AnvilInstance, AnvilWeb3

from web3 import HTTPProvider, Web3

anvil_instance = AnvilInstance()
w3 = Web3(HTTPProvider(anvil_instance.http_url))
anvil(w3)

address = w3.to_checksum_address("0x1000000000000000000000000000000000000000")

print("Balance before", w3.eth.get_balance(address))
cast(AnvilWeb3, w3).anvil.set_balance(address, 10000000000)
print("Balance after", w3.eth.get_balance(address))
