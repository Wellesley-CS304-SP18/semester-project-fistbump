#!/usr/local/bin/python2.7
# Fistbump!

import sys
import MySQLdb
import dbconn2

# ------------------------------------------------------------------------------

# check if user can update table (same poster or admin)
def canUpdate(conn, table, ID, bnum):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    if table == "job":
        curs.execute('select poster from job_opp where jobID= %s', [ID])
    if table == "reu":
        curs.execute('select poster from reu_opp where reuID=%s', [ID])
    if table == "hr":
        curs.execute('select poster from human_resources where uID=%s', [ID])
    info = curs.fetchone()
    if info is not None:
        samePoster = (info['poster'] == bnum)
        isAd = isAdmin(conn, bnum)
        return (samePoster or isAd)
    return True

# check if user is admin
def isAdmin(conn, bnum):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('start transaction')
    curs.execute('select uType from user_id where bnum=%s', [bnum])
    info = curs.fetchone()
    curs.execute('commit')
    return info['uType'] == "admin"

# add city
def addCity(conn, city):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('insert into city (city) values (%s)', [city])
        return city+" added to city."
    except:
        return city+" already in city."

# return all cities in city
def allCities(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from city')
    info = curs.fetchall()
    return info

# update job opp
def updateJob(conn, jobID, bnum, companyName, link, classPref, jobType, jobTitle,
              positionName, season, deadline):
    if canUpdate(conn, "job", jobID, bnum):
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('start transaction')
        addCompany(conn, companyName)
        curs.execute('update job_opp set poster=%s, link=%s, classPref=%s, \
                     jobType=%s, jobTitle=%s, positonName=%s, season=%s, \
                     deadline=%s, companyName=%s where jobID=%s',
                     [bnum, link, classPref, jobType, jobTitle, positonName,
                     season, deadline, companyName, jobID])
        curs.execute('commit')
        return True
    return False

# add job location
def addJobLoc(conn, bnum, jobID, city):
    if canUpdate(conn, "job", jobID, bnum):
        try:
            curs = conn.cursor(MySQLdb.cursors.DictCursor)
            curs.execute('start transaction')
            addCity(conn, city)
            curs.execute('insert into job_location (jobID, city) values \
                         (%s, %s)', [jobID, city])
            curs.execute('commit')
            return True
        except:
            return False
    return False

# delete job location
def deleteJobLoc(conn, bnum, jobID, city):
    if canUpdate(conn, "job", jobID, bnum):
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('delete from job_location where jobID=%s and city=%s',
                     [jobID, city])
        return True
    return False

# return all company names
def allCompany(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from company')
    info = curs.fetchall()
    return info

# add company
def addCompany(conn, companyName):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('insert into company (companyName) values (%s)',
                     [companyName])
        return True
    except:
        return True

# add job opp
def addJob(conn, bnum, companyName, link, classPref, jobType, jobTitle, positionName, season, deadline):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('start transaction')
    addCompany(conn, companyName)
    curs.execute('insert into job_opp (poster, companyName, link, classPref, \
                 jobType, jobTitle, positionName, season, deadline) values \
                 (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                 [bnum, companyName, link, classPref, jobType, jobTitle,
                 positionName, season, deadline])
    curs.execute('select last_insert_id()')
    info = curs.fetchone()
    jobID = info['last_insert_id()']
    curs.execute('commit')
    return jobID

# delete job opp
def deleteJob(conn, bnum, jobID):
    if canUpdate(conn, "job", jobID, bnum):
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('delete from job_opp where jobID=%s', [jobID])
        return True
    return False
 
# add user
def addUser(conn, bnum, firstname, username):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('insert into user_id(bnum, firstname, username, numLogins, uType) \
                      values(%s, %s, %s, %s, %s) \
                      on duplicate key update numLogins = numLogins + 1', [bnum, firstname, username, 1, 'general'])
        return True
    except:
        return False
