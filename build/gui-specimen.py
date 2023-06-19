# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path
from app import c
import app

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import os


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame3")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1280x720")
window.configure(bg="#FFFFFF")


canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=720,
    width=1280,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(1179.0, 45.0, image=image_image_1)

canvas.create_text(
    489.0,
    42.0,
    anchor="nw",
    text="Specimen Settings",
    fill="#000000",
    font=("Inter", 34 * -1),
)

canvas.create_text(
    444.0, 239.0, anchor="nw", text="Length =", fill="#000000", font=("Inter", 20 * -1)
)

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(719.0, 252.5, image=entry_image_1)
entry_1 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_1.place(x=644.0, y=237.0, width=150.0, height=29.0)

canvas.create_text(
    800.0, 239.0, anchor="nw", text="mm", fill="#000000", font=("Inter", 20 * -1)
)

canvas.create_text(
    444.0,
    286.0,
    anchor="nw",
    text="Diameter =",
    fill="#000000",
    font=("Inter", 20 * -1),
)

entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(719.0, 299.0, image=entry_image_2)
entry_2 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
entry_2.place(x=644.0, y=283.0, width=150.0, height=30.0)

canvas.create_text(
    800.0, 286.0, anchor="nw", text="mm", fill="#000000", font=("Inter", 20 * -1)
)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: (window.destroy(), os.system("python ./build/gui-data.py")),
    relief="flat",
)
button_1.place(x=50.0, y=50.0, width=200.0, height=50.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: (print(c), app.import_speciment_settings(c), print(c)),
    relief="flat",
)
button_2.place(x=50.0, y=283.0, width=200.0, height=50.0)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat",
)
button_3.place(x=50.0, y=381.0, width=200.0, height=50.0)
window.resizable(False, False)
window.mainloop()