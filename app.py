import json
import time
from services import ss, psi, jpred, raptorx, pss, sable, sspro, yaspin, emailtools, fileoutput
from datetime import datetime

from flask import Flask, render_template, request, current_app,send_file
from flask_socketio import SocketIO, emit, send
import secrets

#Order of sites to send  #0-Jpred 1-Psipred 2-Psspred	3-Raptorx 4-Sable 5-Yaspin 6-SSPro
siteDict = {
	"JPred": jpred,
	"PSI": psi,
	"PSS": pss,
	"RaptorX": raptorx,
	"Sable": sable,
	"YASPIN": yaspin,
	"SSPro": sspro
}

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
	print(seq)

	#Get start time and prepare result url
	startTime = emailtools.randBase62()
	socketio.emit('resulturl', startTime,room = currentsession)
	
	#Send sequence to sites
	print(input_json['targets'])
	sendTo(input_json['targets'], currentsession, seq, startTime)

#Sends sequence based off whatever was selected before submission
def sendTo(targets, currentsession, seq, startTime):
	ssObject = []
	fileoutput.createFolder(startTime)
	fileoutput.createHTML(startTime, ssObject, seq)
	
	counter = 0
	for key in siteDict.keys():
		if targets[counter]:
			socketio.start_background_task(run, siteDict[key], seq, email, key, currentsession, ssObject, startTime, email_service)
			print("Sending sequence to " + key)
		counter += 1

if __name__ == "__main__":
	#socketio.run(app, debug=True) #Run on localhost 127.0.0.1:5000
	socketio.run(app,host='0.0.0.0', debug=True) #Run online on public IP:5000
