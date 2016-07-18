#!/bin/bash

echo $1;
cut -d ' ' -f 2- $1 > ./meta/match/testfiles/file2$2.tmp;
grep -v '*' ./meta/match/testfiles/file2$2.tmp > ./meta/match/testfiles/file1$2.tmp;
grep -v ':' ./meta/match/testfiles/file1$2.tmp > ./meta/match/testfiles/file3$2.tmp;
awk -F ' ' '{print NF > "./meta/match/testfiles/numbers.tmp"}' ./meta/match/testfiles/file2$2.tmp;
awk '{s+=$1} END {print s > "./meta/match/testfiles/number.tmp"}' ./meta/match/testfiles/numbers.tmp;
cat ./meta/match/testfiles/number.tmp ./meta/match/testfiles/file2$2.tmp > ./meta/match/testfiles/file$2.test;
rm -f ./meta/match/testfiles/*.tmp;
exit
