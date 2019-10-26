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

	counterstr = 14*'&nbsp;'
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

#Saves the output to an HTML file. Takes a startTime for naming and ssObject for the outputs
#"pred month.day.year hr.min.sec" for file name
def createHTML(startTime, ssobj, seq):
	nameFormat = startTime
	filePath = os.getcwd() + "/output/" + nameFormat + "/" + nameFormat + ".html"
	print(filePath)
	if os.path.exists(filePath):
		os.remove(filePath)
	file = open(filePath, "w+")

	output = "<!DOCTYPE html><html><body style='font-family:monospace;'>" #use monospace as font to have equal spacing between all characters

	output += "<div>" + drawCounter(seq).replace(" ","&nbsp;") + "</div>"
	output += "<div>&nbsp;&nbsp;&nbsp;&nbsp;Sequence:&nbsp;" + seq + "</div>"

	for i in ssobj:
		output+='<div>' + i.plabel.replace(" ","&nbsp;") + "&nbsp;" #prediction source
		preds = i.pred #prediction results to be colored
		for c in preds:
			output += "<span style='color:" + getColor(c) + "';>" + c + "</span>"
		output += "</div>"
		if i.conf != "": #only display conf if it is not empty. needed in order for SSPro to not display the conf
			output += "<div>" + i.clabel.replace(" ","&nbsp;") + "&nbsp;" + i.conf + "</div>"
	'''
	output += "<div>Majority Vote:"
	for c in ssList[-1]:
		output += "<span style='color:" + getColor(c) + "';>" + c + "</span>"
	'''
	
	output += "</div></body></html>"
	file.write(output)

#Returns the output as a string
def createText(ssObject, seq): #needs results to be split between lines (jpred splits by 60 chars per line)
	output = ''
	output += drawCounter(seq).replace("&nbsp;", " ") + "\n"
	output += "Sequence:".rjust(14) + seq + "\n"
	
	for i in ssObject:
		if i.status == 1:
			output+=i.plabel.rjust(14) + i.pred+ "\n"
			if i.conf != "":
				output+=i.clabel.rjust(14) + i.conf+ "\n"
	#output += "\nMajority Vote:" + ssList[-1]
	return output

#Takes a character and returns the color it should be represented as
#Helix = blue, Strand = green, Coil = red
def getColor(character):
	if character == 'H':
		return "blue"
	elif character == 'E':
		return "green"
	elif character == 'C':
		return "red"
	
	return "black"
	
#Takes a start time and returns a format for file naming
def getNameFormat(startTime):
	return time.strftime("%m.%d.%Y %H.%M.%S",time.localtime(startTime))
	
