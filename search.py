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

# return all reus
def allREUs(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from reu_opp')
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

# return job, job reviews, job hr for jobID
def findJob(conn, jobID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('start transaction')
    curs.execute('select * from job_opp where jobID=%s', [jobID])
    job = curs.fetchone()
    curs.execute('select jobYear, review from job_review, user_id where jobID=%s and reviewer=bnum', [jobID])
    reviews = curs.fetchall()
    curs.execute('select companyName from job_opp where jobID=%s', [jobID])
    info = curs.fetchone()
    curs.execute('commit')
    return (job, reviews)

# return all reus given search terms
# if didn't pick filter input % for param
def searchREUs(conn, deptID, classPref, deadline, isUROP):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from reu_opp where deptID=%s \
                  intersect \
                  select * from reu_opp where classPref=%s \
                  intersect \
                  select * from reu_opp where deadline=%s \
                  intersect \
                  select * from reu_opp where isUROP=%s',
                  [deptID, classPref, deadline, isUROP])
    info = curs.fetchall()
    return info

# return reu, reu reviews for reuID
def findREU(conn, reuID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('start transaction')
    curs.execute('select * from reu_opp where reuID=%s', [reuID])
    reu = curs.fetchone()
    depID = reu['deptID']
    curs.execute('select * from reu_review where deptID=%s', [deptID])
    reviews = curs.fetchall()
    curs.execute('commit')
    return (reu, reviews)

# return all human resources given
def searchHRs(conn, companyName):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from human_resources where companyName=%s',
        [companyName])
    info = curs.fetchall()
    return info
