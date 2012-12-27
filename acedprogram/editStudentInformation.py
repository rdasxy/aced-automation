__author__ = 'rdasxy'

from universalImports import *
from aadbdef import *
from authHelper import *

################################################################################################################################################################
#Screen presented to the user to view (and approve) student registrations.
class EditStudentInformation(webapp.RequestHandler):
    #Show screen listing all denied students.
    #Also, if 'accept' or 'delete' are available, process those requests.
    def get(self):
        try:    
            #If user currently logged in, show new registrations.
            currentlyLoggedInUser = securelyProceed(self)
            if currentlyLoggedInUser:
                #If an accept request was found, accept the student.
                studentID = escapeString(self.request.get('ID'))
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
                            path = os.path.join(os.path.dirname(__file__), 'editStudentInformation.html')
                            self.response.out.write(template.render(path, {'studentid':studentID, 'studentName':student.name,
                                                                           'phone' : student.phone, 'address' : student.address,
                                                                           'city' : student.city, 'state' : student.state,
                                                                           'zip' : student.zip, 'email': student.email,
                                                                           'newStudent': student.newStudent,
                                                                           'newAddress' : student.newAddress,
                                                                           'specialInstructions' : student.specialInstructions,
                                                                           'name' : emContact.emContactName, 'relationship' : emContact.emContactRelationShip,
                                                                           'homephone' : emContact.emContactHomePhone, 'pager' : emContact.emContactPager,
                                                                           'workphone' : emContact.emContactWork, 'cellphone' : emContact.emContactCell,
                                                                           'semester' : enrollment.semesterCode, 'firstpreferences' : enrollment.classFirstPreferences,
                                                                           'secondpreferences' : enrollment.classSecondPreferences,
                                                                           'notes' : enrollment.notes}))
        except Exception, e:
            reportError(self, "Sorry. There's been an error: " + str(e))
    #Update the information for each student.
    def post(self):
        try:    
            currentlyLoggedInUser = securelyProceed(self)
            if currentlyLoggedInUser:
                #Get the changes from the user
                studentInformation = {'studentID': escapeString(self.request.get("studentID")),
                                      'studentName': escapeString(self.request.get("studentName")), 'phone': escapeString(self.request.get("phone")),
                                      'address': escapeString(self.request.get("address")), 'city': escapeString(self.request.get("city")),
                                      'state': escapeString(self.request.get("state")), 'zip': escapeString(self.request.get("zip")),
                                      'email': escapeString(self.request.get("email")), 'newStudent': escapeString(self.request.get("newStudent")),
                                      'newAddress': escapeString(self.request.get("newAddress")),
                                      'specialInstructions': escapeString(self.request.get("specialInstructions")),
                                      'name': escapeString(self.request.get("name")), 'relationship': escapeString(self.request.get("relationship")),
                                      'homephone': escapeString(self.request.get("homephone")), 'pager': escapeString(self.request.get("pager")),
                                      'workphone': escapeString(self.request.get("workphone")),
                                      'cellphone': escapeString(self.request.get("cellphone")), 'notes' : escapeString(self.request.get("notes"))}
    
                #Find the right student record.
                studentsQuery = db.GqlQuery("SELECT * FROM Student WHERE uniqueID='" + studentInformation['studentID'] + "'")
                studentsResult = studentsQuery.fetch(1)
                if studentsResult:
                    student = studentsResult[0]
                    #Find the right emergency contact.
                    emContactQuery = db.GqlQuery("SELECT * FROM EmergencyContact WHERE forStudentWithUniqueID='" + studentInformation['studentID'] + "'")
                    emContactResult = emContactQuery.fetch(1)
                    if emContactResult:
                        emContact = emContactResult[0]
                    #Save changes to student information.
                    student.name = studentInformation['studentName']
                    student.phone = studentInformation['phone']
                    student.address = studentInformation['address']
                    student.city = studentInformation['city']
                    student.state = studentInformation['state']
                    student.zip = studentInformation['zip']
                    student.email = studentInformation['email']
                    student.newStudent = True if studentInformation['newStudent'] == "Yes" else False
                    student.newAddress = True if studentInformation['newAddress'] == "Yes" else False
                    student.specialInstructions = studentInformation['specialInstructions']
                    student.put()
                    #Save changes to emergency contact information.
                    emContact.emContactCell = studentInformation['cellphone']
                    emContact.emContactHomePhone = studentInformation['homephone']
                    emContact.emContactName = studentInformation['name']
                    emContact.emContactWork = studentInformation['workphone']
                    emContact.emContactPager = studentInformation['pager']
                    emContact.emContactRelationShip = studentInformation['relationship']
                    emContact.put()
    
                    #Find the right enrollment record.
                    enrollmentQuery = db.GqlQuery("SELECT * FROM Enrollment WHERE studentID='" + studentInformation['studentID'] + "'")
                    enrollmentResult = enrollmentQuery.fetch(1)
                    if enrollmentResult:
                        enrollment = enrollmentResult[0]
                        enrollment.notes = studentInformation['notes']
                        enrollment.put()
    
                        self.response.out.write("Your changes have been successfully updated.")
        except Exception, e:
            reportError(self, "Sorry. There's been an error: " + str(e))




