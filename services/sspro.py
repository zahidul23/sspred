import os
import requests
import time
import io
import re
from bs4 import BeautifulSoup
from guerrillamail import GuerrillaMailSession

from services import ss, batchtools

def get(seq, rowid):
	
	SS = ss.SS("SSPro")
	SS.status = 0
	
	if (len(seq) > 400):
		SS.pred += "Sequence is longer than 400"
		SS.conf += "Sequence is longer than 400"
		SS.status = 2 #error status
		print("SSPro failed: Sequence longer than 400")
		return SS #return SS so it will be readable as an ssObject
	
	randName = batchtools.randBase62()
	session = GuerrillaMailSession()	#Creates GuerrillaMail session
	email_address = session.get_session_state()['email_address'] #retrieves temp email address
	
	payload = {'amino_acids': seq,
	'query_name': randName, 
	'email': email_address,
	'ss':'on'}
	
	r = requests.post('http://scratch.proteomics.ics.uci.edu/cgi-bin/new_server/sql_predict.cgi', data = payload)
	
	soup = BeautifulSoup(r.text, 'html.parser')
	msg = soup.find('p')
	if msg == None:
		SS.pred += "Failed to Submit"
		SS.conf += "Failed to Submit"
		SS.status = 2 #error status
		print("SSPro Failed to Submit")
		return SS

	if msg.text.split()[0] == 'ERROR:':
		SS.pred += "Queue Full"
		SS.conf += "Queue Full"
		SS.status = 2 #error status
		print("SSPro Queue Full")
		return SS
	
	query = 'from:(baldig@ics.uci.edu) subject:(Protein Structure Predictions for ' + randName + ')'
	stime  = time.time()
	email_id = False
	
	'''
	#Waits indefinitely until results are out
	email_id, message = batchtools.emailRequestWait(session, query, "Name:", randName, "SSPro Not Ready", 60)
	'''
	
	#Cancels after 15 min. Length 400 sequences take 10-15 min in a batch
	email_id, message = batchtools.emailRequestWait(rowid, "sspro", session, query, "Name:", randName, "SSPro Not Ready", 60, 1500)

	if email_id:
		message_parts = message.splitlines()
		
		index = 0 #current line
		finished_scrape = False
		
		while index < len(message_parts) and not finished_scrape:
			index += 1
			if message_parts[index] == "Predicted Secondary Structure (3 Class):":
				while message_parts[index]: #while not blank line
					index += 1
					SS.pred += message_parts[index]
				finished_scrape = True

		SS.conf = "SSPro Does Not Provide Any Conf" 
		SS.status = 3
		print("SSpro Complete")
	else:
		SS.pred += "failed to respond in time"
		SS.conf += "failed to respond in time"
		SS.status = 2 #error status
		print("SSPro failed: No response")
	return SS