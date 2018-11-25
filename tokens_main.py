#!/usr/bin/python3

from tokens import TokenAPI

import logging
import sys

# Token system settings
token_api_host = "localhost"
token_api_port = 8080

# Ethereum settings
eth_provider_url = "http://127.0.0.1:8545"
eth_contract_addr = ""

allowed_apps = {
	"document-fetcher": "password",
	"scheduler": "password"
}

# Run token system
if __name__ == "__main__":
	api = TokenAPI(
		eth_provider_url,
		eth_contract_addr,
		allowed_apps=allowed_apps
	)
	api.run(host=token_api_host, port=token_api_port)
