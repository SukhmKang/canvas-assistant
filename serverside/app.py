import os
#from io import StringIO, BytesIO

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, send_file, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from webhelpers import apology, login_required, usd
from datetime import datetime, timedelta
from calendar_maker import make_calendar,make_todolist, studybuddies

college_dict = {
    'Boston College': 'https://bostoncollege.instructure.com',
    'Brown University': 'https://canvas.brown.edu',
    'Carnegie Mellon University': 'https://canvas.cmu.edu',
    'Columbia University': 'https://courseworks2.columbia.edu',
    'Cornell University': 'https://canvas.cornell.edu',
    'Dartmouth University': 'https://canvas.dartmouth.edu',
    'Emory University': 'https://canvas.emory.edu',
    'Harvard University': 'https://canvas.harvard.edu',
    'Georgetown University': 'https://georgetown.instructure.com',
    'Massachusetts Institute of Technology' : 'https://canvas.mit.edu',
    'Northeastern University': 'https://northeastern.instructure.com',
    'Northwestern University': 'https://canvas.northwestern.edu',
    'Ohio State University': 'https://osu.instructure.com',
    'Santa Clara University': 'https://camino.instructure.com',
    'Southern Methodist University': 'https://smu.instructure.com',
    'Stanford University': 'https://canvas.stanford.edu',
    'University of California, Berkeley' : "https://bcourses.berkeley.edu",
    'University of California, Davis' : "https://canvas.ucdavis.edu",
    'University of California, Irvine' : 'https://canvas.eee.uci.edu',
    'University of California, Los Angeles' : 'https://bruinlearn.ucla.edu',
    'University of Chicago': "https://canvas.uchicago.edu",
    'University of Michigan': "https://canvas.umich.edu",
    'University of Illinois at Urbana-Champaign': 'https://canvas.illinois.edu',
    'University of Wisconsin-Madison': 'https://canvas.wisc.edu',
    'Yale University': 'https://canvas.yale.edu'
}

timezones = {
    'US/Eastern (ET)': 'US/Eastern',
    'US/Central (CT)': 'US/Central',
    'US/Pacific (PT)': 'US/Pacific',
    'Coordinated Universal Time (UTC)': 'UTC',
}


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET", "POST"])
def homepage():
    """Main page for calling all functions"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        input_data = request.get_json()
        api_key = input_data[0]['api']
        #school = input_data.get('college')
        time_zone = input_data[0]['timezone']
        school = input_data[0]['college']
        numCourses = int(input_data[0]['numcourses'])
        button = input_data[0]['button']
        result = {'worked': False, 'result': '', 'username': ''}
        #Get API Key
        try:
            api_url = college_dict[school]
        except KeyError:
            result['result'] = 'Please select a supported college.'
            return jsonify(result)
            #have to return some kind of error
            # return render_template("index.html",message='Please select a supported college.',college_dict=college_dict,timezones=timezones)

        if button == "ical":
            cal_worked,cal,username = make_calendar(api_key,api_url)
            if cal_worked:
                result['worked'] = True
                result['result'] = cal.decode("utf-8") 
                result['username'] = username
                result = jsonify(result)
                return result
                # ### making temp file stuff
                # mem = BytesIO()
                # mem.write(cal)
                # mem.seek(0)
                # ###

                # return send_file(mem, attachment_filename=f'{username}.ics')
            if username == "user authorization required":
                username = "Invalid API Key / Please enter an API Key."
            result['result'] = username
            result = jsonify(result)
            return result
            # return render_template("index.html",message=username,college_dict=college_dict,timezones=timezones)

        elif button == "todolist":
            try:
                time_zone = timezones[time_zone]
            except KeyError:
                result['result'] = 'Please enter a time zone for to-do list.'
                return jsonify(result)
                #return render_template("index.html",message='Please enter a time zone for to-do list.',college_dict=college_dict,timezones=timezones)
            todolist_worked,todolist,username = make_todolist(api_key,api_url,time_zone)
            if todolist_worked:
                result['worked'] = True
                result['result'] = todolist
                result['username'] = username
                result = jsonify(result)
                return result

                # mem = BytesIO()
                # mem.write(todolist)
                # mem.seek(0)
                # return send_file(mem, attachment_filename=f'{username}.csv')
            else:
                result['result'] = username
                result = jsonify(result)
                return result
                #return render_template("index.html",message=username,college_dict=college_dict,timezones=timezones)

        elif button == "studybuddy":
            # check if they input numcourses
            
            studybudy_worked, listofstudybuddies, username = studybuddies(api_key, api_url, numCourses)
            if studybudy_worked:
                result['worked'] = True
                result['result'] = listofstudybuddies
                result['username'] = username
                result = jsonify(result)
                return result

                # mem = BytesIO()
                # mem.write(listofstudybuddies)
                # mem.seek(0)
                # return send_file(mem, attachment_filename=f'{username}StudyBuddies.csv')
            else:
                result['result'] = listofstudybuddies
                result = jsonify(result)
                return result
                #return render_template("index.html",message=listofstudybuddies,college_dict=college_dict,timezones=timezones)
                
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("howto.html")

@app.route("/privacy", methods=["GET", "POST"])
def privacypolicy():
    return render_template('howto copy.html')