#!/bin/bash

if [ -t 0 ]; then
    echo
    echo "No pipe detected. You need to pipe a file or a command. E.g.:"
    echo " dvgrab | $0"
    echo " cat video.dv | $0"
    echo

    exit 1
fi

pkill -f "python sub.py"
# Redirect stdin into the sub.py python script (should be a DV stream (or file))
python sub.py <&0 &

sleep 1

pkill -f "python serv.py"
python serv.py

pkill -f "python sub.py"
echo "Quitting..."
