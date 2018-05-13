import threading
import time

class Worker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stopFlag = 0
    
    def shutdown(self):
        self.stopFlag = 1
    
    def run(self):
        self.stopFlag = 0
        while not self.stopFlag:
            print "coucou"
            time.sleep(1)

worker = Worker()
worker.start()
time.sleep(10)
worker.shutdown()
