#!/usr/bin/python
import numpy
def create_database ():

    import sqlite3 as DBI
    import sys
    db = DBI.connect('table.db')
    with db:
        cursor = db.cursor()

#parameter
        cursor.execute("DROP TABLE IF EXISTS parameter;")    
        cursor.execute("CREATE TABLE parameter(id INT NOT NULL PRIMARY KEY, statusid INT, last_assigned_time INT, p1 FLOAT, p2 FLOAT, p3 FLOAT, p4 FLOAT, p5 FLOAT);")

#problemstatus
        cursor.execute("DROP TABLE IF EXISTS problemstatus;")    
        cursor.execute("CREATE TABLE problemstatus(id INT NOT NULL PRIMARY KEY, status TINYTEXT);")
        cursor.execute("INSERT INTO problemstatus VALUES(0,'unsolved');")
        cursor.execute("INSERT INTO problemstatus VALUES(1,'solved');")
        cursor.execute("INSERT INTO problemstatus VALUES(2,'unsolvable');")

#user
        cursor.execute("DROP TABLE IF EXISTS user;")
        cursor.execute("CREATE TABLE user(id INT NOT NULL PRIMARY KEY, name TINYTEXT);")

#result
        cursor.execute("DROP TABLE IF EXISTS result;")    
        cursor.execute("CREATE TABLE result(id INT NOT NULL PRIMARY KEY, answer FLOAT);")

#contributor
        cursor.execute("DROP TABLE IF EXISTS contributor;")
        cursor.execute("CREATE TABLE contributor(userid INT, resultid INT);")
        
#joblist
        cursor.execute("DROP TABLE IF EXISTS joblist;")    
        cursor.execute("CREATE TABLE joblist(id INT NOT NULL PRIMARY KEY, parameterid INT, userid INT);") 

    db.commit()
    db.close()
    
#You should specify how many new groups of parameters you want to create
def update_paramters(number_of_groups):
    import sqlite3 as DBI2
    db = DBI2.connect('./table.db')
    cursor = db.cursor()
    cursor.execute('SELECT parameter.id FROM parameter')
    get=cursor.fetchall()
    db.commit()
    number_of_existed_groups = len(get)
    for i in range(int(number_of_groups)):
        mu, sigma = 5, 1
        p1 = float(numpy.random.normal(mu,sigma,1))
        mu, sigma = 2, 0.25
        p2 = float(numpy.random.normal(mu,sigma,1))
        mu, sigma = -2, 0.75
        p3 = float(numpy.random.normal(mu,sigma,1))
        mu, sigma = 0.5, 0.1
        p4 = float(numpy.random.normal(mu,sigma,1))
        mu, sigma = 1.234, 0.321
        p5 = float(numpy.random.normal(mu,sigma,1))
        cursor.execute("INSERT INTO parameter VALUES({},0,0,{},{},{},{},{});".format(number_of_existed_groups+i,p1,p2,p3,p4,p5))
    db.commit()
    
###############################################################################
create_database()
update_paramters(5)
