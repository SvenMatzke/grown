import network
import time
from .store import storage

_sta_if = network.WLAN(network.STA_IF)
_ap_if = network.WLAN(network.AP_IF)


def _connect_to_existing_network(essid, password):
    if essid is None or password is None:
        print('essid or password is not set')
        return False

    print('connecting to network...')
    _sta_if.active(True)

    _sta_if.connect(essid, password)
    start_time = time.time()
    print("connecting")
    while not _sta_if.isconnected() and start_time + 10 >= time.time():
        print(".")
        time.sleep(1)
    if not _sta_if.isconnected():
        _sta_if.active(False)
        print('Connection NOT establisched')
        return False
    else:
        print('network config:', _sta_if.ifconfig())
    return True


def _create_an_network():
    _ap_if.active(True)
    essid = "MyPlantMonitor"
    password = "MyPlantMonitor"
    _ap_if.config(essid=essid, password=password, authmode=4)
    print('essid: ', essid, ', pw: ', password)


def connect_and_configure_wlan(grown_server):
    """
    configures and starts wlan server.
    Also adds routes to server
    :type grown_server: grown.server.GrownWebServer
    """
    # connect
    storage.register_leaf(
        'wlan',
        dict(
            ssid=None,
            password=None,
        )
    )

    wlan_config = storage.get_leaf('wlan')

    print("connect existing network")
    network_connected = _connect_to_existing_network(
        essid=wlan_config.get('ssid'),
        password=wlan_config.get('password'),
    )
    if not network_connected:
        print("Create hotspot")
        _create_an_network()

    # TODO add urls for configuration
