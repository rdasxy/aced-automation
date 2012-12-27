__author__ = 'rdasxy'

#Contains all the Google App Engine imports that can be imported together.
import os
import cgi
import time
import datetime
import re
import copy
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
import logging
from django.utils import simplejson as json
from safeEscape import *

################################################################################################################################################################
domain = "/"
################################################################################################################################################################
#Dictionary Mapping colloquial campus names (values) to database identification keys (key).
campuses = {
    "umkc":"UMKC",
    "br":"MCC-Blue River",
    "lv":"MCC-Longview"
    }
################################################################################################################################################################
studentCodePrefix = "ACEDStudent"
teacherUsers = ['teacherlv', 'teacherumkc', 'teacherbr']
teacherCampuses = ['lv', 'umkc', 'br']
authenticationTimeout = 2880
################################################################################################################################################################
#Returns a list of the "class time slots" (descriptive) for the given semester.
def getClassTimeSlots(semester):
    currentClassesList = db.GqlQuery("SELECT * from Class where semester='" + semester + "' ORDER BY classTimeSlot asc")
    classTimeSlots = []
    currentClassTimeSlot = currentClassesList[0].classTimeOffered
    for currentClass in currentClassesList:
        if currentClassTimeSlot == currentClass.classTimeOffered:
            pass
        else:
            classTimeSlots.append(currentClassTimeSlot)
            currentClassTimeSlot = currentClass.classTimeOffered
    classTimeSlots.append(currentClassTimeSlot)
    return classTimeSlots
################################################################################################################################################################
def reportError(requestHandler, message):
    requestHandler.response.headers['Content-Type'] = 'text/html'
    requestHandler.response.out.write("Error: %s" % message)
