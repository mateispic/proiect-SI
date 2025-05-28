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
from openssl import *
from libressl import *

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

rsa_public_key_path = tk.StringVar()
rsa_private_key_path = tk.StringVar()

cheie_var = tk.StringVar()
tip_operatie= tk.StringVar()

algoritmi = ["AES","RSA"]
frameworkuri = ["OpenSSL","LibreSSL"]

# ------------
# Functii
# ------------

def genereaza_chei():
    generate_rsa_keys()
    messagebox.showinfo("Chei RSA", "Perechea de chei RSA a fost generată.")


def select_file():
    global selected_file
    filename = filedialog.askopenfilename()
    if filename:
        selected_file = filename
        label_fisier.config(text=filename.split("/")[-1])

def select_public_key():
    path = filedialog.askopenfilename(filetypes=[("PEM files", "*.pem")])
    if path:
        rsa_public_key_path.set(path)

def select_private_key():
    path = filedialog.askopenfilename(filetypes=[("PEM files", "*.pem")])
    if path:
        rsa_private_key_path.set(path)



def save():
    if not selected_file:
        label_fisier.config(text="Selectează un fișier!")
        return

    session = SessionLocal()

    try:
        fisier = session.query(Fisier).filter(Fisier.cale == selected_file).first()
        if not fisier:
            fisier = create_file(
                session,
                os.path.basename(selected_file),
                selected_file,
                os.path.getsize(selected_file),
                os.path.splitext(selected_file)[1][1:]
            )
            messagebox.showinfo("Succes", "Fișierul a fost salvat în baza de date!")
        else:
            messagebox.showwarning("Atenție", "Fișierul există deja în baza de date!")

        alg = session.query(AlgoritmCriptare).filter_by(nume=selected_algoritm.get()).first()
        fw = session.query(Framework).filter_by(nume=selected_framework.get()).first()
        if not alg or not fw:
            messagebox.showerror("Eroare", "Algoritm sau framework inexistent.")
            return

        output_file = ""
        pub_key = rsa_public_key_path.get()
        priv_key = rsa_private_key_path.get()

        t_start = time.time()

        # Criptare sau decriptare
        if selected_framework.get() == "OpenSSL":
            if selected_algoritm.get() == "AES":
                if tip_operatie.get() == "criptare":
                    output_file = selected_file + ".enc"
                    aes_encrypt(selected_file, output_file, cheie_var.get())
                else:
                    output_file = selected_file.replace(".enc", ".dec")
                    aes_decrypt(selected_file, output_file, cheie_var.get())
            elif selected_algoritm.get() == "RSA":
                if tip_operatie.get() == "criptare":
                    output_file = selected_file + ".rsa.enc"
                    rsa_encrypt(selected_file, output_file, pub_key)
                else:
                    output_file = selected_file.replace(".rsa.enc", ".dec")
                    rsa_decrypt(selected_file, output_file, priv_key)

        elif selected_framework.get() == "LibreSSL":
            if selected_algoritm.get() == "AES":
                if tip_operatie.get() == "criptare":
                    output_file = selected_file + ".enc"
                    aes_encrypt_libressl(selected_file, output_file, cheie_var.get())
                else:
                    output_file = selected_file.replace(".enc", ".dec")
                    aes_decrypt_libressl(selected_file, output_file, cheie_var.get())

            elif selected_algoritm.get() == "RSA":
                if tip_operatie.get() == "criptare":
                    output_file = selected_file + ".rsa.enc"
                    rsa_encrypt_libressl(selected_file, output_file, pub_key)
                else:
                    output_file = selected_file.replace(".rsa.enc", ".dec")
                    rsa_decrypt_libressl(selected_file, output_file, priv_key)

        t_end = time.time()
        exec_time_ms = int((t_end - t_start) * 1000)

        # Calcul hash pe fisierul rezultat
        with open(output_file, "rb") as f:
            rezultat_hash = hashlib.sha256(f.read()).hexdigest()

        # Verificare integritate doar la decriptare
        if tip_operatie.get() == "decriptare":
            ultima_criptare = (
                session.query(Performanta)
                .filter_by(id_fisier=fisier.id, id_algoritm=alg.id, id_framework=fw.id, tip_operatie="criptare")
                .order_by(Performanta.data_criptare.desc())
                .first()
            )

            if ultima_criptare:
                if ultima_criptare.rezultat_hash == rezultat_hash:
                    messagebox.showinfo("Integritate", "Fișier decriptat corect ✅")
                else:
                    messagebox.showwarning("Integritate", "Fișierul decriptat NU coincide ❌")
            else:
                messagebox.showwarning("Integritate", "Nu s-a găsit un hash de referință pentru comparație.")

        # Salvare performanță
        perf = Performanta(
            id_fisier=fisier.id,
            id_algoritm=alg.id,
            id_framework=fw.id,
            tip_operatie=tip_operatie.get(),
            rezultat_hash=rezultat_hash,
            timp_executie=exec_time_ms,
            memorie_utilizata=0,
            data_criptare=datetime.utcnow()
        )
        session.add(perf)
        session.commit()

        messagebox.showinfo("Succes", "Performanța a fost salvată în baza de date.")
        print(f"Timp de execuție: {exec_time_ms} ms")

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


frame_chei = tk.Frame(root)
frame_chei.pack()

def update_cheie_fields(*args):
    for widget in frame_chei.winfo_children():
        widget.destroy()

    if selected_algoritm.get() == "AES":
        tk.Label(frame_chei, text="Cheie AES:").pack()
        tk.Entry(frame_chei, textvariable=cheie_var).pack()

    elif selected_algoritm.get() == "RSA":
        tk.Label(frame_chei, text="Selectează cheia publică (.pem):").pack()
        tk.Button(frame_chei, text="Alege fișier", command=select_public_key).pack()
        tk.Label(frame_chei, textvariable=rsa_public_key_path).pack()

        tk.Label(frame_chei, text="Selectează cheia privată (.pem):").pack()
        tk.Button(frame_chei, text="Alege fișier", command=select_private_key).pack()
        tk.Label(frame_chei, textvariable=rsa_private_key_path).pack()


selected_algoritm.trace_add("write", update_cheie_fields)
update_cheie_fields()

tk.Button(root, text="Generează chei RSA", command=genereaza_chei).pack()


#-----
# 6. Start
#-----
tk.Button(root, text="Start", command=save).pack(pady=10)





root.mainloop()

