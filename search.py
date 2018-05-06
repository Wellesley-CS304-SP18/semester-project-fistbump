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
def searchJobs(conn, classPref, jobTitle, jobType, season, deadline):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from job_opp where classPref=%s \
                  intersect \
                  select * from job_opp where jobTitle=%s \
                  intersect \
                  select * from job_opp where jobType=%s \
                  intersect \
                  select * from job_opp where season=%s \
                  intersect \
                  select * from job_opp where deadline<=%s',
                  [classPref, jobTitle, jobType, season, deadline])
    info = curs.fetchall()
    return info

# return job, job reviews, job hr for jobID
def findJob(conn, jobID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('start transaction')
    curs.execute('select * from job_opp where jobID=%s', [jobID])
    job = curs.fetchone()
    curs.execute('select * from job_review where jobID=%s', [jobID])
    reviews = curs.fetchall()
    curs.execute('select companyName from job_opp where jobID=%s', [jobID])
    info = curs.fetchone()
    companyName = info['companyName']
    hrs = searchHRs(conn, companyName)
    curs.execute('commit')
    print job
    print reviews
    print hrs
    return (job, reviews, hrs)

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
