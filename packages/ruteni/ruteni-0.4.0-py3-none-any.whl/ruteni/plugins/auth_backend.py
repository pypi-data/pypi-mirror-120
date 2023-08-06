import logging
from typing import Callable, Tuple

from ruteni import configuration
from ruteni.plugins.session import UserType, get_session_user
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    BaseUser,
    UnauthenticatedUser,
)
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import Request

logger = logging.getLogger(__name__)

AuthPair = Tuple[AuthCredentials, BaseUser]
AuthFunc = Callable[[UserType], AuthPair]

providers: dict[str, AuthFunc] = {}


def register_identity_provider(name: str, func: AuthFunc) -> None:
    providers[name] = func


class SessionAuthenticationBackend(AuthenticationBackend):
    async def authenticate(self, request: Request) -> AuthPair:
        user = get_session_user(request)
        if user is not None:
            for provider, func in providers.items():
                if user["provider"] == provider:
                    return func(user)
            logger.warn(f'unknown identity provider: {user["provider"]}')
        return AuthCredentials(), UnauthenticatedUser()


configuration.add_middleware(
    AuthenticationMiddleware, backend=SessionAuthenticationBackend()
)

logger.info("loaded")
