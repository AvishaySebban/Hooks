#!/usr/bin/python

#/*** BEGIN META {
#  The Scripit would scan Jenkins jobs status to generate summary report. 
#} END META***/
from ConfigParser import SafeConfigParser
import requests
import glob
import ConfigParser
import json 
import sys
import urllib2
import time

def get_status(jobName):

    jenkinsUrl = "http://jenkins-master:8080/job/"
	
    config = ConfigParser.RawConfigParser()
    parser = SafeConfigParser()
    parser.read(jenkins_jobs)
	
    try:
        jenkinsStream   = urllib2.urlopen( jenkinsUrl + jobName + "/lastBuild/api/json" )
		
    except urllib2.HTTPError, e:
        print "URL Error: " + str(e.code) 
        print "      (job name [" + jobName + "] probably wrong)"
        sys.exit(2)

    try:
        buildStatusJson = json.load( jenkinsStream )
        print "JobName: " + jobName
        print "Result: " + str(buildStatusJson["result"])
        print "Description: " + str(buildStatusJson["description"])
        print "Link Address: " + jenkinsUrl + jobName + "/HTML_Report/"
        print "\n" 

	# Writing our configuration file to 'conf.properties'
	with open('conf.properties', 'wb') as configfile:
		config.write(configfile)
    except:
        print "Failed to parse json"
        sys.exit(3)
		
    return jobName,buildStatusJson["timestamp"], buildStatusJson["result"],buildStatusJson["description"]

cmdargs = str(sys.argv)
jenkins_jobs=["Callisto-Cucumber","CAS-Cucumber","CFD-Cucumber","CLFX-Cucumber","EQ-Cucumber","ETD-Cucumber-Orchestrator","Harmony5-Cucumber","Harmony5-Cucumber-win","TRC-Cucumber"]
time_now = time.time() * 1000
rc=0
print "\n"
for job in jenkins_jobs:
    status = get_status(job)
    #status = ('ETD-Cucumber-Orchestrator', 1451475177724, u'SUCCESS')
    if time_now - status[1] > 24 * 3600 * 1000 :
         response = requests.post("http://jenkins-master:8080/view/Jupiter/view/Cucumber-All/job/" + job + "/buildWithParameters/", auth=('cmuser', str(sys.argv[1])))
#        print status[0] + "is older than 1 day"
         rc = 999
    if status[2] == u'FAILURE' :
#        print status[0] + " failed"
         rc = 999
#   status(1) = time_now - status(1)
    #print round((time_now - status[1])/3600000.0,2) , status[0], status[2] , "<br>"
sys.exit(0)