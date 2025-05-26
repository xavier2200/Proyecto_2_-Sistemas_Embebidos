import tkinter as tk
from tkinter import ttk
from threading import Thread
import paramiko
import cv2
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import time

emotion_dict = {0: "Enojado", 1: "Disgustado", 2: "Temeroso", 3: "Feliz", 4: "Neutral", 5: "Triste", 6: "Sorprendido"}

class EmotionClientApp:
    def __init__(self, master):
        self.master = master
        master.title("Emotion Video Client")

        self.start_button = ttk.Button(master, text="Iniciar", command=self.start)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(master, text="Parar", command=self.stop, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.video_label = ttk.Label(master)
        self.video_label.pack()

        self.figure, self.ax = plt.subplots(figsize=(6, 3))
        self.canvas = FigureCanvasTkAgg(self.figure, master)
        self.canvas.get_tk_widget().pack()

        self.running = False
        self.ssh_client = None
        self.video_capture = None
        self.emotion_data = []

    def start(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        Thread(target=self.ssh_receive_data, daemon=True).start()
        Thread(target=self.play_video, daemon=True).start()

    def stop(self):
        self.running = False
        if self.video_capture:
            self.video_capture.release()
        if self.ssh_client:
            self.ssh_client.close()
        self.update_plot()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def ssh_receive_data(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(hostname='remote_host', username='user', password='pass')

        stdin, stdout, stderr = self.ssh_client.exec_command('cat emotions.json')  # Ajustar comando
        for line in stdout:
            if not self.running:
                break
            try:
                data = json.loads(line)
                self.emotion_data.append(data['emotion'])
            except json.JSONDecodeError:
                continue

    def play_video(self):
        self.video_capture = cv2.VideoCapture('video.mp4')  # Reemplazar con ruta real
        while self.running and self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            time.sleep(1/30)

    def update_plot(self):
        if not self.emotion_data:
            return
        counts = [self.emotion_data.count(i) for i in range(len(emotion_dict))]
        labels = [emotion_dict[i] for i in range(len(emotion_dict))]
        self.ax.clear()
        self.ax.bar(labels, counts, color='skyblue')
        self.ax.set_title('Distribuci\u00f3n de Emociones')
        self.ax.set_ylabel('Frecuencia')
        self.figure.tight_layout()
        self.canvas.draw()

if __name__ == '__main__':
    root = tk.Tk()
    app = EmotionClientApp(root)
    root.mainloop()
