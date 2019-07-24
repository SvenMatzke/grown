Grown
=====

Sensorbased plattform to create various tasks, apart from gathering data.
The basic idea is to get a firmware for growing plants taking light and watering into a
hand of a microcontroller.

Requirements
============

Any Micropython board available or further anything which can run micropython.

Installation
============
Update and package installation will all be provided via upip.::

    import upip
    upip.install('grown')

enabling the software and configuration is users choice.
Like the webrepl in python is adding a call in your boot or main.py nesserary for activation
like::

    from grown import setup, run_grown

    router = setup()
    # add more tasks or add site to the router

    run_grown()

Setup of grown starts a timesync task and wlan configuration.
After the run_grown a webserver is opened with a rest interface to change settings for each task.

Swagger
=======
Every action and info you add to the router is automaticly provided as open api provided by grown.
We use swagger.ui as description which can be used standalone.
For useing just explore the given link in the ui
Example::

    http:\\myiotdevice\swagger.json

This way after adding all controls you have a good base to develop further views or test
the given params.

data control
============
This module to log data overtime from your sensors. Enable logging is prety simple write a
function which returns a dict with key as name and value.
Those function is called overtime and will be logged.

Example::

    from grown.data_control import add_data_control

    async def mydata():
        return {
            "water": 0,
            "light": 0,
        }

    add_data_control(router, mydata)

light control
=============
Every plant needs light so we need to control these by a timetable.
We need at least 2 functions one to activate and one to deactivate the light.

Example::

    from grown.light_control import add_light_control

    async def activate():
        print("activate")

    async def deactivate():
        print("deactivate")

    add_light_control(router, activate, deactivate)


logging
=======
if you want to add something to the log because you write your own task and so on.
Example::

    from grown.logging import grown_log

    grown_log.info('new entry')

its a ulogging instance from the logger with an add that it logs data not only to console
but also to the file run_information.log.
This might get handy in debugging log term bugs.

store
=====
Another interal element is the store. It´s a minimal redux which also stores
every update to the filesystem.

Example::

    from grown.store import storage

    def _update_reducer(store_dict, data):
        return store_dict.update(data)

    storage.register_leaf(
            'mydata',
            {
            },
            _update_reducer
        )


    leaf = storeage.get_leaf('mydata')

    leaf.update({'new_data': 3.0})

    print(leaf.get())

