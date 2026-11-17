
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def encriptar_password(password: str):
    return password_hash.hash(password)

def verificar_password(password: str, hash_guardado: str):
    return password_hash.verify(password, hash_guardado)
