#!/usr/bin/python
# Author: Asurin

import sys
import os
from optparse import OptionParser
import png


def flawed_file(file, empty_lines):
    count = 0       # counts totla number of empty lines
    data_file = png.Reader(filename=file)
    column_count, row_count, data, meta = data_file.read()
    for line in list(data):
        empty_line = True
        for color in line:
            if color < 250 and color != 11:
                empty_line = False
        if empty_line:
            count += 1
        else:
            count = 0

        if count >= empty_lines:
            return True

    return False

if __name__ == "__main__":

    print '''This is a python script to find flawed
png pictures'''
    print '\n'


    # Read commandLine options...
    version = "%prog 0.1"
    usage = '''usage: %prog [options] /dir'''

    parser = OptionParser(usage=usage, version=version)

    parser.add_option("-q", "--quiet", action="store_false", dest="verbose",
            default=True, help="Little Miss Chatterbox...")
    parser.add_option("-f", "--file", action="store",type="string",
            dest="filename", help="Save the output to a file")
    parser.add_option("-l", "--line", action="store", type="int",
            dest="lines", default=200, help="number of empty lines to check")

    (options, args) = parser.parse_args()

    # This program only check 1 location at a time
    if len(args) == 1:
        png_dir = args[0]
    else:
        parser.error("Wrong number of arguments")

    # find write the output file
    output_file = ""
    if options.filename:
        if os.path.exists(options.filename):
            print "The file "+options.filename+" already exists!"
            var = raw_input("Overwrite?(y/N)")
            if var != "y":
                sys.exit(1)
        output_file = open(options.filename, 'w')

    # number of empty_lines
    empty_lines = options.lines


    # make sure the directory is correct
    if not os.path.isdir(png_dir):
        print "The directory " + png_dir + " dose not exists!"
        sys.exit(1)

    # find the files and check them
    for root, dirs, files in os.walk(png_dir):
        if len(files)>0:
            files = [ x for x in files if ".png" in x ]
            for file in files:
                # output record in output_file and/or on screen
                file = root + file
                if(flawed_file(file, empty_lines)):
                    if output_file:
                        output_file.write(file)
                    if options.verbose:
                        print file

    if output_file:
        output_file.close()



