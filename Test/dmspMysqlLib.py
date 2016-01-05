#!/usr/bin/python

import MySQLdb
import csv
import time
import datetime
from dmspZookeeperLib import *

#Open connection to database
def openConnection():
  env =  getEnv()
  dbuser, dbip, dbpassword = getDBConnectionDetails(env)
  con = MySQLdb.connect(host=dbip, user=dbuser, passwd=dbpassword)
  cur = con.cursor()
  return con,cur

#Closing connection to database
def closeConnection(con,cur):
   cur.close()
   con.close()
   return

#Getting db connection details
def getDBConnectionDetails(env):
   dbuser="root"
   if (env == "production"):
      dbip="dmsp.cx8qillzdedt.us-west-2.rds.amazonaws.com"
      dbpassword="rootproduction"
   else:
      if (env == "preprod"):
         dbip="pre-prod-dmsp-db.cjedaxbso5dk.us-west-2.rds.amazonaws.com"
         dbpassword="dmsproot1!"
      else:
         if (env == "e2e"):
            dbip="127.0.0.1"
            dbpassword="root"
         else:
            dbip="localhost"
            dbpassword="root"
   return dbuser, dbip, dbpassword
   
# The function execute SQL query and export its results to csv or print it to the screen
def execSelectQury(query, isHeaders, csv_full_path):
   #Check if executing select query
   if not query.lower().startswith("select"):
      print "This is not a select query"
      print "Exit..."
      return
   try:
      #Connecting to DB
      cnx, cursor = openConnection() 
      #Execute the query
      row_count=cursor.execute(query)
      if isHeaders.lower() == "true" and csv_full_path == "NONE":
        #print results headers
        print ([ i[0] for i in cursor.description ])
      elif isHeaders.lower() == "true" and not csv_full_path == "NONE":
        f = csv.writer(open(csv_full_path, "w"))
        f.writerow([ i[0] for i in cursor.description ]) 
      elif not isHeaders.lower() == "true" and not csv_full_path == "NONE":
        f = csv.writer(open(csv_full_path, "w"))
      for row_count in cursor.fetchall():
        if not csv_full_path == "NONE":
          #write to csv
          f.writerow(row_count)
        else:
          print row_count
   except Exception,e:
      print e
   finally:
      closeConnection(cnx,cursor)
   return

def execSQLFile(sql_file):
   con,cur = openConnection()
   errorOccur = "false"
   total_start_time = int(time.time() * 1000)
   for line in open(sql_file):
      if not line.startswith("--"):
         print(line)
         start_time = int(time.time() * 1000)
         try:
            cur.execute(line)
            con.commit()
         except Exception,e:
            print str(e)
            errorOccur = "true"
         end_time = int(time.time() * 1000) 
         exec_time = end_time - start_time
         print("Completed in %d ms" % exec_time)
         print ("affected rows: %d" %(cur.rowcount))
         print ("=========================")
   total_end_time = int(time.time() * 1000)
   closeConnection(con,cur)
   print ("Script completed in %d ms" % (total_end_time - total_start_time))
   if errorOccur == 'true':
      print "\n\n\n=======================================\nError occure, view script log ! ! !\n==============================================="
