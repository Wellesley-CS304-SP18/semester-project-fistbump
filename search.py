#!/usr/local/bin/python2.7
# Fistbump!

import sys
import MySQLdb
import dbconn2

# ------------------------------------------------------------------------------

# return all jobs
def allJobs(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from job_opp')
    info = curs.fetchall()
    return info

# return all jobs given search terms
# if didn't pick filter input defaulted % in routing
def searchJobs(conn, classPref, jobTitle, jobType, season):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    # strings for what sql query to execute (since all enums could need regexp)
    classPrefExec = "jobID in (select jobID from job_opp where classPref "+classPref+")"
    jobTitleExec = "jobID in (select jobID from job_opp where jobTitle "+jobTitle+")"
    jobTypeExec = "jobID in (select jobID from job_opp where jobType "+jobType+")"
    seasonExec = "jobID in (select jobID from job_opp where season "+season+")"
    filters = " and ".join([classPrefExec, jobTitleExec, jobTypeExec, seasonExec])
    print('select * from job_opp where '+filters)
    # don't need to worry about sql injections (values coming from our own form)
    curs.execute('select * from job_opp where '+filters)
    info = curs.fetchall()
    return info

# return job, locations, reviews for jobID
def findJob(conn, jobID, bnum):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('start transaction')
    curs.execute('select * from job_opp where jobID=%s', [jobID])
    job = curs.fetchone()
    curs.execute('select * from job_location where jobID=%s', [jobID])
    locations = curs.fetchall()
    curs.execute('select firstname, jobID, jobYear, reviewer, review from job_review, user_id where jobID=%s and bnum=reviewer', [jobID])
    reviews = curs.fetchall()
    curs.execute('select * from job_review where jobID=%s and reviewer=%s', [jobID, bnum])
    ownRev = curs.fetchone()
    if ownRev is None:
        hasRev = False
    else:
        hasRev = True
    curs.execute('commit')
    return (job, locations, reviews, hasRev)

# future implementation w. human resources:
# return all human resources given
def searchHRs(conn, companyName):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from human_resources where companyName=%s',
        [companyName])
    info = curs.fetchall()
    return info
