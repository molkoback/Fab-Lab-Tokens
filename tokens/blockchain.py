# Blockchain related functionality

class BlockChain:
	""" Dummy implementation of our blockchain storage. """
	def __init__(self):
		self.data = {}
	
	def token_id_valid(self, token_id):
		return token_id in self.data
	
	def get_tokens(self, token_id):
		return self.data[token_id]
	
	def withdraw(self, token_id, tokens):
		if not token_id in self.data:
			raise Exception("Invalid token ID")
		total = self.data[token_id] - tokens
		if total < 0:
			raise Exception("Not enough tokens")
		self.data[token_id] = total
		return total
	
	def deposit(self, token_id, tokens):
		if token_id in self.data:
			total = self.data[token_id] + tokens
		else:
			total = tokens
		self.data[token_id] = total
		return total
