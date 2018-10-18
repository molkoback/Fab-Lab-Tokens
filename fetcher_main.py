#!/usr/bin/python3

from fetcher import DocumentFetcher

# Document fetcher settings
doc_api_url = "http://localhost:5000/api/contents/"
token_api_url = "http://localhost:8080"
fetch_interval = 60 * 10 # 10 min

# Run document fetcher
if __name__ == "__main__":
	df = DocumentFetcher(doc_api_url, token_api_url)
	df.run(fetch_interval=fetch_interval)
