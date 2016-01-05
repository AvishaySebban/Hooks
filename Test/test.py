#!/usr/bin/python
import os, sys
import shutil
import glob
import argparse

sourcePath = "/var/logs"
logicalPath = sourcePath + "/archaive_dc_logs"

def logRotate(sourcePath):
    for filename in os.listdir(sourcePath): #for path, subdirs, files in os.walk(r'/var/logs'):
        if filename.startswith("data-collect-REST__"):
            #Log Example: "data-collect-REST__HEALTHCECK_REQUEST.2015-01-20-07-24.log.gz"
            logPrefix=logPrefix_data_collect_REST="data-collect-REST__"
            logType="0"
        elif filename.startswith("data-collect-RPC__"):
            logPrefix=logPrefix_data_collect_RPC="data-collect-RPC__"
            logType="1"
        elif filename.startswith("data-collect-INT__"):
            logPrefix=logPrefix_data_collect_RPC="data-collect-INT__"
            logType="2"
        else:
            continue
        
        basename = filename.split(".") # basename = ['data-collect-REST__HEALTHCECK_REQUEST', '2015-01-20-07-24', 'log', 'gz']
        #logPrefix = basename[0].split(".") #Output: "data-collect-REST"

        dirDate = basename[1].replace("-", "")[:8] #Output: "20150224" 
        ApiName = basename[0].replace(logPrefix, "") #Output: "HEALTHCECK_REQUEST"
        newLogPath = logicalPath + "/" + logType + "/" + dirDate + "/" + ApiName
        # Create dist folder
        if not os.path.exists(newLogPath):
            os.makedirs ( newLogPath )
            print ("Folder [%s] was created" % newLogPath)
        # Move File
        src_file = os.path.join(sourcePath, filename)
#      Force Move
#     dst_file = os.path.join(newLogPath, filename)
#     if not os.path.exists(dst_file):
#       os.remove(dst_file)
#        shutil.move(src_file, newLogPath)
        shutil.move(os.path.join(sourcePath + "/" + filename),newLogPath) #mv the file 
        print ("The file was moved from [%s] to [%s]" % (src_file,newLogPath))

#            Prefix = basename[0].split(".") #Output: "data-collect-REST"
            
            #2:             
            
            #DirName = basename[1].replace("data-collect-REST__", "") #Output: "2015-01-05-20-20"
        return

def exitFunction(msg):
  print (msg) 
  exit (1)
  return
  
  #Main

def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("-s","--source", type=str, help="Need source path in order to rotate: /var/logs/archive/")
        parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
        
       
        args = parser.parse_args()
        
        if args.verbose :
            print ("Source: [%s]" % args.source)
                
        if (not args.source ):
            exitFunction ("The Source is mandatory")
        
        #Source to rotate data collection
        if args.source :
             logRotate(args.source)
          
           
        
        return
        
           
if __name__ == "__main__":
    main()
