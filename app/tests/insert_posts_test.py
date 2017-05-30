import unittest
import os.path
import sqlite3

from app import DB_URL
from app.util import load_post2db

SWITCH = True
p = '/Users/gexinjie/Documents/MyProject/--master/app/articles/mdmd-garbage.md'


class InsertPostsTest(unittest.TestCase):
	def setUp(self):
		self.con = sqlite3.connect(DB_URL)
		row = self.con.execute('select title from post where title = "mdmd"')
		if row:
			self.con.execute('delete from post where title = "mdmd"')
			self.con.commit()

	def tearDown(self):
		self.con.close()

	def test_insert_post(self):
		cur = self.con.cursor()
		filename = os.path.basename(p).rstrip('.md')
		title, category = filename.split('-')

		row = cur.execute('select title from post where title = "{}"'.format(title)).fetchone()
		self.assertTrue(row is None)

		load_post2db(p)

		row = cur.execute('select title from post where title = "{}"'.format(title)).fetchone()
		self.assertTrue(row is not None)


if __name__ == '__main__':
	unittest.main()
