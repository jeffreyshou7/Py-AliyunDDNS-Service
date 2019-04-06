#!/bin/bash
### BEGIN INIT INFO
# Provides:          Py-AliyunDDNS-Service
# Required-Start:    $local_fs $network
# Required-Stop:     $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: AliyunDDBS service
# Description:       Py-AliyunDDNS-Service
### END INIT INFO

filepath="/data/service/py/srv-aliyunddns/main.py"

start(){
    nohup python3 $filepath>/dev/null 2>&1 &
    echo 'AliyunDDBS service OK'
}


stop(){
    serverpid=`ps -aux|grep "$filepath"|grep -v grep|awk '{print $2}'`
    kill -9 $serverpid
    echo 'AliyunDDBS stop OK'
}


restart(){
    stop
    echo 'AliyunDDBS stop OK'
    start
    echo 'AliyunDDBS service start OK'
}


case $1 in
    start)
    start
    ;;
    stop)
    stop
    ;;
    restart)
    restart
    ;;
    *)
    start
esac