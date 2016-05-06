#!/bin/bash

echo "This is created to organize the files generated from"
echo "World View according to year and month- yyyy.mm"
echo "Author: Asurin, Gaby"
echo "version: 1.1"

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

# get all the files in subdirectories
#files=$( find $1 -type f -iname '*' )

#for file in "$(find $1 -type f -iname '*')"
find $1 -type f -print0 | while IFS= read -r -d '' file;
do

        # get the file base name
        filename=${file##*/}

        # get the make sure the file has the correct prefix
        sat=${filename:0:4}
        #echo $sat
        if [ "$sat" == 'WV02' -o "$sat" == 'WV03' ] ; then
                # I found two different name schema and match them with
                # this if
                if [ ${filename:5:2} -gt 18 ] ; then
                        year=${filename:5:4}
                        month=${filename:9:2}
                else
                        year="20"${filename:5:2}
                        month=${filename:7:3}
                        convert_month $month
                fi
                folder=$( echo $year'.'$month )
                if [ ! -d $2/$sat/$folder ]; then
                        echo -ne "\r"
                        mkdir -v -p $2/$sat/$folder
                fi
                # touch is used for test the creation of folders
                # touch $2/$sat/$folder/$filename
                rsync --remove-source-files $file $2/$sat/$folder/
#               rsync $1/$file $2/$folder/
        else
                if [ ! -d $2/extra ]; then
                        mkdir -v $2/extra
                fi
                cp "$file" $2/extra/

        fi

        count=$(($count+1))
        echo -ne "\r$count"
done

echo " total copied and moved."
