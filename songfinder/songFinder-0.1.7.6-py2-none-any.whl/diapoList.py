# -*- coding: utf-8 -*-
from __future__ import division

import Tkinter as tk
import time

import src.elements.elements as elements
import src.globalvar as globalvar
import src.diapo as classDiapo
import src.exception as exception

class DiapoList(object):
	def __init__(self, elementList=[]):
		self.elementList = elementList
		self.diapo_vide = classDiapo.Diapo(elements.Element(), 0, globalvar.genSettings.get('Syntax', 'newslide')[0], 90)
		self._diapos = []
		self.element2diapo = [0]
		self._lenght = -1
		self._num = None
		self._update = False

	def getList(self, elementNum=0):
		if not self._update:
			previous = 'empty'
			for i, element in enumerate(self.elementList):
				if element.etype != 'image' or previous != 'image':
					self._diapos += [self.diapo_vide]
				self._diapos += element.diapos
				self.element2diapo.append(len(self._diapos))
				previous = element.etype
			self._diapos += [self.diapo_vide]
			self._lenght = len(self._diapos)

		self._num = self.element2diapo[elementNum]
		self._update = True
		return self._diapos

	@property
	def lenght(self):
		if self._lenght == -1:
			self.getList()
		return self._lenght

	def prefetch(self, themes, callback=None, args=[]):
		tmp = time.time()
		self.getList()
		for diapo in reversed(self._diapos):
			diapo.prefetch(themes, text=False)
			if callback:
				callback(*args)
		print('Image prefetching time: %f'%(time.time()-tmp))

	def _getFromNum(self, num):
		if num < self.lenght and num >= 0:
			output = self._diapos[num]
		else:
			output = self.diapo_vide
		return output

	@property
	def current(self):
		return self._getFromNum(self._num)

	@property
	def next(self):
		return self._getFromNum(self._num+1)

	@property
	def nextnext(self):
		return self._getFromNum(self._num+2)

	@property
	def previous(self):
		return self._getFromNum(self._num-1)

	def incremente(self):
		self._num = min(self._num+1, self._lenght-1)

	def decremente(self):
		self._num = max(self._num-1, 0)

	@property
	def number(self):
		return self._num

	@number.setter
	def number(self, num):
		if num >= self.lenght and num < 0:
			raise exception.DiapoError(num)
		self._num = num

	def setElem(self, elementNum):
		num = self.element2diapo[elementNum]
		if num >= self.lenght and value < 0:
			raise exception.DiapoError(num)
		self._num = num

	def selectListBox(self, listBox):
		listBox.select_clear(0, tk.END)
		listBox.select_set(self._num)
		listBox.activate(self._num)

	def writeListBox(self, listBox):
		listBox.delete(0,'end')
		for i, diapo in enumerate(self._diapos):
			listBox.insert(i, diapo.title)
			if diapo.etype == 'empty':
				listBox.itemconfig(i, bg='green')
			elif diapo.etype == 'image':
				listBox.itemconfig(i, bg='red')
