import time

#Displays character position 
def drawCounter(mySeq):
	j=0
	p = 1
	#counterstr = 15*'&nbsp;'
	counterstr = ''
	while j < len(mySeq):
		if j%10 != 0:
			counterstr += ' '
			j = j+1
		else:
			for k in range(len(str(p))):
				counterstr += str(str(p)[k])
				j=j+1
			p = p+10
	
	return counterstr

#Writes the output to an HTML format string. 
#Takes a ssObject,seq, and optional pdbdata and majority vote for the outputs
#"pred month.day.year hr.min.sec" for file name
#Splits outputs into lines of length depending on the rowlength parameter + 15
#Returns the outputted HTML as a string so that it can be emailed
def createHTML(ssobj, seq, pdbdata, majority = None, hColor = "blue", eColor = "green", cColor = "red", rowlength = 60):

	output = "<!DOCTYPE html><head><meta http-equiv='refresh' content='30'></head><html><body><table>" 
	
	counter = drawCounter(seq)
	
	for count in range(0, int(len(seq)/rowlength) + 1):
		
		#Counter row
		output += "<tr><td align='right'></td>"
		output += "<td style='font-family:Consolas;'>" + (counter[rowlength * count : rowlength * (count + 1)]).replace(" ", '&nbsp;') + "</td></tr>";
		
		#Sequence row
		output += "<tr><td align='right' style='font-family:Consolas;'>Sequence:</td>"
		output += "<td style='font-family:Consolas;'>" + seq[rowlength * count : rowlength * (count + 1)] + "</td></tr>"
		
		#PDB Row
		if pdbdata is not None:
			output += "<tr><td align='right' style='font-family:Consolas;'>PDB_" + pdbdata['pdbid'] + '_'+ pdbdata['chain'] +":</td>";
			pdbstring = pdbdata['secondary'][rowlength * count : rowlength * (count + 1)]
			pdbstring = pdbstring.replace('C','<span style="color:' + cColor + ';">C</span>');
			pdbstring = pdbstring.replace('H','<span style="color:' + hColor +';">H</span>');
			pdbstring = pdbstring.replace('E','<span style="color:' + eColor +';">E</span>');
			output += "<td style='font-family:Consolas;'>" + pdbstring + "</td></tr>";
		
		#Site Rows
		for obj in ssobj:
			#Pred
			output+="<tr><td align='right' style='font-family:Consolas;'>" + obj.plabel.replace(" ","&nbsp;") + "</td>" #prediction source
				
			output += "<td style='font-family:Consolas;'>"
			preds = obj.pred #prediction results to be colored
			for c in preds[rowlength * count : rowlength * (count + 1)]:
				output += "<span style='color:" + getColor(c, hColor, eColor, cColor) + "';>" + c + "</span>"
			output += "</td></tr>"
			
			#Conf
			if obj.status != 3: #Only display conf if status is not 3
				output += "<tr><td align='right' style='font-family:Consolas;'>" + obj.clabel.replace(" ","&nbsp;") + "</td><td style='font-family:Consolas;'>" + obj.conf[rowlength * count : rowlength * (count + 1)] +"</td></tr>"
				
		#Majority Row
		if majority:
			output += "<tr><td align='right' style='font-family:Consolas;'>Majority Vote:</td><td style='font-family:Consolas;>"
			for c in majority[rowlength * count : rowlength * (count + 1)]:
				output += "<span style='color:" + getColor(c, hColor, eColor, cColor) + "';>" + c + "</span>"	
			output += "</td></tr>"
		output += "<br>"
	output += "</table></body></html>"

	return output

#Takes a character and 3 optional colors. Returns the color it should be represented as
#Default: Helix = blue, Strand = green, Coil = red
def getColor(character, hColor = "blue", eColor = "green", cColor = "red"):
	if character == 'H':
		return hColor
	elif character == 'E':
		return eColor
	elif character == 'C':
		return cColor
	
	return "black"