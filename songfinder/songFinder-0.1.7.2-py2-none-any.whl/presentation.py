# -*- coding: utf-8 -*-
from __future__ import division

import tkFont
from Tkinter import *
import math
import warnings
import time
import traceback
import gc

import src.elements.elements as elements
import src.screen as screen
import src.globalvar as globalvar
import src.diapo as classDiapo
import src.themes as themes
import src.simpleProgress as simpleProgress

### Serveur HTTP
# ~ import BaseHTTPServer
# ~ import CGIHTTPServer
### Serveur HTTP

#~ try:
	#~ import vlc_player
	#~ vlc = 1
#~ except:
	#~ warnings.warn('VLC not found')
	#~ vlc = 0
vlc = 0

class Presentation(object, Frame):
	def __init__(self, fenetre, listeDiapos, debut, **kwargs):
		tmpsTotal=time.time()
		Frame.__init__(self, fenetre, **kwargs)
		self.grid()

		#~ if vlc:
			#~ self.fen_player = Toplevel()
		self.fen_player = None
		self.videopanel = None
		self.player = None

		### Serveur HTTP
		# ~ PORT = 8888
		# ~ server_address = ("", PORT)

		# ~ server = BaseHTTPServer.HTTPServer
		# ~ handler = CGIHTTPServer.CGIHTTPRequestHandler
		# ~ handler.cgi_directories = ["/"]
		# ~ print("Serveur actif sur le port:", PORT)

		# ~ httpd = server(server_address, handler)
		# ~ httpd.serve_forever()
		### Serveur HTTP
		self.sub = globalvar.genSettings.get('Parameters', 'size_of_previews')

		self.listDiapos = listeDiapos

		# Fenetre de presentation
		self.fen_pres = Toplevel(self)
		self.fen_pres.withdraw()
		self.fen_pres.title("Presentation")
		if globalvar.myOs == 'ubuntu':
			self.fen_pres.attributes("-fullscreen", True)
		else:
			self.fen_pres.overrideredirect(1)
		self.fen_pres.protocol("WM_DELETE_WINDOW", self.quitter)
		self.nb_screen, self.screen1, self.screen2, self.screen1use = screen.number_screen() ## very Slow

		ratio_impose = screen.getRatio(globalvar.genSettings.get('Parameters', 'ratio'), self.screen2.ratio)
		self.fen_pres.geometry(self.screen2.full)
		if ratio_impose != 0:
			self.screen2.set_w( int(math.floor(min(ratio_impose*self.screen2.h, self.screen2.w))) )
			self.screen2.set_h( int(math.floor(min(self.screen2.w//ratio_impose, self.screen2.h))) )

		self._themePres = themes.Theme(self.fen_pres, width=self.screen2.w, height=self.screen2.h, bg='black')
		self._themePres.pack(side=TOP, fill=BOTH, expand=1)
		listToPrefetch = [self._themePres]

		print("Nombre d'ecrans: %d -- Resolutions: %s (%s)- %s"\
				%(self.nb_screen, self.screen1, self.screen1use, self.screen2))

		# Gestion liste
		if self.nb_screen > 1:
			self.fen_gestion = Toplevel(self)
			self.fen_gestion.withdraw()
			self.fen_gestion.title("Gestion diapositives")
			self.fen_gestion.resizable(True,True)
			self.fen_gestion.update_idletasks()
			self.fen_gestion.protocol("WM_DELETE_WINDOW", self.quitter)
			previewSubFrame = Frame(self.fen_gestion)

		########
			self._themePrev1 = themes.Theme(previewSubFrame)
			self._themePrev1.pack(side=TOP)
			self._themePrev2 = themes.Theme(previewSubFrame)
			self._themePrev2.pack(side=TOP)
			listToPrefetch.append(self._themePrev1)
			listToPrefetch.append(self._themePrev2)
		########

			self.liste_diapos = Listbox(self.fen_gestion, selectmode=BROWSE, width=40, height=30)
			self.scroll_liste = Scrollbar(self.fen_gestion, command=self.liste_diapos.yview)
			self.liste_diapos['yscrollcommand'] = self.scroll_liste.set

			self.liste_diapos.pack(side=LEFT, fill=Y)
			self.scroll_liste.pack(side=LEFT, fill=Y)

			self.slider = Scale(self.fen_gestion, from_=0.3, to=3, resolution=0.1, length=300, orient=VERTICAL)
			self.slider.pack(side=LEFT)
			self.slider.set(globalvar.genSettings.get('Parameters', 'size_of_previews'))

			previewSubFrame.pack(side=LEFT, fill=BOTH, expand=1)

			self.fen_gestion.update()
			self.widthOffset = self.liste_diapos.winfo_reqwidth() + \
								self.scroll_liste.winfo_reqwidth() + \
								self.slider.winfo_reqwidth()
			self.previewWidth = min((self.screen1use.w-self.widthOffset), self.screen1use.h*self.screen2.ratio)
			self.previewHeight = self.previewWidth/self.screen2.ratio

			self.orient = screen.choose_orient(self.screen1use, self.screen2.ratio, \
												self.widthOffset, 0)

			self.w_g = self.fen_gestion.winfo_reqwidth()
			self.h_g = self.fen_gestion.winfo_reqheight()
			self.fen_gestion.geometry(screen.Screen(self.w_g, self.h_g).full)
			self.fen_gestion.update()

			self.fen_gestion.bind("<KeyRelease-Up>", self.select_diapo)
			self.fen_gestion.bind("<KeyRelease-Down>", self.select_diapo)
			self.liste_diapos.bind("<ButtonRelease-1>", self.select_diapo)
			self.slider.bind("<ButtonRelease-1>", self.place_preview)

			self.liste_diapos.select_set(debut)
			self.liste_diapos.activate(debut)

		globalBindings = {"<Left>":self.diapo_precedant, \
						"<Right>":self.diapo_suivant, \
						"<Prior>":self.diapo_precedant, \
						"<Next>":self.diapo_suivant, \
						"<Escape>":self.quitter}
		self.bindingsObjects = {key:self.bind_all(key, value) for key,value in globalBindings.items()}
		self.fen_pres.bind("<Up>", self.diapo_precedant)
		self.fen_pres.bind("<Down>", self.diapo_suivant)
		self.fen_pres.bind("<Button-1>", self.diapo_suivant)
		self.fen_pres.bind("<Button-3>", self.diapo_precedant)

		if vlc and self.fen_player:
			self.fen_player.bind("<Up>", self.diapo_precedant)
			self.fen_player.bind("<Down>", self.diapo_suivant)
			self.fen_player.bind("<Button-1>", self.diapo_suivant)
			self.fen_player.bind("<Button-3>", self.diapo_precedant)

		if self.nb_screen > 1:
			self.liste_diapos.focus_set()
		elif self.nb_screen == 1:
			self._themePres.focus_set()

		#~ self.videopanel.update_idletasks()
		#~ self.videopanel.focus_set()

		### Setting up diapo list
		progressBar = simpleProgress.SimpleProgress(self, "Création du cache des images", screen=self.screen1)
		progressBar.start(self.listDiapos.lenght)
		self.listDiapos.prefetch(listToPrefetch, progressBar.update)
		progressBar.stop()
		self.listDiapos.getList(debut)
		###

		if self.nb_screen > 1:
			self.place_preview()
			self.select_diapo()
			self.listDiapos.writeListBox(self.liste_diapos)
			self.fen_gestion.deiconify()
		self.fen_pres.deiconify()
		print("Temps creation presentation " + str(time.time()-tmpsTotal))


	def diapo_precedant(self, event):
		self.listDiapos.decremente()
		self.printer()

	def diapo_suivant(self, event):
		self.listDiapos.incremente()
		self.printer()

	def select_diapo(self, event=0):
		self.quit_media()
		if self.liste_diapos.curselection():
			self.listDiapos.number = int(self.liste_diapos.curselection()[0])
		self.printer()

	def printer(self):
		if self.nb_screen > 1:
			self.listDiapos.selectListBox(self.liste_diapos)
		self._printer()
		self._prefetcher()

	def _printer(self):
		diapo = self.listDiapos.current
		if self._themePres.name != diapo.themeName:
			self._themePres.destroy()
			self._themePres = themes.Theme(self.fen_pres, diapo.etype, width=self.screen2.w, height=self.screen2.h)
			self._themePres.pack(side=TOP, fill=BOTH, expand=1)
		diapo.printDiapo(self._themePres)

		if self.nb_screen > 1:
			if self._themePrev1.name != diapo.themeName:
				self._themePrev1.destroy()
				self._themePrev1 = themes.Theme(self.fen_gestion, diapo.etype)
				self._themePrev1.pack(side=self.orient)
			diapo.printDiapo(self._themePrev1)

			diapo = self.listDiapos.next
			if self._themePrev2.name != diapo.themeName:
				self._themePrev2.destroy()
				self._themePrev2 = themes.Theme(self.fen_gestion, diapo.etype)
				self._themePrev2.pack(side=self.orient)
			diapo.printDiapo(self._themePrev2)

	def _prefetcher(self):
		themes = []
		if self.nb_screen > 1:
			themes.append(self._themePrev1)
		themes.append(self._themePres)
		self.listDiapos.previous.prefetch(themes)
		if self.nb_screen > 1:
			self.listDiapos.previous.prefetch([self._themePrev2])
		self.listDiapos.next.prefetch(themes)
		if self.nb_screen > 1:
			self.listDiapos.nextnext.prefetch([self._themePrev2])

	def place_preview(self, event=None):
		try:
			self.sub = float(self.slider.get())
		except ValueError:
			warnings.warn('ValueError in place preview')
			self.sub = globalvar.genSettings.get('Parameters', 'size_of_previews')

		width = self.previewWidth/(1+self.sub)
		height = self.previewHeight/(1+self.sub)

		self._themePrev1.resize(width*self.sub, height*self.sub)
		self._themePrev2.resize(width, height)

		self._themePrev1.pack_forget()
		self._themePrev2.pack_forget()

		self._themePrev1.pack(side=self.orient)
		self._themePrev2.pack(side=self.orient)

		self.printer()
		self.resizeGestion()

	def resizeGestion(self):
		try:
			self.fen_gestion.update_idletasks() # Seems to be necessary ?
			prev1Width = self._themePrev1.winfo_reqwidth()
			prev2Width = self._themePrev2.winfo_reqwidth()
			prev1Height = self._themePrev1.winfo_reqheight()
			prev2Height = self._themePrev2.winfo_reqheight()
			if self.orient == TOP:
				longueur = self.widthOffset + max(prev1Width, prev2Width)
				hauteur = prev1Height + prev2Height
			else:
				longueur = self.widthOffset + prev1Width + prev2Width
				hauteur = max(prev1Height, prev2Height)

			# On windows winfo_x and winfo_y are offset by -8 ?
			longueur = min(longueur, self.screen1use.w - self.fen_gestion.winfo_x()-9)
			hauteur = min(hauteur, self.screen1use.h - self.fen_gestion.winfo_y()-9)
			self.fen_gestion.geometry("%dx%d"%(longueur, hauteur))
		except:
			warnings.warn('Update_fen failed: %s'%traceback.format_exc())

	def quit_media(self):
		if self.videopanel:
			self.videopanel.destroy()
			self.videopanel = None
		if self.player:
			self.player.timer.stop()
			self.player.OnStop()
			self.player.ctrlpanel.grid_forget()
			self.player.ctrlpanel2.grid_forget()
		if self.fen_player:
			self.fen_player.destroy()
			self.fen_player = None

	def quitter(self, event=None):
		self.quit_media()
		for key,value in self.bindingsObjects.items():
			self.unbind(key, value)
		self.listDiapos = None
		if self.nb_screen > 1:
			self.fen_gestion.destroy()
			self.fen_gestion = None
			globalvar.genSettings.set('Parameters', 'size_of_previews', str(self.sub))
		self.fen_pres.destroy()
		self.fen_pres = None
		self.destroy()
		self.master.presentation = None
		print('GC collected objects : %d' % gc.collect())
