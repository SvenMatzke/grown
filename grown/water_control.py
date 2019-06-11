def add_watering_control(grown_server, enable_func, disable_func, safety_function=None):
    """

    Adds an element controling water supply to the plants.
    Further it sets up a task regulating the water which can be configured via rest allowing other tasks from outside to
    optimise the task at hand.
    :type grown_server: grown.server.GrownWebServer
    :param enable_func: async function to enable watering
    :param disable_func: async function to disable watering
    :param safety_function:
    :return:
    """
    raise