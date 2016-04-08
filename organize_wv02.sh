#!/bin/bash

echo "This is created to organize the files generated from"
echo "World View according to year and month- yyyy.mm"
echo "Author: Asurin"

# check the input has 2 params
if [ "$#" -ne 2 ]; then
	echo "Usage: $0 source_dir destination_dir"
	exit
fi

if [ ! -d $1 ]; then
	echo $1 " dose not exist!"
	exit
fi


if [ ! -d $2 ]; then
	echo $2 " dose not exist!"
	exit
fi


# get total number of files moved
count=0

# convert the month from literal to number
convert_month()
{
	case $1 in
	'JAN')
	month=01
	;;
	'FEB')
	month=02
	;;
	'MAR')
	month=03
	;;
	'APR')
	month=04
	;;
	'MAY')
	month=05
	;;
	'JUN')
	month=06
	;;
	'JUL')
	month=07
	;;
	'AUG')
	month=08
	;;
	'SEP')
	month=09
	;;
	'OCT')
	month=10
	;;
	'NOV')
	month=11
	;;
	'DEC')
	month=12
	;;
	esac
}


for file in $1/*
do
	# get the file base name
	file=${file##*/}
	
	# get the make sure the file has the correct prefix
	sat=${file:0:4}
	if [ $sat == 'WV02' ]; then
		year="20"${file:5:2}
		month=${file:7:3}
		convert_month $month
		folder=$( echo $year'.'$month )
		if [ ! -d $2/$folder ]; then
			mkdir -v $2/$folder
		fi
		cp $1/$file $2/$folder/
	else
		if [ ! -d $2/extra ]; then
			mkdir -v $2/extra
		fi
		cp $1/$file $2/extra/

	fi
	
	count=$(($count+1))
done

echo $count

