from tokens import app

# Ethereum settings
app.config["ETH_PROVIDER_URL"] = ""
app.config["ETH_PRIV_KEY"] = ""

# Allowed API users
app.config["ALLOWED_APPS"] = {
	"document-fetcher": "password",
	"scheduler": "password"
}
