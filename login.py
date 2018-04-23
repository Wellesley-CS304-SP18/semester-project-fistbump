#!/usr/local/bin/python2.7

import sys
import MySQLdb
import dbconn2

#------------------------------------------------------

def getPwd(conn, email):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("SELECT pwd FROM user_id WHERE email=%s", [uName])
    return curs.fetchone()

def emailIsFree(conn, email):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("SELECT uID FROM user_id WHERE email=%s", [uName])
    return curs.fetchone() == None

def insertUser(conn, uName, email, pwd):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("INSERT INTO user_id(uType, uName, email, pwd) VALUES (general, %s, %s, %s)", ([uName], [email], [pwd]))
