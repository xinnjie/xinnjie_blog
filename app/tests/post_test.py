import unittest
import sqlite3
import os.path
from datetime import datetime

from markdown import markdown

from app.stuff import Post
from app import app


class PostTest(unittest.TestCase):
	def setUp(self):
		self.con = sqlite3.connect(app.config['DB_URL'])
		self.post = Post('mdmd')

	def test_post_add(self):
		post = self.post
		post.categories = ['garbage']
		with open(os.path.join(app.config['ARTICLES_FOLDER'], 'mdmd-garbage.md')) as f:
			post.content = markdown(f.read())
		post.datetime = datetime.now()
		post.commit()

		row = self.con.execute('select * from post where title = ?', (post.title,)).fetchone()
		self.assertTrue(row is not None)

	def tearDown(self):
		self.post.delete()
		self.post.commit()
		self.con.close()


class PostLoadFromFileTest(unittest.TestCase):
	def setUp(self):
		self.con = sqlite3.connect(app.config['DB_URL'])
		row = self.con.execute('select * from post where title = ?', ('mdmd',)).fetchone()
		self.assertTrue(row is None)
		self.post = Post.load_from_articles_folder('mdmd')

	def test_post_add(self):
		post = self.post
		post.commit()
		con = sqlite3.connect(app.config['DB_URL'])
		row = con.execute('select * from post where title = ?', (post.title,)).fetchone()
		self.assertTrue(row is not None)
		self.assertTrue(row[1] == 'mdmd')

	def tearDown(self):
		self.con.close()
		self.post.delete()
		self.post.commit()


class GetPostsTest(unittest.TestCase):
	def setUp(self):
		with sqlite3.connect(app.config['DB_URL']) as con:
			rows = con.execute('select * from post where title="mdmd" or title="README"').fetchall()
			self.assertEqual(len(rows), 0)
		Post.load_from_articles_folder('README').commit()
		Post.load_from_articles_folder('mdmd').commit()

	def test_get_posts_by_category(self):
		posts = Post.get_posts_by_category('garbage')
		self.assertEqual(len(posts), 2)

	def tearDown(self):
		Post('mdmd').delete().commit()
		Post('README').delete().commit()


if __name__ == '__main__':
	unittest.main()
