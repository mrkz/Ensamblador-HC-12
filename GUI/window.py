#!/usr/bin/env python
# coding=utf-8
"""Clase para el dibujado de la interfaz del proyecto del compilador HC12
   Centro Universitario de Ciencias Exactas e Ingenierías
   Simental Magaña Marcos Eleno Joaquín"""

import pygtk
pygtk.require('2.0')
import gtk
import gtksourceview
import sys

sys.path.append('../src')
from src.analizadorDeLineas import Linea
from src.dictabop import Tabop
from src.contLoc import Contloc

class Ventana:
	def __init__(self,title,type=gtk.WINDOW_TOPLEVEL):

		# crear, fijar titulo, fijar tamaño y conectar señal de la ventana
		self.window = gtk.Window(type) 	# atributo window recibe objeto ventana del tipo 'type'
		self.window.set_title(title) 	# se fija titulo recibido en el constructor
		self.window.set_default_size(400,300) 	#(base,altura)
		self.window.set_resizable(True)
		self.window.connect("delete_event",self.delete_event)
		
		# crear, empaquetar y conectar señales de la vBox
		self.vBox = gtk.VBox(gtk.FALSE,0)	# crear una caja vertical para empaquetar widgets
		self.window.add(self.vBox)	# empaquetar vBox en la ventana

		# crear un item para menu (boton "Archivo")
		self.menu_item_file = gtk.MenuItem("_Archivo")

		# crear menu y empaquetar en la barra de menu
		self.menu_bar = gtk.MenuBar()	# se crea objeto del tipo MenuBar
		self.menu_bar.append(self.menu_item_file)
		self.vBox.pack_start(self.menu_bar,gtk.FALSE,gtk.FALSE,0) # empaquetar la barra en vBox

		# insertar items al item "archivo"
		self.menu = gtk.Menu()

		self.menu_item = gtk.MenuItem("Abrir _archivo...")
		self.menu.append(self.menu_item)
		self.menu_item.connect("activate",self.open_file)
		self.menu_item_file.set_submenu(self.menu)
		
		self.menu_item = gtk.MenuItem("_Guardar")
		self.menu.append(self.menu_item)
		self.menu_item.connect("activate",self.save_file)

		self.menu_item = gtk.MenuItem("_Cerrar")
		self.menu.append(self.menu_item)
		self.menu_item.connect("activate",self.close)
		
		self.menu_separator = gtk.SeparatorMenuItem() # crear un separador para un menu
		self.menu.append(self.menu_separator)         # insertar separador en el menu

		self.menu_item = gtk.MenuItem("_Salir")
		self.menu.append(self.menu_item)
		self.menu_item.connect("activate",self.delete_event)
		
		# crear, empaquetar en vBox una hBox para los botones (barra superior)
		self.hBox_botones = gtk.HBox(gtk.FALSE,0)	# crear caja Horizontal para botones
		self.vBox.pack_start(self.hBox_botones,gtk.FALSE,gtk.FALSE,0)	#meter caja de botones a vBox

		# crear, empaquetar en hBox_botones (barra superior) un boton con etiqueta "run",
		# conectar señal "clicked" al método run
		self.compile_button = gtk.Button("run")	# crear boton con etiqueta "run"
		self.hBox_botones.pack_start(self.compile_button,gtk.FALSE,gtk.FALSE,0)	# meter boton en hBox
		self.compile_button.connect("clicked",self.run)	#conectar la señal clicked al método run

		# crear, empaquetar en hBox_botones (barra superior) un boton con etiqueta "examinar" en el dialogo
		self.file_chooser_button = gtk.Button("Examinar")
		self.file_chooser_button.connect("clicked",self.open_file)
		self.hBox_botones.pack_end(self.file_chooser_button,gtk.FALSE,gtk.FALSE,0)	# meter boton en hbox
		
		# crear un buffer para el TextView (text_area)
		self.text_buffer = gtk.TextBuffer()
		
		# crear, empaquetar eh vBox un area de texto (gtk.TextView)
		self.text_area = gtk.TextView(self.text_buffer)

		# añadir scroll al textView (text_area)
		self.scroll_text = gtk.ScrolledWindow()
		self.scroll_text.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.scroll_text.add(self.text_area)
		# se insertó el area de edición de texto a una ventana con scroll, por lo que no se empaqueta en una Vbox,
		# se empaqueta la ventana con scroll en la Vbox (la misma ventana contiene el area de edición de texto) -> por si no lo leíste antes
		self.vBox.pack_start(self.scroll_text)

		# mostrar todos los elementos de la ventana inclusive.
		self.window.show_all()
		
		#crear diccionario al crear la ventana
		self.tabop = Tabop()
		#crear un contador de localidades al crear ventana
		self.contloc = Contloc()

	def open_file(self,widget,data=None): # método llamado desde el menu "archivo -> Abrir archivo..."
		print "opening file..."
		dialog = gtk.FileChooserDialog("Examinar",self.window,gtk.FILE_CHOOSER_ACTION_OPEN,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
		filter = gtk.FileFilter() # para crear el filtro de archivo en la ventana de dialogo
		filter.set_name("Archivo Ensamblador (*.asm)")
		filter.add_pattern("*.asm")
		filter.add_mime_type("text/txt")
		dialog.add_filter(filter)
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
		    self.namefile = dialog.get_filename()
		    self.file = open(self.namefile,'r+')
		    self.text_in_buffer = self.file.read()
		    self.text_buffer.set_text(self.text_in_buffer)
		    print self.text_buffer.get_line_count(), 'lineas leídas'
		    self.file.close()
		    print dialog.get_filename(), 'selected'
		elif response == gtk.RESPONSE_CANCEL:
		    print 'No file selected...'
		dialog.destroy()
		
		
	def save_file(self,widget,data=None):
		
		# se crean los iteradores para marcar el inicio y final del buffer, para guardar el archivo
		file_start = self.text_buffer.get_start_iter()
		file_end   = self.text_buffer.get_end_iter()
		
		try:
			self.file = open(self.namefile,'w+')
			self.file.write(self.text_buffer.get_text(file_start,file_end))
			self.file.close()
		except AttributeError:
			print "saving a new file"
			dialog = gtk.FileChooserDialog("Guardar como...",self.window,
										    gtk.FILE_CHOOSER_ACTION_SAVE,
										    buttons= (gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
			filter = gtk.FileFilter()
			filter.set_name("Archivo Ensamblador (*.asm)")
			filter.add_pattern("*.asm")
			filter.add_mime_type("text/txt")
			dialog.add_filter(filter)
			response = dialog.run()
			if response == gtk.RESPONSE_OK:
				self.namefile = dialog.get_filename()
				# si al nombrar archivo el usuario no colocó extensión *.asm se le añade
				if self.namefile.find(".asm") == -1:
					self.namefile+=".asm"
				self.file = open(self.namefile,'w+')
				self.file.write(self.text_buffer.get_text(file_start,file_end))
				self.file.close()
			elif response == gtk.RESPONSE_CANCEL:
				print "aborting save..."
			dialog.destroy()
			# se guardaron cambios y la bandera de modificación se apaga
			self.text_buffer.set_modified(False)
			

	def close(self,widget,data=None): # método llamado desde el menu "archivo -> cerrar"
		print "Ctrl + W"
		file_start = self.text_buffer.get_start_iter()
		file_end   = self.text_buffer.get_end_iter()
		cont = self.text_buffer.get_text(file_start,file_end)
		if self.text_buffer.get_modified():
			message = "El Archivo ha sido modificado\n¿Desea guardar cambios?"
			result_dialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
											  gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, message)
			result_dialog.set_title("Cerrar...")
			#result_dialog.show_all()
			response = result_dialog.run()	# se lanza dialogo para salvar cambios
			if response == gtk.RESPONSE_YES:
				self.save_file(None)
		gtk.main_quit()

	def delete_event(self,widget,data=None): # método llamado a presionar boton cerrar
		print "El programa se cerrará..."
		gtk.main_quit()

	def resultDialog(self,messageArray):
		
		result_dialog = gtk.Dialog("Resultados de compilación",self.window,buttons=(gtk.STOCK_OK, gtk.RESPONSE_OK))
		result_dialog.set_size_request(300, 300)
		box = result_dialog.get_content_area()
		scrolled_win = gtk.ScrolledWindow()
		scrolled_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
		string = ""
		for i in messageArray:
			string = string+i+"\n\n"
		label = gtk.Label(string)
		label.set_selectable(True)
		scrolled_win.add_with_viewport(label)
		box.add(scrolled_win)
		result_dialog.show_all()
		response = result_dialog.run()
		if response == gtk.RESPONSE_OK:
			result_dialog.destroy()

	def run(self,widget,data=None):
		objectLine = []		# se crea un arreglo para los objetos "linea"
		print "Se presionó el botón run, aquí comienza la compilación del ensamblador"
		file_start = self.text_buffer.get_start_iter()
		file_end   = self.text_buffer.get_end_iter()
		self.code_in_buffer = self.text_buffer.get_text(file_start,file_end)
		if self.code_in_buffer=="":
			return
		line = self.code_in_buffer.split('\n')
		archivolist = str(self.namefile)
		archivolist = archivolist[:-4] #quito extensión .asm
		self.tbs = open(archivolist+".tbs",'w+')	#creat archivo *.tbs (tabla de símbolos)
		j = 0	#contador para aumentar el número de la línea a escribir en *.lst
		
		# se crea una lista de objetos tipo Linea
		for i in range(len(line)):
			objectLine.append(Linea(line[i],i+1))
		# creo un array para los mensajes de los objetos linea analizados
		messageArray = []
		lstArray = [] #creo lista para escribir en el archivo *.lst
		post_processing = [] # lista de lineas que tienen una etiqueta como operando, se procesan después del *.tbs
		dict_tbs = {}	#diccionario con las etiquetas que existen en el *.tbs
		n = 0 #número a sumar en el contloc
		for i in objectLine:
			if i.toString() != None:
				#envío el tabop para que toString revise si existe la instrucción
				messageArray.append(i.toString(self.tabop))
				#se define el inicio del contador de localidades
				self.contloc.add(n)
				if i.get_opcode() == "ORG":
					opr = i.get_operator()
					val = self.get_dec(opr)
					self.contloc.set_contloc(val)
					i.set_val_contloc(self.contloc.get_format())
					messageArray[-1]+="\nContloc: "+self.contloc.get_format()
					lstArray.append(self.contloc.get_format()+"\t\t\t"+line[j]+"\n")
					n = 0
				# if(es un código de operación)
				if self.tabop.tabop.has_key(i.get_opcode()):
					n=i.get_totalbytes()
					i.set_val_contloc(self.contloc.get_format())
					messageArray[-1]+="\nContloc: "+self.contloc.get_format()
					if i.get_operator()!=None:
						# si el operando es una etiqueta, se añade a la cola de post-procesamiento (*.tbs stuffs :v)
						if i.check_label(cad = i.get_operator()):
							#linea -1 para saber en que indice de lstArray meterlo después (inicia en 0)					
							post_processing.append([i,i.line_number-1,self.contloc.get_format()])
						else: # no es una etiqueta, entonces se añade sin pex :v
							lstArray.append(self.contloc.get_format()+"\t"+i.get_machinecode(self.tabop)+"\t\t"+line[j]+"\n")
					else:
						lstArray.append(self.contloc.get_format()+"\t"+i.get_machinecode(self.tabop)+"\t\t"+line[j]+"\n")
					if i.get_label()!=None:
						self.tbs.write(i.get_label()+"\t"+self.contloc.get_format()+"\n")
						dict_tbs[i.get_label()] = self.contloc.get_format()

				if i.get_opcode() == "EQU":
					opr = i.get_operator()
					val = self.get_dec(opr)
					n = 0
					i.set_val_contloc(self.contloc.fotmatEqu(val))
					messageArray[-1]+="\nContloc: "+self.contloc.fotmatEqu(val)
					lstArray.append(self.contloc.fotmatEqu(val)+"\t\t\t"+line[j]+"\n")
					self.tbs.write(i.get_label()+"\t"+self.contloc.fotmatEqu(val)+"\n")
					dict_tbs[i.get_label()] = self.contloc.fotmatEqu(val)
				if i.get_opcode() == "END":
					i.set_val_contloc(self.contloc.get_format())
					messageArray[-1]+="\nContloc: "+self.contloc.get_format()
					lstArray.append(self.contloc.get_format()+"\t\t\t"+line[j]+"\n")
					if i.get_label() != None:
						self.tbs.write(str(i.get_label())+"\t"+self.contloc.get_format()+"\n")
						dict_tbs[i.get_label()] = self.contloc.get_format()
					break; # si es un END, termina de analizar el código
				j+=1		# se aumenta la linea a escribir en el *.lst
			else:
				j+=1		# se aumenta la linea a escribir en el *.lst
				continue
		#cierro archivos creados al correr el código
		self.tbs.close()
		
		#se procesan las lineas con etiquetas (que están en post_processing
		for i in post_processing:
			if dict_tbs.has_key (i[0].get_operator()):
				lstArray.insert(i[1], (i[2]+"\t"+i[0].get_machinecode(self.tabop,dict_tbs)+"\t\t"+line[i[1]]+"\n"))
			else:
				lstArray.insert(i[1],"Algo raro pasó, la etiqueta no está en el tbs\n")
		self.lst = open(archivolist+".lst",'w+')	#crear archivo *.lst
		for line in lstArray:
			self.lst.write(line)
		self.lst.close()
		
		# se llama método para mostrar en un Dialogo los resultados
		self.resultDialog(messageArray)
			
	def get_dec(self,opr):
		"""método para obtener valor decimal de un ORG"""
		if   opr[0]=='$':
			opr    = opr[1:]		# se le quita el '$'
			valdec = int(opr,16)	# str(hex) -> dec
		elif opr[0]=='%':
			opr    = opr[1:]		# se le quita el '%'
			valdec = int(opr,2)		# str(bin) -> dec
		elif opr[0]=='@':
			opr	   = opr[1:]		# se le quita el '@'
			valdec = int(opr,8)		# str(oct) -> dec
		else:	#se infiere que es decimal
			valdec = int(opr,10)	# str(dec) -> dec
		return valdec			
			

	def main(self):
		gtk.main()

if __name__ == "__main__":
	ventana = Ventana("Taller de programación de sistemas")	# crear un objeto ventana con el titulo fijo
	ventana.main()		# llamar al iniciar la ventana
