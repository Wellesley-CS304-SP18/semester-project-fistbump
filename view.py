#!/usr/local/bin/python2.7                                                   

import sys
import MySQLdb
import dbconn2

#------------------------------------------------------                      

def countOpps(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("SELECT count(jobID) FROM job_opp")
    return curs.fetchone()

#grabs first ten job opportunities
def getOpps(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute("SELECT * FROM job_opp LIMIT 10")
    return curs.fetchall()
