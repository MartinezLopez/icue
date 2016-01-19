#!/usr/bin/python
#-*-coding: utf-8-*-
#
#  eyeDisplay.py
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
from matplotlib.widgets import Cursor

from src.engine import oscilloscope
from src.engine import pin
#from src.engine import modbus
from src.util import resources

class EyeDisplay(QtGui.QWidget):
	
	def __init__(self, ch, rate, length):
		super(EyeDisplay, self).__init__()
		
		self.osc = oscilloscope.Oscilloscope.Instance()
		self.gen = pin.Pins.Instance()
		#self.gen = modbus...
		
		self.timer_osc = QtCore.QTimer()
		self.timer_draw = QtCore.QTimer()
		
		logging.basicConfig(level=logging.DEBUG) 
		self.setWindowTitle('Eye diagramm from ch %s' % (ch,))
		self.setWindowIcon(QtGui.QIcon(resources.getPath('icono.gif')))
		self.setFixedSize(900,700)
		
		# Measurements available for whole class
		self.measure_list = []
		self.inc_t = 0
		self.configure(ch, rate, length)
		self.initUi()
		
		QtCore.QObject.connect(self.timer_draw, QtCore.SIGNAL("timeout()"), self.refresh_data)
		QtCore.QObject.connect(self.timer_osc, QtCore.SIGNAL("timeout()"), lambda chan=ch: self.acquire(chan))
		
		self.timer_osc.start(700)
		self.timer_draw.start(5000)
		
	def initUi(self):
		self.figure = plt.figure(1)
		self.canvas = FigureCanvas(self.figure)
		self.canvas.setParent(self)
		
		self.ax1 = plt.subplot2grid((2,2),(0,0), colspan=2) #Eye diagramm
		self.ax2 = plt.subplot2grid((2,2),(1,0))            #histogram
		self.ax3 = plt.subplot2grid((2,2),(1,1))            #erfc
		plt.subplots_adjust(left=0.15, right=0.85, bottom=0.1, top=0.9, hspace=0.25)
    
		# Creation of units shown on plots
		formatter_time = EngFormatter(unit='s', places=1)
		formatter_amp = EngFormatter(unit='v', places=1)
		
		self.ax1.set_xlabel('time')
		self.ax1.set_ylabel('amplitude')
		self.ax1.xaxis.set_major_formatter(formatter_time)
		self.ax1.yaxis.set_major_formatter(formatter_amp)
		#self.ax1.xaxis.set_minor_locator(MultipleLocator(self.inc_tiempo_t1 * 25))
		self.ax1.yaxis.set_minor_locator(MultipleLocator(0.5))
		
		# Plotting erfc 
		x_axis = np.arange(0, 10, 0.5)
		self.ax3.semilogy(x_axis, 0.5*erfc(x_axis/math.sqrt(2)), color='#08088a')
		
		logging.debug('se crea el eje semilogaritmico')
    		
		self.ax3.set_xlabel('q')
		self.ax3.set_ylabel('BER')
		
		# Creation of horizontal and vertical bars
		self.barSample = self.ax1.axvline(linewidth=3, x=0, color='blue')
		self.barThreshold = self.ax1.axhline(linewidth=3, y=0, color='green')
		self.barThreshold2 = self.ax2.axvline(x=0, color='green')
		self.bar_q = self.ax3.axvline(x=10, color='blue', linestyle='--') # Different from zero to avoiding problems at log calculation
		self.bar_ber = self.ax3.axhline(y=10, color='blue', linestyle='--')
		
		# Creation of font
		font = QtGui.QFont()
		font.setFamily(QtCore.QString.fromUtf8("Helvetica"))
		font.setPixelSize(17)
		
		# Creation of lable to show values of q and BER
		self.results_label = QtGui.QLabel(self)
		self.results_label.setFont(font)
		
		# Matplotlib toolbar
		self.mpl_toolbar = NavigationToolbar(self.canvas, self)
		
		# Stop acquisition button
		but_stop = QtGui.QPushButton(u'Stop acquiring', self)
		but_stop.clicked.connect(self.stopAdq)
		
		hbox = QtGui.QHBoxLayout()
		
		hbox.addStretch(1)
		hbox.addWidget(but_stop)
		
		# Adding to layout
		p1 = QtGui.QVBoxLayout()
		p1.addWidget(self.canvas)
		p1.addWidget(self.mpl_toolbar)
		p1.addWidget(self.results_label)
		p1.addLayout(hbox)
		self.setLayout(p1)
		
		# Interruption on mouse event
		self.cid = self.figure.canvas.mpl_connect('button_press_event', self.on_press)
		
	def refresh_data(self):
		self.ax1.hold(True)
		[self.ax1.plot(self.time_list, self.measure_list[i], '#0b610b') for i in xrange(len(self.measure_list))]
		self.ax1.hold(False)
		self.figure.canvas.draw()
		
	def on_press(self, event):
		QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		QtCore.QCoreApplication.processEvents()
		sampleValue = event.xdata
		#valThreshold = event.ydata # It has some problems with q calculation, but at some point it might be useful
		
		self.amp_range = self.ax1.yaxis.get_data_interval()
		
		if (sampleValue < 0) or (sampleValue > self.time_list[len(self.time_list)-1]):
			sampleValue = self.time_list[(len(self.time_list)-1)/2]
		
		#if (valThreshold < self.amp_range[0]) or (valThreshold > self.amp_range[1]): # Same problem with q as before
		valThreshold = (self.amp_range[0] + self.amp_range[1]) / 2
		
		logging.debug('muestreo %s umbral %s', str(sampleValue), str(valThreshold))    
		self.plot(sampleValue, valThreshold)
    
	def plot(self, sample, threshold):
		# Avoid blocking
		measure_list = self.measure_list
		inc_t = self.inc_t
		
		logging.debug('entramos en dibuja')
		samplingPoint = int(sample/inc_t)
		amp = []
		
		for i in xrange(len(measure_list)): # Saving from -25 to 25 points around sampling point in every trace
			try:
				[amp.append(measure_list[i][samplingPoint + j]) for j in xrange(-25, 25)]
			except IndexError:
				logging.debug('oob')
		
		# discrimination by threshold
		val0 = []
		val1 = []
		
		ap0 = val0.append
		ap1 = val1.append
		
		for i in xrange(len(amp)):
			if(amp[i] < threshold):
				ap0(amp[i])
			else:
				ap1(amp[i])
		
		# Plotting histograms and gaussians
		self.ax2.cla()
		self.ax2.set_xlabel('amplitude')
		norm0, bins, patches = self.ax2.hist(val0, bins=200,range=[(5/4)*self.amp_range[0], (5/4)*self.amp_range[1]], normed=True, histtype='step', color='#8181f7', rwidth=100)
		
		norm1, bins, patches = self.ax2.hist(val1, bins=200,range=[(5/4)*self.amp_range[0], (5/4)*self.amp_range[1]], normed=True, histtype='step', color='#fa5858', rwidth=100)
		
		v0, sigma0 = self.avg_var(val0)
		gauss0 = pylab.normpdf(bins, v0, sigma0)
		self.ax2.plot(bins, gauss0, linewidth=2, color='#0404b4')#blue
		
		v1, sigma1 = self.avg_var(val1)
		gauss1 = pylab.normpdf(bins, v1, sigma1)
		self.ax2.plot(bins, gauss1, linewidth=2, color='#b40404')#red
		
		# BER calc
		q = math.fabs(v1-v0)/(sigma1+sigma0)
		ber = 0.5*erfc(q/math.sqrt(2))
		
		self.show_results(v0, sigma0, v1, sigma1, q, ber, len(val0), len(val1))
		
		# Replacement of bars
		self.ax2.add_line(self.barThreshold2) 
		self.ax3.add_line(self.bar_q)
		self.ax3.add_line(self.bar_ber)
		self.barSample.set_xdata(sample)
		self.barThreshold.set_ydata(threshold)
		self.barThreshold2.set_xdata(threshold)
		logging.debug('colocamos las barras en ax3')
		self.bar_q.set_xdata(q)
		self.bar_ber.set_ydata(ber)
		logging.debug('colocadas')
		
		self.canvas.draw()
		logging.debug('ya se ha redibujado')
		QtCore.QCoreApplication.processEvents()
		QtGui.QApplication.restoreOverrideCursor()
	
	def show_results(self, v0, sigma0, v1, sigma1, q, ber, num0, num1):
		string = u'\tv0: %-*s \u03c3 0: %-*s N. samples 0: %-*s Q: %-*s \n\n\tv1: %-*s \u03c3 1: %-*s N. samples 1: %-*s BER: %.2e' % (17, str(round(v0*1000,1))+' mV', 17, str(round(sigma0*1000,1))+' mV', 17, str(num0), 17, str(round(q,2)), 17, str(round(v1*1000,1))+' mV', 17, str(round(sigma1*1000,1))+' mV', 17, str(num1), ber)
		self.results_label.setText(string)
	
	def avg_var(self, data):
		avg = 0.0
		var = 0.0
		n = len(data)
		for i in xrange(n):
			avg += data[i]
		avg = avg/n
		cuad = math.pow
		for i in xrange(n):
			var += cuad(avg - data[i], 2)
		var = math.sqrt(var / (n-1))
		return avg, var
		
	def configure(self, ch, _rate, _length):
		#Dictionaries
		timebase = {"10 Mbps":'50ns', "30 Mbps":'10ns', "70 Mbps":'5ns', "125 Mbps":'2.5ns'}
		length = {"4":0, "8":1, "12":2, "16":3}
		rate = {"125 Mbps":3, "70 Mbps":2, "30 Mbps":1, "10 Mbps":0}
		
		#Gen config
		self.gen.setClock(ch)
		if ch == '1':
			self.gen.setLength1(length[_length])
			self.gen.setRate1(rate[_rate])
		else:
			self.gen.setLength2(length[_length])
			self.gen.setRate2(rate[_rate])
		
		#Scope config
		self.osc.disp_channel(True, ch)
		self.osc.set_display("YT")
		self.osc.set_persistence_off()
		self.osc.set_horizontal(timebase[_rate])
		self.osc.autoset(ch)
		self.osc.set_trigger('ext5', ch)
		
	def acquire(self, ch):
		measures, inc = self.osc.get_data(ch, 250, 1750, '1') 
		self.measure_list.append(measures)
		self.inc_t = inc
		self.time_list = []
		[self.time_list.append(inc*i) for i in xrange(len(measures))]
	
	def closeEvent(self, evnt):
		self.timer_osc.stop()
		self.timer_draw.stop()
		super(EyeDisplay, self).closeEvent(evnt)
	
	def stopAdq(self):
		self.timer_osc.stop()
		self.timer_draw.stop()
