# Flask API
# Document fetcher gives us tokens
# Scheduler takes them

from .blockchain import BlockChain

import flask
from flask_httpauth import HTTPBasicAuth

import json

class TokenAPI(flask.Flask):
	""" Token API Flask child class.  """
	def __init__(self, **kwargs):
		super().__init__(__name__)
		
		self.allowed_apps = kwargs.get("allowed_apps", {})
		self.auth = HTTPBasicAuth()
		self.bc = BlockChain()
		
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
	
	def tokens_get(self, token_id):
		""" Our GET API. """
		if token_id == None:
			return {"error": "Invalid parameters"}
		elif not self.bc.token_id_valid(token_id):
			return {"error": "Invalid token ID"}
		return {
			"error": "",
			"tokens": self.bc.get_tokens(token_id)
		}
	
	def tokens_post(self, token_id, tokens):
		""" Our POST API. """
		if token_id == None or tokens == None:
			return {"error": "Invalid parameters"}
		try:
			tokens = int(tokens)
		except:
			return {"error": "Invalid parameters"}
		
		if tokens <= 0:
			tokens = abs(tokens)
			try:
				total = self.bc.withdraw(token_id, tokens)
			except Exception as e:
				return {"error": str(e)}
			deposited = 0
			withdrawn = tokens
		else:
			total = self.bc.deposit(token_id, tokens)
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
