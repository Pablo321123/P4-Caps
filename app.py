import keyboard
import pyperclip
import time
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import threading
from threading import Timer, Thread
import tkinter as tk


type_text = 1  # 0 - Lower; 1 - Upper; 2 - Alternative


def textToUper():
    keyboard.send("ctrl+c")
    time.sleep(0.5)

    textCopied = pyperclip.paste()
    textUpper = (
        textCopied.upper()
        if type_text == 1
        else textCopied.lower() if type_text == 0 else textCopied.title()
    )
    # print(textUpper)
    # print(type_text)

    pyperclip.copy(textUpper)
    keyboard.send("ctrl+v")

def lower_text(item, icon=None):
    global type_text  # Faz com que o python
    type_text = 0
    return True


def upper_text(item):
    global type_text
    type_text = 1
    return type_text


def alternate_text(item):
    global type_text
    type_text = 2
    return type_text


def create_image():
    # Cria uma imagem em memória
    width = 64
    height = 64
    color1 = "white"
    color2 = "#0090ff"
    image = Image.new("RGB", (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
    dc.rectangle((0, height // 2, width // 2, height), fill=color2)
    # image.save("icon.ico")
    return image
    # return Image.open("assets/3.png")


def alterTextMode():
    global type_text
    msg = ""

    type_text = type_text + 1
    
    if type_text == 1:
        msg = "MODO: MAIÚSCULAS!"
    elif type_text == 2:
        msg = "Modo: Alternado!"
    elif type_text > 2:
        type_text = 0
        msg = "modo: minúsculas!"
        
    icon.update_menu()
    showMessage(msg)


def on_exit(icon, item):
    msg = (
        "P4 Caps está minúsculo e o P4 Caps odeia minúsculo >:( "
        if type_text == 1
        else (
            "P4 Caps está MAIÚSCULO e o P4 Caps odeia MAIÚSCULO >:( "
            if type_text == 0
            else "Tão Achando Que É Só Mamão, Que É Só Mel, Tao Achando Que É Facil Fabricar Papel?"
        )
    )
    print(msg)
    icon.stop()


def run_program():
    print("P4 Caps iniciado!")
    keyboard.add_hotkey("ctrl + caps lock", textToUper)
    keyboard.add_hotkey("ctrl + shift + q", alterTextMode)
    keyboard.wait()


def showMessage(msg):

    def overlayMessage():
        root = tk.Tk()
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.geometry(
            "+{}+{}".format(
                root.winfo_screenwidth() // 2 - 100, root.winfo_screenheight() // 2 - 50
            )
        )
        label = tk.Label(root, text=msg, font=("Helvetica", 24), bg="black", fg="white")
        label.pack()

        def fade_out():
            alpha = root.attributes("-alpha")
            if alpha > 0:
                alpha -= 0.1
                root.attributes("-alpha", alpha)
                root.after(100, fade_out)
            else:
                root.quit()

        # Destrói o overlay após 2 segundos
        # Timer(2.0, root.quit).start()
        root.after(2000, fade_out)
        root.mainloop()

    Thread(target=overlayMessage).start()


icon = pystray.Icon("test")
icon.icon = create_image()
icon.title = "P4 Caps"
icon.menu = pystray.Menu(
    item("todas minusculas", lower_text, checked=lambda item: type_text == 0),
    item("TODAS MAIUSCULAS", upper_text, checked=lambda item: type_text == 1),
    item("Texto Alternado", alternate_text, checked=lambda item: type_text == 2),
    item("Sair", on_exit),
)

threading.Thread(target=run_program, daemon=True).start()
showMessage("P4 Caps iniciado!")
icon.run()
