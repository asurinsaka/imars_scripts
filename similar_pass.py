#!/usr/bin/python
# Author: Asurin


import sys
import os
from optparse import OptionParser
from datetime import datetime, timedelta
from hashlib import md5


def compare(root, filea, fileb, do_compare):
    if not do_compare:
        return True
    else:
        return md5(open(root+'/'+filea, 'rb').read()).digest() == \
               md5(open(root+'/'+fileb, 'rb').read()).digest()


if __name__ == "__main__":


    print '''This is a python script to find similar passes of
final products from NASA'''
    print '\n'

    # Read commandLine options...
    version = "%prog 0.2"
    usage = '''usage: %prog [options] /dir'''

    parser = OptionParser(usage=usage, version=version)

    parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True,
                        help="Little Miss Chatterbox...")
    parser.add_option("-f", "--file", action="store", type="string", dest="filename",
                      help ="Save the output to a file")
    parser.add_option("-c", "--compare", action="store_true", dest="compare",
                      help ="Check to see if files are the same")
    parser.add_option("-e", "--extention", action="store", dest="extension", default="png",
                      help ="check files with this extension only, default=png")

    (options, args) = parser.parse_args()

    if len(args) == 1:
        root_dir = args[0]
    else:
        parser.error("Wrong number of arguments")


    # find write the output file
    if options.filename:
        if os.path.exists(options.filename):
            print "The file "+options.filename+" already exist!"
            var = raw_input("Overwrite?(y/N)")
            if var != "y":
                sys.exit(1)
        output_file = open(options.filename, 'w')


    # make sure the directory is correct
    if not os.path.isdir(root_dir):
        print "The directory " + root_dir + " does not exists!"
        sys.exit(1)


    # find  files in the each subdirectories and compare their names
    for root, dirs, files in os.walk(root_dir):
        if len(files)>1:
            files = [ x for x in files if options.extension in x ]
            files.sort()
            for i in range(len(files)-1):
                filea = files[i].split('.')
                fileb = files[i+1].split('.')
                if filea[0] == fileb[0] and filea[3] == fileb[3] and \
                    filea[4] == fileb[4] and filea[5] == fileb[5]:
                    timea = datetime(*map(int, [filea[1][:4], filea[1][4:6], filea[1][6:],
                                     filea[2][:2], filea[2][2:]]))
                    timeb = datetime(*map(int, [fileb[1][:4], fileb[1][4:6], fileb[1][6:],
                                     fileb[2][:2], fileb[2][2:]]))
                    if timeb - timea == timedelta(seconds=300) and compare(root, files[i], files[i+1], options.compare):
                        if options.filename:
                            output_file.write(root+'/'+files[i+1]+'\n')
                        if options.verbose:
                            print root+'/'+files[i+1]

    if options.filename:
        output_file.close()
