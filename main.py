# interfata
import tkinter as tk
from tkinter import filedialog, messagebox
from models import *


root = tk.Tk()
root.title("Criptare Fisiere")

selected_file = ""
selected_algoritm = tk.StringVar()
selected_framework = tk.StringVar()
cheie_var = tk.StringVar()


algoritmi = ["a","b","c"]
frameworkuri = ["d","e","f"]


def select_file():
    filename = filedialog.askopenfilename()
    if filename:
        selected_file = filename
        label_fisier.config(text=filename.split("/")[-1])
    
def save():
   return None


#-----
# 1. Selectare fisier
#-----
tk.Label(root, text="1. Alege fișier:").pack()
tk.Button(root, text="Alege fișier", command=select_file).pack()
label_fisier = tk.Label(root, text="Niciun fișier selectat")
label_fisier.pack()

#-----
# 2. Selectare algoritm
#-----
tk.Label(root, text="2. Alege algoritm:").pack()
selected_algoritm.set(algoritmi[0])
tk.OptionMenu(root, selected_algoritm, *algoritmi).pack()

#-----
# 3. Selectare framework
#-----
tk.Label(root, text="3. Alege framework:").pack()
selected_framework.set(frameworkuri[0])
tk.OptionMenu(root, selected_framework, *frameworkuri).pack()

#-----
# 4. Alegere operatie
#-----
tk.Label(root, text="4. Tip operatie:").pack()
tip_operatie = tk.StringVar(value="criptare")
tk.Radiobutton(root, text="Criptare", variable=tip_operatie, value="criptare").pack()
tk.Radiobutton(root, text="Decriptare", variable=tip_operatie, value="decriptare").pack()

#-----
# 5. Introducere cheie
#-----
tk.Label(root, text="5. Introduceti cheie:").pack()
tk.Entry(root, textvariable=cheie_var).pack()

#-----
# 6. Salveaza in BD
#-----
tk.Button(root, text="Salveaza in BD", command=save).pack()

root.mainloop()

