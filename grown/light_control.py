import asyncio
import time

from grown.store import storage
from server import json


async def _ligthing_control_task(enable_func, disable_func, safety_function):
    """
    all parameter are async functions and running in an infinite loop.
    control parameter

    :param enable_func: no parameter just enable light
    :param disable_func: no parameter just enable light
    :param safety_function: in case of an error this function is called. only parameter will be last sensor_reads
    """
    data_leaf = storage.get_leaf('lighting_control')
    sensor_data_leaf = storage.get_leaf('sensor_data')
    while data_leaf is not None:
        data = data_leaf.get()
        current_time = time.time()
        # only need time by day
        sensor_data = sensor_data_leaf.get()
        result = await safety_function(sensor_data)
        if result is not True:
            switch_on_time = data['switch_on_time']
            switch_off_time = data['switch_off_time']
            # if switching off lies in the next day
            if switch_on_time > switch_off_time:
                switch_off_time += 24 * 60 * 60
            # Light on
            if switch_on_time <= current_time <= switch_off_time:
                # Light off
                await enable_func()
            else:
                await disable_func()

        await asyncio.sleep(100)


async def _get_light_control_data(writer, request):
    """
    path for actual data
    """
    data_leaf = storage.get_leaf('lighting_control')
    return json(writer, data_leaf.get())


async def _post_light_control_data(writer, request):
    raise
    data_leaf = storage.get_leaf('lighting_control')
    return json(writer, data_leaf.get())


def add_light_control(grown_server, enable_func, disable_func, safety_function=None):
    """
    Adds an element controling light to the plants. Further it sets up a task regulating the light which can be
    configured via rest allowing other tasks from outside to optimise the task at hand.

    :type grown_server: grown.server.GrownWebServer
    :param enable_func: async function to enable light
    :param disable_func: async function to disable light
    :param safety_function:
    :return:
    """
    storage.register_leaf(
        'lighting_control',
        {
            'switch_on_time': 11 * 3600,
            'switch_off_time': 23 * 3600
        }
    )
    # create lighting task based on set settings
    loop = asyncio.get_event_loop()
    loop.create_task(
        _ligthing_control_task(enable_func, disable_func, safety_function)
    )
    # create subserver for light control
    grown_server.add_route("/rest/light_control", _get_light_control_data)
    grown_server.add_route("/rest/light_control", _post_light_control_data, 'POST')
