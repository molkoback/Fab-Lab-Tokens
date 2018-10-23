#!/usr/bin/python3

from fetcher import DocumentFetcher

import logging
import sys

# Document fetcher settings
doc_api_url = "http://localhost:5000/api/contents/"
token_api_url = "http://localhost:8080/api/"
fetch_interval = 10

def init_logging():
	level = logging.INFO
	root = logging.getLogger()
	root.setLevel(level)
	ch = logging.StreamHandler(sys.stdout)
	ch.setLevel(level)
	formatter = logging.Formatter(
		"[%(asctime)s][%(levelname)s] %(message)s",
		datefmt="%H:%M:%S"
	)
	ch.setFormatter(formatter)
	root.addHandler(ch)

# Run document fetcher
if __name__ == "__main__":
	init_logging()
	df = DocumentFetcher(doc_api_url, token_api_url)
	df.run(fetch_interval=fetch_interval)
