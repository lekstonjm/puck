#!/usr/bin/env python
import pygst
pygst.require("0.10")
import gst
import web

class sounder:
    def __init__(self):
        self.pipeline = gst.Pipeline("sound_pipe")
        self.audiotestsrc = gst.element_factory_make("audiotestsrc", "audio")
        self.pipeline.add(self.audiotestsrc)
        self.sink = gst.element_factory_make("pulsesink","sink")
        self.pipeline.add(self.sink)
        self.audiotestsrc.link(self.sink)
    def start(self):
        self.pipeline.set_state(gst.STATE_PLAYING)
    def stop(self):
        self.pipeline.set_state(gst.STATE_PAUSED)


urls = (
    '/start','start',
    '/stop','stop'
)

app = web.application(urls, globals())


sound = sounder()

class start:
    def GET(self):
        sound.start()
        return "{response:ok}"

class stop:
    def GET(self):
        sound.stop()
        return "{response:ok}"


if __name__ == "__main__":
    app.run()