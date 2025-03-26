from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship
from database import engine
import datetime

Base = declarative_base()

class Fisier(Base):
    __tablename__ = "fisier"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nume = Column(String(255), nullable=False)
    cale = Column(String(500), nullable=False)
    marime = Column(BigInteger, nullable=False)
    format = Column(String(50), nullable=False)
    data_upload = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    performante = relationship("Performanta", back_populates="fisier")

class CheieSimetrica(Base):
    __tablename__ = "cheie_simetrica"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cheie = Column(String(500), nullable=False)
    tip = Column(String(10), nullable=False)
    lungime = Column(Integer, nullable=False)
    id_algoritm = Column(Integer, ForeignKey("algoritm_criptare.id"), nullable=False)

class CheieAsimetrica(Base):
    __tablename__ = "cheie_asimetrica"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cheie_publica = Column(String(500), nullable=False)
    cheie_privata = Column(String(500), nullable=False)
    tip = Column(String(10), nullable=False)
    lungime = Column(Integer, nullable=False)
    id_algoritm = Column(Integer, ForeignKey("algoritm_criptare.id"), nullable=False)

class Framework(Base):
    __tablename__ = "framework"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nume = Column(String(100), nullable=False, unique=True)
    versiune = Column(String(50), nullable=False)


class AlgoritmCriptare(Base):
    __tablename__ = "algoritm_criptare"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nume = Column(String(100), nullable=False, unique=True)
    tip = Column(String(10), nullable=False) 
    lungime_cheie = Column(Integer, nullable=False)

class Performanta(Base):
    __tablename__ = "performanta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_fisier = Column(Integer, ForeignKey("fisier.id"), nullable=False)
    id_algoritm = Column(Integer, ForeignKey("algoritm_criptare.id"), nullable=False)
    id_framework = Column(Integer, ForeignKey("framework.id"), nullable=False)
    tip_operatie = Column(String(10), nullable=False)
    rezultat_hash = Column(String(256), nullable=True)
    timp_executie = Column(Integer, nullable=False)
    memorie_utilizata = Column(Integer, nullable=False)
    data_criptare = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    fisier = relationship("Fisier", back_populates="performante")
    algoritm = relationship("AlgoritmCriptare")
    framework = relationship("Framework")


    

Base.metadata.create_all(engine)  
