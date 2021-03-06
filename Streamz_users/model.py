import requests
import json
import web
import sqlite3
import hashlib

db = web.database(dbn='sqlite', db='streamz.db')

def subscribe(username,uploader):
	db.insert('subscriber', channel=uploader,username=username)
	params={'subscribestatus':"Subscribed"}
	return json.dumps(params)

def unsubscribe(username,uploader):
	authdb = sqlite3.connect('streamz.db')
	cursor=authdb.cursor()
	cursor.execute('select * from subscriber where channel=? and username=?',(uploader,username))
	data=cursor.fetchone()
	id=data[0]
	db.delete('subscriber', where="sid=$id", vars=locals())	
	params={'subscribestatus':"Unsubscribed"}
	return json.dumps(params)

def get_subscribestatus(username,uploader):
	authdb = sqlite3.connect('streamz.db')
	cursor=authdb.cursor()
	cursor.execute('select * from subscriber where channel=? and username=?',(uploader,username))
	data=cursor.fetchone()
	if data is None:
		params={'subscribestatus':0}
	else:
		params={'subscribestatus':1}	
	return json.dumps(params)

def update_like(username,videoid):
	authdb = sqlite3.connect('streamz.db')
	cursor=authdb.cursor()
	cursor.execute('select * from likestatus where username=? and videoid=?',(username,videoid))
	data=cursor.fetchone()
	if data is None:
		id=db.insert('likestatus', username=username,videoid=videoid,status=1)
	elif data[3]==2:
		id=data[0]
		db.update('likestatus',where='id=$id',vars=locals(), status=1)
	params={'likestatus':"Liked"}
	return json.dumps(params)

def update_dislike(username,videoid):
	authdb = sqlite3.connect('streamz.db')
	cursor=authdb.cursor()
	cursor.execute('select * from likestatus where username=? and videoid=?',(username,videoid))
	data=cursor.fetchone()
	if data is None:
		id=db.insert('likestatus', username=username,videoid=videoid,status=2)
	elif data[3]==1:
		id=data[0]
		db.update('likestatus',where='id=$id',vars=locals(), status=2)
	params={'likestatus':"Disliked"}
	return json.dumps(params)

def update_nonelike(username,videoid):
	authdb = sqlite3.connect('streamz.db')
	cursor=authdb.cursor()
	cursor.execute('select * from likestatus where username=? and videoid=?',(username,videoid))
	data=cursor.fetchone()
	id=data[0]
	db.delete('likestatus', where="id=$id", vars=locals())
	params={'likestatus':"Noneliked"}
	return json.dumps(params)

def get_likestatus(username,videoid):
	authdb = sqlite3.connect('streamz.db')
	cursor=authdb.cursor()
	cursor.execute('select * from likestatus where username=? and videoid=?',(username,videoid))
	data=cursor.fetchone()
	if data is None:
		params={'likestatus':0}
	else:
		params={'likestatus':data[3]}
	return json.dumps(params)


def new_user(firstname,lastname,phone,email,username,pwd,subscribers,likes,dislikes,joined):
	id=db.insert('user', firstname=firstname, lastname=lastname,email=email,username=username,pwd=pwd,phone=phone,subscribers=subscribers,likes=likes,dislikes=dislikes,joined=joined)
	params={'status':'Registered','username':username}
	return json.dumps(params)
	
def check_user(username,password):
    authdb = sqlite3.connect('streamz.db')
    #passhash = hashlib.md5(password).hexdigest()
    c= authdb.execute('select * from user where username=? and pwd=?',(username,password))
    row = c.fetchone()
    if row == None:
		logged={"loggedin":"false"}
		return json.dumps(loggedin) 
    else: 
			params={'status':'LoggedIn','username':username}
			return json.dumps(params)
	#error={"loggedin":"true","username":username} 

def get_user(username):
	authdb = sqlite3.connect('streamz.db')
	c= authdb.execute('select * from user where username=?',[username])
	row = c.fetchone()
	fn=row[1]
	ln=row[2]
	eml=row[3]
	un=row[4]
	ph=row[6]
	dob=row[7]
	coun=row[8]
	cat=row[9]
	subs=row[10]
	lik=row[11]
	dlik=row[12]
	about=row[14]
	param={'firstname':fn, 'lastname':ln,'email':eml,'username':un,'phone':ph,'dob':dob,'country':coun,'category':cat,'subscribers':subs,'likes':lik,'dislikes':dlik,'about':about}	
	return json.dumps(param)
	
def update_user(profilepic,coverpic,firstname,lastname,phone,email,username,dob,country,category,about):
	db.update('user', where='username= $username',vars=locals(), firstname=firstname, lastname=lastname,phone=phone,email=email, dob=dob,country=country,category=category,profilepic=profilepic,coverpic=coverpic,about=about)
	if profilepic!='static/profilepic/': 
		db.update('user',where='username= $username',vars=locals(), profilepic=profilepic)
	if coverpic!='static/coverpic/': 
		db.update('user',where='username= $username',vars=locals(), coverpic=coverpic)
	params={'status':'updated'}
	return json.dumps(params)

	
def get_dob(username):

	authdb = sqlite3.connect('streamz.db')
	c= authdb.execute('select * from user where username=?',[username])
	row = c.fetchone()
	dob=row[7]
	param={'dob':dob}
	print param
	return json.dumps(param)

def get_country(username):

	authdb = sqlite3.connect('streamz.db')
	c= authdb.execute('select * from user where username=?',[username])
	row = c.fetchone()
	coun=row[8]
	param={'country':coun}
	print param
	return json.dumps(param)

def get_profilepic(id):
	authdb = sqlite3.connect('streamz.db')
	c= authdb.execute('select * from user where username=?',[username])
	row = c.fetchone()
	url=row[15]
	return open(url,"rb").read()

def get_coverpic(id):
	authdb = sqlite3.connect('streamz.db')
	c= authdb.execute('select * from user where username=?',[username])
	row = c.fetchone()
	url=row[16]
	return open(url,"rb").read()

