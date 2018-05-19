# Fistbump!

import sys
import MySQLdb
import dbconn2

# ------------------------------------------------------------------------------

#inserts the save into the saves table
def saveJob(conn,jobID,bnum):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('insert into saves (jobID,bnum) values (%s,%s)', [jobID,bnum])
    except:
        pass

#deletes the save from the saves table
def deleteSavedJob(conn,jobID,bnum):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('DELETE FROM saves WHERE jobID = %s AND bnum = %s', [jobID,bnum])
    except:
        pass

#return the saved jobIDs for the user
def getSavedJobs (conn,bnum):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select jobID from saves where bnum = %s',[bnum])
    jobs = curs.fetchall()
    return jobs

#get the corresponding information for the proper job
def getJobInfo(conn, jobID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from job_opp where jobID = %s',[jobID])
    return curs.fetchone()

#checks if a job is saved:
def checkSaved(conn,jobID):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from saves where jobID = %s',[jobID])
    return curs.fetchone()
