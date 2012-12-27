__author__ = 'rdasxy'

from universalImports import *
from aadbdef import *
from authHelper import *

################################################################################################################################################################
#Screen presented to the user right after log in. Shows main menu on correct authentication.
class Login(webapp.RequestHandler):
    def post(self):
        try:    
            #Verify that username and password were entered correctly, and then set a cookie with an expiration of 30 minutes.
            authenticatedUsers = db.GqlQuery("SELECT * from User WHERE userName='" + self.request.get('username') + "' AND password='" + self.request.get('password') + "'")
            if (authenticatedUsers.count() == 1):
                isTeacher = successfulLogin(self, self.request.get('username'))
                if not isTeacher:
                    #Display a welcome message.
                    self.response.headers['Content-Type'] = 'text/html'
                    self.response.out.write("<h4>You are logged in as <i>" + self.request.get('username') + "</i></h4><br>")
                    #Set authentication cookie.
                    now = datetime.datetime.fromtimestamp(time.mktime(datetime.datetime.now().timetuple()))
                    interval = datetime.timedelta(minutes=authenticationTimeout)
                    expireTime = now + interval
                    self.response.headers.add_header('Set-Cookie', "currentacedautomationuser=%s;expires=%s" % (self.request.get('username'), expireTime.ctime()))
            else:
                #If username and password were invalid, show error screen.
                self.response.headers['Content-Type'] = 'text/html'
                path = os.path.join(os.path.dirname(__file__), 'error.html')
                self.response.out.write(template.render(path, {'domain':domain}))
        except Exception, e:
            reportError(self, "Sorry. There's been an error: " + str(e))
    def get(self):
        try:    
            #If user currently logged in, show screen to select semesters (and campus if admin).
            currentlyLoggedInUser = securelyProceed(self)
            if currentlyLoggedInUser:
                self.response.headers['Content-Type'] = 'text/html'
                if currentlyLoggedInUser not in teacherUsers:
                    self.response.out.write('<h1>Hello <i> ' + currentlyLoggedInUser + "</i></h1><br>")
                successfulLogin(self, currentlyLoggedInUser)
        except Exception, e:
            reportError(self, "Sorry. There's been an error: " + str(e))
################################################################################################################################################################
#Presents main menu of options.
class MainMenu(webapp.RequestHandler):
    try:
        def get(self):
            #If user currently logged in, show main menu screen.
            currentlyLoggedInUser = securelyProceed(self)
            if currentlyLoggedInUser:
                #Calculate the expiration time for the cookies we're about to set now.
                now = datetime.datetime.fromtimestamp(time.mktime(datetime.datetime.now().timetuple()))
                interval = datetime.timedelta(minutes=authenticationTimeout)
                expireTime = now + interval
                campusDisplay = ""
                if self.request.get("campus"):
                    #Store the correct campus name in a cookie. This doesn't have to be parsed.
                    self.response.headers.add_header('Set-Cookie', "currentcampus=%s;expires=%s" % (self.request.get("campus"), expireTime.ctime()))
                    campusDisplay = self.request.get("campus")
                elif self.request.get("authenticatedcampus"):
                    #Store the correct campus name in a cookie. This has to be parsed.
                    campus = self.request.get("authenticatedcampus")
                    if (campus == "lvccadmin"):
                        campus = "lv"
                    elif (campus == "bradmin"):
                        campus = "br"
                    campusDisplay = campus
                    self.response.headers.add_header('Set-Cookie', "currentcampus=%s;expires=%s" % (campus, expireTime.ctime()))
                campusDisplay = campusDisplay.upper()
                #Store the current semester information in a cookie. There is no parsing to be done here.
                self.response.headers.add_header('Set-Cookie', "currentsemester=%s;expires=%s" % (self.request.get("semester"), expireTime.ctime()))
                self.response.headers['Content-Type'] = 'text/html'
                path = os.path.join(os.path.dirname(__file__), 'master.html')
                if currentlyLoggedInUser == "admin":
                    self.response.out.write(template.render(path, {"currentUser" : currentlyLoggedInUser, "campus" : campusDisplay, "semester" : self.request.get("semester"), "admin" : "YES"}))
                else:
                    self.response.out.write(template.render(path, {"currentUser" : currentlyLoggedInUser, "campus" : campusDisplay, "semester" : self.request.get("semester")}))
    except Exception, e:
        reportError(self, "Sorry. There's been an error: " + str(e))
################################################################################################################################################################
#Presents main menu of options.
class Logout(webapp.RequestHandler):
    try:    
        def get(self):
            #If user currently logged in, show main menu screen.
            currentlyLoggedInUser = securelyProceed(self)
            if currentlyLoggedInUser:
                #Set the cookies to expire 'authenticationTimeout' minutes before - this deletes the cookies.
                now = datetime.datetime.fromtimestamp(time.mktime(datetime.datetime.now().timetuple()))
                interval = datetime.timedelta(minutes=authenticationTimeout)
                expireTime = now - interval
                #Store the current semester information in a cookie. There is no parsing to be done here - this deletes all cookies.
                self.response.headers.add_header('Set-Cookie', "currentcampus=none;expires=%s" % (expireTime.ctime()))
                self.response.headers.add_header('Set-Cookie', "currentsemester=none;expires=%s" % (expireTime.ctime()))
                self.response.headers.add_header('Set-Cookie', "currentacedautomationuser=none;expires=%s" % (expireTime.ctime()))            
                self.response.headers['Content-Type'] = 'text/html'
                path = os.path.join(os.path.dirname(__file__), 'logout.html')
                self.response.out.write(template.render(path, {'domain':domain}))
    except Exception, e:
        reportError(self, "Sorry. There's been an error: " + str(e))
