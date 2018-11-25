#!/usr/bin/python3

from tokens.bank import Bank

# Our Ethereum provider
eth_provider_url = "http://127.0.0.1:8545"

if __name__ == "__main__":
	bank = Bank(eth_provider_url)
	print("Your contract address:")
	print(bank.contract_deploy())
