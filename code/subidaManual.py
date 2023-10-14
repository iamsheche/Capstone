import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("servicesAK.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://capstone-308fc-default-rtdb.firebaseio.com/",
    "storageBucket": "capstone-308fc.appspot.com"
})

ref = db.reference('Users')

data = {
    "132844186":
        {
            "name": "Israel Naranjo",
            "cargo": "Docente",
            "antiguedad": 12,
            "mail": "is.naranjo@duocuc.cl",
            "total_attendance": 44,
            "last_attendance_time": "2023-10-11 00:54:34"
        },
    "127774943":
        {
            "name": "Italo Bonet",
            "cargo": "Docente",
            "antiguedad": 5,
            "mail": "i.bonet@duocuc.cl",
            "total_attendance": 4,
            "last_attendance_time": "2023-07-11 00:54:34"
        },
    "90177990":
        {
            "name": "Guillermo Pinto",
            "cargo": "Docente",
            "antiguedad": 10,
            "mail": "gu.pintof@duocuc.cl",
            "total_attendance": 40,
            "last_attendance_time": "2023-10-13 00:54:34"
        },
    "135390496":
        {
            "name": "Sergio Jadue",
            "cargo": "Ladrón",
            "antiguedad": 45,
            "mail": "jadue@anfp.cl",
            "total_attendance": 1,
            "last_attendance_time": "2015-10-13 00:54:34"
        },
    "190805018":
        {
            "name": "Eduardo Vidal",
            "cargo": "Estudiante",
            "antiguedad": 4,
            "mail": "ed.vidalh@gmail.com",
            "total_attendance": 350,
            "last_attendance_time": "2023-10-13 00:54:34"
        },

"204732671":
        {
            "name": "Sergio Aguilar",
            "cargo": "Estudiante",
            "antiguedad": 5,
            "mail": "saguilaro@uft.edu",
            "total_attendance": 350,
            "last_attendance_time": "2023-10-13 00:54:34"
        }


}

for key, value in data.items():
    ref.child(key).set(value)