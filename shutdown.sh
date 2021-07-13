#!/bin/sh

echo -n $"Shutting down distributed_computing_assist_API: "
pids=(`ps -ax | grep python3.6 | grep  mi_dicomapi | awk '{print $1}'`)
for procid in ${pids[@]}
    do
    kill -15 $procid
    rv=$?
done
echo
[ $rv -eq 0 ]

