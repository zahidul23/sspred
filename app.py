import json
import time
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

#Dictionary containing sent data
post_data = {}

@app.route('/', methods = ['GET', 'POST'])
def hello(name=None):
	if request.method == 'POST':
		global post_data
		post_data = dict(request.form)
		#print(post_data)
		
		if validate_sites(post_data) and validate_seq(post_data['seqtext']):				
			return render_template('sent.html')#output page. keeps the same url

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
 startTime, email_service = None):
	tempSS = predService.get(seq, email, email_service)
	
	socketio.emit('result', json.dumps({
		'pred': tempSS.pred,
		'conf': tempSS.conf,
		'pID': tempSS.name + 'pred',
		'cID': tempSS.name + 'conf',
		'status': tempSS.status}
		), room=sess)
	
	if tempSS.status == 1:
		ssObject.append(tempSS)
		fileoutput.createHTML(startTime, ssObject, seq)
	
@socketio.on('connected')
def connected():
	print()
	
    #print(request.sid)
    #clients.append(request.namespace)
	
@socketio.on('beginProcess') #send once socket is connected
def processInput():
	if post_data:
		sess = request.sid
		seq = ''.join(post_data['seqtext'].split()) #removes all whitespaces
		socketio.emit('seqString', json.dumps({'seq':seq}), room=sess) #send seq to update the seq row
		
		#user_email = post_data['email'] #currently unused
		
		startTime = emailtools.randBase62()
		socketio.emit('resulturl', startTime, room=sess)
		
		#Stores currently completed predictions
		ssObject = []
		#Prepare files for saving results
		fileoutput.createFolder(startTime)
		fileoutput.createHTML(startTime, ssObject, seq)
		
		sendData(post_data,sess, seq, startTime, ssObject)

#Sends sequence based off whatever was selected before submission
def sendData(input,sess, seq, startTime, ssObject):
	for key in input.keys():
		if key in siteDict:
			socketio.start_background_task(run, siteDict[key],sess, seq, email, key, ssObject, startTime, email_service)
			print("Sending sequence to " + key)

#Takes a form from post and checks if seq is empty or not. Backup measure in case elements are editted
def validate_seq(seq):
	if seq == "":
		return False
	return True
#Takes a form from post and checks if at least one site is in it. Backup measure in case elements are editted
def validate_sites(form):
	for key in siteDict.keys():
		if key in form:
			return True
	return False		

if __name__ == "__main__":
	#socketio.run(app, debug=True) #Run on localhost 127.0.0.1:5000
	socketio.run(app,host='0.0.0.0', debug=True) #Run online on public IP:5000