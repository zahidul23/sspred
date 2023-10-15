import requests
import time
from guerrillamail import GuerrillaMailSession

from services import ss, batchtools

def get(seq, rowid):

	SS = ss.SS("Yaspin")
	SS.status = 0

	if (len(seq) > 4000):
		SS.pred += "Sequence longer than 4000"
		SS.conf += "Sequence longer than 4000"
		SS.status = 2 #error status
		print("YASPIN failed: Sequence longer than 4000")
		return SS #return SS so it will be readable as an ssObject
		
	#session = GuerrillaMailSession()	#Creates GuerrillaMail session
	#email_address = session.get_session_state()['email_address'] #retrieves temp email address

	headers = {
    'authority': 'www.ibi.vu.nl',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryZSqqXydHOqYjTZfS',
    'origin': 'https://www.ibi.vu.nl',
    'referer': 'https://www.ibi.vu.nl/programs/yaspinwww/',
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
}

	data = f'------WebKitFormBoundaryZSqqXydHOqYjTZfS\r\nContent-Disposition: form-data; name="seq"\r\n\r\n{seq}\r\n------WebKitFormBoundaryZSqqXydHOqYjTZfS\r\nContent-Disposition: form-data; name="seq_file"; filename=""\r\nContent-Type: application/octet-stream\r\n\r\n\r\n------WebKitFormBoundaryZSqqXydHOqYjTZfS\r\nContent-Disposition: form-data; name="pssm_file"; filename=""\r\nContent-Type: application/octet-stream\r\n\r\n\r\n------WebKitFormBoundaryZSqqXydHOqYjTZfS\r\nContent-Disposition: form-data; name="mbjob[description]"\r\n\r\nYASPIN Job\r\n------WebKitFormBoundaryZSqqXydHOqYjTZfS\r\nContent-Disposition: form-data; name="smethod"\r\n\r\nnr\r\n------WebKitFormBoundaryZSqqXydHOqYjTZfS\r\nContent-Disposition: form-data; name="nnmethod"\r\n\r\ndssp\r\n------WebKitFormBoundaryZSqqXydHOqYjTZfS\r\nContent-Disposition: form-data; name="email"\r\n\r\n\r\n------WebKitFormBoundaryZSqqXydHOqYjTZfS\r\nContent-Disposition: form-data; name="yaspin_align"\r\n\r\nYASPIN prediction\r\n------WebKitFormBoundaryZSqqXydHOqYjTZfS--\r\n'

	
	# payload = {'seq': seq,
	# 'mbjob[description]': 'testprot',
	# 'nnmethod': 'dssp', 
	# 'smethod': 'nr', 
	# 'yaspin_align': 'YASPIN prediction', 
	# 'email': email_address}
	
	# fasta = {'seq_file': ''}
	r= requests.post('https://www.ibi.vu.nl/programs/yaspinwww/', headers=headers, data = data)
	
	if (r.status_code == 500):
		SS.pred += "Server Down"
		SS.conf += "Server Down"
		SS.status = 2
		print("Yaspin Failed: Server Down")
		return SS
	
	result_url = r.url + 'results.out'
	
	requesturl = batchtools.requestWait(rowid, "yaspin", result_url, 'Yaspin Not Ready', )
	
	if requesturl:
		raw = requesturl.text.splitlines()
		
		for i in range(len(raw)):		
			if raw[i].startswith(" Pred:"):
				SS.pred += raw[i][6:].strip()
			if raw[i].startswith(" Conf:"):
				SS.conf += raw[i][6:].strip()
		
		SS.pred = SS.pred.replace('-','C')

		SS.status = 1
		print("Yaspin Complete")
	else:
		SS.pred += "failed to respond in time"
		SS.conf += "failed to respond in time"
		SS.status = 2 #error status
		print("YASPIN failed: No response")
	return SS