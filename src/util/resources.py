#!/usr/bin/python
#-*-coding: utf-8-*-
#
#  resources.py
#  
#  Author: Miguel Angel Martinez <miguelang.martinezl@gmail.com>
# 
 
import os

resourceBasePath = ''

def setBasePath(path):
	global resourceBasePath
	resourceBasePath = path
	
def getPath(name):
	path = os.path.normpath(os.path.join(resourceBasePath, name))
	return path
