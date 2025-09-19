
from hashlib import sha256

def anonymize_email(email: str) -> str:
    """Hash simples para anonimizar; evita armazenar PII em claro."""
    return sha256(email.lower().encode("utf-8")).hexdigest()
