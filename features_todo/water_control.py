
# TODO default safety function
# TODO rest interface
# TODO control_task
# TODO enable and disable need to be wraped for safety
# => instead of safety function may be some mechanism todetermine the datas value to safety and enable or disable water
# lazy and slow adjusting the water overtime with parameter like activate only 2 s then wait for 60 seconds and so on
# also regulating to the middle of 2 ranges.

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