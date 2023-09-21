""""
# Import de OpenCV / OpenCV library
import cv2
import face_recognition
import os
#from simple_facerec import SimpleFacerec

imagenes =r"C:\Users\shech\OneDrive\Documentos\GitHub\Capstone\images/"
image = face_recognition.load_image_file(imagenes)

files = os.listdir(image)
#lector = SimpleFacerec()
#lector.load_encoding_images("images/chayanne.webp")"""

""""
# Ruta al directorio que contiene las imágenes
directorio_imagenes = 'C:/Users/shech/OneDrive/Documentos/GitHub/Capstone/images'



                        


# Obtener la lista de archivos en el directorio
archivos_imagenes = os.listdir(directorio_imagenes)


cam = cv2.VideoCapture(2)

while True:
    ret, frame = cam.read()
    if not ret:
        print("No se pudo obtener un frame de la cámara")
        break


    key = cv2.waitKey(1)
    if key == 27:
        break


cam.release()
cv2.destroyAllWindows()


"""
"""
# Import de OS / Module OS 
import os

# Directorio de Imágenes / Images directory
images=""
"""


""""""""

########################################################################################################################################################


import cv2
import numpy as np
import face_recognition as fr
import os
import random
from datetime import datetime
