__author__ = 'rdasxy'

from universalImports import *
from aadbdef import *
from authHelper import *
################################################################################################################################################################
#Allows the admin to change password for all users.
class AddSemester(webapp.RequestHandler):
    def get(self):
        try:    
            currentlyLoggedInUser = securelyProceed(self)
            if currentlyLoggedInUser:
                #Display the page.
                self.response.headers['Content-Type'] = 'text/html'
                path = os.path.join(os.path.dirname(__file__), 'addsemester.html')
                self.response.out.write(template.render(path, {'classBeginNotes' : "e.g. Class Begin on Saturday March 21, 2011",
                                                               'classEndNotes' : "e.g. Classes End on Sunday March 22 2011, followed by a reception",
                                                               'arrivalNotes' : "e.g. 15 minutes prior to class",
                                                               'attendancePolicy' : "e.g. It is your responsibility to come to class and be on time. Tardiness will be addressed on an individual basis",
                                                               'location' : 'e.g. UMKC Campus',
                                                               'direction' : 'e.g. Royall Hall: 52nd St and Rockhill Road (800 E. 52nd St is the exact address). Please enter Royall Hall and enter the second floor.',
                                                               'building' : 'e.g. Park in the garage across from Royall Hall. Enter on 52nd St. No permit is required on Saturdays.',
                                                               'problemNotice' : 'e.g. If you have problems or questions during the week, please call the ACED office at 813-235-1754. On Saturdays call Phani at 123-456-7890'}))
        except Exception, e:
            reportError(self, "Sorry. There's been an error: " + str(e))                
    def post(self):
        try:
            semesterName = escapeString(self.request.get('semester'))
            year = escapeString(self.request.get('year'))
            classDays = escapeString(self.request.get('meetingDays'))
            if year == "" or semesterName == "" or classDays == "":
                raise Exception
            year = int(year)
            #Calculate the code.
            prefix = ""
            if semesterName == "Spring":
                prefix = "sp"
            elif semesterName == "Fall":
                prefix = "fa"
            elif semesterName == "Summer":
                prefix = "su"
            else:
                raise Exception
            semesterCode = prefix + str(year)
            #Make sure code is unique.
            semestersQuery = db.GqlQuery("SELECT * FROM Semester WHERE code='" + semesterCode + "'")
            if semestersQuery.count() >= 1:
                raise Exception
            #Get the class schedule notes for UMKC.
            classBeginNotes = escapeString(self.request.get('classBeginNotesUMKC'))
            classEndNotes = escapeString(self.request.get('classEndNotesUMKC'))
            arrivalNotes = escapeString(self.request.get('arrivalNotesUMKC'))
            attendancePolicy = escapeString(self.request.get('attendancePolicyUMKC'))
            location = escapeString(self.request.get('locationUMKC'))
            directions = escapeString(self.request.get('directionUMKC'))
            building = escapeString(self.request.get('buildingUMKC'))
            problemNotice = escapeString(self.request.get('problemNoticeUMKC'))
            #Save the class schedule notes for UMKC.
            classScheduleNotes = ClassScheduleInformation()
            classScheduleNotes.classesBeginNotes = classBeginNotes
            classScheduleNotes.classesEndNotes = classEndNotes
            classScheduleNotes.arrivalNotes = arrivalNotes
            classScheduleNotes.location = location
            classScheduleNotes.attendancePolicy = attendancePolicy
            classScheduleNotes.directions = directions
            classScheduleNotes.building = building
            classScheduleNotes.semesterID = semesterCode
            classScheduleNotes.problemNotice = problemNotice
            classScheduleNotes.campus = "UMKC"
            classScheduleNotes.put()
            #Get the class schedule notes for MCC-Longview.
            classBeginNotes = escapeString(self.request.get('classBeginNotesLongview'))
            classEndNotes = escapeString(self.request.get('classEndNotesLongview'))
            arrivalNotes = escapeString(self.request.get('arrivalNotesLongview'))
            attendancePolicy = escapeString(self.request.get('attendancePolicyLongview'))
            location = escapeString(self.request.get('locationLongview'))
            directions = escapeString(self.request.get('directionLongview'))
            building = escapeString(self.request.get('buildingLongview'))
            problemNotice = escapeString(self.request.get('problemNoticeLongview'))
            #Save the class schedule notes for MCC-Longview.
            classScheduleNotes = ClassScheduleInformation()
            classScheduleNotes.classesBeginNotes = classBeginNotes
            classScheduleNotes.classesEndNotes = classEndNotes
            classScheduleNotes.arrivalNotes = arrivalNotes
            classScheduleNotes.location = location
            classScheduleNotes.attendancePolicy = attendancePolicy
            classScheduleNotes.directions = directions
            classScheduleNotes.building = building
            classScheduleNotes.semesterID = semesterCode
            classScheduleNotes.problemNotice = problemNotice
            classScheduleNotes.campus = "LV"
            classScheduleNotes.put()
            #Get the class schedule notes for MCC-BlueRiver.
            classBeginNotes = escapeString(self.request.get('classBeginNotesBR'))
            classEndNotes = escapeString(self.request.get('classEndNotesBR'))
            arrivalNotes = escapeString(self.request.get('arrivalNotesBR'))
            attendancePolicy = escapeString(self.request.get('attendancePolicyBR'))
            location = escapeString(self.request.get('locationBR'))
            directions = escapeString(self.request.get('directionBR'))
            building = escapeString(self.request.get('buildingBR'))
            problemNotice = escapeString(self.request.get('problemNoticeBR'))
            #Save the class schedule notes for MCC-BlueRiver.
            classScheduleNotes = ClassScheduleInformation()
            classScheduleNotes.classesBeginNotes = classBeginNotes
            classScheduleNotes.classesEndNotes = classEndNotes
            classScheduleNotes.arrivalNotes = arrivalNotes
            classScheduleNotes.location = location
            classScheduleNotes.attendancePolicy = attendancePolicy
            classScheduleNotes.directions = directions
            classScheduleNotes.building = building
            classScheduleNotes.semesterID = semesterCode
            classScheduleNotes.problemNotice = problemNotice
            classScheduleNotes.campus = "BR"
            classScheduleNotes.put()
            #Add to datastore.
            semester = Semester()
            semester.session = semesterName
            semester.year = year
            semester.classDays = classDays
            semester.code = semesterCode
            semester.put()
            #Add a semester roster with none.
            semesterRoster = SemesterRoster()
            semesterRoster.forSemesterID = semesterCode
            semesterRoster.attendance = "None"
            semesterRoster.campus = "lv"
            semesterRoster.put()
            semesterRoster = SemesterRoster()
            semesterRoster.forSemesterID = semesterCode
            semesterRoster.attendance = "None"
            semesterRoster.campus = "br"
            semesterRoster.put()
            semesterRoster = SemesterRoster()
            semesterRoster.forSemesterID = semesterCode
            semesterRoster.attendance = "None"
            semesterRoster.campus = "umkc"
            semesterRoster.put()
            self.response.out.write("Successfully added " + semesterCode + "!<br/>")
        except:
            reportError(self, "Invalid input. Please check and try again.")















