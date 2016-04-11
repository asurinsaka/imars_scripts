#!/usr/bin/python
import sys
import os
import getopt
from pyhdf import SD
import numpy as np
import png
import itertools
import math
#from os.path import basename
#import scipy

class PngGenerator:
    filename = ""
    mask_filename =""
    calculation = ""
    out_filename = ""
    north = 90.0
    east = 180.0
    south = -90.0
    west = -180.0

    def __init__(self, filename, mask_filename, calculation, output, north=90.0, east=180.0, south=-90.0, west=-180.0):
        calculation = calculation.replace('\\', '')
        self.filename = filename
        self.mask_filename = mask_filename
        self.calculation = calculation
        self.out_filename = output
        self.north = north
        self.south = south
        self.east = east
        self.west = west

    def setCoordinates(self, north=90.0, east=180.0, south=-90.0, west=-180.0):
        self.north = north
        self.south = south
        self.east = east
        self.west = west

    def applyMask(self, data):
        self.data = data
        mask_file = png.Reader(filename=self.mask_filename)
        column_count, row_count, mask, meta = mask_file.read()

        image_2d = np.vstack(itertools.imap(np.uint16, mask))
        print "Applying land mask"
        #This is the fastest
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if image_2d[i,j] > 251 or data[i,j] < 0 or np.isnan(data[i,j]) or math.isnan(data[i,j]):
                    data[i,j] = image_2d[i,j]
        self.palette = mask_file.palette()
        return self.data, self.palette


    def savePNG(self, data, palette):
        print "Saving file"
        file = open(self.out_filename, 'wb')
        writer = png.Writer(data.shape[1], data.shape[0],palette=palette)
        writer.write(file, data)
        file.close()

    def getPixelResolution(self, max, min, length):
        return float((max - min))/length

    def centerCoordinates(self, north, east, south, west, delta_lat, delta_lon):
        new_north = north - delta_lat / 2.
        new_south = south + delta_lat / 2.
        new_west = west + delta_lon / 2.
        new_east = east - delta_lon / 2.
        return new_north, new_east, new_south, new_west

    def getNewLimits(self, width, height, new_north, new_east, new_south, new_west):
        delta_lat = self.getPixelResolution(self.north, self.south, height)
        delta_lon = self.getPixelResolution(self.east, self.west, width)


        lat_north, lon_east, lat_south, lon_west = self.centerCoordinates(self.north, self.west, self.south, self.east, delta_lat, delta_lon)
        new_north, new_east, new_south, new_west = self.centerCoordinates(new_north, new_west, new_south, new_east, delta_lat, delta_lon)

        lin_north = 1
        lin_south = height
        pix_east = width
        pix_west = 1

        # define the starting and ending pixel-line numbers for the box of interest
        tmp_spix = float(pix_west + (pix_east - pix_west) * (new_west - lon_west) / (lon_east - lon_west))
        # tmp_spix=float((new_west - lon_west) / delta_lon)#float(pix_west+(pix_east-pix_west)*(new_west-lon_west)/(lon_east-lon_west))
        spix = max([pix_west, round(tmp_spix)])
        tmp_epix = float(pix_west + (pix_east - pix_west) * (new_east - lon_west) / (lon_east - lon_west))
        # tmp_epix=float((new_east - lon_west) / delta_lon) + 1#float(pix_west+(pix_east-pix_west)*(new_east-lon_west)/(lon_east-lon_west))
        epix = min([pix_east, round(tmp_epix)])
        tmp_slin = float(lin_south - (lin_south - lin_north) * (new_north - lat_south) / (lat_north - lat_south))
        # tmp_slin=float((lat_north - new_north) / delta_lat)#float(lin_south-(lin_south-lin_north)*(new_north-lat_south)/(lat_north-lat_south))
        slin = max([lin_north, round(tmp_slin)])
        tmp_elin = float(lin_south - (lin_south - lin_north) * (new_south - lat_south) / (lat_north - lat_south))
        # tmp_elin=float((lat_north - new_south) / delta_lat) + 1#float(lin_south-(lin_south-lin_north)*(new_south-lat_south)/(lat_north-lat_south))
        elin = min([lin_south, round(tmp_elin)])
        return slin, spix, elin, epix

    def cutPng(self, sds, new_north, new_east, new_south, new_west, top=255, bottom=0, no_data=np.NaN, valid_max=np.NaN, valid_min=np.NaN):
        data = self.getData(sds)

        height = data.shape[0]
        width = data.shape[1]

        slin, spix, elin, epix = self.getNewLimits(width, height, new_north, new_east, new_south, new_west)

        data = data[slin : elin , spix :epix ]#data[0:height - 1,]

        if(not np.isnan(valid_max)):
            data[np.where(data > valid_max)] = no_data

        if(not np.isnan(valid_min)):
            data[np.where(data < valid_min)] = no_data

        no_data_positions = np.where(data == no_data)

        #Transform data to calculation
        exec "data=np.around(" + self.calculation + ")"

        if(top != np.NaN):
            data[np.where(data > top)] = top

        if(bottom != np.NaN):
            data[np.where(data < bottom)] = bottom

        if(no_data_positions != np.NaN):
            data[no_data_positions] = 251

        data, palette  = self.applyMask(data)
        self.savePNG(data, palette)


    def generatePng(self,sds, top=255, bottom=0, no_data=np.NaN, valid_max=np.NaN, valid_min=np.NaN):
        data = self.getData(sds)

        if(not np.isnan(valid_max)):
            data[np.where(data > valid_max)] = no_data

        if(not np.isnan(valid_min)):
            data[np.where(data < valid_min)] = no_data

        no_data_positions = np.where(data == no_data)

        #Transform data to calculation
        exec "data=np.around(" + self.calculation + ")"

        if(top != np.NaN):
            data[np.where(data > top)] = top

        if(bottom != np.NaN):
            data[np.where(data < bottom)] = bottom

        if(no_data_positions != np.NaN):
            data[no_data_positions] = 251

        data, palette  = self.applyMask(data)
        self.savePNG(data, palette)

    def getData(self, sds):
        path, ext = os.path.splitext(self.filename)
        if ext in (".hdf", ".hdf4", ".HDF", ".HDF4"):
            return self.getHDFData(sds)

    def getHDFData(self, sds):
        # open the hdf file for reading
        hdf=SD.SD(self.filename)
        # read the sds data
        sds=hdf.select(sds)
        data=sds.get()
        return data



def usage():
    print "-h --help  Display this help"
    print "-f --file  Input file"
    print "-o --output Output filename"
    print "-m --mask_file  File containing the png mask"
    print "-s --sds Name of the product to generate the png"
    print "-c --calculation Equation to calculate the pixel to value relation, should include data keyword"
    print "-t --top Top value to use in the color index"
    print "-b --bottom Bottom value to use in the color index"
    print "-n --no_data No data value"
    print "-u --max_data Maximum valid data value"
    print "-l --min_data Minimum valid data value"

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:m:c:o:s:t:b:n:u:l:a:d:e:g:w:x:y:z:", ["help", "file=", "mask_file=", "calculation=", "output=", "sds=", "top=","bottom=","no_data", "max_data", "min_data"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    top = 255
    bottom = 0
    no_data=np.NaN
    max_data=np.NaN
    min_data=np.NaN

    original_north=np.NaN
    original_east=np.NaN
    original_south=np.NaN
    original_west=np.NaN

    north=np.NaN
    east=np.NaN
    south=np.NaN
    west=np.NaN

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-f", "--file"):
            file = arg
        elif opt in ("-m", "--mask_file"):
            mask_file = arg
        elif opt in ("-c", "--calculation"):
            calculation = arg
        elif opt in ("-o", "--output"):
            output = arg
        elif opt in ("-s", "--sds"):
            sds = arg
        elif opt in ("-t", "--top"):
            top = float(arg)
        elif opt in ("-b", "--bottom"):
            bottom = float(arg)
        elif opt in ("-n", "--no_data"):
            no_data = float(arg)
        elif opt in ("-u", "--max_data"):
            if(arg == 'NaN'):
                max_data = np.NaN
            else:
                max_data = float(arg)
        elif opt in ("-l", "--min_data"):
            if(arg == 'NaN'):
                min_data = np.NaN
            else:
                min_data = float(arg)
        elif opt in ("-a"):
            original_north = float(arg)
        elif opt in ("-d"):
            original_east = float(arg)
        elif opt in ("-e"):
            original_south = float(arg)
        elif opt in ("-g"):
            original_west = float(arg)
        elif opt in ("-w"):
            north = float(arg)
        elif opt in ("-x"):
            east = float(arg)
        elif opt in ("-y"):
            south = float(arg)
        elif opt in ("-z"):
            west = float(arg)


    generator = PngGenerator(file,mask_file,calculation, output)
    if(not np.isnan(original_north) and not np.isnan(original_east) and not np.isnan(original_south) and not np.isnan(original_west) and not np.isnan(north) and not np.isnan(east) and not np.isnan(south) and not np.isnan(west)):
        generator.setCoordinates(original_north, original_east, original_south, original_west)
        generator.cutPng(sds, north, east, south, west, top, bottom, no_data, max_data, min_data)
    else:
        generator.generatePng(sds, top, bottom, no_data, max_data, min_data)

         #/home1/gabyq/PycharmProjects/imars/test_data/1994to2012/multiple.1994to2012.44week.gcoos.sst.std.png -h 7.0 -l 2.0 -b (data+2.1)/0.1992 -d 0.1992*byte-2.1 -m /home1/gabyq/PycharmProjects/imars/wrapper/masks/sst_gcoos_mask.png
