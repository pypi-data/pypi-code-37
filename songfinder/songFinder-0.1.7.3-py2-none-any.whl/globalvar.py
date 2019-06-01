# -*- coding: utf-8 -*-

import os
import sys
import platform
import re
try: # Windows only imports
	from win32com.client import Dispatch
except ImportError:
	pass

import src.classSettings as settings

def findParam(chaine):
	deb = data.find(chaine)
	fin = data.find("\n", deb)
	if fin != -1:
		param = data[deb + len(chaine): fin]
	else:
		param = data[deb + len(chaine)]
	return param

def getOs():
	if platform.system() == "Linux":
		if platform.dist()[0] == "Ubuntu":
			myOs = "ubuntu"
		else:
			myOs = "linux"
	elif platform.system() == "Windows":
		myOs = "windows"
	else:
		myOs = "notSupported"
		raise NotImplementedError(
			"Your `%s` isn't a supported operatin system`." % platform.system())
	return myOs

myOs = getOs()

issuedCommand = os.path.splitext( os.path.split(sys.executable)[1] )[0]
if issuedCommand in ['python', 'pypy'] \
			or re.search("./*.py", issuedCommand):
	runByPython = True
else:
	runByPython = False

# Define root diretcory
if runByPython:
	chemin_root = os.path.join( '%s\..'%os.path.split(__file__)[0] )
else:
	chemin_root = os.path.join(os.getcwd(), '')

# Define app name and version
try:
	with open( os.path.join(chemin_root, "setVar.bat") ) as fileIn:
		data = fileIn.read()
		version = findParam("VER=")
		appName = findParam("NAME=")
except IOError: # For freezed version
	try:
		version = Dispatch('Scripting.FileSystemObject').GetFileVersion(sys.executable)
		appName = os.path.splitext( os.path.split(sys.executable)[1] )[0]
	except NameError: # For Ubuntu
		version = '0.1.7.3'
		appName = 'songFinder'

# Define settings directory
if os.path.isfile( os.path.join(chemin_root, 'PORTABLE') ):
	portable = True
else:
	portable = False

# Set if installation is portable
try:
	f = open( os.path.join(chemin_root, 'test.test') ,"w")
	f.close()
	os.remove( os.path.join(chemin_root, 'test.test') )
except IOError as os.errno.EACCES:
	portable = False

# Define Settings directory
if portable == False:
	print 'Installed version'
	settingsPath = os.path.join(os.path.expanduser("~"), '.' + appName, '')
else:
	print 'Portable version'
	settingsPath = os.path.join(chemin_root, '.' + appName, '')


if sys.maxsize == 9223372036854775807:
	arch = 'x64'
else:
	arch = 'x86'
dependances = 'deps-%s'%arch
unittest = False

genSettings = settings.GenSettings(settingsPath, chemin_root, portable)
presSettings = settings.PresSettings(settingsPath, chemin_root, portable)
latexSettings = settings.LatexSettings(settingsPath, chemin_root, portable)
genSettings.create()
genSettings.read()
presSettings.create()
presSettings.read()
latexSettings.create()
latexSettings.read()
