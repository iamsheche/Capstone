# Sección de Import

import cv2
import face_recognition
import numpy as np
import mediapipe as mp
import os
from tkinter import *
import imutils
from PIL import Image, ImageTk
import math

"""
def SignUp():
    global InputName, InputID, InputCargo, InputMail, InputAntiguedad, cam, lblVideo, windows2
    # Extraer Nombre, ID, Cargo,Mail y Antiguedad
    InputName, InputID, InputCargo, InputMail, InputAntiguedad = InputName.get(), InputID.get(), InputCargo.get(), InputMail.get(), InputAntiguedad.get()

    # Si hay campos vacíos

    if len(InputName.get()) == 0 or len(InputID.get()) == 0 or len(InputCargo.get()) == 0 or len(InputMail.get()) == 0 or len(InputAntiguedad.get()) == 0:
        messagebox.showwarning("Campos vacíos", "Los campos no pueden estar vacíos")

    # Si está completo
    else:
        listaUsuarios = os.listdir(PathUserVerif)
        print(listaUsuarios)




# Path

OutFolderPathUser = "C:/Users/shech/OneDrive/Documentos/GitHub/Capstone/DB/usuarios"
PathUserVerif = "C:/Users/shech/OneDrive/Documentos/GitHub/Capstone/DB/usuarios/"


OutFolderPathCara = "C:/Users/shech/OneDrive/Documentos/GitHub/Capstone/DB/caras"

# Creación de listas
datos = []


# GUI

windows = Tk()
windows.title("EyeShot Sign Up")
windows.geometry("1280x720")


# Fondo GUI

fondo = PhotoImage(file = "C:/Users/shech/OneDrive/Documentos/GitHub/Capstone/images/EYESHOT SIGN UP TEMPLATE.png")

background = Label(windows, image = fondo , text="Sign Up")
background.place(x = 0, y = 0, relwidth = 1, relheight = 1)

# Ingreso de datos

# Nombre de Empleado
InputName = Entry(windows)
InputName.place(x = 160, y = 240, width = 250,height = 30)

# ID empleado
InputID = Entry(windows)
InputID.place(x = 90, y = 332, width = 250,height = 30)

# Cargo empleado
InputCargo = Entry(windows)
InputCargo.place(x = 133, y = 435, width = 250,height = 30)

# Mail empleado
InputMail = Entry(windows)
InputMail.place(x = 115, y = 531, width = 250, height = 30)

# Antiguedad empleado
InputAntiguedad = Entry(windows)
InputAntiguedad.place(x = 205, y = 630, width = 250, height = 30)

# Botón de registro

imagenButton = PhotoImage(file = "C:/Users/shech/OneDrive/Documentos/GitHub/Capstone/images/AÑADIR EMPLEADO.png")
btn = Button(windows, image = imagenButton , text="SignUp", command=SignUp)
btn.place(x = 800, y = 634, width = 250, height = 50)


# Abrir ventana
windows.mainloop()



# PARTE 2 - REGISTRO FACIAL

"""


from tkinter import *
from tkinter import messagebox
import os

def SignUp():
    global EntryName, EntryID, EntryCargo, EntryMail, EntryAntiguedad

    # Extraer Nombre, ID, Cargo, Mail y Antiguedad
    input_name = EntryName.get()
    input_id = EntryID.get()
    input_cargo = EntryCargo.get()
    input_mail = EntryMail.get()
    input_antiguedad = EntryAntiguedad.get()

    # Si hay campos vacíos
    if len(input_name) == 0 or len(input_id) == 0 or len(input_cargo) == 0 or len(input_mail) == 0 or len(input_antiguedad) == 0:
        messagebox.showwarning("Campos vacíos", "Los campos no pueden estar vacíos")

    # Si está completo
    else:

        lista_usuarios = os.listdir(PathUserVerif)
        lista = []
        print(lista)

        for x in lista_usuarios:
            user = x
            user = user.split('.')
            id = user[0].split()




            lista.append(id[-1])

        print(lista)


        if input_id in lista:
            messagebox.showwarning("ID existente", "El usuario ya está registrado: Verifique ID")
        else:
            datos.append(input_name)
            datos.append(input_id)
            datos.append(input_cargo)
            datos.append(input_mail)
            datos.append(input_antiguedad)
            messagebox.showinfo("Registro completado", "El registro se ha completado con éxito")

            # Exportar datos
            exp = open(PathUserVerif + input_name +" "+ input_id + ".txt", "w")
            exp.write(input_name +", ")
            exp.write(input_id + ", ")
            exp.write(input_cargo + ", ")
            exp.write(input_mail + ", ")
            exp.write(input_antiguedad + ", ")
            exp.close()

            # Reset de formulario
            EntryName.set('')
            EntryID.set('')
            EntryCargo.set('')
            EntryMail.set('')
            EntryAntiguedad.set('')








# Path
OutFolderPathUser = "C:/Users/shech/OneDrive/Documentos/GitHub/Capstone/DB/usuarios"
PathUserVerif = "C:/Users/shech/OneDrive/Documentos/GitHub/Capstone/DB/usuarios/"
OutFolderPathCara = "C:/Users/shech/OneDrive/Documentos/GitHub/Capstone/DB/caras"

# Creación de listas
datos = []

# GUI
windows = Tk()
windows.title("EyeShot Sign Up")
windows.geometry("1280x720")

# Fondo GUI
fondo = PhotoImage(file="C:/Users/shech/OneDrive/Documentos/GitHub/Capstone/images/EYESHOT SIGN UP TEMPLATE.png")
background = Label(windows, image=fondo, text="Sign Up")
background.place(x=0, y=0, relwidth=1, relheight=1)

# Ingreso de datos
EntryName = StringVar()
InputName = Entry(windows, textvariable=EntryName)
InputName.place(x=160, y=240, width=250, height=30)

EntryID = StringVar()
InputID = Entry(windows, textvariable=EntryID)
InputID.place(x=90, y=332, width=250, height=30)

EntryCargo = StringVar()
InputCargo = Entry(windows, textvariable=EntryCargo)
InputCargo.place(x=133, y=435, width=250, height=30)

EntryMail = StringVar()
InputMail = Entry(windows, textvariable=EntryMail)
InputMail.place(x=115, y=531, width=250, height=30)

EntryAntiguedad = StringVar()
InputAntiguedad = Entry(windows, textvariable=EntryAntiguedad)
InputAntiguedad.place(x=205, y=630, width=250, height=30)

# Botón de registro
imagenButton = PhotoImage(file="C:/Users/shech/OneDrive/Documentos/GitHub/Capstone/images/AÑADIR EMPLEADO.png")
btn = Button(windows, image=imagenButton, text="SignUp", command=SignUp)
btn.place(x=800, y=634, width=250, height=50)

# Abrir ventana
windows.mainloop()




