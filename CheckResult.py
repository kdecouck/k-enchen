#!/usr/bin/python
import numpy
import sqlite3 as dbi
print("Content-Type: text/html\n")

# connect to the database
db = dbi.connect("table.db") ##our database
cursor = db.cursor()

#Data visualization
##############################################
#1. Get values from database
##############################
cursor.execute("SELECT answer FROM result;")
query = cursor.fetchall()
answers = ([i[0] for i in query]) #turns list-of-tuples(query) into a list


#List -> Histogram -> histogram.png
####################################
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pylab as pylab
pylab.hist(answers, bins=50, normed=1)
pylab.savefig("histogram.png")

#Generate html page with that image imbedded
#############################################
#Required to prevent internal server error
print("<html><head><style>table, th, td {border: 1px solid black;border-collapse: collapse;}th, td {padding: 5px;text-align: left;}table{width: 100%;    background-color: #f1f1c1;}</style></head><body>")

print("<h1>Server feedback:</h1>")
print("<h2>Distribution:</h2>")

data_uri = open('histogram.png', 'rb').read().encode('base64').replace('\n', '')
img_tag = '<img src="data:image/png;base64,{0}" align="center">'.format(data_uri)
print(img_tag)

#Mean, stdev, covariance
##################################
print("<h2>Metrics:</h2>")
print("<table id=\"statistics\"><tr><th>Measure</th><th>Value</th></tr>")
print("<tr><td>Mean</td><td>{}</td><br>".format(sum(answers) / float(len(answers))))
print("<tr><td>Standard Deviation</td><td>{}</td><br>".format(numpy.std(answers)))
print("<tr><td>Covariance</td><td>{}</td><br>".format(numpy.cov(answers)))
print("</tr>")

#Contributing users, how many computations
################################################
#cursor.execute("SELECT name,COUNT(name) AS Frequency FROM user GROUP BY name;")
cursor.execute("SELECT userid,COUNT(userid) AS Frequency FROM joblist GROUP BY userid;")
query = cursor.fetchall()
users = ([i[0] for i in query]) #turns list-of-tuples(query) into a list
frequencies = ([i[1] for i in query]) #turns list-of-tuples(query) into a list

print("<table id=\"usertable\"><tr><th>UserID</th><th>Contribution count</th></tr>")

for x in range(0, len(frequencies)):
	print"<tr><td>",users[x]
	print"</td><td>",frequencies[x]
	print"</td></tr>"

print("</body></html>")
