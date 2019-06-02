#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import time
import re


class TimeTime:

    """
    TimeTime est une classe qui permet d'afficher le temps d'exécution de
    fonctions, également de les comparer entre eux. TimTime retourne le
    temps d'exécution total pour <loops> boucles (par défaut 10000) et le
    temps moyen par boucle.

    TimeTime est simple à utiliser. Il est basé sur les modules built-in
    time et re.
    """

    # Special class methods, used in setup.py
    def version(cls):
        """
        Retourne la version de la classe.

        Attention, le numero de version du setup.py est extrait d'ici.
        """
        print("Version 1.0")
    version = classmethod(version)

    # class attributes
    loops = 10000

    def get_loops(cls):
        """
        Retourne le nombre de boucles. Défaut = 10000

        C'est un attribut de classe car ça n'aurait pas de sens de comparer
        2 objets TimeTime n'ayant pas le même nombre de loops.
        """
        return cls.loops
    get_loops = classmethod(get_loops)

    def set_loops(cls, loops):
        """
        Modifie le nombre de boucles. Défaut = 10000

        C'est un attribut de classe car ça n'aurait pas de sens de comparer
        2 objets TimeTime n'ayant pas le même nombre de loops.
        """
        cls.loops = loops
    set_loops = classmethod(set_loops)

    # Constructeur
    def __init__(self, function):
        """
        Constructeur

        Le constructeur préserve la fonction et extrait son nom pour
        futur affichage.
        """
        self.function = function
        self.fname = self._function_name(function)
        # self.loops = 10000

    # Class methods
    def demo(cls):
        """Lance une demo de la classe"""
        from timetime_demo import demo
        demo()
    demo = classmethod(demo)

    # private methods
    def _function_name(self, function):
        """Return le nom de la fonction"""
        p = re.compile(r'(?:[a-zA-Z0-9_])*', re.UNICODE)
        f = re.findall(p, str(function))
        f = f[3]
        return f + "()"

    def _stats(self, fin):
        """Formmate et retourne une chaine de statistique pour la fonction,
        comprenant les temps d'exécution total et moyen"""
        stats = ""
        stats += ("-"*42 + "\n")
        stats += self.fname + ", " + str(self.loops) +\
            " loops.\n"
        stats += "Total runtime = " + str(fin) + "\n"
        stats += "Mean loop = " + str(fin/self.loops)
        stats += ("\n" + "-"*42)
        return stats

    # public methods
    def compute_time(self):
        """Retourne le temps totel d'exécution d'une fonction."""
        start = time.time()
        for i in range(self.loops):
            self.function()
        fin = time.time() - start
        return fin

    # other public methods (overloading)
    def __str__(self):
        """Retourne une chaine de statistique pour la fonction,
        comprenant les temps d'exécution total et moyen"""
        timef = self.compute_time()
        return self._stats(timef)

    def __eq__(self, other):
        """
        2 temps d'exécution égaux sont hautement improbables. On se sert donc
        de l'opérateur == pour retourner une chaine de statistique pour chacune
        des fonctions à comparer.

        Les chaines comprenent chacune les temps d'exécution total et moyen
        pour chaque fonction.

        .. note::
            Exemple d'usage: print(f1 < f2)
        """
        retour = "\n"
        retour += self.fname + " == " + other.fname + "\n"
        retour += self.__str__() + "\n"
        retour += other.__str__()
        return retour

    def __lt__(self, other):
        """
        Retourne:

        - nom f1 < nom f2
        - Total runtime f1 < total runtime f2
        - FALSE or TRUE. Nombre de boucles

        .. note::
            Exemple d'usage: print(f1 < f2)
        """
        retour = ""
        retour += ("-"*42 + "\n")
        retour += self.fname + " < " + other.fname + ", " + str(self.loops) +\
            " loops.\n"
        objet1 = self.compute_time()
        objet2 = other.compute_time()
        retour += str(objet1) + " < " + str(objet2) + "\n"
        retour += "TRUE" if objet1 < objet2 else "FALSE"
        retour += ". Times are total runtimes."
        retour += ("\n" + "-"*42)
        return retour

    def __gt__(self, other):
        """
        Retourne:

        - nom f1 > nom f2
        - Total runtime f1 > total runtime f2
        - FALSE or TRUE. Nombre de boucles

        .. note::
            Exemple d'usage: print(f1 > f2)
        """
        retour = ""
        retour += ("-"*42 + "\n")
        retour += self.fname + " > " + other.fname + ", " + str(self.loops) +\
            " loops.\n"
        objet1 = self.compute_time()
        objet2 = other.compute_time()
        retour += str(objet1) + " > " + str(objet2) + "\n"
        retour += "TRUE" if objet1 > objet2 else "FALSE"
        retour += ". Times are total runtimes."
        retour += ("\n" + "-"*42)
        return retour
