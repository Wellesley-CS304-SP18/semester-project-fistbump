#fistbump!

from flask import (Flask, render_template, make_response, url_for, request, redirect, flash, session, send_from_directory, jsonify)
from werkzeug import secure_filename
app = Flask(__name__)

import sys, os, random
import dbconn2
import bcrypt
from login import *
import opp
import search

app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

db = 'htran_db'

# --------------------------------------------
# ROUTES

@app.route('/', methods=['GET'])
def landing():
    return redirect(url_for('login'))

# login and register on the same html page
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if 'uID' in session:
        uID = session['uID']
        flash('You\'re already logged in!')
        return redirect(url_for('home'))

    errorMsg = 'email and/or password are incorrect.'
    successMsg = 'Successful login.'
    conn = dbconn2.connect(DSN)

    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':

        if request.form['submit'] == 'login':
            email = request.form['email']
            pwd = request.form['pwd']
            hashed = getPwd(conn, email)

            if hashed is not None:
                if bcrypt.hashpw(pwd.encode('utf-8'), hashed['pwd'].encode('utf-8')) != hashed['pwd']:
                    flash(errorMsg)
                    return render_template('login.html')
                else:
                    session['uID'] = getUID(conn, email)['uID']
                    return redirect(url_for('home'))
            else:
                flash(errorMsg)
                return render_template('login.html')

        if request.form['submit'] == 'register':
            uName = request.form['uName']
            email = request.form['email']
            pwd = request.form['pwd']

            if getUID(conn, email) != None:
                flash('Email already in use.')
                return render_template('login.html')
            else:
                hashedPwd = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
                insertUser(conn, uName, email, hashedPwd);
                flash('User successfully added.')
                return redirect(url_for('login'))

@app.route('/home/', methods=['GET','POST'])
def home():
<<<<<<< HEAD
    conn = dbconn2.connect(DSN)
    jobs = search.allJobs(conn)
    reus = search.allREUs(conn)
    return
=======
    if 'uID' not in session:
        flash('Please login to view site')
        return redirect(url_for('login'))
    else:
        uID = session['uID']

    conn = dbconn2.connect(DSN)

    if request.method == 'GET':
        name = getUName(conn, uID)['uName']
        return render_template('home.html',
                               uName = name)

    if request.method == 'POST':
        if request.form['submit'] == "Log Out":
            session.pop('uID', None)
            return redirect(url_for('login'))

@app.route('/addJob', methods=['POST'])
def addJob():
    conn = dbconn2.connect(DSN)
    if request.method == 'POST':
        if request.form['submit'] == 'submit'
            link = request.form[('link')]
    		classPref = request.form[('classPref')] #radio button
    		jobTitle = request.form[('jobTitle')] #radio button
    		jobType = request.form[('jobType')] #radio button
    		positionName = request.form[('positionName')]
            season = request.form[('season')] #radio button
            deadline = request.form[('deadline')]
            company = request.form[('companyName')] #can only add in one job
            uID = session['uID']
        addJob(conn, uID, companyName, link, classPref, jobType, jobTitle, positionName, season, deadline, city)
    return return redirect(url_for('jobLocation'))

@app.route('/addjobLocation/<jobID>', methods=['POST'])
def addJobLocation():
    conn = dbconn2.connect(DSN)
    if request.method == 'POST':
        if request.form['submit'] == 'submit'
            uID = session['uID']
            locations = request.form[('city')] #returns an array? not sure
            for city in locations:
                addJobLoc(conn, uID, jobID, city)
            newLocation = request.form[('newLocation')]
            if newLocation: #can a user submit with an empty value
                addCity(conn, newLocation)
                addJobLoc(conn, uID ,jobID ,city)

>>>>>>> master

@app.route('/job/<jobID>', methods=['GET', 'POST'])
def job():
    conn = dbconn2.connect(DSN)
    job, reviews, hrs = search.findJob(conn, jobID)
    return

@app.route('/reu/<reuID>', methods=['GET', 'POST'])
def reu():
    conn = dbconn2.connect(DSN)
    reu, reviews = search.findREU(conn, reuID)
    return

# --------------------------------------------

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    DSN = dbconn2.read_cnf()
    DSN['db'] = db
    app.debug = True
    app.run('0.0.0.0',port)
