#!/usr/local/bin/python2.7
# Fistbump!

import sys
import MySQLdb
import dbconn2

db = 'mshen4_db'

# check if uID can update table (same poster or admin)
def canUpdate(conn, table, ID, uID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('start transaction')
    if table == "job":
        curs.execute('select poster from job_opp where jobID= %s', [ID])
    if table == "reu":
        curs.execute('select poster from reu_opp where reuID=%s', [ID])
    if table == "hr":
        curs.execute('select poster from human_resources where uID=%s', [ID])
    info = curs.fetchone()
    curs.execute('commit')
    if info is not None:
        samePoster = (info['poster'] == uID)
        isAd = isAdmin(conn, uID)
        return (samePoster or isAd)
    return True

# check if user is admin
def isAdmin(conn, uID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('start transaction')
    curs.execute('select uType from user_id where uID=%s', [uID])
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
def updateJob(conn, jobID, uID, companyName, link, classPref, jobType, jobTitle,
              positionName, season, deadline):
    if canUpdate(conn, "job", jobID, uID):
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('start transaction')
        addCompany(conn, companyName)
        curs.execute('update job_opp set poster=%s, link=%s, classPref=%s, \
            jobType=%s, jobTitle=%s, positonName=%s, season=%s, \
            deadline=%s, companyName=%s where jobID=%s',
            [uID, link, classPref, jobType, jobTitle, positonName,
            season, deadline, companyName, jobID])
        curs.execute('commit')
        #return "Updated job opportunity to: poster="+uID+"; link="+link+"; \
            #classPref="+classPref+"; jobType="+jobType+"; postionName="+
            #positionName+"; season="+season+"; deadline="+
            #deadline+"; companyName="+companyName"."
    #return "Cannot update job opportunity. You are not the original poster or \
        #an admin."

# add job location
def addJobLoc(conn, uID, jobID, city):
    if canUpdate(conn, "job", jobID, uID):
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
def deleteJobLoc(conn, uID, jobID, city):
    if canUpdate(conn, "job", jobID, uID):
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
def addJob(conn, uID, companyName, link, classPref, jobType, jobTitle, positionName, season, deadline):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('start transaction')
    addCompany(conn, companyName)
    curs.execute('insert into job_opp (poster, companyName, link, classPref, \
        jobType, jobTitle, positionName, season, deadline) values \
        (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
        [uID, companyName, link, classPref, jobType, jobTitle, positionName,
        season, deadline])
    curs.execute('select last_insert_id()')
    info = curs.fetchone()
    jobID = info['last_insert_id()']
    curs.execute('commit')
    return jobID

# delete job opp
def deleteJob(conn, uID, jobID):
    if canUpdate(conn, "job", jobID, uID):
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('delete from job_opp where jobID=%s', [jobID])
        return True
    return False

# update reu opp
def updateREU(conn, reuID, uID, deptID, link, classPref, deadline, isUROP):
    if canUpdate(conn, "reu", reuID, uID):
        try:
            curs = conn.cursor(MySQLdb.cursors.DictCursor)
            curs.execute('update reu_opp set poster=%s, deptID=%s, link=%s, \
                classPref=%s, deadline=%s, isUROP=%s where reuID=%s',
                [uID, deptID, link, classPref, deadline, isUROP, reuID])
            return True
        except:
            return False
    return False

# add university
def addUni(conn, university):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('insert into university (university) values (%s)',
            [university])
        return True
    except:
        return False

# delete university (only available if admin)
def deleteUni(conn, uID, university):
    if isAdmin(conn, uID):
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('delete from university where university=%s', [university])
        return True
    return False

# update university (only available if admin)
def updateUni(conn, uID, oldUniversity, newUniversity):
    if isAdmin(conn, uID):
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('start transaction')
        addUni(conn, newUniversity)
        curs.execute('update department university=%s where university=%s',
            [oldUniversity, newUniversity])
        deleteUni(conn, uID, oldUniversity)
        curs.execute('commit')
        return True
    return False

# update dept (only available if admin)
def updateDept(conn, uID, deptID, deptName, city, university):
    if isAdmin(conn, uID):
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('start transaction')
        addCity(conn, city)
        addUni(conn, university)
        curs.execute('update department set deptName=%s, city=%s, \
            university=%s where deptID=%s',[deptName, city, university, deptID])
        curs.execute('commit')
        return True
    return False

# add dept
def addDepartment(conn, deptName, city, university):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('start transaction')
        addCity(conn, city)
        addUni(conn, university)
        curs.execute('insert into department (deptName, city, university) \
            values (%s, %s, %s)', [deptName, city, university])
        curs.execute('commit')
        return True
    except:
        return False

# delete dept (only available if admin)
def deleteDept(conn, uID, deptID):
    if isAdmin(conn, uID):
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('delete from department where deptID=%s', [deptId])
        return True
    return False

# all depts
def allDept(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from department')
    info = curs.fetchall()
    return info

# add reu opp
def addREU(conn, uID, reuTitle, deptID, link, classPref, deadline, isUROP):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('insert into reu_opp (poster, reuTitle, deptID, link, \
        classPref, deadline, isUROP) values (%s, %s, %s, %s, %s, %s)',
        [uID, reuTitle, deptID, link, classPref, deadline, isUROP])
    return True

# delete job opp
def deleteREU(conn, uID, reuID):
    if canUpdate(conn, "reu", reuID, uID):
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('delete from reu_opp where reuID=%s', [reuID])
        return True
    return False

# update human resource
def updateHR(conn, uID, hrUID, uName, companyName, email, personType):
    if canUpdate(conn, "hr", hrUID, uID) or uID==hrUID:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('update human_resources set uName=%s, companyName=%s, \
            email=%s, personType=%s, poster=%s, where uID=%s',
            [uName, companyName, email, personType, uID, hrUID])
        return True
    return False

# add user
def addUser(conn, uName, email):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('start transaction')
        curs.execute('insert into user_id (uName, email, uType) values \
            (%s, %s, %s)', [uName, email, 'general'])
        curs.execute('select last_insert_id()')
        info = curs.fetchone()
        uID = info['last_insert_id()']
        curs.execute('commit')
        return True
    except:
        return False

# add human resource
def addHR(conn, uID, hrUID, uName, companyName, email, personType):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('start transaction')
        addUser(conn, uName, email)
        curs.execute('insert into human_resources (poster, uID, uName, \
            companyName, personType, email) values (%s, %s, %s, %s, %s, %s)',
            [uID, hrUID, uName, companyName, personType, email])
        curs.execute('commit')
        return True
    except:
        return False

# check if uID is an account
def isNotAccount(conn, uID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select pwd from user_id where uID=%s', [uID])
    info = curs.fetchone()
    return (info is None)

# delete job opp
def deleteHR(conn, uID, hrID):
    if canUpdate(conn, "hr", hrID, uID):
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        if isNotAccount(conn, uID):
            curs.execute('delete from user_id where uID=%s', [hrID])
            return True
        else:
            curs.execute('delete from human_resources where uID=%s', [hrID])
            return True
    return False

# ==============================================================================

if __name__ == '__main__':
    DSN = dbconn2.read_cnf()
    DSN['db'] = db     # the database we want to connect to
    dbconn2.connect(DSN)
