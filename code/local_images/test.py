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

cred = credentials.Certificate("../servicesAK.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://capstone-308fc-default-rtdb.firebaseio.com/",
    "storageBucket": "capstone-308fc.appspot.com"
})

lista_usuarios = db.reference('Users').get().keys()

lista = [x.split('.')[0].split()[-1] for x in lista_usuarios]


bucket = storage.bucket()  # Obtener referencia al bucket

print(len(lista))

print(len(bucket.list_blobs()))


