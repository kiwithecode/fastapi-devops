from jose import jwt
from datetime import datetime, timedelta, timezone


SECRET_KEY = "uNs3Cr3t0-larg0-y-coMpL3j0"


def verify_apikey(header_key: str, expected_key: str) -> bool:
    return header_key == expected_key


def generate_jwt(data: dict) -> str:
    payload = data.copy()
    payload.update({
        "exp": datetime.now(timezone.utc) + timedelta(seconds=60)
    })
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
