# Fab Lab Tokens
Fab Lab token system using Ethereum blockchain.

## Installation
### Requirements
Install Python requirements from `requirements.txt`.
```bash
$ pip install -r requirements.txt
```
Install solidity compiler `solc`.
```bash
$ python -m solc.install v0.4.25
```
Make sure it's in your $PATH.

### Installing as Python module (optional)
```bash
$ python setup.py install
```

## Token API
### Configuration
Token API configuration file is `tokens/config.py`. The file uses Flask's config model.
- `ETH_PROVIDER_URL` Ethereum HTTP provider URL. The application has been tested with [Infura](https://infura.io).
- `ETH_PRIV_KEY` Ethereum wallet private key.
- `ALLOWED_APPS` A dictionary of allowed applications with application username as key and password as value. The login system uses HTTP basic access authentication.

### Usage
Token API can be tested by running `tokens-run.py` and deployed to production by using `tokens.wsgi`. File `tokens/contract.py` is generated when the API is ran at the first time. This file includes deployed Ethereum contract address.

## Document Fetcher
### Configuration
Document Fetcher configuration is done by editing `fetcher-run.py`.
- `doc_api_url` Documentation site API URL.
- `token_api_url` Token API URL.
- `token_api_user` Application username for the Token API.
- `token_api_passwd` Application password for the Token API.
- `fetch_interval` Delay between fetches in seconds.
- `pfile` Python pickle file name that will be used to store some runtime settings.
- `loglevel` Python logging module logging level.

### Usage
Document Fetcher is launched by running `fetcher-run.py`. External software should be used for daemonization.
