__author__ = 'rdasxy'

from universalImports import *
from aadbdef import *
from authHelper import *
################################################################################################################################################################
#Allows the admin to change password for all users.
class ChangePassword(webapp.RequestHandler):
    def get(self):
        try:    
            currentlyLoggedInUser = securelyProceed(self)
            if currentlyLoggedInUser:
                #Build a list of all years.
                usersQuery = db.GqlQuery("SELECT * FROM User")
                users = usersQuery.fetch(15)
                userNames = []
                for user in users:
                    userNames.append(str(user.userName))
                #Display the page.
                self.response.headers['Content-Type'] = 'text/html'
                path = os.path.join(os.path.dirname(__file__), 'changepassword.html')
                self.response.out.write(template.render(path, {'users' : userNames}))
        except Exception, e:
            reportError(self, "Sorry. There's been an error: " + str(e))
    def post(self):
        try:
            userName = escapeString(self.request.get('userName'))
            password = escapeString(self.request.get('password'))
            confirmPassword = escapeString(self.request.get('confirmPassword'))
            if password != confirmPassword:
                raise Exception()
            else:
                usersQuery = db.GqlQuery("SELECT * FROM User WHERE userName='" + userName + "'")
                user = usersQuery.fetch(1)[0]
                user.password = password
                user.put()
                self.response.out.write("Password successfully changed!")
        except:
            reportError(self, "Invalid input. Please check and try again.")







