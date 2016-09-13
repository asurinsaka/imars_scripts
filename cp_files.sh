#!/bin/bash
# The default location is /extra_data

echo "This is a script to find and copy files from a list of filenames"
echo "Author: Asurin"
echo "version: 0.2"

# how many process
parallel=3

# check the input has 2 or 3 params
# this program copies files from /extra_data or from arbitrary location.
# files in /extra_data are organized
if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
        echo "If copy files from /extra_data"
        echo "Usage: $0 textfile destination_dir"
        echo "If copy files from other directories"
        echo "Usage: $0 textfile source_dir destination_dir"
        exit
fi

source_dir="/extra_data"

input_file=$1
shift

if [ "$#" -eq 2 ]; then
    source_dir=$1
    shift
fi

dest_dir=$1

if [ ! -f $input_file ]; then
    echo "Can not find input file " $input_file
    exit
fi

if [ ! -d $source_dir ]; then
    echo "Can not find source_dir " $source_dir
    exit
fi


if [ ! -d $dest_dir ]; then
        echo "destination_dir " $dest_dir " dose not exist!"
        exit
fi

if [ $source_dir == $dest_dir ]; then
    echo "source_dir and destination_dir can not be the same"
    exit
fi


# get total number of files moved
count=0
pass_count=0

# convert the month from literal to number
convert_month()
{
        case $1 in
        'JAN') month=01 ;;
        'FEB') month=02 ;;
        'MAR') month=03 ;;
        'APR') month=04 ;;
        'MAY') month=05 ;;
        'JUN') month=06 ;;
        'JUL') month=07 ;;
        'AUG') month=08 ;;
        'SEP') month=09 ;;
        'OCT') month=10 ;;
        'NOV') month=11 ;;
        'DEC') month=12 ;;
        esac
}

files=$(cat $input_file)
total_pass=$(wc -l < $input_file)


if [ $source_dir == '/extra_data' ]; then
    # this file contains wildcard
    for filename in $files;
    do
    	pass_count=$(($pass_count+1))
    	# get the make sure the file has the correct prefix
    	sat=${filename:0:4}
    	
    	if [ ${filename:5:2} -gt 18 ] ; then
                   year=${filename:5:4}
                   month=${filename:9:2}
            else
                   year="20"${filename:5:2}
                   month=${filename:7:3}
                   convert_month $month
            fi
    	folder=$( echo $year'.'$month )
    	for file in $(ls -d -1 /extra_data/$sat/$folder/$filename);
    	do
    		if [ $file ]; then
    			rsync $file $dest_dir/ &
    			count=$(($count+1))
    			echo -ne "\r $pass_count / $total_pass \t $count"
    		fi
    	done
    	#rsync /extra_data/$sat/$folder/$filename $2/ &
    	if (( $count%$parallel == 0 ))
    	then
    		wait
    	fi
    done
else
    for filename in $files;
    do
        pass_count=$(($pass_count+1))
        for file in $(find $source_dir -name $filename);
        do
            if [ $file ]; then
                rsync $file $dest_dir/ &
                count=$(($count+1))
                echo -ne "\r $pass_count / $total_pass \t $count \t"
                #echo -ne "\r $pass_count / $total_pass \t $count \t $filename"

            fi
        done
        #rsync /extra_data/$sat/$folder/$filename $2/ &
        if (( $count%$parallel == 0 ))
        then
            wait
        fi
    done
fi
echo " total copied and moved."
