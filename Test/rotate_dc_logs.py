#!/usr/bin/python
import os, sys
import shutil
import glob
import argparse
from uploadToS3 import *
from django.template.defaultfilters import default
from __builtin__ import file

def logRotate(sourcePath,destPath):
    if not os.path.exists(sourcePath):
        print ("The source folder does not exist [%s]" % sourcePath)
        return 1
    counter=0
    for filename in os.listdir(sourcePath): #for path, subdirs, files in os.walk(r'/var/logs'):
	counter=counter+1
        if filename.startswith("data-collect-REST__"):
            #Log Example: "data-collect-REST__HEALTHCECK_REQUEST.2015-01-20-07-24.log.gz"
            logPrefix=logPrefix_data_collect_REST="data-collect-REST__"
            logType="0"
        elif filename.startswith("data-collect-INT__"):
            logPrefix=logPrefix_data_collect_INT="data-collect-INT__"
            logType="1"
        elif filename.startswith("data-collect-RPC__"):
            logPrefix=logPrefix_data_collect_RPC="data-collect-RPC__"
            logType="2"
        else:
            continue
        
        basename = filename.split(".") # basename = ['data-collect-REST__HEALTHCECK_REQUEST', '2015-01-20-07-24', 'log', 'gz']

        #dirDate = basename[1].replace("-", "")[:8] #Output: "20150224" 
        dirDate = basename[1][:10] #Output: "2015-02-24"
        ApiName = basename[0].replace(logPrefix, "") #Output: "HEALTHCECK_REQUEST"
        newLogPath = destPath + "/" + logType + "/" + dirDate + "/" + ApiName
        # Create dist folder
        if not os.path.exists(newLogPath):
            os.makedirs ( newLogPath )
            print ("Folder [%s] was created" % newLogPath)
        
        src_file = os.path.join(sourcePath, filename)
        # Move File
        shutil.move(os.path.join(sourcePath + "/" + filename),newLogPath) #mv the file 
        print ("The file was moved from [%s] to [%s]" % (src_file,newLogPath))

    return counter # 0 - no files to rotate

def moveLogsToArchive(src,dest):

    if not os.path.exists(src):
        print ("Folder [%s] does not exists" % src)
        return 1

    if not os.path.exists(dest):
        os.makedirs ( dest )
        print ("Folder [%s] was created" % dest)

    for type_dir in os.listdir(src): # for each type dir
        if os.path.isdir(os.path.join(src, type_dir)):
            src_type_dir=os.path.join(os.path.join(src, type_dir))
            for date_dir in os.listdir(src_type_dir):
                if os.path.isdir(os.path.join(src_type_dir, date_dir)):
                    dest_dir=os.path.join(os.path.join(src_type_dir, date_dir))
                    shutil.move(dest_dir,dest) 
                    print ("The folder was moved from [%s] to [%s]" % (dest_dir,dest))
    return

def exitFunction(msg):
  print (msg) 
  exit (1)
  return
 
def createListOfArchivedFiles(pathToList):
    listFilesToUpload = pathToList + ".list"
    f = open(listFilesToUpload,'w')
    for dirpath, dirnames, files in os.walk(pathToList):
        for filename in files:
            results = os.path.join(dirpath, filename)
            # Write results to logfile
            f.write(results + "\n")
    return listFilesToUpload

def getAwsParamsFromZoo():
    
    awsEndpoint= "s3-us-west-2.amazonaws.com" 
    awsBucket= "lab-test-log-dc" 
    awsUser="AKIAJ6P3OIYAWLS2KEIQ"
    awsPass="eqF66qG8w73nrMA5rq4Uxi4LIlyqoUVzgZUDAKgU"
    
    return awsEndpoint, awsBucket, awsUser, awsPass

def uploadToS3(pathToUpload): 
  awsEndpoint, awsBucket, awsUser, awsPass = getAwsParamsFromZoo()
  listToUpload = createListOfArchivedFiles(pathToUpload)
  uploadListToS3(listToUpload,awsUser, awsPass, awsBucket,awsEndpoint,"3")
  
  return
  
  #Main

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--source", type=str, default="/var/logs", help="The logs source path in order to rotate")
    parser.add_argument("-s3","--uploadToS3", action="store_true", help="The logs source path in order to rotate")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
    args = parser.parse_args()

    logicalPath = args.source + "/archive_dc"
    rotatePath = args.source + "/archive"

            
    if args.verbose :
        print ("Source: [%s]" % args.source)

    #Source
    numOfFiles = logRotate(args.source,logicalPath)
	
    #UploadToS3
    if args.uploadToS3 and (numOfFiles > 0) :
        uploadToS3(logicalPath)
    
	#Move to archived dir (other process will maintain this files)
	if numOfFiles > 0:
	    moveLogsToArchive(logicalPath,rotatePath) 

    return
        
           
if __name__ == "__main__":
    main()
