#!/bin/bash

echo $1;
mkdir ./meta/match/testfiles/sorted$2;
cut -d ' ' -f 2- $1 > ./meta/match/testfiles/sorted$2/f1;
cd ./meta/match/testfiles/sorted$2;
grep -v '*' f1 > f2;
grep -v ':' f2 > f3;
sed 's/ /\n/g' f3 | sort -u | sed '/^$/d' > sorted;
wc -l sorted | sed 's/ /\n/g' | head -1 > number;
cat number sorted > ../file$2.test;
cd ../;
rm -rf sorted$2;
head -1 file$2.test;
cd ../../../;
exit

