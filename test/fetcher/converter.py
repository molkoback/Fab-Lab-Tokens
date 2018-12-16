class Converter:
	def __init__(self):
		self.word_val = 0.2
		self.file_val = 10
		self.image_val = 10
		self.audio_val = 10
		self.tokens_max = 200
	
	def post2tokens(self, post):
		""" Converts a fetcher.Post to tokens. """
		tokens = post.word_count * self.word_val
		tokens += post.file_count * self.file_val
		tokens += post.image_count * self.image_val
		tokens += post.audio_count * self.audio_val
		return min(int(tokens), self.tokens_max)
