#!/usr/bin/python
#-*-coding: utf-8-*-
#
#  testing.py
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

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter
import numpy as np
from scipy import signal

from src.util import resources
from src.engine import oscilloscope

class ResponseWindow(QtGui.QWidget):
	
	'''
	Some considerations for setting the sample freq and/or basetime(BT)
	
	Rule of thumb: 5.28/f - 2.78E-6 = BT; f is the freq we want to measure
	
	Theory: Fs = 1/(BT*10/2500)
	'''
	
	def __init__(self):
		super(ResponseWindow, self).__init__()
		
		self.figure = plt.figure()
		self.canvas = FigureCanvas(self.figure)
		self.toolbar = NavigationToolbar(self.canvas, self)
		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.toolbar)
		layout.addWidget(self.canvas)
		self.setLayout(layout)
		self.setFixedSize(1600,900)
		self.setWindowTitle('Response')
		self.setWindowIcon(QtGui.QIcon(resources.getPath('icono.gif')))
		
		self.osc = oscilloscope.Oscilloscope.Instance()
		
		# Creation of units that will be displayed
		self.formatter_freq = EngFormatter(unit='Hz', places=1)
		self.formatter_time = EngFormatter(unit='s', places=1)
		
		# Creation of 4 subplots
		self.out_t = plt.subplot2grid((3,2),(0,0))
		self.out_f = plt.subplot2grid((3,2),(0,1))
		self.in_t = plt.subplot2grid((3,2),(1,0))
		self.in_f = plt.subplot2grid((3,2),(1,1))
		self.res_f = plt.subplot2grid((3,2),(2,0), colspan=2)
		
		self.acquire()
		
		self.show()
		
		
	def acquire(self):
		# Channel 1 - Output
		measures1, inc1 = self.osc.get_data('1', 0, 2500, '1')
		time_list1 = []
		
		# Calculating position on x axis knowing the time difference and the position on the display
		[time_list1.append(inc1*i) for i in xrange(len(measures1))]

		n1 = len(measures1)
		k1 = np.arange(n1)
		T1 = n1*inc1
		frq1 = k1/T1
		frq1 = frq1[range(n1/2)]
		fft1 = np.fft.fft(measures1)/n1 #65536)/n1 # FFT normalized
		fft1 = fft1[range(n1/2)]
		
		# Channel 2 - Input
		measures2, inc2 = self.osc.get_data('2', 0, 2500, '1')
		time_list2 = []

		[time_list2.append(inc2*i) for i in xrange(len(measures2))]

		n2 = len(measures2)
		k2 = np.arange(n2)
		T2 = n2*inc2
		frq2 = k2/T2
		frq2 = frq2[range(n2/2)]
		fft2 = np.fft.fft(measures2)/n2 # FFT normalized
		fft2 = fft2[range(n2/2)]
		
		# Response
		
		resp = np.divide(fft1, fft2)
		
		# Plotting
		
		self.out_f.semilogx(frq1, abs(fft1), '#ff0000')
		self.out_t.plot(time_list1, measures1, '#ff0000')

		self.in_f.semilogx(frq2, abs(fft2), '#0101df')
		self.in_t.plot(time_list2, measures2, '#0101df')
		
		self.res_f.loglog(frq2, abs(resp), '#010110')
		
		# Axis decorators
		self.out_f.set_xlabel('Freq')
		self.out_f.set_ylabel('|Y(freq)|')
		self.out_f.xaxis.set_major_formatter(self.formatter_freq)
		self.out_t.xaxis.set_major_formatter(self.formatter_time)
		self.out_t.set_xlabel('t')
		self.out_t.set_ylabel('v')

		self.in_f.set_xlabel('Freq')
		self.in_f.set_ylabel('|Y(freq)|')
		self.in_f.xaxis.set_major_formatter(self.formatter_freq)
		self.in_t.xaxis.set_major_formatter(self.formatter_time)
		self.in_t.set_xlabel('t')
		self.in_t.set_ylabel('v')
		
		self.res_f.set_xlabel('Freq')
		self.res_f.set_ylabel('|Y(freq)|')
		self.res_f.xaxis.set_major_formatter(self.formatter_freq)
		
		self.figure.canvas.draw_idle()

	'''
	def update(self):
		self.ax1_f.semilogx(self.frq1, abs(self.fft1), '#ff0000')
		self.ax1_t.plot(self.time_list1, self.measures1, '#ff0000')

		self.ax2_f.semilogx(self.frq2, abs(self.fft2), '#0101df')
		self.ax2_t.plot(self.time_list2, self.measures2, '#0101df')

		# Axis decorators
		self.ax1_f.set_xlabel('Freq')
		self.ax1_f.set_ylabel('|Y(freq)|')
		self.ax1_f.xaxis.set_major_formatter(self.formatter_freq)
		self.ax1_t.xaxis.set_major_formatter(self.formatter_time)
		self.ax1_t.set_xlabel('t')
		self.ax1_t.set_ylabel('v')

		self.ax2_f.set_xlabel('Freq')
		self.ax2_f.set_ylabel('|Y(freq)|')
		self.ax2_f.xaxis.set_major_formatter(self.formatter_freq)
		self.ax2_t.xaxis.set_major_formatter(self.formatter_time)
		self.ax2_t.set_xlabel('t')
		self.ax2_t.set_ylabel('v')
		
		self.ax1_f.grid(which='both')
		self.ax2_f.grid(which='both')

		# Redraw
		#self.figure.canvas.update()
		#self.figure.canvas.flush_events()
		
		self.figure.canvas.draw_idle()
		
		#self.canvas.draw()

	def closeEvent(self, event):
		self.timer_update.stop()
		self.timer_acquire.stop()
		event.accept()
	'''
