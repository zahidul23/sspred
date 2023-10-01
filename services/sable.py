import os
import requests
import time
import io
import re
import html
from guerrillamail import GuerrillaMailSession

from services import ss, batchtools

def get(seq, rowid):
	
	SS = ss.SS("Sable")
	if len(seq) <= 12: #<=12 shouldnt happen with input validation
		SS.status = 2
		SS.pred += "Sequence is shorter than or equal to 12"
		SS.conf += "Sequence is shorter than or equal to 12"
		print("SABLE failed: Sequence is shorter than or equal to 12")
		
	SS.status = 0
	
	randName = batchtools.randBase62()
	session = GuerrillaMailSession()	#Creates GuerrillaMail session
	email_address = session.get_session_state()['email_address'] #retrieves temp email address

	payload = {'txtSeq': seq, 
	'seqName': randName,
	'email': email_address, 
	'fileName':'', 
	'SS':'SS', 
	'version':'sable2', 
	'SAaction': 'wApproximator',
	'SAvalue':'REAL'}
	
	r = requests.post('http://sable.cchmc.org/cgi-bin/sable_server_July2003.cgi', data = payload)
	
	#sable uses multiple emails to send results
	query = 'from:(sable) subject:(sable result) query: ' + randName

	#Length 4000 takes around 10 min
	message  = ''
	stime  = time.time()
	email_id = False
	
	'''
	#Waits indefinitely until results are out
	email_id, message = batchtools.emailRequestWait(session, query, "Query:", randName, "Sable Not Ready", 30)
	'''
	
	#Cancel in 15 min
	email_id, message = batchtools.emailRequestWait(rowid, "sable", session, query, "Query:", randName, "Sable Not Ready", 30, 900)
	
	if email_id:
		#message = emailtools.decodeEmail(email_service, email_id)
		#print(message)
		message_parts = message.splitlines()

		#getting the prediction sequence and confidence
		index = 0
		while message_parts[index][:11] != 'END_SECTION':
			if message_parts[index].startswith('>'):
				SS.pred += message_parts[index + 2].strip()
				SS.conf += message_parts[index + 3].strip()
				index + 4 #add 4 then 1 later to get to next set of prediction
			index += 1

		#getting the probabilities for helix, beta strand, coil
		index += 1 #go past the prediction's 'END_SECTION'
		helixProb = ''
		betaProb = ''
		coilProb = ''
		while message_parts[index][:11] != 'END_SECTION':
			if message_parts[index].startswith('>'):
				helixProb += message_parts[index + 2][3:].strip() + ' '
				betaProb += message_parts[index + 3][3:].strip() + ' '
				coilProb += message_parts[index + 4][3:].strip() + ' '
			index += 1
			
		SS.hconf = helixProb.split()
		SS.econf = betaProb.split()
		SS.cconf = coilProb.split()
		
		SS.status = 1
		print(SS.pred)
		print(SS.conf)
		print("Sable Complete")
	else:
		SS.pred += "failed to respond in time"
		SS.conf += "failed to respond in time"
		SS.status = 2 #error status
		print("Sable failed: No response")
	return SS