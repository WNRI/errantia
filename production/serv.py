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
    else:
        start_response('200 OK', [('content-type', 'text/html')])
        return [open(os.path.join(
                     os.path.dirname(__file__), 
                     'sendtext.html')).read()]

if __name__ == "__main__":
    # run an example app from the command line            
    listener = eventlet.listen(('0.0.0.0', 7000))
    print "\nVisit http://localhost:7000/ in your websocket-capable browser.\n"
    wsgi.server(listener, dispatch)
