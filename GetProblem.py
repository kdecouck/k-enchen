#!/usr/bin/python

import cgi
import sys

print("Content-Type: text/html\n") #Required to prevent internal server error

import cgitb
cgitb.enable()#output error to client window 
from job_manager import *
 
def main():
    final_feedback='Summary for job request:\n'#This is all text information that will make the client able to see at last
    form = cgi.FieldStorage()
    manager=job_manager('./table.db')
 
    # set name or use default name if no name was provided
    if form.has_key("username"): 
        username = form.getvalue('username')
        final_feedback+='Server received username: {}.\n'.format(username)
    else:
        username = 'Empty'
        final_feedback+='The Client did not specify a username. The server made it as default: "Empty".\n'
    final_feedback +='Username:{}\n'.format(username)

    userid=manager.register_user(username)#if the username exist in databse, it will return user.id, or it will create a new user.id and return that
    print "ID of the client is {}".format(userid)
    final_feedback += 'ID of the client: {}.\n'.format(userid)

    print "Looking for new problem to solve..."
    parameterid=manager.get_new_parameterid()
    
    if parameterid == None:#If the get_new_parameterid() function return None, there is no problem to be solved. program exists.
        print "There is no problem to be solved."
        print final_feedback
        sys.exit()
    else:
        print "Find one! The ID of the problem is {}".format(parameterid)

    final_feedback += 'ID of the assigned problem is {}.\n'.format(parameterid)

    #The sentence below assign specific problem to a client with specific userid
    parameters=manager.assign_a_job(userid,parameterid)#This will print a dict of parameters
    print "The parameters for this problem are?{}?{}?{}?{}?{}".format(parameters[0],parameters[1],parameters[2],parameters[3],parameters[4])
    print "Waiting for result from client..."
    print final_feedback 
    
    
main()
# form = cgi.FieldStorage()
# results = dict(user='xinsheng')
# print results

#val1 = form.getvalue('first')
#val2 = form.getvalue('last')
#
#results = dict(p1=val1,p2=val2) 
#print results 
