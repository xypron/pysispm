#!/usr/bin/python3
'''
file printenv.py - print U-Boot environment

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

"""
This example demonstrates how to access U-Boot when a computer is being
switched on.

After toggling power off and on the script waits for serial output from
U-Boot to appear. It issues two CRs to enter U-Boot. The printenv command is
used to print the environment variables. At last the computer is switched off
again.

Please, adjust device id, outlet number and serial port as required.
"""

import serial
import sispm
import time

id = '01:01:53:50:26'
port = 1
tty = '/dev/ttyUSB0'

def skip_output(ser, test = None):
	"""
	Reads serial input until a test string is reached.

	@param ser: serial connection
	@param test: string to test for
	"""
	
	line = ''
	while True:
		c = ser.read(1)
		if (len(c) == 0):
			break
		if (c[0] == 0x0d):
			print(line)
			line = ''
		elif (c[0] >= 32 and c[0] < 128):
			line += chr(c[0])
			if (test and line.find(test) != -1):
				break
	print(line)


# Find Enermax devices.
devices = sispm.connect()

# Were they found?
if len(devices) == 0:
	print('No device found')
	quit()

# Find the device with the correct id
dev = None
for d in devices:
	if sispm.getid(d) == id:
		dev = d
		break

if dev is None:
	print('Device ' + id + ' not found')
	quit()

# Open serial connection
ser = serial.Serial(
	port = tty, \
	baudrate =  115200, \
	stopbits = serial.STOPBITS_ONE, \
	bytesize = serial.EIGHTBITS, \
	timeout = 5)

# Switch device off
print("== Switching off ==")
sispm.switchoff(dev, port)

# Wait for two seconds
time.sleep(2)

# Switch device on
print("== Switching on ==")
sispm.switchon(dev, port)

# Wait for U-Boot message
skip_output(ser, 'stop autoboot:')

# Stop boot process
ser.write(b'\r\r')
skip_output(ser)

# Print environment
ser.write(b'printenv\n')
skip_output(ser)

# Switch device off
print("== Switching off ==")
sispm.switchoff(dev, port)

# Close serial connection
ser.close()

