# What is makeMyCSRF ? 
makeMyCSRF is a tool that can be used to automate auto-submit HTML form creation.

The fact is that to test a CSRF in a pentest context, pentesters have to recreate an HTML Form with correct URL and parameters. In my opinion, this painful task can be automated.

makeMyCSRF take formatted input request (BurpSuite and Tamper Date for the moment) and give a ready to use HTML form to try out a CSRF vulnerability injection.

This generated form is automatically **formatted to be used in a CSRF exploitation context** because it contains the following part :
```
[...]
<input style="display:none" type=submit>
<form>
<script>document.forms[0].submit();</script>
</body></html>
```

This JavaScript part will auto-submit the HTML form at load page.

## How to use it

Create a file (e.g. "in.txt") in the same directory as the python script makeMyCSRF.py and know where your request comes from (BurpSuite or Tamper data). Next, execute the python script and specify your input file  ( "`-i`" option) and the used format ( "`-f`" option) : 
```
python makeMyCSRF.py -i in.txt -f Tamper
python makeMyCSRF.py -i in.txt -f BurpSuite
```

Additionnaly, you can redirect the output in a file directly with "`-o`" option : 
```
python makeMyCSRF.py -i in.txt -f BurpSuite -o index.html
```
## How to get request from TamperData / BurpSuite

Basiccaly, you just have to copy the request content from your favorite tool.

This video will show you how to get data from TamperData and use it with makeMyCSRF :


This video will show you how to get data from BurpSuite and use it with makeMyCSRF :


## Additionnal note
Note that Tamper Data generated request will change following your browser language. For the moment, FR and ENG can be used. Please report any other needs or submit your code to process other language ! :)

Enjoy ! :)
