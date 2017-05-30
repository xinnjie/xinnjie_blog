import unittest
import sqlite3

loremipsum = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi. Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum. Typi non habent claritatem insitam; est usus legentis in iis qui facit eorum claritatem. Investigationes demonstraverunt lectores legere me lius quod ii legunt saepius. Claritas est etiam processus dynamicus, qui sequitur mutationem consuetudium lectorum. Mirum est notare quam littera gothica, quam nunc putamus parum claram, anteposuerit litterarum formas humanitatis per seacula quarta decima et quinta decima. Eodem modo typi, qui nunc nobis videntur parum clari, fiant sollemnes in futurum.'


class loremipsumTest(unittest.TestCase):
	def setUp(self):
		self.con = sqlite3.connect('../blog.db')

	def tearDown(self):
		self.con.close()

	def test_append_post(self):
		cur = self.con.cursor()
		res = cur.execute('select title, content, timestamp from post where title = "loremispum"')
		if res.fetchone() is None:
			cur.execute('insert into post (title, category, content, timestamp) values (?,?,?,?);',
			            ('loremsump', 'reading', loremipsum, '2017;3;22'))
			self.con.commit()
		self.assertTrue(cur.execute('select * from post').fetchone() is not None)


if __name__ == '__main__':
	unittest.main()
