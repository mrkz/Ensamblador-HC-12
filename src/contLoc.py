#!usr/bin/env python
#coding=utf-8
"""Clase para diseño y formateo del contador de localidades del compilador HC12
   Centro Universitario de Ciencias Exactas e Ingenierías
   Simental Magaña Marcos Eleno Joaquín"""

import string	# importar el paquete para manejo de cadenas
class Contloc:
	def __init__(self,n = 0):
		self.set_contloc(n)

	def formateo(self):
		return self.contHex.rjust(4,'0')	# rellenas con 0's
	
	def fotmatEqu(self,str):
		n = int(str)
		tmp = hex(n)
		tmp = tmp[2:]
		tmp = tmp.rjust(4,'0')
		return tmp.upper()

	def contToHex(self):
		self.contHex = hex(self.contloc)
		# se toma el valor hexadecimal, excepto los caracteres '0x'
		return self.contHex[2:]
	
	def add(self,str):
		n = int(str)
		self.contloc += n
		self.contHex = self.contToHex()
		self.contStr = self.formateo()
	
	def set_contloc(self,n):
		self.contloc = int(n)				# contador entero
		self.contHex = self.contToHex()		# contador en hexadecimal
		self.contStr = self.formateo()		# contador formateado (cadena)
	
	def get_format(self):
		return self.contStr.upper()
