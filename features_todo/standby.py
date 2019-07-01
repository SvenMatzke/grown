
def load_standby_settings():
    dict(
        reads_without_send=18,
        deepsleep_s=600,  # 10 minutes
        keep_alive_time_s=10,
        max_awake_time_s=30,  # 120 seconds after sending first request data.
        awake_time_for_config=180,  # 3 minutes
        request_url=None,
        added_infos_to_sensor_data=dict(),  # this dict adds additional information for the posted sensor_data
    )

    # reads
    reads_without_send = new_config.get('reads_without_send', old_config.get("reads_without_send", 18))
    if reads_without_send < 1:
        new_config['reads_without_send'] = 1

    # Deepsleep
    deepsleep_s = new_config.get('deepsleep_s', old_config.get('deepsleep_s', 600))
    if deepsleep_s <= 0:  # No Deepsleep
        new_config['deepsleep_s'] = deepsleep_s
    if deepsleep_s >= 3600:  # more only every hour seems odd
        new_config['deepsleep_s'] = 3600

    # timer if connected to a network
    # reset time till max_awake_time_s
    keep_alive_time_s = new_config.get('keep_alive_time_s', old_config.get('keep_alive_time_s', 30))
    max_awake_time_s = new_config.get('max_awake_time_s', old_config.get('max_awake_time_s', 120))
    if max_awake_time_s < keep_alive_time_s:
        keep_alive_time_s = max_awake_time_s
    new_config['keep_alive_time_s'] = keep_alive_time_s
    new_config['max_awake_time_s'] = max_awake_time_s

    # timer if connecting to a network failed
    awake_time_for_config = new_config.get('awake_time_for_config', old_config.get('awake_time_for_config', 180))
    if awake_time_for_config <= 60:
        awake_time_for_config = 60
    new_config['awake_time_for_config'] = awake_time_for_config

    # request and additional information
    if new_config.get('added_infos_to_sensor_data', None) is None:
        new_config['added_infos_to_sensor_data'] = old_config.get('added_infos_to_sensor_data', dict())

    if new_config.get('request_url', None) is None:
        new_config['request_url'] = old_config.get('request_url', None)


import machine

rtc = machine.RTC()


def set_awake_time_and_put_to_deepsleep(time_in_s):
    # configure RTC.ALARM0 to be able to wake the device
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    # set RTC.ALARM0 to fire after 10 seconds (waking the device)
    rtc.alarm(rtc.ALARM0, time_in_s * 1000)

    # put the device to sleep
    machine.deepsleep()
