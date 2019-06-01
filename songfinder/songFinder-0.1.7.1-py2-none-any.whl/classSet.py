# -*- coding: utf-8 -*-
#cython: language_level=2

import xml.etree.cElementTree as ET
import datetime
import os
import warnings

import src.elements.elements as elements
import src.fonctions as fonc
import src.classPaths as classPaths
import globalvar as globalvar

class Set(object):
	def __init__(self, inputData, **kwargs):
		self.__paths = classPaths.Paths()
		if isinstance(inputData, list):
			self.__listElem = inputData
			self.__getName()
			# ~ self.__nbElem
		elif isinstance(inputData, basestring):
			if os.path.isfile(inputData):
				self.__fileName = inputData
			else:
				self.__fileName = os.path.join(self.__paths.sets, inputData)
			if fonc.get_ext(self.__fileName) == '':
				self.__fileName = self.__fileName + globalvar.genSettings.get('Extentions', 'liste')[0]
			self.__name = fonc.get_file_name(self.__fileName)
			self.__read()
		else:
			raise Exception('Wrong input for construction of Set object.\n\
								Must a list of elements or the name of a set file but is "%s"'%type(inputData))

	def setName(self, inputPath):
		self.__fileName = inputPath
		self.__name = fonc.get_file_name(inputPath)

	def getName(self):
		return self.__name

	def getElemList(self):
		return self.__listElem

	def __getName(self):
		proch_dimanche = datetime.timedelta(days = 6-datetime.datetime.today().weekday())
		self.__name = str(datetime.date.today()+ proch_dimanche)
		while os.path.isfile(self.__paths.sets + self.__name):
			if len(self.__name) == 10:
				self.__name = self.__name + '_1'
			else:
				self.__name = self.__name[:11] + str(int(self.__name[11:])+1)
		self.__fileName = os.path.join(self.__paths.sets, self.__name)

	def __read(self):
		tmp = None
		self.__listElem = []
		try:
			tree = ET.parse(self.__fileName)
			tree.getroot().find('slide_groups')[:]
		except (IOError, AttributeError):
			warnings.warn('Not able to read %s'%self.__fileName)
			return 1
		liste_xml = tree.getroot()

		for title in liste_xml.find('slide_groups')[:]:
			if title.attrib['type'] == 'song':
				# Different ways of writting the path, test all
				tmp = elements.Chant( os.path.join(self.__paths.songs, title.attrib['path'], title.attrib['name']) )
				if not tmp.exist():
					tmp = elements.Chant( os.path.join(self.__paths.songs, title.attrib['name']) )
					# ~ if not tmp.exist():
						# ~ warnings.warn('"%s" not found while reading "%s".'%(title.attrib['name'], self.__fileName))

			elif title.attrib['type'] == 'media':
				tmp = elements.Element(title.attrib['name'], title.attrib['type'], title.attrib['path'])
			elif title.attrib['type'] == 'image':
				tmp = elements.Element(title.attrib['name'], title.attrib['type'], title.attrib['path'])
			elif title.attrib['type'] == 'verse':
				tmp = elements.Passage( title.attrib['version'], int(title.attrib['livre']), \
												int(title.attrib['chap1']), int(title.attrib['chap2']), \
												int(title.attrib['vers1']), int(title.attrib['vers2']) )

			# ~ if tmp and tmp.exist():
			self.__listElem.append(tmp)

	def save(self):
		new_set = ET.Element("set")
		new_set.set("name", self.__name)
		slide_groups = ET.SubElement(new_set, "slide_groups")
		slide_group = []
		for i, element in enumerate(self.__listElem):
			chemin = fonc.get_path(element.chemin)
			# For compatibility between linux an windows, all path are writtent with slash
			chemin = chemin.replace(os.sep, '/')
			# Write path relative to songs directory
			chemin = chemin.replace('%s/'%self.__paths.songs , '')

			slide_group.append(ET.SubElement(slide_groups, "slide_group"))
			slide_group[i].set("type", element.etype)
			if element.etype == 'song':
				slide_group[i].set("path", chemin)
				slide_group[i].set("name", element.nom)
			elif element.etype == 'verse':
				slide_group[i].set("name", element.nom)
				slide_group[i].set("path", chemin)
				slide_group[i].set("version", element.version)
				slide_group[i].set("livre", str(element.livre))
				slide_group[i].set("chap1", str(element.chap1))
				slide_group[i].set("chap2", str(element.chap2))
				slide_group[i].set("vers1", str(element.vers1))
				slide_group[i].set("vers2", str(element.vers2))
			elif element.etype == 'image':
				slide_group[i].set("name", element.nom)
				slide_group[i].set("path", chemin)

		tree = ET.ElementTree(new_set)
		fonc.indent(new_set)
		tree.write(self.__fileName, encoding="UTF-8")

	def delete(self):
		try:
			os.remove(self.__fileName)
		except IOError:
			pass
