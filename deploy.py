from web3 import Web3
from solcx import compile_standard, install_solc
import json
from config import INFURA_API_KEY, PRIVATE_KEY

install_solc("0.8.0")

with open("AllowToken.sol", "r", encoding="utf-8") as f:
    source_code = f.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "AllowToken.sol": {
                "content": source_code
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

# Запишем результат в compiled.json
with open("compiled.json", "w", encoding="utf-8") as f:
    json.dump(compiled_sol, f, ensure_ascii=False, indent=4)

# Достаём ABI и Bytecode
abi = compiled_sol["contracts"]["AllowToken.sol"]["AllowToken"]["abi"]
bytecode = compiled_sol["contracts"]["AllowToken.sol"]["AllowToken"]["evm"]["bytecode"]["object"]

# Подключаемся к сети Sepolia через Infura
w3 = Web3(Web3.HTTPProvider(f"https://sepolia.infura.io/v3/{INFURA_API_KEY}"))

account = w3.eth.account.from_key(PRIVATE_KEY)
account_address = account.address

AllowTokenContract = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.get_transaction_count(account_address)

transaction = AllowTokenContract.constructor().build_transaction({
    "chainId": 11155111,
    "gas": 3000000,
    "gasPrice": w3.eth.gas_price,
    "nonce": nonce
})

signed_tx = account.sign_transaction(transaction)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

if __name__ == "__main__":
    print("AllowToken deployed at:", tx_receipt.contractAddress)

## https://docs.etherscan.io/contract-verification/multichain-verification