from .converter import Converter
from .sender import TokenSender

import requests

import logging
import os
import pickle
import time

class Settings:
	""" Pickle based storage. """
	def __init__(self, pfile):
		self.pfile = pfile
		self.dict = {}
		try:
			self._load()
		except:
			self._save()
	
	def _load(self):
		with open(self.pfile, "rb") as fp:
			self.dict = pickle.load(fp)
	
	def _save(self):
		with open(self.pfile, "wb") as fp:
			pickle.dump(self.dict, fp)
	
	def get(self, key, default=None):
		return self.dict.get(key, default)
	
	def set(self, key, val):
		self.dict[key] = val
		self._save()

class Post:
	""" Documentation post wrapper. """
	def __init__(self, json):
		self.id = int(json["id"])
		
		self.token_id = json["author"]["token_id"].lower()
		self.time = int(json["createtime"])
		
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
		self.settings = Settings(kwargs.get("pfile", "fetcher.p"))
		self.converter = Converter()
		self.sender = TokenSender(token_api_url, **kwargs)
	
	def get(self, page):
		""" Returns documentation site API page json. """
		try:
			return requests.get(self.url, params={"page": page}).json()
		except:
			raise Exception("Couldn't fetch from %s" % self.url)
	
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
		logging.info("%s earned %d tokens" % (post.token_id, tokens))
	
	def find_new(self):
		""" Searches for new posts and processes them. """
		for post in self.fetch_post():
			# Break when we reach older posts
			if post.time <= self.settings.get("timestamp", 0):
				break
			self.handle_post(post)
	
	def run(self, fetch_interval=600):
		""" Runs the the fetching program. """
		logging.info("Running Document Fetcher")
		while True:
			logging.info("Looking for new posts")
			try:
				self.find_new()
			except Exception as err:
				logging.error(str(err))
			else:
				# Update timestamp
				self.settings.set("timestamp", int(time.time()))
			time.sleep(fetch_interval)
