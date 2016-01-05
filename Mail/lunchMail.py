#!/usr/bin/python

import logging
from SendMail import *
from conf import *
import sys,os 
import time
from time import gmtime, strftime
from logging.handlers import RotatingFileHandler







def create_Alert(type,name,file):
    subject = "The alert type is: " + type + " for " + name + "."
    body = "BODY_TEXT_123"
    print ("%s" % subject)
    if type == 'WARNING' :
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!! - " + type
    elif type == 'CRITICAL' :
        print "++++++++++++++++++++++++++ - " + type
    result = sendMail(sender,reciever,subject,body,file,SMTP_SERVER)
    if result > 0 :
        print "Mail was not sent !"
    else :
        print "Mail was sent !"
    return
