#!/bin/bash

echo $1
cut -d ' ' -f 2- $1 > ./meta/match/result/file$2.test;
perl -pi -e 'chomp' ./meta/match/result/file$2.test;
#sed -e 's/ /,/g' ./meta/match/result/file$2.test;
sed -e 's/\n$//g' ./meta/match/result/file$2.test;

exit
