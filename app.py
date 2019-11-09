import json
import time
import os
from lxml import html
from services import ss, psi, jpred, raptorx, pss, sable, sspro, yaspin, emailtools, fileoutput
from datetime import datetime

from forms import SubmissionForm
from flask import Flask, render_template, request, current_app,send_file, redirect, url_for
from multiprocessing.pool import ThreadPool
import secrets

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import sql

DATABASE_URL = os.environ.get('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

def dbselect(rowid):
	cursor = conn.cursor(cursor_factory=RealDictCursor)
	cursor.execute("SELECT * FROM seqtable WHERE ID = (%s)",(rowid,))
	jsonresults = json.dumps(cursor.fetchall(), indent=2)
	cursor.close()
	return jsonresults

def dbinsert(rowid, rowseq):
	cursor = conn.cursor()
	cursor.execute("INSERT INTO seqtable (ID, SEQ) VALUES (%s, %s)", (rowid, rowseq))
	conn.commit()
	cursor.close()

def dbupdate(rowid, rowcol, rowval):
	cursor = conn.cursor()
	cursor.execute(
		sql.SQL("UPDATE seqtable SET {} = (%s) WHERE ID = (%s)")
		.format(sql.Identifier(rowcol.lower())),(rowval, rowid))
	conn.commit()
	cursor.close()

#Dictionary containing sites and their classes
siteDict = {
	"JPred": jpred,
	"PSI": psi,
	"PSS": pss,
	"RaptorX": raptorx,
	"Sable": sable,
	"Yaspin": yaspin,
	"SSPro": sspro
}

runningCounter = {
	"JPred": 0,
	"PSI": 0,
	"PSS": 0,
	"RaptorX": 0,
	"Sable": 0,
	"Yaspin": 0,
	"SSPro": 0
}


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET')
if app.config['SECRET_KEY'] is None:
	app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

email_service = emailtools.login()
email = emailtools.getEmailAddress(email_service)

#Url of hosted site
siteurl = os.environ.get('SITE_URL')
if siteurl is None :
	siteurl = ""

@app.route('/', methods = ['GET', 'POST'])
def hello(name=None):
	form = SubmissionForm() 
	if form.validate_on_submit():
		post_data = {
			'seqtext': ''.join(form.seqtext.data.split()),
			'email': form.email.data,
			'JPred': form.JPred.data,
			'PSI':   form.PSI.data,
			'PSS':   form.PSS.data,
			'RaptorX': form.RaptorX.data,
			'Sable':   form.Sable.data,
			'Yaspin':   form.Yaspin.data,
			'SSPro':   form.SSPro.data,
			'submitbtn': 'Submit'
			}

		total_sites = validate_sites(post_data)
		post_data.update({'total_sites' : total_sites, 'completed': 0}) # add total into to post_data dictionary and a completed prediction counter
		print(post_data)
		seq = post_data['seqtext']
		startTime = emailtools.randBase62()
		

		if post_data['email'] != "": #send email to let users know input was received
			emailtools.sendEmail(email_service, post_data['email'],"Prediction Input Received", "<div>Input received for the following sequence:</div><div>" + seq + "</div><div>Results with customization options will be displayed at the following link as soon as they are available:</div><div>" + siteurl + "/dboutput/" + startTime +"</div>")

		#Stores currently completed predictions
		ssObject = []
		#Prepare files for saving results
		fileoutput.createFolder(startTime)
		fileoutput.createHTML(startTime, ssObject, seq)
		
		dbinsert(startTime, seq)
		
		sendData(seq, startTime, ssObject, post_data)
		return redirect(url_for('showdboutput', var = startTime))

	return render_template('index.html', form = form, counter = runningCounter) #default submission page


@app.route('/archive/<page>')
def showall(page):
	if page[0] == '0':
		return("Page not found")
	if page.isdigit():
		if int(page) >= 1:
			#'''
			namelist = []
			timelist= []
			seqlist= []
			
			cursor = conn.cursor(cursor_factory=RealDictCursor)
			limit = 20
			offset = limit * int(page)
			cursor.execute("SELECT id, seq FROM seqtable LIMIT %s OFFSET %s", (limit, offset))
			jsonresults = json.dumps(cursor.fetchall(), indent=2)
			
			cursor.close()		

			return render_template('archives.html', data = jsonresults, pagenum = page)
			'''
			return(page)
			'''
	else:
		return("Page not found")

@app.route('/archive')
def redarchive():
	return redirect(url_for('showall', page = 1))


@app.route('/output/<var>')
def showoutput(var):
	#print("showing output")
	print('output/'+var+'/'+var+'.html')
	try:
		return send_file('output/'+var+'/'+var+'.html')
	except Exception as e:
		return "not found"

@app.route('/dboutput/<var>')
def showdboutput(var):
	outputjson = dbselect(var)
	try:
		return render_template('dboutput.html', data = outputjson)
	except Exception as e:
		return "not found"

def run(predService, seq, email, name, ssObject,
 startTime, post_data, email_service = None):
	tempSS = predService.get(seq, email, email_service)
	runningCounter[tempSS.name] -= 1
	
	dbupdate(startTime, tempSS.name + "pred", tempSS.pred)
	dbupdate(startTime, tempSS.name + "conf", tempSS.conf)
	dbupdate(startTime, tempSS.name + "stat", tempSS.status)

	if tempSS.status >= 1:
		if tempSS.status == 1 or tempSS.status == 3:
			ssObject.append(tempSS)
			majority = majorityVote(seq, ssObject)
			dbupdate(startTime, 'majorityvote', majority)
			post_data.update({'output' : fileoutput.createHTML(startTime, ssObject, seq, majority)}) #create HTML and store it in post_data
		
		post_data['completed'] += 1
		if post_data['completed'] == post_data['total_sites']:
			print("All predictions completed.")
			if post_data['email'] != "": #if all completed and user email is not empty, send email
				print ("Sending results to " + post_data['email'])
				emailtools.sendEmail(email_service, post_data['email'],"Prediction Results", post_data['output'])


#Sends sequence based off whatever was selected before submission
def sendData(seq, startTime, ssObject, post_data):
	pool = ThreadPool(processes=post_data['total_sites'])
	for key in post_data.keys():
		if key in siteDict:
			if post_data[key]:
				pool.apply_async(run, (siteDict[key], seq, email, key, ssObject, startTime, post_data, email_service))
				print("Sending sequence to " + key)
				runningCounter[key] += 1

#Takes current completed outputs and conducts a majority vote then returns it. If a majority vote results in an equal value, currently defaults to 'X'
def majorityVote(seq, ssObject):
	output = ''
	if len(ssObject) >= 2: #vote only if more than 2 ssObjects exist (at least 2 predictions)
		#create a counter for each character appearance
		seqLength = len(seq)
		cCount = [0] * seqLength
		hCount = [0] * seqLength
		eCount = [0] * seqLength
		
		for i in ssObject:
			if i.status == 1 or i.status == 3:
				for j in range(0, seqLength):
					if i.pred[j] == 'C':
						cCount[j] += 1
					elif i.pred[j] == 'E':
						eCount[j] += 1
					elif i.pred[j] == 'H':
						hCount[j] += 1

		for i in range(0, seqLength):
			if eCount[i] > hCount[i] and eCount[i] > cCount[i]:
				output += 'E'
			elif hCount[i] > cCount[i] and hCount[i] > eCount[i]:
				output += 'H'
			elif cCount[i] > hCount[i] and cCount[i] > eCount[i]:
				output += 'C'
			else:
				output += 'X' #use X if unsure - typically shows when not all predictions are completed
	else:
		return None
	return output

#Takes a form from post and checks if seq is empty or not. Backup measure in case elements are editted
def validate_seq(seq):
	if seq == "":
		return False
	return True

#Takes a form from post and returns the number of sites it. Backup measure in case elements are editted, and for checking if all predictions are finished
def validate_sites(form):
	count = 0
	for key in siteDict.keys():
		if form[key]:
			count += 1
	return count	

if __name__ == "__main__":
	#app.run(debug=True) #Run on localhost 127.0.0.1:5000
	app.run(host='0.0.0.0', debug=True) #Run online on public IP:5000