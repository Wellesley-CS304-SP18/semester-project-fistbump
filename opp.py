#!/usr/local/bin/python2.7
# Fistbump!

import sys
import MySQLdb
import dbconn2

db = 'lluo_db'

# check if uID can update table (same poster or admin)
def canUpdate(conn, table, ID, uID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('start transaction')
    if table == "job":
        curs.execute('select poster from job_opp where jobID= %s', [ID])
    if table == "reu":
        curs.execute('select poster from reu_opp where reuID=%s', [ID])
    if table == "hr"
        curs.execute('select poster from human_resources where uID=%s', [ID])
    info = curs.fetchone()
    samePoster = (info['poster'] == uID)
    isAdmin = isAdmin(conn, uID)
    return (samePoster or isAdmin)

# check if user is admin
def isAdmin(conn, uID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('start transaction')
    curs.execute('select uType from user_id where uID=%s', [uID])
    info = curs.fetchone()
    return info['uType'] == "admin"

# update job opp
def updateJob(conn, jobID, uID, companyName, link, classPref, jobType, jobTitle,
              positionName, season, deadline):
    if canUpdate(conn, "job", jobID, uID):
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('start transaction')
        curs.execute('update job_opp set poster=%s, link=%s, classPref=%s, \
            jobType=%s, jobTitle=%s, positonName=%s, season=%s, \
            deadline=%s, companyName=%s where jobID=%s',
            [uID, link, classPref, jobType, jobTitle, positonName,
            season, deadline, companyName, jobID])
        curs.execute('commit')
        return "Updated job opportunity to: poster="+uID+"; cID="+cID+"; \
            link="+link+"; classPref="+classPref+"; jobType="+jobType+"; \
            postionName="+positionName+"; season="+season+"; deadline="+
            deadline+"; companyName="+companyName"."
    return "Cannot update job opportunity. You are not the original poster or \
        an admin."

# check if city is in city table & add it if it isn't
def checkCity(conn, city):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('insert into city (city) values (%s)', [city])
        return city+" added to city."
    except:
        return city+" already in city."

# add job location
def addJobLoc(conn, uID, jobID, city):
    if canUpdate(conn, "job", jobID, uID):
        try:
            curs = conn.cursor(MySQLdb.cursors.DictCursor)
            curs.execute('insert into job_location (jobID, city) values \
                (%s, %s)', [jobID, city])
                return "city="+city+" added for jobID="+jobID
        except:
            return city+" already listed in location."
    return "Cannot add location. You are not the original poster or an admin."

# delete job location
def deleteJobLoc(conn, uID, jobID, city):
    if canUpdate(conn, "job", jobID, uID):
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('delete from job_location where jobID=%s and city=%s',
                [jobID, city])
        return "Deleted city="+city+" for jobID="+jobID+"."
    return "Cannot delete job location. You are not an admin."

# return all company names
def allComp(conn):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from company')
    info = curs.fetchall()
    return info

# check if company name is in company table & add it if it isn't
def checkCompany(conn, companyName):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('insert into company (companyName) values (%s)',
            [companyName])
        return companyName+" added to company."
    except:
        return companyName+" already in company."

# add job opp
def addJob(conn, uID, companyName, link, classPref, jobType, jobTitle,
           positionName, season, deadline, city):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('start transaction')
    curs.execute('insert into job_opp (poster, companyName, link, classPref, \
        jobType, jobTitle, positionName, season, deadline) values \
        (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
        [uID, companyName, link, classPref, jobType, jobTitle, positonName,
        season, deadline])
    curs.execute('insert into location (jobID, city) values (%s, %s)',
        [jobID, city])
    curs.execute('commit')
    return "Added new job opportunity: poster="+uID+"; companyName="+
        companyName+"; link="+link+"; classPref="+classPref+"; jobType="+
        jobType+"; postionName="+positionName+"; season="+season+"; deadline="+
        deadline+"."

# delete job opp
def deleteJob(conn, uID, jobID):
    if canUpdate(conn, "job", jobID, uID):
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('delete from job_opp where jobID=%s', [jobID])
        return "Deleted jobID="+jobID+"."
    return "Cannot delete jobID. You are not the original poster or an admin."

# update reu opp
def updateREU(conn, reuID, uID, deptID, link, classPref, deadline, isUROP):
    if canUpdate(conn, "reu", reuID, uID):
        try:
            curs = conn.cursor(MySQLdb.cursors.DictCursor)
            curs.execute('update reu_opp set poster=%s, deptID=%s, link=%s, \
                classPref=%s, deadline=%s, isUROP=%s where reuID=%s',
                [uID, deptID, link, classPref, deadline, isUROP, reuID])
            return "Updated REU opportunity to: poster="+uID+"; deptID="+
                deptID+"; link="+link+"; classPref="+classPref+"; deadline="+
                deadline+"; isUROP="+isUROP+"."
        except:
            return "Wasn't able to update REU "+reuID+"."
    return "Cannot update REU opportunity. You are not the original poster or \
        an admin."

# update university (only available if admin)
def updateUni(conn, uID, oldUniversity, newUniversity):
    if isAdmin(conn, uID):
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('update university set university=%s where university=%s',
            [oldUniversity, newUniversity])
        return "Updated university to "+university+"."
    return "Cannot update university. You are not an admin."

# add university
def addUni(conn, university):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('insert into university (university) values (%s)',
            [university])
        return "Added university "+university+"."
    except:
        return university+" already in university."

# delete university (only available if admin)
def deleteUni(conn, uID, university):
    if isAdmin(conn, uID):
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('delete from university where university=%s', [university])
            return "Deleted university "+university+"."
    return "Cannot delete university. You are not an admin."

# update dept (only available if admin)
def updateDept(conn, uID, deptID, deptName, cID, university):
    if isAdmin(conn, uID):
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('update department set deptName=%s, cID=%s, university=%s \
            where deptID=%s',[deptID, cID, uniID, deptID])
        return "Updated dept to: deptID="+deptID+"; cID="+cID+"; university="+
            university+"."
    return "Cannot update department. You are not an admin."

# check if dept is in department table & add it if it isn't; return deptID
def addDepartment(conn, deptName, cID, university):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('start transaction')
    try:
        curs.execute('insert into department (deptName, cID, university) \
            values (%s, %s, %s)', [deptName, cID, university])
        curs.execute('select last_insert_id()')
        info = curs.fetchone()
        curs.execute('commit')
        return info['last_insert_id()']
    except:
        curs.execute('commit')
        return info['deptID']

# delete dept (only available if admin)
def deleteDept(conn, uID, deptID):
    if isAdmin(conn, uID):
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('delete from department where deptID=%s', [deptId])
        return "Deleted deptID="+deptID
    return "Cannot delete department. You are not an admin."

# add reu opp
def addREU(conn, uID, reuTitle, deptID, link, classPref, deadline, isUROP):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('insert into reu_opp (poster, reuTitle, deptID, link, \
        classPref, deadline, isUROP) values (%s, %s, %s, %s, %s, %s)',
        [uID, reuTitle, deptID, link, classPref, deadline, isUROP])
    return "Added new REU opportunity: poster="+uID+"; reuTitle="+
        reuTitle+"; deptID="+deptID+"; link="+link+"; classPref="+classPref+
        "; deadline="+deadline+"; isUROP="+isUROP+"."

# delete job opp
def deleteREU(conn, uID, reuID):
    if canUpdate(conn, "reu", reuID, uID):
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('delete from reu_opp where reuID=%s', [reuID])
        return "Deleted reuID="+reuID+"."
    return "Cannot delete reuID. You are not the original poster or an admin."

# update human resource
def updateHR(conn, uID, hrUID, uName, companyName, email, personType):
    if canUpdate(conn, "hr", hrUID, uID) or uID==hrUID:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('update human_resources set uName=%s, companyName=%s, \
            email=%s, personType=%s, poster=%s, where uID=%s',
            [uName, companyName, email, personType, uID, hrUID])
        return "Updated human resource to: poster="+uID+"; uName="+uName+
            "; companyName="+companyName+"; email="+email+"; personType="+
            personType+"."
    return "Cannot update human resource. You are not the original poster or \
        an admin."

# check if email is user & add person if isn't; return uID
def checkUser(conn, uName, email):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('start transaction')
    curs.execute('select * from user_id where email=%s', [email])
    info = curs.fetchone()
    if info is None:
        curs.execute('insert into user_id (uName, email, uType) \
            values (%s, %s, %s)', [uName, email, 'general'])
        curs.execute('select last_insert_id()')
        info = curs.fetchone()
        curs.execute('commit')
        return info['last_insert_id()']
    curs.execute('commit')
    return info['uID']

# add human resource
def addHR(conn, uID, hrUID, uName, companyName, email, personType):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('insert into human_resources (poster, uID, uName, \
        companyName, personType, email) values (%s, %s, %s, %s, %s, %s)',
        [uID, hrUID, uName, companyName, personType, email])
    return "Added new human resource: poster="+uID+"; uID="+hrUID+"; uName="+
        uName+"; companyName="+companyName+"; personType="+personType+
        "; email="+email+"."

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
            return "Deleted uID="+uID+" from human_resources and user_id."
        else:
            curs.execute('delete from human_resources where uID=%s', [hrID])
            return "Deleted uID="+uID+"."
    return "Cannot delete uID. You are not the original poster or an admin."

# ==============================================================================

if __name__ == '__main__':
    DSN = dbconn2.read_cnf()
    DSN['db'] = db     # the database we want to connect to
    dbconn2.connect(DSN)
