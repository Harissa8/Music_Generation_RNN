import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import pyttsx3
engine = pyttsx3.init()
def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()
text_to_speech("Hello, it's nn. Click here to generate your music.")

# Create the GUI window
window = tk.Tk()
window.title("Music Generation")
image_path = "OIP.jpg"
image = Image.open(image_path)
image = image.resize((400, 400))
image = ImageTk.PhotoImage(image)

canvas = tk.Canvas(window, width=400, height=400)
canvas.pack()
canvas.create_image(0, 0, anchor=tk.NW, image=image)
def run_mg():
    subprocess.call(['python', 'mg.py'])
def open_mel_mid():
    subprocess.call(['start', 'mel.mid'], shell=True)
def generate_music():
    run_mg()
def open_mel_mid_button():
    open_mel_mid()
button_generate_music = tk.Button(window, text="Generate Music", command=generate_music)
button_generate_music.pack()
button_run_mel_mid = tk.Button(window, text="Listen to Music", command=open_mel_mid_button)
button_run_mel_mid.pack()
window.mainloop()
text_to_speech(" I hope you enjoyed my music!Thank you. HEHEHE.")