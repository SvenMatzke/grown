# import gc
# import os
import time
from .store import storage
from userv.routing import json_response
from .logging import grown_log

try:
    import uasyncio as asyncio
except ImportError:
    import asyncio


# TODO history of data
# _history_sensor_data_file = "sensor_data_log.json"


# async def _trim_sensor_data(total_lines, keep_lines):
#     os.rename(_history_sensor_data_file, "temp.json")
#     file_ptr = open("temp.json", "r")
#     for _ in range(0, total_lines - keep_lines):
#         file_ptr.readline()
#         gc.collect()
#     new_file_ptr = open(_history_sensor_data_file, "a")
#     while True:
#         read = file_ptr.readline()
#         if read == "":
#             break
#         else:
#             new_file_ptr.write(read)
#         gc.collect()
#
#     new_file_ptr.close()
#     file_ptr.close()
#     os.remove("temp.json")
#
#
# async def _save_sensor_data(sensor_data):
#     string_to_write = json.dumps(sensor_data) + "\n"
#     file_ptr = open(_history_sensor_data_file, "a")
#     file_ptr.write(json.dumps(sensor_data) + "\n")
#     end_byte = file_ptr.tell()
#     file_ptr.close()
#     assumed_total_lines = int(end_byte) // len(string_to_write)
#     if assumed_total_lines > 1200:
#         await _trim_sensor_data(assumed_total_lines, 1000)


def _update_reducer(store_dict, data):
    """
    :type store_dict: dict
    :type data: dict
    :rtype: dict
    """
    new_sensor_data = dict(time=time.time())
    new_sensor_data.update(data)
    return new_sensor_data


async def _sensor_data_task(get_sensor_data):
    """
    task for continues logging
    """
    sensor_data_leaf = storage.get_leaf('sensor_data')

    while True:
        try:
            if isinstance(get_sensor_data, type(lambda: (yield))):
                data = await get_sensor_data()
            else:
                data = get_sensor_data()
            sensor_data_leaf.update(data)
            # TODO sleep from settings
            await asyncio.sleep(60)
        except Exception as e:
            grown_log.error(str(e))


async def _get_sensor_data(request):
    """
    path for actual data
    """
    data_leaf = storage.get_leaf('sensor_data')
    return json_response(data_leaf.get())


def add_data_control(router, gather_data_func):
    """
    :type router: userv.routing.Router
    :param gather_data_func: gather data function
    """
    grown_log.info("Adding data control to grown.")
    try:
        assert callable(gather_data_func) is True, "gather_data_func is not callable"
        # create tasks
        loop = asyncio.get_event_loop()

        storage.register_leaf('sensor_data', {'time': time.time()}, _update_reducer)
        loop.create_task(_sensor_data_task(gather_data_func))

        # adding routes
        router.add("/rest/sensor_data", _get_sensor_data)
    except Exception as e:
        grown_log.error(str(e))
    # TODO history data
