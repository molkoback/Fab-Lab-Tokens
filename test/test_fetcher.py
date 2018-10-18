from fetcher import * 

import unittest
import json

class TestFetcher(unittest.TestCase):
	def test_post(self):
		with open("data/post.json") as fp:
			post = fetcher.Post(json.load(fp))
		self.assertEqual(post.id, 74)
		self.assertEqual(post.token_id, "b36a83701f1c3191e19722d6f90274bc1b5501fe69ebf33313e440fe4b0fe210")
		self.assertEqual(post.time, 1539016000)
		self.assertEqual(post.word_count, 8)
		self.assertEqual(post.image_count, 2)
		self.assertEqual(post.audio_count, 1)
		self.assertEqual(post.file_count, 1)

if __name__ == "__main__":
	unittest.main()
