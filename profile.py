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
        curs.execute('insert into prof_pic (bnum, pic) \
                      values (%s, load_file(%s))', [bnum, fileName])
        return True
    except:
        False

# checks if profile pic exists
def profExists(conn, bnum):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from prof_pic where bnum=%s', [bnum])
    info = curs.fetchone()
    if info is None:
        return False
    return True
