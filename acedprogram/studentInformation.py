__author__ = 'rdasxy'

from universalImports import *
from aadbdef import *
from authHelper import *

################################################################################################################################################################
#Screen presented to the user to view (and edit) student registrations.
class StudentInformation(webapp.RequestHandler):
    #Show screen listing all denied students.
    #Also, if 'accept' or 'delete' are available, process those requests.
    def get(self):
        try:
            #If user currently logged in, show new registrations.
            currentlyLoggedInUser = securelyProceed(self)
            if currentlyLoggedInUser:
                #If an accept request was found, accept the student.
                studentID = self.request.get('ID')
                enrollmentsQuery = db.GqlQuery("SELECT * FROM Enrollment WHERE studentID = '" + studentID + "'")
                enrollmentResult = enrollmentsQuery.fetch(1)
                if enrollmentResult:
                    enrollment = enrollmentResult[0]
                #Get information about the current student.
                studentsQuery = db.GqlQuery("SELECT * FROM Student WHERE uniqueID='" + studentID + "'")
                studentsResult = studentsQuery.fetch(1)
                if studentsResult:
                    student = studentsResult[0]
                #Get information about the student's emergency contact.
                emContactQuery = db.GqlQuery("SELECT * FROM EmergencyContact WHERE forStudentWithUniqueID='" + studentID + "'")
                emContactResult = emContactQuery.fetch(1)
                if emContactResult:
                    emContact = emContactResult[0]
                self.response.headers['Content-Type'] = 'text/html'
                path = os.path.join(os.path.dirname(__file__), 'studentInformation.html')
                self.response.out.write(template.render(path, {'studentid':studentID, 'studentName':student.name,
                                                               'phone' : student.phone, 'address' : student.address,
                                                               'city' : student.city, 'state' : student.state,
                                                               'zip' : student.zip, 'email': student.email,
                                                               'newStudent': "Yes" if student.newStudent else "No",
                                                               'newAddress' : "Yes" if student.newAddress else "No",
                                                               'specialInstructions' : student.specialInstructions,
                                                               'name' : emContact.emContactName, 'relationship' : emContact.emContactRelationShip,
                                                               'homephone' : emContact.emContactHomePhone, 'pager' : emContact.emContactPager,
                                                               'workphone' : emContact.emContactWork, 'cellphone' : emContact.emContactCell,
                                                               'semester' : enrollment.semesterCode, 'firstpreferences' : enrollment.classFirstPreferences,
                                                               'secondpreferences' : enrollment.classSecondPreferences, 'campuses' : enrollment.campus,
                                                               'notes' : enrollment.notes}))
        except Exception, e:
            reportError(self, "Sorry. There's been an error: " + str(e))
