#!/usr/bin/python
#-*-coding: utf-8-*-
#
#  powerMeterWindow.py
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


#import sys
from PyQt4 import QtGui, QtCore
from src.util import resources
from src.engine import powerMeter

class PowerMeterWindow(QtGui.QWidget):
	
	def __init__(self):
		super(PowerMeterWindow, self).__init__()
		self.initUI()
		
	def initUI(self):
		dict_wavelength = {'820 nm':1, '1300 nm':2, 'LD':3}
		
		meas_button = QtGui.QPushButton(self.tr('Measure'), self)
		close_button = QtGui.QPushButton(self.tr('Close'), self)
		lab_wavelength = QtGui.QLabel(self.tr('Wavelength'))
		self.lab_pow_dBm = QtGui.QLabel('')
		self.lab_pow_w = QtGui.QLabel('')
		
		combo_wl = QtGui.QComboBox(self)
		[combo_wl.addItem(i) for i in dict_wavelength.keys()]
		
		meas_button.clicked.connect(lambda: self.measurement(dict_wavelength[str(combo_wl.currentText())]))
		close_button.clicked.connect(self.close)
		
		main_layout = QtGui.QVBoxLayout()
		
		l1 = QtGui.QHBoxLayout()
		l2 = QtGui.QHBoxLayout()
		l3 = QtGui.QHBoxLayout()
		
		l1.addWidget(lab_wavelength)
		l1.addWidget(combo_wl)
		l2.addWidget(self.lab_pow_dBm)
		l2.addWidget(self.lab_pow_w)
		l3.addStretch(1)
		l3.addWidget(meas_button)
		l3.addWidget(close_button)
		
		main_layout.addLayout(l1)
		main_layout.addLayout(l2)
		main_layout.addLayout(l3)
		
		self.setLayout(main_layout)
		self.setWindowTitle(self.tr('Optical power meter'))
		self.setWindowIcon(QtGui.QIcon(resources.getPath('icono.gif')))
		self.show()
	
	def measurement(self, wl):
		pm = powerMeter.PowerMeter(0x03)
		pm.set_lambda(wl)
		
		dbm, w = pm.get_power()
		
		'''
		# It is a very fast method, so it is possible to do an average
		# without adding a significant delay
		dbm = 0.0
		w = 0.0
		itera = 10
		for i in range(itera):
			a,b = pm.get_power()
			dbm += a
			w += b
		dbm /= itera
		w /= itera 
		
		dbm = dbm * (-1/100.0) #Due to Arduino  Modbus library data types
		w = w / 100.0
		'''
		
		self.lab_pow_dBm.setText('%.2f dBm' % (dbm,))
		self.lab_pow_w.setText(u'%.2f \u00b5W' % (w,))
