#!/usr/bin/python
#-*-coding: utf-8-*-
#
#  infoWindow.py
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

class InfoWindow(QtGui.QWidget):
  '''
  Accept button
  '''

  def __init__(self, text):
    super(InfoWindow, self).__init__()
    self.initUi(text)

  def initUi(self, text):
    win = QtGui.QMessageBox()
    win.timer = QtCore.QTimer(self)
    win.timer.timeout.connect(win.close)
    win.timer.start(10000) # It is automatically closed after 10 secs
    win.setInformativeText(text)
    win.setWindowTitle('Warning!')
    win.setWindowIcon(QtGui.QIcon(resources.getPath('icono.gif')))
    win.exec_()
