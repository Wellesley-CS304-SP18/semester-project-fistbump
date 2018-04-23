#fistbump!

from flask import (Flask, render_template, make_response, url_for, request, redirect, flash, session, send_from_director, jsonify)
from werkzeug import secure_filename
app = Flask(__name__)

import sys, os, random
import dbconn2
import bcrypt
from operations import *
from login import * 

app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])
app.confid['TRAP_BAD_REQUEST_ERRORS'] = True

db = 'lluo2_db'

# --------------------------------------------
# ROUTES

@app.route('/login/', methods=['GET', 'POST'])
def login():
    errorMsg = 'Username and/or password are incorrect.'
    successMsg = 'Successful login.'
    conn = dbconn2.connect(DSN)
   
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('pwd')
        hashed = getPwd(conn, email)['pwd']
        if hashed is not None:
            if bcrypt.hashpw(pwd, hashed) != hashed:
                flash(errorMsg)
                return render_template('login.html')
            else:
                flash(successMsg)
                return redirect(url_for('home'))
        else:
            flash(errorMsg)
            return render_template('login.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        uName = request.form.get('uName')
        email = request.form.get('email')
        pwd = request.form.get('pwd')
        
        if not emailIsFree(conn, email):
            flash('Email already in use.')
            return render_template('register.html')
        else:
            hashedPwd = bcrypt.hashpw(pwd, bcrypt.gensalt())
            insertUser(conn, uName, email, hashedPwd);
            flash('User successfully added.')
            return redirect(url_for('login.html'))

@app.route('/home/', methods=['GET','POST'])
def home():
    return

@app.route('/job/<jobID>', methods=['GET', 'POST'])
def job():
    return

@app.route('/reu/<reuID>', methods=['GET', 'POST'])
def reu():
    return

# --------------------------------------------

if __name__ = '__main__':
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
