# Flask API
# Document fetcher gives us tokens
# Scheduler takes them

from .bank import Bank

import flask
from flask_httpauth import HTTPBasicAuth

import json

class TokenAPI(flask.Flask):
	""" Token API Flask child class.  """
	def __init__(self, eth_provider_url, eth_contract_addr, **kwargs):
		super().__init__(__name__)
		
		self.allowed_apps = kwargs.get("allowed_apps", {})
		self.auth = HTTPBasicAuth()
		self.bank = Bank(eth_provider_url)
		self.bank.set_contract_addr(eth_contract_addr)
		
		self.routes_create()
	
	def routes_create(self):
		""" Constructs our GET and POST request Flask routes. """
		@self.auth.get_password
		def get_pw(user):
			if user in self.allowed_apps:
				return self.allowed_apps[user]
			return None
		
		@self.route("/api/", methods=["GET"])
		@self.auth.login_required
		def get_api():
			token_id = flask.request.args.get("token_id")
			obj = self.tokens_get(token_id)
			return self.tokens_resp(obj)
		
		@self.route("/api/", methods=["POST"])
		@self.auth.login_required
		def post_api():
			token_id = flask.request.form.get("token_id")
			tokens = flask.request.form.get("tokens")
			obj = self.tokens_post(token_id, tokens)
			return self.tokens_resp(obj)
	
	def tokens_resp(self, obj):
		""" Constructs a JSON HTTP response. """
		return flask.jsonify(obj)
	
	def token_id_valid(self, token_id):
		try:
			int(token_id, 16)
		except:
			return False
		return len(token_id) == 64
	
	def tokens_get(self, token_id):
		""" Our GET API. """
		if token_id == None or not self.token_id_valid(token_id):
			return {"error": "Invalid parameters"}
		token_id = token_id.lower()
		return {
			"error": "",
			"tokens": self.bank.get_tokens(token_id)
		}
	
	def tokens_post(self, token_id, tokens):
		""" Our POST API. """
		if token_id == None or tokens == None or not self.token_id_valid(token_id):
			return {"error": "Invalid parameters"}
		token_id = token_id.lower()
		try:
			tokens = int(tokens)
		except:
			return {"error": "Invalid parameters"}
		
		if tokens <= 0:
			tokens = abs(tokens)
			try:
				total = self.bank.withdraw(token_id, tokens)
			except Exception as e:
				return {"error": str(e)}
			deposited = 0
			withdrawn = tokens
		else:
			total = self.bank.deposit(token_id, tokens)
			deposited = tokens
			withdrawn = 0
		
		return {
			"error": "",
			"token_id": token_id,
			"tokens": {
				"total": total,
				"deposited": deposited,
				"withdrawn": withdrawn
			}
		}
