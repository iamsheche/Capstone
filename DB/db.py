import cv2
import os
import imutils


personName = "Fotos"
dataPath = 'C:\Users\shech\OneDrive\Documentos\GitHub\Capstone'
personPath = dataPath + '/' + personName


##################################################


if not os.path.exists(personPath):
    print('Carpeta Creada: ', personPath)
    os.makedirs(personPath)

# Conexión con cámara

cam = cv2.videocapture(0, cv2.CAP_DSHOW)


while True:
    ret,frame = cam.read()
    if not ret:
        print("No se pudo obtener un frame de la cámara")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow ("frame",frame)



    if cv2.waitKey(1)== 27:
        break

cam.release()
cv2.destroyAllWindows()


