
import bcrypt

"""
Rounds: bcrypt cost factor -> nomnre de repetitions du calcul interne.
    - exponentiel: veut dire rounds=12 -> 2^12 ( 4096 repetitions ) 
    - 12 : bon equilibre vitesse/resistance

ENCODING: regle de conversion entre str (lecture humaine) et bytes.
    - utf-8: standard universel
""" 
ROUNDS = 12
ENCODING = 'utf-8'
MAX_PASSWORD_BYTES = 72

def hash_pw(
        plain_pw:str,
        personal_encoding: str = ENCODING, 
        personal_rounds: int = ROUNDS,
        max_pw_len: int = MAX_PASSWORD_BYTES,
        ) -> str: 
    """
        Check new password len and generate a hashed password (str).   
        Args:
            - plain_pw: str -> data you want to hash.
            - personal_encoding: str -> encoding type you want [default = 'utf-8'].
            - personal_rounds: int -> complexity of salt [default = 12].
            - max_pw_len: int -> maximum lenght of password in bytes.

        Return:
            - hashed password for DB ( str ).
        Error:
            - raise ValueError if too long password to hash 
    """
    b_pw: bytes = plain_pw.encode(encoding=personal_encoding) 
    if len(b_pw) > max_pw_len:
        raise ValueError('new password too long...')
    s: bytes = bcrypt.gensalt(rounds=personal_rounds)
    return bcrypt.hashpw(b_pw, s).decode(encoding=personal_encoding)


def verify_pw(
        plain_pw: str,
        db_hashed_pw: str,
        personal_encoding: str = ENCODING, 
        ) -> bool:
    """
        Check if password feet with the DB.
        Args:
            - plain_pw: str -> the password who sant to check.
            - db_hashed_pw: str -> the hashed password in the DB.
            - personal_encoding: str -> encoding type you want [default = 'utf-8'].
        Return:
            - True on success, else False
    """
    # les deux doivent etre en bytes:
    plain_pw_b: bytes = plain_pw.encode(encoding=personal_encoding)
    db_hashed_pw_b: bytes = db_hashed_pw.encode(encoding=personal_encoding)

    return bcrypt.checkpw(plain_pw_b, db_hashed_pw_b)










