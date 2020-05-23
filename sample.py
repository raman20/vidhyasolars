import os
from wsgiref.simple_server import make_server
from jinja2 import Environment, FileSystemLoader
from cgi import parse_qs,escape
import sqlite3

class application:
	def __init__(self):
		self.routes = {}

	def __call__(self,environ,start_response):
		response,status = self.handle_request(environ)
		response_headers = [('Content-type','text/html'),]
		start_response(status,response_headers)
		return [response.encode('utf-8')]

	def handle_request(self,environ):
		path = environ.get('PATH_INFO')
		if self.routes.get(path):
			status = '200 OK'
			handler = self.routes.get(path)
			response = handler(environ)
			return response,status
		else:
			status = '404 Not Found'
			response = environ.get('PATH_INFO')
			return '<html><h1>error</h1>\n<h2>'+response+'</h2><h3>url not exist</h3><img src="https://bit.ly/2ThsRlS"></html>',status

	def add_handlers(self,path,handler):
		self.routes[path] = handler
	
app = application()


def home(environ):
	method = environ.get("REQUEST_METHOD")
	temp_env = Environment(loader = FileSystemLoader(os.path.abspath('template')))
	
	if method == 'GET':
		return temp_env.get_template('index.html').render()
	elif method == 'POST':
		request_body_size = int(environ.get('CONTENT_LENGTH',0))
		request_body = environ['wsgi.input'].read(request_body_size)
		d = parse_qs(request_body)
		
		name = d.get(b'name')[0].decode('utf-8')
		if d.get(b'email'):
			email = d.get(b'email')[0].decode('utf-8')
		else:
			email = 'no email'
		if d.get(b'bill'):
			bill = d.get(b'bill')[0].decode('utf-8')
		else:
			bill = 'no bill'
		phone = d.get(b'phone')[0].decode('utf-8')
		date = 'current_date'

		print(name,email,bill,phone,date)


		con = sqlite3.connect('database.db')
		cur = con.cursor()
		cur.execute("insert into test(name,email,bill,phone,date) values(?,?,?,?,current_date)",(name,email,bill,phone))
		cur.close()
		con.commit()
		con.close()

		return temp_env.get_template('index.html').render()
		#response_body = [f'{key}: {value}' for key, value in sorted(environ.items())]
		#response_body = '\n'.join(response_body)
		#return response_body

def database(environ):
	temp_env = Environment(loader = FileSystemLoader(os.path.abspath('template')))
	con = sqlite3.connect('database.db')
	cur = con.cursor()
	cur.execute("select * from test")
	data = cur.fetchall()
	data.reverse()
	cur.close()
	con.commit()
	con.close()

	return temp_env.get_template('database.html').render(data=data)


app.add_handlers('/',home)
app.add_handlers('/<<userdata>>',database)

server = make_server('0.0.0.0',80,app=app)
server.serve_forever()
