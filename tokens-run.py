#!/usr/bin/python3

from tokens import app

token_api_host = "localhost"
token_api_port = 8080

if __name__ == "__main__":
	app.run(host=token_api_host, port=token_api_port)
