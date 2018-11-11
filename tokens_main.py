#!/usr/bin/python3

from tokens import TokenAPI

# Token system settings
token_api_host = "localhost"
token_api_port = 8080

allowed_apps = {
	"document-fetcher": "password",
	"scheduler": "password"
}

# Run token system
if __name__ == "__main__":
	api = TokenAPI(allowed_apps=allowed_apps)
	api.run(host=token_api_host, port=token_api_port)
