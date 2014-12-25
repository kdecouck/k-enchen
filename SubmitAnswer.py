#!/usr/bin/python

import cgi
import sys
import math

print("Content-Type: text/html\n") #Required to prevent internal server error

import cgitb
cgitb.enable()#output error to client window 
from job_manager import *
 
def main():
    form = cgi.FieldStorage()
    manager=job_manager('./table.db')
  
    if form.has_key("result") and form.has_key("userid") and form.has_key("parameterid"): 
        result = form.getvalue('result')
        parameterid = form.getvalue('parameterid')
        userid =  form.getvalue('userid')
        
        if "Cannot find an answer in specified range." in result:
            print "True"
            print "Unsolvable problem."
            manager.change_problem_status(parameterid,2)#Mark this problem as unsolvable
        elif math.isnan(float(result)):
            print "True"
            print "Unsolvable problem."
            manager.change_problem_status(parameterid,2)#Mark this problem as unsolvable
        else:
            #Store this result into result table in database
            result = float(result)
            print "result in server:{}".format(result)
            manager.store_result(result, userid, parameterid)
            manager.change_problem_status(parameterid, 1)
            print "True"
    else:
        print "Cannot store the result"
        print "False"
         
     
    
main()
