from database import SessionLocal
from models import *

session = SessionLocal()

# ------------
# OPERATII CRUD PENTRU TABELA FISIER
# ------------

# --------
# CREATE 
# --------
def create_file(nume, cale, marime, format):        
    session = SessionLocal()
    file = Fisier(nume=nume, cale=cale, marime=marime, format=format)
    session.add(file)
    session.commit()
    session.close()
    print("Fisier adaugat cu succes")

# --------
# READ
# --------
def get_all_files():
    session = SessionLocal()
    files = session.query(Fisier).all()
    print("Fisierele din baza de date sunt:")
    for f in files:
        print(f.nume, f.format)
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
    file = session.query(Fisier).filter_by(nume).first()
    if file:
        session.delete(file)
        session.commit()
        print("Fisier sters cu succes")
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
        print(f.nume, f.versiune)
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
    

