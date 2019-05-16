#!/bin/bash

rm -f failed_good.txt
touch failed_good.txt
for directory in ./good/*; do
    for file in ${directory}/*.bed; do
	bedtools intersect -a intersect_file.bed -b ${file} > /dev/null 2>&1
	if [ $? -eq 0 ] 
	then
	    echo ${file} passed
	else
	    echo ${file} failed
	    echo "%===========================%" >> failed_good.txt
	    echo ${file} >> failed_good.txt >> failed_good.txt
	    echo " " >> failed_good.txt
	    bedtools intersect -a intersect_file.bed -b ${file} >> failed_good.txt 2>&1
	    echo "%===========================%" >> failed_good.txt
	    echo "" >> failed_good.txt
	    echo "" >> failed_good.txt
	fi
    done
done
