#!/usr/bin/env python3.6

"""
Este programa solo extrae los atributos de cada elemento,
y además da por hecho que cada elemento está alojado en una única línea
Usage: 
	./xml2json.py  inputFile outputFile
	./xml2json.py /opt/Posts.xml /opt/Posts.json

"""
import sys
import json
import tqdm # Solo para ver como avanza
from time import time
from hurry.filesize import size
from os import path, remove
from lxml import etree
# Se reciben por parametro el fichero de entrada(xml) y el de salida(json)
_input = sys.argv[1]
_output = sys.argv[2]
count=0 # Simplemente para que se vea por consola que esta trabajando
start = time()

# Se comprueba si el fichero de entrada existe
if path.isfile(_input) == False:
	print('El fichero no existe')
	sys.exit() # Si no existe se interrumpe la ejecución

# Se comprueba si el fichero de salida existe
# Si existe, se le pregunta al usuario si desea sobreescribirlo
if path.isfile(_output):
	isOverwrite = input('El fichero {} ya existe, ¿Desea sobreescribirlo?[Y/n]: '.format(_output))
	if isOverwrite.lower() == 'y':
		remove(_output)

# Metodo para guardar los atributos en json
def save_json(atributos, count):
	# Se convierten los atributos (etree.Attrib) a tipo diccionario
	dict_json = dict()
	for k,v in atributos.items():
		dict_json[k]=v
	# Se convierte el diccionario en un .json y se le añade un salto de línea final
	str_json = json.dumps(dict_json) + '\n'
	# Se abre el fichero en modo 'append' y se escribe el .json
	with open(_output, 'a') as f:
		f.write(str_json)

# Se abre el fichero de entrada
with open(_input, 'r') as f:
	#Creamos un progress bar donde el total de proceso es el tamaño del fichero
	progress = tqdm.tqdm(unit='bytes', leave=False,total=path.getsize(_input), \
		bar_format="{l_bar}{bar}| {percentage:3.0f}% [{elapsed}<{remaining}, {rate_fmt}{postfix}]")
	# Se va leyendo línea a línea
	for line in f:
		# Se va actualizando la barra con el tamaño en bytes de la linea leida.
		progress.update(sys.getsizeof(line)) 
		try:
			node = etree.fromstring(line) 	# Se convierte el texto en un arbol
			atributos = node.attrib 		# Se obtinen los atributos
			if atributos.has_key('Id'):		# Si pertenecen a nuestro tipo se procesan
				save_json(atributos, count)
			count+=1
		except Exception as f: # Algunas líneas como la descripción de formato dan error
			print(line)
	progress.close()


# Se calcula el tiempo completo de la operación
end = (time() - start)
# Se transofrma el tiempo en una unidad legible
m, s = divmod(end, 60)
# Se obtiene el tamaño de los ficheros de entrada y salida
# y se convierten a un formato legible
inputSize = size(path.getsize(_input))
outputSize = size(path.getsize(_output))

# Se informa al usuario del tiempo tardado,
# y los tamaños de los archivos de entrada y salida
print('Se han procesado: {} y {} lineas '.format(inputSize, count))
print('Archivo resultante: {}'.format(outputSize))
print('Operación realizada en: {}m {}s'.format(m,s))
