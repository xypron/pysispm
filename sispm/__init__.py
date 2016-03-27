#!/usr/bin/env python
#
# Copyright (c) 2016, Heinrich Schuchardt <xypron.glpk@gmx.de>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Controling EnerGenie EG-PMS

A library to control the EnerGenie EG-PMS multiple socket outlet.

The EG-PMS has an USB interface. Four outlets (numbered 1 - 4) can be switched
on and off via USB.

The library depends on PyUSB (https://github.com/walac/pyusb).

sispm is licensed under a modified BSD license.
"""

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
	id =  dev.ctrl_transfer(0xa1, 0x01, 0x0301, 0, buf, 500)
	if (len(id) == 0):
		return None
	ret = ''
	sep = ''
	for x in id:
		ret += sep
		ret += format(x, '02x')
		sep = ':'
	return ret

def getstatus(dev, i):
	"""
	Gets the status of a device.

	@param dev: device
	@return: status
	"""
	assert i >= 1 and i < 5
	buf = bytes([3 * i, 0x03, 0x00, 0x00, 0x00]);
	buf = dev.ctrl_transfer(0xa1, 0x01, 0x0300 + 3 * i, 0, buf, 500)
	return 1 & buf[1]

def switchoff(dev, i):
	"""
	Switches device off.

	@param dev: device
	"""
	assert i >= 1 and i < 5
	buf = bytes([3 * i, 0x00, 0x00, 0x00, 0x00]);
	buf = dev.ctrl_transfer(0x21, 0x09, 0x0300 + 3 * i, 0, buf, 500)

def switchon(dev, i):
	"""
	Switches device on.

	@param dev: device
	"""
	assert i >= 1 and i < 5
	buf = bytes([3 * i, 0x03, 0x00, 0x00, 0x00]);
	buf = dev.ctrl_transfer(0x21, 0x09, 0x0300 + 3 * i, 0, buf, 500)

