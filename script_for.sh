#!/bin/bash

#############################

#PBS -N parsingMatches

#PBS -d .

#PBS -l walltime=05:00:00

#PBS -l nodes=1:ppn=1

#PBS -k oe

#PBS -o /home/creda/match.out

#PBS -e /home/creda/match.err

#PBS -m abe

#PBS -M reda.clmc@live.fr

#############################

#if [ -e -r ./meta/match/result ]
#then
#   rm -rf ./meta/match/result
#fi
   
#mkdir ./meta/match/result
i=0
for FILE in ./meta/match/*.match
do
    ./script_execute.sh $FILE $i &
    i=$((i+1))
done

exit
