#!/usr/bin/python3
'''
file sispmctl.py - controling EnerGenie EG-PMS

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

import usb.core
import usb.util

def connect():
	"""
	Returns the list of compatible devices.

	@return: device list
	"""
	ret = list()
	ret += list(usb.core.find(find_all=True,
		idVendor=0x04b4, idProduct=0xfd10))
	ret += list(usb.core.find(find_all=True,
		idVendor=0x04b4, idProduct=0xfd11))
	ret += list(usb.core.find(find_all=True,
		idVendor=0x04b4, idProduct=0xfd12))
	ret += list(usb.core.find(find_all=True,
		idVendor=0x04b4, idProduct=0xfd13))
	return ret

def getid(dev):
	"""
	Gets the id of a device.

	@return: id
	"""
	buf = bytes([0x00, 0x00, 0x00, 0x00, 0x00]);
	return dev.ctrl_transfer(0xa1, 0x01, 0x0301, 0, buf, 500)

def getstatus(dev, i):
	"""
	Gets the status of a device.

	@param dev: device
	@return: status
	"""
	assert i >= 0 and i < 4
	buf = bytes([3 * i, 0x03, 0x00, 0x00, 0x00]);
	buf = dev.ctrl_transfer(0xa1, 0x01, 0x0300 + 3 * i, 0, buf, 500)
	return 1 & buf[1]

def printid(id):
	"""
	Prints the id of a device.

	@param id: id
	"""
	print("id = ", end="")
	sep=""
	for x in id:
		print(sep, end="")
		print(format(x, '02x'), end="")
		sep=":"
	print()

def switchoff(dev, i):
	"""
	Switches device off.

	@param dev: device
	"""
	assert i >= 0 and i < 4
	buf = bytes([3 * i, 0x00, 0x00, 0x00, 0x00]);
	buf = dev.ctrl_transfer(0x21, 0x09, 0x0300 + 3 * i, 0, buf, 500)

def switchon(dev, i):
	"""
	Switches device on.

	@param dev: device
	"""
	assert i >= 0 and i < 4
	buf = bytes([3 * i, 0x03, 0x00, 0x00, 0x00]);
	buf = dev.ctrl_transfer(0x21, 0x09, 0x0300 + 3 * i, 0, buf, 500)

# Find our devices.
devices = connect()

# Were they found?
if len(devices) == 0:
	print('No device found')
	exit

for dev in devices:
	print('device {}'.format(devices.index(dev)), end=", ")
	# Set the active configuration.
	dev.set_configuration(1)
	# Print device id.
	printid(getid(dev))
	# Print status of all outlets.
	for i in range(0, 4):
		print('\tstatus[{}] = {}'.format(i, getstatus(dev, i)))
	# Switch off outlet 2.
	switchoff(dev, 2)
