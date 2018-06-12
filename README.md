k-enchen
========
A Python-based distributed computing application (server+client), to run simulation studies. 
Originally made as part of #cee505

Simulation studies require many simulation instances of similar problems, differing through a series of parameters.  These parameters are typically given as fixed set of parameters (not applicable here) or as random variables with mean value and standard variation.  Given multiple available computers, this client-server tool helps to parallelize and thus speed up the computations. The system does not assign the same problem twice, and the analysis stops when complete.

Part 1: Server Application (Runs on a web server)
========
Setup stage1: generate a database holding values for various parameters
Setup stage2: generate a combination table that defines loadcases and parameter IDs for parameters used in the analysis.
Generate a request function that responds to a HTTP-request: http://server_name/GetProblem.py?UID=uid?JOB=new by returning “{‘jobID’:jid, ‘param1’:val1, ‘param2’:val2, … }” through the web interface (visible in browser)
Keep track of which user works on what combination (through the database). Generate a new user if uid is not yet known.  Also keep track when a job was assigned and have the problem expire/reset if no solution is submitted within a given time (1 minute). Generate a request function that responds to a HTTP request: http://server_name/SubmitAnswer.py?UID=uid?JOB=jid?result=val that 
- Checks for valid uid and active jid
- Registers the result and stores it within the combinations table (SQL UPDATE statement)
- Marks the problem as completed
- Returns ‘TRUE’ if action was successful and ‘FALSE’ if a problem was encounters. Add proper description of the problem in a separate line of output (will be displayed over the HTTP connection.
- Generate a request function that responds to a HTTP request (3-people team only): http://server_name/CheckResult.py that shows:
- a distribution graph for the submitted values (density function)
- presents mean, std dev, and COV for the computed results. 
- Lists all contributing users and how many computations they submitted.

Part 2: Client Application (runs on multiple computers)
========
Obtain a new set of input parameters by submitting the following request via a HTTP connection (check out the url feature in python): http://server_name/GetProblem.py?UID=uid?JOB=new where uid is your personal ID.  I suggest using your student ID or your nickname.  ‘new’ is a keyword.  The server will return a single line in the form “{‘jobID’:jid, ‘param1’:val1, ‘param2’:val2, … }” through the web interface (visible in a browser if you type the request).  Note that this string represents a dictionary and can be converted easily.
Use these parameters to solve a problem: iteratively solve and return X through a HTTP request: http://server_name/SubmitAnswer.py?UID=uid?JOB=jid?result=X The server will return ‘TRUE’ if action was successful and
‘FALSE’ if a problem was encounters. Add proper description of the problem in a separate line of output (will be displayed over the HTTP connection. 

Example data
========
PARAMETER, MEAN, STD DEV
param1 5 1
param2 2 .25
param3 -2 .75
param4 .5 .1
param5 1.234 .321
 
Database design
========
The database consists of six tables. A unique id is added for ‘joblist’, ‘parameter’, ‘user’, ‘problemstatus’, and ‘result’. The id serves as the primary key for each table and connects the tables across the database (as shown in the diagram above).

The FLOAT type was applied to columns containing parameter values and submitted answers. Both of these can be decimal numbers. INT type was used for other columns containing system ids.
We chose TINYTEXT instead of other text options to save memory space. The ‘user’ (user defined through input) and ‘problemstatus’ (unsolved, solved, unsolvable) are both expected to be shorter than 255 characters.

The table ‘joblist’ is comprised of three columns. It has its own unique id, parameter id, and user id. From this table we can see which job was calculated with which set of parameters by which user.

The table ‘user’ consists of two columns: id and name. When a user submits his/her name for the first time, he/she will be assigned a new unique id. If the server called again, the program will find the name in the database and use the existing user id. 

From the table ‘contributor’, we can check which user submitted which results. By counting these records we can also deduce how many problems each user solved.

The ‘parameter’ table is consists of 8 columns. It has its own unique id. Status id indicates the current status of that problem (unsolved, solved, unsolvable), coded as 0 - 2. Last_assigned_time represents a time stamp of when the problem was last assigned to a client. Through the last_assigned_time column, we can check how long the client has been working on a problem and reassign the problem if that time surpasses a limit. The reason we specify last_assigned_time as an integer is because we call the time.time() package in python to get the current time, which returns a floating number based on UNIX time with millisecond unit. (More information on UNIX time: en.wikipedia.org/wiki/Unix_time.)
The other columns hold the  parameter values for parameters 1 through 5.
 
The table ‘problemstatus’ consists of two columns (id and status). The three possible values of status are {‘0’=’unsolved’, ‘1’=’solved’, ‘2’=’unsolvable’}. The ‘unsolved’ status means the group of parameters has not yet been assigned. ‘Solved’ means the group of parameters has already been assigned, calculated and the result submitted by a certain client. ‘Unsolvable’ means that the answer that results from that set of parameters is out of boundaries described by the equation. 

Finall, the table ‘result’ is composed of two columns: id and answer. Both are submitted after the calculation is over, when the client submits a new result to the server. The ‘id’ of the result table corresponds to the ‘id’ of the parameter table.

Algorithm
========
create_database.py
‘create_database.py’ generates the database file. It constructs all the tables needed, generates a predefined amount of sets of random parameter values and stores them. The number of sets generated is specified at the end of create_database.py

To work, create_database needs to import SQLite3 and numpy. The SQLite3 package is needed to build tables and insert parameter data. Numpy is required to generate random parameter values. Each table is generated by three basic SQLite3 code:
• DROP - delete the table if it already exists
• CREATE - make a table with specified columns and types.
• INSERT - input values into the table where you want to save the data 
There are two functions defined in this python file.  
The first function is  create_database().  This master function will create all the tables we need and insert some default values.
The second function is update_parameters ().  In this function generates several sets of new parameters and inserts this data into the parameter table in the database. 

client.py
This file should be executed on each client machine that participates in the computation. It will repeatedly call the main() function to solve each given problem until the server tells it there are no problems left to solve.

main() function
There is a main() function in this file, which coordinates all of the client’s actions. It sends a username to the server, gets a set of parameters back from server, solves the problem, sends the result to the server and receives a response to indicate whether it was correctly received.
The interaction between client and server is done with features from the urlib and urlib2 package.  Using a try statement, we can handle different types of error when trying to connect to the server. After sending a username to the server, we received a bunch of information in string type back from server. In this long string, we look for a specific keyword to get parameterid, userid and our five assigned parameters. Those are then stored in local variables. After that we call the solve_problem() function to compute the result. The type of result returned by solve_problem() function can vary. If it cannot solve the problem, it returns a NaN or string type. If it solved the problem, it returns a float number. This information will be passed to the server and the server will handle it accordingly.  The server may change the status of the problem from ‘unsolved’ to either ‘unsolvable’ or ‘solved’ in the database.

solve_problem() function
The function ‘solve_problem’ finds the solution from the five given parameters. It does this by implementing the Newton-Raphson method. However, it is possible to get answers out of the problem’s boundaries (0≤x<2π). If we get an out of boundary solution,  we consider the problem as ‘unsolvable’ and return this info as a string to the server. 
job_manager.py

This file contains a class called job_manager. It acts as a library of methods used to interact with the database. A list of methods defined in this class are listed below.

__init__(database_path)
This is the constructor for this class. It define a sqlite3 object connecting our database and a corresponding database cursor object.

assign_a_job(userid,parameterid)
This function takes userID and parameterID of a set as input, returns the 5 parameters for that problem, records this in the ‘joblist’ table and updates the ‘last_assigned_time’ column with the current time. After the execution of this function, the time that this problem was assigned is recorded in the ‘parameter’ table. 

add_to_joblist(userid,parameterid)
This functions takes userID and parameterID of a set as input, and inserts it as a new row in the ‘joblist’ table. In this way, we have a record for every job assigned in history.

get_new_jobid()
This function returns a new job id, which is used in the add_to_joblist() function.

change_problem_time(parameterid,assigned_time)
This function updates the ‘last_assigned_time’ column in the ‘parameter’ table with the current time. It is used whenever a new job is assigned using that set of parameters.

change_problem_status(parameterid,statusid)
This function takes the ID of a set of parameters and the problem status ID. The status of the set of parameters is changed in correspondence to the status ID. The status can be changed from ‘0’ (unsolved) to ‘1’ (‘solved’) or ‘2’ (‘unsolvable’).  

get_new_parameterid()
This function calculates the time difference between the current system time and the last time those parameters were assigned. Then, the function will create a list of unsolved parameterids where that time difference is larger than 60 seconds. Finally, it will return the first parameter set from this list. If the list is empty it will return ‘None’, which means there are no unassigned problems. 

check_result(parameterid)
This function checks whether the answer is in the result table or not. If the result ID (= parameter set ID) exists in the result table, the function returns ‘True’. If not, the function returns ‘False’. The confirmed presence of the result ID means that the problem was solved using those parameters and the answer was correctly saved in the database.

store_result(result,userid,parameterid)
This function takes result, userid, and parameterid. ‘Result’ represents the answer to the assigned problem.  First, check whether (a) the result table is empty or (b) where the ID of result matches the parameterid. If the result table is empty, INSERT the result data. If the table already exists, UPDATE the result data. Also, input the data into the contributor table by using INSERT or UPDATE depending on the situation.

get_parameters(parameterid)
This function return the five values of parameters corresponding to the parameterID.   

register_user(username)
This function returns the userID corresponding to a specific username. The userID is a unique integer (starting from 0). Whenever a client sends his/her name, this function checks whether the typed user name is already in the table. If the user name already exists in the table, the function returns the userid corresponding to the user name. If a client types nothing or the typed username does not exist in the table, the function assigns a new userID to that user name.

display_user() and display_parameter()
‘display_user’ and ‘display_parameter’ respectively show the contents of the user table and parameter table. Using these two functions, we can check the user and parameter data. It also helps us recognize and fix errors related to user or parameter data.
GetProblem.py
This is a python file on the server, which is typically waiting for job request from a client. At the beginning of this file, we call cgi.FieldStorage() to store the data submitted by the client in a dictionary. We check whether it contains a ‘username’ key, and call register_user() from the job_manager class to register that user if needed. Next, we get an ID of a problem to be solved. If that method return ‘None’ it means there are no problems left to solve. In that case it prints out a message and sends a code to kill the client. If an ID an unsolved problem is still available, the program calls assigne_a_job() from job_manager to assign that problem and get the corresponding 5 parameters. The 5 parameters are put in a special text format: “The parameters for this problem are?{parameter1}?{parameter2}?{parameter3}?{parameter4}?{parameter4}”. This makes it easier to decode for the client’s human user.
SubmitAnswer.py
Another file that resides server side. It responds to a request from the client to submit an answer. Similarly to GetProblem, it stores the client data in a local variable and gets result, problem ID and the userID of that problem’s assigned contributor. If the result contains a string saying “Cannot find a answer in specified range” (unsolvable problem), the server will mark it as unsolvable in the parameter table. If the result is a NaN type (the problem exceeds the range of numpy.float64), the server will also mark it as unsolvable in the parameter table in database. If the result is a floating type (problem solved), the server will update the result and contributor table in database and register who solved it.
CheckResult.py
CheckResult is a completely self contained, independent server script. It is meant to be called from the browser. When called it generates an HTML page containing some basic information on the results received by the server so far. More specifically it generates a histogram, gives a few basic statistical measures and shows the number of contributions for each client.

The script starts by establishing a connection to the database. It reads in every received answers in the ‘result’ table so far, and puts them in a list of tuples. The reason it uses tuples is because of SQL quirk returning some extra characters (brackets, commas). That list of tuples is then changed to an ordinary list containing floating numbers. This list is then fed to matplotlib, which generates the histogram. Thus, the histogram is generated by the server itself and saved locally on the server. The expression ‘mpl.use(‘Agg’)’ is needed to suppress matplotlib from trying to open up a hidden display window (which on the server inevidably fails and breaks the code).

We then start generating the HTML script. The histogram is loaded from the server. Mean, SD and COV are calculated from the same list object as the histogram.

Finally, CheckResult sends a query asking for all the userids in the ‘joblist’ table plus a count of how many times each userid appears. The returned list of tuples is then broken up into two separate lists (one for userids, one for the contribution count) and put into an HTML table. Getting a HTML table with user contributions is a little tricky because the users’ names aren’t stored in the same ‘joblist’ table, only their userids are. Since names are stored in a different table that would already require joining two tables together, which would significantly slow down the script. We decided to settle for userids instead to keep the query faster and simpler.

Test Procedure
========
Initial server setup
During development and initial testing we used an Apache HTTP server (“httpd”, v.2.2.29). This server was run locally from one of our team’s laptops. No information was given about the instructor’s target web server other than that the client request had to happen over HTTP, and no other kind of connection would be allowed. (Note: HTTP has a low level security associated with it and should always be available, no matter the server’s security settings).
System setup involved creating a cgi-bin folder locally where the python files would reside. A detailed tutorial on how to do this is:
http://www.linux.com/community/blogs/129-servers/757148-configuring-apache2-to-run-python-scripts

File permissions
GetProblem.py, SubmitAnswer.py, create_database.py and CheckRresult.py should be put in cgi-bin folder. The script create_database.py should then be executed to generate a table.db database file in that folder. The database will already contain the necessary sets of parameters. Running create_database again will regenerate a new database with new sets of random parameters (Beware: all previously stored userids will be lost).

Care had to be taken to match all server side scripts’ owner and group permissions to mimic the permissions for the cgi-bin folder (chown, chgrp). All files need to be made executable (chmod +x *.py). Also, creating a database on the server generates a read-only database file by default. The database has to be made writeable first before it can be used (chmod a+w table.db).

Getting the right server address
After the server is set up, each client user should modify the url and url2 variable in their client.py file to correspond to the IP address of the server. During our testing this address kept changing since the server was run locally from one of our team’s laptops within the UW wifi network. Each session the laptop was assigned a new ipaddress which forced us to change the client code. A fixed server is definitely recommended.

Starting the code
Users can begin their work simply by running client.py on their machine. The program will keep requesting problems from the server until there are no problems left to be solved on the server’s database.
