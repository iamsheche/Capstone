import cv2
import face_recognition
import pickle
import numpy as np
import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate("servicesAK.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://capstone-308fc-default-rtdb.firebaseio.com/",
    "storageBucket": "capstone-308fc.appspot.com"
})

bucket = storage.bucket()
carpeta_bucket = "caras"  # Nombre de la carpeta en el bucket

# Lista para almacenar las imágenes y los identificadores
imgList = []
empleadosID = []

# Iterar sobre los objetos en la carpeta del bucket
blobs = bucket.list_blobs(prefix=carpeta_bucket)
for blob in blobs:
    # Descargar la imagen desde el bucket y convertirla a una matriz NumPy
    try:
        datos_imagen = blob.download_as_bytes()
        imagen_np = cv2.imdecode(np.frombuffer(datos_imagen, np.uint8), cv2.IMREAD_COLOR)
        print(f"Decodificación exitosa. Forma de la imagen: {imagen_np.shape}")
    except Exception as e:
        print(f"Error al procesar la imagen {blob.name}: {e}")
        continue  # Saltar a la siguiente iteración si hay un error

    # Extraer el identificador del nombre del objeto (imagen) en el bucket
    id = blob.name.split('/')[-1].split('.')[0]

    # Agregar la imagen y el identificador a las listas
    imgList.append(imagen_np)
    empleadosID.append(id)

def encontrar_codificaciones(images_list):
    encode_list = []

    for img in images_list:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(img)

        if len(face_locations) > 0:
            encode = face_recognition.face_encodings(img, face_locations)[0]
            encode_list.append(encode)
        else:
            print("No se encontraron caras en una imagen. Omitiendo.")

    return encode_list

print("Inicio de la codificación...")
encodeListKnown = encontrar_codificaciones(imgList)
encodeListKnownWithIds = [encodeListKnown, empleadosID]
print("Codificación completa")

# Guardar el archivo con las codificaciones de características faciales
archivo = open("ArchivoCodificado.p", 'wb')
pickle.dump(encodeListKnownWithIds, archivo)
archivo.close()
print("Archivo Guardado")
