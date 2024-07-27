# anvil-web3
Easily interact with and create [anvil](https://github.com/foundry-rs/foundry/tree/master/crates/anvil) chains from python

## Install
`anvil-web3` assumes anvil is already installed, click [here](https://book.getfoundry.sh/getting-started/installation) if you don't have anvil installed
```
python3 -m pip install anvil-web3
```

## Usage
This example shows how to programatically create an Anvil chain and how to inject the anvil rpc methods to a
web3.py `Web3` object:
```python
from web3 import Web3, HTTPProvider
from anvil_web3 import anvil, AnvilWeb3, AnvilInstance

# create an anvil chain
instance = AnvilInstance(
    chain_id=42
)

# use the injection function
w3 = Web3(HTTPProvider(instance.http_url))
anvil(w3)

# or contruct a Web3 object from the AnvilWeb3 class (recommended for better autocompletion support)
w3 = AnvilWeb3(HTTPProvider(instance.http_url))

test_account = w3.eth.account.from_key(w3.keccak(text="42"))

# call an anvil method
w3.anvil.set_balance(test_account.address, 42424242)
assert w3.eth.get_balance(test_account.address) == 42424242 and w3.eth.chain_id == 42

instance.kill()
```
More complex demos in `/examples`

## Tests
WIP

### Current API Support

- [x] anvil_impersonateAccount
- [x] anvil_stopImpersonatingAccount
- [x] anvil_autoImpersonateAccount
- [x] anvil_getAutomine
- [x] anvil_mine
- [x] anvil_dropTransaction
- [x] anvil_reset
- [ ] anvil_setRpcUrl
- [x] anvil_setBalance
- [x] anvil_setCode
- [x] anvil_setNonce
- [x] anvil_setStorageAt
- [ ] anvil_setCoinbase
- [ ] anvil_setLoggingEnabled
- [ ] anvil_setMinGasPrice
- [ ] anvil_setNextBlockBaseFeePerGas
- [x] anvil_setChainId
- [ ] anvil_dumpState
- [ ] anvil_loadState
- [ ] anvil_nodeInfo
- [ ] evm_setAutomine
- [x] evm_setIntervalMining
- [ ] evm_snapshot
- [ ] evm_revert
- [ ] evm_increaseTime
- [x] evm_setNextBlockTimestamp
- [ ] anvil_setBlockTimestampInterval
- [ ] evm_setBlockGasLimit
- [ ] anvil_removeBlockTimestampInterval
- [ ] evm_mine
- [ ] anvil_enableTraces
- [ ] eth_sendUnsignedTransaction
