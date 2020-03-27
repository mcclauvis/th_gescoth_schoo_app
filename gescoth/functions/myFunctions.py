# -*- coding: utf-8 -*-

def Rang(note, sexe, data):
	"""Fonction permettant de calculer le rang
	d'une note en en se bansant le sexes
	"""
	rang = ""
	data.sort()
	data.reverse()
	index = data.index(note) + 1
	if index == 1 and sexe == 'F':
		rang = '1ère'
	elif index == 1 and sexe == 'M':
		rang= '1er'
	else:
		rang = str(index) + 'ème'
	if data.count(note) > 1:
		rang += ' ex'
	return rang
