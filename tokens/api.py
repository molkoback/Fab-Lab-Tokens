from tokens import app, auth, bank

from flask import jsonify, request

def tokens_resp(obj):
	""" Constructs a JSON HTTP response. """
	return jsonify(obj)

def token_id_valid(token_id):
	try:
		int(token_id, 16)
	except:
		return False
	return len(token_id) == 64

def tokens_get(token_id):
	""" Our GET API. """
	if token_id == None or not token_id_valid(token_id):
		return {"error": "Invalid parameters"}
	token_id = token_id.lower()
	return {
		"error": "",
		"tokens": bank.get_tokens(token_id)
	}

def tokens_post(token_id, tokens):
	""" Our POST API. """
	if token_id == None or tokens == None or not token_id_valid(token_id):
		return {"error": "Invalid parameters"}
	token_id = token_id.lower()
	try:
		tokens = int(tokens)
	except:
		return {"error": "Invalid parameters"}
	
	if tokens <= 0:
		tokens = abs(tokens)
		try:
			total = bank.withdraw(token_id, tokens)
		except Exception as e:
			return {"error": str(e)}
		deposited = 0
		withdrawn = tokens
	else:
		total = bank.deposit(token_id, tokens)
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

@auth.get_password
def get_pw(user):
	aa = app.config["ALLOWED_APPS"]
	if user in aa:
		return aa[user]
	return None

@app.route("/api/", methods=["GET"])
@auth.login_required
def get_api():
	token_id = request.args.get("token_id")
	obj = tokens_get(token_id)
	return tokens_resp(obj)

@app.route("/api/", methods=["POST"])
@auth.login_required
def post_api():
	token_id = request.form.get("token_id")
	tokens = request.form.get("tokens")
	obj = tokens_post(token_id, tokens)
	return tokens_resp(obj)
