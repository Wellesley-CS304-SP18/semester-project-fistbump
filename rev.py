#!/usr/local/bin/python2.7
# Fistbump!

import sys
import MySQLdb
import dbconn2

#-------------------------------------------------------------------------------

# add a job review (individual can only make 1 review for a single jobID)
def addJobRev(conn, uID, jobID, jobYear, review):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('insert into job_review (jobID, jobYear, reviewer, \
            review) values (%s, %s, %s, %s)', [jobID, jobYear, uID, review])
        return 'job review inserted'
    except:
        'job review already made for this job & user'

# update a job review (can update year & review, given uID & jobID)
def updateJobRev(conn, uID, jobID, jobYear, review):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('update job_review set jobYear=%s, review=%s where jobID=%s \
        and reviewer=%s', [jobYear, review, jobID, uID])

# delete a review based on uID & jobID/reviewID (depending what kind of review)
def deleteJobRev(conn, table, uID, rID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    if table == "job":
        curs.execute('delete from job_review where reviewer=%s and jobID=%s',
            [uID, jobID])
    if table == "reu":
        curs.execute('delete from reu_review where reviewID=%s', [reviewID])

# return all reviews (tuple of job & reu) an user has made given their uID
def allRevs(conn, uID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from job_review where reviewer=%s', [uID])
    jobRev = curs.fetchall()
    curs.execute('select * from reu_review where reviewer=%s', [uID])
    reuRev = curs.fetchall()
    return (jobRev, reuRev)
