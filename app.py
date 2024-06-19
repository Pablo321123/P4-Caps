import keyboard
import pyperclip
import time
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import threading


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
    print(textUpper)
    print(type_text)

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
    return image
    # return Image.open("assets/3.png")


def on_exit(icon, item):
    msg = (
        "P4 Caps está minusculo e o P4 Caps odeia minusculo >:( "
        if type_text == 1
        else (
            "P4 Caps está MAIUSCULO e o P4 Caps odeia MAIUSCULO >:( "
            if type_text == 0
            else "Tão Achando Que É Só Mamão, Que É Só Mel, Tao Achando Que É Facil Fabricar Papel?"
        )
    )
    print("")
    icon.stop()


def run_program():
    print("P4 Caps iniciado!")
    keyboard.add_hotkey("ctrl + caps lock", textToUper)
    keyboard.wait()


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

icon.run()
