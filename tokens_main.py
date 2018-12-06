#!/usr/bin/python3

from tokens import TokenAPI
from tokens.bank import Bank

import logging
import sys

# Token system settings
token_api_host = "localhost"
token_api_port = 8080

# Ethereum settings
eth_provider_url = "http://127.0.0.1:8545"

# Allowed API users
allowed_apps = {
	"document-fetcher": "password",
	"scheduler": "password"
}

def contract_deploy():
	print("Deploying Token API Contract")
	bank = Bank(eth_provider_url)
	addr = bank.contract_deploy()
	print("Deployed: %s" % addr)
	print("Generating contract file contract.py")
	with open("contract.py", "w") as fp:
		fp.write("eth_contract_addr = \"%s\"\n" % addr)
	print("Contract file generated")

# Run token system
if __name__ == "__main__":
	try:
		from contract import eth_contract_addr
	except:
		contract_deploy()
	from contract import eth_contract_addr
	
	api = TokenAPI(
		eth_provider_url,
		eth_contract_addr,
		allowed_apps=allowed_apps
	)
	api.run(host=token_api_host, port=token_api_port)
