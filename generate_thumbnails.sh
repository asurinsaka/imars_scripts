#!/bin/bash
#This is the file to gnerate thumbnails for true color images. Run this on thing1 and mount the imars_data folder

debug=false
areas=( gcoos east_caribbean west_caribbean argentina_egi argentina_epea argentina_patagonia argentina_san_jorge brazil_se brazil_south chile_central chile_chiloe chile_north chile_south venezuela_scar seacoos argentina_bahia )
today=$(date +%Y%m%d)
#today=20170129


datediff() {
	d1=$(date -d "$1" +%s)
	d2=$(date -d "$2" +%s)
	res=$(( (d1 - d2) / 86400 ))
	echo $res
}

genrate_thumb_for_area() {
	area=$1
	targetFolder=$2

	if [ $(find $targetFolder -type f -mtime -1 -name "*crefl_rgb.png" | wc -l) -eq "0" ]
	then
		echo "no file exists yet"
		return 0
	fi
	for i in $targetFolder/*crefl_rgb.png
	do
		#echo $i
		#echo $i | sed 's/png/s.png/'
		thumbnailName=$(echo $i | sed 's/png/s.png/')
		if [ ! -f $thumbnailName ]
		then
			echo ; echo
			echo $i | sed 's/png/s.png/'
			if [ $debug = false ]
			then
				convert $i -resize 200 $thumbnailName > null
			fi
		fi
		# if convert command not working, the png is corrupted, copy the original file here and convert again.
		if [ ! -f $thumbnailName ]
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
			#echo $year $month $day
			day=$(datediff $year-$month-$day $year-01-01)
			#add leading 0 and add 1 day to the day
			printf -v day '%03d' $((10#$day+1))
			imageDate=$year$day
			#echo $imageDate
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
					echo "Copy 1km image"
					cp -v $origin1k $i
					convert $i -resize 200 $thumbnailName
				elif [ -f $origin250 ]
				then
					echo "Copy 250m image"
					cp -v $origin250 $i
					convert $i -resize 200 $thumbnailName
				else
					echo "Create Link"
					ln -v $i $thumbnailName
				fi
			fi
		fi
	done
}

for area in "${areas[@]}"
do
	echo $area
	targetFolderModis=/imars_data/pub/modis/imars/final/pass/1km/crefl_rgb/$area/$(date +%Y).$(date +%m)
	targetFolderViirs=/imars_data/pub/viirs/imars/final/pass/1km/mcrefl_rgb/$area/$(date +%Y).$(date +%m)
	yesterdayModis=/imars_data/pub/modis/imars/final/pass/1km/crefl_rgb/$area/$(date --date="yesterday" +%Y).$(date --date="yesterday" +%m)
	yesterdayViirs=/imars_data/pub/viirs/imars/final/pass/1km/mcrefl_rgb/$area/$(date --date="yesterday" +%Y).$(date --date="yesterday" +%m)

	if [ -d $targetFolderModis ]
	then
		genrate_thumb_for_area $area $targetFolderModis
	fi
	if [ -d $targetFolderViirs ]
	then
		genrate_thumb_for_area $area $targetFolderViirs

	fi
	if [ $(date +%d) -eq "01" ]
	then
		if [ -d $yesterdayModis ]
		then
			genrate_thumb_for_area $area $yesterdayModis
		elif [ -d $yesterdayViirs  ]; then
			genrate_thumb_for_area $area $yesterdayViirs
		fi

	fi

done
