import argparse

from .stuff import Post

parser = argparse.ArgumentParser()
parser.add_argument('--delete', '-d', dest='deleting_files', nargs='+', help='delete specific passage(s) from db'
                                                                             'e.g. -d a b c  delete passages name start with a,b,c')
parser.add_argument('--update', '-u', dest='updating_files', nargs='+', help='update specific passage(s) in the db'
                                                                             'e.g. -d a b c  delete passages name start with a,b,c')
parser.add_argument('--new', '-n', dest='new_files', nargs='+', help='import  specific passage(s) into db'
                                                                     'e.g. -d a b c  delete passages name start with a,b,c')

args = parser.parse_args('--new mdmd README'.split())

if args.new_files:
	for file_name in args.new_files:
		try:
			post = Post.load_from_articles_folder(file_name)
			post.commit()
			print(file_name, 'insert into db successfully')
		except FileNotFoundError as e:
			print(file_name, 'not found')

if args.deleting_files:
	for file_name in args.deleting_files:
		# 若file_name存在则从数据库中读取post并删除；若不存在则会创建一个占位post后进行删除；所以并不需要检查file_name是否存在
		post = Post(file_name)
		post.delete()
		post.commit()
		print(file_name, 'has been deleted successfully')

if args.updating_files:
	for file_name in args.updating_files:
		try:
			old_post = Post(file_name)
			new_post = Post.load_from_articles_folder(file_name)
			new_post.datetime = old_post.datetime
			new_post.commit()
			print(__file__, 'update successfully')
		except FileNotFoundError as e:
			print(file_name, 'not found')
