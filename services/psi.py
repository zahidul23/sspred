import requests
import time

from services import ss


def get(seq, email_address, email_service):
	
	SS = ss.SS("PSI")

	if (len(seq) < 30 or len(seq) > 1500):
		SS.pred += "Sequence is shorter than 30 or longer than 1500"
		SS.conf += "Sequence is shorter than 30 or longer than 1500"
		SS.status = 2 #error status
		print("PsiPred failed: Sequence is shorter than 30 or longer than 1500")
		return SS #return SS so it will be readable as an ssObject
		
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


	page = requests.get(horiz)


	while not requests.get(horiz).ok:
		print('PsiPred Not Ready')
		time.sleep(20)

	raw = requests.get(horiz).text.splitlines()


	for i in range(len(raw)):
		raw[i] = raw[i].strip()
		if raw[i].startswith("Conf"):
			SS.conf += raw[i][6:]
		if raw[i].startswith("Pred"):
			SS.pred += raw[i][6:]
			
	SS.status = 1
	print("PsiPred Complete")

	print("PSI::")
	print(SS.pred)
	print(SS.conf)
	return SS
	