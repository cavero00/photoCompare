########################################################################
# Author: Victor Cavero Herranz
#
# Description: Software to detect photos duplicates
#
#
# Nexts steps:
#		- Leer todas las fotos de una ruta determinada.
#		- Clasificar por tamaños las fotos.
#		- Comparar las fotos por tamaño y las que estén
#		  moverlas a una ruta con un nombre especifico.
########################################################################

import cv2
import numpy as np
import os

########################################################################
#                       DEFINICION DE FUNCIONES

# Funcion que compara dos imagenes
# Devuelve un true si son iguales y un false si no lo son
def comparar(im1,im2):
	diferencia = cv2.subtract(im1,im2)

	if not np.any(diferencia):
		return True
	else:
		return False

########################################################################
#                            CLASE IMAGEN
class Imagen:
	def __init__(self, sh,sv,na,p,g):
		self.horizontalSize = sh
		self.verticalSize = sv
		self.name = na
		self.path = p
		self.group = g

	def mostrar(self):
		print("La ruta es: {}, el nombre es: {}, su vertical es: {}, su horizontal es: {} y su grupo es: {}".format(self.path,self.name,self.horizontalSize,self.verticalSize,self.group))


########################################################################
#                           CODIGO PRINCIPAL

# Lista que guardará todas las imagenes
imgs = []
path = "/home/cavero00/Imágenes/ImagesCompare_prueba"
path_delete = path + "/delete/"

# Se leen todas las imagenes del directorio especificado
os.chdir(path);

# De esta forma me devuelve un iterador para recorrer todas las imagenes
obj = os.scandir()
i = 1 # Contador del total de grupos
grupo = 0 # Numeracion del grupo al que pertenece cada imagen
heigth_list = []
width_list = []
for img in obj:
	if img.is_file():
		imgRead = cv2.imread(img.name)
		heigth= imgRead.shape[0]
		width = imgRead.shape[1]

		# Se escoge a que grupo perteneze la imagen, el grupo se determina
		# en funcion del tamaño de la imagen
		if not heigth_list and not width_list:
			heigth_list.append(heigth)
			width_list.append(width)
			grupo = 1
		else:
			# Se comprueba si las dimensiones son iguales
			# a las otras imagenes leidas
			altura = False
			ancho = False
			pos_h = 0
			pos_v = 0
			stop = False
			for h in heigth_list:
				pos_h+=1

				if h != heigth:
					altura = True
				else:
					altura = False
					for w in width_list:
						pos_v+=1

						if w != width:
							ancho = True
						else:
							ancho = False
							stop = True
							break
				if stop == True:
					break

			# Si las dimensiones no cuadran se instrducen en la lista
			# y se aumenta el grupo
			if altura == True or ancho == True:
				heigth_list.append(heigth)
				width_list.append(width)
				i+=1
				grupo = i
			else:
				if pos_h == pos_v:
					grupo = pos_h
				else:
					grupo = -1

		# Se añade la imagen con sus datos a la lista
		imgs.append(Imagen(width,heigth,img.name,img.path,grupo))


obj.close()


# Una vez se ha realizado la agrupacion, se comparan las imagenes por grupos
deletes = []
for i in range(0,len(imgs)):
	for j in range(i+1,len(imgs)):
		print("\n---> Las imagenes analizadas son: {} y {} ".format(imgs[i].name,imgs[j].name))
		if imgs[i].group == imgs[j].group:
			img1 = cv2.imread(imgs[i].name)
			img2 = cv2.imread(imgs[j].name)

			if comparar(img1,img2):
				print("!! Las imagenes son iguales, se mueve la segunda imagen")
				deletes.append(imgs[j].name)

			else:
				print("- Las imagenes son diferentes")
		else:
			print("- Las imagenes son diferentes, no tienen las mismas dimensiones")

# Se eliminan las imagenes duplicadas
for d in deletes:
	os.rename(d,path_delete+d)



