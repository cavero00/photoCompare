# photoCompare
Es un codigo que agrupa imagenes por tamaño y las compara para detectar duplicados. Las imagenes duplicadas las mueve a un directorio llamado "delete". Las imagenes se deben encontrar en la misma ruta para poder acceder a ellas.


# Instalacion
Para instalar el paquete se recomiendo usar un entorno virtual de python e intalar allí las dependencias necesarias.
Para poder instalar las dependencias hay que modificar el archivo "pyvenv.cfg" y poner "include-system-site-packages" a true

## Dependencias
- pip install opencv-python
- pip install numpy
- pip install PySimpleGUI

## Generar ejecutable
Para generar el ejecutable hay que instalar el paquete: 
- pip install pyinstaller

Una vez instalado seteamos la variable de entorno (es posible que no haga falta):
- set PATH=%PATH%;%VIRTUAL_ENV%\Scripts

Se genera un archivo ".spec"
- python -m PyInstaller --name=PhotoCompare --onefile photoCompare.py

Se añaden las dependencias necesarias en el archivo ".spec" en el campo:
- hiddenimports=[]

Se genera el ejecutable con:
- python -m PyInstaller PhotoCompare.spec

El ejecutable se encuentra en el directorio dist\
