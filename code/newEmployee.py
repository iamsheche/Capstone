import cv2
import os

# Directorio principal donde se almacenarán las fotos
base_dir = "captured_faces"

# Crear el directorio principal si no existe
if not os.path.exists(base_dir):
    os.mkdir(base_dir)

# Contador para rastrear el número de fotos tomadas
photo_count = 0

# Configurar la cámara
cam = cv2.VideoCapture('http://192.168.1.6:4747/video')
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = cam.read()

    if not ret:
        print("No se pudo encontrar la cámara")
        break

    # Detección de caras en el fotograma
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Recortar la región de la cara
        face = frame[y:y+h, x:x+w]

        # Crear una carpeta para cada sujeto si no existe
        subject_dir = os.path.join(base_dir, f"subject_{photo_count // 5 + 1}")
        if not os.path.exists(subject_dir):
            os.mkdir(subject_dir)

        # Guardar la foto de la cara en la carpeta correspondiente
        file_name = os.path.join(subject_dir, f"face_{photo_count % 5}.jpg")
        cv2.imwrite(file_name, face)

        # Dibujar un rectángulo alrededor de la cara en el fotograma
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        photo_count += 1

    cv2.imshow("Captura de Caras", frame)

    key = cv2.waitKey(1)
    
    if key == 27 or photo_count >= 100:  # Presiona Esc o toma 100 fotos (10 por cada carpeta) para salir
        break

cam.release()
cv2.destroyAllWindows()
