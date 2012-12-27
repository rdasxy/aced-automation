__author__ = 'rdasxy'
'''
Module: authHelper
Helps maintain authentication and sessions.
'''
from universalImports import *
#Function to check currentacedautomationuser to check if an user is logged on.
#Argument: A subclass of RequestHandler.
#If yes, name username is returned.
#Otherwise, None is returned.
def validateAuthenticationCookie(requestHandler):
    cookie_str = requestHandler.request.headers.get('Cookie')
    if cookie_str:
        #Use regular expressions to break down cookie string
        m = re.compile(r"[a-zA-Z0-9]+")
        cookies = m.findall(cookie_str)
        if cookies[0] == "currentacedautomationuser":
            return cookies[1]
        else:
            return None
    else:
        return None
################################################################################################################################################################
#Function checks if secure information can be displayed.
#Returns the username that's currently logged in. Otherwise redirects user to login page and returns 'False'.
#Usage:
'''
currentlyLoggedInUser = securelyProceed(self)
    if currentlyLoggedInUser:
        self.response.out.write('Welcome back ' + currentlyLoggedInUser)
'''
def securelyProceed(requestHandler):
    currentlyLoggedInUser = validateAuthenticationCookie(requestHandler)
    if not currentlyLoggedInUser:
        #Delete all cookies that might have been set/
        now = datetime.datetime.fromtimestamp(time.mktime(datetime.datetime.now().timetuple()))
        interval = datetime.timedelta(minutes=authenticationTimeout)
        expireTime = now - interval
        requestHandler.response.headers.add_header('Set-Cookie', "currentcampus=none;expires=%s" % (expireTime.ctime()))
        requestHandler.response.headers.add_header('Set-Cookie', "currentsemester=none;expires=%s" % (expireTime.ctime()))
        requestHandler.response.headers.add_header('Set-Cookie', "currentacedautomationuser=none;expires=%s" % (expireTime.ctime()))
        requestHandler.response.headers['Content-Type'] = 'text/html'
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        requestHandler.response.out.write(template.render(path, {}))
        return False
    else:
        return currentlyLoggedInUser
################################################################################################################################################################
#Function that reads cookies and returns the current campus and semester.
#Argument: RequestHandler subclass.
#Returns (campus, semester) as a tuple or strings. Otherwise returns NONE.
def getCampusAndSemester(requestHandler):
    cookie_str = requestHandler.request.headers.get('Cookie')
    if cookie_str:
        #Use regular expressions to break down cookie string.
        m = re.compile(r"[a-zA-Z0-9]+")
        cookies = m.findall(cookie_str)
        campus = ""
        semester = ""
        try:
            currentcampusIdx = cookies.index("currentcampus")
            campus = cookies[currentcampusIdx + 1]
            currentsemesterIdx = cookies.index("currentsemester")
            semester = cookies[currentsemesterIdx + 1]            
            return (campus, semester)
        except ValueError:
            return (None, None)
    else:
        return None
################################################################################################################################################################
#Called after successful login. Shows the select campus/semester depending on who the user is.
#Admin can see all campuses and all semesters. The others can only view the semesters at their institution.
#Returns: True if user is a teacher, otherwise false
def successfulLogin(requestHandler, username):
    #If user is a teacher, display the teacher page.
    if username in teacherUsers:
        #Figure out the current campus and semester. The semester is always the correct one.
        currentSemesterQuery = db.GqlQuery("SELECT * FROM CurrentSemester")
        currentSemester = currentSemesterQuery.fetch(1)[0].code
        currentCampus = teacherCampuses[teacherUsers.index(username)]
        #Calculate the expiration time for the cookies we're about to set now.
        now = datetime.datetime.fromtimestamp(time.mktime(datetime.datetime.now().timetuple()))
        interval = datetime.timedelta(minutes=authenticationTimeout)
        expireTime = now + interval
        #Set cookies for current campus and semester.
        requestHandler.response.headers.add_header('Set-Cookie', "currentacedautomationuser=%s;expires=%s" % (username, expireTime.ctime()))
        requestHandler.response.headers.add_header('Set-Cookie', "currentcampus=%s;expires=%s" % (currentCampus, expireTime.ctime()))
        requestHandler.response.headers.add_header('Set-Cookie', "currentsemester=%s;expires=%s" % (currentSemester, expireTime.ctime()))
        #Get the current list of classes.
        classesQuery = db.GqlQuery("SELECT * FROM Class WHERE semester='" + currentSemester + "' ORDER BY classTimeSlot")
        classes = classesQuery.fetch(500)
        classNames = [classItem.name for classItem in classes]
        classTimeSlots = [classItem.classTimeOffered for classItem in classes]
        classIDs = [classItem.classID for classItem in classes]
        classListData = zip(classNames, classTimeSlots, classIDs)
        requestHandler.response.headers['Content-Type'] = 'text/html'
        path = os.path.join(os.path.dirname(__file__), 'teachers.html')
        requestHandler.response.out.write(template.render(path, {'classListData' : classListData}))
        return True
    #User is an admin, and display the right admin page.
    else:
        #Build the list of all semesters as strings.
        semestersQuery = db.GqlQuery("SELECT * from Semester")
        semesters = {}
        for semester in semestersQuery:
            semesters[semester.code] = semester.session + " " + str(semester.year)
        #Display the right webpage depending on the user.
        if username == "admin":
            path = os.path.join(os.path.dirname(__file__), 'select.html')
            requestHandler.response.out.write(template.render(path, {'campuses':campuses, 'authenticatedcampus':None, 'semesters':semesters}))
        else:
            path = os.path.join(os.path.dirname(__file__), 'select.html')
            requestHandler.response.out.write(template.render(path, {'campuses':None, 'authenticatedcampus':username, 'semesters':semesters}))
        return False
################################################################################################################################################################
