#!/usr/bin/python
#-*-coding: utf-8-*-
#
#  modbus.py
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

import serial
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
from src.util import singleton

@singleton.Singleton
class Modbus:
  
  def __init__(self):
    self.master = modbus_rtu.RtuMaster(serial.Serial(port="/dev/ttyAMA0", baudrate=9600, bytesize=8, parity='N', stopbits=2, xonxoff=0))
    self.master.set_timeout(1.0)
    self.master.set_verbose(False)
  
  def write_registers(self, slaveAddress, firstRegister, data):
    self.master.execute(slaveAddress, cst.WRITE_MULTIPLE_REGISTERS, firstRegister, output_value=data)
  
  def read_registers(self, slaveAddress, firstRegister, numRegisters):
    val = self.master.execute(slaveAddress, cst.READ_HOLDING_REGISTERS, firstRegister, numRegisters)
    return val
