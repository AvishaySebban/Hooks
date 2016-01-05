#!/usr/bin/python
import os

with open("output.txt", "w") as a:
    for path, subdirs, files in os.walk(r'/asaban/bulids/dmsp/dmsp-python-modules/src/main/dmsp-python-modules/lib/Test'):
       for filename in files:
         f = os.path.join(path, filename)
         a.write(str(f) + os.linesep)
         print filename
         
		 
		
