from bluepy.btle import Scanner, DefaultDelegate
class ScanDelegate(DefaultDelegate):
	def __init__(self):
		DefaultDelegate.__init__(self)
	def handleDiscovery(self, dev, isNewDev, isNewData):
		print "Device %s" % dev.addr
		for (adtype, desc, value) in dev.getScanData():
			print "adtype %s, desc  %s, value %s" % (adtype,desc, value)
		print "---------------"

scanner = Scanner().withDelegate(ScanDelegate())
scanner.clear()
scanner.start()
while True: scanner.process(10)
scanner.stop()
