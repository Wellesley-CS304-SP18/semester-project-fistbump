 # Fistbump!

from flask import (Flask, render_template, make_response, url_for, request, redirect, flash, session, send_from_directory, jsonify)
from werkzeug import secure_filename
from flask_cas import CAS

import os
import imghdr


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
from profile import *

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
    if 'CAS_ATTRIBUTES' in session:
        flash('You\'re already logged in!')
        return redirect(url_for('home'))

    #render empty login page
    if request.method == 'GET':
        return render_template('login.html')

@app.route('/home/', methods=['GET', 'POST'])
def home():

    conn = dbconn2.connect(DSN)

    if 'CAS_ATTRIBUTES' in session:
        attribs = session['CAS_ATTRIBUTES']
        if 'bnum' in session:
            bnum = session['bnum']
        else:
            session['bnum'] = attribs['cas:id']
            bnum = session['bnum']
            firstname = attribs['cas:givenName']
            username = attribs['cas:sAMAccountName']
            opp.addUser(conn, bnum, firstname, username)

        exists = profExists(conn,bnum)
        if exists == True:
            filename = secure_filename(str(bnum)+'.jpeg')
            src=url_for('pic',fname=filename)

    if 'CAS_USERNAME' in session:
        username = session['CAS_USERNAME']
    else:
        flash('Please login to view this page content')
        return redirect(url_for('login_pg'))

    if request.method == 'GET':
        return render_template('home.html',
                               uName = username,
                               opportunities=getOpps(conn), 
                               picture_exists=exists,
                               src=src)

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
                                   uName=username,
                                   opportunities=jobs, 
                                   src=src, 
                                   picture_exists=exists)

@app.route('/addNewJob/', methods=['GET','POST'])
def addNewJob():

    conn = dbconn2.connect(DSN)

    if 'bnum' in session:
        bnum = session['bnum']
    if 'CAS_USERNAME' in session:
        username = session['CAS_USERNAME']
    else:
        flash('Please login to view this page content')
        return redirect(url_for('login_pg'))

    exists = profExists(conn,bnum)
    if exists == True:
        filename = secure_filename(str(bnum)+'.jpeg')
        src=url_for('pic',fname=filename)

    formErr = 'Please fill in the blank fields'

    if request.method == 'GET':
        return render_template('job_form.html',
                               uName=username,
                               companies=opp.allCompany(conn),
                               picture_exists=exists,
                               src=src)

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
            city = request.form[('location')]
            if company == 'none':
                company = request.form[('newCompany')]
            jobID = opp.addJob(conn, bnum, company, link, classPref, jobType, jobTitle, positionName, season, deadline)
            opp.addJobLoc(conn, bnum, jobID, city)
            return redirect(url_for('addJobLocation', jobID=jobID))

@app.route('/addJobLocation/<jobID>', methods=['GET','POST'])
def addJobLocation(jobID):

    conn = dbconn2.connect(DSN)

    if 'bnum' in session:
        bnum = session['bnum']
    if 'CAS_USERNAME' in session:
        username = session['CAS_USERNAME']
    else:
        flash('Please login to view this page content')
        return redirect(url_for('login_pg'))

    exists = profExists(conn,bnum)
    if exists == True:
        filename = secure_filename(str(bnum)+'.jpeg')
        src=url_for('pic',fname=filename)

    if request.method == 'GET':
        cities = opp.allCities(conn)
        return render_template('jobLocation.html',
                               jobID=jobID,
                               cities=cities,
                               uName=username, 
                               src=src, 
                               picture_exists=exists)

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

    conn = dbconn2.connect(DSN)

    if 'bnum' in session:
        bnum = session['bnum']
    if 'CAS_USERNAME' in session:
        username = session['CAS_USERNAME']
    else:
        flash('Please login to view this page content')
        return redirect(url_for('login_pg'))

    exists = profExists(conn,bnum)
    if exists == True:
        filename = secure_filename(str(bnum)+'.jpeg')
        src=url_for('pic',fname=filename)

    # displays job info & reviews
    if request.method == 'GET':
        (job, locations, reviews) = search.findJob(conn, jobID, bnum)
        return render_template('job.html',
                               bnum=bnum,
                               uName=username,
                               job=job,
                               locations=locations,
                               reviews=reviews,
                               src=src, 
                               picture_exists=exists)

    if request.method == 'POST':
        # if user wants to add a review for job --> redirects to review form  
        if request.form['submit'] == 'Add Job Review':
            return redirect(url_for('addNewReview',
                                    jobID=jobID))

        # if user wants to edit their own review --> redirects to update form
        if request.form['submit'] == 'Edit Review':
            return redirect(url_for('editReview',
                                    jobID=jobID))

        # if user wants to delete their own review --> rerenders page
        if request.form['submit'] == 'Delete Review':
            deleteJobRev(conn, bnum, jobID)
            (job, locations, reviews) = search.findJob(conn, jobID, bnum)
            return render_template('job.html',
                                   bnum=bnum,
                                   uName=username,
                                   job=job,
                                   locations=locations,
                                   reviews=reviews,
                                   src=src, 
                                   picture_exists=exists)

@app.route('/addNewReview/<jobID>', methods=['GET','POST'])
def addNewReview(jobID):

    conn = dbconn2.connect(DSN)

    if 'bnum' in session:
        bnum = session['bnum']
    if 'CAS_USERNAME' in session:
        username = session['CAS_USERNAME']
    else:
        flash('Please login to view this page content')
        return redirect(url_for('login_pg'))

    exists = profExists(conn,bnum)
    if exists == True:
        filename = secure_filename(str(bnum)+'.jpeg')
        src=url_for('pic',fname=filename)
    
    if request.method == 'GET':
        return render_template('review_form.html',
                               jobID=jobID,
                               uName=username, 
                               src=src, 
                               picture_exists=exists)

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

# editting a review user made
@app.route('/editReview/<jobID>', methods=['GET','POST'])
def editReview(jobID):

    conn = dbconn2.connect(DSN)

    if 'bnum' in session:
        bnum = session['bnum']
    if 'CAS_USERNAME' in session:
        username = session['CAS_USERNAME']
    else:
        flash('Please login to view this page content')
        return redirect(url_for('login_pg'))

    exists = profExists(conn,bnum)
    if exists == True:
        filename = secure_filename(str(bnum)+'.jpeg')
        src=url_for('pic',fname=filename)

    if request.method == 'GET':
        rev = getRev(conn, bnum, jobID)
        if rev is None:
            flash('You do not have a review for this job.')
            return redirect(url_for('job', jobID=jobID))
        return render_template('update_review.html',
                               uName=username,
                               jobID=jobID,
                               jobYear=rev['jobYear'],
                               review=rev['review'],
                               src=src, 
                               picture_exists=exists)

    if request.method == 'POST':
        if request.form['submit'] == 'Update Review':
            jobYear = request.form[('jobYear')]
            review = request.form[('review')]

            update = updateJobRev(conn, bnum, jobID, jobYear, review)
            return redirect(url_for('job', jobID=jobID))

#upload
@app.route('/profile/', methods=["GET", "POST"])
def profile():

    conn = dbconn2.connect(DSN)
    
    if 'bnum' in session:
        bnum = session['bnum']
        user = getUserInfo(conn, bnum)
        username = user['username']
        exists = profExists(conn,bnum)

        if exists == True:
            filename = secure_filename(str(bnum)+'.jpeg')
            pathname = 'images/'+filename
            src=url_for('pic',fname=filename)
        
    if request.method == 'GET':
        return render_template('profile.html', 
                               user=user, 
                               uName=username, 
                               src=src,
                               picture_exists=exists)
    else:
        try:
            if request.form['submit'] == 'Update Picture':
                f = request.files['photo']
                mime_type = imghdr.what(f.stream)
                if mime_type != 'jpeg':
                    raise Exception('Not a JPEG')
                filename = secure_filename(str(bnum)+'.jpeg')
                pathname = 'images/'+filename
                f.save(pathname)
                flash('Upload successful')
                addProfPic(conn, bnum, pathname)
                return render_template('profile.html',
                                   bnum=bnum,
                                   user=user,
                                   uName=username,
                                   src=src,
                                   picture_exists=exists)

        except Exception as err:
            flash('Upload failed: {why}'.format(why=err))
            return render_template('profile.html',
                                   bnum=bnum, 
                                   user=user, 
                                   uName=username, 
                                   src=src,
                                   picture_exists=exists)

#uploading pic route
@app.route('/pic/<fname>')
def pic(fname):
    f = secure_filename(fname)
    return send_from_directory('images',f)


# ------------------------------------------------------------------------------

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = 1946
    DSN = dbconn2.read_cnf()
    DSN['db'] = db
    app.debug = True
    app.run('0.0.0.0',port)
