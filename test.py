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

def get_thpot(nnonce):
    # 创建随机私钥并生成新钱包
    private_key_new_wallet = "0x" + secrets.token_hex(32)
    new_wallet = Account.from_key(private_key_new_wallet)

    # 获取新钱包的地址
    new_wallet_address = new_wallet.address
    print(f"New Wallet Address: {new_wallet_address}")
    print(f"New Wallet Private Key: {private_key_new_wallet}")

    # 构造交易
    tx = {
    'nonce': nnonce,
    'to': new_wallet_address,
    'value': w3.to_wei(0.002, 'ether'),  # 发送 0.01 ETH
    'gas': 22000,
    'maxPriorityFeePerGas': w3.to_wei('40', 'gwei'),  # 设置优先费
    'maxFeePerGas': w3.to_wei('40', 'gwei'),  # 设置最大 Gas 费用
    'chainId': 80084,  # 主网为 1；测试网取决于网络，例如 Rinkeby 为 4
    }

    # 对交易进行签名
    signed_tx = w3.eth.account.sign_transaction(tx, root_private_key)

    # 发送交易
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # 输出交易哈希
    print(f"Transaction Hash: {w3.to_hex(tx_hash)}")

    # 合约地址（假设你已经有了合约地址）
    contract_address = "0xfc5e3743E9FAC8BB60408797607352E24Db7d65E"

    # 合约方法的 MethodID (faucet 函数)
    faucet_method_id = "0xde5f72fd"

    nonce = w3.eth.get_transaction_count(new_wallet_address)

    # 构造交易
    tx = {
    'nonce': nonce,
    'to': contract_address,
    'value': 0,  # 调用合约方法不需要发送 ETH
    'gas': 150000,  # 估算合适的 Gas limit
    'maxPriorityFeePerGas': w3.to_wei('6', 'gwei'),  # 设置优先费
    'maxFeePerGas': w3.to_wei('6', 'gwei'),  # 设置最大 Gas 费用
    'data': faucet_method_id,  # 指定调用的合约方法
    'chainId': 80084,  # 主网为 1；测试网取决于网络，例如 Rinkeby 为 4
    }

    # 对交易进行签名
    signed_tx = w3.eth.account.sign_transaction(tx, private_key_new_wallet)

    time.sleep(20)

    # 发送交易
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # 输出交易哈希
    print(f"Transaction Hash: {w3.to_hex(tx_hash)}")

    # tHPOT 代币合约 ABI (ERC-20 通用 ABI, 只包括 transfer 方法)
    token_abi = '''
    [
        {
            "constant": false,
            "inputs": [
                {
                    "name": "_to",
                    "type": "address"
                },
                {
                    "name": "_value",
                    "type": "uint256"
                }
            ],
            "name": "transfer",
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

    # 加载合约
    token_contract = w3.eth.contract(address=contract_address, abi=token_abi)

    # 代币数量 (注意 ERC-20 通常以最小单位表示, 如果代币有 18 位小数, 需要乘以 10^18)
    token_amount = 299 * (10 ** 18)

    # 构造交易数据
    transaction = token_contract.functions.transfer(root_address, token_amount).build_transaction({
        'chainId': 80084,  # 主网为 1；测试网取决于网络，例如 Rinkeby 为 4
        'gas': 100000,  # 估算合适的 Gas limit
        'maxPriorityFeePerGas': w3.to_wei('2', 'gwei'),  # 设置优先费
        'maxFeePerGas': w3.to_wei('2', 'gwei'),  # 设置最大 Gas 费用   
        'nonce': nonce+1,
    })

    # 对交易进行签名
    signed_tx = w3.eth.account.sign_transaction(transaction, private_key_new_wallet)

    # 发送交易
    time.sleep(5)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # 输出交易哈希
    print(f"Transaction Hash: {w3.to_hex(tx_hash)}")



threads = []
# 创建多个线程并启动

for i in range(1000):  # 例如创建5个线程
    thread = threading.Thread(target=get_thpot, args=(root_nonce+i,))
    time.sleep(3)
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()
