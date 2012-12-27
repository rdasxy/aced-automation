__author__ = 'rdasxy'

from universalImports import *
from aadbdef import *
from authHelper import *
################################################################################################################################################################
#Shows list of classes for the current semester.
class ClassList(webapp.RequestHandler):
    def get(self):
        try:
            #If user currently logged in, show the list of current courses.
            currentlyLoggedInUser = securelyProceed(self)
            if currentlyLoggedInUser:
                campus, semester = getCampusAndSemester(self)
                classesQuery = db.GqlQuery("SELECT * FROM Class WHERE semester='" + semester + "' ORDER BY classTimeSlot")
                classes = classesQuery.fetch(500)
                classNames = [classItem.name for classItem in classes]
                classTimeSlots = [classItem.classTimeOffered for classItem in classes]
                classIDs = [classItem.classID for classItem in classes]
                classListData = zip(classNames, classTimeSlots, classIDs)
                self.response.headers['Content-Type'] = 'text/html'
                path = os.path.join(os.path.dirname(__file__), 'classList.html')
                self.response.out.write(template.render(path, {'classListData' : classListData}))
        except Exception, e:
            reportError(self, "Sorry. There's been an error: " + str(e))
################################################################################################################################################################
#Class roster for the specified class.
class ClassRosters(webapp.RequestHandler):
    #Displays the class roster for the specified class.
    def get(self):
        try:
            currentlyLoggedInUser = securelyProceed(self)
            if currentlyLoggedInUser:
                #Get current class ID, campus and semester.
                classID = self.request.get('ID')
                campus, semester = getCampusAndSemester(self)
                #Get the class asked for and get the number of times it meets, along with other information.
                classesQuery = db.GqlQuery("SELECT * FROM Class WHERE classID = " + str(classID))
                classItem = classesQuery.fetch(1)[0]
                classDaysList = classItem.classDays.split(',')
                daysCount = len(classDaysList)
                classTeacher = classItem.teacherName
                classTAs = classItem.taNames
                classTime = classItem.classTimeOffered
                className = classItem.name
                #Get the full name of the semester.
                semesterQuery = db.GqlQuery("SELECT * FROM Semester WHERE code='" + semester + "'")
                semesterName = semesterQuery.fetch(1)[0].session + " " + str(semesterQuery.fetch(1)[0].year)
                #Create the list of student names, and build a dictionary mapping student names with their IDs.
                studentNames = []
                studentNamesAndIDs = {}
                enrollmentsQuery = db.GqlQuery("SELECT * FROM Enrollment WHERE campus='" + campus.upper() + "' AND semesterCode='" + semester + "' AND approved=True")
                enrollments = enrollmentsQuery.fetch(500)
                for enrollment in enrollments:
                    enrolledClasses = enrollment.classIDs.split(",")
                    if classID in enrolledClasses:
                        studentsQuery = db.GqlQuery("SELECT * FROM Student WHERE uniqueID='" + enrollment.studentID + "'")
                        studentNames.append(studentsQuery.fetch(1)[0].name)
                        studentNamesAndIDs[studentsQuery.fetch(1)[0].name] = enrollment.studentID
                #Create the list of student attendances.
                attendanceQuery = db.GqlQuery("SELECT * FROM ClassRoster WHERE forClassID=" + str(classID) + " AND campus='" + campus + "'")
                #Get the overall attendance.
                classAttendance = attendanceQuery.fetch(1)[0]
                classAttendanceStr = classAttendance.attendance
                #'AttendanceByStudent' is used to build each student's attendance as a dictionary.
                attendanceByStudent = {}
                #If the class's attendance list is empty, build it.
                #e.g. {'studentName':[0,0,0]}
                if classAttendanceStr == "None":
                    for student in studentNames:
                        attendanceByStudent[student] = []
                        for i in range(daysCount):
                            attendanceByStudent[student].append(0)
                    #Commit to datastore.
                    classAttendance.attendance = json.dumps(attendanceByStudent)
                    classAttendance.put()
                #If the class's attendance list is non empty, use it.
                else:
                    attendanceByStudent = json.loads(classAttendanceStr)
                    #Calculate any changes in the class's students.
                    removedStudents = [studentName for studentName in attendanceByStudent.keys() if studentName not in studentNames]
                    #Remove any students that have been removed from the class.
                    for removedStudent in removedStudents:
                        del attendanceByStudent[removedStudent]
                    newStudents = [studentName for studentName in studentNames if studentName not in attendanceByStudent.keys()]
                    #Add students with "Not Present" values that have been added to the class.
                    for newStudent in newStudents:
                        attendanceByStudent[newStudent] = []
                        for i in range(daysCount):
                            attendanceByStudent[newStudent].append(0)
                    #Commit to datastore.
                    classAttendance.attendance = json.dumps(attendanceByStudent)
                    classAttendance.put()
    
                #Create the data structure for the view.
                attendanceByStudentForView = {}
                for student, attendanceAll in attendanceByStudent.items():
                    tempHTMLAttendanceList = []
                    studentAttendanceCount = 0
                    for attendance in attendanceAll:
                        if attendance == 0:
                            tempHTMLAttendanceList.append("<input type=checkbox name='" + studentNamesAndIDs[student] + "attendance" + str(studentAttendanceCount) + "'/>Yes")
                        else:
                            tempHTMLAttendanceList.append("<input type=checkbox name='" + studentNamesAndIDs[student] + "attendance" + str(studentAttendanceCount) + "' checked/>Yes")
                        studentAttendanceCount += 1
                    attendanceByStudentForView[student] = tempHTMLAttendanceList
    
                self.response.headers['Content-Type'] = 'text/html'
                path = os.path.join(os.path.dirname(__file__), 'classRoster.html')
                self.response.out.write(template.render(path, {'classID' : classID,'classTeacher' : classTeacher,
                                                               'classTAs' : classTAs, 'classTime' : classTime, 'campus' : campus.upper(),
                                                               'className' : className, 'semesterName' : semesterName,
                                                               'classDaysList' : classDaysList, 'attendanceByStudent' : attendanceByStudentForView}))
        except Exception, e:
            reportError(self, "Sorry. There's been an error: " + str(e))        
    def post(self):
        try:    
            currentlyLoggedInUser = securelyProceed(self)
            if currentlyLoggedInUser:
                #Get current class ID, campus and semester.
                classID = self.request.get('classID')
                campus, semester = getCampusAndSemester(self)
                #Create the list of student names, and build a dictionary mapping student names with their IDs.
                studentNames = []
                studentNamesAndIDs = {}
                enrollmentsQuery = db.GqlQuery("SELECT * FROM Enrollment WHERE campus='" + campus.upper() + "' AND semesterCode='" + semester + "' AND approved=True")
                enrollments = enrollmentsQuery.fetch(500)
                for enrollment in enrollments:
                    enrolledClasses = enrollment.classIDs.split(",")
                    if classID in enrolledClasses:
                        studentsQuery = db.GqlQuery("SELECT * FROM Student WHERE uniqueID='" + enrollment.studentID + "'")
                        studentNames.append(studentsQuery.fetch(1)[0].name)
                        studentNamesAndIDs[studentsQuery.fetch(1)[0].name] = enrollment.studentID
                #Create the list of student attendances.
                attendanceQuery = db.GqlQuery("SELECT * FROM ClassRoster WHERE forClassID=" + str(classID) + " AND campus='" + campus + "'")
                #Get the overall attendance.
                classAttendance = attendanceQuery.fetch(1)[0]
                classAttendanceStr = classAttendance.attendance
                attendanceByStudent = json.loads(classAttendanceStr)
                #Calculate any changes made to the student's attendance.
                for student, attendanceAll in attendanceByStudent.items():
                    for i in range(len(attendanceAll)):
                        newAttendance = self.request.get(studentNamesAndIDs[student] + "attendance" + str(i))
                        if newAttendance:#Student was present
                            attendanceByStudent[student][i] = 1
                        else:#Student was absent.
                            attendanceByStudent[student][i] = 0
                        logging.error("Receiving item "+ studentNamesAndIDs[student] + "attendance" + str(i) +
                                      "=" + self.request.get(studentNamesAndIDs[student] + "attendance" + str(i)))
                #Commit changes to database.
                classAttendance.attendance = json.dumps(attendanceByStudent)
                classAttendance.put()
    
                self.response.headers['Content-Type'] = 'text/html'
                self.response.out.write("Your changes to the class roster have been updated.")
        except Exception, e:
            reportError(self, "Sorry. There's been an error: " + str(e))
