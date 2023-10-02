from firebase import firebase

firebase = firebase.FirebaseApplication("https://capstone-308fc-default-rtdb.firebaseio.com",None)


datos = {

    "Name": "Juan",
    "ID": "123",
    "Cargo": "Developer",
    "Mail": "juan@gmail.com",
    "Antiguedad": "2"


}


resultado = firebase.post('/Capstone/usuarios', datos)