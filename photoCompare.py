########################################################################
# Author: Victor Cavero Herranz
#
# Description: Software to detect duplicates images
#
# Dependencies:
#		- OpenCV
#		- tkinter (lo necesesita PySimpleGUI)
#			sudo apt-get install python3-tk
#		- PySimpleGUI
#			pip3 install pysimplegui
#
#
# Nexts steps:
#		- (x) Leer todas las fotos de una ruta determinada.
#		- (x) Clasificar por tamaños las fotos.
#		- (x) Comparar las fotos por tamaño y las que estén
#		  moverlas a una ruta con un nombre especifico.
#		- (x) Comprobar si existe el directorio "delete" y sino 
# 		  crearlo
#		- (x) Crear interfaz grafica
########################################################################

import cv2
import numpy as np
import os

import PySimpleGUI as sg

########################################################################
#                            CLASSES
class Imagen:
	def __init__(self, sh,sv,na,p,g):
		self.horizontalSize = sh
		self.verticalSize = sv
		self.name = na
		self.path = p
		self.group = g

	def show(self):
		print("The paths is: {}, the name is: {}, vertical size is: {}, horizontal size is: {} and her group is: {}".format(self.path,self.name,self.horizontalSize,self.verticalSize,self.group))

########################################################################
#                            FUNCTIONS

# Funcion que compara dos imagenes
# Devuelve un true si son iguales y un false si no lo son
def compare(im1,im2):
	diferencia = cv2.subtract(im1,im2)

	if not np.any(diferencia):
		return True
	else:
		return False

# Funcion que agrupa por dimensiones las imagenes de una ruta
# Devuelve 3 listas, dos con las dimensiones vertical y horizontal
# de cada agrupacion y otra con informacion de cada imagen
def agrupation(path):
	print("### Start the images agrupation ...")

	# Lista que guardará todas las imagenes
	imgs = []
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

			# Se determina a que grupo perteneze la imagen, el grupo se determina
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
						print("\n> WARNING: A problem occurred during the classification of the img: {}\n",format(img.name))
						grupo = -1

			# Se añade la imagen con sus datos a la lista
			imgs.append(Imagen(width,heigth,img.name,img.path,grupo))


	obj.close()
	
	print("### Finish the images agrupation")

	return heigth_list,width_list,imgs

# Funcion que mueve las imagenes duplicadas a un directorio
def deleteImages(imgs,path_delete):
	# Una vez se ha realizado la agrupacion, se comparan las imagenes por grupos
	deletes = []
	for i in range(0,len(imgs)):
		for j in range(i+1,len(imgs)):
			print("\n---> The images to analyze are: {} y {} ".format(imgs[i].name,imgs[j].name))
			if imgs[i].group == imgs[j].group:
				img1 = cv2.imread(imgs[i].name)
				img2 = cv2.imread(imgs[j].name)

				if compare(img1,img2):
					print("!! The images are equal, prepare to move the second image")
					deletes.append(imgs[j].name)

				else:
					print("- The images are different")
			else:
				print("- The images are different, not have the same dimensions")

	# Se eliminan las imagenes duplicadas
	for d in deletes:
		os.rename(d,path_delete+d)
	

########################################################################
#                           MAIN CODE

# Se prepara la interfaz gráfica de inserccion de datos
explanation = "Enter the path where the images are located. The images must be in single folder. The code will compare the images and move the duplicate images to a deletion folder. This deletion folder is named delete"

layout = [
	[sg.Frame(layout=[
		[sg.Text(explanation,size=(int(len(explanation)/4),4),justification='center')]
		],title='Explanation',title_color='black')],
	[sg.Text("Source for images",size=(15,1),justification='right'), sg.InputText(),sg.FolderBrowse()],
	[sg.Submit(),sg.Cancel()]
	]

finalLayout = [[sg.Column(layout,element_justification='c')]]
window = sg.Window("Photo compare",finalLayout)

event, values = window.read()

if event == 'Submit':
	# Se prepara la interfaz grafica para mostrar los logs
	print = sg.Print # Se convierten todos los print en sg.Print

	logs = [
		[sg.Text("Photo compare finish")],
		[sg.Button('Ok')]
		]

	window = sg.Window("Info",logs)

	#time.sleep(1)
	
	# Se genera la ruta de borrado y se procede a comprar las imagenes
	img_path = values[0]
	path_delete = img_path + "/delete/"

	# Se comprueba que el directorio de borrado de las imagenes exista y sino se crea
	if not os.path.exists(path_delete):
		print("\n> WARNING: The directory to delete images not exists, creating the directory\n")
		os.mkdir(path_delete)

	# Se agrupan las imagenes por dimensiones
	heigth_list, width_list, imgs = agrupation(img_path)

	# Se mueven las imagenes
	deleteImages(imgs,path_delete)

	# Se comprueba que el directorio de borrado ed imagenes no este vacio, si lo esta se borra
	if not os.listdir(path_delete):
		print("\n> WARNING: The directory to delete images is empty, deleting the directory\n")
		os.rmdir(path_delete)

	print("\n### Complete delete images ###")
	
	while True:
		event,values = window.read()
		print(event,values)
		if event in (sg.WIN_CLOSED,'Ok'):
			window.close()
			break

if event in (sg.WIN_CLOSED,'Cancel'):
	window.close()

