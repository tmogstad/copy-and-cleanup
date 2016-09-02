#!/usr/bin/env python

#Copyright (c) 2016 Data Equipment AS
#Author: Tor Mogstad <torm _AT_ dataequipment.no>

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
"""Script consists of two methods. One for copying files, and one for cleanup.

The copy method copies files from a source folder to several destinationfolders
based on filenames. Method also checks if file aldready exists in destination.

Cleanup method will delete all files in source and destination folder,
except for the x newest files based on timestamps. x is defined in global
variable RETENTION.

"""


import fnmatch
import os
import glob
import shutil
import operator
import argparse
import logging

# List of destination folder names. Theese must be subfolders under DESTINATIONFOLDER
PACKAGE = {
    "panupv2-all-contents",
    "panupv2-all-apps",
    "panup-all-antivirus",
    "panup-all-wildfire",
    "panupv2-all-wildfire",
    "panup-all-wfmeta",
}
SOURCEFOLDER = "/home/tor/script/content-install/files/" # Folder where original files are located
DESTINATIONFOLDER = "/home/tor/script/content-install/contentuploader/" #Root folder where files are copied.
RETENTION = 2  # Number of files to keep for each package type


def find_files(pattern):
    files = []
    for current_file in os.listdir('./files'):
        if fnmatch.fnmatch(current_file, '*%s*' % (pattern)):
            timestamp = key=os.path.getctime
            files.append(current_file)
    return files

# Copy all new files matching a packe name from sourcefolder to subfolders in destinationfolder


def copy_files(verbose):
    for content_type in PACKAGE:
        logging.info("Copy files in directory %s" % (SOURCEFOLDER))
        # Loop through all files in SOURCEFOLDER
        for current_file in os.listdir(SOURCEFOLDER):
            # Move file to correct folder if filename contains a package-name
            if fnmatch.fnmatch(current_file,'*%s*' % (content_type)):
                copy = True # Copy file is default
                src_folder_file = SOURCEFOLDER + current_file
                dst_folder_file = "%s%s/%s" % (DESTINATIONFOLDER, content_type, current_file)
                for dest_file in os.listdir("%s%s" % (DESTINATIONFOLDER, content_type)):
                    if dest_file == current_file: copy = False  # If filenames matches, don't copy file.
                #Copy if we have'ent find same file in destinationfolder
                if copy:
                    shutil.copy(src_folder_file, dst_folder_file)
                    if verbose: logging.debug("Moving file %s from %s to %s" % (current_file,src_folder_file,dst_folder_file))

""" Cleans up subfolders under DESTINATIONFOLDER. Delets all files containing package-name,
    except the number of files in RETENTION variable. """


def cleanup_files(verbose):
    # Run for each packe type
    logging.info("Cleaning up directory %s" % (SOURCEFOLDER))
    for content_type in PACKAGE:
        files = []
        folder = DESTINATIONFOLDER + content_type
        logging.info("Cleaning up directory %s and %s for files matching %s" % (folder, SOURCEFOLDER, content_type))
        # Loop through all files in folder
        for current_file in os.listdir(folder):
            # If filename matches package name, add it to a list with name and timestamp
            if fnmatch.fnmatch(current_file, '*%s*' % (content_type)):
                timestamp = os.path.getmtime(DESTINATIONFOLDER + content_type + "/" + current_file)
                files.append([current_file, timestamp])
        # Sort list with files based on timestamp
        files = sorted(files, key= operator.itemgetter(1))  # sort list by timestamp
        # Get lenght of list and set variables used to delete files
        files_lenght = len(files)
        items_to_remove = files_lenght - RETENTION
        next_index_to_remove = items_to_remove - 1 #since list index starts at 0
        # Delete all files in list, except the x newest based on RETENTION variable
        while items_to_remove > 0:
            filename  = files[next_index_to_remove][0]
            filepath_dst = DESTINATIONFOLDER + content_type + "/" + filename
            filepath_src = SOURCEFOLDER + filename
            if verbose: logging.debug("Deleting files %s and %s" % (filepath_src,filepath_dst))
            os.remove(filepath_dst)
            os.remove(filepath_src)
            next_index_to_remove = next_index_to_remove - 1
            items_to_remove = items_to_remove - 1

def enable_logging(options):
    # Logging
    if options.verbose is not None:
        if options.verbose == 1:
            logging_level = logging.INFO
            logging_format = ' %(message)s'
        else:
            logging_level = logging.DEBUG
            logging_format = '%(levelname)s: %(message)s'
        logging.basicConfig(format=logging_format, level=logging_level)
    return True if options.verbose > 1 else False

def parse_arguments():
    parser = argparse.ArgumentParser(description='Move downloaded content files, and cleanup destiantion directory to just keep x number of files')
    parser.add_argument('-v', '--verbose', action='store_true', help="Turn on Debug mode. Logs actions prompt")
    return parser.parse_args()



def main():
    #Parse input arguments
    options = parse_arguments()
    #Turn on logging
    enable_logging(options)
    if options.verbose: verbose = True
    else: verbose = False
    #Move files from source to destination folders
    copy_files(verbose)
    #Clean up destination directories
    cleanup_files(verbose)


if __name__ == '__main__':
        main()
