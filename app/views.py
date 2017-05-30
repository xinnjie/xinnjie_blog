from flask import render_template, url_for, redirect, abort

from .blog_app import app
from .stuff import Post


@app.route('/')
@app.route('/index')
def index():
	posts = Post.get_posts()
	return render_template("index.html", title='xinjie', posts=posts)


@app.route('/articles/<article_title>')
def articles(article_title: str):
	posts = Post.get_posts('title = "{}"'.format(article_title))
	if posts:
		return render_template("article.html", post=posts[0])
	return abort(404)


@app.route('/categories/<category_name>')
def categories(category_name: str):
	if category_name not in app.config['CATEGORY_NAMES']:
		abort(404)

	posts = Post.get_posts_by_category(category_name)
	return render_template("categories.html", posts=posts, title=category_name)


@app.route('/about')
def aboutme():
	return render_template('about.html')


@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html')
