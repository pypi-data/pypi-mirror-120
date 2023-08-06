import logging
import os
from typing import Any, Callable, List, Optional, Sequence, Union

import socketio
from starlette.applications import Starlette
from starlette.authentication import requires
from starlette.config import Config
from starlette.middleware import Middleware
from starlette.routing import BaseRoute, Mount, Route
from starlette.staticfiles import PathLike, StaticFiles
from starlette.types import ASGIApp

from .types import Callback, Service

# @todo https://nuculabs.dev/2021/05/18/fastapi-uvicorn-logging-in-production/
# logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


class Api:
    """
    Manage a web API
    """

    def __init__(
        self,
        app: Starlette,
        name: str,
        version: int,
        *,
        scopes: Union[str, Sequence[str]] = None,
        status_code: int = 403,
        redirect: str = None,
    ) -> None:
        self.app = app
        self.name = name
        self.version = version
        self.urls: dict[str, str] = {}
        self.shield = requires(scopes, status_code, redirect) if scopes else None

    def add_route(
        self,
        path: str,
        endpoint: Callable,
        *,
        methods: List[str] = None,
        name: Optional[str] = None,
        include_in_schema: bool = True,
    ) -> None:
        func = self.shield(endpoint) if self.shield else endpoint
        real_path = f"/api/{self.name}/v{self.version}" + path  # TODO: format as pref
        if name:
            self.urls[name] = real_path
        self.app.add_route(
            real_path,
            func,
            methods=methods,
            name=f"{self.name}-{name}" if name else None,
            include_in_schema=include_in_schema,
        )

    def url_for(self, name: str) -> Optional[str]:
        return self.urls.get(name, None)


class Configuration(Config):
    def __init__(self) -> None:
        super().__init__(os.environ.get("RUTENI_CONFIG", ".env"))
        self.routes: list[Union[Route, Mount]] = []
        self.middleware: list[Middleware] = []
        self.on_startup: list[Callable] = []
        self.on_shutdown: list[Callable] = []
        self.starlette: dict[str, list[Any]] = dict(
            routes=self.routes,
            middleware=self.middleware,
            on_startup=self.on_startup,
            on_shutdown=self.on_shutdown,
        )
        self.socketio: dict[str, Any] = {}
        self.asgi: dict[str, Any] = {}
        self.services: list[Service] = []

    def set(self, key: str, value: Any) -> None:
        self.environ[key] = value

    @property
    def env(self) -> str:
        return self.get("RUTENI_ENV", default="production")

    @property
    def is_devel(self) -> bool:
        return self.env == "development"

    @property
    def is_debug(self) -> bool:
        return self.get("RUTENI_DEBUG", cast=bool, default=False)

    def add_service(self, name: str, startup: Callback, shutdown: Callback) -> Service:
        service = Service(name=name, startup=startup, shutdown=shutdown)
        self.services.append(service)
        return service

    def create_public_api(self, name: str, version: int) -> Api:
        return Api(self, name, version)

    def create_protected_api(
        self,
        name: str,
        version: int,
        scopes: Union[str, Sequence[str]],
        *,
        status_code: int = 403,
        redirect: str = None,
    ) -> Api:
        return Api(
            self,
            name,
            version,
            scopes=scopes,
            status_code=status_code,
            redirect=redirect,
        )

    def add_middleware(self, cls: type, **options: Any) -> Middleware:
        middleware = Middleware(cls, **options)
        self.middleware.append(middleware)
        return middleware

    def add_route(
        self,
        path: str,
        endpoint: Callable,
        *,
        methods: List[str] = None,
        name: str = None,
        include_in_schema: bool = True,
    ) -> Route:
        route = Route(
            path,
            endpoint,
            methods=methods,
            name=name,
            include_in_schema=include_in_schema,
        )
        self.routes.append(route)
        return route

    def add_mount(
        self,
        path: str,
        app: ASGIApp = None,
        routes: Sequence[BaseRoute] = None,
        name: str = None,
    ) -> Mount:
        mount = Mount(path, app, routes, name)
        self.routes.append(mount)
        return mount

    def add_static(
        self,
        path: str,
        directory: PathLike = None,
        packages: List[str] = None,
        html: bool = False,
        check_dir: bool = True,
    ) -> Mount:
        return self.add_mount(
            path,
            app=StaticFiles(
                directory=directory, packages=packages, html=html, check_dir=check_dir
            ),
        )

    def add_event_handler(self, event_type: str, func: Callable) -> None:
        assert event_type in ("startup", "shutdown")
        if event_type == "startup":
            self.on_startup.append(func)
        else:
            self.on_shutdown.append(func)

    def use_redis(
        self, uri: str = "redis+unix:///var/run/redis/redis-server.sock"
    ) -> None:
        self.socketio["client_manager"] = socketio.AsyncRedisManager(uri)


configuration = Configuration()


class Ruteni(socketio.ASGIApp):
    def __init__(self) -> None:
        configuration.add_event_handler("startup", self._start_services)
        configuration.add_event_handler("shutdown", self._stop_services)
        super().__init__(
            socketio.AsyncServer(async_mode="asgi", **configuration.socketio),
            Starlette(debug=configuration.is_debug, **configuration.starlette),
            **configuration.asgi,
        )
        self.other_asgi_app.state.sio = self.engineio_server
        self.shutdown_callbacks: list[Service] = []

    async def _start_services(self) -> None:
        try:
            for service in configuration.services:
                await service.startup(self.other_asgi_app)
                self.shutdown_callbacks.append(service)
        except BaseException:
            logger.exception("start")
            await self._stop_services()
            raise

    async def _stop_services(self) -> None:
        while len(self.shutdown_callbacks):
            service = self.shutdown_callbacks.pop()
            try:
                await service.shutdown(self.other_asgi_app)
            except Exception:
                logger.exception("stop")
