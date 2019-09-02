from userv import swagger
from .logging import grown_log, configure_logging as _configure_logging
from .store import storage as _storage
from userv.routing import Router as _Router, text_response
from userv.async_server import run_server as _runserver
from .wlan import connect_and_configure_wlan as _connect_and_configure_wlan, _sta_if
from .time_control import add_time_control as _add_time_control
import gc
import upip
import machine
try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

_last_router = None


@swagger.info("get current data from light control")
@swagger.response(500, "Reset will cause this")
def _update_grown(request):
    gc.collect()
    upip.install("grown")
    machine.reset()
    return text_response("Hard reseting after update please wait!", status=200)


def setup():
    """
    setting up grown tasks server

    This setup provides basic functions like connection to wlan or setting up a regular hotspot.

    configurable by a rest interface
    further functions can be added by each control

    :rtype: userv.routing.Router
    """
    # adding tasks
    # routes can be added till a run is triggered
    router = _Router()

    # configurable tasks
    # logging
    _configure_logging(router)

    # time
    _add_time_control(router)

    # wlan
    _connect_and_configure_wlan(router)

    # adding async webserver
    router.add("/rest/update", _update_grown, method="POST")

    _runserver(router)
    global _last_router
    _last_router = router
    return router


def run_grown():
    """
    runs a grown application
    """
    try:
        # need to add swagger before run
        if _last_router is not None:
            _last_router.add(
                "/swagger.json",
                swagger.swagger_file(
                    'Grown swagger api',
                    "Grown",
                    host=_sta_if.ifconfig()[0],
                    router_instance=_last_router
                ),
                method="GET"
            )
        asyncio.get_event_loop().run_forever()
    except Exception as e:
        grown_log.error(str(e))
    finally:
        # TODO save log to file?
        pass
