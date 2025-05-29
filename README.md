# Sistem local de management al cheilor de criptare

## Autori
Caraman Talida, Pricop Matei-Ioan  
Grupa 1409A  
Coordonator: Tudorache Alexandru-Gabriel

## Descriere generală
Aplicație locală care permite criptarea și decriptarea fișierelor folosind algoritmi simetrici (AES) și asimetrici (RSA), utilizând framework-urile OpenSSL și LibreSSL. Toate operațiile efectuate sunt salvate într-o bază de date relațională împreună cu performanțele măsurate (timp, memorie, hash).

## Funcționalități principale
- Criptare și decriptare fișiere
- Alegerea algoritmului și framework-ului
- Generare chei RSA și salvare în baza de date
- Calcul hash SHA-256 și verificare integritate
- Măsurare timp execuție și memorie utilizată
- Vizualizare performanțe și calcul medii
- Interfață grafică realizată cu Tkinter

## Structura bazei de date
Tabele principale:
- `fisier`
- `algoritm_criptare`
- `cheie_simetrica`, `cheie_asimetrica`
- `framework`
- `performanta`

## Tehnologii utilizate
- Python 3, Tkinter
- SQLAlchemy + MySQL
- OpenSSL, LibreSSL (prin subprocess)
- hashlib, psutil

## Observații
Cheile RSA sunt stocate ca text în baza de date. Performanțele sunt salvate și vizualizate în interfață. Compararea integrității se face prin hash SHA-256.
