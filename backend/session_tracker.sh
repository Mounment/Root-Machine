#!bin/bash
ssh_tag=$1
for i in $(seq 1 30);do
     process_id=$(ps -ef |grep $ssh_tag |grep -v sshpass |grep -v grep |grep -v  $0 | awk '{ print $2 }'  )
     echo "process id:$process_id"
     if [ ! -z $process_id ];then
         echo 'runing strace'
         log_path=/home/crazy_audit/CrazyEye/log/`date +%F`
         mkdir -p $log_path
         sudo strace -fp $process_id -t -o $log_path/session_$2.log
         break;
     fi;

     sleep 1;
done;
