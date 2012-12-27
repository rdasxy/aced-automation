__author__ = 'rdasxy'

from universalImports import *
from aadbdef import *
from classRegistrations import *
from authHelper import *

################################################################################################################################################################
#Screen presented to the user to edit student registrations - classes and campus only.
class EditEnrollment(webapp.RequestHandler):
    #Present the screen showing currently signed up classes with the option to change.
    def get(self):
        try:    
            #If user currently logged in, show new registrations.
            currentlyLoggedInUser = securelyProceed(self)
            if currentlyLoggedInUser:
                studentID = self.request.get('ID')
                enrollmentsQuery = db.GqlQuery("SELECT * FROM Enrollment WHERE studentID = '" + studentID + "'")
                enrollmentResult = enrollmentsQuery.fetch(1)
                if enrollmentResult:
                    enrollment = enrollmentResult[0]
    
                    studentsQuery = db.GqlQuery("SELECT * FROM Student WHERE uniqueID='" + studentID + "'")
                    studentsResult = studentsQuery.fetch(1)
                    if studentsResult:
                        student = studentsResult[0]
    
                    studentClassFirstPriorities = enrollment.classFirstPreferences.split(',')
    
                    #Get the list of classes for the current semester.
                    currentClassesList = getCurrentClassesList() #(type, semesterName, semesterCode, classListAndTimeSlots)
                    classListAndTime = currentClassesList[3]
                    #Pick out just the names of the classes.
                    classList = []
                    for className in classListAndTime:
                        classList.append(className[0])
    
                    #Zip the list of classes the student signed up for and the list of available choices into a list of tuples.
                    classes = zip (studentClassFirstPriorities, classList)
    
                    self.response.headers['Content-Type'] = 'text/html'
                    path = os.path.join(os.path.dirname(__file__), 'editEnrollment.html')
                    self.response.out.write(template.render(path, {'studentID':studentID, 'studentName':student.name,
                                                                   'secondPreferences' : enrollment.classSecondPreferences,
                                                                   'firstPreferences' : enrollment.classFirstPreferences,
                                                                   'semester' : enrollment.semesterCode, 'class_list' : classes,
                                                                   'campus' : enrollment.campus}))
        except Exception, e:
            reportError(self, "Sorry. There's been an error: " + str(e))
    #Process requests for change.
    def post(self):
        try:    
            studentID = self.request.get("studentID")
            firstPreferencesStr = self.request.get("firstPreferences")
            firstPreferences = firstPreferencesStr.split(",")
    
            #Find the enrollment record.
            enrollmentsQuery = db.GqlQuery("SELECT * FROM Enrollment WHERE studentID = '" + studentID + "'")
            enrollmentResult = enrollmentsQuery.fetch(1)
            if enrollmentResult:
                enrollment = enrollmentResult[0]
                #Determine if the campus was changed.
                oldCampus = self.request.get("oldCampus")
                newCampus = self.request.get("newCampus")
                if not (newCampus == "No Change" or oldCampus == newCampus):
                    enrollment.campus = newCampus
                else:
                    newCampus = oldCampus
                #Check for duplicate enrollments.
                enrollmentDuplicatesQuery = db.GqlQuery("SELECT * FROM Enrollment WHERE studentID = '" + enrollment.studentID
                                                        + "' AND campus='" + newCampus + "' AND semesterCode='" + enrollment.semesterCode + "'")
                if enrollmentDuplicatesQuery.count() > 1:
                    self.response.out.write("Error: This student is already signed up for that campus for this semester.")
                    return
                #Calculate any changes in classes.
                classesChosen = []
                classIDs = []
                classFees = 0
                #Get the list of classes for the current semester.
                currentClassesList = getCurrentClassesList() #(type, semesterName, semesterCode, classListAndTimeSlots)
                classListAndTime = currentClassesList[3]
                #Calculate what needs to be changed with the classes.
                for i in range (1, len(classListAndTime) + 1):
                    classSubmitted = self.request.get('class%d1' % i)
                    if (classSubmitted == "No Change" or classSubmitted == firstPreferences[i-1]):
                        classesChosen.append(firstPreferences[i-1])
                        #Update fees if enrollment has already been approved.
                        if enrollment.approved and firstPreferences[i-1] != "None":
                            classQuery = db.GqlQuery("SELECT * FROM Class WHERE name='" + firstPreferences[i-1] + "'")
                            currentClasses = classQuery.fetch(1)
                            currentClass = currentClasses[0]
                            #Update student counts.
                            correctStudentCount = 0
                            if newCampus != oldCampus:
                                if oldCampus == "UMKC":
                                    currentClass.studentCountUMKC -= 1
                                elif oldCampus == "BR":
                                    currentClass.studentCountBR -= 1
                                elif oldCampus == "LV":
                                    currentClass.studentCountLV -= 1
    
                                if newCampus == "UMKC":
                                    currentClass.studentCountUMKC += 1
                                    correctStudentCount = currentClass.studentCountUMKC
                                elif newCampus == "BR":
                                    currentClass.studentCountBR += 1
                                    correctStudentCount = currentClass.studentCountBR
                                elif newCampus == "LV":
                                    currentClass.studentCountLV += 1
                                    correctStudentCount = currentClass.studentCountLV
    
                            if correctStudentCount >= currentClass.studentLimit:
                                self.response.out.write("Note: " + currentClass.name + " is overflowing. ("
                                                        + str(currentClass.studentCount) + "/" + str(currentClass.studentLimit) + ")<br/>")
                            classIDs.append(str(currentClass.classID))
                            classFees += currentClass.classFee
                    elif (classSubmitted == "No class for this time"):
                        classesChosen.append("None")
                        #Update class record if enrollment has already been approved.
                        if enrollment.approved and firstPreferences[i-1] != "None":
                            classQuery = db.GqlQuery("SELECT * FROM Class WHERE name='" + firstPreferences[i-1] + "'")
                            currentClasses = classQuery.fetch(1)
                            currentClass = currentClasses[0]
                            #Update student counts.
                            currentClass.studentCount -= 1
                            correctStudentCount = 0
                            if oldCampus == "UMKC":
                                currentClass.studentCountUMKC -= 1
                                correctStudentCount = currentClass.studentCountUMKC
                            elif oldCampus == "BR":
                                currentClass.studentCountBR -= 1
                                correctStudentCount = currentClass.studentCountBR
                            elif oldCampus == "LV":
                                currentClass.studentCountLV -= 1
                                correctStudentCount = currentClass.studentCountLV
    
                            if correctStudentCount >= currentClass.studentLimit:
                                self.response.out.write("Note: " + currentClass.name + " is overflowing. ("
                                                        + str(currentClass.studentCount) + "/" + str(currentClass.studentLimit) + ")<br/>")
                            classIDs.append(str(0))
                            currentClass.put()
                    else:
                        classesChosen.append(classSubmitted)
                        if enrollment.approved:
                            #Update class record for new class.
                            classQuery = db.GqlQuery("SELECT * FROM Class WHERE name='" + classSubmitted + "'")
                            currentClasses = classQuery.fetch(1)
                            currentClass = currentClasses[0]
                            #Update student counts for new class.
                            currentClass.studentCount += 1
                            correctStudentCount = 0
                            if newCampus == "UMKC":
                                currentClass.studentCountUMKC += 1
                                correctStudentCount = currentClass.studentCountUMKC
                            elif newCampus == "BR":
                                currentClass.studentCountBR += 1
                                correctStudentCount = currentClass.studentCountBR
                            elif newCampus == "LV":
                                currentClass.studentCountLV += 1
                                correctStudentCount = currentClass.studentCountLV
                            if correctStudentCount >= currentClass.studentLimit:
                                self.response.out.write("Note: " + currentClass.name + " is overflowing. ("
                                                        + str(currentClass.studentCount) + "/" + str(currentClass.studentLimit) + ")<br/>")
                            classIDs.append(str(currentClass.classID))
                            classFees += currentClass.classFee
                            currentClass.put()
                            #Update class record for old class.
                            if firstPreferences[i-1] != "None":
                                classQuery = db.GqlQuery("SELECT * FROM Class WHERE name='" + firstPreferences[i-1] + "'")
                                currentClasses = classQuery.fetch(1)
                                currentClass = currentClasses[0]
                                correctStudentCount = 0
                                if oldCampus == "UMKC":
                                    currentClass.studentCountUMKC -= 1
                                    correctStudentCount = currentClass.studentCountUMKC
                                elif oldCampus == "BR":
                                    currentClass.studentCountBR -= 1
                                    correctStudentCount = currentClass.studentCountBR
                                elif oldCampus == "LV":
                                    currentClass.studentCountLV -= 1
                                    correctStudentCount = currentClass.studentCountLV
                                currentClass.studentCount -= 1
                                currentClass.put()
                                if correctStudentCount >= currentClass.studentLimit:
                                    self.response.out.write("Note: " + currentClass.name + " is overflowing. ("
                                                            + str(currentClass.studentCount) + "/" + str(currentClass.studentLimit) + ")<br/>")
    
                enrollment.classIDs = ",".join(classIDs)
                enrollment.notes = "Fees Owed = $" + str(classFees)
                #Update the classes in the enrollment record.
                enrollment.classFirstPreferences = ",".join(classesChosen)
                enrollment.put()
                self.response.out.write("Your changes have been successfully updated.")
        except Exception, e:
            reportError(self, "Sorry. There's been an error: " + str(e))