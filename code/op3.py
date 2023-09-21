import cv2
import face_recognition
import os

cam = cv2.VideoCapture('http://192.168.1.3:8080/video')

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