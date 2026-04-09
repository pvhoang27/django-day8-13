from dataclasses import dataclass

import jwt
from django.conf import settings
from rest_framework import authentication, exceptions


@dataclass
class ServiceUser:
    id: int

    @property
    def is_authenticated(self) -> bool:
        return True


class ServiceJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        header = authentication.get_authorization_header(request).decode("utf-8")
        if not header:
            return None

        parts = header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise exceptions.AuthenticationFailed("Invalid authorization header format.")

        token = parts[1]
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SIGNING_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
        except jwt.InvalidTokenError as exc:
            raise exceptions.AuthenticationFailed("Invalid token.") from exc

        user_id = payload.get("user_id")
        if not user_id:
            raise exceptions.AuthenticationFailed("Token missing user_id.")

        return ServiceUser(id=user_id), payload
