#!/usr/bin/env python
import sys
import pygtk
import gtk
import gtk.glade
import gst

class Main:
    # GTK signal handlers
    def on_window_destroy(self, widget, data=None):
        print "Window destroy"
        gtk.main_quit()
        sys.exit(1)

    def on_playbutton_toggled(self, widget, data=None):
        if widget.get_active():
            self.player.set_state(gst.STATE_PLAYING)
        else:
            self.player.set_state(gst.STATE_READY)

    # GStreamer signal handlers
    def on_sync_message(self, bus, message):
        if message.structure is None:
            return

        message_name = message.structure.get_name()
        if message_name == "prepare-xwindow-id":
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            gtk.gdk.threads_enter()
            imagesink.set_xwindow_id(self.video_window.window.xid)
            gtk.gdk.threads_leave()
 

    def __init__(self):
        # Set up the GUI
        builder = gtk.Builder()
        builder.add_from_file("gui.glade")
        builder.connect_signals(self)
        self.window = builder.get_object("window")
        self.video_window = builder.get_object("video")

        # Set up GStreamer
        self.player = gst.Pipeline("player")
        source = gst.element_factory_make("videotestsrc", "file-source")
        videosink = gst.element_factory_make("autovideosink", "video-output")

        self.player.add(source, videosink)
        gst.element_link_many(source, videosink)

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        #bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)

        self.player.set_state(gst.STATE_READY)

    def run(self):
        self.window.show_all()
        gtk.gdk.threads_init()
        gtk.main()

if __name__ == "__main__":
    app = Main()
    app.run()
