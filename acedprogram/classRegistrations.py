__author__ = 'rdasxy'

from universalImports import *
from aadbdef import *
import random

################################################################################################################################################################
#Returns (Type, Semester Name, Semester Code, {[list of times]:[list of [lists of classes by timeslot]]})
def getCurrentClassesList():
    currentSemester = db.GqlQuery("SELECT * from CurrentSemester")
    type = currentSemester[0].semesterKind
    semesterCode = currentSemester[0].code
    currentClassesList = db.GqlQuery("SELECT * from Class where semester='" + semesterCode + "' ORDER BY classTimeSlot ASC")

    currentSemester = db.GqlQuery("SELECT * from Semester WHERE code = '" + semesterCode + "'")
    semesterName = currentSemester[0].session + " " + str(currentSemester[0].year)

    #Build list of classes, as smaller lists of classes with the same time slot.
    #The first time slot is assumed to be one.
    currentTimeSlot = 1
    classList = []
    tempClassList = []
    for currentClass in currentClassesList:
        if currentClass.classTimeSlot == currentTimeSlot:
            tempClassList.append (unescapeString(currentClass.name))
        else:
            classList.append (tempClassList)
            tempClassList = [unescapeString(currentClass.name)]
            currentTimeSlot = currentClass.classTimeSlot
    classList.append (tempClassList)

    #Build list of class times.
    classTimeSlots = []
    currentClassTimeSlot = currentClassesList[0].classTimeOffered
    for currentClass in currentClassesList:
        if currentClassTimeSlot == currentClass.classTimeOffered:
            pass
        else:
            classTimeSlots.append(currentClassTimeSlot)
            currentClassTimeSlot = currentClass.classTimeOffered
    classTimeSlots.append(currentClassTimeSlot)

    classListAndTimeSlots = zip(classList, classTimeSlots)

    return (type, semesterName, semesterCode, classListAndTimeSlots)
################################################################################################################################################################
#Screen presented to the user when registering for classes. No authentication required.
class ClassRegistrations(webapp.RequestHandler):
    #Handle a class registration after the form has been submitted.
    def post(self):
        try:
            #Get the student's basic information.
            studentRegistration = {'semesterCode': escapeString(self.request.get('SemesterCode')), 'studentName': escapeString(self.request.get('Name'))
                                   , 'studentPhone': escapeString(self.request.get('AreaCode')) + escapeString(self.request.get('PhoneNumber')),
                                   'studentAddress': escapeString(self.request.get('Address')), 'studentCity': escapeString(self.request.get('City')),
                                   'studentState': escapeString(self.request.get('State')), 'studentZip': escapeString(self.request.get('Zip')),
                                   'studentEmail': escapeString(self.request.get('Email')),
                                   'studentNew': True if escapeString(self.request.get('AttendedACED')) == 'No' else False,
                                   'studentAddressNew': True if escapeString(self.request.get('NewAddress')) == 'Yes' else False,
                                   'specialInstructions': escapeString(self.request.get('SpecialInstructions'))}

            #Get the student's emergency contact information.
            emergencyContact = {'emergencyContactName': escapeString(self.request.get('ContactName')),
                                'emergencyContactRelationship': escapeString(self.request.get('ContactRelationship')),
                                'emergencyContactHome': escapeString(self.request.get('AreaCodeHome')) + escapeString(self.request.get('ContactHome')),
                                'emergencyContactPager': escapeString(self.request.get('AreaCodePager')) + escapeString(self.request.get(
                                    'ContactPager')),
                                'emergencyContactWorkPhone': escapeString(self.request.get('AreaCodeWork')) + escapeString(self.request.get(
                                    'ContactWork')),
                                'emergencyContactCellPhone': escapeString(self.request.get('AreaCodeCell')) + escapeString(self.request.get(
                                    'ContactCell'))}

            #Get the campus the student signed up for.
            campus = escapeString(self.request.get("campus"))
            if campus == "":
                self.response.headers['Content-Type'] = 'text/html'
                path = os.path.join(os.path.dirname(__file__), 'thankyou.html')
                self.response.out.write(template.render(path, {'message' : "Sorry! You did not select a campus! You need to select a campus to sign up for classes.<br/><br/>We have classes at UMKC, MCC-Longview and MCC-Blue River."}))
                return
                campus = "No campus chosen"

            #Get the list of classes for the current semester.
            currentClassesList = getCurrentClassesList() #(type, semesterName, semesterCode, classListAndTimeSlots)
            currentSemesterType = currentClassesList[0]
            semesterName = currentClassesList[1]
            semesterCode = currentClassesList[2]
            classListAndTime = currentClassesList[3]

            #Get and store the first and second preferences for classes.
            classFirstPreferences = []
            classSecondPreferences = []
            for i in range (1, len(classListAndTime) + 1):
                currentClass = escapeString(self.request.get('class%d1' % i))
                if currentClass == "Click Here to Choose":
                    classFirstPreferences.append("None")
                else:
                    classFirstPreferences.append(currentClass)
            firstPreferences = ','.join(classFirstPreferences)
            #The previous statement produces string like: "Demo Class 3,Demo Class 2,Demo Class 5"
            for i in range (1, len(classListAndTime) + 1):
                currentClass =escapeString(self.request.get('class%d2' % i))
                if currentClass == "Click Here to Choose":
                    classSecondPreferences.append("None")
                else:
                    classSecondPreferences.append(currentClass)
            secondPreferences = ','.join(classSecondPreferences)
            #The previous statement produces string like: "Demo Class 3,Demo Class 2,Demo Class 5"


            #Check if the student is already in the database.
            studentName = studentRegistration['studentName'].strip()
            sameStudents = db.GqlQuery("SELECT * FROM Student where name='" + studentName + "'")
            if sameStudents.count() == 0:
                #Student hasn't registered before. Create new record.
                student = Student()
                student.name = studentRegistration['studentName']
                student.phone = studentRegistration['studentPhone']
                student.address = studentRegistration['studentAddress']
                student.city = studentRegistration['studentCity']
                student.state = studentRegistration['studentState']
                student.zip = studentRegistration['studentZip']
                student.email = studentRegistration['studentEmail']
                student.newAddress = studentRegistration['studentAddressNew']
                student.newStudent = studentRegistration['studentNew']
                student.specialInstructions = studentRegistration['specialInstructions']

                #Generate student ID - this is a continuously growing number.
                counterQuery = db.GqlQuery("SELECT * FROM Counter")
                counter = counterQuery.fetch(1)
                counter[0].studentCount += 1
                student.uniqueID = studentCodePrefix + str(counter[0].studentCount)
                counter[0].put()
                uniqueID = student.uniqueID

                #Create new enrollment record.
                enrollment = Enrollment()
                enrollment.classFirstPreferences = firstPreferences
                enrollment.classSecondPreferences = secondPreferences
                enrollment.campus = campus
                enrollment.semesterCode = semesterCode
                enrollment.studentID = uniqueID #Linked with student.
                enrollment.approved = False
                enrollment.denied = False
                enrollment.notes = ""
                enrollment.classIDs = "" #This is updated later, on 'accept' or class edit.

                #Create new student emergency contact.
                studentContact = EmergencyContact()
                studentContact.emContactName = emergencyContact['emergencyContactName']
                studentContact.emContactCell = emergencyContact['emergencyContactCellPhone']
                studentContact.emContactHomePhone = emergencyContact['emergencyContactHome']
                studentContact.emContactPager = emergencyContact['emergencyContactPager']
                studentContact.emContactWork = emergencyContact['emergencyContactWorkPhone']
                studentContact.emContactRelationShip = emergencyContact['emergencyContactRelationship']
                studentContact.forStudentWithUniqueID = uniqueID #Linked with student.

                #Save the records.
                student.put()
                studentContact.put()
                enrollment.put()

                #Display pretty thank you page.
                self.response.headers['Content-Type'] = 'text/html'
                path = os.path.join(os.path.dirname(__file__), 'thankyou.html')
                self.response.out.write(template.render(path, {'name':studentRegistration['studentName'], 'valid':"Yes"}))
            else:
                #Student has registered for classes before.
                #Assign a new enrollment to the same student ID.
                studentRecord = sameStudents.fetch(1)[0]
                studentRecord.name = studentRegistration['studentName']
                studentRecord.phone = studentRegistration['studentPhone']
                studentRecord.address = studentRegistration['studentAddress']
                studentRecord.city = studentRegistration['studentCity']
                studentRecord.state = studentRegistration['studentState']
                studentRecord.zip = studentRegistration['studentZip']
                studentRecord.email = studentRegistration['studentEmail']
                studentRecord.newAddress = studentRegistration['studentAddressNew']
                studentRecord.newStudent = studentRegistration['studentNew']
                studentRecord.specialInstructions = studentRegistration['specialInstructions']
                uniqueID = studentRecord.uniqueID
                #Do not change the studentID because it's the same student.

                #Create new enrollment record.
                enrollment = Enrollment()
                enrollment.classFirstPreferences = firstPreferences
                enrollment.classSecondPreferences = secondPreferences
                enrollment.campus = campus
                enrollment.semesterCode = semesterCode
                enrollment.studentID = uniqueID #Linked with student.
                enrollment.approved = False
                enrollment.denied = False
                enrollment.notes = ""
                enrollment.classIDs = "" #This is updated later, on 'accept' or class edit.

                #Check for duplicate enrollments.
                enrollmentDuplicatesQuery = db.GqlQuery("SELECT * FROM Enrollment WHERE studentID = '" + uniqueID
                                                        + "' AND campus='" + campus + "' AND semesterCode='" + semesterCode + "'")
                if enrollmentDuplicatesQuery.count() >= 1:
                    self.response.headers['Content-Type'] = 'text/html'
                    path = os.path.join(os.path.dirname(__file__), 'thankyou.html')
                    self.response.out.write(template.render(path, {'message' : "We have already received your registration for this semester and"
                    + " location.<br/><br/>Did you mean to sign up for a different location?<br/><br/>We have classes at UMKC, MCC-Longview and MCC-Blue River."}))
                    return



                #Update the existing student emergency contact.
                studentContactQuery = db.GqlQuery("SELECT * FROM Enrollment WHERE studentID='" + studentRecord.uniqueID + "'")
                studentContact = studentContactQuery.fetch(1)[0]
                studentContact.emContactName = emergencyContact['emergencyContactName']
                studentContact.emContactCell = emergencyContact['emergencyContactCellPhone']
                studentContact.emContactHomePhone = emergencyContact['emergencyContactHome']
                studentContact.emContactPager = emergencyContact['emergencyContactPager']
                studentContact.emContactWork = emergencyContact['emergencyContactWorkPhone']
                studentContact.emContactRelationShip = emergencyContact['emergencyContactRelationship']
                studentContact.forStudentWithUniqueID = uniqueID #Linked with student.

                #Save the records.
                studentRecord.put()
                studentContact.put()
                enrollment.put()

                #Display pretty thank you page.
                self.response.headers['Content-Type'] = 'text/html'
                path = os.path.join(os.path.dirname(__file__), 'thankyou.html')
                self.response.out.write(template.render(path, {'name':studentRegistration['studentName'], 'valid':"Yes"}))
        except Exception, e:
            logging.error("Enrollment Error:" + str(e))
            #Display pretty try again page.
            self.response.headers['Content-Type'] = 'text/html'
            path = os.path.join(os.path.dirname(__file__), 'thankyou.html')
            self.response.out.write(template.render(path, {}))
    def get(self):
        try:
            self.response.headers['Content-Type'] = 'text/html'
            currentClassList = getCurrentClassesList() #(type, semesterName, semesterCode, classListAndTimeSlots)
            #Get the names of the contacts.
            contactsQuery = db.GqlQuery("SELECT * FROM CurrentSemester")
            contacts = contactsQuery.fetch(1)[0]
            umkcContact = contacts.umkcContactName
            lvContact = contacts.lvContactName
            brContact = contacts.brContactName
            if currentClassList[0] == "Spring" or currentClassList[0] == "Fall":
                path = os.path.join(os.path.dirname(__file__), 'registerationform.html')
                self.response.out.write(template.render(path, {'SemesterCode':currentClassList[2], 'semester':currentClassList[1],
                    'class_list_overall':currentClassList[3], 'umkcname':umkcContact,'lvname':lvContact,'brname':brContact}))
        except Exception, e:
            reportError(self, "Sorry. There's been an error: " + str(e))
