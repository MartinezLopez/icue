#!/usr/bin/python
#-*-coding: utf-8-*-
#
#  mainWindow.py
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
from src.gui import dispFreq
from src.gui import eyeConfigWindow
from src.gui import genConfigWindow
from src.gui import powerMeterWindow

from src.gui import testing

class MainWindow(QtGui.QWidget):
  
  def __init__(self):
    
    super(MainWindow, self).__init__()
    self.initUi()
  
  def initUi(self):
    
    grid = QtGui.QVBoxLayout()
    
    tit_aptd1 = QtGui.QLabel(u'Generator configuration')
    tit_aptd2 = QtGui.QLabel(u'Eye diagramm')
    tit_aptd3 = QtGui.QLabel(u'Optical power meter')
    tit_aptd4 = QtGui.QLabel(u'FFT')
    tit_aptd5 = QtGui.QLabel(u'Testing')
    
    but_a1 = QtGui.QPushButton('Go', self)
    but_a2 = QtGui.QPushButton('Go', self)
    but_a3 = QtGui.QPushButton('Go', self)
    but_a4 = QtGui.QPushButton('Go', self)
    but_a5 = QtGui.QPushButton('Go', self)
    but_close = QtGui.QPushButton('Close', self)
    
    but_a1.setFixedSize(60,30)
    but_a2.setFixedSize(60,30)
    but_a3.setFixedSize(60,30)
    but_a4.setFixedSize(60,30)
    but_a5.setFixedSize(60,30)
    but_close.setFixedSize(60,30)
    
    l1 = QtGui.QHBoxLayout()
    l2 = QtGui.QHBoxLayout()
    l3 = QtGui.QHBoxLayout()
    l4 = QtGui.QHBoxLayout()
    l5 = QtGui.QHBoxLayout()
    l6 = QtGui.QHBoxLayout()
    
    l1.addWidget(tit_aptd1)
    l1.addWidget(but_a1)
    l2.addWidget(tit_aptd2)
    l2.addWidget(but_a2)
    l3.addWidget(tit_aptd3)
    l3.addWidget(but_a3)
    l4.addWidget(tit_aptd4)
    l4.addWidget(but_a4)
    l5.addWidget(tit_aptd5)
    l5.addWidget(but_a5)
    l6.addWidget(but_close)
    
    but_close.clicked.connect(QtCore.QCoreApplication.instance().quit)
    but_a1.clicked.connect(self.gen_config)
    but_a2.clicked.connect(self.eye)
    but_a3.clicked.connect(self.power_meter)
    but_a4.clicked.connect(self.fft)
    but_a5.clicked.connect(self.testing)
    
    grid.addLayout(l1)
    grid.addLayout(l2)
    grid.addLayout(l3)
    grid.addLayout(l4)
    grid.addLayout(l5)
    grid.addLayout(l6)
    
    self.setLayout(grid)
    self.setWindowTitle(u'Sistemas de Comunicación')
    self.setWindowIcon(QtGui.QIcon(resources.getPath('icono.gif')))
    self.setFixedSize(440,250)
    self.show()
    
  def gen_config(self):
    self.gen_window = genConfigWindow.GenConfigWindow()
  
  def eye(self):
    self.eye_config = eyeConfigWindow.EyeConfigWindow()
    
  def power_meter(self):
	  self.pow_meter = powerMeterWindow.PowerMeterWindow()
  
  def fft(self):
    self.spectrum = dispFreq.DispFreq()
  
  def testing(self):
	  self.response = testing.ResponseWindow()
