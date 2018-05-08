# Fistbump!

from flask import (Flask, render_template, make_response, url_for, request, redirect, flash, session, send_from_directory, jsonify)
from werkzeug import secure_filename
app = Flask(__name__)

import sys, os, random
import dbconn2
import bcrypt
from login import *
from view import *
import opp
import search

app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

db = 'mshen4_db'

# ------------------------------------------------------------------------------
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

@app.route('/home/', methods=['GET', 'POST'])
def home():
    if 'uID' not in session:
        flash('Please login to view site')
        return redirect(url_for('login'))
    else:
        uID = session['uID']

    conn = dbconn2.connect(DSN)
    name = getUName(conn, uID)['uName']

    if request.method == 'GET':
        return render_template('home.html',
                               uName = name,
                               opportunities = getOpps(conn))

    if request.method == 'POST':
        # log out of account & session
        if request.form['submit'] == "Log Out":
            session.pop('uID', None)
            return redirect(url_for('login'))

        # add a new job opportunity
        if request.form['submit'] == "Add New Job":
            return redirect(url_for('addNewJob'))

        # search for a job or reu with a key word
        if request.form['submit'] == "Search":
            # SEARCH JOB TITLE?
            pass

        # filter through all opportunities
        if request.form['submit'] == "Filter":
            # try & except (do not need to check something for all filters)
            try:
                classPref = "='"+request.form['classPref']+"'"
            except:
                classPref = "regexp 'freshman|sophomore|junior|senior|underclassman|upperclassman|all'"
            try:
                jobType = "='"+request.form['jobType']+"'"
            except:
                jobType = "regexp 'internship|part-time|full-time'"
            try:
                jobTitle = "='"+request.form['jobTitle']+"'"
            except:
                jobTitle = "regexp 'engineering|design|pm|other'"
            try:
                season = "='"+request.form['season']+"'"
            except:
                season = "regexp 'fall|spring|summer|winter|year-round'"

            jobs = search.searchJobs(conn, classPref, jobTitle, jobType,
                                     season)
            return render_template('home.html',
                                   uName = name,
                                   opportunities = jobs)

@app.route('/addNewJob/', methods=['GET','POST'])
def addNewJob():
    conn = dbconn2.connect(DSN)

    if request.method == 'GET':
        return render_template('job_form.html')

    if request.method == 'POST':
        if request.form['submit'] == 'submit':
            link = request.form[('link')]
            classPref = request.form[('classPref')] #radio button
            jobTitle = request.form[('jobTitle')] #radio button
            jobType = request.form[('jobType')] #radio button
            positionName = request.form[('positionName')]
            season = request.form[('season')] #radio button
            deadline = request.form[('deadline')]
            company = request.form[('companyName')] #can only add in one job
            if company == 'none':
                company = request.form[('newCompany')]
            #uID = session['uID']
            uID = 1
        jobID = opp.addJob(conn, uID, company, link, classPref, jobType, jobTitle, positionName, season, deadline)
    return redirect(url_for('addJobLocation', jobID=jobID))

@app.route('/addJobLocation/<jobID>', methods=['GET','POST'])
def addJobLocation(jobID):
    conn = dbconn2.connect(DSN)

    if request.method == 'GET':
        cities = opp.allCities(conn)
        return render_template('jobLocation.html',
                               jobID = jobID,
                               cities = cities)

    if request.method == 'POST':
        if request.form['submit'] == 'submit':
            uID = 1
            #uID = session['uID']
            cities = opp.allCities(conn)
            if bool(cities):
                try:
                    locations = request.form.getlist('city')
                    for city in locations:
                        opp.addJobLoc(conn, uID, jobID, city)
                except:
                    pass
            newLocation = request.form[('newLocation')]
            if newLocation: #can a user submit with an empty value
                opp.addCity(conn, newLocation)
                opp.addJobLoc(conn, uID ,jobID, newLocation)
    return redirect(url_for('home'))

@app.route('/job/<jobID>', methods=['GET', 'POST'])
def job(jobID):
    conn = dbconn2.connect(DSN)
    (job, reviews, hrs) = search.findJob(conn, jobID)
    for rev in reviews:
        print rev['review']
    return render_template('job.html',
                           job=job,
                           reviews=reviews,
                           hrs=hrs)

@app.route('/reu/<reuID>', methods=['GET', 'POST'])
def reu(reuID):
    return

# ------------------------------------------------------------------------------

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
