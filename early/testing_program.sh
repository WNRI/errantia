#!/bin/bash

function a() {
	echo -e "CONNECT

\0
SUBSCRIBE
destination: /topic/graph2

\0
SEND
destination: /topic/graph2

{\"cur\":$1,\"total\":13}

\0
DISCONNECT

\0" \
		| nc 127.0.0.1 61613

	echo "{\"cur\":$1,\"total\":13}" > htdocs/first.json
}

while true; do
	for i in `seq 0 12`; do
		a $i
		#dvsource-file -h 10.0.1.1 -p 1234 htdocs/img/ting-$i.png.dv
		sleep 2
	done
done

