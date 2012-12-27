__author__ = 'rdasxy'

from universalImports import *
from aadbdef import *
from authHelper import *
################################################################################################################################################################
#Allows the admin to change the current registration form on the website.
class WebsiteRegistrationEdit(webapp.RequestHandler):
    #Displays a list of all current semesters to choose from.
    def get(self):
        try:    
            currentlyLoggedInUser = securelyProceed(self)
            if currentlyLoggedInUser:
                #Build a list of all years. Make sure years are unique.
                semestersQuery = db.GqlQuery("SELECT * FROM Semester")
                semesters = semestersQuery.fetch(500)
                years = []
                for semester in semesters:
                    year = str(semester.year)
                    if year not in years:
                        years.append(year)
                #Get the names of the contacts.
                contactsQuery = db.GqlQuery("SELECT * FROM CurrentSemester")
                contacts = contactsQuery.fetch(1)[0]
                umkcContact = contacts.umkcContactName
                lvContact = contacts.lvContactName
                brContact = contacts.brContactName
                #Display the page.
                self.response.headers['Content-Type'] = 'text/html'
                path = os.path.join(os.path.dirname(__file__), 'websiteregistrationedit.html')
                self.response.out.write(template.render(path, {'years' : years, 'umkcname':umkcContact,'lvname':lvContact,'brname':brContact}))
        except Exception, e:
            reportError(self, "Sorry. There's been an error: " + str(e))
    def post(self):
        try:
            semesterName = escapeString(self.request.get('semester'))
            year = escapeString(self.request.get('year'))
            UMKCcontact = escapeString(self.request.get('UMKCcontact'))
            LVcontact = escapeString(self.request.get('LVcontact'))
            BRcontact = escapeString(self.request.get('BRcontact'))
            #Get the semester code.
            semesterQuery = db.GqlQuery("SELECT * FROM Semester WHERE session='" + semesterName + "' AND year=" + year)
            semester = semesterQuery.fetch(1)[0]
            #Update the current semester.
            currentSemesterQuery = db.GqlQuery("SELECT * FROM CurrentSemester")
            currentSemester = currentSemesterQuery.fetch(1)[0]
            currentSemester.code = semester.code
            currentSemester.semesterKind = semesterName
            currentSemester.umkcContactName = UMKCcontact
            currentSemester.lvContactName = LVcontact
            currentSemester.brContactName = BRcontact
            currentSemester.put()
            self.response.out.write("Your changes have been changed.")
        except:
            reportError(self, "Invalid input. Please check and try again.")


