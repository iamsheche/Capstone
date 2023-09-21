import cv2
import numpy as np
import face_recognition as fr
import os
import random
from datetime import datetime


ruta = "images/"

images = []
clases = []
lista = os.listdir(ruta)
#print(lista)

var1 = 100

# Recorrer directorio de imágenes
for x in lista:

    img = cv2.imread(f'{ruta}/{x}')
    images.append(img)
    clases.append(os.path.splitext(x)[0])

print(clases)



# Leer rostros

def face(images):
    lista2 = []

    for y in images:

        y = cv2.cvtColor(y,cv2.COLOR_BGR2RGB)
        cod = fr.face_encodings(y)[0]
        lista2.append(cod)
    return lista2



app = face(images)

cam = cv2.VideoCapture('http://192.168.1.3:8080/video')

while True:
    ret, frame = cam.read()


    
    if not ret:
        print("No se pudo encontrar la cámara")
        break

    frame2 = cv2.resize(frame, (0,0), None, 0.25,0.25)

    rgb = cv2.cvtColor(frame2,cv2.COLOR_BGR2RGB)




    caras = fr.face_locations(rgb)

    facescod = fr.face_encodings(rgb,caras)

    for x,y in zip (facescod,caras):
        comp = fr.compare_faces(face, facescod)

        similutd = fr.face_distance(face, facescod)

        minimo = np.argmin(similutd)

        if comp[minimo]:
            name = clases[minimo].upper()
            print(name)
            yi,xf,yf,xi = faceloc

            yi,xf,yf,xi = yi*4,xf*4,yf*4,xi*4

            indice = comp.index(True)

            if var1 != indice:
                r = random.randrange(0,255,50)
                g = random.randrange(0,255,50)
                b = random.randrange(0,255,50)

                var1 = indice

            if var1 == indice:

                cv2.rectangle(frame, (xi,yi), (xf,yf), (r,g,b),3)
                cv2.rectangle(frame, (xi,yi-35), (xf,yf), (r,g,b), cv2.FILLED)
                cv2.putText(frame, name,( xi+6, yf-6), cv2.FONT_HERSHEY_SIMPLEX,1 , (255,255,255),2)
        
    




                

                

    cv2.imshow("Eyeshot", frame)        



    off = cv2.waitKey(1)
    if off == 27:
        break


cam.release()
cv2.destroyAllWindows()


