import requests

class TokenSender:
	""" Sends tokens to blockchain API. """
	def __init__(self, token_api_url):
		self.url = token_api_url
	
	def post(self, token_id, tokens):
		""" Token API POST request to insert tokens. """
		data = data={
			"token_id": token_id,
			"tokens": tokens
		}
		return requests.post(self.url, data=data).json()
	
	def send(self, token_id, tokens):
		""" Sends tokens to blockchain API. """
		json = self.post(token_id, tokens)
		if json["error"]:
			raise Exception(json["error"])
