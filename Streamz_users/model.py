import requests
import json
import web
import sqlite3

db = web.database(dbn='sqlite', db='streamz.db')

def new_user(firstname,lastname,phone,email,username,pwd):
	id=db.insert('user', firstname=firstname, lastname=lastname, phone=phone,email=email,username=username,pwd=pwd)
	return json.dumps(id)


def check_user(username,password):
	authdb = sqlite3.connect('streamz.db')
	check = authdb.execute('select * from users where username=? and pwd=?', (username, password))
	if check: 
		logged={'loggedin':true}
		#raise web.seeother('/results')
		return json.dumps(logged)   
	else: 
		error={'Those login details dont work.':try_again} 
		return json.dumps(error)

