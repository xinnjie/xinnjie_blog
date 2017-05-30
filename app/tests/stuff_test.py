import unittest
from app.stuff import Post
from datetime import date


class StuffTest(unittest.TestCase):
	def setUp(self):
		self.post = Post()

	def test_deafault_construction(self):
		self.assertEqual(self.post.datetime.date(), date(2000, 1, 1))

	def test_datetime_setter(self):
		self.post.datetime = '2017-3-22'
		self.assertEqual(self.post.datetime.date(), date(2017, 3, 22))


if __name__ == '__main__':
	unittest.main()
