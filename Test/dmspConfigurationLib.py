#!/usr/bin/python

from dmspGenericLib import *
from dmspZookeeperLib import *
import argparse

######################################### 
# CONFIGURATION FUNCTIONS:				#
#########################################

# Main
def main():
 parser = argparse.ArgumentParser()
 parser.add_argument("zkParentKey", type=str, help="The configuration location in ZooKeeper e.g. /site, /site/<componentName>, etc.")
 parser.add_argument("confFileSource", type=str, help="The location of the configuration file to sync with 'zkConfPath'")
 parser.add_argument("--logFile", type=str, help="The location of the log file")
 parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
 args = parser.parse_args()
 
 if args.verbose :
  print ("The configuration location in ZooKeeper: [%s]" % args.zkConfPath)
  print ("The location of the configuration file to sync with zookeeper: [%s]" % args.confFileSource)
  print ("The location of the log file: [%s]" % args.logFile)

 # get Zookeeper tree
 zkWriteTreeToFile(zkParentKey,confFilePath,fileStatus)
 
 return
 
main()
