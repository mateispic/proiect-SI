import subprocess

LIBRESSL_PATH = "/opt/homebrew/opt/libressl/bin/openssl"


def rsa_encrypt_libressl(input_path, output_path, public_key_path):
    try:
        subprocess.run([
            LIBRESSL_PATH, "rsautl", "-encrypt",
            "-inkey", public_key_path,
            "-pubin",
            "-in", input_path,
            "-out", output_path
        ], check=True)
        print("Criptare RSA realizata cu succes.")
    except subprocess.CalledProcessError as e:
        print("Eroare la criptare RSA:", e)



def rsa_decrypt_libressl(input_path, output_path, private_key_path):
    try:
        subprocess.run([
            LIBRESSL_PATH, "rsautl", "-decrypt",
            "-inkey", private_key_path,
            "-in", input_path,
            "-out", output_path
        ], check=True)
        print("Decriptare RSA realizata cu succes.")
    except subprocess.CalledProcessError as e:
        print("Eroare la decriptare RSA:", e)

def generate_rsa_keys_libressl(private_path="/Users/admin/Desktop/SI-Proiect/private_key.pem", public_path="/Users/admin/Desktop/SI-Proiect/public_key.pem"):
    subprocess.run([LIBRESSL_PATH, "genrsa", "-out", private_path, "1024"], check=True)
    subprocess.run([LIBRESSL_PATH, "rsa", "-in", private_path, "-pubout", "-out", public_path], check=True)




def aes_encrypt_libressl(input_path, output_path, key):
    try:
        subprocess.run([
            LIBRESSL_PATH, "enc", "-aes-128-cbc", "-salt",
            "-in", input_path,
            "-out", output_path,
            "-k", key
        ], check=True)
        print("Criptare AES realizata cu succes.")
    except subprocess.CalledProcessError as e:
        print("Eroare la criptare AES:", e)

def aes_decrypt_libressl(input_path, output_path, key):
    try:
        subprocess.run([
            LIBRESSL_PATH, "enc", "-aes-128-cbc", "-d",
            "-in", input_path,
            "-out", output_path,
            "-k", key
        ], check=True)
        print("Decriptare AES realizata cu succes.")
    except subprocess.CalledProcessError as e:
        print("Eroare la decriptare AES:", e)

