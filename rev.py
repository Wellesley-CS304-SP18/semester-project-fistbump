#!/usr/local/bin/python2.7
# Fistbump!

import sys
import MySQLdb
import dbconn2

#-------------------------------------------------------------------------------

# add a job review (individual can only make 1 review for a single jobID)
def addJobRev(conn, bnum, jobID, jobYear, review):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('insert into job_review (jobID, jobYear, reviewer, \
            review) values (%s, %s, %s, %s)', [jobID, jobYear, bnum, review])
        return True
    except:
        False

# gets job review based on bnum & jobID
def getRev(conn, bnum, jobID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from job_review where reviewer=%s and jobID=%s', [bnum, jobID])
    info = curs.fetchone()
    return info

# update a job review (can update year & review, given bnum & jobID)
def updateJobRev(conn, bnum, jobID, jobYear, review):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('update job_review set jobYear=%s, review=%s where jobID=%s \
        and reviewer=%s', [jobYear, review, jobID, bnum])

# delete a review based on bnum & jobID
def deleteJobRev(conn, bnum, jobID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('delete from job_review where reviewer=%s and jobID=%s', [bnum, jobID])

# return all reviews a user has made given their bnum
def allRevs(conn, bnum):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from job_review where reviewer=%s', [bnum])
    jobRev = curs.fetchall()
    return jobRev
