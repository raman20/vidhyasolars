from flask import Flask,render_template,request
import os
import sqlite3 as sq

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
	if request.method == 'GET':
		return render_template('index.html')
	elif request.method == 'POST':
		name = request.form.get('name')
		email = request.form.get('email')
		if not email:
			email = 'no email'
		bill = request.form.get('bill')
		if not bill:
			bill = 'no bill'
		phone = request.form.get('phone')
		date = 'current_date'

		print(name,email,bill,phone,date)

		con = sq.connect('database.db')
		cur = con.cursor()
		cur.execute("insert into test(name,email,bill,phone,date) values(?,?,?,?,current_date)",(name,email,bill,phone))
		cur.close()
		con.commit()
		con.close()	

		return render_template('index.html')


@app.route('/**userdata**')
def database():
	con = sq.connect('database.db')
	cur = con.cursor()
	cur.execute("select * from test")
	data = cur.fetchall()
	data.reverse()
	cur.close()
	con.commit()
	con.close()
	return render_template('database.html',data=data)

if __name__ == "__main__":
	app.run(host='localhost',port=9090)