#!/bin/sh

exec="python3.6 mi_dicomapi.py &"

cd /home/misystem/misrc_distributed_computing_assist_api
echo -n $"Stating distributed_computing_assist_API: "
eval $exec
rv=$?
echo
[ $rv -eq 0 ]
pids=`ps -ax | grep python3.6 | grep mi_dicomapi | awk '{print $1}'`

