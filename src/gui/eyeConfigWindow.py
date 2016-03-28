#!/usr/bin/python
#-*-coding: utf-8-*-
#
#  eyeConfigWindow.py
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


import sys
from PyQt4 import QtGui, QtCore
from src.util import resources
from src.gui import eyeDisplay

class EyeConfigWindow(QtGui.QWidget):
  
  def __init__(self):
    super(EyeConfigWindow, self).__init__()
    self.initUi()
  
  def initUi(self):
    grid = QtGui.QGridLayout()
    grid.setSpacing(5)
    
    tit_ch = QtGui.QLabel(self.tr('Channel'))
    tit_rate = QtGui.QLabel(self.tr('Rate'))
    tit_length = QtGui.QLabel(self.tr('Length'))
    
    combo_rate = QtGui.QComboBox(self)
    combo_length = QtGui.QComboBox(self)
    combo_ch = QtGui.QComboBox(self)
    
    rates = ["10 Mbps","30 Mbps","70 Mbps","125 Mbps"]
    lengths = ["4", "8", "12", "16"]
    channels = ['1', '2']
    
    for r in rates:
      combo_rate.addItem(r)
    for l in lengths:
      combo_length.addItem(l)
    for c in channels:
      combo_ch.addItem(c)
    
    but_accept = QtGui.QPushButton(self.tr('Acquire'), self)
    
    grid.addWidget(tit_ch, 1, 1)
    grid.addWidget(tit_rate, 2, 1)
    grid.addWidget(tit_length, 3, 1)
    grid.addWidget(combo_ch, 1, 2)
    grid.addWidget(combo_rate, 2, 2)
    grid.addWidget(combo_length, 3, 2)
    grid.addWidget(but_accept, 4, 3)
    
    but_accept.clicked.connect(lambda: self.accept(combo_ch.currentText(), combo_rate.currentText(), combo_length.currentText()))
    
    self.setLayout(grid)
    self.setWindowTitle(self.tr('Acquisition configuration'))
    self.setWindowIcon(QtGui.QIcon(resources.getPath('icono.gif')))
    self.show()
    
  def accept(self, ch, rate, length):
		QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		self.eye = eyeDisplay.EyeDisplay(str(ch), str(rate), str(length))
		self.eye.show()
		QtGui.QApplication.restoreOverrideCursor()
