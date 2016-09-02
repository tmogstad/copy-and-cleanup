# copy-and-cleanup
Script copies files from a source folder to several destinationfolders
based on defined filenames. Method also checks if file aldready exists in destination.

In addition, script will delete all files matching filename definition in source and destination folder,
except for the x newest files based on timestamps. 

##Installation and configuration
Install instructions are for linux only.
Download copy_and_cleanup.py and install dependencies if needed. Script used the following python repos:
* fnmatch
* os
* glob
* shutil
* operator
* argparse
* logging

Change the following global variables inside copy_and_cleanup.py, to match your environment
```
PACKAGE = { } # Folder names under DESTINATIONFOLDER path, where files will be copied. 
SOURCEFOLDER = "/home/user/xxx" # path where original files are located
DESTINATIONFOLDER = "/home/user/xxx/destination" #Root folder where files are copied.
RETENTION = 2  # Number of files to keep for each package type
````
#Usage
Simply execute .py file without any arguments.

Optional arguments
* -v - Verbose. Prints status messages to stdout
