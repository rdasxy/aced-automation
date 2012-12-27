__author__ = 'rdasxy'

from universalImports import *
from aadbdef import *
from authHelper import *
################################################################################################################################################################
#Allows the admin to add a class.
class AddClass(webapp.RequestHandler):
    def get(self):
        try:
            currentlyLoggedInUser = securelyProceed(self)
            if currentlyLoggedInUser:
                #Get a list of all semesters in the system.
                semesterQuery = db.GqlQuery("SELECT * FROM Semester")
                semestersList = semesterQuery.fetch(500)
                semesterNames = [semester.session + " " + str(semester.year) for semester in semestersList]
                semesterCodes = [semester.code for semester in semestersList]
                semesters = zip(semesterCodes, semesterNames)
                #Display the page.
                self.response.headers['Content-Type'] = 'text/html'
                path = os.path.join(os.path.dirname(__file__), 'addclass.html')
                self.response.out.write(template.render(path, {'semesters' : semesters}))
        except Exception, e:
            reportError(self, "Sorry. There's been an error: " + str(e))
    def post(self):
        try:
            className = escapeString(self.request.get('className'))
            teacher = escapeString(self.request.get('teacher'))
            tA = escapeString(self.request.get('tA'))
            studentLimit = escapeString(self.request.get('studentLimit'))
            classFees = escapeString(self.request.get('classFees'))
            timeSlot = escapeString(self.request.get('timeslot'))
            semester = escapeString(self.request.get('semester'))
            BR = escapeString(self.request.get('BR'))
            LV = escapeString(self.request.get('LV'))
            UMKC = escapeString(self.request.get('UMKC'))
            #Make sure at least one campus has been selected.
            if not BR or not UMKC or not LV:
                self.response.out.write("Please pick a campus.")
                return
            #Make sure class name is unique.
            classQuery = db.GqlQuery("SELECT * FROM Class WHERE name='" + className + "'")
            if classQuery.count() >= 1:
                self.response.out.write("Class name has been used before. Class names need to be unique.")
                return
            #Create a new class.
            newClass = Class()
            if BR:
                newClass.name = '*' + className
                newClass.campuses = "br"
                if UMKC:
                    newClass.campuses += ",umkc"
                if LV:
                    newClass.campuses += ",lv"
            else:
                newClass.name = className
                if UMKC:
                    newClass.campuses += "umkc"
                if LV:
                    newClass.campuses += ",lv"
            newClass.teacherName = teacher
            newClass.taNames = tA
            newClass.studentLimit = int(studentLimit)
            newClass.classFee = int(classFees)
            newClass.semester = semester
            newClass.studentCount = 0
            newClass.studentCountUMKC = 0
            newClass.studentCountBR = 0
            newClass.studentCountLV = 0
            #Assign a class ID.
            countersQuery = db.GqlQuery("SELECT * FROM Counter")
            counter = countersQuery.fetch(1)[0]
            counter.classCount += 1
            newClass.classID = counter.classCount
            #Assign class times.
            newClass.classTimeSlot = int(timeSlot)
            if int(timeSlot) == 1:
                newClass.classTimeOffered = "9:00a.m. - 10:00a.m."
            elif int(timeSlot) == 2:
                newClass.classTimeOffered = "10:10a.m. - 11:10a.m."
            elif int(timeSlot) == 3:
                newClass.classTimeOffered = "11:20a.m. - 12:35p.m."
            #Assign semester code.
            currentSemesterQuery = db.GqlQuery("SELECT * FROM CurrentSemester")
            currentSemesterID = currentSemesterQuery.fetch(1)[0].code
            newClass.semester = currentSemesterID
            #Assign class days.
            semestersQuery = db.GqlQuery("SELECT * FROM Semester WHERE code='" + currentSemesterID + "'")
            newClass.classDays = semestersQuery.fetch(1)[0].classDays
            #Add class rosters for all campuses.
            if UMKC:
                attendance = ClassRoster()
                attendance.forClassID = newClass.classID
                attendance.attendance = "None"
                attendance.campus = "umkc"
                attendance.put()
            if BR:
                attendance = ClassRoster()
                attendance.forClassID = newClass.classID
                attendance.attendance = "None"
                attendance.campus = "br"
                attendance.put()
            if LV:
                attendance = ClassRoster()
                attendance.forClassID = newClass.classID
                attendance.attendance = "None"
                attendance.campus = "lv"
                attendance.put()
            newClass.put()
            counter.put()
            self.response.out.write("You have successfully added class: " + className)
        except Exception, e:
            reportError(self, "Sorry. There's been an error: " + str(e))

        


