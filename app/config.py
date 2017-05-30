import os.path


class Config:
	DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
	APP_PATH = os.path.dirname(__file__)
	DB_URL = os.path.join(APP_PATH, 'blog.db')
	ARTICLES_FOLDER = os.path.join(APP_PATH, 'articles')
	POST_THUMBNAIL_LINES = 4
	CATEGORY_NAMES = frozenset(('net', 'algo', 'garbage', 'reading', 'default'))
	SECRET_KEY = 'HELLO'
