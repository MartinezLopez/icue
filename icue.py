#!/usr/bin/python
#-*-coding: utf-8-*-
#
#  icue.py
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

import os, sys
from PyQt4 import QtGui, QtCore
from src.util import resources
resources.setBasePath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./res"))
from src.gui import mainWindow

def main():
  app = QtGui.QApplication(sys.argv)
  app.setStyle("cleanlooks")
  main_window = mainWindow.MainWindow()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
