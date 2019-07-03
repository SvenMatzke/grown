"""
rudimentary monkey_patch till module has fileio write
"""
import ulogging


def log(self, level, msg, *args):
    _log_file = open('run_information.log', 'a')
    _log_file.write("%s:%s: %s \n" % (self._level_str(level), self.name, msg))
    _log_file.close()
    if level >= (self.level or ulogging._level):
        ulogging._stream.write("%s:%s:" % (self._level_str(level), self.name))
        if not args:
            print(msg, file=ulogging._stream)
        else:
            print(msg % args, file=ulogging._stream)


ulogging.Logger.log = log


ulogging.basicConfig(
    ulogging.DEBUG,
)
grown_log = ulogging.getLogger("grown")
