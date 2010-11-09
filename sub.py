# vim: set ts=4 sws=4 expandtab
#
# Run this command to etch live text onto the video:
#   while read line; do echo -n "$line " > sub; done
#
import gobject
import gst
import os
import socket
from datetime import datetime

FIFO=False
COMMFILE = "/tmp/errantia-sub"
LOGFILE = "sub.log"

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
videotestsrc
  ! video/x-raw-yuv,width=640,height=360,framerate=15/1
  ! textoverlay text="Hello" name="overlay" font-desc="Ubuntu 26" line-alignment=left halign=left valign=bottom shaded-background=true
  ! xvimagesink sync="false" """)
#  ! ffmpegcolorspace
#  ! theoraenc bitrate=500 keyframe-force=64
#  ! queue
#  ! oggmux
#  ! queue
#  ! shout2send ip=video.knut.s0.no port=80 password=sTeodorx2 mount=/sub.ogv
#  """)

overlay = pipeline.get_by_name('overlay')
pipeline.set_state(gst.STATE_PLAYING)

def timer(user_data, f):
    line = f.recv(1024)
    if (line):
       sublog.write("%s,%s\n" % (datetime.now(), line,) )
       user_data.set_property('text', line)
    return True


gobject.timeout_add_seconds(1, timer, overlay, sock)

loop = gobject.MainLoop()
loop.run()

sock.close()
