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
    classPrefExec = "classPref=%s"
    jobTitleExec = "jobTitle=%s"
    jobTypeExec = "jobType=%s"
    seasonExec = "season=%s"

    # only filters that were selected
    selFilters = []
    filterInputs = []
    if classPref:
        selFilters.append(classPrefExec)
        filterInputs.append(classPref)
    if jobTitle:
        selFilters.append(jobTitleExec)
        filterInputs.append(jobTitle)
    if jobType:
        selFilters.append(jobTypeExec)
        filterInputs.append(jobType)
    if season:
        selFilters.append(seasonExec)
        filterInputs.append(season)

    filters = " and ".join(selFilters)

    # if no filters applied then set as jobID>0 (returns all job opps)
    if filters == "":
        filters = "jobID > 0"
    print 'select * from job_opp where '+filters
    curs.execute('select * from job_opp where '+filters, filterInputs)
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
    curs.execute('commit')
    return (job, locations, reviews)

# future implementation w. human resources:
# return all human resources given
def searchHRs(conn, companyName):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from human_resources where companyName=%s',
        [companyName])
    info = curs.fetchall()
    return info
