from .converter import Converter
from .sender import TokenSender

import requests

import os
import pickle
import time

class Settings:
	""" Pickle based storage. """
	def __init__(self, pfile):
		self.pfile = pfile
		self.dict = {}
	
	def get(self, key):
		if not key in self.dict:
			return None
		return self.dict[key]
	
	def set(self, key, val):
		self.dict[key] = val
	
	def load(self):
		with open(self.pfile, "rb") as fp:
			self.dict = pickle.load(fp)
	
	def save(self):
		with open(self.pfile, "wb") as fp:
			pickle.dump(self.dict, fp)

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
		self.settings = self.load_settings(kwargs.get("pfile", "fetcher.p"))
		
		self.converter = Converter()
		self.sender = TokenSender(token_api_url)
		
		# Load timestamp from settings
		self.stamp = self.settings.get("timestamp")
		if not self.stamp:
			self.stamp = 0
	
	def load_settings(self, pfile):
		settings = Settings(pfile)
		if os.path.isfile(pfile):
			# Load settings from file
			settings.load()
		else:
			# Create new settings file
			settings.save()
		return settings
	
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
		for post in self.fetch_post():
			# Break when we reach older posts
			if post.time < self.stamp:
				break
			self.handle_post(post)
	
	def update_time(self):
		""" Updates our timestamp and saves it to settings. """
		self.stamp = int(time.time())
		self.settings.set("timestamp", self.stamp)
		self.settings.save()
	
	def run(self, fetch_interval=600):
		""" Runs the the fetching program. """
		self.update_time()
		while True:
			self.find_new()
			self.update_time()
			time.sleep(fetch_interval)
