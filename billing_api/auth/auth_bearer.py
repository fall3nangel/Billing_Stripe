from http import HTTPStatus
from typing import Any, Dict, Optional

from fastapi import HTTPException, Request
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .auth_handler import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN,
                    detail="Invalid authentication scheme.",
                )
            if not (payload := self.verify_jwt(credentials.credentials)):
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN,
                    detail="Invalid token or expired token.",
                )
            request.state.user_id = payload["user_id"]
            return ORJSONResponse(credentials.credentials)
        else:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail="Invalid authorization code."
            )

    def verify_jwt(self, token: str) -> Optional[Dict[Any, Any]]:
        try:
            payload = decode_jwt(token)
        except:
            payload = None
        return payload


auth = JWTBearer()
