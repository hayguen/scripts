#!/bin/bash

export LANG=en_US
export LANGUGAGE=en_US
export LC_ALL=C

echo "--------------------------------------"
echo "hostname ; echo $HOSTNAME"
hostname
echo "$HOSTNAME"

echo "--------------------------------------"
echo "whoami"
whoami

echo "--------------------------------------"
echo "lsblk"
lsblk

echo "--------------------------------------"
echo "free -m"
free -m

echo "--------------------------------------"
echo "lscpu"
lscpu

echo "--------------------------------------"
echo "cat /etc/os-release"
cat /etc/os-release

echo "--------------------------------------"
echo "lsb_release -a"
lsb_release -a

