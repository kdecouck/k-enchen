#!/usr/bin/python
import urllib
import urllib2
import sys
import math
from numpy import *

def get_username():
    username = raw_input("Enter the username:")
    return username

def main(username):
#Below we send username to the server and get userid and parameters back from server
    #url='http://localhost:8000/GetProblem.py'
    url='http://173.250.205.144/cgi-bin/GetProblem.py'
    values = {'username':username}  
    data = urllib.urlencode(values)#this function from urllib encode the value passed to server
    req = urllib2.Request(url,data)#a Request object which represents the HTTP request you are making
    try: 
        response = urllib2.urlopen(req)
    #Error handling
    except urllib2.HTTPError as error:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', error.code
    except urllib2.URLError as error:
        print error.reason 
    except:
        print "Unexpected error:",sys.exc_info()[0]
    else:
        #feedback stores all informatin sent back from server
        feedback = response.read().split('\n')#split the whole text into lines and store them in a list
        #Looking for some key words from the server feedback
        flag = 0
        for i in range(len(feedback)):
            if 'There is no problem to be solved.' in feedback[i]:
                flag = 1#After this for loop, if flag ==1, exit this program

            #The parameters are here
            if 'The parameters for this problem are?' in feedback[i]:
                print feedback[i]
                words = feedback[i].split('?')
                continue

            if 'Find one! The ID of the problem is ' in feedback[i]:
                print feedback[i]
                pid_group = feedback[i].split(' ')
                parameterid = int(pid_group[-1])
                continue

            if 'ID of the client is ' in feedback[i]:
                print feedback[i]
                userid_group = feedback[i].split(' ')
                userid = int(userid_group[-1])
                continue
                
            print feedback[i]
        if flag == 1:
            print "All mission completed"
            return False
        #Below are the parameters obtained from the server
        p1 = float(words[1])
        p2 = float(words[2])
        p3 = float(words[3])
        p4 = float(words[4])
        p5 = float(words[5])
        #solve the problem on client machine
        result =solve_problem(p1, p2, p3, p4, p5)
        
        #The solve_problem() functino may return float, NaN, or string type
        if type(result) == str:
            #This will still be sent back to server, marking this problem as unsolvable on server
            result = "Cannot find an answer in specified range."
        elif math.isnan(result): #if result is an NaN
            result = "Cannot find an answer in specified range."
        else:
            print "result in client.py is: {}".format(result)
        response.close()  # best practice to close the file
        
        
    #Now let's submit the answer to the server
    #url2='http://localhost:8000/SubmitAnswer.py'
    url2 = 'http://173.250.205.144/cgi-bin/SubmitAnswer.py'
    result_dict = {'result':result,'userid':userid,'parameterid':parameterid}
    data2 = urllib.urlencode(result_dict)#this function from urllib encode the value passed to server
    req2= urllib2.Request(url2,data2)#a Request object which represents the HTTP request you are making

    try: 
        response2= urllib2.urlopen(req2)
    except urllib2.HTTPError as error:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', error.code
    except urllib2.URLError as error:
        print error.reason 
    except:
        print "Unexpected error:",sys.exc_info()[0]
    else:
        submit_answer_feedback = response2.read()
        print"Answer submission feedback from the server:"
        if 'True' in submit_answer_feedback:
            if 'Unsolvable problem.' in submit_answer_feedback:
                print "Problem marked as unsolvable"
            else:
                print "Answer submitted successfully"
        else:
            print "Something went wrong with the answer submission"
    return True
    
#This function solve the problem with the 5 parameters
def solve_problem(p1,p2,p3,p4,p5):
    '''solve the function with Newton's method
    '''
    def f(x):
        return p1*sin(p2*x)-p3-p4*exp(p5*x)
        #original given function of problem
    def df(x):
        return p1*p2*cos(p2*x)-p4*p5*exp((p5*x))
        #derivative of given function of problem
        
    tolerance=.00000001 #set up tolerance
    x=2*pi #initial guess
    t=1 #initial set up for tolerance
    while t > tolerance:
    #iterate until the difference between results of current step and next step satisfies the tolerance
        x1 = x - f(x)/df(x) #implementation of Newton-Raphson method
        t = abs(x1 - x) #calculated tolerance : difference between results of current step and next step
        x = x1 #change the current step answer to next step answer

    if x<0 or x>=2*pi: #check whether the answer is out of boundaries or not
        result = 'can not find the approx. answer'
        print(result)
        return result 
    #It's possible that we can get the answers out of boundary. 
    #Therefore, we consider the group of parameters leading the wrong answer as 'unsolvable' parameters.   
    else: #If the answer satisfies the boundaries
        print('Find an answer:{}'.format(x))
        return x
        #return the calculated answer
username=get_username()
while main(username):
    
    print "\n"*3
    print "New mission start..."
