#!/usr/bin/python3 -W ignore::DeprecationWarning
import unittest
from test import UvicornTestServer
from unittest import IsolatedAsyncioTestCase

from ruteni import Ruteni
from socketio import AsyncClient


class PresenceTest(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.server = UvicornTestServer(Ruteni())

    async def asyncSetUp(self) -> None:
        await self.server.up()
        self.sio = AsyncClient(reconnection=False)
        self.sio.on("connect", lambda: print("connected"))
        self.sio.on("connect_error", lambda: print("The connection failed!"))
        self.sio.on("disconnect", lambda: print("I'm disconnected!"))
        self.sio.on("*", lambda *args: print(args))
        await self.sio.connect("http://localhost:8000", transports=["websocket"])
        print("my sid is", self.sio.sid)

    async def test_response(self) -> None:
        print("test_response")
        try:
            await self.sio.emit("test")
        except Exception as e:
            print("error:", e)

    async def asyncTearDown(self) -> None:
        await self.sio.disconnect()
        await self.server.down()

    def tearDown(self) -> None:
        print("done")


if __name__ == "__main__":
    unittest.main()
