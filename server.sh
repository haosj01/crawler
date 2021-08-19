#!/bin/sh

APP_NAME=crawler

case "$1" in
	start)
	cd ./$APP_NAME
	nohup python3 run.py prod > run.log 2>&1 &
	echo $! >../pid.text
	echo "=== start $APP__NAME"
	;;

	stop)
	kill `cat pid.text`
	rm -rf pid.text
	echo "=== stop $APP__NAME"
	;;

	restart)
	$0 stop
	sleep 2
	$0 start
	echo "=== restart $APP__NAME"
	;;
	
	*)
	$0 stop
        sleep 2
        $0 start
        echo "=== restart $APP__NAME"
        ;;

esac
exit 0
