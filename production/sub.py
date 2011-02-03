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
from ConfigParser import SafeConfigParser

# from least to most important
configs = ['errantia-default.conf', os.path.expanduser('~/.errantia'), '.errantia', 'errantia.conf',]
parser = SafeConfigParser()
found = parser.read(configs)

if len(found) == 1:
    print "\nYou should make an errantia.conf file in one of these locations:"
    for c in configs[1:]:
        print "- %s" % c
    print

if os.path.exists(parser.get('subtitle', 'commfile')):
    os.remove(parser.get('subtitle', 'commfile'))

sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
sock.bind(parser.get('subtitle', 'commfile'))

sublog = open(parser.get('subtitle', 'log'), "a")
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
        ! video/x-raw-yuv,width={w},height={h},fps={fps},pixel-aspect-ratio=1/1
        ! textoverlay text="" name="overlay" font-desc="Ubuntu 26" line-alignment=left halign=left valign=bottom shaded-background=true xpad=0 ypad=15
        ! tee name=preview
        ! ffmpegcolorspace
        ! queue
        ! theoraenc bitrate={t_rate} keyframe-force=64
        ! queue
        ! mux.
demux.
        ! queue
        ! decodebin2
        ! audioconvert
        ! audio/x-raw-float,channels=1
        ! queue
        ! vorbisenc max-bitrate={v_rate}000
        ! queue
        ! mux.
preview.
        ! queue
        ! xvimagesink sync="false"
oggmux name=mux
        ! queue
        ! progressreport update-freq=60
        ! shout2send ip={url} port={port} password={pw} mount={mnt}
  """.format(
      w=parser.get('gst', 'width'),
      h=parser.get('gst', 'height'),
      fps=parser.get('gst', 'fps'),
      t_rate=parser.get('gst', 'theora_bitrate'),
      v_rate=parser.get('gst', 'vorbis_bitrate'),
      url=parser.get('icecast', 'url'),
      port=parser.get('icecast', 'port'),
      pw=parser.get('icecast', 'password'),
      mnt=parser.get('icecast', 'mount'),
      )
)

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
       sublog.flush()
       user_data.set_property('text', line)
    else:
       user_data.set_property('text', '')
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
