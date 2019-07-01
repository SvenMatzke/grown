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

TODO
====

- data_control
- light_control
- time_control
- logging

description of development for tasks and therefore the store

