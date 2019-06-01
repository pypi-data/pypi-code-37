# -*- coding: utf-8 -*-
from __future__ import division

from Tkinter import *
import tkFont
import ttk
import src.messages as tkMessageBox
import src.messages as tkFileDialog
import os
import threading
import sys
import copy
import traceback
import gc
import time

import globalvar as globalvar
import src.versionning as version
import src.latex as latex
import src.elements.elements as elements
import src.presentation as pres
import src.versets as classverset
import src.preferences as pref
import src.fonctions as fonc
import src.commandLine as commandLine
import src.classSet as classSet
import src.classPaths as classPaths
import src.exception as exception
import src.guiHelper as guiHelper
import src.gestchant as gestchant
import src.search as search
import src.dataBase as dataBase
import src.background as background
import src.inputFrame as inputFrame
import src.themes as themes
import src.screen as screen
import src.diapo as classDiapo
import src.diapoList as diapoList
import src.simpleProgress as simpleProgress

#~ try:
	#~ import vlc_player
	#~ vlc = 1
#~ except:
	#~ warnings.warn('VLC not found')
	#~ vlc = 0
vlc = 0


class Interface(object, Frame):
	def __init__(self, fenetre, myScreen, fileIn=None, **kwargs):
		Frame.__init__(self, fenetre, **kwargs)
		self._screen = myScreen
		if self._screen.w < 1000:
			self.fontSize = 8
		else:
			self.fontSize = 9
		for font in ["TkDefaultFont", "TkTextFont", "TkFixedFont", "TkMenuFont"]:
			default_font = tkFont.nametofont(font)
			default_font.configure(size=self.fontSize)

		self.dataBase = dataBase.DataBase()
		self.searcher = search.Searcher(self.dataBase)

		self.paths = classPaths.Paths(fenetre)
		try:
			self.repo = version.Repo(self.paths.root, 'hg', True, self, screen=self._screen)
		except exception.CommandLineError as e:
			tkMessageBox.showerror(u'Erreur', traceback.format_exc(), parent = self.papa)

		self.mainmenu = Menu(self)  ## Barre de menu
		self.menuFichier = Menu(self.mainmenu)  ## Menu fils menuExample
		self.menuFichier.add_command(label="Mettre à jour la base de données", \
						command = self.updateData )
		self.menuFichier.add_command(label="Quitter", \
						command=self.quitter)
		self.mainmenu.add_cascade(label = "Fichier", \
						menu = self.menuFichier)

		self.menuEditer = Menu(self.mainmenu)
		self.menuEditer.add_command(label="Paramètres généraux", \
						command = self.paramGen )
		self.menuEditer.add_command(label="Paramètres de présentation", \
						command = self.paramPres )
		self.mainmenu.add_cascade(label = "Editer", menu = self.menuEditer)

		self.menuSync = Menu(self.mainmenu)
		self.menuSync.add_command(label="Envoyer les chants", \
						command = self.sendSongs )
		self.menuSync.add_command(label="Recevoir les chants",\
						command = self.recieveSongs )
		self.mainmenu.add_cascade(label = "Réception/Envoi", \
						menu = self.menuSync)

		self.menuLatex = Menu(self.mainmenu)
		self.menuLatex.add_command(label="Générer les fichiers Latex",\
						command = lambda noCompile=1: self.writeLatex(noCompile) )
		self.menuLatex.add_command(label="Compiler les fichiers Latex",\
						command = self.compileLatex )
		self.mainmenu.add_cascade(label = "Latex", menu = self.menuLatex)

		self.menuHelp = Menu(self.mainmenu)
		self.menuHelp.add_command(label="README",command = self.showREADME )
		self.menuHelp.add_command(label = "Documentation", command = self.showDoc)
		self.mainmenu.add_cascade(label = "Aide", menu = self.menuHelp)

		fenetre.config(menu=self.mainmenu)

		self.FILETYPES = [ ("All files", "*.*"), ]
		self.filename = StringVar(self)
		self.chant_affiche = None
		self.nouveau_title = ''
		self.nouveau_chant = None
		self.fen_pres = None
		self.presentation = None
		self.fenetre_versets = None
		self.fenetre_crea = None
		self.fen_paramGen = None
		self.fen_paramPres = None
		self.fenetre_set = None
		self.fen_latex = None

		self.widgetScroll = None

		self.FILETYPES_video = [(ext[1:].upper(), ext) for ext in \
					globalvar.genSettings.get('Extentions', 'video')] + [("All files", "*.*")]
		self.FILETYPES_audio = [(ext[1:].upper(), ext) for ext in \
					globalvar.genSettings.get('Extentions', 'audio')] + [("All files", "*.*")]
		self.FILETYPES_image = [(ext[1:].upper(), ext) for ext in \
					globalvar.genSettings.get('Extentions', 'image')] + [("All files", "*.*")]
		self.FILETYPES_present = [(ext[1:].upper(), ext) for ext in \
					globalvar.genSettings.get('Extentions', 'presentation')] + [("All files", "*.*")]
		self.FILETYPES_media = [("MP4", ".mp4"), ("All files", "*.*")] + \
					self.FILETYPES_video[:-1] + self.FILETYPES_audio[:-1]

		self.chants_trouve = []
		self.chants_selection = []
		self.chants_selection_previous = []
		self.current_selection = -1
		self.setName = ''

		leftPanel = ttk.Frame(fenetre)
		searchPanel = ttk.Frame(leftPanel)
		listPanel = ttk.Frame(leftPanel)
		editPanel = ttk.Frame(fenetre)
		rightPanel = ttk.Frame(fenetre)
		previewPanel = ttk.Frame(rightPanel)
		presentPanel = ttk.Frame(rightPanel)

		searchPanel.pack(side=TOP, fill=X)
		listPanel.pack(side=TOP, fill=BOTH, expand=1)

		leftPanel.pack(side=LEFT, fill=BOTH, expand=1)
		editPanel.pack(side=LEFT, fill=BOTH, expand=1)
		rightPanel.pack(side=LEFT, fill=X)
		previewPanel.pack(side=TOP)
		presentPanel.pack(side=TOP, fill=X)

		####### Search panel
		self.chant_entre = inputFrame.entryField(searchPanel, width=50, text="Recherche: ")
		self.message_trouve = Label(searchPanel, text="Chants trouvés: \n"
								"Utilisez leur numéro dans la liste pour les selectionner")
		self.var_selection = StringVar()
		self.liste_chants = Listbox(searchPanel, width=50, height=9, \
									listvariable = self.var_selection)

		self.chant_entre.pack(side=TOP, fill=X, expand=1)

		self.message_trouve.pack(side=TOP, fill=X)
		self.liste_chants.pack(side=TOP, fill=X, expand=1)
		#######

		####### List panel
		lisButtonSubPanel = ttk.Frame(listPanel)
		listSubPanel = ttk.Frame(listPanel)

		lisButtonSubPanel.pack(side=TOP, fill=X)
		listSubPanel.pack(side=TOP, fill=BOTH, expand=1)

		self.bouton_sauv_set = Button(lisButtonSubPanel, \
								text='Sauver', \
								command=self.save_set, \
								state=DISABLED)
		self.bouton_suppr_set = Button(lisButtonSubPanel, \
								text='Suppr', \
								command=self.supprimer_set, \
								state=DISABLED)

		self.bouton_up_song = Button(lisButtonSubPanel, \
								text='Monter', \
								command=self.monter, state=DISABLED)
		self.bouton_down_song = Button(lisButtonSubPanel, \
								text='Descendre', \
								command=self.descendre, state=DISABLED)
		self.bouton_suppr_song = Button(lisButtonSubPanel, \
								text='Suppr', \
								command=self.supprimer, state=DISABLED)
		self.bouton_clear = Button(lisButtonSubPanel, \
								text='Initialiser', \
								command=self.clear, state=DISABLED)

		self.affiche_title_set = Label(lisButtonSubPanel, text="Liste: ")

		self.liste_set = []
		self.set_selection	= StringVar()
		self.combobox_set	= ttk.Combobox(lisButtonSubPanel, \
								textvariable = self.set_selection, \
								values = self.liste_set, \
								state = 'readonly', width=20)

		self.add_media_button = Button(lisButtonSubPanel, \
								text='Ajouter\nMedias', \
								command=self.add_media)
		if vlc == 0:
			self.add_media_button.config(state=DISABLED)
		self.add_image_button = Button(lisButtonSubPanel, \
								text='Ajouter\nImages', \
								command=self.add_image)
		self.add_vers_button = Button(lisButtonSubPanel,\
								text='Ajouter\nVersets', \
								command=self.add_vers)

		self.liste_selection = Listbox(listSubPanel, width=50)
		self.scroll_liste_select = Scrollbar(listSubPanel, command=self.liste_selection.yview)
		self.liste_selection['yscrollcommand'] = self.scroll_liste_select.set

		self.affiche_title_set.grid(row=0, column=0, columnspan=2, rowspan=1)
		self.combobox_set.grid(row=0, column=2, columnspan=6)
		self.bouton_sauv_set.grid(row=0, column=8, columnspan=2)
		self.bouton_suppr_set.grid(row=0, column=10, columnspan=2)

		self.add_media_button.grid(row=1, column=6, columnspan=2, rowspan=2)
		self.add_image_button.grid(row=1, column=8, columnspan=2, rowspan=2)
		self.add_vers_button.grid(row=1, column=10, columnspan=2, rowspan=2)

		self.bouton_up_song.grid(row=1, column=0, columnspan=3)
		self.bouton_down_song.grid(row=2, column=0, columnspan=3)
		self.bouton_suppr_song.grid(row=1, column=3, columnspan=3)
		self.bouton_clear.grid(row=2, column=3, columnspan=3)

		self.liste_selection.pack(side=LEFT, fill=BOTH, expand=1)
		self.scroll_liste_select.pack(side=LEFT, fill=Y)

		#######


		####### Present panel
		self.bouton_present = Button(presentPanel, \
							text='Présentation de la liste',  \
							command=self.present)
		self.bouton_present_select = Button(presentPanel, \
							text='Présentation du chant selectionné', \
							command=lambda mode='chant', \
							event=0: self.present(mode, event))
		self.bouton_createPDF = Button(presentPanel, \
							text='Générer un PDF', \
							command=self.quickPDF)

		self.messageRatio = Label(presentPanel, text='Format de l\'écran :')
		ratioList = globalvar.genSettings.get('Parameters', 'ratio_avail')
		self.ratioSelection	= StringVar()
		self.ratioSelect	= ttk.Combobox(presentPanel, \
								textvariable = self.ratioSelection, \
								values = ratioList, \
								state = 'readonly', width=20)
		ratio = self.ratioSelect.set(globalvar.genSettings.get('Parameters', 'ratio'))

		self.bouton_present.pack(side=TOP, fill=X)
		self.bouton_present_select.pack(side=TOP, fill=X)
		self.bouton_createPDF.pack(side=TOP, fill=X)
		self.messageRatio.pack(side=TOP)
		self.ratioSelect.pack(side=TOP)

		#######


		# Edit Panel
		buttonSubPanel = ttk.Frame(editPanel)
		titleSubPanel = ttk.Frame(editPanel)
		chordsSubPanel = ttk.Frame(editPanel)
		supinfoSubPanel = ttk.Frame(editPanel)
		textSubPanel = ttk.Frame(editPanel)

		buttonSubPanel.pack(side=TOP)
		titleSubPanel.pack(side=TOP, fill=X)
		chordsSubPanel.pack(side=TOP, fill=X)
		supinfoSubPanel.pack(side=TOP, fill=X)
		textSubPanel.pack(side=TOP, fill=BOTH, expand=1)

		self.title_chant = inputFrame.TextField(titleSubPanel, width=30, \
								text="Titre :", packing=LEFT, state=DISABLED)

		self.key_chant = inputFrame.TextField(chordsSubPanel, width=5, \
								text='Tonalité: ', packing=LEFT, state=DISABLED)
		self.transpose_chant = inputFrame.TextField(chordsSubPanel, width=3, \
								text='Transposition: ', packing=LEFT, state=DISABLED)
		self.capo_chant = inputFrame.TextField(chordsSubPanel, width=3, \
								text='Capo: ', packing=LEFT, state=DISABLED)
		self.numCCLIPrint = inputFrame.TextField(supinfoSubPanel, width=3, \
								text='Num (CCLI): ', packing=LEFT, state=DISABLED)
		self.numTurfPrint = inputFrame.TextField(supinfoSubPanel, width=3, \
								text='Num (Turf): ', packing=LEFT, state=DISABLED)
		self.numCustomPrint = inputFrame.TextField(supinfoSubPanel, width=3, \
								text='Num (Custom): ', packing=LEFT, state=DISABLED)

		self.bouton_save_song = Button(buttonSubPanel, text='Sauver', \
							command=self.save_song, state=DISABLED)
		self.bouton_creation = Button(buttonSubPanel, text='Créer un nouveau chant', \
							command=self.fenetre_creation_chant)
		self.bouton_version = Button(buttonSubPanel, text='Créer une autre version du chant', \
							command=lambda: self.fenetre_creation_chant(self.chant_affiche))

		self.message_affiche_chant = Text(textSubPanel, width=48, height=32, \
										undo=True, state=DISABLED)
		self.scroll_text = Scrollbar(textSubPanel, command=self.message_affiche_chant.yview)
		self.message_affiche_chant['yscrollcommand'] = self.scroll_text.set

		self.title_chant.pack(side=TOP, fill=X, expand=1)

		self.key_chant.pack(side=LEFT, fill=X, expand=1)
		self.transpose_chant.pack(side=LEFT, fill=X, expand=1)
		self.capo_chant.pack(side=LEFT, fill=X, expand=1)

		self.numCCLIPrint.pack(side=LEFT, fill=X, expand=1)
		self.numTurfPrint.pack(side=LEFT, fill=X, expand=1)
		self.numCustomPrint.pack(side=LEFT, fill=X, expand=1)

		self.bouton_save_song.pack(side=LEFT)
		self.bouton_creation.pack(side=LEFT)
		self.bouton_version.pack(side=LEFT)

		# ~ self.message_diapo.grid(row=8, column=22, rowspan=1)
		# ~ self.message_ligne.grid(row=9, column=22, rowspan=1)

		self.message_affiche_chant.pack(side=LEFT, fill=BOTH, expand=1)
		self.scroll_text.pack(side=LEFT, fill=Y)
		#######

		#######
		# Preview panel
		self.previewSize = 300
		ratio = screen.getRatio(globalvar.genSettings.get('Parameters', 'ratio'))
		self._themePres = themes.Theme(previewPanel, \
						width=self.previewSize, height=self.previewSize/ratio)
		self._themePres.pack(side=TOP, fill=BOTH, expand=1)
		diapo_vide = classDiapo.Diapo(elements.Element(), 0, \
						globalvar.genSettings.get('Syntax', 'newslide')[0], 20)
		diapo_vide.printDiapo(self._themePres)

		#######


		self.inputFildsList = [self.title_chant, \
							self.transpose_chant, self.capo_chant, self.key_chant, \
							self.numCCLIPrint, self.numTurfPrint, self.numCustomPrint]
		#######
		self.bind_class("Text","<Control-a>", self.selectall)

		self.bind_all("<F5>", lambda event=0, mode='liste' : self.present(event, mode))
		self.bind_all("<F6>", lambda event=0, mode='chant' : self.present(event, mode))
		self.liste_chants.bind("<ButtonRelease-1>", self.printer)
		self.liste_chants.bind("<KeyRelease-Up>", self.printer)
		self.liste_chants.bind("<KeyRelease-Down>", self.printer)
		self.liste_selection.bind("<ButtonRelease-1>", self.printer)
		self.liste_selection.bind("<KeyRelease-Up>", self.printer)
		self.liste_selection.bind("<KeyRelease-Down>", self.printer)
		self.chant_entre.bind("<KeyRelease>", self.chercher)
		self.liste_chants.bind("<Double-Button-1>", lambda event, clique=1: \
												self.selection(event, clique))
		self.combobox_set.bind("<<ComboboxSelected>>", self.affiche_set)
		self.ratioSelect.bind("<<ComboboxSelected>>", self.format)

		self.chant_entre.bind("<KeyRelease-BackSpace>", self.rien)
		self.chant_entre.bind("<KeyRelease-Left>", self.rien)
		self.chant_entre.bind("<KeyRelease-Right>", self.rien)
		self.chant_entre.bind("<KeyRelease-Up>", self.rien)
		self.chant_entre.bind("<KeyRelease-Down>", self.rien)
		# Edition de la liste de selection
		self.liste_selection.bind("<u>", self.monter)
		self.liste_selection.bind("<d>", self.descendre)
		self.liste_selection.bind("<Delete>", self.supprimer)
		self.liste_chants.bind("<Delete>", self.supprimer_paroles)
		self.bind_all("<Control-s>", self.save_song)
		self.message_affiche_chant.bind("<KeyRelease>", self.unsave_song)
		for field in self.inputFildsList:
			field.bind("<KeyRelease>", self.unsave_song)

		self.bind_all('<Enter>', self._bound_to_mousewheel)
		self.bind_all('<Leave>', self._unbound_to_mousewheel)

		self.focus_set()

		self.get_liste_set()
		if globalvar.genSettings.get('Parameters', 'autoload') == 'oui':
			if len(self.liste_set) > 0:
				self.combobox_set.set(self.liste_set[0])

		self.timer = threading.Timer(1, self.rien)
		self.chant_entre.focus_set()
		self.active_boutons()
		self.unsave_set()
		self.paths.sync(self)

		#~ backColor = '#F0F0F0'
		#~ self.configure(background=backColor)
		#~ for item in all_children(self):
			#~ if item.winfo_class() == 'Label' or item.winfo_class() == 'Radiobutton':
				#~ item['bg'] = backColor
			#~ elif item.winfo_class() == 'Text' or item.winfo_class() == 'Entry':
				#~ item['bg'] = 'white'
			#~ elif item.winfo_class() == 'Button' or item.winfo_class() == 'Menu':
				#~ item['bg'] = '#FFFBF5'

		# Open file in argument
		if fileIn:
			fileIn = os.path.abspath(fileIn)
			ext = fonc.get_ext(fileIn)
			if ext in globalvar.genSettings.get('Extentions', 'chant'):
				element = elements.Chant(fileIn)
				if element.exist():
					self.chants_trouve.append(element)
					self.affiche_resultats()
					self.printer()
			elif ext in globalvar.genSettings.get('Extentions', 'liste'):
				self.combobox_set.set(fileIn)

		self.affiche_set()
		fenetre.attributes("-alpha", 1)
		fenetre.lift()

	def _bound_to_mousewheel(self, event):
		self.widgetScroll = event.widget
		self.bind_all("<MouseWheel>", self._on_mousewheel)

	def _unbound_to_mousewheel(self, event):
		self.widgetScroll = None
		self.unbind_all("<MouseWheel>")

	def _on_mousewheel(self, event):
		try:
			self.widgetScroll.focus_set()
			self.widgetScroll.yview_scroll(-1*(event.delta//8), "units")
		except AttributeError:
			pass

	def updateData(self):
		progressBar = simpleProgress.SimpleProgress(self, \
									"Mise à jour de la base de données", \
									screen=self._screen)
		progressBar.start(self.dataBase.lenght)
		self.dataBase.update(progressBar.update)
		self.searcher.resetCache()
		self.get_liste_set()
		for chant in self.chants_trouve + self.chants_selection + [self.chant_affiche]:
			try:
				chant.resetText()
			except AttributeError:
				pass
		self.affiche_resultats()
		self.affiche_set()
		self.printer()
		progressBar.stop()
		tkMessageBox.showinfo('Confirmation', 'La base de donnée a '
								'été mise à jour: %d chants.'%self.dataBase.lenght)

	def format(self, event=0):
		ratio = self.ratioSelect.get()
		globalvar.genSettings.set('Parameters', "ratio", ratio)

		ratioNum = screen.getRatio(ratio)
		self._themePres.resize(self.previewSize, self.previewSize/ratioNum)
		if self.chant_affiche:
			self.chant_affiche.diapos[0].printDiapo(self._themePres)
		# ~ self.printer()

	def selectall(self, event):
		event.widget.tag_add("sel","1.0","end")

	def add_media(self):
		medias = tkFileDialog.askopenfilenames(filetypes=self.FILETYPES_media)
		if medias:
			for media in medias:
				fichier = fonc.get_file_name(media)
				extention = fonc.get_ext(media)
				reponse = 1
				typeMedia = globalvar.genSettings.get('Extentions', 'audio') \
							+ globalvar.genSettings.get('Extentions', 'video')
				if media and (extention not in typeMedia):
					reponse = tkMessageBox.askyesno('Type de fichier', \
					'Le fichier "%s.%s" ne semble pas être un fichier audio ou vidéo. '
					'Voulez-vous continuer malgré tout ?'%(fichier.encode('utf-8'), \
														extention.encode('utf-8')))
				if media and reponse:
					self.current_selection = int(self.current_selection) + 1
					self.chants_selection.insert(self.current_selection, \
												elements.Element(fichier, 'media', media))
					self.affiche_selection()
		self.chant_entre.focus_set()

	def add_image(self):
		images = tkFileDialog.askopenfilenames(filetypes=self.FILETYPES_image)
		if images:
			for full_path in images:
				fichier = fonc.get_file_name_ext(full_path)
				extention = fonc.get_ext(full_path)
				reponse = 1
				typeImage = globalvar.genSettings.get('Extentions', 'image')
				if full_path and (extention not in typeImage):
					reponse = tkMessageBox.askyesno('Type de fichier', \
					'Le fichier "%s.%s" ne semble pas être un fichier image. '
					'Voulez-vous continuer malgré tout ?'%(fichier.encode('utf-8'),\
														extention.encode('utf-8')))
				if full_path and reponse:
					self.current_selection = int(self.current_selection) + 1
					self.chants_selection.insert(self.current_selection, \
												elements.ImageObj(full_path))
					self.affiche_selection()
		self.chant_entre.focus_set()

	def add_vers(self):
		self.closeVerseWindow()
		self.fenetre_versets = Toplevel(self)
		self.fenetre_versets.wm_attributes("-topmost", 1)
		self.interface_versets = classverset.class_versets(self.fenetre_versets, self)
		self.fenetre_versets.title("Bible")
		self.fenetre_versets.update_idletasks()
		self.fenetre_versets.protocol("WM_DELETE_WINDOW", self.closeVerseWindow)
		w = self.fenetre_versets.winfo_width()
		h = self.fenetre_versets.winfo_height()
		self.fenetre_versets.resizable(False,False)
		self.fenetre_versets.update()

	def select_vers(self):
		try:
			passage = elements.Passage(self.interface_versets.version, \
												self.interface_versets.livre, \
												self.interface_versets.chap1, \
												self.interface_versets.chap2, \
												self.interface_versets.vers1, \
												self.interface_versets.vers2)
		except exception.DataReadError as e:
			tkMessageBox.showerror(u'Attention', traceback.format_exc())
			return 1
		else:
			self.interface_versets.select_state()
			self.current_selection = int(self.current_selection) + 1
			self.chants_selection.insert(self.current_selection, passage)
			self.affiche_selection()
			self.printer()

	def closeVerseWindow(self):
		if self.fenetre_versets:
			self.interface_versets.quitter()
			self.interface_versets = None
			self.fenetre_versets = None
			print('GC collected objects : %d' % gc.collect())

	def get_liste_set(self):
		self.liste_set = []
		for root, dirs, files in os.walk(self.paths.sets):
			for i,fichier in enumerate(sorted(files, reverse=True)):
				self.liste_set.append(fonc.get_file_name(fichier))
		self.combobox_set['values'] = self.liste_set

	def affiche_set(self, event=0):
		newSetName = self.combobox_set.get()
		if newSetName:
			if self.bouton_sauv_set['state'] != DISABLED:
				if tkMessageBox.askyesno('Sauvegarde', \
						'Voulez-vous sauvegarder les modifications '
						'sur la liste "%s" ?'%self.setName):
					self.combobox_set.set(self.setName)
					self.save_set()
			self.setName = newSetName
			try:
				curSet = classSet.Set(self.setName)
			except exception.DataReadError as e:
				tkMessageBox.showerror(u'Attention', traceback.format_exc())
				return 1
			self.chants_selection = curSet.getElemList()
			self.affiche_selection()
			self.printer()
			self.chants_selection_previous = copy.copy(self.chants_selection)

		self.unsave_set()
		self.active_suppr_set()

	def chercher(self, event):
		#~ self.timer.cancel()
		#~ self.timer = threading.Timer(0.1, self.chercher_core, [event])
		#~ self.timer.start()
		self.chercher_core(event)


	def chercher_core(self, event):
		tmps4=time.time()
		if self.chant_entre.get():
			chantIn = fonc.safeUnicode(self.chant_entre.get())
			self.chants_trouve = self.searcher.search(chantIn)
			self.affiche_resultats()
		self.selection(event)
		self.liste_selection.selection_clear(0, END)
		self.printer(event)


	def affiche_resultats(self):
		self.liste_chants.delete(0,'end')
		for i,chant in enumerate(self.chants_trouve):
			self.liste_chants.insert(i, '%s -- %s'%(str(i+1), str(chant)))

	def selection(self, event, clique=0):

		chiffres = [str(i) for i in range(1,10)]
		# For ubuntu num lock wierd behaviour
		toucheNumPad = event.keycode
		if globalvar.myOs == "ubuntu":
			listNumPad = [87, 88, 89, 83, 84, 85, 79, 80, 81]
		else:
			listNumPad = []
		if not self.chant_entre.get().isdigit():
			if toucheNumPad in listNumPad:
				touche = str(listNumPad.index(toucheNumPad) + 1)
			else:
				touche = event.keysym
		else:
			touche = None
		if clique == 1 and self.liste_chants.curselection():
			touche = str(int(self.liste_chants.curselection()[0])+1)
		if touche in chiffres:
			if int(touche) < self.liste_chants.size()+ 1:
				self.current_selection = int(self.current_selection) + 1
				element = self.chants_trouve[int(touche)-1]
				self.chants_selection.insert(self.current_selection, element)
				self.affiche_selection()
			self.chant_entre.delete(0, END)
			self.chant_entre.focus_set()

	def affiche_selection(self):
		if self.setName != '':
			self.combobox_set.set(self.setName)
		nb_chants = len(self.chants_selection)
		self.liste_selection.delete(0,'end')
		for i,element in enumerate(self.chants_selection):
			self.liste_selection.insert(i, str(i+1) + ' -- ' + str(element))
			if not element.exist() and self.liste_selection.itemcget(i, 'fg') != 'green':
				self.liste_selection.itemconfig(i, fg='green')

		if len(self.chants_selection) is not 0:
			self.liste_selection.yview('moveto', self.current_selection/len(self.chants_selection))
		self.liste_selection.activate(self.current_selection)
		self.unsave_set()

	def printer(self, event=0):
		element = elements.Element()
		if self.liste_selection.curselection():
			self.current_selection = int(self.liste_selection.curselection()[0])
			element = self.chants_selection[self.current_selection]
		elif self.liste_chants.curselection() and self.chants_trouve:
			select = self.liste_chants.curselection()[0]
			element = self.chants_trouve[select]
		elif self.liste_chants.size() > 0 and self.chants_trouve: # ValueError None
			element = self.chants_trouve[0]
		elif self.liste_selection.size() > 0 and self.chants_selection:
			element = self.chants_selection[0]

		if self.chants_selection and not element.exist() and self.current_selection != -1:
			element = self.cherche_alternate(element)
			if element.exist():
				self.chants_selection[self.current_selection] = element
			else:
				self.current_selection = -1
			self.affiche_selection()
		if element.exist():
			self.printOn()

			if self.message_affiche_chant.edit_modified() and element.title:
				if tkMessageBox.askyesno('Sauvegarde', \
							'Voulez-vous sauvegarder les modifications '
							'sur le chant:\n"%s" ?'%self.chant_affiche.title):
					self.save_song()
			self.chant_affiche = element
			guiHelper.change_text(self.message_affiche_chant, element.text)
			guiHelper.change_text(self.title_chant, element.title)
			guiHelper.change_text(self.transpose_chant, element.transpose or '')
			guiHelper.change_text(self.capo_chant, element.capo or '')
			guiHelper.change_text(self.key_chant, element.key)
			guiHelper.change_text(self.numCCLIPrint, element.nums.get('hymn') or '')
			guiHelper.change_text(self.numTurfPrint, element.nums.get('turf') or '')
			guiHelper.change_text(self.numCustomPrint, element.nums.get('custom') or '')
			self.coloration()
		else:
			self.printOff()

		self.message_affiche_chant.edit_modified(False)
		self.title_chant.edit_modified(False)
		self.bouton_save_song.config(state=DISABLED)
		self.message_affiche_chant.edit_reset()
		self.active_boutons()
		if self.chant_affiche:
			self.chant_affiche.diapos[0].printDiapo(self._themePres)

	def printOff(self):
		guiHelper.change_text(self.message_affiche_chant, '')
		self.message_affiche_chant["state"] = DISABLED
		for field in self.inputFildsList:
			guiHelper.change_text(field, '')
			field.state = DISABLED

	def printOn(self):
		self.message_affiche_chant["state"] = NORMAL
		for field in self.inputFildsList:
			field.state = NORMAL

	def cherche_alternate(self, element):
		nameClean = fonc.safeUnicode(element.nom)
		chants_trouve = self.searcher.search(nameClean)
		if chants_trouve:
			proposition = chants_trouve[0]
			if len(chants_trouve) == 1 and proposition.nom == element.nom:
				return proposition
			else:
				for proposition in chants_trouve[:5]:
					if tkMessageBox.askyesno('Remplacement', \
							'L\'élément "%s" est introuvable. '
							'Voulez le remplacer par "%s" ?'\
							%(element.nom, proposition.nom)):
						return proposition
		else:
			tkMessageBox.showerror('Attention', \
						'L\'élément "%s" est introuvable, '
						'il va être supprimé.'%element.nom)
			self.supprimer()
		return element

	def supprimer_set(self):
		if self.combobox_set.get():
			selected_set = self.combobox_set.get()
			if tkMessageBox.askyesno('Confirmation', \
							'Etes-vous sur de supprimer '
							'la liste:\n"%s" ?'%selected_set):
				path = self.paths.sets + selected_set \
						+ globalvar.genSettings.get('Extentions', 'liste')[0]
				if os.path.isfile(path):
					os.remove(path)
			if selected_set in self.liste_set:
				indice = self.liste_set.index(selected_set)
			self.get_liste_set()
			if len(self.liste_set) >= indice:
				self.combobox_set.set(self.liste_set[indice])
				self.affiche_set()
			self.active_suppr_set()


	def supprimer_paroles(self, event):
		# todo a refaire supression du chant dans la liste chant_trouve
		if tkMessageBox.askyesno('Confirmation', \
					'Etes-vous sur de supprimer '
					'le chant:\n"%s" ?'%self.chant_affiche.nom):
			path = self.chant_affiche.chemin
			if os.path.isfile(path):
				os.remove(path)
			self.dataBase.remove(self.chant_affiche)
			self.searcher.resetCache()
			if self.chant_affiche in self.chants_trouve:
				self.chants_trouve.remove(self.chant_affiche)
			self.affiche_resultats()
			self.printer()

	def supprimer(self, event=0):
		select = self.liste_selection.curselection()
		if select:
			index = int(select[0])
			del self.chants_selection[index]
			self.affiche_selection()
			lenght = self.liste_selection.size()
			if index < lenght:
				self.liste_selection.activate(index)
				self.liste_selection.selection_set(index)
			elif lenght > 0:
				self.liste_selection.activate(lenght-1)
				self.liste_selection.selection_set(lenght-1)
		self.active_boutons()

	def monter(self, event=0):
		index = int(self.liste_selection.curselection()[0])
		if index > 0:
			self.chants_selection[index-1], self.chants_selection[index] \
					= self.chants_selection[index], self.chants_selection[index-1]
			self.affiche_selection()
			self.liste_selection.activate(index-1)
			self.liste_selection.selection_set(index-1)
			self.current_selection = index-1

	def descendre (self, event=0):
		index = int(self.liste_selection.curselection()[0])
		if index < len(self.chants_selection)-1:
			self.chants_selection[index+1], self.chants_selection[index] \
				= self.chants_selection[index], self.chants_selection[index+1]
			self.affiche_selection()
			self.liste_selection.activate(index+1)
			self.liste_selection.selection_set(index+1)
			self.current_selection = index+1

	def coloration(self):
		guiHelper.coloration(self.message_affiche_chant, "black")
		guiHelper.coloration(self.message_affiche_chant, "blue", \
							globalvar.genSettings.get('Syntax', 'newline'))
		guiHelper.coloration(self.message_affiche_chant, "red", '\\ac')
		guiHelper.coloration(self.message_affiche_chant, "red", '[', ']')
		guiHelper.coloration(self.message_affiche_chant, "red", '\\...')
		guiHelper.coloration(self.message_affiche_chant, "red", "(bis)")
		guiHelper.coloration(self.message_affiche_chant, "red", "(ter)")
		for newslideSyntax in globalvar.genSettings.get('Syntax', 'newslide'):
			guiHelper.coloration(self.message_affiche_chant, "blue", newslideSyntax) # TclError None

	def quitter(self):
		try:
			globalvar.genSettings.write()
			globalvar.presSettings.write()
			globalvar.latexSettings.write()
		except Exception as e:
			tkMessageBox.showerror('Attention', \
					'Error while writting settings:\n%s'%traceback.format_exc())
		try:
			background.cleanDiskCacheImage()
		except Exception as e:
			tkMessageBox.showerror('Attention', \
					'Error in clean cache:\n%s'%traceback.format_exc())
		self.destroy()
		sys.exit()

	def rien(self,event=0):
		pass

	def save_song(self, event=0):
		if self.chant_affiche.etype == 'song':
			position = self.message_affiche_chant.index("insert")
			psosition_scroll = self.scroll_text.get()[0]

			# a retirer
			title = self.chant_affiche.title
			if title[:3] in ['JEM', 'SUP'] and title[3:6].isdigit():
				self.chant_affiche.title = title[7:]

			print('Saving %s'%self.chant_affiche.chemin)
			self.chant_affiche.transpose =  self.transpose_chant.get(1.0, END)
			self.chant_affiche.capo = self.capo_chant.get(1.0, END)
			self.chant_affiche.key = self.key_chant.get(1.0, END)
			self.chant_affiche.turfNumber = self.numTurfPrint.get(1.0, END)
			self.chant_affiche.hymnNumber = self.numCCLIPrint.get(1.0, END)
			self.chant_affiche.text = self.message_affiche_chant.get(1.0, END)
			self.chant_affiche.title = self.title_chant.get(1.0, END)
			self.chant_affiche.save()
			self.dataBase.add(self.chant_affiche)
			self.searcher.resetCache()

			guiHelper.change_text(self.message_affiche_chant, self.chant_affiche.text)
			guiHelper.change_text(self.title_chant, self.chant_affiche.title)
			guiHelper.change_text(self.transpose_chant, self.chant_affiche.transpose or '')
			guiHelper.change_text(self.capo_chant, self.chant_affiche.capo or '')
			guiHelper.change_text(self.key_chant, self.chant_affiche.key)
			guiHelper.change_text(self.numCCLIPrint, self.chant_affiche.nums.get('hymn') or '')
			guiHelper.change_text(self.numTurfPrint, self.chant_affiche.nums.get('turf') or '')
			guiHelper.change_text(self.numCustomPrint, self.chant_affiche.nums.get('custom') or '')
			self.coloration()

			self.message_affiche_chant.mark_set("insert", position )
			self.message_affiche_chant.yview('moveto', psosition_scroll)
			self.message_affiche_chant.edit_modified(False)

			for field in self.inputFildsList:
				field.edit_modified(False)

			for chant in self.chants_trouve + self.chants_selection:
				if chant.nom == self.chant_affiche.nom:
					chant.resetText()

			self.bouton_save_song.config(state=DISABLED)
			self.affiche_resultats()
			self.affiche_selection()
			if self.chant_affiche:
				self.chant_affiche.diapos[0].printDiapo(self._themePres)

	def save_set(self):
		if not self.chants_selection:
			tkMessageBox.showerror(u'Attention', u'La liste est vide')
		else:
			try:
				curSet = classSet.Set(self.chants_selection)
			except exception.DataReadError as e:
				tkMessageBox.showerror(u'Attention', traceback.format_exc())
				return 1
			if self.combobox_set.get():
				curSet.setName( self.combobox_set.get() )
			extention = globalvar.genSettings.get('Extentions', 'liste')[0]
			nom_sortie = tkFileDialog.asksaveasfilename(initialdir = self.paths.sets, \
										initialfile = curSet.getName(), \
										defaultextension=extention, \
										filetypes=((extention + " file", "*" + extention),
										("All Files", "*.*") ))
			curSet.setName(nom_sortie)
			if nom_sortie != '':
				curSet.save()
				self.chants_selection_previous = copy.copy(self.chants_selection)
				self.get_liste_set()
				self.unsave_set()
				self.combobox_set.set(curSet.getName())
				self.affiche_set()

	def unsave_song(self, event=0):
		notModified = all([not field.edit_modified() for field in self.inputFildsList])

		if (self.message_affiche_chant.edit_modified() or not notModified ) \
				and self.chant_affiche \
				and self.chant_affiche.etype == 'song':
			self.bouton_save_song.config(state=NORMAL)
			self.coloration()

	def unsave_set(self):
		if len(self.chants_selection) == 0:
			self.bouton_present.config(state=DISABLED)
		elif self.chants_selection_previous == self.chants_selection:
			self.bouton_sauv_set.config(state=DISABLED)
			self.bouton_present.config(state=NORMAL)
		else:
			self.bouton_sauv_set.config(state=NORMAL)
			self.bouton_present.config(state=NORMAL)

	def active_suppr_set(self):
		if self.combobox_set.get():
			self.bouton_suppr_set.config(state=NORMAL)
		else:
			self.bouton_suppr_set.config(state=DISABLED)

	def clear(self):
		if self.bouton_sauv_set['state'] != DISABLED:
			if tkMessageBox.askyesno('Sauvegarde', \
					'Voulez-vous sauvegarder les modifications '
					'sur la liste "%s" ?'%self.setName):
				self.combobox_set.set(self.setName)
				self.save_set()
		self.setName = ''
		self.combobox_set.delete(0, END)
		self.chants_selection = []
		self.affiche_selection()
		self.unsave_set()

	def active_boutons(self):
		if self.chant_affiche:
			self.bouton_version.config(state=NORMAL)
			self.bouton_present_select.config(state=NORMAL)
		else:
			self.bouton_version.config(state=DISABLED)
			self.bouton_present_select.config(state=DISABLED)

		if self.liste_selection.curselection(): # ValueError
			self.bouton_up_song.config(state=NORMAL)
			self.bouton_down_song.config(state=NORMAL)
			self.bouton_suppr_song.config(state=NORMAL)
		else:
			self.bouton_up_song.config(state=DISABLED)
			self.bouton_down_song.config(state=DISABLED)
			self.bouton_suppr_song.config(state=DISABLED)

		if self.chants_selection:
			self.bouton_clear.config(state=NORMAL)
		else:
			self.bouton_clear.config(state=DISABLED)

	def fenetre_creation_chant(self, chant_copier=''):
		if self.fenetre_crea:
			self.fenetre_crea.destroy()
			self.fenetre_crea = None
		self.fenetre_crea = Toplevel(self)
		self.fenetre_crea.wm_attributes("-topmost", 1)
		self.fenetre_crea.title("Nouveau chant")
		self.fenetre_crea.geometry("%dx%d+%d+%d"%(200, 80, \
						self._screen.w//2-100, self._screen.h//4-25))

		self.text=Label(self.fenetre_crea, text="title du nouveau chant")
		self.title=Entry(self.fenetre_crea, width=30)
		if chant_copier:
			self.title.insert(0, chant_copier.nom)
		self.bouton = Button(self.fenetre_crea, text='Créer',\
			command = lambda chant = chant_copier: self.crea_chant(chant))

		self.text.grid(row=0, column=0)
		self.title.grid(row=1, column=0)
		self.bouton.grid(row=2, column=0)

		self.fenetre_crea.update()
		self.title.focus_set()

	def	crea_chant(self, chant_copier=''):
		tmp = self.title.get()
		tmp = fonc.upper_first(tmp)
		tmp, title = gestchant.genere_chant(tmp, self.dataBase.getSetSongNames())
		self.nouveau_chant = elements.Chant(tmp, title)

		if self.nouveau_chant.nom not in self.dataBase.getSetSongNames() or \
		(self.nouveau_chant.nom in self.dataBase.getSetSongNames() and\
		tkMessageBox.askyesno('Création', 'Le chant "%s" existe déjà, '
						'voulez-vous l\'écraser ?'%self.nouveau_chant.nom)):
			self.fenetre_crea.destroy()
			self.fenetre_crea = None
			self.chant_affiche = self.nouveau_chant
			self.message_affiche_chant.focus_set()
			if not chant_copier:
				self.printOff()
				self.printOn()
				guiHelper.change_text(self.message_affiche_chant, \
									"%s\n text" \
									%globalvar.genSettings.get('Syntax', 'newslide')[0])
				guiHelper.change_text(self.title_chant, self.chant_affiche.title)
			self.save_song()
			self.dataBase.add(self.nouveau_chant)
			self.searcher.resetCache()
			tkMessageBox.showinfo('Confirmation', \
					'Le chant "%s" a été créé.'%self.nouveau_chant.nom)
			self.chants_trouve = [self.nouveau_chant]
			self.affiche_resultats()
			self.printer()

		if self.fenetre_crea != None:
			self.fenetre_crea.focus_set()
		self.active_boutons()

	def present(self, event=0, mode='liste'):
		missingBacks = background.checkBackgrounds()
		if missingBacks != []:
			tkMessageBox.showerror(u'Attention', 'Les fonds d\'écran '
								'pour les types "%s" sont introuvable.'\
								%', '.join(missingBacks))

		globalvar.presSettings.write()
		self.closeVerseWindow()
		if self.fen_paramGen:
			self.fen_paramGen.destroy()
			self.fen_paramGen = None
		if self.presentation:
			self.presentation.quitter()
		debut = 0
		if self.liste_selection.curselection() and mode == 'liste':
			debut = self.liste_selection.curselection()[0]
		chants_present =[]
		if mode == 'liste':
			for element in self.chants_selection:
				prefix = element.etype
				sufix = element.nom
				if element.exist():
					chants_present.append(element)

		elif self.chant_affiche:
			chants_present.append(self.chant_affiche)
		listDiapos = diapoList.DiapoList(chants_present)
		if listDiapos.lenght>0:
			self.presentation = pres.Presentation(self, listDiapos, debut)

	def paramGen(self):
		if self.fen_paramGen:
			self.fen_paramGen.destroy()
			self.fen_paramGen = None
		self.fen_paramGen = Toplevel(self)
		self.fen_paramGen.title('Paramètres généraux')
		self.fen_paramGen.resizable(width=True, height=True)
		self.fen_paramGen.wm_attributes("-topmost", 1)
		self.fen_paramGen.update_idletasks()
		paramGen = pref.ParamGen(self.fen_paramGen, self)

	def paramPres(self):
		if self.fen_paramPres:
			self.fen_paramPres.destroy()
			self.fen_paramPres = None
		self.fen_paramPres = Toplevel(self)
		self.fen_paramPres.title('Paramètres de présentation')
		self.fen_paramPres.resizable(width=True, height=True)
		self.fen_paramPres.wm_attributes("-topmost", 1)
		self.fen_paramPres.update_idletasks()
		paramPres = pref.ParamPres(self.fen_paramPres, self)
		for element in self.chants_selection:
			del element.diapos[:]

	def writeLatex(self, noCompile=0):
		if self.chants_selection == []:
			tkMessageBox.showerror('Attention', \
						"Il n'y a aucun chants dans la liste.")
			return 1

		if self.fen_latex:
			self.fen_latex.destroy()
			self.fen_latex = None
		self.fen_latex = Toplevel(self)
		self.fen_latex.title('Paramètres Export PDF')
		self.fen_latex.resizable(width=True, height=True)
		self.fen_latex.lift()
		self.fen_latex.update_idletasks()
		self.LatexParam = latex.LatexParam(self.fen_latex, self.chants_selection, self, noCompile)

	def compileLatex(self):
		latexCompiler = latex.CreatePDF([])
		latexCompiler.compileLatex()

	def quickPDF(self):
		self.writeLatex()

	def showDoc(self):
		docPath = os.path.join(globalvar.chemin_root, 'doc')
		if globalvar.portable or globalvar.runByPython:
			docFile = os.path.join(docPath, '%s.pdf'%globalvar.appName)
		else:
			docFile = os.path.join(globalvar.chemin_root, '%s.pdf'%globalvar.appName)
		if not os.path.isfile(docFile):
			fileToCompile = os.path.join(docPath, '%s.tex'%globalvar.appName)
			if os.path.isfile(fileToCompile):
				os.chdir(docPath)
				pdflatex = commandLine.MyCommand('pdflatex')
				pdflatex.checkCommand()
				code, out, err = pdflatex.run(options=[fileToCompile, '&&', fileToCompile], timeOut=10)
				os.chdir(globalvar.chemin_root)
				if code != 0:
					tkMessageBox.showerror('Attention', \
							'Error while compiling latex files. '
							'Error %s:\n%s'%(str(code), err))
					return 1
		if os.path.isfile(docFile):
			commandLine.run_file(docFile)
		else:
			tkMessageBox.showerror(u'Attention', u'Impossible d\'ouvrire '
								'la documentation, le fichier "%s" n\'existe pas.'%docFile)

	def showREADME(self):
		readmeFile = os.path.join(globalvar.chemin_root, 'README.txt')
		if os.path.isfile(readmeFile):
			commandLine.run_file(readmeFile)
		else:
			tkMessageBox.showerror(u'Attention', u'Impossible d\'ouvrire '
								'le fichier README, le fichier "%s" n\'existe pas.'%readmeFile)

	def sendSongs(self):
		self.repo.send()

	def recieveSongs(self):
		if self.repo.receive() == 0:
			self.updateData()
