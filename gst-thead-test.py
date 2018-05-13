#!/usr/bin/env python
import threading
import time
import gi
gi.require_version("Gst","1.0")
from gi.repository import Gst, GLib
current_sound_location = "/usr/share/sounds/puck/cloche_F3.mp3"

class Sound(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        gst_string = "filesrc name=source location=" + self.current_sound_location + " ! mad ! audioconvert ! alsasink"
        self.player = Gst.parse_launch(gst_string)
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.handleGstMessage)
        self.player.set_state(Gst.State.PLAYING)
        
        self.loop = GLib.MainLoop()
        self.loop.run()
    
    def handleGstMessage(self, bus, message):
        print message.type
        if message.type == Gst.MessageType.EOS or message.type == Gst.MessageType.ERROR:
            print "end of playing"
            self.player.set_state(Gst.State.NULL)
            self.loop.quit()
            self.loop.unref()
    
    def play(self, filename):
        self.current_sound_location = filename
        self.start()



Gst.init(None)
sound = Sound()
sound.play(current_sound_location)
sound.join()
sound = Sound()
sound.play(current_sound_location)
sound.join()