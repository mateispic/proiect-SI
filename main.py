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
import psutil



# ------------
# Initializare fereastra
# ------------
root = tk.Tk()
root.title("Criptare Fisiere")


# ------------
# Variabile
# ------------
selected_file = ""
ultima_criptare=""
rezultat_hash = ""
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

def genereaza_chei(session):
    if selected_framework.get() == "OpenSSL":
        generate_rsa_keys() 
    else:
        generate_rsa_keys_libressl() 
    with open("/Users/admin/Desktop/SI-Proiect/public_key.pem", "r") as f_pub, open("/Users/admin/Desktop/SI-Proiect/private_key.pem", "r") as f_priv:
        cheie_pub = f_pub.read()
        cheie_priv = f_priv.read()

    #session = SessionLocal()
    alg = session.query(AlgoritmCriptare).filter_by(nume="RSA").first()
    if alg:
        create_asymmetric_key(cheie_pub, cheie_priv, tip="RSA", id_algoritm=alg.id)
        messagebox.showinfo("Chei RSA", "Perechea de chei RSA a fost generata si salvata in baza de date.")
    else:
        messagebox.showerror("Eroare", "Algoritmul RSA nu exista in baza de date.")
    session.close()


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

def afiseaza_performante():
    win = tk.Toplevel(root)
    win.title("Performante salvate in DB")

    canvas = tk.Canvas(win)
    scrollbar = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    headers = ["Fisier", "Algoritm", "Framework", "Tip operatie", "Hash", "Memorie utilizata (KB)", "Timp (ms)", "Data"]
    for i, h in enumerate(headers):
        tk.Label(scroll_frame, text=h, font=("Arial", 10, "bold"), borderwidth=1, relief="solid", padx=4, pady=2).grid(row=0, column=i)

    session = SessionLocal()
    performante = session.query(Performanta).all()

    medii = {}

    for idx, p in enumerate(performante, start=1):
        fisier = session.query(Fisier).filter_by(id=p.id_fisier).first()
        algoritm = session.query(AlgoritmCriptare).filter_by(id=p.id_algoritm).first()
        framework = session.query(Framework).filter_by(id=p.id_framework).first()

        nume_alg = algoritm.nume if algoritm else "-"
        nume_fw = framework.nume if framework else "-"
        cheie = (nume_alg, nume_fw)

        medii.setdefault(cheie, []).append(p.timp_executie)

        valori = [
            fisier.nume if fisier else "-",
            nume_alg,
            nume_fw,
            p.tip_operatie,
            p.rezultat_hash[:16] + "..." if len(p.rezultat_hash) > 16 else p.rezultat_hash,
            f"{round(p.memorie_utilizata / 1024, 2)} KB" if p.memorie_utilizata else "0 KB",
            f"{p.timp_executie} ms",
            p.data_criptare.strftime("%Y-%m-%d %H:%M:%S")
        ]

        for j, val in enumerate(valori):
            tk.Label(scroll_frame, text=val, borderwidth=1, relief="solid", padx=4, pady=2).grid(row=idx, column=j)


    tk.Label(scroll_frame, text="").grid(row=idx + 1, column=0)

    tk.Label(scroll_frame, text="Medii timp executie: Algoritm + Framework", font=("Arial", 10, "bold")).grid(row=idx + 2, column=0, columnspan=3)

    row_offset = idx + 3
    for k, timpi in medii.items():
        medie = round(sum(timpi) / len(timpi), 2)
        mesaj = f"{k[0]} + {k[1]}: {medie} ms"
        tk.Label(scroll_frame, text=mesaj).grid(row=row_offset, column=0, columnspan=3, sticky="w", padx=10)
        row_offset += 1

    session.close()



session = SessionLocal()

def save():
    global rezultat_hash
    global ultima_criptare
    global session

    if not selected_file:
        label_fisier.config(text="Selecteaza un fisier!")
        return

   # session = SessionLocal()

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
            messagebox.showinfo("Succes", "Fisierul a fost salvat in baza de date!")
        else:
            messagebox.showwarning("Atentie", "Fisierul exista deja in baza de date!")

        alg = session.query(AlgoritmCriptare).filter_by(nume=selected_algoritm.get()).first()
        fw = session.query(Framework).filter_by(nume=selected_framework.get()).first()
        if not alg or not fw:
            messagebox.showerror("Eroare", "Algoritm sau framework inexistent.")
            return

        output_file = ""
        
        pub_key = rsa_public_key_path.get()
        priv_key = rsa_private_key_path.get()
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss 

        t_start = time.time()

        if selected_framework.get() == "OpenSSL":
            if selected_algoritm.get() == "AES":
                if tip_operatie.get() == "criptare":
                    output_file = selected_file + ".enc"
                    create_symmetric_key(
                        cheie=cheie_var.get(),
                        tip="AES",
                        id_algoritm=alg.id
                    )
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
                    create_symmetric_key(
                        cheie=cheie_var.get(),
                        tip="AES",
                        id_algoritm=alg.id
                    )
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
        mem_after = process.memory_info().rss
        memorie_utilizata = mem_after - mem_before


        if tip_operatie.get() == "criptare":
            with open(selected_file, "rb") as f:
                rezultat_hash = hashlib.sha256(f.read()).hexdigest()
            print("Rezultatul criptarii:", rezultat_hash)
            ultima_criptare = rezultat_hash
            print("Ultima criptare:", ultima_criptare)
        else:
            ultima_criptare = rezultat_hash
            with open(output_file, "rb") as f:
                rezultat_hash = hashlib.sha256(f.read()).hexdigest()

        
        if tip_operatie.get() == "decriptare":
            print("ultima_criptare:", ultima_criptare)
            print("rezultat_hash:", rezultat_hash)
            if ultima_criptare:
                if ultima_criptare== rezultat_hash:

                    messagebox.showinfo("Integritate", "Fisier decriptat corect ")
                else:
                    messagebox.showwarning("Integritate", "Fisierul decriptat NU coincide")
            else:
                messagebox.showwarning("Integritate", "Nu s-a gasit un hash de referinta pentru comparatie.")

        perf = Performanta(
            id_fisier=fisier.id,
            id_algoritm=alg.id,
            id_framework=fw.id,
            tip_operatie=tip_operatie.get(),
            rezultat_hash=rezultat_hash,
            timp_executie=exec_time_ms,
            memorie_utilizata=memorie_utilizata,
            data_criptare=datetime.utcnow()
        )
        session.add(perf)
        session.commit()

        messagebox.showinfo("Succes", "Performanya a fost salvata in baza de date.")
        print(f"Timp de executie: {exec_time_ms} ms")

    except Exception as e:
        print("Eroare:", e)
        label_fisier.config(text="Eroare la salvare.")
    finally:
        session.close()


#-----
# 1. Selectare fisier
#-----
tk.Label(root, text="1. Alege fisier:").pack()
tk.Button(root, text="Alege fisier", command=select_file).pack()
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
        tk.Label(frame_chei, text="Selecteaza cheia publica (.pem):").pack()
        tk.Button(frame_chei, text="Alege fisier", command=select_public_key).pack()
        tk.Label(frame_chei, textvariable=rsa_public_key_path).pack()

        tk.Label(frame_chei, text="Selecteaza cheia privata (.pem):").pack()
        tk.Button(frame_chei, text="Alege fisier", command=select_private_key).pack()
        tk.Label(frame_chei, textvariable=rsa_private_key_path).pack()


selected_algoritm.trace_add("write", update_cheie_fields)
update_cheie_fields()

#-----
# 6. Generare chei RSA
#-----
tk.Button(root, text="Genereaza chei RSA", command=lambda: genereaza_chei(session)).pack()



#-----
# 7. Start
#-----
tk.Button(root, text="Start", command=save).pack(pady=10)

#-----
# 8. Performanta
#-----
tk.Button(root, text="Vezi performante", command=afiseaza_performante).pack(pady=5)



root.mainloop()

