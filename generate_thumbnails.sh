#!/bin/bash
#This is the file to gnerate thumbnails for true color images. Run this on thing1 and mount the imars_data folder

targetFolder=/imars_data/pub/modis/imars/final/pass/1km/crefl_rgb/gcoos/$(date +%Y).$(date +%m)
debug=true

datediff() {
        d1=$(date -d "$1" +%s)
        d2=$(date -d "$2" +%s)
        res=$(( (d1 - d2) / 86400 ))
        echo $res
}
today=$(date +%Y%m%d)
#today=20170129
if [ $(find $targetFolder -type f -name "*$today*crefl_rgb.png" | wc -l) -eq "0" ]
then
        echo "no file exists yet"
        exit
fi
for i in $targetFolder/*$today*crefl_rgb.png
do
        #echo $i
        #echo $i | sed 's/png/s.png/'
        if [ ! -f $(echo $i | sed 's/png/s.png/') ]
        then
                echo ; echo
                echo $i | sed 's/png/s.png/'
                if [ $debug = false ]
                then
                        convert $i -resize 200 $(echo $i | sed 's/png/s.png/') > null
                fi
        fi
        # if convert command not working, the png is corrupted, copy the original file here and convert again.
        if [ ! -f $(echo $i | sed 's/png/s.png/') ]
        then
                filename=$(basename $i)
                temp=$filename
                #echo $temp
                sat=${temp%%.*}
                temp=${temp#*.}
                #echo $sat $temp
                imageDate=${temp%%.*}
                year=${imageDate:0:4}
                month=${imageDate:4:2}
                day=${imageDate:6}
                imageDate=$year$(expr 335+$day)
                echo $year $month $day
                day=$(datediff $year-$month-$day $year-01-01)
                #add leading 0 and add 1 day to the day
                printf -v day '%03d' $((10#$day+1))
                imageDate=$year$day
                echo $imageDate
                temp=${temp#*.}
                #echo $imageDate $temp
                imageTime=${temp%%.*}
                temp=${temp#*.}
                #echo $imageTime $temp
                area=${temp%%.*}
                temp=${temp#*.}
                #echo $area $temp
                product=${temp%%.*}
                ext=${temp#*.}
                #echo $product $ext
                origin1k=/thing1/ipopp-nrt/pub/data/$sat/modis/level3/$sat.$imageDate.$imageTime.$area.tcolor.1km.$ext
                #echo $origin1k
                origin250=/thing1/ipopp-nrt/pub/data/$sat/modis/level3/$sat.$imageDate.$imageTime.$area.tcolor.250m.$ext
                if [ $debug = false ]
                then
                        if [ -f $origin1k ]
                        then
                                cp -v $origin1k $i
                                convert $i -resize 200 $(echo $i | sed 's/png/s.png/')
                        elif [ -f $origin250 ]
                        then
                                cp -v $origin250 $i
                                convert $i -resize 200 $(echo $i | sed 's/png/s.png/')
                        fi
                fi

        fi
done
