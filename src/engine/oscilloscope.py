#!/usr/bin/python
#-*-coding: utf-8-*-
#
#  oscilloscope.py
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

import usbtmc
import time
import os
from struct import unpack
from src.util import singleton

@singleton.Singleton
class Oscilloscope:
    
  def __init__(self):
	  '''
	  Oscilloscope constructor, initialize all dictionaries needed to assure that the values selected are consistent with values accepted by the scope.
	  
	  Without an oscilloscope connected on the USB port, application will fail.
	  
	  Params:
	  id: string 0xYYYY::0xZZZZ where YYYY is idVendor and ZZZZ idProduct of the scope 
	  '''
	  
	  # Dictionaries init
	  self.vol_div = {"5v":'5', "2v":'2', "1v":'1', "500mv":'500e-3', "200mv":'200e-3', "100mv":'100e-3', "50mv":'50e-3', "20mv":'20e-3', "10mv":'10e-3', "5mv":'5e-3', "2mv":'2e-3'}
	  self.sec_div = {"50s":'50', "25s":'25', "10s":'10', "5s":'5', "2.5s":'2.5', "1s":'1',"500ms":'500e-3', "250ms":'250e-3', "100ms":'100e-3',"50ms":'50e-3', "25ms":'25e-3', "10ms":'10e-3', "5ms":'5e-3', "2.5ms":'2.5e-3', "1ms":'1e-3', "500us":'500e-6', "250us":'250e-6', "100us":'100e-6',"50us":'50e-6', "25us":'25e-6', "10us":'10e-6', "5us":'5e-6', "2.5us":'2.5e-6', "1us":'1e-6', "500ns":'500e-9', "250ns":'250e-9', "100ns":'100e-9',"50ns":'50e-9', "25ns":'25e-9', "10ns":'10e-9', "5ns":'5e-9', "2.5ns":'2.5e-9'}
	  self.coupling = {"AC":'AC', "DC":'DC', "GND":'GND'}
	  self.channel = {"1":'CH1', "2":'CH2'}
	  self.att = {"1":'1', "10":'10'} 
	  self.bytes_meas = {"2":'2', "1":'1'}
	  self.measures = {"frecuencia":'FREQ', "periodo":'PERI', "vmedio":'MEAN', "vpp":'PK2', "vrms":'CRM', "vmin":'MINI', "vmax":'MAXI', "tsubida":'RIS', "tbajada":'FALL'}
	  self.ch_trigg = {"1":'CH1', "2":'CH2', "ext":'EXT', "ext5":'EXT5'}
	  
	  # Scope init
	  try:
		id = self.get_id()
		self.ins = usbtmc.Instrument("USB::%s::INSTR" % (id,))
	  except ValueError:
		from src.gui import InfoWindow
		warning = InfoWindow.InfoWindow("It looks like there is no oscilloscope connection.\nMake sure that it is connected or restart it and the relaunch the app")
      
  def get_id(self):
    usb = os.popen("lsusb | grep Tektronix") #Looking for a Tektronix device
    id = usb.read()
    id = id[23:32] #Getting is idNumber and idVendor
    id = id.replace(':', '::0x') #Formatting
    id = '0x%s' % (id,)
    return id
  
  
  def set_display(self, mode):
    if mode == "XY":
      self.ins.write("DIS:FORM XY")
    else:
      self.ins.write("DIS:FORM YT")
  
  def set_horizontal(self, time):
    hor = self.sec_div[time]
    self.ins.write("HOR:SCA %s" % (hor))
  
  def set_trigger(self, channel, level):
    ch = self.ch_trigg[channel]
    self.ins.write("TRIG:MAI:LEV %s;EDGE:SOU %s" % (str(level), ch))
  
  def set_vertical(self, channel, v_d, coupling, probe):
    ch = self.channel[channel]
    vdiv = self.vol_div[v_d]
    coup = self.coupling[coupling]
    att = self.att[probe]
    
    self.ins.write("%s:COUP %s;PRO %s;VOL %s" % (ch, coup, att, vdiv))
  
  def get_data(self, source, start, stop, width):
    tries = 0
    while tries < 8:
      try: 
        encoding = "RIB" #Between 127 y -128 using a byte
        ch = self.channel[source]
        self.ins.write("%s:POS 0.0" % (ch)) # Sets it to zero
        if start < 1:
          start = 1
        if stop > 2500:
          stop = 2500
        prec = self.bytes_meas[width]
        self.ins.write("DAT:ENC %s;SOU %s;STAR %s;STOP %s;WID %s" % (encoding, ch, str(start), str(stop), prec))
        
        points_div = 250 #2500 points / 10 divisions
        inc_t = float(self.ins.ask("HOR:MAI:SCA?")) / points_div
        v_div = float(self.ins.ask("%s:SCA?" % (ch)))
        
        points = self.ins.ask_raw("CURV?")
        header_length = 2 + int(points[1]) #Calculation of header length to avoid it
        points = points[header_length:-1]
        points = unpack('%sb' % len(points), points) #Conversion from signed integer
        
        if prec == '2':
          scale = 6553.4 #32767/5
        else:
          scale = 25.4 #127/5
        
        amplitude = [p*v_div/scale for p in points]
        return amplitude, inc_t
      
      except Exception as e:
        print('Excepcion')
        print e
        tries += 1
  
  def disp_channel(self, state, channel):
    ch = self.channel[channel]
    if(state == True):
      self.ins.write("SEL:%s ON" % (ch))
    else:
      self.ins.write("SEL:%s OFF" %(ch))
  
  def get_measure(self, channel, measure):
    # Sleep times are necessary because of oscilloscope time to configure and send a response
    ch = self.channel[channel]
    meas_type = self.measures[measure]
    tries = 0
    while tries < 5:
      try:
        self.ins.write_raw("MEASU:IMM:SOU %s" % (ch))
        time.sleep(0.5)
        self.ins.write_raw("MEASU:IMM:TYP %s" % (meas_type))
        time.sleep(0.5)
        value = self.ins.ask_raw("MEASU:IMM:VAL?")
        value = self.formatter(value)
        units = self.ins.ask_raw("MEASU:IMM:UNI?")
        value = value + units[1:-2] #To remove quotation marks
        
        return value
      except Exception as e:
        tries += 1
  
  def formatter(self, value):
    # decimal point + digits after it
    prec = 3
    
    index = value.find('E')
    number = float(value[0:index])
    exp = value[index:-1]
    
    # To assure it gets defined
    new_exp = exp
    mult = 1
    
    # Es una chapuza, probablemente iria mejor un diccionario o algo asi. Hay que darle una vuelta, de momento no corre prisa.
    if(exp == 'E-12'):
      mult = 1
      new_exp = 'p'
    if(exp == 'E-11'):
      mult = 10
      new_exp = 'p'
    if(exp == 'E-10'):
      mult == 100
      new_exp = 'p'
    if(exp == 'E-9'):
      mult = 1
      new_exp = 'n'
    if(exp == 'E-8'):
      mult = 10
      new_exp = 'n'
    if(exp == 'E-7'):
      mult = 100
      new_exp = 'n'
    if(exp == 'E-6'):
      mult = 1
      new_exp = '\u00b5'
    if(exp == 'E-5'):
      mult = 10
      new_exp = '\u00b5'
    if(exp == 'E-4'):
      mult = 100
      new_exp = '\u00b5'
    if(exp == 'E-3'):
      mult = 1
      new_exp = 'm'
    if(exp == 'E-2'):
      mult = 10
      new_exp = 'm'
    if(exp == 'E-1'):
      mult = 100
      new_exp = 'm'
    if(exp == 'E0'):
      mult = 1
      new_exp = ''
    if(exp == 'E1'):
      mult = 10
      new_exp = ''
    if(exp == 'E2'):
      mult = 100
      new_exp = ''
    if(exp == 'E3'):
      mult = 1
      new_exp = 'K'
    if(exp == 'E4'):
      mult = 10
      new_exp = 'K'
    if(exp == 'E5'):
      mult = 100
      new_exp = 'K'
    if(exp == 'E6'):
      mult = 1
      new_exp = 'M'
    if(exp == 'E7'):
      mult = 10
      new_exp = 'M'
    if(exp == 'E8'):
      mult = 100
      new_exp = 'M'
    if(exp == 'E9'):
      mult = 1
      new_exp = 'G'
    if(exp == 'E10'):
      mult = 10
      new_exp = 'G'
    if(exp == 'E11'):
      mult = 100
      new_exp = 'G'
    if(exp == 'E12'):
      mult = 1
      new_exp = 'T'
    
    num = str(number * mult)
    dot = num.find('.')
    num = num[0:(dot+prec)]
    num = num + ' ' + new_exp
    if num == '9.9 E37':
      num = 'Err '
    return num
  
  def autoset(self, channel):
    ch = self.channel[channel]
    units = {'V':'', 'mV':'E-3'}
    self.ins.write("%s:POS 0.0" % (ch))
    self.set_vertical(channel, '50mv', "AC", "1")
    time.sleep(0.5)
    measure = self.get_measure(channel, 'vpp')
    a, b = measure.split(' ')
    a = str(float(a)/6)
    c = units[b]
    self.ins.write("%s:VOL %s%s" % (ch,a,c))
  
  def set_persistence_off(self):
    self.ins.write("DIS:PERS OFF")
    
