from web3 import Web3
import solc

import os

class Bank:
	""" Our Ethereum bank Web3 implementation. """
	def __init__(self, http_url, priv_key):
		self._provider = Web3.HTTPProvider(http_url)
		self._w3 = Web3(self._provider)
		self._account = self._w3.eth.account.privateKeyToAccount(priv_key)
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
	
	def _transact(self, func):
		tx = func.buildTransaction({
			"from": self._account.address,
			"nonce": self._w3.eth.getTransactionCount(self._account.address)
		})
		tx_signed = self._account.signTransaction(tx)
		tx_hash = self._w3.eth.sendRawTransaction(tx_signed.rawTransaction)
		tx_receipt = self._w3.eth.waitForTransactionReceipt(tx_hash)
		return tx_receipt.contractAddress
	
	def _call(self, func):
		return func.call({"from": self._account.address})
	
	def contract_deploy(self):
		""" Deploys our contract to blockchain. Should be called only once. """
		Bank = self._w3.eth.contract(
			abi=self._iface["abi"],
			bytecode=self._iface["bin"]
		)
		func = Bank.constructor()
		return self._transact(func)
	
	def set_contract_addr(self, addr):
		""" Sets the contract address to use. """
		self.contract_addr = addr
		self._bank_inst = self._w3.eth.contract(
			address=self.contract_addr,
			abi=self._iface["abi"],
		)
	
	def get_tokens(self, token_id):
		func = self._bank_inst.functions.get_tokens(token_id)
		return self._call(func)
	
	def withdraw(self, token_id, tokens):
		func = self._bank_inst.functions.withdraw(token_id, tokens)
		ret = self._call(func)
		if ret < 0:
			raise Exception("Not enough tokens")
		self._transact(func)
		return self.get_tokens(token_id)
	
	def deposit(self, token_id, tokens):
		func = self._bank_inst.functions.deposit(token_id, tokens)
		ret = self._call(func)
		if ret < 0:
			return 0
		self._transact(func)
		return self.get_tokens(token_id)
