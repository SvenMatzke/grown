def add_watering_control(router, enable_func, disable_func, safety_function=None):
    """

    Adds an element controling water supply to the plants.
    Further it sets up a task regulating the water which can be configured via rest allowing other tasks from outside to
    optimise the task at hand.
    :type router: userv.routing.Router
    :param enable_func: async function to enable watering
    :param disable_func: async function to disable watering
    :param safety_function:
    :return:
    """
    # TODO i need sensor data and so on
    raise