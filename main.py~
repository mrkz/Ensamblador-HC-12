#!/usr/bin/env python
# coding=utf-8
"""Código que inicia la interfaz del proyecto del compilador HC12
   Centro Universitario de Ciencias Exactas e Ingenierías
   Simental Magaña Marcos Eleno Joaquín"""
import sys # se importa clase para importar directorios de códigos

# añado directorios de los demás códigos python necesarios
sys.path.append('./src')
sys.path.append('./GUI')

# se importan las clases de los archivos *.py importados
from src.analizadorDeLineas import Linea	# se importa del archivo analizadorDeLineas.py la clase Linea
from GUI.window import Ventana

if __name__ == "__main__":
	window = Ventana("Taller de programación de sistemas")	# crear un objeto ventana con el titulo fijo
	linea = []	# lista de lineas que rebibiré del area de texto
	window.main()		# llamar al iniciar la ventana
