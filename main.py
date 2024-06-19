import pickle
import numpy as np
import cv2
import os
import cvzone
import face_recognition
import mysql.connector
from datetime import datetime
import sys

# Conexión a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="asistencia"
)

cursor = db.cursor()

print("conexion correcta")

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

if "--resize" in sys.argv:
    cap.set(3, 544)
    cap.set(4, 408)

imgBackground = cv2.imread('Resources/background.png')

# Importamos las imágenes de modos en una lista
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in modePathList]

# Cargar la información de trabajadores desde la base de datos
query = "SELECT id, imagen FROM trabajadores"
cursor.execute(query)
worker_data = cursor.fetchall()
encodeListKnown = []
workerIds = []

for worker_info in worker_data:
    # Obtener el ID del trabajador y la imagen
    id_worker, ruta_imagen = worker_info[0], worker_info[1]

    # Cargar la imagen y obtener la codificación facial
    imgWorker = cv2.imread(ruta_imagen)
    imgWorker = cv2.cvtColor(imgWorker, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(imgWorker)[0]

    # Agregar la codificación y el ID a las listas
    encodeListKnown.append(encode)
    workerIds.append(id_worker)

modeType = 0
counter = 0
id = -1
imgWorker = []
# Cambios para ajustar el tamaño de la ventana
cv2.namedWindow("ASISTENCIA_ALLQOVET", cv2.WINDOW_NORMAL)
cv2.resizeWindow("ASISTENCIA_ALLQOVET", 1000, 600)

while True:
    success, img = cap.read()
    if not success:
        print('Error al leer el fotograma de la cámara.')
        break

    # Voltear horizontalmente la imagen capturada
    img_flipped = cv2.flip(img, 1)

    # Hacer más pequeñas las imágenes
    imgS = cv2.resize(img, None, fx=0.25, fy=0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Utilizamos face_recognition
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    # Superponemos la imagen de la cámara en BG
    imgBackground[162:162 + 480, 55:55 + 640] = img_flipped
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        # Coincidencia con imágenes de trabajadores
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)
            print("Lista de IDs de trabajadores:", workerIds)
            print("Lista de codificaciones conocidas:", encodeListKnown)

            if matches[matchIndex]:
                print("imagen  si encontrada")

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

                # Ajuste para corregir la posición si la imagen está flipeada
                if img_flipped is not None:
                    x1, x2 = img.shape[1] - x2, img.shape[1] - x1

                bbox = (55 + x1, 162 + y1, x2 - x1, y2 - y1)
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

                id = workerIds[matchIndex]

                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Cargando", (275, 400))
                    cv2.imshow("ASISTENCIA_ALLQOVET", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:
            print("imagen  si encontrada")
            if counter == 1:
                # Consigue la data de la BD
                query = f"SELECT id, imagen,nombre,puesto FROM trabajadores WHERE id = {id}"
                cursor.execute(query)
                workerinfo = cursor.fetchone()

                # Consigue la imagen del almacenamiento local
                ruta_imagen = workerinfo[1]  # Supongamos que la ruta de la imagen está en la columna 3
                imgWorker = cv2.imread(ruta_imagen)

                # Actualiza la base de datos o realiza acciones según tus necesidades
                # Puedes agregar lógica adicional aquí
                # Obtener la fecha y hora actual
                fecha_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Insertar registro de asistencia en la base de datos
                insert_query = f"INSERT INTO asistencias (id_trabajador, fecha_hora) VALUES ({id}, '{fecha_hora_actual}')"
                cursor.execute(insert_query)
                db.commit()  # Confirmar la transacción

                print(f"Asistencia registrada para el trabajador con ID {id} en {fecha_hora_actual}")

            if modeType != 3:
                if 5 < counter < 10:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                if counter <= 5:
                    (w, h), _ = cv2.getTextSize(workerinfo[1], cv2.FONT_HERSHEY_COMPLEX, 0.6, 2)
                    offset_x = (414 - w) // 2
                    offset_y = -10  # Ajusta según el tamaño de la fuente

                    cv2.putText(imgBackground, str(workerinfo[2]), (808 + offset_x, 445 + offset_y),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (50, 50, 50), 2)

                    cv2.putText(imgBackground, str(workerinfo[3]), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)

                    imgBackground[175:175 + 216, 909:909 + 216] = imgWorker

            counter += 1

            if counter >= 10:
                counter = 0
                modeType = 0
                workerinfo = []
                imgWorker = []
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                print("acceso correcto elias")
                cv2.waitKey(2000)  # Pausa de 4 segundos
                break
    else:
        modeType = 0
        counter = 0

    cv2.imshow("ASISTENCIA_ALLQOVET", imgBackground)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.getWindowProperty("ASISTENCIA_ALLQOVET", cv2.WND_PROP_VISIBLE) < 1:
        break  # Salir del bucle si la ventana está cerrada

# Liberar la cámara y cerrar la conexión a MySQL
cap.release()
cv2.destroyAllWindows()
cursor.close()
db.close()
