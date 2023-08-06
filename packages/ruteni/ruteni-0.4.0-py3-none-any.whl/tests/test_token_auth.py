import asyncio
import sqlite3
from test.support import EnvironmentVarGuard
from unittest import IsolatedAsyncioTestCase

from ruteni import Ruteni
from starlette.testclient import TestClient

from .config import (
    CLIENT_ID,
    DATABASE_PATH,
    USER_EMAIL,
    USER_LOCALE,
    USER_NAME,
    USER_PASSWORD,
)

env = EnvironmentVarGuard()
env.set("RUTENI_DATABASE_URL", "sqlite:///" + DATABASE_PATH)

with env:
    import ruteni.plugins.token_auth
    from ruteni.plugins.passwords import register_user


class TokenAuthTestCase(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.app = Ruteni()

    def test_login(self) -> None:
        with TestClient(self.app) as client:
            asyncio.run(
                register_user(USER_NAME, USER_EMAIL, USER_LOCALE, USER_PASSWORD)
            )
            # conn = sqlite3.connect(DATABASE_PATH)
            # cursor = conn.cursor()
            # cursor.execute(
            #     "INSERT INTO users VALUES(2,'username','username@bar.fr',2,'2021-09-20 11:57:25',NULL)"
            # )
            # cursor.execute(
            #     "INSERT INTO passwords VALUES(1,2,'$2a$06$4eO8HKDXY./w2gLZ.Jq.iuXKTOIP6GFj80JBqiWB6TyWIfdgKFF5e','2021-09-20 11:57:25',NULL)"
            # )

            response = client.get("/")
            assert response.status_code == 404


if __name__ == "__main__":
    import unittest

    unittest.main()
