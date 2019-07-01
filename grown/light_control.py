import time

from grown.store import storage
from userv.routing import json_response, text_response

try:
    import ujson as json
except ImportError:
    import json
try:
    import uasyncio as asyncio
except ImportError:
    import asyncio


async def _ligthing_control_task(enable_func, disable_func, safety_function):
    """
    all parameter are async functions and running in an infinite loop.
    control parameter

    :param enable_func: no parameter just enable light
    :param disable_func: no parameter just enable light
    :param safety_function: in case of an error this function is called. only parameter will be last sensor_reads
    """
    if safety_function is None:
        safety_function = lambda x: True
    data_leaf = storage.get_leaf('lighting_control')
    sensor_data_leaf = storage.get_leaf('sensor_data')
    while data_leaf is not None:
        data = data_leaf.get()
        current_time = time.time()
        # only need time by day
        sensor_data = sensor_data_leaf.get()

        result = safety_function(sensor_data)
        if isinstance(safety_function, type(lambda: (yield))):
            result = await result
        if result is not True:
            switch_on_time = data['switch_on_time']
            switch_off_time = data['switch_off_time']
            # if switching off lies in the next day
            if switch_on_time > switch_off_time:
                switch_off_time += 24 * 60 * 60
            # Light on
            if switch_on_time <= current_time <= switch_off_time:
                # Light off
                enable = enable_func()
                if isinstance(enable_func, type(lambda: (yield))):
                    await enable
            else:
                disable = disable_func()
                if isinstance(disable_func, type(lambda: (yield))):
                    await disable

        await asyncio.sleep(100)


async def _get_light_control_data(request):
    """
    path for actual data
    """
    data_leaf = storage.get_leaf('lighting_control')
    return json_response(data_leaf.get())


async def _post_light_control_data(request):
    leaf = storage.get_leaf('lighting_control')
    try:
        new_lighting_control = json.loads(request.get('body', ""))
        leaf.update(new_lighting_control)
        return json_response(new_lighting_control)
    except Exception as e:
        return text_response(str(e), status=400)


def _update_reducer(store_dict, data):
    """
    :type store_dict: dict
    :type data: dict
    :rtype: dict
    """
    return store_dict.update(data)


def add_light_control(router, enable_func, disable_func, safety_function=None):
    """
    Adds an element controling light to the plants. Further it sets up a task regulating the light which can be
    configured via rest allowing other tasks from outside to optimise the task at hand.

    :type router: user.routing.Router
    :param enable_func: async function to enable light
    :param disable_func: async function to disable light
    :param safety_function:
    """
    assert callable(enable_func) is True, "enable_func is not callable"
    assert callable(disable_func) is True, "enable_func is not callable"
    storage.register_leaf(
        'lighting_control',
        {
            'switch_on_time': 11 * 3600,
            'switch_off_time': 23 * 3600
        },
        _update_reducer
    )
    # create lighting task based on set settings
    loop = asyncio.get_event_loop()
    loop.create_task(
        _ligthing_control_task(enable_func, disable_func, safety_function)
    )
    # create subserver for light control
    router.add("/rest/light_control", _get_light_control_data, 'GET')
    router.add("/rest/light_control", _post_light_control_data, 'POST')
