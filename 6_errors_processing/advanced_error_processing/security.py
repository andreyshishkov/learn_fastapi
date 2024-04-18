from passlib.hash import pbkdf2_sha256


def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def verify_password(password, hashed_db_password) -> bool:
    return pbkdf2_sha256.verify(password, hashed_db_password)
