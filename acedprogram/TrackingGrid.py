__author__ = 'rdasxy'

from universalImports import *
from aadbdef import *
from authHelper import *

################################################################################################################################################################
#Screen presented to the view student registration tracking grid for the current semester and campus.
class TrackingGrid(webapp.RequestHandler):
    try:    
        def get(self):
            #If user currently logged in, show tracking grid.
            currentlyLoggedInUser = securelyProceed(self)
            if currentlyLoggedInUser:
                campus, semester = getCampusAndSemester(self)
                timeSlots = getClassTimeSlots(semester)
                trackingGridData = []
                totalRegistrations = 0
                availableSpaces = 0
                for timeSlot in timeSlots:
                    classesQuery = db.GqlQuery("SELECT * FROM Class WHERE classTimeOffered='" + timeSlot + "' AND semester='" + semester + "'")
                    classes = classesQuery.fetch(500)
                    classesData = []
                    for currentClass in classes:
                        if campus == 'lv':
                            totalRegistrations += currentClass.studentCountLV
                            classesData.append((currentClass.name, currentClass.studentCountLV, currentClass.studentLimit))
                        elif campus == 'br':
                            totalRegistrations += currentClass.studentCountBR
                            classesData.append((currentClass.name, currentClass.studentCountBR, currentClass.studentLimit))
                        elif campus == 'umkc':
                            totalRegistrations += currentClass.studentCountUMKC
                            classesData.append((currentClass.name, currentClass.studentCountUMKC, currentClass.studentLimit))
                        availableSpaces += currentClass.studentLimit
                    trackingGridData.append((timeSlot, classesData))
                spacesFilled = round(float(totalRegistrations)/float(availableSpaces) * 100, 2)
    
                studentsQuery = db.GqlQuery("SELECT * FROM Enrollment WHERE campus = '" + campus.upper() + "'")
                totalStudents = studentsQuery.count()
    
                self.response.headers['Content-Type'] = 'text/html'
                path = os.path.join(os.path.dirname(__file__), 'trackingGrid.html')
                self.response.out.write(template.render(path, {'campus' : campus, 'semester' : semester,
                                                               'trackingGridData' : trackingGridData, 'total' : totalRegistrations,
                                                               'available' : availableSpaces, 'percent' : spacesFilled, 'totalStudentCount' : totalStudents}))
    except Exception, e:
        reportError(self, "Sorry. There's been an error: " + str(e))