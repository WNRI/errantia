# vim: set ts=4 sws=4 expandtab
#
# Subtitle, compress, and send theora.
#
# Pipe dv into this script, and it will subtitle, compress and send the video.
#
# You can run it like this: dvsink-command -- python sub.py
# Remember to start serv.py in order to get subtitles into the socket
import sys
import gst
import os
import socket
import gobject
from datetime import datetime

COMMFILE = "/tmp/errantia-sub"
LOGFILE = "sub.log"

# If you enable this, you can enter subtitles without the serv.py script.
# Use this bash-command (if you change COMMFILE, change the path here as well):
#    while read line; do echo -n "$line " > /tmp/errantia-sub; done
#
FIFO=False

if os.path.exists(COMMFILE):
    os.remove(COMMFILE)

if FIFO:
    os.mkfifo(COMMFILE)
    f = open(COMMFILE, "r")

else:
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    sock.bind(COMMFILE)

sublog = open(LOGFILE, "a")
sublog.write("- start %s\n" % datetime.now())

pipeline = gst.parse_launch("""
fdsrc
        ! queue
        ! dvdemux name=demux
demux.
        ! queue
        ! dvdec quality=5
        ! video/x-raw-yuv
        ! ffvideoscale
        ! video/x-raw-yuv,width=500,height=375,pixel-aspect-ratio=1/1
        ! textoverlay text="Hello" name="overlay" font-desc="Ubuntu 26" line-alignment=left halign=left valign=bottom shaded-background=true xpad=0 ypad=15
        ! tee name=preview
        ! ffmpegcolorspace
        ! queue
        ! theoraenc bitrate=200 keyframe-force=64
        ! queue
        ! mux.
demux.
        ! queue
        ! decodebin2
        ! audioconvert
        ! audio/x-raw-float,channels=1
        ! queue
        ! vorbisenc max-bitrate=36864
        ! queue
        ! mux.
preview.
        ! queue
        ! xvimagesink sync="false"
oggmux name=mux
        ! queue
        ! progressreport update-freq=60
        ! shout2send ip=video.knut.s0.no port=80 password=sTeodorx2 mount=/video.ogv
  """)

# Let fdsrc collect from stdin
fdsrc = [a for a in pipeline.iterate_sources()][0]
fdsrc.set_property("fd", sys.stdin.fileno())

overlay = pipeline.get_by_name('overlay')
pipeline.set_state(gst.STATE_PLAYING)

def timer(user_data, sock):
    # Blocking here, waiting for text via socket
    line = sock.recv(1024)
    if (line):
       sublog.write("%s,%s\n" % (datetime.now(), line,) )
       user_data.set_property('text', line)
    return True

gobject.timeout_add_seconds(1, timer, overlay, sock)

loop = gobject.MainLoop()
try:
    loop.run()
except:
    pass

print "Finishing"
sock.close()
del pipeline
