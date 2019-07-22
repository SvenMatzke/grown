from grown.light_control import _should_light_be_enabled

def seconds_for_one_day(time_s):
    """
    strips away all seconds not in one day
    :param time_s:
    :return:
    """
    return time_s % (60 * 60 * 24)

# TODO import
def test_on_time_over_24_oclock_currenttime_on_time():
    on_time = 18*3600
    off_time = 11*3600
    current_time1 = 23*3600
    current_time2 = 6*3600

    assert _should_light_be_enabled(on_time, off_time, current_time1) is True
    assert _should_light_be_enabled(on_time, off_time, current_time2) is True


def test_on_time_over_24_oclock_currenttime_off_time():
    on_time = 18 * 3600
    off_time = 11 * 3600
    current_time1 = 15 * 3600

    assert _should_light_be_enabled(on_time, off_time, current_time1) is False


def test_off_time_over_24_oclock_currenttime_on_time():
    on_time = 11 * 3600
    off_time = 18 * 3600
    current_time1 = 15 * 3600

    assert _should_light_be_enabled(on_time, off_time, current_time1) is True


def test_off_time_over_24_oclock_currenttime_off_time():
    on_time = 11 * 3600
    off_time = 18 * 3600
    current_time1 = 23 * 3600
    current_time2 = 6 * 3600

    assert _should_light_be_enabled(on_time, off_time, current_time1) is False
    assert _should_light_be_enabled(on_time, off_time, current_time2) is False


