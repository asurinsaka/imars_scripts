#/usr/bin/python
#this program generate center_lat and center_lon for mapping_configs/*.cfg files for true colors.

import glob, os, re

class AddCenter(object):
    filename = ''
    lines = ''
    center_lat = 0.0
    center_lon = 0.0


    def __init__(self, filename):
        self.filename=filename;


    def read_file(self):
        with open(self.filename, 'r') as f:
            self.lines = f.readlines()
            f.close()

    def rewrite_centers(self):
        p = re.compile('center*')
        with  open(self.filename, 'w') as f:
            for line in self.lines:
                if not p.match(line):
                    f.write(line)
            f.write("center_lat = "+str(self.center_lat)+'\n')
            f.write("center_lon = "+str(self.center_lon)+'\n')
            f.close()

    def load_parms(self):
        for line in self.lines:
            s = line.split()
            if len(s) > 0:
                parameter = s[0]
                if parameter == "latmin":
                    latmin = float(s[len(s) - 1])
                elif parameter == "latmax":
                    latmax = float(s[len(s) - 1])
                elif parameter == "lonmin":
                    lonmin = float(s[len(s) - 1])
                elif parameter == "lonmax":
                    lonmax = float(s[len(s) - 1])
        self.center_lat = (latmin + latmax) / 2
        self.center_lon = (lonmin + lonmax) / 2

    def write_centers(self):
        self.read_file();
        self.load_parms();
        self.rewrite_centers();


os.chdir("./mapping_configs")
cwd = os.getcwd()
print cwd

for file in glob.glob("*.cfg"):
    ac = AddCenter(file)
    ac.write_centers();
