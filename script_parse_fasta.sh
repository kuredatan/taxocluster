#!/bin/bash

i=0

if [ -e ./meta/fasta ]
then
   rm -rf ./meta/fasta
fi
   
mkdir ./meta/fasta
echo "/!\ Created fake FASTA folder."

for FILE in ./meta/*.fasta
do
    sed 'n;d' $FILE > ./meta/fasta/newfastafile$i.fasta
    i=$(($i + 1))
done

for FILE in ./meta/fasta/*.fasta
do

    echo "/!\ Parsing " $FILE " file:"
    while read LINE
    do
	IFS=' ' read -r -a LINE_ARRAY <<< "$LINE"
	break
    done
    break

done

rm -rf ./meta/fasta
echo "/!\ Deleted fake FASTA folder."

exit
