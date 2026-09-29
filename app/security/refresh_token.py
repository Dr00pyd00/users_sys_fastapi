"""
    le refresh token est juste un str au hasard qui agit comme un id random sans prise pour les hacks.
    on va envoyer ce token au client 
    PUIS le server stock le hash de ce token dans une table
    dans le systeme le client va envoyer le vrai token et le server va le hashwer pour le comparer a la table etc..

"""

import secrets
import hashlib

def generate_refresh_token() -> str:
    """
    Generate a new opaque refresh token.

    Return:
        - random URL-safe string (~43 chars, 256 bits of randomness)
    """
    return secrets.token_urlsafe(32)


def hash_refresh_token(refresh_token: str) -> str:
    """
    Take a refresh_token and hash it with hashlib for db.

    Args:
        - refresh_token: str: the plain one 
    Returns:
        - hashed refresh_token: str
    """
    b_refresh_token: bytes = refresh_token.encode() 
    hash_obj = hashlib.sha256(b_refresh_token)

    return hash_obj.hexdigest()
