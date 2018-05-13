#!/usr/bin/env python
import threading
import time
import struct
import web
import gi
gi.require_version("Gst","1.0")
from gi.repository import GLib, Gst
from bluepy.btle import Scanner, DefaultDelegate

current_sound_location = "/usr/share/sounds/puck/cloche_F3.mp3"
device_address = "ce:2b:40:b3:f8:37"

class SoundPlayer(threading.Thread):
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

class PuckClickDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.click_watchdog = 0
    
    def resetClickWatchdog(self):
        self.click_watchdog = 0

    def handleDiscovery(self, dev, isNewDev, isNewData):
        print "found " + dev.addr
        if dev.addr != device_address :
            return
        current_click_watchdog = self.click_watchdog
        for (adtype, _, value) in dev.getScanData():
            if adtype == 255 and value[:4] == "9005":
                data = value[4:]
                current_click_watchdog = int(data,16)
                break
        if (self.click_watchdog != current_click_watchdog):
            if self.click_watchdog != 0:
                sound = SoundPlayer()
                sound.play(current_sound_location)
            self.click_watchdog = current_click_watchdog
                
class ScannerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop = False

    def run(self):
        scanner = Scanner().withDelegate(PuckClickDelegate())
        scanner.start()
        while not self.stop:
            print "coucou"
            scanner.process(10)
        scanner.stop()

    def shutdown(self):
        self.stop = True
 
Gst.init(None)

scanner_thread = None

class StartRequestHandler:
    def GET(self):
        global scanner_thread
        if scanner_thread is None:
            scanner_thread = ScannerThread()
            scanner_thread.start()
        return "{response:ok}"

class StopRequestHandler:
    def GET(self):
        global scanner_thread
        if scanner_thread is not None:
            scanner_thread.shutdown()
            scanner_thread.join()
            scanner_thread = None
        return "{response:ok}"
        
urls = (
    '/start','StartRequestHandler',
    '/stop','StopRequestHandler'
)
app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()