import requests

class TokenSender:
	""" Sends tokens to blockchain API. """
	def __init__(self, token_api_url):
		self.url = token_api_url
	
	def send(self, token_id, tokens):
		""" TODO """
		raise NotImplementedError()
		
		# TODO
		
		r = requests.post(self.url, data={})
		return r.ok
