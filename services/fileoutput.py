import time
import os
import webbrowser

#Creates folder in running directory using "pred month.day.year hr.min.sec" as the name (based off startTime)
def createFolder(startTime):
	nameFormat = getNameFormat(startTime)
	try:
		os.mkdir(os.getcwd() + "/output/" + nameFormat);
	except OSError:
		print ("Folder " + nameFormat + " failed to be created.")
	else:
		print("Created folder " + nameFormat + " at " + os.getcwd() + "\output\ to save output to.")

#Saves the output to an HTML file. Takes a startTime for naming and ssObject for the outputs
#"pred month.day.year hr.min.sec" for file name
def createHTML(startTime, ssobj):
	nameFormat = getNameFormat(startTime)
	filePath = os.getcwd() + "/output/" + nameFormat + "/pred " + nameFormat + ".html"
	if os.path.exists(filePath):
		os.remove(filePath)
	file = open(filePath, "w+")

	output = "<!DOCTYPE html><html><body style='font-family:monospace;'>" #use monospace as font to have equal spacing between all characters

	for i in ssobj:
		output+="<div>" + i.name + " Pred: " #prediction source
		preds = i.pred #prediction results to be colored
		for c in preds:
			output += "<span style='color:" + getColor(c) + "';>" + c + "</span>"
		output += "</div>"
		output += "<div>" + i.name + " Conf: " + i.conf + "</div>"

	'''
	output += "<div>Majority Vote:"
	for c in ssList[-1]:
		output += "<span style='color:" + getColor(c) + "';>" + c + "</span>"
	'''
	
	output += "</div></body></html>"
	file.write(output)


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
	
