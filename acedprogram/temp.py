__author__ = 'rdasxy'
from universalImports import *
from aadbdef import *
#Sets up the database with temporary data
def setUpTempData():
    try:    
        #Set up Google DataStore with initial login credentials for Site Admins - this is for first runs only.
        currentUsers = db.GqlQuery("SELECT * FROM User")
        if currentUsers.count() == 0:            
            user1 = User()
            user1.userName = "lvccadmin"
            user1.password = "password"
            user1.put()
            user2 = User()
            user2.userName = "bradmin"
            user2.password = "password"
            user2.put()
            user3 = User()
            user3.userName = "admin"
            user3.password = "password"
            user3.put()
            user4 = User()
            user4.userName = "teacher"
            user4.password = "password"
            user4.put()
            user = User()
            user.userName = "teacherlv"
            user.password = "password"
            user.put()
            user = User()
            user.userName = "teacherbr"
            user.password = "password"
            user.put()
            user = User()
            user.userName = "teacherumkc"
            user.password = "password"
            user.put()
            #Current Semester - used for enrollment
            currentSemester = CurrentSemester()
            currentSemester.code = "fa2011"
            currentSemester.semesterKind = "Fall"
            currentSemester.umkcContactName = "Wendy Seelbinder"
            currentSemester.brContactName = "Karen Crowell"
            currentSemester.lvContactName = "Nancy Carter"
            currentSemester.put()
            counter = Counter()
            counter.studentCount = 0
            counter.classCount = 21
            counter.put()
            #From here and below, it's dummy data.
            #Semesters
            semester1 = Semester()
            semester1.session = "Fall"
            semester1.year = 2011
            semester1.code = "fa2011"
            semester1.classDays = "9/10,9/17,9/24,10/1,10/8,10/15"
            semester1.put()
            semester2 = Semester()
            semester2.session = "Fall"
            semester2.classDays = "5/15,5/16,5/17"
            semester2.year = 2010
            semester2.code = "fa2010"
            semester2.put()
            #Classes
            class1 = Class()
            class1.name = "Music To My Ears"
            class1.classID = 1
            class1.semester = "fa2011"
            class1.campuses = "umkc,br,lv"
            class1.studentLimit = 15
            class1.classDays = "9/10,9/17,9/24,10/1,10/8,10/15"
            class1.teacherName = ""
            class1.taNames = ""
            class1.studentCount = 0
            class1.classTimeSlot = 1
            class1.classTimeOffered = "9:00a.m. - 10:00a.m."
            class1.classFee = 6
            class1.studentCountBR = 0
            class1.studentCountLV = 0
            class1.studentCountUMKC = 0
            class1.put()
            class1 = Class()
            class1.name = "Math-Cha-Ching!"
            class1.classID = 2
            class1.semester = "fa2011"
            class1.campuses = "umkc,br,lv"
            class1.studentLimit = 15
            class1.classDays = "9/10,9/17,9/24,10/1,10/8,10/15"
            class1.teacherName = ""
            class1.taNames = ""
            class1.studentCount = 0
            class1.classTimeSlot = 1
            class1.classTimeOffered = "9:00a.m. - 10:00a.m."
            class1.classFee = 6
            class1.studentCountBR = 0
            class1.studentCountLV = 0
            class1.studentCountUMKC = 0
            class1.put()
            class1 = Class()
            class1.name = "Disasters"
            class1.classID = 3
            class1.semester = "fa2011"
            class1.campuses = "umkc,br,lv"
            class1.studentLimit = 15
            class1.classDays = "9/10,9/17,9/24,10/1,10/8,10/15"
            class1.teacherName = ""
            class1.taNames = ""
            class1.studentCount = 0
            class1.classTimeSlot = 1
            class1.classTimeOffered = "9:00a.m. - 10:00a.m."
            class1.classFee = 6
            class1.studentCountBR = 0
            class1.studentCountLV = 0
            class1.studentCountUMKC = 0
            class1.put()
            class1 = Class()
            class1.name = "Yoga Wherever You Go"
            class1.classID = 4
            class1.semester = "fa2011"
            class1.campuses = "umkc,lv"
            class1.studentLimit = 15
            class1.classDays = "9/10,9/17,9/24,10/1,10/8,10/15"
            class1.teacherName = ""
            class1.taNames = ""
            class1.studentCount = 0
            class1.classTimeSlot = 1
            class1.classTimeOffered = "9:00a.m. - 10:00a.m."
            class1.classFee = 6
            class1.studentCountBR = 0
            class1.studentCountLV = 0
            class1.studentCountUMKC = 0
            class1.put()
            class1 = Class()
            class1.name = "Where is Flat Stanley"
            class1.classID = 5
            class1.semester = "fa2011"
            class1.campuses = "umkc,lv"
            class1.studentLimit = 15
            class1.classDays = "9/10,9/17,9/24,10/1,10/8,10/15"
            class1.teacherName = ""
            class1.taNames = ""
            class1.studentCount = 0
            class1.classTimeSlot = 1
            class1.classTimeOffered = "9:00a.m. - 10:00a.m."
            class1.classFee = 6
            class1.studentCountBR = 0
            class1.studentCountLV = 0
            class1.studentCountUMKC = 0
            class1.put()
            class1 = Class()
            class1.name = "Mini Size Me!"
            class1.classID = 6
            class1.semester = "fa2011"
            class1.campuses = "umkc,lv"
            class1.studentLimit = 15
            class1.classDays = "9/10,9/17,9/24,10/1,10/8,10/15"
            class1.teacherName = ""
            class1.taNames = ""
            class1.studentCount = 0
            class1.classTimeSlot = 1
            class1.classTimeOffered = "9:00a.m. - 10:00a.m."
            class1.classFee = 6
            class1.studentCountBR = 0
            class1.studentCountLV = 0
            class1.studentCountUMKC = 0
            class1.put()
            class1 = Class()
            class1.name = "Drawing/Painting"
            class1.classID = 7
            class1.semester = "fa2011"
            class1.campuses = "umkc,lv"
            class1.studentLimit = 15
            class1.classDays = "9/10,9/17,9/24,10/1,10/8,10/15"
            class1.teacherName = ""
            class1.taNames = ""
            class1.studentCount = 0
            class1.classTimeSlot = 1
            class1.classTimeOffered = "9:00a.m. - 10:00a.m."
            class1.classFee = 6
            class1.studentCountBR = 0
            class1.studentCountLV = 0
            class1.studentCountUMKC = 0
            class1.put()
            class1 = Class()
            class1.name = "Kickin' Karaoke"
            class1.classID = 8
            class1.semester = "fa2011"
            class1.campuses = "umkc,br,lv"
            class1.studentLimit = 15
            class1.classDays = "9/10,9/17,9/24,10/1,10/8,10/15"
            class1.teacherName = ""
            class1.taNames = ""
            class1.studentCount = 0
            class1.classTimeSlot = 2
            class1.classTimeOffered = "10:10a.m. - 11:10a.m."
            class1.classFee = 6
            class1.studentCountBR = 0
            class1.studentCountLV = 0
            class1.studentCountUMKC = 0
            class1.put()
            class1 = Class()
            class1.name = "Bit by Byte: Become a Computer Whiz"
            class1.classID = 9
            class1.semester = "fa2011"
            class1.campuses = "umkc,br,lv"
            class1.studentLimit = 15
            class1.classDays = "9/10,9/17,9/24,10/1,10/8,10/15"
            class1.teacherName = ""
            class1.taNames = ""
            class1.studentCount = 0
            class1.classTimeSlot = 2
            class1.classTimeOffered = "10:10a.m. - 11:10a.m."
            class1.classFee = 6
            class1.studentCountBR = 0
            class1.studentCountLV = 0
            class1.studentCountUMKC = 0
            class1.put()
            class1 = Class()
            class1.name = "Under the Sea"
            class1.classID = 10
            class1.semester = "fa2011"
            class1.campuses = "umkc,br,lv"
            class1.studentLimit = 15
            class1.classDays = "9/10,9/17,9/24,10/1,10/8,10/15"
            class1.teacherName = ""
            class1.taNames = ""
            class1.studentCount = 0
            class1.classTimeSlot = 2
            class1.classTimeOffered = "10:10a.m. - 11:10a.m."
            class1.classFee = 6
            class1.studentCountBR = 0
            class1.studentCountLV = 0
            class1.studentCountUMKC = 0
            class1.put()
            class1 = Class()
            class1.name = "Two Thumbs Up"
            class1.classID = 11
            class1.semester = "fa2011"
            class1.campuses = "umkc,lv"
            class1.studentLimit = 15
            class1.classDays = "9/10,9/17,9/24,10/1,10/8,10/15"
            class1.teacherName = ""
            class1.taNames = ""
            class1.studentCount = 0
            class1.classTimeSlot = 2
            class1.classTimeOffered = "10:10a.m. - 11:10a.m."
            class1.classFee = 6
            class1.studentCountBR = 0
            class1.studentCountLV = 0
            class1.studentCountUMKC = 0
            class1.put()
            class1 = Class()
            class1.name = "Garrett's Gadgets"
            class1.classID = 12
            class1.semester = "fa2011"
            class1.campuses = "umkc,lv"
            class1.studentLimit = 15
            class1.classDays = "9/10,9/17,9/24,10/1,10/8,10/15"
            class1.teacherName = ""
            class1.taNames = ""
            class1.studentCount = 0
            class1.classTimeSlot = 2
            class1.classTimeOffered = "10:10a.m. - 11:10a.m."
            class1.classFee = 6
            class1.studentCountBR = 0
            class1.studentCountLV = 0
            class1.studentCountUMKC = 0
            class1.put()
            class1 = Class()
            class1.name = "Ladies and Gentleman"
            class1.classID = 13
            class1.semester = "fa2011"
            class1.campuses = "umkc,lv"
            class1.studentLimit = 15
            class1.classDays = "9/10,9/17,9/24,10/1,10/8,10/15"
            class1.teacherName = ""
            class1.taNames = ""
            class1.studentCount = 0
            class1.classTimeSlot = 2
            class1.classTimeOffered = "10:10a.m. - 11:10a.m."
            class1.classFee = 6
            class1.studentCountBR = 0
            class1.studentCountLV = 0
            class1.studentCountUMKC = 0
            class1.put()
            class1 = Class()
            class1.name = "Tales Told in a Tent"
            class1.classID = 14
            class1.semester = "fa2011"
            class1.campuses = "umkc,lv"
            class1.studentLimit = 15
            class1.classDays = "9/10,9/17,9/24,10/1,10/8,10/15"
            class1.teacherName = ""
            class1.taNames = ""
            class1.studentCount = 0
            class1.classTimeSlot = 2
            class1.classTimeOffered = "10:10a.m. - 11:10a.m."
            class1.classFee = 6
            class1.studentCountBR = 0
            class1.studentCountLV = 0
            class1.studentCountUMKC = 0
            class1.put()
            class1 = Class()
            class1.name = "Oh Fudge"
            class1.classID = 15
            class1.semester = "fa2011"
            class1.campuses = "umkc,br,lv"
            class1.studentLimit = 15
            class1.classDays = "9/10,9/17,9/24,10/1,10/8,10/15"
            class1.teacherName = ""
            class1.taNames = ""
            class1.studentCount = 0
            class1.classTimeSlot = 3
            class1.classTimeOffered = "11:20a.m. - 12:35a.m."
            class1.classFee = 6
            class1.studentCountBR = 0
            class1.studentCountLV = 0
            class1.studentCountUMKC = 0
            class1.put()
            class1 = Class()
            class1.name = "Pick Up the Pace"
            class1.classID = 16
            class1.semester = "fa2011"
            class1.campuses = "umkc,br,lv"
            class1.studentLimit = 15
            class1.classDays = "9/10,9/17,9/24,10/1,10/8,10/15"
            class1.teacherName = ""
            class1.taNames = ""
            class1.studentCount = 0
            class1.classTimeSlot = 3
            class1.classTimeOffered = "11:20a.m. - 12:35a.m."
            class1.classFee = 6
            class1.studentCountBR = 0
            class1.studentCountLV = 0
            class1.studentCountUMKC = 0
            class1.put()
            class1 = Class()
            class1.name = "Hula Hoop Weaving"
            class1.classID = 17
            class1.semester = "fa2011"
            class1.campuses = "umkc,br,lv"
            class1.studentLimit = 15
            class1.classDays = "9/10,9/17,9/24,10/1,10/8,10/15"
            class1.teacherName = ""
            class1.taNames = ""
            class1.studentCount = 0
            class1.classTimeSlot = 3
            class1.classTimeOffered = "11:20a.m. - 12:35a.m."
            class1.classFee = 6
            class1.studentCountBR = 0
            class1.studentCountLV = 0
            class1.studentCountUMKC = 0
            class1.put()
            class1 = Class()
            class1.name = "Getting to the Core - Apples & Orchards"
            class1.classID = 18
            class1.semester = "fa2011"
            class1.campuses = "umkc,lv"
            class1.studentLimit = 15
            class1.classDays = "9/10,9/17,9/24,10/1,10/8,10/15"
            class1.teacherName = ""
            class1.taNames = ""
            class1.studentCount = 0
            class1.classTimeSlot = 3
            class1.classTimeOffered = "11:20a.m. - 12:35a.m."
            class1.classFee = 6
            class1.studentCountBR = 0
            class1.studentCountLV = 0
            class1.studentCountUMKC = 0
            class1.put()
            class1 = Class()
            class1.name = "Unusual Sports"
            class1.classID = 19
            class1.semester = "fa2011"
            class1.campuses = "umkc,lv"
            class1.studentLimit = 15
            class1.classDays = "9/10,9/17,9/24,10/1,10/8,10/15"
            class1.teacherName = ""
            class1.taNames = ""
            class1.studentCount = 0
            class1.classTimeSlot = 3
            class1.classTimeOffered = "11:20a.m. - 12:35a.m."
            class1.classFee = 6
            class1.studentCountBR = 0
            class1.studentCountLV = 0
            class1.studentCountUMKC = 0
            class1.put()
            class1 = Class()
            class1.name = "Pat Rat Beware"
            class1.classID = 20
            class1.semester = "fa2011"
            class1.campuses = "umkc,lv"
            class1.studentLimit = 15
            class1.classDays = "9/10,9/17,9/24,10/1,10/8,10/15"
            class1.teacherName = ""
            class1.taNames = ""
            class1.studentCount = 0
            class1.classTimeSlot = 3
            class1.classTimeOffered = "11:20a.m. - 12:35a.m."
            class1.classFee = 6
            class1.studentCountBR = 0
            class1.studentCountLV = 0
            class1.studentCountUMKC = 0
            class1.put()
            class1 = Class()
            class1.name = "Courtroom Drama"
            class1.classID = 21
            class1.semester = "fa2011"
            class1.campuses = "umkc,lv"
            class1.studentLimit = 15
            class1.classDays = "9/10,9/17,9/24,10/1,10/8,10/15"
            class1.teacherName = ""
            class1.taNames = ""
            class1.studentCount = 0
            class1.classTimeSlot = 3
            class1.classTimeOffered = "11:20a.m. - 12:35a.m."
            class1.classFee = 6
            class1.studentCountBR = 0
            class1.studentCountLV = 0
            class1.studentCountUMKC = 0
            class1.put()
            ##
            attendance = ClassRoster()
            attendance.forClassID = 1
            attendance.attendance = "None"
            attendance.campus = "umkc"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 2
            attendance.attendance = "None"
            attendance.campus = "umkc"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 3
            attendance.attendance = "None"
            attendance.campus = "umkc"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 4
            attendance.attendance = "None"
            attendance.campus = "umkc"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 5
            attendance.attendance = "None"
            attendance.campus = "umkc"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 6
            attendance.attendance = "None"
            attendance.campus = "umkc"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 7
            attendance.attendance = "None"
            attendance.campus = "umkc"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 8
            attendance.attendance = "None"
            attendance.campus = "umkc"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 9
            attendance.attendance = "None"
            attendance.campus = "umkc"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 10
            attendance.attendance = "None"
            attendance.campus = "umkc"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 11
            attendance.attendance = "None"
            attendance.campus = "umkc"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 12
            attendance.attendance = "None"
            attendance.campus = "umkc"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 13
            attendance.attendance = "None"
            attendance.campus = "umkc"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 14
            attendance.attendance = "None"
            attendance.campus = "umkc"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 15
            attendance.attendance = "None"
            attendance.campus = "umkc"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 16
            attendance.attendance = "None"
            attendance.campus = "umkc"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 17
            attendance.attendance = "None"
            attendance.campus = "umkc"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 18
            attendance.attendance = "None"
            attendance.campus = "umkc"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 19
            attendance.attendance = "None"
            attendance.campus = "umkc"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 20
            attendance.attendance = "None"
            attendance.campus = "umkc"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 21
            attendance.attendance = "None"
            attendance.campus = "umkc"
            attendance.put()
            ##
            attendance = ClassRoster()
            attendance.forClassID = 1
            attendance.attendance = "None"
            attendance.campus = "br"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 2
            attendance.attendance = "None"
            attendance.campus = "br"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 3
            attendance.attendance = "None"
            attendance.campus = "br"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 4
            attendance.attendance = "None"
            attendance.campus = "br"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 5
            attendance.attendance = "None"
            attendance.campus = "br"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 6
            attendance.attendance = "None"
            attendance.campus = "br"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 7
            attendance.attendance = "None"
            attendance.campus = "br"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 8
            attendance.attendance = "None"
            attendance.campus = "br"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 9
            attendance.attendance = "None"
            attendance.campus = "br"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 10
            attendance.attendance = "None"
            attendance.campus = "br"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 11
            attendance.attendance = "None"
            attendance.campus = "br"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 12
            attendance.attendance = "None"
            attendance.campus = "br"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 13
            attendance.attendance = "None"
            attendance.campus = "br"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 14
            attendance.attendance = "None"
            attendance.campus = "br"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 15
            attendance.attendance = "None"
            attendance.campus = "br"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 16
            attendance.attendance = "None"
            attendance.campus = "br"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 17
            attendance.attendance = "None"
            attendance.campus = "br"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 18
            attendance.attendance = "None"
            attendance.campus = "br"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 19
            attendance.attendance = "None"
            attendance.campus = "br"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 20
            attendance.attendance = "None"
            attendance.campus = "br"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 21
            attendance.attendance = "None"
            attendance.campus = "br"
            attendance.put()
            ##
            attendance = ClassRoster()
            attendance.forClassID = 1
            attendance.attendance = "None"
            attendance.campus = "lv"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 2
            attendance.attendance = "None"
            attendance.campus = "lv"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 3
            attendance.attendance = "None"
            attendance.campus = "lv"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 4
            attendance.attendance = "None"
            attendance.campus = "lv"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 5
            attendance.attendance = "None"
            attendance.campus = "lv"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 6
            attendance.attendance = "None"
            attendance.campus = "lv"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 7
            attendance.attendance = "None"
            attendance.campus = "lv"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 8
            attendance.attendance = "None"
            attendance.campus = "lv"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 9
            attendance.attendance = "None"
            attendance.campus = "lv"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 10
            attendance.attendance = "None"
            attendance.campus = "lv"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 11
            attendance.attendance = "None"
            attendance.campus = "lv"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 12
            attendance.attendance = "None"
            attendance.campus = "lv"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 13
            attendance.attendance = "None"
            attendance.campus = "lv"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 14
            attendance.attendance = "None"
            attendance.campus = "lv"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 15
            attendance.attendance = "None"
            attendance.campus = "lv"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 16
            attendance.attendance = "None"
            attendance.campus = "lv"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 17
            attendance.attendance = "None"
            attendance.campus = "lv"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 18
            attendance.attendance = "None"
            attendance.campus = "lv"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 19
            attendance.attendance = "None"
            attendance.campus = "lv"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 20
            attendance.attendance = "None"
            attendance.campus = "lv"
            attendance.put()
            attendance = ClassRoster()
            attendance.forClassID = 21
            attendance.attendance = "None"
            attendance.campus = "lv"
            attendance.put()
            ##
            attendance = SemesterRoster()
            attendance.forSemesterID = "fa2011"
            attendance.attendance = "None"
            attendance.campus = "lv"
            attendance.put()
            attendance = SemesterRoster()
            attendance.forSemesterID = "fa2011"
            attendance.attendance = "None"
            attendance.campus = "br"
            attendance.put()
            attendance = SemesterRoster()
            attendance.forSemesterID = "fa2011"
            attendance.attendance = "None"
            attendance.campus = "umkc"
            attendance.put()
            
            
            #Add Class Schedule information
            scheduleInfo1 = ClassScheduleInformation()
            scheduleInfo1.semesterID = "fa2011"
            scheduleInfo1.campus = 'BR'
            scheduleInfo1.classesBeginNotes = "Class Begin on Saturday September 10, 2011"
            scheduleInfo1.classesEndNotes = "Classes End on Saturday, October 15, followed by a reception"
            scheduleInfo1.arrivalNotes = "Please plan on arriving 15 minutes early"
            scheduleInfo1.attendancePolicy = "Come every day"
            scheduleInfo1.location = "Blue River"
            scheduleInfo1.directions = "Directions TO BR"
            scheduleInfo1.problemNotice = "For problems call Blue River at xxxxx"
            scheduleInfo1.building = "Royall Hall"
            scheduleInfo1.put()
            scheduleInfo2 = ClassScheduleInformation()
            scheduleInfo2.semesterID = "fa2011"
            scheduleInfo2.campus = 'LV'
            scheduleInfo2.classesBeginNotes = "Class Begin on Saturday October 22, 2011"
            scheduleInfo2.classesEndNotes = "Classes End on Saturday December 3, followed by a reception"
            scheduleInfo2.arrivalNotes = "Please plan on arriving 15 minutes early"
            scheduleInfo2.attendancePolicy = "Come every day"
            scheduleInfo1.building = "LV Hall"
            scheduleInfo2.location = "LongView"
            scheduleInfo2.directions = "Directions TO LV"
            scheduleInfo2.problemNotice = "For problems call Phani at xxxxx"
            scheduleInfo2.put()
            scheduleInfo3 = ClassScheduleInformation()
            scheduleInfo3.semesterID = "fa2011"
            scheduleInfo3.campus = 'UMKC'
            scheduleInfo3.classesBeginNotes = "Class Begin on Saturday October 22, 2011"
            scheduleInfo3.classesEndNotes = "Classes End on Saturday December 3, followed by a reception"
            scheduleInfo3.arrivalNotes = "Please plan on arriving 15 minutes early"
            scheduleInfo3.attendancePolicy = "Come every day"
            scheduleInfo1.building = "BR Hall"
            scheduleInfo3.location = "UMKC"
            scheduleInfo3.directions = "Directions TO UMKC"
            scheduleInfo3.problemNotice = "For problems call Phani at xxxxx"
            scheduleInfo3.put()
    except Exception, e:
        reportError(self, "Sorry. There's been an error: " + str(e))
