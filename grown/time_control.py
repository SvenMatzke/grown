"""
module for time
"""
import machine
import utime
from .logging import grown_log

try:
    import uasyncio as asyncio
except ImportError:
    import asyncio
try:
    import usocket as socket
except ImportError:
    import socket
try:
    import ustruct as struct
except ImportError:
    import struct

# (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
NTP_DELTA = 3155673600

host = "pool.ntp.org"


def _set_system_time(ntp_time):
    """
    There's currently no timezone support in MicroPython, so
    utime.localtime() will return UTC time (as if it was .gmtime())
    """
    tm = utime.localtime(ntp_time)
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    machine.RTC().datetime(tm)
    grown_log.info(str(utime.localtime()))


async def _time_from_server():
    # TODO use async socket
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1b
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)
    res = s.sendto(NTP_QUERY, addr)
    msg = s.recv(48)
    s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    return val - NTP_DELTA


async def time_sync_task(time_between_syncs_s=300):
    """
    task for synchronising time
    """
    while True:
        try:
            server_time = await _time_from_server()
            _set_system_time(server_time)
        except Exception as e:
            grown_log.error(str(e))

        await asyncio.sleep(time_between_syncs_s)


def get_current_time():
    """
    retuns the current hh:mm:ss in seconds
    :rtype: int
    """
    current_time = utime.time()
    return current_time % (60*60*24)
