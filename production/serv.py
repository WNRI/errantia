# vim: sw=4 ts=4 expandtab
import eventlet
from eventlet import wsgi
from eventlet import websocket
from eventlet.green import socket
import os

sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
sock.connect("/tmp/errantia-sub")

@websocket.WebSocketWSGI
def handle(ws):
    """  This is the websocket handler function.  Note that we 
    can dispatch based on path in here, too."""

    if ws.path == '/data':
        while True:
            m = ws.wait()
            if m is None:
                break
            sock.send(m.encode("utf-8"))

def dispatch(environ, start_response):
    """ This resolves to the web page or the websocket depending on
    the path."""
    if environ['PATH_INFO'] == '/data':
        return handle(environ, start_response)
    elif environ['PATH_INFO'] == '/ajax':
        sock.send(environ['wsgi.input'].read())
        start_response('200 OK', [('content-type', 'text/plain')])
        return ["OK\n"]
    else:
        start_response('200 OK', [('content-type', 'text/html')])
        return [open(os.path.join(
                     os.path.dirname(__file__), 
                     'sendtext.html')).read()]

# Helper
def get_ip_addresses():
    #Use ip route list
    import subprocess
    arg='ip route list'
    p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
    data = p.communicate()
    l = []
    for d in data:
        if d == None:
            continue
        sdata = d.split()
        ipaddr = sdata[ sdata.index('src')+1 ]
        netdev = sdata[ sdata.index('dev')+1 ]
        l.append( (ipaddr, netdev,) )
    return l

if __name__ == "__main__":
    # run an example app from the command line            
    listener = eventlet.listen(('0.0.0.0', 7000))
    print "\nVisit one of these addresses in your websocket-capable browser:"
    for ips in get_ip_addresses():
        print "- http://%s:%d/ (%s)" % (ips[0], 7000, ips[1])
    print

    wsgi.server(listener, dispatch)
