#!/usr/bin/env python
# Fix it!

import cgi
import cgitb; cgitb.enable() # Optional; for debugging only
from Cheetah.Template import Template
from subprocess import call, check_output
import os

arguments = cgi.FieldStorage()

print "Content-type: text/html\n"

if arguments:
	for key in arguments.keys():
		log = call(["mkclean", "--optimize", "--quiet",  arguments[key].value])

t = Template(file="fix.tmpl", searchList={"arguments":arguments, "log":log})
print str(t)