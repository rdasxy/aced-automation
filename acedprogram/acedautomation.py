#Todo: Look at 'RDDebug's
#Todo: Take debug=True out
from universalImports import *
from login import *
from classRegistrations import *
from newStudentRegistrations import *
from deniedStudents import *
from studentInfoGrid import *
from studentInformation import *
from editEnrollment import *
from editStudentInformation import *
from nametags import *
from TrackingGrid import *
from classSchedule import *
from classRoster import *
from studentCheckin import *
from websiteRegistrationEdit import *
from changePassword import *
from addSemester import *
from addClasses import *
from temp import *#RDDebug
################################################################################################################################################################
#Author: Riddhiman Das
#Project: ACEDAutomation
#This is a Google App Engine web application. It runs on a custom domain but uses Google's infrastructure.
################################################################################################################################################################
#First page presented to the user. Shows login stuff.
class MainPage(webapp.RequestHandler):
    def get(self):
        '''
        First verify (using cookies) if an user is already logged in.
        If someone is already logged in, redirect to main menu.
        Else, present login/welcome screen.
        '''
        currentlyLoggedInUser = validateAuthenticationCookie(self)
        if not currentlyLoggedInUser:
            self.response.headers['Content-Type'] = 'text/html'
            path = os.path.join(os.path.dirname(__file__), 'index.html')
            self.response.out.write(template.render(path, {}))
        else:
            self.redirect('/login')
        setUpTempData()#RDDebug
################################################################################################################################################################
#Handles any incoming request that is not handled by any of the defined request handlers.
class NotFoundPageHandler(webapp.RequestHandler):
    def get(self):
        self.error(404)
        path = os.path.join(os.path.dirname(__file__), '404.html')
        self.response.out.write(template.render(path, {'domain':domain}))
################################################################################################################################################################
class WelcomePage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'welcomepage.html')
        self.response.out.write(template.render(path, {}))
################################################################################################################################################################
application = webapp.WSGIApplication([( '/', MainPage ),
    ('/login',Login),
    ('/menuOptions',MainMenu),
    ('/logout',Logout),
    ('/register',ClassRegistrations),
    ('/newStudentRegistrations',NewStudentRegistrations),
    ('/deniedStudents', DeniedStudentRegistrations),
    ('/studentInformation', StudentInformation),
    ('/studentInformationGrid', studentInformationGrid),
    ('/editEnrollment', EditEnrollment),
    ('/editStudentInformation', EditStudentInformation),
    ('/nametags', Nametags),
    ('/welcomepage', WelcomePage),
    ('/trackingGrid', TrackingGrid),
    ('/classSchedule', ClassSchedule),
    ('/classList', ClassList),
    ('/classRoster', ClassRosters),
    ('/studentCheckin', StudentCheckin),
    ('/websiteRegistrationEdit', WebsiteRegistrationEdit),
    ('/changePassword', ChangePassword),
    ('/addSemester', AddSemester),
    ('/addClass', AddClass),
    ('/.*',NotFoundPageHandler)], debug = True)
################################################################################################################################################################
def main():
    run_wsgi_app(application)
################################################################################################################################################################
if __name__ == "__main__":
    main()
################################################################################################################################################################
