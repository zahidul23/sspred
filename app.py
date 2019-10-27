import json
import time
import os
from services import ss, psi, jpred, raptorx, pss, sable, sspro, yaspin, emailtools, fileoutput
from datetime import datetime

from forms import SubmissionForm
from flask import Flask, render_template, request, current_app,send_file
from flask_socketio import SocketIO, emit, send
import secrets

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

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
socketio = SocketIO(app)

email_service = emailtools.login()
email = emailtools.getEmailAddress(email_service)

#Url of hosted site
siteurl = os.environ.get('SITE_URL')
if siteurl is None :
	siteurl = ""

@app.route('/', methods = ['GET', 'POST'])
def hello(name=None):
	if request.method == 'POST':
		post_data = dict(request.form) #Dictionary containing sent data
		#print(post_data)
		
		total_sites = validate_sites(post_data)
		post_data.update({'total_sites' : total_sites, 'completed': 0}) # add total into to post_data dictionary and a completed prediction counter
		
		if total_sites > 0 and validate_seq(post_data['seqtext']):
			return render_template('sent.html', post = post_data)#output page. keeps the same url. send post_data to begin predictions

	#request.method == 'GET':
	form = SubmissionForm() 
	return render_template('index.html', form = form) #default submission page

@app.route('/output/<var>')
def showoutput(var):
	print("showing output")
	print('output/'+var+'/'+var+'.html')
	try:
		return send_file('output/'+var+'/'+var+'.html')
	except Exception as e:
		return "not found"

def run(predService,sess, seq, email, name, ssObject,
 startTime, post_data, email_service = None):
	tempSS = predService.get(seq, email, email_service)
	
	socketio.emit('result', json.dumps({
		'pred': tempSS.pred,
		'conf': tempSS.conf,
		'pID': tempSS.name + 'pred',
		'cID': tempSS.name + 'conf',
		'status': tempSS.status}
		), room=sess)

	if tempSS.status >= 1:
		if tempSS.status == 1 or tempSS.status == 3:
			ssObject.append(tempSS)
			post_data.update({'output' : fileoutput.createHTML(startTime, ssObject, seq)}) #create HTML and store it in post_data

		post_data['completed'] += 1
		if post_data['completed'] == post_data['total_sites']:
			print("All predictions completed.")
			if post_data['email'] != "": #if all completed and user email is not empty, send email
				print ("Sending results to " + post_data['email'])
				emailtools.sendEmail(email_service, post_data['email'],"Prediction Results", post_data['output'])
	
@socketio.on('connected')
def connected():
	print()
	#print(request.sid)
	#clients.append(request.namespace)
	
@socketio.on('beginProcess') #send once socket is connected
def processInput(post):
	if post:
		post_data = json.loads(post) #convert from string to dict
		#print(post_data)
		
		sess = request.sid
		seq = ''.join(post_data['seqtext'].split()) #removes all whitespaces
		post_data['seqtext'] = seq
		socketio.emit('seqString', json.dumps({'seq':seq, 'email': post_data['email']}), room=sess) #send seq and email to update their elements in sent.html

		startTime = emailtools.randBase62()
		socketio.emit('resulturl', startTime, room=sess)
		
		if post_data['email'] != "": #send email to let users know input was received
			emailtools.sendEmail(email_service, post_data['email'],"Prediction Input Received", "<div>Input received for the following sequence:</div><div>" + seq + "</div><div>Results will be displayed at the following link as soon as they are available:</div><div>" + siteurl + "/output/" + startTime +"</div>")
			
			#Non HTML version
			#emailtools.sendEmail(email_service, post_data['email'],"Prediction Input Received", "Input received for the following sequence:\n" + seq + "\n\nResults will be displayed at the following link as soon as they are available:\n" + siteurl + "/output/" + startTime +"/" + startTime + ".html")
			
		#Stores currently completed predictions
		ssObject = []
		#Prepare files for saving results
		fileoutput.createFolder(startTime)
		
		sendData(sess, seq, startTime, ssObject, post_data)

#Sends sequence based off whatever was selected before submission
def sendData(sess, seq, startTime, ssObject, post_data):
	for key in post_data.keys():
		if key in siteDict:
			socketio.start_background_task(run, siteDict[key],sess, seq, email, key, ssObject, startTime, post_data, email_service)
			print("Sending sequence to " + key)

#Takes a form from post and checks if seq is empty or not. Backup measure in case elements are editted
def validate_seq(seq):
	if seq == "":
		return False
	return True

#Takes a form from post and returns the number of sites it. Backup measure in case elements are editted, and for checking if all predictions are finished
def validate_sites(form):
	count = 0
	for key in siteDict.keys():
		if key in form:
			count += 1
	return count	

if __name__ == "__main__":
	#socketio.run(app, debug=True) #Run on localhost 127.0.0.1:5000
	socketio.run(app,host='0.0.0.0', debug=True) #Run online on public IP:5000