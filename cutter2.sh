#!/bin/bash
for f in n19avhrr_new/*
do
        file=$(basename "${f%.*}")
        year=${file:4:4}
        month=${file:8:2}
        python PngGenerator.py -f $f -m /imars_data/masks/sst_venezuela_scar_mask.png -c data -o ~/n19avhrr_mcsst_png/$year\.$month/$file.png -s mcsst -n 0 -l NaN -u NaN -a 55 -d -45 -e -5 -g -125 -w 16 -x -58 -y 8 -z -77
done
