from datetime import UTC, datetime

from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from pwdlib import PasswordHash

from .core.config import get_settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def _serializer() -> URLSafeTimedSerializer:
    secret_key = get_settings().secret_key
    if not secret_key:
        raise RuntimeError("SECRET_KEY must be configured before creating session tokens.")
    return URLSafeTimedSerializer(secret_key, salt="thermocomposite-session")


def create_session_token(subject: str) -> str:
    return _serializer().dumps({"sub": subject, "iat": datetime.now(UTC).isoformat()})


def decode_session_token(token: str) -> str | None:
    try:
        payload = _serializer().loads(token, max_age=get_settings().session_ttl_seconds)
    except (BadSignature, SignatureExpired):
        return None
    subject = payload.get("sub")
    return subject if isinstance(subject, str) and subject else None
