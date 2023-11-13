import os
import pickle
import numpy as np
import cv2
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime
import dlib

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

# Utilizamos el detector de caras HOG de dlib
face_detector = dlib.get_frontal_face_detector()

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_detector(imgS)
    encodeCurFrame = [dlib.face_encodings(imgS, faceRect)[0] for faceRect in faceCurFrame]

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:

        for encodeFace, faceRect in zip(encodeCurFrame, faceCurFrame):
            matches = [np.linalg.norm(encodeFace - known_face) < 0.6 for known_face in encodeListKnown]

            if any(matches):
                matchIndex = matches.index(True)
                y1, x2, y2, x1 = faceRect.top(), faceRect.right(), faceRect.bottom(), faceRect.left()
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Cargando", (275, 400))
                    cv2.imshow("Registro de Asistencia", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:
            if counter == 1:
                empInfo = db.reference(f'Users/{id}').get()
                print(empInfo)

                blob = bucket.get_blob(f"caras/{id}.jpg")
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgEmpleado = cv2.imdecode(array, cv2.COLOR_BGRA2RGB)

                datetimeOb = datetime.strptime(empInfo['last_attendance_time'], '%Y-%m-%d %H:%M:%S')
                tiempo = (datetime.now() - datetimeOb).total_seconds()

                if tiempo > 30:
                    ref = db.reference(f'Users/{id}')
                    empInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(empInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:
                if 10 < counter < 20:
                    modeType = 2
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
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

    cv2.imshow("Registro de Asistencia", imgBackground)
    cv2.waitKey(1)
