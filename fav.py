#!/usr/local/bin/python2.7                                                                       

import sys
import MySQLdb
import dbconn2

#------------------------------------------------------                                          

def addFav(conn, bnum, jobID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("INSERT into favorites VALUES(%s, %s)", [bnum, jobID])

def deleteFav(conn, bnum, jobID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("DELETE  * FROM favorites WHERE bnum=%s and jobID=%s", [bnum, jobID])

def allFav(conn, bnum):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("GET * from favorits WHERE bnum=%s", [bnum])
    return curs.fetchall()
