#!/bin/bash

# The command line arguments are the lines needed to run the tool.
line=$1

correct=0
total=0
# A log of the results of passing tests
rm -f passed_bad.txt
touch passed_bad.txt
for directory in ./bad/*; do
    for file in ${directory}/*.bed; do
		# ===Run the tool=== #
		# Redirect stderr to a outfile called error
		execute_line=${line/FILE/${file}}
		echo $execute_line
		eval "$execute_line >/dev/null 2>error"
		# Check if the error file is empty or not
		len=`cat error | wc -c`
		if [ ${len} -eq '0' ] ## ADD THE EXIT VALUE!
		then # If it's empty, then the test passed without error or warning, which shouldn't happen
			echo "%===========================%" >> passed_bad.txt
			echo ${file} passed incorrectly >> passed_bad.txt
			echo " " >> passed_bad.txt
			eval "$execute_line >> passed_bad.txt "
			echo "%===========================%" >> passed_bad.txt
			echo ${file} passed incorrectly.
		else # Otherwise at least one error/warning was given, which is good
			echo ${file} failed correctly.
			let "correct=correct+1"
		fi
		let "total=total+1"
    done
done
rm -f error # Remove the temporary file

echo $'\n\n'
echo Tests completed.
echo $correct correct out of $total.
