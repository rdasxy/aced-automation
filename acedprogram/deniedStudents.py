__author__ = 'rdasxy'

from universalImports import *
from aadbdef import *
from authHelper import *

################################################################################################################################################################
#Screen presented to the user to view and/or approve and/or delete denied student registrations.
class DeniedStudentRegistrations(webapp.RequestHandler):
    #Show screen listing all denied students.
    #Also, if 'accept' or 'delete' are available, process those requests.
    def get(self):
        try:    
            #If user currently logged in, show new registrations.
            currentlyLoggedInUser = securelyProceed(self)
            if currentlyLoggedInUser:
                #If an accept request was found, accept the student.
                if self.request.get('accept'):
                    enrollmentsQuery = db.GqlQuery("SELECT * FROM Enrollment WHERE studentID = '" + self.request.get('accept') + "'")
                    enrollmentResult = enrollmentsQuery.fetch(5000)
                    if enrollmentResult:
                        for enrollment in enrollmentResult:
                            #First, verify that a campus was chosen.
                            if enrollment.campus != "No campus chosen":
                                #Check for duplicate enrollments.
                                enrollmentDuplicatesQuery = db.GqlQuery("SELECT * FROM Enrollment WHERE studentID = '" + enrollment.studentID
                                                                        + "' AND campus='" + enrollment.campus + "' AND semesterCode='" + enrollment.semesterCode + "'")
                                if enrollmentDuplicatesQuery.count() > 1:
                                    self.response.out.write("This student is already signed up for the same campus for this semester. Cannot approve enrollment."+
                                                            "<br/>To delete this enrollment, please hit 'back' and then click 'Delete'")
                                    return
                                #Approve enrollment.
                                enrollment.approved = True
                                enrollment.denied = False
                                classIDs = []
                                classFees = 0
                                #Update class IDs and calculate fees owed.
                                classes = enrollment.classFirstPreferences.split(',')
                                for className in classes:
                                    #If no class is chosen for a slot, just append 'None' and do not update the class records.
                                    if className == "None":
                                        classIDs.append("None")
                                    else:
                                        classQuery = db.GqlQuery("SELECT * FROM Class WHERE name='" + className + "'")
                                        currentClasses = classQuery.fetch(1)
                                        currentClass = currentClasses[0]
                                        currentClass.studentCount += 1
                                        correctStudentLimit = 0
                                        if enrollment.campus == "UMKC":
                                            currentClass.studentCountUMKC += 1
                                            correctStudentLimit = currentClass.studentCountUMKC
                                        elif enrollment.campus == "BR":
                                            currentClass.studentCountBR += 1
                                            correctStudentLimit = currentClass.studentCountBR
                                        elif enrollment.campus == "LV":
                                            currentClass.studentCountLV += 1
                                            correctStudentLimit = currentClass.studentCountLV
                                        if correctStudentLimit >= currentClass.studentLimit:
                                            self.response.out.write("Note: " + currentClass.name + " is overflowing. ("
                                                                    + str(currentClass.studentCount) + "/" + str(currentClass.studentLimit) + ")<br/>")
                                        classIDs.append(str(currentClass.classID))
                                        classFees += currentClass.classFee
                                        currentClass.put()
                                enrollment.classIDs = ",".join(classIDs)
                                enrollment.notes = "Fees Owed = $" + str(classFees)
                                enrollment.put()
                                self.response.out.write("Accepted student " + self.request.get('accept'))
                            else:
                                self.response.out.write("ERROR: Please assign the student to a valid campus. Hit the browser back button to go back.")
                                return
                #If a delete request was found, delete the student.
                elif self.request.get('delete'):
                    enrollmentsQuery = db.GqlQuery("SELECT * FROM Enrollment WHERE studentID = '" + self.request.get('delete') + "'")
                    enrollmentResult = enrollmentsQuery.fetch(1)
                    if enrollmentResult:
                        enrollment = enrollmentResult[0]
                    enrolledClasses = enrollment.classIDs.split(',')
                    for classID in enrolledClasses:
                        if classID != "None":
                            classesQuery = db.GqlQuery("SELECT * FROM Class WHERE classID=" + classID)
                            currentClass = classesQuery.fetch(1)[0]
                            if enrollment.campus == "UMKC":
                                currentClass.studentCountUMKC -= 1
                            elif enrollment.campus == "BR":
                                currentClass.studentCountBR -= 1
                            elif enrollment.campus == "LV":
                                currentClass.studentCountLV -= 1
                            currentClass.put()
                    enrollment.approved = False
                    enrollment.denied = True
                    enrollment.delete()
                #Display list of all new students that haven't been deleted yet (but have been denied).
                self.response.headers['Content-Type'] = 'text/html'
                #currentSemester = db.GqlQuery("SELECT * from CurrentSemester")
                #semesterCode = currentSemester[0].code
                campus, semesterCode = getCampusAndSemester(self)
                currentSemesterEnrollments = db.GqlQuery("SELECT * FROM Enrollment WHERE semesterCode='" + semesterCode + "' AND approved=False AND denied=True")
                studentIDandName = {}
                for currentEnrollment in currentSemesterEnrollments:
                    currentStudent = db.GqlQuery("SELECT * FROM Student WHERE uniqueID='" + currentEnrollment.studentID + "'")
                    studentIDandName[currentEnrollment.studentID] = currentStudent[0].name
                self.response.headers['Content-Type'] = 'text/html'
                path = os.path.join(os.path.dirname(__file__), 'deniedStudents.html')
                if len(studentIDandName) >= 1:
                    self.response.out.write(template.render(path, {'studentsList':studentIDandName, 'semester':semesterCode}))
                else:
                    self.response.out.write(template.render(path, {'semester':semesterCode}))
        except Exception, e:
            reportError(self, "Sorry. There's been an error: " + str(e))
