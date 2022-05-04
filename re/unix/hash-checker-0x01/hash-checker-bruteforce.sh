#!/bin/sh

i=100000
max=1000000

while [ $i -lt $max ]
do
	./crackme $i | grep "Key is valid" && echo "key: " $i

	i=`expr $i + 1`
done