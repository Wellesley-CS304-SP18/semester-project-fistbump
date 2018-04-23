#!/usr/local/bin/python2.7
# Fistbump!

import sys
import MySQLdb
import dbconn2

db = 'lluo_db'

# checks if uID can update opp (same poster or admin)
def canUpdate(conn, opp, oppID, uID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    if opp == "job":
        curs.execute('select poster from job_opp where jobID= %s', [oppID])
    if opp == "reu":
        curs.execute('select poster from reu_opp where reuID=%s', [oppID])
    info = curs.fetchone()
    samePoster = (info['poster'] == uID)
    isAdmin = isAdmin(conn, uID)
    return (samePoster or isAdmin)

# checks if user is admin
def isAdmin(conn, uID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select uType from user_id where uID=%s', [uID])
    info = curs.fetchone()
    return info['uType'] == "admin"

# adds new company (returns cID if successful, -1 if not)
def addCompany(conn, companyName):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from company where companyName=%s', [companyName])
    info = curs.fetchone()
    if info is None:
        curs.execute('insert into company (companyName) values %s',
            [companyName])
        curs.execute('select cID from company where companyName=%s',
            [companyName])
        info = curs.fetchone()
        return info['cID']
    return -1

# update job opp
def updateJob(conn, jobID, uID, cID, link, classPref, jobType, jobTitle,
              positionName, season, deadline):
    canUpdate(conn, "job", jobID, uID):
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('update job_opp set poster=%s, cID=%s, link=%s, \
            classPref=%s, jobType=%s, jobTitle=%s, positonName=%s, season=%s, \
            deadline=%s where jobID=%s',
            [uID, cID, link, classPref, jobType, jobTitle, positonName,
            season, deadline, jobID])
        return "Updated job opportunity to: poster="+poster+"; cID="+cID+"; \
            link="+link+"; classPref="+classPref+"; jobType="+jobType+"; \
            postionName="+positionName+"; season="+season+"; deadline="+
            deadline+"."
    return "Cannot update job opportunity. You are not the original job poster \
        or an admin."

# add job opp
def addJob(conn, jobID, uID, cID, link, classPref, jobType, jobTitle,
           positionName, season, deadline):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('insert into job_opp set (poster, cID, link, classPref, \
            jobType, jobTitle, positionName, season, deadline) values \
            (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            [uID, cID, link, classPref, jobType, jobTitle, positonName,
            season, deadline])
        return "Added new job opportunity to: poster="+poster+"; cID="+cID+"; \
            link="+link+"; classPref="+classPref+"; jobType="+jobType+"; \
            postionName="+positionName+"; season="+season+"; deadline="+
            deadline+"."
    return "Cannot update job opportunity. You are not the original job poster \
        or an admin."

# update reu opp
def updateREU(conn, reuID, uID, deptID, link, classPref, deadline, isUROP):
    canUpdate(conn, "reu", reuID, uID):
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('update reu_opp set poster=%s, deptID=%s, link=%s, \
            classPref=%s, deadline=%s, isUROP=%s where reuID=%s',
            [uID, deptID, link, classPref, deadline, isUROP, reuID])
        return "Updated REU opportunity to: poster="+poster+"; deptID="+deptID+
            "; linke="+link+"; classPref="+classPref+"; deadline="+
            deadline+"; isUROP="+isUROP+"."
    return "Cannot update REU opportunity. You are not the original REU poster \
        or an admin."

# returns all jobs
def allJobs(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from job_opp')
    info = curs.fetchall()
    return info

# ==============================================================================

if __name__ == '__main__':
    DSN = dbconn2.read_cnf()
    DSN['db'] = db     # the database we want to connect to
    dbconn2.connect(DSN)
