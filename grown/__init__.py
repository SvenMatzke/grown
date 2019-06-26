from .store import storage as _storage
from userv.routing import Router as _Router
from userv.async_server import run_server as _runserver
from .wlan import connect_and_configure_wlan as _connect_and_configure_wlan
from .time_control import time_sync_task as _time_sync_task
try:
    import uasyncio as asyncio
except ImportError:
    import asyncio


def setup():
    """
    setting up grown tasks server

    This setup provides basic functions like connection to wlan or setting up a regular hotspot.

    configurable by a rest interface
    further functions can be added by each control

    :rtype: userv.routing.Router
    """

    # create tasks
    loop = asyncio.get_event_loop()
    # setup time sync
    loop.create_task(_time_sync_task())

    # adding routes
    # routes can be added till a run is triggered
    router = _Router()

    # configurable tasks
    # wlan
    _connect_and_configure_wlan(router)

    # TODO add also swagger ui

    # adding async webserver
    _runserver(router)
    return router


def run_grown():
    """
    runs a grown application
    """
    asyncio.get_event_loop().run_forever()
