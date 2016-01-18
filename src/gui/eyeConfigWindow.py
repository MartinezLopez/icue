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
    
    tit_ch = QtGui.QLabel('Channel')
    tit_rate = QtGui.QLabel('Rate')
    tit_length = QtGui.QLabel('Length')
    
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
    
    but_accept = QtGui.QPushButton('Acquire', self)
    
    grid.addWidget(tit_ch, 1, 1)
    grid.addWidget(tit_rate, 2, 1)
    grid.addWidget(tit_length, 3, 1)
    grid.addWidget(combo_ch, 1, 2)
    grid.addWidget(combo_rate, 2, 2)
    grid.addWidget(combo_length, 3, 2)
    grid.addWidget(but_accept, 4, 3)
    
    but_accept.clicked.connect(lambda: self.accept(combo_ch.currentText(), combo_rate.currentText(), combo_length.currentText()))
    
    self.setLayout(grid)
    self.setWindowTitle(u'Acquisition configuration')
    self.setWindowIcon(QtGui.QIcon(resources.getPath('icono.gif')))
    self.show()
    
  def accept(self, ch, rate, length):
		QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		self.eye = eyeDisplay.EyeDisplay(str(ch), rate, length)
		self.eye.show()
		QtGui.QApplication.restoreOverrideCursor()
		
		
    ## Diccionarios
    #base_tiempos = {"10 Mbps":'50ns', "30 Mbps":'10ns', "70 Mbps":'5ns', "125 Mbps":'2.5ns'}
    #length = {"4":0, "8":1, "12":2, "16":3}
    #rate = {"125 Mbps":3, "70 Mbps":2, "30 Mbps":1, "10 Mbps":0}
    
    ## Mostramos los dos canales del osciloscopio
    #self.osc.disp_channel(True, '1')
    #self.osc.disp_channel(True, '2')
    
    ## Llamada a Pines o a Modbus
    #'''
    #pines = PinesFPGA()
    #pines.setClock(1)
    
    #pines.setLength1(length[str(long_u)])
    #pines.setRate1(rate[str(tasa_u)])
    
    #pines.setLength2(length[str(long_d)])
    #pines.setRate2(rate[str(tasa_d)])
    #'''
    
    #self.osc.set_display("YT")
    #self.osc.set_persistence_off()
    #self.osc.set_horizontal(base_tiempos[str(tasa_u)]) #Por los qstring de qt4
    #self.osc.autoset('1')
    
    ## Configuramos el disparo
    #self.osc.set_trigger('ext', 1)
    #aviso = VentanaAviso('La adquisicion de datos puede tardar un tiempo.\n\nEspere, por favor.')
    #aviso.show()
    #self.disp_ojo = DisplayOjo()
    #lista_medidas1 = []
    #self.disp_ojo.show()
    
    ## Toma 32 trazas del osciloscopio
    #for i in range(32):
      #aviso.actualiza_barra(i)
      #QtCore.QCoreApplication.processEvents()
      #medidas1 , inc_tiempo1 = self.osc.get_data('1', 250, 1750, '1')
      #lista_medidas1.append(medidas1)
    
    ##pines.setClock(2)
    #self.osc.set_horizontal(base_tiempos[str(tasa_d)]) #Por los qstring de qt4
    #self.osc.autoset('2')
    
    #q = multiprocessing.Queue()
    #p1 = multiprocessing.Process(target=self.disp_ojo.update_t1, args=(lista_medidas1, inc_tiempo1,))
    #p1.start()
    #p2 = multiprocessing.Process(target=self.puntos2, args=(q,))
    #p2.start()
    #p2.join()
    
    #'''lista_medidas2 = []
    ## Toma 32 trazas del osciloscopio
    #for i in range(32):
      #aviso.actualiza_barra(i+32)
      ##QtCore.QCoreApplication.processEvents()
      #medidas2 , inc_tiempo2 = self.osc.get_data('2', 250, 1750, '1')
      #lista_medidas2.append(medidas2)
    #'''
    #lista_medidas2 = q.get()
    #inc_tiempo2 = q.get()
    #self.disp_ojo.update_t2(lista_medidas2, inc_tiempo2)
    
    ## Quitamos el disiparo externo
    #self.osc.set_trigger('1', 0)
    
    ##Quitamos los pines
    ##pines.quitGPIO()
  
  #def puntos2(self, q):
    #lista_medidas = []
    ## Toma 32 trazas del osciloscopio
    #for i in range(32):
      ##aviso.actualiza_barra(i+32)
      ##QtCore.QCoreApplication.processEvents()
      #medidas2 , inc_tiempo = self.osc.get_data('2', 250, 1750, '1')
      #lista_medidas.append(medidas2)
    #q.put(lista_medidas)
    #q.put(inc_tiempo)
