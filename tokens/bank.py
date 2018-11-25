# Blockchain related functionality

# Ethereum blockchain based bank

from web3 import Web3
import solc

import os

class Bank:
	""" Our Ethereum bank Web3 implementation. """
	def __init__(self, http_url):
		self.url = http_url
		
		self._provider = Web3.HTTPProvider(self.url)
		self._w3 = Web3(self._provider)
		
		self._w3.eth.defaultAccount = self._w3.eth.accounts[0]
		
		self._iface = self._contract_compile()
		
		self.contract_addr = None
		self._bank_inst = None
	
	def _contract_compile(self):
		fn = os.path.join(
			os.path.dirname(os.path.abspath(__file__)),
			"sol",
			"bank.sol"
		)
		src = solc.compile_files([fn])
		return list(src.values())[0]
	
	def contract_deploy(self):
		""" Deploys our contract to blockchain. Should be called only once. """
		Bank = self._w3.eth.contract(
			abi=self._iface["abi"],
			bytecode=self._iface["bin"]
		)
		tx_hash = Bank.constructor().transact()
		tx_receipt = self._w3.eth.waitForTransactionReceipt(tx_hash)
		return tx_receipt.contractAddress
	
	def set_contract_addr(self, addr):
		""" Sets the contract address to use. """
		self.contract_addr = addr
		self._bank_inst = self._w3.eth.contract(
			address=self.contract_addr,
			abi=self._iface["abi"],
		)
	
	def get_tokens(self, token_id):
		return self._bank_inst.functions.get_tokens(token_id).call()
	
	def withdraw(self, token_id, tokens):
		func = self._bank_inst.functions.withdraw(token_id, tokens)
		if not func.call():
			raise Exception("Not enough tokens")
		self._w3.eth.waitForTransactionReceipt(func.transact())
		return self.get_tokens(token_id)
	
	def deposit(self, token_id, tokens):
		func = self._bank_inst.functions.deposit(token_id, tokens)
		if not func.call():
			return 0
		self._w3.eth.waitForTransactionReceipt(func.transact())
		return self.get_tokens(token_id)
