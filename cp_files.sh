#!/bin/bash

echo "This is a script to find and copy World View files from /extra_data"
echo "Author: Asurin"
echo "version: 0.1"

# how many process
parallel=3

# check the input has 2 params
# this program copies file from default location which is /extra_data
if [ "$#" -ne 2 ]; then
        echo "Usage: $0 textfile destination_dir"
        exit
fi

if [ ! $1 ]; then
        echo "Can not find " $1
        exit
fi

if [ ! -d $2 ]; then
        echo $2 " dose not exist!"
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

files=$(cat $1)
total_pass=$(wc -l < $1)

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
                        rsync $file $2/ &
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

echo " total copied and moved."
