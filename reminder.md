
#inputs

wlan_settings

standbysettings = {

}

functions:
gather_sensor_data func # return dict

# return bools
enable_light 
disable_light

start_watering
stop_watering


if standbysettings are not given we will be always online 
if no wlan_settings are given we will open a wlan

depending on functions given we enable rest features or disable them
how do we connect those

# possible api

## ansich will ich keine settings machen sondern das soll man per rest einstellen
## oder bei massendeployment eine json hinterlegen

```python
import grown

async def my_gather_func():
    # to your io stuff
    return {
        'soil_moisture': 0,
        'light': 0,
    }

#various control tasks
grown_server = grown.setup(my_gather_func)

# i need a smart way to comunicate sensor data
sub_grown_server = grown.add_light_control(
        get_light_sensor_data,
        enable_light,
        disable_light,
        safety_function=optional_func,
    )

grown_server = grown.add_watering_control(
    get_water_sensor_data,
    start_watering,
    stop_watering,
    safety_function=optional_func,
)
```


## here custom adds can be done easily
the run will have serveral tasks added already for watering light gathering periodic data and a restful server to view

server.run()

