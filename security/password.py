import bcrypt
from DB.ORM import *
from security.TOTP import check2fa
import os, hashlib

def authenticate(user_name, passwd, totp_token):
    with Session(engine) as session:
        user: User = session.query(User).filter(User.Name == user_name).first()
        if not user:
            raise Exception("Login inválido")
        is_pass_ok = _check_password(user.PasswordHash, passwd)
        if not is_pass_ok:
            raise Exception("Login inválido")

        if user.TwoFactorKey is not None and len(user.TwoFactorKey) == 32:
            totp_ok = check2fa(user.TwoFactorKey, totp_token)
            if not totp_ok:
                raise Exception("Login inválido")

        return user


def hash_password(password: str):
    hash_value = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hash_value.decode('utf-8')

def _check_password(stored_hash: str, provided_password: str) -> bool:
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash.encode('utf-8'))