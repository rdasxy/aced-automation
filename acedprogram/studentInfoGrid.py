__author__ = 'rdasxy'

from universalImports import *
from aadbdef import *
from authHelper import *

################################################################################################################################################################
#Shows student information grid.
class studentInformationGrid(webapp.RequestHandler):
    def get(self):
        try:    
            campus, semester = getCampusAndSemester(self)
            #Get the list of enrollments for the current semester.
            enrollmentQuery = db.GqlQuery("SELECT * FROM Enrollment WHERE semesterCode = '" + semester + "' AND campus = '" + campus.upper() + "' AND approved=True ORDER BY studentID")
            enrollments = enrollmentQuery.fetch(500)
            #Get the list of students for the current campus.
            studentIDs = [enrollment.studentID for enrollment in enrollments]
            #Get the list of students notes.
            studentNotes = [enrollment.notes for enrollment in enrollments]
            #Get the list of classes for all student for the current campus.
            studentClassesListsOverall = [enrollment.classFirstPreferences for enrollment in enrollments]
            studentClasses = []
            for classEntity in studentClassesListsOverall:
                classesBreakDown = classEntity.split(',')
                studentClasses.append(classesBreakDown)
            #Get the list of student names and addresses for all the relevant enrollments.
            studentNames = []
            studentAddresses = []
            emContacts = []
            studentSpecialInstructions = []
            for studentID in studentIDs:
                studentsQuery = db.GqlQuery("SELECT * FROM Student WHERE uniqueID = '" + studentID + "'")
                student = studentsQuery.fetch(1)
                #Save student name.
                studentName = student[0].name
                studentNames.append(studentName)
                #Save student address.
                studentAddress = student[0].address + "<br/>" + student[0].city + " " + student[0].state + " " + student[0].zip
                if student[0].phone != "":
                    studentAddress += "<br/>Phone: " + student[0].phone
                studentAddresses.append(studentAddress)
                #Save the student's special instructions.
                studentSpecialInstructions.append(student[0].specialInstructions)
                #Save student emergency contact.
                emContactsQuery = db.GqlQuery("SELECT * FROM EmergencyContact WHERE forStudentWithUniqueID = '" + studentID + "'")
                emContact = emContactsQuery.fetch(1)
                emContactInfo = emContact[0].emContactName + "<br/><i>" + emContact[0].emContactRelationShip + "</i>"
                if emContact[0].emContactHomePhone != "":
                    emContactInfo += "<br/>Home: " + emContact[0].emContactHomePhone
                if emContact[0].emContactPager != "":
                    emContactInfo += "<br/>Pager: " + emContact[0].emContactPager
                if emContact[0].emContactWork != "":
                    emContactInfo += "<br/>Work: " + emContact[0].emContactWork
                if emContact[0].emContactCell != "":
                    emContactInfo += "<br/>Cell: " + emContact[0].emContactCell
                emContacts.append(emContactInfo)
            #Get the list of current class time slots.
            classTimeSlots = getClassTimeSlots(semester)
            #Zip all the required information into one big tuple of lists.
            studentInfoGridInfo = zip(studentIDs, studentNames, studentClasses, studentNotes, studentAddresses, emContacts, studentSpecialInstructions)
            
            self.response.headers['Content-Type'] = 'text/html'
            path = os.path.join(os.path.dirname(__file__), 'studentInfoGrid.html')
            self.response.out.write(template.render(path, {'semester':semester.upper(), 'campus':campus.upper(), 'classTimeSlots' : classTimeSlots,
                                                           'studentData' : studentInfoGridInfo}))
        except Exception, e:
            reportError(self, "Sorry. There's been an error: " + str(e))

