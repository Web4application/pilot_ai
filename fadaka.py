from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("FADAKA_RPC_URL")))
contract_address = Web3.to_checksum_address("0xCaAA9A2A8B4d0dfD9ca5eC406ae11663CdC3Dd43")
wallet = w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))
fadaka_abi = [...]  # Paste the FDAK ABI here

contract = w3.eth.contract(address=contract_address, abi=fadaka_abi)

def mint_fdak(to, amount_eth):
    to = Web3.to_checksum_address(to)
    amount = w3.to_wei(amount_eth, 'ether')
    tx = contract.functions.mint(to, amount).build_transaction({
        'from': wallet.address,
        'nonce': w3.eth.get_transaction_count(wallet.address),
        'gas': 200000,
        'gasPrice': w3.to_wei('2', 'gwei')
    })
    signed = wallet.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return tx_hash.hex()
