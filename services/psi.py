import requests
import time
from guerrillamail import GuerrillaMailSession

from services import ss, batchtools


def get(seq, rowid):
	
	SS = ss.SS("PSI")

	if (len(seq) < 30 or len(seq) > 1500): #<30 shouldnt happen with input validation
		SS.pred += "Sequence is longer than 1500"
		SS.conf += "Sequence is longer than 1500"
		SS.status = 2 #error status
		print("PsiPred failed: Sequence is longer than 1500")
		'''
		SS.pred += "Sequence is shorter than 30 or longer than 1500"
		SS.conf += "Sequence is shorter than 30 or longer than 1500"
		SS.status = 2 #error status
		print("PsiPred failed: Sequence is shorter than 30 or longer than 1500")
		'''
		return SS 
		
	session = GuerrillaMailSession()	#Creates GuerrillaMail session
	email_address = session.get_session_state()['email_address'] #retrieves temp email address
	
	url = 'http://bioinf.cs.ucl.ac.uk/psipred/api/submission/'
	payload = {'input_data': seq}
	data = {'job': 'psipred',
        	'submission_name': 'testing',
        	'email': email_address, }
	r = requests.post(url, data=data, files=payload, headers={'accept': 'application/json'})

	uuid = r.json()['UUID']
	

	jsonurl = 'http://bioinf.cs.ucl.ac.uk/psipred/api/submission/' + uuid + '?format=json'


	r = requests.get(jsonurl)

	filesUUID = r.json()['submissions'][0]['UUID'] 

	horiz = 'http://bioinf.cs.ucl.ac.uk/psipred/api/submissions/' + filesUUID + '.horiz'
	
	#Length 1500 takes around 5 min
	requesturl = batchtools.requestWait(rowid, "psi", horiz, 'PsiPred Not Ready')
	
	if requesturl:
		raw = requesturl.text.splitlines()
		for i in range(len(raw)):
			raw[i] = raw[i].strip()
			if raw[i].startswith("Conf"):
				SS.conf += raw[i][6:]
			if raw[i].startswith("Pred"):
				SS.pred += raw[i][6:]
				
		SS.status = 1
		print("PsiPred Complete")
	else:
		SS.pred += "failed to respond in time"
		SS.conf += "failed to respond in time"
		SS.status = 2 #error status
		print("PsiPred failed: No response")

	print("PSI::")
	print(SS.pred)
	print(SS.conf)
	
	return SS
	