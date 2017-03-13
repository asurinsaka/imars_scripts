#!/usr/bin/env python

from optparse import OptionParser
import os
import sys
import re
from shutil import copyfile

def check_filename(file, namelist):
    match = False
    for name in namelist:
        if name == '':
            continue
        if re.match(name, file):
            #print "name", name
            #print file
            match = True
            break
    return match

if __name__ == "__main__":
    print '''
    This is a python script to find and copy files from a list of file names.

    '''

    # Read command line opotions..
    version = "%prog 0.1"
    usage = '''usage: %prog -s source_dir input_file dest_dir'''

    parser = OptionParser(usage=usage, version=version)

    parser.add_option("-s", "--source", action="store", type="string",\
                      dest="source_dir", help="Get the source directory")
    (options, args) = parser.parse_args()

    # can only copy to 1 location
    if len(args) == 2:
        input_file = args[0]
        dest_dir = args[1]
    else:
        parser.error("You only can have 1 destination folder. Please check usage.")

    # check exists of input file and get file names
    if not os.path.isfile(input_file):
        print "The file " + input_file + " does not exist!"
        sys.exit(1)
    else:
        with open(input_file, 'r') as f:
            filenames=f.read().splitlines()
        f.closed
        if '' in filenames:
            filenames.remove('')
        name_total = len(filenames)
    #print filenames

    # check source directory
    if options.source_dir:
        source_dir = options.source_dir
    else:
        source_dir = "/extra_data"
    if not os.path.isdir(source_dir):
        print "The source directory" + source_dir + " does not exist!"
        sys.exit(1)

    # check the destination directory
    if not os.path.isdir(dest_dir):
        print
        "The destination directory" + dest_dir + " does not exist!"
        sys.exit(1)

    file_count = 0
    for root, dirs, files in os.walk(source_dir):
        if len(files) > 0:
            for file in files:
                print root, dirs, file
                sys.stdout.write("%d Copied\t : %s   \r" % (file_count, root[:50]))
                sys.stdout.flush()
                if check_filename(file, filenames):
                    file_count+=1
                    copyfile(root+'/'+file, dest_dir+'/'+file)
    print "Copied ", file_count, " files"
