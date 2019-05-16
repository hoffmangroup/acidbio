#!/bin/bash

rm -f passed_bad.txt
touch passed_bad.txt
for directory in ./bad/*; do
    for file in ${directory}/*.bed; do
	bedtools intersect -a intersect_file.bed -b ${file} 2>error
	len=`cat error | wc -c`
	if [ ${len} -eq '0' ]
	then
	    echo ${file} passed incorrectly.
	else
	    echo ${file} failed correctly.
	fi
    done
done
rm -f error
	    
