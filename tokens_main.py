#!/usr/bin/python3

from tokens import TokenAPI
from tokens.bank import Bank

import logging
import sys

# Token system settings
token_api_host = "localhost"
token_api_port = 8080

# Ethereum settings
eth_provider_url = ""
eth_priv_key = ""

# Allowed API users
allowed_apps = {
	"document-fetcher": "password",
	"scheduler": "password"
}

def deploy():
	print("Deploying Token API Contract")
	bank = Bank(eth_provider_url, eth_priv_key)
	addr = bank.contract_deploy()
	print("Deployed: %s" % addr)
	print("Generating contract file contract.py")
	with open("contract.py", "w") as fp:
		fp.write("eth_contract_addr = \"%s\"\n" % addr)
	print("Contract file generated")

def run():
	bank = Bank(eth_provider_url, eth_priv_key)
	bank.set_contract_addr(eth_contract_addr)
	api = TokenAPI(bank, allowed_apps=allowed_apps)
	api.run(host=token_api_host, port=token_api_port)

# Run token system
if __name__ == "__main__":
	try:
		from contract import eth_contract_addr
	except:
		deploy()
		from contract import eth_contract_addr
	run()
