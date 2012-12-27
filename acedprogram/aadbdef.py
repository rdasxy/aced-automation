__author__ = 'rdasxy'

'''
Module: aadbdef - ACEDAutomationDatabaseDefinition
Establishes all the datastore entities for ACEDAutomation.
'''
from universalImports import *
################################################################################################################################################################
#Datastore entity description of all the users currently accessing the application.
#Note: There is no way to add users.
class User(db.Model):
    userName = db.StringProperty()
    password = db.StringProperty()
################################################################################################################################################################
#Datastore entity description of all semesters currently in the system.
#Session: Fall/Spring/Summer. Year: 2011, 2012 ...
#'classDays' is a comma separated list of all the days the class is offered on. e.g. "10/23,10/30,11/06 etc."
class Semester(db.Model):
    session = db.StringProperty()
    year = db.IntegerProperty()
    code = db.StringProperty()
    classDays = db.StringProperty()
################################################################################################################################################################
#Datastore entity description for each student.
class Student(db.Model):
    uniqueID = db.StringProperty()
    name = db.StringProperty()
    phone = db.StringProperty()
    address = db.StringProperty()
    city = db.StringProperty()
    state= db.StringProperty()
    zip = db.StringProperty()
    email = db.StringProperty()
    newStudent = db.BooleanProperty()
    newAddress = db.BooleanProperty()
    specialInstructions = db.StringProperty()
################################################################################################################################################################
#Datastore entity description for a student's emergency contact.
#Linked to individual student using the 'forStudentWithUniqueID' field.
class EmergencyContact(db.Model):
    forStudentWithUniqueID = db.StringProperty()
    emContactName = db.StringProperty()
    emContactRelationShip = db.StringProperty()
    emContactHomePhone = db.StringProperty()
    emContactPager = db.StringProperty()
    emContactWork = db.StringProperty()
    emContactCell = db.StringProperty()
################################################################################################################################################################
#Datastore entity description to manage enrollment for each student for each semester.
#Linked to semester code using 'semesterCode' field.
#Linked to campuses using codes defined in 'campuses' dict.
#Linked to students using 'studentID'.
#'classFirstPreferences' and 'classSecondPreferences' are comma separated list of class names.
#'notes' is used for general notes (internal) about the enrollment record.
#'approved' is set to 'True' when admin approves the registration.
#'classIDs' is a comma separated list of all 'classID's the student is enrolled in.
class Enrollment(db.Model):
    semesterCode = db.StringProperty()
    studentID = db.StringProperty()
    campus = db.StringProperty()#Upper case campus.
    classFirstPreferences = db.StringProperty()
    classSecondPreferences = db.StringProperty()
    notes = db.StringProperty()
    approved = db.BooleanProperty()
    denied = db.BooleanProperty()
    classIDs = db.StringProperty()
################################################################################################################################################################
#Datastore entity description to store data about all the classes.
#'name' is the general class name.
#'classID' gives serial number - e.g. 1.
#'semester' gives 'code' of semester - e.g. su2011.
#'campuses' is a commma-separated list of campuses. e.g. "lv,br".
#'studentLimit' is an upper bound on the number of students.
#'classTimeSlot' is used to differentiate between classes that aren't offered at the same time.
#'classTimeOffered' is a general string description of the class duration. e.g. "9:00 a.m. - 10:00 a.m."
#'classDays' is a comma separated list of all the days the class is offered on. e.g. "10/23,10/30,11/06 etc."
#'classFee' is the dollar value of the fee for this class.
#'studentCount' is the current count of the number of students in the class.
#'teacherName' is the name of the instructor.
#'taNames' is the names of the teacher aides.
class Class(db.Model):
    name = db.StringProperty()
    classID = db.IntegerProperty()
    classTimeSlot = db.IntegerProperty()
    classTimeOffered = db.StringProperty()
    classDays = db.StringProperty()
    teacherName = db.StringProperty()
    taNames = db.StringProperty()
    semester = db.StringProperty()
    campuses = db.StringProperty()
    studentCount = db.IntegerProperty()
    studentCountBR = db.IntegerProperty()
    studentCountLV = db.IntegerProperty()
    studentCountUMKC = db.IntegerProperty()
    studentLimit = db.IntegerProperty()
    classFee = db.IntegerProperty()
################################################################################################################################################################
#Datastore entity description to store data about the attendance from the classes.
#'forClassID' associates it with a specific class.
#'attendance' is a semi-colon and comma separated list of Yes or Nos. e.g. 'Yes,Yes,No;Yes,Yes,No;Yes,No,No'.
#'campus' is either 'br', 'lv' or 'umkc'.
class ClassRoster (db.Model):
    forClassID = db.IntegerProperty()
    campus = db.StringProperty()#Lowercase campus
    attendance = db.StringProperty()
################################################################################################################################################################
#Datastore entity description to store data about the attendance from every day of the session.
#'forSemesterID' associates it with a specific semester.
#'attendance' is a semi-colon and comma separated list of Yes or Nos. e.g. 'Yes,Yes,No;Yes,Yes,No;Yes,No,No'.
#'campus' is either 'br', 'lv' or 'umkc'.
class SemesterRoster (db.Model):
    forSemesterID = db.StringProperty()
    campus = db.StringProperty()#Lowercase campus
    attendance = db.StringProperty()
################################################################################################################################################################
#Datastore entity to store the current semester.
#Contains only one item in total ever.
#Linked to semesters using 'code'.
#Kind tells whether it's a summer semester or spring/fall.
class CurrentSemester(db.Model):
    code = db.StringProperty()
    semesterKind = db.StringProperty()
    umkcContactName = db.StringProperty()
    brContactName = db.StringProperty()
    lvContactName = db.StringProperty()
################################################################################################################################################################
#Datastore entity to store the counter.
#Contains only one item in total ever.
#'studentCount' is the current count of the number of students.
#'classCount' is the current count of the class.
class Counter(db.Model):
    studentCount = db.IntegerProperty()
    classCount = db.IntegerProperty()
################################################################################################################################################################
#Datastore entity to store the information that goes with the student class schedules of the current semester and campus.
#Linked to semesters using 'code'.
#Kind tells whether it's a summer semester or spring/fall.
class ClassScheduleInformation(db.Model):
    semesterID = db.StringProperty()
    campus = db.StringProperty()#Upper case campus.
    classesBeginNotes = db.StringProperty()
    classesEndNotes = db.StringProperty()
    arrivalNotes = db.StringProperty()
    attendancePolicy = db.StringProperty()
    location = db.StringProperty()
    building = db.StringProperty()
    directions = db.StringProperty()
    problemNotice = db.StringProperty()
