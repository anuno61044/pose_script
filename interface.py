import cv2
from tkinter import *
from PIL import Image, ImageTk

def update_camera_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    photo = ImageTk.PhotoImage(image=img)
    camera_label.config(image=photo)
    camera_label.image = photo
    root.after(10, update_camera_frame)

def load_photo(path):
    img = Image.open(path)
    photo = ImageTk.PhotoImage(image=img)
    fixed_label.config(image=photo)
    fixed_label.image = photo

root = Tk()
root.attributes('-fullscreen', True)  # Hace que la ventana sea de pantalla completa
root.title("Cámara y Foto")

cap = cv2.VideoCapture(0)

# Configurar la ventana para usar grid
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

camera_label = Label(root)
camera_label.grid(row=0, column=0, sticky='nsew')

fixed_label = Label(root)
fixed_label.grid(row=0, column=1, sticky='nsew')

load_photo('./gangam.jpg')
update_camera_frame()

root.mainloop()