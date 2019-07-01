import gc

gc.collect()
from grown import setup, run_grown
from grown.light_control import add_light_control
from grown.data_control import add_data_control

router = setup()
add_data_control(router, lambda: {'data': 1, 'more sensor': 2.0})


def _enable():
    print("heja enabled light")


def _disable():
    print("heja disabled light")


add_light_control(router, _enable, _disable)

run_grown()
