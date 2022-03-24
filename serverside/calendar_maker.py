from operator import index
from canvasapi import Canvas
import requests
import icalendar as ical
from datetime import datetime,timedelta
import pytz
import pandas as pd

#Canvas website you are using
API_URL = "https://canvas.uchicago.edu"

#User-generated API Key (can access this under user profile)
API_KEY = "2349~IYqEsKDHOn6s3i8mJZf5NYO1KhOXIuYKvpoCPz69Nw74UKG3nLv7pXT7cT341Wlb"

ISHAN_API = "1072~WHCbODVo8f39Z21k69bV8uw1rk22VbkonmwAUnm8r4pP6dqxk0zEpWAp40zMmmtr"
ISHAN_URL = "https://bcourses.berkeley.edu"
SAI_API = "1116~MkfdhO2F0r7tL5LRU37xj8vvt73fXrrAa5H1iTRKjRLPN9bEvlH2QmJqqtHZNV8L"
SAI_URL = "https://canvas.brown.edu"
NORTHEASTERNAPI = "14523~Lq5ROkPN0gHg9rZocytHViorq8mYqDxp4KkAc2rTIMOTVvi9H8GPMFrjZTVMzPpR"
CORNELLAPI = "9713~YPLxPI0wn0gQVPbD1HcoimzuqI3ev4MvW8f5lp7bprjka8bwEpjHykB0Bhnmy9hy"
irvineapi = "4407~tP2UY0qqN7l2ulqFmkl2pAhfREGR3DGic5AFBSnLq5pQywh6qUvdZToFb9FdQcp6"

def make_calendar(APIKEY,URL):
    #Initializing calendar
    cal = ical.Calendar()
    timezone = pytz.timezone('UTC')

    #Getting to-do items
    url = URL + '/api/v1/users/self/todo'
    headers = {'Authorization' : f'Bearer {APIKEY}'}
    try:
        r = requests.get(url,headers = headers)
    except requests.exceptions.ConnectionError:
        return False,'','Failed to establish a new connection'
    response = r.json()
    num_assignments = len(response)
    #If invalid access token: r.json() = {'errors': [{'message': 'Invalid access token.'}]}
    if isinstance(response, dict):
        if 'errors' in response.keys():
            try:
                errors = response['errors'][0]['message']
                return False,'',errors
            except KeyError:
                pass
            except TypeError:
                pass
    for assignment in response:
        event = ical.Event()
        assignment_name = assignment['assignment']['name']
        due_date = assignment['assignment']['due_at']
        due_date = datetime.strptime(due_date, '%Y-%m-%dT%H:%M:%SZ')
        end_date = timezone.localize(due_date)
        start_date = end_date - timedelta(minutes=15)
        html_url = assignment['html_url']
        course_name = assignment['context_name']
        event.add('summary',assignment_name)
        event.add('description',course_name)
        event.add('dtstart', start_date)
        event.add('dtend',end_date)
        event.add('url',html_url)
        cal.add_component(event)
    
    #getting user account
    url = URL + '/api/v1/users/self'
    try:
        r = requests.get(url,headers = headers)
    except requests.exceptions.ConnectionError:
        return 'Failed to establish a new connection:'
    response = r.json()
    username = response['name']

    # with open(f'/Users/sukhmkang/Desktop/College/CodingPractice/PythonPractice/Practice/Canvas/{username}.ics','wb') as export:
        # export.write(cal.to_ical())
    return True,cal.to_ical(),username


def make_todolist(APIKEY,URL,timezone):
    #Initializing time zone
    timezone = pytz.timezone(timezone)
    utc = pytz.timezone('UTC')

    #Getting to-do items
    url = URL + '/api/v1/users/self/todo'
    headers = {'Authorization' : f'Bearer {APIKEY}'}
    try:
        r = requests.get(url,headers = headers)
    except requests.exceptions.ConnectionError:
        return False,'','Failed to establish a new connection'
    response = r.json()
    num_assignments = len(response)
    #If invalid access token: r.json() = {'errors': [{'message': 'Invalid access token.'}]}
    if isinstance(response, dict):
        if 'errors' in response.keys():
            try:
                errors = response['errors'][0]['message']
                return False,'',errors
            except KeyError:
                pass
            except TypeError:
                pass
    
    todolist = pd.DataFrame(columns = ['Due Date','Assignment','Course','URL','Time Zone'])
    for assignment in response:
        assignment_name = assignment['assignment']['name']
        due_date = assignment['assignment']['due_at']
        due_date = utc.localize(datetime.strptime(due_date, '%Y-%m-%dT%H:%M:%SZ')).astimezone(timezone)
        html_url = assignment['html_url']
        course_name = assignment['context_name']
        todolist = todolist.append(
            {
                'Due Date': due_date,
                'Assignment': assignment_name,
                'Course': course_name,
                'URL': html_url,
                'Time Zone': timezone
            }, ignore_index=True
        )
    
    #getting user account
    url = URL + '/api/v1/users/self'
    try:
        r = requests.get(url,headers = headers)
    except requests.exceptions.ConnectionError:
        return 'Failed to establish a new connection:'
    response = r.json()
    username = response['name']

    return True,todolist.to_csv(mode='w'),username

def getsmallestindex(courses):
    smallestindex = 0
    for x in range(0, len(courses)):
        if courses[x][1] < courses[smallestindex][1]:
            smallestindex = x
    return smallestindex

def studybuddies(APIKEY,URL, numCourses):
    #Getting items
    url = URL + '/api/v1/users/self/courses?enrollment_state=active&per_page=100&include[]=term'
    headers = {'Authorization' : f'Bearer {APIKEY}'}
    try:
        r = requests.get(url,headers = headers)
    except requests.exceptions.ConnectionError:
        return False, 'Failed to establish a new connection:', ""
    response = r.json()
    #If invalid access token: r.json() = {'errors': [{'message': 'Invalid access token.'}]}
    if isinstance(response, dict):
        if 'errors' in response.keys():
            try:
                errors = response['errors'][0]['message']
                return False,errors, ""
            except KeyError:
                pass
            except TypeError:
                pass

    if len(response) == 0:
        return False, "You do not have any Canvas courses.", ""

    idToName = {}
    for elem in response:
        idToName[elem['id']] = elem['name']
    
    #checking for error case when user inputs numCourses > number of classes on Canvas
    if numCourses > len(response):
        numCourses = len(response)

    # setting up 2-d array of courseIDs and startDates for the first n classes
    # smallestIndex reflects the min startdate in the array
    currentcourses = []
    smallestIndex = 0
    counter=0
    for x in range(numCourses):
        course = response[x]
        courseid = course['id']
        startdate = course['start_at']
        try:
            startdate = datetime.strptime(startdate, '%Y-%m-%dT%H:%M:%SZ')
        except TypeError:
            counter+=1
            continue
        currentcourses.append([courseid, startdate])
        if startdate < currentcourses[smallestIndex][1]:
            smallestIndex = x



    # iterate through the rest of the courses in response and swap a course with the smallestIndex if it has a more recent startDate
    for x in range(numCourses, len(response)):
        course = response[x]
        courseid = course['id']
        startdate = course['start_at']
        try:
            startdate = datetime.strptime(startdate, '%Y-%m-%dT%H:%M:%SZ')
        except TypeError:
            continue
        if counter !=0:
            currentcourses.append([courseid, startdate])
            if startdate < currentcourses[smallestIndex][1]:
                smallestIndex = x
            counter-=1
            continue
        if startdate > currentcourses[smallestIndex][1]:
            currentcourses[smallestIndex] = [courseid, startdate]
            smallestIndex = getsmallestindex(currentcourses)
    
    # setting up dictionary mapping students to their set of common courses with the user
    peers = {}

    counter = 0

    idtonumstudents = {}

    for course in currentcourses:
        courseid = course[0]
        url = URL + f'/api/v1/courses/{courseid}/students'
        s = requests.get(url, headers = headers)
        students = s.json()
        try:
            for student in students:
                name = student['name']
                if name not in peers.keys():
                    peers[name] = [courseid]
                else:
                    peers[name].append(courseid)
        except TypeError:
            counter+=1
            continue
        idtonumstudents[courseid] = len(students)
    if counter == len(currentcourses):
        return False, 'Your school does not allow you to see users in your courses.', ""


    # looping through dict to find top students based on number of common classes OR all students with > 1 common course (whichever executes first)
    courseColumns = ["Course #" + str(i+1) for i in range(numCourses)]
    columns = ['Number of Common Courses','Name'] + courseColumns + ['TotalStudents']
    columns2= ['Number of Common Courses','Name'] + courseColumns

    studybuddies = pd.DataFrame(columns = columns)
    for k, v in peers.items():
        v = set(v)
        if len(v) > 1 and len(v) <= numCourses:
            temp = dict.fromkeys(columns)
            commonClasses = len(v)
            temp["TotalStudents"] = 0
            for i, elem in enumerate(v):
                temp["Course #" + str(i+1)] = [idToName[elem]]
                temp["TotalStudents"] += idtonumstudents[elem]
            temp["TotalStudents"] = [temp["TotalStudents"]]
            temp["Number of Common Courses"] = [commonClasses]
            temp["Name"] = [k]
            tempdf = pd.DataFrame.from_dict(temp)
            studybuddies = pd.concat([studybuddies, tempdf], axis = 0)
            #studybuddies = studybuddies.append(temp, ignore_index=True)
    studybuddies = studybuddies[studybuddies["Name"]!="Test Student"]
    studybuddies = studybuddies.sort_values(by=["TotalStudents"], ascending=True)
    output = pd.DataFrame()
    courses = [6,5,4,3,2]
    for elem in courses:
        currslice = studybuddies[studybuddies['Number of Common Courses'] == elem] 
        output = pd.concat([output,currslice],axis = 0)
        
    studybuddies=output[columns2]

    #getting user account
    url = URL + '/api/v1/users/self'
    try:
        r = requests.get(url,headers = headers)
    except requests.exceptions.ConnectionError:
        return False, 'Failed to establish a new connection:', ""
    response = r.json()
    username = response['name']
    studybuddies = studybuddies[studybuddies["Name"]!=username]

    if len(studybuddies) == 0:
        return False, "There are no common users between your courses.", ""
    return True, studybuddies.to_csv(index=False), username

kev_api = '1072~8FBszF2Ao4PY3jKEpdz4oTmNudLdpU0haEhAU26KbcXfn2iSpjRErzSzm4HyDsPx'

def debugging(api,url):
    return