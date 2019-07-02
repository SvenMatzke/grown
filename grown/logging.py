import ulogging

# todo print stream support
class FileHandler(object):
    def __init__(self, filename, mode="a"):
        self.mode = mode
        self.terminator = "\n"
        self.filename = filename
        self._f = open(self.filename, self.mode)

    def write(self, output):
        self._f.write(output)
        self._f.flush()

    def flush(self):
        self._f.flush()

    def close(self):
        self._f.close()


ulogging.basicConfig(
    ulogging.DEBUG,
    'run_information.log',
    FileHandler('run_information.log')
)
grown_log = ulogging.getLogger("grown")
