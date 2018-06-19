#!/usr/bin/env python
import gi
gi.require_version("Gst","1.0")
from gi.repository import Gst, GLib
import random
import math
import struct

class Sound:
    def __init__(self):
        self.player = Gst.parse_launch('appsrc name=source ! capsfilter caps=audio/x-raw,rate=44100,channels=2,format=F32LE ! pulsesink')
        playersrc = self.player.get_by_name('source')
        playersrc.connect('need-data', self.need_data)
        self.time = 0
        #self.BYTES_PER_SAMPLE = 2
        self.BYTES_PER_SAMPLE = 4
        self.CHANNELS = 2
        self.SAMPLE_SIZE = self.BYTES_PER_SAMPLE * self.CHANNELS 
        self.RATE = 44100
        self.dt = 1.0 / float(self.RATE)

    def start(self):
        self.player.set_state(Gst.State.PLAYING)

    def stop(self):
        self.player.set_state(Gst.State.PAUSED)

    def need_data(self, src, length):
        sample_number = int(length / self.SAMPLE_SIZE)
        data = bytearray()
        print "cou"
        for i in range(0,sample_number):
            value_float = math.sin(self.time * 2.0 * math.pi * 440.0) * 0.5
            if value_float > 1.0:
                value_float = 1.0
            if value_float < -1.0:
                value_float = -1.0
            value_bytes = struct.pack('f',value_float)            
            for byte in value_bytes:
                data.append(byte)
            for byte in value_bytes:
                data.append(byte)
            self.time += self.dt
        src.emit('push-buffer', Gst.Buffer.new_wrapped(data))

Gst.init(None)
sa = Sound() 

loop = GLib.MainLoop()
loop.run()

