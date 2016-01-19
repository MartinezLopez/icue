#!/usr/bin/python
#-*-coding: utf-8-*-
#
#  genConfigWindow.py
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

from PyQt4 import QtGui, QtCore
from src.util import resources
from src.engine import pin

class GenConfigWindow(QtGui.QWidget):
  
  def __init__(self):
    super(GenConfigWindow, self).__init__()
    
    grid = QtGui.QGridLayout()
    grid.setSpacing(5)
    
    tit_rate1 = QtGui.QLabel('Rate 1')
    tit_rate2 = QtGui.QLabel('Rate 2')
    tit_len1 = QtGui.QLabel('Length 1')
    tit_len2 = QtGui.QLabel('Length 2')
    tit_sync = QtGui.QLabel('Sync')
    
    rates = ["10 Mbps","30 Mbps","70 Mbps","125 Mbps"]
    lengths = ["4", "8", "12", "16"]
    
    combo_rate1 = QtGui.QComboBox(self)
    combo_rate2 = QtGui.QComboBox(self)
    combo_len1 = QtGui.QComboBox(self)
    combo_len2 = QtGui.QComboBox(self)
    combo_sync = QtGui.QComboBox(self)
    
    for r in rates:
      combo_rate1.addItem(r)
      combo_rate2.addItem(r)
    
    for l in lengths:
      combo_len1.addItem(l)
      combo_len2.addItem(l)
    
    combo_sync.addItem('Sync 1')
    combo_sync.addItem('Sync 2')
    combo_sync.addItem('SoF 1')
    combo_sync.addItem('SoF 2')
    
    but_accept = QtGui.QPushButton('Ok', self)
    
    grid.addWidget(tit_rate1, 1, 1)
    grid.addWidget(combo_rate1, 1, 2)
    grid.addWidget(tit_len1, 1, 3)
    grid.addWidget(combo_len1, 1, 4)
    
    grid.addWidget(tit_rate2, 2, 1)
    grid.addWidget(combo_rate2, 2, 2)
    grid.addWidget(tit_len2, 2, 3)
    grid.addWidget(combo_len2, 2, 4)
    
    grid.addWidget(tit_sync, 3, 2)
    grid.addWidget(combo_sync, 3, 3)
    grid.addWidget(but_accept, 3, 5)
    
    but_accept.clicked.connect(lambda: self.accept(combo_rate1.currentText(), combo_rate2.currentText(), combo_len1.currentText(), combo_len2.currentText(), combo_sync.currentText()))
    
    self.setLayout(grid)
    self.setWindowTitle(u'Generator configuration')
    self.setWindowIcon(QtGui.QIcon(resources.getPath('icono.gif')))
    self.setFixedSize(420, 130)
    self.show()
    
  def accept(self, rate1, rate2, len1, len2, sync):
    length = {"4":0, "8":1, "12":2, "16":3}
    rate = {"10 Mbps":0, "30 Mbps":1, "70 Mbps":2, "125 Mbps":3}
    syn = {'Sync 1':1, 'Sync 2':2, 'SoF 1':3, 'SoF 2':4}
    
    pins = pin.Pins.Instance()
    pins.setClock(syn[str(sync)])
    pins.setLength1(length[str(len1)])
    pins.setRate1(rate[str(rate1)])
    pins.setLength2(length[str(len2)])
    pins.setRate2(rate[str(rate2)])
