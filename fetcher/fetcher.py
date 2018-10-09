# Fetches documents from the documentation site
# Converts them to tokens
# Sends them to the blockchain API

import config
from converter import Converter

import time

class DocumentFetcher:
	def __init__(self):
		self.converter = Converter()
	
	def wait(self):
		time.sleep(config.fetch_interval)
	
	def run(self):
		while True:
			print("Fetching")
			self.wait()
