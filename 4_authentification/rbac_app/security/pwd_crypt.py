from passlib.hash import pbkdf2_sha256


def encode_password(password: str) -> str:
    encoded_password = pbkdf2_sha256.hash(password)
    return encoded_password


def verify_password(password: str, hashed_db_password) -> bool:
    return pbkdf2_sha256.verify(password, hashed_db_password)
