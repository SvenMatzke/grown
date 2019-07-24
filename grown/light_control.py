from .store import storage
from userv.routing import json_response, text_response
from userv import swagger
from .logging import grown_log
from grown.time_control import get_current_time, seconds_for_one_day

try:
    import ujson as json
except ImportError:
    import json
try:
    import uasyncio as asyncio
except ImportError:
    import asyncio


def _should_light_be_enabled(on_time, off_time, current_time):
    """
    calculated if light should be enabled
    :type on_time: int
    :type off_time: int
    :type current_time: int
    :rtype: bool
    """
    current_time = seconds_for_one_day(current_time)
    # we only watch the last 24 hours
    if on_time > off_time:
        if current_time < on_time and current_time > off_time:
            off_time += 24 * 60 * 60
        else:
            return current_time >= on_time or current_time <= off_time
    return on_time <= current_time <= off_time


async def _light_control_task(enable_func, disable_func, safety_function):
    """
    all parameter are async functions and running in an infinite loop.
    control parameter

    :param enable_func: no parameter just enable light
    :param disable_func: no parameter just enable light
    :param safety_function: safety functions is always called before. returned true if not safe to run
    """
    if safety_function is None:
        safety_function = lambda x: False
    data_leaf = storage.get_leaf('light_control')
    sensor_data_leaf = storage.get_leaf('sensor_data')
    last_state = None
    while data_leaf is not None:
        try:
            data = data_leaf.get()
            current_time = get_current_time()
            # only need time by day
            sensor_data = sensor_data_leaf.get()

            result = safety_function(sensor_data)
            if isinstance(safety_function, type(lambda: (yield))):
                result = await result
            if result is not True:
                switch_on_time = data['switch_on_time']
                switch_off_time = data['switch_off_time']
                if _should_light_be_enabled(switch_on_time, switch_off_time, current_time):
                    # Light on
                    if last_state is not True:
                        grown_log.info("light_control: enable light")
                        last_state = True
                    enable = enable_func()
                    if isinstance(enable_func, type(lambda: (yield))):
                        await enable
                else:
                    # Light off
                    if last_state is not False:
                        grown_log.info("light_control: disable light")
                        last_state = False
                    disable = disable_func()
                    if isinstance(disable_func, type(lambda: (yield))):
                        await disable
        except Exception as e:
            grown_log.error(str(e))
        await asyncio.sleep(100)


@swagger.info("get current data from light control")
async def _get_light_control_data(request):
    """
    path for actual data
    """
    data_leaf = storage.get_leaf('light_control')
    return json_response(data_leaf.get())


@swagger.info("Sets light control")
@swagger.body('light_control',
              summary="Sets an on or off time. time in seconds. max value is 24*3600 seconds.",
              example={
                'switch_on_time': 11 * 3600,
                'switch_off_time': 23 * 3600
            })
async def _post_light_control_data(request):
    leaf = storage.get_leaf('light_control')
    try:
        new_light_control = json.loads(request.get('body', ""))
        leaf.update(new_light_control)
        return json_response(new_light_control)
    except Exception as e:
        return text_response(str(e), status=400)


def _update_reducer(store_dict, data):
    """
    :type store_dict: dict
    :type data: dict
    :rtype: dict
    """
    if data.get('switch_on_time', None) is not None:
        store_dict['switch_on_time'] = data['switch_on_time'] % 24*3600

    if data.get('switch_off_time', None) is not None:
        store_dict['switch_off_time'] = data['switch_off_time'] % 24*3600
    return store_dict


def add_light_control(router, enable_func, disable_func, safety_function=None):
    """
    Adds an element controling light to the plants. Further it sets up a task regulating the light which can be
    configured via rest allowing other tasks from outside to optimise the task at hand.

    :type router: user.routing.Router
    :param enable_func: async function to enable light
    :param disable_func: async function to disable light
    :param safety_function:
    """
    grown_log.info('Adding light control to grown server')
    try:
        assert callable(enable_func) is True, "enable_func is not callable"
        assert callable(disable_func) is True, "enable_func is not callable"
        storage.register_leaf(
            'light_control',
            {
                'switch_on_time': 11 * 3600,
                'switch_off_time': 23 * 3600
            },
            _update_reducer
        )
        # create lighting task based on set settings
        loop = asyncio.get_event_loop()
        loop.create_task(_light_control_task(enable_func, disable_func, safety_function))
        # create subserver for light control
        router.add("/rest/light_control", _get_light_control_data, 'GET')
        router.add("/rest/light_control", _post_light_control_data, 'POST')
    except Exception as e:
        grown_log.error(str(e))
