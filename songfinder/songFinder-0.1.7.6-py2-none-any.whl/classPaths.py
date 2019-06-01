# -*- coding: utf-8 -*-
#cython: language_level=2


import os
import src.messages as tkMessageBox
from Tkinter import *
import traceback
import src.messages as tkFileDialog

import src.globalvar as globalvar
import src.versionning as vers
import src.exception as exception

class Paths:
	def __init__(self, fenetre = None):
		self.fenetre = fenetre
		self.maj()

	def save(self, chemin): # TODO do it better
		if chemin != '':
			try:
				f = open(chemin + 'test.test',"w")
				f.close()
				os.remove(chemin + 'test.test')
			except IOError as os.errno.EACCES:
				tkMessageBox.showerror('Erreur', 'Le chemin "%s" n\'est pas '
										'accesible en écriture, '
										'choisissez un autre répertoire.'\
										%chemin.encode('utf-8'), parent = self.fenetre)
				self.save( tkFileDialog.askdirectory(parent = self.fenetre) )
				return 1
			if os.path.isdir(chemin):
				globalvar.genSettings.set('Paths', 'data', chemin)
				self.root = chemin
				self.maj()
			else:
				tkMessageBox.showerror('Erreur', 'Le chemin "%s" n\'existe pas.'\
										%chemin.encode('utf-8'), parent = self.fenetre)

	def maj(self):
		self.root = globalvar.genSettings.get('Paths', 'data')
		if self.root == '':
			tkMessageBox.showinfo('Répertoire', 'Aucun répertoire pour les chants et '
									'les listes n\'est configuré.\n'
									'Selectionnez ou créez un répertoire '
									'pour la base de donnés.', \
									parent = self.fenetre)
			path = tkFileDialog.askdirectory( initialdir = os.path.expanduser("~"), \
												parent = self.fenetre )
			if path:
				chemin = path
				try:
					os.makedirs(chemin)
				except OSError as os.errno.EEXIST:
					pass
				except IOError as os.errno.EACCES:
					tkMessageBox.showerror('Erreur', 'Le chemin "%s" n\'est '
											'pas accesible en ecriture, '
											'choisissez un autre répertoire.'\
											%chemin.encode('utf-8'), parent = self.fenetre)
					self.save( tkFileDialog.askdirectory(parent = self.fenetre) )
					return 1
				self.save(chemin)
			else:
				raise Exception('No data directory configured, shuting down SongFinder.')

		self.songs = os.path.join(self.root, 'songs', '')
		self.sets = os.path.join(self.root, 'sets', '')
		self.bibles = os.path.join(self.root, 'bibles', '')
		self.pdf = os.path.join(self.root, 'pdf', '')
		self.preach = os.path.join(self.root, 'preach', '')
		self.listPaths = [self.songs, self.sets, self.bibles, self.pdf, self.preach]

		for path in self.listPaths:
			try:
				os.makedirs(path)
			except OSError as os.errno.EEXIST:
				pass

	def sync(self, interface):
		if globalvar.genSettings.get('Parameters', 'sync') == 'oui' and\
			not os.path.isdir(self.root + '.hg') and\
			tkMessageBox.askyesno('Sauvegarde', 'Voulez-vous définir le dépot distant ?\n'
									'Ceci supprimera tout documents présent dans "%s"'\
									%self.root.encode('utf-8'), parent = interface.fen_paramGen):

			fen_clone = Toplevel()
			fen_clone.wm_attributes("-topmost", 1)
			fen_clone.title("Clonage d'un dépôt")
			fen_clone.grab_set()
			fen_clone.focus_set()
			fen_clone.prog = Label(fen_clone, text="", justify='left')
			fen_clone.update()
			try:
				addRepo = vers.AddRepo(fen_clone, self, 'hg', interface)
			except exception.CommandLineError as e:
				tkMessageBox.showerror('Erreur', traceback.format_exc(), \
												parent = self.papa)
		else:
			globalvar.genSettings.set('Parameters', 'sync', 'non')
