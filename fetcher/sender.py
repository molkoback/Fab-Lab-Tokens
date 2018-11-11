import requests
from requests.auth import HTTPBasicAuth

class TokenSender:
	""" Sends tokens to blockchain API. """
	def __init__(self, token_api_url, **kwargs):
		self.token_api_user = kwargs.get("token_api_user", "")
		self.token_api_passwd = kwargs.get("token_api_passwd", "")
		self.url = token_api_url
	
	def post(self, token_id, tokens):
		""" Token API POST request to insert tokens. """
		if self.token_api_user and self.token_api_passwd:
			auth = HTTPBasicAuth(self.token_api_user, self.token_api_passwd)
		else:
			auth = None
		data = data={
			"token_id": token_id,
			"tokens": tokens
		}
		return requests.post(self.url, data=data, auth=auth).json()
	
	def send(self, token_id, tokens):
		""" Sends tokens to blockchain API. """
		json = self.post(token_id, tokens)
		if json["error"]:
			raise Exception(json["error"])
