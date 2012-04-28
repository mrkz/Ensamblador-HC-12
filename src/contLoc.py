#!usr/bin/env python
#coding=utf-8
"""Clase para diseño y formateo del contador de localidades del compilador HC12
   Centro Universitario de Ciencias Exactas e Ingenierías
   Simental Magaña Marcos Eleno Joaquín"""

import string	# importar el paquete para manejo de cadenas
class Contloc:
	def __init__(self):
		self.contloc = 0					# contador entero
		self.contHex = self.contToHex()		# contador en hexadecimal
		self.contStr = self.format()		# contador formateado (cadena)

	def format():
		self.contStr = contHex.rjustrjust(4,'0')	# rellenas con 0's

	def contToHex():
		self.contHex = hex(self.contloc)
		# se toma el valor hexadecimal, excepto los caracteres '0x'
		self.contHex = self.contHex[2:]
	
	def add(int):
		self.contloc += int
		self.contHex = self.contToHex()
		self.contStr = self.format()

	def get_format():
		return self.contStr
