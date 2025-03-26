from database import SessionLocal
from models import Fisier

session = SessionLocal()

# ------------
# OPERATII CRUD PENTRU TABELA FISIER
# ------------

# --------
# CREATE 
# --------
fisier = Fisier(
    nume="test.txt",
    cale="/home/user/test.txt",
    marime=1234,
    format="txt"
)

session.add(fisier)
session.commit()
print("Fisier adaugat cu succes")

# --------
# READ
# --------
fisiere = session.query(Fisier).all()
print("Fisierele din baza de date sunt:")
for f in fisiere:
    print(f.nume, f.marime)

# --------
# UPDATE 
# --------
fisier = session.query(Fisier).filter_by(nume="test.txt").first()
if fisier:
    fisier.marime = 2048
    session.commit()
    print("Fisier modificat cu succes")


# --------
# DELETE 
# --------
fisier = session.query(Fisier).filter_by(nume="test.txt").first()
if fisier:
    session.delete(fisier)
    session.commit()
    print("Fisier sters cu succes")
