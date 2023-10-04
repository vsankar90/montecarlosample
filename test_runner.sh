#!/bin/bash
#Command line input arguments
testcase=$1
nthreads=$2
noptions=$3
pathlength=$4
pathblocklength=$5

 

#Static variables
cdate=$(date +"%F_%H:%M:%S")
result_log="/tmp/cdp/$1/result_MonteCarlo_$cdate.txt"
nmon_log="/tmp/cdp/$1/nmon_MonteCarlo_$cdate.nmon"
find . -name "*.nmon" -type f -delete
sudo rm -rf "/tmp/cdp/$1/"              #Delete the existing log directories
mkdir -p "/tmp/cdp/$1/"                 #Create new log directories

 

#start nmon service
nmon -f -s 30 -c 20 2>&1  | tee -a $nmon_log

 

echo "<<<<<<<<<<<<<<<<<<<<<<<<< Running [$1] >>>>>>>>>>>>>>>>>>>>>>>>>"
#Run Montecarlo tool
./MonteCarlo $nthreads $noptions $pathlength $pathblocklength 2>&1  | tee -a $result_log
#Sleep for 2 Sec.
sleep 6
#Stop nmon service
ps -ef | grep nmon | grep -v grep | awk '{print $2}' | xargs kill
sleep 2

 

#Convert .nmon data to .html
./nmonchart *.nmon /tmp/cdp/$1/nmon_MonteCarlo_$cdate.html
sleep 7
#copying the HTML file to webserver
cp /tmp/cdp/$1/nmon_MonteCarlo_$cdate.html /var/www/html/montecarlo/svm/$1/
