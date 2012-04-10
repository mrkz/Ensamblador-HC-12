#!/usr/bin/env python
# coding=utf-8
"""Clase para crear un objeto instrucción, con atributos tipo lista para
	proyecto del compilador HC12.
   Centro Universitario de Ciencias Exactas e Ingenierías
   Simental Magaña Marcos Eleno Joaquín"""

class operador:
	def __init__(self,operador,has_operando,direccionamiento,
				 bytecodes,bytes_generados,faltan,total):
		self.op = operador
		# si el has_operando es falso, entonces self.has_op es falso, 
		# sino self.has_op es verdadero
		self.has_op = (True,False)[has_operando=="false"]
		self.dir = 
	
