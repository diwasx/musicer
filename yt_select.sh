#!/bin/sh

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
else
    echo "Playing - "$1
    killall "yt" & killall "mpv"
    # echo "yt /$1, 1, all"
    yt /$1, all
fi
