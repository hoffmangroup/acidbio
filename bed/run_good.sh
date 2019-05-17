#!/bin/bash

# The first command line argument is the way of executing the tool
line=$1

correct=0
total=0
# A log of the failing tests
rm -f failed_good.txt
touch failed_good.txt
for directory in ./good/*; do
    for file in ${directory}/*.bed; do
	# === Run the tool === #
	execute_line=${line/FILE/$file}
	$execute_line > /dev/null 2>&1
	if [ $? -eq 0 ] 
	then # If the exit code is 0, then it passed, which is good
	    echo ${file} passed correctly
		correct=`correct+1`
	else # If the exit code is not 0, then it failed, which is bad
	    echo ${file} failed incorrectly
	    echo "%===========================%" >> failed_good.txt
	    echo ${file} >> failed_good.txt
	    echo " " >> failed_good.txt
	    # log the error
	    $execute_line >> failed_good.txt 2>&1
	    echo "%===========================%" >> failed_good.txt
	    echo "" >> failed_good.txt
	    echo "" >> failed_good.txt
	fi
	total=`total+1`
    done
done
