# interfata
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox
from models import *
from database import SessionLocal 
import os
import time
import datetime
from operatii_crud import *

# ------------
# Initializare fereastra
# ------------
root = tk.Tk()
root.title("Criptare Fisiere")


# ------------
# Variabile
# ------------
selected_file = ""
selected_algoritm = tk.StringVar()
selected_framework = tk.StringVar()
cheie_var = tk.StringVar()
tip_operatie= tk.StringVar()

algoritmi = ["AES","b","c"]
frameworkuri = ["OpenSSL","e","f"]

# ------------
# Functii
# ------------
def select_file():
    global selected_file
    filename = filedialog.askopenfilename()
    if filename:
        selected_file = filename
        label_fisier.config(text=filename.split("/")[-1])


    
def save():
    global tip_operatie
    if not selected_file:
        label_fisier.config(text="Selecteaza un fisier!!!")
        return
   
    session = SessionLocal()

    try:
        fisier = session.query(Fisier).filter(Fisier.cale == selected_file).first()
        if not fisier:
            fisier = create_file(session, os.path.basename(selected_file), selected_file, os.path.getsize(selected_file), os.path.splitext(selected_file)[1][1:])
        
            messagebox.showinfo("Succes", "Fisierul a fost salvat in baza de date!")
        else:
            messagebox.showwarning("Atentie", "Fisierul exista deja in baza de date!!")

        alg = session.query(AlgoritmCriptare).filter_by(nume=selected_algoritm.get()).first()
        if not alg:
            messagebox.showerror("Eroare", "Algoritm inexistent.")
            return
        fw = session.query(Framework).filter_by(nume=selected_framework.get()).first()
        if not fw:
            messagebox.showerror("Eroare", "Framework inexistent.")
            return
        
        t_start = time.time()

        with open(selected_file, "rb") as f:
            file_data = f.read()
        hash_result = hashlib.sha256(file_data).hexdigest()

        t_end = time.time()
        exec_time_ms = int((t_end - t_start) * 1000)

        
        if tip_operatie.get() == "criptare":
            print("Criptare in desfasurare...")
        elif tip_operatie.get() == "decriptare":
            print("Decriptare in desfasurare...")
        else:
            print("Nicio operație selectată")



        perf = Performanta(
        id_fisier=fisier.id,
        id_algoritm=alg.id,
        id_framework=fw.id,
        tip_operatie=tip_operatie.get(),
        rezultat_hash=hash_result,
        timp_executie=exec_time_ms,
        memorie_utilizata=0,
        data_criptare=datetime.utcnow()
        )
        session.add(perf)
        session.commit()

        messagebox.showinfo("Succes", "Performanța a fost salvată în baza de date.")

        
    except Exception as e:
        print("Eroare:", e)
        label_fisier.config(text="Eroare la salvare.")
    finally:
        session.close()


#-----
# 1. Selectare fisier
#-----
tk.Label(root, text="1. Alege fisier:").pack()
tk.Button(root, text="Alege fișier", command=select_file).pack()
label_fisier = tk.Label(root, text="Niciun fisier selectat")
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
# 6. Start
#-----
tk.Button(root, text="Start", command=save).pack(pady=10)








root.mainloop()

