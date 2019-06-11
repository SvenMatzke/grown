import asyncio
import gc
import os
import time
from grown import storage
from .server import json

_history_sensor_data_file = "sensor_data_log.json"


async def _trim_sensor_data(total_lines, keep_lines):
    os.rename(_history_sensor_data_file, "temp.json")
    file_ptr = open("temp.json", "r")
    for _ in range(0, total_lines - keep_lines):
        file_ptr.readline()
        gc.collect()
    new_file_ptr = open(_history_sensor_data_file, "a")
    while True:
        read = file_ptr.readline()
        if read == "":
            break
        else:
            new_file_ptr.write(read)
        gc.collect()

    new_file_ptr.close()
    file_ptr.close()
    os.remove("temp.json")


async def _save_sensor_data(sensor_data):
    string_to_write = json.dumps(sensor_data) + "\n"
    file_ptr = open(_history_sensor_data_file, "a")
    file_ptr.write(json.dumps(sensor_data) + "\n")
    end_byte = file_ptr.tell()
    file_ptr.close()
    assumed_total_lines = int(end_byte) // len(string_to_write)
    if assumed_total_lines > 1200:
        await _trim_sensor_data(assumed_total_lines, 1000)


def _update_reducer(store_dict, data):
    """
    :type store_dict: dict
    :type data: dict
    :rtype: dict
    """
    # TODO safe to history and safe to store
    return store_dict.update(data)


async def _sensor_data_task(get_sensor_data):
    """
    task for continues logging
    """
    sensor_data_leaf = storage.get_leaf('sensor_data')

    while True:
        new_sensor_data = dict(time=time.time())
        new_sensor_data.update(await get_sensor_data())
        sensor_data_leaf.update(new_sensor_data)
        # TODO sleep from settings
        await asyncio.sleep(60)


async def _get_sensor_data(writer, request):
    """
    path for actual data
    """
    data_leaf = storage.get_leaf('sensor_data')
    return json(writer, data_leaf.get())


def configure_data_sync(grown_server, gather_data_func):
    """
    :type grown_server: grown.server.GrownWebServer
    :param gather_data_func: gather data function
    """
    # create tasks
    loop = asyncio.get_event_loop()

    storage.register_leaf('sensor_data', {}, _update_reducer)
    loop.create_task(_sensor_data_task(gather_data_func))

    # adding routes
    grown_server.add_route("/rest/sensor_data", _get_sensor_data)
    # TODO history data


