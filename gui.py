import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
import cv2
import threading
import paramiko
import pandas as pd
import time
import os

class VideoInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz con Raspberry Pi")
        self.running = False
        self.video_label = tk.Label(root)
        self.video_label.pack()

        # Botones
        self.start_btn = tk.Button(root, text="Iniciar video y detector", command=self.start_video)
        self.start_btn.pack()

        self.pause_btn = tk.Button(root, text="Pausar y cargar CSV", command=self.pause_video)
        self.pause_btn.pack()

        self.cargar_btn = tk.Button(root, text="Recargar CSV", command=self.mostrar_csv)
        self.cargar_btn.pack()

        # Tabla para CSV
        self.tree = ttk.Treeview(root)
        self.tree.pack()

        if os.path.exists("output.csv"):
            self.mostrar_csv()

    def start_video(self):
        if not self.running:
            self.running = True
            self.cap = cv2.VideoCapture("./video_xavier.mp4")
            self.update_video()  # no thread
            threading.Thread(target=self.ejecutar_remoto, args=("python3 modelo_optimo.py &",), daemon=True).start()

    def update_video(self):
        if self.running and self.cap:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (640, 480))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk  # Keep reference
                self.video_label.config(image=imgtk)
            else:
                self.pause_video()

        self.video_label.after(30, self.update_video)
            

    def pause_video(self):
        if self.running:
            self.running = False
            self.cap.release()
            self.video_label.config(image="")
            self.ejecutar_remoto("kill $(pgrep python)")
            time.sleep(1)
            self.descargar_csv()
            self.mostrar_csv()

    def ejecutar_remoto(self, comando):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('192.168.10.105', username='root', password='', look_for_keys=False, allow_agent=False)
            ssh.exec_command(f'cd /home/root/emodetec && {comando}')
            ssh.close()
        except Exception as e:
            print("Error SSH:", e)

    def descargar_csv(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect('192.168.10.105', username='root', password='', look_for_keys=False, allow_agent=False)

            sftp = ssh.open_sftp()
            sftp.get('/home/root/emodetec/emociones_detectadas.csv', 'output.csv')
            sftp.close()
            ssh.close()
            print("Archivo CSV descargado exitosamente.")
        except Exception as e:
            print("Error al descargar CSV:", e)

    def mostrar_csv(self):
        try:
            df = pd.read_csv("output.csv")

            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)

            self.tree["columns"] = list(df.columns)
            self.tree["show"] = "headings"

            for col in df.columns:
                self.tree.heading(col, text=col)

            for _, row in df.iterrows():
                self.tree.insert("", "end", values=list(row))

        except Exception as e:
            print("Error al mostrar CSV:", e)

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoInterface(root)
    root.mainloop()
