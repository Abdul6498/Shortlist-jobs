from cryptography.fernet import Fernet

def decrypt(email,password, encoding_type, key, encoder):
    key = bytes(key, encoding=encoder)
    f = Fernet(key)
    email = f.decrypt(bytes(email, encoding=encoder))
    email = email.decode(encoding_type)
    password = f.decrypt(bytes(password, encoding=encoder))
    password = password.decode(encoding_type)

    return email, password
