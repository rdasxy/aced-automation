__author__ = 'rdasxy'

from universalImports import *
from aadbdef import *
from authHelper import *

################################################################################################################################################################
#Shows student class schedule for the required semester.
class ClassSchedule(webapp.RequestHandler):
    def get(self):
        try:    
            studentID = self.request.get('ID')
            campus, semester = getCampusAndSemester(self)
            #Get the list of enrollments for the current semester.
            enrollmentQuery = db.GqlQuery("SELECT * FROM Enrollment WHERE semesterCode = '" + semester + "' AND campus = '" + campus.upper() + "' AND studentID='" + studentID + "'")
            enrollment = enrollmentQuery.fetch(1)[0]
            #Get the list of classes the student signed up for.
            studentClasses = enrollment.classFirstPreferences.split(',')
            #Get the list of current class time slots.
            classTimeSlots = getClassTimeSlots(semester)
            #Zip all the required information into one big tuple of lists.
            classScheduleData = zip(studentClasses, classTimeSlots)
            #Get the student's name.
            studentsQuery = db.GqlQuery("SELECT * FROM Student WHERE uniqueID='" + studentID + "'")
            studentName = studentsQuery.fetch(1)[0].name
            #Get the full name of the semester.
            semesterQuery = db.GqlQuery("SELECT * FROM Semester WHERE code='" + semester + "'")
            semesterName = semesterQuery.fetch(1)[0].session + " " + str(semesterQuery.fetch(1)[0].year)
            #Get all the information that goes with class schedules.
            classScheduleQuery = db.GqlQuery("SELECT * FROM ClassScheduleInformation WHERE semesterID='" + semester + "' AND campus='" + campus.upper() + "'")
            classScheduleInfo = classScheduleQuery.fetch(1)[0]
            classBeginData = classScheduleInfo.classesBeginNotes
            classEndData = classScheduleInfo.classesEndNotes
            arrivalNotes = classScheduleInfo.arrivalNotes
            attendancePolicy = classScheduleInfo.attendancePolicy
            location = classScheduleInfo.location
            directions = classScheduleInfo.directions
            problemNotice = classScheduleInfo.problemNotice
            building = classScheduleInfo.building
            #Display the web page.
            self.response.headers['Content-Type'] = 'text/html'
            path = os.path.join(os.path.dirname(__file__), 'classSchedule.html')
            self.response.out.write(template.render(path, {'studentID': studentID, 'semester':semesterName, 'campus':campus.upper(),
                                                           'classScheduleData' : classScheduleData, 'studentName' : studentName,
                                                           'classBeginData' : classBeginData, 'classEndData' : classEndData,
                                                           'arrivalNotes' : arrivalNotes, 'attendancePolicy' : attendancePolicy,
                                                           'location' : location, 'directions' : directions,
                                                           'problemNotice' : problemNotice, 'building' : building}))
        except Exception, e:
            reportError(self, "Sorry. There's been an error: " + str(e))

