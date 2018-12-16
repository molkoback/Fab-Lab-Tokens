from tokens.bank import Bank

from flask import Flask
from flask_httpauth import HTTPBasicAuth

import os

app = Flask(__name__)
import tokens.config

auth = HTTPBasicAuth()

bank = Bank(app.config["ETH_PROVIDER_URL"], app.config["ETH_PRIV_KEY"])
try:
	# Contract file exists
	from tokens.contract import eth_contract_addr
	app.config["ETH_CONTRACT_ADDR"] = eth_contract_addr
except:
	# Contract file doesn't exist
	print("Deploying Token API Contract")
	app.config["ETH_CONTRACT_ADDR"] = bank.contract_deploy()
	print("Deployed: %s" % app.config["ETH_CONTRACT_ADDR"])
	print("Saving contract file contract.py")
	fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contract.py")
	with open(fn, "w") as fp:
		fp.write("eth_contract_addr = \"%s\"\n" % app.config["ETH_CONTRACT_ADDR"])
	print("Contract file saved")
bank.set_contract_addr(app.config["ETH_CONTRACT_ADDR"])

import tokens.api
