#! /usr/bin/env python3
# Python Module to plot the DC/AC Network Response

import os,sys,time
import matplotlib.pyplot as plt


def matplot(units='Hz',ylab=None, plotdata=None):

	if ylab != None :
		matplotdc(ylab,data=plotdata)
	else:
		matplotac(units,data=plotdata)


def matplotdc(ylab,data):
	""" This module formats the commands Matplotlib
	to plot the DC network valuse of a circuit. The only
	parameters required are the Y axis label amd the plot data.
	Plot data contains filename and magnitude data.
	"""
	if ylab == 'Volts':
		xlab = 'Node Number'
	else:
		xlab = 'Mash Number'

	name,mag = data
	plt.title(name)
	plt.ylabel(ylab)
	plt.xlabel(xlab)
	plt.grid(True)
	labs = range(1,len(mag)+1)
	plt.plot(labs, mag, 'r-o')

	# Add timestamp to plot
	ts = time.ctime()
	plt.figtext(0.02,0.015,ts,fontsize=7, ha='left')
	plt.show()
	plt.close('all')

def matplotac(units,data):
	"""
	This module formats the commands required by Matplotlib
	to plot the network analysis response/tansfer fuction
	of an AC network where the output report contains three cols of
	data in the following order: frequency, magnitude (dB),
	and phase angle (degrees). The computed data is passed to this functions.

	This function "matplotac" is called with string such as Hz, Kz, Mz)
	and filename,frequency, magnitude, and phahase angle data.

	call as follows:  plotutil.matplotac(units='Hz', data)
	"""

	name, freq, mag, pa = data
	plt.figure(1)
	plt.subplot(211)
	plt.title(name)
	plt.ylabel('Gain (db)')
	plt.grid(True)
	plt.plot(freq, mag)

	plt.subplot(212)
	plt.ylabel('Phase Angle (Deg.)')
	plt.xlabel('Frequency (' + units[0] + units[1].lower() + ')')
	plt.grid(True)
	plt.plot(freq, pa)
	# Add timestamp to plot
	ts = time.ctime()
	plt.figtext(0.02,0.015,ts,fontsize=7, ha='left')
	plt.show()
	plt.close('all')


