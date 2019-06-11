try:
    import ujson as json
except ImportError:
    import json
try:
    import uasyncio as asyncio
except ImportError:
    import asyncio
import ulogging as logging

#


# TODO streamreader


async def text(text, status=200):
    raise


async def json(writer, data, status=200):
    """
    converts input into json and returns a response function
    :param data:
    """
    raise


class GrownWebServer():

    def __init__(self):
        self._routes = []

    def add_route(self, route, function, method="GET"):
        """

        :type route: str
        :param function: function
        :type method: str
        :param method: GET, POST, DELETE, UPDATE
        """
        self._routes.append(
            (route, function, method)
        )

    def run(self):
        logging.basicConfig(level=logging.INFO)
        picoweb_server = picoweb.WebApp(__name__)
        picoweb_server.run()


#
# def create_main_app(get_sensor_data):
#     """
#
#     :rtype: picoweb.WebApp
#     """
#
#     async def _get_data(writer, request):
#         sens_data = await get_sensor_data
#         return picoweb.jsonify(writer, sens_data)
#
#     # async def _history_data(writer, request):
#     #     global last_request_time
#     #     last_request_time = time.time()
#     #
#     #     content_len = 0
#     #     if sensor.history_sensor_data_file in os.listdir():
#     #         content_len = os.stat(sensor.history_sensor_data_file)[6]
#     #
#     #     writer.write(
#     #         userv.utils._response_header(
#     #             status=200,
#     #             content_type="application/json",
#     #             content_length=content_len + 2 - 1  # +2 braces -1 tailoring \n
#     #         )
#     #     )
#     #     writer.write("[")
#     #     if content_len > 0:
#     #         file_ptr = open(sensor.history_sensor_data_file, "r")
#     #         read = ""
#     #         while True:
#     #             last_read = read
#     #             read = file_ptr.readline().replace("\n", "")
#     #             if read == "":
#     #                 break
#     #             else:
#     #                 if last_read != "":
#     #                     writer.write(",")
#     #                 writer.write(read)
#     #             gc.collect()
#     #
#     #         file_ptr.close()
#     #
#     #     writer.write("]")
#     #     return True
#
#     def _get_settings(writer, request):
#         return picoweb.jsonify(writer, settings.get_settings())
#
#     def _post_settings(writer, request):
#         try:
#             new_settings = json.loads(request.get('body'))
#         except Exception as e:
#             error.add_error(json.dumps({'time': time.time(), 'error': str(e)}))
#             return picoweb.jsonify(writer, {"message": "Request had no valid json body."}, status=406)
#         updated_settings = settings.save_settings(settings.get_settings(), new_settings)
#         return userv.socketserver.json(writer, updated_settings)
#
#     # routes
#     routes = [
#         ("/rest/settings", _get_settings, 'GET'),
#         ("/rest/settings", _post_settings, 'POST'),
#         # ("/rest/sensor_history", _history_data, method='GET'),
#         ("/rest/data", _get_data, 'GET')
#     ]
#
#     return picoweb.WebApp(__name__)
