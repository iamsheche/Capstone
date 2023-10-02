# Sección de Import

import face_recognition
import numpy as np
import mediapipe as mp
from tkinter import *
import math
from tkinter import Tk, Toplevel, Entry, Button, StringVar, PhotoImage, Label, messagebox
from PIL import Image, ImageTk
import os
import cv2
import imutils
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("capstone-308fc-firebase-adminsdk-zpzei-ba69fbb316.json")

firebase_admin.initialize_app(cred)

db = firestore.client()

def camReg():
    global windows2, count, parpadeo, img_info, step, cap, lblVideo

    if cap is not None and cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Error al leer desde la cámara")
            return

        # Redimensionar
        frame = imutils.resize(frame, width=1280)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frameSave = frameRGB.copy()

        if ret == True:
            # Incorporar malla facial
            resultado = FaceMesh.process(frameRGB)

            # Lista de resultados
            px = []
            py = []
            listaCoordenadas = []
            if resultado.multi_face_landmarks:
                for faceLms in resultado.multi_face_landmarks:
                    mpDraw.draw_landmarks(frame, faceLms, FacemeshObject.FACEMESH_TESSELATION, configDraw , configDraw)

                    # Extraer coordenadas
                    for id, puntos in enumerate(faceLms.landmark):

                        al,an, c = frame.shape
                        x,y = int(puntos.x * an), int(puntos.y * al)
                        px.append(x)
                        py.append(y)
                        listaCoordenadas.append((id, x, y))

                        # 468 Total
                        if len(listaCoordenadas) == 468:
                            # Puntos ojo derecho
                            x1,y1 = listaCoordenadas[145][1:]
                            x2, y2 = listaCoordenadas[159][1:]
                            longitud1 = math.hypot(x1 - x2, y1 - y2)

                            # Puntos ojo izquierdo
                            x3,y3 = listaCoordenadas[374][1:]
                            x4,y4 = listaCoordenadas[386][1:]
                            longitud2  =  math.hypot(x4 - x3, y4 - y3)

                            # Parietal Derecho
                            x5, y5 = listaCoordenadas[139][1:]
                            # Parietal Izquierdo
                            x6, y6 = listaCoordenadas[368][1:]

                            # Ceja derecha
                            x7, y7 = listaCoordenadas[70][1:]
                            # Ceja izquierda
                            x8, y8 = listaCoordenadas[300][1:]


                            # Detección de rostros

                            faces = detector.process(frameRGB)
                            if faces.detections is not None:

                                for face in faces.detections:

                                    #  Cuadricula : ID, CAJA, SCORE

                                    score = face.score
                                    score = score[0]
                                    bbox = face.location_data.relative_bounding_box
                                    if score >confThreshold:

                                        # Conversión coordenadas a píxeles
                                        xi, yi, anc, alt = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                                        xi , yi , anc , alt = int(xi * an), int(yi * al), int(anc * an), int(alt * al)

                                        # Offset en X
                                        offsetan =  (offsetx/100)* anc
                                        xi = int(xi-int(offsetan/2))
                                        anc= int(anc + offsetan)
                                        xf =xi + anc

                                        # Offset en Y
                                        offsetal = (offsety / 100) * alt
                                        yi = int(yi - offsetal)
                                        alt = int(alt + offsetal)
                                        yf = yi + alt


                                        # Control de error

                                        if xi < 0: xi=0
                                        if yi < 0: yi=0
                                        if anc < 0: anc=0
                                        if alt < 0: alt=0

                                        # Verificación

                                        if step == 0:

                                            # Dibujar
                                            cv2.rectangle(frame, (xi, yi, anc, alt), (255, 255, 255), 2)

                                            # IMG Verificacion
                                            als0, ans0, c = img_verificacion.shape
                                            frame[50:50+als0, 50:50+ans0] = img_verificacion

                                            # IMG Mirar Cámara
                                            img_mirar_resized = cv2.resize(img_mirar, (250, 300))
                                            als1, ans1, c = img_mirar_resized.shape

                                            frame[50:50 + als1, 1030:1030 + ans1] = img_mirar_resized

                                            # IMG Parpadedar
                                            img_parpadear_resized = cv2.resize(img_parpadear, (250, 300))

                                            als2, ans2, c = img_parpadear_resized.shape
                                            frame[350:350 + als2, 1030:1030 + ans2] = img_parpadear_resized


                                            # Mirarcentro

                                            if x7 > x5 and x8<x6:
                                                img_check_resized = cv2.resize(img_check, (55, 100))

                                                alch, ansch, c = img_check_resized.shape
                                                frame[145:145 + alch, 1130:1130 + ansch] = img_check_resized

                                                # Conteo parpadeos
                                                if longitud1<=10 and longitud2<=10 and parpadeo== False:
                                                    count += 1
                                                    parpadeo = True

                                                elif longitud1>10 and longitud2>10 and parpadeo==True:

                                                    parpadeo = False
                                                cv2.putText(frame, f'Parpadeo: {count}', (1050, 523), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

                                                if count == 3:
                                                    alch, ansch, c = img_check_resized.shape
                                                    frame[530:530 + alch, 1130:1130 + ansch] = img_check_resized

                                                    # Toma de captura

                                                    if longitud1> 14 and longitud2> 14:
                                                        # Toma de píxeles
                                                        pix = frameSave[yi:yf, xi:xf]

                                                        # Guardar caras


                                                        cv2.imwrite(f'{OutFolderPathCara}/ {input_id}.jpg', pix)

                                                        step=1



                                            else:
                                                count = 0

                                        if step == 1:
                                            cv2.rectangle(frame, (xi, yi, anc, alt), (0, 255, 0), 2)

                                            # IMG Verificacion Exitosa
                                            alli, anli, c = img_exito.shape
                                            frame[50:50 + alli, 50:50 + anli] = img_exito




                                        # Dibujar marco

                                        #cv2.rectangle(frame, (xi, yi, anc, alt), (255, 255, 255), 2)




                            #cv2.circle(frame, (x1, y1), 5, (0, 0, 255), cv2.FILLED)


        # Conversión a vídeo
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)

        # Mostrar vídeo
        lblVideo.configure(image=img)
        lblVideo.image = img
        lblVideo.after(10, camReg)
    else:
        messagebox.showwarning("Error", "No hay cámara")
        if cap is not None:
            cap.release()

def SignUp():
    global EntryName, EntryID, EntryCargo, EntryMail, EntryAntiguedad, cap, lblVideo, windows2, input_id

    # Extraer Nombre, ID, Cargo, Mail y Antiguedad
    input_name = EntryName.get()
    input_id = EntryID.get()
    input_cargo = EntryCargo.get()
    input_mail = EntryMail.get()
    input_antiguedad = EntryAntiguedad.get()

    # Si hay campos vacíos
    if not all([input_name, input_id, input_cargo, input_mail, input_antiguedad]):
        messagebox.showwarning("Campos vacíos", "Los campos no pueden estar vacíos")
    else:
        lista_usuarios = os.listdir(PathUserVerif)
        lista = [x.split('.')[0].split()[-1] for x in lista_usuarios]

        if input_id in lista:
            messagebox.showwarning("ID existente", "El usuario ya está registrado: Verifique ID")
        else:
            datos.extend([input_name, input_id, input_cargo, input_mail, input_antiguedad])
            messagebox.showinfo("Registro completado", "El registro se ha completado con éxito")

            # Exportar datos
            with open(PathUserVerif + f"{input_name} {input_id}.txt", "w") as exp:
                exp.write(", ".join(datos))

            # Reset de formulario
            EntryName.set('')
            EntryID.set('')
            EntryCargo.set('')
            EntryMail.set('')
            EntryAntiguedad.set('')

            # Ventana 2
            windows2 = Toplevel(windows)
            windows2.title("EyeShot Sign Up AI")
            windows2.geometry("1280x720")

            # Vídeo
            global lblVideo
            lblVideo = Label(windows2)
            lblVideo.place(x=0, y=0, relwidth=1, relheight=1)

            # Captura
            global cap
            cap = cv2.VideoCapture(0)
            cap.set(3, 1280)
            cap.set(4, 720)
            camReg()




script_dir = os.path.dirname(os.path.abspath(__file__))
# Path
OutFolderPathUser = os.path.join(script_dir, "Capstone/DB/usuarios")
PathUserVerif = os.path.join(script_dir, "Capstone/DB/usuarios/")
OutFolderPathCara = os.path.join(script_dir, "Capstone/DB/caras")


# Lectura de imágenes

img_verificacion = cv2.imread(os.path.join(script_dir, "Capstone/images/VERIFICACION.png"))
img_mirar = cv2.imread(os.path.join(script_dir, "Capstone/images/MIRARCAMARA.png"))
img_parpadear = cv2.imread(os.path.join(script_dir, "Capstone/images/PARPADEAR.png"))
img_check = cv2.imread(os.path.join(script_dir, "Capstone/images/check.png"))
img_exito = cv2.imread(os.path.join(script_dir, "Capstone/images/VERIFICACIONEXITOSA.png"))
# Creación de variables

count = 0
step = 0
parpadeo = False
muestra = 0

# Margen de reconocimiento facial

offsety = 30
offsetx = 20

# Precisión mínima
confThreshold = 0.5

# Herramienta de dibujo MP
mpDraw = mp.solutions.drawing_utils
configDraw = mpDraw.DrawingSpec(thickness=2, circle_radius=2)

# Malla Facial

FacemeshObject = mp.solutions.face_mesh
FaceMesh =  FacemeshObject.FaceMesh(max_num_faces=1)


# Detector de  rostros

FaceObject = mp.solutions.face_detection
detector = FaceObject.FaceDetection(min_detection_confidence=0.5, model_selection=1)

# Creación de listas
datos = []

# GUI
windows = Tk()
windows.title("EyeShot Sign Up")
windows.geometry("1280x720")

# Fondo GUI
fondo = PhotoImage(file=os.path.join(script_dir, "images/EYESHOT SIGN UP TEMPLATE.png"))
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
imagenButton = PhotoImage(file=os.path.join(script_dir, "images/AÑADIR EMPLEADO.png"))
btn = Button(windows, image=imagenButton, text="SignUp", command=SignUp)
btn.place(x=800, y=634, width=250, height=50)

# Abrir ventana
windows.mainloop()


