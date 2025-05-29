from database import SessionLocal
from models import *

# ------------
# OPERATII CRUD PENTRU TABELA FISIER
# ------------

# --------
# CREATE 
# --------
def create_file(session, nume, cale, marime, format):        
    #session = SessionLocal()
    file = Fisier(nume=nume, cale=cale, marime=marime, format=format)
    session.add(file)
    session.commit()
  #  session.close()
    print("Fisier adaugat cu succes")
    return file

# --------
# READ
# --------
def get_all_files():
    session = SessionLocal()
    files = session.query(Fisier).all()
    print("Fisierele din baza de date sunt:")
    for f in files:
        print(f'{f.nume}.{f.format}')
    session.commit()
    session.close()


# --------
# UPDATE 
# --------
# update doar pentru nume, o sa fie implementat update pt tot pe viitor
def update_file_name(nume, nume_nou): 
    session = SessionLocal()
    file = session.query(Fisier).filter_by(nume).first()
    if file:
        file.nume = nume_nou
        session.commit()
        print("Numele fisierului modificat cu succes")
    session.commit()
    session.close()

# --------
# DELETE 
# --------
def delete_file(nume):
    session = SessionLocal()
    file = session.query(Fisier).filter_by(nume=nume).first()
    if file:
        session.delete(file)
        session.commit()
        print(f'Fisierul {nume} a fost sters cu succes')
    else:
        print(f'Fisierul {nume} nu a fost gasit.')
    session.commit()
    session.close()
       
        
# ------------
# OPERATII CRUD PENTRU TABELA FRAMEWORK
# ------------

# --------
# CREATE 
# --------
def create_framework(nume, versiune):
    session = SessionLocal()
    framework = Framework(nume=nume, versiune=versiune)
    session.add(framework)
    session.commit()
    session.close()
    print("Framework adaugat cu succes")
    

# --------
# READ
# --------
def get_all_frameworks():
    session = SessionLocal()
    frameworks = session.query(Framework).all()
    print("Framework-urile din baza de date sunt:")
    for f in frameworks:
        print(f'Nume: {f.nume}, Versiune: {f.versiune}')
    session.commit()
    session.close()

# --------
# UPDATE 
# --------
# update doar pentru nume, o sa fie implementat update pt tot pe viitor
def update_framework_name(nume, nume_nou): 
    session = SessionLocal()
    framework = session.query(Framework).filter_by(nume).first()
    if framework:
        framework.nume = nume_nou
        session.commit()
        print("Numele fisierului modificat cu succes")
    session.commit()
    session.close()

# --------
# DELETE 
# --------
def delete_framework(nume):
    session = SessionLocal()
    framework = session.query(Framework).filter_by(nume).first()
    if framework:
        session.delete(framework)
        session.commit()
        print("Framework sters cu succes")
    session.commit()
    session.close()
    

# ------------
# OPERATII CRUD PENTRU TABELA CHEIE SIMETRICA
# ------------

# --------
# CREATE 
# --------
def create_symmetric_key(cheie, tip, id_algoritm):
    session = SessionLocal()
    symm_key = CheieSimetrica(cheie=cheie, tip=tip, lungime=len(cheie), id_algoritm=id_algoritm)
    session.add(symm_key)
    session.commit()
    session.close()
    print("Cheie simetrica adaugata cu succes")

# --------
# READ
# --------
def get_all_symmetrical_keys():
    session = SessionLocal()
    symm_keys = session.query(CheieSimetrica).all()
    print("Cheile simetrice din baza de date sunt:")
    for k in symm_keys:
        print(f'Cheie: {k.cheie}, Tip: {k.tip}, Lungime: {k.lungime}, ID algoritm: {k.id_algoritm}')
    session.commit()
    session.close()

# --------
# UPDATE 
# --------
# update doar pentru cheie, o sa fie implementat update pt tot pe viitor
def update_symmetrical_key(cheie, cheie_noua): 
    session = SessionLocal()
    symm_key = session.query(symm_key).filter_by(cheie).first()
    if symm_key:
        symm_key.cheie = cheie_noua
        symm_key.lungime = len(cheie_noua)
        session.commit()
        print("Cheia simetrica modificata cu succes")
    session.commit()
    session.symmetrical_keylose()

# --------
# DELETE 
# --------
def delete_symmetrical_key(cheie):
    session = SessionLocal()
    symm_key = session.query(CheieSimetrica).filter_by(cheie).first()
    if symm_key:
        session.delete(symm_key)
        session.commit()
        print("Cheie simetrica stearsa cu succes")
    session.commit()
    session.close()
    
# ------------
# OPERATII CRUD PENTRU TABELA CHEIE ASIMETRICA
# ------------

# --------
# CREATE 
# --------
def create_asymmetric_key(cheie_publica, cheie_privata, tip, id_algoritm):
    session = SessionLocal()
    asymm_key = CheieAsimetrica(cheie_publica=cheie_publica, cheie_privata=cheie_privata, tip=tip, lungime=len(cheie_publica), id_algoritm=id_algoritm)
    session.add(asymm_key)
    session.commit()
    session.close()
    print("Chei asimetrice adaugate cu succes")

# --------
# READ
# --------
def get_all_asymmetrical_keys():
    session = SessionLocal()
    asymm_keys = session.query(CheieAsimetrica).all()
    print("Cheile asimetrice din baza de date sunt:")
    for k in asymm_keys:
        print(f'Cheie publica: {k.cheie_publica}, Cheie privata: {k.cheie_privata}, Tip: {k.tip}, Lungime: {k.lungime}, ID algoritm: {k.id_algoritm}')
    session.commit()
    session.close()

# --------
# UPDATE 
# --------
# update doar pentru cheie, o sa fie implementat update pt tot pe viitor
def update_asymmetrical_public_key(cheie_publica, cheie_publica_noua): 
    session = SessionLocal()
    asymm_key = session.query(asymm_key).filter_by(cheie_publica).first()
    if asymm_key:
        asymm_key.cheie_publica = cheie_publica_noua
        asymm_key.lungime = len(cheie_publica_noua)
        session.commit()
        print("Cheia publica asimetrica modificata cu succes")
    session.commit()
    session.close()

# --------
# DELETE 
# --------
def delete_asymmetrcal_key(cheie_publica):
    session = SessionLocal()
    symm_key = session.query(CheieAsimetrica).filter_by(cheie_publica).first()
    if symm_key:
        session.delete(symm_key)
        session.commit()
        print("Cheie asimetrica stearsa cu succes")
    session.commit()
    session.close()
    
# ------------
# OPERATII CRUD PENTRU TABELA ALGORITM CRIPTARE
# ------------

# --------
# CREATE 
# --------
def create_encryption_algorithm(nume, tip, lungime_cheie):        
    session = SessionLocal()
    enc_alg = AlgoritmCriptare(nume=nume, tip=tip, lungime_cheie=lungime_cheie)
    session.add(enc_alg)
    session.commit()
    session.close()
    print("Algoritm de criptare adaugat cu succes")

# --------
# READ
# --------
def get_all_encryption_algorithms():
    session = SessionLocal()
    enc_alg = session.query(AlgoritmCriptare).all()
    print("Algoritmii de criptare din baza de date sunt:")
    for a in enc_alg:
        print(f'Nume: {a.nume}, Tip: {a.tip}, Lungime: {a.lungime_cheie}')
    session.commit()
    session.close()

# --------
# UPDATE 
# --------
# update doar pentru nume, o sa fie implementat update pt tot pe viitor
def update_encryption_algorithm_name(nume, nume_nou, tip, tip_nou): 
    session = SessionLocal()
    enc_alg = session.query(AlgoritmCriptare).filter_by(nume).first()
    if enc_alg:
        enc_alg.nume = nume_nou
        enc_alg.tip = tip_nou
        session.commit()
        print("Algoritmul de criptare a fost modificat cu succes")
    else:
        print("Algorimtul cautat nu exista")
    session.commit()
    session.close()

# --------
# DELETE 
# --------
def delete_encryption_algorithm(nume):
    session = SessionLocal()
    enc_alg = session.query(Fisier).filter_by(nume=nume).first()
    if enc_alg:
        session.delete(enc_alg)
        session.commit()
        print(f'Algoritmul de criptare {nume} a fost sters cu succes')
    else:
        print(f'Algoritmul de criptare {nume} nu a fost gasit.')
    session.commit()
    session.close()
    
# ------------
# OPERATII CRUD PENTRU TABELA PERFORMANTA
# ------------

# --------
# CREATE 
# --------
def create_performance(id_fisier, id_algoritm, id_framework, tip_operatie, rezultat_hash, timp_executie, memorie_utilizata, data_criptare):        
    session = SessionLocal()
    performance = Performanta(id_fisier=id_fisier, id_algoritm=id_algoritm, id_framework=id_framework, tip_operatie=tip_operatie, rezultat_hash=rezultat_hash, timp_executie=timp_executie, memorie_utilizata=memorie_utilizata, data_criptare=data_criptare)
    session.add(performance)
    session.commit()
    session.close()
    print("Performante algoritm adaugat cu succes")

# --------
# READ
# --------
def get_all_performances():
    session = SessionLocal()
    performances = session.query(Performanta).all()
    print("Performantele algoritmilor din baza de date sunt:")
    for p in performances:
        print(f'ID fisier = {p.id_fisier}, ID algoritm = {p.id_algoritm}, ID framework = {p.id_framework}, Tip operatie = {p.tip_operatie}, Rezultat hash = {p.rezultat_hash}, Timp executie = {p.timp_executie}, Memorie utilizata = {p.memorie_utilizata}, Data criptare = {p.data_criptare}')
    session.commit()
    session.close()

# # --------
# # UPDATE 
# # --------
# # update doar pentru nume, o sa fie implementat update pt tot pe viitor
# def update_file_name(nume, nume_nou): 
#     session = SessionLocal()
#     file = session.query(Fisier).filter_by(nume).first()
#     if file:
#         file.nume = nume_nou
#         session.commit()
#         print("Numele fisierului modificat cu succes")
#     session.commit()
#     session.close()

# --------
# DELETE 
# --------
def delete_performance(id_fisier, id_algoritm, id_framework, tip_operatie):
    session = SessionLocal()
    performance = session.query(Performanta).filter_by(id_fisier=id_fisier, id_algoritm=id_algoritm, id_framework=id_framework, tip_operatie=tip_operatie).first()
    if performance:
        session.delete(performance)
        session.commit()
        print(f'Performantele {performance} au fost sterse cu succes')
    else:
        print(f'Performantele {performance} nu au fost gasite.')
    session.commit()
    session.close()