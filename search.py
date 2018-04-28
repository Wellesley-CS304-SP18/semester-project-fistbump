#!/usr/local/bin/python2.7
# Fistbump!

import sys
import MySQLdb
import dbconn2

db = 'lluo_db'

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
def searchJobs(conn, companyName, classPref, jobTitle, jobType, season,
               deadline, orderBy):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from job_opp where companyName=%s \
                  intersect \
                  select * from job_opp where classPref=%s \
                  intersect \
                  select * from job_opp where jobTitle=%s \
                  intersect \
                  select * from job_opp where jobType=%s \
                  intersect \
                  select * from job_opp where season=%s \
                  intersect \
                  select * from job_opp where deadline<=%s',
                  [companyName, classPref, jobTitle, jobType, season, deadline])
    info = curs.fetchall()
    return info

# return all reus given search terms
def searchREUs(conn, deptID, classPref, deadline, isUROP, orderBy):
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

# return  all human resources given
def searchHRs(conn, companyName, personType):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from human_resources where companyName=%s \
                  intersect \
                  select * from human_resources where personType=%s',
                  [companyName, personType])
    info = curs.fetchall()
    return info

# ==============================================================================

if __name__ == '__main__':
    DSN = dbconn2.read_cnf()
    DSN['db'] = db     # the database we want to connect to
    dbconn2.connect(DSN)
