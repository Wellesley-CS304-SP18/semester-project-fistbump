# Fistbump!

from flask import (Flask, render_template, make_response, url_for, request, redirect, flash, session, send_from_directory, jsonify)
from werkzeug import secure_filename
from flask_cas import CAS

app = Flask(__name__)
CAS(app)

import sys, os, random
import dbconn2
import bcrypt
import view, opp, search, rev
from view import *
from opp import *
from search import *
from rev import *

app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config['CAS_SERVER'] = 'https://login.wellesley.edu:443'
app.config['CAS_AFTER_LOGIN'] = 'home'
app.config['CAS_LOGIN_ROUTE'] = '/module.php/casserver/cas.php/login'
app.config['CAS_LOGOUT_ROUTE'] = '/module.php/casserver/cas.php/logout'
app.config['CAS_AFTER_LOGOUT'] = 'login_pg'
app.config['CAS_VALIDATE_ROUTE'] = '/module.php/casserver/serviceValidate.php'

db = 'lluo2_db'

# ------------------------------------------------------------------------------
# ROUTES

@app.route('/', methods=['GET'])
def landing():
    return redirect(url_for('login_pg'))

# login and register on the same html page
@app.route('/login_pg/', methods=['GET', 'POST'])
def login_pg():
    #if user is already logged in, redirect to home

    #render empty login page
    if request.method == 'GET':
        return render_template('login.html')

@app.route('/home/', methods=['GET', 'POST'])
def home():

    conn = dbconn2.connect(DSN)

    if 'CAS_ATTRIBUTES' in session:
        attribs = session['CAS_ATTRIBUTES']
        if 'bnum' in session:
            pass
        else: 
            session['bnum'] = attribs['cas:id']
            bnum = session['bnum']
            firstname = attribs['cas:givenName']
            username = attribs['cas:sAMAccountName']
            opp.addUser(conn, bnum, firstname, username)
    if 'CAS_USERNAME' in session:
        username = session['CAS_USERNAME']
    else:
        flash('Please login to view this page content')
        return redirect(url_for('login_pg'))
    

    if request.method == 'GET':
        return render_template('home.html',
                               uName = username,
                               opportunities = getOpps(conn))

    if request.method == 'POST':
        # add a new job opportunity
        if request.form['submit'] == "Add New Job":
            return redirect(url_for('addNewJob'))

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

            jobs = search.searchJobs(conn, classPref, jobTitle, jobType, season)
            return render_template('home.html',
                                   uName = username,
                                   opportunities = jobs)

@app.route('/addNewJob/', methods=['GET','POST'])
def addNewJob():
    
    if 'bnum' in session:
        bnum = session['bnum']
    if 'CAS_USERNAME' in session:
        username = session['CAS_USERNAME']
    else:
        flash('Please login to view this page content')
        return redirect(url_for('login_pg'))

    formErr = 'Please fill in the blank fields'
    conn = dbconn2.connect(DSN)

    if request.method == 'GET':
        return render_template('job_form.html',
                               uName = username,
                               companies = opp.allCompany(conn))

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
            jobID = opp.addJob(conn, bnum, company, link, classPref, jobType, jobTitle, positionName, season, deadline)
            return redirect(url_for('addJobLocation', jobID=jobID))

@app.route('/addJobLocation/<jobID>', methods=['GET','POST'])
def addJobLocation(jobID):

    if 'bnum' in session:
        bnum = session['bnum']
    if 'CAS_USERNAME' in session:
        username = session['CAS_USERNAME']
    else:
        flash('Please login to view this page content')
        return redirect(url_for('login_pg'))

    conn = dbconn2.connect(DSN)

    if request.method == 'GET':
        cities = opp.allCities(conn)
        return render_template('jobLocation.html',
                               jobID = jobID,
                               cities = cities,
                               uName = username)

    if request.method == 'POST':
        if request.form['submit'] == 'submit':
            cities = opp.allCities(conn)
            if bool(cities):
                try:
                    locations = request.form.getlist('city')
                    for city in locations:
                        opp.addJobLoc(conn, bnum, jobID, city)
                except:
                    pass
            newLocation = request.form[('newLocation')]
            if newLocation: #can a user submit with an empty value
                opp.addCity(conn, newLocation)
                opp.addJobLoc(conn, bnum, jobID, newLocation)
        return redirect(url_for('home'))

@app.route('/job/<jobID>', methods=['GET', 'POST'])
def job(jobID):

    if 'bnum' in session:
        bnum = session['bnum']
    if 'CAS_USERNAME' in session:
        username = session['CAS_USERNAME']
    else:
        flash('Please login to view this page content')
        return redirect(url_for('login_pg'))

    conn = dbconn2.connect(DSN)

    if request.method == 'GET':
        (job, reviews) = search.findJob(conn, jobID)
        return render_template('job.html',
                               uName=username,
                               job=job,
                               reviews=reviews)

    if request.method == 'POST':
        if request.form['submit'] == 'Add Job Review':
            return redirect(url_for('addNewReview',
                                    jobID=jobID))

@app.route('/addNewReview/<jobID>', methods=['GET','POST'])
def addNewReview(jobID):

    if 'bnum' in session:
        bnum = session['bnum']
    if 'CAS_USERNAME' in session:
        username = session['CAS_USERNAME']
    else:
        flash('Please login to view this page content')
        return redirect(url_for('login_pg'))

    conn = dbconn2.connect(DSN)

    if request.method == 'GET':
        return render_template('review_form.html',
                               jobID = jobID,
                               uName = username)

    if request.method == 'POST':
        if request.form['submit'] == 'Submit Review':
            jobYear = request.form[('jobYear')]
            review = request.form[('review')]

            addJob = addJobRev(conn, bnum, jobID, jobYear, review)
            if not addJob:
                flash("A review already exists for this job and user")
            else:
                flash("Review added successfully")
            return redirect(url_for('job', jobID=jobID))

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
