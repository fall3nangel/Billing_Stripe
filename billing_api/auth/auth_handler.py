import time
from typing import Any, Dict, Optional

import jwt

from core.config import settings


def encode_jwt(user_id: str) -> dict[str, str]:
    payload = {"user_id": str(user_id), "exp": time.time() + 600}
    token = jwt.encode(
        payload,
        settings.users_app.jwt_secret_key,
        algorithm=settings.users_app.algorithm,
    )

    return {"access_token": token}


def decode_jwt(token: str) -> Optional[Dict[Any, Any]]:
    try:
        decoded_token = jwt.decode(
            token,
            settings.users_app.jwt_secret_key,
            algorithms=[settings.users_app.algorithm],
        )
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except:
        return {}
