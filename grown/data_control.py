# import gc
# import os
import gc
import os
import time

from userv import swagger, response_header
from .store import storage
from userv.routing import json_response, text_response
from .logging import grown_log

try:
    import uasyncio as asyncio
except ImportError:
    import asyncio
try:
    import ujson as json
except ImportError:
    import json

_history_sensor_data_file = "sensor_data.log"


def _trim_log(file_name):
    """
    if log is over the maximum we trim 10% old logs
    TODO alternative we average the data by 2 elements each
    """
    max_log_size = storage.get_leaf('sensor_config').get('logsize', 5 * 512)
    file_size_in_bytes = os.stat(file_name)[6]
    if file_size_in_bytes <= max_log_size:
        return
    # trim log
    os.rename(file_name, "temp_data.log")
    file_ptr = open("temp_data.log", "r")
    trim_size = int(max_log_size * 0.1)
    sum_trimmed = 0
    while True:
        size = len(file_ptr.readline())
        sum_trimmed += size
        gc.collect()
        if sum_trimmed >= trim_size or size == 0:
            break

    new_file_ptr = open(file_name, "a")
    while True:
        read = file_ptr.readline()
        if read == "":
            break
        else:
            new_file_ptr.write(read)
        gc.collect()

    new_file_ptr.close()
    file_ptr.close()
    os.remove("temp_data.log")


def _history_data_response(headers=None):
    """
    slightly modified file serve to add 2 more braces
    """
    try:
        file_ptr = open(_history_sensor_data_file, "rb")
        firstline = file_ptr.readline()
        for line in response_header(
                status=200,
                content_type="application/json",
                headers=headers
        ):
            yield b"%s" % line
        yield b"[%s" % firstline
        while True:
            read = file_ptr.readline()
            if read == b"":
                break
            else:
                yield b",%s" % read
            gc.collect()
    finally:
        file_ptr.close()
    yield b"]\r\n"


def _update_reducer(store_dict, data):
    """
    :type store_dict: dict
    :type data: dict
    :rtype: dict
    """
    new_sensor_data = dict(time=time.time())
    new_sensor_data.update(data)
    # add to history
    _log_file = open(_history_sensor_data_file, 'a')
    _log_file.write(json.dumps(new_sensor_data) + "\n")
    _log_file.close()
    _trim_log(_history_sensor_data_file)
    return new_sensor_data


def _update_config_reducer(store_dict, data):
    """
    :type store_dict: dict
    :type data: dict
    :rtype: dict
    """
    # gather frequency needs always to be positive and not too fast
    if data.get('gather_frequency', 0) < 30:
        data['gather_frequency'] = 30
    store_dict.update(data)
    return store_dict


async def _sensor_data_task(get_sensor_data):
    """
    task for continues logging
    """
    sensor_data_leaf = storage.get_leaf('sensor_data')
    sensor_configuration = storage.get_leaf('sensor_config')
    while True:
        try:
            if isinstance(get_sensor_data, type(lambda: (yield))):
                data = await get_sensor_data()
            else:
                data = get_sensor_data()
            sensor_data_leaf.update(data)
        except Exception as e:
            grown_log.error("data_control: %s" % str(e))
        await asyncio.sleep(sensor_configuration.get('gather_frequency', 60))


@swagger.info("Returns a dictionary with sensor data and timestamp")
async def _get_sensor_data(request):
    """
    path for actual data
    """
    data_leaf = storage.get_leaf('sensor_data')
    return json_response(data_leaf.get())


@swagger.info("Returns a list of the latest sensordata measured")
async def _get_sensor_data_history(request):
    return _history_data_response()


@swagger.info("gets sensor config like size of log and frequency of data gathering")
async def _get_sensor_config(request):
    sensor_config = storage.get_leaf('sensor_config')
    return json_response(sensor_config.get())


@swagger.info("Sets sensor config")
@swagger.body('SensorConfig',
              summary="sets certain control like data log size and gathering frequency",
              example={
                  'gather_frequency': 60,
                  'logsize': 8 * 512
              })
async def _post_sensor_config(request):
    sensor_config = storage.get_leaf('sensor_config')
    try:
        new_sensor_config = json.loads(request.get('body', ""))
        sensor_config.update(new_sensor_config)
        return json_response(sensor_config.get())
    except Exception as e:
        return text_response("data_control: %s" % str(e), status=400)


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

        storage.register_leaf(
            'sensor_data',
            {'time': time.time()},
            _update_reducer
        )
        storage.register_leaf(
            'sensor_config',
            {
                'gather_frequency': 60,
                'logsize': 8 * 512
            },
            _update_config_reducer
        )
        loop.create_task(_sensor_data_task(gather_data_func))

        # adding routes
        router.add("/rest/sensor/data", _get_sensor_data)
        router.add("/rest/sensor/config", _get_sensor_config)
        router.add("/rest/sensor/config", _post_sensor_config, method="POST")
        router.add("/rest/sensor/history", _get_sensor_data_history)
    except Exception as e:
        grown_log.error("data_control: %s" % str(e))
