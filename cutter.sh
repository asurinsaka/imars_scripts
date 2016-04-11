#!/bin/bash
base=/imars_data/avhrr/husf/daily/1km/sst/fullpass_hdf/

for year in {1993..2016}
do
  for month in {01..12}
  do
    dated_folder=$year.$month
    mkdir $dated_folder
    for file in $base/$dated_folder/*hdf
    do
      out_filename=$dated_folder/`basename $file | sed 's/hdf/png/g'`
      ~/PycharmProjects/imars/algorithm/PngGenerator.py -f $file -m /imars_data/masks/sst_east_caribbean_mask.png -c data -o $out_filename -s mcsst -n 0 -l NaN -u NaN -a 55 -d -45 -e -5 -g -125 -w 16 -x -58 -y 8 -z -77
    done
  done
done
#~/PycharmProjects/imars/algorithm/PngGenerator.py -f /imars_data/avhrr/husf/daily/1km/sst/fullpass_hdf/2015.01/n19.20150131.1943.usf.sst.hdf -m /imars_data/masks/sst_venezuela_scar_mask.png -c data -o n19.20150131.1943.usf.sst.png -s mcsst -n 0 -l NaN -u NaN -a 55 -d -45 -e -5 -g -125 -w 16 -x -58 -y 8 -z -77
