#!/usr/bin/env python

from optparse import OptionParser
import os
import sys
import urllib
import platform
import subprocess


class cp_files():
    def __init__(self, files, dest):
        self.files = files
        self.dest = dest
        self.id = []
        self.count = 0
        self.cwd = os.getcwd()
        self.check_gdrive()

    def get_auth(self):
        # print self.gdrive
        # print "{0} list".format(self.gdrive)
        print "Try to list 1 file to check whether your token file works."
        subprocess.call("{0} list -m 1".format(self.gdrive), shell=True)

    def check_gdrive(self):
        """Check whether gdrive command line tool is downloaded,
        If not, download it"""
        if 'Windows' == platform.uname()[0]:
            self.gdrive = os.path.join(self.cwd, 'gdrive.exe')
            if not os.path.isfile(self.gdrive):
                urllib.urlretrieve("https://drive.google.com/uc?id=0B3X9GlR6EmbnbnBsTXlfS1J5UjQ&export=download", 'gdrive.exe')
        elif "Linux" == platform.uname()[0]:
            self.gdrive = os.path.join(self.cwd, 'gdrive')
            if not os.path.isfile(self.gdrive):
                urllib.urlretrieve("https://docs.google.com/uc?id=0B3X9GlR6EmbnQ0FtZmJJUXEyRTA&export=download", 'gdrive')
                # st = os.stat(self.gdrive)
                # print st.st_mode, stat.S_IXUSR, st.st_mode | stat.S_IXUSR, type(st.st_mode | stat.S_IXUSR)
                os.chmod(self.gdrive, 0755)
        else:
            print "Your OS is not supported"
            sys.exit(1)
        self.get_auth()

    def get_file_id(self):
        """Get id of the files in the file list,
        We need those ids to download files."""

        print "Start getting file ids:"
        for file in self.files:
            cmd = "{0} list -q \"name contains '{1}'\"".format(self.gdrive, file)
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for line in process.stdout:
                file_id, file_name = line.split()[:2]
                if file_id != 'Id':
                    self.id.append(file_id)
                    self.count += 1
                    # print "{}\t{}\t{} \r".format(file_id, file_name, self.count)
                    sys.stdout.write("\r {0}\t{1}\t{2}".format(file_id, file_name, self.count))
                    sys.stdout.flush()
        print "\n Finished Getting file ids"

    def download_files(self):
        print "Start Downloading files"
        total = self.count
        os.chdir(self.dest)
        for id in self.id:
            cmd = "{0} download {1}".format(self.gdrive, id)
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for line in process.stdout:
                if "Downloaded" in line or "Downloading" in line:
                    sys.stdout.write("\r {0} \t {1}/{2}".format(line.strip(), self.count, total))
                    sys.stdout.flush()
            self.count -= 1
        os.chdir(self.cwd)
        print "Finished Downloading files"



if __name__ == "__main__":
    print '''
    This is a python script to find and copy files from google drive with a list of file names.
    '''

    # Read command line opotions..
    version = "%prog 0.3"
    usage = '''usage: %prog input_file dest_dir'''

    parser = OptionParser(usage=usage, version=version)
    (options, args) = parser.parse_args()

    # can only copy to 1 location
    if len(args) == 2:
        input_file = args[0]
        dest_dir = args[1]
    else:
        parser.error("Please provide input file and destination folder.")

    # check exists of input file and get file names
    if not os.path.isfile(input_file):
        print "The file " + input_file + " does not exist!"
        sys.exit(1)
    else:
        with open(input_file, 'r') as f:
            filenames=f.read().splitlines()
        f.closed
        while '' in filenames:
            filenames.remove('')
        name_total = len(filenames)
    #print filenames


    # check the destination directory
    if not os.path.isdir(dest_dir):
        print
        "The destination directory" + dest_dir + " does not exist!"
        sys.exit(1)

    cp = cp_files(filenames, dest_dir)

    cp.get_file_id()
    cp.download_files()
