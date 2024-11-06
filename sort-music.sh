#!/bin/bash
THIS_PATH=$(realpath "$0")
SCRIPTS_FOLDER=$(dirname "$THIS_PATH")
while true; do
    python $SCRIPTS_FOLDER/sort-music.py $1 $2
    sleep 1
    echo
    echo Restarting...
done
