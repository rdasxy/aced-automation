__author__ = 'rdasxy'

from universalImports import *
from aadbdef import *
from authHelper import *
################################################################################################################################################################
#Attendance Roster/Student Check-in for the specified semester.
class StudentCheckin(webapp.RequestHandler):
    #Displays the attendance roster for the specified semester.
    def get(self):
        try:    
            currentlyLoggedInUser = securelyProceed(self)
            if currentlyLoggedInUser:
                #Get current campus and semester.
                campus, semester = getCampusAndSemester(self)
                #Get the full name of the semester.
                semesterQuery = db.GqlQuery("SELECT * FROM Semester WHERE code='" + semester + "'")
                semesterName = semesterQuery.fetch(1)[0].session + " " + str(semesterQuery.fetch(1)[0].year)
                semesterDaysList = semesterQuery.fetch(1)[0].classDays.split(",")
                daysCount = len(semesterDaysList)
                #Create the list of student names, and build a dictionary mapping student names with their IDs.
                studentNames = []
                studentNamesAndIDs = {}
                enrollmentsQuery = db.GqlQuery("SELECT * FROM Enrollment WHERE campus='" + campus.upper() + "' AND semesterCode='" + semester + "' AND approved=True")
                enrollments = enrollmentsQuery.fetch(500)
                for enrollment in enrollments:
                    studentsQuery = db.GqlQuery("SELECT * FROM Student WHERE uniqueID='" + enrollment.studentID + "'")
                    studentNames.append(studentsQuery.fetch(1)[0].name)
                    studentNamesAndIDs[studentsQuery.fetch(1)[0].name] = enrollment.studentID
                #Create the list of student attendances.
                attendanceQuery = db.GqlQuery("SELECT * FROM SemesterRoster WHERE forSemesterID='" + semester + "' AND campus='" + campus + "'")
                #Get the overall attendance.
                semesterAttendance = attendanceQuery.fetch(1)[0]
                semesterAttendanceStr = semesterAttendance.attendance
                #'AttendanceByStudent' is used to build each student's attendance as a dictionary.
                attendanceByStudent = {}
                #If the class's attendance list is empty, build it.
                #e.g. {'studentName':[[0,0],[0,0],[0,0]]}
                if semesterAttendanceStr == "None":
                    for student in studentNames:
                        attendanceByStudent[student] = []
                        for i in range(daysCount):
                            attendanceByStudent[student].append([0,0])
                    #Commit to datastore.
                    semesterAttendance.attendance = json.dumps(attendanceByStudent)
                    semesterAttendance.put()
                #If the class's attendance list is non empty, use it.
                else:
                    attendanceByStudent = json.loads(semesterAttendanceStr)
                    #Calculate any changes in the class's students.
                    removedStudents = [studentName for studentName in attendanceByStudent.keys() if studentName not in studentNames]
                    #Remove any students that have been removed from the semester.
                    for removedStudent in removedStudents:
                        del attendanceByStudent[removedStudent]
                    newStudents = [studentName for studentName in studentNames if studentName not in attendanceByStudent.keys()]
                    #Add students with "Not Present" values that have been added to the semester.
                    for newStudent in newStudents:
                        attendanceByStudent[newStudent] = []
                        for i in range(daysCount):
                            attendanceByStudent[newStudent].append([0,0])
                    #Commit to datastore.
                    semesterAttendance.attendance = json.dumps(attendanceByStudent)
                    semesterAttendance.put()
    
                #Create the data structure for the view.
                attendanceByStudentForView = {}
                for student, attendanceAll in attendanceByStudent.items():
                    tempHTMLAttendanceList = []
                    studentAttendanceCount = 0
                    for checkInCheckOut in attendanceAll:
                        if checkInCheckOut[0] == 0:
                            tempHTMLAttendanceList.append("<input type=checkbox name='" + studentNamesAndIDs[student] + "attendancecheckin" + str(studentAttendanceCount) + "'/>In")
                        else:
                            tempHTMLAttendanceList.append("<input type=checkbox name='" + studentNamesAndIDs[student] + "attendancecheckin" + str(studentAttendanceCount) + "' checked/>In")
                        if checkInCheckOut[1] == 0:
                            tempHTMLAttendanceList.append("<input type=checkbox name='" + studentNamesAndIDs[student] + "attendancecheckout" + str(studentAttendanceCount) + "'/>Out")
                        else:
                            tempHTMLAttendanceList.append("<input type=checkbox name='" + studentNamesAndIDs[student] + "attendancecheckout" + str(studentAttendanceCount) + "' checked/>Out")
                        studentAttendanceCount += 1
                    attendanceByStudentForView[student] = tempHTMLAttendanceList
    
                self.response.headers['Content-Type'] = 'text/html'
                path = os.path.join(os.path.dirname(__file__), 'studentCheckIn.html')
                self.response.out.write(template.render(path, {'campus' : campus.upper(), 'semesterName' : semesterName,
                                                               'semesterDaysList' : semesterDaysList, 'attendanceByStudent' : attendanceByStudentForView}))
        except Exception, e:
            reportError(self, "Sorry. There's been an error: " + str(e))
            
    def post(self):
        try:    
            currentlyLoggedInUser = securelyProceed(self)
            if currentlyLoggedInUser:
                 #Get current campus and semester.
                campus, semester = getCampusAndSemester(self)
                #Create the list of student names, and build a dictionary mapping student names with their IDs.
                studentNames = []
                studentNamesAndIDs = {}
                enrollmentsQuery = db.GqlQuery("SELECT * FROM Enrollment WHERE campus='" + campus.upper() + "' AND semesterCode='" + semester + "' AND approved=True")
                enrollments = enrollmentsQuery.fetch(500)
                for enrollment in enrollments:
                    studentsQuery = db.GqlQuery("SELECT * FROM Student WHERE uniqueID='" + enrollment.studentID + "'")
                    studentNames.append(studentsQuery.fetch(1)[0].name)
                    studentNamesAndIDs[studentsQuery.fetch(1)[0].name] = enrollment.studentID
                #Create the list of student attendances.
                attendanceQuery = db.GqlQuery("SELECT * FROM SemesterRoster WHERE forSemesterID='" + semester + "' AND campus='" + campus + "'")
                #Get the overall attendance.
                semesterAttendance = attendanceQuery.fetch(1)[0]
                semesterAttendanceStr = semesterAttendance.attendance
                attendanceByStudent = json.loads(semesterAttendanceStr)
                #Calculate any changes made to the student's attendance.
                for student, attendanceAll in attendanceByStudent.items():
                    for i in range(len(attendanceAll)):
                        newCheckin = self.request.get(studentNamesAndIDs[student] + "attendancecheckin" + str(i))
                        newCheckout = self.request.get(studentNamesAndIDs[student] + "attendancecheckout" + str(i))
                        if newCheckin:#Student checked in.
                            attendanceByStudent[student][i][0] = 1
                        else: #Student did not check in.
                            attendanceByStudent[student][i][0] = 0
                        if newCheckout:#Student checked out.
                            attendanceByStudent[student][i][1] = 1
                        else:#Student did not check out.
                            attendanceByStudent[student][i][1] = 0
                        logging.error("Receiving item "+ studentNamesAndIDs[student] + "attendance" + str(i) +
                                      "=" + self.request.get(studentNamesAndIDs[student] + "attendance" + str(i)))
                #Commit changes to database.
                semesterAttendance.attendance = json.dumps(attendanceByStudent)
                semesterAttendance.put()
    
                self.response.headers['Content-Type'] = 'text/html'
                self.response.out.write("Your changes to the class roster have been updated.")
        except Exception, e:
            reportError(self, "Sorry. There's been an error: " + str(e))
