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
		self.__is_label = False
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
	
	def set_is_label(self):
		self.__is_label = True

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
	
	def is_label(self):
		return self.__is_label
	
	def set_val_contloc(self,string):
		self.__contloc = string
	
	def get_val_contloc(self):
		return self.__contloc
	
	def get_rel8(self):
		operator = self.get_decimal(self.get_operator())
		contLocDec = int(self.get_val_contloc(),16)
		total = operator - (contLocDec + self.get_totalbytes())
		if total < 0: # es valor negativo y se saca a pata :v
			operator = hex( (total + (1<<8)) % (1<<8))
			operator = operator[2:]
		else:
			operator = self.get_hexadecimal_format(str(total))
		operator = operator.upper()
		return operator
	
	def get_rel16(self):
		operator = self.get_decimal(self.get_operator())
		contLocDec = int(self.get_val_contloc(),16)
		total = operator - (contLocDec + self.get_totalbytes())
		if total < 0: # es valor negativo y se saca a pata :v
			operator = hex( (total + (1<<16)) % (1<<16))
			operator = operator[2:]
			operator = operator[:2]+" "+operator[2:]
		else:
			operator = self.get_hexadecimal_format(str(total))
		operator = operator.upper()
		return operator
	
	def get_rel9(self):
		register_dict = {'A':0, 'B':1, 'D':4, 'X':5, 'Y':6, 'SP':7} #diccionario con registros
		cod_op_dict = {'DBEQ':0, 'DBNE':32, 'TBEQ':64, 'TBNE':96, 'IBEQ':128, 'IBNE': 160}
		contLocDec = int(self.get_val_contloc(),16)
		operator = self.get_operator()	# se recibe cadena completa i.e.: SP,643
		register = operator[:operator.find(',')].upper() # se extrae el registro i.e.: SP y se hace mayúscula
		operNum = operator[operator.find(',')+1:] # se extrae el valor numérico i.e.: 643
		operNum = self.get_decimal(operNum) # se obtiene entero decimal i.e: F → 15
		contLocDec = int(self.get_val_contloc(),16)
		total = operNum - (contLocDec + self.get_totalbytes())
		if total < 0: # es valor negativo y se saca a pata :v
			operNumHex = hex( (total + (1<<8)) % (1<<8))
			operNumHex = operNumHex[2:].upper()
		else:
			operNumHex = self.get_hexadecimal_format(str(total))
		operNumHex = operNumHex.rjust(2,'0')
		rr = register_dict[register]
		lb = cod_op_dict[self.get_opcode()] + rr
		if operNum < (contLocDec + self.get_totalbytes()): # salto negativo se le suman 10
			lb = lb + 16
		lb = hex(lb)
		lb = lb[2:].rjust(2,'0').upper()
		operator = lb+" "+operNumHex
		return operator
	
	def get_idx_pre_post(self):
		opr_dict = {'1':'0000', '2':'0001', '3':'0010', '4':'0011', '5':'0100', '6':'0101', '7':'0110', '8': '0111',
					'+1':'0000', '+2':'0001', '+3':'0010', '+4':'0011', '+5':'0100', '+6':'0101', '+7':'0110', '+8': '0111',
					'-1':'1111', '-2':'1110', '-3':'1101', '-4':'1100', '-5':'1011', '-6':'1010', '-7':'1001', '-8':'1000'}
		
		rr1p_dict = {'+X':'0010', '-X':'0010', 'X+':'0011', 'X-':'0011', '+Y':'0110', '-Y':'0110', 'Y+':'0111', 'Y-':'0111',
					 '+SP':'1010', '-SP':'1010', 'SP+':'1011', 'SP-':'1011'}
		operator = self.get_operator()
		operNum = int(operator[:operator.find(',')])
		if "-" in operator:
			operNum*= -1
		operNum = str(operNum)
		xysp = operator[operator.find(',')+1:]
		strBin = rr1p_dict[xysp]+opr_dict[operNum]
		operator = hex(int(strBin,2))[2:].upper()
		operator = operator.rjust(2,'0')	# si no está completo, se rellena con ceros
		return operator
	
	def get_idx_5bits(self):
		opr_dict = {'-16':'10000', '-15':'10001', '-14':'10010', '-13':'10011', '-12':'10100', '-11':'10101', '-10':'10110',
				    '-9' :'10111', '-8' :'11000', '-7' :'11001', '-6' :'11010', '-5' :'11011', '-4' :'11100', '-3' :'11101',
				    '-2' :'11110', '-1' :'11111', '0'  :'00000', '1'  :'00001', '2'  :'00010', '3'  :'00011', '4'  :'00100',
				    '5'  :'00101', '6'  :'00110', '7'  :'00111', '8'  :'01000', '9'  :'01001', '10' :'01010', '11' :'01011',
				    '12' :'01100', '13' :'01101', '14' :'01110', '15' :'01111'}
		rr_dict = {'X':'000','Y':'010', 'SP':'100', 'PC': '110'}
		operator = self.get_operator().upper()
		if operator.find(',') == 0:
			operNum = '0'
		else:
			operNum = operator[:operator.find(',')]
		xysp = operator[operator.find(',')+1:]
		strBin = rr_dict[xysp]+opr_dict[operNum]
		operator = hex(int(strBin,2))[2:].upper()
		operator = operator.rjust(2,'0')	# si no está completo, se rellena con ceros
		return operator
	
	def get_idx_acum(self):
		operator = self.get_operator().upper()
		abd_dict = {'A':'100','B':'101','D':'110'}
		rr_dict = {'X':'11100', 'Y':'11101', 'PC':'11111', 'SP':'11110'}
		abd = operator[:operator.find(',')]
		xysp = operator[operator.find(',')+1:]
		strBin =  rr_dict[xysp]+abd_dict[abd]
		operator = hex(int(strBin,2))[2:].upper()
		operator = operator.rjust(2,'0')	# si no está completo, se rellena con ceros
		return operator
	
	def get_machinecode(self,tabop, dict_tbs=None): #dict_tbs para los elementos que tienen etiqueta en el operando
		#obtengo código de la lista en diccionario[CODOP][DIRECCIONAMIENTO] 
		machCode = tabop.tabop[self.get_opcode()][self.get_direccionamiento()][1]
		if self.get_direccionamiento() == "DIR":
			machCode+= " " + self.get_hexadecimal_format(self.get_operator())
		elif self.get_direccionamiento() == "REL":
			if self.get_totalbytes() == 4:
				machCode+= " "+self.get_rel16()
			elif self.get_totalbytes() == 3:
				machCode+= " "+self.get_rel9()
			else: #se infiere que self.get_totalbytes() == 2
				machCode+= " "+self.get_rel8()
		elif self.get_direccionamiento() == "EXT":
			#machCode+= " hh ll"
			if dict_tbs == None: # no hay diccionario por que no hay etiqueta y no se llamó al método con diccionario
				machCode+= " " + self.get_hexadecimal_format_filled(self.get_operator())
			else: # se envió un diccionario y se añadirá el contloc de la etiqueta
				format_contloc = dict_tbs[self.get_operator()]
				format_contloc = format_contloc[:2]+" "+format_contloc[2:]
				machCode+= " " + format_contloc
		elif self.get_direccionamiento() == "IMM":
			if self.get_totalbytes() == 2:
				machCode+= " " + self.get_hexadecimal_format(self.get_operator())
			else:
				machCode+= " " + self.get_hexadecimal_format_filled(self.get_operator())
		elif self.get_direccionamiento() == "IDX":
			op = self.get_operator().upper()
			if (("+X" in op) or ("-X" in op) or ("X+" in op) or ("X-" in op) or\
			   ("+Y" in op) or ("-Y" in op) or ("Y+" in op) or ("Y-" in op) or\
			   ("+SP" in op) or ("-SP" in op) or ("SP+" in op) or ("SP-" in op)):
				machCode+= " "+self.get_idx_pre_post()
			elif (self.contain_digit(self.get_operator()) and ("," in self.get_operator())) or op[0]==',':	# es un idx de 5 bits (hasta p8)
				machCode+= " "+self.get_idx_5bits()
			else:
				machCode+= " "+self.get_idx_acum()
		elif self.get_direccionamiento() == "IDX1":
			machCode+=" xb ff "
		elif self.get_direccionamiento() == "IDX2":
			machCode+= " xb ee ff"
		elif self.get_direccionamiento() == "[IDX2]":
			machCode+= " [xb ee ff]"
		elif self.get_direccionamiento() == "[D,IDX]":
			machCode+= " [xb]"
		return machCode
	
	def contain_digit(self,string):
		band = False
		for i in string:
			if i.isdigit():
				band = True
				break
		return band

	def check_label(self,cad=None):
		"""método que revisa la composición de una etiqueta mediante expresiones regulares
				La etiqueta es válida si:
					- Tiene una longitud de entre 1 y 5 caracteres inclusive
					- Inicia con letra o guión bajo
					- Contiene solo letras, guión bajo o números"""
		# compilar patrón para una etiqueta
		label_pattern = re.compile('[a-zA-Z_][\w]+')
		if cad == None:
			cad = self.get_label()
		# verdadero si la cadena dada (etiqueta) coincide con la ex. regular y tiene tamaño 0<cad<6
		if label_pattern.match(cad) and len(cad) < 6:
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
				string = string+"Instrucción: "+self.get_opcode()+"\n"
			else:
				return "Línea "+str(self.line_number)+":\nLinea inválida: código de operación no válido\n"
		else:
			string = string+"Instrucción: "+"\n"
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
		#print operando # linea temporal para ver hasta donde dice crash :v
		commaIndex = operando.find(',')
		if operando == None:
			return "INH"
		elif operando[0]=='#':
			return "IMM"
		
		# si el operando tiene una coma es REL o uno de la familia de IDX
		elif commaIndex >= 0: # puede ser REL9 o IDX
			sp = operando.find('SP'); a = operando.find('A'); b = operando.find('B');
			d = operando.find('D'); x = operando.find('X'); y = operando.find('Y');
			if ((sp <  commaIndex) and (sp != -1)) or (((a <  commaIndex) and (a != -1)) and (operando[-1].isdigit())) or\
													  (((b <  commaIndex) and (b != -1)) and (operando[-1].isdigit())) or\
													  (((d <  commaIndex) and (d != -1)) and (operando[-1].isdigit())) or\
			   ((x < commaIndex) and (x != -1))   or ((y < commaIndex) and (y != -1)):	# es REL
				return "REL"
			else:
				# nido de indexados
				number = self.get_number_from_idx(operando)
				print number, operando
				if number != None:
					number = self.get_decimal(number)
				if '[' in operando:
					if 'D' in operando.upper():
						return "[D,IDX]"
					else:
						return "[IDX2]"
				elif (number >= -16) and (number <= 15):
					return "IDX" #idx de 5 bits
				elif (number >=-256) and (number<= 255):
					return "IDX1"
				else:	# se infiere que es un IDX2 (IDX de 16 bits)
					return "IDX2"
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
			self.set_is_label()
			return "EXT"
	
	def get_number_from_idx(self,str):
		st = ""	 # cadena donde se almacenará el número
		for i in str:
			if i.isdigit() or i=='-' or i=='@' or i=='$' or i=='%':
				st+=i
		if st == "":
			return None
		return st
	
	def get_decimal(self,cadena):
		if cadena[0]=='#':
			cadena = cadena[1:]
			
		if cadena[0]=='@':
			cadena = cadena[1:]
			return int(cadena,8)
		elif cadena[0]=='%':
			cadena = cadena[1:]
			return int(cadena,2)
		elif cadena[0]=='$':
			cadena = cadena[1:]
			return int(cadena,16)
		else: 	#es un entero i.e: 10
			return int(cadena)

	def get_hexadecimal_format(self,cadena):
		hex_format = hex(self.get_decimal(cadena))
		hex_format = hex_format[2:].upper() # se le quita el '0x' y se hace mayúsculas
		return hex_format
	
	def get_hexadecimal_format_filled(self,cadena):
		hex_format_filled = self.get_hexadecimal_format(cadena)
		hex_format_filled = hex_format_filled.rjust(4,'0') # se rellena con ceros
		hex_format_filled = hex_format_filled[:2]+" "+hex_format_filled[2:]
		return hex_format_filled

	def all_none(self):
		if self.get_label() == None and self.get_opcode() == None and self.get_operator() == None:
			return True
		return False

