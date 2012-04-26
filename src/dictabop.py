#!usr/bin/env python
#coding=utf-8
"""Clase que crea un Diccionario con los códigos de operación
	del compilador HC12.
   Centro Universitario de Ciencias Exactas e Ingenierías
   Simental Magaña Marcos Eleno Joaquín"""
class Tabop:

	tabop   = {}
	
	def __init__(self):
		print "Creating dict..."
		tmpfile = open("TABOP/TABOP.data",'r')
		cad = tmpfile.readlines()
		tmpfile.close()
		for i in cad:
			tmpline = i.split('|')
			tmplist = self.createList(i)
			if self.tabop.has_key(tmpline[0]):
				self.tabop[tmpline[0]][tmpline[2]] = tmplist
			else:
				self.tabop[tmpline[0]] = {tmpline[2]:tmplist}
		
	def createList(self,string):
		tmplist = string.split('|')
		tmplist.pop(2)
		tmplist.pop(0)
		return tmplist
