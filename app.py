import json
import time
from services import ss, psi, jpred, raptorx, pss, sable, sspro, yaspin, emailtools, fileoutput
from datetime import datetime

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
socketio = SocketIO(app)


email_service = emailtools.login()
email = emailtools.getEmailAddress(email_service)

@app.route('/')
def hello(name=None):
	return render_template('index.html')

def run(predService, seq, email, name, sess, email_service = None):
	tempSS = predService.get(seq, email, email_service)

	'''
	#test without running any prediction scripts
	tempSS = ss.SS(name)
	tempSS.pred = datetime.now().strftime("%H:%M:%S")
	tempSS.conf = datetime.now().strftime("%H:%M:%S")
	#''' 
	
	socketio.emit('result', json.dumps({
		'pred': tempSS.pred,
		'conf': tempSS.conf,
		'pID': tempSS.name + 'pred',
		'cID': tempSS.name + 'conf',
		'status': tempSS.status}
		),room=sess)
	
	if tempSS.status == 1:
		ssObject.append(tempSS)
		fileoutput.createHTML(startTime, ssObject)
	
	#'''

@socketio.on('connected')
def connected():
	print()
	
    #print(request.sid)
    #clients.append(request.namespace)


@socketio.on('sendSeq')
def processInput(input_json):
	currentsession = request.sid
	print(currentsession)
	seq = input_json['data'].strip()
	
	
	global ssObject
	ssObject = []
	
	global startTime
	startTime = time.time()
	fileoutput.createFolder(startTime)
	
	print(seq)
	socketio.start_background_task(run, psi, seq, email, "PSI", currentsession)
	socketio.start_background_task(run, jpred, seq, email, "JPred", currentsession)
	socketio.start_background_task(run, raptorx, seq, email, "RaptorX", currentsession)
	socketio.start_background_task(run, pss, seq, email, "PSS", currentsession)
	socketio.start_background_task(run, yaspin, seq, email, "Yaspin", currentsession)
	socketio.start_background_task(run, sable, seq, email, "Sable", currentsession, email_service)
	socketio.start_background_task(run, sspro, seq, email, "SSPro", currentsession, email_service)

if __name__ == "__main__":
	socketio.run(app, debug=True) #Run on localhost 127.0.0.1:5000
	#socketio.run(app,host='0.0.0.0', debug=True) #Run online on public IP:5000