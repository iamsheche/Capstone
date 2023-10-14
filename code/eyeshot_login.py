import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime

cred = credentials.Certificate("servicesAK.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://capstone-308fc-default-rtdb.firebaseio.com/",
    "storageBucket": "capstone-308fc.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('../images/background.png')

# Importing the mode images into a list
folderModePath = '../recursos/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

# Load the encoding file
print("Loading Encode File ...")
file = open('ArchivoCodificado.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print(studentIds)
print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
imgEmpleado = []





while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:

        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            print("matches", matches)
            print("faceDis", faceDis)
            matchIndex = np.argmin(faceDis)


            if matches[matchIndex]:
                print("Rostro detectado")
                print(studentIds[matchIndex])
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground= cvzone.cornerRect(imgBackground,bbox, rt=0)
                id = studentIds[matchIndex]
                if counter==0:
                    cvzone.putTextRect(imgBackground, "Cargando", (275, 400))
                    cv2.imshow("Registro de Asistencia", imgBackground)
                    cv2.waitKey(1)

                    counter=1
                    modeType=1

        if counter!=0:
            if counter==1:
                empInfo = db.reference(f'Users/{id}').get()
                print(empInfo)

                blob = bucket.get_blob(f"caras/{id}.jpg")
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgEmpleado = cv2.imdecode(array, cv2.COLOR_BGRA2RGB)

                # Actualizar asistencias
                datetimeOb = datetime.strptime(empInfo['last_attendance_time'], '%Y-%m-%d %H:%M:%S')
                tiempo = (datetime.now()- datetimeOb).total_seconds()

                if tiempo>30:

                    ref = db.reference(f'Users/{id}')
                    empInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(empInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:

                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType!=3:


                if 10<counter<20:
                    modeType=2
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter<=10:


                    cv2.putText(imgBackground, str(empInfo['name']), (861, 122), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1),
                    cv2.putText(imgBackground, str(id), (966, 488), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1),
                    cv2.putText(imgBackground, str(empInfo['cargo']), (990, 564), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1),
                    cv2.putText(imgBackground, str(empInfo['mail']), (910, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)

                    imgEmpleado_resized = cv2.resize(imgEmpleado, (216, 216))
                    imgBackground[175:175 + 216, 909:909 + 216] = imgEmpleado_resized

                counter += 1

            else:
                modeType = 0
                counter = 0

        #if counter>=20:
         #   counter=0
          #  modeType=0
           # studentInfo=[]
            #imgEmpleado=[]


    cv2.imshow("Registro de Asistencia", imgBackground)
    cv2.waitKey(1)








"""
while True:
    success, img = cap.read()
    if not success or img is None:
        print("Error al leer desde la cámara.")
        continue

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:
            if counter == 1:
                # Get the Data
                studentInfo = db.reference(f'Users/{id}').get()
                datetimeObject = datetime.strptime(studentInfo['hora_conexion'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:
                    ref = db.reference(f'Users/{id}')
                   # studentInfo['total_attendance'] += 1
                    #ref.child('total_attendance').set(studentInfo['total_attendance'])
                    #ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:
                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(imgBackground, str(studentInfo['antiguedad']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['cargo']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['mail']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['name']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['hora_conexion']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    # Convertir la lista a una matriz NumPy
                    imgStudent = np.array(imgStudent)

                    print("imgStudent shape:", imgStudent.shape)
                    print("imgBackground region shape:", imgBackground[175:175 + 216, 909:909 + 216].shape)

                    imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0

    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)
"""