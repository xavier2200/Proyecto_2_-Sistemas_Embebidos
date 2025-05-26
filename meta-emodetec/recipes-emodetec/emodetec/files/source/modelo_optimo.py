#!/usr/bin/env python3

import numpy as np
import cv2
import datetime
import time
import csv
import tflite_runtime.interpreter as tflite
from BlazeFaceDetection.blazeFaceDetector import blazeFaceDetector
##For face detection model
scoreThreshold = 0.7
iouThreshold = 0.3
modelType = "front"

# Initialize face detector
faceDetector = blazeFaceDetector(modelType, scoreThreshold, iouThreshold)
#camera = cv2.VideoCapture(0)

# Cargar modelo
print("Cargando modelo...")
interpreter = tflite.Interpreter(model_path="./models/model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Deshabilitar OpenCL para estabilidad
cv2.ocl.setUseOpenCL(False)

# Diccionario de emociones (igual al tuyo)
emotion_dict = {
    0: "Enojado", 
    1: "Disgustado", 
    2: "Temeroso", 
    3: "Feliz", 
    4: "Neutral", 
    5: "Triste", 
    6: "Sorprendido"
}

# Inicializar cámara
print("Iniciando camara...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: No se pudo abrir la camara")
    exit(1)
print("Camara iniciada")

# Crear/abrir archivo CSV (reescribir cada vez)
csv_filename = "emociones_detectadas.csv"
print(f"Creando archivo: {csv_filename}")

try:
    csv_file = open(csv_filename, 'w', newline='')
    csv_writer = csv.writer(csv_file)
    
    # Escribir headers del CSV
    csv_writer.writerow(['Timestamp', 'Emocion', 'Confianza'])
    
    print("Archivo CSV creado")
    
except Exception as e:
    print(f"ERROR: No se pudo crear archivo CSV: {e}")
    cap.release()
    exit(1)

# Variables de tiempo
emotion_start_time = time.time()
last_emotion = "Desconocido"

print("\nIniciando deteccion de emociones...")
print("Guardando resultados en CSV...")
print("Presiona Ctrl+C para salir\n")

try:
    while True:
        # Read frame from the webcam
        ret, img = cap.read()
        detectionResults = faceDetector.detectFaces(img)
        #llamar a main.py
        face = faceDetector.image_resize(img,detectionResults)
        if not(np.all(face==0)):
            face = np.expand_dims(np.expand_dims(face, -1), 0)
            face = np.array(face, dtype='f')
            # Realizar predicción de emoción
            interpreter.set_tensor(input_details[0]['index'], face)
            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details[0]['index'])
            
            # Obtener emoción predicha
            maxindex = int(np.argmax(output_data))
            confidence = float(np.max(output_data))
            current_emotion = emotion_dict[maxindex]
            
            # Registrar resultado en CSV cada segundo o cuando cambie la emoción
            if (time.time() - emotion_start_time >= 1.0) or (current_emotion != last_emotion):
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Escribir al CSV
                csv_writer.writerow([timestamp, current_emotion, f"{confidence:.3f}"])
                csv_file.flush()  # Asegurar que se escriba inmediatamente
                
                emotion_start_time = time.time()
                last_emotion = current_emotion
                print(f"[{timestamp}] Emoción: {current_emotion}")
        else:
            current_emotion = "No Face"
            if (time.time() - emotion_start_time >= 1.0) or (current_emotion != last_emotion):
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Escribir al CSV
                csv_writer.writerow([timestamp, current_emotion, f"0"])
                csv_file.flush()  # Asegurar que se escriba inmediatamente
                
                emotion_start_time = time.time()
                last_emotion = current_emotion
                print(f"[{timestamp}] Emoción: {current_emotion}")
            
            
        # Control de FPS (reducir carga CPU)
        time.sleep(0.5)  # ~2 FPS

except KeyboardInterrupt:
    print("\nDeteniendo detección de emociones...")

except Exception as e:
    print(f"ERROR: {e}")

finally:
    # Limpiar recursos
    cap.release()
    csv_file.close()
    print(f"Archivo CSV guardado: {csv_filename}")
    print("Camara liberada")
