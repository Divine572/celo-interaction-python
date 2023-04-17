import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# Celo network parameters
CELO_ALFAJORES_RPC_URL = "https://alfajores-forno.celo-testnet.org"

# Connect to the Celo Alfajores testnet
w3 = Web3(Web3.HTTPProvider(CELO_ALFAJORES_RPC_URL))

# Load private key and initialize account
private_key = os.environ.get("CELO_DEPLOYER_PRIVATE_KEY")
deployer = w3.eth.account.from_key(private_key)

ERC20_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "to", "type": "address"},
            {"name": "value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {"name": "owner", "type": "address"},
            {"name": "spender", "type": "address"}
        ],
        "name": "allowance",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "spender", "type": "address"},
            {"name": "value", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "from", "type": "address"},
            {"name": "to", "type": "address"},
            {"name": "value", "type": "uint256"}
        ],
        "name": "transferFrom",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]


# Get cUSD balance
def get_cusd_balance(account_address, contract_address):
    # Get cUSD contract
    cusd_contract = w3.eth.contract(address=contract_address, abi=ERC20_ABI)

    # Get cUSD balance
    balance = cusd_contract.functions.balanceOf(account_address).call()
    balance = w3.from_wei(balance, "ether")

    return balance


# Send cUSD
def send_cusd(account, to, amount, contract_address):
    # Get cUSD contract
    cusd_contract = w3.eth.contract(address=contract_address, abi=ERC20_ABI)

    # Estimate gas required
    gas_estimate = cusd_contract.functions.transfer(to, w3.to_wei(amount, "ether")).estimate_gas(
        {"from": account.address}
    )

    # Create a transaction
    transaction = cusd_contract.functions.transfer(to, w3.to_wei(amount, "ether")).build_transaction(
        {
            "from": account.address,
            "gas": gas_estimate,
            "gasPrice": w3.eth.gas_price,
            "nonce": w3.eth.get_transaction_count(account.address),
        }
    )

    # Sign and send the transaction
    signed_transaction = account.sign_transaction(transaction)
    transaction_hash = w3.eth.send_raw_transaction(
        signed_transaction.rawTransaction)

    return transaction_hash


# Get CUSD balance
CUSD_ALFAJORES_CONTRACT_ADDRESS = "0x874069Fa1Eb16D44d622F2e0Ca25eeA172369bC1"
print(
    f"cUSD Balance: {get_cusd_balance(deployer.address, CUSD_ALFAJORES_CONTRACT_ADDRESS)} cUSD")

# Send CUSD
recipient_address = "0xcdd1151b2bC256103FA2565475e686346CeFd813"
amount_to_send = 1  # cUSD
transaction_hash = send_cusd(
    deployer, recipient_address, amount_to_send, CUSD_ALFAJORES_CONTRACT_ADDRESS)
print(f"Sent {amount_to_send} cUSD to {recipient_address}. Transaction hash: {transaction_hash.hex()}")
