import sqlite3
import hashlib
import os
from datetime import datetime

from markdown import markdown

from .blog_app import app


class Post:
	"""
	attribute:
		title: str
		categories: list(of str)
		content: str
		datetime: datetime


		post in db:
		ID INTEGER PRIMARY KEY AUTOINCREMENT,
		 TITLE CHAR(50) NOT NULL, 
		CATEGORYA CHAR(50) NOT NULL, 
		CATEGORYB CHAR(50), 
		CATEGORYC CHAR(50), 
		CATEGORYD CHAR(50), 
		CONTENT TEXT NOT NULL, 
		DATETTIME CHAR(30) NOT NULL
	"""

	def __init__(self, title: str):
		self._con = sqlite3.connect(app.config['DB_URL'])
		cur = self._con.cursor()

		row = cur.execute('SELECT * FROM post WHERE title = ?', (title,)).fetchone()
		if row:
			self._title = title
			self.categories = [m for m in row[2:6] if m != '']
			self.content = row[6]
			self.datetime = row[7]
		else:
			self._title = title
			self.categories = None
			self.content = None
			self.datetime = None
			# 向db中添加一个占位行, 不用commit，commit操作交与post.commit()执行
			cur.execute('INSERT INTO post (title, categorya, categoryb, categoryc, categoryd, content, datetime)'
			            'VALUES (?,?,?,?,?,?,?)', (self.title, '', '', '', '', '', ''))

	def __del__(self):
		self._con.close()

	def commit(self):
		"""
		如果有update行为， 需要调用commit以使操作生效
		not null 列属性不可以为空
		"""
		if self.title and self.categories and self.content and self.datetime:
			# 向categories属性填充进占位空字符串
			if len(self.categories) < 4:
				for i in range(4 - len(self.categories)):
					self.categories.append('')

			cur = self._con.execute('UPDATE post SET categorya=?, categoryb=?, categoryc=?, categoryd=?,'
			                        ' content=?, datetime=? WHERE title =?',
			                        (self.categories[0], self.categories[1], self.categories[2], self.categories[3],
			                         self.content, self.datetime.strftime(app.config['DATETIME_FORMAT']), self.title))
			self._con.commit()
		else:
			raise ValueError(self.__class__, 'commit with None value')

	def delete(self):
		"""
		删除post自己
		:return: Post
		"""
		cur = self._con.cursor()
		cur.execute('DELETE FROM post WHERE title=?', (self.title,))
		return self

	@classmethod
	def load_from_articles_folder(cls, article_name: str):
		"""
		:param article_name:  the complete file name
						e.g. example-catgoryA-categoryB.md
					Or  the title
						e.g. example match the filename  example-catgoryA-categoryB.md
		:return: Post
		:exception if article not found in the articles_folder raise  FileNotFoundError
		"""
		# 所有文件名打包为 filenames
		filenames = []
		for _, _, fnames in os.walk(app.config['ARTICLES_FOLDER']):
			filenames.extend(fnames)

		# 处理article_name 使其拓展成文件全名
		if not article_name.endswith('.md'):
			for filename in filenames:
				if filename.startswith(article_name):
					article_name = filename
					break
		# article_name 此时有几种情况
		# 1.本来不含拓展名，但经过拓展现在有拓展名的 ok
		# 2.本来不含拓展名，但找不到文件拓展的 no
		# 3.本来有拓展名，找到文件 ok
		# 4.本来有拓展名，找不到文件 no
		# 直接尝试open, 能找到OK，不能找到抛出FileNotFoundError
		with open(os.path.join(app.config['ARTICLES_FOLDER'], article_name)) as f:
			article_name = article_name.rstrip('.md')
			title, *categories = article_name.split('-')
			post = Post(title)
			post.categories = categories
			post.content = markdown(f.read())
			post.datetime = datetime.now()

		return post

	@classmethod
	def get_posts_by_category(cls, categoryname: str):
		"""
		:param: categoryname
		:return: list Posts
		"""
		with sqlite3.connect(app.config['DB_URL']) as con:
			rows = con.execute('select title from post where categorya=? or categoryb=? or categoryc=? or categoryd=?',
			                   (categoryname, categoryname, categoryname, categoryname)).fetchall()
			titles = [title[0] for title in rows]
		posts = []
		for title in titles:
			posts.append(Post(title))
		return posts

	@classmethod
	def get_posts(cls, condition: str = '1'):
		with sqlite3.connect(app.config['DB_URL']) as con:
			rows = con.execute('select title from post where {}'.format(condition)).fetchall()
			titles = [title[0] for title in rows]
		posts = []
		for title in titles:
			posts.append(Post(title))
		return posts

	@property
	def title(self):
		"""
		title 不可更改
		"""
		return self._title

	@property
	def thumbnail(self):
		if self.content is None:
			raise AttributeError(self.__class__, 'has content attribute of None')
		lines = self.content.splitlines(keepends=True)
		n = min(app.config['POST_THUMBNAIL_LINES'], len(lines))
		thumbnail = ''.join(lines[0:n])
		return thumbnail

	@property
	def datetime(self):
		return self._datetime

	@datetime.setter
	def datetime(self, time: str or datetime):
		if isinstance(time, datetime):
			self._datetime = time
		elif isinstance(time, str):
			self._datetime = datetime.strptime(time, app.config['DATETIME_FORMAT'])

	@property
	def md5(self):
		if self.content is None:
			raise AttributeError(self.__class__, 'has content attribute of None')
		return hashlib.md5(self.content.encode()).hexdigest()
