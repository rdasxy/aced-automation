__author__ = 'rdasxy'

from universalImports import *
from aadbdef import *
from authHelper import *

################################################################################################################################################################
#Screen presented to the view nametags for the current semester and campus.
class Nametags(webapp.RequestHandler):
    def get(self):
        try:    
            #If user currently logged in, show nametags.
            currentlyLoggedInUser = securelyProceed(self)
            if currentlyLoggedInUser:
                #If an accept request was found, accept the student.
                campus, semester = getCampusAndSemester(self)
                enrollmentsQuery = db.GqlQuery("SELECT * FROM Enrollment WHERE campus='" + campus.upper() + "' AND semesterCode='" + semester + "' AND approved=True")
                enrollmentsRecords = enrollmentsQuery.fetch(500)
    
                studentNames = []
                studentIDs = []
                studentInfo = {}
                for enrollment in enrollmentsRecords:
                    studentsQuery = db.GqlQuery("SELECT * FROM Student WHERE uniqueID='" + enrollment.studentID + "'")
                    student = studentsQuery.fetch(1)[0]
                    studentNames.append(student.name)
                    studentIDs.append(student.uniqueID)
    
                    studentClassesQuery = db.GqlQuery("SELECT * FROM Enrollment WHERE studentID='" + student.uniqueID + "'")
                    studentClassIDsStr = studentClassesQuery.fetch(1)[0].classIDs
                    classIDs = studentClassIDsStr.split(",")
                    studentClassNames = []
                    
                    if len(classIDs) > 0:
                        logging.error("ClassIDS = " + str(classIDs))
                        for classID in classIDs:
                            if classID != 'None':
                                classNamesQuery = db.GqlQuery("SELECT * FROM Class WHERE classID=" + classID)
                                className = classNamesQuery.fetch(1)[0].name
                                classTimeOffered = classNamesQuery.fetch(1)[0].classTimeOffered
                                studentClassNames.append(classTimeOffered + ":&nbsp;&nbsp;&nbsp;&nbsp;" + className)
                            else:
                                studentClassNames.append ("None")
                        studentInfo[student.name] = studentClassNames
                    else:
                        studentInfo[student.name] = "       "
    
                nametagOutput = []
                pageBreakList = [i for i in range(4,5500,6)]
                if (len(studentInfo)%2) != 0:
                    studentInfo["PlaceHolder:Ignore"] = ["This was added because there were an odd number of nametags. Please ignore."]
                for i in range(0,len(studentInfo),2):
                    if i in pageBreakList:
                        nametagOutput.append((studentInfo.keys()[i],studentInfo.keys()[i+1],studentInfo[studentInfo.keys()[i]], studentInfo[studentInfo.keys()[i+1]], "page"))
                    else:
                        nametagOutput.append((studentInfo.keys()[i],studentInfo.keys()[i+1],studentInfo[studentInfo.keys()[i]], studentInfo[studentInfo.keys()[i+1]]))
    
                self.response.headers['Content-Type'] = 'text/html'
                path = os.path.join(os.path.dirname(__file__), 'nametag.html')
                self.response.out.write(template.render(path, {'nametagOutput' : nametagOutput}))
        except Exception, e:
            reportError(self, "Sorry. There's been an error: " + str(e))
