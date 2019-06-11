from .store import storage
from .server import GrownWebServer
from data_control import configure_data_sync
from .time_control import time_sync_task
try:
    import uasyncio as asyncio
except ImportError:
    import asyncio


def setup():
    """
    setting up grown tasks server
    This setup provides basic functions like connection to Wlan or setting up a regular Hotspot.
    Also adding rest interface to various functions like settings the logged sensor data and current sensor data.

    All this is returned by a small async web server, which is able to add more tasks and routes

    :param gather_data_func: async function returning a dict with sensor_data
    :rtype: GrownWebServer
    """

    # create tasks
    loop = asyncio.get_event_loop()
    # setup time sync
    loop.create_task(time_sync_task())

    # adding routes
    server_instance = GrownWebServer()
    # TODO add also swagger ui


    return server_instance
