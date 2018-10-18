from .converter import Converter
from .sender import TokenSender

import requests

import time

class Post:
	""" Documentation post wrapper. """
	def __init__(self, json):
		self.id = json["id"]
		
		self.token_id = json["author"]["token_id"]
		self.time = json["createtime"]
		
		self.word_count = len(json["content"].split())
		self.file_count = len(json["files"])
		
		images = json["images"]
		self.image_count = len(images)
		self.audio_count = 0
		for im in images:
			try:
				if im["voice"]["id"]:
					self.audio_count += 1
			except:
				pass
	
	def __repr__(self):
		return "<Post %d>" % self.id

class DocumentFetcher:
	"""
	Fetches documents from the documentation site, converts them to tokens
	and sends the tokens to blockchain API.
	"""
	def __init__(self, doc_api_url, token_api_url, **kwargs):
		self.url = doc_api_url
		
		self.converter = Converter()
		self.sender = TokenSender(token_api_url)
		self.stamp = 0
	
	def get(self, page):
		""" Returns documentation site API page json. """
		return requests.get(self.url, params={"page": page}).json()
	
	def fetch_post(self):
		""" Yields posts from documentation site. """
		page = 1
		while True:
			json = self.get(page)
			for json_post in json["items"]:
				yield Post(json_post)
			if page >= json["pages"]:
				break
			page += 1
	
	def handle_post(self, post):
		""" Converts the post to tokens and sends them to blockchain API. """
		tokens = self.converter.post2tokens(post)
		self.sender.send(post.token_id, tokens)
	
	def find_new(self):
		""" Searches for new posts and processes them. """
		raise NotImplementedError()
		
		for post in self.fetch_post():
			
			# TODO: Make sure that the post is new
			
			self.handle_post(post)
	
	def update_time(self):
		self.stamp = int(time.time())
	
	def run(self, fetch_interval=600):
		""" Runs the the fetching program. """
		self.update_time()
		while True:
			self.find_new()
			self.update_time()
			time.sleep(fetch_interval)
