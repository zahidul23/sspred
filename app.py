import json
import time
from services import ss, psi, jpred, raptorx, pss, sable, sspro, yaspin, emailtools, fileoutput
from datetime import datetime

from flask import Flask, render_template, request, current_app,send_file
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
	
@app.route('/output/<var>')
def showoutput(var):
	print("showing output")
	print('output/'+var+'/'+var+'.html')
	try:
		return send_file('output/'+var+'/'+var+'.html')
	except Exception as e:
		return "not found"

def run(predService, seq, email, name, sess, ssObject,
 startTime, email_service = None):
	tempSS = predService.get(seq, email, email_service)

	'''
	#test without running any prediction scripts
	tempSS = ss.SS(name)
	tempSS.pred = datetime.now().strftime("%H:%M:%S")
	tempSS.conf = datetime.now().strftime("%H:%M:%S")
	tempSS.status = 1
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
		fileoutput.createHTML(startTime, ssObject, seq)
	
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
	seq = ''.join(input_json['data'].split())
	
	ssObject = []
	
	startTime = emailtools.randBase62()
	fileoutput.createFolder(startTime)
	fileoutput.createHTML(startTime, ssObject, seq)

	socketio.emit('resulturl', startTime,room = currentsession)
	
	print(seq)
	socketio.start_background_task(run, psi, seq, email, "PSI", currentsession, ssObject, startTime)
	socketio.start_background_task(run, jpred, seq, email, "JPred", currentsession, ssObject, startTime)
	socketio.start_background_task(run, raptorx, seq, email, "RaptorX", currentsession, ssObject, startTime)
	socketio.start_background_task(run, pss, seq, email, "PSS", currentsession, ssObject, startTime)
	socketio.start_background_task(run, yaspin, seq, email, "Yaspin", currentsession, ssObject, startTime)
	socketio.start_background_task(run, sable, seq, email, "Sable", currentsession, ssObject, startTime, email_service)
	socketio.start_background_task(run, sspro, seq, email, "SSPro", currentsession, ssObject, startTime, email_service)

if __name__ == "__main__":
	#socketio.run(app, debug=True) #Run on localhost 127.0.0.1:5000
	socketio.run(app,host='0.0.0.0', debug=True) #Run online on public IP:5000
