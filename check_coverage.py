#!/usr/bin/python
import re
import sys
import getopt
import os
import subprocess
import h5py
import numpy as np
import multiprocessing

class CheckCoverage:
    coords = []
    data_file = ""
    covered = "false"
    lat_name = "latitude"
    lon_name = "longitude"
    north = 90
    south = -90
    east = 180
    west = -180
    covered = False

    def __init__(self, north=90, south=-90, east=180, west=-180, lat_name=None, lon_name=None):
        if (lat_name != None):
            self.lat_name = lat_name
        if (lon_name != None):
            self.lon_name = lon_name
        self.north = north
        self.south = south
        self.east = east
        self.west = west

    def check(self, ifile):
        # does executable exist?
        mimecmd = ['file', '--brief', ifile]
        mime = subprocess.Popen(mimecmd, stdout=subprocess.PIPE).communicate()[0]

        if re.search('Hierarchical.*version.5', mime):
            self.check_hdf5(ifile)
        else:
            self.check_hdf4(ifile)

    def check_hdf5(self, ifile):
        lats = self.get_hdf5_array(ifile, self.lat_name)
        lons = self.get_hdf5_array(ifile, self.lon_name)
        if not self.check_line_limits(lats, lons):
            return self.covered

        pool = multiprocessing.Pool(10)

        def check_line(self, lons, lats):
            if not self.check_line_limits(lons, lats):
                pass
            else:
                if self.check_points(lons, lats):
                    self.covered = True
                    pool.terminate()
            return self.covered

        for i in range(len(lats)):
            pool.apply_async(check_line,(lons[i], lats[i]))
        pool.close()

        pool.join()
        return self.covered



    # check the limits of the array
    def check_line_limits(self, lons, lats):
        #asurin 011017: adding those lines to remove negtive result fast
        max_lons = np.amax(lons)
        min_lons = np.amin(lons)
        max_lats = np.amax(lats)
        min_lats = np.amin(lats)
        if max_lons < self.west or min_lons > self.east or max_lats < self.south or min_lats > self.north:
            return False
        else:
            return True

    def check_points(self, lons, lats):
        for x in zip(lons, lats):
            if self.west <= x[0] <= self.east and self.south <= x[1] <= self.north:
                return True
            else:
                return False

    def get_hdf5_array(self, ifile, array_name):
        data = h5py.File(ifile, 'r')
        for name in array_name.split("/"):
            if name != '':
                data = data[name]
        return data

    def check_hdf4(self, ifile):
        lats = [float(x) for x in self.get_data_array(ifile, self.lat_name)]
        lons = [float(x) for x in self.get_data_array(ifile, self.lon_name)]
        coords = zip(lons, lats)

        if not self.check_line_limits(lons, lats):
            return False

        covered = False
        for x in coords:
            if self.west <= x[0] <= self.east and self.south <= x[1] <= self.north:
                covered = True
                break
        return covered


    # Dump the array specified
    def get_data_array(self, ifile, array_name):
        # does executable exist?
        mimecmd = ['file', '--brief', ifile]
        mime = subprocess.Popen(mimecmd, stdout=subprocess.PIPE).communicate()[0]

        if re.search('Hierarchical.*version.4', mime):
            hdp = os.path.join(os.getenv('LIB3_BIN'), 'hdp')
            if not (os.path.isfile(hdp) and os.access(hdp, os.X_OK)):
                print hdp, "is not executable."
                return None

            # dump file header
            cmd = [hdp, 'dumpsds', '-d', '-n', array_name, ifile]
            f = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
            contents = f.read()

            return contents.split()
        # Asurin: removed here
        # elif re.search('Hierarchical.*version.5', mime):
        #     data = h5py.File(ifile, 'r')
        #     for name in array_name.split("/"):
        #         if name != '':
        #             data = data[name]
        #     return data.value.reshape(data.maxshape[0] * data.maxshape[1])
        elif re.search('NetCDF Data Format', mime):
            ncdump_hdf = os.path.join(os.getenv('LIB3_BIN'), 'ncdump_hdf')
            if not (os.path.isfile(ncdump_hdf) and os.access(ncdump_hdf, os.X_OK)):
                print ncdump_hdf, "is not executable."
                return None
            cmd = ' '.join([ncdump_hdf, '-h', ifile])
            f = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()
            return f[0].split('\n')
        else:
            print "File format not recognized"


def usage():
    print('check_coverage.py -n <north_lat> -s <south_lat> -e <east_lon> -w <west_lon> -i <infiles>')
    print('infiles can be multiple files separated by commas. Ex file1,file2,file3')

if __name__ == "__main__":
    argv = sys.argv[1:]
    north = "-999"
    south = "-999"
    west = "-999"
    east = "-999"
    lat_name = None
    lon_name = None
    data_files_str = ""

    try:
        opts, args = getopt.getopt(argv, "hn:s:w:e:v:l:i:",
                                   ["north=", "south=", "west=", "east=", "ifiles=", "lat=", "lon="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(
                "check_coverage.py -n <north_lat> -s <south_lat> -e <east_lon> -w <west_lon> [-v latitude_name -l longitude_name] -i <infiles>")
            sys.exit()
        elif opt in ("-v", "--lat"):
            lat_name = arg
        elif opt in ("-l", "-lon"):
            lon_name = arg
        elif opt in ("-n", "--north"):
            north = float(arg)
        elif opt in ("-s", "--south"):
            south = float(arg)
        elif opt in ("-w", "--west"):
            west = float(arg)
        elif opt in ("-e", "--east"):
            east = float(arg)
        elif opt in ("-i", "--infiles"):
            data_files_str = arg

    data_files = data_files_str.split(",")
    objCheckCoverage = CheckCoverage(north, south, east, west, lat_name, lon_name)
    print "needed_files=" + " ".join([f for f in data_files if os.path.isfile(f) and objCheckCoverage.check(f)])

