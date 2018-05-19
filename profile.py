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
                      values (%s, load_file(%s)) \
                      on duplicate key update pic=values(pic)', [bnum, fileName])
        return True
    except:
        False

# delete a profile pic
def deleteProfPic(conn, bnum):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('delete from prof_pic where bnum=%s', [bnum])


# checks if profile pic exists
def profExists(conn, bnum):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from prof_pic where bnum=%s', [bnum])
    info = curs.fetchone()
    return info is not None

#does all the checking of the database for a prof and gives the proper src for the html
def getSrc(conn, bnum, src):
    exists = profExists(conn,bnum)
    if exists == True:
        filename = secure_filename(str(bnum)+'.jpeg')
        src=url_for('pic',fname=filename)
    else:
        src=None
