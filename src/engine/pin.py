#!/usr/bin/python
#-*-coding: utf-8-*-
#
#  pin.py
#  
#  Author: Miguel Angel Martinez Lopez <miguelang.martinezl@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  Some code here is reused from Adafruit_Python_GPIO/Adafruit_GPIO/Platform.py
#  Copyright (c) 2014 Adafruit Industries
#  Author: Tony DiCola

import platform
import re
from src.util import singleton

@singleton.Singleton
class Pins:
  def __init__(self):  
    pi = self.pi_version()
    if pi is not None:
        import RPi.GPIO as _gpio #RbP
        self.pins = {'l1_ls': 12,'l1_ms': 11, 'r1_ls': 22, 'r1_ms': 21,'l2_ls': 16,'l2_ms': 15, 'r2_ls': 24, 'r2_ms': 23, 'sync_ls': 19, 'sync_ms': 18, 'rst': 13} #RbP
        _gpio.setmode(_gpio.BOARD) #RbP
        global gpio
	gpio = _gpio
    else:
	plat = platform.platform()
	if plat.lower().find('armv7l-with-debian') > -1:
		import Adafruit_BBIO.GPIO as _gpio #BBB
		self.pins = {'l1_ls': "P8_10",'l1_ms': "P8_8", 'r1_ls': "P8_14", 'r1_ms': "P8_12",'l2_ls': "P8_9",'l2_ms': "P8_7", 'r2_ls': "P8_13", 'r2_ms': "P8_11", 'sync_ls': "P8_18", 'sync_ms': "P8_16", 'rst': "P8_17"} #BBB
                global gpio
                gpio = _gpio
	
    [gpio.setup(self.pins[i], gpio.OUT) for i in self.pins.keys()]	
    [gpio.output(self.pins[i], gpio.LOW) for i in self.pins.keys()]
    self.reset(True)
		
  def pi_version(self):
    """Detect the version of the Raspberry Pi.  Returns either 1, 2 or
    None depending on if it's a Raspberry Pi 1 (model A, B, A+, B+),
    Raspberry Pi 2 (model B+), or not a Raspberry Pi.
    """
    # Check /proc/cpuinfo for the Hardware field value.
    # 2708 is pi 1
    # 2709 is pi 2
    # Anything else is not a pi.
    with open('/proc/cpuinfo', 'r') as infile:
        cpuinfo = infile.read()
    # Match a line like 'Hardware   : BCM2709'
    match = re.search('^Hardware\s+:\s+(\w+)$', cpuinfo,
                      flags=re.MULTILINE | re.IGNORECASE)
    if not match:
        # Couldn't find the hardware, assume it isn't a pi.
        return None
    if match.group(1) == 'BCM2708':
        # Pi 1
        return 1
    elif match.group(1) == 'BCM2709':
        # Pi 2
        return 2
    else:
        # Something else, not a pi.
        return None
  
  def setLength1(self, length):
    if length == 0:
      gpio.output(self.pins["l1_ms"], gpio.LOW)
      gpio.output(self.pins["l1_ls"], gpio.LOW)
    elif length == 1:
      gpio.output(self.pins["l1_ms"], gpio.LOW)
      gpio.output(self.pins["l1_ls"], gpio.HIGH)
    elif length == 2:
      gpio.output(self.pins["l1_ms"], gpio.HIGH)
      gpio.output(self.pins["l1_ls"], gpio.LOW)
    elif length == 3:
      gpio.output(self.pins["l1_ms"], gpio.HIGH)
      gpio.output(self.pins["l1_ls"], gpio.HIGH)
  
  def setRate1(self, rate):
    if rate == 0:
      gpio.output(self.pins["r1_ms"], gpio.LOW)
      gpio.output(self.pins["r1_ls"], gpio.LOW)
    elif rate == 1:
      gpio.output(self.pins["r1_ms"], gpio.LOW)
      gpio.output(self.pins["r1_ls"], gpio.HIGH)
    elif rate == 2:
      gpio.output(self.pins["r1_ms"], gpio.HIGH)
      gpio.output(self.pins["r1_ls"], gpio.LOW)
    elif rate == 3:
      gpio.output(self.pins["r1_ms"], gpio.HIGH)
      gpio.output(self.pins["r1_ls"], gpio.HIGH)
  
  def setLength2(self, length):
    if length == 0:
      gpio.output(self.pins["l2_ms"], gpio.LOW)
      gpio.output(self.pins["l2_ls"], gpio.LOW)
    elif length == 1:
      gpio.output(self.pins["l2_ms"], gpio.LOW)
      gpio.output(self.pins["l2_ls"], gpio.HIGH)
    elif length == 2:
      gpio.output(self.pins["l2_ms"], gpio.HIGH)
      gpio.output(self.pins["l2_ls"], gpio.LOW)
    elif length == 3:
      gpio.output(self.pins["l2_ms"], gpio.HIGH)
      gpio.output(self.pins["l2_ls"], gpio.HIGH)
  
  def setRate2(self, rate):
    if rate == 0:
      gpio.output(self.pins["r2_ms"], gpio.LOW)
      gpio.output(self.pins["r2_ls"], gpio.LOW)
    elif rate == 1:
      gpio.output(self.pins["r2_ms"], gpio.LOW)
      gpio.output(self.pins["r2_ls"], gpio.HIGH)
    elif rate == 2:
      gpio.output(self.pins["r2_ms"], gpio.HIGH)
      gpio.output(self.pins["r2_ls"], gpio.LOW)
    elif rate == 3:
      gpio.output(self.pins["r2_ms"], gpio.HIGH)
      gpio.output(self.pins["r2_ls"], gpio.HIGH)
  
  def setClock(self, clock):
    if clock == 1:
      gpio.output(self.pins["sync_ms"], gpio.LOW)
      gpio.output(self.pins["sync_ls"], gpio.LOW)
    if clock == 2:
      gpio.output(self.pins["sync_ms"], gpio.HIGH)
      gpio.output(self.pins["sync_ls"], gpio.LOW)
    if clock == 3: #SoF1
      gpio.output(self.pins["sync_ms"], gpio.LOW)
      gpio.output(self.pins["sync_ls"], gpio.HIGH)
    if clock == 4: #SoF2
      gpio.output(self.pins["sync_ms"], gpio.HIGH)
      gpio.output(self.pins["sync_ls"], gpio.HIGH)
  
  def reset(self, state):
    if state:
      gpio.output(self.pins["rst"], gpio.LOW)
      for i in range(100): # Losing some time
        a = i+1
      gpio.output(self.pins["rst"] , gpio.HIGH)
    else:
      gpio.output(self.pins["rst"], gpio.HIGH)
      
  def config(self, r1, l1, r2, l2, sync):
	  self.setRate1(r1)
	  self.setLength1(l1)
	  self.setRate2(r2)
	  self.setLength2(l2)
	  self.setClock(sync)
  
  def quitGPIO(self):
    gpio.cleanup()
