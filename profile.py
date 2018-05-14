#!/usr/local/bin/python2.7
# Fistbump!

import sys
import MySQLdb
import dbconn2

#-------------------------------------------------------------------------------
# add a profile pic
def addProfPic(conn, bnum, fileName):
    try:
        curs = conn.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('insert into prof_pic(bnum, pic) \
                      values (%s, load_file(%s))', [bnum, fileName])
        return True
    except:
        False

#get blob from database
def get_blob(cursor,bnum):
    cursor.execute('SELECT pic FROM prof_pic WHERE bnum=%s',(bnum))
    row = cursor.fetchone()
    data = row[0]
    return data
