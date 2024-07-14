from cx_Freeze import setup, Executable

build_exe_options = {
    "includes": ["keyboard", "pyperclip", "pystray", "PIL", "tkinter"],
    "zip_include_packages": ["encodings", "PySide6", "shiboken6"],
}

setup(
    name="P4Caps",
    version="0.1",
    description="P4 Caps Application",
    options={"build_exe": build_exe_options},
    executables=[Executable("app.py", base="gui")],
)