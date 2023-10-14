from firebase_admin import credentials, initialize_app, db, storage
from PIL import Image
import requests
from io import BytesIO
import os
from faker import Faker

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


# Función para generar datos de prueba con datos de personas reales
def generate_real_user():
    # URL de la API que proporciona datos de personas reales
    api_url = "https://randomuser.me/api/"

    # Realiza una solicitud a la API
    response = requests.get(api_url)

    # Parsea la respuesta JSON
    user_data = response.json()['results'][0]

    return {
        'name': f"{user_data['name']['first']} {user_data['name']['last']}",
        'id': str(fake.random_int(min=10000000, max=309999999)),  # ID entre 8 y 9 dígitos
        'cargo': user_data['location']['city'],
        'mail': user_data['email'],
        'antiguedad': fake.random_int(min=10, max=50),
        'hora_conexion': fake.date_time_this_decade().strftime("%Y-%m-%d %H:%M:%S"),
        'profile_image_url': user_data['picture']['large']
    }


# Función para descargar y guardar una imagen
def save_profile_image(image_url, local_path):
    image_data = requests.get(image_url).content
    image = Image.open(BytesIO(image_data))
    image.save(local_path)


# Directorio para almacenar imágenes localmente
local_images_folder = "local_images"
os.makedirs(local_images_folder, exist_ok=True)

# Configura Faker para generar datos en español
fake = Faker('es_ES')

# Generar y subir datos de prueba
for _ in range(250):
    user_data = generate_real_user()

    # Subir datos a la base de datos
    ref.child(user_data['id']).set(user_data)

    # Generar y subir imágenes a Firebase Storage-
    image_path = os.path.join(local_images_folder, f"{user_data['id']}.jpg")
    save_profile_image(user_data['profile_image_url'], image_path)

    blob_name = f"caras/{user_data['id']}.jpg"
    blob = bucket.blob(blob_name)

    try:
        blob.upload_from_filename(image_path)
        print(f"Imagen {blob_name} subida correctamente a Firebase Storage.")
    except Exception as e:
        print(f"Error al subir la imagen a Firebase Storage: {e}")

print("Proceso completo.")
