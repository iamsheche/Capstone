import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("servicesAK.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://capstone-308fc-default-rtdb.firebaseio.com/"})


ref = db.reference('Empleados')

data =  { "204732671":
    {

    "name": "Sergio Aguilar",
    "email": "saguilaro@uft.edu",
    "cargo": "Estudiante",
    "antiguedad": "5",
    "total_asistencias": "0",
    "ultima:asistencia": "2023-10-05 12:00:00",
}}

for key, value in data.items():
    ref.child(key).set(value)