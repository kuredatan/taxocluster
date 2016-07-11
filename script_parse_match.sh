#!/bin/bash

for FILE in ./meta/match/*.match
do
    
    echo "/!\ Parsing " $FILE " file:"
    
    while read LINE
    do
	IFS=' ' read -r -a LINE_ARRAY <<< "$LINE"
	#First element of the line is the number of reads
	#which is of no interest
	unset LINE_ARRAY[0]
	echo ${LINE_ARRAY[@]}
	export LINE_ARRAY
	
    done < $FILE
    
done

exit
