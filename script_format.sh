#!/bin/bash

#if ![-e -r files]
#then
#    mkdir files;
#fi

#if ![-e -r meta]
#then
#    mkdir meta;
#    cd meta;
#    mkdir match;
#    cd match;
#    mkdir testfiles;
#    cd ../../../;
#else
#    cd meta/match;
#    mkdir testfiles;
#    cd ../../..;
#fi

i=0
chmod +rwx script_format_per_file.sh;
for FILE in ./meta/match/*.match
do
    ./script_format_per_file.sh $FILE $i &
    i=$((i + 1));
done
