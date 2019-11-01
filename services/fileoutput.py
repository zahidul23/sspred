import time
import os
import webbrowser

#Creates folder in running directory using "pred month.day.year hr.min.sec" as the name (based off startTime)
def createFolder(startTime):
	nameFormat = startTime
	try:
		os.mkdir(os.getcwd() + "/output/" + nameFormat);
	except OSError:
		print ("Folder " + nameFormat + " failed to be created.")
	else:
		print("Created folder " + nameFormat + " at " + os.getcwd() + "\output\ to save output to.")

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

#Saves the output to an HTML file. 
#Takes a startTime for naming and ssObject,seq, and optional majority vote for the outputs
#"pred month.day.year hr.min.sec" for file name
#Splits outputs into lines of length depending on the rowlength parameter + 15
#Returns the outputted HTML as a string so that it can be emailed
def createHTML(startTime, ssobj, seq, majority = None, hColor = "blue", eColor = "green", cColor = "red", rowlength = 60):
	nameFormat = startTime
	filePath = os.getcwd() + "/output/" + nameFormat + "/" + nameFormat + ".html"
	print(filePath)
	if os.path.exists(filePath):
		os.remove(filePath)
	file = open(filePath, "w+")

	output = "<!DOCTYPE html><head><meta http-equiv='refresh' content='30'></head><html><body style='font-family:Consolas;'>" #use consolas as font to have equal spacing between all characters
	
	counter = drawCounter(seq)
	
	for count in range(0, int(len(seq)/rowlength) + 1):
		output += "<div>" + (15*'&nbsp;') + (counter[rowlength * count : rowlength * (count + 1)]).replace(" ", '&nbsp;') + "</div>"
		output += "<div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sequence:&nbsp;" + seq[rowlength * count : rowlength * (count + 1)] + "</div>"
		for obj in ssobj:
			output+='<div>' + obj.plabel.replace(" ","&nbsp;") + "&nbsp;" #prediction source
			preds = obj.pred #prediction results to be colored
			for c in preds[rowlength * count : rowlength * (count + 1)]:
				output += "<span style='color:" + getColor(c, hColor, eColor, cColor) + "';>" + c + "</span>"
			output += "</div>"
			if obj.status != 3: #Only display conf if status is not 3
				output += "<div>" + obj.clabel.replace(" ","&nbsp;") + "&nbsp;" + obj.conf[rowlength * count : rowlength * (count + 1)] +"</div>"
		if majority:
			output += "<div>Majority Vote: "
			for c in majority[rowlength * count : rowlength * (count + 1)]:
				output += "<span style='color:" + getColor(c, hColor, eColor, cColor) + "';>" + c + "</span>"	
			output += "</div>"
		output += "<br>"
	output += "</body></html>"
	
	file.write(output)
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
	
#Takes a start time and returns a format for file naming
def getNameFormat(startTime):
	return time.strftime("%m.%d.%Y %H.%M.%S",time.localtime(startTime))
	
