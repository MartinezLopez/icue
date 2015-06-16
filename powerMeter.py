#!/usr/bin/python
#-*-coding: utf-8-*-
#
#  powerMeter.py
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

from modbus import Modbus

class PowerMeter:
	
	def __init__(self, address):
		self.address = address
		self.mbID = 0x04
		
	def set_lambda(self, wavelength):
		mb = Modbus.Instance()
		mb.write_registers(self.address, 3, [wavelength]) # Register for lambda is number 3 on arduino implementation
	
	def get_power(self):
		mb = Modbus.Instance()
		#rcv_id, w, dbm = mb.read_registers(self.address, 0, 3)
		
		# It is a very fast method, so it is possible to do an average
		# without adding a significant delay
		dbm = 0.0
		w = 0.0
		itera = 10
		for i in range(itera):
			rcv_id, b, a = mb.read_registers(self.address, 0, 3)
			dbm += a
			w += b
		dbm /= itera
		w /= itera 
		
		dbm *= (-1/100.0) #Due to Arduino  Modbus library data types
		w /= 100.0
		
		if rcv_id == self.mbID:
			return dbm, w
		else:
			return 'Err', 'Err'
