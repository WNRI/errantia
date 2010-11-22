#!/bin/bash

pkill -f "python sub.py"
python sub.py &

sleep 1

pkill -f "python serv.py"
python serv.py

pkill -f "python sub.py"
echo "Quitting..."
