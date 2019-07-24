import network
import time

from userv import swagger
from .store import storage
from .logging import grown_log
from userv.routing import json_response, text_response
try:
    import ujson as json
except ImportError:
    import json

_sta_if = network.WLAN(network.STA_IF)
_ap_if = network.WLAN(network.AP_IF)


def _connect_to_existing_network(essid, password):
    if essid is None or password is None:
        grown_log.info('essid or password is not set')
        return False

    grown_log.info('connecting to network...')
    _sta_if.active(True)

    _sta_if.connect(essid, password)
    start_time = time.time()
    grown_log.info("connecting")
    while not _sta_if.isconnected() and start_time + 10 >= time.time():
        print(".")
        time.sleep(1)
    if not _sta_if.isconnected():
        _sta_if.active(False)
        grown_log.info('Connection NOT establisched')
        return False
    else:
        grown_log.info('network config: %s' % str(_sta_if.ifconfig()))
    return True


def _create_an_network():
    _ap_if.active(True)
    essid = "MyPlantMonitor"
    password = "MyPlantMonitor"
    _ap_if.config(essid=essid, password=password, authmode=4)
    grown_log.info('essid: %s  pw: %s' % (essid, password))


def _update_wlan_data(old_data, new_data):
    """
    :type old_data: dict
    :type new_data: dict
    :rtype: dict
    """
    old_data.update(new_data)
    return old_data


@swagger.info("gets current wlan configuration")
def _get_wlan_config(request):
    # we should not transmit the password
    wlan_config = storage.get_leaf('wlan').get()
    wlan_config['password'] = "*" * len(wlan_config['password'])
    return json_response(wlan_config)


@swagger.info("sets wlan configuration")
@swagger.body('WlanConfiguration',
              summary="Wlan  configuration",
              example={
                  'ssid': "",
                  'password': "",
              })
def _post_wlan_config(request):
    leaf = storage.get_leaf('wlan')
    try:
        new_wlan_config = json.loads(request.get('body', ""))
        leaf.update(new_wlan_config)
        return json_response(new_wlan_config)
    except Exception as e:
        return text_response(str(e), status=400)


def connect_and_configure_wlan(router):
    """
    configures and starts wlan server.
    Also adds routes to server
    :type router: userv.routing.Router
    """
    # connect
    storage.register_leaf(
        'wlan',
        dict(
            ssid=None,
            password=None,
        ),
        _update_wlan_data
    )

    wlan_config = storage.get_leaf('wlan')

    grown_log.info("connect existing network")
    network_connected = _connect_to_existing_network(
        essid=wlan_config.get('ssid'),
        password=wlan_config.get('password'),
    )
    if not network_connected:
        grown_log.info("Create hotspot")
        _create_an_network()

    #
    router.add("/setting/wlan", _get_wlan_config, method="GET")
    router.add("/setting/wlan", _post_wlan_config, method="POST")
