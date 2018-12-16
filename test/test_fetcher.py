from fetcher import *

import unittest
import json

class TestFetcher(unittest.TestCase):
	def open_post(self):
		with open("data/post.json") as fp:
			post = fetcher.Post(json.load(fp))
		return post
	
	def test_post(self):
		post = self.open_post()
		self.assertEqual(post.id, 74)
		self.assertEqual(post.token_id, "b36a83701f1c3191e19722d6f90274bc1b5501fe69ebf33313e440fe4b0fe210")
		self.assertEqual(post.time, 1539016000)
		self.assertEqual(post.word_count, 8)
		self.assertEqual(post.image_count, 2)
		self.assertEqual(post.audio_count, 1)
		self.assertEqual(post.file_count, 1)
	
	def test_converter(self):
		post = self.open_post()
		conv = converter.Converter()
		tokens = conv.post2tokens(post)
		self.assertEqual(tokens, 41)

	# Initiates a Settings Object from an empty file and asserts
	# that it is empty. Then sets one file and asserts that the 
	# dictionary has one entry
	# Uses the get function and asserts that the result pushed is the same
	# with the one pulled
	def test_settings(self):
		settings = fetcher.Settings("data/settingsFile.p")
		self.assertEqual(False, bool(settings.dict))
		settings.set("1", "Hello world")
		self.assertEqual(True, bool(settings.dict))
		self.assertEqual("Hello world", settings.get("1"))
		with open("data/settingsFile.p", "w") as fp:
			fp.seek(0)
			fp.truncate()

if __name__ == "__main__":
	unittest.main()
