# vim: set ts=4 sws=4 expandtab
#
# Run this command to etch live text onto the video:
#   while read line; do echo -n "$line " > sub; done
#
import gobject
import gst
import os

FIFO=True
FIFOFILE = "sub"

if FIFO:

    if not os.path.exists(FIFOFILE):
        os.mkfifo(FIFOFILE)

    f = open(FIFOFILE, "r")

else:
    sock = socket.socket()
    sock.bind(("0.0.0.0", 7367,))
    sock.listen(1)

    # repeat this
    conn = sock.accept()
    f = conn[0].makefile()
    buf = f.read()

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
overlay.count = 0

pipeline.set_state(gst.STATE_PLAYING)

def timer(user_data, f):
    user_data.count += 1
    line = f.read()
    if (line):
       user_data.set_property('text', line)
    return True


gobject.timeout_add_seconds(1, timer, overlay, f)

loop = gobject.MainLoop()
loop.run()

f.close()
os.unlink(FIFOFILE)
