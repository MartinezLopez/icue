#!/usr/bin/python
#-*-coding: utf-8-*-
#
#  ventana.py
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
from osciloscopio import Osciloscopio
#from modbus import *
#from pines import *
import numpy as np
import time
import math
import pylab
from scipy.special import erfc
import logging

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter, MultipleLocator
from matplotlib.widgets import Cursor, Slider
from matplotlib.patches import Rectangle

class VentanaInfo(QtGui.QWidget):
  '''Tiene un boton aceptar para volver al orden de ejecucion'''
  
  def __init__(self, texto):
    '''Constructor de una ventana de informacion
    
    Parametros:
      texto: Texto que mostrara la ventana
    
    '''
    super(VentanaInfo, self).__init__()
    self.inicializa(texto)
  
  def inicializa(self, texto):
    win = QtGui.QMessageBox()
    win.timer = QtCore.QTimer(self)
    win.timer.timeout.connect(win.close)
    win.timer.start(10000) # Se cierra automaticamente a los 10 segundos
    win.setInformativeText(texto)
    win.setWindowTitle('Aviso')
    win.setWindowIcon(QtGui.QIcon('%s/img/icono.gif' % sys.path[0]))
    win.exec_()

class VentanaAviso(QtGui.QDialog):
  '''No tiene boton'''
  
  def __init__(self, texto):
    QtGui.QDialog.__init__(self)
    self.setModal(True)
    self.inicializa(texto)
  
  def inicializa(self, texto):
    grid = QtGui.QGridLayout()
    grid.setSpacing(5)
    
    aviso = QtGui.QLabel(texto)
    self.barra = QtGui.QProgressBar(self)
    self.barra.setMinimum(1)
    self.barra.setMaximum(64)

    grid.addWidget(aviso, 1, 1)
    grid.addWidget(self.barra, 2, 1)
    
    self.setLayout(grid) 
    self.setGeometry(200, 200, 200, 200)
    self.setWindowTitle('Aviso')
    self.setWindowIcon(QtGui.QIcon('%s/img/icono.gif' % sys.path[0]))
    
  def actualiza_barra(self, val):
    self.barra.setValue(val)

class VentanaPrincipal(QtGui.QWidget):
  
  def __init__(self):
    ''' Constructor de la ventana de inicio de la aplicacion.
    
    Parametros:
      osciloscopio: Objeto de la clase Osciloscopio
    
    '''
    
    super(VentanaPrincipal, self).__init__()
    self.rellenaVentana()
  
  def rellenaVentana(self):
    
    grid = QtGui.QVBoxLayout()
    
    tit_aptd1 = QtGui.QLabel(u'Configuración del generador')
    tit_aptd2 = QtGui.QLabel(u'Adquisición diagrama de ojo')
    
    bot_a1 = QtGui.QPushButton('Ir', self)
    bot_a2 = QtGui.QPushButton('Ir', self)
    bot_cerrar = QtGui.QPushButton('Cerrar', self)
    bot_a1.setFixedSize(60,30)
    bot_a2.setFixedSize(60,30)
    bot_cerrar.setFixedSize(60,30)
    
    l1 = QtGui.QHBoxLayout()
    l2 = QtGui.QHBoxLayout()
    l3 = QtGui.QHBoxLayout()
    
    l1.addWidget(tit_aptd1)
    l1.addWidget(bot_a1)
    l2.addWidget(tit_aptd2)
    l2.addWidget(bot_a2)
    l3.addWidget(bot_cerrar)
    
    bot_cerrar.clicked.connect(QtCore.QCoreApplication.instance().quit)
    bot_a1.clicked.connect(lambda: self.long_trama())
    bot_a2.clicked.connect(lambda: self.ojo())
    
    grid.addLayout(l1)
    grid.addLayout(l2)
    grid.addLayout(l3)
    
    self.setLayout(grid)
    self.setWindowTitle(u'Sistemas de Comunicación')
    self.setWindowIcon(QtGui.QIcon('%s/img/icono.gif' % sys.path[0]))
    self.setFixedSize(280,150)
    self.show()
    
  def long_trama(self):
    self.c_trama = VentanaConfigIO()
  
  def ojo(self):
    self.ConfOjo = VentanaConfigOjo()

class VentanaConfigOjo(QtGui.QWidget):
  
  def __init__(self):
    ''' Constructor de la ventana de configuracion del diagrama de ojo.
    
    
    
    '''
    
    super(VentanaConfigOjo, self).__init__()
    self.rellenaVentana()
  
  def rellenaVentana(self):
    
    grid = QtGui.QGridLayout()
    grid.setSpacing(5)
    
    #tit_up = QtGui.QLabel('Uplink')
    #tit_dw = QtGui.QLabel('Downlink')
    tit_ch = QtGui.QLabel('Canal')
    tit_tasa = QtGui.QLabel('Tasa binaria')
    #tit_tasa_d = QtGui.QLabel('Tasa binaria')
    tit_long = QtGui.QLabel('Longitud de trama')
    #tit_long_d = QtGui.QLabel('Longitud de trama')
    
    desp_tasa = QtGui.QComboBox(self)
    #desp_tasa_d = QtGui.QComboBox(self)
    desp_long = QtGui.QComboBox(self)
    #desp_long_d = QtGui.QComboBox(self)
    desp_ch = QtGui.QComboBox(self)
    
    tasas = ["10 Mbps","30 Mbps","70 Mbps","125 Mbps"]
    longitudes = ["4", "8", "12", "16"]
    canales = ['1', '2']
    
    for t in tasas:
      desp_tasa.addItem(t)
      #desp_tasa_d.addItem(t)
    for l in longitudes:
      desp_long.addItem(l)
      #desp_long_d.addItem(l)
    for c in canales:
      desp_ch.addItem(c)
    
    
    bot_aceptar = QtGui.QPushButton('Adquirir', self)
    
    '''grid.addWidget(tit_up, 0, 1)
    grid.addWidget(tit_dw, 0, 4)
    grid.addWidget(tit_tasa_u, 2, 1)
    grid.addWidget(tit_tasa_d, 2, 4)
    grid.addWidget(tit_long_u, 3, 1)
    grid.addWidget(tit_long_d, 3, 4)
    grid.addWidget(desp_tasa_u, 2, 2)
    grid.addWidget(desp_tasa_d, 2, 5)
    grid.addWidget(desp_long_u, 3, 2)
    grid.addWidget(desp_long_d, 3, 5)
    grid.addWidget(bot_aceptar, 6, 3)
    '''
    grid.addWidget(tit_ch, 1, 1)
    grid.addWidget(tit_tasa, 2, 1)
    grid.addWidget(tit_long, 3, 1)
    grid.addWidget(desp_ch, 1, 2)
    grid.addWidget(desp_tasa, 2, 2)
    grid.addWidget(desp_long, 3, 2)
    grid.addWidget(bot_aceptar, 4, 3)
    
    
    bot_aceptar.clicked.connect(lambda: self.aceptar(desp_ch.currentText(), desp_tasa.currentText(), desp_long.currentText()))
    
    self.setLayout(grid)
    self.setWindowTitle(u'Configuración de la adquisición')
    self.setWindowIcon(QtGui.QIcon('%s/img/icono.gif' % sys.path[0]))
    self.show()
    
  def aceptar(self, ch, tasa, long):
          QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
	  self.ojo = DisplayOjo(str(ch), tasa, long)
	  self.ojo.show()
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
    

class DisplayOjo(QtGui.QWidget):
	
	def __init__(self, ch, rate, length):
		super(DisplayOjo, self).__init__()
		
		self.osc = Osciloscopio.Instance()
		
		self.timer_osc = QtCore.QTimer()
		self.timer_draw = QtCore.QTimer()
		
		logging.basicConfig(level=logging.DEBUG) # Trazas para comprobar el correcto funcionamiento
		self.setWindowTitle('Diagrama de ojo del canal %s' % (ch,))
		self.setWindowIcon(QtGui.QIcon('%s/img/icono.gif' % sys.path[0]))
		self.setFixedSize(900,700)
		
		# Hacemos las medidas disponibles a todo el objeto
		self.lista_medidas = []
		self.inc_tiempo = 0
		
		self.configura(ch, rate, length)
		self.crea_interfaz()
		
		QtCore.QObject.connect(self.timer_draw, QtCore.SIGNAL("timeout()"), self.actualiza_datos)
        	QtCore.QObject.connect(self.timer_osc, QtCore.SIGNAL("timeout()"), lambda chan=ch: self.adquiere(chan))
        	
        	self.timer_osc.start(700)
		self.timer_draw.start(5000)
		
	def crea_interfaz(self):
		self.figure = plt.figure(1)
		self.canvas = FigureCanvas(self.figure)
		self.canvas.setParent(self)
		
		self.ax1 = plt.subplot2grid((2,2),(0,0), colspan=2) #Diagrama de ojo
		self.ax2 = plt.subplot2grid((2,2),(1,0))            #Histogramas
		self.ax3 = plt.subplot2grid((2,2),(1,1))            #erfc
		plt.subplots_adjust(left=0.15, right=0.85, bottom=0.1, top=0.9, hspace=0.25)
    
		# Creamos los formatos que van a mostrar las unidades que se pintan
		formatter_tiempo = EngFormatter(unit='s', places=1)
		formatter_amp = EngFormatter(unit='v', places=1)
		
		self.ax1.set_xlabel('tiempo')
		self.ax1.set_ylabel('amplitud')
		self.ax1.xaxis.set_major_formatter(formatter_tiempo)
		self.ax1.yaxis.set_major_formatter(formatter_amp)
		#self.ax1.xaxis.set_minor_locator(MultipleLocator(self.inc_tiempo_t1 * 25))
		self.ax1.yaxis.set_minor_locator(MultipleLocator(0.5))
		
		 # Pintamos la erfc
		eje_x = np.arange(0, 10, 0.5)
		self.ax3.semilogy(eje_x, 0.5*erfc(eje_x/math.sqrt(2)), color='#08088a')
		
		logging.debug('se crea el eje semilogaritmico')
    		
		self.ax3.set_xlabel('q')
		self.ax3.set_ylabel('BER')
		
		# Creamos las barras horizontales y verticales de los subplots
		self.barMuestreo = self.ax1.axvline(linewidth=3, x=0, color='blue')
		self.barUmbral = self.ax1.axhline(linewidth=3, y=0, color='green')
		self.barDecision2 = self.ax2.axvline(x=0, color='green')
		self.bar_q = self.ax3.axvline(x=10, color='blue', linestyle='--') # Valor distinto de cero para el logaritmo
		self.bar_ber = self.ax3.axhline(y=10, color='blue', linestyle='--')
		
		# Creamos la fuente que se va a usar
		font = QtGui.QFont()
		font.setFamily(QtCore.QString.fromUtf8("Helvetica"))
		font.setPixelSize(17)
		
		# Esto hay que hacerlo antes de dibujar para que pueda poner los valores medios, q y la ber
		self.resultados_label = QtGui.QLabel(self)
		self.resultados_label.setFont(font)
		
		# Barra de herramientas de matplotlib
		self.mpl_toolbar = NavigationToolbar(self.canvas, self)
		
		# Boton de parada de la adquisicion
		bot_stop = QtGui.QPushButton(u'Detener la adquisición', self)
		bot_stop.clicked.connect(self.stopAdq)
		
		hbox = QtGui.QHBoxLayout()
		
		hbox.addStretch(1)
		hbox.addWidget(bot_stop)
		
		# Anadimos los elementos al layout
		p1 = QtGui.QVBoxLayout()
		p1.addWidget(self.canvas)
		p1.addWidget(self.mpl_toolbar)
		p1.addWidget(self.resultados_label)
		p1.addLayout(hbox)
		self.setLayout(p1)
		
		# Se gestionan los clicks del raton
		self.cid = self.figure.canvas.mpl_connect('button_press_event', self.on_press)
		
	def actualiza_datos(self):
		self.ax1.hold(True)
		#for i in range(len(self.lista_medidas)):
		#	self.ax1.plot(self.lista_tiempo, self.lista_medidas[i], '#0b610b')
		[self.ax1.plot(self.lista_tiempo, self.lista_medidas[i], '#0b610b') for i in xrange(len(self.lista_medidas))]
		self.ax1.hold(False)
		self.figure.canvas.draw()
		
	def on_press(self, event):
		QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		QtCore.QCoreApplication.processEvents()
		valMuestreo = event.xdata
		#valUmbral = event.ydata
		
		self.intervalo_amplitud = self.ax1.yaxis.get_data_interval()
		
		if (valMuestreo < 0) or (valMuestreo > self.lista_tiempo[len(self.lista_tiempo)-1]):
			valMuestreo = self.lista_tiempo[(len(self.lista_tiempo)-1)/2]
		#if (valUmbral < self.intervalo_amplitud[0]) or (valUmbral > self.intervalo_amplitud[1]):
		valUmbral = (self.intervalo_amplitud[0] + self.intervalo_amplitud[1]) / 2
		
		logging.debug('muestreo %s umbral %s', str(valMuestreo), str(valUmbral))    
		self.dibuja(valMuestreo, valUmbral)
    
	def dibuja(self, muestreo, umbral):
		# Para que no se actualice mientras pinte y no bloquee al otro proceso
		lista_medidas = self.lista_medidas
		inc_tiempo = self.inc_tiempo
		
		logging.debug('entramos en dibuja')
		puntoMuestreo = int(muestreo/inc_tiempo)
		amp = []
		
		'''for i in range(len(lista_medidas)): # Guardamos los puntos entre mas y menos 25 posiciones del punto de muestreo de todas las tramas guardadas
			for j in range(-25, 25):
				try:
					amp.append(lista_medidas[i][puntoMuestreo + j])
				except IndexError:
					logging.debug('oob')
		'''
		for i in xrange(len(lista_medidas)): # Guardamos los puntos entre mas y menos 25 posiciones del punto de muestreo de todas las tramas guardadas
			try:
				[amp.append(lista_medidas[i][puntoMuestreo + j]) for j in xrange(-25, 25)]
			except IndexError:
				logging.debug('oob')
		
		# Discriminamos segun el umbral
		val0 = []
		val1 = []
		
		ap0 = val0.append
		ap1 = val1.append
		
		for i in xrange(len(amp)):
			if(amp[i] < umbral):
				ap0(amp[i])
			else:
				ap1(amp[i])
		
		'''for i in range(len(amp)):
			if(amp[i] < umbral):
				val0.append(amp[i])
			else:
				val1.append(amp[i])
		'''
		
		
		# Pintamos los histogramas y las gaussianas
		self.ax2.cla()
		self.ax2.set_xlabel('amplitud')
		norm0, bins, patches = self.ax2.hist(val0, bins=200,range=[(5/4)*self.intervalo_amplitud[0], (5/4)*self.intervalo_amplitud[1]], normed=True, histtype='step', color='#8181f7', rwidth=100)
		
		norm1, bins, patches = self.ax2.hist(val1, bins=200,range=[(5/4)*self.intervalo_amplitud[0], (5/4)*self.intervalo_amplitud[1]], normed=True, histtype='step', color='#fa5858', rwidth=100)
		
		v0, sigma0 = self.media_y_varianza(val0)
		gauss0 = pylab.normpdf(bins, v0, sigma0)
		self.ax2.plot(bins, gauss0, linewidth=2, color='#0404b4')#azul
		
		v1, sigma1 = self.media_y_varianza(val1)
		gauss1 = pylab.normpdf(bins, v1, sigma1)
		self.ax2.plot(bins, gauss1, linewidth=2, color='#b40404')#rojo
		
		# Calculamos la ber
		q = math.fabs(v1-v0)/(sigma1+sigma0)
		ber = 0.5*erfc(q/math.sqrt(2))
		
		self.muestra_resultados(v0, sigma0, v1, sigma1, q, ber, len(val0), len(val1))
		
		# Recolocamos todas las barras
		self.ax2.add_line(self.barDecision2) # Vuelve a pintar la barra del umbral cuando se redibuja
		self.ax3.add_line(self.bar_q)
		self.ax3.add_line(self.bar_ber)
		self.barMuestreo.set_xdata(muestreo)
		self.barUmbral.set_ydata(umbral)
		self.barDecision2.set_xdata(umbral)
		logging.debug('colocamos las barras en ax3')
		self.bar_q.set_xdata(q)
		self.bar_ber.set_ydata(ber)
		logging.debug('colocadas')
		
		self.canvas.draw()
		logging.debug('ya se ha redibujado')
		QtCore.QCoreApplication.processEvents()
		QtGui.QApplication.restoreOverrideCursor()
	
	def muestra_resultados(self, v0, sigma0, v1, sigma1, q, ber, num0, num1):
		string = '\tv0: %-*s Sigma 0: %-*s N. muestras 0: %-*s Q: %-*s \n\n\tv1: %-*s Sigma 1: %-*s N. muestras 1: %-*s BER: %.2e' % (17, str(round(v0*1000,1))+' mV', 17, str(round(sigma0*1000,1))+' mV', 17, str(num0), 17, str(round(q,2)), 17, str(round(v1*1000,1))+' mV', 17, str(round(sigma1*1000,1))+' mV', 17, str(num1), ber)
		self.resultados_label.setText(string)
	
	def media_y_varianza(self, data):
		media = 0.0
		var = 0.0
		n = len(data)
		for i in xrange(n):
			media += data[i]
		media = media/n
		cuad = math.pow
		for i in xrange(n):
			var += cuad(media - data[i], 2)
		var = math.sqrt(var / (n-1))
		return media, var
		
	def configura(self, ch, rate, length):
		a=3
		
	def adquiere(self, ch):
		medidas, inc = self.osc.get_data(ch, 250, 1750, '1') # Hay que cambiar el 1 por el canal seleccionado
		self.lista_medidas.append(medidas)
		self.inc_tiempo = inc
		self.lista_tiempo = []
		#for i in range(len(medidas)):
		#	self.lista_tiempo.append(inc*i)
		[self.lista_tiempo.append(inc*i) for i in xrange(len(medidas))]
	
	def closeEvent(self, evnt):
		self.timer_osc.stop()
		self.timer_draw.stop()
		super(DisplayOjo, self).closeEvent(evnt)
	
	def stopAdq(self):
		self.timer_osc.stop()
		self.timer_draw.stop()
		
		

class VentanaConfigIO(QtGui.QWidget):
  
  def __init__(self):
    super(VentanaConfigIO, self).__init__()
    
    grid = QtGui.QGridLayout()
    grid.setSpacing(5)
    
    tit_rate1 = QtGui.QLabel('Rate 1')
    tit_rate2 = QtGui.QLabel('Rate 2')
    tit_len1 = QtGui.QLabel('Length 1')
    tit_len2 = QtGui.QLabel('Length 2')
    tit_sync = QtGui.QLabel('Sync')
    
    tasas = ["10 Mbps","30 Mbps","70 Mbps","125 Mbps"]
    longitudes = ["4", "8", "12", "16"]
    
    combo_rate1 = QtGui.QComboBox(self)
    combo_rate2 = QtGui.QComboBox(self)
    combo_len1 = QtGui.QComboBox(self)
    combo_len2 = QtGui.QComboBox(self)
    combo_sync = QtGui.QComboBox(self)
    
    for t in tasas:
      combo_rate1.addItem(t)
      combo_rate2.addItem(t)
    
    for l in longitudes:
      combo_len1.addItem(l)
      combo_len2.addItem(l)
    
    combo_sync.addItem('sync 1')
    combo_sync.addItem('sync 2')
    combo_sync.addItem('SoF 1')
    combo_sync.addItem('SoF 2')
    
    bot_aceptar = QtGui.QPushButton('Aceptar', self)
    
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
    grid.addWidget(bot_aceptar, 3, 5)
    
    bot_aceptar.clicked.connect(lambda: self.aceptar(combo_rate1.currentText(), combo_rate2.currentText(), combo_len1.currentText(), combo_len2.currentText(), combo_sync.currentText()))
    
    self.setLayout(grid)
    self.setWindowTitle(u'Configuración del generador')
    self.setWindowIcon(QtGui.QIcon('%s/img/icono.gif' % sys.path[0]))
    self.setFixedSize(420, 130)
    self.show()
    
  def aceptar(self, rate1, rate2, len1, len2, sync):
    length = {"4":0, "8":1, "12":2, "16":3}
    rate = {"10 Mbps":0, "30 Mbps":1, "70 Mbps":2, "125 Mbps":3}
    syn = {'sync 1':1, 'sync 2':2, 'SoF 1':3, 'SoF 2':4}
    
    '''
    pines = PinesFPGA()
    pines.setClock(syn[str(sync)])
    pines.setLength1(length[str(len1)])
    pines.setRate1(rate[str(rate1)])
    pines.setLength2(length[str(len2)])
    pines.setRate2(rate[str(rate2)])
    '''
