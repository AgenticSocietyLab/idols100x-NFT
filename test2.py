from web3 import Web3
from eth_account import Account
import secrets
import time
import threading

# 连接到以太坊网络（例如Infura或本地节点）
infura_url = "https://bartio.rpc.berachain.com/"
w3 = Web3(Web3.HTTPProvider(infura_url))

# 检查连接状态
if w3.is_connected():
    print("Connected to Ethereum network")
else:
    print("Failed to connect to Ethereum network")


# Wallet1 的私钥（这个私钥需要妥善保管，不要泄露）
root_private_key = "0xd110227375ab838e8743192d278c105e30f253c966987c50b754412c9b986fe3"
# 获取 Wallet1 的地址
root_address = Account.from_key(root_private_key).address
root_nonce = w3.eth.get_transaction_count(root_address)

# infrared.sol 0xe41779952f5485db5440452DFa43350556AA4673
# cast call [Infrared-Address] "vaultRegistry(address)" [LP-Token-Address] --rpc-url [RPC-URL]
abi = '''
[
    {
        "constant": false,
        "inputs": [
            {
                "name": "address",
                "type": "address"
            }
        ],
        "name": "vaultRegistry",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "type": "function"
    }
]
'''

# read from chain
infra_contract = w3.eth.contract(address="0xe41779952f5485db5440452DFa43350556AA4673", abi=abi)
