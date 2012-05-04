#!usr/bin/env python
#coding=utf-8
"""Clase para análisis de código ensamblador del compilador HC12
   Centro Universitario de Ciencias Exactas e Ingenierías
   Simental Magaña Marcos Eleno Joaquín"""

import re 		# importar el paquete de manejo de expresiones regualres
import string 	# importar el paquete para manejo de cadenas
import sys
class Linea:
	"""Clase que abstrae una linea de código ensamblador como un objeto"""
	# constructor de la clase Linea
	def __init__(self,line,line_number):
		self.set_none()
		"""Constructor de la clase Linea, __init__(self,line,line_number), Linea(str,int)""" 
		# el objeto linea tiene atributos
		#	linea 		-> tiene todo el contenido de la linea del código ([etiqueta],<codop>|<directiva>,[operador],[comentario])
		#	line_number -> el numero de linea que le corresponde en el código ensamblador
		#	direccionamiento -> el modo de direccionamiento de la linea según su código de operación
		#	totalbytes -> el número de bytes que genera el código de operación con ese direccionamiento (porposito: para sumar el contloc)
		# si hay un caracter ';' se retirará desde el indice del caracter hasta el final de la linea
		if line.find(';') >= 0:
			line = line[:line.find(';')]
		self.line = line.replace('\t',' ')
		self.line_number = line_number
		self.list_line_split = self.line.split() # linea dividida en tokens. Criterio de divisibilidad es el espacio en blanco.
		if self.line.startswith(' '):
			if   len(self.list_line_split) == 1:
				self.set_none()
				self.set_opcode(self.list_line_split[0])
			elif len(self.list_line_split) == 2:
				self.set_label()
				self.set_opcode(self.list_line_split[0])
				self.set_operator(self.list_line_split[1])
			elif len(self.list_line_split) > 2:
				self.set_none()
				return
		else:
			if   len(self.list_line_split) == 2:
				self.set_label(self.list_line_split[0])
				self.set_opcode(self.list_line_split[1])
			elif len(self.list_line_split) == 3:
				self.set_label(self.list_line_split[0])
				self.set_opcode(self.list_line_split[1])
				self.set_operator(self.list_line_split[2])
			elif len(self.list_line_split) > 3 or len(self.list_line_split) < 2:
				self.set_none()
				return


	def set_none(self):
		self.set_label()
		self.set_opcode()
		self.set_operator()
			
	def set_label(self,label=None):
		self.__label = label

	def set_opcode(self,opcode=None):
		self.__opcode = opcode

	def set_operator(self,operator=None):
		self.__operator = operator
	
	def set_direccionamiento(self,dire):
		self.__direccionamiento=str(dire)
	
	def set_totalbytes(self,n):
		self.__totalbytes = n

	def get_label(self):
		return self.__label

	def get_opcode(self):
		return self.__opcode

	def get_operator(self):
		return self.__operator
	
	def get_direccionamiento(self):
		return self.__direccionamiento
	
	def get_totalbytes(self):
		return self.__totalbytes
	
	def get_machinecode(self,tabop):
		#obtengo código de la lista en diccionario[CODOP][DIRECCIONAMIENTO] 
		machCode = tabop.tabop[self.get_opcode()][self.get_direccionamiento()][1]
		if self.get_direccionamiento() == "DIR":
			machCode+= " dd"
		elif self.get_direccionamiento() == "REL":
			if self.get_totalbytes() == 4:
				machCode+= " qq rr"
			elif self.get_totalbytes() == 3:
				machCode+= " lb rr"
			else: #se infiere que self.get_totalbytes() == 2
				machCode+= " rr"
		elif self.get_direccionamiento() == "EXT":
			machCode+= " hh ll"
		elif self.get_direccionamiento() == "IMM":
			if self.get_totalbytes() == 2:
				machCode+= " ii"
			else:
				machCode+= " jj kk"
		return machCode

	def check_label(self):
		"""método que revisa la composición de una etiqueta mediante expresiones regulares
				La etiqueta es válida si:
					- Tiene una longitud de entre 1 y 5 caracteres inclusive
					- Inicia con letra o guión bajo
					- Contiene solo letras, guión bajo o números"""
		# compilar patrón para una etiqueta
		label_pattern = re.compile('[\w^0-9][\w]+')
		
		# verdadero si la etiqueta coincide con la ex. regular y tiene tamaño 0<label<6
		if label_pattern.match( self.get_label()) and len( self.get_label()) < 6:
			return True
		return False
	
	def check_opcode(self):
		"""método que revisa la composición de un código de operacion mediante expresiones regulares
				El código de operación es válido si:
					-Comienza con mayúscula o minúscula.
					-Puede o no tener un punto.
					-Longitud máxima de 8 caracteres."""
		
		#compilo patrón de la expresión
		opcode_pattern = re.compile('[a-zA-Z]+\\.?[a-zA-Z]*')
		
		#verdadero si el codigo de operación coindide con la expresión regular y tamaño 0<opcode<6
		if opcode_pattern.match(self.get_opcode()) and len(self.get_opcode())  < 6:
			return True
		return False

	def toString(self,tabop=None):
		# verdadero si linea vacía y sale del método
		if len(self.list_line_split) == 0:
			return None
		string = "Línea "+str(self.line_number)+':'+"\n"
		if self.get_label()!=None:
			if (self.check_label()==False):
				return ("Línea "+str(self.line_number)+":\nLinea inválida: etiqueta no válida\n")
		# se define una lista (self.get_label(),""), y dependiendo el valor de la comparacion tomará el elemento
		string = string+"Etiqueta:    "+(self.get_label(),"")[self.get_label()==None]+"\n"
		if self.get_opcode() != None:
			if(self.check_opcode()):
				string = string+"Instrucción142: "+self.get_opcode()+"\n"
			else:
				return "Línea "+str(self.line_number)+":\nLinea inválida: código de operación no válido\n"
		else:
			string = string+"Instrucción146: "+"\n"
		string = string+"Operando(s): "+(self.get_operator(),"")[self.get_operator()==None]+"\n"
		operator = self.get_operator()
		if operator != None:
			if operator.find(','):
				operator_list = operator.split(',')
				string = string+"Número de operandos: "+str(len(operator_list))
			elif operator != None:
				string = string+"Número de operandos: 1"
		else:
			string = string+"Número de operandos: 0"
		if tabop != None:
			if tabop.tabop.has_key(self.get_opcode()):
				mode = self.selectMode(self.get_opcode(), self.get_operator(), tabop)
				self.set_direccionamiento(mode)
				string = string + "\nDireccionamientos: " + self.get_direccionamiento()
				#i.e.: diccionario[ABA][INH][Total_bytes]
				#donde Total_bytes es el último elemento de la lista que alberga el diccionario en
				#la posición diccionario[ABA][INH] /* = ["false",1806,2,0,2] */
				self.set_totalbytes(int(tabop.tabop[self.get_opcode()][self.get_direccionamiento()][-1]))
				string = string + "\nCantidad de bytes: " + str(self.get_totalbytes())
		return string
	
	def selectMode(self, codop, operando, tabop):
		if operando == None:
			return "INH"
		elif operando[0]=='#':
			return "IMM"
		#puede ser DIR,EXT,REL
		elif operando[0]=='@' or operando[0]=='$' or operando[0]=='%' or operando[0].isdigit():
			valor_decimal = self.get_decimal(operando)
			if operando[0].isdigit():
				valor_decimal = int(operando,10)
			if   valor_decimal <= 255 and valor_decimal >= -256:
				if tabop.tabop[codop].has_key("DIR"):
					return "DIR"
				else:
				# linea nueva de p4
					if tabop.tabop[codop].has_key("EXT"):
						return "EXT"
					else:
				# termina linea nueva de p4
						return "REL"
			elif valor_decimal <= 65535 and valor_decimal >= -32768:
				if tabop.tabop[codop].has_key("EXT"):
					return "EXT"
				else:
					return "REL"
		#se infiere que es una etiqueta
		else:
			return "EXT"
			
	def get_decimal(self,cadena):
		if cadena[0]=='@':
			cadena = cadena[1:]
			return int(cadena,8)
		elif cadena[0]=='%':
			cadena = cadena[1:]
			return int(cadena,2)
		else:
			cadena = cadena[1:]
			return int(cadena,16)

	def all_none(self):
		if self.get_label() == None and self.get_opcode() == None and self.get_operator() == None:
			return True
		return False

