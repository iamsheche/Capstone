from firebase_admin import credentials, initialize_app, db, storage
from PIL import Image
import os
from io import BytesIO
from faker import Faker
import requests

# Configuración de Firebase
cred = credentials.Certificate("servicesAK.json")
initialize_app(cred, {
    "databaseURL": "https://capstone-308fc-default-rtdb.firebaseio.com/",
    "storageBucket": "capstone-308fc.appspot.com"
})

# Referencia a la base de datos
ref = db.reference('Users')

# Referencia al bucket de Firebase Storage
bucket = storage.bucket()

# Configura Faker para generar datos en español
fake = Faker('es_ES')

# Función para generar datos de prueba con datos de personas reales
def generate_real_user():
    return {
        'name': fake.name(),
        #'id': str(fake.random_int(min=10000000, max=999999999)),  # ID entre 8 y 9 dígitos
        'cargo': fake.job(),
        'mail': fake.email(),
        'antiguedad': fake.random_int(min=1, max=10),
        'last_attendance_time': fake.date_time_this_decade().strftime("%Y-%m-%d %H:%M:%S"),
        'total_attendance': fake.random_int(min=1, max=10000),
    }

# Función para descargar y guardar una imagen redimensionada
def save_profile_image(image_url, local_path, size=(500, 500)):
    response = requests.get(image_url)

    if response.status_code == 200:
        image_data = response.content
        image = Image.open(BytesIO(image_data))

        # Verificar dimensiones de la imagen
        if image.width > 0 and image.height > 0:
            # Redimensionar la imagen
            image.thumbnail(size)

            # Convertir la imagen a modo RGB antes de guardarla
            image = image.convert('RGB')

            image.save(local_path)
        else:
            print(f"La imagen descargada desde {image_url} tiene dimensiones no válidas.")
    else:
        print(f"Error al descargar la imagen desde {image_url}. Código de estado: {response.status_code}")




# Directorio para almacenar imágenes localmente
local_images_folder = "local_images"
os.makedirs(local_images_folder, exist_ok=True)

# Generar y subir datos de prueba
for _ in range(1800):

    id= str(fake.random_int(min=10000000, max=999999999))
    user_data = generate_real_user()

    # Subir datos a la base de datos
    ref.child(id).set(user_data)

    # Generar y subir imágenes a Firebase Storage
    image_path = os.path.join(local_images_folder, f"{id}.jpg")
    save_profile_image(fake.image_url(), image_path)

    blob_name = f"caras/{id}.jpg"
    blob = bucket.blob(blob_name)

    try:
        blob.upload_from_filename(image_path)
        print(f"Imagen {blob_name} subida correctamente a Firebase Storage.")
    except Exception as e:
        print(f"Error al subir la imagen a Firebase Storage: {e}")

print("Proceso completo.")






############################################################################################################



# OPCIÓN B) ROSTROS HUMANOS DE UNSPLASH ( NO permite muchos)