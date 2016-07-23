#!/usr/bin/python3
'''
file sispmctl.py - controlling EnerGenie EG-PMS

Copyright (c) 2016, Heinrich Schuchardt <xypron.glpk@gmx.de>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import getopt
import sispm
import sys

def checkport(dev, p):
	"""
	Checks if port p exists on the device.

	@param dev device
	@param p port
	@return port exists
	"""
	pmin = sispm.getminport(dev)
	pmax = sispm.getmaxport(dev)
	if p < pmin or p > pmax:
		print("Device {} only has ports {}..{}".format(
			sispm.getid(dev), pmin, pmax))
		return False
	return True

def main():
	# Find our devices.
	devices = sispm.connect()

	# Were they found?
	if len(devices) == 0:
		print('No device found')
		sys.exit(1)

	# If there is only one device, use it as default.
	if len(devices) == 1:
		dev = devices[0]
	else:
		dev = None

	# Define command line options.
	try:
		opts, args = getopt.getopt(sys.argv[1:], "D:d:f:ho:t:")
	except getopt.GetoptError as err:
		print(str(err))
		usage()
		sys.exit(2)

	# Handle command line.
	for o, a in opts:
		if o == "-D":
			dev = None
			for d in devices:
				if sispm.getid(d) == a:
					dev = d
					break
			if dev == None:
				print("device with id {} not found".format(a))
				break
		elif o == "-d":
			d = int(a)
			if d < 0 or d >= len(devices):
				print("unknown device {}".format(d))
				break
			dev = devices[d];
		elif o == "-f":
			p = int(a)
			if not checkport(dev, p):
				break
			sispm.switchoff(dev, p)
		elif o == "-h":
			usage()
			print()
		elif o == "-o":
			p = int(a)
			if not checkport(dev, p):
				break
			sispm.switchon(dev, p)
		elif o == "-t":
			p = int(a)
			if not checkport(dev, p):
				break
			if sispm.getstatus(dev, p) == 0:
				sispm.switchon(dev, p)
			else:
				sispm.switchoff(dev, p)
		else:
			break

	# Always output the device status.
	status(devices)

	# Workaround for bug in old version of usb library.
	devices = None

def status(devices):
	"""
	Outputs the status of all devices.

	@param devices list of devices
	"""
	for dev in devices:
		print('device {}'.format(devices.index(dev)), end=", ")
		# Print device id.
		print(sispm.getid(dev))
		# Print status of all outlets.
		for i in range(sispm.getminport(dev), 1 + sispm.getmaxport(dev)):
			print('\tstatus[{}] = {}'.format(i, sispm.getstatus(dev, i)))

def usage():
	"""
	Outputs the online help.
	"""
	print("Usage: sispmctl.py [OPTIONS]")
	print("Switches Enermax USB controlled plugstrips")
	print()
	print("  -D ID         id of device to be controlled")
	print("  -d DEVICE     index of device to be controlled")
	print("  -f OUTLET     switch outlet off")
	print("  -h            print this help")
	print("  -o OUTLET     switch outlet on")
	print("  -t OUTLET     toggle outlet")

if __name__ == "__main__":
	main()

