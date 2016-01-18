#!/usr/bin/python
#-*-coding: utf-8-*-
#
#  warningWindow.py
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

class WarningWindow(QtGui.QDialog):
  '''
  No button
  '''
  
  def __init__(self, text):
    QtGui.QDialog.__init__(self)
    self.setModal(True)
    self.initUi(text)
  
  def initUi(self, text):
    grid = QtGui.QGridLayout()
    grid.setSpacing(5)
    
    warn = QtGui.QLabel(text)
    self.bar = QtGui.QProgressBar(self)
    self.bar.setMinimum(1)
    self.bar.setMaximum(64)

    grid.addWidget(warn, 1, 1)
    grid.addWidget(self.bar, 2, 1)
    
    self.setLayout(grid) 
    self.setGeometry(200, 200, 200, 200)
    self.setWindowTitle('Warning!')
    self.setWindowIcon(QtGui.QIcon(resources.getPath('icono.gif'))) 
    
  def refresh_bar(self, val):
    self.bar.setValue(val)
