#!/bin/bash
# for taskid in $(seq 1 9); do 
#   for baseid in $(seq 1 21); do
#     echo "base changed $baseid"
#     for uid in $(seq 1 21); do
#         # echo $taskid, $uid
#         go run pertask.go -tid $taskid -users $baseid,$uid -sim 1
#     done;
#   done;
# done

for taskid in $(seq 1 9); do 
    # go run pertask.go -tid $taskid -users 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21 -sim 1
    go run pertask.go -tid $taskid -users 1,19,20,21 -sim 1
done