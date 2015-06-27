#!/bin/sh
for VARIABLE in 1 2 3 4 5 6 7 8
do
    start=$(($VARIABLE + 0))
    index=$(($start))
    time python cm/cm/tag_single_worker.py $index > /tmp/tag_log/$index 2>&1 &
done