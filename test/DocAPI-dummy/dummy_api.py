#!/usr/bin/python3

import flask

import json
import time

doc_api_host = "localhost"
doc_api_port = 5000

if __name__ == "__main__":
	app = flask.Flask(__name__)
	
	t = int(time.time())
	
	@app.route("/api/contents/", methods=["GET"])
	def get_api():
		with open("posts.json") as fp:
			obj = json.load(fp)
			obj["items"][0]["createtime"] = t
		return flask.jsonify(obj)
	
	app.run(host=doc_api_host, port=doc_api_port)
